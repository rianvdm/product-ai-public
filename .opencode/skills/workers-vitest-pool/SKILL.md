---
name: workers-vitest-pool
description: Set up or upgrade vitest tests for Cloudflare Workers using @cloudflare/vitest-pool-workers. Use when scaffolding tests in a new Worker, when an existing Worker is on pool-workers <0.13 (vitest 2/3) and needs to upgrade, or when the test suite hits "Isolated storage failed" / "Expected .sqlite, got .sqlite-shm" errors. Pins the modern stack (vitest 4 + pool-workers ≥0.15 + Node 22) and documents the v2→v4 migration recipe.
---

# Workers vitest pool: known-good setup + v2→v4 upgrade recipe

Amazon's `@cloudflare/vitest-pool-workers` had a long-lived bug in the `0.5.x` line where the per-test storage isolation snapshot asserts every persist file ends in `.sqlite`, but SQLite-backed Durable Objects in WAL mode produce `.sqlite-shm` and `.sqlite-wal` files alongside. The bug manifests as:

```
Failed to pop isolated storage stack frame in <test name>'s test "<...>".
In particular, we were unable to pop Durable Objects storage.
- AssertionError [ERR_ASSERTION]: Expected .sqlite, got .../foo.sqlite-shm
```

Upstream fix landed in **`@cloudflare/vitest-pool-workers@0.13`**, which requires **vitest 4** and **Node 22+**. This skill captures the canonical setup and the migration recipe — battle-tested in `tldl` (PR #39, 2026-05-02).

## When to use this skill

- **Scaffolding tests in a new Worker.** Use the "Known-good setup" section to pin the modern stack from day one.
- **An existing Worker is on pool-workers `0.5.x` / `0.6.x` / `0.7.x` / `0.8.x` / `0.9.x` / `0.10.x` / `0.11.x` / `0.12.x`.** Even if tests appear to pass, the bug is latent — any test that uses a SQLite-backed Durable Object will hit it eventually. Run the migration.
- **Tests are reporting "Isolated storage failed" or "Expected .sqlite, got .sqlite-shm".** That is exactly this bug.

## Known-good setup (use this for new projects)

```jsonc
// package.json — devDependencies
{
  "@cloudflare/vitest-pool-workers": "^0.15",
  "@cloudflare/workers-types": "^4",
  "@types/node": "^22",
  "typescript": "^5",
  "vitest": "^4",
  "wrangler": "^4"
}
```

```jsonc
// tsconfig.json — types entry
{
  "compilerOptions": {
    "types": [
      "@cloudflare/workers-types",
      "@cloudflare/vitest-pool-workers/types",  // ← /types subpath, not bare
      "node"
    ]
  }
}
```

```ts
// vitest.config.ts — v4 shape
import { cloudflareTest, readD1Migrations } from "@cloudflare/vitest-pool-workers";
import { defineConfig } from "vitest/config";
import path from "node:path";

const migrations = await readD1Migrations(path.join(import.meta.dirname, "migrations"));

export default defineConfig({
    plugins: [
        cloudflareTest({
            wrangler: { configPath: "./wrangler.toml" },
            miniflare: {
                bindings: {
                    // test-only env vars + secret stand-ins
                },
            },
        }),
    ],
    test: {
        provide: { DB_MIGRATIONS: migrations },
    },
});
```

```text
// .nvmrc
22
```

```yaml
# .github/workflows/ci.yml
name: CI
on:
  push:
    branches: [main]
  pull_request:
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: 22
          cache: npm
      - run: npm ci
      - run: npm run typecheck
      - run: npm test
```

## Per-test storage isolation: don't rely on it

With the known-good `cloudflareTest` config above, D1 / KV / R2 state is **NOT reset between `it()` blocks** — it persists across every test in a file (storage behaves as per-file, not per-test). The package's "isolated storage" reliably covers only Durable Objects; relational / KV / R2 writes accumulate.

So tests must not depend on a clean slate. Either:

- **Use unique identifiers per test** — emails, display names, codes, any natural key randomised per `it()` (e.g. `t-${Math.random()}@x.test`). A test that signs up a fixed `t-fixed@x.test` makes every later test in the file that reuses it fail with an unexpected `409`.
- **Or add a `beforeEach` reset** when tests genuinely need an empty DB — truncate the D1 tables in FK-safe (child→parent) order, then drain the KV namespace and R2 bucket by paginating `list()` + `delete()`.

Symptom when this bites: the *first* test in a `describe` passes and every later one fails — typically a `409`/`401` where a `2xx`/`403` was expected, because a fixed-identity signup now collides with a row a prior test left behind. Discovered 2026-05-19 on the Therapy Space backend: a 22-test security-sweep file with fixed identifiers had 12 failures until a `beforeEach` reset was added.

## Migration recipe (vitest 2 + pool-workers 0.5 → vitest 4 + pool-workers 0.15)

Apply these in one branch. Order matters — config first, then types, then test casts, then latent bugs.

### 1. Bump devDependencies

```bash
npm install -D vitest@^4 @cloudflare/vitest-pool-workers@^0.15 @types/node
echo 22 > .nvmrc
```

Pool-workers 0.15+ requires **vitest ^4.1** and **Node ≥22**. There is no in-between version that fixes the bug while staying on vitest 2 — the assertion was removed in `0.13`, which already requires vitest 4.

### 2. Migrate `vitest.config.ts`

`defineWorkersConfig` from `@cloudflare/vitest-pool-workers/config` was removed. The new shape uses the standard `defineConfig` from `vitest/config` with `cloudflareTest` as a plugin. Move whatever was in `test.poolOptions.workers` into the plugin call:

```diff
-import { defineWorkersConfig, readD1Migrations } from "@cloudflare/vitest-pool-workers/config";
+import { cloudflareTest, readD1Migrations } from "@cloudflare/vitest-pool-workers";
+import { defineConfig } from "vitest/config";
 import path from "node:path";

 const migrations = await readD1Migrations(path.join(import.meta.dirname, "migrations"));

-export default defineWorkersConfig({
+export default defineConfig({
+    plugins: [
+        cloudflareTest({
+            wrangler: { configPath: "./wrangler.toml" },
+            miniflare: { bindings: { /* ... */ } },
+        }),
+    ],
     test: {
-        poolOptions: {
-            workers: {
-                wrangler: { configPath: "./wrangler.toml" },
-                miniflare: { bindings: { /* ... */ } },
-            },
-        },
         provide: { DB_MIGRATIONS: migrations },
     },
 });
```

There is also a codemod available if your config is more complex:
`npx jscodeshift -t node_modules/@cloudflare/vitest-pool-workers/dist/codemods/vitest-v3-to-v4.mjs vitest.config.ts`

### 3. Update `tsconfig.json`

Two changes:

- `"@cloudflare/vitest-pool-workers"` → `"@cloudflare/vitest-pool-workers/types"`. The new package no longer exports test types from the bare entry — they moved to a `/types` subpath.
- Add `"node"` to surface `Error.captureStackTrace`, `node:crypto`, and other Node-shimmed globals you previously got transitively.

```diff
 "types": [
   "@cloudflare/workers-types",
-  "@cloudflare/vitest-pool-workers"
+  "@cloudflare/vitest-pool-workers/types",
+  "node"
 ],
```

### 4. Loosen `as Env` casts in test helpers

`@cloudflare/workers-types` v4 made `DurableObjectNamespace<T>` stricter: `T` must extend `Rpc.DurableObjectBranded`. The auto-generated `worker-configuration.d.ts` has the precise generic, but a hand-written `Env` in `src/types/index.ts` typically declares `JOB_STATUS: DurableObjectNamespace` (no generic = `<undefined>`). The two no longer satisfy each other.

Test fixtures that do `{ ...env, OPENAI_API_KEY: "..." } as Env` will fail with:

> Conversion of type ... to type 'Env' may be a mistake because neither type sufficiently overlaps with the other. If this was intentional, convert the expression to 'unknown' first.

**Fix:** widen every test cast to `as unknown as Env`. The `unknown` middle step bypasses TS's overlap check. The `Env` you cast to is the hand-written one, so its DO generic stays loose.

```diff
-} as Env;
+} as unknown as Env;
```

If your DO class still uses `implements DurableObject` (the older interface), keep `JOB_STATUS: DurableObjectNamespace` (no generic) in your hand-written `Env`. Don't try to parameterize it — the class won't satisfy `Rpc.DurableObjectBranded` without inheriting from a base class. The auto-generated worker-configuration.d.ts already has the precise type for runtime checks; the hand-written one is only for app code that needs an explicit shape.

### 5. Loosen `MessageBatch<T>` mock casts

Same generic-strictness story for `MessageBatch`. The `metadata` field is now required:

```diff
-return {
-    messages: mockMessages,
-    queue: "test-queue",
-    ackAll: vi.fn(),
-    retryAll: vi.fn(),
-};
+return {
+    messages: mockMessages,
+    queue: "test-queue",
+    ackAll: vi.fn(),
+    retryAll: vi.fn(),
+} as unknown as MessageBatch<QueueMessage>;
```

### 6. Reporter: drop `--reporter=basic`

Vitest 4 removed the `basic` reporter. Use the default reporter or `--reporter=default`. Update any local scripts, debug aliases, or CI invocations.

### 7. Hunt for latent bugs that the broken isolation was masking

This is the part most easily missed. Once storage isolation works correctly, tests that were passing for the wrong reason start failing for real reasons. Check each failure carefully — most are bugs in the test, not the code.

**Common pattern A: index keys not being cleaned.**

If your code maintains an index alongside per-record keys (`episodes:index` alongside `episode:<id>`), and your `clearTestData` only wipes one prefix, the index persists across tests. Under broken isolation it got reset incidentally; under working isolation it carries stale entries.

```diff
-const prefixes = ["episode:", "transcript:", "summary:"];
+const prefixes = ["episode:", "episodes:", "transcript:", "summary:"];
```

**Common pattern B: queue retry-vs-fail tests with `attempts: 1`.**

Amazon Queue consumers typically have a retry policy: `if (message.attempts >= maxAttempts) markFailed() else retry()`. Tests that assert a job becomes "failed" after an exception need `attempts >= maxAttempts` in the mock message — otherwise the consumer retries and the job stays in its pre-failure state.

```diff
 const message = createQueueMessage();
-const batch = createMockBatch([message]);
+const batch = createMockBatch([message], { attempts: 3 });

 await consumer.queue(batch, env);

-expect(batch.messages[0].retry).toHaveBeenCalled();
+expect(batch.messages[0].ack).toHaveBeenCalled();

 const updatedJob = await getJob(env.KV, job.id);
 expect(updatedJob?.status).toBe("failed");
```

These tests were exercising the retry path while asserting failed state — logically impossible. They passed under broken pool-workers because storage state ended up in weird places by accident.

**Common pattern C: response logging at WARN level.**

Vitest 4 surfaces this warning more aggressively:

> Constructing a Response with a null body status (304) and a non-null, zero-length body. This is technically incorrect.

If you see it, fix the offending `new Response("", { status: 304 })` to `new Response(null, { status: 304 })`. Doesn't fail tests, but it's noise that's easy to clean up while you're in here.

### 8. Run typecheck + tests; expect a clean exit

```bash
npm run typecheck   # exit 0
npm test            # exit 0
npm audit --omit=dev   # 0 production vulns is the bar
```

If anything still fails, the most likely culprit is step 7 (a test that was wrong before). Don't paper over it — the test was lying.

## Quick diagnostic

Repos to spot-check across an account:

```bash
for repo in ~/git/<worker-repo-1> ~/git/<worker-repo-2>; do
  printf "%-40s " "$(basename $repo)"
  jq -r '.devDependencies["@cloudflare/vitest-pool-workers"] // "—"' "$repo/package.json" 2>/dev/null
done
```

Anything `<0.15` is on the broken stack and should be migrated. Anything missing has no test setup yet — use the "Known-good setup" section.

## Provenance

Recipe distilled from the `tldl` v2→v4 upgrade — [PR #39](https://github.com/rianvdm/tldl/pull/39), 2026-05-02. Before: 462/477 passing with 3 unhandled isolation errors. After: 477/477 passing, typecheck clean, exit 0.
