from pathlib import Path
import os
R=Path(__file__).resolve().parent
s=(R/'prepare_cutoff_cfc_fiche.py').read_text(encoding='utf8')
s=s.replace("pat='regularInverseGeneratorCutoff_cfc|regularInverseGeneratorCutoff_sqrt_right|scalarRightAction_sqrt|inverseCutoffFunction'","pat='scalarRightAction_weight_norm|scalarPerturbedWeight|inverseCutoffPerturbedWeight|scalarWeight.*sandwich.*norm'")
s=s.replace('search_cutoff_cfc','search_perturbed_weight_norm').replace('REAPROVEITAMENTO_A1B_CFC_CORTES','REAPROVEITAMENTO_A1B_PESO_PERTURBADO_NORMA')
a=s.index('specs=');b=s.index('\n\n\nproviders=',a)
s=s[:a]+"""specs=[('TGLExt/V351ScalarRightActionAlgebra.lean','ScalarPolarRight'),('TGLExt/V351ScalarRightActionAlgebra.lean','scalarPolarRightAlgebra'),('TGLExt/V350ScalarWeightAction.lean','scalarWeightGNSEmbedding_norm_sq'),('TGLExt/V350AntiunitaryPositiveConjugation.lean','antiunitaryConjugate_apply'),('TGLExt/V351InverseCutoffCFC.lean','regularInverseGeneratorCutoff_sqrt_right'),('TGLExt/V350ScalarDualWeight.lean','scalarDualWeight'),('TGLExt/V350ScalarDualWeight.lean','scalarDualWeight_normal'),('TGLExt/V350DualFixedWeightLaws.lean','PositiveCoreInput.conjugate')]
""" +s[b:]
a=s.index("target='");b=s.index("\n\n\nstamp=",a)
s=s[:a]+"""target='For P, b in the same scalarPolarRightAlgebra and A in n_nu, prove dualQuadraticIntegral(star b.val*(star A.val.val*A.val.val)*b.val)(regularVacuum P) = ENNReal.ofReal(norm(scalarGNSRepresentation P (star b) ((scalarTomitaPolarFactor P).symm (scalarWeightGNSEmbedding P A)))^2). Obtain A*b membership from the already proved right identity, rewrite the GNS norm-square and use the isometry of the SAME J. Consumer: bounded cut perturbations with b=hilbertPositiveSqrt(B_epsilon), already constructed. This only gives values on squares of n_nu; do not claim it extends to all positive inputs, proves monotonicity in epsilon, or gives a trace. PositiveCoreInput.conjugate is only a pattern because it requires b in dualFixedCore, whereas our cut lies in regularCoreAlgebra; do not pass it by homonym or claim theta-fixity.'
""" +s[b:]
s=s.replace('OPEN__FICHE_BEFORE_EXISTING_CUTOFF_CFC','OPEN__FICHE_BEFORE_PERTURBED_WEIGHT_NORM')
a=s.index("s='[OPEN —");b=s.index("\n\nfor q in providers",a)
s=s[:a]+"""s='[OPEN — ficha anterior à identidade de norma do peso perturbado]\\n\\n# A1(b): consumir a ação dos cortes nos valores do peso\\n\\n'+stamp+'\\n\\n'+target+'\\n\\nADAPTAR: a identidade da ação direita já fornece Ab no domínio e seu vetor GNS. Basta a ponte algébrica para a norma do peso; não criar outra realização, peso escalar ou inscrição. A normalidade/aditividade de ν são fornecedores, não novos alvos. Não usar a caracterização falsa por minorantes positivos finitos para ν. A passagem a todos positivos e a tracialidade são obrigações posteriores nomeadas, não consequências deste lema isolado.\\n\\n'
""" +s[b:]
p=R/'prepare_perturbed_norm_fiche.py';assert not p.exists()
b=s.encode('utf8');q=p.with_name(p.name+'.tmp');q.write_bytes(b);assert q.read_bytes()==b;os.replace(q,p)

