---
kind: docs-index
version: 5
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
- `docs/slice-005-wan-2.1-t2v-14b-benchmark.md` for the planned but not authorized 14B benchmark boundary and safety gates.
- `manifests/upstream-wan.json` for machine-readable upstream provenance.
- `manifests/models/wan2.1-t2v-1.3b.json` for exact model files, hashes, revision, and license evidence.
- `manifests/benchmarks/slice-002-wan-1.3b-results.json` for machine-readable runtime, memory, media, and quality results.

## Retrieval Rule
- Add only version-specific, non-obvious documentation pointers that the worker cannot recover reliably from code and config alone.
