"""Derive the core-inclusion stage helpers without modifying their sealed parents."""
import ast
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
OLD_NAMES = ['LevelExpectationUniformBound', 'LevelExpectationStrongLimit', 'LocalBasePolarCommutation', 'BasePolarStrongLimit']
NAMES = ['FiniteSetFibreRead', 'FibreSlices', 'ReducingCommutantTransport', 'ScalarGNSGeneratorTransport', 'CorePolarInclusion']
OLD_FLAGS = ['finite_level_expectations_uniformly_bounded', 'actual_polar_conjugates_entire_base_into_commutant', 'finite_level_expectations_strongly_approximate_base', 'base_polar_commutes_with_every_core_left_element']
FLAGS = ['finite_set_reads_total', 'actual_polar_conjugates_core_into_commutant', 'scalar_GNS_generator_transport_proved', 'core_polar_commutes_with_every_core_left_element']
BODY = '''No mesmo espaço H_I=ScalarGNSHilbert P do peso escalar,
N=regularCoreAlgebra P, π=scalarGNSRepresentation P, Δ=S†S e
J=scalarTomitaPolarFactor P permanecem os objetos já construídos.

Os operadores de inserção E_S(v)=1_S v, com S mensurável de medida finita, satisfazem
E_S†f=integral_S f. Todas essas leituras juntas determinam f em L².
Seus coeficientes E_S† T E_U determinam cada operador limitado T.
Isso transporta a comutação dos geradores para sua álgebra gerada por
bicomutante na amplificação fibre. A conjugação dualOrbit e a extensão
por zero no complemento ortogonal transportam a geração ao GNS atual.
O lema genérico de restrição exige geração ambiente; essa premissa é
demonstrada na aplicação efetiva scalarGNS_commutation_from_generators.

Combinando a base inteira e os unitários regulares, já cobertos, a
involução do MESMO J e a geração agora demonstrada fornecem:

    [J π(x) J⁻¹, π(y)] = 0, para TODO x∈N e TODO y∈N;
    J π(N) J ⊆ π(N)'.

[REAL] A passagem dos geradores ao core inteiro foi resolvida para a
inclusão acima. Não há troca pelo J da torre, nem hipótese de densidade
ou normalidade restante no enunciado concreto. Não se usa avaliação
pontual de representantes L² ou função constante não integrável na reta.
[OPEN] A inclusão inversa π(N)'⊆Jπ(N)J ainda não foi provada. J²=I
e a inclusão direta não a fornecem automaticamente.
Também permanecem identificação de Δ^it com o fluxo/KMS do mesmo peso,
traço/escala/canto Three Locks, H1/H2/H3 físicos compatíveis, setor quântico
interagente e composição/consumo pelos certificados/runtime.
Reutilizar Einstein/Fisher/gauge de Chatgpt com suas hipóteses. Seis flags falsas.

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
    text = text.replace('base_polar', 'core_polar').replace('BASE_POLAR', 'CORE_POLAR')
    text = text.replace('matrix_polar_custody.json', 'base_polar_custody.json')
    text = text.replace('CONJUGACAO_POLAR_BASE', 'INCLUSAO_POLAR_CORE')
    text = text.replace('quatro módulos/19 alvos', 'cinco módulos/28 alvos')
    text = text.replace('Quatro módulos/19 alvos', 'Cinco módulos/28 alvos')
    text = text.replace('Conjugação polar da álgebra-base', 'Inclusão polar do core inteiro')
    for old, new in zip(OLD_FLAGS, FLAGS):
        text = text.replace(old.replace('base_polar', 'core_polar'), new)
    text = text.replace('len(targets) == 19', 'len(targets) == 28')
    text = text.replace('len(modules) == 4', 'len(modules) == 5')
    return text

def replace_body(text):
    text, count = re.subn(r'M=theFactorObject P, N=regularCoreAlgebra P.*?(?=\[REAL — fiação preservada\])',
        lambda _: BODY, text, flags=re.S)
    assert count in (1, 2), count
    return text

t = common((ROOT / 'record_base_polar_draft.py').read_text(encoding='utf-8'))
t = t.replace(repr(OLD_NAMES), repr(NAMES))
t = t.replace("assert parent['actual_polar_conjugates_base_matrix_units']",
              "assert parent['actual_polar_conjugates_entire_base_into_commutant']")
t = replace_body(t)
t = t.replace('Freeze four modules extending polar commutation to the entire base algebra.',
              'Freeze five modules extending polar commutation to the entire core.')
create('record_core_polar_draft.py', t)

t = common((ROOT / 'prepare_base_polar_stage.py').read_text(encoding='utf-8'))
t = t.replace(repr(OLD_NAMES), repr(NAMES))
t = t.replace("len(draft['targets']) == 19", "len(draft['targets']) == 28")
t = t.replace('assert count == 444', 'assert count == 463')
t = t.replace("text = once(text, '== 444', '== 463')", "text = once(text, '== 463', '== 491')")
t = t.replace("'MatrixUnitPolarTransport', 'MatrixUnitPolarCommutation'",
              "'LocalBasePolarCommutation', 'BasePolarStrongLimit'")
t = t.replace('TGLExt/V350MatrixUnitPolarCommutation.lean', 'TGLExt/V350BasePolarStrongLimit.lean')
begin = t.index('anchor = "        \'matrixUnit_positiveRoot_right_scaling\'')
end = t.index('save(path, text)', begin)
t = t[:begin] + '''anchor = "        'localBase_polar_commutes', 'base_polar_commutes'),\\n"
text = once(text, anchor, anchor + "    'same_polar_entire_core_inclusion': (\\n"
    "        'finiteSetEmbedding_reads_separate', 'fibre_generated_mem',\\n"
    "        'scalarGNS_commutation_from_generators', 'scalarTomitaPolar_core_commutant_mem'),\\n")
''' + t[end:]
t = t.replace("'new_targets': 19", "'new_targets': 28").replace('count + 19', 'count + 28')
t = t.replace('Prepare the independently reviewed local right scaling on D(S†S).',
              'Prepare the independently reviewed inclusion for the entire core.')
create('prepare_core_polar_stage.py', t)

t = common((ROOT / 'record_base_polar_progress.py').read_text(encoding='utf-8'))
t = replace_body(t)
t = t.replace('Registro anterior, cuja passagem dos níveis à base inteira foi resolvida',
              'Registro anterior, cuja passagem dos geradores ao core foi resolvida para a inclusão direta')
t = t.replace('RELATORIO_CONJUGACAO_POLAR_MATRICIAL_INTEGRADA.md',
              'RELATORIO_CONJUGACAO_POLAR_BASE_INTEGRADA.md')
t = t.replace('Record reviewed entire-base polar commutation with the complete memory lineage.',
              'Record reviewed core polar inclusion with the complete memory lineage.')
create('record_core_polar_progress.py', t)

t = common((ROOT / 'verify_base_polar_custody.py').read_text(encoding='utf-8'))
t = t.replace('Reread the integrated right-adjoint bridge, exact-byte backups and two parent links.',
              'Reread the integrated core inclusion, exact-byte backups and parent lineage.')
create('verify_core_polar_custody.py', t)
print('Created five-module/28-target helpers. No integration or memory writes executed.')
