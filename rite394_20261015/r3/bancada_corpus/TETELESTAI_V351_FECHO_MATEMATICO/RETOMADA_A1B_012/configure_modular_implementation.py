from pathlib import Path
import os
R=Path(__file__).resolve().parent
s=(R/'prepare_average_fixed_pair_fiche.py').read_text(encoding='utf8')
a=s.index("pat='");b=s.index('\nqueries=',a)
s=s[:a]+"pat='scalarTomitaImaginaryPower_eq_regular_implementation|modular.{0,25}implementator|modular.{0,25}implementation|right.{0,20}average.{0,20}total'"+s[b:]
s=s.replace('search_average_fixed_pair','search_modular_implementation')
a=s.index('specs=[');b=s.index('\nproviders=[]',a)
s=s[:a]+"""specs=[('TGLExt/V351ModularFixedVectors.lean','regularAverage_square_modular_fixed'),('TGLExt/V351ScalarImaginaryCoreAction.lean','scalarTomitaImaginaryPower_core_conjugation'),('TGLExt/V350ScalarRegularPolarCommutation.lean','regularRightGNS_commutes_left'),('TGLExt/V350ScalarRegularPolarCommutation.lean','scalarTomitaPolar_regular_generator'),('TGLExt/V350ScalarRegularRightGNS.lean','regularRightGNS_intertwines'),('TGLExt/V350StrongOperatorIntegral.lean','operatorIntegral_commutes'),('TGLExt/V350ContractionAdjointLimit.lean','regularAverage_star_tendsto_identity'),('TGLExt/V350ScalarWeightAction.lean','scalarWeightGNSEmbedding_denseRange'),('TGLExt/V350ScalarWeightAction.lean','scalarWeightGNSAction_intertwines'),('TGLExt/V350ScalarGNSStrongContinuity.lean','scalarGNSRepresentation_tendsto_of_uniformly_bounded'),('TGLExt/V351ScalarRightActionAlgebra.lean','ScalarPolarRight'),('TGLExt/V350StrongBoundedApplication.lean','bounded_application_tendsto')]
"""+s[b:]
a=s.index('cp=K/');b=s.index('\nd=dict(',a)
s=s[:a]+"""cp=K/'TGLExt/V351RegularCoreTraceContract.lean';ls=cp.read_text(encoding='utf8').splitlines();line=next(i+1 for i,s in enumerate(ls) if s.startswith('  tracial :'))
target='ADAPTAR: prove on ALL vectors of the SAME scalar GNS that U_t equals pi(lambda_t) R_{-t}. Use actual fixed vectors Lambda(z_delta), z_delta=e_delta* e_delta (star(e_delta)*e_delta), from delta31, plus existing all-core covariance. Prove the same W_t fixes Lambda(z_delta) by the actual left/right product identities and z_delta commutation with regular unitaries. That commutation reuses StrongIntegral.operatorIntegral_commutes, not the inaccessible private proof of delta29. Transfer the existing contraction strong/strong-star approximation z_delta to pi(z_delta), then conjugate by original J to obtain rho(z_delta) -> I strongly. Right identity gives rho(z_delta)Lambda(a)=pi(a)Lambda(z_delta), so limits plus dense original Lambda(n_nu) prove totality and equality. No premise of single-vector cyclicity, no inference of implementator identity from covariance alone. No new operator definition or general integration/CFC framework. One public theorem, local or private adapters only where type transport requires. Delta31 standalone underway when fiche created; final delivery depends on independent acceptance. Consumer tracial field remains INDIRECT: later half-power/Q domain compatibility still required, not furnished merely by this implementation identity. Same h, Delta_nu, nu, tau, GNS; never identify h=Delta_nu.'
"""+s[b:]
s=s.replace('OPEN__FICHE_BEFORE_AVERAGE_FIXED_PAIR','OPEN__FICHE_BEFORE_MODULAR_IMPLEMENTATION').replace('REAPROVEITAMENTO_A1B_MEDIA_PAR_FIXO','REAPROVEITAMENTO_A1B_IMPLEMENTADOR_MODULAR')
s=s.replace('ficha anterior ao par fixo de Tomita','ficha anterior à igualdade dos implementadores modulares')
s=s.replace('Consulta2 V2 lida; delta29 fornece a ação direita da média, usada no quadrado auto-adjunto.','Consulta2 V2 relida; consumidores futuros Q/meias potências/tracialidade continuam abertos. A fonte StrongIntegral.operatorIntegral_commutes foi lida integralmente antes de propor a adaptação; usar esse fornecedor evita reproduzir integração vetorial.')
def put(p,s):
    assert not p.exists(),p
    b=s.encode('utf8');t=p.with_suffix('.tmp');t.write_bytes(b);assert t.read_bytes()==b;os.replace(t,p)
put(R/'prepare_modular_implementation_fiche.py',s)
s=(R/'dev_compile_modular_fixed_vectors.py').read_text(encoding='utf8')
s=s.replace('modular_fixed_vectors','modular_implementation').replace('V351ModularFixedVectors','V351ModularImplementation').replace('REAPROVEITAMENTO_A1B_VETORES_FIXOS_MODULARES','REAPROVEITAMENTO_A1B_IMPLEMENTADOR_MODULAR')
put(R/'dev_compile_modular_implementation.py',s)
