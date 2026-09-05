---
task_id: slice-010-wan2.2-exact-first-last-full-render
task_type: feature
status: pending-owner-motion-review
branch: feature/slice-010-wan2-2-exact-full-render
date: 2026-09-05
---

# Implementation Result

## Outcome

Slice 010 completed exactly one authorized Wan2.2 I2V-A14B BF16 first/last-frame full render. The output passed technical validation and is pending the owner’s twelve-gate motion review. This does not accept a production model, resolve anchor rights, or authorize publication.

## Execution

- Configuration commit: `0938014460f187c0169bb86f742d03f248b4523d`.
- Run window: 2026-09-05 13:32:09Z–15:34:43Z.
- Wrapper duration: 7,354 seconds (2 h 02 m 34 s).
- Runtime generation: 7,293.22 seconds; save: 45.39 seconds; total generation and save: 7,338.61 seconds.
- Exact route: 832×480, 81 frames, 16 fps, 50 steps, seed 42, guidance 5.0/5.0, flow shift 5.0, UniPC, BF16, `canvas_policy=exact-resize`, local-files-only flags.
- Denoising events: 50/50; safety stop: none.

## Technical Result

- Output: H.264/YUV420P, 832×480, 81 frames, 16 fps, 5.0625 seconds, 1,262,186 bytes.
- Output SHA-256: `de81c77df5cbf6d9d4b25ecc2012f9db130e7ec853671cda947b066b53995205`.
- Metadata SHA-256: `e30f4c495d5d52d33aff4f86a52f91f7db195d0e8a874aa64833aec7891e9568`.
- Full decode and independent 81-frame count: pass.
- Contact-sheet SHA-256: `87158a7f9601488008e260d708201a33a78b78c088a3dbd4831b64e0b1e1d2ef`.
- Minimum sampled memory free: 89%; maximum swap: 0 MiB.
- Maximum sampled process-tree RSS: 29,139,856 KiB.
- MLX peak memory: 37,249,511,812 bytes.
- Process peak RSS: 29,818,617,856 bytes.
- Peak physical footprint: 39,499,554,168 bytes.
- Minimum free disk on required paths: 7,361,894,656 KiB.
- Thermal/performance warnings: none.

## Verification

The configuration-only check proved that only the Slice 009 canvas policy changed. The host preflight verified the clean committed branch, exact anchors, complete 44-file model package, pinned runtime, direct `--last-image` support, Metal, zero swap, disk, warnings, and process exclusivity. The runner performed full decode and created the six-frame contact sheet. Independent FFmpeg decode and counted-frame FFprobe checks passed after completion.

The attempt marker remains and the runner refuses another launch. No retry, download, installation, offline duplicate, tuning, parallel/cloud inference, publication, production acceptance, Memory Core promotion, push, pull request, or merge occurred.

## Owner Review Boundary

The owner must assess all twelve frozen motion gates against the video. Technical success alone does not determine motion acceptance.
