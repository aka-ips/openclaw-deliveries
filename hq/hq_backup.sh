#!/bin/bash
# HQ正本バックアップスクリプト（Mac mini用）
#
# 目的: ~/hq/（charter.md・tools/・spec/・GUIDE.md・bin/hq 等の正本）を
#       プライベートGitHubリポジトリへスナップショット保存する。
#       憲章の C3（秘密汚染）検査を通らない限りプッシュしない（不明＝不合格）。
#
# 使い方:
#   初回:   ./hq_backup.sh setup https://github.com/aka-ips/hq-backup.git
#   以後:   ./hq_backup.sh run     （cron / launchd で日次実行を推奨）
#
# 注意: バックアップ先は必ずプライベートリポジトリにすること。
set -euo pipefail

HQ_DIR="${HQ_DIR:-$HOME/hq}"
CMD="${1:-run}"

secret_scan() {
  # C3: 秘密汚染の簡易検査。1件でもヒットしたらプッシュ中止（fail-closed）
  local hits
  hits=$(grep -rEl \
    -e 'sk-(ant-)?[A-Za-z0-9_-]{20,}' \
    -e 'ghp_[A-Za-z0-9]{20,}' \
    -e 'github_pat_[A-Za-z0-9_]{20,}' \
    -e 'xox[baprs]-[A-Za-z0-9-]{10,}' \
    -e 'AKIA[0-9A-Z]{16}' \
    -e '\-\-\-\-\-BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY\-\-\-\-\-' \
    -e '[0-9]{9,10}:[A-Za-z0-9_-]{35}' \
    --exclude-dir=.git "$HQ_DIR" 2>/dev/null || true)
  if [ -n "$hits" ]; then
    echo "!! 秘密情報らしき文字列を検出したためプッシュを中止しました（不明＝不合格）" >&2
    echo "$hits" >&2
    echo "該当ファイルを .gitignore に追加するか、内容をマスクしてから再実行してください。" >&2
    exit 1
  fi
}

case "$CMD" in
  setup)
    REPO_URL="${2:?使い方: hq_backup.sh setup <プライベートrepoのURL>}"
    cd "$HQ_DIR"
    [ -d .git ] || git init -b main
    if [ ! -f .gitignore ]; then
      cat > .gitignore <<'EOF'
.env
*.env
*.key
*.pem
*secret*
*token*
vault/
logs/
*.log
__pycache__/
.DS_Store
EOF
    fi
    if git remote get-url origin >/dev/null 2>&1; then
      git remote set-url origin "$REPO_URL"
    else
      git remote add origin "$REPO_URL"
    fi
    secret_scan
    git add -A
    git commit -m "HQ snapshot (initial)" || true
    git push -u origin main
    echo "OK: 初回バックアップ完了 → $REPO_URL"
    ;;
  run)
    cd "$HQ_DIR"
    secret_scan
    git add -A
    if git diff --cached --quiet; then
      echo "変更なし（スキップ）"
      exit 0
    fi
    git commit -m "HQ snapshot $(date '+%Y-%m-%d %H:%M')"
    ok=""
    for i in 1 2 3 4; do
      if git push; then ok=1; break; fi
      sleep $((2 ** i))
    done
    [ -n "$ok" ] || { echo "!! プッシュ失敗（ネットワーク確認後に再実行）" >&2; exit 1; }
    echo "OK: バックアップ完了"
    ;;
  *)
    echo "使い方: hq_backup.sh setup <プライベートrepoのURL> | hq_backup.sh run" >&2
    exit 2
    ;;
esac
