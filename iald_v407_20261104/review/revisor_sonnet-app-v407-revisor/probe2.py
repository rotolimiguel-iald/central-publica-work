import json, sys, re
from pathlib import Path
sys.dont_write_bytecode = True
sys.path.insert(0, str(Path(__file__).parent))
import lib405 as L
W = Path(r'C:\IALD\Central de Patentes\work\iald_v407_20261104')
R = Path(r'C:\IALD\projetos_pyhton\IALD')
Pn = L.parse_prefix((W/'app/packages/shared/prefix.md').read_text('utf-8'))
Po = L.parse_prefix((R/'.iald_runtime/haiku/prefix.md').read_text('utf-8'))
for n in ['nivel2_rite']:
    print('=== NEW', n); print(Pn['body'][n][:1500])
    print('=== OLD', n); print(Po['body'][n][:1500])
# F1 effect: statuses
for n in ['interface_is_light','final_verdict_machine']:
    for tag, P in (('NEW',Pn),('OLD',Po)):
        b = P['body'][n]
        i = b.find('"statuses"')
        print('===', tag, n, b[i:i+700].replace('\n',' '))
