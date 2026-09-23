#!/bin/zsh
# Bruk: verktoy/publish.sh "commit-melding"
set -e
cd "$(dirname "$0")/.."
python3 verktoy/lenker.py
git add -A
git -c user.name="Erlend Schei" -c user.email="erlend.schei@dig.oslo.kommune.no" commit -qm "$1"
git push -q
echo "pushet: $(git log --oneline | head -1)"
