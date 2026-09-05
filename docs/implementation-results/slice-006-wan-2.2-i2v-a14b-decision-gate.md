---
task_id: slice-006-wan-2.2-i2v-a14b-decision-gate
task_type: investigation
status: complete
branch: feature/slice-006-wan-2-2-i2v-decision-gate
date: 2026-09-04
write_scope:
  - docs/slice-006-wan-2.2-i2v-a14b-decision-gate.md
  - manifests/decisions/slice-006-wan-2.2-i2v-a14b.json
  - scripts/verify-slice-006.py
  - docs/implementation-results/slice-006-wan-2.2-i2v-a14b-decision-gate.md
  - .project-memory/canon/current-state.md
  - .project-memory/verify-commands.md
  - .project-memory/docs-index.md
  - generated project-local Memory Core workspace artifacts
  - Git-ignored Slice 006 source-still candidates and contact sheet
forbidden_moves:
  - runtime installation or model-weight download
  - model-package preparation or inference
  - generated or externally sourced replacement image
  - cloud inference, API key, publication, or parallel inference
  - historical Slice 002 or Slice 005 evidence changes
  - model-cache, Ollama, Obsidian, or automatic Memory Core promotion changes
verification_surface:
  - exact model, runtime, package, revision, license, inventory, and parameter consistency
  - reopened LTX-2.5 comparison and corrected disposition
  - source-video identity, media properties, and still provenance
  - frozen prompts, scout/full/offline sequence, and safety thresholds
  - historical deterministic verifiers and repository safety checks
  - strict project-local Memory Core audit
success_criteria:
  - select one future benchmark candidate and pin one exact owner-approved source still without download or inference
slice_restrictions:
  - Slice 004 remains postponed
  - Wan2.2 I2V-A14B is a benchmark candidate, not a production model
  - Slice 007 requires a separate owner-approved plan
---

# Implementation Result

## Outcome

Slice 006 is complete. The reopened comparison retains Wan2.2 I2V-A14B BF16 through pinned MLX-Gen 0.33.1 as the single future motion-scout candidate. LTX-2.5 Fast is corrected from “API-only on macOS” to a viable local Apple Silicon MPS alternative and is deferred to a separate license and runtime-evidence gate.

The owner selected candidate D, the left image in the second row. Its exact local, Git-ignored provenance is pinned without committing the image. Slice 007 remains subject to a separate owner-approved implementation plan.

## Work Performed

- Verified the clean `main` baseline at `3411dcacd9aebbc43ec2fc2632c747c139cda8ed` against live `origin/main` before branching.
- Confirmed that no Wan, MLX-Gen, or LTX inference process was running.
- Classified the work as a controller-led investigation and decision gate.
- Created `feature/slice-006-wan-2-2-i2v-decision-gate`.
- Rechecked pinned Wan, MLX-Gen, PyPI, prepared-package, LTX, HunyuanVideo, and Mochi primary metadata on 2026-09-04.
- Verified the official Wan model revision, Apache-2.0 task metadata, and 50-file/126,204,155,463-byte source inventory.
- Verified MLX-Gen 0.33.1 source commit, MIT license, wheel hash, I2V parameter behavior, source-aspect canvas behavior, local-file boundary, and Wan q8-to-BF16 runtime correction.
- Verified the prepared BF16 package revision and exact 44-file/68,791,046,058-byte inventory.
- Reopened the LTX-2.5 comparison and recorded its gated model revision, custom license hash, exact repository inventory, five-file local subset, current Apple Silicon MPS runtime revisions, and remaining evidence gaps.
- Re-hashed and probed both Slice 005 outputs, confirming their recorded byte identity and media properties.
- Extracted six 832×480 candidate stills and a 3×2 contact sheet under the ignored `outputs/slice-006/` boundary.
- Added a deterministic Slice 006 verifier with a bounded pending-selection mode and a strict final mode.
- Recorded the owner selection and completed the strict verification and review-closeout cycle.

## Selected Source Still

- Candidate: D, the left image in the second row.
- Local path: `outputs/slice-006/source-still-candidates/candidate-d-frame-048.png`.
- SHA-256: `7e7f0a20ebaa62551cad700d7e17fecd0fdc68a7003c9e1eb2e846f7fd6ec0c7`.
- Dimensions: 832×480.
- Source frame: zero-based frame 48 at `00:00:03.000`.
- Source-video SHA-256: `ce7a61c21ef0811062ea6229b3ddf89c6843bdc6569234cab060915bd39f2ad4`.
- Storage boundary: local and Git-ignored; not committed.

## Verification

- `command:` `.venv/bin/python scripts/verify-slice-006.py`
  - `result:` pass in complete state
  - `notes:` identifiers, revisions, inventories, prompts, comparison dispositions, scout/full/offline parameters, resource thresholds, source-video hashes, exact candidate-D provenance, ignore rules, and Git artifact boundaries are consistent.
- `command:` `.venv/bin/python scripts/verify-slice-002.py`
  - `result:` pass
- `command:` `.venv/bin/python scripts/verify-slice-005.py`
  - `result:` pass
  - `notes:` includes complete output decode.
- `command:` repository language, artifact, compile, diff, and Memory Core checks
  - `result:` pass
  - `notes:` Python compilation passed; the Cyrillic scan returned no matches; the generated-media and weight scan found only the four expected ignored Slice 002/005 MP4s; no weight files or tracked weight/video artifacts were found; `git diff --check` passed; the strict project-local audit reported zero findings.

## Review and Closeout

The pending-state review found one context-hygiene issue: the first interim `current-state.md` update exceeded the always-on context limit. The state entry was compressed without removing the selected route, corrected LTX disposition, or slice boundaries; the repeated strict audit passed with zero findings.

The final review found that the verifier initially accepted any candidate copied consistently into the selected object rather than enforcing the owner’s exact choice. The verifier now pins candidate D, its path, hash, frame, timecode, selection wording, source hash, and local-only storage boundary. The strict verifier and all applicable repository checks pass after the correction. The Memory Core closeout completed in non-apply mode with zero promotions, and the repeated project-local audit reported zero findings. No runtime installation, weight download, inference, cloud service, API key, parallel inference, publication, or Memory Core promotion occurred.
