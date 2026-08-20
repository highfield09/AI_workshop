#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

[[ -f .env ]] || { echo "Run scripts/generate_secrets.sh first" >&2; exit 1; }
set -a; source .env; set +a

docker compose up -d course-init db vllm litellm api-proxy jupyterhub

echo
echo "Local JupyterHub: http://127.0.0.1:${LOCAL_HUB_PORT:-8000}"
echo "Local API gateway: http://127.0.0.1:${LOCAL_GATEWAY_PORT:-4000}/v1"
echo "Follow model startup: docker compose logs -f vllm"
