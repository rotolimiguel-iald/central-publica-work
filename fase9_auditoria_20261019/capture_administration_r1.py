"""Read-only dated view of the applicable board and operator pending list."""
from setup_audit import ROOT, pin, save
from pathlib import Path
import json, datetime

p=Path(r'C:\IALD\PROGRAMA_IALD\PENDENCIAS_DO_OPERADOR.md')
lines=p.read_text(encoding='utf-8').splitlines()
board=Path(r'C:\IALD\PROGRAMA_IALD\PROGRAMA.json')
j=json.loads(board.read_text(encoding='utf-8'))
units=j.get('unidades',{})
if isinstance(units,list):
    units={u['id']:u for u in units}
ids=['F3.1','F3.2','F3.3','F3.4','F3.5','F3.AUDITORIA_20261019']
save('ADMINISTRATIVE_SNAPSHOT_R1.json',{
 'created_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
 'pending_source':pin(p),'pending_excerpts':[{'line':i+1,'text':s} for i,s in enumerate(lines) if i<5 or any(x in s for x in ['**X13**','**X12**','**F3.5'])],
 'board_source':pin(board),'units':{k:units.get(k) for k in ids},
 'limit':'Read-only snapshot. A pending label in a draft is not proof that no later authorization exists. No consent inferred. D-H/D-J are also pinned in the audited draft; F3.4 is closed.'})
print(json.dumps({k:units.get(k,{}).get('status') for k in ids},ensure_ascii=False))
