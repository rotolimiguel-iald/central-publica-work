from pathlib import Path
import os
R=Path(__file__).resolve().parent
s=(R/'prepare_average_polar_right_fiche.py').read_text(encoding='utf8')
a=s.index("pat='");b=s.index('\nqueries=',a)
s=s[:a]+"pat='average.{0,30}fixed.{0,30}(pair|tomita)|scalarWeightStar_fixed_pair|regularAverage_square_fixed_pair'"+s[b:]
s=s.replace('search_average_polar_right','search_average_fixed_pair')
a=s.index('specs=[');b=s.index('\nproviders=[]',a)
s=s[:a]+"""specs=[('TGLExt/V351AveragePolarRight.lean','regularAverage_mem_scalarPolarRightAlgebra'),('TGLExt/V350ScalarRightAdjointPair.lean','scalarRightAdjointPair_maximal'),('TGLExt/V350ScalarWeightTomitaIdentification.lean','scalarClosedTomita_extends_weight_star'),('TGLExt/V350ScalarWeightAction.lean','scalarWeightGNSAction_intertwines'),('TGLExt/V351AntiunitaryResolventPhase.lean','antiunitaryConjugate_selfadjoint'),('TGLExt/V350ScalarWeightDomain.lean','HasFiniteScalarSquare.left_mul'),('TGLExt/V350DualSemifiniteIdeal.lean','regularAverage_hasFiniteDualSquare')]
"""+s[b:]
a=s.index('cp=K/');b=s.index('\nd=dict(',a)
s=s[:a]+"""cp=K/'TGLExt/V350ScalarTomitaSquare.lean';ls=cp.read_text(encoding='utf8').splitlines();line=next(i+1 for i,s in enumerate(ls) if s.startswith('theorem scalarTomitaSquare_domain_iff'))
target='ADAPTAR: within original scalarWeightStarCore/GNS/S/F, prove a selfadjoint A with A.val in scalarPolarRightAlgebra has Lambda(A) simultaneously fixed by S and F. Construct the actual ScalarRightAdjointPair (right and adjoint vectors both Lambda(A)) from polar-right identity and the old left-action identity; use maximality, not a supplied fixed-vector hypothesis. Then exhibit such an A whose ambient value is EXACTLY regularAverage(delta)* star-squared, specifically star(e_delta)*e_delta, delta>0. E-membership follows from accepted algebra operations and preceding delta29; finite domain from e_delta finite and left ideal, selfadjoint by star laws. No new operator/GNS/weight/J, no average-selfadjoint assertion, no normalization or trace. Consumer: scalarTomitaSquare_domain_iff and scalarTomitaResolvent_inverse for the next eigenvector/implementator step. These later consequences are not delivered merely by naming them. Delta29 standalone audit/review in progress at fiche, wait for acceptance before final consumer delivery.'
"""+s[b:]
s=s.replace('OPEN__FICHE_BEFORE_AVERAGE_POLAR_RIGHT','OPEN__FICHE_BEFORE_AVERAGE_FIXED_PAIR').replace('REAPROVEITAMENTO_A1B_MEDIA_ACAO_DIREITA','REAPROVEITAMENTO_A1B_MEDIA_PAR_FIXO')
s=s.replace('ficha anterior à pertença da média à álgebra direita','ficha anterior ao par fixo de Tomita')
s=s.replace('Consulta2 corrigida V2 já lida; rota reduzida à partição exata da integral e limites existentes.','Consulta2 V2 lida; delta29 fornece a ação direita da média, usada no quadrado auto-adjunto.')
def put(p,s):
    assert not p.exists();b=s.encode();t=p.with_suffix('.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
put(R/'prepare_average_fixed_pair_fiche.py',s)
s=(R/'dev_compile_average_polar_right.py').read_text(encoding='utf8')
s=s.replace('average_polar_right','average_fixed_pair').replace('V351AveragePolarRight','V351AverageFixedPair').replace('REAPROVEITAMENTO_A1B_MEDIA_ACAO_DIREITA','REAPROVEITAMENTO_A1B_MEDIA_PAR_FIXO')
put(R/'dev_compile_average_fixed_pair.py',s)

