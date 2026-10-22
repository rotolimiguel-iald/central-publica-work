"""Create this stage's helpers from the reviewed parent, preserving all parent files."""
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OLD_NAMES = ['PositiveRootIntertwining', 'ScaledPositiveResolvent', 'ScaledResolventRoots',
             'ScaledRootGraphTransport', 'MatrixUnitResolventScaling', 'MatrixUnitRootScaling',
             'MatrixUnitPolarTransport', 'MatrixUnitPolarCommutation']
NAMES = ['LevelExpectationUniformBound', 'LevelExpectationStrongLimit',
         'LocalBasePolarCommutation', 'BasePolarStrongLimit']
OLD_FLAGS = ['matrix_unit_same_root_scaling_proved', 'actual_polar_conjugates_base_matrix_units',
             'matrix_unit_root_domain_preserved', 'homogeneous_right_commutes_with_every_left_element']
FLAGS = ['finite_level_expectations_uniformly_bounded', 'actual_polar_conjugates_entire_base_into_commutant',
         'finite_level_expectations_strongly_approximate_base', 'base_polar_commutes_with_every_core_left_element']
BODY = '''M=theFactorObject P, N=regularCoreAlgebra P, π=scalarGNSRepresentation P,
ι=regularCoreEmbedding P, Δ=S†S e J=scalarTomitaPolarFactor P permanecem os mesmos.
As esperanças E_n dos níveis finitos satisfazem, para TODO x∈M:

    ||E_n(x)|| ≤ 4 ||x||, uniformemente em n;
    E_n(x) → x fortemente;
    π(ι(E_n(x))) → π(ι(x)) fortemente no mesmo H_I.

A ordem positiva herdada de M é construída usando a raiz quadrada dentro
da álgebra fechada em norma. A positividade e a unidade da família dos níveis
produzem a cota explícita por quatro partes positivas. A constante 4 é
suficiente para o limite; não se afirma que seja a norma ótima.
LevelExpectationFamily não é o contrato centralizante ExpectationInput.

A indução matricial trata todos os coeficientes complexos com conjugação:
J(cX)J⁻¹=conj(c) JXJ⁻¹. A comutação passa ao limite forte contra cada
operador limitado fixo. Conclusão no MESMO H_I e com o MESMO J:

    [J π(ι(x)) J⁻¹, π(y)] = 0, para TODO x∈M e TODO y∈N.

[REAL] A pendência de passar das unidades matriciais/níveis finitos à
álgebra-base inteira foi resolvida. A família regular λ_t já estava coberta.
[OPEN] Isso ainda não é Jπ(N)J=π(N)'. Falta passar desses geradores ao
core inteiro na representação e obter a inclusão inversa/global.
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
    text = text.replace('matrix_polar', 'base_polar').replace('MATRIX_POLAR', 'BASE_POLAR')
    text = text.replace('regular_polar_custody.json', 'matrix_polar_custody.json')
    text = text.replace('CONJUGACAO_POLAR_MATRICIAL', 'CONJUGACAO_POLAR_BASE')
    text = text.replace('oito módulos/32 alvos', 'quatro módulos/19 alvos')
    text = text.replace('Oito módulos/32 alvos', 'Quatro módulos/19 alvos')
    text = text.replace('Conjugação polar matricial', 'Conjugação polar da álgebra-base')
    for old, new in zip(OLD_FLAGS, FLAGS):
        text = text.replace(old, new)
    text = text.replace('len(targets) == 32', 'len(targets) == 19')
    text = text.replace('len(modules) == 8', 'len(modules) == 4')
    return text

def replace_body(text, opening):
    count = text.count(opening)
    assert count in (1, 2)
    for _ in range(count):
        begin = text.index(opening)
        end = text.index('[REAL — fiação preservada]', begin)
        text = text[:begin] + BODY + text[end:]
    return text

t = common((ROOT / 'record_matrix_polar_draft.py').read_text(encoding='utf-8'))
t = t.replace(repr(OLD_NAMES), repr(NAMES))
t = t.replace("assert parent['actual_polar_conjugates_regular_generator']",
              "assert parent['actual_polar_conjugates_base_matrix_units']")
t = replace_body(t, 'No mesmo H_I do peso escalar')
t = t.replace('Freeze eight modules proving matrix-unit root and polar transport.',
              'Freeze four modules extending polar commutation to the entire base algebra.')
create('record_base_polar_draft.py', t)

t = common((ROOT / 'prepare_matrix_polar_stage.py').read_text(encoding='utf-8'))
t = t.replace(repr(OLD_NAMES), repr(NAMES))
t = t.replace("len(draft['targets']) == 32", "len(draft['targets']) == 19")
t = t.replace('assert count == 412', 'assert count == 444')
t = t.replace("text = once(text, '== 412', '== 444')", "text = once(text, '== 444', '== 463')")
t = t.replace("'ScalarRegularRightPolar', 'ScalarRegularPolarCommutation', 'ScalarRegularRightContinuity'",
              "'MatrixUnitPolarTransport', 'MatrixUnitPolarCommutation'")
t = t.replace('TGLExt/V350ScalarRegularRightContinuity.lean', 'TGLExt/V350MatrixUnitPolarCommutation.lean')
begin = t.index('anchor = "        \'scalarTomitaPolar_regular_generator_commutes\'')
end = t.index('save(path, text)', begin)
t = t[:begin] + '''anchor = "        'matrixUnit_positiveRoot_right_scaling', 'matrixUnit_polar_generator_commutes'),\\n"
text = once(text, anchor, anchor + "    'same_polar_entire_base': (\\n"
    "        'levelExpectation_uniform_norm_bound', 'represented_levelExpectation_strong_tendsto',\\n"
    "        'localBase_polar_commutes', 'base_polar_commutes'),\\n")
''' + t[end:]
t = t.replace("'new_targets': 32", "'new_targets': 19").replace('count + 32', 'count + 19')
create('prepare_base_polar_stage.py', t)

t = common((ROOT / 'record_matrix_polar_progress.py').read_text(encoding='utf-8'))
t = replace_body(t, 'Sobre o mesmo H_I do peso escalar')
t = t.replace('Registro anterior, cuja passagem matricial à raiz e J foi resolvida',
              'Registro anterior, cuja passagem dos níveis à base inteira foi resolvida')
t = t.replace('RELATORIO_CONJUGACAO_POLAR_REGULAR_INTEGRADA.md',
              'RELATORIO_CONJUGACAO_POLAR_MATRICIAL_INTEGRADA.md')
t = t.replace('Record reviewed matrix-unit polar transport with the complete memory lineage.',
              'Record reviewed entire-base polar commutation with the complete memory lineage.')
create('record_base_polar_progress.py', t)

t = common((ROOT / 'verify_matrix_polar_custody.py').read_text(encoding='utf-8'))
create('verify_base_polar_custody.py', t)
print('Created helpers for four modules / nineteen targets. No integration or memory writes executed.')
