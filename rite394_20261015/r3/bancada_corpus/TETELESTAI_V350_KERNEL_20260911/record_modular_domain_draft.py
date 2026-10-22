"""Pin compiled development proofs without promoting them to reviewed integration."""
from pathlib import Path
import datetime
import hashlib
import json
import re

ROOT = Path(__file__).resolve().parent
MODULES = ['ScalarModularInvariance', 'RegularScalarWeightCertificate',
           'ContractionAdjointLimit', 'StrongBoundedApplication', 'FiniteDualStarCore']
STAMP = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def save(p, raw):
    assert p.resolve().is_relative_to(ROOT)
    if p.exists():
        before = p.read_bytes()
        b = p.with_name(p.name + '.bak_' + STAMP)
        with b.open('xb') as f:
            f.write(before)
        assert b.read_bytes() == before
    t = p.with_name(p.name + '.tmp_' + STAMP)
    with t.open('xb') as f:
        f.write(raw)
    assert t.read_bytes() == raw and len(raw) > 0
    t.replace(p)
    assert p.read_bytes() == raw


records = {}
targets = {}
for name in MODULES:
    source = ROOT / 'kernel/TGLV350' / (name + '.lean')
    matches = []
    for log in (ROOT / 'logs').glob(name + '_*.json'):
        row = json.loads(log.read_bytes())
        if row['sha256'] == sha(source) and row['returncode'] == 0:
            matches.append((log, row))
    assert matches, name
    log, row = sorted(matches, key=lambda pair: pair[1]['timestamp'])[-1]
    assert row['source_unchanged_during_compile']
    assert row['output_sha256'] == sha(ROOT / 'build/TGLV350' / (name + '.olean'))
    output = Path(row['stdout']).read_text(encoding='utf-8')
    names = re.findall(r'^#print axioms ([\w.]+)$', source.read_text(encoding='utf-8'), re.M)
    for target in names:
        full = 'TGLV350.Regular.' + target
        m = re.search(re.escape("'" + full + "' depends on axioms:") + r'\s*\[([^\]]*)\]', output)
        assert m, full
        axioms = {s.strip() for s in m.group(1).split(',')}
        assert axioms <= {'propext', 'Classical.choice', 'Quot.sound'}, (full, axioms)
        targets[full] = sorted(axioms)
    records[name] = {'log': str(log), **row}
assert len(targets) == 17
base = json.loads((ROOT / 'scalar_weight_custody.json').read_bytes())
assert sha(ROOT / 'um.py') == base['working_sha256']
note = """# Domínio do peso e certificado da mesma representação — desenvolvimento

[REAL — Lean local, ainda sem integração ou revisão independente]
Cinco módulos, 17 alvos. Os hashes de fontes e binários e os logs aceitos
estão em modular_domain_draft_status.json. As tentativas anteriores falhas
continuam nos logs; nenhuma delas é tratada como prova.

ScalarModularInvariance prova invariância de ν por A↦Λ_t* A Λ_t. O argumento
usa as translações ordinárias no comutante de N, a bimodularidade da forma
dual e Δ^(it)Ω=Ω. Este resultado NÃO identifica o grupo modular: KMS falta.

RegularScalarWeightCertificate reúne 13 campos em Prop, parametrizados
pelo mesmo SiteProfile e referidos às definições efetivas de N, F, M, q e ν.
O construtor descarrega os campos, inclusive normalidade para redes de
universo arbitrário, densidade do ideal esquerdo e invariância. Não recebe
as propriedades como hipóteses residuais. O certificado ainda não é
consumido pelo gate Python e não contém traço ou dados físicos.

ContractionAdjointLimit prova: contrações que tendem fortemente à identidade
têm adjuntos que também tendem fortemente à identidade. O controle de norma
é essencial; não se usa continuidade geral da adjunção na topologia forte.
StrongBoundedApplication permite mover o vetor numa família de operadores
uniformemente limitada, com uma estimativa de norma explícita.

FiniteDualStarCore constrói a subálgebra complexa sem unidade I∩I*, onde I
é o ideal esquerdo de quadrados limitados da forma dual. Para todo A∈N,
A_h=X_h* A X_h pertence a essa subálgebra quando h>0, ||A_h||≤||A||, A_h→A
e A_h*→A* fortemente. Tanto ν(A_h* A_h) quanto ν(A_h A_h*) são finitos.
Não se afirma que A_h seja positivo para A arbitrário, que esteja abaixo de
A, ou que a aproximação seja em norma. Tampouco se identifica o domínio
algébrico com um espaço GNS completo antes de construí-lo.

[OPEN] Próximo passo matemático: inscrição GNS da forma ν e condição KMS,
seguida do gerador afiliado, perturbação e traço canônico com escala dual.
Three Locks/H1, H2/H3 físicos, estado quântico interagente, BRST/QME/anomalias,
UV, contrato ampliado consumido e runtime integral isolado permanecem no
objetivo. As seis flags maiores seguem false na integração custodiada.
Original preservado; este rascunho não amplia o escopo da custódia integrada.
"""
save(ROOT / 'ROTA_DOMINIO_MODULAR_RASCUNHO.md', note.encode('utf-8'))
result = {
    'timestamp': datetime.datetime.now().astimezone().isoformat(),
    'status': 'DEVELOPMENT_COMPILED__NOT_INTEGRATED__NOT_INDEPENDENTLY_REVIEWED',
    'records': records, 'targets': targets,
    'integrated_custody': 'scalar_weight_custody.json',
    'integrated_custody_sha256': sha(ROOT / 'scalar_weight_custody.json'),
    'working_sha256': base['working_sha256'],
    'draft_note_sha256': sha(ROOT / 'ROTA_DOMINIO_MODULAR_RASCUNHO.md'),
    'full_runtime': False, 'canonical_trace_constructed': False,
    'KMS_proved': False, 'full_goal_complete': False,
}
save(ROOT / 'modular_domain_draft_status.json', json.dumps(result, ensure_ascii=False, indent=2).encode())
print(json.dumps({'development_modules': len(records), 'development_targets': len(targets),
                  'integrated': False, 'independently_reviewed': False}))
