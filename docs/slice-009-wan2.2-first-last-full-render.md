---
project: Living Literature
document: wan2.2-first-last-full-render
status: complete-pre-denoise-configuration-rejection
verified: 2026-09-05
slice: slice-009-wan2.2-first-last-full-render
---

# Slice 009 — Wan2.2 First/Last Full Render

## Purpose

Measure one full-size Wan2.2 I2V-A14B first/last-frame render after the Slice 008 motion scout passed. This slice maps the reusable Wan2.1 Slice 005 benchmark parameters onto the pinned Wan2.2 BF16 route while preserving the Slice 008 anchors and prompts.

## Exact Route

- Reuse `AbstractFramework/wan2.2-i2v-a14b-diffusers-bf16` revision `ef2a0bfe5b4ca7edb84c93f1675edb1a8bfe7d60`; no download.
- Reuse MLX-Gen 0.33.1 at commit `23cee803f10aacdf943a9565f7cd67c25c825080`, wheel SHA-256 `1a19e6510a166cbe0fe4975146813fb61adf98f0e073abb4e63f27f012882d0a`; no installation.
- Use the direct `mlxgen-generate-wan` executable with experimental `--last-image` bracket conditioning.
- Execute exactly one sequential local-files-only attempt. The durable marker is created before launch and prevents a retry.

## Frozen Anchors and Prompts

The first anchor remains `outputs/next-slice-reference-candidates/right-facing-aegean-galley-start-frame-candidate-v2.png`, SHA-256 `9441f1a783f42ef1e7b605f0c4c6981462e071c46f49c7607a4ba6ab9533ffde`. The last anchor remains `outputs/next-slice-reference-candidates/right-facing-aegean-galley-approved-end-frame-v1.png`, SHA-256 `6c0f3d2ee62e4ff563a1fc02d6e42a3f255bc75d3bed8fa6210904f862ef85ce`. Both are 1672×940 and owner-approved.

The positive and negative prompts are byte-for-byte identical to Slice 008. They preserve right-facing bow-first travel, the two-anchor displacement, a locked camera, coherent left-to-right wind, a filled sail, visible wavelets, a prow bow wave, and a stern-only wake.

The anchors retain unresolved user-reference lineage. This run is internal-evaluation-only and cannot clear publication or production use.

## Frozen Full-Render Configuration

- 832×480 requested source-aspect canvas;
- 81 frames at 16 fps;
- 50 denoising steps;
- seed 42;
- guidance 5.0 and guidance-2 5.0;
- flow shift 5.0;
- UniPC;
- BF16, low-RAM, metadata on, prompt cache off, inactive denoiser release;
- local-files-only Hugging Face, Transformers, and Diffusers flags;
- output `outputs/slice-009/wan2.2-i2v-a14b-first-last-full-render-seed-42.mp4`.

Wan2.1’s 832×480, 81-frame, 16-fps, 50-step, seed-42, guidance-5.0, shift-5.0, UniPC values are reused. Wan2.1’s model-specific 8-bit quantization is not portable to the already pinned Wan2.2 BF16 package; therefore Slice 009 remains BF16. The one Wan2.1 guidance value maps to both Wan2.2 expert guidance controls, and Wan2.1 shift maps to Wan2.2 flow shift.

Although the frozen prompt says 5.125 seconds because it is reused exactly from Slice 008, 81 frames encoded at 16 fps resolve to approximately 5.063 seconds. The discrepancy is documented rather than silently changing the passed prompt.

## Safety and Stop Boundary

Preflight requires at least 90% free memory, zero swap, at least 120 GiB free on required volumes, no thermal/performance warning, exact local model/runtime inventories, exact anchor hashes, direct `--last-image` support, clean committed configuration, and no competing inference process.

The monitor stops the process tree at 10% or less free memory, more than 8 GiB swap, less than 100 GiB disk, a thermal/performance warning, 20 minutes without a denoising event after denoising starts, or four hours total. It samples every 15 seconds.

The slice authorizes no download, installation, tuning, retry, alternate seed or sampler, adapter, offline duplicate, parallel or cloud inference, publication, production acceptance, or automatic Memory Core promotion. After technical validation, the owner reviews the same twelve motion gates used for Slice 008.

## Accepted Plan

- Exact references: completed Slice 008 commit `6a3e3381b3190c348697557f60ed05b257c60115`, the two frozen anchor hashes, the pinned model/runtime revisions, and the exact parameter mapping above.
- Write scope: Slice 009 benchmark, runner, verifier, results and documentation; three repo-canon registries; generated project-local workflow artifacts; ignored Slice 009 output and telemetry.
- Verification: configuration and host preflight, historical inventory preflight, runtime telemetry, media probe and full decode, hashes, metadata, contact sheet, and owner motion review.
- Success: one safe completed render and technically valid review artifact. Motion acceptance is a separate owner verdict.

## Execution Result

The launch was interrupted before denoising because `source-aspect` resolved the requested 832×480 canvas to 848×480. No video was produced and no retry occurred. See the implementation result for measured evidence and the authority boundary for any corrected attempt.
