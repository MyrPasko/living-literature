#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import struct
import subprocess
from pathlib import Path


DECISION_ID = "slice-006-wan-2.2-i2v-a14b-decision-gate"
MODEL_REPOSITORY = "Wan-AI/Wan2.2-I2V-A14B-Diffusers"
MODEL_REVISION = "596658fd9ca6b7b71d5057529bbf319ecbc61d74"
RUNTIME_VERSION = "0.33.1"
RUNTIME_COMMIT = "23cee803f10aacdf943a9565f7cd67c25c825080"
RUNTIME_WHEEL_SHA256 = "1a19e6510a166cbe0fe4975146813fb61adf98f0e073abb4e63f27f012882d0a"
PACKAGE_REPOSITORY = "AbstractFramework/wan2.2-i2v-a14b-diffusers-bf16"
PACKAGE_REVISION = "ef2a0bfe5b4ca7edb84c93f1675edb1a8bfe7d60"
PACKAGE_FILE_COUNT = 44
PACKAGE_SIZE_BYTES = 68_791_046_058
SOURCE_VIDEO_SHA256 = "ce7a61c21ef0811062ea6229b3ddf89c6843bdc6569234cab060915bd39f2ad4"
SELECTED_CANDIDATE_ID = "D"
SELECTED_CANDIDATE_PATH = "outputs/slice-006/source-still-candidates/candidate-d-frame-048.png"
SELECTED_CANDIDATE_SHA256 = "7e7f0a20ebaa62551cad700d7e17fecd0fdc68a7003c9e1eb2e846f7fd6ec0c7"
SELECTED_FRAME = 48
SELECTED_TIMECODE = "00:00:03.000"
NEXT_SLICE = "slice-007-wan-2.2-i2v-a14b-motion-scout"

POSITIVE_PROMPT = (
    "Single continuous five-second shot, locked-off wide side view. A Late Bronze Age "
    "Aegean galley with a long black hull, curved prow and stern, one mast and one "
    "rectangular square sail moves steadily from left to right across a dark wine-colored "
    "sea before dawn. The bow always points right; the stern remains left. Moderate wind "
    "blows from left to right, naturally filling the sail and raising aligned wavelets. A "
    "small bow wave splits outward at the prow; a narrow foamy wake begins only behind the "
    "stern and trails leftward. Heavy purple clouds drift slowly. Stable geometry, physically "
    "coherent motion, no camera movement, text, or modern objects. Preserve the approved input "
    "image’s ship design, palette, atmosphere, framing, and horizon."
)
NEGATIVE_PROMPT = (
    "reverse playback, backward sailing, wake or foam ahead of the bow, wake extending "
    "forward, perfectly still water with a filled sail, deformed sail, changing hull "
    "geometry, extra mast, camera dolly, pan, zoom, text, watermark, modern vessel, blurry "
    "image, JPEG artifacts"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify the Slice 006 decision gate.")
    parser.add_argument(
        "--allow-pending-still",
        action="store_true",
        help="Validate the pre-selection state while the owner still choice is pending.",
    )
    return parser.parse_args()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def png_dimensions(path: Path) -> tuple[int, int]:
    with path.open("rb") as source:
        header = source.read(24)
    require(header[:8] == b"\x89PNG\r\n\x1a\n", f"not a PNG: {path}")
    require(header[12:16] == b"IHDR", f"missing PNG IHDR: {path}")
    return struct.unpack(">II", header[16:24])


def git(repo_root: Path, *args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=repo_root,
        check=True,
        capture_output=True,
        text=True,
    ).stdout


def verify_identifiers(manifest: dict, document: str) -> None:
    require(manifest["decision_id"] == DECISION_ID, "decision id drift")
    require(manifest["task_type"] == "controller_led_investigation_decision_gate", "task type drift")
    require(manifest["production_model_accepted"] is False, "production model was accepted")

    selected = manifest["selected_future_benchmark_candidate"]
    model = selected["official_model"]
    runtime = selected["runtime"]
    package = selected["prepared_package"]
    require(model["repository"] == MODEL_REPOSITORY, "model repository drift")
    require(model["revision"] == MODEL_REVISION, "model revision drift")
    require(model["license"] == "Apache-2.0", "model license drift")
    require(model["pipeline_tag"] == "image-to-video", "model task drift")
    require(runtime["version"] == RUNTIME_VERSION, "runtime version drift")
    require(runtime["source_commit"] == RUNTIME_COMMIT, "runtime source drift")
    require(runtime["wheel_sha256"] == RUNTIME_WHEEL_SHA256, "runtime wheel hash drift")
    require(runtime["license"] == "MIT", "runtime license drift")
    require(package["repository"] == PACKAGE_REPOSITORY, "prepared package repository drift")
    require(package["revision"] == PACKAGE_REVISION, "prepared package revision drift")
    require(package["file_count"] == PACKAGE_FILE_COUNT, "prepared package file-count drift")
    require(package["size_bytes"] == PACKAGE_SIZE_BYTES, "prepared package size drift")
    require(package["runtime_precision"] == "BF16", "runtime precision drift")
    require(selected["execution_policy"] == "sequential_only", "sequential-only rule missing")
    require(selected["production_acceptance"] == "not_accepted", "benchmark candidate marked production accepted")

    for exact_text in (
        DECISION_ID,
        MODEL_REPOSITORY,
        MODEL_REVISION,
        RUNTIME_COMMIT,
        RUNTIME_WHEEL_SHA256,
        PACKAGE_REPOSITORY,
        PACKAGE_REVISION,
        f"{PACKAGE_SIZE_BYTES:,}",
        NEXT_SLICE,
    ):
        require(exact_text in document, f"decision document missing exact value: {exact_text}")


def verify_comparison(manifest: dict, document: str) -> None:
    reopened = manifest["comparison_reopened"]
    require(reopened["owner_direction_received"] is True, "comparison was not owner-authorized")
    ltx = next(item for item in manifest["alternatives"] if item["candidate"].startswith("LTX-2.5"))
    require(
        ltx["disposition"] == "viable_but_deferred_for_separate_license_and_runtime_evidence_gate",
        "LTX disposition drift",
    )
    require(ltx["model_revision"] == "5e6e71018ee1756ed329b697a7b4aedc934dfce9", "LTX model revision drift")
    require(ltx["desktop_runtime_revision"] == "68cd86c15e5fd25f56229ea63c0dbcb0338f7812", "LTX Desktop revision drift")
    require(ltx["minimum_fully_local_size_bytes"] == 71_114_917_404, "LTX local inventory drift")
    require("prior API-only rejection is obsolete" in document, "LTX correction missing from decision document")


def verify_prompts(manifest: dict, document: str) -> None:
    prompts = manifest["prompts"]
    require(prompts["positive"] == POSITIVE_PROMPT, "positive prompt drift")
    require(prompts["negative"] == NEGATIVE_PROMPT, "negative prompt drift")
    require(document.count(POSITIVE_PROMPT) == 1, "positive prompt must appear once verbatim")
    require(document.count(NEGATIVE_PROMPT) == 1, "negative prompt must appear once verbatim")


def verify_future_benchmarks(manifest: dict) -> None:
    scout = manifest["future_motion_scout"]
    require(scout["slice_id"] == NEXT_SLICE, "scout slice identity drift")
    require(scout["requires_separate_owner_approved_plan"] is True, "scout lacks plan gate")
    require(scout["precision"] == "BF16", "scout precision drift")
    require((scout["requested_width"], scout["requested_height"]) == (448, 256), "scout canvas drift")
    require(scout["canvas_policy"] == "source_aspect", "scout canvas policy drift")
    require(scout["record_resolved_dimensions"] is True, "resolved-dimension recording missing")
    require((scout["frames"], scout["fps"], scout["denoising_steps"]) == (41, 8, 15), "scout frame/fps/step drift")
    require(scout["seed"] == 42, "scout seed drift")
    require((scout["guidance"], scout["guidance_2"], scout["flow_shift"]) == (4.0, 3.0, 3.0), "scout guidance drift")
    require(scout["solver"] == "unipc", "scout solver drift")
    require(scout["low_ram"] is True and scout["metadata"] is True, "scout safety metadata drift")
    for disabled in (
        "prompt_extension",
        "cache_acceleration",
        "video_to_video_input",
        "parallel_process",
        "cloud_service",
        "api_key",
    ):
        require(scout[disabled] is False, f"scout prohibition drift: {disabled}")
    require(scout["lora"] is None and scout["lightning_adapter"] is None, "scout adapter prohibition drift")
    require(len(scout["hard_gates"]) == 10, "scout hard-gate count drift")
    require(scout["failure_policy"]["reject_route_on_any_hard_gate_failure"] is True, "scout fail-closed rule missing")
    require(len(scout["failure_policy"]["forbidden_after_failure"]) == 7, "scout no-tuning boundary drift")

    full = manifest["later_full_benchmark"]
    require(full["requires_explicit_owner_acceptance_of_motion_scout"] is True, "full benchmark lacks owner gate")
    require((full["requested_width"], full["requested_height"]) == (832, 480), "full canvas drift")
    require(full["canvas_policy"] == "source_aspect", "full canvas policy drift")
    require((full["frames"], full["fps"], full["denoising_steps"]) == (81, 16, 40), "full frame/fps/step drift")
    require(full["network_denied_repeat_after_human_quality_pass_only"] is True, "offline order drift")
    frozen = set(full["same_frozen_inputs"])
    require(
        frozen
        == {
            "model",
            "runtime",
            "prepared_package",
            "input_still",
            "positive_prompt",
            "negative_prompt",
            "seed",
            "guidance",
            "guidance_2",
            "flow_shift",
            "solver",
            "BF16_precision",
        },
        "full benchmark does not freeze the scout inputs",
    )


def verify_safety(manifest: dict) -> None:
    offline = manifest["offline_proof"]
    require(offline["freeze_before_inference"] is True, "offline proof is not frozen before inference")
    require(offline["may_not_be_weakened_after_results"] is True, "offline proof may be weakened")
    required_offline = {
        "exact_allowlisted_model_inventory",
        "separately_recorded_download_operation",
        "local_model_resolution_after_download",
        "HF_HUB_OFFLINE",
        "TRANSFORMERS_OFFLINE",
        "DIFFUSERS_OFFLINE",
        "local_files_only",
        "macOS_deny_network_sandbox",
        "loopback_bind_denial_preflight",
        "full_video_decode",
        "media_property_verification",
        "sha256_comparison",
    }
    require(set(offline["requirements"]) == required_offline, "offline proof requirements drift")
    require(offline["deterministic_acceptance"].startswith("byte_identical_output_unless"), "byte-identity default missing")

    resource = manifest["resource_plan"]
    published = resource["published_profile"]
    require((published["width"], published["height"], published["frames"], published["steps"], published["fps"]) == (384, 384, 33, 12, 8), "published profile drift")
    require((published["mlx_peak_gib"], published["maximum_rss_gib"], published["full_process_physical_peak_gib"], published["runtime_seconds"]) == (28.2, 31.8, 33.7, 228.2), "published resource evidence drift")
    estimate = resource["full_run_estimate"]
    require(estimate["mlx_peak_gb"] == {"minimum": 35, "maximum": 60}, "MLX estimate drift")
    require(estimate["process_footprint_gb"] == {"minimum": 50, "maximum": 90}, "process estimate drift")
    require(estimate["runtime_hours"] == {"minimum": 1.0, "maximum": 3.5}, "runtime estimate drift")
    require(estimate["maximum_runtime_hours"] == 4, "maximum runtime drift")
    preflight = resource["future_preflight"]
    require(preflight["minimum_system_memory_free_percent"] == 90, "preflight memory drift")
    require(preflight["required_swap_gib"] == 0, "preflight swap drift")
    require(preflight["minimum_free_disk_gib_before_download_or_preparation"] == 180, "download disk gate drift")
    require(preflight["minimum_free_disk_gib_before_inference"] == 120, "inference disk gate drift")
    stops = resource["future_automatic_stops"]
    require(stops["memory_free_percent_at_or_below"] == 10, "memory stop drift")
    require(stops["swap_gib_above"] == 8, "swap stop drift")
    require(stops["free_disk_gib_below"] == 100, "disk stop drift")
    require(set(stops["thermal_state"]) == {"serious", "critical"}, "thermal stop drift")
    require(stops["no_denoising_progress_minutes"] == 20, "progress stop drift")
    require(stops["elapsed_runtime_hours_above"] == 4, "runtime stop drift")

    authority = manifest["slice_006_authority"]
    require(all(value is False for value in authority.values()), "Slice 006 performed or authorized a forbidden action")


def verify_source_stills(repo_root: Path, manifest: dict, document: str, allow_pending: bool) -> None:
    gate = manifest["source_still_gate"]
    require(gate["git_ignored"] is True, "candidate directory is not declared ignored")
    require(gate["candidate_media_committed"] is False, "candidate media marked committed")
    require(gate["source_media"]["online_offline_byte_identical"] is True, "source videos not byte-identical")
    require((gate["source_media"]["width"], gate["source_media"]["height"]) == (832, 480), "source dimensions drift")
    require((gate["source_media"]["frames"], gate["source_media"]["fps"]) == (81, 16), "source frame/fps drift")

    for source in gate["source_videos"]:
        require(source["sha256"] == SOURCE_VIDEO_SHA256, "recorded source-video hash drift")
        path = repo_root / source["path"]
        require(path.is_file(), f"missing source video: {path}")
        require(path.stat().st_size == source["size_bytes"], f"source-video size drift: {path}")
        require(sha256(path) == SOURCE_VIDEO_SHA256, f"source-video hash mismatch: {path}")

    candidates = {item["id"]: item for item in gate["candidates"]}
    require(set(candidates) == {"A", "B", "C", "D", "E", "F"}, "candidate set drift")
    for item in candidates.values():
        path = repo_root / item["path"]
        require(path.is_file(), f"missing local candidate: {path}")
        require(sha256(path) == item["sha256"], f"candidate hash drift: {item['id']}")
        require(png_dimensions(path) == (item["width"], item["height"]), f"candidate dimensions drift: {item['id']}")
        ignored = subprocess.run(
            ["git", "check-ignore", "-q", item["path"]],
            cwd=repo_root,
            check=False,
        ).returncode == 0
        require(ignored, f"candidate is not Git-ignored: {item['path']}")

    sheet = gate["contact_sheet"]
    sheet_path = repo_root / sheet["path"]
    require(sheet_path.is_file(), "missing contact sheet")
    require(sha256(sheet_path) == sheet["sha256"], "contact-sheet hash drift")
    require(png_dimensions(sheet_path) == (sheet["width"], sheet["height"]), "contact-sheet dimensions drift")

    selected = gate["selected"]
    if selected is None:
        require(allow_pending, "owner source-still selection is still pending")
        require(manifest["status"] == "awaiting_owner_source_still_selection", "pending manifest status drift")
        require(gate["status"] == "owner_selection_required", "pending still-gate status drift")
        return

    require(not allow_pending, "remove --allow-pending-still after owner selection")
    require(manifest["status"] == "accepted_for_one_future_benchmark", "selected manifest status drift")
    require(gate["status"] == "owner_selected", "selected still-gate status drift")
    require(selected["candidate_id"] == SELECTED_CANDIDATE_ID, "owner-selected candidate drift")
    expected = candidates[selected["candidate_id"]]
    for field in ("path", "sha256", "width", "height", "frame_number_zero_based", "timecode"):
        require(selected[field] == expected[field], f"selected-still provenance drift: {field}")
    require(selected["source_video_sha256"] == SOURCE_VIDEO_SHA256, "selected source-video hash drift")
    require(selected["path"] == SELECTED_CANDIDATE_PATH, "selected path drift")
    require(selected["sha256"] == SELECTED_CANDIDATE_SHA256, "selected hash drift")
    require(selected["frame_number_zero_based"] == SELECTED_FRAME, "selected frame drift")
    require(selected["timecode"] == SELECTED_TIMECODE, "selected timecode drift")
    require(selected["owner_selection"] == "left image in the second row", "owner selection wording drift")
    require(selected["committed"] is False, "selected still marked committed")
    require(selected["git_ignored"] is True, "selected still not declared Git-ignored")
    for exact_text in (
        "candidate D",
        SELECTED_CANDIDATE_PATH,
        SELECTED_CANDIDATE_SHA256,
        str(SELECTED_FRAME),
        SELECTED_TIMECODE,
        SOURCE_VIDEO_SHA256,
    ):
        require(exact_text in document, f"decision document missing selected-still value: {exact_text}")


def verify_git_artifact_boundary(repo_root: Path) -> None:
    tracked = set(git(repo_root, "ls-files").splitlines())
    forbidden_suffixes = {
        ".safetensors",
        ".ckpt",
        ".pt",
        ".pth",
        ".gguf",
        ".mp4",
        ".mov",
        ".mkv",
        ".webm",
    }
    forbidden = sorted(path for path in tracked if Path(path).suffix.lower() in forbidden_suffixes)
    require(not forbidden, f"model weight or generated video is tracked: {forbidden}")
    require(
        not any(path.startswith("outputs/slice-006/") for path in tracked),
        "Slice 006 local media is tracked",
    )


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parent.parent
    manifest_path = repo_root / "manifests/decisions/slice-006-wan-2.2-i2v-a14b.json"
    document_path = repo_root / "docs/slice-006-wan-2.2-i2v-a14b-decision-gate.md"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    document = document_path.read_text(encoding="utf-8")

    verify_identifiers(manifest, document)
    verify_comparison(manifest, document)
    verify_prompts(manifest, document)
    verify_future_benchmarks(manifest)
    verify_safety(manifest)
    verify_source_stills(repo_root, manifest, document, args.allow_pending_still)
    verify_git_artifact_boundary(repo_root)

    state = "pending-owner-still" if args.allow_pending_still else "complete"
    print(f"slice-006-verification=pass state={state}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
