---
task_id: slice-005-wan-2.1-t2v-14b-benchmark
task_type: feature
status: complete-model-rejected
branch: slice-005-wan-2.1-t2v-14b-benchmark
date: 2026-09-04
write_scope:
  - /Users/myroslavpasko/projects/living-literature
  - /Users/myroslavpasko/obsidian/Docs/CLAUDE_KASSANDRA/Projects/Living-Literature
forbidden_moves:
  - any model other than the exact authorized Wan2.1 T2V 14B revision
  - prompt tuning, seed sweep, image-to-video, or multi-model bake-off
  - cloud inference or API-key path
  - tracked weights, generated media, detailed runtime logs, or secrets
  - publication or production-model acceptance without passing quality gates
  - automatic Memory Core promotion
verification_surface:
  - exact model revision, file inventory, sizes, hashes, and license
  - fixed benchmark parameters and immutable runner commit
  - online-capable and OS-network-denied local inference
  - runtime, MLX/process memory, swap, disk, and thermal observations
  - MP4 metadata, full decode, SHA-256, and byte identity
  - owner playback review and representative-frame inspection
  - repository safety, deterministic verifier, and Memory Core audit
success_criteria:
  - complete the bounded investigation and record either acceptance or measured rejection
slice_restrictions:
  - Slice 004 remains postponed and is not deleted or renumbered
---

# Implementation Result

## Outcome

Slice 005 is complete as a measured rejection. BigBoy successfully ran the exact Wan2.1 T2V 14B model locally twice, including a network-denied repeat, within every resource and runtime gate. The two H.264 outputs are byte-identical. The model demonstrated excellent image quality, color, atmosphere, and a plausible ancient single-mast silhouette, but failed hard motion gates: wind, water, sail, and wake direction were not physically coherent.

Wan2.1 T2V 14B is not accepted as the production model for this shot. The failed quality decision does not invalidate the successful local-capability and offline-reproducibility evidence.

## Exact References

- Model: `Wan-AI/Wan2.1-T2V-14B` at `a064a6c71f5be440641209c07bf2a5ce7a2ff5e4`.
- Model license: Apache-2.0, captured and hashed at the exact revision.
- Apple implementation: `mlx-examples/video/wan2.1` at `796f5b53cab69a3d48a44233ce21aae889e94a08`.
- Immutable successful-run commit: `715b073ff1d6734d5652667b7361813735da9510`.
- Parameters: `benchmarks/slice-005-wan-2.1-t2v-14b.json`.
- Model inventory: `manifests/models/wan2.1-t2v-14b.json`.
- Results: `manifests/benchmarks/slice-005-wan-14b-results.json`.
- Prompt and motion analysis: `docs/t2v-prompt-motion-analysis.md`.
- External model store: `~/models/huggingface/hub`; Ollama remained untouched.

## Changes Made

- Downloaded only the ten authorized runtime files plus license and model-card evidence into the external model store.
- Recorded and verified 69,040,541,912 runtime bytes (64.299 GiB) and exact SHA-256 hashes.
- Added exact-revision download, guarded run, safety-wrapper, and deterministic verification scripts.
- Ran the fixed 832x480, 81-frame, 50-step, seed-42 benchmark with 8-bit DiT, UniPC, guidance 5.0, shift 5.0, TeaCache disabled, and Metal cache disabled.
- Repeated the benchmark with Hugging Face offline flags, local-only resolution, macOS network denial, and a successful socket-bind denial preflight.
- Recorded identical media, runtime, memory, swap, disk, thermal, and process evidence.
- Performed owner normal-speed review and representative-frame inspection.
- Added an English prompt/motion analysis and a non-authorizing future cross-model comparison boundary.

## Benchmark Evidence

- Online-capable run: 13,061 seconds wrapper wall time; 13,055.32 seconds inference; 29.722 GB MLX peak; 39,442,448,384-byte maximum resident set; 39,402,631,560-byte peak footprint; 84% minimum observed free memory; zero swap; no warning.
- Offline network-denied run: 12,038 seconds wrapper wall time; 12,017.43 seconds inference; 29.722 GB MLX peak; 39,438,303,232-byte maximum resident set; 39,400,599,944-byte peak footprint; 85% minimum observed free memory; zero swap; no warning.
- Both runs remained below the four-hour limit and triggered no safety stop.
- Both outputs: H.264, 832x480, 81 frames, 16 fps, 5.0625 seconds, 708,216 bytes.
- Both outputs: SHA-256 `ce7a61c21ef0811062ea6229b3ddf89c6843bdc6569234cab060915bd39f2ad4`.
- Full decode: pass for both outputs.
- Offline network-denial preflight: pass.

## Quality Evidence

- **Image quality and color — pass:** the owner was fully satisfied with the visual quality and colors and singled out the sky as exceptionally compelling.
- **Bronze Age Greek ship specificity — pass:** a long, low, single-mast, square-sail silhouette with curved ends plausibly reads as an ancient Aegean galley.
- **Directed square-sail motion — fail:** the filled sail is inconsistent with the nearly calm sea surface.
- **Atmosphere — pass:** dark wine-colored sea, heavy purple clouds, pre-dawn light, wide composition, and restrained palette are strong and coherent.
- **Temporal/object coherence — fail:** stable geometry is undermined by a foamy trail ahead of the vessel, producing a reverse-playback impression.
- **Restrained realism — fail:** wind, sail, sea, and wake do not form a physically plausible causal system.
- **Forbidden content — pass:** no text, watermark, modern object, or unsafe content.
- **Material improvement — fail:** visual specificity improved, but the Slice 002 motion limitation did not become a pass.

## Findings and Recovery

- The first online wrapper invocation exited before inference because Bash 3.2 treated an empty array expansion as unset under `set -u`. No Wan process survived and no output was produced. The failed local attempt was preserved, the process-tree sampler was rewritten recursively, and the successful runs used committed fix `715b073` without live entrypoint edits.
- An attempted offline start from the Codex sandbox stopped before inference because host swap and thermal metrics were inaccessible there. No offline run artifact was created. The same committed wrapper was then launched on the host; its child inference process remained inside macOS network denial.
- Sampled process-tree RSS remained lower than `/usr/bin/time` maximum RSS because macOS unified-memory accounting is not equivalent across those surfaces. Final reporting retains both and does not treat either alone as the total resource envelope.
- The original 1.5–3.0-hour planning estimate was low. Measured wrapper times were approximately 3.35–3.63 hours, still within the declared four-hour ceiling.

## Verification

- `command:` `.venv/bin/python scripts/verify-slice-005.py --model-only`
  - `result:` pass
  - `notes:` exact revision, allowlisted runtime files, sizes, hashes, index shards, license, external store, and Apple source revision passed.
- `command:` `./scripts/run-slice-005-benchmark.sh online`
  - `result:` pass after the pre-inference Bash sampler fix
  - `notes:` fixed benchmark completed normally with no safety stop.
- `command:` `./scripts/run-slice-005-benchmark.sh offline`
  - `result:` pass on the macOS host
  - `notes:` network-denial preflight, local-only model resolution, inference, media checks, and wrapper closeout passed.
- `check:` owner normal-speed playback plus first, middle, last, and ten evenly spaced samples
  - `result:` visual pass with hard motion failures
  - `notes:` strong sky, color, atmosphere, and ancient silhouette; forward wake and wind/water inconsistency reject the shot.
- `command:` `.venv/bin/python scripts/verify-slice-005.py`
  - `result:` pass
  - `notes:` exact model inventory, runtime summaries, safety evidence, complete media decodes, SHA-256 values, and online/offline byte identity passed.
- `command:` `./scripts/verify-local-environment.sh`
  - `result:` pass on the macOS host
  - `notes:` Python 3.12.13 arm64, MLX 0.32.2 with Metal, PyTorch 2.14.0 with MPS, FFmpeg 9.0.1, the pinned Apple source, offline flags, ignore rules, and the tracked-artifact scan passed. The expected sandbox-only Metal visibility failure was not treated as host evidence.
- `command:` repository language, artifact, diff, and Memory Core checks
  - `result:` pass
  - `notes:` all tracked JSON parsed; `git diff --check` passed; no project-facing Cyrillic was found; weights, generated media, and detailed runtime artifacts remained local and ignored.
- `command:` exact staged-to-vault Obsidian comparison plus frontmatter and Wikilink target checks
  - `result:` pass
  - `notes:` the Slice 005 note, project hub, roadmap, decision log, research sources, and durable current-state summary matched their staged copies; Slice 004 remained resolvable and postponed.
- `command:` `./.automation/scripts/aira-memory finish --task-id slice-005-wan-2.1-t2v-14b-benchmark` without `--apply`, then `./.automation/scripts/aira-memory audit --mode project-local --fail-on-drift`
  - `result:` pass
  - `notes:` dry-run planned one session-capsule write, promoted zero artifacts, and the strict project-local audit reported zero drift, duplicate, stale, metadata, context-hygiene, state-authority, or completion findings.

## Review Closeout

The acceptance decision separates technical execution from editorial quality. Hardware feasibility, runtime safety, offline operation, deterministic output, and visual direction passed. Production motion quality failed. No prompt rewrite, seed sweep, sampling change, second model, or unquantized rerun was smuggled into Slice 005 after the failure became visible.

The Memory Core dry-run initially found that `repo-landmines.md` exceeded its always-on-context limit by 42 bytes. Its wording was compressed without removing any boundary; the repeated dry-run and strict audit then passed with zero findings.

## Open Findings

- None after final verification and review closeout.

## Exact Recommendation for Slice 006

Execute only `slice-006-flagship-video-model-comparison-gate`. Refresh the exact open flagship shortlist and primary-source evidence; compare license, Apple Silicon runtime, weight size, resource envelope, and model-native controls; then select and bound the next benchmark sequence. Preserve the causal prompt and low-cost motion-scout requirements in `docs/t2v-prompt-motion-analysis.md`. Do not download or run another model until the gate names exact repositories, revisions, files, benchmarks, and safety boundaries.

`slice-004-rights-ledger-foundation` remains postponed without deletion or renumbering.

## Distillation Candidates

**Decision**: Reject the fixed Wan2.1 T2V 14B configuration for this production motion shot while retaining it as proven local visual-direction capability.
- **Rationale**: Offline reproducibility, resources, atmosphere, color, and still-image quality passed; physical motion hard gates failed.
- **Alternatives considered**: prompt tuning inside Slice 005, changing the seed, unquantized rerun, immediate I2V, and automatic multi-model download.
- **Impact**: The next gate can compare flagship models and stronger conditioning without erasing the successful BigBoy capability evidence or entering an unbounded tuning loop.

No candidate is promoted by this closeout. Promotion remains a separate owner-approved act.
