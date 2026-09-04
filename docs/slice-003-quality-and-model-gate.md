---
project: Living Literature
document: quality-and-model-gate
status: complete
verified: 2026-09-03
slice: slice-003-quality-and-model-gate
---

# Slice 003 — Quality and Model Gate

## Decision

Accept **Wan2.1-T2V-14B through the pinned Apple MLX implementation, with 8-bit DiT quantization**, as the single next model/workflow to benchmark on BigBoy.

This accepts one bounded experiment, not a production model. No 14B weights were downloaded and no inference ran in Slice 003.

The decision is not based on memory capacity alone. It is the lowest-confound test of the unresolved Slice 002 question: whether greater model capacity can improve Bronze Age Greek specificity and directed sail motion while preserving the atmosphere and temporal coherence already demonstrated by 1.3B. It keeps the same task, prompt, geometry, frame count, sampler, seed, and Apple-native implementation. Wan I2V offers stronger control, but it first needs a rights-cleared and historically reviewed source still; LTX 2.5 changes the runtime, license, and output envelope simultaneously.

The future benchmark is assigned **Slice 005**. The existing `Slice-004-Rights-Ledger-Foundation` remains unchanged and is still the next numbered slice.

## Evidence Boundary

### Verified Slice 002 facts

- `Wan-AI/Wan2.1-T2V-1.3B` revision `37ec512624d61f7aa208f7ea8140a131f93afc9a` and Apple `mlx-examples` revision `796f5b53cab69a3d48a44233ce21aae889e94a08` produced byte-identical online-capable and network-denied outputs.
- The offline run took 2,200.93 seconds of inference and 2,222 seconds wall-clock.
- MLX peak memory was 25.693 GB; peak process footprint was approximately 68.3 GB; minimum observed free memory was 56%; swap and warning count were zero.
- The clip passed atmosphere, composition, restrained motion, and forbidden-content checks. It only partially passed ship specificity and wind-driven sail motion.

### Current primary-source snapshot

Accessed 2026-09-03. Repository revisions and file inventories are drift-prone and must be rechecked before any future download.

- Wan T2V 14B model: `Wan-AI/Wan2.1-T2V-14B` at `a064a6c71f5be440641209c07bf2a5ce7a2ff5e4`; [model card](https://huggingface.co/Wan-AI/Wan2.1-T2V-14B/tree/a064a6c71f5be440641209c07bf2a5ce7a2ff5e4), [Apache-2.0 license](https://huggingface.co/Wan-AI/Wan2.1-T2V-14B/blob/a064a6c71f5be440641209c07bf2a5ce7a2ff5e4/LICENSE.txt), license SHA-256 `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4`.
- Wan I2V 14B model: `Wan-AI/Wan2.1-I2V-14B-480P` at `6b73f84e66371cdfe870c72acd6826e1d61cf279`; [model card](https://huggingface.co/Wan-AI/Wan2.1-I2V-14B-480P/tree/6b73f84e66371cdfe870c72acd6826e1d61cf279), [Apache-2.0 license](https://huggingface.co/Wan-AI/Wan2.1-I2V-14B-480P/blob/6b73f84e66371cdfe870c72acd6826e1d61cf279/LICENSE.txt), license SHA-256 `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4`.
- LTX candidate: `Lightricks/LTX-2.5` at `5e6e71018ee1756ed329b697a7b4aedc934dfce9`; [gated model repository](https://huggingface.co/Lightricks/LTX-2.5/tree/5e6e71018ee1756ed329b697a7b4aedc934dfce9), [LTX-2.x Community License](https://github.com/Lightricks/LTX-2/blob/a95ab856bf29407b6b066ede0abe1846050db56c/LICENSE-2_x), license SHA-256 `be75acae5c99b0fb16ed6cfbf8f731e5121a729bef112d20337699407e796451`.
- LTX Apple runtime: `Lightricks/ltx-desktop` at `68cd86c15e5fd25f56229ea63c0dbcb0338f7812`; [source](https://github.com/Lightricks/ltx-desktop/tree/68cd86c15e5fd25f56229ea63c0dbcb0338f7812), Apache-2.0 for the application, with separate model terms.
- Deterministic animation runtime: installed FFmpeg 9.0.1, upstream tag `n9.0.1` at commit `bf1b838f2ab88b4f8fd83443325c782ea0e0f7fa`; the installed Homebrew build is GPLv3 because GPL components are enabled.
- Apple Wan runtime: pinned local submodule `mlx-examples` at `796f5b53cab69a3d48a44233ce21aae889e94a08`, MIT licensed.

Upstream quality claims are self-reported planning evidence, not proof for the Living Literature prompt. Only a measured BigBoy run can establish resource use and quality.

## Options

### 1. Stop local text-to-video work

**Decision:** rejected now; retain as the failure outcome if Slice 005 does not materially improve quality inside the resource boundary.

- Repository/revision and license: not applicable.
- Runtime files/download: none.
- Compatibility/source changes: none.
- Resource expectation: none.
- Quality outlook: deterministic avoidance of further cost, but it abandons an already proven local and repeatable atmosphere workflow before testing the directly supported larger model.
- Principal risk: stopping on evidence from only the smallest candidate would leave the BigBoy ceiling uncharacterized.

### 2. Wan2.1 T2V 14B

**Decision:** accepted for Slice 005.

- Repository/revision: `Wan-AI/Wan2.1-T2V-14B` at `a064a6c71f5be440641209c07bf2a5ce7a2ff5e4`.
- License: Apache-2.0; exact license SHA-256 `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4`. The model card claims no rights over generated content and makes the user accountable for lawful, non-harmful use. Project rights review remains separate for prompts, references, outputs, and publication.
- Required runtime files: the safetensors index and six DiT shards, `Wan2.1_VAE.pth`, `models_t5_umt5-xxl-enc-bf16.pth`, and `google/umt5-xxl/tokenizer.json`.
- Verified current file total: **69,040,541,912 bytes (64.299 GiB)** across ten runtime files. License and model-card files add only small metadata overhead. Network transfer may vary with cache deduplication; disk planning must reserve the full total plus temporary and output margin.
- Pinned Apple compatibility: direct. The pinned source declares `t2v-14B`, its six-shard index layout, 8-bit quantization, UniPC, TeaCache, and cache disabling.
- Required changes for Slice 005: add a 14B allowlisted downloader, exact-revision guards for every Hugging Face request, a separate immutable benchmark manifest and runner, descendant-process sampling, and a verifier. No dependency-family change is expected.
- Precision/cache assumptions for the accepted workflow: Apple pipeline defaults; 8-bit MLX quantization of the DiT after loading; no TeaCache; Metal buffer cache disabled; no explicit offloading path; sequential T5/DiT release as implemented.
- Published planning figures: Apple reports about 36 GB unquantized RAM and about 230 seconds per DiT step on M4 Max for 81 frames. These are not M5 Max measurements and do not include the Slice 002 wrapper's process-footprint semantics.
- Estimated BigBoy envelope: **35–55 GB MLX peak**, **75–110 GB peak process footprint**, and **1.5–3.0 hours inference per run** at the fixed 50 steps. The lower runtime anchor is 2,200.93 seconds multiplied by Apple's published M4 step-time ratio, `230/90`, which gives approximately 5,625 seconds; the wider range covers quantization, cache, thermal, and measurement differences. Confidence is low-to-medium until measured.
- Likely improvement: higher capacity may improve prompt semantics, detail, motion dynamics, and object fidelity while preserving a direct comparison to the baseline.
- Principal risks: 8-bit quantization may reduce quality; the model may still produce generic historic imagery; full process footprint can be much larger than the MLX counter; runtime may be operationally poor; quantization occurs after model construction, so transient load behavior is not proven by the steady-state estimate.

### 3. Wan2.1 I2V 14B 480P

**Decision:** viable, deferred.

- Repository/revision: `Wan-AI/Wan2.1-I2V-14B-480P` at `6b73f84e66371cdfe870c72acd6826e1d61cf279`.
- License/material restrictions: Apache-2.0 with license SHA-256 `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4`, plus the same model-card responsibility statement. The conditioning still has its own copyright, provenance, and editorial boundary.
- Required runtime files: the safetensors index and seven DiT shards, VAE, T5, tokenizer, and CLIP vision encoder.
- Verified current file total: **82,238,491,725 bytes (76.591 GiB)** across twelve runtime files.
- Pinned Apple compatibility: direct `i2v-14B` support at 832×480, 81 frames, 40 steps, guidance 5.0, shift 3.0, 4/8-bit quantization, and optional cache controls.
- Required changes: a separate allowlisted downloader and I2V runner/verifier plus an exact, hashed, rights-cleared, historically reviewed input still. No new dependency family is expected.
- Precision/offloading/cache assumptions considered: 8-bit DiT, no TeaCache, disabled Metal cache, no explicit offloading, default bfloat16 pipeline compute.
- Published planning figures: Apple reports about 39 GB unquantized RAM and about 250 seconds per DiT step on M4 Max for 81 frames.
- Estimated BigBoy envelope: **40–60 GB MLX peak**, **80–115 GB peak process footprint**, and **1.4–3.0 hours inference per 40-step run**, all low-confidence estimates.
- Likely improvement: the input frame can lock ship silhouette, palette, and composition more directly than text alone.
- Principal risks: a poor or uncleared still contaminates the test; image adherence may suppress desired motion; it changes both model capacity and conditioning, so it cannot isolate why quality changed.

### 4. LTX-family candidate: LTX 2.5 Fast 22B distilled

**Decision:** viable on paper, deferred.

- Model repository/revision: gated `Lightricks/LTX-2.5` at `5e6e71018ee1756ed329b697a7b4aedc934dfce9`.
- Runtime repository/revision: `Lightricks/ltx-desktop` at `68cd86c15e5fd25f56229ea63c0dbcb0338f7812` or `Lightricks/LTX-2` at `a95ab856bf29407b6b066ede0abe1846050db56c`.
- License/material restrictions: the runtime is Apache-2.0; the model uses the LTX-2.x Community License dated 2026-08-11, verified at SHA-256 `be75acae5c99b0fb16ed6cfbf8f731e5121a729bef112d20337699407e796451`. It requires a paid license for entities with at least USD 10 million annual revenue except bounded non-commercial uses, incorporates a changeable acceptable-use policy, requires machine-generated disclosure, imposes use restrictions, and gates repository access behind account acceptance. These terms require legal review before publication or commercial use.
- Fully local minimum file set from the official LTX 2.5 instructions: distilled bf16 transformer, Gemma 4 text encoder, video VAE, audio VAE, and spatial upscaler.
- Verified current file total: **71,114,917,404 bytes (66.231 GiB)**. Optional alternative VAE, duration head, prompt enhancer, and LoRAs add more.
- Pinned Apple compatibility: none with the project's Apple MLX submodule. Current LTX Desktop instead documents local Apple Silicon execution through PyTorch MPS.
- Required changes: a new pinned source/dependency stack, gated-access procedure, exact download manifest, local-text-encoder configuration, offline/network-denial proof, MPS-specific resource instrumentation, and a new parameter mapping.
- Precision/offloading/cache assumptions: bf16 transformer and text encoder on MPS; no FP8 path on Darwin. LTX Desktop streams from disk below its full-resident threshold and selects full residency at at least 85 GiB free RAM. Its source explicitly marks the Darwin full-resident tier unverified on real hardware.
- Expected BigBoy working set: approximately **74–100+ GiB** including weights, VAE/latents, allocator/driver overhead, and the application. This is a source-informed estimate, not a BigBoy measurement.
- Runtime relative to Slice 002: unknown. Official current sources provide no comparable M5 Max benchmark, so no numeric speed claim is safe.
- Likely improvement: higher native output resolution, explicit camera-motion and multi-keyframe capabilities, and a newer 22B family.
- Principal risks: restrictive and drift-prone license terms, gated access, large new integration surface, unmeasured full-resident MPS behavior, non-comparable resolution/frame semantics, and possible fallback to cloud features unless configured fail-closed.

### 5. Deterministic camera animation over a generated still

**Decision:** viable fallback, deferred.

- Runtime/revision: FFmpeg 9.0.1, upstream tag `n9.0.1` at `bf1b838f2ab88b4f8fd83443325c782ea0e0f7fa`.
- License/material restrictions: the installed build reports GPLv3 because GPL components are enabled. The source still and every element used to make it retain separate provenance and rights requirements.
- Runtime files/download: no model weights; the required creative input is one rights-cleared high-resolution still. The needed FFmpeg runtime is already installed.
- Compatibility/source changes: independent of Apple MLX; implement a deterministic `zoompan`/crop/overlay render manifest and verify the encoded output.
- Precision/quantization/offloading/cache: not applicable.
- Expected working set/runtime: well below the model options and plausibly minutes rather than hours, but exact figures require a measured render at the selected still resolution.
- Likely improvement: strongest composition, historical-detail, and camera-path control.
- Principal risks: it cannot create convincing independent sail, water, cloth, or character motion without additional authored layers; a single still may feel like a slideshow; the still-generation workflow remains an unsolved model and rights decision.

## Why T2V 14B Wins This Gate

Wan T2V 14B is the only option that changes one central variable—model capacity—while holding the proven local workflow and benchmark semantics substantially constant. Its exact revision and runtime inventory are public, its Apache-2.0 boundary is simpler than LTX's, and the pinned Apple source already implements it. The benchmark is expensive but bounded, and its failure would be informative: if it cannot turn the two Slice 002 partial scores into passes without exceeding the resource ceiling, further local pure T2V work should stop rather than enter a tuning loop.

Wan I2V remains the strongest later controllability candidate, but only after the rights ledger and a controlled source still exist. Deterministic animation remains the low-resource fallback. LTX 2.5 deserves a separate future decision only if Wan 14B fails and the owner accepts its license and integration costs.

## Decision Status

- Accepted next test: Wan2.1-T2V-14B, 8-bit DiT, Slice 005.
- Production model: not accepted.
- Slice 004: unchanged; Rights Ledger Foundation remains next.
- Weights downloaded in Slice 003: none.
- Inference in Slice 003: none.
