from pathlib import Path
import os
R=Path(__file__).resolve().parent
def put(p,s):
    assert not p.exists() and p.is_relative_to(R)
    b=s.encode('utf8');t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
s=(R/'prepare_inverse_limit_scaling_fiche.py').read_text(encoding='utf8')
a=s.index("pat='");b=s.index('\nqueries=',a)
s=s[:a]+"pat='regularDomainCut|inverseLimitWeight_domainCut|inverseLimitWeight_square_finite|corte.{0,20}dominio.{0,20}limite'"+s[b:]
s=s.replace('search_inverse_limit_scaling','search_domain_cut')
a=s.index('specs=[');b=s.index('\nproviders=[]',a)
s=s[:a]+"""specs=[('TGLExt/V351InverseGeneratorCutoff.lean','regularInverseGeneratorCutoff_nonneg'),('TGLExt/V351InverseGeneratorCutoff.lean','regularInverseGeneratorCutoff_le'),('TGLExt/V351InverseGeneratorCutoff.lean','regularInverseGeneratorCutoff_one'),('TGLExt/V351RegulatorWeightOrder.lean','regularInverseGeneratorCutoff_commutes'),('TGLExt/V351RegulatorWeightOrder.lean','regularInverseGeneratorCutoff_resolvent_identity'),('TGLExt/V351InverseCutoffCFC.lean','regularInverseGeneratorCutoff_right'),('TGLExt/V351ScalarRightActionAlgebra.lean','scalarPolarRightAlgebra'),('TGLExt/V351RegularPositiveGraph.lean','regularSpectralResolvent_complement_injective'),('TGLExt/BoundedGraphOperator.lean','bounded_graph_domain_dense'),('.lake/packages/mathlib/Mathlib/Topology/UniformSpace/Equicontinuity.lean','Equicontinuous.isClosed_setOf_tendsto'),('TGLExt/V351PerturbedWeightOrder.lean','scalarWeight_right_perturbed_mono'),('TGLExt/V351ScalarWeightSemifiniteness.lean','scalarWeight_square_finite_wot_closure'),('TGLExt/V350RegularNormality.lean','strong_tendsto_wot'),('TGLExt/V350RegularTopology.lean','regularCore_wot_closed')]
"""+s[b:]
a=s.index("target='");b=s.index('\nstamp=',a)
target='Use q_delta=1-delta*B_delta, in the SAME regular core and polar right algebra. Prove positivity/contraction, the uniform product bound B_epsilon*q_delta^2 <= delta^(-1)*I and strong convergence q_(1/(n+1)) to I. Reuse the inverse identity, positivity of commuting products and dense range of 1-R. Consumers: finite-domain cutoff estimate of scalarInverseLimitWeight and WOT density of its square-finite set. This fiche covers that sequential route; it does not assert any new theorem or semifinal contract. No new root, spectral calculus, GNS, traciality or positive finite minorants of the original nontracial weight.'
s=s[:a]+'target='+repr(target)+'\n'+s[b:]
s=s.replace('OPEN__FICHE_BEFORE_INVERSE_LIMIT_SCALING','OPEN__FICHE_BEFORE_DOMAIN_CUT').replace('REAPROVEITAMENTO_A1B_ESCALA_PESO_LIMITE','REAPROVEITAMENTO_A1B_CORTE_DOMINIO_LIMITE')
a=s.index("s='[OPEN —");b=s.index('for q in providers:',a)
s=s[:a]+"s='[OPEN — ficha anterior ao corte de domínio do peso limite]\\n\\n# A1(b): corte algébrico sem outra raiz\\n\\n'+stamp+'\\n\\n'+target+'\\n\\nADAPTAR a rota menor q_delta da consulta independente revisao_consulta_semifinitude_limite/CONSULTA_SEMIFINITUDE_LIMITE. A cota pode depender de delta, mas deve ser uniforme em epsilon antes do supremo. Semifinitude usual e minorantes positivos do contrato são obrigações distintas.\\n\\n'\n"+s[b:]
put(R/'prepare_domain_cut_fiche.py',s)
s=(R/'dev_compile_inverse_limit_scaling.py').read_text(encoding='utf8')
for a,b in [('inverse_limit_scaling','domain_cut'),('V351InverseLimitScaling','V351RegularDomainCut'),('REAPROVEITAMENTO_A1B_ESCALA_PESO_LIMITE','REAPROVEITAMENTO_A1B_CORTE_DOMINIO_LIMITE')]:s=s.replace(a,b)
put(R/'dev_compile_domain_cut.py',s)
