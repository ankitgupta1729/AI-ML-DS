#!/bin/bash
# Fires on the `Stop` event — when Claude finishes responding to a turn.
# Reads the hook payload from stdin, appends a line to the log file,
# and exits 0 so Claude is allowed to stop normally.

set -euo pipefail

LOG_FILE="${CLAUDE_PROJECT_DIR}/logs/claude-hooks.log"
mkdir -p "$(dirname "$LOG_FILE")"

INPUT="$(cat)"
TIMESTAMP="$(date '+%Y-%m-%d %H:%M:%S')"
SESSION_ID="$(printf '%s' "$INPUT" | jq -r '.session_id // "unknown"')"

echo "[$TIMESTAMP] [DONE]     session=$SESSION_ID  Claude finished responding." >> "$LOG_FILE"

exit 0
