import re, sys, collections, json
from pathlib import Path
W = Path(r'C:\IALD\Central de Patentes\work\iald_v407_20261104')
CONF = re.compile(r'CONFIRMED|(?<![A-Za-z])confirmed|\bconfirmad[ao]s?\b|\bconfirmada\b', re.I)
seen = collections.OrderedDict()
for pkg in ('shared','haiku_expanded','sonnet_public'):
    t = (W/'app/packages'/pkg/'prefix.md').read_text('utf-8')
    for m in CONF.finditer(t):
        c = ' '.join(t[max(0,m.start()-140):m.end()+90].split())
        key = re.sub(r'[0-9a-f]{12,}', 'HEX', c)
        seen.setdefault(key, []).append(pkg)
rows = [{'ctx': k, 'pkgs': sorted(set(v)), 'n': len(v)} for k, v in seen.items()]
json.dump(rows, open('conf_contexts_all.json','w',encoding='utf8'), ensure_ascii=False, indent=1)
print(len(rows), 'distinct contexts (union of 3 prefixes)')
for i, r in enumerate(rows, 1):
    tag = ''.join({'shared':'S','haiku_expanded':'H','sonnet_public':'P'}[p] for p in r['pkgs'])
    print('[%d|%s] %s' % (i, tag, r['ctx']))
