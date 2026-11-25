#!/usr/bin/env python3
"""生成某个分类子仓库的 README.md。用法: python3 gen_cat_readme.py <cat> <repo简称> <一句话>
   例: python3 gen_cat_readme.py server 免费服务器 '永久免费云服务器 / VPS 精选'"""
import sqlite3, re, sys
DB = '/opt/aiworkhard/data/app.db'
BASE = 'https://www.aiworkhard.com'
MAIN = 'https://github.com/dragonkin/aiworkhard-free-resources'


def short(w, n=90):
    w = re.sub(r'\s+', ' ', str(w or '')).strip()
    return (w[:n] + '…') if len(w) > n else w


def main():
    cat, repo_name, tagline = sys.argv[1], sys.argv[2], sys.argv[3]
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row
    rows = [r for r in conn.execute('SELECT * FROM articles ORDER BY number DESC')
            if r['cat'] == cat]
    conn.close()
    total = len(rows)
    out = []
    out.append('# %s\n' % repo_name)
    out.append('> %s · 资料整理自 **AI很忙**。' % tagline)
    out.append('> 完整清单（全部分类）见主仓库：[aiworkhard-free-resources](%s)' % MAIN)
    out.append('> 主站：**[AI很忙](%s/)** · 本仓收录 **%d** 条\n' % (BASE, total))
    out.append('### %s（%d 条）\n' % (repo_name, total))
    for r in rows:
        st = (r['status'] or '').strip()
        out.append('- [%s](%s/a/%d) %s — %s' % (r['title'], BASE, r['number'],
                                               ('`' + st + '`') if st else '', short(r['what'])))
    out.append('\n> 说明：免费额度和可用性会变，领取步骤与坑点见原站详情页 %s/a/<编号>。' % BASE)
    print('\n'.join(out))


if __name__ == '__main__':
    main()