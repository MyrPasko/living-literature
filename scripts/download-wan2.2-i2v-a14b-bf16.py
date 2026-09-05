#!/usr/bin/env python3

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
from datetime import datetime, timezone
from pathlib import Path

from huggingface_hub import HfApi, hf_hub_download


MODEL_REPOSITORY = "AbstractFramework/wan2.2-i2v-a14b-diffusers-bf16"
MODEL_REVISION = "ef2a0bfe5b4ca7edb84c93f1675edb1a8bfe7d60"
EXPECTED_FILE_COUNT = 44
EXPECTED_SIZE_BYTES = 68_791_046_058
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
    parser = argparse.ArgumentParser(description="Download and verify the exact Slice 007 BF16 package.")
    parser.add_argument(
        "--model-store",
        type=Path,
        default=Path(os.environ.get("LIVING_LITERATURE_MODEL_STORE", Path.home() / "models/huggingface/hub")),
    )
    parser.add_argument(
        "--expected-manifest",
        type=Path,
        default=repo_root / "manifests/models/wan2.2-i2v-a14b-bf16.json",
    )
    parser.add_argument(
        "--report",
        type=Path,
        default=repo_root / "benchmarks/artifacts/slice-007/model-download-report.json",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    repo_root = Path(__file__).resolve().parent.parent
    model_store = args.model_store.expanduser().resolve()
    allowed_root = (Path.home() / "models").resolve()
    if not model_store.is_relative_to(allowed_root):
        raise RuntimeError(f"Model store must remain below {allowed_root}")
    model_store.mkdir(parents=True, exist_ok=True)
    if shutil.disk_usage(model_store).free < MINIMUM_DISK_GIB * 1024**3:
        raise RuntimeError(f"Refusing download: {MINIMUM_DISK_GIB} GiB free required")

    expected = json.loads(args.expected_manifest.read_text(encoding="utf-8"))
    allowed_files = set(expected["expected_files"])
    if len(allowed_files) != EXPECTED_FILE_COUNT:
        raise RuntimeError("Expected manifest does not contain exactly 44 unique files")
    if expected["model_repository"] != MODEL_REPOSITORY or expected["model_revision"] != MODEL_REVISION:
        raise RuntimeError("Expected manifest model identity drift")

    started_at = datetime.now(timezone.utc).isoformat()
    info = HfApi().model_info(MODEL_REPOSITORY, revision=MODEL_REVISION, files_metadata=True)
    if info.sha != MODEL_REVISION:
        raise RuntimeError(f"Prepared-package revision drift: expected {MODEL_REVISION}, found {info.sha}")
    siblings = {item.rfilename: item for item in info.siblings}
    if set(siblings) != allowed_files:
        missing = sorted(allowed_files - set(siblings))
        unexpected = sorted(set(siblings) - allowed_files)
        raise RuntimeError(f"Remote inventory drift: missing={missing} unexpected={unexpected}")
    remote_size = sum(int(item.size) for item in siblings.values())
    if remote_size != EXPECTED_SIZE_BYTES:
        raise RuntimeError(f"Remote size drift: expected {EXPECTED_SIZE_BYTES}, found {remote_size}")
    print(f"Remote revision and {len(siblings)}-file inventory verified at {MODEL_REVISION}", flush=True)

    records: list[dict[str, object]] = []
    resolved_snapshot: Path | None = None
    for filename in sorted(allowed_files):
        remote = siblings[filename]
        print(f"Resolving {filename} at {MODEL_REVISION}", flush=True)
        resolved = Path(
            hf_hub_download(
                repo_id=MODEL_REPOSITORY,
                filename=filename,
                revision=MODEL_REVISION,
                cache_dir=model_store,
            )
        )
        if resolved_snapshot is None:
            relative_parts = resolved.relative_to(model_store).parts
            snapshot_index = relative_parts.index("snapshots")
            resolved_snapshot = model_store.joinpath(*relative_parts[: snapshot_index + 2])
        actual_size = resolved.stat().st_size
        if actual_size != remote.size:
            raise RuntimeError(f"Size mismatch for {filename}: expected {remote.size}, found {actual_size}")
        actual_hash = sha256(resolved)
        remote_lfs = getattr(remote, "lfs", None)
        lfs_hash = getattr(remote_lfs, "sha256", None) if remote_lfs is not None else None
        if lfs_hash is not None and actual_hash != lfs_hash:
            raise RuntimeError(f"LFS SHA-256 mismatch for {filename}")
        records.append(
            {
                "path": filename,
                "size_bytes": actual_size,
                "sha256": actual_hash,
                "remote_lfs_sha256": lfs_hash,
                "cache_path": str(resolved.relative_to(model_store)),
            }
        )
        print(f"Verified {filename}: {actual_size} bytes sha256={actual_hash}", flush=True)

    if resolved_snapshot is None:
        raise RuntimeError("No model files were resolved")
    report = {
        "model_repository": MODEL_REPOSITORY,
        "model_revision": MODEL_REVISION,
        "status": "complete",
        "download_started_at_utc": started_at,
        "download_completed_at_utc": datetime.now(timezone.utc).isoformat(),
        "cache_root": portable(model_store),
        "snapshot_path": portable(resolved_snapshot),
        "file_count": len(records),
        "size_bytes": sum(int(record["size_bytes"]) for record in records),
        "files": records,
    }
    if report["size_bytes"] != EXPECTED_SIZE_BYTES:
        raise RuntimeError("Downloaded inventory byte total drift")
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(f"slice-007-model-download=pass report={args.report}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
