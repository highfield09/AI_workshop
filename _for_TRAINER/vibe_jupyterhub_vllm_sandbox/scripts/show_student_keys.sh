#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "WARNING: these are live student credentials. Do not paste this output into chat or logs."
docker compose exec -T jupyterhub sh -c \
  'test -f /srv/jupyterhub/student_keys.json && cat /srv/jupyterhub/student_keys.json || echo "No keys have been provisioned yet; log in and start a user server first."'
