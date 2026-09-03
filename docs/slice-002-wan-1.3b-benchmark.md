---
project: Living Literature
document: wan-1.3b-offline-benchmark
status: complete
verified: 2026-09-03
slice: slice-002-wan-1.3b-offline-benchmark
---

# Wan2.1 1.3B Offline Benchmark

## Outcome

Slice 002 proves that the pinned Wan2.1-T2V-1.3B candidate can generate the fixed benchmark locally on BigBoy and repeat it with all network access denied. Both runs produced the same playable 832×480, 81-frame H.264 MP4 and the same SHA-256 hash.

This is a feasibility and repeatability result. The candidate is not accepted as the production model.

## Exact References

- model repository: `Wan-AI/Wan2.1-T2V-1.3B`;
- model revision: `37ec512624d61f7aa208f7ea8140a131f93afc9a`;
- model license: Apache-2.0, preserved at `docs/licenses/wan2.1-t2v-1.3b-apache-2.0.txt`;
- model manifest: `manifests/models/wan2.1-t2v-1.3b.json`;
- Apple MLX implementation: `mlx-examples` at `796f5b53cab69a3d48a44233ce21aae889e94a08`;
- fixed benchmark: `benchmarks/slice-002-wan-1.3b.json`;
- measured result: `manifests/benchmarks/slice-002-wan-1.3b-results.json`.

The model card recommends 480p for this 1.3B checkpoint. The benchmark used its supported 832×480 geometry. Its guidance and shift values were declared before the first run and were not changed to match later model-card recommendations.

## Fixed Benchmark

Prompt:

> A black ancient Greek ship crosses a dark wine-colored sea before dawn. Bronze Age aesthetic, heavy clouds, cold wind moving the square sail, cinematic wide shot, restrained realistic motion, no text, no modern objects.

Parameters:

- seed: 42;
- size: 832×480;
- frames: 81;
- steps: 50;
- guidance: 5.0;
- shift: 5.0;
- sampler: UniPC;
- quantization: none;
- TeaCache: disabled;
- frame rate: 16 fps.

## Weight Boundary

The downloader requested only the license, model card, and four runtime files required by the pinned Apple implementation. The complete verified download was 17,562,466,409 bytes. Runtime weights and cache paths remain Git-ignored; only hashes, sizes, provenance, and the license snapshot are tracked.

## Measured Runs

| Evidence | Online-capable baseline | Offline network-denied repeat |
|---|---:|---:|
| Inference exit | 0 | 0 |
| Inference runtime | 1,989.82 s | 2,200.93 s |
| Wrapper wall time | recovery record | 2,222 s |
| MLX peak memory | 25.693 GB | 25.693 GB |
| Maximum resident set | 39,437,451,264 bytes | 39,435,894,784 bytes |
| Peak process footprint | 67,432,368,168 bytes | 68,272,064,576 bytes |
| Minimum observed free memory | 57% | 56% |
| Maximum observed swap | 0 MB | 0 MB |
| Thermal/performance warning | none | none |
| Output size | 615,420 bytes | 615,420 bytes |
| Output SHA-256 | `9984555b3918a56c0ad8f4043b234cdbec2ba15bbaffc46e49eddae86838390f` | same |

The offline run enabled `HF_HUB_OFFLINE`, `TRANSFORMERS_OFFLINE`, and `DIFFUSERS_OFFLINE`; forced every Hugging Face lookup through `local_files_only=True`; and executed the process under macOS `sandbox-exec` with `(deny network*)`. Before inference, a loopback socket-bind attempt inside that sandbox failed as required. The run therefore did not need an API key or network service.

Both files report H.264, 832×480, 81 frames, 16 fps, and 5.0625 seconds. Both completed a full FFmpeg decode without error. Byte-identical outputs provide deterministic-repeat evidence for this pinned environment and seed.

## Quality Rubric

The review used normal-speed QuickTime playback plus the first, midpoint, last, and ten evenly spaced frame samples.

| Criterion | Result | Observation |
|---|---|---|
| Black ancient Greek ship | Partial | A coherent black vessel is present, but the two-masted silhouette reads as generic rather than unmistakably Bronze Age Greek. |
| Dark wine-colored sea before dawn | Pass | The water is dark wine-purple and the lighting reads as pre-dawn. |
| Heavy clouds and cinematic wide shot | Pass | Mood, cloud mass, and composition remain consistent. |
| Cold wind moving the square sail | Partial | Water motion and a slow camera approach are convincing; sail movement is subtle. |
| Restrained realistic motion | Pass | Playback is calm and coherent, without abrupt morphing. |
| No text or modern objects | Pass | No text, watermark, or obvious modern object is visible. |
| Production suitability | Not accepted | Strong feasibility control and mood draft; historical specificity and directed motion remain insufficient for model acceptance. |

## Review Finding

The online inference and video save succeeded, but its outer shell wrapper encountered an unexpected EOF during finalization because the runner file was edited while that shell was still reading it. The model log, `/usr/bin/time` record, output hash, FFprobe metadata, full decode, and sampled system evidence were recovered and preserved. The runner was then frozen before the offline run, whose wrapper completed normally. Future long-running scripts must never be patched in place while active.

## Decision Boundary

Slice 002 is complete. Slice 003 is the existing Quality and Model Gate. It may compare the measured 1.3B result against current primary-source evidence and select one next approach, but it does not authorize a heavier-model download or inference by itself. No 14B, image-to-video, LTX, prompt-tuning, audio, complete Short, or publication work belongs in this closeout.
