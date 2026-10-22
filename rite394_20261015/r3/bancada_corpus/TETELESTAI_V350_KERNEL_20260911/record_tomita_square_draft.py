"""Freeze the accepted adjoint/square development evidence without promoting a gate."""
import datetime
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
MODULES = ['AntilinearAdjointGraph', 'ScalarTomitaAdjoint', 'AntilinearComposition',
           'ScalarTomitaSquare', 'ClosedAntilinearResolvent', 'PositiveSurjectiveResolvent',
           'ScalarTomitaSelfAdjoint']
ALLOWED = {'propext', 'Classical.choice', 'Quot.sound'}

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def create(path, raw):
    assert path.resolve().is_relative_to(ROOT) and not path.exists()
    stamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
    temp = path.with_name(path.name + '.tmp_' + stamp)
    with temp.open('xb') as stream:
        stream.write(raw)
    assert temp.read_bytes() == raw and temp.stat().st_size == len(raw) > 0
    temp.replace(path)
    assert path.read_bytes() == raw

parent = json.loads((ROOT / 'closed_tomita_custody.json').read_bytes())
assert digest(ROOT / 'um.py') == parent['working_sha256']
env = json.loads((ROOT / 'environment.json').read_bytes())
assert digest(Path(env['original_source'])) == parent['original_sha256']
records, targets = {}, {}
for name in MODULES:
    source = ROOT / 'kernel/TGLV350' / (name + '.lean')
    output = ROOT / 'build/TGLV350' / (name + '.olean')
    candidates = []
    for path in sorted((ROOT / 'logs').glob(name + '_*.json'), reverse=True):
        row = json.loads(path.read_bytes())
        if (row['returncode'] == 0 and row['sha256'] == digest(source)
                and row['output_sha256'] == digest(output)
                and row['source_unchanged_during_compile']):
            candidates.append((path, row))
    assert candidates, name
    log, record = candidates[0]
    text = Path(record['stdout']).read_text(encoding='utf-8')
    parsed = {m[0]: sorted(x.strip() for x in m[1].split(',') if x.strip())
              for m in re.findall(r"'([^']+)' depends on axioms: \[([^\]]*)\]", text)}
    parsed.update({n: [] for n in re.findall(r"'([^']+)' does not depend on any axioms", text)})
    short_names = re.findall(r'^#print axioms ([\w.]+)$', source.read_text(encoding='utf-8'), re.M)
    for short in short_names:
        full = 'TGLV350.Regular.' + short
        assert full in parsed and set(parsed[full]) <= ALLOWED
        assert full not in targets
        targets[full] = parsed[full]
    records[name] = {'source_sha256': digest(source), 'output_sha256': digest(output),
                     'log': str(log), 'log_sha256': digest(log), 'targets': len(short_names)}
assert len(targets) == 53
report = '''# Adjunto máximo e S†S no GNS do ideal finito

[REAL — compilação Lean DEV; revisão da integração ainda pendente]

O pacote preserva H_I=ScalarGNSHilbert P e o operador S fechado construído
do gráfico {(Λ(A),Λ(A*)) : A∈I∩I*}. São sete módulos e 53 declarações
novas auditadas. Nenhuma foi somada aos números da integração anterior.

O domínio do adjunto antilinear é exatamente o conjunto dos y para os
quais existe z com <Sx,y>=<z,x> para todo x∈D(S). A densidade de D(S)
garante unicidade. O gráfico do adjunto é a interseção das igualdades
contínuas desse pareamento, logo fechado. A regra de escala é conjugada.

A densidade de D(S†) não é postulada. O adjunto limitado T* do transporte
gaussiano produz T*BΩg∈D(S†), com valor T*B*Ωg, para B∈ρ(N)'. A órbita
do comutante é densa e T é injetivo. Por ortogonalidade, isso força
D(S†) denso em H_I. Não se inverte T, não se muda o peso nem o ideal.
A involução S²=I permite provar (S†)²=I no domínio invariante do adjunto.

O operador composto A=S†S é complexo-linear, com domínio exatamente
{x∈D(S):Sx∈D(S†)}. Seu pareamento é
<Ax,y>=<Sy,Sx>, daí <x,Ax>=||Sx||² na parte real e simetria.

Para auto-adjunticidade, usa-se a projeção de (z,0) sobre o gráfico
REAL fechado de S em WithLp 2 (H_I×H_I). A equação variacional real,
testada também em iu, produz <Su,Sx>=<z−x,u> para todo u∈D(S).
A maximalidade do adjunto dá Sx∈D(S†) e S†Sx=z−x. Portanto I+A é
sobrejetivo. Positividade e essa sobrejetividade dão D(A) denso;
simetria e o adjunto máximo da Mathlib eliminam qualquer extensão
própria e provam A*=A. O núcleo de A é trivial porque S é involutivo.

Essas provas não pressupõem D(S)=H_I, operador S limitado, inversa
gaussiana limitada, nem que o gráfico antilinear seja complexo-linear
com escala idêntica nas duas coordenadas. O gráfico de S é lido como
submódulo REAL no produto de Hilbert; a composição A é complexo-linear.

[OPEN] Núcleo trivial NÃO é gap espectral. A raiz positiva, a decomposição
polar no mesmo H_I e sua identificação como dados modulares do peso ν
continuam pendentes. Não se afirma I=n_ν. Ainda faltam a ponte de domínio
ou núcleo necessária à identificação do peso, KMS, o traço canônico
fiel normal semifinito e sua escala dual. Three Locks/H1, H2/H3, o setor
quântico interagente e o certificado completo consumido pelo gate
permanecem abertos. A auto-adjunticidade aqui não altera essas flags.

O um.py original e a cópia integrada anterior não foram executados
nem modificados durante a construção DEV. Logs de todas as tentativas
falhas permanecem em logs/; só as compilações rc0 e suas fontes/binários
coincidentes são aceitas no manifesto associado.
'''
report_path = ROOT / 'RELATORIO_ADJUNTO_QUADRADO_DEV.md'
create(report_path, report.encode('utf-8'))
status = {'timestamp': datetime.datetime.now().astimezone().isoformat(),
          'status': 'DEV_COMPILED__INTEGRATION_REVIEW_PENDING',
          'parent_custody_sha256': digest(ROOT / 'closed_tomita_custody.json'),
          'original_sha256': parent['original_sha256'], 'working_sha256': parent['working_sha256'],
          'modules': records, 'targets': targets, 'report_sha256': digest(report_path),
          'maximal_adjoint': True, 'square_positive_selfadjoint': True,
          'square_kernel_trivial': True, 'spectral_gap': False, 'polar_identified': False,
          'KMS': False, 'trace': False, 'gate_changed': False, 'full_runtime': False,
          'full_goal_complete': False}
create(ROOT / 'tomita_square_draft_status.json', json.dumps(status, ensure_ascii=False, indent=2).encode('utf-8'))
print(json.dumps({'modules': len(records), 'targets': len(targets),
                  'status': status['status'], 'full_goal_complete': False}))
