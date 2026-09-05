---
project: Living Literature
document: wan-2.2-i2v-a14b-decision-gate
status: complete
verified: 2026-09-04
slice: slice-006-wan-2.2-i2v-a14b-decision-gate
---

# Slice 006 — Wan2.2 I2V-A14B Decision Gate

## Decision

Select `Wan-AI/Wan2.2-I2V-A14B-Diffusers` through the pinned `mlx-gen` BF16 package as the single future motion-scout candidate.

This accepts one bounded future benchmark route, not a production model. Slice 006 installs no runtime, downloads no weights, runs no inference, generates no replacement image, uses no cloud service or API key, publishes nothing, authorizes no parallel inference, and applies no Memory Core promotion.

The owner selected candidate D, the left image in the second row, as the exact source still. No Slice 007 inference plan is accepted by this document; Slice 007 requires its own owner-approved implementation plan.

## Reopened Comparison Result

The owner reopened the comparison after primary-source review invalidated an earlier LTX disposition. Official LTX Desktop releases now support local LTX-2.5 Fast generation on Apple Silicon through MPS; LTX 2.5 Pro remains API-only. The corrected finding makes LTX-2.5 Fast a viable local alternative, but it does not displace Wan2.2 I2V-A14B for the first motion scout.

Wan remains the quality-first choice because it currently provides the cleaner and better-bounded evidence chain:

- Apache-2.0 model and prepared-package licensing;
- an exact official model revision and exact prepared-package revision;
- an exact 44-file, 68,791,046,058-byte BF16 package inventory;
- a pinned MLX-Gen source commit and PyPI wheel hash;
- explicit Apple Silicon and I2V parameter documentation;
- local-file-only generation behavior after a separate download;
- documented input-aspect-ratio resolution;
- published Apple M5 Max BF16 memory, process-footprint, and runtime evidence.

LTX-2.5 Fast is deferred to a separate license and runtime-evidence gate. Its Apple route is newly released beta software, its 22B weights are gated under the LTX-2.x Community License, and current primary sources do not publish a comparable pinned M5 Max resource, deterministic-repeat, or network-denied profile. The prior API-only rationale is explicitly withdrawn.

## Exact Selected References

Primary sources were rechecked on 2026-09-04. Revisions, inventories, licenses, releases, and runtime behavior remain drift-prone and must be rechecked before any Slice 007 download.

### Official model

- Repository: [`Wan-AI/Wan2.2-I2V-A14B-Diffusers`](https://huggingface.co/Wan-AI/Wan2.2-I2V-A14B-Diffusers/tree/596658fd9ca6b7b71d5057529bbf319ecbc61d74).
- Revision: `596658fd9ca6b7b71d5057529bbf319ecbc61d74`.
- License: Apache-2.0.
- Task: image-to-video through Diffusers.
- Inventory at the exact revision: 50 files and 126,204,155,463 bytes.
- Official Wan source reviewed at [`Wan-Video/Wan2.2`](https://github.com/Wan-Video/Wan2.2/tree/42bf4cfaa384bc21833865abc2f9e6c0e67233dc), commit `42bf4cfaa384bc21833865abc2f9e6c0e67233dc`.
- Official behavior: I2V-A14B supports 480P and 720P; its requested size is an area target and output aspect ratio follows the input image.

### Apple Silicon runtime

- Runtime: [`mlx-gen` 0.33.1](https://pypi.org/project/mlx-gen/0.33.1/).
- Runtime repository: [`lpalbou/mlx-gen`](https://github.com/lpalbou/mlx-gen/tree/23cee803f10aacdf943a9565f7cd67c25c825080).
- Source commit: `23cee803f10aacdf943a9565f7cd67c25c825080`.
- Wheel: `mlx_gen-0.33.1-py3-none-any.whl`.
- Wheel SHA-256: `1a19e6510a166cbe0fe4975146813fb61adf98f0e073abb4e63f27f012882d0a`.
- Runtime license: MIT.
- Version-pinned usage documentation: [`docs/wan-video.md`](https://github.com/lpalbou/mlx-gen/blob/23cee803f10aacdf943a9565f7cd67c25c825080/docs/wan-video.md).
- Version-pinned precision documentation: [`docs/quantization.md`](https://github.com/lpalbou/mlx-gen/blob/23cee803f10aacdf943a9565f7cd67c25c825080/docs/quantization.md).

MLX-Gen exposes Wan2.2 I2V-A14B on Apple Silicon, with `--guidance`, `--guidance-2`, `--flow-shift`, `--solver`, frame, fps, source-image, canvas-policy, low-RAM, metadata, LoRA, and cache-related controls. Image-to-video defaults to `source-aspect`: requested width and height are a size target, and the runtime resolves the nearest supported canvas from the input image ratio. Future execution must record the resolved dimensions and all effective parameters rather than assuming that requested values were honored.

Generation does not implicitly download missing model files. MLX-Gen requires a separate `download` or `prepare` operation and raises a download-required error when a requested local package is incomplete. Slice 007 must still implement exact-revision pinning, local resolution, and OS-level network-denial proof; library behavior alone is not offline evidence.

### Prepared BF16 package

- Repository: [`AbstractFramework/wan2.2-i2v-a14b-diffusers-bf16`](https://huggingface.co/AbstractFramework/wan2.2-i2v-a14b-diffusers-bf16/tree/ef2a0bfe5b4ca7edb84c93f1675edb1a8bfe7d60).
- Revision: `ef2a0bfe5b4ca7edb84c93f1675edb1a8bfe7d60`.
- License: Apache-2.0, following the source model.
- Inventory: exactly 44 files and 68,791,046,058 bytes, approximately 64.07 GiB.
- Precision: BF16 MLX-Gen saved-weight layout.
- Task: image-to-video.

The package is an MLX-Gen layout, not a Diffusers or Transformers `from_pretrained()` checkpoint. Its exact file allowlist must be copied into the separately approved Slice 007 download manifest before any download begins.

## Precision Decision

Use BF16. Do not substitute q8 merely to reduce memory.

The pinned MLX-Gen quantization documentation records a 2026-06-12 runtime-precision correction: Wan q8 transformer-block linears are dequantized to BF16 at load. Therefore q8 now saves download and disk space but does not provide a runtime-memory or speed reduction. BigBoy has sufficient planning capacity for the quality-first BF16 candidate, but capacity is not production acceptance.

## Reopened Alternatives

### Wan2.2 TI2V-5B

Retain as a smaller and faster fallback. MLX-Gen documents T2V and first-frame I2V support plus BF16 and q8 packages, but this route is not selected as the quality-first benchmark.

### LTX-2.5 Fast 22B distilled

Viable and deferred; the prior API-only rejection is obsolete.

- Model: gated [`Lightricks/LTX-2.5`](https://huggingface.co/Lightricks/LTX-2.5/tree/5e6e71018ee1756ed329b697a7b4aedc934dfce9) at `5e6e71018ee1756ed329b697a7b4aedc934dfce9`.
- Model license: LTX-2.x Community License Agreement, SHA-256 `be75acae5c99b0fb16ed6cfbf8f731e5121a729bef112d20337699407e796451` at runtime commit `a95ab856bf29407b6b066ede0abe1846050db56c`.
- Complete model repository: 17 files and 200,853,702,175 bytes.
- Minimum official fully local distilled set: five files and 71,114,917,404 bytes: BF16 distilled transformer, BF16 Gemma 4 text encoder, BF16 video VAE, BF16 audio VAE, and BF16 spatial upscaler.
- Apple runtime: [`Lightricks/LTX-Desktop`](https://github.com/Lightricks/LTX-Desktop/tree/68cd86c15e5fd25f56229ea63c0dbcb0338f7812), release `v1.2.7`, commit `68cd86c15e5fd25f56229ea63c0dbcb0338f7812`, Apache-2.0 application license.
- Source runtime: [`Lightricks/LTX-2`](https://github.com/Lightricks/LTX-2/tree/a95ab856bf29407b6b066ede0abe1846050db56c), commit `a95ab856bf29407b6b066ede0abe1846050db56c`.
- Current local capability: LTX-2.5 Fast T2V/I2V/A2V on Apple Silicon through MPS; a local text encoder makes the path fully local without an API key. LTX-2.5 Pro remains API-only.

The custom model license permits covered use below its revenue threshold but carries use, redistribution, derivative, disclosure, and update-sensitive acceptable-use terms. It is less predictable than Apache-2.0 for a future globally published workflow and requires a separate legal review before production use. Runtime eligibility also does not prove BigBoy performance: the public 15 GB free-RAM floor is a routing threshold, not a peak-memory or output-quality measurement. Release `v1.2.7` fixed a Mac local-denoise memory spike, showing that this Apple path is still operationally young.

LTX-2.5 Fast should be reconsidered only through a separate exact slice that pins the gated files, model terms, desktop or source runtime, parameter mapping, local text encoder, MPS safety instrumentation, deterministic acceptance, and network-denial plan. Slice 006 does not turn the reopened comparison into a multi-model bake-off.

### HunyuanVideo-1.5

Reject for this slice. The official repository at reviewed commit `60783e704160023913bee78f0b47036d393d4dfa` supports T2V and I2V, but its published runtime requires Linux, NVIDIA, and CUDA. Its Tencent Hunyuan Community License excludes the European Union, United Kingdom, and South Korea from the licensed territory, making predictable global publication unsuitable.

### Mochi 1 Preview

Reject for this slice. The official repository at reviewed commit `0c86aebf386e6622deadfb47ff1996878cefc0ac` is Apache-2.0, but Mochi remains an older T2V-only research preview. The official implementation recommends H100-class hardware and provides neither first-frame conditioning nor a proven native Apple Silicon route comparable to the selected path.

### FLF2V, trajectory control, VACE, and related forks

Defer. No reviewed candidate presently combines flagship quality, acceptable provenance and licensing, and a comparably verified native Apple Silicon runtime. This disposition does not claim that the techniques are incapable; it says the exact evidence chain required by this project is incomplete.

## Source-Still Selection Gate

The only allowed source is the byte-identical Slice 005 result pair:

- `outputs/slice-005/wan-14b-online-seed-42.mp4`
- `outputs/slice-005/wan-14b-offline-seed-42.mp4`

Both files were rechecked on 2026-09-04:

- SHA-256: `ce7a61c21ef0811062ea6229b3ddf89c6843bdc6569234cab060915bd39f2ad4`;
- size: 708,216 bytes;
- H.264, `yuv420p`, 832×480;
- 81 frames at 16 fps;
- 5.0625 seconds;
- byte-identical online/offline content.

Six clean still candidates were extracted from the online-named copy. Because the source MP4s are byte-identical, either copy represents the same bytes. The candidate files and contact sheet are local and Git-ignored under `outputs/slice-006/source-still-candidates/`.

Exact extraction command:

```sh
ffmpeg -hide_banner -loglevel error -i outputs/slice-005/wan-14b-online-seed-42.mp4 -vf "select='eq(n,0)+eq(n,16)+eq(n,32)+eq(n,48)+eq(n,64)+eq(n,80)'" -fps_mode vfr outputs/slice-006/source-still-candidates/sample-%02d.png
```

The samples were renamed monotonically to the candidate paths below without changing their bytes. Contact sheet command:

```sh
ffmpeg -y -hide_banner -loglevel error -framerate 1 -pattern_type glob -i 'outputs/slice-006/source-still-candidates/candidate-*.png' -vf 'scale=416:240,tile=3x2' -frames:v 1 outputs/slice-006/source-still-candidates/contact-sheet.png
```

Contact sheet order is left-to-right: A–C on the top row, D–F on the bottom row.

| Candidate | Zero-based frame | Timecode | SHA-256 |
| --- | ---: | --- | --- |
| A | 0 | `00:00:00.000` | `8c38d38a1a0a64aa66fd3ea9323ad4ef79e9e276c95663a6a9b6c7c6af34f299` |
| B | 16 | `00:00:01.000` | `ede310f9423fdc3a7bcc70a75f4523768e0dac37a9dfd8e0022cf5a5ae7b4388` |
| C | 32 | `00:00:02.000` | `bbf50425e086d8dd4689146bb77eb0a2cc368a9f55bf8e6af5a92f449abc1aa0` |
| D | 48 | `00:00:03.000` | `7e7f0a20ebaa62551cad700d7e17fecd0fdc68a7003c9e1eb2e846f7fd6ec0c7` |
| E | 64 | `00:00:04.000` | `3d32f50e2d49073dac33e09ef3bc1c930daa9970e9213afcb8922074448d85c1` |
| F | 80 | `00:00:05.000` | `dd63430af36a10a796ab4a753d6e20a0e535f1e7687a3331747dba6d77dcf53f` |

All candidates are 832×480 and show the same accepted ancient Aegean silhouette: bow right, stern left, one mast, one rectangular square sail, stable horizon and composition, no text, watermark, or modern object, and no forward wake embedded in the still.

The owner selected candidate D, described as the left image in the second row. Its pinned provenance is:

- local path: `outputs/slice-006/source-still-candidates/candidate-d-frame-048.png`;
- SHA-256: `7e7f0a20ebaa62551cad700d7e17fecd0fdc68a7003c9e1eb2e846f7fd6ec0c7`;
- dimensions: 832×480;
- source video SHA-256: `ce7a61c21ef0811062ea6229b3ddf89c6843bdc6569234cab060915bd39f2ad4`;
- zero-based frame: 48;
- timecode: `00:00:03.000`.

The selected image remains local and Git-ignored. It is not committed.

## Frozen Future Prompts

Positive prompt, stored verbatim:

> Single continuous five-second shot, locked-off wide side view. A Late Bronze Age Aegean galley with a long black hull, curved prow and stern, one mast and one rectangular square sail moves steadily from left to right across a dark wine-colored sea before dawn. The bow always points right; the stern remains left. Moderate wind blows from left to right, naturally filling the sail and raising aligned wavelets. A small bow wave splits outward at the prow; a narrow foamy wake begins only behind the stern and trails leftward. Heavy purple clouds drift slowly. Stable geometry, physically coherent motion, no camera movement, text, or modern objects. Preserve the approved input image’s ship design, palette, atmosphere, framing, and horizon.

Negative prompt, stored verbatim:

> reverse playback, backward sailing, wake or foam ahead of the bow, wake extending forward, perfectly still water with a filled sail, deformed sail, changing hull geometry, extra mast, camera dolly, pan, zoom, text, watermark, modern vessel, blurry image, JPEG artifacts

## Future Slice 007 Motion Scout

The next executable slice is `slice-007-wan-2.2-i2v-a14b-motion-scout`. It may authorize the exact runtime installation, model download, prepared-package verification, and one low-cost inference only after a separate owner-approved implementation plan.

Freeze this proposed scout configuration:

- exact model, package, runtime, revisions, prompts, and selected source still declared here;
- BF16 precision and sequential execution only;
- requested 448×256 canvas using the source-aspect policy;
- record resolved width and height before generation;
- 41 frames at 8 fps, approximately 5.1 seconds;
- 15 denoising steps;
- seed 42;
- guidance 4.0;
- guidance-2 3.0;
- flow shift 3.0;
- UniPC solver;
- low-RAM mode and metadata enabled;
- no LoRA, Lightning adapter, prompt extension, cache acceleration, video-to-video input, parallel process, cloud service, or API key;
- local files only after the separately authorized and recorded download;
- record every requested and effective runtime parameter.

### Scout hard gates

All must pass:

- bow remains right and stern remains left;
- ship moves continuously left to right;
- wake starts only behind the stern and trails leftward;
- a small bow wave begins at the prow and does not resemble a forward wake;
- water movement is consistent with the wind and filled sail;
- sail does not deform;
- ship, mast, hull, horizon, and camera remain stable;
- no text, watermark, modern object, unsafe content, or major visual collapse appears.

Any failure rejects the route. It authorizes no seed sweep, prompt tuning, parameter tuning, alternate sampler, LoRA experiment, unplanned rerun, or full-resolution render.

## Later Full Benchmark

Only after explicit owner acceptance of the motion scout, define a later full benchmark with the exact same model, runtime, package, selected still, prompts, seed, guidance values, flow shift, solver, and BF16 precision.

- requested 832×480 output under documented source-aspect resolution;
- record resolved dimensions;
- 81 frames;
- 16 fps;
- 40 steps;
- complete effective-runtime, memory, swap, disk, thermal, decode, metadata, and SHA-256 evidence.

Run the network-denied repeat only after the online-capable full output passes human quality review.

## Offline Proof Contract

Before future inference, freeze:

- an exact allowlisted model inventory;
- a separately recorded download operation;
- local model resolution after download;
- `HF_HUB_OFFLINE`, `TRANSFORMERS_OFFLINE`, and `DIFFUSERS_OFFLINE`;
- local-files-only behavior;
- macOS deny-network sandbox;
- loopback-bind denial preflight;
- full video decode;
- media-property verification;
- SHA-256 comparison.

Require byte-identical output unless primary runtime documentation proves before inference that this backend cannot provide byte identity and the slice defines a narrower deterministic acceptance criterion. The proof must not be weakened after results are visible.

## Resource and Safety Plan

Published BF16 I2V evidence on Apple M5 Max, recorded separately from estimates:

- 384×384;
- 33 frames;
- 12 steps;
- 8 fps;
- approximately 28.2 GiB MLX peak;
- approximately 31.8 GiB maximum RSS;
- approximately 33.7 GiB full-process physical peak;
- approximately 228.2 seconds.

This profile is not a guarantee for 832×480.

Conservative full-run planning estimate:

- MLX peak: 35–60 GB;
- process footprint: 50–90 GB;
- expected swap: zero;
- runtime: 1–3.5 hours;
- confidence: low;
- maximum permitted runtime: four hours.

Future preflight requires at least 90% system memory free, zero swap, no other model-inference process, no parallel execution, no thermal or performance warning, at least 180 GiB free disk before download or package preparation, and at least 120 GiB free disk before inference.

Future automatic stops trigger when memory free reaches 10%, swap exceeds 8 GiB, free disk falls below 100 GiB, thermal state becomes serious or critical, a performance warning appears, no denoising progress occurs for 20 consecutive minutes, an undeclared network or file request occurs, the process exits unexpectedly, or elapsed runtime exceeds four hours.

## Authority and Completion Boundary

Slice 006 is complete after pinning the owner-selected source still and passing final verification and closeout. The selected route is a benchmark candidate, not a production model. Slice 004 remains postponed without deletion or renumbering.

No model weights, generated video, candidate still, contact sheet, runtime installation, or model cache may be committed. No Memory Core promotion is authorized.
