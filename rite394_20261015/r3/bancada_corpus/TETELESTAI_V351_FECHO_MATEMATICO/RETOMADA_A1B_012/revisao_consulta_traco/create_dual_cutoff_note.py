from pathlib import Path
import json, hashlib, os
from datetime import datetime

R=Path(__file__).resolve().parents[1]
out=Path(__file__).parent
def pin(p):
    b=p.read_bytes()
    return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def fresh(p,b):
    assert not p.exists(),p
    t=p.with_name(p.name+'.tmp')
    with t.open('xb') as f:f.write(b)
    assert t.read_bytes()==b
    os.replace(t,p)
providers=[
 ('V351RegularGeneratorDualScaling.lean','regularPositiveGenerator_dual_scaling'),
 ('V350RegularDualAction.lean','regularDualAction'),
 ('V350RegularDualAction.lean','dualAmbient_add'),
 ('V350RegularDualAction.lean','regularDualAction_apply'),
 ('V350ResolventGraph.lean','resolvent_graph_resolvent_equation'),
 ('V351RegularPositiveGraph.lean','regularSpectralResolvent_nonneg'),
 ('V351RegularPositiveGraph.lean','regularSpectralResolvent_le_one'),
 ('V351RegularGeneratorAffiliation.lean','regularSpectralResolvent_mem')]
records=[]
for name,decl in providers:
    p=R/'v/TGLExt'/name
    lines=p.read_text(encoding='utf8').splitlines()
    hits=[i+1 for i,l in enumerate(lines) if l.startswith(('def '+decl+' ', 'theorem '+decl+' '))]
    assert len(hits)==1,(decl,hits)
    records.append(dict(declaration=decl,line=hits[0],source=pin(p)))
text='''# Consulta — cortes do mesmo h por escala dual

[DERIVED — consulta, não novo Lean] A proposta do agente principal é correta para ε>0 e é mais econômica, nesta etapa, que reconstruir o corte por uma função racional no CFC. Fixe h=regularPositiveGenerator P, R=regularSpectralResolvent P, C_s=characterMultiplier s e θ_s=dualAmbient s. O delta7 prova hC_s=e^s C_sh em domínio completo, equivalentemente Ad(C_s)h=e^(−s)h.

Defina Bε=ε⁻¹ θ_(log ε)(R). Como θ preserva a álgebra N e 0≤R≤I, obtém-se Bε∈N e 0≤Bε≤ε⁻¹I; logo Bε é limitado, com norma ≤ε⁻¹. Não é preciso supor h com inversa limitada, gap ou domínio total, nem CompleteSpace do subtipo N. A positividade é a ordem usual dos operadores no Hilbert.

Prova exata de que este operador é (h+ε)⁻¹, sem usar esse nome como hipótese: dado u, ponha t=log ε e z=C_(-t)u. A equação já compilada do resolvente dá (Rz,z−Rz)∈graph(h). Transporte por C_t, usando exp(log ε)=ε, e divida AS DUAS componentes por ε. Resulta

    (Bεu, u−εBεu) ∈ graph(h).

Assim (h+ε)Bε=I, com Bεu no domínio efetivo. Para a recíproca, h+ε é injetivo: se hx+εx=0, a positividade de h dá 0≤Re⟨x,hx⟩=−ε‖x‖², portanto x=0. Essa unicidade implica Bε(hx+εx)=x para TODO x∈D(h). Paga-se a igualdade do grafo do inverso, não apenas uma identidade em um núcleo denso.

A composição da ação dual fornece diretamente

    θ_s(Bε)=ε⁻¹θ_(s+log ε)(R)=e^s B_(εe^s).

Os sinais estão coerentes: h escala por e^(−s), o inverso regularizado por e^s e o parâmetro por εe^s. A identidade exige ε>0; não se pode aplicar exp(log ε)=ε em ε=0. No código, dualAmbient_add usa StarAlgEquiv.trans, cuja ordem de avaliação deve ser respeitada; a soma real permite trocar s e log ε sem assumir comutação arbitrária de operadores.

[DERIVED — próximo consumidor] A família de cortes pode, portanto, ser construída agora usando apenas escala dual, ordem e o resolvente existente. Para compará-los, a equação dos inversos também dá Bε−Bδ=(δ−ε)BεBδ e comutação dos dois cortes; para 0<ε≤δ isso dá Bδ≤Bε. São lemas algébricos de resolvente ainda a formalizar, não novos objetos espectrais.

[OPEN — limite PT] Isto constrói os cortes limitados e sua escala. Não demonstra a ordem de ν(Bε^(1/2) A Bε^(1/2)) para todo A≥0 apenas pela ordem Bδ≤Bε: sanduíches não preservam essa comparação não comutativa. Continua necessária a lei específica de perturbação no centralizador (ou prova direta equivalente), a definição/limite do peso perturbado e a tracialidade. A raiz limitada, se usada, reaproveita a infraestrutura existente; não precisa ser reconstruída para provar o corte. Não se cobra novamente semifinitude de ν por minorantes positivos. A consulta anterior sobre PT permanece distinta e não foi editada.

[REAL — limites de execução] Somente leitura de fornecedores e escrita desta nota/JSON; nenhum novo Lean, build, objeto, memória ou alteração de parecer selado. Esta consulta não agrega alvos ao aceite separado da escala dual7.

Fornecedores relidos e pins medidos:

'''
for rec in records:
    p=rec['source']
    text+=f"- `{rec['declaration']}` — [{Path(p['path']).name}](<{p['path']}:{rec['line']}>) — SHA256 `{p['sha256']}`.\n"
text+='\nData: '+datetime.now().astimezone().isoformat()+'.\n'
p=out/'CONSULTA_CORTES_POR_ESCALA_DUAL.md'
fresh(p,text.encode('utf8'))
data=dict(status='DERIVED_CONSULTATION__NOT_LEAN_ACCEPTANCE__TRACE_OPEN',
    note=pin(p),sourcepins=records,prior_consultation=pin(out/'CONSULTA_PERTURBACAO_TRACIALIDADE.md'),
    scale_review=pin(R/'revisao_escala_dual/REVIEW_A1_REGULAR_DUAL_SCALING_FINAL.md'),
    new_theorems=0,compilation_executed=False,original_files_modified=False)
fresh(out/'CONSULTA_CORTES_POR_ESCALA_DUAL.json',json.dumps(data,ensure_ascii=False,indent=2).encode('utf8'))
print(json.dumps(dict(note=pin(p),json=pin(out/'CONSULTA_CORTES_POR_ESCALA_DUAL.json')),ensure_ascii=False))
