"""Derive isolated scalar VNA stage helpers without running integration or memory writes."""
import ast
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
OLD_NAMES = ['ScalarGaussianRightPairs', 'ScalarRightPairVector', 'ScalarRightHilbertCore']
NAMES = ['ReducingCommutantCompression', 'ReducingBicommutantLift',
    'SeparatingRestrictionVonNeumann', 'ScalarGNSVonNeumann']
OLD_FLAGS = ['full_weight_gaussian_right_pairs_constructed',
    'right_vector_injective_dense_embedding_constructed',
    'right_vector_products_dense_and_involution_closable']
FLAGS = ['restricted_bicommutant_bounded_lift_constructed',
    'separating_restriction_bicommutant_closed', 'actual_scalar_GNS_image_von_neumann']
BODY = '''[REAL] A imagem da representação escalar π(N), no H_I original,
é agora provada igual ao seu bicomutante. Não se trata apenas de definir
a álgebra gerada: mem_scalarGNSVonNeumann_iff fornece para TODO elemento
dela uma pré-imagem efetiva em N; scalarGNSVonNeumann_coe prova a igualdade
com Set.range scalarGNSRepresentation.

A prova usa um levantamento limitado. Para M VNA, K redutor e Ω∈K
separante para M, a órbita M'Ω é densa. Para B no bicomutante da imagem
restrita, a coluna C=D∘incl tem Gram C*C no comutante dessa imagem.
B comuta com a raiz positiva, e ||DBΩ||≤||B|| ||DΩ||.
T(DΩ)=DBΩ estende-se a um operador limitado, que comuta com M'
e por isso pertence a M. A órbita projetada P_K M'Ω é densa em K;
a restrição de T é B. O levantamento satisfaz ||T||≤||B||.

Na aplicação, M é dualOrbitVonNeumann(regularCoreAlgebra P), K é
scalarGaussianImage P e Ω é scalarGaussianVacuum P. Redução, separação
e pertença do vetor foram descarregadas nos objetos concretos. A unidade
LINEAR scalarGaussianUnitary transporta a igualdade à representação π em H_I.
Essa unidade não foi identificada com o J modular; S, F e J originais
não foram substituídos.

[OPEN] Continuam pendentes a igualdade do grafo da involução em j(A_right)
com graph F, reconstrução R=Jπ(b)J e inclusão inversa π(N)'⊆Jπ(N)J.
A consulta CONSULTA_GRAPH_CORE_ORIGINAL_F.md propõe uma rota por blocos
da projeção do grafo de multiplicação direita, ainda sem formalização Lean.
Δ^it/KMS, traço/escala/canto Three Locks, H1/H2/H3 físicos, setor interagente
e consumo por certificados tipados/runtime continuam abertos.
Seis flags maiores falsas; esta construção não muda o gate.

'''

def create(name, text):
    ast.parse(text)
    path = ROOT / name
    assert not path.exists()
    raw = text.encode('utf-8')
    temp = path.with_suffix('.py.tmp')
    with temp.open('xb') as stream:
        stream.write(raw)
    assert temp.read_bytes() == raw
    temp.replace(path)
    assert path.read_bytes() == raw

def common(text):
    text = text.replace('right_vector', 'scalar_vna').replace('RIGHT_VECTOR', 'SCALAR_VNA')
    text = text.replace('paired_right_custody.json', 'right_vector_custody.json')
    text = text.replace('VETORES_DIREITOS_DENSOS', 'IMAGEM_ESCALAR_VON_NEUMANN')
    text = text.replace('três módulos/25 alvos', 'quatro módulos/27 alvos')
    text = text.replace('Três módulos/25 alvos', 'Quatro módulos/27 alvos')
    text = text.replace('Vetores direitos densos e involução original', 'Imagem escalar de von Neumann')
    for old, new in zip(OLD_FLAGS, FLAGS):
        text = text.replace(old.replace('right_vector', 'scalar_vna'), new)
    text = text.replace('len(targets) == 25', 'len(targets) == 27')
    text = text.replace('len(modules) == 3', 'len(modules) == 4')
    text = text.replace(repr(OLD_NAMES), repr(NAMES))
    return text

def replace_body(text):
    text, count = re.subn(r'No mesmo H_I e ideal completo.*?(?=\[REAL — fiação preservada\])',
        lambda _: BODY, text, flags=re.S)
    assert count in (1, 2), count
    return text

t = replace_body(common((ROOT / 'record_right_vector_draft.py').read_text(encoding='utf-8')))
t = t.replace("parent['paired_right_algebra_generates_commutant']",
    "parent['right_vector_products_dense_and_involution_closable']")
t = t.replace('Freeze actual dense right vectors and their closable original-adjoint involution.',
    'Freeze the actual scalar GNS image as a von Neumann algebra.')
create('record_scalar_vna_draft.py', t)

t = common((ROOT / 'prepare_right_vector_stage.py').read_text(encoding='utf-8'))
t = t.replace("len(draft['targets']) == 25", "len(draft['targets']) == 27")
t = t.replace('assert count == 573', 'assert count == 598')
t = t.replace("text = once(text, '== 573', '== 598')", "text = once(text, '== 598', '== 625')")
t = t.replace("'ScalarCommutantSandwich', 'ScalarPairedRightAlgebra'",
    "'ScalarRightPairVector', 'ScalarRightHilbertCore'")
t = t.replace('TGLExt/V350ScalarPairedRightAlgebra.lean', 'TGLExt/V350ScalarRightHilbertCore.lean')
begin = t.index('anchor = "        \'scalarPairedRightAlgebra_generated_eq_commutant\'')
end = t.index('save(path, text)', begin)
t = t[:begin] + '''anchor = "        'scalarRightPairVector_products_dense'),\\n"
text = once(text, anchor, anchor + "    'actual_scalar_GNS_image_von_neumann': (\\n"
    "        'reducingBicommutant_orbit_bound', 'reducingBicommutantLift_mem',\\n"
    "        'reducingBicommutantLift_restrict', 'mem_generated_restriction_iff',\\n"
    "        'scalarGaussianImage_generated_iff', 'mem_scalarGNSVonNeumann_iff',\\n"
    "        'scalarGNSVonNeumann_coe'),\\n")
''' + t[end:]
t = t.replace("'new_targets': 25", "'new_targets': 27").replace('count + 25', 'count + 27')
create('prepare_scalar_vna_stage.py', t)

t = replace_body(common((ROOT / 'record_right_vector_progress.py').read_text(encoding='utf-8')))
t = t.replace('Record reviewed dense right vectors with the complete exact-byte memory lineage.',
    'Record the reviewed scalar VNA image with the complete exact-byte memory lineage.')
create('record_scalar_vna_progress.py', t)

t = common((ROOT / 'verify_right_vector_custody.py').read_text(encoding='utf-8'))
create('verify_scalar_vna_custody.py', t)
print('Created four-module/27-target helpers. No integration or memory writes executed.')
