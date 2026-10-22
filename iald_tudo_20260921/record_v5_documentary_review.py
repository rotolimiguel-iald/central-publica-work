"""Pin the 23 pairs fully read by the primary reviewer; not a proof audit."""
from pathlib import Path
from datetime import datetime
import hashlib,json
W=Path(__file__).resolve().parent
D=W/'topic_capsules_v5'
def sha(b):return hashlib.sha256(b).hexdigest()
delivery=json.loads((D/'DELIVERY_ALL_30.json').read_bytes())
base=(W/'haiku_reviewed_section_20260922_130747_311801.md').read_bytes()
assert sha(base)==delivery['source_sha256']
rows=[]
for topic in delivery['positive_only_topics']:
    original=(D/(topic+'.original.md')).read_bytes()
    assert original.strip() in base
    filename=topic+'_v2.md' if topic=='alpha_inversion' else topic+'.md'
    capsule=(D/filename).read_bytes()
    if topic=='alpha_inversion':
        delta=json.loads((D/'alpha_inversion_v2.provenance.json').read_bytes())
        previous=(D/'alpha_inversion.md').read_bytes()
        assert sha(previous)==delta['parent_capsule']['sha256']
        assert sha(capsule)==delta['capsule_v2_sha256']
        assert previous.decode().replace(delta['change']['before'],delta['change']['after'],1)==capsule.decode()
    rows.append({'topic':topic,'original_path':str(D/(topic+'.original.md')),
                 'original_sha256':sha(original),'capsule_path':str(D/filename),
                 'capsule_sha256':sha(capsule),'status':'APROVADA_FIDELIDADE_DOCUMENTAL'})
report={'status':'APROVADA_FIDELIDADE_DOCUMENTAL','source_sha256':sha(base),'reviewed_topics':rows,
 'method':'Leitura integral dos 23 pares pelo revisor principal, independente do construtor Cicero; correção alpha_inversion_v2 conferida integralmente.',
 'correction':'Zb/Zl determina q=(Zb-Zl)/(Zb+Zl); não é igual a q. Corrigida apenas cápsula derivada, preservada fonte.',
 'preserved':'Fórmulas, hipóteses, negativos, distinção finito/contínuo, estatutos KERNEL/KNOWN/ONTO/OPEN e escopo histórico.',
 'limits':'Não certifica Lean, prova física, atualidade global, implantação, compreensão pelo modelo ou orçamento. Sete propostas sem economia ficam fora; originais preservados.'}
p=W/'adversarial_memory_review'/('topic_v5_positive23_'+datetime.now().strftime('%Y%m%d_%H%M%S_%f')+'.json')
with p.open('x',encoding='utf-8')as f:json.dump(report,f,ensure_ascii=False,indent=2)
print(p)
