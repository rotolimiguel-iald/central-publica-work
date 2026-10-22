from pathlib import Path
import os
R=Path(__file__).resolve().parent
s=(R/'prepare_perturbed_norm_fiche.py').read_text(encoding='utf8')
s=s.replace("pat='scalarRightAction_weight_norm|scalarPerturbedWeight|inverseCutoffPerturbedWeight|scalarWeight.*sandwich.*norm'", "pat='scalarInverse(CutoffWeight_one|LimitWeight)_faithful|inverse.{0,20}limit.{0,20}faithful|peso.{0,20}limite.{0,20}fiel'")
s=s.replace('search_perturbed_weight_norm','search_limit_weight_faithful')
a=s.index('specs=[');b=s.index('\nproviders=[]',a)
s=s[:a]+"""specs=[('TGLExt/V350ResolventSquareRoot.lean','positive_sqrt_injective'),('TGLExt/V350ResolventSquareRoot.lean','resolventSquareRoot_dense'),('TGLExt/V350ScalarDualWeightFaithfulness.lean','dualQuadraticIntegral_vacuum_faithful'),('TGLExt/V351RegularPositiveGraph.lean','regularSpectralResolvent_injective'),('TGLExt/V351RegularPositiveGraph.lean','regularSpectralResolvent_nonneg'),('TGLExt/V351InverseGeneratorCutoff.lean','regularInverseGeneratorCutoff_one'),('TGLExt/V351InverseCutoffCFC.lean','regularInverseGeneratorCutoff_sqrt_right'),('TGLExt/V351InverseLimitWeight.lean','scalarInverseCutoffWeight_le_limit'),('TGLExt/V351InverseLimitWeight.lean','scalarInverseLimitWeight_zero')]
"""+s[b:]
a=s.index("target='");b=s.index('\nstamp=',a)
target='Prove scalarInverseCutoffWeight P 1 faithful on PositiveCoreInput P using B_1=R, membership of the existing sqrt(R) in N and faithfulness of the SAME vacuum dual weight. The ORIGINAL positive_sqrt_injective and resolventSquareRoot_dense imply injectivity and dense range of the bounded CFC root; adapt the wrapper only. If star sqrt(R) X sqrt(R)=0, injectivity cancels the left root and continuity/dense range cancels the right root, giving X=0. Then scalarInverseLimitWeight dominates n=0 (epsilon_0=1), so it is faithful. No new GNS/root/resolvent and no need to prove every regulator inverse injective. Consumer: faithful field of RegularCoreTraceData for the candidate value. Neither semifinitude, traciality nor dual scaling follows from this.'
s=s[:a]+'target='+repr(target)+'\n'+s[b:]
s=s.replace('OPEN__FICHE_BEFORE_PERTURBED_WEIGHT_NORM','OPEN__FICHE_BEFORE_LIMIT_WEIGHT_FAITHFUL').replace('REAPROVEITAMENTO_A1B_PESO_PERTURBADO_NORMA','REAPROVEITAMENTO_A1B_FIDELIDADE_PESO_LIMITE')
a=s.index("s='[OPEN —");b=s.index('for q in providers:',a)
s=s[:a]+"""s='[OPEN — ficha anterior à fidelidade do peso limite]\\n\\n# A1(b): um corte já basta para a fidelidade do limite\\n\\n'+stamp+'\\n\\n'+target+'\\n\\nADAPTAR: o domínio do fornecedor resolventSquareRoot_dense é a imagem da raiz LIMITADA CFC.sqrt R. Não confundir essa raiz com o operador parcial resolventSquareRoot. A dupla injetividade/densidade é reutilizada; não é pressuposta a fidelidade do limite.\\n\\n'
"""+s[b:]
p=R/'prepare_limit_faithful_fiche.py';assert not p.exists();b=s.encode('utf8');t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
