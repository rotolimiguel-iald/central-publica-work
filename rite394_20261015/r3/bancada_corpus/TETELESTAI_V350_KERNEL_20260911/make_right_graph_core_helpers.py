"""Derive the original-F graph-core stage helpers; no integration/memory writes."""
import ast
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
OLD_NAMES = ['ReducingCommutantCompression', 'ReducingBicommutantLift',
    'SeparatingRestrictionVonNeumann', 'ScalarGNSVonNeumann']
NAMES = ['ComplexGraphProjection', 'ScalarRightMultiplicationGraph',
    'HilbertProjectionBlocks', 'ScalarRightProjectionPair',
    'FixedVectorGraphCore', 'ScalarRightGraphCore']
OLD_FLAGS = ['restricted_bicommutant_bounded_lift_constructed',
    'separating_restriction_bicommutant_closed', 'actual_scalar_GNS_image_von_neumann']
FLAGS = ['original_F_fixed_vectors_detected',
    'right_selfadjoint_vectors_dense_in_original_F_fixed_space',
    'right_pair_graph_core_equals_original_F']
BODY = '''[REAL] O fecho do grafo da involução em j(A_right) é agora igual
ao grafo do adjunto maximal F ORIGINAL, no H_I original e no ideal completo
do peso escalar. scalarRightPairGraph_closure_eq_original prova a igualdade;
o adjunto não foi redefinido a partir desse fecho.

Para η em Fix(F), o grafo complexo auxiliar fecha os pares (Λa,π(a)η).
A identidade de pareamento S/F torna-o simétrico, e sua projeção comuta
com a ação diagonal de π(N). Seus blocos A,B,D fornecem um par direito
limitado efetivo B com vetores Aη e η−Dη. O elemento auto-adjunto B+B*
tem inscrição vη=Aη+η−Dη e satisfaz
Re<η,vη>=||P(η,0)||²+||Pperp(0,η)||²>0 para η diferente de zero.
A estrita positividade usa a densidade de Λ, sem supor limitada
a multiplicação direita a↦π(a)η.

Essa detecção positiva prova a densidade REAL das inscrições auto-adjuntas
em Fix(F). A decomposição do domínio da involução original em h+ik,
F(h+ik)=h−ik, e a continuidade dessa mistura dão a densidade no grafo.
O grafo complexo auxiliar não foi confundido com o grafo real de F.
Todas as hipóteses do lema genérico foram descarregadas nos objetos
concretos: fecho, domínio invariante, involutividade, pareamento e detecção.
S, F e J originais não foram substituídos; não há graph-core recebido
como campo de uma estrutura nem sorryAx na rodada aceita.

[OPEN] Permanecem a reconstrução R=Jπ(b)J e a inclusão inversa
π(N)'⊆Jπ(N)J para o J original. A igualdade de grafos entrega uma
obrigação necessária, não essa conclusão inteira automaticamente.
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
    text = text.replace('scalar_vna', 'right_graph_core').replace('SCALAR_VNA', 'RIGHT_GRAPH_CORE')
    text = text.replace('right_vector_custody.json', 'scalar_vna_custody.json')
    text = text.replace('IMAGEM_ESCALAR_VON_NEUMANN', 'GRAPH_CORE_ADJUNTO_ORIGINAL_F')
    text = text.replace('quatro módulos/27 alvos', 'seis módulos/57 alvos')
    text = text.replace('Quatro módulos/27 alvos', 'Seis módulos/57 alvos')
    text = text.replace('Imagem escalar de von Neumann', 'Graph core do adjunto original F')
    for old, new in zip(OLD_FLAGS, FLAGS):
        text = text.replace(old, new)
    text = text.replace('len(targets) == 27', 'len(targets) == 57')
    text = text.replace('len(modules) == 4', 'len(modules) == 6')
    text = text.replace(repr(OLD_NAMES), repr(NAMES))
    return text

def replace_body(text):
    text, count = re.subn(r'\[REAL\] A imagem da representação escalar.*?(?=\[REAL — fiação preservada\])',
        lambda _: BODY, text, flags=re.S)
    assert count in (1, 2), count
    return text

t = replace_body(common((ROOT / 'record_scalar_vna_draft.py').read_text(encoding='utf-8')))
t = t.replace("parent['right_vector_products_dense_and_involution_closable']",
    "parent['actual_scalar_GNS_image_von_neumann']")
t = t.replace('Freeze the actual scalar GNS image as a von Neumann algebra.',
    'Freeze the right-algebra graph core of the original maximal adjoint F.')
create('record_right_graph_core_draft.py', t)

t = common((ROOT / 'prepare_scalar_vna_stage.py').read_text(encoding='utf-8'))
t = t.replace("len(draft['targets']) == 27", "len(draft['targets']) == 57")
t = t.replace('assert count == 598', 'assert count == 625')
t = t.replace("text = once(text, '== 598', '== 625')", "text = once(text, '== 625', '== 682')")
t = t.replace("'ScalarRightPairVector', 'ScalarRightHilbertCore'",
    "'SeparatingRestrictionVonNeumann', 'ScalarGNSVonNeumann'")
t = t.replace('TGLExt/V350ScalarRightHilbertCore.lean', 'TGLExt/V350ScalarGNSVonNeumann.lean')
begin = t.index('anchor = "        \'scalarRightPairVector_products_dense\'')
end = t.index('save(path, text)', begin)
t = t[:begin] + '''anchor = "        'scalarGNSVonNeumann_coe'),\\n"
text = once(text, anchor, anchor + "    'right_pair_graph_core_equals_original_F': (\\n"
    "        'scalarRightMultiplicationVector_symmetric', 'hilbertProjectionWitness_energy',\\n"
    "        'complexGraph_witness_positive', 'scalarRightProjectionPair',\\n"
    "        'scalarRight_selfadjoint_detects_fixed', 'selfadjointVectorSubmodule_closure',\\n"
    "        'conjugateGraph_closure_eq_original', 'scalarRightSelfadjointVectors_closure',\\n"
    "        'scalarRightPairGraph_closure_eq_original'),\\n")
''' + t[end:]
t = t.replace("'new_targets': 27", "'new_targets': 57").replace('count + 27', 'count + 57')
create('prepare_right_graph_core_stage.py', t)

t = replace_body(common((ROOT / 'record_scalar_vna_progress.py').read_text(encoding='utf-8')))
t = t.replace('Record the reviewed scalar VNA image with the complete exact-byte memory lineage.',
    'Record the reviewed original-F graph core with exact-byte memory lineage.')
create('record_right_graph_core_progress.py', t)
create('verify_right_graph_core_custody.py', common((ROOT / 'verify_scalar_vna_custody.py').read_text(encoding='utf-8')))
print('Created six-module/57-target helpers. No integration or memory writes executed.')
