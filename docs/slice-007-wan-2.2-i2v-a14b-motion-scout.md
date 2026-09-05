---
project: Living Literature
document: wan-2.2-i2v-a14b-motion-scout
status: active
verified: pending
slice: slice-007-wan-2.2-i2v-a14b-motion-scout
---

# Slice 007 — Wan2.2 I2V-A14B Motion Scout

## Purpose

Execute one low-cost, sequential image-to-video motion scout using the exact Wan2.2 I2V-A14B BF16 route selected by Slice 006. The scout tests direction, wake placement, wind/water causality, sail stability, geometry, horizon, and camera stability before any full-resolution benchmark is considered.

This slice does not accept a production model. It authorizes one prepared-package download, one isolated MLX-Gen 0.33.1 runtime installation, and at most one generation attempt after denoising begins. It does not authorize a seed sweep, prompt or parameter tuning, LoRA or Lightning use, a full render, an offline duplicate, parallel inference, cloud service, API key, publication, or Memory Core promotion.

## Exact References

- Prepared model: `AbstractFramework/wan2.2-i2v-a14b-diffusers-bf16`.
- Prepared revision: `ef2a0bfe5b4ca7edb84c93f1675edb1a8bfe7d60`.
- Prepared inventory: 44 files, 68,791,046,058 bytes.
- Source model: `Wan-AI/Wan2.2-I2V-A14B-Diffusers`.
- Source revision: `596658fd9ca6b7b71d5057529bbf319ecbc61d74`.
- Model license: Apache-2.0.
- Runtime: MLX-Gen 0.33.1.
- Runtime source commit: `23cee803f10aacdf943a9565f7cd67c25c825080`.
- Runtime wheel SHA-256: `1a19e6510a166cbe0fe4975146813fb61adf98f0e073abb4e63f27f012882d0a`.
- Runtime license: MIT.
- Precision: BF16.
- Execution: sequential only.

The runtime is isolated from the existing project environment because MLX-Gen 0.33.1 requires MLX below 0.32 while the project environment currently carries MLX 0.32.2.

## Pinned Source Still

- Candidate D: `outputs/slice-006/source-still-candidates/candidate-d-frame-048.png`.
- SHA-256: `7e7f0a20ebaa62551cad700d7e17fecd0fdc68a7003c9e1eb2e846f7fd6ec0c7`.
- Dimensions: 832×480.
- Source frame: zero-based frame 48 at `00:00:03.000`.
- Source-video SHA-256: `ce7a61c21ef0811062ea6229b3ddf89c6843bdc6569234cab060915bd39f2ad4`.

The still remains local and Git-ignored.

## Frozen Prompts

Positive prompt:

> Single continuous five-second shot, locked-off wide side view. A Late Bronze Age Aegean galley with a long black hull, curved prow and stern, one mast and one rectangular square sail moves steadily from left to right across a dark wine-colored sea before dawn. The bow always points right; the stern remains left. Moderate wind blows from left to right, naturally filling the sail and raising aligned wavelets. A small bow wave splits outward at the prow; a narrow foamy wake begins only behind the stern and trails leftward. Heavy purple clouds drift slowly. Stable geometry, physically coherent motion, no camera movement, text, or modern objects. Preserve the approved input image’s ship design, palette, atmosphere, framing, and horizon.

Negative prompt:

> reverse playback, backward sailing, wake or foam ahead of the bow, wake extending forward, perfectly still water with a filled sail, deformed sail, changing hull geometry, extra mast, camera dolly, pan, zoom, text, watermark, modern vessel, blurry image, JPEG artifacts

## Frozen Scout Configuration

- requested canvas: 448×256 with `source-aspect` resolution;
- record resolved width and height;
- 41 frames at 8 fps;
- 15 denoising steps;
- seed 42;
- guidance 4.0;
- guidance-2 3.0;
- flow shift 3.0;
- UniPC solver;
- BF16 and low-RAM mode;
- metadata enabled;
- prompt-embedding disk cache disabled;
- no LoRA, Lightning adapter, prompt extension, cache acceleration, video input, compiled transformer, or parallel process;
- local prepared-package path and Hugging Face offline flags during inference.

## Safety Boundary

Preflight requires at least 90% memory free, zero swap, no other model-inference process, no thermal or performance warning, at least 180 GiB free disk before download, and at least 120 GiB before inference.

The runner stops when memory free reaches 10%, swap exceeds 8 GiB, free disk falls below 100 GiB, macOS reports a serious thermal or performance warning, denoising progress is silent for 20 consecutive minutes, the process exits unexpectedly, or elapsed runtime exceeds four hours.

## Motion Hard Gates

All gates must pass:

1. Bow remains on the right.
2. Stern remains on the left.
3. Ship moves continuously left to right.
4. Wake starts only behind the stern and trails leftward.
5. A small bow wave begins at the prow.
6. The bow wave does not resemble a forward wake.
7. Water movement matches the wind and filled sail.
8. Sail does not deform.
9. Ship, mast, hull, horizon, and camera remain stable.
10. No text, watermark, modern object, unsafe content, or major visual collapse appears.

Any failure rejects the route without tuning, alternate seeds or samplers, adapters, unplanned reruns, or a full-resolution render.

## Completion Boundary

After technical validation, the owner reviews the generated scout. The slice remains awaiting editorial verdict until the owner marks every hard gate. A passing scout may inform a separately approved later full-benchmark slice; it does not authorize that run.
