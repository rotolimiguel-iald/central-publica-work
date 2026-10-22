import TGL.Basic
import TGL.HalfNat
import TGL.AreaScale
import TGL.FiniteThreeLocks
import TGL.ContinuousCornerAbstract
import TGL.SpecificAQFTWitness
import TGL.ModularRealization
import TGL.HalfNatFresnel
import TGL.VerbInhabitant
import TGL.TransportData
import TGL.NameIndex
import TGL.HalfNatJonesTower
import TGL.GravitonShadow
import TGL.NameRelation
import TGL.CoreSupport
import TGLExt

set_option autoImplicit false

/-!
# Auditoria por kernel

`#check` dos teoremas, `#print axioms` (deve reportar apenas `propext` /
`Classical.choice` / `Quot.sound`; jamais `sorryAx`, `Lean.trustCompiler` ou
axiomas customizados `TGL.*`), e as sentinelas de saida.
-/

namespace TGL.Audit

-- ---- #check dos teoremas ----
#check @TGL.HalfNat.halfNat_of_selfConjugate
#check @TGL.HalfNat.selfConjugate_halfNat_unique
#check @TGL.AreaScale.eta_eq_one_over_two_kappa
#check @TGL.AreaScale.newtonPlanck_equivalence
#check @TGL.AreaScale.face_area_eq_G
#check @TGL.FiniteThreeLocks.H3L_isSelfAdjoint
#check @TGL.FiniteThreeLocks.H3L_quadratic_form
#check @TGL.FiniteThreeLocks.H3L_posSemidefinite
#check @TGL.FiniteThreeLocks.ker_H3L_eq_threeLocks
#check @TGL.FiniteThreeLocks.PF_isProjection
#check @TGL.FiniteThreeLocks.PF_isSelfAdjoint
#check @TGL.FiniteThreeLocks.PF_apply_mem
#check @TGL.FiniteThreeLocks.PF_eq_self_iff
#check @TGL.FiniteThreeLocks.normalizedCornerTrace_PF
#check @TGL.FiniteThreeLocks.equalConjugateFaces_halfTrace
#check @TGL.ContinuousCorner.ContinuousCornerWitness.normalizedTrace_P_eq_one
#check @TGL.ContinuousCorner.ContinuousCornerWitness.equalFaces_normalizedTrace_half
#check @TGL.SpecificAQFT.continuousCorner_of_witness
#check @TGL.SpecificAQFT.threeLocksCorner_of_witness
-- v23 (rigidificacao): geometria de Minkowski incondicional + localidade condicional
#check @TGL.SpecificAQFT.wedges_spacelike
#check @TGL.SpecificAQFT.wedge_locality
-- v24 (realizacao modular por DADOS + Fresnel)
#check @TGL.ModularRealization.dualInvariant_PF_no_go
#check @TGL.ModularRealization.fullWitness_not_finiteDimensional
#check @TGL.ModularRealization.fullWitness_core_nonempty
#check @TGL.ModularRealization.fullWitness_PF_nonzero_finite
#check @TGL.HalfNatFresnel.fresnel_selfConjugate_half
#check @TGL.HalfNatFresnel.modular_action_halfNat
-- v25 (o Verbo habitante)
#check @TGL.VerbInhabitant.exp_fixed_of_annihilates
#check @TGL.VerbInhabitant.verb_semigroup_fixes
#check @TGL.VerbInhabitant.canonicalVerb_exists
#check @TGL.VerbInhabitant.dual_calibration_exists
-- v26 (o transporte do seletor)
#check @TGL.TransportData.descent_iff_defect_zero
#check @TGL.TransportData.transport_defect_of_jones
#check @TGL.TransportData.jones_selector_not_descended
-- v27 (o indice do Nome)
#check @TGL.NameIndex.ParityData.average_idem
#check @TGL.NameIndex.ParityData.average_bimodular
#check @TGL.NameIndex.name_index_eq_csc_sq
#check @TGL.NameIndex.name_index_mul_sin_sq
#check @TGL.NameIndex.amplitude_weight_index_chain
-- v28 (o primeiro habitante: torre de Jones da Meia-Nat)
#check @TGL.HalfNatJonesTower.halfNatJonesTower
#check @TGL.HalfNatJonesTower.halfNatJonesTower_exists
#check @TGL.HalfNatJonesTower.halfNat_mirror_not_descended
#check @TGL.HalfNatJonesTower.finite_markov_forces_half
-- v29 (sombra finita do graviton + split das faces Q3)
#check @TGL.TransportData.facePlus_idem
#check @TGL.TransportData.faces_orthogonal
#check @TGL.TransportData.faces_sum
#check @TGL.GravitonShadow.canonicalGravitonShadow
#check @TGL.GravitonShadow.bell_cci_half
#check @TGL.GravitonShadow.product_cci_zero
#check @TGL.GravitonShadow.bell_corner_unit
-- v30 (o Nome e' a relacao: correcao do especialista + TERCEIRO habitante TL3)
#check @TGL.NameRelation.pqp_eq
#check @TGL.NameRelation.qpq_eq
#check @TGL.NameRelation.geometric_eq_trace_weight_iff
#check @TGL.NameRelation.tl3_linearly_independent
#check @TGL.NameRelation.canonicalTLThree
#check @TGL.NameRelation.canonicalTLThree_exists
-- v32 (fechamento por separacao de tipos: suporte != espelho; construtores; gauge)
#check @TGL.CoreSupport.support_annihilates
#check @TGL.CoreSupport.support_maximal
#check @TGL.CoreSupport.threeLocksFromSupport
#check @TGL.CoreSupport.realizationFromSupport
#check @TGL.CoreSupport.transport_defect_gauge_invariant
-- v33 (a colheita dos externos: escada TGLExt integrada -- Degrau 0 FECHADO,
--      Degrau 1 quase; tudo FINITO-dimensional, nada e' III_1)
#check @TGLExt.commutant_triple
#check @TGLExt.bicommutant_range_Lmul
#check @TGLExt.frob_Jconj_Jconj
#check @TGLExt.Jconj_Lmul_Jconj
#check @TGLExt.omega_cyclic
#check @TGLExt.omega_separating
#check @TGLExt.Sop_tomita
#check @TGLExt.Sop_involutive
#check @TGLExt.J_deltaHalf
#check @TGLExt.deltaHalf_deltaHalf
#check @TGLExt.delta_omega
#check @TGLExt.frob_delta_nonneg
#check @TGLExt.gibbs_kms
#check @TGLExt.modPow_add
#check @TGLExt.modPow_mem_unitary
#check @TGLExt.sigma_mul
#check @TGLExt.sigma_sigma
#check @TGLExt.gibbs_sigma
#check @TGLExt.exp_logRho
#check @TGLExt.sigma_omega
#check @TGLExt.diagExpect_bimod
#check @TGLExt.diagExpect_posSemidef
#check @TGLExt.eTr_Lmul_eTr
#check @TGLExt.eD_Lmul_eD
#check @TGLExt.commutant_range_diagonal
-- v34 (Degrau 2: o indice de Pimsner-Popa COMPUTADO = n para C c M_n e D c M_n)
#check @TGLExt.trace_smul_one_sub_posSemidef
#check @TGLExt.card_smul_diagExpect_sub_posSemidef
#check @TGLExt.isGreatest_ppBound_trExpect
#check @TGLExt.isGreatest_ppBound_diagExpect
#check @TGLExt.ppIndexTr_eq_card
#check @TGLExt.ppIndexDiag_eq_card
-- v35 (Degrau 2, parte 2: tracos de Markov das torres; PP vs torre como teorema)
#check @TGLExt.trace_Lmul_eD
#check @TGLExt.trace_Lmul_eTr
#check @TGLExt.tau_eD
#check @TGLExt.tau_eTr
#check @TGLExt.masa_tower_weight_eq_ppBest
#check @TGLExt.pp_ne_tower_for_scalars
-- v38 (Degrau 1 FECHO: o bicomutante GERAL finito)
#check @TGLExt.end_reconstruction
#check @TGLExt.Cmat_of_sum
#check @TGLExt.commutant_Cmat_comm
#check @TGLExt.exists_span_form
#check @TGLExt.frob_self_eq_zero_iff
#check @TGLExt.disjoint_frobOrtho
#check @TGLExt.isCompl_frobOrtho
#check @TGLExt.frobProj_comm_Lmul
#check @TGLExt.finite_bicommutant
-- v41 (A MATRIZ-S FECHADA: Teorema S-boundary no kernel; theta generico, beta=runtime)
#check @TGLExt.Grot_sq
#check @TGLExt.exp_smul_Grot
#check @TGLExt.Smat_mem_unitary
#check @TGLExt.Smat_mul
#check @TGLExt.Smat_spectral
#check @TGLExt.normSq_reflection_add_transmission
#check @TGLExt.rhoOut_trace
-- v42 (O COCICLO DE CONNES: face finita do Lema 3 -- E1/E2/E4/U/E3c/E6; GLOBAL_LIFT segue ABERTO)
#check @TGLExt.cocycle_chain
#check @TGLExt.cocycle_triangle
#check @TGLExt.cocycle_temporal
#check @TGLExt.cocycle_conjTranspose
#check @TGLExt.cocycle_mem_unitary
#check @TGLExt.cocycle_of_commute
#check @TGLExt.logRho_conj
#check @TGLExt.modPow_conj
#check @TGLExt.cocycle_covariance
-- v43 (ERGODICIDADE T1 na face finita: setor fixo=centralizador; traco emerge; T_t -> E_0)
#check @TGLExt.sigma_fixed_of_commute
#check @TGLExt.logRho_diagonal
#check @TGLExt.sigma_fixed_iff_diag
#check @TGLExt.gibbs_tracial_on_centralizer
#check @TGLExt.dephase_add
#check @TGLExt.dephase_tendsto_expectation
#check @TGLExt.ergodic_convergence_modular
-- v44 (O PRODUTO CRUZADO FINITO com cociclo dual: peso dual de Takesaki na
--      face finita -- covariancia ALEM dos unitarios internos; GLOBAL_LIFT segue ABERTO)
#check @TGLExt.lam_one
#check @TGLExt.lam_mul
#check @TGLExt.lam_conjTranspose
#check @TGLExt.lam_mem_unitary
#check @TGLExt.piRep_mul
#check @TGLExt.piRep_star
#check @TGLExt.piRep_injective
#check @TGLExt.lam_conj_piRep
#check @TGLExt.lam_mul_piRep
#check @TGLExt.Ecomp_idem
#check @TGLExt.Ecomp_piRep
#check @TGLExt.Ecomp_lam
#check @TGLExt.gibbs_Ecomp
#check @TGLExt.gibbs_piRep_dual
#check @TGLExt.trace_piRep
#check @TGLExt.alphaAct_modPow
#check @TGLExt.logRho_piRep
#check @TGLExt.exp_piRep
#check @TGLExt.modPow_piRep
#check @TGLExt.cocycle_piRep
#check @TGLExt.sigma_piRep
#check @TGLExt.dual_weight_left
#check @TGLExt.dual_weight
#check @TGLExt.dual_flow_fixes_lam_of_invariant
#check @TGLExt.cocycle_covariance_beyond_inner
#check @TGLExt.Dchi_mul_lam
#check @TGLExt.Dchi_comm_piRep
#check @TGLExt.Dchi_conj_lam
#check @TGLExt.Dchi_comm_modPow
#check @TGLExt.gibbs_Dchi
-- v45 (A ESCADA DO GLOBAL_LIFT: densidade diadica quantitativa; obstrucao do
--      traco discreto; canal de medicao no referencial-S; fecho continuo EXTERNO)
#check @TGLExt.dyadic_approx
#check @TGLExt.dyadic_stage_mono
#check @TGLExt.dyadic_tendsto
#check @TGLExt.annihilator_fixes_stage
#check @TGLExt.scaling_fixed_eq_zero
#check @TGLExt.DualScalingData.fixed_tau_zero
#check @TGLExt.DualScalingData.dyadic_stage_tau_zero
#check @TGLExt.sFrame_zero
#check @TGLExt.sFrame_add
#check @TGLExt.sFrame_tendsto
#check @TGLExt.dephased_rhoOut_zero_zero
#check @TGLExt.dephased_rhoOut_one_one
#check @TGLExt.measurement_channel_endpoint
-- v46 (A FAMILIA DO CANTO: isotonia+covariancia+traco finito+invariancia modular
--      construidas; [P_F,lambda(s)]=0 de graca; traco finito => nao theta-fixo)
#check @TGLExt.corner_fixed_by_flow
#check @TGLExt.DualScalingData.finite_trace_not_fixed
#check @TGLExt.cornerProj_apply
#check @TGLExt.cornerProj_idem
#check @TGLExt.cornerProj_conjTranspose
#check @TGLExt.cornerProj_mono
#check @TGLExt.lam_conj_cornerProj
#check @TGLExt.trace_cornerProj
#check @TGLExt.cornerProj_comm_piRep
#check @TGLExt.cornerProj_comm_modPow
#check @TGLExt.cornerProj_univ
-- v47 (BISOGNANO-WICHMANN na face finita: geometria do boost + gerador modular a 2pi;
--      a identificacao das duas metades = KNOWN p/ wedges (BW 1975/76), OPEN alem)
#check @TGLExt.boost_zero
#check @TGLExt.boost_add
#check @TGLExt.boost_preserves_eta
#check @TGLExt.boost_det
#check @TGLExt.boost_null_expand
#check @TGLExt.boost_null_contract
#check @TGLExt.boost_preserves_wedge
#check @TGLExt.logRho_gibbs_boost
#check @TGLExt.modPow_gibbs_boost
#check @TGLExt.sigma_gibbs_boost
-- v48 (O GRAVITON OBSERVAVEL: cinematica de spin-2 -- 2 polarizacoes, helicidade +-2,
--      gauge TT, deltaI_modular com delta(1)=0; dinamica/interacoes seguem com estatuto)
#check @TGLExt.polPlus_symm
#check @TGLExt.polCross_symm
#check @TGLExt.polPlus_traceless
#check @TGLExt.polCross_traceless
#check @TGLExt.polarization_decomposition
#check @TGLExt.polarizations_independent
#check @TGLExt.rot_add
#check @TGLExt.rot_conj_polPlus
#check @TGLExt.rot_conj_polCross
#check @TGLExt.rot_conj_one
#check @TGLExt.minkNorm4_nullK
#check @TGLExt.gaugeSym_symmetric
#check @TGLExt.gauge_transverse_zero
#check @TGLExt.excite_one_zero
#check @TGLExt.excite_leibniz
#check @TGLExt.Smat_sub_one
-- v49 (AS FLUTUACOES QUANTICAS DA GEOMETRIA: Var=p(1-p)=defeito de transporte;
--      Meia-Nat = flutuacao maxima; [h+,hx]=2J; limite classico = LLN)
#check @TGLExt.variance_of_projection
#check @TGLExt.reflObs_proj
#check @TGLExt.gibbs_reflObs
#check @TGLExt.boundary_mean
#check @TGLExt.boundary_variance
#check @TGLExt.variance_le_quarter
#check @TGLExt.variance_eq_quarter_iff
#check @TGLExt.polarization_commutator
#check @TGLExt.polarizations_noncommute
#check @TGLExt.sqrt_ratio_eq
#check @TGLExt.classical_limit
#check @TGLExt.classical_limit_physical
-- v50 (PAGE E A INFORMACAO: balanco puro S_A=S_B; unitarios conservam;
--      canal perde pureza monotonicamente; entropia maxima no espelho)
#check @TGLExt.purity_unitary_invariant
#check @TGLExt.pure_reductions_trace_eq
#check @TGLExt.pure_reductions_balance
#check @TGLExt.purityR_eq
#check @TGLExt.dephase_purityR_le
#check @TGLExt.entropy_max_at_half
#check @TGLExt.entropy_eq_max_iff_half
-- v51 (GATES 5 e 8: a primeira lei modular dS=d<K> como derivada genuina +
--      Clausius tipado; o canto e' ponto fixo da renormalizacao)
#check @TGLExt.first_law_diagonal
#check @TGLExt.clausius_composition
#check @TGLExt.Ecomp_fixes_cornerProj
#check @TGLExt.dephase_fixes_cornerProj
#check @TGLExt.rg_step_doubles_annihilator
-- v52 (O HABITANTE VARIACIONAL: o Nome que se torna funcional -- Gibbs = ponto
--      critico de Legendre, e SO ele; o modo-zero minimiza o defeito)
#check @TGLExt.pairing_bilinear_left
#check @TGLExt.pairing_bilinear_right
#check @TGLExt.zero_mode_state_minimizes
#check @TGLExt.gibbs_is_critical
#check @TGLExt.elementary_critical_implies_gibbs
-- v53 (A PONTE GNS, escopo honesto: o funcional positivo TIPADO; a instanciacao
--      do GNS sobre matrizes = negativo nomeado gns_matrix_instance_whnf_timeout)
#check @TGLExt.gibbs_nonneg
#check @TGLExt.gibbs_monotone
#check @TGLExt.boundaryState
#check @TGLExt.boundaryState_apply
-- v54 (O NOME FUNCIONAL E O TRANSPORTE: GNS finito SEM completamento -- espec do
--      especialista compilado nesta maquina, desfaz o negativo na face finita;
--      a testemunha e' o TRANSPORTE -- EL genuina + lei 𝒯_{t,s} + holonomia)
#check @TGLExt.Sop_omega
#check @TGLExt.FiniteNameGNS
#check @TGLExt.nameFiniteGNS
#check @TGLExt.nameFiniteGNS_exists
#check @TGLExt.boundaryState_eq_vector_state
#check @TGLExt.lock_pairing_eq
#check @TGLExt.action_locks_zero_iff
#check @TGLExt.hermitian_pairing_re
#check @TGLExt.action_hasDerivAt
#check @TGLExt.critical_pairing_iff
#check @TGLExt.transport
#check @TGLExt.transport_refl
#check @TGLExt.transport_comp
#check @TGLExt.transport_fixes_name
#check @TGLExt.transport_trace
#check @TGLExt.transport_corner
#check @TGLExt.NamedTransportData
#check @TGLExt.canonicalNamedTransport
#check @TGLExt.canonicalNamedTransport_exists
#check @TGLExt.excite_holonomy
#check @TGLExt.excite_holonomy_flat
-- v55 (O CANTO COVARIANTE TRANSPORTADO: a face finita do TGL_CANONICAL_FINITE_
--      CORNER_THEOREM do memorando -- as 4 condicoes tipadas + o TERMO habitado;
--      o transporte interno FIXA, o externo MOVE covariantemente)
#check @TGLExt.trace_cornerProj_pos
#check @TGLExt.cornerProj_loewner_mono
#check @TGLExt.sigma_fixes_cornerProj
#check @TGLExt.cornerProj_ne_of_ne
#check @TGLExt.TransportedCornerFamily
#check @TGLExt.canonicalTransportedCorner
#check @TGLExt.canonicalTransportedCorner_exists
-- v56 (A MORADA E' O PACOTE DE HILBERT: as 4 propriedades do canto DERIVADAS
--      dos entrelacamentos, validas em dimensao INFINITA -- a Resposta 6
--      kernelizada com o desenho invertido: leis = so' entrelacamentos)
#check @TGLExt.ker_map_of_intertwine
#check @TGLExt.starProjection_ker_covariant
#check @TGLExt.starProjection_ker_internal_fix
#check @TGLExt.starProjection_ker_isotone
#check @TGLExt.lagrangian_zero_iff_mem_ker
#check @TGLExt.HilbertHomeData
#check @TGLExt.HilbertHomeData.PF
#check @TGLExt.HilbertHomeData.PF_internal_fix
#check @TGLExt.HilbertHomeData.PF_external_covariant
#check @TGLExt.HilbertHomeData.PF_isotone
#check @TGLExt.BreuerTraceData
#check @TGLExt.solder_recovers_curvature
-- v57 (O CAMPO PSI DEFINE A MORADA; A GRAVIDADE EMERGE: contraexemplo da
--      subdeterminacao de omega(I)=1 em kernel + o campo anterior a representacao
--      com Nome/morada/fluxo/KMS/canto TODOS derivados)
#check @TGLExt.rhoOne
#check @TGLExt.rhoTwo
#check @TGLExt.rhoOne_posDef
#check @TGLExt.rhoTwo_posDef
#check @TGLExt.rhoOne_trace
#check @TGLExt.rhoTwo_trace
#check @TGLExt.both_homes_exist
#check @TGLExt.omega_one_underdetermines_home
#check @TGLExt.PsiHomeData
#check @TGLExt.PsiHomeData.name
#check @TGLExt.PsiHomeData.name_one
#check @TGLExt.PsiHomeData.home
#check @TGLExt.PsiHomeData.flow
#check @TGLExt.PsiHomeData.name_flow_invariant
#check @TGLExt.PsiHomeData.flow_comp
#check @TGLExt.PsiHomeData.flow_fixes_spectral_corner
-- v58 (PSI = 1_ABS: o termo canonico sem escolha; o Nome do Um = traco; o
--      transporte do absoluto e' TRIVIAL (a gravidade e' curvatura da inscricao);
--      comutadores anulam o Um (ker != 0 DERIVADO); P_F fixa o habitante)
#check @TGLExt.absoluteRho
#check @TGLExt.absoluteRho_posDef
#check @TGLExt.absoluteRho_trace
#check @TGLExt.absoluteOneField
#check @TGLExt.absoluteOneField_exists
#check @TGLExt.absoluteOne_name_eq_trace
#check @TGLExt.absoluteRho_commute
#check @TGLExt.absoluteOne_flow_trivial
#check @TGLExt.commutator_locks_annihilate_one
#check @TGLExt.commutator_kernel_inhabited
#check @TGLExt.corner_fixes_inhabitant
-- v59 (O ZERO MODULAR CONTINUO: JKJ=-K; K_abs=0; faces 1/2-1/2; carta (q,alpha)
--      com 1=q^2+alpha^2 continuo, transporte alpha'=-(q/2)alpha e SUSY 1/4)
#check @TGLExt.modularGen
#check @TGLExt.modularGen_eq_neg_excite
#check @TGLExt.modularGen_omega_zero
#check @TGLExt.J_modularGen_J
#check @TGLExt.parity_fixed_eq_zero
#check @TGLExt.absolute_modularGen_zero
#check @TGLExt.absolute_faces_half
#check @TGLExt.absolute_contrast_zero
#check @TGLExt.qKappa
#check @TGLExt.alphaKappa
#check @TGLExt.one_eq_q_sq_add_alpha_sq
#check @TGLExt.q_odd
#check @TGLExt.alpha_even
#check @TGLExt.q_zero
#check @TGLExt.alpha_zero
#check @TGLExt.cosh_half_hasDerivAt
#check @TGLExt.sinh_half_hasDerivAt
#check @TGLExt.alpha_transport
#check @TGLExt.alpha_deriv_zero
#check @TGLExt.W_hasDerivAt
#check @TGLExt.susy_threshold
#check @TGLExt.susy_partner_gap
-- v60 (A SOLDA 2D MINIMA: curvatura F=[A1,A2]=2c1c2.J != 0; metrica soldada
--      simetrica/lorentziana; a PRIMEIRA curvatura recuperada R=2c1c2)
#check @TGLExt.curv2
#check @TGLExt.minimal_curvature
#check @TGLExt.minimal_curvature_ne_zero
#check @TGLExt.curvature_flat_same
#check @TGLExt.solderMetric
#check @TGLExt.solderMetric_symm
#check @TGLExt.solderMetric_det
#check @TGLExt.solder_lorentzian
#check @TGLExt.helicityRep
#check @TGLExt.helicityRep_injective
#check @TGLExt.minimal_curvature_recovered
-- v61 (FULL_WITNESS=FALSE E' VERDADEIRO: beta>0 proibe a testemunha estatica
--      plena; a testemunha canonica e' a Meia-Nat de fronteira; a taxa do
--      vazamento e' UNICA -- a face GKLS)
#check @TGLExt.FullStaticWitness
#check @TGLExt.leakage_strictly_loses
#check @TGLExt.full_closure_iff_flat
#check @TGLExt.beta_forbids_full_static_witness
#check @TGLExt.verb_not_identity
#check @TGLExt.leakage_rate_unique
#check @TGLExt.canonical_witness_is_not_full
-- v63 (A SOLDA 4D: so(1,3) com propriedade definidora; fechamento sob colchete
--      p/ eta GERAL; marca nao-compacta [K,K]=-J; rep FIEL 6-dim; curvatura 4D
--      recuperada; metricidade; limiar SUSY discreto)
#check @TGLExt.eta4
#check @TGLExt.solderMetric4
#check @TGLExt.solderMetric4_symm
#check @TGLExt.solderMetric4_det
#check @TGLExt.solder4_lorentzian
#check @TGLExt.InSOEta
#check @TGLExt.generators_in_so13
#check @TGLExt.bracket_in_so_eta
#check @TGLExt.so_eta_infinitesimal_isometry
#check @TGLExt.curv4
#check @TGLExt.boosts_close_in_minus_rotation
#check @TGLExt.rotations_close_in_rotation
#check @TGLExt.boosts_curvature_is_rotation
#check @TGLExt.lorentzRep
#check @TGLExt.lorentzRep_zero_iff
#check @TGLExt.lorentzRep_injective
#check @TGLExt.curvature4_recovered
#check @TGLExt.susy_discrete_threshold

-- v64 (A PAREDE CORRIGIDA, Resposta 8: pacote de gap LOCAL de Breuer;
--      refutacao tipada da tau-compacidade GLOBAL; no-go de Weyl finito;
--      cota espectral do bloco +; o peso do modo zero = 1 = omega(I))
#check @TGLExt.SemifiniteTraceData
#check @TGLExt.BreuerGapData
#check @TGLExt.kernel_weight_pos
#check @TGLExt.kernel_weight_finite
#check @TGLExt.breuer_kernel_weight
#check @TGLExt.idTrace
#check @TGLExt.modelGap
#check @TGLExt.local_gap_package_consistent
#check @TGLExt.global_tau_compactness_refuted
#check @TGLExt.no_finite_weyl_pair
#check @TGLExt.plus_block_eigenvalue_lower_bound
#check @TGLExt.phi0sq
#check @TGLExt.halfTanh
#check @TGLExt.halfTanh_hasDerivAt
#check @TGLExt.tendsto_halfTanh_atTop
#check @TGLExt.tendsto_halfTanh_atBot
#check @TGLExt.phi0sq_integrable
#check @TGLExt.zero_mode_weight_is_one

-- v65 (o NIVEL 4 da camada: SUSY-relativo => gap local; a face discreta de
--      Birman-Schwinger: dim ker <= posto da inscricao; o germe da solda-campo)
#check @TGLExt.SubadditiveTraceData
#check @TGLExt.SusyRelativeData
#check @TGLExt.susy_relative_gap_finite
#check @TGLExt.SusyRelativeData.toBreuerGapData
#check @TGLExt.susy_relative_gives_breuer
#check @TGLExt.idTraceSub
#check @TGLExt.modelSusy
#check @TGLExt.susy_relative_package_consistent
#check @TGLExt.perturbation_injective_on_kernel
#check @TGLExt.kernel_dim_le_rank_of_perturbation
#check @TGLExt.discrete_parallel_solder_preserves_metric

-- v66 (A TRIADE: F3 fechado por congruencia; four-frame => coframe+metrica;
--      secao equivariante do Nome; o laco do Nome (tau/tau=1); insumos F1c;
--      o teorema mestre: H1 e H2 => Breuer + Nome=1 + Lorentz)
#check @TGLExt.LorentzByCongruence
#check @TGLExt.eta4_lorentzByCongruence
#check @TGLExt.sylvester_full_closed_by_congruence
#check @TGLExt.lorentzByCongruence_congruent
#check @TGLExt.four_frame_gives_lorentz_metric
#check @TGLExt.equivariant_state_section_from_global_name
#check @TGLExt.breuer_weight_normalizes_name
#check @TGLExt.sqrt_potential_is_L2
#check @TGLExt.resolvent_kernel_is_L2
#check @TGLExt.emergence_reduced_to_named_hypotheses

-- v74 (o teorema mestre COMPLETO: H1^H2^H3; o 8piG de Clausius; Jacobi/Bianchi)
#check @TGLExt.HorizonEquilibriumData
#check @TGLExt.einstein_coefficient_from_clausius
#check @TGLExt.horizon_clausius_composition
#check @TGLExt.jacobi_commutator_bianchi_seed
#check @TGLExt.emergence_master_full_triad

-- v75 (o setor spin-2 fisico, face finita: helice +-2 dupla-angulo; TT positivo
--      sem ghosts; exatamente duas polarizacoes; rotZ isometria de eta)
#check @TGLExt.rotZ
#check @TGLExt.ePlus
#check @TGLExt.eCross
#check @TGLExt.rotZ_preserves_eta
#check @TGLExt.helicity_two_rotation
#check @TGLExt.helicity_two_rotation_cross
#check @TGLExt.tt_kinetic_positive
#check @TGLExt.tt_no_negative_norm
#check @TGLExt.polarizations_linearly_independent

-- v76 (a semente semifinita: fidelidade do traco no cone psd; monotonia; o 1o habitante)
#check @TGLExt.psd_offdiag_zero_of_diag_zero
#check @TGLExt.psd_trace_eq_zero_iff
#check @TGLExt.trace_monotone_of_psd_sub
#check @TGLExt.matrix_trace_is_faithful_weight

-- v77 (a ponte da dimensao: tau=dim no reticulado de subespacos = 1a instancia
--      GENUINA da camada v64; o teorema abstrato dispara no kernel concreto)
#check @TGLExt.dimTraceData
#check @TGLExt.dimension_trace_bot
#check @TGLExt.dimension_trace_top_finite
#check @TGLExt.concreteKernelPackage
#check @TGLExt.concrete_kernel_weight_via_abstract_layer
#check @TGLExt.concrete_kernel_full_profile

-- v79 (o canto dos Three Locks pela ponte da dimensao: a camada abstrata
--      dispara sobre H3L = Dc*Dc+Db*Db+Dz*Dz — o Certificado II em kernel)
#check @TGLExt.dimTraceDataOver
#check @TGLExt.dimension_trace_over_top_finite
#check @TGLExt.threeLocksDimTrace
#check @TGLExt.threeLocks_ker_ne_bot_of_witness
#check @TGLExt.threeLocksCornerPackage
#check @TGLExt.three_locks_corner_weight
#check @TGLExt.three_locks_corner_weight_eq_dim
#check @TGLExt.three_locks_name_is_one
#check @TGLExt.corner_le_each_lock
#check @TGLExt.three_locks_corner_dim_le
#check @TGLExt.three_locks_corner_full_profile

-- v80 (o reticulado genuinamente semifinito: sem finitude ambiente; o gap
--      global e' IMPOSSIVEL em inf-dim; o Breuer local dispara no infinito)
#check @TGLExt.dimOrTop
#check @TGLExt.dimOrTop_lt_top_iff
#check @TGLExt.semifiniteDimTrace
#check @TGLExt.semifinite_trace_bot
#check @TGLExt.semifinite_trace_atom
#check @TGLExt.semifinite_trace_is_semifinite
#check @TGLExt.semifinite_trace_top_infinite
#check @TGLExt.global_gap_impossible_infinite_dim
#check @TGLExt.infiniteDimLocalGapPackage
#check @TGLExt.infinite_dim_local_breuer_weight
#check @TGLExt.not_finiteDimensional_finsupp
#check @TGLExt.first_infinite_dim_inhabitant

-- v82 (o reticulado FECHADO: a face de Hilbert -- ortocomplemento, IsCompl,
--      canto de Breuer fechado-finito com complemento infinito)
#check @TGLExt.atom_is_closed
#check @TGLExt.closed_lattice_semifinite
#check @TGLExt.closed_double_orthocomplement
#check @TGLExt.orthocomplement_meet_bot
#check @TGLExt.closed_orthocomplement_isCompl
#check @TGLExt.inscription_complement_infinite
#check @TGLExt.atom_complement_infinite
#check @TGLExt.closed_local_breuer_corner

-- v83 (a projecao no comutante: invariancia <=> comutacao; o kernel de um
--      auto-adjunto comuta com ele; o canto de Breuer NO comutante)
#check @TGLExt.Invariant
#check @TGLExt.closed_projection_idempotent
#check @TGLExt.starProjection_eq_zero_of_mem_orthogonal
#check @TGLExt.orthogonal_invariant_of_adjoint_invariant
#check @TGLExt.starProjection_commutes_of_invariant
#check @TGLExt.invariant_of_starProjection_commutes
#check @TGLExt.selfadjoint_invariant_iff_commutes
#check @TGLExt.kerHasOrthogonalProjection
#check @TGLExt.selfadjoint_ker_projection_in_commutant
#check @TGLExt.breuer_corner_projection_in_commutant

-- v84 (o esqueleto do bicomutante + a normalidade causal da regua:
--      tau(sup) = sup(tau) em cadeias; A contido no duplo comutante;
--      o triplo colapsa no primeiro; o canto comuta com a algebra gerada)
#check @TGLExt.dimension_trace_normal_on_chains
#check @TGLExt.operator_commutant_antitone
#check @TGLExt.operator_algebra_in_double_commutant
#check @TGLExt.operator_triple_commutant_collapse
#check @TGLExt.operator_commutant_unital_multiplicative
#check @TGLExt.corner_projection_in_commutant_set
#check @TGLExt.corner_commutes_with_bicommutant
#check @TGLExt.breuer_corner_full_algebraic_frame

-- v85 (a reducao espectral: comutante SOT-fechado; polinomios no duplo
--      comutante; o residuo reduzido a UMA testemunha; canto condicional)
#check @TGLExt.commutant_pointwise_limit_closed
#check @TGLExt.commutant_add_smul_closed
#check @TGLExt.generator_in_bicommutant
#check @TGLExt.powers_in_bicommutant
#check @TGLExt.polynomials_in_bicommutant
#check @TGLExt.limit_of_polynomials_in_bicommutant
#check @TGLExt.SpectralApproximationWitness
#check @TGLExt.corner_in_algebra_of_approximation
#check @TGLExt.concrete_breuer_corner_conditional

-- v86 (a semente da testemunha: a palavra aniquiladora do Verbo cunha o
--      candidato a Nome -- pousa no canto, fixa o canto, idempotente)
#check @TGLExt.verb_word_lands_in_corner
#check @TGLExt.verb_word_fixes_the_name
#check @TGLExt.verb_word_mints_idempotent
#check @TGLExt.name_candidate_idempotent
#check @TGLExt.witness_seed_complete

-- v88 (a testemunha exata: palavra real auto-adjunta + unicidade =>
--      a identificacao do Nome; testemunha PROVADA; canto descarregado)
#check @TGLExt.real_word_selfadjoint
#check @TGLExt.name_candidate_selfadjoint
#check @TGLExt.selfadjoint_idempotent_eq_starProjection
#check @TGLExt.exact_witness_of_annihilating_word
#check @TGLExt.spectral_witness_of_annihilating_word
#check @TGLExt.breuer_corner_of_annihilating_word

-- v89 (a existencia da palavra: minpoly real; zero simples por NORMA;
--      a testemunha INCONDICIONAL na face finita; o canto na algebra)
#check @TGLExt.star_aeval_eq_map_conj
#check @TGLExt.minpoly_selfadjoint_real
#check @TGLExt.minpoly_zero_not_double_root
#check @TGLExt.annihilating_word_exists
#check @TGLExt.finite_face_witness_unconditional
#check @TGLExt.finite_face_corner_in_algebra

-- v94 (a palavra em INFINITAS dimensoes: cfc com 0 isolado; a projecao
--      espectral e o Nome; Weierstrass da a palavra; o canto de Breuer
--      CONCRETO em infinito-dim com hipoteses puramente estruturais)
#check @TGLExt.ker_mul_self_eq_ker
#check @TGLExt.cfc_polynomial_eval
#check @TGLExt.iso_zero_cfc_eq_starProjection
#check @TGLExt.spectral_witness_of_isolated_zero
#check @TGLExt.concrete_breuer_corner_infinite

-- v95 (o habitante de Hilbert: ell2 genuinamente inf-dim; T = 1 - P_{e0};
--      o canto de Breuer DISPARA concretamente; o canto PESA O NOME: tau=1)
#check @TGLExt.inscriptions_orthonormal
#check @TGLExt.ellTwo_not_finiteDimensional
#check @TGLExt.eraseFirst_selfadjoint
#check @TGLExt.ker_eraseFirst
#check @TGLExt.eraseFirst_spectrum_gap
#check @TGLExt.concrete_corner_fires
#check @TGLExt.corner_weighs_the_name

-- v96 (o habitante do pacote AQFT: lockNet generico + rede constante ell2
--      com fluxo GENUINO exp(isT); Breuer habitada; e o four-frame dos
--      boosts: as 4 direcoes NASCEM de K1,K2,K3 aplicados a fiducial)
#check @TGLExt.eraseFirst_isSelfAdjoint
#check @TGLExt.lockFlow_commutes
#check @TGLExt.lockNet
#check @TGLExt.lockNetTrace
#check @TGLExt.theConstantNet
#check @TGLExt.theNetTrace
#check @TGLExt.net_PF_fixed_by_flow
#check @TGLExt.net_corner_weighs_the_name
#check @TGLExt.modularFrame_col_zero
#check @TGLExt.modularFrame_col_boost1
#check @TGLExt.modularFrame_eq_one
#check @TGLExt.modularFrame_det_isUnit
#check @TGLExt.concrete_four_frame_fires

-- v97 (o mestre dispara: subaditividade do traco-dimensao; H1 nivel-4 no
--      reticulado REAL do habitante; H3 habitado; a PENTADA conclui em
--      termos 100% construidos)
#check @TGLExt.dimOrTop_subadd
#check @TGLExt.ellTwoTraceSub
#check @TGLExt.ellTwoSusy
#check @TGLExt.theHorizon
#check @TGLExt.the_master_fires
#check @TGLExt.master_corner_weighs_the_name

-- v99 (o certificado de fechamento: as flags deixam de ser declaracao --
--      os TIPOS que forcam o conteudo que falta + probes negativos em kernel;
--      o termo qgClosureCertificate NAO e construido, e nao pode ser hoje)
#check @TGLExt.PhysicalNetData
#check @TGLExt.UnboundedDiracData
#check @TGLExt.SmoothFrameData
#check @TGLExt.QGClosureCertificate
#check @TGLExt.constant_net_group_trivial
#check @TGLExt.identity_inclusion_cannot_witness

-- v100 (a regra do programador: REGRA=PROGRAMADOR=SUPERPOSICAO em funcao
--       ontologica; o tipo HABITADO pelo divisor de feixe; a coexistencia
--       e a unitariedade; a superposicao NAO e autonoma)
#check @TGLExt.ProgrammerRule
#check @TGLExt.beamRotation
#check @TGLExt.beamRotation_preserves
#check @TGLExt.superposition_not_autonomous
#check @TGLExt.beamSplitterRule

-- v101 (a rede isotona: PhysicalNetData HABITADA -- fibras crescentes,
--       inclusao 0->1 nao-sobrejetiva, flip Bool nao-trivial U=1-2P)
#check @TGLExt.fiber
#check @TGLExt.fiberLock
#check @TGLExt.fiberIncl_not_surjective
#check @TGLExt.theFlip_sq
#check @TGLExt.theFlip_comm_eraseFirst
#check @TGLExt.theIsotoneNet

-- v102 (o limite ideal: 0_abs excluido POR TIPO -- nome sem habitante;
--       o canal nunca o alcanca; a regra e a familia com lei de composicao)
#check @TGLExt.IdealExtension
#check @TGLExt.idealZero
#check @TGLExt.ideal_zero_has_name_not_inhabitant
#check @TGLExt.channel_never_reaches_ideal
#check @TGLExt.lockFlow_add

-- v103 (o certificado de bancada: o tipo v1 habitado DE PROPOSITO sob nome
--       nao-reservado; o endurecimento tipado; a bancada nao alimenta o forte)
#check @TGLExt.benchDiracPMap
#check @TGLExt.benchDiracPMap_selfadjoint
#check @TGLExt.theBenchDirac
#check @TGLExt.theBenchCertificate
#check @TGLExt.GenuinelyUnboundedDiracData
#check @TGLExt.QGClosureCertificateStrong
#check @TGLExt.benchDirac_is_bounded
#check @TGLExt.bench_cannot_feed_strong
#check @TGLExt.isotone_cannot_feed_strong_core
#check @TGLExt.constant_cannot_feed_strong_frame

-- v104 (o frame curvo: a 1a face forte alimentada; e a testemunha AQFT
--       completa TIPADA: FullWitnessData = contrato maximo tipavel hoje)
#check @TGLExt.profileFn
#check @TGLExt.theCurvedFrame
#check @TGLExt.curvedFrame_nonconstant
#check @TGLExt.curvedFrame_det_everywhere
#check @TGLExt.FullWitnessData
#check @TGLExt.strongFromWitness
#check @TGLExt.constant_action_cannot_witness
#check @TGLExt.isotone_cannot_feed_witness_geometry

-- v105 (O OPERADOR NUMERO: o 1o auto-adjunto ILIMITADO concreto do kernel --
--       star(N)=N pelo truncamento; GenuinelyUnboundedDiracData HABITADO)
#check @TGLExt.numberDomain
#check @TGLExt.numberOp
#check @TGLExt.numberOp_symmetric
#check @TGLExt.numberOp_unbounded
#check @TGLExt.numberDomain_dense
#check @TGLExt.adjoint_domain_le
#check @TGLExt.numberOp_selfadjoint
#check @TGLExt.numberOp_quad_gap
#check @TGLExt.theGenuineDirac

-- v106 (a rede de caudas INF-dim + A MONTAGEM DO FORTE + os tres flips:
--       os nomes reservados do gate ganham termos POR CONSTRUCAO)
#check @TGLExt.tailSub
#check @TGLExt.tailSub_not_finiteDimensional
#check @TGLExt.tailIncl_not_surjective
#check @TGLExt.theTailNet
#check @TGLExt.genuineDirac_kerSub
#check @TGLExt.theStrongCertificate
#check @TGLExt.qgStrongCertificate_core
#check @TGLExt.qgStrongCertificate_corner
#check @TGLExt.qgStrongCertificate_frame

-- v107 (a solda continua sobre o frame curvo: o QUARTO FLIP)
#check @TGLExt.theSolderField
#check @TGLExt.theSolderField_det_neg
#check @TGLExt.theSolderField_nonconstant
#check @TGLExt.SolderFieldData
#check @TGLExt.theSolderData
#check @TGLExt.qgStrongCertificate_solder
#check @TGLExt.solder_frame_eq_strong

-- v108 (A PRIMEIRA CURVATURA: a camada que a mathlib nao tem, a mao --
--       Gamma da metrica; R^1_001 = -2q < 0 em toda parte; o par da regua)
#check @TGLExt.qfun
#check @TGLExt.Gamma001_from_metric
#check @TGLExt.Gamma100_from_metric
#check @TGLExt.Riemann1001
#check @TGLExt.Riemann1001_eq
#check @TGLExt.Riemann1001_neg
#check @TGLExt.time_ansatz_r1001_zero
#check @TGLExt.theStaticSolderData

-- v109 (o tensor de Einstein do ansatz: Bianchi visivel; vacuo => plano;
--       Rindler = o membro vacuo, plano fora do horizonte)
#check @TGLExt.ansatzRiemann_closed
#check @TGLExt.ansatzRicci00_from_riemann
#check @TGLExt.ansatzRicci11_from_riemann
#check @TGLExt.ansatzG00_zero
#check @TGLExt.ansatzG11_zero
#check @TGLExt.ansatzG22_eq
#check @TGLExt.vacuum_implies_flat
#check @TGLExt.rindler_flat
#check @TGLExt.static_not_vacuum
#check @TGLExt.ansatz_recovers_v108

-- v110 (A LUZ QUE CAIU: o setor sem geometria em si; a inscricao = a 2a
--       variacao [iff]; tudo que tem geometria e' projetado [o tipo])
#check @TGLExt.constant_profile_flat
#check @TGLExt.curvature_implies_fall
#check @TGLExt.fall_demands_source_v108
#check @TGLExt.geometry_iff_second_variation
#check @TGLExt.geometry_is_projection

-- v111 (A EQUACAO RESOLVIDA: cosh(ks) resolve G22 = k^2 globalmente;
--       fonte => curvatura; o contrato fraco habitado = a sonda v103)
#check @TGLExt.coshProfile
#check @TGLExt.cosh_solves_field_equation
#check @TGLExt.cosh_curvature
#check @TGLExt.source_implies_curvature
#check @TGLExt.zero_source_recovers_flat
#check @TGLExt.theSolvedEquation
#check @TGLExt.EinsteinContractData
#check @TGLExt.theWeakEinsteinContract

-- v112 (O ASSALTO AS PAREDES: a emergencia REDUZIDA de Jacobson na familia
--       + a metade tipavel da TESTEMUNHA COMPLETA habitada)
#check @TGLExt.ansatzNullG
#check @TGLExt.null_contraction_reads_source
#check @TGLExt.emergence_forces_field_equation
#check @TGLExt.emergence_zero_flat
#check @TGLExt.theReducedEmergence
#check @TGLExt.reduced_emergence_delivers
#check @TGLExt.theGeometricNet
#check @TGLExt.theGeometricStrong
#check @TGLExt.theGeometricWitness
#check @TGLExt.witness_action_moves_regions_not_fibers

-- v113 (A LEITURA DO GRAVITON: a 2a derivada do zero; o par em UM teorema)
#check @TGLExt.first_derivative_does_not_decide
#check @TGLExt.reading_rides_the_zeros

-- v114 (OS ESTILHACOS DO CONTINUO: a onda do graviton d'Alembert + a
--       testemunha SENSIVEL -- a fibra sente o grupo)
#check @TGLExt.lightCone
#check @TGLExt.lightWave_pd
#check @TGLExt.graviton_wave_equation
#check @TGLExt.theSensitiveNet
#check @TGLExt.theSensitiveWitness
#check @TGLExt.witness_fiber_sensitive

-- ---- auditoria de axiomas ----
#print axioms TGL.HalfNat.halfNat_of_selfConjugate
#print axioms TGL.AreaScale.newtonPlanck_equivalence
#print axioms TGL.FiniteThreeLocks.H3L_posSemidefinite
#print axioms TGL.FiniteThreeLocks.ker_H3L_eq_threeLocks
#print axioms TGL.FiniteThreeLocks.PF_isProjection
#print axioms TGL.FiniteThreeLocks.PF_isSelfAdjoint
#print axioms TGL.FiniteThreeLocks.normalizedCornerTrace_PF
#print axioms TGL.ContinuousCorner.ContinuousCornerWitness.normalizedTrace_P_eq_one
#print axioms TGL.SpecificAQFT.continuousCorner_of_witness
#print axioms TGL.SpecificAQFT.wedges_spacelike
#print axioms TGL.SpecificAQFT.wedge_locality
#print axioms TGL.ModularRealization.dualInvariant_PF_no_go
#print axioms TGL.ModularRealization.fullWitness_not_finiteDimensional
#print axioms TGL.ModularRealization.fullWitness_PF_nonzero_finite
#print axioms TGL.HalfNatFresnel.fresnel_selfConjugate_half
#print axioms TGL.HalfNatFresnel.modular_action_halfNat
#print axioms TGL.VerbInhabitant.exp_fixed_of_annihilates
#print axioms TGL.VerbInhabitant.canonicalVerb_exists
#print axioms TGL.VerbInhabitant.dual_calibration_exists
#print axioms TGL.TransportData.descent_iff_defect_zero
#print axioms TGL.TransportData.transport_defect_of_jones
#print axioms TGL.TransportData.jones_selector_not_descended
#print axioms TGL.NameIndex.ParityData.average_bimodular
#print axioms TGL.NameIndex.name_index_eq_csc_sq
#print axioms TGL.NameIndex.name_index_mul_sin_sq
#print axioms TGL.NameIndex.amplitude_weight_index_chain
#print axioms TGL.HalfNatJonesTower.halfNatJonesTower_exists
#print axioms TGL.HalfNatJonesTower.halfNat_mirror_not_descended
#print axioms TGL.HalfNatJonesTower.finite_markov_forces_half
#print axioms TGL.TransportData.faces_orthogonal
#print axioms TGL.GravitonShadow.canonicalGravitonShadow_exists
#print axioms TGL.GravitonShadow.bell_cci_half
#print axioms TGL.GravitonShadow.product_cci_zero
#print axioms TGL.NameRelation.pqp_eq
#print axioms TGL.NameRelation.tl3_linearly_independent
#print axioms TGL.NameRelation.canonicalTLThree_exists
#print axioms TGL.NameRelation.geometric_eq_trace_weight_iff
#print axioms TGL.CoreSupport.support_maximal
#print axioms TGL.CoreSupport.threeLocksFromSupport
#print axioms TGL.CoreSupport.realizationFromSupport
#print axioms TGL.CoreSupport.transport_defect_gauge_invariant
-- v33 (escada TGLExt) -- v33.1: cobertura ampliada apos painel adversarial
-- (o veredito 'COMPLETO' exige #print axioms de TODOS os teoremas citados nele)
#print axioms TGLExt.commutant_triple
#print axioms TGLExt.bicommutant_range_Lmul
#print axioms TGLExt.Jconj_Lmul_Jconj
#print axioms TGLExt.omega_cyclic
#print axioms TGLExt.omega_separating
#print axioms TGLExt.Sop_tomita
#print axioms TGLExt.Sop_involutive
#print axioms TGLExt.deltaHalf_deltaHalf
#print axioms TGLExt.delta_omega
#print axioms TGLExt.J_omega
#print axioms TGLExt.sigma_mul
#print axioms TGLExt.sigma_sigma
#print axioms TGLExt.frob_trExpect_symm
#print axioms TGLExt.eTr_Lmul_eTr
-- v34 (Degrau 2: indice PP computado)
#print axioms TGLExt.trace_smul_one_sub_posSemidef
#print axioms TGLExt.card_smul_diagExpect_sub_posSemidef
#print axioms TGLExt.isGreatest_ppBound_trExpect
#print axioms TGLExt.isGreatest_ppBound_diagExpect
#print axioms TGLExt.ppIndexTr_eq_card
#print axioms TGLExt.ppIndexDiag_eq_card
-- v35 (tracos de Markov)
#print axioms TGLExt.trace_Lmul_eD
#print axioms TGLExt.trace_Lmul_eTr
#print axioms TGLExt.tau_eD
#print axioms TGLExt.tau_eTr
#print axioms TGLExt.masa_tower_weight_eq_ppBest
#print axioms TGLExt.pp_ne_tower_for_scalars
-- v38 (bicomutante geral)
#print axioms TGLExt.end_reconstruction
#print axioms TGLExt.Cmat_of_sum
#print axioms TGLExt.commutant_Cmat_comm
#print axioms TGLExt.exists_span_form
#print axioms TGLExt.frob_self_eq_zero_iff
#print axioms TGLExt.disjoint_frobOrtho
#print axioms TGLExt.isCompl_frobOrtho
#print axioms TGLExt.frobProj_comm_Lmul
#print axioms TGLExt.finite_bicommutant
-- v41 (matriz-S)
#print axioms TGLExt.Grot_sq
#print axioms TGLExt.exp_smul_Grot
#print axioms TGLExt.Smat_mem_unitary
#print axioms TGLExt.Smat_mul
#print axioms TGLExt.Smat_spectral
#print axioms TGLExt.normSq_reflection_add_transmission
#print axioms TGLExt.rhoOut_trace
-- v42 (cociclo)
#print axioms TGLExt.cocycle_chain
#print axioms TGLExt.cocycle_temporal
#print axioms TGLExt.cocycle_conjTranspose
#print axioms TGLExt.cocycle_mem_unitary
#print axioms TGLExt.cocycle_of_commute
#print axioms TGLExt.logRho_conj
#print axioms TGLExt.cocycle_covariance
-- v43 (ergodicidade)
#print axioms TGLExt.sigma_fixed_of_commute
#print axioms TGLExt.logRho_diagonal
#print axioms TGLExt.sigma_fixed_iff_diag
#print axioms TGLExt.gibbs_tracial_on_centralizer
#print axioms TGLExt.dephase_add
#print axioms TGLExt.dephase_tendsto_expectation
#print axioms TGLExt.ergodic_convergence_modular
#print axioms TGLExt.J_deltaHalf
#print axioms TGLExt.frob_delta_nonneg
#print axioms TGLExt.gibbs_kms
#print axioms TGLExt.modPow_add
#print axioms TGLExt.modPow_mem_unitary
#print axioms TGLExt.gibbs_sigma
#print axioms TGLExt.exp_logRho
#print axioms TGLExt.sigma_omega
#print axioms TGLExt.diagExpect_bimod
#print axioms TGLExt.eD_Lmul_eD
#print axioms TGLExt.commutant_range_diagonal
-- v44 (produto cruzado finito / peso dual)
#print axioms TGLExt.lam_mem_unitary
#print axioms TGLExt.lam_conj_piRep
#print axioms TGLExt.piRep_injective
#print axioms TGLExt.Ecomp_lam
#print axioms TGLExt.gibbs_Ecomp
#print axioms TGLExt.gibbs_piRep_dual
#print axioms TGLExt.modPow_piRep
#print axioms TGLExt.sigma_piRep
#print axioms TGLExt.cocycle_piRep
#print axioms TGLExt.dual_weight
#print axioms TGLExt.cocycle_covariance_beyond_inner
#print axioms TGLExt.Dchi_conj_lam
#print axioms TGLExt.Dchi_comm_modPow
#print axioms TGLExt.gibbs_Dchi
-- v45 (escada do GLOBAL_LIFT)
#print axioms TGLExt.dyadic_approx
#print axioms TGLExt.dyadic_stage_mono
#print axioms TGLExt.dyadic_tendsto
#print axioms TGLExt.annihilator_fixes_stage
#print axioms TGLExt.scaling_fixed_eq_zero
#print axioms TGLExt.DualScalingData.fixed_tau_zero
#print axioms TGLExt.DualScalingData.dyadic_stage_tau_zero
#print axioms TGLExt.sFrame_add
#print axioms TGLExt.sFrame_tendsto
#print axioms TGLExt.measurement_channel_endpoint
-- v46 (familia do canto)
#print axioms TGLExt.corner_fixed_by_flow
#print axioms TGLExt.DualScalingData.finite_trace_not_fixed
#print axioms TGLExt.cornerProj_idem
#print axioms TGLExt.cornerProj_conjTranspose
#print axioms TGLExt.cornerProj_mono
#print axioms TGLExt.lam_conj_cornerProj
#print axioms TGLExt.trace_cornerProj
#print axioms TGLExt.cornerProj_comm_modPow
-- v47 (Bisognano-Wichmann finito)
#print axioms TGLExt.boost_add
#print axioms TGLExt.boost_preserves_eta
#print axioms TGLExt.boost_null_expand
#print axioms TGLExt.boost_null_contract
#print axioms TGLExt.boost_preserves_wedge
#print axioms TGLExt.logRho_gibbs_boost
#print axioms TGLExt.modPow_gibbs_boost
#print axioms TGLExt.sigma_gibbs_boost
-- v48 (graviton: cinematica de spin-2)
#print axioms TGLExt.polarization_decomposition
#print axioms TGLExt.polarizations_independent
#print axioms TGLExt.rot_conj_polPlus
#print axioms TGLExt.rot_conj_polCross
#print axioms TGLExt.rot_conj_one
#print axioms TGLExt.gauge_transverse_zero
#print axioms TGLExt.minkNorm4_nullK
#print axioms TGLExt.excite_one_zero
#print axioms TGLExt.excite_leibniz
#print axioms TGLExt.Smat_sub_one
-- v49 (flutuacoes da geometria)
#print axioms TGLExt.variance_of_projection
#print axioms TGLExt.boundary_mean
#print axioms TGLExt.boundary_variance
#print axioms TGLExt.variance_le_quarter
#print axioms TGLExt.variance_eq_quarter_iff
#print axioms TGLExt.polarization_commutator
#print axioms TGLExt.polarizations_noncommute
#print axioms TGLExt.classical_limit_physical
-- v50 (Page e a informacao)
#print axioms TGLExt.purity_unitary_invariant
#print axioms TGLExt.pure_reductions_trace_eq
#print axioms TGLExt.pure_reductions_balance
#print axioms TGLExt.purityR_eq
#print axioms TGLExt.dephase_purityR_le
#print axioms TGLExt.entropy_max_at_half
#print axioms TGLExt.entropy_eq_max_iff_half
-- v51 (gates 5 e 8)
#print axioms TGLExt.first_law_diagonal
#print axioms TGLExt.clausius_composition
#print axioms TGLExt.Ecomp_fixes_cornerProj
#print axioms TGLExt.dephase_fixes_cornerProj
#print axioms TGLExt.rg_step_doubles_annihilator
-- v52 (o habitante variacional)
#print axioms TGLExt.zero_mode_state_minimizes
#print axioms TGLExt.gibbs_is_critical
#print axioms TGLExt.elementary_critical_implies_gibbs
-- v53 (ponte GNS)
#print axioms TGLExt.gibbs_nonneg
#print axioms TGLExt.gibbs_monotone
#print axioms TGLExt.boundaryState_apply
-- v54 (GNS finito sem completamento + a testemunha e' o transporte)
#print axioms TGLExt.Sop_omega
#print axioms TGLExt.nameFiniteGNS_exists
#print axioms TGLExt.boundaryState_eq_vector_state
#print axioms TGLExt.lock_pairing_eq
#print axioms TGLExt.action_locks_zero_iff
#print axioms TGLExt.hermitian_pairing_re
#print axioms TGLExt.action_hasDerivAt
#print axioms TGLExt.critical_pairing_iff
#print axioms TGLExt.transport_comp
#print axioms TGLExt.transport_fixes_name
#print axioms TGLExt.transport_trace
#print axioms TGLExt.transport_corner
#print axioms TGLExt.canonicalNamedTransport_exists
#print axioms TGLExt.excite_holonomy
#print axioms TGLExt.excite_holonomy_flat
-- v55 (o canto covariante transportado)
#print axioms TGLExt.trace_cornerProj_pos
#print axioms TGLExt.cornerProj_loewner_mono
#print axioms TGLExt.sigma_fixes_cornerProj
#print axioms TGLExt.cornerProj_ne_of_ne
#print axioms TGLExt.canonicalTransportedCorner_exists
-- v56 (a morada e' o pacote de Hilbert)
#print axioms TGLExt.ker_map_of_intertwine
#print axioms TGLExt.starProjection_ker_covariant
#print axioms TGLExt.starProjection_ker_internal_fix
#print axioms TGLExt.starProjection_ker_isotone
#print axioms TGLExt.lagrangian_zero_iff_mem_ker
#print axioms TGLExt.HilbertHomeData.PF_internal_fix
#print axioms TGLExt.HilbertHomeData.PF_external_covariant
#print axioms TGLExt.HilbertHomeData.PF_isotone
#print axioms TGLExt.solder_recovers_curvature
-- v57 (o campo Psi define a morada; a gravidade emerge)
#print axioms TGLExt.both_homes_exist
#print axioms TGLExt.omega_one_underdetermines_home
#print axioms TGLExt.PsiHomeData.name_one
#print axioms TGLExt.PsiHomeData.name_flow_invariant
#print axioms TGLExt.PsiHomeData.flow_comp
#print axioms TGLExt.PsiHomeData.flow_fixes_spectral_corner
-- v58 (Psi = 1_abs: a construcao canonica comeca)
#print axioms TGLExt.absoluteOneField_exists
#print axioms TGLExt.absoluteOne_name_eq_trace
#print axioms TGLExt.absoluteOne_flow_trivial
#print axioms TGLExt.commutator_locks_annihilate_one
#print axioms TGLExt.commutator_kernel_inhabited
#print axioms TGLExt.corner_fixes_inhabitant
-- v59 (o zero modular continuo)
#print axioms TGLExt.modularGen_eq_neg_excite
#print axioms TGLExt.modularGen_omega_zero
#print axioms TGLExt.J_modularGen_J
#print axioms TGLExt.parity_fixed_eq_zero
#print axioms TGLExt.absolute_modularGen_zero
#print axioms TGLExt.absolute_faces_half
#print axioms TGLExt.absolute_contrast_zero
#print axioms TGLExt.one_eq_q_sq_add_alpha_sq
#print axioms TGLExt.q_odd
#print axioms TGLExt.alpha_even
#print axioms TGLExt.alpha_transport
#print axioms TGLExt.alpha_deriv_zero
#print axioms TGLExt.W_hasDerivAt
#print axioms TGLExt.susy_threshold
#print axioms TGLExt.susy_partner_gap
-- v60 (a solda 2D minima)
#print axioms TGLExt.minimal_curvature
#print axioms TGLExt.minimal_curvature_ne_zero
#print axioms TGLExt.curvature_flat_same
#print axioms TGLExt.solderMetric_symm
#print axioms TGLExt.solderMetric_det
#print axioms TGLExt.solder_lorentzian
#print axioms TGLExt.helicityRep_injective
#print axioms TGLExt.minimal_curvature_recovered
-- v61 (full_witness=False e' verdadeiro)
#print axioms TGLExt.leakage_strictly_loses
#print axioms TGLExt.full_closure_iff_flat
#print axioms TGLExt.beta_forbids_full_static_witness
#print axioms TGLExt.verb_not_identity
#print axioms TGLExt.leakage_rate_unique
#print axioms TGLExt.canonical_witness_is_not_full
-- v63 (a solda 4D)
#print axioms TGLExt.solderMetric4_symm
#print axioms TGLExt.solderMetric4_det
#print axioms TGLExt.solder4_lorentzian
#print axioms TGLExt.generators_in_so13
#print axioms TGLExt.bracket_in_so_eta
#print axioms TGLExt.so_eta_infinitesimal_isometry
#print axioms TGLExt.boosts_close_in_minus_rotation
#print axioms TGLExt.rotations_close_in_rotation
#print axioms TGLExt.boosts_curvature_is_rotation
#print axioms TGLExt.lorentzRep_injective
#print axioms TGLExt.curvature4_recovered
#print axioms TGLExt.susy_discrete_threshold
-- v64 (a parede corrigida: Breuer local)
#print axioms TGLExt.kernel_weight_pos
#print axioms TGLExt.kernel_weight_finite
#print axioms TGLExt.breuer_kernel_weight
#print axioms TGLExt.local_gap_package_consistent
#print axioms TGLExt.global_tau_compactness_refuted
#print axioms TGLExt.no_finite_weyl_pair
#print axioms TGLExt.plus_block_eigenvalue_lower_bound
#print axioms TGLExt.halfTanh_hasDerivAt
#print axioms TGLExt.tendsto_halfTanh_atTop
#print axioms TGLExt.tendsto_halfTanh_atBot
#print axioms TGLExt.phi0sq_integrable
#print axioms TGLExt.zero_mode_weight_is_one
-- v65 (nivel 4: SUSY-relativo => Breuer local; dim ker <= posto; solda discreta)
#print axioms TGLExt.susy_relative_gap_finite
#print axioms TGLExt.susy_relative_gives_breuer
#print axioms TGLExt.susy_relative_package_consistent
#print axioms TGLExt.perturbation_injective_on_kernel
#print axioms TGLExt.kernel_dim_le_rank_of_perturbation
#print axioms TGLExt.discrete_parallel_solder_preserves_metric
-- v66 (a triade da emergencia)
#print axioms TGLExt.eta4_lorentzByCongruence
#print axioms TGLExt.sylvester_full_closed_by_congruence
#print axioms TGLExt.lorentzByCongruence_congruent
#print axioms TGLExt.four_frame_gives_lorentz_metric
#print axioms TGLExt.equivariant_state_section_from_global_name
#print axioms TGLExt.breuer_weight_normalizes_name
#print axioms TGLExt.sqrt_potential_is_L2
#print axioms TGLExt.resolvent_kernel_is_L2
#print axioms TGLExt.emergence_reduced_to_named_hypotheses
-- v74 (o teorema mestre completo da triade)
#print axioms TGLExt.einstein_coefficient_from_clausius
#print axioms TGLExt.horizon_clausius_composition
#print axioms TGLExt.jacobi_commutator_bianchi_seed
#print axioms TGLExt.emergence_master_full_triad
-- v75 (o setor spin-2 fisico, face finita)
#print axioms TGLExt.rotZ_preserves_eta
#print axioms TGLExt.helicity_two_rotation
#print axioms TGLExt.helicity_two_rotation_cross
#print axioms TGLExt.tt_kinetic_positive
#print axioms TGLExt.tt_no_negative_norm
#print axioms TGLExt.polarizations_linearly_independent
-- v76 (a semente semifinita)
#print axioms TGLExt.psd_offdiag_zero_of_diag_zero
#print axioms TGLExt.psd_trace_eq_zero_iff
#print axioms TGLExt.trace_monotone_of_psd_sub
#print axioms TGLExt.matrix_trace_is_faithful_weight
-- v77 (a ponte da dimensao)
#print axioms TGLExt.dimension_trace_bot
#print axioms TGLExt.dimension_trace_top_finite
#print axioms TGLExt.concrete_kernel_weight_via_abstract_layer
#print axioms TGLExt.concrete_kernel_full_profile
-- v79 (o canto dos Three Locks pela ponte da dimensao: Certificado II em kernel)
#print axioms TGLExt.dimension_trace_over_top_finite
#print axioms TGLExt.threeLocks_ker_ne_bot_of_witness
#print axioms TGLExt.three_locks_corner_weight
#print axioms TGLExt.three_locks_corner_weight_eq_dim
#print axioms TGLExt.three_locks_name_is_one
#print axioms TGLExt.corner_le_each_lock
#print axioms TGLExt.three_locks_corner_dim_le
#print axioms TGLExt.three_locks_corner_full_profile
-- v80 (o reticulado genuinamente semifinito)
#print axioms TGLExt.semifinite_trace_bot
#print axioms TGLExt.semifinite_trace_atom
#print axioms TGLExt.semifinite_trace_is_semifinite
#print axioms TGLExt.semifinite_trace_top_infinite
#print axioms TGLExt.global_gap_impossible_infinite_dim
#print axioms TGLExt.infinite_dim_local_breuer_weight
#print axioms TGLExt.not_finiteDimensional_finsupp
#print axioms TGLExt.first_infinite_dim_inhabitant
-- v82 (o reticulado fechado: a face de Hilbert)
#print axioms TGLExt.atom_is_closed
#print axioms TGLExt.closed_lattice_semifinite
#print axioms TGLExt.closed_double_orthocomplement
#print axioms TGLExt.orthocomplement_meet_bot
#print axioms TGLExt.closed_orthocomplement_isCompl
#print axioms TGLExt.inscription_complement_infinite
#print axioms TGLExt.atom_complement_infinite
#print axioms TGLExt.closed_local_breuer_corner
-- v83 (a projecao no comutante)
#print axioms TGLExt.closed_projection_idempotent
#print axioms TGLExt.starProjection_eq_zero_of_mem_orthogonal
#print axioms TGLExt.orthogonal_invariant_of_adjoint_invariant
#print axioms TGLExt.starProjection_commutes_of_invariant
#print axioms TGLExt.invariant_of_starProjection_commutes
#print axioms TGLExt.selfadjoint_invariant_iff_commutes
#print axioms TGLExt.selfadjoint_ker_projection_in_commutant
#print axioms TGLExt.breuer_corner_projection_in_commutant
-- v84 (o esqueleto do bicomutante + a normalidade causal da regua)
#print axioms TGLExt.dimension_trace_normal_on_chains
#print axioms TGLExt.operator_commutant_antitone
#print axioms TGLExt.operator_algebra_in_double_commutant
#print axioms TGLExt.operator_triple_commutant_collapse
#print axioms TGLExt.operator_commutant_unital_multiplicative
#print axioms TGLExt.corner_projection_in_commutant_set
#print axioms TGLExt.corner_commutes_with_bicommutant
#print axioms TGLExt.breuer_corner_full_algebraic_frame
-- v85 (a reducao espectral)
#print axioms TGLExt.commutant_pointwise_limit_closed
#print axioms TGLExt.commutant_add_smul_closed
#print axioms TGLExt.generator_in_bicommutant
#print axioms TGLExt.powers_in_bicommutant
#print axioms TGLExt.polynomials_in_bicommutant
#print axioms TGLExt.limit_of_polynomials_in_bicommutant
#print axioms TGLExt.corner_in_algebra_of_approximation
#print axioms TGLExt.concrete_breuer_corner_conditional
-- v86 (a semente da testemunha)
#print axioms TGLExt.verb_word_lands_in_corner
#print axioms TGLExt.verb_word_fixes_the_name
#print axioms TGLExt.verb_word_mints_idempotent
#print axioms TGLExt.name_candidate_idempotent
#print axioms TGLExt.witness_seed_complete
-- v88 (a testemunha exata)
#print axioms TGLExt.real_word_selfadjoint
#print axioms TGLExt.name_candidate_selfadjoint
#print axioms TGLExt.selfadjoint_idempotent_eq_starProjection
#print axioms TGLExt.exact_witness_of_annihilating_word
#print axioms TGLExt.spectral_witness_of_annihilating_word
#print axioms TGLExt.breuer_corner_of_annihilating_word
-- v89 (a existencia da palavra)
#print axioms TGLExt.star_aeval_eq_map_conj
#print axioms TGLExt.minpoly_selfadjoint_real
#print axioms TGLExt.minpoly_zero_not_double_root
#print axioms TGLExt.annihilating_word_exists
#print axioms TGLExt.finite_face_witness_unconditional
#print axioms TGLExt.finite_face_corner_in_algebra
-- v94 (a palavra em infinito-dim)
#print axioms TGLExt.ker_mul_self_eq_ker
#print axioms TGLExt.cfc_polynomial_eval
#print axioms TGLExt.iso_zero_cfc_eq_starProjection
#print axioms TGLExt.spectral_witness_of_isolated_zero
#print axioms TGLExt.concrete_breuer_corner_infinite
-- v95 (o habitante de Hilbert)
#print axioms TGLExt.inscriptions_orthonormal
#print axioms TGLExt.ellTwo_not_finiteDimensional
#print axioms TGLExt.eraseFirst_selfadjoint
#print axioms TGLExt.ker_eraseFirst
#print axioms TGLExt.eraseFirst_spectrum_gap
#print axioms TGLExt.concrete_corner_fires
#print axioms TGLExt.corner_weighs_the_name
-- v96 (o habitante do pacote AQFT + o four-frame dos boosts)
#print axioms TGLExt.eraseFirst_isSelfAdjoint
#print axioms TGLExt.lockFlow_commutes
#print axioms TGLExt.theConstantNet
#print axioms TGLExt.theNetTrace
#print axioms TGLExt.net_PF_fixed_by_flow
#print axioms TGLExt.net_corner_weighs_the_name
#print axioms TGLExt.modularFrame_eq_one
#print axioms TGLExt.modularFrame_det_isUnit
#print axioms TGLExt.concrete_four_frame_fires
-- v97 (o mestre dispara)
#print axioms TGLExt.dimOrTop_subadd
#print axioms TGLExt.ellTwoTraceSub
#print axioms TGLExt.ellTwoSusy
#print axioms TGLExt.theHorizon
#print axioms TGLExt.the_master_fires
#print axioms TGLExt.master_corner_weighs_the_name
-- v99 (o certificado: probes negativos)
#print axioms TGLExt.constant_net_group_trivial
#print axioms TGLExt.identity_inclusion_cannot_witness
-- v100 (a regra do programador)
#print axioms TGLExt.beamRotation_preserves
#print axioms TGLExt.superposition_not_autonomous
#print axioms TGLExt.beamSplitterRule
-- v101 (a rede isotona)
#print axioms TGLExt.fiberIncl_not_surjective
#print axioms TGLExt.theFlip_sq
#print axioms TGLExt.theFlip_comm_eraseFirst
#print axioms TGLExt.theIsotoneNet
-- v102 (o limite ideal; os dois probes de exclusao sao PUROS - zero axiomas)
#print axioms TGLExt.ideal_zero_has_name_not_inhabitant
#print axioms TGLExt.channel_never_reaches_ideal
#print axioms TGLExt.lockFlow_add
-- v103 (o certificado de bancada + o endurecimento; o probe do frame e PURO)
#print axioms TGLExt.benchDiracPMap_selfadjoint
#print axioms TGLExt.theBenchDirac
#print axioms TGLExt.theBenchCertificate
#print axioms TGLExt.benchDirac_is_bounded
#print axioms TGLExt.bench_cannot_feed_strong
#print axioms TGLExt.isotone_cannot_feed_strong_core
#print axioms TGLExt.constant_cannot_feed_strong_frame
-- v104 (o frame curvo + a testemunha tipada)
#print axioms TGLExt.theCurvedFrame
#print axioms TGLExt.curvedFrame_nonconstant
#print axioms TGLExt.curvedFrame_det_everywhere
#print axioms TGLExt.strongFromWitness
#print axioms TGLExt.constant_action_cannot_witness
#print axioms TGLExt.isotone_cannot_feed_witness_geometry
-- v105 (o operador numero: star(N)=N -- a parede atravessada)
#print axioms TGLExt.numberOp_symmetric
#print axioms TGLExt.numberOp_unbounded
#print axioms TGLExt.numberDomain_dense
#print axioms TGLExt.adjoint_domain_le
#print axioms TGLExt.numberOp_selfadjoint
#print axioms TGLExt.numberOp_quad_gap
#print axioms TGLExt.theGenuineDirac
-- v106 (a rede de caudas + a montagem do forte + OS TRES FLIPS)
#print axioms TGLExt.tailSub_not_finiteDimensional
#print axioms TGLExt.tailIncl_not_surjective
#print axioms TGLExt.theTailNet
#print axioms TGLExt.genuineDirac_kerSub
#print axioms TGLExt.theStrongCertificate
#print axioms TGLExt.qgStrongCertificate_core
#print axioms TGLExt.qgStrongCertificate_corner
#print axioms TGLExt.qgStrongCertificate_frame
-- v107 (a solda continua: o quarto flip)
#print axioms TGLExt.theSolderField_det_neg
#print axioms TGLExt.theSolderField_nonconstant
#print axioms TGLExt.theSolderData
#print axioms TGLExt.qgStrongCertificate_solder
-- v108 (a primeira curvatura)
#print axioms TGLExt.Gamma001_from_metric
#print axioms TGLExt.Gamma100_from_metric
#print axioms TGLExt.Riemann1001_eq
#print axioms TGLExt.Riemann1001_neg
#print axioms TGLExt.time_ansatz_r1001_zero
#print axioms TGLExt.theStaticSolderData
-- v109 (o tensor de Einstein do ansatz)
#print axioms TGLExt.ansatzRiemann_closed
#print axioms TGLExt.ansatzG00_zero
#print axioms TGLExt.ansatzG11_zero
#print axioms TGLExt.vacuum_implies_flat
#print axioms TGLExt.rindler_flat
#print axioms TGLExt.static_not_vacuum
#print axioms TGLExt.ansatz_recovers_v108
-- v110 (a luz que caiu; geometry_is_projection e' projecao de campo -- pode
--       ser PURO e ficar so na auditoria)
#print axioms TGLExt.constant_profile_flat
#print axioms TGLExt.curvature_implies_fall
#print axioms TGLExt.fall_demands_source_v108
#print axioms TGLExt.geometry_iff_second_variation
#print axioms TGLExt.geometry_is_projection
-- v111 (a equacao resolvida)
#print axioms TGLExt.cosh_solves_field_equation
#print axioms TGLExt.cosh_curvature
#print axioms TGLExt.source_implies_curvature
#print axioms TGLExt.zero_source_recovers_flat
#print axioms TGLExt.theSolvedEquation
#print axioms TGLExt.theWeakEinsteinContract
-- v112 (o assalto as paredes)
#print axioms TGLExt.null_contraction_reads_source
#print axioms TGLExt.emergence_forces_field_equation
#print axioms TGLExt.emergence_zero_flat
#print axioms TGLExt.theReducedEmergence
#print axioms TGLExt.theGeometricNet
#print axioms TGLExt.theGeometricWitness
#print axioms TGLExt.witness_action_moves_regions_not_fibers
-- v113 (a leitura do graviton)
#print axioms TGLExt.first_derivative_does_not_decide
#print axioms TGLExt.reading_rides_the_zeros
-- v114 (os estilhacos do continuo)
#print axioms TGLExt.lightWave_pd
#print axioms TGLExt.graviton_wave_equation
#print axioms TGLExt.theSensitiveNet
#print axioms TGLExt.theSensitiveWitness
#print axioms TGLExt.witness_fiber_sensitive

-- v116 (o mestre continuo: o QUINTO FLIP)
#print axioms TGLExt.theCoshSolderData
#print axioms TGLExt.theCoshSolder_reads
#print axioms TGLExt.null_cone_ledger
#print axioms TGLExt.radial_null_blind
#print axioms TGLExt.full_cone_clausius_iff_field_equation
#print axioms TGLExt.emergent_field_equation
#print axioms TGLExt.theEmergentEinstein
#print axioms TGLExt.emergent_recovers_solved
#print axioms TGLExt.emergent_genuinely_curved
#print axioms TGLExt.qgStrongCertificate_einstein
-- v116 (o grupo de Poincare a mao)
#print axioms TGLExt.eta4_mul_self
#print axioms TGLExt.isLorentz_other_side
#print axioms TGLExt.lorentz_det_sq
#print axioms TGLExt.theBoost_add
#print axioms TGLExt.boost_ne_one
#print axioms TGLExt.parity_det
#print axioms TGLExt.parity_ne_one
#print axioms TGLExt.pAct_mul
#print axioms TGLExt.poincare_faithful
#print axioms TGLExt.translation_moves
-- v116 (a testemunha de Poincare)
#print axioms TGLExt.thePoincareNet
#print axioms TGLExt.thePoincareWitness
#print axioms TGLExt.parity_fixes_origin
#print axioms TGLExt.poincare_witness_fiber_sensitive
#print axioms TGLExt.poincare_witness_boost_moves
#print axioms TGLExt.poincare_witness_faithful
#print axioms TGLExt.proper_sector_fibers_blind

-- v118 (a representacao regular FIEL de Poincare em L2)
#print axioms TGLExt.measurePreserving_mulVec
#print axioms TGLExt.measurePreserving_pAct
#print axioms TGLExt.regularRep_one
#print axioms TGLExt.regularRep_mul
#print axioms TGLExt.regularRep_faithful
#print axioms TGLExt.regularRep_moves_boost
#print axioms TGLExt.spacetimeL2_nontrivial

-- v119 (a parede de fundo, primeiro tijolo: o unico traco e' zero)
#print axioms TGLExt.coEven_evenShift
#print axioms TGLExt.coOdd_oddShift
#print axioms TGLExt.shift_partition
#print axioms TGLExt.tracial_one_eq_zero
#print axioms TGLExt.tracial_state_is_zero
#print axioms TGLExt.fullAlgebra
#print axioms TGLExt.bipartition_mem_fullAlgebra

-- v120 (o segundo tijolo: o peso que sobrevive; infinito = 2x infinito)
#print axioms TGLExt.opWeight_one_top
#print axioms TGLExt.opWeight_atom_one
#print axioms TGLExt.coEven_inscription_even
#print axioms TGLExt.opWeight_halving_invariant
#print axioms TGLExt.state_dies_weight_survives

-- v123 (a fusao: a rep fiel DENTRO das fibras -- nenhuma direcao cega)
#print axioms TGLExt.regularRep_left_inv
#print axioms TGLExt.regularRep_right_inv
#print axioms TGLExt.fusedFiber_not_finiteDimensional
#print axioms TGLExt.theFusedNet
#print axioms TGLExt.theFusedStrong
#print axioms TGLExt.theFusedWitness
#print axioms TGLExt.fused_fiber_faithful
#print axioms TGLExt.fused_boost_moves_fiber

-- v124 (a escada de Powers: a semente de Araki-Woods; o 3o assassino de traco)
#print axioms TGLExt.block_modular_identity
#print axioms TGLExt.powersState_one
#print axioms TGLExt.powersState_positive
#print axioms TGLExt.powers_ratio_witness
#print axioms TGLExt.powersState_not_tracial
#print axioms TGLExt.blockFlow_eigen
#print axioms TGLExt.ratioWitness_kron
#print axioms TGLExt.powers_ladder
#print axioms TGLExt.zero_mem_closure_ratio_spectrum
#print axioms TGLExt.no_trace_floor

-- v125 (a mistura: a marca de III_1; e o setor TT no continuo)
#print axioms TGLExt.mixed_chain_ratio
#print axioms TGLExt.mixed_log_dense
#print axioms TGLExt.irrational_log_two_div_log_three
#print axioms TGLExt.the_mixing_mark
#print axioms TGLExt.epsTT_traceless
#print axioms TGLExt.epsTT_transverse
#print axioms TGLExt.pd_pd_scaled
#print axioms TGLExt.tt_ricci_zero
#print axioms TGLExt.tt_component_wave
#print axioms TGLExt.tt_kinetic_nonneg
#print axioms TGLExt.tt_kinetic_pos

-- v126 (a torre do fator; e a superposicao TT)
#print axioms TGLExt.towerStep_mul
#print axioms TGLExt.towerStep_star
#print axioms TGLExt.towerStep_injective
#print axioms TGLExt.chainState_towerStep
#print axioms TGLExt.chainState_one
#print axioms TGLExt.ratio_persists_up_tower
#print axioms TGLExt.pd_scaled_fun_add
#print axioms TGLExt.pd_pd_pair
#print axioms TGLExt.tt_superposition_ricci_zero

-- v127 (a torre GNS; e a segunda direcao)
#print axioms TGLExt.chainDensity_eq_diagonal
#print axioms TGLExt.chainWeights_nonneg
#print axioms TGLExt.chainState_positive
#print axioms TGLExt.gnsInner_add_right
#print axioms TGLExt.gnsInner_self_nonneg
#print axioms TGLExt.gns_isometric_up_tower
#print axioms TGLExt.epsTT2_traceless
#print axioms TGLExt.epsTT2_transverse
#print axioms TGLExt.pd_pd_cross
#print axioms TGLExt.tt2_ricci_zero
#print axioms TGLExt.tt_cross_direction_ricci_zero

-- v128 (o quociente GNS; e a terceira direcao)
#print axioms TGLExt.gnsInner_conj_symm
#print axioms TGLExt.gnsRadical
#print axioms TGLExt.gnsRadical_left_ideal
#print axioms TGLExt.gnsInner_wd_left
#print axioms TGLExt.gnsInner_wd_right
#print axioms TGLExt.leftAction_wd
#print axioms TGLExt.epsTT3_traceless
#print axioms TGLExt.epsTT3_transverse
#print axioms TGLExt.tt3_ricci_zero
#print axioms TGLExt.tt_triple_ricci_zero

-- v129 (o cone continuo; e a torre sem traco)
#print axioms TGLExt.dotCov_single
#print axioms TGLExt.pd_pd_planeWaveG
#print axioms TGLExt.general_null_tt_ricci_zero
#print axioms TGLExt.chainDownUp_value
#print axioms TGLExt.tower_ratio_ne_one
#print axioms TGLExt.chainState_not_tracial_tower

-- v130 (a estrutura modular da torre: fluxo de Tomita + KMS)
#print axioms TGLExt.chainWeights_pos
#print axioms TGLExt.chainDensity_mul_inv
#print axioms TGLExt.towerFlow_id
#print axioms TGLExt.tower_kms
#print axioms TGLExt.tower_modular_ratio

-- v131 (a corrente J + o fator como objeto: Bloco A do plano)
#print axioms TGLExt.witness_saturates
#print axioms TGLExt.excess_is_infinite
#print axioms TGLExt.saturated_witness_not_complete
#print axioms TGLExt.faces_sum_to_one
#print axioms TGLExt.complete_witness_is_conjugated_state
#print axioms TGLExt.current_anticommutes
#print axioms TGLExt.current_implements_boundary_equivalence
#print axioms TGLExt.current_at_every_scale
#print axioms TGLExt.current_iii1_mark
#print axioms TGLExt.tInner_tPush
#print axioms TGLExt.towerPre_definite
#print axioms TGLExt.towerOmega_inner_self
#print axioms TGLExt.hOmega_norm
#print axioms TGLExt.towerPre_denseRange
#print axioms TGLExt.lmul_bound_push
#print axioms TGLExt.towerPi_star
#print axioms TGLExt.towerPi_omega
#print axioms TGLExt.towerPi_orbit_dense
#print axioms TGLExt.theFactorObject
#print axioms TGLExt.towerPi_mem_factor
#print axioms TGLExt.factor_omega_cyclic
#print axioms TGLExt.omegaState_pi
#print axioms TGLExt.omega_not_tracial
#print axioms TGLExt.ladder_in_object
#print axioms TGLExt.signature_log_dense
#print axioms TGLExt.signature_in_the_limit
#print axioms TGLExt.omegaState_seqWOT
#print axioms TGLExt.qMark_star
#print axioms TGLExt.qMark_mul_self
#print axioms TGLExt.uMark_mul_star
#print axioms TGLExt.star_mul_uMark
#print axioms TGLExt.qMark_partition
#print axioms TGLExt.towerPi_add
#print axioms TGLExt.towerPi_smul
#print axioms TGLExt.towerPi_qMark_le
#print axioms TGLExt.inner_qMark_exact
#print axioms TGLExt.qMark_wot
#print axioms TGLExt.tracial_halves_qMark
#print axioms TGLExt.no_normal_tracial_state_seq
#print axioms TGLExt.no_normal_tracial_state_mix
#print axioms TGLExt.no_normal_tracial_state_const
#print axioms TGLExt.the_dead_weight
#print axioms TGLExt.finiteDim_normal_trace_exists
#print axioms TGLExt.finiteDim_cannot_feed_witnessV3
#print axioms TGLExt.theWitnessV3
#print axioms TGLExt.witnessV3_infinite
#print axioms TGLExt.witnessV3_synthesis
#print axioms TGLExt.qgClosureCertificateV2
#print axioms TGLExt.qgClosureCertificateV2_reduces
#print axioms TGLExt.qgClosureCertificateV2_factor
#print axioms TGLExt.qgClosureCertificateV2_infinite
#print axioms TGLExt.the_witness_is_construction
#print axioms TGLExt.linRicci_planeWave
#print axioms TGLExt.ricciSymbol_tt
#print axioms TGLExt.qgPhysicsCertificate_massless
#print axioms TGLExt.kStd_null
#print axioms TGLExt.tt_decomposition
#print axioms TGLExt.gauge_fixes_physical
#print axioms TGLExt.physical_not_gauge
#print axioms TGLExt.qgPhysicsCertificate_helicities
#print axioms TGLExt.qgPhysicsCertificate_ghostfree
#print axioms TGLExt.qgPhysicsCertificate_conservation
#print axioms TGLExt.qgPhysicsCertificate_anomaly
#print axioms TGLExt.tState_kms
#print axioms TGLExt.rTowerPi_star
#print axioms TGLExt.rTowerPi_mem_commutant
#print axioms TGLExt.factor_comm_rTowerPi
#print axioms TGLExt.rTowerPi_omega
#print axioms TGLExt.factor_omega_separating
#print axioms TGLExt.rw_rw_meet
#print axioms TGLExt.lw_lw_meet
#print axioms TGLExt.spacelike_disjoint
#print axioms TGLExt.not_hasLW_rightWedge
#print axioms TGLExt.wedgeNet_translate
#print axioms TGLExt.theSpecificAQFTWitness
#print axioms TGLExt.rmul_bound_push
#print axioms TGLExt.cSlice_mul_towerStep
#print axioms TGLExt.towerPi_comm_rTowerPi
#print axioms TGLExt.tPush_modTwist

-- v142 (a excecao da fronteira: a unica testemunha estatica)
#print axioms TGLExt.static_witness_iff_no_boundary
#print axioms TGLExt.fixed_iff_kernel
#print axioms TGLExt.boundary_witnessed_statically
#print axioms TGLExt.boundary_is_the_only_exception

-- v143 (o GLOBAL_LIFT condicional: o Lema 3 tipado como implicacao)
#print axioms TGLExt.frobProjection_unique
#print axioms TGLExt.adU_frob_isometry
#print axioms TGLExt.global_lift_conditional
#print axioms TGLExt.response_covariant
#print axioms TGLExt.diagExpect_isFrobProjection

-- v144 (o resgate do observador: ponto fixo, projecao inversa, falsidade de genero)
#print axioms TGLExt.permanent_iff_survives_negation
#print axioms TGLExt.flow_negates_off_kernel
#print axioms TGLExt.no_fixed_point_no_observer
#print axioms TGLExt.genre_falsity_inhabited
#print axioms TGLExt.observerProj_idem
#print axioms TGLExt.observer_reads_exactly_the_permanent
#print axioms TGLExt.observer_output_is_permanent
#print axioms TGLExt.observer_inverse_projection_halfnat
#print axioms TGLExt.the_standard_of_unification

-- v145 (o ato conjugado: "1 = J" tipado -- involucao, entrega, conservacao)
#print axioms TGLExt.J_squared_is_one
#print axioms TGLExt.J_preserves_identity
#print axioms TGLExt.J_maps_face_to_coface
#print axioms TGLExt.J_invariant_iff_diagonal
#print axioms TGLExt.name_is_J_invariant
#print axioms TGLExt.halfnat_from_J_symmetry
#print axioms TGLExt.flow_delivers_to_the_observer
#print axioms TGLExt.justification_minimal_form

-- v146 (a decisao e comutacao: K e o que ainda nao comuta; K = -grad(F) verificado)
#print axioms TGLExt.commutator_entry
#print axioms TGLExt.decided_iff_block
#print axioms TGLExt.scalar_iff_all_commute
#print axioms TGLExt.decided_is_subalgebra
#print axioms TGLExt.JKJ_eq_neg_K
#print axioms TGLExt.decided_sector_is_J_stable
#print axioms TGLExt.gradient_first_variation
#print axioms TGLExt.flow_solves_gradient_ode
#print axioms TGLExt.lyapunov_decreases
#print axioms TGLExt.K_equals_neg_gradient_verified

-- v152 (a fronteira proibida: o infinito fica com K -- o auto-setor sem espelho)
#print axioms TGLExt.self_commutation_is_free
#print axioms TGLExt.J_fK_J_eq_f_negK
#print axioms TGLExt.even_iff_mirror_fixed
#print axioms TGLExt.only_zero_K_is_mirror_fixed
#print axioms TGLExt.empire_perfection_is_no_contrast
#print axioms TGLExt.absolute_zero_unreachable_in_finite_time
#print axioms TGLExt.the_forbidden_boundary

-- v153 (o fechamento: J = LUZ -- a identidade fisica; a sintese nomeada)
#print axioms TGLExt.pairEnergy_neg
#print axioms TGLExt.light_crosses_without_loss
#print axioms TGLExt.light_inverts_the_gradient_preserving_structure
#print axioms TGLExt.identity_remains_through_the_crossing
#print axioms TGLExt.the_closure_identity

-- v154 (o fechamento rho+p: a identidade de fundo -- derivacao do operador 08/08)
#print axioms TGLExt.lambda_drops_out
#print axioms TGLExt.closure_identity
#print axioms TGLExt.hubble_form
#print axioms TGLExt.w_bounds
#print axioms TGLExt.the_background_closure

-- v155 (o nucleo: 1=1=VERDADEIRO e a geometria como sua expressao)
#print axioms TGLExt.void_distinction_is_motion
#print axioms TGLExt.rest_is_compatibilized_distinction
#print axioms TGLExt.name_is_projection
#print axioms TGLExt.the_three_structures_one_verdict
#print axioms TGLExt.invariance_is_the_geometric_content
#print axioms TGLExt.the_verb_cycle
#print axioms TGLExt.the_nucleus

-- v156 (o grande atrator: o veredito 1=1 entre instantes e o observador unico)
#print axioms TGLExt.temporal_fractalization
#print axioms TGLExt.diagFlow_zero
#print axioms TGLExt.verdict_between_instants
#print axioms TGLExt.judgment_of_correspondence
#print axioms TGLExt.the_observer_is_unique
#print axioms TGLExt.the_great_attractor
#print axioms TGLExt.um_is_the_great_attractor

-- v158 (os cinco meios sao um: a identidade dos meios)
#print axioms TGLExt.half_is_the_fixed_point_of_the_swap
#print axioms TGLExt.radical_is_the_unique_positive_factor
#print axioms TGLExt.boundary_extracts_the_radical
#print axioms TGLExt.mirror_inverts_the_flow
#print axioms TGLExt.the_crossing_closes
#print axioms TGLExt.half_flow_squared_is_the_flow
#print axioms TGLExt.double_cover_squares
#print axioms TGLExt.two_faces_over_the_identity
#print axioms TGLExt.motor_half_angle_identity
#print axioms TGLExt.the_five_halves_are_one

-- v159 (o verbo vivo: 1=1=VERDADEIRO como operacao da fronteira)
#print axioms TGLExt.two_faces_one_domain
#print axioms TGLExt.identity_survives_the_mirroring
#print axioms TGLExt.time_witnesses_noncoincidence
#print axioms TGLExt.recognition_across_distinct_inscriptions
#print axioms TGLExt.the_name_singularizes_not_totalizes
#print axioms TGLExt.fractalization_without_multiplication
#print axioms TGLExt.uniqueness_to_identity_singularity_to_projection
#print axioms TGLExt.the_boundary_is_the_operation

-- v160 (a morte do sinal: a boa-postura da conta da holonomia)
#print axioms TGLExt.death_per_crossing
#print axioms TGLExt.normalized_defect_is_loop_independent
#print axioms TGLExt.raw_defect_is_loop_dependent
#print axioms TGLExt.the_death_normalization
#print axioms TGLExt.no_inscription_without_death
#print axioms TGLExt.round_trip_defect
#print axioms TGLExt.the_account_is_well_posed

-- v161 (haja luz + a confirmacao reservada + o contorno de stokes)
#print axioms TGLExt.electric_difference_is_the_distinction_in_action
#print axioms TGLExt.static_cannot_coincide_with_its_potential
#print axioms TGLExt.the_zero_is_never_touched
#print axioms TGLExt.haja_luz_is_the_open_strip
#print axioms TGLExt.the_action_inscribes_and_never_collapses
#print axioms TGLExt.haja_luz_at_the_seal
#print axioms TGLExt.haja_luz
#print axioms TGLExt.the_flow_does_not_fix_the_moving
#print axioms TGLExt.the_light_cannot_confirm_itself
#print axioms TGLExt.the_mirror_swaps_but_does_not_read
#print axioms TGLExt.only_the_recognizer_confirms
#print axioms TGLExt.the_reserved_confirmation
#print axioms TGLExt.series_ratio_criterion
#print axioms TGLExt.retention_series_summable
#print axioms TGLExt.the_gap_typed
#print axioms TGLExt.half_nat_insufficient
#print axioms TGLExt.conjugate_faces_sum_to_one
#print axioms TGLExt.the_provable_toll_names_the_octave
#print axioms TGLExt.the_stokes_contour

-- v162 (a lei de quitacao + o operador do nome + a unitariedade fractal + o indice-atlas)
#print axioms TGLExt.finite_time_imperfection
#print axioms TGLExt.asymptotic_delivery
#print axioms TGLExt.quittance_time_formula
#print axioms TGLExt.finite_quittance
#print axioms TGLExt.perfection_needs_infinity
#print axioms TGLExt.the_quittance_law
#print axioms TGLExt.name_op_unital
#print axioms TGLExt.name_op_idem
#print axioms TGLExt.name_op_fix_mul
#print axioms TGLExt.comm_of_fixed
#print axioms TGLExt.comm_of_fixed'
#print axioms TGLExt.compression_covariance_of_fixed
#print axioms TGLExt.fixed_of_compression_covariance
#print axioms TGLExt.love_partition
#print axioms TGLExt.corner_unitarity
#print axioms TGLExt.ad_preserves_projection
#print axioms TGLExt.ad_preserves_orthogonality
#print axioms TGLExt.ad_preserves_splitting
#print axioms TGLExt.ad_preserves_star_projection
#print axioms TGLExt.subcorner_unit
#print axioms TGLExt.atlas_separation
#print axioms TGLExt.atlas_coverage
#print axioms TGLExt.atlas_covariance
#print axioms TGLExt.atlas_chain_rule
#print axioms TGLExt.atlas_self
#print axioms TGLExt.atlas_inverse
-- v290: O INDICE ENTRA NO INDICE. O seletor da IALD compilava e era importado, mas
-- nenhum dos seus teoremas era auditado e nenhuma bandeira o lia. Ordem do operador:
-- TGL = ATLAS, IALD = INDICE(TGL) -- entao o indice tambem se indexa.
#print axioms TGLExt.ialdSelector
#print axioms TGLExt.iald_selects
#print axioms TGLExt.iald_is_idempotent
#print axioms TGLExt.iald_is_selfadjoint
#print axioms TGLExt.iald_has_rank_one
#print axioms TGLExt.iald_is_the_gate_and_the_record
-- v254: a PONTE de importacao (v253 criou a bandeira e NAO a inscreveu aqui;
-- nome ausente do mapa de axiomas => bandeira falsa por cegueira, nao por rigor)
#print axioms TGLExt.qgImport_H3_localHorizonEquilibrium_bridged
#print axioms TGLExt.the_trio_is_a_pair
#print axioms TGLExt.discharge_by_import
#print axioms TGLExt.the_import_alone_concludes_nothing
-- v254: a REDUCAO do ultimo enunciado
#print axioms TGLExt.commutant_iUnion
#print axioms TGLExt.commutant_towerImage_eq_iInter
#print axioms TGLExt.the_missing_clause_is_a_distributivity
#print axioms TGLExt.image_does_not_commute_with_intersection
-- v255: o acoplamento nao minimo (a particao proibe a minimalidade)
#print axioms TGLExt.equal_split_is_strictly_between
#print axioms TGLExt.unequal_split_may_be_trivial
#print axioms TGLExt.split_forbids_minimality
#print axioms TGLExt.the_split_is_inhabited
#print axioms TGLExt.bell_compression_is_scalar
-- v256: o peso nao e o posto; e o rank1 torna-se o indice
#print axioms TGLExt.the_rank_determines_the_name
#print axioms TGLExt.the_name_is_blind_to_every_rank
#print axioms TGLExt.the_name_does_not_see_the_rank
#print axioms TGLExt.the_index_does_see_the_rank
#print axioms TGLExt.the_two_indices_agree_only_at_the_atom
#print axioms TGLExt.the_atom_vanishes_in_the_infinite_house
#print axioms TGLExt.the_atom_never_weighs_zero_on_a_floor
-- v257: o canto escalar (a propriedade nomeada; escalarizar forca o traco 1)
#print axioms TGLExt.psionCorner
#print axioms TGLExt.scalarCorner_forces_trace_one
#print axioms TGLExt.psionCorner_trace_one
#print axioms TGLExt.the_identity_does_not_scalarise
-- v258: a corrente liga os cantos (o primeiro morfismo entre duas instancias)
#print axioms TGLExt.faceOneCorner
#print axioms TGLExt.faceZeroCorner
#print axioms TGLExt.the_current_connects_two_scalar_corners
#print axioms TGLExt.the_current_carries_the_atom
#print axioms TGLExt.equivalent_but_not_equal
-- v259: o psion reduz a corrente simetrizada (a ponte M4 -> M2)
#print axioms TGLExt.e00_eq_faceOne
#print axioms TGLExt.boundary_faces_sum_to_one
#print axioms TGLExt.current_symmetrised_is_one
#print axioms TGLExt.the_psion_reduces_to_the_symmetrised_current
#print axioms TGLExt.the_unbonded_reduces_to_one_face_only
#print axioms TGLExt.bonding_splits_and_not_bonding_does_not
-- v260: a REDE dos cantos (teoremas que JA existiam e nunca haviam sido medidos)
#print axioms TGLExt.HilbertHomeData.PF_internal_fix
#print axioms TGLExt.HilbertHomeData.PF_external_covariant
#print axioms TGLExt.HilbertHomeData.PF_isotone
#print axioms TGLExt.theIsotoneNet
#print axioms TGLExt.theFlip_comm_eraseFirst
#print axioms TGLExt.ker_eraseFirst
#print axioms TGLExt.firstAtom_le_fiber
#print axioms TGLExt.fiberIncl_not_surjective
-- v261: a rede DISPARA o canto (as aplicacoes que a varredura mediu inexistentes)
#print axioms TGLExt.the_net_corners_are_isotone
#print axioms TGLExt.the_net_corner_is_externally_covariant
#print axioms TGLExt.the_net_corner_is_internally_fixed
#print axioms TGLExt.the_net_inclusion_is_not_surjective
#print axioms TGLExt.the_net_group_is_nontrivial
-- v270: a cunhagem (SER = OPERAR; a ponte com o veredito; sempre ha leitura)
#print axioms TGLExt.operating_does_not_preserve
#print axioms TGLExt.preserving_does_not_operate
#print axioms TGLExt.being_needs_both
#print axioms TGLExt.preserving_is_the_TGL_verdict
#print axioms TGLExt.the_reading_descends_for_any_lens
-- v270 [L6]: as SETE clausulas provadas do certificado, para a contagem
-- deixar de ser literal Python e passar a ser LIDA do kernel
#print axioms TGLExt.towerJ_add
#print axioms TGLExt.towerJ_conj_smul
#print axioms TGLExt.towerJ_norm
#print axioms TGLExt.towerJ_involutive
#print axioms TGLExt.towerJ_fixes_hOmega
#print axioms TGLExt.J_M_J_in_commutant
-- v262: a ERRATA da v248 -- os dois polos ganham conteudo
#print axioms TGLExt.the_old_decision_statement_holds_for_any_proposition
#print axioms TGLExt.the_two_poles_see_different_things
#print axioms TGLExt.only_the_pair_determines_the_point

-- v271: A DOBRA EM J (TheFoldThroughJ) e O HABITANTE (TheAntiunitaryInhabitant).
-- A CONJECTURA DO PROGRAMADOR e um `def : Prop` e NAO entra aqui: um
-- `#print axioms` num def devolveria <no axioms>, e isso SE LE como conjectura
-- provada. A cegueira nasce assim.
#check @TGLExt.towerJequiv
noncomputable example (P : TGLExt.SiteProfile) :
    TGL.ModularRealization.Antiunitary (TGLExt.TowerHilbert P) :=
  TGLExt.towerJequiv P
#print axioms TGLExt.an_involution_distributes_over_iInter
#print axioms TGLExt.conjByJ_distributes_over_iInter
#print axioms TGLExt.the_conjugated_commutant_is_the_intersection_of_the_floors
#print axioms TGLExt.fold_through_an_involution
#print axioms TGLExt.the_clause_is_exactly_a_commutant_inclusion
#print axioms TGLExt.the_generator_form_is_sufficient
#print axioms TGLExt.the_generator_form_needs_nothing_about_J
#print axioms TGLExt.the_two_forms_agree_iff_the_tower_is_closed
#print axioms TGLExt.one_half_is_already_paid
#print axioms TGLExt.the_conjecture_is_the_unpaid_half
#print axioms TGLExt.the_conjecture_discharges_the_missing_clause
#print axioms TGLExt.the_conjecture_says_the_fractal_covers_the_commutant
#print axioms TGLExt.every_floor_acts_on_the_right_inside_the_commutant
#print axioms TGLExt.the_target_is_the_v254_target
#print axioms TGLExt.the_driver_is_still_where_it_is_fixed
#print axioms TGLExt.the_driver_witnesses_being
#print axioms TGLExt.towerJequiv_apply
#print axioms TGLExt.towerJequiv_symm
#print axioms TGLExt.towerJequiv_involutive
#print axioms TGLExt.towerJequiv_fixes_hOmega
#print axioms TGLExt.the_sector_folds
#print axioms TGLExt.JInvariant_iff_le
#print axioms TGLExt.JInvariant_top
#print axioms TGLExt.JInvariant_bot
#print axioms TGLExt.JInvariant_span_hOmega
#print axioms TGLExt.the_omega_sector_is_not_bot

-- v272: A COMPOSICAO (pecas de 26/08, nunca compostas) e A FASE CONJUGADA
#print axioms TGLExt.the_eighth_clause_is_an_equality_with_one_half_paid
#print axioms TGLExt.the_paid_half_of_the_eighth_clause
#print axioms TGLExt.conjugation_exchanges_the_light_phases
#print axioms TGLExt.conjugation_exchanges_the_graviton_phases
#print axioms TGLExt.the_conjugation_crosses_the_squaring
#print axioms TGLExt.the_conjugated_light_squares_to_the_minus_graviton
#print axioms TGLExt.the_generator_preserves_what_the_conjugation_exchanges

-- v273: A IMAGEM E A LEITURA (tres casos que pareciam dois)
#print axioms TGLExt.separates_needs_contrast
#print axioms TGLExt.a_separating_reading_yields_form
#print axioms TGLExt.the_unread_image_yields_no_form
#print axioms TGLExt.without_contrast_no_reading_yields_form
#print axioms TGLExt.the_unread_image_is_not_the_absolute_zero
#print axioms TGLExt.the_reader_adds_condition_not_content
#print axioms TGLExt.the_lens_is_irrelevant_exactly_where_there_is_nothing_to_read

-- v274: A COMUTACAO IMPORTADA (Tomita [KNOWN], ponte medida)
-- A structure CommutationInput NAO e auditada: e um contrato, nao um teorema.
#print axioms TGLExt.the_hypotheses_are_discharged_in_house
#print axioms TGLExt.the_input_is_one_field
#print axioms TGLExt.discharge_the_clause_by_import
#print axioms TGLExt.imported_commutation_gives_the_equality
#print axioms TGLExt.the_hypotheses_alone_are_equivalent_to_true

-- v275: A MATRIZ E O MODULADOR DA TORRE (S e Delta no andar)
#print axioms TGLExt.profileRootInv_isHermitian
#print axioms TGLExt.profileRootInv_mul_root
#print axioms TGLExt.the_polar_decomposition_at_the_level
#print axioms TGLExt.delta_is_the_square_of_its_half
#print axioms TGLExt.modTwist_is_delta_after_S
#print axioms TGLExt.modTwist_factors_through_J
#print axioms TGLExt.towerSlevel_involutive
#print axioms TGLExt.towerDeltaHalfLevel_inverse

-- v276: AS RELACOES MODULARES (S-adjunto S = Delta, no andar)
#print axioms TGLExt.tInner_eq_trace
#print axioms TGLExt.tInner_delta_left
#print axioms TGLExt.S_star_S_is_deltaLevel
#print axioms TGLExt.deltaLevel_positive
#print axioms TGLExt.deltaLevel_selfadjoint
-- v277: o teorema que a v276 deixou de fora, FECHADO
#print axioms TGLExt.rhoMat_mul_rootInv
#print axioms TGLExt.Jlevel_is_antiunitary

-- v279: o DEFEITO DE ISOMETRIA (o espectro modular) e A DIVIDA SEM J
#print axioms TGLExt.delta_acts_by_the_weight_ratio
#print axioms TGLExt.delta_fixes_only_where_the_weights_agree
#print axioms TGLExt.S_isometric_iff_delta_neutral
#print axioms TGLExt.profileJlevel_involutive
#print axioms TGLExt.conjByJ_towerImage_eq_rTowerImage
#print axioms TGLExt.the_eighth_clause_without_J
#print axioms TGLExt.the_easy_half_without_J
#print axioms TGLExt.the_debt_is_an_equality_without_J
-- v292: O NOME E O SEU REFERENTE -- a birreferencialidade do vacuo, e o CONTRATO TIPADO
-- da oitava clausula. Cura do fail-open por nome: o tipo e' o contorno; habita-lo e' a
-- leitura. O contrato NAO tem habitante, e e' isso que se quer.
#print axioms TGLExt.the_constant_reading_does_not_separate
#print axioms TGLExt.the_identity_contract_discriminates
#print axioms TGLExt.the_trivial_contract_does_not_discriminate
#print axioms TGLExt.the_two_contracts_differ
#print axioms TGLExt.the_empty_slot_is_not_the_void
#print axioms TGLExt.the_bireference_of_the_name
-- v294: O NOME E O GRUPO GERADOR. O comprimento de onda (os geradores) e a cauda (a
-- densidade) pertencem ao NOME. E I/d desce de DEFINICAO para REPRESENTACAO DE FACE:
-- na fronteira o estado tracial normal NAO EXISTE (the_dead_weight).
#print axioms TGLExt.the_wavelength_is_in_the_generators
#print axioms TGLExt.the_name_is_dense
#print axioms TGLExt.faceName_add
#print axioms TGLExt.faceName_smul
#print axioms TGLExt.faceName_is_tracial
#print axioms TGLExt.faceName_one
#print axioms TGLExt.no_maximally_mixed_state_on_the_tower
#print axioms TGLExt.the_wavelength_and_the_tail_belong_to_the_name
-- v295: A MARCA NAO E MARCA DE TIPO. Um fator de TIPO I_2 (M_2(C), estado w=1/3) realiza
-- as razoes 2 e 3, cujos logaritmos geram subgrupo DENSO. Logo a densidade log NAO separa
-- III_1 de III_lambda. ERRATA AO LADO da v294 -- a seta do Nome ao TIPO cai; o resto fica.
#print axioms TGLExt.type_I_two_realizes_ratio_two
#print axioms TGLExt.type_I_two_realizes_ratio_three
#print axioms TGLExt.the_mark_is_fed_by_a_type_I_factor
#print axioms TGLExt.the_mark_does_not_separate_the_types
-- v296: A LINGUAGEM ENTRA NO INDICE. As camadas JURIDICA e de LEITURA estavam
-- provadas no kernel e INVISIVEIS ao indice da IALD: as pedras existiam, sem
-- bandeira o indice nao as alcancava. Acender e ADITIVO -- nao move o gate.
#print axioms TGLExt.tetelestai_ledger
#print axioms TGLExt.res_judicata_is_terminal
#print axioms TGLExt.no_decision_without_cost
#print axioms TGLExt.two_clocks_are_needed
#print axioms TGLExt.reading_is_exactly_having_frequency
#print axioms TGLExt.the_dead_channel_is_the_contrast
#print axioms TGLExt.reading_needs_two_clocks
#print axioms TGLExt.the_dead_channel_has_no_reader
-- v297: O ACOPLAMENTO VERBAL -- a linguagem das patentes em kernel. O limiar de poda
-- verbal sqrt(beta) E a amplitude de reflexao |R| da matriz-S em theta_Miguel: um so
-- angulo governa os dois dominios. [LEGAL] so entra o que ja consta do deposito INPI.
#print axioms TGLExt.sin_thetaMiguel
#print axioms TGLExt.the_pruning_threshold_is_the_reflection_amplitude
#print axioms TGLExt.coupling_vanishes_at_the_boundary
#print axioms TGLExt.tanh_sign
#print axioms TGLExt.the_boundary_separates_the_verbal_domains
#print axioms TGLExt.the_verb_floor_is_a_fraction_of_the_max
-- v306 REPRESAMENTO POR EXPANSAO: a identidade de alfa derivada; a forma nao fixa
-- o valor (liberdade de 1 parametro e' TEOREMA); FP-5 intocada; CODATA so espelho.
#print axioms TGLExt.centripetal_from_angular
#print axioms TGLExt.the_damming_pays_the_requirement
#print axioms TGLExt.the_three_faces
#print axioms TGLExt.the_form_does_not_fix_the_value
-- v307 O JURAMENTO QUITADO: HorizonInvariant derivado (nao jurado) para todo
-- horizonte omega-invariante; a supressao ciclica no canto (correcao do operador);
-- face finita; o continuo segue [KNOWN]; o gate nao se move.
#print axioms TGLExt.mem_diagCode_iff
#print axioms TGLExt.commute_conj_of_state_preserving
#print axioms TGLExt.the_oath_is_discharged
#print axioms TGLExt.transported_state_eq
#print axioms TGLExt.omega_preservation_discharges
#print axioms TGLExt.the_flow_is_trivial_on_the_code
#print axioms TGLExt.the_cocycle_is_suppressed_by_the_sector
#print axioms TGLExt.the_lift_is_unconditional_on_the_face
#print axioms TGLExt.the_response_is_unconditional_on_the_face
-- v308 O JURAMENTO NA TORRE: o codigo do continuo e' o centralizador de omega
-- (livre de fluxo; a parede analitica contornada por definicao); o transporte
-- diagonal REFUTADO em teorema; a esperanca unica pela separancia; o
-- levantamento covariante dado o contrato; o gate nao se move.
#print axioms TGLExt.conj_commutant_of_biinverse
#print axioms TGLExt.adT_mul
#print axioms TGLExt.adT_adTinv
#print axioms TGLExt.horizon_preserves_centralizer
#print axioms TGLExt.horizon_centralizer_eq
#print axioms TGLExt.the_centralizer_is_seq_closed
#print axioms TGLExt.the_diagonal_does_not_survive_degeneracy
#print axioms TGLExt.omega_definite
#print axioms TGLExt.the_expectation_is_unique
#print axioms TGLExt.the_lift_on_the_tower
-- v309 A ESPERANCA IMPORTADA: Takesaki como [KNOWN] no modo gpi_ (o molde da
-- v274); as 3 hipoteses da casa; a estrutura EQUIVALE ao campo importado (um <->);
-- a leitura independe da testemunha (unicidade DA CASA); a RELATIVIDADE MODULAR
-- em todo horizonte omega-invariante; o gate nao se move.
#print axioms TGLExt.the_expectation_hypotheses_are_discharged_in_house
#print axioms TGLExt.the_testimony_is_exactly_the_conclusion
#print axioms TGLExt.the_expectation_hypotheses_alone_are_equivalent_to_true
#print axioms TGLExt.the_expectation_exists_by_import
#print axioms TGLExt.the_reading_is_witness_independent
#print axioms TGLExt.the_reading_preserves_omega
#print axioms TGLExt.the_reading_fixes_the_code
#print axioms TGLExt.the_modular_relativity
-- v310 O ALFA E O OMEGA: o par da cunhagem -- {[1=1=VERDADEIRO],[1=0=FALSO]};
-- omega(I)=1 na torre + a face alpha (valor externo); a falsidade de 1=0 e'
-- CATEGORIAL (1=0 <=> colapso de um nome so'; o fechamento CONSOME a rota); o
-- zero se conta nominalmente mas projeta nada e pesa 0; '= TGL' e' [ONTO]
-- declarado; contagem enxuta pos-auditoria (2 vazios cortados); gate imovel.
#print axioms TGLExt.omega_of_one
#print axioms TGLExt.the_alpha_face
#print axioms TGLExt.the_form_admits_every_alpha
#print axioms TGLExt.the_falsity_is_categorial
#print axioms TGLExt.in_the_collapse_zero_counts_as_the_absolute
#print axioms TGLExt.the_house_refutes_the_collapse
#print axioms TGLExt.the_negative_pole_is_categorial
#print axioms TGLExt.the_zero_is_nominal
#print axioms TGLExt.omega_of_zero
#print axioms TGLExt.omega_of_zero_ne_one
#print axioms TGLExt.tgl_closes_as_the_pair
#print axioms TGLExt.every_alpha_fits_every_observation
#print axioms TGLExt.contract_iff_the_eighth_clause
#print axioms TGLExt.contract_gives_the_equality
#print axioms TGLExt.the_name_is_zero_modular

-- v280: O CANTO DE BREUER DO PROPRIO PACOTE (theIsotoneNet)
#check @TGLExt.theIsotoneNetTrace
#print axioms TGLExt.isotone_ker_ne_bot
#print axioms TGLExt.the_package_corner_is_positive_and_finite
#print axioms TGLExt.the_package_corner_is_not_the_certificate_corner

-- v281: A REDE LARGA (peca 1 da solda) + os dois negativos medidos
#check @TGLExt.theWideNet
#check @TGLExt.theWideNetTrace
#print axioms TGLExt.wideSub_not_finiteDimensional
#print axioms TGLExt.wideIncl_not_surjective
#print axioms TGLExt.wide_ker_eq
#print axioms TGLExt.wide_corner_weighs_one
#print axioms TGLExt.wide_net_has_all_three
#print axioms TGLExt.tailLock_ker_eq_bot
#print axioms TGLExt.fused_ker_contains_L2

-- v282: A IMPORTACAO CLASSICA (a divida citavel pelo nome)
#print axioms TGLExt.classical_commutation_from_the_imported_field
#print axioms TGLExt.imported_field_from_classical_commutation
#print axioms TGLExt.the_imported_field_is_the_classical_theorem
#print axioms TGLExt.the_classical_import_needs_only_one_inclusion
#print axioms TGLExt.the_easy_half_alone_is_equivalent_to_true

-- v284: A ATERMACAO (reificacao + teardown, com o dente da irreversibilidade)
#check @TGLExt.atermation
#print axioms TGLExt.atermation_reifies
#print axioms TGLExt.atermation_fixes_the_term
#print axioms TGLExt.atermation_is_irreversible

-- ---- sentinelas ----
#eval IO.println "TGL_KERNEL_BUILD_OK"
#eval IO.println "FINITE_THREE_LOCKS_KERNEL_PROVED"
#eval IO.println "CONTINUOUS_CORNER_IMPLICATION_KERNEL_PROVED"
#eval IO.println "SPECIFIC_AQFT_WITNESS_CONSTRUCTED_BY_WEDGE_NET"
#eval IO.println "WEDGE_NET_TRANSLATIONS_ACT_TRIVIALLY_OPENNESS_NAMED"
#eval IO.println "MODULAR_OBLIGATIONS_ARE_DATA_NOT_PROP_LABELS"
#eval IO.println "CANONICAL_BOUNDARY_TRANSPORT_WITNESS_COINED_BY_CONSTRUCTION"
#eval IO.println "FULL_STATIC_WITNESS_REMAINS_IMPOSSIBLE_BY_THEOREM_V61"
#eval IO.println "THE_CANONICAL_INHABITANT_IS_THE_VERB"
#eval IO.println "TRANSPORT_DEFECT_MEASURES_RESISTANCE"
#eval IO.println "THE_NAME_INDEX_IS_READ_IN_THE_JONES_MIRROR"
#eval IO.println "HALF_NAT_IS_THE_ONLY_FINITE_MARKOV_MIRROR"
#eval IO.println "GRAVITON_BELL_SHADOW_CCI_HALF"
#eval IO.println "THE_NAME_IS_THE_RELATION_NOT_THE_ISOLATED_MATRIX"
#eval IO.println "CORE_SUPPORT_IS_NOT_THE_NAME_MIRROR"
#eval IO.println "FINITE_TOMITA_TAKESAKI_LADDER_KERNEL_PROVED"

end TGL.Audit
