---
task_id: slice-009-wan2.2-first-last-full-render
task_type: feature
status: complete-pre-denoise-configuration-rejection
branch: feature/slice-009-wan2-2-first-last-full-render
date: 2026-09-05
---

# Implementation Result

## Outcome

Slice 009 created no video. The single process launch reached runtime initialization but was interrupted before the first denoising step because MLX-Gen changed the requested 832×480 canvas to 848×480 under `canvas_policy=source-aspect`. Continuing would have violated the exact Wan2.1 resolution mapping and the frozen verifier.

## Evidence

- Frozen configuration commit: `0a47698deb095cfea18b2335cb6d10278f99e562`.
- Runtime start: 2026-09-05 12:40:09Z.
- Runtime diagnostic: source image 940×1672 caused requested 480×832 to resolve to 480×848; the runtime recommends `exact-resize` to honor the requested canvas.
- Denoising events: 0 of 50.
- Output video, metadata, and contact sheet: absent.
- Telemetry samples: 12; minimum free memory 89%; maximum swap 0 MiB; maximum sampled process-tree RSS 29,133,904 KiB; no thermal or performance warning.
- The process tree was confirmed absent after interruption.

The durable marker remains in ignored run evidence. It was not removed, and no retry was performed. Motion review is not applicable because no video exists.

## Verification

The configuration-only verifier passed before commit. The host preflight passed twice, including exact anchors, the full 44-file model inventory, pinned runtime and Metal availability, zero swap, disk, thermal state, and absence of competing inference. The recorded result verifier checks the marker, zero denoising events, exact 848×480 runtime diagnostic, absent outputs, and sampled safety evidence.

## Stop Boundary

Slice 009 is complete as a pre-denoise configuration rejection. A corrected launch would require a new exact owner-approved slice using `canvas_policy=exact-resize`, a new run identity and durable marker, and a committed runner/verifier before launch. No download, installation, publication, production acceptance, Memory Core promotion, push, pull request, or merge occurred.
