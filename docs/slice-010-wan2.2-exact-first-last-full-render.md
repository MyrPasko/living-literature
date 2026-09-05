---
project: Living Literature
document: wan2.2-exact-first-last-full-render
status: complete-rejected-motion
verified: 2026-09-05
slice: slice-010-wan2.2-exact-first-last-full-render
---

# Slice 010 — Wan2.2 Exact First/Last Full Render

## Purpose

Execute one corrected full-size Wan2.2 I2V-A14B first/last-frame render after Slice 009 stopped before denoising. The sole configuration correction is `canvas_policy=exact-resize`, which forces the approved 832×480 canvas instead of resolving it to 848×480.

## Exact References

- Baseline: completed Slice 009 commit `96a1ac2f9dbad2e99e120ae8606edd49fe2019ca`.
- Model: `AbstractFramework/wan2.2-i2v-a14b-diffusers-bf16` revision `ef2a0bfe5b4ca7edb84c93f1675edb1a8bfe7d60`; no download.
- Runtime: MLX-Gen 0.33.1, commit `23cee803f10aacdf943a9565f7cd67c25c825080`, wheel SHA-256 `1a19e6510a166cbe0fe4975146813fb61adf98f0e073abb4e63f27f012882d0a`; no installation.
- First anchor SHA-256: `9441f1a783f42ef1e7b605f0c4c6981462e071c46f49c7607a4ba6ab9533ffde`.
- Last anchor SHA-256: `6c0f3d2ee62e4ff563a1fc02d6e42a3f255bc75d3bed8fa6210904f862ef85ce`.

The anchors and positive/negative prompts are unchanged from Slice 008 and Slice 009. Their unresolved user-reference lineage limits this render to internal evaluation and prohibits publication or production use.

## Frozen Configuration

- exact 832×480 canvas with `canvas_policy=exact-resize` and resize mode `resize`;
- 81 frames at 16 fps and 50 denoising steps;
- seed 42, guidance 5.0, guidance-2 5.0, flow shift 5.0, UniPC;
- BF16, low-RAM, metadata on, prompt cache off, inactive denoiser release;
- direct `mlxgen-generate-wan` with `--last-image` and local-files-only flags;
- one sequential launch with a new durable marker and no replacement;
- output `outputs/slice-010/wan2.2-i2v-a14b-exact-first-last-full-render-seed-42.mp4`.

The prompt still says 5.125 seconds because it remains byte-identical to the passed Slice 008 prompt. The 81-frame, 16-fps encoded duration is approximately 5.063 seconds.

## Safety and Restrictions

Preflight requires a clean committed branch, exact anchors, exact local model/runtime inventories, direct `--last-image` support, Metal, at least 90% free memory, zero swap, at least 120 GiB free disk, no warning state, and no competing inference process.

The monitor samples every 15 seconds and stops at 10% or less free memory, more than 8 GiB swap, less than 100 GiB disk, a thermal/performance warning, 20 minutes without denoising progress after denoising starts, or four hours total.

No retry, tuning, alternate seed/sampler, adapter, offline duplicate, parallel/cloud inference, download, installation, publication, production acceptance, or automatic Memory Core promotion is authorized.

## Accepted Plan

- Write scope: Slice 010 benchmark, runner, verifier, results and documentation; repo-canon state, verification registry, docs index; generated workflow artifacts; ignored Slice 010 output and telemetry.
- Verification: frozen-configuration check, host and historical inventory preflight, runtime telemetry, exact media probe, full decode, hashes, metadata, contact sheet, and twelve-gate owner review.
- Success: exactly one safe 832×480 technical result ready for owner review.

## Technical Execution

The single launch completed normally in 7,354 seconds. It produced an exact 832×480, 81-frame H.264 video at 16 fps with SHA-256 `de81c77df5cbf6d9d4b25ecc2012f9db130e7ec853671cda947b066b53995205`. Full decode passed, swap remained zero, and no thermal/performance warning occurred.

## Owner Motion Verdict

The owner passed the image sharpness and realism, atmosphere, colour palette, ship silhouette, and sail silhouette. Motion failed because the hull pitches, bobs, and seesaws fore and aft as if rocked from bow to stern. The steering oar also cycles like a propulsion oar and bends like a flexible tail instead of remaining a rigid, stable steering control. The route is therefore `rejected-motion`; no retry is authorized by Slice 010.
