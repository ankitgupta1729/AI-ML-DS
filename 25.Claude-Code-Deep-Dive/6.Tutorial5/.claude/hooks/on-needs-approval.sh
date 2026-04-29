#!/bin/bash
# Fires on the `Notification` event with matcher `permission_prompt` — Claude
# is asking the user to approve a tool call. We simply log the request; we do
# NOT auto-approve anything (Notification hooks cannot grant permission anyway).

set -euo pipefail

LOG_FILE="${CLAUDE_PROJECT_DIR}/logs/claude-hooks.log"
mkdir -p "$(dirname "$LOG_FILE")"

INPUT="$(cat)"
TIMESTAMP="$(date '+%Y-%m-%d %H:%M:%S')"
SESSION_ID="$(printf '%s' "$INPUT" | jq -r '.session_id // "unknown"')"
MESSAGE="$(printf '%s' "$INPUT" | jq -r '.message // "Permission required"')"

echo "[$TIMESTAMP] [APPROVAL] session=$SESSION_ID  $MESSAGE" >> "$LOG_FILE"

exit 0
