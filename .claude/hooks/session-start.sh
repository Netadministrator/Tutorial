#!/bin/bash
# Bulut oturumu başlarken Drex için gereken Python kütüphanelerini kurar.
set -euo pipefail

if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
  exit 0
fi

python3 -m pip install -q --root-user-action=ignore -r "$CLAUDE_PROJECT_DIR/requirements.txt"
