#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import importlib.metadata
import json
import os
import shutil
import subprocess
import urllib.request
from datetime import datetime, timezone
from pathlib import Path


RUNTIME_VERSION = "0.33.1"
RUNTIME_COMMIT = "23cee803f10aacdf943a9565f7cd67c25c825080"
WHEEL_NAME = "mlx_gen-0.33.1-py3-none-any.whl"
WHEEL_SHA256 = "1a19e6510a166cbe0fe4975146813fb61adf98f0e073abb4e63f27f012882d0a"
MINIMUM_DISK_GIB = 180


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as source:
        for chunk in iter(lambda: source.read(8 * 1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def portable(path: Path) -> str:
    resolved = path.resolve()
    try:
        return f"~/{resolved.relative_to(Path.home().resolve())}"
    except ValueError:
        return str(resolved)


def parse_args() -> argparse.Namespace:
    repo_root = Path(__file__).resolve().parent.parent
    parser = argparse.ArgumentParser(description="Prepare the isolated pinned Slice 007 MLX-Gen runtime.")
    parser.add_argument(
        "--runtime-root",
        type=Path,
        default=Path.home() / "models/living-literature/runtimes/mlx-gen-0.33.1",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=repo_root / "benchmarks/artifacts/slice-007/runtime-install-report.json",
    )
    return parser.parse_args()


def verify_pypi_wheel() -> None:
    with urllib.request.urlopen("https://pypi.org/pypi/mlx-gen/0.33.1/json", timeout=30) as response:
        payload = json.load(response)
    matches = [item for item in payload["urls"] if item["filename"] == WHEEL_NAME]
    if len(matches) != 1:
        raise RuntimeError(f"Expected one {WHEEL_NAME} on PyPI, found {len(matches)}")
    wheel = matches[0]
    if wheel["digests"]["sha256"] != WHEEL_SHA256 or wheel.get("yanked"):
        raise RuntimeError("Pinned MLX-Gen wheel metadata drifted")


def installed_packages(runtime_python: Path) -> list[dict[str, str]]:
    script = (
        "import importlib.metadata, json; "
        "print(json.dumps(sorted([{'name': d.metadata['Name'], 'version': d.version} "
        "for d in importlib.metadata.distributions()], key=lambda x: x['name'].lower())))"
    )
    output = subprocess.run(
        [str(runtime_python), "-c", script],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    return json.loads(output)


def runtime_probe(runtime_python: Path) -> dict[str, object]:
    script = (
        "import importlib.metadata, json, mlx.core as mx, platform; "
        "print(json.dumps({'mlx_gen': importlib.metadata.version('mlx-gen'), "
        "'mlx': importlib.metadata.version('mlx'), "
        "'torch': importlib.metadata.version('torch'), "
        "'transformers': importlib.metadata.version('transformers'), "
        "'python': platform.python_version(), 'machine': platform.machine(), "
        "'metal_available': mx.metal.is_available()}))"
    )
    output = subprocess.run(
        [str(runtime_python), "-c", script],
        check=True,
        capture_output=True,
        text=True,
    ).stdout
    return json.loads(output)


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parent.parent
    project_root = repo_root / "runtimes/mlx-gen-0.33.1"
    lockfile = project_root / "uv.lock"
    lock_text = lockfile.read_text(encoding="utf-8")
    if WHEEL_SHA256 not in lock_text or f'version = "{RUNTIME_VERSION}"' not in lock_text:
        raise RuntimeError("Runtime lockfile does not contain the pinned MLX-Gen wheel")
    if shutil.disk_usage(args.runtime_root.parent).free < MINIMUM_DISK_GIB * 1024**3:
        raise RuntimeError(f"Refusing runtime installation: {MINIMUM_DISK_GIB} GiB free required")

    verify_pypi_wheel()
    args.runtime_root.mkdir(parents=True, exist_ok=True)
    runtime_environment = args.runtime_root / ".venv"
    env = os.environ.copy()
    env.update(
        {
            "UV_CACHE_DIR": str(repo_root / ".cache/uv"),
            "UV_PYTHON_INSTALL_DIR": str(repo_root / ".python"),
            "UV_PROJECT_ENVIRONMENT": str(runtime_environment),
        }
    )
    subprocess.run(
        ["uv", "sync", "--frozen", "--project", str(project_root)],
        check=True,
        cwd=repo_root,
        env=env,
    )

    runtime_python = runtime_environment / "bin/python"
    runtime_cli = runtime_environment / "bin/mlxgen"
    if not runtime_python.is_file() or not runtime_cli.is_file():
        raise RuntimeError("Installed runtime is missing Python or mlxgen")
    probe = runtime_probe(runtime_python)
    if probe["mlx_gen"] != RUNTIME_VERSION:
        raise RuntimeError(f"Installed mlx-gen version drift: {probe['mlx_gen']}")
    if probe["machine"] != "arm64" or probe["metal_available"] is not True:
        raise RuntimeError(f"Host MLX/Metal probe failed: {probe}")

    report = {
        "runtime": "mlx-gen",
        "version": RUNTIME_VERSION,
        "source_commit": RUNTIME_COMMIT,
        "wheel": WHEEL_NAME,
        "wheel_sha256": WHEEL_SHA256,
        "license": "MIT",
        "installed_at_utc": datetime.now(timezone.utc).isoformat(),
        "environment_root": portable(args.runtime_root),
        "runtime_python": portable(runtime_python),
        "runtime_cli": portable(runtime_cli),
        "lockfile": str(lockfile.relative_to(repo_root)),
        "lockfile_sha256": sha256(lockfile),
        "python_version": probe["python"],
        "probe": probe,
        "installed_packages": installed_packages(runtime_python),
    }
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"slice-007-runtime-preparation=pass report={args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
