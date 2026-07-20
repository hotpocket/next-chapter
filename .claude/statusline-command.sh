#!/bin/bash
# StatusLine: Context % | Model | PWD

# Read JSON input from stdin (provided by Claude Code)
input=$(cat)

# Extract context percentage used (null if no messages yet)
CONTEXT_USED=$(echo "$input" | jq -r '.context_window.used_percentage // empty' 2>/dev/null)

# Extract model display name
MODEL=$(echo "$input" | jq -r '.model.display_name // empty' 2>/dev/null)

# Extract current directory from JSON, fallback to pwd
CURRENT_DIR=$(echo "$input" | jq -r '.workspace.current_dir // empty' 2>/dev/null)
if [ -z "$CURRENT_DIR" ]; then
  CURRENT_DIR=$(pwd)
fi

# Format: Context: X% | Model Name | /path/to/directory
if [ -n "$CONTEXT_USED" ]; then
  printf 'Context: %.0f%% | %s | %s' "$CONTEXT_USED" "$MODEL" "$CURRENT_DIR"
else
  # No messages yet, omit context percentage
  printf '%s | %s' "$MODEL" "$CURRENT_DIR"
fi
