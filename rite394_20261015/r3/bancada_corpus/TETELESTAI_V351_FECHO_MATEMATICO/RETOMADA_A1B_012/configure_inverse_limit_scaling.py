from pathlib import Path
import os
R=Path(__file__).resolve().parent
def put(p,s):
    assert not p.exists() and p.is_relative_to(R)
    b=s.encode('utf8');t=p.with_name(p.name+'.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
s=(R/'prepare_limit_faithful_fiche.py').read_text(encoding='utf8')
a=s.index("pat='");b=s.index('\nqueries=',a)
s=s[:a]+"pat='scalarInverse(CutoffWeight_dual|LimitWeight_(scaled_sequence|dual))|regularInverseCutoffSqrt_dual|peso.{0,20}limite.{0,20}escala'"+s[b:]
s=s.replace('search_limit_weight_faithful','search_inverse_limit_scaling')
a=s.index('specs=[');b=s.index('\nproviders=[]',a)
s=s[:a]+"""specs=[('TGLExt/V351InverseGeneratorCutoff.lean','regularInverseGeneratorCutoff_dual'),('TGLExt/V351InverseGeneratorCutoff.lean','regularInverseGeneratorCutoff_nonneg'),('TGLExt/V350DualWeightCuts.lean','dualAmbient_nonneg'),('TGLExt/V350RegularDualAction.lean','dualAmbient_symm'),('TGLExt/V350DualWeightForm.lean','dualQuadraticIntegral_dual_invariant'),('TGLExt/V350DualQuadraticLaws.lean','dualQuadraticIntegral_smul_operator'),('TGLExt/V351RegularCoreTraceContract.lean','positiveDual'),('TGLExt/V351InverseLimitWeight.lean','scalarInverseCutoffWeight_antitone'),('TGLExt/V351InverseLimitWeight.lean','scalarInverseLimitWeight'),('.lake/packages/mathlib/Mathlib/Analysis/SpecialFunctions/ContinuousFunctionalCalculus/Rpow/Basic.lean','mul_self_eq_mul_self_iff'),('.lake/packages/mathlib/Mathlib/Algebra/Order/Archimedean/Basic.lean','exists_nat_one_div_lt'),('.lake/packages/mathlib/Mathlib/Data/ENNReal/Inv.lean','mul_iSup')]
"""+s[b:]
a=s.index("target='");b=s.index('\nstamp=',a)
target='Prove dual scaling of the SAME scalarInverseLimitWeight on existing TGLV351.positiveDual: tau(theta_s X)=ofReal(exp(-s))*tau(X). Adapt positive-square uniqueness for the existing hilbertPositiveSqrt, actual inverse-cutoff dual identity, original dual weight invariance and real homogeneity; no new root/GNS/cone. Then prove cofinality of r/(n+1) for r>0 using two supremum inequalities and existing regulator antitonicity, including infinite values. Four consumer-linked targets: root transport, cutoff weight transport, scaled sequence cofinality, limit dual scaling. Consumer is the exact dual_scaling field of RegularCoreTraceData, not a substitute trace contract. Semifinitude and traciality remain open.'
s=s[:a]+'target='+repr(target)+'\n'+s[b:]
s=s.replace('OPEN__FICHE_BEFORE_LIMIT_WEIGHT_FAITHFUL','OPEN__FICHE_BEFORE_INVERSE_LIMIT_SCALING').replace('REAPROVEITAMENTO_A1B_FIDELIDADE_PESO_LIMITE','REAPROVEITAMENTO_A1B_ESCALA_PESO_LIMITE')
a=s.index("s='[OPEN —");b=s.index('for q in providers:',a)
s=s[:a]+"s='[OPEN — ficha anterior à escala dual do peso limite]\\n\\n# A1(b): ação dual no mesmo candidato\\n\\n'+stamp+'\\n\\n'+target+'\\n\\nADAPTAR. A escala do peso tem sinal MENOS, obtida transportando o sanduíche por theta_(-s). A sequência de reguladores muda e sua cofinalidade precisa ser paga. Não confundir invariância do peso dual com tracialidade.\\n\\n'\n"+s[b:]
put(R/'prepare_inverse_limit_scaling_fiche.py',s)
s=(R/'dev_compile_inverse_limit_faithful.py').read_text(encoding='utf8')
for a,b in [('inverse_limit_faithful','inverse_limit_scaling'),('V351InverseLimitFaithful','V351InverseLimitScaling'),('REAPROVEITAMENTO_A1B_FIDELIDADE_PESO_LIMITE','REAPROVEITAMENTO_A1B_ESCALA_PESO_LIMITE')]:s=s.replace(a,b)
put(R/'dev_compile_inverse_limit_scaling.py',s)
