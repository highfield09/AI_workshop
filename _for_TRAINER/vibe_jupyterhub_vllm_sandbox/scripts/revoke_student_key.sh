#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

USER_ID="${1:-}"
if [[ -z "$USER_ID" ]]; then
  echo "Usage: $0 <jupyterhub-username>" >&2
  exit 1
fi

if docker ps --format '{{.Names}}' | grep -Fxq "vibe-$USER_ID"; then
  echo "Stop $USER_ID's JupyterHub server before revoking its injected key." >&2
  exit 1
fi

docker compose exec -T jupyterhub python - "$USER_ID" <<'PY'
from __future__ import annotations

import json
import os
import sys
from pathlib import Path

import requests

username = sys.argv[1]
store_path = Path('/srv/jupyterhub/student_keys.json')
if not store_path.exists():
    raise SystemExit('No student key store exists')
store = json.loads(store_path.read_text())
record = store.get(username)
if not record or not record.get('key'):
    raise SystemExit(f'No cached key for {username}')

response = requests.post(
    os.environ['LITELLM_ADMIN_URL'].rstrip('/') + '/key/delete',
    headers={'Authorization': f"Bearer {os.environ['LITELLM_MASTER_KEY']}"},
    json={'keys': [record['key']]},
    timeout=30,
)
response.raise_for_status()
store.pop(username, None)
temp = store_path.with_suffix('.tmp')
temp.write_text(json.dumps(store, indent=2, sort_keys=True))
os.chmod(temp, 0o600)
temp.replace(store_path)
print(f'Revoked and removed cached key for {username}. The next server spawn will create a new key.')
PY
