#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
[[ -f .env ]] || { echo "Missing .env; run scripts/generate_secrets.sh" >&2; exit 1; }
set -a; source .env; set +a

echo "WARNING: login credentials follow. Run this only in a private terminal."
python - <<'PY'
import json
import os
passwords = json.loads(os.environ["JUPYTERHUB_USER_PASSWORDS_JSON"])
for username, password in passwords.items():
    print(f"{username}\t{password}")
PY
