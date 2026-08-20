#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

BASE_URL="${1:-http://127.0.0.1:4000/v1}"
API_KEY="${OPENAI_API_KEY:-${2:-}}"

if [[ -z "$API_KEY" ]]; then
  echo "Set OPENAI_API_KEY to a student's virtual key or pass it as argument 2." >&2
  echo "The instructor can inspect the sandbox key mapping with scripts/show_student_keys.sh." >&2
  exit 1
fi

curl --fail-with-body --silent --show-error \
  "$BASE_URL/chat/completions" \
  -H "Authorization: Bearer $API_KEY" \
  -H 'Content-Type: application/json' \
  -d '{
    "model": "classroom-qwen",
    "messages": [
      {"role": "system", "content": "You are a concise biology coding tutor."},
      {"role": "user", "content": "Write one Python function that calculates GC percentage."}
    ],
    "max_tokens": 256,
    "temperature": 0.2
  }' | python -m json.tool
