#!/usr/bin/env python3
"""生成某个分类子仓库的英文 README.en.md。
用法: python3 gen_cat_readme_en.py <cat> <repo名EN> <sloganEN>
例: python3 gen_cat_readme_en.py server free-servers 'Free Servers / VPS'"""
import sqlite3, re, sys
from datetime import datetime
DB = '/opt/aiworkhard/data/app.db'
BASE = 'https://www.aiworkhard.com'
MAIN = 'https://github.com/dragonkin/aiworkhard-free-resources'


def short(w, n=90):
    w = re.sub(r'\s+', ' ', str(w or '')).strip()
    return (w[:n] + '…') if len(w) > n else w


def main():
    cat, name_en, tagline = sys.argv[1], sys.argv[2], sys.argv[3]
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    rows = [r for r in conn.execute('SELECT * FROM articles ORDER BY number DESC')
            if r['cat'] == cat]
    conn.close()
    total = len(rows)
    out = []
    out.append('# %s\n' % name_en)
    out.append('> %s · curated by **AI很忙 (AI Hustle)**.' % tagline)
    out.append('> Full multi-category list: [aiworkhard-free-resources](%s)' % MAIN)
    out.append('> Live site: **[AI很忙](%s/)** · **%d** entries\n' % (BASE, total))
    out.append('### %s (%d)\n' % (name_en, total))
    for r in rows:
        st = (r['status'] or '').strip()
        out.append('- [%s](%s/a/%d) %s — %s' % (r['title'], BASE, r['number'],
                                               ('`' + st + '`') if st else '', short(r['what']) + ' · ' + datetime.fromtimestamp(r['updated_at'] or r['created_at']).strftime('%m-%d')))
    out.append('')
    out.append('---')
    out.append('> Note: free quotas change; see the source page `%s/a/<id>` for steps & caveats.' % BASE)
    print('\n'.join(out))


if __name__ == '__main__':
    main()