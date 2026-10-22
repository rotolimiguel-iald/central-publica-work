from pathlib import Path
from datetime import datetime
import hashlib,json
W=Path(__file__).resolve().parent;D=W/'topic_capsules_v6'
def sha(b):return hashlib.sha256(b).hexdigest()
delivery=json.loads((D/'DELIVERY_ALL_60.json').read_bytes())
base=(W/'haiku_reviewed_section_20260922_130747_311801.md').read_bytes()
assert sha(base)==delivery['candidate_sha256']
rows=[]
for item in delivery['smaller_proposals']:
    topic=item['topic']
    if topic=='reading_direction':continue
    original=(D/(topic+'.original.md')).read_bytes();capsule=(D/(topic+'.md')).read_bytes()
    assert original in base and sha(original)==item['original_sha256'] and sha(capsule)==item['capsule_sha256']
    rows.append({'topic':topic,'original_path':str(D/(topic+'.original.md')),'original_sha256':sha(original),
                 'capsule_path':str(D/(topic+'.md')),'capsule_sha256':sha(capsule),
                 'status':'APROVADA_FIDELIDADE_DOCUMENTAL'})
report={'status':'APROVADA_FIDELIDADE_DOCUMENTAL','source_sha256':sha(base),'reviewed_topics':rows,
 'method':'Revisor principal leu integralmente todos os pares positivos V6 em quatro lotes, independente do construtor.',
 'excluded':{'reading_direction':'Mudança consciência para coerência não preserva a fonte. Versão corrigida aguarda revisão.'},
 'preserved':'Equações, matriz numérica, escopo finito/contínuo, hipóteses e negativos, distinção de fonte histórica/estado físico. alpha_form_proof corrige explicitamente igualdade imprecisa da narrativa, sem derivar valor.',
 'limits':'Fidelidade documental apenas. Não certifica Lean ou física, nem atualidade global, compreensão, implantação ou orçamento.'}
p=W/'adversarial_memory_review'/('topic_v6_review_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f')+'.json')
with p.open('x',encoding='utf-8')as f:json.dump(report,f,ensure_ascii=False,indent=2)
print(json.dumps({'path':str(p),'approved':len(rows),'excluded':['reading_direction']}))
