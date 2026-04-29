#!/bin/bash
# Fires on the `PreToolUse` event — every time Claude is about to run a tool
# (Bash, Edit, Write, Read, Grep, …). Treat each upcoming tool call as a
# "pending task" and log which tool is about to run.

set -euo pipefail

LOG_FILE="${CLAUDE_PROJECT_DIR}/logs/claude-hooks.log"
mkdir -p "$(dirname "$LOG_FILE")"

INPUT="$(cat)"
TIMESTAMP="$(date '+%Y-%m-%d %H:%M:%S')"
SESSION_ID="$(printf '%s' "$INPUT" | jq -r '.session_id // "unknown"')"
TOOL_NAME="$(printf '%s' "$INPUT" | jq -r '.tool_name // "unknown"')"

# Pull a small detail per tool so the log is informative without dumping the whole payload.
case "$TOOL_NAME" in
  Bash)
    DETAIL="$(printf '%s' "$INPUT" | jq -r '.tool_input.command // ""' | head -c 120)"
    ;;
  Write|Edit|Read)
    DETAIL="$(printf '%s' "$INPUT" | jq -r '.tool_input.file_path // ""')"
    ;;
  *)
    DETAIL=""
    ;;
esac

echo "[$TIMESTAMP] [PENDING]  session=$SESSION_ID  tool=$TOOL_NAME  ${DETAIL:+detail=$DETAIL}" >> "$LOG_FILE"

exit 0
