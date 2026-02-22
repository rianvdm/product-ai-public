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
8. **Testing Plan** — Unit, integration, and edge case coverage

**Security Section Must Include:**
- Routes that trigger paid API calls (OpenAI, etc.) and their protection strategy
- Authentication requirements per route (public vs. authenticated)
- Fail-closed vs. fail-open behavior for auth middleware
- Rate limiting strategy to prevent abuse
- Any debug/development routes and their production disposition


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