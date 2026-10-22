"""Freeze the original full-domain F=BJ=JSJ and transported graph core."""
import datetime
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
NAMES = ['ScalarTomitaAdjointPolar', 'ScalarRightConjugateGraph']
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

parent_path = ROOT / 'right_graph_core_custody.json'
parent = json.loads(parent_path.read_bytes())
assert sha(ROOT / 'um.py') == parent['working_sha256']
assert parent['right_pair_graph_core_equals_original_F'] and not parent['KMS_proved']
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
assert len(targets) == 17
report = ROOT / 'RELATORIO_ADJUNTO_POLAR_GRAFOS_ORIGINAIS_DEV.md'
create(report, f'''# Adjunto polar e grafos originais — DEV

{DATE}. [REAL — dois módulos/17 alvos compilados; revisão e integração pendentes]

[REAL] O adjunto maximal F original satisfaz F=BJ=JSJ, onde B é
a raiz positiva já construída de S†S e J é seu fator polar original.
A igualdade inclui TODO o domínio: D(F)=J^-1D(B)=J^-1D(S).
O lema generic_adjoint_maximal da bancada Chatgpt (Continuous050) foi
reaproveitado: a auto-adjunção de B elimina qualquer extensão maior.
O pareamento original S/F identifica o valor, sem redefinir F ou J.

[REAL] A conjugação simultânea J×J transporta o grafo fechado original de S
no grafo original de F e vice-versa. O fecho do grafo da inscrição direita
j(a),j(a*) já era F. Como J×J é homeomorfismo, o fecho dos pares
(Jj(a),Jj(a*)) é agora o grafo original de S. A inscrição a↦Jj(a) é
conjugado-linear; não foi confundida com uma identificação de álgebras.
Isso prova densidade no grafo inteiro, não apenas densidade dos vetores.

[OPEN] Ainda falta provar JRJ pertence a π(N) para todo R em π(N)', ou
uma geração efetiva do comutante que forneça essa inclusão inversa.
F=JSJ e os grafos densos não são apresentados como prova automática
de π(N)'=Jπ(N)J. Δ^it/KMS, traço/escala/canto Three Locks, H1/H2/H3
físicos, setor interagente e consumo por certificados tipados/runtime
continuam abertos. Seis flags maiores falsas; o gate permanece igual.

[REAL — fiação preservada] As seis flags maiores qgf/gpf não entram diretamente
em evaluate_quantum_gravity_closure: o selo legado lê qgc_, qgp_ e o feed
experimental; kernel_frontier é anexado depois. O consumo por certificado
tipado continua necessário para que novas provas movam esse selo.

Integração anterior: {parent['integrated_records']} registros,
{parent['controls']} controles, {parent['audit_declarations']} declarações Audit.
Este DEV não altera um.py nem as 34 memórias; atualização pendente de revisão
nesta sessão. Cópia `{sha(ROOT / 'um.py')}`, mãe `{sha(parent_path)}`.
Tentativas Lean recusadas e fontes anteriores foram preservadas; somente
logs rc0 dos bytes atuais são aceitos. Nenhum monólito executado/importado.
'''.encode('utf-8'))
manifest = {'timestamp': DATE, 'status': 'DEV_COMPILED__REVIEW_AND_INTEGRATION_PENDING',
    'modules': modules, 'targets': targets, 'report_path': str(report), 'report_sha256': sha(report),
    'parent_custody_path': str(parent_path), 'parent_custody_sha256': sha(parent_path),
    'integrated_working_sha256': sha(ROOT / 'um.py'),
    'original_adjoint_equals_BJ_full_domain': True,
    'original_adjoint_equals_JSJ_full_domain': True,
    'right_conjugate_graph_core_equals_original_S': True,
    'original_weight_J_not_replaced': True,
    'KMS_proved': False, 'modular_square_flow_identified': False,
    'independent_review_complete': False, 'integrated': False,
    'memory_update_pending_review_in_this_turn': True,
    'gate_changed': False, 'full_goal_complete': False}
create(ROOT / 'adjoint_polar_graph_draft_status.json', json.dumps(manifest, ensure_ascii=False, indent=2).encode('utf-8'))
print(json.dumps({'modules': len(modules), 'targets': len(targets), 'integrated': False}))
