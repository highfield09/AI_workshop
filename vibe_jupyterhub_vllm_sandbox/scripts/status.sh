#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

docker compose ps
echo
echo "GPU 0:"
nvidia-smi -i 0 --query-gpu=index,name,memory.total,memory.used,utilization.gpu --format=csv
