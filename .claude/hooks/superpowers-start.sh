#!/bin/bash
# Superpowers eklentisinin SessionStart hook'unun yerine geçer: eklentiler bu
# ortamda kullanılamadığı için beceriler .claude/skills altına kopyalandı ve
# using-superpowers rehberi oturum başında buradan bağlama eklenir.
set -euo pipefail

skill_md="$CLAUDE_PROJECT_DIR/.claude/skills/using-superpowers/SKILL.md"
[ -r "$skill_md" ] || exit 0

python3 - "$skill_md" <<'EOF'
import json, sys

content = open(sys.argv[1], encoding="utf-8").read()
context = (
    "<EXTREMELY_IMPORTANT>\nYou have superpowers.\n\n"
    "Superpowers skills are installed as project skills, so a reference like "
    "'superpowers:brainstorming' means the 'brainstorming' skill.\n\n"
    "**Below is the full content of your 'using-superpowers' skill - your "
    "introduction to using skills. For all other skills, use the 'Skill' tool:**\n\n"
    + content + "\n</EXTREMELY_IMPORTANT>"
)
print(json.dumps({"hookSpecificOutput": {"hookEventName": "SessionStart", "additionalContext": context}}))
EOF
