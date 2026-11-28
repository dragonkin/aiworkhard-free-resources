#!/usr/bin/env python3
"""从 aiworkhard app.db 生成 GitHub 开源清单 README.md（含徽章/横幅/最新精选）。"""
import sqlite3, re
from datetime import datetime, timezone
DB = '/opt/aiworkhard/data/app.db'
BASE = 'https://www.aiworkhard.com'
LABEL = {'ai': '免费 AI / API', 'tool': '免费工具', 'server': '免费服务器', 'deal': '低价优惠',
         'chat': '免费聊天 / 编程', 'db': '免费数据库', 'media': '图片 / 视频生成',
         'store': '免费存储 / CDN', 'gpu': '免费 GPU / 算力', 'domain': '域名 / SSL / DNS'}
ORDER = ['ai', 'tool', 'server', 'gpu', 'chat', 'db', 'store', 'media', 'deal', 'domain']


def short(w, n=90):
    w = re.sub(r'\s+', ' ', str(w or '')).strip()
    return (w[:n] + '…') if len(w) > n else w


def main():
    today = datetime.now(timezone.utc).strftime('%Y-%m-%d')
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    rows = conn.execute('SELECT * FROM articles ORDER BY number DESC').fetchall()
    conn.close()
    total = len(rows)
    groups = {}
    for r in rows:
        groups.setdefault(r['cat'], []).append(r)
    newest = rows[:10]

    out = []
    out.append('<p align="center"><img src="assets/banner.png" width="820" alt="AI很忙 · 免费资源日报"/></p>')
    out.append('')
    out.append('<p align="center">**[中文](README.md) · [English](README.en.md)**</p>')
    out.append('')
    out.append('# AI很忙 · 全免费 AI / 服务器 / API 资源精选')
    out.append('')
    out.append('<p align="center">每天核实一条免费资源——免费 AI 模型 · 免费服务器 · 免费 API · 免费云算力 · 开源工具 · 低价优惠</p>')
    out.append('')
    out.append('![license](https://img.shields.io/badge/license-CC0--1.0-blue) '
               '![count](https://img.shields.io/badge/收录-%d+-blueviolet) '
               '![updated](https://img.shields.io/badge/更新-%s-brightgreen) '
               '![website](https://img.shields.io/badge/网站-%s-0B8CAD)' % (total, today, 'www.aiworkhard.com'))
    out.append('')
    out.append('> 每条资源都附 **免费额度 / 官方地址 / 操作步骤 / 坑点**，并带 `已核实` `免卡` `有风险` 状态标签，每日持续更新验证。')
    out.append('> 主站：**[AI很忙](%s/)** · 收录合计 **%d** 条' % (BASE, total))
    out.append('')

    # 最新精选
    out.append('## 🔥 最新精选')
    for r in newest:
        st = (r['status'] or '').strip()
        out.append('- **[%s](%s/a/%d)** [%s] — %s' % (r['title'], BASE, r['number'],
                                                      st if st else r['cat'], short(r['what'], 70) + ' · ' + datetime.fromtimestamp(r['updated_at'] or r['created_at']).strftime('%m-%d')))
    out.append('')

    # 目录
    out.append('## 📂 目录')
    out.append('| 分类 | 数量 |')
    out.append('|---|--|')
    for c in ORDER:
        if c in groups:
            out.append('| [%s](#%s) | %d |' % (LABEL[c], re.sub(r'\W+', '-', LABEL[c]).lower(), len(groups[c])))
    out.append('')

    # 分类正文
    for c in ORDER:
        if c not in groups:
            continue
        items = sorted(groups[c], key=lambda r: -r['number'])
        out.append('\n## %s\n' % LABEL[c])
        for r in items:
            st = (r['status'] or '').strip()
            out.append('- **[%s](%s/a/%d)** %s — %s' % (r['title'], BASE, r['number'],
                                                       ('`' + st + '`') if st else '', short(r['what']) + ' · ' + datetime.fromtimestamp(r['updated_at'] or r['created_at']).strftime('%m-%d')))
        out.append('')

    # 如何使用 / 说明
    out.append('---')
    out.append('## 📖 如何使用')
    out.append('1. 点任意标题进入该资源的**详情页** `%s/a/<编号>`，看它的【免费额度 / 官方地址 / 操作步骤 / 坑点】。' % BASE)
    out.append('2. 状态标签含义：`已核实`=实测可用 · `免卡`=无需绑卡 · `有风险`=可能是绕过玩法/易失效，谨慎使用。')
    out.append('3. 收藏本仓库 = 订阅每日更新的免费资源清单。')
    out.append('')
    out.append('## 🤝 一起维护')
    out.append('- 数据由 **[AI很忙](%s/)** 每日人工核实并更新。' % BASE)
    out.append('- 想收录你发现的免费资源，或发现某条已失效？点进对应详情页/提 Issue，我们会核查更新。')
    out.append('')
    out.append('## ⚠️ 免责声明')
    out.append('- 列表仅做聚合推荐，所有权利归各资源官方；**是否可用/是否合规**以官方最新信息为准。')
    out.append('- 标注 `有风险` 的条目可能随时失效或违反平台条款，请自行判断。')
    out.append('')
    out.append('---')
    out.append('<p align="center"><a href="%s/">www.aiworkhard.com</a> · 每天核实的免费资源日报</p>' % BASE)
    out.append('')
    print('\n'.join(out))


if __name__ == '__main__':
    main()