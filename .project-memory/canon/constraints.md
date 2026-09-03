---
project: living-literature
kind: constraints
---

# Constraints

## Product and Language
- The mission is to lead viewers toward reading, not maximize generated volume.
- Project-facing text is English. Original literary quotations are exempt; metadata, explanation, and translation are English.
- Evaluate rights separately for the work, edition, translation, recording, and visual assets.
- Human editorial and legal review is required before publication.

## Local Inference
- All AI inference must run locally on Apple Silicon.
- No inference path may require an API key or cloud text, prompt, TTS, image, or video service.
- Treat source/dependency download, weight download, and inference as separate operations.
- Pin model and dependency revisions. Keep weights, caches, generated media, and secrets local and Git-ignored.
- Help proves readiness, not generation or offline inference. `Wan2.1-T2V-1.3B` is a candidate, not an accepted model.

## Scope Control
- Work one bounded slice at a time.
- Model download and inference require a slice that names the exact model, revision, file set, benchmark, and safety boundary.
- Slice 003 is a decision gate and does not authorize a heavier-model download or inference.
- Do not optimize before a measured baseline.
- Do not publish automatically.

## Process
- Keep PRs narrow and reviewable.
- Claim only verification that ran; treat review findings as gates.
- Keep controller decisions out of worker execution unless the accepted plan includes them.
- Agents are useful because their authority is limited.

## Memory Core
- Keep repo canon short, current, and non-discoverable.
- Active state lives only in `current-state.md`; executable verification lives only in `verify-commands.md`.
- Distilled knowledge requires an explicit lifecycle status.
- Promotion is a separate act from extraction.
- Encode rules as scripts or gates where practical.
- Do not duplicate active state outside repo project memory.

## Ownership
- Root bootstrap stays minimal and points into `/.project-memory/`.
- Repo canon wins over Obsidian summaries when they disagree.
- Worker output becomes durable memory only through explicit promotion.
