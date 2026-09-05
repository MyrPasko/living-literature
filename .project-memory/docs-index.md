---
kind: docs-index
version: 14
---

# Docs Index

## Framework Docs
- Apple MLX documentation: `https://ml-explore.github.io/mlx/`
- Apple MLX installation requirements: `https://ml-explore.github.io/mlx/build/html/install.html`
- Pinned Wan example README: `third_party/mlx-examples/video/wan2.1/README.md`
- Pinned Apple source license: `third_party/mlx-examples/LICENSE`

## Local Docs
- `README.md` for repository purpose, setup, and authority.
- `docs/local-video-environment.md` for Slice 001 hardware, dependency, source, FFmpeg, and offline boundaries.
- `docs/slice-002-wan-1.3b-benchmark.md` for the measured online/offline result, quality rubric, and limitations.
- `docs/slice-003-quality-and-model-gate.md` for the five-option analysis and accepted next-model decision.
- `manifests/decisions/slice-003-quality-and-model-gate.json` for machine-readable candidate, license, file-size, resource-estimate, and disposition data.
- `docs/slice-005-wan-2.1-t2v-14b-benchmark.md` for the completed 14B benchmark boundary, measured outcome, external model store, and safety gates.
- `docs/t2v-prompt-motion-analysis.md` for the observed Slice 005 visual/motion split, prompt diagnosis, reviewed prompt candidates, and future low-cost motion gate.
- `docs/implementation-results/slice-005-wan-2.1-t2v-14b-benchmark.md` for exact execution, resource, quality, recovery, and closeout evidence.
- `benchmarks/slice-005-wan-2.1-t2v-14b.json` for the immutable Slice 005 prompt, parameters, run identities, and thresholds.
- `manifests/upstream-wan.json` for machine-readable upstream provenance.
- `manifests/models/wan2.1-t2v-1.3b.json` for exact model files, hashes, revision, and license evidence.
- `manifests/benchmarks/slice-002-wan-1.3b-results.json` for machine-readable runtime, memory, media, and quality results.
- `manifests/models/wan2.1-t2v-14b.json` for the exact external-store file inventory, hashes, revision, and license evidence.
- `manifests/benchmarks/slice-005-wan-14b-results.json` for machine-readable 14B runtime, safety, media, quality, and disposition evidence.
- `docs/slice-006-wan-2.2-i2v-a14b-decision-gate.md` for the reopened flagship comparison, selected Wan2.2 I2V-A14B BF16 candidate, source-still gate, and bounded future scout/full/offline plan.
- `manifests/decisions/slice-006-wan-2.2-i2v-a14b.json` for exact model/runtime/package provenance, corrected LTX-2.5 disposition, prompts, source-still provenance, benchmark parameters, and safety thresholds.
- `docs/implementation-results/slice-006-wan-2.2-i2v-a14b-decision-gate.md` for Slice 006 execution, verification, review, and closeout evidence.
- `docs/slice-007-wan-2.2-i2v-a14b-motion-scout.md` for the exact one-shot scout configuration, safety stops, motion hard gates, and prohibited follow-up work.
- `benchmarks/slice-007-wan-2.2-i2v-a14b-motion-scout.json` for the immutable Slice 007 model, runtime, source-still, prompt, parameters, thresholds, and one-attempt policy.
- `runtimes/mlx-gen-0.33.1/uv.lock` for the exact isolated Slice 007 runtime dependency graph and package hashes.
- `manifests/runtimes/mlx-gen-0.33.1.json` and `manifests/models/wan2.2-i2v-a14b-bf16.json` for verified local runtime and model-package provenance.
- `manifests/benchmarks/slice-007-wan2.2-i2v-a14b-motion-scout-results.json` for measured execution, resource, media, and rejected owner motion-review evidence.
- `docs/implementation-results/slice-007-wan-2.2-i2v-a14b-motion-scout.md` for Slice 007 execution, owner rejection, verification, and closeout evidence.
- `docs/slice-008-corrected-first-last-motion-scout.md` for the internal two-anchor retry, frozen prompts, direct Wan CLI route, one-attempt authorization, and review boundary.
- `benchmarks/slice-008-corrected-first-last-motion-scout.json` for exact anchor hashes, model/runtime identity, frozen parameters, one-attempt authorization, and motion gates.
- `manifests/benchmarks/slice-008-corrected-first-last-motion-scout-results.json` for the single scout’s measured technical evidence and pending owner motion review.
- `docs/implementation-results/slice-008-corrected-first-last-motion-scout.md` for execution, verification, review boundary, and closeout evidence.

## Retrieval Rule
- Add only version-specific, non-obvious documentation pointers that the worker cannot recover reliably from code and config alone.
