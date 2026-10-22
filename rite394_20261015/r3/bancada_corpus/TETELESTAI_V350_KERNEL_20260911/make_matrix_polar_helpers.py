"""Create new stage helpers; never edit any previously sealed helper."""
import ast
from pathlib import Path

ROOT = Path(__file__).resolve().parent
NAMES = ['PositiveRootIntertwining', 'ScaledPositiveResolvent', 'ScaledResolventRoots',
         'ScaledRootGraphTransport', 'MatrixUnitResolventScaling', 'MatrixUnitRootScaling',
         'MatrixUnitPolarTransport', 'MatrixUnitPolarCommutation']
OLD_NAMES = ['ScalarRegularRightPolar', 'ScalarRegularPolarCommutation', 'ScalarRegularRightContinuity']
OLD_FLAGS = ['same_actual_root_domain_regular_invariant', 'actual_polar_conjugates_regular_generator',
             'regular_right_strongly_continuous', 'regular_right_commutes_with_every_left_element']
NEW_FLAGS = ['matrix_unit_same_root_scaling_proved', 'actual_polar_conjugates_base_matrix_units',
             'matrix_unit_root_domain_preserved', 'homogeneous_right_commutes_with_every_left_element']
BODY = '''No mesmo H_I do peso escalar, A=S†S, T=(I+A)⁻¹, B=√A e
J=scalarTomitaPolarFactor P continuam os objetos efetivos já construídos.
Para r=w_i/w_j>0 e R_ij a ação direita da unidade matricial:

    B R_ij x=√r R_ij Bx, para TODO x∈D(B), com R_ij D(B)⊆D(B);
    J π(e_ij*) J⁻¹=√r R_ij;
    J π(e_ij) J⁻¹=√(w_j/w_i) R_ji.

A passagem usa D=rI+(1-r)T estritamente positivo, Q=T D⁻¹ positivo≤I,
T R_ij=R_ij Q e cálculo funcional sobre a união compacta dos espectros.
O gráfico parametrizado por √T e √(1-T) é transportado inteiro, usando
apenas a sobrejetividade da raiz de D⁻¹, que é limitada e inversível.
Não se supõe inversa limitada de B nem invertibilidade de R_ij.
Usando S=JB em D(B), prova-se √r·J R_ij=π(e_ij*)J em Ran(B); a densidade de Ran(B) e a continuidade dos dois membros estendem essa identidade a H_I. O fator polar J é o mesmo já construído.

Toda direita homogênea construída comuta com TODO π(a), a∈N, por
associatividade no domínio escalar completo n_ν e densidade. Portanto o
J-conjugado de cada unidade matricial local da base comuta com todo π(N).
Isso soma-se à família regular e sua continuidade forte já integradas.
A pendência de escala matricial até a raiz/J do estágio anterior está resolvida.

[OPEN] Estender dos geradores/níveis locais ao fecho da álgebra representada
e provar a igualdade global Jπ(N)J=π(N)', não só as inclusões nos geradores.
Ainda faltam identificação de A^it com o fluxo/KMS do mesmo peso,
traço/escala/canto Three Locks, H1/H2/H3 físicos compatíveis, setor quântico
interagente e composição/consumo pelos certificados/runtime.
Reutilizar Einstein/Fisher/gauge de Chatgpt com suas hipóteses. Seis flags falsas.

'''

def create(name, text):
    ast.parse(text)
    p = ROOT / name
    assert not p.exists()
    raw = text.encode('utf-8')
    tmp = p.with_suffix('.py.tmp')
    with tmp.open('xb') as stream:
        stream.write(raw)
    assert tmp.read_bytes() == raw
    tmp.replace(p)
    assert p.read_bytes() == raw

def convert_common(text):
    text = text.replace('regular_polar', 'matrix_polar').replace('REGULAR_POLAR', 'MATRIX_POLAR')
    text = text.replace('regular_right_custody.json', 'regular_polar_custody.json')
    text = text.replace('CONJUGACAO_POLAR_REGULAR', 'CONJUGACAO_POLAR_MATRICIAL')
    text = text.replace('três módulos/16 alvos', 'oito módulos/32 alvos')
    text = text.replace('Três módulos/16 alvos', 'Oito módulos/32 alvos')
    text = text.replace('Conjugação polar regular', 'Conjugação polar matricial')
    for old, new in zip(OLD_FLAGS, NEW_FLAGS):
        text = text.replace(old, new)
    text = text.replace('assert len(targets) == 16', 'assert len(targets) == 32')
    text = text.replace('len(modules) == 3 and len(targets) == 16', 'len(modules) == 8 and len(targets) == 32')
    return text

t = convert_common((ROOT / 'record_regular_polar_draft.py').read_text(encoding='utf-8'))
t = t.replace(repr(OLD_NAMES), repr(NAMES))
t = t.replace("assert parent['regular_right_commutes_on_full_square_domain']", "assert parent['actual_polar_conjugates_regular_generator']")
begin = t.index('No mesmo H_I do peso escalar')
end = t.index('[REAL — fiação preservada]', begin)
t = t[:begin] + BODY + t[end:]
t = t.replace('"""Freeze the two full-domain right-scaling modules before independent review."""',
              '"""Freeze eight modules proving matrix-unit root and polar transport."""')
create('record_matrix_polar_draft.py', t)

t = convert_common((ROOT / 'prepare_regular_polar_stage.py').read_text(encoding='utf-8'))
t = t.replace(repr(OLD_NAMES), repr(NAMES))
t = t.replace("len(draft['targets']) == 16", "len(draft['targets']) == 32")
t = t.replace('assert count == 396', 'assert count == 412')
t = t.replace("'ScalarRegularRightGNS', 'ScalarRegularRightTomita', 'ScalarRegularRightSquare'",
              "'ScalarRegularRightPolar', 'ScalarRegularPolarCommutation', 'ScalarRegularRightContinuity'")
t = t.replace("text = once(text, '== 396', '== 412')", "text = once(text, '== 412', '== 444')")
t = t.replace('TGLExt/V350ScalarRegularRightSquare.lean', 'TGLExt/V350ScalarRegularRightContinuity.lean')
begin = t.index("anchor = \"        'scalarTomitaSquare_regular_right_commutes'")
end = t.index('save(path, text)', begin)
block = '''anchor = "        'scalarTomitaPolar_regular_generator_commutes', 'regularRightGNS_strongly_continuous'),\\n"
text = once(text, anchor, anchor + "    'same_polar_matrix_unit_root_scaling': (\\n"
    "        'positive_sqrt_intertwines', 'scaledResolventDenominator_positive',\\n"
    "        'resolvent_root_graph_scaled', 'matrixUnit_resolvent_right_scaling',\\n"
    "        'matrixUnit_positiveRoot_right_scaling', 'matrixUnit_polar_generator_commutes'),\\n")
'''
t = t[:begin] + block + t[end:]
t = t.replace("'new_targets': 16", "'new_targets': 32").replace('count + 16', 'count + 32')
create('prepare_matrix_polar_stage.py', t)

t = convert_common((ROOT / 'record_regular_polar_progress.py').read_text(encoding='utf-8'))
for _ in range(2):
    begin = t.index('No mesmo H_I do peso escalar')
    end = t.index('[REAL — fiação preservada]', begin)
    t = t[:begin] + BODY.replace('No mesmo H_I', 'Sobre o mesmo H_I', 1) + t[end:]
t = t.replace('Registro anterior, cuja pendência de continuidade foi resolvida',
              'Registro anterior, cuja passagem matricial à raiz e J foi resolvida')
t = t.replace('RELATORIO_DIREITA_UNITARIA_REGULAR_INTEGRADA.md', 'RELATORIO_CONJUGACAO_POLAR_REGULAR_INTEGRADA.md')
t = t.replace('"""Record the reviewed right-scaling integration and append the full memory lineage."""',
              '"""Record reviewed matrix-unit polar transport with the complete memory lineage."""')
create('record_matrix_polar_progress.py', t)

t = convert_common((ROOT / 'verify_regular_polar_custody.py').read_text(encoding='utf-8'))
create('verify_matrix_polar_custody.py', t)
print('Created four helpers for 8 modules / 32 targets; no stage mutation executed.')
