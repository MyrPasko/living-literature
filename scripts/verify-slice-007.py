#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import os
import struct
import subprocess
from pathlib import Path


BENCHMARK_ID = "slice-007-wan-2.2-i2v-a14b-motion-scout"
MODEL_REPOSITORY = "AbstractFramework/wan2.2-i2v-a14b-diffusers-bf16"
MODEL_REVISION = "ef2a0bfe5b4ca7edb84c93f1675edb1a8bfe7d60"
SOURCE_REPOSITORY = "Wan-AI/Wan2.2-I2V-A14B-Diffusers"
SOURCE_REVISION = "596658fd9ca6b7b71d5057529bbf319ecbc61d74"
RUNTIME_VERSION = "0.33.1"
RUNTIME_COMMIT = "23cee803f10aacdf943a9565f7cd67c25c825080"
RUNTIME_WHEEL_SHA256 = "1a19e6510a166cbe0fe4975146813fb61adf98f0e073abb4e63f27f012882d0a"
MODEL_SIZE_BYTES = 68_791_046_058
STILL_SHA256 = "7e7f0a20ebaa62551cad700d7e17fecd0fdc68a7003c9e1eb2e846f7fd6ec0c7"
SOURCE_VIDEO_SHA256 = "ce7a61c21ef0811062ea6229b3ddf89c6843bdc6569234cab060915bd39f2ad4"
RUN_ID = "local-files-only-motion-scout-seed-42"
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
POSITIVE_PROMPT = (
    "Single continuous five-second shot, locked-off wide side view. A Late Bronze Age Aegean "
    "galley with a long black hull, curved prow and stern, one mast and one rectangular square sail "
    "moves steadily from left to right across a dark wine-colored sea before dawn. The bow always "
    "points right; the stern remains left. Moderate wind blows from left to right, naturally filling "
    "the sail and raising aligned wavelets. A small bow wave splits outward at the prow; a narrow "
    "foamy wake begins only behind the stern and trails leftward. Heavy purple clouds drift slowly. "
    "Stable geometry, physically coherent motion, no camera movement, text, or modern objects. "
    "Preserve the approved input image’s ship design, palette, atmosphere, framing, and horizon."
)
NEGATIVE_PROMPT = (
    "reverse playback, backward sailing, wake or foam ahead of the bow, wake extending forward, "
    "perfectly still water with a filled sail, deformed sail, changing hull geometry, extra mast, "
    "camera dolly, pan, zoom, text, watermark, modern vessel, blurry image, JPEG artifacts"
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Verify Slice 007 configuration and evidence.")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--configuration-only", action="store_true")
    mode.add_argument("--preflight", action="store_true")
    parser.add_argument("--allow-pending-review", action="store_true")
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


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def load_env(path: Path) -> dict[str, str]:
    values: dict[str, str] = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        key, separator, value = line.partition("=")
        require(bool(separator), f"malformed summary line: {line}")
        values[key] = value
    return values


def expand_portable(path: str) -> Path:
    return Path(path).expanduser().resolve()


def verify_configuration(repo_root: Path, benchmark: dict, model: dict, runtime: dict) -> None:
    require(benchmark["benchmark_id"] == BENCHMARK_ID, "benchmark id drift")
    require(benchmark["authorization"].startswith("Owner approved"), "owner plan authorization missing")
    require(benchmark["model"]["repository"] == MODEL_REPOSITORY, "benchmark model repository drift")
    require(benchmark["model"]["revision"] == MODEL_REVISION, "benchmark model revision drift")
    require(benchmark["model"]["source_repository"] == SOURCE_REPOSITORY, "source repository drift")
    require(benchmark["model"]["source_revision"] == SOURCE_REVISION, "source revision drift")
    require(benchmark["model"]["file_count"] == 44, "model file count drift")
    require(benchmark["model"]["size_bytes"] == MODEL_SIZE_BYTES, "model byte total drift")
    require(benchmark["model"]["precision"] == "BF16", "precision drift")
    require(benchmark["runtime"]["version"] == RUNTIME_VERSION, "runtime version drift")
    require(benchmark["runtime"]["source_commit"] == RUNTIME_COMMIT, "runtime commit drift")
    require(benchmark["runtime"]["wheel_sha256"] == RUNTIME_WHEEL_SHA256, "runtime wheel drift")
    require(benchmark["source_still"]["candidate_id"] == "D", "selected still drift")
    require(benchmark["source_still"]["sha256"] == STILL_SHA256, "selected still hash drift")
    require(benchmark["source_still"]["source_video_sha256"] == SOURCE_VIDEO_SHA256, "source video drift")
    require(benchmark["prompt"] == POSITIVE_PROMPT, "positive prompt drift")
    require(benchmark["negative_prompt"] == NEGATIVE_PROMPT, "negative prompt drift")

    parameters = benchmark["parameters"]
    require(parameters["task"] == "image-to-video", "task drift")
    require((parameters["requested_width"], parameters["requested_height"]) == (448, 256), "canvas drift")
    require(parameters["canvas_policy"] == "source-aspect", "canvas policy drift")
    require((parameters["frames"], parameters["fps"], parameters["steps"]) == (41, 8, 15), "frame/fps/step drift")
    require(parameters["seed"] == 42, "seed drift")
    require((parameters["guidance"], parameters["guidance_2"], parameters["flow_shift"]) == (4.0, 3.0, 3.0), "guidance drift")
    require(parameters["solver"] == "unipc", "solver drift")
    require(parameters["low_ram"] and parameters["metadata"], "low-RAM or metadata missing")
    require(parameters["prompt_cache"] is False, "prompt cache must be disabled")
    for name in (
        "prompt_extension",
        "cache_acceleration",
        "video_to_video_input",
        "parallel_process",
        "cloud_service",
        "api_key",
        "compile_transformer",
    ):
        require(parameters[name] is False, f"forbidden parameter enabled: {name}")
    require(parameters["lora"] is None and parameters["lightning_adapter"] is None, "adapter configured")

    safety = benchmark["safety"]
    require(safety["minimum_preflight_memory_free_percent"] == 90, "preflight memory drift")
    require(safety["required_preflight_swap_mb"] == 0, "preflight swap drift")
    require(safety["minimum_disk_before_download_gib"] == 180, "download disk drift")
    require(safety["minimum_disk_before_inference_gib"] == 120, "inference disk drift")
    require(safety["stop_memory_free_percent"] == 10, "memory stop drift")
    require(safety["stop_swap_above_mb"] == 8192, "swap stop drift")
    require(safety["stop_disk_below_gib"] == 100, "disk stop drift")
    require(safety["stop_progress_silence_seconds"] == 1200, "progress stop drift")
    require(safety["maximum_run_seconds"] == 14400, "runtime stop drift")
    require(safety["sequential_only"] is True, "sequential-only rule missing")
    require(benchmark["run"]["maximum_generation_attempts_after_denoising_starts"] == 1, "one-shot rule drift")
    require(len(benchmark["hard_gates"]) == 10, "hard-gate count drift")
    require(benchmark["failure_policy"]["no_automatic_rerun_after_denoising_starts"] is True, "no-rerun rule missing")
    require(len(benchmark["failure_policy"]["forbidden_after_failure"]) == 7, "failure boundary drift")
    require(all(value is False for key, value in benchmark["slice_restrictions"].items() if key != "slice_004_remains_postponed"), "forbidden slice authority enabled")
    require(benchmark["slice_restrictions"]["slice_004_remains_postponed"] is True, "Slice 004 disposition drift")

    require(model["model_repository"] == MODEL_REPOSITORY, "model manifest repository drift")
    require(model["model_revision"] == MODEL_REVISION, "model manifest revision drift")
    require(model["expected_file_count"] == 44, "model expected count drift")
    require(model["expected_size_bytes"] == MODEL_SIZE_BYTES, "model expected size drift")
    require(set(model["expected_files"]) == EXPECTED_FILES, "model allowlist drift")
    require(runtime["version"] == RUNTIME_VERSION, "runtime manifest version drift")
    require(runtime["source_commit"] == RUNTIME_COMMIT, "runtime manifest commit drift")
    require(runtime["wheel_sha256"] == RUNTIME_WHEEL_SHA256, "runtime manifest wheel drift")
    lockfile = repo_root / runtime["lockfile"]
    require(lockfile.is_file(), "runtime lockfile missing")
    lock_text = lockfile.read_text(encoding="utf-8")
    require(RUNTIME_WHEEL_SHA256 in lock_text, "runtime wheel hash missing from lockfile")
    require('name = "mlx-gen"' in lock_text and 'version = "0.33.1"' in lock_text, "runtime lock drift")

    document = (repo_root / "docs/slice-007-wan-2.2-i2v-a14b-motion-scout.md").read_text(encoding="utf-8")
    require(document.count(POSITIVE_PROMPT) == 1, "positive prompt must appear once in the document")
    require(document.count(NEGATIVE_PROMPT) == 1, "negative prompt must appear once in the document")
    for text in (BENCHMARK_ID, MODEL_REPOSITORY, MODEL_REVISION, RUNTIME_COMMIT, RUNTIME_WHEEL_SHA256, STILL_SHA256):
        require(text in document, f"decision document missing exact value: {text}")

    tracked = set(subprocess.run(["git", "ls-files"], cwd=repo_root, check=True, capture_output=True, text=True).stdout.splitlines())
    forbidden_suffixes = {".safetensors", ".ckpt", ".pt", ".pth", ".gguf", ".mp4", ".mov", ".mkv", ".webm"}
    require(not [path for path in tracked if Path(path).suffix.lower() in forbidden_suffixes], "tracked model weight or video found")


def verify_preflight(repo_root: Path, model: dict, runtime: dict) -> None:
    still = repo_root / "outputs/slice-006/source-still-candidates/candidate-d-frame-048.png"
    require(still.is_file(), "selected source still missing")
    require(sha256(still) == STILL_SHA256, "selected source still hash drift")
    require(png_dimensions(still) == (832, 480), "selected source still dimensions drift")
    ignored = subprocess.run(["git", "check-ignore", "-q", str(still.relative_to(repo_root))], cwd=repo_root).returncode == 0
    require(ignored, "selected source still is not Git-ignored")

    require(runtime["status"] == "complete" and runtime["installed"] is True, "runtime is not complete")
    runtime_root = expand_portable(runtime["environment_root"])
    require(runtime_root.is_relative_to((Path.home() / "models").resolve()), "runtime is outside ~/models")
    runtime_python = runtime_root / ".venv/bin/python"
    require(runtime_python.is_file(), "runtime Python missing")
    probe_script = (
        "import importlib.metadata, json, mlx.core as mx, platform; "
        "print(json.dumps({'mlx_gen': importlib.metadata.version('mlx-gen'), "
        "'mlx': importlib.metadata.version('mlx'), 'machine': platform.machine(), "
        "'metal_available': mx.metal.is_available()}))"
    )
    probe = json.loads(subprocess.run([str(runtime_python), "-c", probe_script], check=True, capture_output=True, text=True).stdout)
    require(probe["mlx_gen"] == RUNTIME_VERSION, "installed runtime version drift")
    require(probe["machine"] == "arm64" and probe["metal_available"] is True, "runtime Metal probe failed")

    require(model["status"] == "complete" and model["downloaded"] is True, "model download is not complete")
    snapshot = expand_portable(model["snapshot_path"])
    require(snapshot.is_relative_to((Path.home() / "models").resolve()), "model snapshot is outside ~/models")
    require(snapshot.is_dir(), "model snapshot missing")
    records = {item["path"]: item for item in model["files"]}
    require(set(records) == EXPECTED_FILES, "downloaded model file set drift")
    require(sum(int(item["size_bytes"]) for item in records.values()) == MODEL_SIZE_BYTES, "downloaded model size drift")
    for filename, record in records.items():
        path = snapshot / filename
        require(path.is_file(), f"missing model file: {filename}")
        require(path.stat().st_size == record["size_bytes"], f"model file size drift: {filename}")
        require(sha256(path) == record["sha256"], f"model file hash drift: {filename}")


def verify_result(repo_root: Path, benchmark: dict, allow_pending_review: bool) -> None:
    results_path = repo_root / "manifests/benchmarks/slice-007-wan2.2-i2v-a14b-motion-scout-results.json"
    require(results_path.is_file(), "Slice 007 results manifest missing")
    results = load_json(results_path)
    require(results["benchmark_id"] == BENCHMARK_ID, "results benchmark drift")
    require(results["run_id"] == RUN_ID, "results run id drift")
    require(results["generation_attempts"] == 1, "generation attempt count drift")
    require(results["model_revision"] == MODEL_REVISION, "results model revision drift")
    require(results["runtime_version"] == RUNTIME_VERSION, "results runtime drift")
    require(results["source_still_sha256"] == STILL_SHA256, "results still drift")

    run_root = repo_root / "benchmarks/artifacts/slice-007" / RUN_ID
    summary = load_env(run_root / "summary.env")
    require((run_root / "generation-attempt-started.marker").is_file(), "attempt marker missing")
    require(summary["run_id"] == RUN_ID, "summary run id drift")
    require(summary["mode"] == "local-files-only", "summary mode drift")
    require(summary["inference_exit_code"] == "0", "inference failed")
    require(summary["safety_stop"] == "none", "safety stop occurred")
    require(summary["denoising_started"] == "1", "denoising did not start")
    require(summary["full_decode"] == "pass", "full decode did not pass")
    require(summary["wrapper_closeout"] == "normal", "runner closeout drift")
    require(int(summary["duration_seconds"]) <= 14_400, "scout exceeded four hours")

    sample_rows = (run_root / "system-samples.tsv").read_text(encoding="utf-8").splitlines()[1:]
    require(bool(sample_rows), "system samples missing")
    columns = [row.split("\t") for row in sample_rows]
    minimum_free = min(int(float(row[1])) for row in columns)
    maximum_swap = max(float(row[2]) for row in columns)
    maximum_tree_rss_kb = max(int(row[5]) for row in columns)
    require(minimum_free > 10, "memory safety boundary reached")
    require(maximum_swap <= 8192, "swap safety boundary exceeded")
    require(all("No thermal warning" in row[6] and "No performance warning" in row[6] for row in columns), "thermal or performance warning observed")
    require(results["resources"]["minimum_memory_free_percent"] == minimum_free, "results memory drift")
    require(results["resources"]["maximum_swap_mb"] == maximum_swap, "results swap drift")
    require(results["resources"]["maximum_sampled_process_tree_rss_kb"] == maximum_tree_rss_kb, "results RSS drift")

    output = repo_root / benchmark["run"]["output"]
    require(output.is_file(), "scout output missing")
    require(sha256(output) == summary["output_sha256"] == results["output"]["sha256"], "output hash drift")
    require(output.stat().st_size == int(summary["output_size_bytes"]) == results["output"]["size_bytes"], "output size drift")
    probe = load_json(run_root / "ffprobe.json")
    video = next(stream for stream in probe["streams"] if stream.get("codec_name"))
    require(video["codec_name"] == "h264", "output codec drift")
    require(video["nb_frames"] == "41" and video["r_frame_rate"] == "8/1", "output frame/fps drift")
    require((video["width"], video["height"]) == (results["output"]["width"], results["output"]["height"]), "resolved dimensions drift")
    require(results["output"]["full_decode"] == "pass", "results decode drift")

    metadata = Path(summary["metadata"])
    require(metadata.is_file(), "runtime metadata missing")
    require(sha256(metadata) == summary["metadata_sha256"] == results["output"]["metadata_sha256"], "runtime metadata hash drift")
    effective = results["effective_parameters"]
    require(effective["frames"] == 41 and effective["fps"] == 8 and effective["steps"] == 15, "effective frame/fps/step drift")
    require(effective["seed"] == 42, "effective seed drift")
    require((effective["guidance"], effective["guidance_2"], effective["flow_shift"]) == (4.0, 3.0, 3.0), "effective guidance drift")
    require(effective["solver"] == "unipc" and effective["precision"] == "BF16", "effective solver or precision drift")

    review = results["owner_motion_review"]
    if review["status"] == "pending":
        require(allow_pending_review, "owner motion review is pending")
        require(all(value == "pending" for value in review["hard_gates"].values()), "pending review has decided gates")
    else:
        require(not allow_pending_review, "remove --allow-pending-review after owner verdict")
        require(review["status"] in {"pass", "fail"}, "owner review status invalid")
        require(set(review["hard_gates"]) == set(benchmark["hard_gates"]), "owner gate set drift")
        require(all(value in {"pass", "fail"} for value in review["hard_gates"].values()), "owner gate verdict missing")
        expected_status = "pass" if all(value == "pass" for value in review["hard_gates"].values()) else "fail"
        require(review["status"] == expected_status, "owner aggregate verdict drift")


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parent.parent
    benchmark = load_json(repo_root / "benchmarks/slice-007-wan-2.2-i2v-a14b-motion-scout.json")
    model = load_json(repo_root / "manifests/models/wan2.2-i2v-a14b-bf16.json")
    runtime = load_json(repo_root / "manifests/runtimes/mlx-gen-0.33.1.json")
    verify_configuration(repo_root, benchmark, model, runtime)
    if args.configuration_only:
        print("slice-007-verification=pass state=configuration")
        return 0
    verify_preflight(repo_root, model, runtime)
    if args.preflight:
        print("slice-007-verification=pass state=preflight")
        return 0
    verify_result(repo_root, benchmark, args.allow_pending_review)
    state = "pending-owner-review" if args.allow_pending_review else "complete"
    print(f"slice-007-verification=pass state={state}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
