#!/usr/bin/env bash
set -euo pipefail

BASE_URL=${DARA_BASE_URL:-http://localhost:3000}
WEBHOOK_URL_ENV=${WEBHOOK_URL:-}
TIMEOUT=30  # Maximum time in seconds for each curl request

echo "Checking health..."
curl -fsS --max-time "$TIMEOUT" "$BASE_URL/health" >/dev/null

echo "Fetching model presets..."
PRESETS=$(curl -fsS --max-time "$TIMEOUT" "$BASE_URL/api/models/presets")
echo "$PRESETS" | grep -q '"active"'

echo "Switching model preset to fast..."
curl -fsS --max-time "$TIMEOUT" -X POST "$BASE_URL/api/models/presets/active" \
  -H "Content-Type: application/json" \
  -d '{"preset":"fast"}' >/dev/null

echo "Listing workflows..."
WORKFLOWS=$(curl -fsS --max-time "$TIMEOUT" "$BASE_URL/api/workflows")
WORKFLOW_ID=$(echo "$WORKFLOWS" | python -c "import json,sys; data=json.load(sys.stdin); match=[wf for wf in data if wf['id']=='agent0-smoke']; print(match[0]['id'] if match else data[0]['id'])")

echo "Starting workflow run..."
RUN=$(curl -fsS --max-time "$TIMEOUT" -X POST "$BASE_URL/api/workflows/run" \
  -H "Content-Type: application/json" \
  -d "{\"workflow_id\":\"$WORKFLOW_ID\",\"input\":{}}")
RUN_ID=$(echo "$RUN" | python -c "import json,sys; print(json.load(sys.stdin)['run_id'])")

STATUS=$(curl -fsS --max-time "$TIMEOUT" "$BASE_URL/api/workflows/run/$RUN_ID")

if echo "$STATUS" | grep -q '"waiting_approval"'; then
  APPROVAL_ID=$(echo "$STATUS" | python -c "import json,sys; data=json.load(sys.stdin); print(data['approvals'][0]['id'])")
  curl -fsS --max-time "$TIMEOUT" -X POST "$BASE_URL/api/workflows/run/$RUN_ID/approve" \
    -H "Content-Type: application/json" \
    -d "{\"approval_id\":\"$APPROVAL_ID\",\"decision\":\"approved\"}" >/dev/null
fi

if [ -n "$WEBHOOK_URL_ENV" ]; then
  echo "Webhook configured at $WEBHOOK_URL_ENV (verify receiver logs)."
else
  echo "WEBHOOK_URL not set; skipping webhook assertion."
fi

echo "Smoke test completed."
