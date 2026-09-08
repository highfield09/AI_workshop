#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

[[ -f .env ]] || { echo "Run scripts/generate_secrets.sh first" >&2; exit 1; }
set -a; source .env; set +a

for value in LLM_DOMAIN ACME_EMAIL; do
  current="${!value:-}"
  if [[ -z "$current" || "$current" == *example.edu* ]]; then
    echo "Set a real $value in .env before enabling public HTTPS" >&2
    exit 1
  fi
done

docker compose --profile public up -d edge

echo "Public API: https://$LLM_DOMAIN/v1"
echo "JupyterHub remains localhost-only by design. Use VPN/SSH forwarding for this sandbox."
