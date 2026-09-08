#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

[[ -f .env ]] || { echo "Missing .env; run scripts/generate_secrets.sh" >&2; exit 1; }
set -a; source .env; set +a

fail=0
check_cmd() {
  if command -v "$1" >/dev/null 2>&1; then
    printf '[OK] %s: %s\n' "$1" "$(command -v "$1")"
  else
    printf '[FAIL] missing command: %s\n' "$1" >&2
    fail=1
  fi
}

check_cmd docker
check_cmd openssl
check_cmd curl

if docker compose version >/dev/null 2>&1; then
  echo "[OK] docker compose: $(docker compose version --short)"
else
  echo "[FAIL] Docker Compose v2 is unavailable" >&2
  fail=1
fi

if [[ -d "$QWEN_MODEL_ROOT/snapshots/$QWEN_SNAPSHOT_ID" ]]; then
  echo "[OK] model snapshot exists"
else
  echo "[FAIL] missing model snapshot: $QWEN_MODEL_ROOT/snapshots/$QWEN_SNAPSHOT_ID" >&2
  fail=1
fi

if command -v nvidia-smi >/dev/null 2>&1; then
  echo "[OK] GPU inventory:"
  nvidia-smi --query-gpu=index,name,memory.total,memory.used --format=csv,noheader
else
  echo "[FAIL] nvidia-smi is unavailable" >&2
  fail=1
fi

if docker info 2>/dev/null | grep -qi 'nvidia'; then
  echo "[OK] NVIDIA runtime appears in docker info"
else
  echo "[WARN] NVIDIA runtime was not obvious in docker info; test with:"
  echo "       docker run --rm --gpus 'device=0' ubuntu:24.04 nvidia-smi"
fi

docker compose config >/dev/null
echo "[OK] docker-compose.yml renders successfully"

exit "$fail"
