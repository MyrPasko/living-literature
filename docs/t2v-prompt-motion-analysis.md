---
project: Living Literature
document: t2v-prompt-motion-analysis
status: recorded-for-future-slices
created: 2026-09-04
source_slice: slice-005-wan-2.1-t2v-14b-benchmark
---

# T2V Prompt and Motion Analysis

## Outcome

The Slice 005 prompt was valid for a controlled capacity benchmark but under-specified for an expensive production-oriented motion shot. Reusing the exact Slice 002 prompt correctly isolated the change from Wan2.1 T2V 1.3B to 14B. The resulting 14B output materially improved image quality, color, atmosphere, and composition, but it did not establish physically coherent ship motion.

The owner judged the image quality and colors fully satisfactory and highlighted the sky as especially successful. The same playback review found two decisive motion defects:

- the square sail appears filled while the sea surface reads as nearly calm; and
- the foamy trail appears ahead of the vessel instead of remaining behind the stern, creating the impression of reverse playback.

The current result should therefore record a strong visual-quality pass and a motion-physics failure. Offline reproducibility, if proven, will show that the same deterministic configuration reproduces the defect; it will not convert the output into an accepted production shot.

## Experimental Interpretation

There was no benchmark-design error in preserving the 34-word prompt, seed, geometry, frame count, sampler, and core conditioning values from Slice 002. That design tested the capacity hypothesis with limited confounding.

There was, however, a production-prompt gap. The prompt described the desired image and mood more precisely than the causal motion:

| Dimension | Existing prompt signal | Missing control |
| --- | --- | --- |
| Entity | Black ancient Greek ship | More specific hull, mast, sail, bow, and stern geometry |
| Scene | Wine-colored sea, pre-dawn light, heavy clouds | Nothing material; this dimension succeeded |
| Ship motion | `crosses` | Screen direction, bow/stern orientation, speed, and continuity |
| Wind | `cold wind moving the square sail` | Strength, direction, and a causal relationship to sail and water |
| Water | No explicit hydrodynamic description | Bow wave origin, stern wake origin, wake direction, and surface response |
| Camera | `cinematic wide shot` | Fixed versus tracking camera and prohibited camera motion |
| Realism | `restrained realistic motion` | Concrete observable constraints instead of an abstract quality request |
| Negative conditioning | Text, watermarks, blur, and JPEG artifacts | Reverse motion, forward wake, backward sailing, inconsistent water, and camera drift |

The model strongly satisfied the well-specified aesthetic dimensions and invented the under-specified motion relationships. This is consistent with a video generator producing plausible learned visual patterns rather than running a wind and fluid dynamics simulation.

## Parameter Assessment

The observed reverse-motion defect is not evidence that the core sampling parameters were wrong:

- 50 denoising steps, guidance 5.0, shift 5.0, and UniPC are standard Wan2.1 T2V values in the upstream implementation;
- adding denoising steps would refine a sample but would not teach the model which side is the stern;
- the fixed seed may represent an unlucky motion sample, but one output cannot isolate seed sensitivity;
- 8-bit DiT quantization may affect quality, but the current evidence does not attribute the directional error to quantization; and
- Metal-cache disabling changes resource behavior, not prompt semantics.

Any future attempt to isolate seed, quantization, guidance, shift, sampler, or step count must change only one variable at a time. A prompt rewrite must not be combined with several sampling changes and then treated as causal evidence.

## Official Prompting Evidence

The official Wan prompt guide describes an advanced prompt as:

`Entity description + Scene description + Motion description + Aesthetic control + Stylization`

It recommends describing motion amplitude, speed, and effect, and specifying camera movement or a fixed camera. The Wan2.1 prompt-extension system separately instructs its text model to strengthen spatial relationships, motion, natural actions, and camera behavior, using simple direct verbs and an approximately 80–100-word English result.

Primary references reviewed on 2026-09-04:

- [Alibaba Cloud Wan text-to-video and image-to-video prompt guide](https://www.alibabacloud.com/help/en/model-studio/text-to-video-prompt)
- [Wan2.1 prompt-extension implementation](https://github.com/Wan-Video/Wan2.1/blob/main/wan/utils/prompt_extend.py)
- [Wan2.1 official repository and local prompt-extension options](https://github.com/Wan-Video/Wan2.1)
- [Wan2.1 upstream T2V sampling implementation](https://github.com/Wan-Video/Wan2.1/blob/main/wan/text2video.py)
- pinned Apple MLX usage and parameter surface: `third_party/mlx-examples/video/wan2.1/README.md`

The current Alibaba prompt guide also documents newer hosted Wan generations. Future slices may use its general prompt structure and motion vocabulary, but must not assume that newer API-only controls exist in the pinned Wan2.1 Apple MLX implementation.

## Proposed Positive Prompt

This is a reviewed candidate for a future slice, not an authorized replacement for the immutable Slice 005 benchmark prompt:

> Single continuous five-second shot, locked-off wide side view. A Late Bronze Age Aegean galley with a long black hull, curved prow and stern, one mast and one rectangular square sail moves steadily from left to right across a dark wine-colored sea before dawn. The bow always points right; the stern remains left. Moderate wind blows from left to right, naturally filling the sail and raising aligned wavelets. A small bow wave splits outward at the prow; a narrow foamy wake begins only behind the stern and trails leftward. Heavy purple clouds drift slowly. Stable geometry, physically coherent motion, no camera movement, text, or modern objects.

The prompt makes the intended causal chain observable:

1. The bow remains on the right and the stern on the left.
2. The ship moves continuously from left to right.
3. The wind direction is explicit and fills the sail.
4. The same wind produces visible surface response.
5. A small bow wave splits at the prow.
6. A separate wake begins behind the stern and trails leftward.
7. The camera is locked, preventing camera motion from masking object direction.

## Proposed Negative Prompt

This is also a future-slice candidate, not an active configuration change:

> reverse playback, backward sailing, wake or foam ahead of the bow, wake extending forward, perfectly still water with a filled sail, deformed sail, changing hull geometry, extra mast, camera dolly, pan, zoom, text, watermark, modern vessel, blurry image, JPEG artifacts

Positive causal statements remain primary. Negative prompting can reduce an unwanted pattern but is not a hard spatial or physical constraint.

## Future Slice Gate

A future prompt-and-motion slice should avoid paying full-render cost before obvious direction errors are screened:

1. Review the candidate prompt against entity, scene, motion, aesthetic/camera, and style dimensions.
2. Require explicit object orientation, movement direction, environmental response, and camera behavior.
3. Freeze the reviewed positive and negative prompts before inference.
4. Run one low-cost 14B motion scout, provisionally 33 frames and 20 steps at 832x480 with the current 8-bit model and a declared seed. These values are a planning proposal and require their own authorization and safety estimate.
5. Judge only direction, wake placement, wind/water consistency, sail motion, camera stability, and gross geometry in the scout. Do not use it for final image-quality acceptance.
6. Run the full 81-frame, 50-step candidate only after the scout passes every motion gate.
7. Run the network-denied duplicate only after the first full output passes human quality review.
8. If a causally explicit prompt still fails, stop further pure T2V prompt tuning and open a decision gate for stronger conditioning such as I2V, first/last-frame video, trajectory control, or deterministic compositing.

Prompt extension may prepare a draft locally, including through a separately approved local text model, but the final English prompt must be human-reviewed and stored verbatim. No cloud service or API key may become a project dependency.

## Future Cross-Model Comparison

The owner requested a later comparison of other flagship video models under analogous conditions. This must be a separate decision and benchmark sequence after Slice 005 closes; it is not authorization to download or run another model now.

The future decision gate should refresh a candidate shortlist from primary sources. Candidate families may include Wan2.2 A14B, the then-current open HunyuanVideo release, Mochi, and LTX, but no exact checkpoint is selected by this document. Each candidate must have an exact repository and revision, license review, runtime-file allowlist, download size, Apple Silicon execution path, memory estimate, and explicit local-only proof plan before approval.

The comparison should preserve these dimensions where the model supports them:

- the same scene semantics and human-reviewed causal motion requirements;
- one continuous approximately five-second shot;
- approximately 480p output and the nearest supported frame count and frame rate;
- a declared seed and deterministic repeat where supported;
- the same visual, historical, motion, forbidden-content, and physical-coherence rubric; and
- runtime, peak model/process memory, swap, thermals, disk, decode, and offline evidence.

Model-native sampling requirements must not be forced into false equivalence. Sampler, step count, guidance, precision, quantization, and conditioning differences must be declared rather than hidden. Quality should be compared at each model's documented practical local configuration, with deviations listed next to the results.

Each model should proceed sequentially through metadata review, a low-cost motion scout, human review, one full candidate run, and only then a network-denied repeat. BigBoy concurrency is not assumed safe or beneficial; parallel 14B-class inference requires its own measured concurrency gate.

## Authority Boundary

This document records analysis for later implementation. It does not:

- change the immutable Slice 005 benchmark;
- authorize another inference run, seed sweep, prompt-tuning loop, model download, or runtime substitution;
- select or authorize any model in the future cross-model candidate families;
- accept Wan2.1 T2V 14B as a production model;
- authorize I2V, FLF2V, trajectory-control, or deterministic-animation implementation; or
- promote any project memory automatically.
