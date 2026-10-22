from pathlib import Path
import os
R=Path(__file__).resolve().parent
s=(R/'prepare_perturbed_norm_fiche.py').read_text(encoding='utf8')
s=s.replace("pat='scalarRightAction_weight_norm|scalarPerturbedWeight|inverseCutoffPerturbedWeight|scalarWeight.*sandwich.*norm'","pat='scalarWeight_square_eq_iSup_averages|scalarWeight.{0,60}(recover|Fatou|exhaustion)|(Fatou|fatou).{0,120}(peso|weight|regular)'")
s=s.replace('search_perturbed_weight_norm','search_weight_average_recovery')
start=s.index('specs=[');end=s.index('\nproviders=[]',start)
s=s[:start]+"""specs=[('TGLExt/V350ScalarRightAverage.lean','scalarWeight_right_average_le'),('TGLExt/V350ScalarRightAverage.lean','scalarOrbit_right_average_tendsto'),('TGLExt/V350DualSemifiniteIdeal.lean','regularAverage_hasFiniteDualSquare'),('TGLExt/V350DualSemifiniteIdeal.lean','HasFiniteDualSquare.left_mul'),('TGLExt/V350DualWeightForm.lean','dualQuadraticIntegral'),('TGLExt/V350DualWeightForm.lean','dualQuadraticIntegrand_measurable'),('TGLExt/V350RegularFiniteWeight.lean','dualQuadraticIntegrand_star_mul'),('.lake/packages/mathlib/Mathlib/MeasureTheory/Integral/Lebesgue/Add.lean','lintegral_liminf_le'),('.lake/packages/mathlib/Mathlib/Analysis/SpecificLimits/Basic.lean','tendsto_one_div_add_atTop_nhds_zero_nat')]
""" +s[end:]
start=s.index("target='");end=s.index('\nstamp=',start)
target="For EVERY A in regularCoreAlgebra P, prove nu(A*A)=iSup_n nu((A e_n)*(A e_n)), e_n=regularAverage P (1/(n+1)). No finite-weight hypothesis on A; values may be infinity. Consume pointwise orbit convergence and the existing upper bound under right averages, via Fatou for a SEQUENCE atTop. No monotonicity of e_n or of its squares asserted. A e_n is already uniformly square-finite by existing ideal lemmas. Consumer: extend the cut-weight order from square-finite inputs to all positive inputs, after proving commutation of cuts with the SAME averages. This does not claim finite positive minorants or normal-weight semifiniteness in that stronger sense."
s=s[:start]+'target='+repr(target)+'\n'+s[end:]
s=s.replace('OPEN__FICHE_BEFORE_PERTURBED_WEIGHT_NORM','OPEN__FICHE_BEFORE_WEIGHT_AVERAGE_RECOVERY').replace('REAPROVEITAMENTO_A1B_PESO_PERTURBADO_NORMA','REAPROVEITAMENTO_A1B_RECUPERACAO_PELAS_MEDIAS')
a=s.index("s='[OPEN —");b=s.index('for q in providers:',a)
s=s[:a]+"""s='[OPEN — ficha anterior à recuperação de valores estendidos por médias]\\n\\n# A1(b): recuperar todos os valores sem supor minorantes finitos\\n\\n'+stamp+'\\n\\n'+target+'\\n\\nADAPTAR: limite pontual e cota já pagos, compostos com Fatou. Reutilizar a família regularAverage, sem novo regularizador ou novo peso. Consulta independente TODOS_POSITIVOS é roteiro, não prova.\\n\\n'
""" +s[b:]
p=R/'prepare_average_recovery_fiche.py';assert not p.exists();b=s.encode();t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)

