#!/usr/bin/env bash
set -euo pipefail
PKG_DIR="$(cd "$(dirname "$0")" && pwd)"
REPO_PATH="${1:-$PKG_DIR/UBP_Repo}"
if [ ! -d "$REPO_PATH/.git" ]; then
  echo "[setup] Cloning UBP_Repo into $REPO_PATH"
  rm -rf "$REPO_PATH"
  git clone --depth 1 https://github.com/DigitalEuan/UBP_Repo.git "$REPO_PATH"
fi
cd "$REPO_PATH"
git fetch --depth 1 origin a024e223d6133fdac400a985c5ab6e8356dd3729 || true
git checkout a024e223d6133fdac400a985c5ab6e8356dd3729 || true
python3 "$PKG_DIR/src/reproduce_study.py" --repo-path "$REPO_PATH" --package-root "$PKG_DIR"
