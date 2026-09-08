#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
set -a; source .env; set +a

USER_ID="${1:-}"
if [[ -z "$USER_ID" ]]; then
  echo "Usage: $0 <jupyterhub-username>" >&2
  exit 1
fi

docker compose exec -T litellm python - "$USER_ID" "$LITELLM_MASTER_KEY" <<'PY'
import json
import sys
import urllib.parse
import urllib.request

user_id, master_key = sys.argv[1:]
url = "http://127.0.0.1:4000/user/info?" + urllib.parse.urlencode({"user_id": user_id})
request = urllib.request.Request(url, headers={"Authorization": f"Bearer {master_key}"})
with urllib.request.urlopen(request, timeout=15) as response:
    print(json.dumps(json.load(response), indent=2))
PY
