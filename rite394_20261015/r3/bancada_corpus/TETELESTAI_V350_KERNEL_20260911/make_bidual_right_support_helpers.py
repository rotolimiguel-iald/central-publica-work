"""Prepare scripts for original biduality and right-pair functional stability."""
import ast
from pathlib import Path
import re
ROOT=Path(__file__).resolve().parent
NAMES=['ScalarTomitaBidual','ScalarRightFunctionalStability']
BODY="""[REAL] O adjunto maximal de F é exatamente o S ORIGINAL, incluindo todo
seu domínio. O pareamento contra D(F) é equivalente à pertinência ao grafo de
S. A prova usa a conjugação polar J já construída, F=JSJ e a maximalidade de
F; não redefine S/F/J nem pressupõe a inclusão inversa dos comutantes.

[REAL] Se a=a* é um par direito e T=T* pertence ao comutante inteiro,
comutando com a, então Ta é um par direito auto-adjunto com inscrição
j(Ta)=Tj(a). T não precisa previamente pertencer à álgebra dos pares direitos.
A construção exibe os dois vetores do par e as duas leis de multiplicação.
Para qualquer par direito R, sua inscrição pertence ao fecho normado de Ran R,
provado pelas médias regulares no ideal do peso original. Não se supõe uma
cota uniforme para os vetores GNS dessas médias.

[OPEN] Os lemas preparam cortes racionais e a aproximação por combinações de
quadrados, mas não provam ainda que esses quadrados sejam núcleo de grafo
para F. Tampouco colocam automaticamente o par ponderado no domínio de S.
Faltam essa aproximação, o teste ponderado, a cota inferior uniforme do bloco
A e o multiplicador limitado. Inclusão inversa pelo J original, Delta^it/KMS,
traço/escala/canto Three Locks, H1/H2/H3 físicos, setor interagente e consumo
por certificados/runtime continuam abertos. Seis flags maiores falsas.

"""
OLD=['real_phase_variational_solution_unique','original_S_phase_variational_constructed','original_S_graph_variational_identity']
NEW=['original_S_is_maximal_adjoint_of_F','selfadjoint_right_pairs_stable_under_commuting_multipliers','right_pair_vectors_in_multiplier_range_closure']
def common(t):
 t=t.replace('phase_variational','bidual_right_support').replace('PHASE_VARIATIONAL','BIDUAL_RIGHT_SUPPORT')
 t=t.replace('adjoint_polar_graph_custody.json','phase_variational_custody.json')
 t=t.replace('SELECAO_VARIACIONAL_GRAFO_ORIGINAL','BIDUAL_SUPORTE_DIREITO')
 t=t.replace('Seleção variacional e grafo original','Bidual original e suporte direito')
 t=t.replace("['RealPhaseVariational', 'ScalarPhaseVariational']",repr(NAMES))
 t=t.replace('21 alvos','9 alvos').replace('len(targets) == 21','len(targets) == 9')
 for a,b in zip(OLD,NEW):t=t.replace(a.replace('phase_variational','bidual_right_support'),b)
 return t

def body(t):
 t,n=re.subn(r'\[REAL\] Para qualquer subespaço real fechado.*?(?=\[REAL — fiação preservada\])',lambda _:BODY,t,flags=re.S)
 assert n in (1,2),n
 return t

def create(name,t):
 ast.parse(t);p=ROOT/name;assert not p.exists();raw=t.encode('utf-8');q=p.with_suffix('.py.tmp');q.write_bytes(raw);assert q.read_bytes()==raw;q.replace(p)

t=body(common((ROOT/'record_phase_variational_draft.py').read_text(encoding='utf-8')))
t=t.replace("parent['right_conjugate_graph_core_equals_original_S']","parent['original_S_graph_variational_identity']")
create('record_bidual_right_support_draft.py',t)
t=common((ROOT/'prepare_phase_variational_stage.py').read_text(encoding='utf-8'))
t=t.replace("len(draft['targets']) == 21","len(draft['targets']) == 9")
t=t.replace('assert count == 699','assert count == 720')
t=t.replace("text = once(text, '== 699', '== 720')","text = once(text, '== 720', '== 729')")
t=t.replace("'ScalarTomitaAdjointPolar', 'ScalarRightConjugateGraph'","'RealPhaseVariational', 'ScalarPhaseVariational'")
t=t.replace('TGLExt/V350ScalarRightConjugateGraph.lean','TGLExt/V350ScalarPhaseVariational.lean')
b=t.index('anchor = "        \'scalarRightConjugateGraph_closure_eq_original\'');e=t.index('save(path, text)',b)
t=t[:b]+"""anchor = "        'scalarPhaseVariational_graph_equation'),\\n"
text = once(text, anchor, anchor + "    'original_bidual_and_right_support': (\\n"
    "        'scalarClosedTomita_bidual_maximal', 'scalarClosedTomita_bidual_graph_iff',\\n"
    "        'scalarSelfadjointRightMultiplier_star', 'scalarSelfadjointRightMultiplier_vector',\\n"
    "        'scalarRightPairVector_mem_range_closure'),\\n")
"""+t[e:]
t=t.replace("'new_targets': 21","'new_targets': 9").replace('count + 21','count + 9')
create('prepare_bidual_right_support_stage.py',t)
create('record_bidual_right_support_progress.py',body(common((ROOT/'record_phase_variational_progress.py').read_text(encoding='utf-8'))))
create('verify_bidual_right_support_custody.py',common((ROOT/'verify_phase_variational_custody.py').read_text(encoding='utf-8')))
print('Created 2-module/9-target stage scripts, no integration or memory changes.')
