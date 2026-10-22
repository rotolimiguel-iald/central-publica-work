from pathlib import Path
import os
R=Path(__file__).resolve().parent
s=(R/'prepare_perturbed_norm_fiche.py').read_text(encoding='utf8')
s=s.replace("pat='scalarRightAction_weight_norm|scalarPerturbedWeight|inverseCutoffPerturbedWeight|scalarWeight.*sandwich.*norm'", "pat='scalarInverseCutoffWeight|scalarInverseLimitWeight|peso.{0,20}limite.{0,20}(normal|aditiv)|cutoff.{0,20}weight.{0,20}normal'")
s=s.replace('search_perturbed_weight_norm','search_limit_weight')
a=s.index('specs=[');b=s.index('\nproviders=[]',a)
s=s[:a]+"""specs=[('TGLExt/V351RegulatorWeightOrder.lean','scalarWeight_inverseCutoff_antitone'),('TGLExt/V350DualWeightForm.lean','dualQuadraticIntegral_zero'),('TGLExt/V350DualWeightForm.lean','dualQuadraticIntegral_add'),('TGLExt/V350DualQuadraticLaws.lean','dualQuadraticIntegral_smul_operator'),('TGLExt/V350DualFormFaithfulness.lean','dualQuadraticIntegral_mono'),('TGLExt/V350DualFormNormality.lean','dualQuadraticIntegral_of_monotone_strong_limit'),('TGLExt/V350RegularNormality.lean','vonNeumann_exists_positive_isLUB'),('TGLExt/V350DualFixedWeightLaws.lean','PositiveCoreInput.conjugate'),('TGLExt/V350ScalarDualWeight.lean','positive_internal_isLUB_nonneg')]
"""+s[b:]
s=s.replace("('TGLExt/V350ScalarDualWeight.lean','positive_internal_isLUB_nonneg')","('TGLExt/V350DualFixedWeightLaws.lean','positive_internal_isLUB_nonneg')")
a=s.index("target='");b=s.index('\nstamp=',a)
target='Define scalarInverseCutoffWeight P epsilon on the EXISTING PositiveCoreInput as nu(star sqrt(B_epsilon) X sqrt(B_epsilon)). Prove zero, addition, NNReal homogeneity, input monotonicity and normality for internal positive directed suprema, using the old strong operator limit and old normality of dualQuadraticIntegral. Read scalarWeight_inverseCutoff_antitone as regulator order, and prove the natural-number sequence epsilon_n=1/(n+1) gives monotone weights. Define scalarInverseLimitWeight as that SAME sequence supremum; prove zero/add/homogeneous/monotone/normal and domination of each sequence cutoff. All values ENNReal, no finiteness premise. No separate GNS, trace structure inhabitant, final semifinitude, faithfulness, traciality or dual scaling claimed by these laws. Explicit two definitions are consumers of already constructed cutoffs and of the final RegularCoreTraceData value field. Existing PositiveCoreInput.conjugate is NOT usable directly: requires dualFixedCore; use raw integral laws without asserting that cuts are theta-fixed.'
s=s[:a]+'target='+repr(target)+'\n'+s[b:]
s=s.replace('OPEN__FICHE_BEFORE_PERTURBED_WEIGHT_NORM','OPEN__FICHE_BEFORE_LIMIT_WEIGHT_LAWS').replace('REAPROVEITAMENTO_A1B_PESO_PERTURBADO_NORMA','REAPROVEITAMENTO_A1B_LEIS_PESO_LIMITE')
a=s.index("s='[OPEN —");b=s.index('for q in providers:',a)
s=s[:a]+"""s='[OPEN — ficha anterior às leis do peso limite]\\n\\n# A1(b): o peso limite pelos cortes já construídos\\n\\n'+stamp+'\\n\\n'+target+'\\n\\nADAPTAR: leis integrais e supremos existentes; não criar outro espaço de estados. A normalidade do sanduíche segue por limite forte de redes positivas, não por presumir que uma conjugação não invertível preserva qualquer supremo. Fornecedores ENNReal serão registrados em adendo antes do alvo.\\n\\n'
"""+s[b:]
p=R/'prepare_limit_weight_fiche.py';assert not p.exists();b=s.encode('utf8');t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
