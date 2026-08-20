#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
[[ -f .env ]] || { echo "Missing .env" >&2; exit 1; }
set -a; source .env; set +a

BASE="http://127.0.0.1:${LOCAL_GATEWAY_PORT:-4000}"

printf '1. Gateway rejects key-management route: '
status="$(curl -sS -o /dev/null -w '%{http_code}' "$BASE/key/generate")"
[[ "$status" == "404" ]] && echo PASS || { echo "FAIL ($status)"; exit 1; }

printf '2. Gateway rejects unauthenticated inference: '
status="$(curl -sS -o /dev/null -w '%{http_code}' \
  "$BASE/v1/chat/completions" \
  -H 'Content-Type: application/json' \
  -d '{"model":"classroom-qwen","messages":[{"role":"user","content":"test"}]}')"
[[ "$status" == "401" || "$status" == "403" ]] && echo PASS || { echo "FAIL ($status)"; exit 1; }

printf '3. Host does not publish raw vLLM port 8000: '
if docker compose port vllm 8000 2>/dev/null | grep -q .; then
  echo FAIL
  exit 1
fi
echo PASS

printf '4. vLLM only shares the internal backend network: '
container_id="$(docker compose ps -q vllm)"
networks="$(docker inspect -f '{{range $k, $v := .NetworkSettings.Networks}}{{$k}} {{end}}' "$container_id" 2>/dev/null || true)"
if [[ "$networks" == *"vibe-backend-net"* && "$networks" != *"vibe-jhub-net"* && "$networks" != *"vibe-public-net"* ]]; then
  echo PASS
else
  echo "FAIL/CHECK ($networks)"
  exit 1
fi
