from pathlib import Path
import os
R=Path(__file__).resolve().parent
s=(R/'prepare_perturbed_norm_fiche.py').read_text(encoding='utf8')
s=s.replace("pat='scalarRightAction_weight_norm|scalarPerturbedWeight|inverseCutoffPerturbedWeight|scalarWeight.*sandwich.*norm'","pat='scalarWeight.*perturbed.*mono|scalarWeight.*right.*order|perturb.*(monoton|order)|right.*square.*(order|mono)'")
s=s.replace('search_perturbed_weight_norm','search_perturbed_weight_order')
start=s.index('specs=[');end=s.index('\nproviders=[]',start)
s=s[:start]+"""specs=[('TGLExt/V351PerturbedWeightNorm.lean','scalarWeight_right_perturbed_norm'),('TGLExt/V351ScalarRightActionAlgebra.lean','scalarPolarRightAlgebra'),('.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Adjoint.lean','apply_norm_sq_eq_inner_adjoint_left'),('.lake/packages/mathlib/Mathlib/Algebra/Order/Star/Basic.lean','NonUnitalStarRingHom.map_le_map_of_map_star'),('TGLExt/V351InverseCutoffCFC.lean','regularInverseGeneratorCutoff_sqrt_right'),('TGLExt/V350ScalarRightAverage.lean','scalarWeight_right_average_le')]
""" + s[end:]
start=s.index("target='");end=s.index('\nstamp=',start)
target="For P, b,c in scalarPolarRightAlgebra P with b*star b <= c*star c in the same core, and A in scalarWeightLeftIdeal P, prove nu(star b*(star A*A)*b) <= nu(star c*(star A*A)*c). Consume the previously proved perturbed norm identity, positivity/order preservation of the original star representation and the adjoint quadratic-form identity. Consumer: order of inverse-generator cut perturbations. This is an order theorem on the existing square-finite domain only; no all-positive extension, no new weight, no trace. The comparison is b b* rather than b* b; selfadjoint square roots later discharge that distinction."
s=s[:start]+'target='+repr(target)+'\n'+s[end:]
s=s.replace('OPEN__FICHE_BEFORE_PERTURBED_WEIGHT_NORM','OPEN__FICHE_BEFORE_PERTURBED_WEIGHT_ORDER').replace('REAPROVEITAMENTO_A1B_PESO_PERTURBADO_NORMA','REAPROVEITAMENTO_A1B_ORDEM_PESO_PERTURBADO')
a=s.index("s='[OPEN —");b=s.index('for q in providers:',a)
s=s[:a]+"""s='[OPEN — ficha anterior ao transporte da ordem para os valores perturbados]\\n\\n# A1(b): ordem dos valores no mesmo domínio do peso\\n\\n'+stamp+'\\n\\n'+target+'\\n\\nADAPTAR: norma GNS, positividade de homomorfismos estrela e produto interno de A†A já existem. Uma ponte compõe esses fornecedores. Nenhuma nova representação ou peso.\\n\\n'
""" +s[b:]
p=R/'prepare_perturbed_order_fiche.py';assert not p.exists();b=s.encode();q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b;os.replace(q,p)

