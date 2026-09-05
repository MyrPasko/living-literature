---
task_id: slice-007-wan-2.2-i2v-a14b-motion-scout
task_type: feature
status: complete-rejected
branch: feature/slice-007-wan-2-2-i2v-motion-scout
date: 2026-09-05
write_scope:
  - Slice 007 benchmark, runtime, model, runner, verifier, results, and documentation artifacts
  - .project-memory/canon/current-state.md
  - .project-memory/verify-commands.md
  - .project-memory/docs-index.md
  - generated project-local Memory Core workspace artifacts
  - Git-ignored model, runtime, source still, scout output, review media, and run logs
forbidden_moves:
  - more than one generation attempt after denoising begins
  - tuning, alternate seeds or samplers, adapters, full render, or offline duplicate
  - cloud inference, API key, publication, or parallel inference
  - model-cache migration, Obsidian update, or automatic Memory Core promotion
verification_surface:
  - exact model and runtime provenance and complete local file inventories
  - immutable prompt, parameters, source still, one-attempt marker, and safety controls
  - measured resource telemetry, output identity, media properties, and full decode
  - owner motion hard gates and rejected disposition
  - historical deterministic verifiers and repository safety checks
success_criteria:
  - execute exactly one bounded local motion scout and record a technical and owner verdict
slice_restrictions:
  - Slice 004 remains postponed
  - Wan2.2 I2V-A14B is not accepted for production
  - Slice 007 authorizes no additional inference
---

# Implementation Result

## Outcome

Slice 007 is complete and rejected for motion. The single authorized Wan2.2 I2V-A14B BF16 scout passed technical execution and safety validation, but failed owner review. No production model is accepted, and this slice authorizes no rerun, tuning, duplicate, or full render.

## Work Performed

- Installed and pinned an isolated MLX-Gen 0.33.1 runtime at source commit `23cee803f10aacdf943a9565f7cd67c25c825080`; the wheel SHA-256 is `1a19e6510a166cbe0fe4975146813fb61adf98f0e073abb4e63f27f012882d0a`.
- Downloaded and hashed the exact 44-file, 68,791,046,058-byte BF16 package `AbstractFramework/wan2.2-i2v-a14b-diffusers-bf16` at revision `ef2a0bfe5b4ca7edb84c93f1675edb1a8bfe7d60`.
- Verified the pinned candidate-D source still and frozen prompt, parameter, resource, and one-attempt boundaries.
- Executed exactly one local-files-only sequential scout after denoising began.
- Recorded runtime, system, output, metadata, contact-sheet, and owner-review evidence.

## Technical Result

- Run: `local-files-only-motion-scout-seed-42`.
- Duration: 272 seconds wrapper time; 258.63 seconds reported generation and save time.
- Output: 448×256 H.264, 41 frames at 8 fps, 5.125 seconds.
- Output SHA-256: `112805f168d717825e11ce3b9796dedbb6ddb07f83e6fc97507a9da6768a9656`.
- Full decode: pass.
- Minimum sampled memory free: 89%.
- Maximum sampled swap: 0 MiB.
- MLX peak memory: 30,550,431,788 bytes.
- Peak physical footprint: 32,338,977,872 bytes.
- Safety stop: none; no sampled thermal or performance warning.

## Owner Motion Review

The owner rejected the result on 2026-09-05 for four observed problems:

- the ship moved in reverse rather than continuously from left to right;
- the sail implied wind inconsistent with the intended travel direction;
- the taut filled sail lacked corresponding wind-driven waves on the sea surface;
- the ship moved too quickly for the depicted slow wind.

The continuous-left-to-right and wind/water-causality hard gates are explicitly failed. Remaining hard gates are `not_assessed` because one failure already rejects the route. The technical pass does not override the owner motion failure.

## Verification

- `command:` `.venv/bin/python scripts/verify-slice-007.py`
  - `result:` pass in complete rejected state
  - `notes:` exact runtime/model/source identities, one-attempt evidence, resource telemetry, output hash and full decode, owner failure, and rejected disposition are consistent.
- `command:` `.venv/bin/python scripts/verify-slice-002.py`; `.venv/bin/python scripts/verify-slice-005.py`; `.venv/bin/python scripts/verify-slice-006.py`
  - `result:` pass
  - `notes:` Slice 005 includes complete output decode; Slice 006 is complete.
- `command:` Python compilation, JSON parsing, `git diff --check`, language scan, artifact scan, and project-local Memory Core audit
  - `result:` pass
  - `notes:` no Cyrillic matches; only five expected ignored Slice 002, 005, and 007 videos; no tracked weights or videos; zero audit findings.

## Review and Closeout

The rejected result preserves the one-attempt boundary. Closeout verification found no unresolved failure or scope drift. No additional inference, cloud service, API key, parallel inference, publication, or Memory Core promotion is authorized.
