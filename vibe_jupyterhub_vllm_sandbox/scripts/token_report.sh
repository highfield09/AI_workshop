#!/usr/bin/env bash
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
set -a; source .env; set +a

# Spend logs are written asynchronously, so very recent calls may take a few seconds to appear.
docker compose exec -T db psql -U litellm -d litellm -P pager=off <<'SQL'
SELECT
  COALESCE(NULLIF("user", ''), '(unattributed)') AS user_id,
  COUNT(*) AS requests,
  SUM(prompt_tokens) AS input_tokens,
  SUM(completion_tokens) AS output_tokens,
  SUM(total_tokens) AS total_tokens,
  ROUND(AVG(request_duration_ms)) AS avg_request_ms,
  MAX("endTime") AS last_request
FROM "LiteLLM_SpendLogs"
GROUP BY 1
ORDER BY total_tokens DESC NULLS LAST;
SQL
