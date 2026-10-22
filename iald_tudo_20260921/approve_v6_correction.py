from pathlib import Path
from datetime import datetime
import json,hashlib
W=Path(__file__).resolve().parent;D=W/'topic_capsules_v6'
def sha(b):return hashlib.sha256(b).hexdigest()
report=json.loads((W/'adversarial_memory_review/topic_v6_review_20260922_141358_247824.json').read_bytes())
delta=json.loads((D/'reading_direction_v2.provenance.json').read_bytes())
old=(D/'reading_direction.md').read_bytes();new=(D/'reading_direction_v2.md').read_bytes();original=(D/'reading_direction.original.md').read_bytes()
assert sha(old)==delta['parent_capsule_sha256'] and sha(new)==delta['capsule_v2_sha256'] and sha(original)==delta['original_sha256']
assert old.decode().replace(delta['delta']['before'],delta['delta']['after'],1)==new.decode()
report['reviewed_topics'].append({'topic':'reading_direction','original_path':str(D/'reading_direction.original.md'),
 'original_sha256':sha(original),'capsule_path':str(D/'reading_direction_v2.md'),'capsule_sha256':sha(new),'status':'APROVADA_FIDELIDADE_DOCUMENTAL'})
report['excluded']={}
report['correction_review']='Leitura integral V2 pelo pai confirmou restauração razão/consciência [ONTO]; somente delta declarado, fórmulas/remissões preservadas.'
p=W/'adversarial_memory_review'/('topic_v6_all38_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f')+'.json')
with p.open('x',encoding='utf-8')as f:json.dump(report,f,ensure_ascii=False,indent=2)
print(p)
