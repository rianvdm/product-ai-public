---
title: Antiphon — mood library (template)
---

# Moods

A living library of mood / context buckets and the picks validated
against them. When the assistant offers a pick for a mood and the user
keeps it, move it from **candidates** to **validated**. When the user
rejects it, move it to **dismissed** with a one-line reason.

Add new buckets freely. Buckets should be evocative ("small hours",
"long drive", "deep work") rather than genre labels.

The three-state shape below is the whole pattern: **validated** picks
that landed, **candidates** the assistant has proposed but you haven't
confirmed, and **dismissed** picks with a reason so the same miss isn't
suggested twice. Cite a specific signal on every candidate (play count,
rank, a similar-artist link) so nothing is a vibes-only guess.

---

## deep work (example bucket)

*One-line description of the mood: what it's for, the tempo/texture,
and — importantly — what it is **not**, so neighbouring buckets stay
distinct.*

### Validated
- _Artist — Album/Track — the signal that made it land (e.g. "sits next
  to your #1 played artist in this lane")_

### Candidates
- _Artist — Album/Track — the signal that suggested it (e.g. "Last.fm
  #1-similar to your anchor artist; 3 plays in your history")_

### Dismissed
- _Artist — Album/Track — one-line reason it didn't fit (e.g. "too
  upbeat; this bucket needs more atmosphere than song")_

---

<!-- Add new buckets below using the same shape -->
