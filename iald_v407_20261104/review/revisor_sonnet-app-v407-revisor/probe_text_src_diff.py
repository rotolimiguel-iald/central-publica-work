import json
from pathlib import Path
R = Path(r'C:\IALD\projetos_pyhton\IALD'); V = Path(r'C:\IALD\Central de Patentes\vault\originals_copy\um_unificado_v407')
core = json.loads((V/'um_absoluto.json').read_bytes())['core']
m = json.loads((R/'iald_nucleo_fixo.json').read_bytes()); core6 = json.loads(Path(m['published_evidence']['result']['path']).read_bytes())['core']
def dd(a, b, p=''):
    if type(a) != type(b): yield (p, 'type'); return
    if isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a: yield (p+'/'+k, 'only-new')
            elif k not in b: yield (p+'/'+k, 'only-old')
            else: yield from dd(a[k], b[k], p+'/'+k)
    elif isinstance(a, list):
        if len(a) != len(b): yield (p, 'len %d->%d' % (len(b), len(a))); return
        for i, (x, y) in enumerate(zip(a, b)): yield from dd(x, y, p+'/%d' % i)
    elif a != b: yield (p, 'val')
for n in ['gw_angular_rite', 'h2_reproduction_result', 'small_diamond_lattice_v364', 'd1_camb_v3_pipeline']:
    d = list(dd(core[n], core6[n]))
    print(n, len(d), d[:6])
# all 70 changed topics: which top-level keys differ most often
import collections
c = collections.Counter()
for n in core:
    if n in core6 and core6[n] != core[n]:
        for p, k in dd(core[n], core6[n]):
            c[p.split('/')[-1]] += 1
print(c.most_common(12))
