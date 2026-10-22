"""Prepare stage scripts for variational selection on the original Fix S."""
import ast
from pathlib import Path
import re
ROOT = Path(__file__).resolve().parent
NAMES = ['RealPhaseVariational', 'ScalarPhaseVariational']
BODY = """[REAL] Para qualquer subespaço real fechado K de um Hilbert complexo e
Re(lambda)>0, a forma B_lambda(u,v)=Re(lambda< u,v >) é limitada e coerciva.
Lax-Milgram constrói uma solução real-linear contínua, única, com
Re(lambda)||eta||<=||xi||. Não se supõe simetria da forma. Em lambda=1,
a solução é a projeção ortogonal real. A cota é do VETOR, não do multiplicador.

[REAL] A construção foi instanciada no Fix S ORIGINAL sobre o Hilbert escalar
original. eta pertence ao domínio original de S e S eta=eta. Para xi em
Fix F original, o pareamento adjunto S/F e a decomposição do domínio de S
estendem a equação real à identidade complexa em TODO o grafo original:
2<xi,S u> = lambda<eta,S u> + conjugate(lambda)<u,eta>.
Foram reutilizados o subespaço padrão e a decomposição da bancada Chatgpt;
não foi escolhido outro S, F, J ou espaço de representação.

[OPEN] A identidade do grafo exige u em D(S). Ainda falta provar essa condição
para os pares ponderados da projeção do gráfico de multiplicação da álgebra
direita. Depois é preciso obter a cota inferior uniforme do bloco A e construir
o multiplicador limitado. A proposta de parte positiva por CFC consta da
consulta RVD56, com estatuto DERIVED, ainda não compilada. Seleção variacional
não prova por si só a inclusão inversa JRJ em pi(N). Fluxo Delta^it/KMS,
traço/escala/canto Three Locks, H1/H2/H3 físicos, setor interagente e consumo
por certificados tipados/runtime continuam abertos. Seis flags maiores falsas.

"""
OLD_FLAGS = ['original_adjoint_equals_BJ_full_domain', 'original_adjoint_equals_JSJ_full_domain',
    'right_conjugate_graph_core_equals_original_S']
FLAGS = ['real_phase_variational_solution_unique', 'original_S_phase_variational_constructed',
    'original_S_graph_variational_identity']

def common(text):
    text=text.replace('adjoint_polar_graph','phase_variational').replace('ADJOINT_POLAR_GRAPH','PHASE_VARIATIONAL')
    text=text.replace('right_graph_core_custody.json','adjoint_polar_graph_custody.json')
    text=text.replace('ADJUNTO_POLAR_GRAFOS_ORIGINAIS','SELECAO_VARIACIONAL_GRAFO_ORIGINAL')
    text=text.replace('Adjunto polar e grafos originais','Seleção variacional e grafo original')
    text=text.replace('17 alvos','21 alvos').replace('len(targets) == 17','len(targets) == 21')
    text=text.replace("['ScalarTomitaAdjointPolar', 'ScalarRightConjugateGraph']",repr(NAMES))
    for old,new in zip(OLD_FLAGS,FLAGS): text=text.replace(old,new)
    return text

def replace_body(text):
    text,n=re.subn(r'\[REAL\] O adjunto maximal F original.*?(?=\[REAL — fiação preservada\])',lambda _:BODY,text,flags=re.S)
    assert n in (1,2),n
    return text

def create(name,text):
    ast.parse(text);p=ROOT/name;assert not p.exists()
    raw=text.encode('utf-8');t=p.with_suffix('.py.tmp');t.write_bytes(raw)
    assert t.read_bytes()==raw;t.replace(p)

t=replace_body(common((ROOT/'record_adjoint_polar_graph_draft.py').read_text(encoding='utf-8')))
t=t.replace("parent['right_pair_graph_core_equals_original_F']","parent['right_conjugate_graph_core_equals_original_S']")
create('record_phase_variational_draft.py',t)
t=common((ROOT/'prepare_adjoint_polar_graph_stage.py').read_text(encoding='utf-8'))
t=t.replace("len(draft['targets']) == 17","len(draft['targets']) == 21")
t=t.replace('assert count == 682','assert count == 699')
t=t.replace("text = once(text, '== 682', '== 699')","text = once(text, '== 699', '== 720')")
t=t.replace("'FixedVectorGraphCore', 'ScalarRightGraphCore'","'ScalarTomitaAdjointPolar', 'ScalarRightConjugateGraph'")
t=t.replace('TGLExt/V350ScalarRightGraphCore.lean','TGLExt/V350ScalarRightConjugateGraph.lean')
begin=t.index('anchor = "        \'scalarRightPairGraph_closure_eq_original\'')
end=t.index('save(path, text)',begin)
t=t[:begin]+"""anchor = "        'scalarRightConjugateGraph_closure_eq_original'),\\n"
text = once(text, anchor, anchor + "    'original_phase_variational_graph': (\\n"
    "        'phaseVariationalForm_coercive', 'phaseVariationalSolution_unique',\\n"
    "        'phaseVariationalSolution_bound', 'scalarPhaseVariational_fixed',\\n"
    "        'scalarPhaseVariational_graph_equation'),\\n")
"""+t[end:]
t=t.replace("'new_targets': 17","'new_targets': 21").replace('count + 17','count + 21')
create('prepare_phase_variational_stage.py',t)
create('record_phase_variational_progress.py',replace_body(common((ROOT/'record_adjoint_polar_graph_progress.py').read_text(encoding='utf-8'))))
create('verify_phase_variational_custody.py',common((ROOT/'verify_adjoint_polar_graph_custody.py').read_text(encoding='utf-8')))
print('Created phase-variational stage scripts. No integration/memory changes.')
