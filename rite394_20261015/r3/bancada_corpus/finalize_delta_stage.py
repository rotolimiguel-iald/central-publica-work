"""Record exact verification metadata and preserve the original archive read-only."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent
assert ROOT.name == 'Chatgpt'
stamp = datetime.now().strftime('%Y%m%d_%H%M%S')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()

def create(path, data):
    assert not path.exists(), path
    temp = path.with_name(path.name + '.tmp')
    with temp.open('xb') as stream:
        stream.write(data)
    assert temp.stat().st_size == len(data) > 0
    temp.rename(path)

def append(name, text):
    path = ROOT/name
    old = path.read_bytes()
    backup = path.with_name(path.name+'.bak_'+stamp)
    create(backup, old)
    assert backup.read_bytes() == old
    new = old + text.encode('utf-8')
    temp = path.with_name(path.name+'.append_'+stamp)
    create(temp,new)
    assert temp.stat().st_size > len(old)
    temp.replace(path)
    assert path.read_bytes() == new
    return {'file':name,'backup':backup.name,'backup_sha256':sha(backup),'current_sha256':sha(path)}

proofs = []
for name in ['ModularSquare','ModularSquareAdjoint','TomitaAdjoint','ModularInverse']:
    source = ROOT/(name+'.lean')
    meta_path = sorted(ROOT.glob(name+'.*.json'))[-1]
    meta = json.loads(meta_path.read_text(encoding='utf-8-sig'))
    assert meta['exit_code'] == 0 and meta['source_stable'],meta
    assert meta['proof_sha256'] == sha(source),name
    log = (ROOT/meta['log']).read_text(encoding='utf-8-sig')
    assert not any(x in log for x in ['sorryAx','error:','warning:']),log
    lists = re.findall(r'depends on axioms:\s*\[([^\]]*)\]',log,re.S)
    assert lists,name
    for axiom_list in lists:
        assert set(x.strip() for x in axiom_list.split(',')) <= {'propext','Classical.choice','Quot.sound'},axiom_list
    code = source.read_text(encoding='utf-8-sig')
    assert not re.search(r'\b(sorry|admit|axiom)\b',code),name
    proofs.append({'module':name,'source_sha256':sha(source),'olean_sha256':sha(ROOT/(name+'.olean')),
                   'theorems':len(re.findall(r'^theorem ',code,re.M)),
                   'verification':meta_path.name,'log':meta['log']})

manifest = json.loads((ROOT/'manifesto_fontes.json').read_text(encoding='utf-8-sig'))
rows = []
for item in manifest:
    try:
        current = sha(Path(item['source']))
        rows.append({'source':item['source'],'initial_sha256':item['sha256'],'current_sha256':current,
                     'unchanged':current == item['sha256'].upper()})
    except OSError as exc:
        rows.append({'source':item['source'],'unchanged':False,'read_error':str(exc)})
changed = sum(not row['unchanged'] for row in rows)
preservation_name = f'preservacao_delta_{stamp}.json'
create(ROOT/preservation_name,json.dumps({'timestamp':datetime.now().isoformat(),'files':len(rows),
       'changed_or_unreadable':changed,'rows':rows},ensure_ascii=False,indent=2).encode())
assert changed == 0,'Source preservation mismatch; inspect the recorded result'

note = '''

## ADENDO — 05/09/2026: Δ e S†S agora construídos e verificados

[REAL — Lean] `ModularSquare.lean` constrói `towerDeltaClosed P` no domínio x∈Dom(JS) e JSx∈Dom(JS), prova densidade, positividade e coincidência com `towerDeltaLevel` nos andares. `ModularSquareAdjoint.lean` prova auto-adjunticidade e fechamento por uma estimativa de energia que controla as duas condições de domínio. `TomitaAdjoint.lean` constrói o adjunto antilinear S†=(JS)J, prova sua identidade e maximalidade, e verifica S†S=Δ com o domínio de composição. `ModularInverse.lean` prova injetividade de Δ e JΔJ=Δ⁻¹ como equivalência de gráficos.

Estas construções superam as pendências formais de quadrado e adjunto descritas anteriormente. JS é uma raiz quadrada positiva auto-adjunta explicitamente construída de Δ. [OPEN — Lean] Permanecem o cálculo funcional espectral, sua operação de raiz e unicidade geral, o grupo Δ^{it} e a invariância modular tipados. As pontes geométricas e físicas permanecem abertas.

O registro atual é `DELTA_FORMAL.md`. Os quatro arquivos finais compilaram com código 0 e sem avisos; as listas de axiomas impressas foram conferidas e contêm somente propext, Classical.choice e Quot.sound. Os hashes foram lidos dos fontes e objetos compilados. As tentativas recusadas, incluindo um excesso de inferência e uma detecção de mudança do fonte durante verificação, permanecem preservadas; não são o resultado final validado. Nenhum original, memória canônica ou selo foi alterado.
'''
updates = [append(name,note) for name in ['RELATORIO.md','FECHO_FORMAL_JS.md','JS_POSITIVO_AUTOADJUNTO.md']]
updates.append(append('RECONSTRUCAO_GRAVITACIONAL_GERAL.md','''

## ADENDO — 05/09/2026: Δ positivo auto-adjunto e a identidade modular

[REAL — Lean] A análise da torre agora inclui Δ=(JS)² com domínio correto, positividade, auto-adjunticidade, fechamento, construção maximal do adjunto antilinear S† e identidade S†S=Δ. Também foi verificada a reciprocidade JΔJ=Δ⁻¹ em gráficos. Consulte `DELTA_FORMAL.md`. Estes resultados atualizam o bloco de análise modular; localização, dimensão, assinatura, escala e realização termodinâmica continuam [OPEN].
'''))
updates.append(append('DELTA_FORMAL.md','''

## ADENDO: reciprocidade modular no domínio correto

[REAL — Lean] `ModularInverse.lean` verifica `delta_graph_J_swap`: (x,y)∈Graph(Δ) se e somente se (Jy,Jx)∈Graph(Δ). Essa é a forma de JΔJ=Δ⁻¹ que explicita o domínio, sem declarar que Δ⁻¹ exista como operador limitado em todo H. O argumento aplica duas vezes a relação recíproca de A=JS, derivada da involução de S. Também foi verificada a injetividade de Δ. Os teoremas finais imprimiram somente os três axiomas usuais.
'''))
result = {'timestamp':datetime.now().isoformat(),'proofs':proofs,
          'new_theorems':sum(p['theorems'] for p in proofs),
          'Delta_positive_selfadjoint_closed':True,'Tomita_adjoint_maximal':True,
          'Delta_equals_SdaggerS_with_domains':True,'JDeltaJ_inverse_graph':True,
          'spectral_functional_calculus_formalized':False,'physical_gravity_reconstruction_complete':False,
          'originals_checked':len(rows),'originals_changed':changed,'preservation':preservation_name,
          'workbench_memory_updates':updates,'current_report':'DELTA_FORMAL.md',
          'current_report_sha256':sha(ROOT/'DELTA_FORMAL.md')}
create(ROOT/f'verificacao_delta_{stamp}.json',(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps(result,ensure_ascii=False,indent=2))
