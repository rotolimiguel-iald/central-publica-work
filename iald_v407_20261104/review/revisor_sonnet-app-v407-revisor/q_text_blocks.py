"""Revisor sonnet-app-v407-revisor -- blocos TEXT (sinteses em prosa, nao restauraveis por maquina): quais tem fonte alterada na v407 e o que mudou na fonte. Somente leitura."""
import json, sys
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).parent; sys.path.insert(0, str(HERE))
import lib405 as L
W = Path(r'C:\IALD\Central de Patentes\work\iald_v407_20261104'); R = Path(r'C:\IALD\projetos_pyhton\IALD'); V = Path(r'C:\IALD\Central de Patentes\vault\originals_copy\um_unificado_v407')
core = json.loads((V / 'um_absoluto.json').read_bytes())['core']
m = json.loads((R / 'iald_nucleo_fixo.json').read_bytes()); core6 = json.loads(Path(m['published_evidence']['result']['path']).read_bytes())['core']
P = L.parse_prefix((W / 'app/packages/shared/prefix.md').read_text('utf-8')); Po = L.parse_prefix((R / '.iald_runtime/haiku/prefix.md').read_text('utf-8'))
def dd(a, b, p=''):
    if type(a) != type(b): yield (p, 'type'); return
    if isinstance(a, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a: yield (p + '/' + k, 'only-new')
            elif k not in b: yield (p + '/' + k, 'only-old')
            else: yield from dd(a[k], b[k], p + '/' + k)
    elif isinstance(a, list):
        if len(a) != len(b): yield (p, 'len'); return
        for i, (x, y) in enumerate(zip(a, b)): yield from dd(x, y, p + '/%d' % i)
    elif a != b: yield (p, 'val')
tx = [n for n in core if n in P['body'] and L.decode_block(P, n)[0] == 'TEXT']
chg = [n for n in tx if core6.get(n) != core[n]]
rows = {n: {'changed_paths': [p for p, _ in dd(core[n], core6[n])], 'body_equal_v406_installed': P['body'][n] == Po['body'].get(n)} for n in chg}
out = {'text_blocks': len(tx), 'unchanged_source': len(tx) - len(chg), 'changed_source': rows, 'all_changed_only_runtime_s': all(r['changed_paths'] == ['/runtime_s'] for r in rows.values()), 'all_bodies_equal_v406_installed': all(r['body_equal_v406_installed'] for r in rows.values())}
json.dump(out, open(HERE / 'q_text_blocks_out.json', 'w', encoding='utf8'), ensure_ascii=False, indent=1)
print(json.dumps(out, ensure_ascii=False, indent=1))
