"""Freeze the full scalar-weight GNS and star-graph identification before review."""
import datetime
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
DATE = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
NAMES = ['ScalarWeightDomain', 'ScalarWeightOrbit', 'ShiftCharacterAverage',
         'ScalarRightAverage', 'ScalarWeightCompletion', 'ScalarWeightAction',
         'ScalarWeightSandwich', 'ScalarWeightStarCore', 'ScalarWeightTomitaIdentification']

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def create(path, raw):
    assert raw and not path.exists() and path.resolve().is_relative_to(ROOT)
    temporary = path.with_suffix(path.suffix + '.tmp')
    with temporary.open('xb') as stream:
        stream.write(raw)
    assert temporary.read_bytes() == raw
    temporary.replace(path)
    assert path.read_bytes() == raw

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
    stdout = Path(row['stdout'])
    text = stdout.read_text(encoding='utf-8')
    names = re.findall(r'^#print axioms ([\w.]+)$', source.read_text(encoding='utf-8'), re.M)
    for short in names:
        full = 'TGLV350.Regular.' + short
        match = re.search(re.escape("'" + full + "' depends on axioms: [") + r'([^]]*)\]', text)
        assert match, full
        axioms = sorted(x.strip() for x in match.group(1).split(',') if x.strip())
        assert set(axioms) <= {'propext', 'Classical.choice', 'Quot.sound'}
        assert full not in targets
        targets[full] = axioms
    modules[name] = {'source_sha256': sha(source), 'binary_sha256': sha(binary),
        'targets': len(names), 'final_log': str(log), 'final_log_sha256': sha(log),
        'stdout_sha256': sha(stdout),
        'failed_attempts': [str(p) for p, v in history if v['returncode']]}
assert len(targets) == 60
parent_path = ROOT / 'tomita_involution_custody.json'
parent = json.loads(parent_path.read_bytes())
assert sha(ROOT / 'um.py') == parent['working_sha256']
report = ROOT / 'RELATORIO_GNS_PESO_COMPLETO_DEV.md'
create(report, f'''# GNS do peso escalar completo e identificação do gráfico de Tomita — DEV

{DATE}. [REAL — nove módulos/60 alvos compilados; revisão independente e integração pendentes]

O domínio n_ν é definido pela finitude de ν(A* A), no vetor regularVacuum P e
com o mesmo dualHaarFactor. O ideal anterior I exigia limite uniforme da forma
em todos os vetores. Provou-se I ⊆ n_ν, sem supor igualdade desses ideais.

1. Λ_ν(A) é a órbita s ↦ θ_s(A)Ω com a normalização já usada. Sua norma ao
quadrado é exatamente ν(A* A); a aplicação é linear e injetiva. Para A ∈ I,
ela coincide literalmente com a inscrição GNS anterior.
2. λ_t Ω = shift_t Ω. Como shift_t pertence ao comutante, a órbita de Aλ_t
é uma translação isométrica da órbita de A, multiplicada pela fase de caráter.
3. X_h = h⁻¹∫₀ʰλ_t dt dá A X_h ∈ I para h > 0. A média contrai a norma
pontual da órbita e tende à identidade. A diferença quadrática é dominada por
4‖θ_s(A)Ω‖², integrável quando A ∈ n_ν. Convergência dominada prova
Λ_ν(A X_h) → Λ_ν(A) em norma GNS.
4. Consequentemente, o completamento da imagem de n_ν é exatamente o H_I
anterior. A representação existente entrelaça Λ_ν(BA)=π(B)Λ_ν(A).
5. X_h* A X_h pertence ao núcleo involutivo anterior para h > 0 e converge
em norma GNS a A; a mesma construção vale para A*. A passagem ao adjunto usa
o lema já provado para contrações que tendem à identidade. Não se presume que
star seja contínuo na topologia forte geral.
6. As duas coordenadas do gráfico involutivo completo são aproximadas pelo
mesmo sandwich. Logo closure(graph de Λ_ν(A) ↦ Λ_ν(A*)) é exatamente o gráfico
do S fechado anterior. Este S estende a involução de todo n_ν ∩ n_ν*.

O resultado é igualdade dos completamentos e dos fechos de gráficos. Não afirma
I=n_ν nem que D(S) seja apenas a imagem algébrica Λ_ν(n_ν ∩ n_ν*). A construção
polar e U²=I anteriores permanecem no mesmo H_I; não é necessário trocar de
espaço ou postular uma equivalência entre GNS diferentes.

Os 60 alvos usam somente propext, Classical.choice e Quot.sound. Falhas rc1 de
elaboração/simplificação e qualquer tentativa substituída permanecem nos logs;
o manifesto aceita somente fontes e binários finais conferidos byte a byte.
Não houve acréscimo de hipótese KMS nem uso dela para a aproximação.

[OPEN] Ainda é preciso identificar o fluxo modular do peso com o fluxo candidato
e provar KMS; construir o traço canônico, sua escala dual e o canto Three Locks;
entregar H1/H2/H3 físicos compatíveis; completar o setor quântico interagente e
consumir tudo no certificado e runtime integrais. Identificar o gráfico não
identifica automaticamente a conjugação polar com outros candidatos chamados J.
As seis flags maiores continuam falsas e o gate legado permanece inalterado.

Este pacote ainda não integra o um.py. Mãe integrada `{sha(parent_path)}`;
cópia integrada `{sha(ROOT / 'um.py')}`. Original não executado, importado ou
modificado. O reexame de Chatgpt continua orientando o reaproveitamento das
pontes de Einstein, métrica de Fisher e gauge linearizado já existentes.
'''.encode('utf-8'))
record = {'timestamp': DATE, 'status': 'DEV_COMPILED__REVIEW_AND_INTEGRATION_PENDING',
    'modules': modules, 'targets': targets, 'report_sha256': sha(report),
    'parent_custody_path': str(parent_path), 'parent_custody_sha256': sha(parent_path),
    'integrated_working_sha256': sha(ROOT / 'um.py'),
    'full_scalar_weight_GNS_identified': True, 'full_scalar_weight_closed_graph_identified': True,
    'literal_ideal_equality_claimed': False, 'raw_graph_equals_closed_graph_claimed': False,
    'KMS_proved': False, 'canonical_trace_constructed': False, 'integrated': False,
    'gate_changed': False, 'full_goal_complete': False}
manifest = ROOT / 'scalar_weight_gns_draft_status.json'
create(manifest, json.dumps(record, ensure_ascii=False, indent=2).encode('utf-8'))
print(json.dumps({'modules': len(modules), 'targets': len(targets), 'manifest_sha256': sha(manifest)}))
