#!/usr/bin/env bash

set -euo pipefail

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
wan_path="$repo_root/third_party/mlx-examples"
wan_commit="796f5b53cab69a3d48a44233ce21aae889e94a08"

git -C "$repo_root" submodule update --init third_party/mlx-examples

if ! git -C "$wan_path" cat-file -e "${wan_commit}^{commit}" 2>/dev/null; then
  git -C "$wan_path" fetch --depth 1 origin "$wan_commit"
fi

git -C "$wan_path" checkout --detach "$wan_commit"
git -C "$wan_path" sparse-checkout init --no-cone
git -C "$wan_path" sparse-checkout set /LICENSE /video/wan2.1/

actual_commit="$(git -C "$wan_path" rev-parse HEAD)"
if [[ "$actual_commit" != "$wan_commit" ]]; then
  printf 'Wan source mismatch: expected %s, found %s\n' "$wan_commit" "$actual_commit" >&2
  exit 1
fi

printf 'Wan source ready at %s\n' "$actual_commit"
