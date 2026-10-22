"""Preserve the unreviewed graph-core advance without promoting integrated evidence."""
import datetime
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
DATE = datetime.datetime.now().astimezone().isoformat(timespec='seconds')

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def create(path, raw):
    assert not path.exists() and raw
    temp = path.with_suffix(path.suffix + '.tmp')
    with temp.open('xb') as stream:
        stream.write(raw)
    assert temp.read_bytes() == raw
    temp.replace(path)
    assert path.read_bytes() == raw

modules, targets = {}, {}
for name in ['RealGraphCore', 'ScalarTomitaGraphCore']:
    source = ROOT / 'kernel/TGLV350' / (name + '.lean')
    binary = ROOT / 'build/TGLV350' / (name + '.olean')
    history = [(p, json.loads(p.read_bytes())) for p in sorted((ROOT / 'logs').glob(name + '_*.json'))]
    accepted = [(p, v) for p, v in history if v['returncode'] == 0 and
                v['sha256'] == sha(source) and v['output_sha256'] == sha(binary)]
    assert accepted
    log, row = accepted[-1]
    stdout = Path(row['stdout'])
    text = stdout.read_text(encoding='utf-8')
    module_targets = re.findall(r'^#print axioms ([\w.]+)$', source.read_text(encoding='utf-8'), re.M)
    for short in module_targets:
        full = 'TGLV350.Regular.' + short
        match = re.search(re.escape("'" + full + "' depends on axioms: [") + r'([^]]*)\]', text)
        assert match, full
        axioms = sorted(v.strip() for v in match.group(1).split(','))
        assert set(axioms) <= {'propext', 'Classical.choice', 'Quot.sound'}
        targets[full] = axioms
    modules[name] = {'source_sha256': sha(source), 'binary_sha256': sha(binary),
        'final_log': str(log), 'final_log_sha256': sha(log), 'stdout_sha256': sha(stdout),
        'targets': len(module_targets), 'failed_attempts': [str(p) for p, v in history if v['returncode']]}
assert len(targets) == 10
report_path = ROOT / 'RELATORIO_DOMINIO_GRAFICO_DEV.md'
text = f'''# D(S†S) como núcleo do gráfico de S — DEV

{DATE}. [REAL — compilação DEV; revisão independente e integração pendentes]

O lema genérico usa um gráfico REAL fechado de um mapa real-linear sobre
submódulo complexo. Uma família resolvente fraca completa com valores em C
faz o gráfico restrito a C denso no gráfico inteiro. O complemento ortogonal
é zero: testa-se a identidade com o próprio primeiro componente do vetor.
A densidade fornece sequências que convergem nas duas coordenadas do gráfico.
Não basta supor C denso somente na norma de H.

Aplicação ao S atual no mesmo H_I: C=D(A), A=S†S; C⊆D(S). A família
x+Ax=z já construída e o pareamento de S† fornecem a identidade fraca.
Logo, para todo x∈D(S), existem x_n∈D(A) com x_n→x e Sx_n→Sx.
Dois módulos/10 alvos, todos no trio propext/Classical.choice/Quot.sound.

[OPEN] Não foi ainda construído o núcleo de gráfico análogo de B nem provada
D(B)=D(S). Igualdade de energia no domínio inteiro, J/polar, KMS e traço
continuam abertos. Os dez alvos não entram na integração da raiz (cinco/30)
ou nas contagens integradas. Nenhuma flag ou gate é promovido.

Tentativas anteriores rc1 preservadas: colisão de nome de instância real,
orientação do produto interno/nome de lema, e timeout de reescrita sobre o
tipo concreto. As fontes finais corrigem esses pontos; só seus rc0 e pins
compõem a evidência. Um stdout com sorryAx após erro nunca foi aceito.

Próxima etapa: obter D(A) como núcleo do gráfico da raiz positiva B;
usar igualdade de normas em D(A), convergência de Cauchy e fechamento para
transportar ambos os domínios. Só então construir o fator antiunitário.
Esse parágrafo é roteiro, não prova nova.
'''
create(report_path, text.encode('utf-8'))
record = {'timestamp': DATE, 'status': 'DEV_COMPILED__REVIEW_AND_INTEGRATION_PENDING',
    'modules': modules, 'targets': targets, 'report_sha256': sha(report_path),
    'integrated_working_sha256': sha(ROOT / 'um.py'), 'integrated': False,
    'square_domain_graph_core_for_Tomita': True, 'root_domain_equals_tomita_domain': False,
    'KMS_proved': False, 'gate_changed': False, 'full_goal_complete': False}
create(ROOT / 'graph_core_draft_status.json', json.dumps(record, ensure_ascii=False, indent=2).encode())
print(json.dumps({'modules': 2, 'targets': len(targets), 'status': record['status'],
    'manifest_sha256': sha(ROOT / 'graph_core_draft_status.json')}))
