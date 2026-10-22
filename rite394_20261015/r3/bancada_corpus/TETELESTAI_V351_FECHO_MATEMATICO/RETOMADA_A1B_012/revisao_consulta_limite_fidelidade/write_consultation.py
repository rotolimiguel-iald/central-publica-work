from pathlib import Path
from datetime import datetime
import json,hashlib,os
R=Path(r'C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012');V=R/'v';O=R/'revisao_consulta_limite_fidelidade';O.mkdir(exist_ok=True)
def pin(p):
 b=p.read_bytes();return dict(path=str(p),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def fresh(p,b):
 assert p.resolve().is_relative_to(O.resolve()) and not p.exists()
 t=p.with_name(p.name+'.tmp')
 with t.open('xb') as f:f.write(b)
 assert t.read_bytes()==b;os.replace(t,p)
def link(f,line,label):
 return '['+label+'](<'+str(V/f).replace('\\','/')+':'+str(line)+'>)'
specs=[
('TGLExt/V350ScalarDualWeightFaithfulness.lean',[(54,57)]),
('TGLExt/V350ScalarDualWeight.lean',[(15,16),(36,42)]),
('TGLExt/V351InverseGeneratorCutoff.lean',[(13,29),(43,46),(81,95),(99,102)]),
('TGLExt/V351RegularPositiveGraph.lean',[(84,87),(98,102)]),
('TGLExt/BoundedGraphOperator.lean',[(117,128)]),
('TGLExt/V351ResolventImaginaryPowers.lean',[(19,23)]),
('TGLExt/V350DualWeightForm.lean',[(87,95)]),
('TGLExt/V350RegularDualAction.lean',[(18,24),(42,48),(76,86)]),
('TGLExt/V350DualWeightCuts.lean',[(40,44)]),
('TGLExt/V350DualQuadraticLaws.lean',[(61,66)]),
('TGLExt/V351RegulatorWeightOrder.lean',[(66,90)]),
('TGLExt/V351InverseCutoffCFC.lean',[(125,135)]),
('.lake/packages/mathlib/Mathlib/Analysis/SpecialFunctions/ContinuousFunctionalCalculus/Rpow/Basic.lean',[(265,266),(283,296)]),
('.lake/packages/mathlib/Mathlib/Algebra/Order/Archimedean/Basic.lean',[(211,218)]),
('.lake/packages/mathlib/Mathlib/Data/ENNReal/Inv.lean',[(805,819)]),
('.lake/packages/mathlib/Mathlib/Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Unique.lean',[(450,464)])]
records=[]
for f,ranges in specs:
 p=V/f;ls=p.read_text(encoding='utf-8-sig').splitlines()
 records.append(dict(source=pin(p),excerpts=[dict(start=a,end=min(b,len(ls)),text='\n'.join(ls[a-1:b])) for a,b in ranges]))
math='.lake/packages/mathlib/Mathlib/'
date=datetime.now().astimezone().isoformat()
md=f"""# Consulta — fidelidade e escala dual do limite
{date}

[DERIVED — proposta, não prova Lean nova] Use Wε(X)=ν(Sε* X Sε), Sε=hilbertPositiveSqrt(Bε), δn=1/(n+1), τ(X)=sup_n Wδn(X). É notação matemática para o candidato descrito; **não li V351InverseLimitWeight em DEV**. Os alvos sugeridos abaixo ainda não estão certificados nesta consulta.

**Fidelidade: basta n=0.** Se τ(X)=0, então W1(X)=0 por le_iSup. O fornecedor {link('TGLExt/V351InverseGeneratorCutoff.lean',43,'regularInverseGeneratorCutoff_one')} dá B1=R. A raiz S=√R pertence ao mesmo core pelo fornecedor já pago de raízes dos cortes; S*XS é positivo. Aplicar {link('TGLExt/V350ScalarDualWeightFaithfulness.lean',54,'dualQuadraticIntegral_vacuum_faithful')} dá SXS=0, usando S*=S.

É possível **evitar até um novo lema de imagem densa/injetividade da raiz**: como S²=R, multiplicar a igualdade por S dos dois lados dá RXR=0. {link('TGLExt/V351RegularPositiveGraph.lean',98,'regularSpectralResolvent_injective')} dá XR=0. A imagem de R é densa pela auto-adjunção de R≥0 e pelo fornecedor genérico {link('TGLExt/BoundedGraphOperator.lean',118,'ChatgptAudit.Continuous049.bounded_graph_domain_dense')} aplicado a R e 0. Atenção ao tipo literal: ele conclui densidade do domínio de boundedGraphOperator; esse domínio é range(R). A conversão já é usada em {link('TGLExt/V351ResolventImaginaryPowers.lean',20,'resolventDampingOperator_denseRange')}. Continuidade de X, ou DenseRange.induction com isClosed_eq, conclui X=0. O sentido inverso é zero do peso. Nenhuma finitude de ν(X), gap ou inversa limitada foi usada. graph_iff também permitiria investigar injetividade de cada Bε, mas isso excede o necessário para esta fidelidade.

**Raiz dual: a unicidade positiva pode ser menor que um adaptador mapCFC.** Já existe
θ_s(Bε)=exp(s) B_(ε exp(s)).
Com κ=√exp(s)>0, os operadores θ_s(Sε) e κ S_(ε exp(s)) são positivos e têm o mesmo quadrado. Usar {link('TGLExt/V350DualWeightCuts.lean',40,'dualAmbient_nonneg')}, map_mul, Sε²=Bε e Real.sq_sqrt; {link(math+'Analysis/SpecialFunctions/ContinuousFunctionalCalculus/Rpow/Basic.lean',294,'CFC.mul_self_eq_mul_self_iff')} conclui:
θ_s(Sε)=√exp(s) • S_(ε exp(s)).
Também serve CFC.sqrt_unique (:283). Fixar instâncias numa Hilbert genérica e especializar o wrapper antigo evita repetir sua construção. Se optar por mapCFC, {link(math+'Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Unique.lean',461,'StarAlgHomClass.map_cfc')} exige continuidade do homomorfismo e os predicados CFC; dualAmbient é a equivalência estrela por conjugação unitária. Essa alternativa não é necessária para a igualdade pela unicidade.

**Sinal da escala: exp(−s).** O fornecedor certo de νθ=ν é {link('TGLExt/V350DualWeightForm.lean',87,'dualQuadraticIntegral_dual_invariant')}, válido para todo A e vetor. Não o confundir com invariância por regularUnitary, que é outra ação.

Transportar o sanduíche inteiro por θ_(−s), usando θ_(−s)θ_s=id e a raiz transportada, fornece exatamente
Wε(θ_s X) = ofReal(exp(−s)) · W_(ε exp(−s))(X).
O coeficiente quadrático usa {link('TGLExt/V350DualQuadraticLaws.lean',61,'dualQuadraticIntegral_smul_operator')}; √exp(−s) aparece duas vezes. A identidade equivalente de transporte simultâneo é Wε(X)=ofReal(exp(s)) W_(ε exp(s))(θ_s X). O fator positivo finito preserva o caso ∞. A ação sobre PositiveCoreInput deve manter o mesmo operador θ_s(X.val), com pertença via regularDualAction e positividade via dualAmbient_nonneg; nenhum novo cone ou GNS.

**Cofinalidade: duas desigualdades de supremo bastam.** Para r>0, provar sup_n W_(r δn)(X)=sup_n Wδn(X). O fornecedor {link('TGLExt/V351RegulatorWeightOrder.lean',66,'scalarWeight_inverseCutoff_antitone')} fornece a direção de comparação. Para cada n, escolher m com δm<rδn dá W_(rδn)≤Wδm; para a volta escolher m com δm<δn/r dá Wδn≤W_(rδm). Ambas escolhas vêm diretamente de {link(math+'Algebra/Order/Archimedean/Basic.lean',213,'exists_nat_one_div_lt')}. Aplicar iSup_le/le_iSup_of_le. Isso evita construir uma reindexação por bijeção, provar continuidade em ε ou usar atBot de ℝ (que significaria −∞, não 0 pela direita). {link(math+'Data/ENNReal/Inv.lean',807,'ENNReal.mul_iSup')} transporta o fator, sem hipótese de supremum finito.

Alvos propostos, nomes apenas sugestivos [DERIVED]:

1. inverseLimitWeight_faithful: τ(X)=0 ↔ X=0, X:PositiveCoreInput P.
2. regularInverseCutoffSqrt_dual: θ_s Sε=√exp(s) • S_(ε exp(s)), ε>0, s real.
3. inverseCutoffWeight_dual: Wε(θ_s X)=ofReal(exp(−s))·W_(ε exp(−s))(X).
4. inverseLimitWeight_scaled_sequence: para r>0, sup_n W_(rδn)(X)=τ(X).
5. inverseLimitWeight_dual: τ(θ_s X)=ofReal(exp(−s))·τ(X).

[OPEN] Fidelidade e escala dual do candidato ainda precisam dessas ligações compiladas. Nenhuma delas, isolada ou conjuntamente, demonstra tracialidade ou semifinitude de τ. Sem minorantes positivos finitos de ν, novo GNS, nova realização espectral ou antecipação do review22.

[REAL — alcance] Consulta local delimitada; fontes e APIs acima lidas, pins e excertos no JSON. Os objetos próprios dos deltas20/21 e relatórios entregues foram apenas referenciados. Nenhuma compilação, execução de monólito/recorder, alteração de fonte autoral ou memória. Aguardarei o congelamento para a revisão formal.
"""
base=[]
for d in ['revisao_ordem_todos_positivos','revisao_ordem_reguladores']:
 p=R/d/'compilation.json';j=json.loads(p.read_bytes());assert j['all_axioms_allowed'] and not j['P0'] and not j['P1'] and not j['P2'];base.append(pin(p))
fresh(O/'CONSULTA_LIMITE_FIDELIDADE.md',md.encode('utf-8'))
data=dict(timestamp=date,status='CONSULTA_DERIVED__CANDIDATE_DEV_NOT_INSPECTED',notation={'delta_n':'1/(n+1)','S_epsilon':'existing hilbertPositiveSqrt(regularInverseGeneratorCutoff P epsilon)','W_epsilon':'nu(star S_epsilon * X * S_epsilon)','tau':'sup_n W_delta_n'},recommended_faithfulness='use only n=0, B1=R, sandwich multiply to RXR=0, R injective and dense',dual_scaling_sign='tau(theta_s X) = ENNReal.ofReal(exp(-s)) * tau(X)',proposed_targets=[dict(name='inverseLimitWeight_faithful',statement='tau(X)=0 iff X=0'),dict(name='regularInverseCutoffSqrt_dual',statement='theta_s S_epsilon = sqrt(exp(s)) smul S_(epsilon exp(s)); epsilon>0'),dict(name='inverseCutoffWeight_dual',statement='W_epsilon(theta_s X)=ofReal(exp(-s))*W_(epsilon exp(-s))(X); epsilon>0'),dict(name='inverseLimitWeight_scaled_sequence',statement='sup_n W_(r/(n+1))(X)=tau(X); r>0'),dict(name='inverseLimitWeight_dual',statement='tau(theta_s X)=ofReal(exp(-s))*tau(X)')],supplier_records=records,prior_compilations_read_only=base,report=pin(O/'CONSULTA_LIMITE_FIDELIDADE.md'),new_lean_theorems=0,compilation_executed=False,candidate_dev_read=False,author_source_modified=False,memory_modified=False,search_exhaustive=False,trace_open=True,limit_weight_semifiniteness_open=True)
fresh(O/'CONSULTA_LIMITE_FIDELIDADE.json',(json.dumps(data,ensure_ascii=False,indent=2)+'\n').encode('utf-8'))
print(json.dumps(dict(report=data['report'],json=pin(O/'CONSULTA_LIMITE_FIDELIDADE.json')),ensure_ascii=False))

