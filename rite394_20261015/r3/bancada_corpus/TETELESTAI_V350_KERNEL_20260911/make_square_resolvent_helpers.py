"""Prepare guarded custody helpers for the rational cutoffs and original-S tests."""
import ast
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
NAMES = ['SquareResolventSupport', 'ScalarRightSquareApproximation', 'ScalarSquareAdjointTest']
BODY = '''[REAL] Para A limitado auto-adjunto, R_n=(I+(n+1)A²)^−1 é uma
sequência antítona de contrações positivas. A estimativa
(n+1)||R_n A v||² ≤ ||v||²/4 e o limite forte existente provam R_n x→0
para x no fecho normado de Ran A. Não se supõe injetividade ou gap, nem
se afirma convergência em norma de operador ou em todo H.

[REAL] Para a=a* na álgebra não unital dos pares direitos, constroem-se
b_n=R_n a, d_n=(n+1)a b_n e c_n=a d_n dentro da MESMA álgebra.
Como operadores, d_n=I−R_n. Os c_n são auto-adjuntos, diferenças de
quadrados auto-adjuntos com coeficiente 1/4, e j(c_n)→j(a).
Não se presumiu I ou R_n pertencente à álgebra não unital.

[REAL] Testes de pareamento nos j(b²), b=b*, caracterizam exatamente o
grafo do S original. A prova estende o pareamento por aproximação,
fecho de Fix F e decomposição h+ik/h−ik, e usa a bidualidade anterior.
Se K e K* limitados realizam as duas ações sobre todos os vetores j(a),
o par de vetores pertence ao grafo desse S. Não se redefine S/F/J.

[OPEN] Ainda é preciso verificar essas duas ações para o candidato
ponderado dos blocos de projeção, provar a cota inferior uniforme do
bloco A e construir o multiplicador limitado. A inclusão inversa pelo
J original, Delta^it/KMS, traço/escala/canto Three Locks, H1/H2/H3 físicos,
setor interagente e consumo por certificados/runtime continuam abertos.
O critério de teste é provado; a aplicação ao candidato não é automática.
Seis flags maiores falsas; objetivo integral ativo.

'''
OLD_FLAGS = ['original_S_is_maximal_adjoint_of_F',
             'selfadjoint_right_pairs_stable_under_commuting_multipliers',
             'right_pair_vectors_in_multiplier_range_closure']
NEW_FLAGS = ['square_resolvents_vanish_on_range_closure',
             'selfadjoint_right_vectors_approximated_by_square_differences',
             'original_S_characterized_by_selfadjoint_square_tests']

def common(text):
    text = text.replace('bidual_right_support', 'square_resolvent')
    text = text.replace('BIDUAL_RIGHT_SUPPORT', 'SQUARE_RESOLVENT')
    text = text.replace('phase_variational_custody.json', 'bidual_right_support_custody.json')
    text = text.replace('BIDUAL_SUPORTE_DIREITO', 'RESOLVENTES_QUADRADOS_TESTE_ORIGINAL')
    text = text.replace('Bidual original e suporte direito e continuidade', 'Resolventes, quadrados e teste do S original')
    text = text.replace('Bidual original e suporte direito', 'Resolventes, quadrados e teste do S original')
    text = text.replace("['ScalarTomitaBidual', 'ScalarRightFunctionalStability']", repr(NAMES))
    text = text.replace('dois módulos/9 alvos', 'três módulos/20 alvos')
    text = text.replace('Dois módulos/9 alvos', 'Três módulos/20 alvos')
    text = text.replace('len(modules) == 2', 'len(modules) == 3')
    text = text.replace('len(targets) == 9', 'len(targets) == 20')
    for old, new in zip(OLD_FLAGS, NEW_FLAGS):
        text = text.replace(old, new)
    return text

def body(text):
    text, count = re.subn(r'\[REAL\] O adjunto maximal de F.*?(?=\[REAL — fiação preservada\])',
                         lambda _: BODY, text, flags=re.S)
    assert count in (1, 2), count
    return text

def create(name, text):
    ast.parse(text)
    path = ROOT / name
    assert not path.exists()
    raw = text.encode('utf-8')
    temp = path.with_suffix('.py.tmp')
    with temp.open('xb') as out:
        out.write(raw)
    assert temp.read_bytes() == raw
    temp.replace(path)
    assert path.read_bytes() == raw

text = body(common((ROOT / 'record_bidual_right_support_draft.py').read_text(encoding='utf-8')))
text = text.replace("parent['original_S_graph_variational_identity']", "parent['original_S_is_maximal_adjoint_of_F']")
text = text.replace('Tentativas Lean recusadas e fontes anteriores foram preservadas;',
                    'Tentativas Lean recusadas e seus logs foram preservados;')
create('record_square_resolvent_draft.py', text)

text = common((ROOT / 'prepare_bidual_right_support_stage.py').read_text(encoding='utf-8'))
text = text.replace("len(draft['targets']) == 9", "len(draft['targets']) == 20")
text = text.replace('assert count == 720', 'assert count == 729')
text = text.replace("text = once(text, '== 720', '== 729')", "text = once(text, '== 729', '== 749')")
text = text.replace("'RealPhaseVariational', 'ScalarPhaseVariational'", "'ScalarTomitaBidual', 'ScalarRightFunctionalStability'")
text = text.replace('TGLExt/V350ScalarPhaseVariational.lean', 'TGLExt/V350ScalarRightFunctionalStability.lean')
start = text.index('anchor = "        \'scalarPhaseVariational_graph_equation\'')
end = text.index('save(path, text)', start)
text = text[:start] + '''anchor = "        'scalarRightPairVector_mem_range_closure'),\\n"
text = once(text, anchor, anchor + "    'rational_squares_and_original_adjoint_test': (\\n"
    "        'squareResolvent_tendsto_zero_on_rangeClosure',\\n"
    "        'scalarRightSquareApproximation_difference_of_squares',\\n"
    "        'scalarRightSquareApproximation_vector_tendsto',\\n"
    "        'scalarClosedTomita_squarePairing_iff', 'scalarClosedTomita_of_boundedPairAction'),\\n")
''' + text[end:]
text = text.replace("'new_targets': 9", "'new_targets': 20").replace('count + 9', 'count + 20')
create('prepare_square_resolvent_stage.py', text)

text = body(common((ROOT / 'record_bidual_right_support_progress.py').read_text(encoding='utf-8')))
text = text.replace('[Rota racional por energia e limite antítono — DERIVED, não compilada]',
                    '[Consulta prévia da rota racional; resultados compilados discriminados acima]')
text = text.replace('[Proposta de aproximação por quadrados — DERIVED, não compilada]',
                    '[Consulta prévia dos quadrados; resultado de teste original formalizado acima]')
create('record_square_resolvent_progress.py', text)
create('verify_square_resolvent_custody.py', common((ROOT / 'verify_bidual_right_support_custody.py').read_text(encoding='utf-8')))
print('Created guarded scripts for 3 modules/20 targets; no proof or integration accepted by generation.')
