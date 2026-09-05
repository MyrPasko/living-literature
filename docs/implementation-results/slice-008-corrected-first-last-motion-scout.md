---
task_id: slice-008-corrected-first-last-motion-scout
task_type: feature
status: technical-pass-pending-owner-motion-review
branch: feature/slice-008-corrected-first-last-motion-scout
date: 2026-09-05
write_scope:
  - Slice 008 benchmark, guarded runner, verifier, results, and documentation artifacts
  - .project-memory/canon/current-state.md
  - .project-memory/verify-commands.md
  - .project-memory/docs-index.md
  - generated project-local Memory Core workspace artifacts
  - Git-ignored Slice 008 scout output, review media, and run evidence
forbidden_moves:
  - more than one generation attempt after denoising begins
  - tuning, alternate seeds or samplers, adapters, full render, or offline duplicate
  - cloud inference, API key, publication, or parallel inference
  - model/runtime download or installation, Obsidian update, or automatic Memory Core promotion
verification_surface:
  - exact anchors, model and runtime provenance, and complete local inventories
  - immutable prompts, parameters, one-attempt marker, and safety controls
  - measured resource telemetry, output identity, media properties, full decode, and contact sheet
  - twelve owner motion hard gates, which remain pending
  - historical verifiers and repository safety checks
success_criteria:
  - execute exactly one bounded local first/last-frame scout and record its technical result for owner review
slice_restrictions:
  - Slice 004 remains postponed
  - no production video model is accepted
  - Slice 008 authorizes no additional inference
---

# Implementation Result

## Outcome

Slice 008 completed exactly one authorized Wan2.2 I2V-A14B BF16 first/last-frame inference attempt. The runner and media passed technical validation with no safety stop. Motion acceptance remains pending the owner’s twelve hard-gate verdicts. No additional inference, tuning, duplicate, or full render is authorized.

## Work Performed

- Revalidated the clean branch, required preparation and merged-baseline ancestry, absence of another model-inference process, both owner-approved 1672×940 anchors and their exact hashes, the complete 44-file model package, the pinned MLX-Gen runtime, direct `--last-image` support, and live host safety.
- Implemented and committed the guarded runner and complete-result verifier before inference at commit `2351629f06b810aad8c549957d8e8f72ee254ce2`.
- Created the durable attempt marker before launch and executed the direct Wan CLI once with the frozen positive and negative prompts, both anchors, BF16, 448×256, 41 frames, 8 fps, 15 steps, seed 42, guidance 4.0/3.0, flow shift 3.0, UniPC, low-RAM mode, prompt cache disabled, inactive-denoiser release, metadata, JSON events, no replacement, and local-files-only environment flags.
- Recorded 15-second host and process telemetry, runtime metrics, output and metadata hashes, full decode evidence, and a contact sheet from zero-based frames 0, 8, 16, 24, 32, and 40.

## Technical Result

- Run: `local-files-only-first-last-motion-scout-seed-42`.
- Generation window: 2026-09-05 11:30:14Z–11:34:01Z.
- Duration: 227 seconds wrapper time; 217.34 seconds runtime generation and save time.
- Output: 448×256 H.264/YUV420P, 41 frames at 8 fps, 5.125 seconds, 212,750 bytes.
- Output SHA-256: `c931088d0f3194c2e0e48c1f6b838c548ed0f75bc004e93ddfb9b26472f30693`.
- Metadata SHA-256: `d45d1fbade8c68ffe4944e1a481184024bff57668c46e4d4424bd7b7f511c47a`.
- Full decode: pass.
- Contact-sheet SHA-256: `c0eb8c56118f854f3100acd07343b6feda4a0ccfe3ba04919b65175029e316d9`.
- Minimum sampled memory free: 89%.
- Maximum sampled swap: 0 MiB.
- Maximum sampled process-tree RSS: 29,057,248 KiB.
- MLX peak memory: 30,550,431,788 bytes.
- Process peak RSS: 29,734,027,264 bytes.
- Peak physical footprint: 32,198,059,088 bytes.
- Minimum free disk on both required paths: 7,359,893,612 KiB.
- Safety stop: none; no sampled thermal or performance warning.

The sampling loop emitted progress through step 14 before the fast final decode transition, so `summary.env` records 14 observed loop events. The immutable runtime log contains all 15 ordered denoising events, followed by decode, convert, generated, save, and complete; the verifier reconciles both evidence sources without altering the raw run record.

## Owner Motion Review

Pending. Technical success does not decide any visual gate. The owner must review the generated video and six-frame contact sheet and provide verdicts for all twelve frozen gates covering orientation, travel direction, displacement, speed, wind, sail, water, bow wave, wake, geometric/camera stability, and forbidden content.

## Commands Run

- `./.automation/scripts/aira-memory feature --query "Implement and execute exactly one Slice 008 Wan2.2 first-last-frame motion scout"`
- `.venv/bin/python scripts/verify-slice-008.py` against the preparation commit, before implementation
- `.venv/bin/python scripts/verify-slice-007.py --preflight`
- `.venv/bin/python scripts/verify-slice-008.py --preflight` against the frozen implementation
- Python compilation, JSON parsing, shell syntax, and `git diff --check` before the pre-inference commit
- `./scripts/run-slice-008-motion-scout.sh` exactly once; the runner repeated both preflight verifiers before launch
- `ffmpeg -v error -i outputs/slice-008/wan2.2-i2v-a14b-first-last-motion-scout-seed-42.mp4 -f null -` as an independent post-run full decode
- `.venv/bin/python scripts/verify-slice-008.py --allow-pending-review`
- `.venv/bin/python scripts/verify-slice-002.py`
- `.venv/bin/python scripts/verify-slice-005.py`
- `.venv/bin/python scripts/verify-slice-006.py`
- `.venv/bin/python scripts/verify-slice-007.py`
- `bash -n scripts/run-slice-008-motion-scout.sh` and `.venv/bin/python -m py_compile scripts/verify-slice-008.py`
- `.venv/bin/python -m json.tool` for every tracked or newly created JSON file
- `git diff --check`
- `rg --hidden -n '\p{Cyrillic}' -g '!.git/**' -g '!third_party/**' -g '!.venv/**' -g '!.python/**' -g '!.cache/**' .`
- the registered repository artifact scan for model-weight and video suffixes
- `./.automation/scripts/aira-memory audit --mode project-local --fail-on-drift`

All commands above passed. The language scan returned no matches. The artifact scan found only the six expected ignored Slice 002, 005, 007, and 008 videos and no tracked weight or video. The strict project-local Memory Core audit reported zero issues in every category.

## Stop Boundary

The single attempt is consumed. The attempt marker and output both exist, and the runner refuses another launch. No push, pull request, merge, additional generation, publication, or Memory Core promotion was performed.
