"""Derive isolated right-vector integration helpers from the reviewed parent stage."""
import ast
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
OLD_NAMES = ['ScalarRightAdjointPair', 'ScalarCommutantSandwich', 'ScalarPairedRightAlgebra']
NAMES = ['ScalarGaussianRightPairs', 'ScalarRightPairVector', 'ScalarRightHilbertCore']
OLD_FLAGS = ['original_adjoint_right_pairs_constructed', 'paired_right_star_algebra_constructed',
    'paired_right_algebra_generates_commutant']
FLAGS = ['full_weight_gaussian_right_pairs_constructed', 'right_vector_injective_dense_embedding_constructed',
    'right_vector_products_dense_and_involution_closable']
BODY = '''No mesmo H_I e ideal completo n_ν, CΛν(a)=ρ(a)Ωg foi estendido
ao mapa gaussiano original. Para B∈ρ(N)', C*BC tem par direito real
(C*BΩg,C*B*Ωg). C não foi invertido e o J original não foi trocado.

[REAL] O vetor de um par é único para cada operador; o operador é único
para cada vetor. A escolha de representante produz uma aplicação linear
injetiva j da álgebra de operadores pareados em H_I, independente da escolha.
A imagem de j é densa em NORMA de H_I, usando C injetivo e a órbita
densa do comutante auxiliar. Vale j(ab)=a j(b) e F j(a)=j(a*), no F original.

[REAL] Foram provados o bound ||j(ab)||≤||a||_op ||j(b)|| e a identidade
de produto interno <j(ab),j(c)>=<j(b),j(a*c)>. K_h(I)=R_h*R_h fornece
aproximação forte da identidade por operadores pareados. Os próprios
produtos j(ab) são densos em H_I. O fecho do grafo da involução em j(A)
está contido no grafo fechado do F original e não tem parte vertical não nula.

[OPEN] Falta a IGUALDADE desse fecho com o grafo de F; densidade Hilbert
e densidade de produtos não são densidade na norma de grafo. Não se afirmou
plenitude de álgebra de Hilbert, reconstrução R=Jπ(b)J, inclusão inversa
π(N)'⊆Jπ(N)J ou fechamento von Neumann da imagem π(N).
Δ^it/KMS, traço/escala/canto Three Locks, H1/H2/H3 físicos, setor interagente
e consumo por certificados tipados/runtime continuam abertos.
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
    text = text.replace('paired_right', 'right_vector').replace('PAIRED_RIGHT', 'RIGHT_VECTOR')
    text = text.replace('right_regularization_custody.json', 'paired_right_custody.json')
    text = text.replace('ALGEBRA_DIREITA_ADJUNTO', 'VETORES_DIREITOS_DENSOS')
    text = text.replace('módulos/29 alvos', 'módulos/25 alvos')
    text = text.replace('Álgebra direita e adjunto original', 'Vetores direitos densos e involução original')
    # Names containing paired_right have already been converted above.
    for old, new in zip(OLD_FLAGS, FLAGS):
        text = text.replace(old.replace('paired_right', 'right_vector'), new)
    text = text.replace('len(targets) == 29', 'len(targets) == 25')
    text = text.replace(repr(OLD_NAMES), repr(NAMES))
    return text

def replace_body(text):
    text, count = re.subn(r'No mesmo H_I, com o ideal completo.*?(?=\[REAL — fiação preservada\])',
        lambda _: BODY, text, flags=re.S)
    assert count in (1, 2), count
    return text

t = replace_body(common((ROOT / 'record_paired_right_draft.py').read_text(encoding='utf-8')))
t = t.replace("parent['full_weight_right_averages_constructed']", "parent['paired_right_algebra_generates_commutant']")
t = t.replace('Freeze actual right pairs, their original maximal adjoint and generated commutant.',
    'Freeze actual dense right vectors and their closable original-adjoint involution.')
create('record_right_vector_draft.py', t)

t = common((ROOT / 'prepare_paired_right_stage.py').read_text(encoding='utf-8'))
t = t.replace("len(draft['targets']) == 29", "len(draft['targets']) == 25")
t = t.replace('assert count == 544', 'assert count == 573')
t = t.replace("text = once(text, '== 544', '== 573')", "text = once(text, '== 573', '== 598')")
t = t.replace("'ScalarRightRegularization', 'ScalarCommutantRegularization'", "'ScalarCommutantSandwich', 'ScalarPairedRightAlgebra'")
t = t.replace('TGLExt/V350ScalarCommutantRegularization.lean', 'TGLExt/V350ScalarPairedRightAlgebra.lean')
begin = t.index('anchor = "        \'scalarCommutant_mem_generated_rightBounded\'')
end = t.index('save(path, text)', begin)
t = t[:begin] + '''anchor = "        'scalarPairedRightAlgebra_generated_eq_commutant'),\\n"
text = once(text, anchor, anchor + "    'dense_right_vectors_and_closable_original_involution': (\\n"
    "        'scalarGaussianRightAdjointPair', 'scalarRightPairVector_injective',\\n"
    "        'scalarRightPairVector_denseRange', 'scalarRightPairVector_original_adjoint',\\n"
    "        'scalarRightPairGraph_closure_subset_original', 'scalarRightPairGraph_closable',\\n"
    "        'scalarRightPairVector_products_dense'),\\n")
''' + t[end:]
t = t.replace("'new_targets': 29", "'new_targets': 25").replace('count + 29', 'count + 25')
t = t.replace('Prepare the independently reviewed original-adjoint right-pair algebra.',
    'Prepare independently reviewed dense right vectors and their closable involution.')
create('prepare_right_vector_stage.py', t)

t = replace_body(common((ROOT / 'record_paired_right_progress.py').read_text(encoding='utf-8')))
t = t.replace('Record reviewed original-adjoint right pairs with the complete memory lineage.',
    'Record reviewed dense right vectors with the complete exact-byte memory lineage.')
create('record_right_vector_progress.py', t)

t = common((ROOT / 'verify_paired_right_custody.py').read_text(encoding='utf-8'))
t = t.replace('Reread integrated original-adjoint right pairs and exact-byte memory lineage.',
    'Reread integrated dense right vectors and exact-byte memory lineage.')
create('verify_right_vector_custody.py', t)
print('Created three-module/25-target helpers. No integration or memory writes executed.')
