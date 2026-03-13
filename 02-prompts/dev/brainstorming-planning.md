# Project brainstorming and spec creation

Build ideas from scratch through guided discovery, then produce developer-ready specs and implementation prompts.

---

## When to Use

- Starting a new side project from a rough idea
- Need structured thinking before jumping into code
- Want implementation prompts for a code-generation LLM

---

## Phase 1: Idea Brainstorming

We're going to flesh out an idea together. Ask me ~20-25 questions, one at a time, building on your answers until we have enough detail for a solid specification.

You must:
- Challenge assumptions to ensure the idea meets real user needs
- Dig into edge cases and potential issues
- Keep going until we've covered all relevant aspects
- We are going to build on the Cloudflare platform, so consider what services are available and how they can be used
- Remember: ask one question at a time

Paste your idea below:

---IDEA---

---

## Phase 2: Create Spec

Compile our brainstorming into a comprehensive, developer-ready specification using a modern serverless/edge platform where viable.

**Output Structure:**
1. **Overview** — Problem, solution, target users
2. **Requirements** — Functional and non-functional
3. **Architecture** — Components, data flow, Cloud services used
4. **Data Model** — Schemas, storage (key-value store, database, object storage, etc.)
5. **API Design** — Endpoints, request/response formats
6. **Security** — Authentication, authorization, and cost protection
7. **Error Handling** — Failure modes and recovery strategies
8. **Testing Plan** — Unit, integration, and edge case coverage. CRITICAL: we will use a red/green TDD approach

**Security Section Must Include:**
- Routes that trigger paid API calls (OpenAI, etc.) and their protection strategy
- Authentication requirements per route (public vs. authenticated)
- Fail-closed vs. fail-open behavior for auth middleware
- Rate limiting strategy to prevent abuse
- Any debug/development routes and their production disposition

Write this to a .md file in the /05-personal/plans folder

---

## Phase 3: Create Prompt Plan

Turn the spec into a series of implementation prompts for a code-generation LLM.

**Process:**
1. Draft a step-by-step implementation blueprint
2. Break into small, iterative chunks that build on each other
3. Review and re-chunk until steps are right-sized:
   - Small enough for safe implementation with strong testing
   - Large enough to make meaningful progress
4. Generate a prompt for each step

**Prompt Requirements:**
- Each prompt builds on previous work
- No orphaned code — everything integrates immediately
- Prioritize: performance, best practices, early testing
- No large complexity jumps between steps

**Output Format:**
Each prompt in a fenced code block, with brief context above explaining what it accomplishes.

Create a new .md file in the same directory as the spec. Name it `prompt-plan.md`.

Spec:

---INSERT SPEC---

---

## Phase 4: Create To Do List

Generate `todo.md` — a markdown checklist covering the full project (spec + prompt plan). Be thorough.

## Phase 5: Write AGENTS.md

Now write a `AGENTS.md` that Opencode can use for development. Do a web search about what a good AGENTS.md looks like and follow those guidelines.

Make sure to include:

* The Cloudflare skills that should be loaded for each session
* The MCP servers available

As well as these instructions for how we will approach each coding session:

1. Read `spec.md`, `prompt-plan.md` and `todo.md` in the `docs` folder. Identify any prompts / items not marked as completed.
2. For each incomplete prompt:
    - Double-check if it's truly unfinished (if uncertain, ask for clarification).
    - If you confirm it's already done, skip it.
    - Otherwise, implement it as described. Before starting implementation, provide an ELI5 explanation of what you're about to do.
    - Make sure the tests pass, and the program builds/runs.
    - Update `todo.md` to mark this task as completed.
    - Commit the changes to the repository with a clear commit message.
3. After you finish each prompt, explain what you did and what should now be possible. If I am able to manually test the latest change myself to make sure it works, give me instructions on how I can do that.
4. Pause and wait for user review or feedback.
5. Repeat with the next unfinished prompt as directed by the user.