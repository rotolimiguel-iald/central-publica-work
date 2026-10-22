"""Derive a separate bounded right-pair stage from reviewed parent helpers."""
import ast
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
OLD_NAMES = ['ScalarRightRegularization', 'ScalarCommutantRegularization']
NAMES = ['ScalarRightAdjointPair', 'ScalarCommutantSandwich', 'ScalarPairedRightAlgebra']
OLD_FLAGS = ['full_weight_right_averages_constructed', 'commutant_right_bounded_approximation_constructed',
    'right_bounded_reconstruction_still_open', 'original_weight_J_not_replaced']
FLAGS = ['original_adjoint_right_pairs_constructed', 'paired_right_star_algebra_constructed',
    'paired_right_algebra_generates_commutant', 'original_weight_J_not_replaced']
BODY = '''No mesmo H_I, com o ideal completo n_ν e os operadores fechados originais
S e F=S†, ScalarRightAdjointPair dá dois vetores η, ζ para um operador limitado R:
RΛν(a)=π(a)η e R*Λν(a)=π(a)ζ para todo a∈n_ν.
[REAL] A relação Fη=ζ é PROVADA dessas identidades, não incluída nas hipóteses.
A prova regulariza, passa ao limite no pareamento e usa o fecho do grafo
completo de S e a caracterização maximal do adjunto original.

[REAL] Para todo T∈π(N)', K_h(T)=R_h* T R_h possui esse par direito,
com η=R_h*Tη_h e ζ=R_h*T*η_h, onde η_h=Λν(e_h), h>0.
||K_h(T)||≤||T|| e K_h(T)→T fortemente-* quando h↓0.
A ordem dos fatores é preservada: não se supõe que T comute com R_h.
R_h*→I usa o bound de contração; não se presume continuidade geral de star em SOT.

[REAL] Os operadores com par direito formam uma NonUnitalStarSubalgebra:
zero, soma, multiplicação escalar, produto e adjunto foram construídos.
A álgebra de von Neumann gerada por ela é TODO o comutante π(N)'.

[OPEN] Isso é uma álgebra de operadores limitados com dois vetores direitos.
Ainda não é a plenitude de uma álgebra de Hilbert, nem a densidade de um
núcleo de grafo para F, nem a reconstrução R=Jπ(b)J. A inclusão inversa
π(N)'⊆Jπ(N)J e o fechamento von Neumann da imagem π(N) continuam abertos.
O J original não foi trocado por conjugação de estado gaussiano.
Permanecem abertos Δ^it/KMS, traço/escala/canto Three Locks, H1/H2/H3 físicos,
setor interagente e consumo por certificados tipados/runtime.
Seis flags maiores falsas; esta construção não muda o gate.

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

def common(text):
    text = text.replace('right_regularization', 'paired_right').replace('RIGHT_REGULARIZATION', 'PAIRED_RIGHT')
    text = text.replace('gaussian_polar_custody.json', 'right_regularization_custody.json')
    text = text.replace('REGULARIZACAO_COMUTANTE', 'ALGEBRA_DIREITA_ADJUNTO')
    text = text.replace('dois módulos/19 alvos', 'três módulos/29 alvos').replace('Dois módulos/19 alvos', 'Três módulos/29 alvos')
    text = text.replace('Regularização de todo o comutante', 'Álgebra direita e adjunto original')
    for old, new in zip(OLD_FLAGS, FLAGS):
        text = text.replace(old, new)
    text = text.replace('len(targets) == 19', 'len(targets) == 29').replace('len(modules) == 2', 'len(modules) == 3')
    text = text.replace(repr(OLD_NAMES), repr(NAMES))
    return text

def replace_body(text):
    text, count = re.subn(r'No mesmo H_I e com o ideal completo.*?(?=\[REAL — fiação preservada\])',
        lambda _: BODY, text, flags=re.S)
    assert count in (1, 2), count
    return text

t = replace_body(common((ROOT / 'record_right_regularization_draft.py').read_text(encoding='utf-8')))
t = t.replace("parent['gaussian_polar_unitary_constructed']", "parent['full_weight_right_averages_constructed']")
t = t.replace('Freeze actual bounded right regularization of the entire commutant.',
    'Freeze actual right pairs, their original maximal adjoint and generated commutant.')
create('record_paired_right_draft.py', t)

t = common((ROOT / 'prepare_right_regularization_stage.py').read_text(encoding='utf-8'))
t = t.replace("len(draft['targets']) == 19", "len(draft['targets']) == 29")
t = t.replace('assert count == 525', 'assert count == 544')
t = t.replace("text = once(text, '== 525', '== 544')", "text = once(text, '== 544', '== 573')")
t = t.replace("'ScalarGaussianImage', 'ScalarGaussianUnitary'", "'ScalarRightRegularization', 'ScalarCommutantRegularization'")
t = t.replace('TGLExt/V350ScalarGaussianUnitary.lean', 'TGLExt/V350ScalarCommutantRegularization.lean')
begin = t.index('anchor = "        \'scalarGNSCyclicVector_cyclic\'')
end = t.index('save(path, text)', begin)
t = t[:begin] + '''anchor = "        'scalarCommutant_mem_generated_rightBounded'),\\n"
text = once(text, anchor, anchor + "    'original_adjoint_pairs_and_generated_right_star_algebra': (\\n"
    "        'scalarRightAdjointPair_maximal', 'scalarCommutantSandwich_in_original_adjoint',\\n"
    "        'scalarCommutant_paired_right_approximation',\\n"
    "        'scalarPairedRightAlgebra_generated_eq_commutant'),\\n")
''' + t[end:]
t = t.replace("'new_targets': 19", "'new_targets': 29").replace('count + 19', 'count + 29')
t = t.replace('Prepare the independently reviewed full-weight right regularization.',
    'Prepare the independently reviewed original-adjoint right-pair algebra.')
create('prepare_paired_right_stage.py', t)

t = replace_body(common((ROOT / 'record_right_regularization_progress.py').read_text(encoding='utf-8')))
t = t.replace('RELATORIO_POLAR_GAUSSIANO_CICLICO_INTEGRADA.md', 'RELATORIO_REGULARIZACAO_COMUTANTE_INTEGRADA.md')
t = t.replace('Record reviewed right regularization with the complete memory lineage.',
    'Record reviewed original-adjoint right pairs with the complete memory lineage.')
create('record_paired_right_progress.py', t)

t = common((ROOT / 'verify_right_regularization_custody.py').read_text(encoding='utf-8'))
t = t.replace('Reread integrated commutant regularization and exact-byte memory lineage.',
    'Reread integrated original-adjoint right pairs and exact-byte memory lineage.')
create('verify_paired_right_custody.py', t)
print('Created three-module/29-target helpers. No integration or memory writes executed.')
