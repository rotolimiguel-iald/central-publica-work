"""Prepare stage scripts for the original adjoint/polar graph identities."""
import ast
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
OLD_NAMES = ['ComplexGraphProjection', 'ScalarRightMultiplicationGraph',
    'HilbertProjectionBlocks', 'ScalarRightProjectionPair', 'FixedVectorGraphCore', 'ScalarRightGraphCore']
NAMES = ['ScalarTomitaAdjointPolar', 'ScalarRightConjugateGraph']
OLD_FLAGS = ['original_F_fixed_vectors_detected',
    'right_selfadjoint_vectors_dense_in_original_F_fixed_space',
    'right_pair_graph_core_equals_original_F']
FLAGS = ['original_adjoint_equals_BJ_full_domain',
    'original_adjoint_equals_JSJ_full_domain',
    'right_conjugate_graph_core_equals_original_S']
BODY = '''[REAL] O adjunto maximal F original satisfaz F=BJ=JSJ, onde B é
a raiz positiva já construída de S†S e J é seu fator polar original.
A igualdade inclui TODO o domínio: D(F)=J^-1D(B)=J^-1D(S).
O lema generic_adjoint_maximal da bancada Chatgpt (Continuous050) foi
reaproveitado: a auto-adjunção de B elimina qualquer extensão maior.
O pareamento original S/F identifica o valor, sem redefinir F ou J.

[REAL] A conjugação simultânea J×J transporta o grafo fechado original de S
no grafo original de F e vice-versa. O fecho do grafo da inscrição direita
j(a),j(a*) já era F. Como J×J é homeomorfismo, o fecho dos pares
(Jj(a),Jj(a*)) é agora o grafo original de S. A inscrição a↦Jj(a) é
conjugado-linear; não foi confundida com uma identificação de álgebras.
Isso prova densidade no grafo inteiro, não apenas densidade dos vetores.

[OPEN] Ainda falta provar JRJ pertence a π(N) para todo R em π(N)', ou
uma geração efetiva do comutante que forneça essa inclusão inversa.
F=JSJ e os grafos densos não são apresentados como prova automática
de π(N)'=Jπ(N)J. Δ^it/KMS, traço/escala/canto Three Locks, H1/H2/H3
físicos, setor interagente e consumo por certificados tipados/runtime
continuam abertos. Seis flags maiores falsas; o gate permanece igual.

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
    text = text.replace('right_graph_core', 'adjoint_polar_graph').replace('RIGHT_GRAPH_CORE', 'ADJOINT_POLAR_GRAPH')
    text = text.replace('scalar_vna_custody.json', 'right_graph_core_custody.json')
    text = text.replace('GRAPH_CORE_ADJUNTO_ORIGINAL_F', 'ADJUNTO_POLAR_GRAFOS_ORIGINAIS')
    text = text.replace('seis módulos/57 alvos', 'dois módulos/17 alvos').replace('Seis módulos/57 alvos', 'Dois módulos/17 alvos')
    text = text.replace('Graph core do adjunto original F', 'Adjunto polar e grafos originais')
    for old, new in zip(OLD_FLAGS, FLAGS):
        text = text.replace(old, new)
    text = text.replace('len(targets) == 57', 'len(targets) == 17')
    text = text.replace('len(modules) == 6', 'len(modules) == 2')
    return text.replace(repr(OLD_NAMES), repr(NAMES))

def replace_body(text):
    text, count = re.subn(r'\[REAL\] O fecho do grafo da involução.*?(?=\[REAL — fiação preservada\])',
        lambda _: BODY, text, flags=re.S)
    assert count in (1, 2), count
    return text

t = replace_body(common((ROOT / 'record_right_graph_core_draft.py').read_text(encoding='utf-8')))
t = t.replace("parent['actual_scalar_GNS_image_von_neumann']", "parent['right_pair_graph_core_equals_original_F']")
t = t.replace('Freeze the right-algebra graph core of the original maximal adjoint F.',
    'Freeze the original full-domain F=BJ=JSJ and transported graph core.')
create('record_adjoint_polar_graph_draft.py', t)

t = common((ROOT / 'prepare_right_graph_core_stage.py').read_text(encoding='utf-8'))
t = t.replace("len(draft['targets']) == 57", "len(draft['targets']) == 17")
t = t.replace('assert count == 625', 'assert count == 682')
t = t.replace("text = once(text, '== 625', '== 682')", "text = once(text, '== 682', '== 699')")
t = t.replace("'SeparatingRestrictionVonNeumann', 'ScalarGNSVonNeumann'", "'FixedVectorGraphCore', 'ScalarRightGraphCore'")
t = t.replace('TGLExt/V350ScalarGNSVonNeumann.lean', 'TGLExt/V350ScalarRightGraphCore.lean')
begin = t.index('anchor = "        \'scalarGNSVonNeumann_coe\'')
end = t.index('save(path, text)', begin)
t = t[:begin] + '''anchor = "        'scalarRightPairGraph_closure_eq_original'),\\n"
text = once(text, anchor, anchor + "    'original_adjoint_polar_graph_transport': (\\n"
    "        'scalarTomitaAdjoint_polar_domain_iff', 'scalarTomitaAdjoint_polar_value',\\n"
    "        'scalarTomitaAdjoint_conjugate_domain_iff', 'scalarTomitaAdjoint_conjugate_value',\\n"
    "        'scalarTomitaPolar_conjugates_closed_graph', 'scalarRightConjugateVector_star',\\n"
    "        'scalarRightConjugateGraph_closure_eq_original'),\\n")
''' + t[end:]
t = t.replace("'new_targets': 57", "'new_targets': 17").replace('count + 57', 'count + 17')
create('prepare_adjoint_polar_graph_stage.py', t)

t = replace_body(common((ROOT / 'record_right_graph_core_progress.py').read_text(encoding='utf-8')))
t = t.replace('Record the reviewed original-F graph core with exact-byte memory lineage.',
    'Record the reviewed original adjoint/polar graph identities and byte lineage.')
create('record_adjoint_polar_graph_progress.py', t)
create('verify_adjoint_polar_graph_custody.py', common((ROOT / 'verify_right_graph_core_custody.py').read_text(encoding='utf-8')))
print('Created two-module/17-target scripts. No integration or memory writes executed.')
