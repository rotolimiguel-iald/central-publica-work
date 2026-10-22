"""Derive Gaussian polar stage helpers without modifying their sealed parents."""
import ast
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
OLD_NAMES = ['FiniteSetFibreRead', 'FibreSlices', 'ReducingCommutantTransport', 'ScalarGNSGeneratorTransport', 'CorePolarInclusion']
NAMES = ['DenseLinearPolarExtension', 'BoundedInjectivePolar', 'ScalarGaussianImage', 'ScalarGaussianUnitary']
OLD_FLAGS = ['finite_set_reads_total', 'actual_polar_conjugates_core_into_commutant', 'scalar_GNS_generator_transport_proved', 'core_polar_commutes_with_every_core_left_element']
FLAGS = ['gaussian_polar_unitary_constructed', 'gaussian_closed_image_identified', 'same_scalar_GNS_cyclic_separating_vector_constructed', 'original_weight_J_not_replaced']
BODY = '''No mesmo H_I=ScalarGNSHilbert P, com a mesma representação π do core N,
C=scalarGaussianGNSMap P é o mapa injetivo já construído. Seu contradomínio
correto para a parte polar é K=closure(Ran C), não o ambiente L² inteiro.

[REAL] Provados K redutor e Ωg∈K por médias regulares de quadrado finito,
limitadas por 1, com h↓0. A densidade das inscrições e a invariância dão
K=closure(dualOrbit(N) Ωg). Não se usa C^{-1} limitado nem C(H_I)⊆H_I.

Para C_K:H_I→K, D=(C_K†C_K)^(1/2) tem imagem densa e
||Dx||=||C_Kx||. A regra V(Dx)=C_Kx estende uma UNITÁRIA LINEAR V.
O entrelaçamento para a e a* prova Vπ(a)=ρ_K(a)V. Logo
ξ=V^{-1}Ωg pertence ao H_I ORIGINAL e é cíclico separante para a MESMA π.
Não se afirma norma 1; ξ representa o funcional gaussiano, não o peso
semifinito original. Todas as densidades são demonstradas na aplicação.

[OPEN] V não é J. O Tomita/conjugação do novo vetor ξ não foi identificado
com S/J do peso. A inclusão de gráficos por C não autoriza cancelar D:
sua inversa pode ser não limitada e os domínios precisam ser controlados.
A inclusão direta Jπ(N)J⊆π(N)' da etapa anterior permanece provada.
Esta preparação cíclica NÃO prova a inclusão inversa com o J original.

Continuam abertos Δ^it/KMS do mesmo peso, traço/escala/canto Three Locks,
H1/H2/H3 físicos compatíveis, setor interagente e consumo por certificados
tipados/runtime. Reutilizar as provas anteriores de Chatgpt com suas hipóteses.
Seis flags maiores falsas; o gate não muda por esta preparação.

'''

def create(name, text):
    ast.parse(text)
    p = ROOT / name
    assert not p.exists(), p
    raw = text.encode('utf-8')
    tmp = p.with_suffix('.py.tmp')
    with tmp.open('xb') as stream:
        stream.write(raw)
    assert tmp.read_bytes() == raw
    tmp.replace(p)
    assert p.read_bytes() == raw

def common(text):
    text = text.replace('core_polar', 'gaussian_polar').replace('CORE_POLAR', 'GAUSSIAN_POLAR')
    text = text.replace('base_polar_custody.json', 'core_polar_custody.json')
    text = text.replace('INCLUSAO_POLAR_CORE', 'POLAR_GAUSSIANO_CICLICO')
    text = text.replace('cinco módulos/28 alvos', 'quatro módulos/34 alvos')
    text = text.replace('Cinco módulos/28 alvos', 'Quatro módulos/34 alvos')
    text = text.replace('Inclusão polar do core inteiro', 'Polar gaussiano e vetor cíclico separante')
    for old, new in zip(OLD_FLAGS, FLAGS):
        text = text.replace(old.replace('core_polar', 'gaussian_polar'), new)
    text = text.replace('len(targets) == 28', 'len(targets) == 34')
    text = text.replace('len(modules) == 5', 'len(modules) == 4')
    return text

def replace_body(text):
    text, count = re.subn(r'No mesmo espaço H_I=ScalarGNSHilbert P.*?(?=\[REAL — fiação preservada\])',
        lambda _: BODY, text, flags=re.S)
    assert count in (1, 2), count
    return text

t = common((ROOT / 'record_core_polar_draft.py').read_text(encoding='utf-8'))
t = t.replace(repr(OLD_NAMES), repr(NAMES))
t = t.replace("assert parent['actual_polar_conjugates_entire_base_into_commutant']",
              "assert parent['actual_polar_conjugates_core_into_commutant']")
t = replace_body(t)
t = t.replace('Freeze five modules extending polar commutation to the entire core.',
              'Freeze the Gaussian polar unitary and cyclic separating vector construction.')
create('record_gaussian_polar_draft.py', t)

t = common((ROOT / 'prepare_core_polar_stage.py').read_text(encoding='utf-8'))
t = t.replace(repr(OLD_NAMES), repr(NAMES))
t = t.replace("len(draft['targets']) == 28", "len(draft['targets']) == 34")
t = t.replace('assert count == 463', 'assert count == 491')
t = t.replace("text = once(text, '== 463', '== 491')", "text = once(text, '== 491', '== 525')")
t = t.replace("'LocalBasePolarCommutation', 'BasePolarStrongLimit'",
              "'ScalarGNSGeneratorTransport', 'CorePolarInclusion'")
t = t.replace('TGLExt/V350BasePolarStrongLimit.lean', 'TGLExt/V350CorePolarInclusion.lean')
begin = t.index('anchor = "        \'localBase_polar_commutes\'')
end = t.index('save(path, text)', begin)
t = t[:begin] + '''anchor = "        'scalarGNS_commutation_from_generators', 'scalarTomitaPolar_core_commutant_mem'),\\n"
text = once(text, anchor, anchor + "    'gaussian_unitary_and_same_GNS_cyclic_separating_vector': (\\n"
    "        'boundedInjectivePolar_intertwines', 'scalarGaussianImage_eq_orbit',\\n"
    "        'scalarGaussianUnitary_intertwines', 'scalarGNSCyclicVector_separating',\\n"
    "        'scalarGNSCyclicVector_cyclic'),\\n")
''' + t[end:]
t = t.replace("'new_targets': 28", "'new_targets': 34").replace('count + 28', 'count + 34')
t = t.replace('Prepare the independently reviewed inclusion for the entire core.',
              'Prepare the independently reviewed Gaussian polar and cyclic vector.')
create('prepare_gaussian_polar_stage.py', t)

t = common((ROOT / 'record_core_polar_progress.py').read_text(encoding='utf-8'))
t = replace_body(t)
t = t.replace('Registro anterior, cuja passagem dos geradores ao core foi resolvida para a inclusão direta',
              'Registro anterior: inclusão direta preservada; inversa ainda aberta')
t = t.replace('RELATORIO_CONJUGACAO_POLAR_BASE_INTEGRADA.md',
              'RELATORIO_INCLUSAO_POLAR_CORE_INTEGRADA.md')
t = t.replace('Record reviewed core polar inclusion with the complete memory lineage.',
              'Record reviewed Gaussian cyclic preparation with the complete memory lineage.')
create('record_gaussian_polar_progress.py', t)

t = common((ROOT / 'verify_core_polar_custody.py').read_text(encoding='utf-8'))
t = t.replace('Reread the integrated core inclusion, exact-byte backups and parent lineage.',
              'Reread the integrated Gaussian polar preparation and exact-byte memory lineage.')
create('verify_gaussian_polar_custody.py', t)
print('Created four-module/34-target helpers. No integration or memory writes executed.')

