from pathlib import Path
import os
R=Path(__file__).resolve().parent
s=(R/'prepare_perturbed_norm_fiche.py').read_text(encoding='utf8')
s=s.replace("pat='scalarRightAction_weight_norm|scalarPerturbedWeight|inverseCutoffPerturbedWeight|scalarWeight.*sandwich.*norm'", "pat='scalarWeight_right_perturbed_mono_all|perturbed.{0,35}(all_positive|all_squares)|peso.{0,35}perturbado.{0,25}todos'")
s=s.replace('search_perturbed_weight_norm','search_all_positive_weight_order')
start=s.index('specs=[');end=s.index('\nproviders=[]',start)
s=s[:start]+"""specs=[('TGLExt/V351PerturbedWeightOrder.lean','scalarWeight_right_perturbed_mono'),('TGLExt/V351WeightAverageRecovery.lean','scalarWeight_square_eq_iSup_averages'),('TGLExt/V350ScalarDualWeight.lean','scalarDualWeight_square_finite_strong_density'),('TGLExt/V351CutoffAverageCommutation.lean','regularInverseCutoffSqrt_commutes_average'),('TGLExt/V351InverseCutoffCFC.lean','regularInverseGeneratorCutoff_sqrt_right'),('TGLExt/V350AntiunitaryPositiveConjugation.lean','hilbertPositiveSqrt'),('TGLExt/V351ScalarRightActionAlgebra.lean','scalarRightAction_cfc')]
"""+s[end:]
start=s.index("target='");end=s.index('\nstamp=',start)
target='Extend scalarWeight_right_perturbed_mono from A in n_nu to EVERY A in N, using exact average recovery for A*b and A*c, finite averages A*e_n, and explicit hypotheses that b and c commute with the SAME regularAverage P delta. Then for EVERY positive X in the SAME N instantiate A as the EXISTING hilbertPositiveSqrt(X), proving its membership in N by norm closure and existing real CFC membership, and A*A=X by existing sqrt identity. Keep b b* <= c c*, membership in scalarPolarRightAlgebra and average commutation explicit. No new definition of weight, root, GNS, core or regularizer. The actual cutoff roots discharge those hypotheses via existing suppliers; regulator-order B_epsilon <= B_eta itself is a separate consumer/obligation. Infinite values allowed. This does not prove traciality, final semifinitude, or completion of A1(b).'
s=s[:start]+'target='+repr(target)+'\n'+s[end:]
s=s.replace('OPEN__FICHE_BEFORE_PERTURBED_WEIGHT_NORM','OPEN__FICHE_BEFORE_ALL_POSITIVE_WEIGHT_ORDER').replace('REAPROVEITAMENTO_A1B_PESO_PERTURBADO_NORMA','REAPROVEITAMENTO_A1B_ORDEM_TODOS_POSITIVOS')
a=s.index("s='[OPEN —");b=s.index('for q in providers:',a)
s=s[:a]+"""s='[OPEN — ficha anterior à extensão de ordem]\\n\\n# A1(b): ordem em todos os positivos do mesmo core\\n\\n'+stamp+'\\n\\n'+target+'\\n\\nADAPTAR: compor os três fornecedores já provados; não criar outro ideal ou peso. A aproximação é dos VALORES e não de minorantes positivos. Reusar CFC.sqrt_eq_real_sqrt, cfcₙ_mem e CFC.sqrt_mul_sqrt_self para o mesmo wrapper de raiz. O adendo dos fornecedores mathlib será anexado antes do alvo.\\n\\n'
"""+s[b:]
p=R/'prepare_all_positive_weight_order_fiche.py';assert not p.exists()
b=s.encode('utf8');t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
