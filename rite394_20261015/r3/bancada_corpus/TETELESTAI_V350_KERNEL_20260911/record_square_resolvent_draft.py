"""Freeze rational resolvents, square approximations and the original-S test."""
import datetime
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
NAMES = ['SquareResolventSupport', 'ScalarRightSquareApproximation', 'ScalarSquareAdjointTest']
DATE = datetime.datetime.now().astimezone().isoformat(timespec='seconds')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def create(path, raw):
    assert raw and not path.exists() and path.resolve().is_relative_to(ROOT)
    temp = path.with_suffix(path.suffix + '.tmp')
    with temp.open('xb') as stream:
        stream.write(raw)
    assert temp.read_bytes() == raw
    temp.replace(path)
    assert path.read_bytes() == raw

parent_path = ROOT / 'bidual_right_support_custody.json'
parent = json.loads(parent_path.read_bytes())
assert sha(ROOT / 'um.py') == parent['working_sha256']
assert parent['original_S_is_maximal_adjoint_of_F'] and not parent['KMS_proved']
for name, pin in parent['artifacts'].items():
    assert sha(ROOT / name) == pin, name
for name, pin in parent['surface_sha256'].items():
    assert sha(Path(name)) == pin, name
modules, targets = {}, {}
for name in NAMES:
    source = ROOT / 'kernel/TGLV350' / (name + '.lean')
    binary = ROOT / 'build/TGLV350' / (name + '.olean')
    history = [(p, json.loads(p.read_bytes())) for p in sorted((ROOT / 'logs').glob(name + '_*.json'))]
    accepted = [(p, v) for p, v in history if v['returncode'] == 0 and
        v['sha256'] == sha(source) and v['output_sha256'] == sha(binary)]
    assert accepted, name
    log, row = accepted[-1]
    assert row['source_unchanged_during_compile']
    stdout, stderr = Path(row['stdout']), Path(row['stderr'])
    output = stdout.read_text(encoding='utf-8')
    assert stderr.read_bytes() == b''
    names = re.findall(r'^#print axioms ([\w.]+)$', source.read_text(encoding='utf-8'), re.M)
    for short in names:
        full = 'TGLV350.Regular.' + short
        match = re.search(re.escape("'" + full + "' depends on axioms: [") + r'([^]]*)\]', output)
        assert match, full
        axioms = sorted(x.strip() for x in match.group(1).split(',') if x.strip())
        assert set(axioms) <= {'propext', 'Classical.choice', 'Quot.sound'}
        assert full not in targets
        targets[full] = axioms
    modules[name] = {'source_sha256': sha(source), 'binary_sha256': sha(binary),
        'targets': len(names), 'final_log': str(log), 'final_log_sha256': sha(log),
        'stdout_sha256': sha(stdout), 'stderr_sha256': sha(stderr),
        'failed_attempts': [str(p) for p, v in history if v['returncode']]}
assert len(targets) == 20
report = ROOT / 'RELATORIO_RESOLVENTES_QUADRADOS_TESTE_ORIGINAL_DEV.md'
create(report, f'''# Resolventes, quadrados e teste do S original — DEV

{DATE}. [REAL — três módulos/20 alvos compilados; revisão e integração pendentes]

[REAL] Para A limitado auto-adjunto, R_n=(I+(n+1)A²)^−1 é uma
sequência antítona de contrações positivas. A estimativa
(n+1)||R_n A v||² ≤ ||v||²/4 e o limite forte existente provam R_n x→0
para x no fecho normado de Ran A. Não se supõe injetividade ou gap, nem
se afirma convergência em norma de operador ou em todo H.

[REAL] Para a=a* na álgebra não unital dos pares direitos, constroem-se
b_n=R_n a, d_n=(n+1)a b_n e c_n=a d_n dentro da MESMA álgebra.
Como operadores, d_n=I−R_n. Os c_n são auto-adjuntos, diferenças de
quadrados auto-adjuntos com coeficiente 1/4, e j(c_n)→j(a).
Não se presumiu I ou R_n pertencente à álgebra não unital.

[REAL] Testes de pareamento nos j(b²), b=b*, caracterizam exatamente o
grafo do S original. A prova estende o pareamento por aproximação,
fecho de Fix F e decomposição h+ik/h−ik, e usa a bidualidade anterior.
Se K e K* limitados realizam as duas ações sobre todos os vetores j(a),
o par de vetores pertence ao grafo desse S. Não se redefine S/F/J.

[OPEN] Ainda é preciso verificar essas duas ações para o candidato
ponderado dos blocos de projeção, provar a cota inferior uniforme do
bloco A e construir o multiplicador limitado. A inclusão inversa pelo
J original, Delta^it/KMS, traço/escala/canto Three Locks, H1/H2/H3 físicos,
setor interagente e consumo por certificados/runtime continuam abertos.
O critério de teste é provado; a aplicação ao candidato não é automática.

[REAL — leitura dos tipos; OPEN — nova construção] O gráfico já existente
scalarRightMultiplicationGraph usa o ideal esquerdo do peso, Λ e η fixo por F.
A próxima etapa requer G_η=fecho{{(j(a),aη):a∈E}}, com E a álgebra dos pares
direitos e η fixo por S. Reaproveitar a infraestrutura de projeções não
identifica esses gráficos: a simetria e as ações devem ser provadas nesse E.
Os blocos novos deverão comutar com E; não se supõe comutação entre A e B.
Seis flags maiores falsas; objetivo integral ativo.

[REAL — fiação preservada] As seis flags maiores qgf/gpf não entram diretamente
em evaluate_quantum_gravity_closure: o selo legado lê qgc_, qgp_ e o feed
experimental; kernel_frontier é anexado depois. O consumo por certificado
tipado continua necessário para que novas provas movam esse selo.

Integração anterior: {parent['integrated_records']} registros,
{parent['controls']} controles, {parent['audit_declarations']} declarações Audit.
Este DEV não altera um.py nem as 34 memórias; atualização pendente de revisão
nesta sessão. Cópia `{sha(ROOT / 'um.py')}`, mãe `{sha(parent_path)}`.
Tentativas Lean recusadas e seus logs foram preservados; somente
logs rc0 dos bytes atuais são aceitos. Nenhum monólito executado/importado.
'''.encode('utf-8'))
manifest = {'timestamp': DATE, 'status': 'DEV_COMPILED__REVIEW_AND_INTEGRATION_PENDING',
    'modules': modules, 'targets': targets, 'report_path': str(report), 'report_sha256': sha(report),
    'parent_custody_path': str(parent_path), 'parent_custody_sha256': sha(parent_path),
    'integrated_working_sha256': sha(ROOT / 'um.py'),
    'square_resolvents_vanish_on_range_closure': True,
    'selfadjoint_right_vectors_approximated_by_square_differences': True,
    'original_S_characterized_by_selfadjoint_square_tests': True,
    'original_weight_J_not_replaced': True,
    'KMS_proved': False, 'modular_square_flow_identified': False,
    'independent_review_complete': False, 'integrated': False,
    'memory_update_pending_review_in_this_turn': True,
    'gate_changed': False, 'full_goal_complete': False}
create(ROOT / 'square_resolvent_draft_status.json', json.dumps(manifest, ensure_ascii=False, indent=2).encode('utf-8'))
print(json.dumps({'modules': len(modules), 'targets': len(targets), 'integrated': False}))
