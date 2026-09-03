#!/usr/bin/env bash

set -euo pipefail

machine_name="$(system_profiler SPHardwareDataType -json | plutil -extract SPHardwareDataType.0.machine_name raw -o - -)"
chip_name="$(system_profiler SPHardwareDataType -json | plutil -extract SPHardwareDataType.0.chip_type raw -o - -)"
processor_layout="$(system_profiler SPHardwareDataType -json | plutil -extract SPHardwareDataType.0.number_processors raw -o - -)"
physical_memory="$(system_profiler SPHardwareDataType -json | plutil -extract SPHardwareDataType.0.physical_memory raw -o - -)"
gpu_summary="$(system_profiler SPDisplaysDataType -detailLevel mini | sed -n -E '/Chipset Model:|Total Number of Cores:|Metal Support:/s/^[[:space:]]+//p')"

printf 'machine_name=%s\n' "$machine_name"
printf 'hardware_model=%s\n' "$(sysctl -n hw.model)"
printf 'chip=%s\n' "$chip_name"
printf 'architecture=%s\n' "$(uname -m)"
printf 'processor_layout=%s\n' "$processor_layout"
printf 'physical_cpu_cores=%s\n' "$(sysctl -n hw.physicalcpu)"
printf 'logical_cpu_cores=%s\n' "$(sysctl -n hw.logicalcpu)"
printf 'unified_memory=%s\n' "$physical_memory"
printf '%s\n' "$gpu_summary"
printf 'macos_version=%s\n' "$(sw_vers -productVersion)"
printf 'macos_build=%s\n' "$(sw_vers -buildVersion)"
printf 'disk_available=%s\n' "$(df -h "$PWD" | awk 'NR == 2 { print $4 }')"
memory_pressure | sed -n -E '/System-wide memory free percentage:/p'
printf 'swap=%s\n' "$(sysctl -n vm.swapusage)"
printf 'uv_path=%s\n' "$(command -v uv)"
printf 'uv_version=%s\n' "$(uv --version)"
printf 'ffmpeg_path=%s\n' "$(command -v ffmpeg)"
ffmpeg -version 2>&1 | sed -n '1p'
printf 'command_line_tools_path=%s\n' "$(xcode-select -p)"
pkgutil --pkg-info com.apple.pkg.CLTools_Executables | sed -n -E 's/^version: /command_line_tools_version=/p'
