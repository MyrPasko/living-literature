---
kind: repo-landmines
project: living-literature
authoritative_since: 2026-09-03
---

# Repo Landmines

## Critical Landmines
- Repo project memory is authoritative over Obsidian and generated summaries when they disagree.
- Worker output becomes durable only after extraction and explicit promotion.
- Do not widen an accepted slice without controller approval and updated write-scope.
- Reproducing the Slice 002 benchmark must use `scripts/run-pinned-wan-benchmark.py`; direct Apple CLI invocation bypasses the exact model-revision guard.
- The Slice 002 cache boundary contains only the four declared 1.3B runtime files plus its license and model card evidence.
- The Slice 002 benchmark prompt and parameters are immutable.
- Never patch a long-running shell or Python entrypoint while its process is active.
- Slice 003 is a decision gate; it permits no new weight download or inference.
- Stop a run at 10% free memory, 32 GiB swap, or 100 GiB free disk.
- Slice 005 is complete and authorizes no further inference. Its Wan2.1 T2V 14B result passed local/offline execution but failed production motion hard gates.
- Single-run headroom does not prove two 14B processes are safe; concurrency requires measured throughput, memory, swap, and thermal gates.
- New model caches belong under `~/models`, outside the checkout. Do not import Wan video diffusion into Ollama or migrate the immutable Slice 002 cache inside Slice 005.
- Never use `git submodule update --remote`; the Apple source must remain at the exact approved commit.
- The Apple example source is MIT licensed. The candidate model weights are a separate license and revision gate.
- Do not treat library offline flags alone as proof that inference made no network calls.
- Do not emit or store machine serial numbers, hardware UUIDs, or provisioning identifiers.

## Do Not Infer From Code Alone
- Successful MLX import and Metal checks do not prove the Wan model can generate video.
- Successful CLI help does not prove model weights are present.
- `Wan2.1-T2V-1.3B` is a feasibility candidate, not an accepted production model.
- Low CPU utilization or a high free-memory percentage alone does not bound a Metal workload; use MLX peak memory, process footprint, swap, thermals, runtime, and output quality together.
- A public-domain original does not clear a modern translation, recording, edition, or visual reference.
