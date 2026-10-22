"""Consolidate checked imaginary powers; all writes stay in this workbench."""
from pathlib import Path
from datetime import datetime
import hashlib, json, re

ROOT = Path(__file__).resolve().parent
assert ROOT.name == 'Chatgpt'
stamp = datetime.now().strftime('%Y%m%d_%H%M%S')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()

def create(path, data):
    assert not path.exists(), path
    temp = path.with_name(path.name+'.tmp')
    with temp.open('xb') as stream:
        stream.write(data)
    assert temp.stat().st_size == len(data) > 0
    temp.rename(path)

def append(name, text):
    path = ROOT/name
    old = path.read_bytes()
    backup = path.with_name(path.name+'.bak_'+stamp)
    create(backup,old)
    assert backup.read_bytes() == old
    new = old+text.encode('utf-8')
    temp = path.with_name(path.name+'.append_'+stamp)
    create(temp,new)
    assert temp.stat().st_size > len(old)
    temp.replace(path)
    assert path.read_bytes() == new
    return {'file':name,'backup':backup.name,'backup_sha256':sha(backup),'current_sha256':sha(path)}

proofs = []
modules = ['ModularFlowLevel','ModularFlowPre','ModularFlowHilbert',
           'ModularFlowAlgebra','ModularFlowSpectrum','ModularPower']
for name in modules:
    source = ROOT/(name+'.lean')
    metadata_path = sorted(ROOT.glob(name+'.*.json'))[-1]
    metadata = json.loads(metadata_path.read_text(encoding='utf-8-sig'))
    assert metadata['exit_code'] == 0 and metadata['source_stable'],metadata
    assert metadata['proof_sha256'] == sha(source),name
    log = (ROOT/metadata['log']).read_text(encoding='utf-8-sig')
    assert not any(x in log for x in ['sorryAx','error:','warning:']),log
    axiom_lists = re.findall(r'depends on axioms:\s*\[([^\]]*)\]',log,re.S)
    assert axiom_lists,name
    for text in axiom_lists:
        assert set(x.strip() for x in text.split(',')) <= {'propext','Classical.choice','Quot.sound'},text
    code = source.read_text(encoding='utf-8-sig')
    assert not re.search(r'\b(sorry|admit|axiom)\b',code),name
    proofs.append({'module':name,'source_sha256':sha(source),
        'olean_sha256':sha(ROOT/(name+'.olean')),'theorems':len(re.findall(r'^theorem ',code,re.M)),
        'verification':metadata_path.name,'log':metadata['log']})

manifest = json.loads((ROOT/'manifesto_fontes.json').read_text(encoding='utf-8-sig'))
rows = []
for item in manifest:
    try:
        current = sha(Path(item['source']))
        rows.append({'source':item['source'],'initial_sha256':item['sha256'],
                     'current_sha256':current,'unchanged':current == item['sha256'].upper()})
    except OSError as exc:
        rows.append({'source':item['source'],'unchanged':False,'error':str(exc)})
changed = sum(not row['unchanged'] for row in rows)
preservation = f'preservacao_fluxo_{stamp}.json'
create(ROOT/preservation,json.dumps({'timestamp':datetime.now().isoformat(),'files':len(rows),
       'changed_or_unreadable':changed,'rows':rows},ensure_ascii=False,indent=2).encode())
assert changed == 0,'Preservation check failed; inspect its recorded result'

note = '''

## ADENDO — 05/09/2026: potência imaginária, grupo e invariância modular verificados

[REAL — Lean] Foi construído `deltaImaginaryPower P t`, um grupo unitário fortemente contínuo no Hilbert da torre. A caracterização espectral foi verificada: os vetores locais E_ij pertencem ao domínio de Δ, têm autovalores λ=w_i/w_j>0, geram um span denso e recebem a fase exp(it log λ). O operador limitado com essa ação é único. A construção, portanto, liga a potência imaginária ao Δ existente.

[REAL — Lean] Também foram provadas a conjugação da representação local, a invariância do bicomutante `theFactorObject P`, Ω fixo e a invariância de `omegaState P` sob a conjugação. Não se presumiu o grupo nem a invariância como campos de um contrato. A invariância do estado usa Ω fixo e unitariedade, não apenas ω(I)=1.

Esses resultados superam a pendência de formalizar o grupo Δ^{it}, sua continuidade forte e a invariância de M para esta torre produto. [OPEN] Permanecem a biblioteca geral de cálculo funcional, a construção da esperança condicional para as subálgebras pretendidas e as pontes geométricas/físicas. O parâmetro modular não foi identificado automaticamente com tempo próprio ou geometria.

O registro atual é `FLUXO_MODULAR_FORMAL.md`. Os seis módulos finais, de `ModularFlowLevel` a `ModularPower`, compilaram com código 0, sem avisos, sorry ou novos axiomas. As listas impressas foram conferidas contra propext, Classical.choice e Quot.sound. Os hashes e a contagem de teoremas foram lidos dos artefatos. Os 290 originais do manifesto foram rehasheados; o resultado de preservação acompanha a verificação consolidada. Nenhuma memória canônica ou selo foi alterado.
'''
updates = [append(name,note) for name in ['RELATORIO.md','FECHO_FORMAL_JS.md',
    'JS_POSITIVO_AUTOADJUNTO.md','DELTA_FORMAL.md','RECONSTRUCAO_GRAVITACIONAL_GERAL.md']]
result = {'timestamp':datetime.now().isoformat(),'proofs':proofs,
    'new_theorems':sum(p['theorems'] for p in proofs),
    'imaginary_power_spectral_characterization':True,'unitary_group_strongly_continuous':True,
    'factor_invariance':True,'state_invariance':True,'generic_unbounded_functional_calculus':False,
    'conditional_expectation_constructed':False,'physical_gravity_reconstruction_complete':False,
    'originals_checked':len(rows),'originals_changed':changed,'preservation':preservation,
    'workbench_memory_updates':updates,'current_report':'FLUXO_MODULAR_FORMAL.md',
    'current_report_sha256':sha(ROOT/'FLUXO_MODULAR_FORMAL.md')}
create(ROOT/f'verificacao_fluxo_{stamp}.json',(json.dumps(result,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps(result,ensure_ascii=False,indent=2))
