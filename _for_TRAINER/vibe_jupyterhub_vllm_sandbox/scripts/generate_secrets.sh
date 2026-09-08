#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ENV_FILE="$ROOT/.env"
EXAMPLE="$ROOT/.env.example"

if [[ -e "$ENV_FILE" ]]; then
  echo "Refusing to overwrite existing $ENV_FILE" >&2
  exit 1
fi

python - "$EXAMPLE" "$ENV_FILE" <<'PY'
from __future__ import annotations

import json
import secrets
import sys
from pathlib import Path

source = Path(sys.argv[1])
target = Path(sys.argv[2])
lines = source.read_text().splitlines()

values: dict[str, str] = {}
for line in lines:
    if not line or line.lstrip().startswith("#") or "=" not in line:
        continue
    key, value = line.split("=", 1)
    values[key] = value.strip().strip("'").strip('"')

users = [u.strip() for u in values["JUPYTERHUB_ALLOWED_USERS"].split(",") if u.strip()]
passwords = {user: secrets.token_urlsafe(18) for user in users}

replacements = {
    "JUPYTERHUB_USER_PASSWORDS_JSON": "'" + json.dumps(passwords, separators=(",", ":")) + "'",
    "JUPYTERHUB_COOKIE_SECRET": secrets.token_hex(32),
    "LITELLM_MASTER_KEY": "sk-" + secrets.token_hex(24),
    "LITELLM_SALT_KEY": secrets.token_urlsafe(32),
    "VLLM_INTERNAL_KEY": "sk-" + secrets.token_hex(24),
    "POSTGRES_PASSWORD": secrets.token_urlsafe(24),
}

out: list[str] = []
for line in lines:
    key = line.split("=", 1)[0] if "=" in line else None
    if key in replacements:
        line = f"{key}={replacements[key]}"
    out.append(line)

target.write_text("\n".join(out) + "\n")
PY

chmod 600 "$ENV_FILE"
echo "Created $ENV_FILE with mode 600 and unique passwords for every allowed username."
echo "Run scripts/show_login_credentials.sh locally to view the generated test credentials."
echo "Review the model path, users, limits, and public-domain placeholders before starting."
