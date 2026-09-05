#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import re
import struct
import subprocess
from pathlib import Path


BENCHMARK_ID = "slice-008-corrected-first-last-motion-scout"
RUN_ID = "local-files-only-first-last-motion-scout-seed-42"
BASELINE_COMMIT = "39d3ad3fbc965d70a267c20fb7e57cc839769a79"
MODEL_REPOSITORY = "AbstractFramework/wan2.2-i2v-a14b-diffusers-bf16"
MODEL_REVISION = "ef2a0bfe5b4ca7edb84c93f1675edb1a8bfe7d60"
SOURCE_REPOSITORY = "Wan-AI/Wan2.2-I2V-A14B-Diffusers"
SOURCE_REVISION = "596658fd9ca6b7b71d5057529bbf319ecbc61d74"
MODEL_SIZE_BYTES = 68_791_046_058
RUNTIME_VERSION = "0.33.1"
RUNTIME_COMMIT = "23cee803f10aacdf943a9565f7cd67c25c825080"
RUNTIME_WHEEL_SHA256 = "1a19e6510a166cbe0fe4975146813fb61adf98f0e073abb4e63f27f012882d0a"
FIRST_SHA256 = "9441f1a783f42ef1e7b605f0c4c6981462e071c46f49c7607a4ba6ab9533ffde"
LAST_SHA256 = "6c0f3d2ee62e4ff563a1fc02d6e42a3f255bc75d3bed8fa6210904f862ef85ce"
POSITIVE_PROMPT = (
    "One continuous 5.125-second shot from a completely locked camera. Image 1 is the exact first "
    "frame; Image 2 is the exact last frame. The Late Bronze Age Aegean galley travels slowly and "
    "continuously from LEFT TO RIGHT, bow first. The unmistakable RIGHT-facing curved prow and short "
    "massive submerged ram lead the motion in every frame. The LEFT stern and its separate steering "
    "oar always trail behind. Movement is smooth and uniform at approximately 3 knots. Across the "
    "entire shot, the ship moves only the distance fixed by the two anchor images—approximately "
    "one-quarter of its hull length. No sudden acceleration, sliding, sideways drift, or speedboat "
    "motion. A steady 8–10-knot following wind blows strictly from LEFT TO RIGHT. The rectangular "
    "square sail remains taut and naturally filled. Its cloth belly and loose edges bow gently toward "
    "the RIGHT, downwind, throughout the shot. Because the sail is filled, small wind-driven wavelets "
    "and short ripples remain clearly visible across the entire sea surface. The water must never "
    "become flat, glassy, or motionless. A small bow wave begins precisely at the RIGHT-facing prow and "
    "submerged ram. A narrow, low-energy wake begins only behind the LEFT stern and trails leftward. No "
    "foam or wake appears ahead of the bow. Preserve the approved ship, ram, steering oar, hull, mast, "
    "rigging, sail, purple pre-dawn sky, wine-dark sea, horizon, framing, scale, and lighting. Keep "
    "geometry and camera completely stable."
)
NEGATIVE_PROMPT = (
    "reverse travel, stern-first movement, backward sailing, bow or ram pointing left, stern leading "
    "the ship, rapid movement, acceleration, sliding, sideways drift, speedboat wake, sail bending or "
    "bulging left, wind from right to left, limp sail, flat water, glassy sea, motionless water with a "
    "filled sail, wake ahead of the bow, foam on the right ahead of the ram, missing steering oar, "
    "exposed long ram, deformed hull, changing mast, changing rigging, camera pan, camera tracking, "
    "zoom, horizon movement, text, watermark, modern object"
)
EXPECTED_FILES = {
    ".gitattributes",
    "README.md",
    "examples/i2v_takeoff_source.png",
    "model_index.json",
    "scheduler/scheduler_config.json",
    "text_encoder/config.json",
    "text_encoder/model-00001-of-00003.safetensors",
    "text_encoder/model-00002-of-00003.safetensors",
    "text_encoder/model-00003-of-00003.safetensors",
    "text_encoder/model.safetensors.index.json",
    "tokenizer/tokenizer.json",
    "tokenizer/tokenizer_config.json",
    *{f"transformer/{index}.safetensors" for index in range(14)},
    "transformer/model.safetensors.index.json",
    *{f"transformer_2/{index}.safetensors" for index in range(14)},
    "transformer_2/model.safetensors.index.json",
    "vae/0.safetensors",
    "vae/model.safetensors.index.json",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify Slice 008 configuration and evidence.")
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
    require(header[:8] == b"\x89PNG\r\n\x1a\n", f"not a PNG: {path}")
    require(header[12:16] == b"IHDR", f"missing PNG IHDR: {path}")
    return struct.unpack(">II", header[16:24])


def expand_portable(path: str) -> Path:
    return Path(path).expanduser().resolve()


def command_output(command: list[str]) -> str:
    return subprocess.run(command, check=True, capture_output=True, text=True).stdout


def verify_configuration(repo_root: Path, benchmark: dict, model: dict, runtime: dict) -> None:
    require(benchmark["benchmark_id"] == BENCHMARK_ID, "benchmark id drift")
    require(benchmark["status"] == "inference-authorized-frozen", "benchmark execution status drift")
    require(benchmark["baseline_commit"] == BASELINE_COMMIT, "merged baseline drift")
    require(benchmark["execution_authorization"].startswith("Owner pasted"), "execution authorization missing")

    benchmark_model = benchmark["model"]
    require(benchmark_model["repository"] == MODEL_REPOSITORY, "benchmark model repository drift")
    require(benchmark_model["revision"] == MODEL_REVISION, "benchmark model revision drift")
    require(benchmark_model["source_repository"] == SOURCE_REPOSITORY, "source repository drift")
    require(benchmark_model["source_revision"] == SOURCE_REVISION, "source revision drift")
    require(benchmark_model["file_count"] == 44, "model file-count drift")
    require(benchmark_model["size_bytes"] == MODEL_SIZE_BYTES, "model size drift")
    require(benchmark_model["precision"] == "BF16", "model precision drift")
    require(benchmark_model["download_authorized"] is False, "model download was authorized")

    benchmark_runtime = benchmark["runtime"]
    require(benchmark_runtime["version"] == RUNTIME_VERSION, "runtime version drift")
    require(benchmark_runtime["source_commit"] == RUNTIME_COMMIT, "runtime commit drift")
    require(benchmark_runtime["wheel_sha256"] == RUNTIME_WHEEL_SHA256, "runtime wheel drift")
    require(benchmark_runtime["executable"].endswith("/.venv/bin/mlxgen-generate-wan"), "wrong runtime executable")
    require(benchmark_runtime["endpoint_option"] == "--last-image", "endpoint option drift")
    require(benchmark_runtime["generic_wrapper_exposes_endpoint_option"] is False, "generic wrapper claim drift")

    anchors = benchmark["anchors"]
    for name, expected_hash in (("first", FIRST_SHA256), ("last", LAST_SHA256)):
        record = anchors[name]
        path = repo_root / record["path"]
        require(path.is_file(), f"missing {name} anchor")
        require(sha256(path) == record["sha256"] == expected_hash, f"{name} anchor hash drift")
        require(png_dimensions(path) == (record["width"], record["height"]) == (1672, 940), f"{name} anchor dimensions drift")
        ignored = subprocess.run(["git", "check-ignore", "-q", str(path.relative_to(repo_root))], cwd=repo_root).returncode == 0
        require(ignored and record["git_ignored"] is True, f"{name} anchor is not Git-ignored")
    require(anchors["rights_status"] == "internal-evaluation-only-unresolved-user-reference-lineage", "rights boundary drift")

    first_provenance = load_json(repo_root / "outputs/next-slice-reference-candidates/right-facing-aegean-galley-start-frame-candidate-v2.provenance.json")
    last_provenance = load_json(repo_root / "outputs/next-slice-reference-candidates/right-facing-aegean-galley-approved-end-frame-v1.provenance.json")
    require(first_provenance["sha256"] == FIRST_SHA256, "first-anchor provenance drift")
    require(last_provenance["sha256"] == LAST_SHA256, "last-anchor provenance drift")
    require(benchmark["prompt"] == POSITIVE_PROMPT, "positive prompt drift")
    require(benchmark["negative_prompt"] == NEGATIVE_PROMPT, "negative prompt drift")

    parameters = benchmark["parameters"]
    require(parameters["task"] == "image-to-video", "task drift")
    require((parameters["requested_width"], parameters["requested_height"]) == (448, 256), "canvas drift")
    require(parameters["canvas_policy"] == "source-aspect" and parameters["resize_mode"] == "resize", "canvas policy drift")
    require((parameters["frames"], parameters["fps"], parameters["steps"]) == (41, 8, 15), "frame/fps/step drift")
    require(parameters["seed"] == 42, "seed drift")
    require((parameters["guidance"], parameters["guidance_2"], parameters["flow_shift"]) == (4.0, 3.0, 3.0), "guidance drift")
    require(parameters["solver"] == "unipc", "solver drift")
    require(parameters["low_ram"] and parameters["metadata"], "low-RAM or metadata missing")
    require(parameters["prompt_cache"] is False and parameters["release_inactive_denoiser"] is True, "cache or denoiser-release drift")
    for name in ("prompt_extension", "cache_acceleration", "video_to_video_input", "parallel_process", "cloud_service", "api_key", "compile_transformer"):
        require(parameters[name] is False, f"forbidden parameter enabled: {name}")
    require(parameters["lora"] is None and parameters["lightning_adapter"] is None, "adapter configured")

    safety = benchmark["safety"]
    expected_safety = {
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
    require(all(safety[key] == value for key, value in expected_safety.items()), "safety threshold drift")
    require(safety["sequential_only"] is True, "sequential-only rule missing")
    require(benchmark["run"]["run_id"] == RUN_ID, "run id drift")
    require(benchmark["run"]["maximum_generation_attempts_after_denoising_starts"] == 1, "one-attempt rule drift")
    require(len(benchmark["hard_gates"]) == 12, "hard-gate count drift")
    require(benchmark["failure_policy"]["no_automatic_rerun_after_denoising_starts"] is True, "no-rerun rule missing")
    restrictions = benchmark["slice_restrictions"]
    require(restrictions["inference_authorized"] is True, "single inference is not authorized")
    require(restrictions["slice_004_remains_postponed"] is True, "Slice 004 disposition drift")
    require(all(restrictions[key] is False for key in restrictions if key not in {"inference_authorized", "slice_004_remains_postponed"}), "forbidden slice authority enabled")

    require(model["model_repository"] == MODEL_REPOSITORY and model["model_revision"] == MODEL_REVISION, "model manifest identity drift")
    require(model["expected_file_count"] == 44 and model["expected_size_bytes"] == MODEL_SIZE_BYTES, "model manifest inventory drift")
    require(set(model["expected_files"]) == EXPECTED_FILES, "model allowlist drift")
    require(runtime["version"] == RUNTIME_VERSION and runtime["source_commit"] == RUNTIME_COMMIT, "runtime manifest drift")
    require(runtime["wheel_sha256"] == RUNTIME_WHEEL_SHA256, "runtime manifest wheel drift")
    lockfile = repo_root / runtime["lockfile"]
    lock_text = lockfile.read_text(encoding="utf-8")
    require(RUNTIME_WHEEL_SHA256 in lock_text, "runtime wheel hash missing from lockfile")
    require('name = "mlx-gen"' in lock_text and 'version = "0.33.1"' in lock_text, "runtime lock drift")

    document = (repo_root / "docs/slice-008-corrected-first-last-motion-scout.md").read_text(encoding="utf-8")
    for value in (BENCHMARK_ID, MODEL_REPOSITORY, MODEL_REVISION, RUNTIME_COMMIT, RUNTIME_WHEEL_SHA256, FIRST_SHA256, LAST_SHA256):
        require(value in document, f"Slice 008 document missing exact value: {value}")
    runner = (repo_root / "scripts/run-slice-008-motion-scout.sh").read_text(encoding="utf-8")
    for value in (POSITIVE_PROMPT, NEGATIVE_PROMPT, "mlxgen-generate-wan", "--image-path", "--last-image", "--release-inactive-denoiser", "--no-prompt-cache", "--json-events", "--no-replace"):
        require(value in runner, f"runner missing frozen value: {value[:48]}")
    require('"$runtime_cli"\n  generate' not in runner, "runner uses the generic generate subcommand")

    tracked = set(command_output(["git", "-C", str(repo_root), "ls-files"]).splitlines())
    forbidden_suffixes = {".safetensors", ".ckpt", ".pt", ".pth", ".gguf", ".mp4", ".mov", ".mkv", ".webm"}
    require(not [path for path in tracked if Path(path).suffix.lower() in forbidden_suffixes], "tracked model weight or video found")


def verify_no_inference_process() -> None:
    process_lines = command_output(["ps", "-axo", "pid=,command="]).splitlines()
    patterns = ("mlxgen generate", "mlxgen-generate-wan", "mflux.models.wan.cli.wan_generate", "comfyui")
    matches = []
    for line in process_lines:
        lowered = line.lower()
        if any(pattern in lowered for pattern in patterns) or ("diffusers" in lowered and ("generate" in lowered or "inference" in lowered)):
            matches.append(line.strip())
    require(not matches, f"another model-inference process is running: {matches}")


def verify_preflight(repo_root: Path, model: dict, runtime: dict) -> None:
    verify_no_inference_process()
    runtime_root = expand_portable(runtime["environment_root"])
    runtime_python = runtime_root / ".venv/bin/python"
    wan_cli = runtime_root / ".venv/bin/mlxgen-generate-wan"
    generic_cli = runtime_root / ".venv/bin/mlxgen"
    require(runtime_root.is_relative_to((Path.home() / "models").resolve()), "runtime is outside ~/models")
    require(runtime["status"] == "complete" and runtime["installed"] is True, "runtime is not complete")
    require(runtime_python.is_file() and wan_cli.is_file() and generic_cli.is_file(), "runtime executable missing")
    probe_script = (
        "import importlib.metadata, json, mlx.core as mx, platform; "
        "print(json.dumps({'mlx_gen': importlib.metadata.version('mlx-gen'), "
        "'machine': platform.machine(), 'metal_available': mx.metal.is_available()}))"
    )
    probe = json.loads(command_output([str(runtime_python), "-c", probe_script]))
    require(probe["mlx_gen"] == RUNTIME_VERSION, "installed runtime version drift")
    require(probe["machine"] == "arm64" and probe["metal_available"] is True, "runtime Metal probe failed")
    wan_help = command_output([str(wan_cli), "--help"])
    generic_help = command_output([str(generic_cli), "generate", "--help"])
    require("--last-image" in wan_help, "direct Wan CLI lacks --last-image")
    require("--last-image" not in generic_help, "generic wrapper unexpectedly exposes --last-image")

    require(model["status"] == "complete" and model["downloaded"] is True, "model package is not complete")
    snapshot = expand_portable(model["snapshot_path"])
    require(snapshot.is_relative_to((Path.home() / "models").resolve()) and snapshot.is_dir(), "model snapshot missing or misplaced")
    records = {item["path"]: item for item in model["files"]}
    require(set(records) == EXPECTED_FILES, "downloaded model file set drift")
    require(sum(int(item["size_bytes"]) for item in records.values()) == MODEL_SIZE_BYTES, "downloaded model size drift")
    for filename, record in records.items():
        path = snapshot / filename
        require(path.is_file(), f"missing model file: {filename}")
        require(path.stat().st_size == record["size_bytes"], f"model file size drift: {filename}")
        require(sha256(path) == record["sha256"], f"model file hash drift: {filename}")

    memory = command_output(["memory_pressure"])
    memory_match = re.search(r"System-wide memory free percentage: (\d+)%", memory)
    require(memory_match is not None and int(memory_match.group(1)) >= 90, "less than 90% memory is free")
    swap = command_output(["sysctl", "-n", "vm.swapusage"])
    swap_match = re.search(r"used = ([0-9.]+)M", swap)
    require(swap_match is not None and float(swap_match.group(1)) == 0.0, "preflight swap is not zero")
    model_store = snapshot.parents[2]
    for path in (repo_root, model_store):
        lines = command_output(["df", "-Pk", str(path)]).splitlines()
        require(int(lines[-1].split()[3]) >= 125_829_120, f"less than 120 GiB free for {path}")
    thermal = command_output(["pmset", "-g", "therm"])
    require("No thermal warning level" in thermal and "No performance warning level" in thermal, "thermal or performance warning active")


def metric_from_time_log(log_text: str, label: str) -> int:
    match = re.search(rf"^\s*(\d+)\s+{re.escape(label)}$", log_text, re.MULTILINE)
    require(match is not None, f"missing time metric: {label}")
    return int(match.group(1))


def verify_result(repo_root: Path, benchmark: dict, allow_pending_review: bool) -> None:
    results_path = repo_root / "manifests/benchmarks/slice-008-corrected-first-last-motion-scout-results.json"
    require(results_path.is_file(), "Slice 008 results manifest missing")
    results = load_json(results_path)
    require(results["benchmark_id"] == BENCHMARK_ID and results["run_id"] == RUN_ID, "results identity drift")
    require(results["generation_attempts"] == 1 and results["technical_verdict"] == "pass", "technical result drift")
    require(results["model_revision"] == MODEL_REVISION and results["runtime_version"] == RUNTIME_VERSION, "result model/runtime drift")
    require(results["first_anchor_sha256"] == FIRST_SHA256 and results["last_anchor_sha256"] == LAST_SHA256, "result anchor drift")

    run_root = repo_root / "benchmarks/artifacts/slice-008" / RUN_ID
    summary = load_env(run_root / "summary.env")
    marker = run_root / "generation-attempt-started.marker"
    require(marker.is_file(), "attempt marker missing")
    require(summary["run_id"] == RUN_ID and summary["mode"] == "local-files-only", "summary identity drift")
    require(summary["inference_exit_code"] == "0" and summary["safety_stop"] == "none", "inference or safety failure")
    log_text = (run_root / "run.log").read_text(encoding="utf-8")
    final_denoise_event_count = log_text.count('"phase": "denoise"')
    sampled_denoise_event_count = int(summary["denoise_event_count"])
    require(summary["denoising_started"] == "1", "denoising-start evidence missing")
    require(final_denoise_event_count == 15, "runtime log does not contain all denoising steps")
    require(1 <= sampled_denoise_event_count <= final_denoise_event_count, "sampled denoising count drift")
    require(results["execution"]["runtime_denoise_event_count"] == final_denoise_event_count, "result runtime event count drift")
    require(results["execution"]["sampled_loop_denoise_event_count"] == sampled_denoise_event_count, "result sampled event count drift")
    require(results["execution"]["git_commit"] == summary["git_commit"], "result run commit drift")
    require(summary["full_decode"] == "pass" and summary["wrapper_closeout"] == "normal", "runner closeout drift")
    require(int(summary["duration_seconds"]) <= 14_400, "scout exceeded four hours")

    sample_rows = (run_root / "system-samples.tsv").read_text(encoding="utf-8").splitlines()[1:]
    require(bool(sample_rows), "system samples missing")
    columns = [row.split("\t", 6) for row in sample_rows]
    require(all(len(row) == 7 for row in columns), "malformed system sample")
    minimum_free = min(int(float(row[1])) for row in columns)
    maximum_swap = max(float(row[2]) for row in columns)
    maximum_tree_rss_kb = max(int(row[5]) for row in columns)
    minimum_repo_disk_kb = min(int(row[3]) for row in columns)
    minimum_model_disk_kb = min(int(row[4]) for row in columns)
    require(minimum_free > 10 and maximum_swap <= 8192, "memory or swap safety boundary reached")
    require(minimum_repo_disk_kb >= 104_857_600 and minimum_model_disk_kb >= 104_857_600, "disk safety boundary reached")
    require(all("No thermal warning" in row[6] and "No performance warning" in row[6] for row in columns), "thermal or performance warning observed")

    output = repo_root / benchmark["run"]["output"]
    require(output.is_file(), "scout output missing")
    require(sha256(output) == summary["output_sha256"] == results["output"]["sha256"], "output hash drift")
    require(output.stat().st_size == int(summary["output_size_bytes"]) == results["output"]["size_bytes"], "output size drift")
    probe = load_json(run_root / "ffprobe.json")
    video = next(stream for stream in probe["streams"] if stream.get("codec_name"))
    require(video["codec_name"] == "h264" and video["pix_fmt"] == "yuv420p", "output codec or pixel format drift")
    require(video["nb_frames"] == "41" and video["r_frame_rate"] == "8/1", "output frame/fps drift")
    require((video["width"], video["height"]) == (448, 256), "resolved output dimensions drift")
    require(abs(float(probe["format"]["duration"]) - 5.125) <= 0.001, "output duration drift")
    require(results["output"]["full_decode"] == "pass", "results decode drift")
    subprocess.run(["ffmpeg", "-v", "error", "-i", str(output), "-f", "null", "-"], check=True)
    result_output = results["output"]
    require((result_output["codec"], result_output["pixel_format"]) == ("h264", "yuv420p"), "result codec drift")
    require((result_output["width"], result_output["height"], result_output["frames"], result_output["fps"]) == (448, 256, 41, 8), "result media dimensions drift")
    require(abs(float(result_output["duration_seconds"]) - 5.125) <= 0.001, "result duration drift")

    metadata_path = Path(summary["metadata"])
    metadata = load_json(metadata_path)
    require(sha256(metadata_path) == summary["metadata_sha256"] == results["output"]["metadata_sha256"], "metadata hash drift")
    require(Path(metadata["image_path"]).resolve() == Path(summary["first_image"]).resolve(), "metadata first anchor drift")
    require(Path(metadata["last_image_path"]).resolve() == Path(summary["last_image"]).resolve(), "metadata last anchor drift")
    require(metadata["prompt"] == POSITIVE_PROMPT and metadata["negative_prompt"] == NEGATIVE_PROMPT, "metadata prompt drift")
    require((metadata["width"], metadata["height"], metadata["frames"], metadata["fps"], metadata["steps"]) == (448, 256, 41, 8, 15), "metadata media parameters drift")
    require((metadata["seed"], metadata["guidance"], metadata["guidance_2"], metadata["flow_shift"], metadata["solver"]) == (42, 4.0, 3.0, 3.0, "unipc"), "metadata generation parameters drift")
    require(metadata["precision"] == "mlx.core.bfloat16" and metadata["quantize"] is None, "metadata precision drift")
    require(metadata["released_inactive_denoiser"] is True, "inactive denoiser was not released")
    require(results["runtime_generation_time_seconds"] == metadata["generation_time_seconds"], "runtime generation time drift")
    require(results["runtime_save_time_seconds"] == metadata["save_time_seconds"], "runtime save time drift")
    require(results["runtime_total_generation_time_seconds"] == metadata["total_generation_time_seconds"], "runtime total time drift")
    require(results["wrapper_duration_seconds"] == int(summary["duration_seconds"]), "wrapper duration drift")

    contact_sheet = Path(summary["contact_sheet"])
    require(contact_sheet.is_file(), "contact sheet missing")
    require(sha256(contact_sheet) == summary["contact_sheet_sha256"] == results["review_evidence"]["contact_sheet_sha256"], "contact-sheet hash drift")
    require(results["review_evidence"]["sampled_frame_numbers_zero_based"] == [0, 8, 16, 24, 32, 40], "contact-sheet frame selection drift")
    require(contact_sheet.stat().st_size == results["review_evidence"]["contact_sheet_size_bytes"], "contact-sheet size drift")
    require(png_dimensions(contact_sheet) == (results["review_evidence"]["contact_sheet_width"], results["review_evidence"]["contact_sheet_height"]), "contact-sheet dimensions drift")

    process_peak_rss = metric_from_time_log(log_text, "maximum resident set size")
    physical_peak = metric_from_time_log(log_text, "peak memory footprint")
    resources = results["resources"]
    require(resources["sample_count"] == len(columns), "sample count drift")
    require(resources["minimum_memory_free_percent"] == minimum_free, "result memory drift")
    require(resources["maximum_swap_mb"] == maximum_swap, "result swap drift")
    require(resources["maximum_sampled_process_tree_rss_kb"] == maximum_tree_rss_kb, "result sampled RSS drift")
    require(resources["minimum_repo_disk_available_kb"] == minimum_repo_disk_kb, "result repo disk drift")
    require(resources["minimum_model_disk_available_kb"] == minimum_model_disk_kb, "result model disk drift")
    require(resources["mlx_peak_memory_bytes"] == metadata["runtime_memory"]["mlx_peak_memory_bytes"], "result MLX peak drift")
    require(resources["process_peak_rss_bytes"] == process_peak_rss == metadata["runtime_memory"]["process_peak_rss_bytes"], "result process peak drift")
    require(resources["darwin_peak_physical_footprint_bytes"] == physical_peak == metadata["runtime_memory"]["darwin_peak_physical_footprint_bytes"], "result footprint drift")
    require(resources["thermal_warning_observed"] is False and resources["performance_warning_observed"] is False, "result warning drift")

    review = results["owner_motion_review"]
    require(set(review["hard_gates"]) == set(benchmark["hard_gates"]), "owner gate set drift")
    if review["status"] == "pending":
        require(allow_pending_review, "owner motion review is pending")
        require(results["status"] == "pending-owner-motion-review" and results["disposition"] == "pending", "pending result status drift")
        require(all(value == "pending" for value in review["hard_gates"].values()), "pending review has decided gates")
    else:
        require(not allow_pending_review, "remove --allow-pending-review after owner verdict")
        require(review["status"] in {"pass", "fail"}, "owner review status invalid")
        gate_values = set(review["hard_gates"].values())
        require(gate_values <= {"pass", "fail", "not_assessed"}, "owner gate verdict invalid")
        if review["status"] == "pass":
            require(gate_values == {"pass"}, "passing review must pass every hard gate")
        else:
            require("fail" in gate_values and results["disposition"] == "rejected-motion", "failed review disposition drift")
        require(results["status"] == "complete" and review["reviewed_at_utc"] and review["notes"], "review closeout incomplete")


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parent.parent
    benchmark = load_json(repo_root / "benchmarks/slice-008-corrected-first-last-motion-scout.json")
    model = load_json(repo_root / "manifests/models/wan2.2-i2v-a14b-bf16.json")
    runtime = load_json(repo_root / "manifests/runtimes/mlx-gen-0.33.1.json")
    verify_configuration(repo_root, benchmark, model, runtime)
    if args.preflight:
        require(not args.allow_pending_review, "--allow-pending-review is not valid with --preflight")
        verify_preflight(repo_root, model, runtime)
        print("slice-008-verification=pass state=preflight inference=one-attempt-authorized")
        return 0
    verify_result(repo_root, benchmark, args.allow_pending_review)
    state = "pending-owner-review" if args.allow_pending_review else "complete"
    print(f"slice-008-verification=pass state={state}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
