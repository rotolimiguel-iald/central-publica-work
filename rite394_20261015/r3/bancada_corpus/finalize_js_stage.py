"""Preserve the audit trail, verify current proofs, and rehash original sources read-only."""
from pathlib import Path
from datetime import datetime
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent
assert ROOT.name == 'Chatgpt'
stamp = datetime.now().strftime('%Y%m%d_%H%M%S')

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()

def save_new(path, data):
    assert not path.exists(), path
    temp = path.with_name(path.name + '.tmp')
    with temp.open('xb') as f:
        f.write(data)
    assert temp.stat().st_size == len(data) > 0
    temp.rename(path)

proofs = []
for module in ['DiagonalOperator', 'ModularProbe', 'GeneralNullCone']:
    source = ROOT / (module + '.lean')
    metadata_path = sorted(ROOT.glob(module + '.*.json'))[-1]
    metadata = json.loads(metadata_path.read_text(encoding='utf-8-sig'))
    assert metadata['exit_code'] == 0, metadata
    assert metadata['proof_sha256'] == digest(source), source
    log = (ROOT / metadata['log']).read_text(encoding='utf-8-sig')
    assert 'sorryAx' not in log and 'error:' not in log and 'warning:' not in log, log
    contents = source.read_text(encoding='utf-8-sig')
    assert not re.search(r'\b(sorry|admit|axiom)\b', contents), source
    proofs.append({'module': module, 'sha256': digest(source),
                   'theorem_count': len(re.findall(r'^theorem ', contents, re.M)),
                   'verification': metadata_path.name, 'log': metadata['log']})

manifest = json.loads((ROOT/'manifesto_fontes.json').read_text(encoding='utf-8-sig'))
rows = []
for entry in manifest:
    source = Path(entry['source'])
    try:
        current = digest(source)
        rows.append({'source':str(source), 'unchanged':current == entry['sha256'].upper(),
                     'current_sha256':current, 'initial_sha256':entry['sha256']})
    except OSError as error:
        rows.append({'source':str(source), 'unchanged':False, 'read_error':str(error)})
changed = sum(not row['unchanged'] for row in rows)
preservation = {'timestamp':datetime.now().isoformat(), 'files':len(rows),
                'changed_or_unreadable':changed,'rows':rows}
preservation_name = f'preservacao_JS_{stamp}.json'
save_new(ROOT/preservation_name, (json.dumps(preservation,ensure_ascii=False,indent=2)+'\n').encode())
assert changed == 0, 'Source preservation check failed visibly; inspect the saved result'

report = ROOT/'RELATORIO.md'
old = report.read_bytes()
backup = report.with_name(report.name+'.bak_'+stamp)
save_new(backup, old)
assert digest(backup) == digest(report)
addition = '''

## ADENDO — 05/09/2026: positividade, auto-adjunticidade e gravitação geral

[DERIVED] A demonstração escrita `JS_POSITIVO_AUTOADJUNTO.md` identifica o JS da torre produto com o operador diagonal máximo em uma base ortonormal de excitações finitas. A identidade de teste no domínio inteiro fornece JS⊆D; truncamentos em norma de gráfico e o fechamento de JS fornecem D⊆JS. Assim JS é positivo e auto-adjunto, Δ=D², JS=Δ¹ᐟ² e S=JΔ¹ᐟ², com os domínios explícitos. O texto também deriva o grupo modular e a invariância da álgebra nesta realização produto.

[REAL — Lean] Foram compilados três novos arquivos: `DiagonalOperator.lean` (11 teoremas), `ModularProbe.lean` (4 teoremas) e `GeneralNullCone.lean` (1 teorema). Eles verificam o operador diagonal e seu adjunto, a identidade de teste de JS no domínio completo e a rigidez do cone nulo para um tensor simétrico arbitrário em quatro dimensões. As verificações finais têm código 0, sem avisos ou sorryAx; os axiomas impressos são apenas os três usuais registrados nos logs. A contagem foi lida dos fontes, totalizando 16 novos teoremas.

[OPEN — Lean] A base infinita, a transformação unitária U e o transporte que conclui IsSelfAdjoint para `closedModulatorCandidate P` ainda não estão codificados. O argumento escrito não deve ser confundido com uma certificação integral pelo kernel. A denominação Candidate do arquivo anterior permanece coerente com essa fronteira formal.

[DERIVED] `RECONSTRUCAO_GRAVITACIONAL_GERAL.md` desenvolve a passagem geral de Clausius local, Raychaudhuri e rigidez tensorial à equação de Einstein por Bianchi, sob hipóteses geométricas e termodinâmicas explícitas. Não depende do ansatz q(t) anterior. [OPEN] A torre ainda precisa construir localização, dimensão, assinatura, escala, energia-momento e correspondência entropia-área. O teorema condicional não prova a realização dessas hipóteses na natureza.

[REAL] Os seis controles exatos de `controles_modular_geometria.json` passaram. Incluem a base modular de um e dois sítios e o par g₀=diag(1,−1,−1,−1), g₁=e^(2t)g₀: mesmos cones nulos, mas escalar de g₁ igual a −6e^(−2t) na convenção registrada. Portanto cones sem escala adicional não determinam curvatura.

Este adendo supera a pendência da DEMONSTRAÇÃO ESCRITA de positividade do adendo anterior; não apaga a pendência de sua formalização integral. Não houve selo novo, execução do rito integral, reconstrução completa das dependências ou aprovação independente. Os originais e as memórias canônicas não foram editados.
'''
new = old + addition.encode('utf-8')
temp = report.with_name(report.name+'.tmp_'+stamp)
save_new(temp,new)
assert temp.stat().st_size > len(old)
temp.replace(report)
assert report.read_bytes() == new
summary = {'timestamp':datetime.now().isoformat(),'proofs':proofs,
           'new_theorems':sum(p['theorem_count'] for p in proofs),
           'originals_checked':len(rows),'originals_changed':changed,
           'preservation':preservation_name,'report_backup':backup.name,
           'full_JS_transport_formalized':False,'physical_gravity_reconstruction_complete':False,
           'artifacts':{name:digest(ROOT/name) for name in ['JS_POSITIVO_AUTOADJUNTO.md',
                       'RECONSTRUCAO_GRAVITACIONAL_GERAL.md','controles_modular_geometria.json']}}
save_new(ROOT/f'verificacao_etapa_JS_{stamp}.json',(json.dumps(summary,ensure_ascii=False,indent=2)+'\n').encode())
print(json.dumps(summary,ensure_ascii=False,indent=2))
