from pathlib import Path
import os
R=Path(__file__).resolve().parent
s=(R/'prepare_average_fixed_pair_fiche.py').read_text(encoding='utf8')
a=s.index("pat='");b=s.index('\nqueries=',a)
s=s[:a]+"pat='scalarTomitaImaginaryPower_fixed_of_fixed_pair|regularAverage_square_modular_fixed|resolventPhaseOperator_fixed_at_half|cfc.{0,25}eigenvector'"+s[b:]
s=s.replace('search_average_fixed_pair','search_modular_fixed_vectors')
a=s.index('specs=[');b=s.index('\nproviders=[]',a)
s=s[:a]+"""specs=[('TGLExt/V351AverageFixedPair.lean','regularAverage_square_fixed_pair'),('TGLExt/V350ScalarTomitaSquare.lean','scalarTomitaSquare_domain_iff'),('TGLExt/V350ScalarTomitaSquare.lean','scalarTomitaSquare_apply'),('TGLExt/V350ScalarTomitaResolvent.lean','scalarTomitaResolvent_inverse'),('TGLExt/V351ScalarTomitaImaginaryPowers.lean','scalarTomitaImaginaryPower_damping'),('TGLExt/V351ResolventImaginaryIntertwining.lean','resolventPhaseOperator_intertwines'),('TGLExt/V351ResolventPhaseFunctions.lean','resolventPhaseFunction_continuous'),('.lake/packages/mathlib/Mathlib/Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Unital.lean','cfc_algebraMap')]
"""+s[b:]
a=s.index('cp=K/');b=s.index('\nd=dict(',a)
s=s[:a]+"""cp=K/'TGLExt/V351ScalarImaginaryCoreAction.lean';ls=cp.read_text(encoding='utf8').splitlines();line=next(i+1 for i,s in enumerate(ls) if s.startswith('theorem scalarTomitaImaginaryPower_core_conjugation'))
target='ADAPTAR: for the SAME S,F,Delta_nu=FS,T_nu and U_t, prove a vector fixed by S and F in their actual domains is fixed by every U_t. Use the exact composition domain, the inverse identity to get T_nu*x=(1/2)*x, then the existing damped phase intertwiner with rankOne(x,x) and (1/2)I to read g_t(1/2)=1/4. Evaluate at x and cancel norm squared only when x is nonzero; handle zero separately. Damping is also (1/4)*x, so existing U*damping=phase fixes x. Then consume the preceding fixed pair of star(e_delta)*e_delta to exhibit those same modular-fixed vectors. Consumer is core covariance for equality of U with pi(lambda)R_-t on pi(N)Lambda(z_delta), followed by a separate totality argument. No new CFC, imaginary group, generator, GNS, weight, normalization, or claim that a single vector is cyclic. Delta30 standalone/review pending when fiche created; source frozen and target delivery depends on its acceptance. One generic private phase/eigenvector adapter is anticipated; no generic CFC framework.'
"""+s[b:]
s=s.replace('OPEN__FICHE_BEFORE_AVERAGE_FIXED_PAIR','OPEN__FICHE_BEFORE_MODULAR_FIXED_VECTORS').replace('REAPROVEITAMENTO_A1B_MEDIA_PAR_FIXO','REAPROVEITAMENTO_A1B_VETORES_FIXOS_MODULARES')
s=s.replace('ficha anterior ao par fixo de Tomita','ficha anterior aos vetores fixos do grupo modular')
s=s.replace('Consulta2 V2 lida; delta29 fornece a ação direita da média, usada no quadrado auto-adjunto.','Consulta2 V2 e consulta curta do revisor de 15/09 relidas: usar o intertwiner de fase já especializado, sem construir o grupo de (1/2)I. rankOne_apply consultado na Mathlib Analysis/InnerProductSpace/LinearMap.lean:322; enumeração de fornecedores registra também o contexto desse import.')
def put(p,s):
 assert not p.exists();b=s.encode();t=p.with_suffix('.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
put(R/'prepare_modular_fixed_vectors_fiche.py',s)
s=(R/'dev_compile_average_fixed_pair.py').read_text(encoding='utf8')
s=s.replace('average_fixed_pair','modular_fixed_vectors').replace('V351AverageFixedPair','V351ModularFixedVectors').replace('REAPROVEITAMENTO_A1B_MEDIA_PAR_FIXO','REAPROVEITAMENTO_A1B_VETORES_FIXOS_MODULARES')
put(R/'dev_compile_modular_fixed_vectors.py',s)

