---
project: Living Literature
document: wan-2.1-t2v-14b-benchmark-plan
status: planned-not-authorized
created: 2026-09-03
slice: slice-005-wan-2.1-t2v-14b-benchmark
depends_on:
  - slice-003-quality-and-model-gate
  - slice-004-rights-ledger-foundation
---

# Slice 005 — Wan2.1 T2V 14B Benchmark

## Authority Boundary

This document specifies exactly one future benchmark. It does **not** authorize model download or inference. Slice 005 requires separate owner authorization after Slice 004.

No multi-model bake-off, prompt tuning, distilled checkpoint, I2V input, LTX run, or production work is part of this benchmark.

## Exact Model Boundary

- family/task: Wan2.1 text-to-video;
- repository: `Wan-AI/Wan2.1-T2V-14B`;
- revision: `a064a6c71f5be440641209c07bf2a5ce7a2ff5e4`;
- license: Apache-2.0 at that revision;
- implementation: Apple `mlx-examples/video/wan2.1` at `796f5b53cab69a3d48a44233ce21aae889e94a08`;
- implementation license: MIT.

Before any future download, re-query repository metadata. Revision drift is a stop, not permission to silently substitute a newer commit.

## Fixed Prompt and Configuration

Reuse the immutable Slice 002 prompt:

> A black ancient Greek ship crosses a dark wine-colored sea before dawn. Bronze Age aesthetic, heavy clouds, cold wind moving the square sail, cinematic wide shot, restrained realistic motion, no text, no modern objects.

Primary configuration:

- model selector: `t2v-14B`;
- width × height: 832×480;
- frames: 81;
- frame rate: 16 fps;
- steps: 50;
- guidance: 5.0;
- shift: 5.0;
- seed: 42;
- sampler: UniPC;
- negative prompt: `Text, watermarks, blurry image, JPEG artifacts`;
- pipeline compute default: bfloat16 where selected by the pinned Apple implementation;
- DiT quantization: MLX 8-bit through `--quantize 8`;
- offloading: none; the pinned Apple implementation exposes no offload mode;
- TeaCache: disabled (`0.0`);
- Metal buffer cache: disabled through `--no-cache`;
- preload: disabled;
- prompt extension: disabled;
- output: H.264 MP4 through the pinned implementation's FFmpeg path.

The deliberate deviations from Slice 002 are the 14B model, 8-bit DiT quantization, and disabled Metal buffer cache. Apple documents quantization for 14B; cache disabling reduces swap pressure. The test therefore asks whether the practical bounded 14B workflow beats the unquantized 1.3B baseline, not whether raw unquantized 14B wins at any cost.

## Download and Disk Boundary

Allowlist only these ten runtime files at the exact model revision:

1. `diffusion_pytorch_model.safetensors.index.json`
2. `diffusion_pytorch_model-00001-of-00006.safetensors`
3. `diffusion_pytorch_model-00002-of-00006.safetensors`
4. `diffusion_pytorch_model-00003-of-00006.safetensors`
5. `diffusion_pytorch_model-00004-of-00006.safetensors`
6. `diffusion_pytorch_model-00005-of-00006.safetensors`
7. `diffusion_pytorch_model-00006-of-00006.safetensors`
8. `Wan2.1_VAE.pth`
9. `models_t5_umt5-xxl-enc-bf16.pth`
10. `google/umt5-xxl/tokenizer.json`

Current verified total: **69,040,541,912 bytes (64.299 GiB)**. License and model-card evidence must also be captured at the exact revision. Reserve at least **165 GiB free disk before download**: the 64.299 GiB runtime set, generous temporary/cache overhead, both MP4s and logs, while preserving the existing 100 GiB runtime stop floor.

## Resource Estimate

These are planning estimates, not measurements:

- MLX peak: 35–55 GB;
- peak process footprint: 75–110 GB;
- inference time: 5,400–10,800 seconds (1.5–3.0 hours) per run;
- two-run wrapper budget: 3–6.5 hours plus download, hashing, and review;
- expected swap: zero;
- confidence: low-to-medium.

The runtime anchor is the measured 2,200.93-second 1.3B run scaled by Apple's published M4 Max per-step ratio of 230/90, approximately 5,625 seconds. Quantization, cache policy, M5 Max behavior, and process-footprint semantics widen the range.

## Required Future Implementation

- A downloader that pins every Hugging Face request to the exact revision and rejects any filename outside the allowlist.
- Size and SHA-256 verification recorded in a tracked model manifest.
- A new immutable benchmark JSON; do not reuse or mutate the Slice 002 JSON.
- A dedicated runner copied from the proven pattern and frozen before launch.
- Descendant-process-tree RSS/footprint sampling, not wrapper-only RSS sampling.
- MLX peak, free-memory percentage, swap, disk, thermal/performance state, elapsed time, and last-progress timestamp monitoring.
- Online-capable first run followed by a network-denied offline repeat using exact cached paths.
- Output metadata, complete decode, SHA-256, byte-identity comparison, and quality review.

## Safety Gates

Preflight requirements:

- no other model inference process is running;
- at least 90% system memory is free immediately before launch;
- swap usage is zero immediately before launch;
- at least 165 GiB disk is free before download and 120 GiB before inference;
- source, runner, benchmark, and model manifest are committed or checksummed and will not be edited while active;
- the exact ten-file cache and license evidence pass before inference.

Stop the run immediately if any condition occurs:

- free memory reaches 10%;
- swap grows above 8 GiB;
- free disk reaches 100 GiB;
- macOS thermal state becomes serious or critical, or a performance warning is observed;
- the descendant process exits unexpectedly;
- no denoising progress is recorded for 20 consecutive minutes after model loading;
- an undeclared network request, file request, model revision, or checkpoint appears.

These thresholds are no weaker than Slice 002. The lower swap ceiling is intentional because a heavily paging multi-hour run is not a useful production candidate even if it eventually completes.

## Offline Proof

1. Run the fixed benchmark once in online-capable mode with all model requests revision-pinned.
2. Verify and freeze the resulting cache inventory.
3. Repeat the same benchmark with `HF_HUB_OFFLINE`, `TRANSFORMERS_OFFLINE`, and `DIFFUSERS_OFFLINE`; force `local_files_only=True`; and apply macOS `(deny network*)`.
4. Require a socket-bind denial preflight inside the same sandbox before inference.
5. Require both runs to complete, fully decode, match the declared media properties, and produce byte-identical MP4 hashes. A mismatch is a reproducibility finding and fails the offline-repeat criterion even if both videos play.

## Quality Rubric

Review normal-speed playback, the first/middle/last frames, and at least ten evenly spaced samples. Record pass/partial/fail with observations for:

1. **Bronze Age Greek ship specificity — hard gate:** the vessel must read as plausibly Bronze Age Greek rather than a generic later sailing ship; no obviously anachronistic multi-mast or modern rigging.
2. **Directed square-sail motion — hard gate:** wind-driven movement must be visibly present and temporally coherent without sail deformation.
3. **Atmosphere:** dark wine-colored sea, pre-dawn light, heavy clouds, and cinematic wide composition remain legible.
4. **Temporal/object coherence — hard gate:** stable ship geometry, horizon, water, sail, and camera motion; no abrupt morphing, duplication, or collapse.
5. **Restrained realism:** motion remains calm and physically plausible for the scene.
6. **Forbidden content — hard gate:** no text, watermark, modern object, or unsafe content.
7. **Material improvement:** both Slice 002 partial criteria must become passes. Merely adding surface detail while retaining a generic ship or static sail is not enough.

This is an editorial benchmark, not archaeological certification. A human reviewer must still distinguish visual plausibility from verified historical accuracy.

## Success Criteria

The benchmark succeeds only if:

- both runs complete within all safety gates;
- each inference run is no longer than 14,400 seconds (4 hours);
- offline network denial is proven;
- outputs are byte-identical and pass media/decode checks;
- all quality hard gates pass;
- both Slice 002 partial criteria improve to pass;
- all weights, caches, logs, and videos remain Git-ignored;
- no prompt or parameter is changed between runs.

Success accepts Wan2.1-T2V-14B as a candidate for later shot-production work. It does not establish production readiness or publication clearance.

## Rejection Criteria

Reject this 14B workflow, with no tuning loop inside Slice 005, if:

- any safety stop triggers;
- either run exceeds four hours;
- the offline repeat fails or differs byte-for-byte;
- historical specificity or sail motion remains partial/fail;
- temporal coherence or forbidden-content hard gates fail;
- execution requires an undeclared model, cloud service, API key, or runtime substitution.

If rejected, return to a separate decision gate between Wan I2V with a rights-cleared still and deterministic animation. Do not automatically download another model.
