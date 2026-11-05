import json, sys
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).parent))
import lib405 as L
W = Path(r'C:\IALD\Central de Patentes\work\iald_v407_20261104'); R = Path(r'C:\IALD\projetos_pyhton\IALD'); V = Path(r'C:\IALD\Central de Patentes\vault\originals_copy\um_unificado_v407')
core = json.loads((V/'um_absoluto.json').read_bytes())['core']
m = json.loads((R/'iald_nucleo_fixo.json').read_bytes()); core6 = json.loads(Path(m['published_evidence']['result']['path']).read_bytes())['core']
P = L.parse_prefix((W/'app/packages/shared/prefix.md').read_text('utf-8'))
Po = L.parse_prefix((R/'.iald_runtime/haiku/prefix.md').read_text('utf-8'))
tx = [n for n in core if n in P['body'] and L.decode_block(P, n)[0] == 'TEXT']
chg = [n for n in tx if core6.get(n) != core[n]]
print(len(tx), 'TEXT blocks;', len(chg), 'with changed source:', chg)
for n in chg:
    b = P['body'][n]; bo = Po['body'].get(n)
    print('--', n, '| bytes new/old:', len(b.encode()), len(bo.encode()) if bo else None, '| same body as v406 installed:', b == bo)
    print('   new head:', ' '.join(b.split())[:260])
