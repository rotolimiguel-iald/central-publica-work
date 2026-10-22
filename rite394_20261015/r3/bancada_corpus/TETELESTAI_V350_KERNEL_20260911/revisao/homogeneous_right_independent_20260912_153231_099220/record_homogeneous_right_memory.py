"""Record the reviewed right-adjoint DEV stage, with exact-byte lineage backups."""
import datetime
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parent
CENTRAL = ROOT.parent.parent
STAMP = datetime.datetime.now().strftime('%Y%m%d_%H%M%S_%f')
DATE = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
MARKER = 'TETELESTAI_V350_HOMOGENEOUS_RIGHT_GNS_DEV_REVIEWED_20260912'

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def create(path, raw):
    assert not path.exists() and raw and path.resolve().is_relative_to(ROOT)
    temp = path.with_name(path.name + '.tmp_' + STAMP)
    with temp.open('xb') as stream:
        stream.write(raw)
    assert temp.read_bytes() == raw
    temp.replace(path)
    assert path.read_bytes() == raw

assert '--review-read' in sys.argv
parent_path = ROOT / 'scalar_weight_gns_custody.json'
parent = json.loads(parent_path.read_bytes())
draft_path = ROOT / 'homogeneous_right_draft_status.json'
draft = json.loads(draft_path.read_bytes())
review = ROOT / 'revisao/REVIEW_HOMOGENEOUS_RIGHT_GNS.md'
assert 'HOMOGENEOUS_RIGHT_GNS_DEV_REVIEW' in review.read_text(encoding='utf-8')
assert draft['parent_custody_sha256'] == sha(parent_path)
assert sha(ROOT / 'um.py') == parent['working_sha256'] == draft['integrated_working_sha256']
original = Path(json.loads((ROOT / 'environment.json').read_bytes())['original_source'])
assert sha(original) == sha(ROOT / 'fontes/um_v350_original.py') == parent['original_sha256']
for name, pin in parent['artifacts'].items():
    assert sha(ROOT / name) == pin, name
for name, row in draft['modules'].items():
    assert sha(ROOT / 'kernel/TGLV350' / (name + '.lean')) == row['source_sha256']
    assert sha(ROOT / 'build/TGLV350' / (name + '.olean')) == row['binary_sha256']
    log_path = Path(row['final_log'])
    assert sha(log_path) == row['final_log_sha256']
    log = json.loads(log_path.read_bytes())
    assert log['returncode'] == 0 and log['source_unchanged_during_compile']
    assert sha(Path(log['stdout'])) == row['stdout_sha256']
assert len(draft['modules']) == 5 and len(draft['targets']) == 28
assert not draft['integrated'] and not draft['global_KMS_proved']
evidence = json.loads((ROOT / 'kernel_incremental_evidence.json').read_bytes())
assert all(evidence[k] is False for k in parent['remaining_flags'])
surfaces = [Path(p) for p in parent['surface_sha256']]
assert len(surfaces) == 34
before = {str(p): p.read_bytes() for p in surfaces}
for path in surfaces:
    assert path.resolve().is_relative_to(ROOT) or path.resolve() in (
        CENTRAL / 'memory/TGL_ATLAS.md', CENTRAL / 'memory/TGL_INDICE_VIVO.md')
    assert sha(path) == parent['surface_sha256'][str(path)]
    assert MARKER.encode() not in before[str(path)]

report_path = ROOT / 'RELATORIO_DIREITA_MODULAR_GNS_REVISADO.md'
report = f'''# Multiplicação à direita e adjunto no mesmo GNS — etapa revisada

{DATE}. [REAL — DEV compilado e revisado; integração pendente]

Cinco módulos/28 alvos transportam a multiplicação à direita por cada unidade
matricial local y ao GNS completo do peso escalar ν. O operador direito preserva
n_ν e o mesmo H_I anterior, e seu adjunto é a direita de ρy*ρ⁻¹. O pareamento
⟨Λ_ν(Ay),Λ_ν(B)⟩=⟨Λ_ν(A),Λ_ν(Bρy*ρ⁻¹)⟩ vale para quaisquer A,B∈n_ν.
A frequência c=log(w_i/w_j) entra como shift(c) na órbita dual; o sinal foi
verificado a partir do caráter exp(-isx). As instâncias matriciais fornecem
todas as hipóteses do contrato genérico; KMS não é hipótese inserida.

[Provas, hipóteses e limites](<{(ROOT / 'RELATORIO_DIREITA_MODULAR_GNS_DEV.md').as_posix()}>).
[Manifesto](<{draft_path.as_posix()}>).
[Revisão independente](<{review.as_posix()}>).

A integração anterior continua com {parent['integrated_records']} registros,
{parent['controls']} controles e {parent['audit_declarations']} declarações Audit.
Esses números são evidência herdada, não uma execução nova do monólito nem
integração dos 28 alvos. A cópia um.py permanece `{sha(ROOT / 'um.py')}`.

O que ainda pode mover o gate, quando provado e consumido com tipos completos:

| Obrigação | Resultado já disponível | Lacuna atual |
|---|---|---|
| Realização modular contínua | Mesmo GNS completo, S fechado, S=UB, U²=I; agora direita e adjunto locais | Identificar o fluxo com (S†S)^it no domínio correto e provar KMS global |
| Canto contínuo | Álgebra regular, ação dual e peso construídos | Traço canônico, escala dual e canto finito Three Locks no mesmo modelo |
| H1 | Resultados do setor finito | Lacuna relativa SUSY fora da face finita, com as hipóteses exigidas |
| H2 | Métrica refletida de Fisher e implicações geométricas existentes | Dados suaves de posto quatro e identificação geométrica oriundos do mesmo estado/peso |
| H3 | Ponte condicional de Einstein e primeira lei/custos internos | Equilíbrio área-calor no mesmo horizonte físico, com as condições de fonte e limite |
| Testemunha completa | Contratos e provas parciais | Setor quântico interagente, BRST/QME, anomalias/escopo UV, composição e consumo efetivo pelo certificado/runtime |

As seis flags maiores permanecem falsas. O gate legado não foi alterado.
A identidade de adjunto acima não equivale à condição KMS analítica global;
falta a identificação espectral/núcleo de gráfico de S†S no H_I. A extensão
por somas a qualquer matriz local também não foi acrescentada nesta etapa.

O reexame de Chatgpt já identificou as pontes de Einstein, Fisher e gauge geral
linearizado; não tratá-las como ausentes nem como testemunhas físicas sem suas
hipóteses. [Reaproveitamento](<{(ROOT / 'REEXAME_CHATGPT_20260912/RELATORIO_REAPROVEITAMENTO.md').as_posix()}>).
As indicações antigas sobre polar/GNS abertos foram superadas pelas etapas
datadas posteriores, preservadas ao lado na memória.

Original relido `{sha(original)}`, preservado; não executado ou importado.
Mãe integrada e de memória `{sha(parent_path)}`. Objetivo integral ativo.
'''
create(report_path, report.encode('utf-8'))
note = f'''

## {MARKER} — {DATE}

[INPUT — direção preservada] Examinar o trabalho já existente em Chatgpt,
identificar pendências de kernel que podem mover o gate e atualizar a memória.

[REAL — DEV compilado e revisado; integração pendente] Cinco módulos/28 alvos
constroem a direita de cada unidade matricial local no mesmo GNS completo n_ν,
com adjunto ρy*ρ⁻¹ e pareamento para quaisquer A,B∈n_ν. O transporte conserva
o deslocamento s-c da órbita dual. Não houve hipótese KMS inserida nem troca
de GNS. O compilador aceitou apenas o trio propext/Classical.choice/Quot.sound.

Integração anterior permanece: {parent['integrated_records']} registros,
{parent['controls']} controles, {parent['audit_declarations']} declarações Audit;
nenhum runtime integral novo. Cópia {sha(ROOT / 'um.py')}; original preservado.
Esta etapa ainda não está embutida no um.py. Seis flags maiores falsas.

[OPEN] Identificação espectral do S†S e KMS global, traço/escala/canto Three
Locks, H1/H2/H3 físicos compatíveis, interação quântica e consumo pelo gate.
Pareamento direito local não é KMS global. Reutilizar Einstein/Fisher/gauge
já encontrados com suas hipóteses; o objetivo integral permanece ativo.

[Relatório e tabela de pendências](<{report_path.as_posix()}>).
[Revisão independente](<{review.as_posix()}>).
'''
backups = {}
for path in surfaces:
    raw = before[str(path)]
    assert path.read_bytes() == raw
    backup = path.with_name(path.name + '.bak_' + STAMP)
    with backup.open('xb') as stream:
        stream.write(raw)
    assert backup.read_bytes() == raw
    backups[str(path)] = str(backup)
    newline = '\r\n' if b'\r\n' in raw else '\n'
    after = raw + note.replace('\n', newline).encode('utf-8')
    temp = path.with_name(path.name + '.tmp_' + STAMP)
    with temp.open('xb') as stream:
        stream.write(after)
    assert temp.read_bytes() == after and after.startswith(raw) and len(after) > len(raw)
    assert path.read_bytes() == raw
    temp.replace(path)
    assert path.read_bytes() == after

custody = {'timestamp': DATE, 'status': 'DEV_REVIEWED__INTEGRATION_PENDING',
    'previous_custody_path': str(parent_path), 'previous_custody_sha256': sha(parent_path),
    'original_sha256': sha(original), 'working_sha256': sha(ROOT / 'um.py'),
    'draft_sha256': sha(draft_path), 'report_sha256': sha(report_path),
    'review_sha256': sha(review), 'modules': draft['modules'], 'targets': draft['targets'],
    'surface_sha256': {str(p): sha(p) for p in surfaces}, 'backups': backups,
    'surface_before_sha256': {str(p): sha(Path(backups[str(p)])) for p in surfaces},
    'remaining_flags': parent['remaining_flags'],
    'right_adjoint_pairing_on_same_full_GNS': True,
    'KMS_proved': False, 'integrated': False, 'gate_changed': False, 'full_goal_complete': False}
create(ROOT / 'homogeneous_right_dev_custody.json',
       json.dumps(custody, ensure_ascii=False, indent=2).encode('utf-8'))
assert custody['surface_before_sha256'] == parent['surface_sha256']
for path in surfaces:
    assert path.read_bytes().startswith(Path(backups[str(path)]).read_bytes())
    assert sha(path) == custody['surface_sha256'][str(path)]
create(ROOT / 'homogeneous_right_dev_verification.json', json.dumps({
    'timestamp': DATE, 'custody_sha256': sha(ROOT / 'homogeneous_right_dev_custody.json'),
    'custody_ok': True, 'source_binary_pairs_reread': len(draft['modules']),
    'byte_backups_and_prefixes': len(surfaces), 'original_unchanged': True,
    'gate_changed': False, 'integrated': False}, indent=2).encode('utf-8'))
print(json.dumps({'surfaces': len(surfaces), 'modules': len(draft['modules']),
    'targets': len(draft['targets']), 'custody_ok': True, 'integrated': False}))
