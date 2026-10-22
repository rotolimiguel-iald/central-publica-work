"""Freeze the same-GNS homogeneous right adjoint bridge before review."""
import datetime
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
DATE = datetime.datetime.now().astimezone().isoformat(timespec='seconds')
NAMES = ['LocalRightModularTransport', 'HomogeneousCommutantTransport',
         'ScalarHomogeneousRightOrbit', 'HomogeneousRightData', 'ScalarHomogeneousRightGNS']

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
    output = stdout.read_text(encoding='utf-8')
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
        'stdout_sha256': sha(stdout),
        'failed_attempts': [str(p) for p, v in history if v['returncode']]}
assert len(targets) == 28
parent_path = ROOT / 'scalar_weight_gns_custody.json'
parent = json.loads(parent_path.read_bytes())
assert sha(ROOT / 'um.py') == parent['working_sha256']
report = ROOT / 'RELATORIO_DIREITA_MODULAR_GNS_DEV.md'
create(report, f'''# Direita modular no GNS completo do mesmo peso — DEV

{DATE}. [REAL — cinco módulos/28 alvos compilados; revisão independente e integração pendentes]

Para a unidade matricial local y=e_ij, escreva D=rTowerPi(y) e
c=log(w_i/w_j). A conjugação modular da torre satisfaz Ad Δ₀^it(D)=exp(itc)D.
O levantamento ao comutante do core é characterMultiplier(-c)·fibre(D).
Portanto, para todo A do core e todo s real:

    θ_s(A·fibre(y))Ω = fibre(D) θ_(s-c)(A)Ω.

O sinal s-c é consequência da ação de caracteres efetivamente definida.
Provou-se também ν(A* A)<∞ se e somente se s↦θ_s(A)Ω pertence a L².
Translação de Lebesgue e aplicação linear contínua preservam L²; assim
a multiplicação à direita por y preserva o domínio escalar completo n_ν.
Não se restringe o enunciado ao ideal uniforme inicial I.

No ambiente L² externo o operador direito é

    R_y = fibre(fibre(D))·shift(c).

Ele preserva o mesmo H_I já identificado com o completamento de Λ_ν(n_ν),
e sua restrição satisfaz R_y Λ_ν(A)=Λ_ν(Ay). Não foi postulado outro GNS.
O adjunto local anterior D*=rTowerPi(modTwist(y)) fornece agora, no mesmo H_I:

    R_y* = R_(modTwist(y)),     modTwist(y)=ρ y* ρ⁻¹,
    ⟨Λ_ν(Ay),Λ_ν(B)⟩ = ⟨Λ_ν(A),Λ_ν(B modTwist(y))⟩.

O pareamento vale para quaisquer A,B∈n_ν e cada unidade matricial local y.
Os dados genéricos HomogeneousRightData são explicitamente instanciados por
matrixUnitRightData e matrixUnitTwistedRightData; nenhuma hipótese KMS é
campo desse contrato. A extensão por somas a todo y local não foi acrescentada
nesta rodada, embora a identidade já esteja provada para cada gerador matricial.

[OPEN] Esta é uma identidade de adjunto, não a condição KMS global de faixa
complexa nem a identificação do fluxo com (S†S)^it. Ainda faltam domínio/núcleo
apropriado e identificação espectral no H_I, o traço canônico e escala dual,
o canto Three Locks, H1/H2/H3 físicos compatíveis, setor quântico interagente
e consumo pelo certificado e runtime integrais. Nenhuma dessas obrigações
foi inserida como axioma nos 28 alvos.

Convenção de sinal: σ_t(A)=λ_t A λ_t*; a função regularConjugate do estágio
anterior usa λ_t* A λ_t e representa σ_-t. Invariância vale nas duas orientações
e não basta para escolher a orientação KMS. O implementador candidato no GNS
também não deve ser confundido com π(λ_t), que age por multiplicação à esquerda.

Consulta independente de Pasteur (somente leitura, sem compilação) indicou
a rota adicional de convoluções locais, Plancherel e núcleo de gráfico para
identificar S†S por autovalores w_i/w_j. Essa rota é proposta, não prova pronta.
A prova desta rodada usa diretamente a órbita dual para o pareamento.

Falhas de elaboração permanecem nos logs; somente rc0 com fontes/binários
atuais e axiomas propext, Classical.choice, Quot.sound entram no manifesto.
Cópia integrada ainda `{sha(ROOT / 'um.py')}`; mãe `{sha(parent_path)}`.
Original não executado/importado/modificado; gate inalterado e objetivo ativo.
'''.encode('utf-8'))
record = {'timestamp': DATE, 'status': 'DEV_COMPILED__REVIEW_AND_INTEGRATION_PENDING',
    'modules': modules, 'targets': targets, 'report_sha256': sha(report),
    'parent_custody_path': str(parent_path), 'parent_custody_sha256': sha(parent_path),
    'integrated_working_sha256': sha(ROOT / 'um.py'),
    'right_matrix_unit_preserves_full_scalar_weight_domain': True,
    'right_adjoint_pairing_on_same_full_GNS': True,
    'global_KMS_proved': False, 'modular_square_flow_identified': False,
    'canonical_trace_constructed': False, 'integrated': False,
    'gate_changed': False, 'full_goal_complete': False}
manifest = ROOT / 'homogeneous_right_draft_status.json'
create(manifest, json.dumps(record, ensure_ascii=False, indent=2).encode('utf-8'))
print(json.dumps({'modules': len(modules), 'targets': len(targets), 'manifest_sha256': sha(manifest)}))
