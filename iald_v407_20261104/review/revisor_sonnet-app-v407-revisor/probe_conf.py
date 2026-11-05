import re, sys, collections
from pathlib import Path
W = Path(r'C:\IALD\Central de Patentes\work\iald_v407_20261104')
CONF = re.compile(r'CONFIRMED|(?<![A-Za-z])confirmed|\bconfirmad[ao]s?\b|\bconfirmada\b', re.I)
for pkg in ('shared','haiku_expanded','sonnet_public'):
    t = (W/'app/packages'/pkg/'prefix.md').read_text('utf-8')
    ms = list(CONF.finditer(t))
    print(pkg, len(ms), 'matches')
    # distinct contexts after normalising digits/hex
    ctx = collections.Counter()
    for m in ms:
        c = ' '.join(t[max(0,m.start()-110):m.end()+70].split())
        c = re.sub(r'[0-9a-f]{12,}', 'HEX', c)
        ctx[c] += 1
    print('  distinct contexts:', len(ctx))
