from pathlib import Path
import os
R=Path(__file__).resolve().parent
s=(R/'prepare_right_action_algebra_fiche.py').read_text(encoding='utf8')
s=s.replace("pat='ScalarPolarRight|scalarPolarRightAlgebra|scalarRightAction_cfc|right_action_cfc'","pat='regularSineApprox|sine.*resolvent|resolvent.*sine|sigmoid.*sin|realScalarMultiplier.*tendsto'")
s=s.replace('search_right_action_algebra','search_sine_resolvent').replace('REAPROVEITAMENTO_A1B_ALGEBRA_ACAO_DIREITA','REAPROVEITAMENTO_A1B_APROXIMANTES_SENO')
a=s.index('specs=');b=s.index('\n\n\nproviders=',a)
s=s[:a]+"""specs=[('TGLExt/V351ScalarRightActionAlgebra.lean','scalarRightAction_cfc'),('TGLExt/V351ScalarRightActionAlgebra.lean','scalarPolarRightAlgebra_regular_mem'),('TGLExt/V351ScalarRightActionLimits.lean','scalarRightAction_closed_of_bounded_strongStar'),('TGLExt/V351RegularImaginaryPowers.lean','regularSpectralCoordinates_character'),('TGLExt/V351ScalarMultiplierCalculus.lean','realScalarMultiplier_cfc_ae'),('TGLExt/V350L2PositiveMultiplier.lean','realScalarMultiplier_norm_le'),('TGLExt/V351RegularPositiveGraph.lean','regularSpectralResolvent'),('TGLExt/V351RegularGeneratorAffiliation.lean','regularSpectralResolvent_mem'),('.lake/packages/mathlib/Mathlib/Analysis/SpecialFunctions/Trigonometric/Sinc.lean','continuous_sinc'),('.lake/packages/mathlib/Mathlib/Analysis/SpecificLimits/Basic.lean','tendsto_one_div_add_atTop_nhds_zero_nat')]
""" + s[b:]
a=s.index("target='");b=s.index("\n\n\nstamp=",a)
s=s[:a]+"""target='Construct actual b_n in the SAME regularCoreAlgebra P with b_n and b_n* satisfying the original polar right identity, uniform norm at most 1, and strong-star limit regularSpectralResolvent P. Use m=n+1, X_m=1/2 I + (1/(4i))(Lambda_{-1/m}-Lambda_{1/m}), g_m(x)=(1+sin(2*pi*x/m))/2, f_m(z)=sigmoid(m*(2*Re(z)-1)), b_n=cfc(f_m,X_m). Prove spectral identity with the same regularSpectralCoordinates, then symbol sigmoid(m*sin(2*pi*x/m)) convergence to sigmoid(2*pi*x). Reuse cfc_mem through scalarRightAction_cfc, bounded strong-star closure and L2 dominated convergence. The final consumer is P(R) and hence sqrt(B_epsilon) after a separate exact CFC identification. No norm convergence, no monotonicity b_n, no bounded h or log(h), no trace claimed.'
""" + s[b:]
s=s.replace('OPEN__FICHE_BEFORE_RIGHT_ACTION_CFC','OPEN__FICHE_BEFORE_SINE_RESOLVENT_APPROXIMATION')
a=s.index("s='[OPEN —");b=s.index("\n\nfor q in providers",a)
s=s[:a]+"""s='[OPEN — ficha anterior aos aproximantes explícitos do mesmo resolvente]\\n\\n# A1(b): translações, seno, CFC e limite forte-*\\n\\n'+stamp+'\\n\\n'+target+'\\n\\nADAPTAR: os fornecedores identificam translações e CFC, mas não produzem a família de aproximantes nem o seu limite no tipo exigido. O alvo consome exatamente esses fornecedores, sem novo GNS/J/core. O ramo por grafos/Schwartz/Kaplansky não será construído. A álgebra da ação direita tem DEV limpo e está em validação autoral/revisão neste instante; não é presumida aceita.\\n\\n'
""" +s[b:]
p=R/'prepare_sine_resolvent_fiche.py';assert not p.exists()
q=p.with_name(p.name+'.tmp');q.write_bytes(s.encode('utf8'));assert q.read_bytes()==s.encode('utf8');os.replace(q,p)
print(p)

