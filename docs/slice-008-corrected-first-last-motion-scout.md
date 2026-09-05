---
project: Living Literature
document: corrected-first-last-motion-scout
status: anchors-and-prompts-approved
verified: 2026-09-05
slice: slice-008-corrected-first-last-motion-scout
---

# Slice 008 — Corrected First/Last Motion Scout

## Purpose

Prepare a bounded retry of the Wan2.2 I2V-A14B motion scout using explicit first- and last-frame bracket conditioning. This preparation addresses Slice 007’s reverse travel, wrong sail/wind direction, missing wind-driven surface waves, and excessive speed. It stops before video-model inference.

## Exact Route

- Reuse the existing pinned BF16 model package at revision `ef2a0bfe5b4ca7edb84c93f1675edb1a8bfe7d60`; no download.
- Reuse MLX-Gen 0.33.1 at commit `23cee803f10aacdf943a9565f7cd67c25c825080`; no installation.
- Invoke the pinned direct Wan executable `mlxgen-generate-wan`, which exposes experimental A14B `--last-image` bracket conditioning. The generic `mlxgen generate` wrapper does not expose that option and must not be used for this route.
- Remain sequential and allow at most one later attempt after denoising begins.

## Anchor Pair

First-frame candidate:

- `outputs/next-slice-reference-candidates/right-facing-aegean-galley-start-frame-candidate-v2.png`
- SHA-256 `9441f1a783f42ef1e7b605f0c4c6981462e071c46f49c7607a4ba6ab9533ffde`
- 1672×940; owner-approved on 2026-09-05.

Last-frame candidate:

- `outputs/next-slice-reference-candidates/right-facing-aegean-galley-approved-end-frame-v1.png`
- SHA-256 `6c0f3d2ee62e4ff563a1fc02d6e42a3f255bc75d3bed8fa6210904f862ef85ce`
- 1672×940; owner-approved as the Slice 008 endpoint on 2026-09-05.

The first image places the same right-facing galley a modest distance left of the endpoint, constraining slow rightward travel rather than the excessive Slice 007 speed. Both remain local and Git-ignored. Their lineage includes a user-supplied anatomical reference with unverified rights, so the pair is internal-evaluation-only and cannot clear publication or production use.

## Frozen Positive Prompt

> One continuous 5.125-second shot from a completely locked camera. Image 1 is the exact first frame; Image 2 is the exact last frame.
>
> The Late Bronze Age Aegean galley travels slowly and continuously from LEFT TO RIGHT, bow first. The unmistakable RIGHT-facing curved prow and short massive submerged ram lead the motion in every frame. The LEFT stern and its separate steering oar always trail behind.
>
> Movement is smooth and uniform at approximately 3 knots. Across the entire shot, the ship moves only the distance fixed by the two anchor images—approximately one-quarter of its hull length. No sudden acceleration, sliding, sideways drift, or speedboat motion.
>
> A steady 8–10-knot following wind blows strictly from LEFT TO RIGHT. The rectangular square sail remains taut and naturally filled. Its cloth belly and loose edges bow gently toward the RIGHT, downwind, throughout the shot.
>
> Because the sail is filled, small wind-driven wavelets and short ripples remain clearly visible across the entire sea surface. The water must never become flat, glassy, or motionless.
>
> A small bow wave begins precisely at the RIGHT-facing prow and submerged ram. A narrow, low-energy wake begins only behind the LEFT stern and trails leftward. No foam or wake appears ahead of the bow.
>
> Preserve the approved ship, ram, steering oar, hull, mast, rigging, sail, purple pre-dawn sky, wine-dark sea, horizon, framing, scale, and lighting. Keep geometry and camera completely stable.

## Frozen Negative Prompt

> reverse travel, stern-first movement, backward sailing, bow or ram pointing left, stern leading the ship, rapid movement, acceleration, sliding, sideways drift, speedboat wake, sail bending or bulging left, wind from right to left, limp sail, flat water, glassy sea, motionless water with a filled sail, wake ahead of the bow, foam on the right ahead of the ram, missing steering oar, exposed long ram, deformed hull, changing mast, changing rigging, camera pan, camera tracking, zoom, horizon movement, text, watermark, modern object

## Future Scout Configuration

- 448×256 requested source-aspect canvas;
- 41 frames at 8 fps, 15 steps, seed 42;
- guidance 4.0, guidance-2 3.0, flow shift 3.0, UniPC;
- BF16, low-RAM, metadata on, prompt cache off;
- Slice 007 safety thresholds unchanged;
- one future attempt only, authorized when the owner pastes the self-contained Slice 008 inference prompt in the next session.

## Approval Gate

The owner approved the first image, the existing last image as the Slice 008 endpoint, and both frozen prompts on 2026-09-05. No inference is authorized in the current session. The self-contained next-session execution prompt is the authorization for exactly one bounded sequential inference attempt when pasted; the next session must still revalidate the committed configuration, local assets, model/runtime inventories, and live host safety conditions before denoising.
