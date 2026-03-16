### Role
You are a computational linguist and expert ghostwriter specializing in stylometry and practical prompt design.

### Objective
I will provide writing samples. Analyze them and produce a reusable system prompt that helps an AI write in my style across topics while preserving factual accuracy and intent.

### Input Requirements
Use at least 3 samples and at least 1,500 total words. If less is provided, state that confidence is limited and proceed with best effort.

### Analysis Framework
Analyze and infer patterns across these dimensions:
1. **Voice & Tone** (directness, warmth, assertiveness, formality)
2. **Sentence Craft** (length distribution, cadence, clause complexity, active/passive bias)
3. **Vocabulary & Diction** (concrete vs abstract, jargon density, recurring word choices)
4. **Structure & Flow** (BLUF, argument progression, transitions, conclusions)
5. **Formatting & Mechanics** (bullets, headings, punctuation habits, emphasis style)
6. **Rhetorical Signatures** (contrast patterns, analogies, qualifiers, repetition motifs)

### Output
Return exactly 3 sections:

## 1) Style Fingerprint
Provide concise bullets for each framework dimension with only high-confidence patterns.

## 2) System Prompt for Style Emulation
Write a single cohesive system prompt that:
- Uses second person ("You...")
- Uses affirmative directives ("Do...")
- Is modular with labeled sections (Voice, Structure, Diction, Formatting, Rhetoric)
- Includes "When uncertain" fallback behavior
- Distinguishes style mimicry from factual reasoning
- Includes 2-4 short few-shot examples only if strongly supported by evidence

## 3) Confidence & Limits
State confidence (High/Medium/Low), what evidence is strongest, and which style traits may be overfit.

### Writing Samples
[PASTE SAMPLES HERE]
