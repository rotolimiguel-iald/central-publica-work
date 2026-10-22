"""Read a bounded delivery batch; printing is not a claim of review."""
import json
from pathlib import Path
import sys
sys.stdout.reconfigure(encoding='utf-8')

root=Path(__file__).resolve().parent
inventory=json.loads((root/'JOINT_DEFINITION_INVENTORY.json').read_text(encoding='utf-8'))
rows=[r for r in inventory['sources'] if r['review_group']=='PHYSICAL_QUANTUM_AND_RECENT']
start,end=map(int,sys.argv[1:3])
for index,row in enumerate(rows[start:end],start):
    print(json.dumps({'index':index,'path':row['path'],'content':Path(row['path']).read_text(encoding='utf-8')},ensure_ascii=False))
