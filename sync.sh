#!/usr/bin/env bash
# AI很忙 GitHub 清单 一键同步
# 用法: ./sync.sh
# 作用: 从站内数据库重生成最新 README → 本地 commit → 推送到 GitHub（保持仓库永远最新）
#
# 前置: 已配置 gh 登录（gh auth status），并能 SSH 到网站服务器。
set -euo pipefail

VPS="ubuntu@129.225.166.250"
SSH_KEY="${SSH_KEY:-/tmp/vps2/id_rsa}"
GEN_SCRIPT="${GEN_SCRIPT:-/tmp/gen_gh.py}"   # 服务器端的 README 生成脚本路径
REPO_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "[1/3] 从服务器拉取最新数据生成 README ..."
ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no -o ConnectTimeout=20 "$VPS" \
  "sudo -u ubuntu python3 '$GEN_SCRIPT'" > "$REPO_DIR/README.md"

echo "[2/3] 检查是否有更新 ..."
cd "$REPO_DIR"
git add -A >/dev/null
if git diff --cached --quiet; then
  echo "   无变更，跳过提交。"
else
  git -c user.name="aiworkhard" -c user.email="aiworkhard@example.com" \
      commit -qm "sync: 资源清单更新 $(date -u +%Y-%m-%d)"
  echo "   已提交: $(git log --oneline -1)"
fi

echo "[3/3] 推送到 GitHub ..."
gh repo set-default dragonkin/aiworkhard-free-resources 2>/dev/null || true
git push origin master

echo "完成 ✓"