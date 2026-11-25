#!/usr/bin/env bash
# AI很忙 GitHub 清单 一键同步
# 用法: ./sync.sh
# 作用: 把仓库自带的生成器拷到服务器 → 从站内数据库重生成最新 README → 本地 commit → 推 GitHub
# 前置: 已 gh 登录（gh auth status）；能 SSH 到网站服务器。
set -euo pipefail

VPS="ubuntu@129.225.166.250"
SSH_KEY="${SSH_KEY:-/tmp/vps2/id_rsa}"
VPS_RUN="/tmp/gen_gh_run.py"
REPO_DIR="$(cd "$(dirname "$0")" && pwd)"

echo "[1/3] 同步生成器并生成最新 README ..."
scp -i "$SSH_KEY" -o StrictHostKeyChecking=no "$REPO_DIR/tools/gen_readme.py" "$VPS:$VPS_RUN" >/dev/null
ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no -o ConnectTimeout=20 "$VPS" \
  "sudo chown ubuntu:ubuntu '$VPS_RUN' && sudo -u ubuntu python3 '$VPS_RUN'" > "$REPO_DIR/README.md"

echo "[2/3] 检查更新 ..."
cd "$REPO_DIR"
git add -A >/dev/null
if git diff --cached --quiet; then
  echo "   无变更，跳过提交。"
else
  git -c user.name="aiworkhard" -c user.email="aiworkhard@example.com" \
      commit -qm "sync: 资源清单更新 $(date -u +%Y-%m-%d)"
  echo "   已提交: $(git log --oneline -1)"
fi

echo "[3/3] 推送 GitHub ..."
git push origin master

# ---- 同步三个分类子仓库 ----
CATS="servers:server:免费服务器大全:永久免费云服务器/VPS精选 ai:ai:免费AI/API大全:免费AI模型/API精选 tools:tool:免费工具大全:免费开源工具精选"
for item in $CATS; do
  IFS=':' read -r sub cat name tag <<<"$item"
  FILE="$REPO_DIR/../aiworkhard-free-$sub"
  [ -d "$FILE" ] || continue
  echo "── 同步 $sub ..."
  scp -i "$SSH_KEY" -o StrictHostKeyChecking=no "$REPO_DIR/tools/gen_cat_readme.py" "$VPS:/tmp/gen_cat_run.py" >/dev/null
  ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no -o ConnectTimeout=20 "$VPS" \
    "sudo chown ubuntu:ubuntu /tmp/gen_cat_run.py && sudo -u ubuntu python3 /tmp/gen_cat_run.py $cat '$name' '$tag'" > "$FILE/README.md"
  ( cd "$FILE" \
    && git add -A \
    && git diff --cached --quiet \
       || git -c user.name="aiworkhard" -c user.email="aiworkhard@example.com" commit -qm "sync: $(date -u +%Y-%m-%d)" \
    && git push origin master ) >/dev/null 2>&1 || true
done

echo "完成 ✓"