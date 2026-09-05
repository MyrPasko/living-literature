#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
import subprocess
from pathlib import Path


BENCHMARK_ID = "slice-010-wan2.2-exact-first-last-full-render"
RUN_ID = "local-files-only-exact-first-last-full-render-seed-42"
BASELINE_COMMIT = "96a1ac2f9dbad2e99e120ae8606edd49fe2019ca"
MODEL_REVISION = "ef2a0bfe5b4ca7edb84c93f1675edb1a8bfe7d60"
RUNTIME_VERSION = "0.33.1"
FIRST_SHA256 = "9441f1a783f42ef1e7b605f0c4c6981462e071c46f49c7607a4ba6ab9533ffde"
LAST_SHA256 = "6c0f3d2ee62e4ff563a1fc02d6e42a3f255bc75d3bed8fa6210904f862ef85ce"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify Slice 010 configuration and evidence.")
    parser.add_argument("--configuration-only", action="store_true")
    parser.add_argument("--preflight", action="store_true")
    parser.add_argument("--allow-pending-review", action="store_true")
    return parser.parse_args()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise RuntimeError(message)


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        key, separator, value = line.partition("=")
        require(bool(separator), f"malformed summary line: {line}")
        values[key] = value
    return values


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def png_dimensions(path: Path) -> tuple[int, int]:
    with path.open("rb") as source:
        header = source.read(24)
    require(header[:8] == b"\x89PNG\r\n\x1a\n" and header[12:16] == b"IHDR", f"invalid PNG: {path}")
    return struct.unpack(">II", header[16:24])


def command_output(command: list[str]) -> str:
    return subprocess.run(command, check=True, capture_output=True, text=True).stdout


def verify_configuration(repo_root: Path, benchmark: dict) -> None:
    require(benchmark["benchmark_id"] == BENCHMARK_ID, "benchmark id drift")
    require(benchmark["status"] == "inference-authorized-frozen", "authorization status drift")
    require(benchmark["baseline_commit"] == BASELINE_COMMIT, "baseline drift")
    require("explicitly approved" in benchmark["execution_authorization"], "owner authorization missing")
    require(benchmark["model"]["revision"] == MODEL_REVISION, "model revision drift")
    require(benchmark["runtime"]["version"] == RUNTIME_VERSION, "runtime version drift")

    first = repo_root / benchmark["anchors"]["first"]["path"]
    last = repo_root / benchmark["anchors"]["last"]["path"]
    require(first.is_file() and last.is_file(), "anchor missing")
    require(sha256(first) == FIRST_SHA256 and sha256(last) == LAST_SHA256, "anchor hash drift")
    require(png_dimensions(first) == (1672, 940) and png_dimensions(last) == (1672, 940), "anchor dimensions drift")

    params = benchmark["parameters"]
    require((params["requested_width"], params["requested_height"]) == (832, 480), "resolution drift")
    require(params["canvas_policy"] == "exact-resize" and params["resize_mode"] == "resize", "canvas policy drift")
    require((params["frames"], params["fps"], params["steps"]) == (81, 16, 50), "frame, fps, or step drift")
    require((params["seed"], params["guidance"], params["guidance_2"], params["flow_shift"]) == (42, 5.0, 5.0, 5.0), "generation parameter drift")
    require(params["solver"] == "unipc" and params["precision"] == "BF16" and params["quantization"] is None, "solver or precision drift")
    require(params["low_ram"] and params["metadata"] and params["release_inactive_denoiser"], "required runtime control missing")
    require(not params["prompt_cache"] and not params["parallel_process"] and not params["cloud_service"] and not params["api_key"], "forbidden runtime mode enabled")

    safety = benchmark["safety"]
    expected = {
        "minimum_preflight_memory_free_percent": 90,
        "required_preflight_swap_mb": 0,
        "minimum_disk_before_inference_gib": 120,
        "stop_memory_free_percent": 10,
        "stop_swap_above_mb": 8192,
        "stop_disk_below_gib": 100,
        "stop_progress_silence_seconds": 1200,
        "maximum_run_seconds": 14400,
        "sample_interval_seconds": 15,
    }
    require(all(safety[key] == value for key, value in expected.items()), "safety threshold drift")
    require(safety["sequential_only"] is True, "sequential-only rule missing")
    require(benchmark["run"]["run_id"] == RUN_ID, "run id drift")
    require(benchmark["run"]["maximum_generation_attempts_after_denoising_starts"] == 1, "one-attempt rule drift")
    require(len(benchmark["hard_gates"]) == 12, "hard-gate count drift")
    restrictions = benchmark["slice_restrictions"]
    require(restrictions["inference_authorized"] and restrictions["slice_004_remains_postponed"], "required slice state drift")
    require(all(not restrictions[key] for key in restrictions if key not in {"inference_authorized", "slice_004_remains_postponed"}), "forbidden authority enabled")

    slice8 = load_json(repo_root / "benchmarks/slice-008-corrected-first-last-motion-scout.json")
    require(benchmark["prompt"] == slice8["prompt"] and benchmark["negative_prompt"] == slice8["negative_prompt"], "Slice 008 prompt drift")
    runner = (repo_root / "scripts/run-slice-010-exact-full-render.sh").read_text(encoding="utf-8")
    for value in (benchmark["prompt"], benchmark["negative_prompt"], "--last-image", "--canvas-policy exact-resize", "--width 832", "--height 480", "--frames 81", "--fps 16", "--steps 50", "--guidance 5.0", "--guidance-2 5.0", "--flow-shift 5.0", "--no-replace"):
        require(value in runner, f"runner missing frozen value: {value[:40]}")
    tracked = command_output(["git", "-C", str(repo_root), "ls-files"]).splitlines()
    forbidden = {".safetensors", ".ckpt", ".pt", ".pth", ".gguf", ".mp4", ".mov", ".mkv", ".webm"}
    require(not [path for path in tracked if Path(path).suffix.lower() in forbidden], "tracked weight or video found")


def verify_preflight(repo_root: Path) -> None:
    require(command_output(["git", "-C", str(repo_root), "branch", "--show-current"]).strip() == "feature/slice-010-wan2-2-exact-full-render", "wrong branch")
    require(not command_output(["git", "-C", str(repo_root), "status", "--porcelain=v1"]).strip(), "working tree is not clean")
    subprocess.run([str(repo_root / ".venv/bin/python"), str(repo_root / "scripts/verify-slice-007.py"), "--preflight"], check=True)


def time_metric(log_text: str, label: str) -> int:
    match = re.search(rf"^\s*(\d+)\s+{re.escape(label)}$", log_text, re.MULTILINE)
    require(match is not None, f"missing time metric: {label}")
    return int(match.group(1))


def verify_result(repo_root: Path, benchmark: dict, allow_pending_review: bool) -> None:
    result_path = repo_root / "manifests/benchmarks/slice-010-wan2.2-exact-first-last-full-render-results.json"
    require(result_path.is_file(), "Slice 010 results manifest missing")
    result = load_json(result_path)
    require(result["benchmark_id"] == BENCHMARK_ID and result["run_id"] == RUN_ID, "result identity drift")

    run_root = repo_root / "benchmarks/artifacts/slice-010" / RUN_ID
    summary = load_env(run_root / "summary.env")
    require((run_root / "generation-attempt-started.marker").is_file(), "attempt marker missing")
    if result["technical_verdict"] == "fail":
        require(not allow_pending_review, "pending review is invalid for a pre-denoise rejection")
        require(result["status"] == "complete-pre-denoise-configuration-rejection", "rejection status drift")
        require(result["generation_attempts"] == 0 and result["generation_attempts_after_denoising_started"] == 0, "generation count drift")
        log_text = (run_root / "run.log").read_text(encoding="utf-8")
        require(log_text.count('\"phase\": \"denoise\"') == 0, "denoising unexpectedly started")
        require("Adjusting requested video size (480, 832)" in log_text and '"width": 848, "height": 480' in log_text, "resolution mismatch evidence drift")
        require(not (repo_root / benchmark["run"]["output"]).exists(), "unexpected video output exists")
        require(not Path(summary["metadata"]).exists(), "unexpected metadata output exists")
        rows = (run_root / "system-samples.tsv").read_text(encoding="utf-8").splitlines()[1:]
        columns = [row.split("\t", 6) for row in rows]
        require(len(rows) == result["resources"]["sample_count"] and all(len(row) == 7 for row in columns), "sample evidence drift")
        observed = (
            min(int(float(row[1])) for row in columns),
            max(float(row[2]) for row in columns),
            max(int(row[5]) for row in columns),
            min(int(row[3]) for row in columns),
            min(int(row[4]) for row in columns),
        )
        recorded = (
            result["resources"]["minimum_memory_free_percent"],
            result["resources"]["maximum_swap_mb"],
            result["resources"]["maximum_sampled_process_tree_rss_kb"],
            result["resources"]["minimum_repo_disk_available_kb"],
            result["resources"]["minimum_model_disk_available_kb"],
        )
        require(observed == recorded, "recorded resource evidence drift")
        require(all("No thermal warning" in row[6] and "No performance warning" in row[6] for row in columns), "warning observed")
        require(result["owner_motion_review"]["status"] == "not_applicable_no_video", "motion review status drift")
        require(all(value == "not_assessed" for value in result["owner_motion_review"]["hard_gates"].values()), "unexpected motion verdict")
        return

    require(result["generation_attempts"] == 1 and result["technical_verdict"] == "pass", "technical result drift")
    require(summary["inference_exit_code"] == "0" and summary["safety_stop"] == "none", "inference or safety failure")
    require(summary["full_decode"] == "pass" and summary["wrapper_closeout"] == "normal", "runner closeout drift")
    require(int(summary["duration_seconds"]) <= 14400, "run exceeded four hours")
    log_text = (run_root / "run.log").read_text(encoding="utf-8")
    require(log_text.count('"phase": "denoise"') == 50, "denoising event count drift")

    rows = (run_root / "system-samples.tsv").read_text(encoding="utf-8").splitlines()[1:]
    columns = [row.split("\t", 6) for row in rows]
    require(rows and all(len(row) == 7 for row in columns), "system samples missing or malformed")
    min_free = min(int(float(row[1])) for row in columns)
    max_swap = max(float(row[2]) for row in columns)
    max_rss = max(int(row[5]) for row in columns)
    min_repo_disk = min(int(row[3]) for row in columns)
    min_model_disk = min(int(row[4]) for row in columns)
    require(min_free > 10 and max_swap <= 8192, "memory or swap boundary reached")
    require(min_repo_disk >= 104_857_600 and min_model_disk >= 104_857_600, "disk boundary reached")
    require(all("No thermal warning" in row[6] and "No performance warning" in row[6] for row in columns), "thermal warning observed")

    output = repo_root / benchmark["run"]["output"]
    require(output.is_file() and sha256(output) == summary["output_sha256"] == result["output"]["sha256"], "output drift")
    require(output.stat().st_size == int(summary["output_size_bytes"]) == result["output"]["size_bytes"], "output size drift")
    probe = load_json(run_root / "ffprobe.json")
    video = next(stream for stream in probe["streams"] if stream.get("codec_name"))
    require((video["codec_name"], video["pix_fmt"], video["width"], video["height"], video["nb_frames"], video["r_frame_rate"]) == ("h264", "yuv420p", 832, 480, "81", "16/1"), "media properties drift")
    require(abs(float(probe["format"]["duration"]) - 5.063) <= 0.002, "duration drift")
    subprocess.run(["ffmpeg", "-v", "error", "-i", str(output), "-f", "null", "-"], check=True)

    metadata_path = Path(summary["metadata"])
    metadata = load_json(metadata_path)
    require(sha256(metadata_path) == summary["metadata_sha256"] == result["output"]["metadata_sha256"], "metadata drift")
    require((metadata["width"], metadata["height"], metadata["frames"], metadata["fps"], metadata["steps"]) == (832, 480, 81, 16, 50), "metadata media parameter drift")
    require((metadata["seed"], metadata["guidance"], metadata["guidance_2"], metadata["flow_shift"], metadata["solver"]) == (42, 5.0, 5.0, 5.0, "unipc"), "metadata generation parameter drift")
    require(metadata["precision"] == "mlx.core.bfloat16" and metadata["quantize"] is None, "metadata precision drift")
    require(result["resources"]["mlx_peak_memory_bytes"] == metadata["runtime_memory"]["mlx_peak_memory_bytes"], "MLX peak drift")
    require(result["resources"]["process_peak_rss_bytes"] == time_metric(log_text, "maximum resident set size"), "RSS peak drift")
    require(result["resources"]["darwin_peak_physical_footprint_bytes"] == time_metric(log_text, "peak memory footprint"), "physical footprint drift")
    require((result["resources"]["minimum_memory_free_percent"], result["resources"]["maximum_swap_mb"], result["resources"]["maximum_sampled_process_tree_rss_kb"]) == (min_free, max_swap, max_rss), "sampled resource drift")
    require((result["resources"]["minimum_repo_disk_available_kb"], result["resources"]["minimum_model_disk_available_kb"]) == (min_repo_disk, min_model_disk), "disk result drift")

    contact_sheet = Path(summary["contact_sheet"])
    require(contact_sheet.is_file() and sha256(contact_sheet) == summary["contact_sheet_sha256"] == result["review_evidence"]["contact_sheet_sha256"], "contact sheet drift")
    require(result["review_evidence"]["sampled_frame_numbers_zero_based"] == [0, 16, 32, 48, 64, 80], "contact-sheet frame drift")
    require(png_dimensions(contact_sheet) == (1280, 504), "contact-sheet dimensions drift")

    review = result["owner_motion_review"]
    require(set(review["hard_gates"]) == set(benchmark["hard_gates"]), "owner gate set drift")
    if review["status"] == "pending":
        require(allow_pending_review and result["status"] == "pending-owner-motion-review", "pending review state invalid")
        require(all(value == "pending" for value in review["hard_gates"].values()), "pending review contains verdict")
    else:
        require(not allow_pending_review and review["status"] in {"pass", "fail"}, "review state invalid")
        verdicts = set(review["hard_gates"].values())
        require((review["status"] == "pass" and verdicts == {"pass"}) or (review["status"] == "fail" and "fail" in verdicts), "gate verdict inconsistency")


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parent.parent
    benchmark = load_json(repo_root / "benchmarks/slice-010-wan2.2-exact-first-last-full-render.json")
    verify_configuration(repo_root, benchmark)
    if args.configuration_only:
        require(not args.preflight and not args.allow_pending_review, "configuration-only cannot be combined with another mode")
        print("slice-010-verification=pass state=configuration-only")
        return 0
    if args.preflight:
        require(not args.allow_pending_review, "pending review flag is invalid during preflight")
        verify_preflight(repo_root)
        print("slice-010-verification=pass state=preflight inference=one-attempt-authorized")
        return 0
    verify_result(repo_root, benchmark, args.allow_pending_review)
    result = load_json(repo_root / "manifests/benchmarks/slice-010-wan2.2-exact-first-last-full-render-results.json")
    if result["technical_verdict"] == "fail":
        print("slice-010-verification=pass state=complete-pre-denoise-configuration-rejection")
    else:
        print(f"slice-010-verification=pass state={'pending-owner-review' if args.allow_pending_review else 'complete'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
