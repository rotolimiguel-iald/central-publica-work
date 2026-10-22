"""Inventory every current tunnel delivery for a disjoint documentary review."""
import hashlib
import json
from pathlib import Path
import re
import finalize_weyl_bridge as c

folder=c.WORK/'TUNEL/DO_CHATGPT'
rows=[]
for path in sorted(folder.glob('*.md')):
    name=path.name
    number=re.match(r'ENTREGA_(\d{3})_',name)
    if name.startswith('ENTREGA_011_A') or (name.startswith('ENTREGA_012_') and 'ESPONTANEA' not in name):
        group='CORE_AND_FRIEDMANN'
    elif number and int(number.group(1))<=59:
        group='GEOMETRY_AND_MODULAR_EARLY'
    else:
        group='PHYSICAL_QUANTUM_AND_RECENT'
    raw=path.read_bytes()
    rows.append(dict(path=str(path),name=name,bytes=len(raw),lines=len(raw.splitlines()),
                     sha256=hashlib.sha256(raw).hexdigest(),review_group=group))
receipt=c.WORK/'TUNEL/PARA_CHATGPT/RESPOSTA_OPERADOR_16SET_DEFINICAO_CONJUNTA_NO_ESTUDO_INTEIRO.md'
report=dict(timestamp=c.NOW,operator_receipt=c.pin(receipt),scope='ALL_MD_IN_DO_CHATGPT_AT_SNAPSHOT',
            sources=rows,total_bytes=sum(r['bytes'] for r in rows),count=len(rows),
            read_status='INVENTORIED_NOT_YET_ALL_READ')
c.atomic(c.ROOT/'JOINT_DEFINITION_INVENTORY.json',json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({g:{'files':sum(r['review_group']==g for r in rows),'bytes':sum(r['bytes'] for r in rows if r['review_group']==g)} for g in sorted({r['review_group'] for r in rows})}))
