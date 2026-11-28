#!/usr/bin/env python3
"""生成英文版 README.en.md（英文结构 + 数据条目，标题保留原文以保可追溯）"""
import sqlite3, re
from datetime import datetime, timezone
DB = '/opt/aiworkhard/data/app.db'
BASE = 'https://www.aiworkhard.com'
LABEL = {'ai': 'Free AI / API', 'tool': 'Free Tools', 'server': 'Free Servers / VPS',
         'deal': 'Deals / Discounts', 'chat': 'Free Chat / Coding', 'db': 'Free Databases',
         'media': 'Image / Video Generation', 'store': 'Free Storage / CDN',
         'gpu': 'Free GPU / Compute', 'domain': 'Domains / SSL / DNS'}
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

    out = []
    out.append('# AI Hustle · Curated Free AI / Server / API Resources')
    out.append('')
    out.append('<p align="center"><img src="assets/banner.png" width="820" alt="AI很忙 banner"/></p>')
    out.append('')
    out.append('> One hand-verified free resource every day — free AI models, free servers, free APIs, free cloud GPU, open-source tools & deals.')
    out.append('> Each entry carries **free quota / official link / steps / pitfalls** with status tags (`verified`, `no-card`, `risky`).')
    out.append('> Main site: **[AI很忙](%s/)** · **%d** entries · last update **%s**' % (BASE, total, today))
    out.append('')
    out.append('### Top 10 latest')
    for r in rows[:10]:
        st = (r['status'] or '').strip()
        out.append('- [%s](%s/a/%d) [%s] — %s' % (r['title'], BASE, r['number'], st if st else r['cat'], short(r['what'], 70) + ' · ' + datetime.fromtimestamp(r['updated_at'] or r['created_at']).strftime('%m-%d')))
    out.append('')
    out.append('### Index')
    for c in ORDER:
        if c in groups:
            out.append('- **%s** (%d)' % (LABEL[c], len(groups[c])))
    out.append('')
    for c in ORDER:
        if c not in groups:
            continue
        items = sorted(groups[c], key=lambda r: -r['number'])
        out.append('## %s\n' % LABEL[c])
        for r in items:
            st = (r['status'] or '').strip()
            out.append('- [%s](%s/a/%d) %s — %s' % (r['title'], BASE, r['number'],
                                                   ('`' + st + '`') if st else '', short(r['what']) + ' · ' + datetime.fromtimestamp(r['updated_at'] or r['created_at']).strftime('%m-%d')))
        out.append('')
    out.append('---')
    out.append('Note: this is a curated list. Verify official current terms before use; entries tagged `risky` may expire or violate ToS.')
    out.append('Source: https://www.aiworkhard.com — a free-resources daily verified feed.')
    print('\n'.join(out))


if __name__ == '__main__':
    main()