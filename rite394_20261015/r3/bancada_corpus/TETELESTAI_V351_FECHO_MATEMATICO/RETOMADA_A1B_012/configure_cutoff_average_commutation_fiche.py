from pathlib import Path
import os
R=Path(__file__).resolve().parent
s=(R/'prepare_perturbed_norm_fiche.py').read_text(encoding='utf8')
s=s.replace("pat='scalarRightAction_weight_norm|scalarPerturbedWeight|inverseCutoffPerturbedWeight|scalarWeight.*sandwich.*norm'","pat='regularSpectralResolvent.{0,45}commut|regularInverseCutoffSqrt.{0,45}commut|regularAverage.{0,45}commut|commut.{0,45}(average|cutoff)'")
s=s.replace('search_perturbed_weight_norm','search_cutoff_average_commutation')
start=s.index('specs=[');end=s.index('\nproviders=[]',start)
s=s[:start]+"""specs=[('TGLExt/V351RegularGeneratorAffiliation.lean','character_commutation_realScalarMultiplier'),('TGLExt/V351RegularImaginaryPowers.lean','regularSpectralCoordinates_character'),('TGLExt/V350L2CharacterMultiplier.lean','characterMultiplier_mul'),('TGLExt/V351InverseCutoffCFC.lean','regularInverseGeneratorCutoff_cfc'),('TGLExt/V350AntiunitaryPositiveConjugation.lean','hilbertPositiveSqrt'),('TGLExt/V350RegularApproximation.lean','regularAverage_apply'),('TGLExt/V351RegularPositiveGraph.lean','regularSpectralResolvent_nonneg')]
""" +s[end:]
start=s.index("target='");end=s.index('\nstamp=',start)
target="For P,t prove Commute(regularSpectralResolvent P)(regularUnitary P t), using SAME spectral coordinates and commuting characters. For epsilon>0 use existing cutoff CFC identity and existing hilbertPositiveSqrt=CFC.sqrt to deduce Commute(sqrt(B_epsilon))(regularUnitary P t). Integrate the actual regularUnitary using regularAverage_apply to prove Commute(sqrt(B_epsilon))(regularAverage P delta) for EVERY real delta. No new spectral transform, resolvent, average, square root or weight. Consumer: use the already established average recovery on a sqrt(B_epsilon) to extend perturbed-weight order to all positive inputs. This does not infer commutation of arbitrary b in the right algebra with the averages. Mathematical helper is generic CFC commutation instantiated on Hilbert operators."
s=s[:start]+'target='+repr(target)+'\n'+s[end:]
s=s.replace('OPEN__FICHE_BEFORE_PERTURBED_WEIGHT_NORM','OPEN__FICHE_BEFORE_CUTOFF_AVERAGE_COMMUTATION').replace('REAPROVEITAMENTO_A1B_PESO_PERTURBADO_NORMA','REAPROVEITAMENTO_A1B_COMUTACAO_CORTES_MEDIAS')
a=s.index("s='[OPEN —");b=s.index('for q in providers:',a)
s=s[:a]+"""s='[OPEN — ficha anterior à comutação dos cortes com as médias]\\n\\n# A1(b): as médias comutam com as raízes dos cortes originais\\n\\n'+stamp+'\\n\\n'+target+'\\n\\nADAPTAR: coordenação espectral, comutação de caracteres, CFC e integral das translações existentes. Não reconstruir as coordenadas nem o resolvente. A consulta TODOS_POSITIVOS nomeia esta ponte como necessária. Mathlib Commute.cfc/IsSelfAdjoint.commute_cfc e Commute.cfcₙ_nnreal foram lidos no fornecedor ContinuousFunctionalCalculus/Commute.lean.\\n\\n'
""" +s[b:]
p=R/'prepare_cutoff_average_commutation_fiche.py';assert not p.exists();b=s.encode();t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)

