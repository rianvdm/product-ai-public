# Avoid AI Visual Patterns

*Last updated: 2026-09-04*

This file covers visual composition in authored HTML explainers and rendered screenshots. It complements `01-context/avoid-ai-patterns.md`, which remains focused on words and phrases. This is a judgment guide, not a component blacklist. An isolated match is a reason to inspect the page, not proof that the page is wrong.

## Positive contract

- Compose each scene around the subject's actual objects and relationships.
- Use whitespace, scale, alignment, colour fields, and hairline rules to create hierarchy.
- Keep explanatory content visible when it arrives on screen.
- Repeat a component only when the subject contains repeated peer objects.
- Let motion explain change, direction, sequence, timing, or cause and effect.

## Evidenced tells

### Interchangeable rounded-card grids

A collection of interchangeable rounded content cards, especially white cards with coloured accent stripes, is a visual AI tell when it supplies the page's default structure rather than depicting real peer objects in the subject.

Ask what each card represents and what relationship the arrangement shows. If the answer is only “each card contains a section of content,” replace the grid with a composition that explains the subject: its objects, their relationships, a change over time, a scale, or a sequence.

### Scroll-triggered reveals

Fade, slide, or reveal effects that hide explanatory content until the reader scrolls to it are a visual AI tell. Content should be understandable when it arrives on screen. Motion may show a meaningful process, but it must not gate text, figures, or scenes.

## Semantic versus decorative

Judge the treatment in context. Rounded shapes, shadows, gradients, glows, and colour accents are not failures by themselves. They can depict real rooms, agents, boundaries, objects, or states. The question is whether the treatment makes the adjacent claim easier to understand or merely supplies a fashionable surface.

A CSS property cannot determine intent. The screenshot, the scene claim, and the relationship between the visual and the subject decide the finding.

Reviewers may report nearby symptoms, such as a grid of decorative icons replacing a real diagram or every scene repeating the same composition. Do not turn one observed symptom into a universal ban without evidence that it recurs.

## Review rule

Read this file before reviewing a visual page. Inspect desktop and phone captures, and the reduced-motion capture when motion exists. Record every finding with a scope (`page` or one or more scene IDs), the evidence, and a keep-or-fix decision. A semantic rounded object is report-only; it is not an automatic failure.
