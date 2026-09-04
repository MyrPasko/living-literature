---
task_id: slice-003-quality-and-model-gate
task_type: feature
status: complete
branch: main
date: 2026-09-03
write_scope:
  - /Users/myroslavpasko/projects/living-literature/.project-memory/canon/current-state.md
  - /Users/myroslavpasko/projects/living-literature/.project-memory/docs-index.md
  - /Users/myroslavpasko/projects/living-literature/docs/slice-003-quality-and-model-gate.md
  - /Users/myroslavpasko/projects/living-literature/docs/slice-005-wan-2.1-t2v-14b-benchmark.md
  - /Users/myroslavpasko/projects/living-literature/docs/implementation-results/slice-003-quality-and-model-gate.md
  - /Users/myroslavpasko/projects/living-literature/manifests/decisions/slice-003-quality-and-model-gate.json
  - /Users/myroslavpasko/projects/living-literature/.automation/workspace/implement.result.md
  - /Users/myroslavpasko/obsidian/Docs/CLAUDE_KASSANDRA/Projects/Living-Literature/Slices/Slice-003-Quality-and-Model-Gate.md
  - /Users/myroslavpasko/obsidian/Docs/CLAUDE_KASSANDRA/Projects/Living-Literature/Decision-Log.md
  - /Users/myroslavpasko/obsidian/Docs/CLAUDE_KASSANDRA/Projects/Living-Literature/Roadmap.md
  - /Users/myroslavpasko/obsidian/Docs/CLAUDE_KASSANDRA/Projects/Living-Literature/Research-Sources.md
  - /Users/myroslavpasko/obsidian/Docs/CLAUDE_KASSANDRA/Projects/Living-Literature/Index.md
  - /Users/myroslavpasko/obsidian/Docs/CLAUDE_KASSANDRA/Projects/Living-Literature/project-memory/canon/current-state.md
forbidden_moves:
  - model-weight download or inference
  - multi-model bake-off or prompt tuning
  - mutation of Slice 002 evidence
  - cloud inference or API-key path
  - production, publication, push, or pull request
  - automatic Memory Core promotion
verification_surface:
  - current primary-source revisions, licenses, file inventories, and implementation support
  - Slice 002 report, manifests, verifier, and existing MP4 inspection
  - JSON validation and cross-source assertions
  - repository language, artifact, diff, and tracked-content safety
  - scoped Obsidian copy and link verification
  - Memory Core dry-run closeout and project-local audit
success_criteria:
  - exactly one future approach and benchmark are selected and bounded
  - Slice 004 is preserved and the future benchmark receives Slice 005
  - all verification and review findings close before a narrow local commit
slice_restrictions:
  - Slice 003 is a decision gate and authorizes no download or inference
---

# Implementation Result

## Outcome

Selected `Wan-AI/Wan2.1-T2V-14B` at `a064a6c71f5be440641209c07bf2a5ce7a2ff5e4`, through pinned Apple `mlx-examples` revision `796f5b53cab69a3d48a44233ce21aae889e94a08`, with 8-bit DiT quantization for exactly one future benchmark.

The experiment is `slice-005-wan-2.1-t2v-14b-benchmark`. Existing `slice-004-rights-ledger-foundation` remains the active next slice. No production model was accepted.

## Exact References

- Slice 002 baseline: `docs/slice-002-wan-1.3b-benchmark.md`, `docs/implementation-results/slice-002-wan-1.3b-offline-benchmark.md`, `benchmarks/slice-002-wan-1.3b.json`, `manifests/models/wan2.1-t2v-1.3b.json`, and `manifests/benchmarks/slice-002-wan-1.3b-results.json`.
- Selected model: `Wan-AI/Wan2.1-T2V-14B` at `a064a6c71f5be440641209c07bf2a5ce7a2ff5e4`.
- Deferred Wan I2V: `Wan-AI/Wan2.1-I2V-14B-480P` at `6b73f84e66371cdfe870c72acd6826e1d61cf279`.
- Deferred LTX model: `Lightricks/LTX-2.5` at `5e6e71018ee1756ed329b697a7b4aedc934dfce9`.
- LTX source: `Lightricks/ltx-desktop` at `68cd86c15e5fd25f56229ea63c0dbcb0338f7812` and `Lightricks/LTX-2` at `a95ab856bf29407b6b066ede0abe1846050db56c`.
- Deterministic fallback: FFmpeg tag `n9.0.1` at `bf1b838f2ab88b4f8fd83443325c782ea0e0f7fa`.

## Write-Scope

- `.project-memory/canon/current-state.md`
- `.project-memory/docs-index.md`
- `docs/slice-003-quality-and-model-gate.md`
- `docs/slice-005-wan-2.1-t2v-14b-benchmark.md`
- `docs/implementation-results/slice-003-quality-and-model-gate.md`
- `manifests/decisions`
- `.automation/workspace/implement.result.md`
- `/Users/myroslavpasko/obsidian/Docs/CLAUDE_KASSANDRA/Projects/Living-Literature/Slices/Slice-003-Quality-and-Model-Gate.md`
- `/Users/myroslavpasko/obsidian/Docs/CLAUDE_KASSANDRA/Projects/Living-Literature/Decision-Log.md`
- `/Users/myroslavpasko/obsidian/Docs/CLAUDE_KASSANDRA/Projects/Living-Literature/Roadmap.md`
- `/Users/myroslavpasko/obsidian/Docs/CLAUDE_KASSANDRA/Projects/Living-Literature/Research-Sources.md`
- `/Users/myroslavpasko/obsidian/Docs/CLAUDE_KASSANDRA/Projects/Living-Literature/Index.md`
- `/Users/myroslavpasko/obsidian/Docs/CLAUDE_KASSANDRA/Projects/Living-Literature/project-memory/canon/current-state.md`

## Forbidden Moves

- No model-weight download or inference.
- No multi-model bake-off or prompt tuning.
- No mutation of Slice 002 evidence.
- No cloud inference or API-key path.
- No production, publication, push, or pull request.
- No automatic Memory Core promotion.

## Research Result

- The selected Wan T2V 14B Apple-runtime set contains ten files totaling 69,040,541,912 bytes (64.299 GiB). The exact Apache-2.0 license hash is `c71d239df91726fc519c6eb72d318ec65820627232b2f796219e87dcf35d0ab4`.
- Wan I2V 14B 480P contains twelve required Apple-runtime files totaling 82,238,491,725 bytes (76.591 GiB) under the same exact Apache-2.0 license text.
- The evaluated fully local LTX 2.5 file set totals 71,114,917,404 bytes (66.231 GiB). Its model license is the materially more restrictive LTX-2.x Community License, exact reviewed hash `be75acae5c99b0fb16ed6cfbf8f731e5121a729bef112d20337699407e796451`.
- The pinned Apple Wan source directly implements 1.3B T2V, 14B T2V, and 14B I2V. It supports 4/8-bit DiT quantization, UniPC, optional TeaCache, and Metal-cache disabling, but no explicit model offload mode.
- Current LTX Desktop documents local Apple Silicon MPS execution and source-defines an 85 GiB free-memory threshold for full residency, while explicitly stating that the full-resident Darwin tier is unverified on real hardware.
- The installed FFmpeg 9.0.1 build is GPLv3 and can provide deterministic camera motion with negligible model resource cost, but it cannot independently synthesize convincing sail or water motion from one still.

## Decision Rationale

T2V 14B is the cleanest capacity experiment because it preserves the proven prompt, task, geometry, seed, frame count, sampler, and Apple MLX implementation. This is more diagnostic than I2V, which introduces a source still, and lower-risk than LTX, which introduces a gated model, new license, new runtime, and different output envelope.

The expected BigBoy envelope is 35–55 GB MLX peak, 75–110 GB peak process footprint, and 1.5–3.0 hours per inference run. These ranges are estimates derived from the measured 1.3B run and Apple's published M4 Max per-step ratio, not BigBoy measurements.

## Changes Made

- Added the tracked Slice 003 analysis and machine-readable decision manifest.
- Added the planned-but-not-authorized Slice 005 benchmark specification with one exact model, prompt, configuration, file allowlist, resource estimate, offline proof, safety gates, and quality rubric.
- Updated repo canon to mark Slice 003 complete, keep Slice 004 next, and queue Slice 005.
- Synchronized only the scoped Living Literature Slice 003, Decision Log, Roadmap, Research Sources, Index, and durable current-state notes after repo canon was correct.
- Preserved all Slice 002 evidence without modification.

## Verification

- `command:` starting-state and `git ls-remote origin main` checks
- `result:` pass
- `notes:` `main` started clean at `ac7ef661f87fc1b709984d1bdea604787fe75e04`; origin URL matched; remote `main` had no ref.
- `command:` FFprobe plus temporary Slice 002 contact-sheet inspection
- `result:` pass
- `notes:` the existing ignored file remained H.264, 832×480, 81 frames, 16 fps, 5.0625 seconds, and 615,420 bytes; it was not regenerated.
- `command:` `.venv/bin/python scripts/verify-slice-002.py`
- `result:` pass
- `notes:` exact cached baseline, request pins, network-denial evidence, hashes, metadata, and complete decodes passed.
- `command:` `./scripts/verify-local-environment.sh`
- `result:` pass
- `notes:` outside-sandbox host evidence showed Python 3.12.13 arm64, MLX 0.32.2 Metal, PyTorch 2.14.0 MPS, FFmpeg 9.0.1, pinned Apple source, offline help, ignore rules, and tracked-artifact scan. The expected sandbox-only Metal visibility failure was not treated as host evidence.
- `command:` JSON parsing and cross-source revision/size/license assertions
- `result:` pass
- `notes:` all tracked JSON parsed; live metadata matched all three model revisions and totals; exact Wan licenses matched the tracked Apache text; LTX license was hashed.
- `command:` project language, 14B/LTX cache, repository media, and Obsidian synchronization checks
- `result:` pass
- `notes:` no project-facing Cyrillic or 14B/LTX cache; only two expected ignored Slice 002 MP4s; six exact Obsidian copies, frontmatter, and Slice 004 link verified.
- `command:` `./.automation/scripts/aira-memory finish --task-id slice-003-quality-and-model-gate` without `--apply`, then strict project-local audit
- `result:` pass
- `notes:` dry-run planned two candidate writes, applied zero, and reported zero drift, duplicate, stale, metadata, context-hygiene, state-authority, or completion findings.

## Review Closeout

Deterministic review covered correctness, evidence/estimate separation, license boundaries, scope leakage, identifier preservation, benchmark reproducibility, safety thresholds, and forbidden operations. The first Memory Core dry-run found that repo `current-state.md` exceeded its 2,400-character always-on-context limit; the canon was compressed to 1,905 characters without changing decisions, and the rerun passed with zero findings.

## Open Findings

- None

## Distillation Candidates

**Decision**: Test Wan2.1 T2V 14B with 8-bit DiT quantization before changing conditioning or runtime families.
- **Rationale**: It isolates the capacity hypothesis against the measured 1.3B control while staying on the pinned Apple MLX path.
- **Alternatives considered**: stop local T2V, Wan I2V 14B, LTX 2.5 Fast, and deterministic camera animation.
- **Impact**: Slice 005 has one falsifiable benchmark; failure returns to a new decision gate without tuning or automatic model download.

No candidate is promoted by this closeout. Promotion remains a separate owner-approved action.
