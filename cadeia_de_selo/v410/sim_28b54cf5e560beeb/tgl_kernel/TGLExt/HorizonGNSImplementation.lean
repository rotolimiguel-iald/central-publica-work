-- ---------------------------------------------------------------------
-- PEDRA DA BANCADA CHATGPT — ENTREGA_053 (06-07/09/2026), transposta em 07/09/2026
-- Lote 046..054 (ORDEM_008 cumprida; «tudo o que a bancada podia», 9 entregas, 43 modulos).
--   046: a ESPERANCA APERIODICA — aperiodicExpectationInput P : ExpectationInput P para TODO perfil da torre
--     (media de Cesaro do fluxo modular; limite forte; into/fixes/ortho); o levantamento do Lema 3 dispara para
--     todo perfil e todo horizonte (the_lift_fires_on_the_aperiodic_tower); unicidade; E comuta com sigma_t.
--   047: propriedades da esperanca — linear sobre M, preserva 1/estado/adjunto, bimodular sobre o centralizador,
--     COMPLETAMENTE POSITIVA (CompletelyPositiveMap da mathlib), contracao GNS, NORMAL (supremos positivos dirigidos).
--   048: obstrucoes da identificacao modular/geometrica — Borchers trivial sobrevive ao transporte de estado (027);
--     periodo do fluxo forca retorno de rotulos em localizacao fiel covariante; ligado ao boost 044 (negativos tipados).
--   049-050: SUBESPACO PADRAO CONTINUO em L^2 — T_c = M_exp(-c xi) positivo auto-adjunto (grafo limitado), J
--     antiunitaria, S_c = J T_c involucao fechada, K_c = Fix S_c subespaco padrao; adjunto S_c^dagger = T_c J,
--     Delta_c = S_c^dagger S_c = T_c^2 = T_{2c} com igualdade de dominios, resolvente (I + Delta_c)^{-1}.
--     Identificacao T_c = Delta_c^{1/2} e BW seguem OPEN.
--   051: balanco optico finito — Q - K DeltaA = K E com E >= 0 (integral optica), E/t^4 -> (a^2 + c^2)/12; Riccati;
--     no caso variavel o drift Z_R(s) - s R(s) persiste (controles).
--   052: setor horizontal (plano de Pauli X,Y do 1o sitio) — a esperanca centralizante zera as duas direcoes;
--     o horizonte modular faz o quarto de volta; forma invariante = c x produto GNS real; [INPUT] traco relativo = 1
--     fixa c = 1/2 (densidade de area 1/2); forma efetiva de densidade |2p - 1|. Escala livre sem calibracao por Omega.
--   053: polarizador D = P_R(-i)P_R no Hilbert real; acao GNS de todo TowerHorizon preserva Omega e entrelaca D;
--     radical = centralizador (setor auto-adjunto); CONTRAEXEMPLO: covariancia + calibracao comum NAO da unicidade
--     da area (9/10 vs 1377/1250 no 2o par).
--   054: custo modular do polarizador C_D(x) = sum 2||D^(n+1)x||^2/(2n+1): l.s.c., preservado por todo TowerHorizon,
--     custo zero <=> centralizador; f(0)=0, f(0)=2 localModularCost; C_D(X_1 Omega) = log2/3 na referencia p = 1/3.
--   Estatuto: [REAL] o que esta compilado; [INPUT] calibracao por Omega, traco relativo = 1; [OPEN] H3, selecao
--   fisica da area, escala dimensional, regiao <-> algebra, BW/identificacao T_c = Delta^{1/2}, reconstrucao geral.
-- Auditoria da gerencia (sessao d554e796, 07/09/2026): hashes 185/185 (9 entregas); 9/9 auditores exit 0;
--   recompilacao INDEPENDENTE 43/43, axiomas no trio; guarda de colisao; enunciados lidos.
--   Transposicao: cabecalho + prefixo TGLExt. (+ regra 3).
-- NAO move gate; nao e fisica; NOT_FALSIFIED nunca e CONFIRMED; CONFIRMADA proibido.
-- ---------------------------------------------------------------------
import TGLExt.ExpectationContinuity
import Mathlib.Topology.Algebra.Module.Basic

set_option autoImplicit false
set_option maxHeartbeats 1600000

namespace ChatgptAudit.Covariant053
open TGLExt ChatgptAudit UniformSpace Filter
open scoped Topology
noncomputable section

theorem horizon_ad_add (P : SiteProfile) (h : TowerHorizon P)
    (A B : TowerHilbert P →L[ℂ] TowerHilbert P) :
    adT h (A + B) = adT h A + adT h B := by
  simp only [adT, mul_add, add_mul]

theorem horizon_ad_smul (P : SiteProfile) (h : TowerHorizon P) (c : ℂ)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) :
    adT h (c • A) = c • adT h A := by
  simp only [adT, mul_smul_comm, smul_mul_assoc]

theorem horizon_ad_one (P : SiteProfile) (h : TowerHorizon P) :
    adT h (1 : TowerHilbert P →L[ℂ] TowerHilbert P) = 1 := by
  simpa only [adT, mul_one] using h.unitary_right

theorem horizon_gns_inner_factor (P : SiteProfile) (h : TowerHorizon P)
    (A B : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hA : A ∈ theFactorObject P) (hB : B ∈ theFactorObject P) :
    inner ℂ (adT h A (hOmega P)) (adT h B (hOmega P)) =
      inner ℂ (A (hOmega P)) (B (hOmega P)) := by
  have he := omega_adT h (mul_mem (star_mem hA) hB)
  rw [adT_mul, adT_star, omega_product_inner, star_star,
    omega_product_inner, star_star] at he
  exact he

theorem horizon_gns_norm_factor (P : SiteProfile) (h : TowerHorizon P)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : A ∈ theFactorObject P) :
    ‖adT h A (hOmega P)‖ = ‖A (hOmega P)‖ := by
  have hs : ‖adT h A (hOmega P)‖ ^ 2 = ‖A (hOmega P)‖ ^ 2 := by
    rw [norm_sq_eq_re_inner (𝕜 := ℂ), norm_sq_eq_re_inner (𝕜 := ℂ),
      horizon_gns_inner_factor P h A A hA hA]
  nlinarith [norm_nonneg (adT h A (hOmega P)), norm_nonneg (A (hOmega P))]

theorem horizon_gns_dist_factor (P : SiteProfile) (h : TowerHorizon P)
    (A B : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hA : A ∈ theFactorObject P) (hB : B ∈ theFactorObject P) :
    dist (adT h A (hOmega P)) (adT h B (hOmega P)) =
      dist (A (hOmega P)) (B (hOmega P)) := by
  have hn := horizon_gns_norm_factor P h (A - B) (sub_mem hA hB)
  simpa only [adT_sub, sub_apply, dist_eq_norm] using hn

/-- The image of a local vector need not be local, so the codomain is the complete Hilbert space. -/
def horizonGNSPre (P : SiteProfile) (h : TowerHorizon P) :
    TowerPre P → TowerHilbert P :=
  Quotient.lift
    (fun x : TowerPt => adT h (towerPi P x.2) (hOmega P))
    (by
      rintro x y ⟨K, hx, hy, heq⟩
      have he : towerPi P x.2 = towerPi P y.2 := by
        calc
          towerPi P x.2 = towerPi P (tPush hx x.2) := (towerPi_compat hx x.2).symm
          _ = towerPi P (tPush hy y.2) := congrArg (fun a => towerPi P a) heq
          _ = towerPi P y.2 := towerPi_compat hy y.2
      rw [he])

theorem horizon_gns_pre_tof (P : SiteProfile) (h : TowerHorizon P)
    (N : ℕ) (A : Matrix (chainIdx N) (chainIdx N) ℂ) :
    horizonGNSPre P h (tof P N A) = adT h (towerPi P A) (hOmega P) := rfl

theorem horizon_gns_pre_add (P : SiteProfile) (h : TowerHorizon P)
    (x y : TowerPre P) :
    horizonGNSPre P h (x + y) = horizonGNSPre P h x + horizonGNSPre P h y := by
  obtain ⟨N, A, rfl⟩ := exists_tof x
  obtain ⟨M, B, rfl⟩ := exists_tof y
  rw [tof_add_hetero, horizon_gns_pre_tof, horizon_gns_pre_tof, horizon_gns_pre_tof,
    towerPi_add, towerPi_compat, towerPi_compat, horizon_ad_add]
  rfl

theorem horizon_gns_pre_smul (P : SiteProfile) (h : TowerHorizon P)
    (c : ℂ) (x : TowerPre P) :
    horizonGNSPre P h (c • x) = c • horizonGNSPre P h x := by
  obtain ⟨N, A, rfl⟩ := exists_tof x
  rw [tof_smul, horizon_gns_pre_tof, horizon_gns_pre_tof,
    towerPi_smul, horizon_ad_smul]
  rfl

def horizonGNSPreLinear (P : SiteProfile) (h : TowerHorizon P) :
    TowerPre P →ₗ[ℂ] TowerHilbert P where
  toFun := horizonGNSPre P h
  map_add' := horizon_gns_pre_add P h
  map_smul' := horizon_gns_pre_smul P h

theorem horizon_gns_pre_norm (P : SiteProfile) (h : TowerHorizon P) (x : TowerPre P) :
    ‖horizonGNSPre P h x‖ = ‖x‖ := by
  obtain ⟨N, A, rfl⟩ := exists_tof x
  rw [horizon_gns_pre_tof, horizon_gns_norm_factor P h _ (towerPi_mem_factor A),
    towerPi_omega, Completion.norm_coe]

theorem horizon_gns_pre_isometry (P : SiteProfile) (h : TowerHorizon P) :
    Isometry (horizonGNSPre P h) := by
  apply Isometry.of_dist_eq
  intro x y
  rw [dist_eq_norm, dist_eq_norm]
  have hs := (horizonGNSPreLinear P h).map_sub x y
  change horizonGNSPre P h (x - y) = horizonGNSPre P h x - horizonGNSPre P h y at hs
  rw [← hs, horizon_gns_pre_norm]

def horizonGNSMap (P : SiteProfile) (h : TowerHorizon P) :
    TowerHilbert P → TowerHilbert P :=
  Completion.extension (horizonGNSPre P h)

theorem horizon_gns_map_continuous (P : SiteProfile) (h : TowerHorizon P) :
    Continuous (horizonGNSMap P h) := Completion.continuous_extension

theorem horizon_gns_map_coe (P : SiteProfile) (h : TowerHorizon P) (x : TowerPre P) :
    horizonGNSMap P h (x : TowerHilbert P) = horizonGNSPre P h x :=
  Completion.extension_coe (horizon_gns_pre_isometry P h).uniformContinuous x

theorem horizon_gns_map_add (P : SiteProfile) (h : TowerHorizon P)
    (x y : TowerHilbert P) :
    horizonGNSMap P h (x + y) = horizonGNSMap P h x + horizonGNSMap P h y := by
  refine Completion.induction_on₂ x y (isClosed_eq
    ((horizon_gns_map_continuous P h).comp (continuous_fst.add continuous_snd))
    (((horizon_gns_map_continuous P h).comp continuous_fst).add
      ((horizon_gns_map_continuous P h).comp continuous_snd))) ?_
  intro a b
  rw [← Completion.coe_add, horizon_gns_map_coe, horizon_gns_pre_add,
    horizon_gns_map_coe, horizon_gns_map_coe]

theorem horizon_gns_map_smul (P : SiteProfile) (h : TowerHorizon P)
    (c : ℂ) (x : TowerHilbert P) :
    horizonGNSMap P h (c • x) = c • horizonGNSMap P h x := by
  refine Completion.induction_on x (isClosed_eq
    ((horizon_gns_map_continuous P h).comp (continuous_const.smul continuous_id))
    (continuous_const.smul (horizon_gns_map_continuous P h))) ?_
  intro a
  rw [← Completion.coe_smul, horizon_gns_map_coe, horizon_gns_pre_smul, horizon_gns_map_coe]

theorem horizon_gns_map_norm (P : SiteProfile) (h : TowerHorizon P) (x : TowerHilbert P) :
    ‖horizonGNSMap P h x‖ = ‖x‖ := by
  refine Completion.induction_on x (isClosed_eq
    (continuous_norm.comp (horizon_gns_map_continuous P h)) continuous_norm) ?_
  intro a
  rw [horizon_gns_map_coe, horizon_gns_pre_norm, Completion.norm_coe]

def horizonGNSIsometry (P : SiteProfile) (h : TowerHorizon P) :
    TowerHilbert P →ₗᵢ[ℂ] TowerHilbert P where
  toLinearMap :=
    { toFun := horizonGNSMap P h
      map_add' := horizon_gns_map_add P h
      map_smul' := horizon_gns_map_smul P h }
  norm_map' := horizon_gns_map_norm P h

/-- Norm preservation of the state automorphism passes the local formula to every factor element. -/
theorem horizon_gns_map_apply_factor (P : SiteProfile) (h : TowerHorizon P)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : A ∈ theFactorObject P) :
    horizonGNSMap P h (A (hOmega P)) = adT h A (hOmega P) := by
  have hl := (horizon_gns_map_continuous P h).continuousAt.tendsto.comp
    (expectation_omega_limit (P := P) A)
  have hlocal (N : ℕ) :
      horizonGNSMap P h (towerExpectation P N A (hOmega P)) =
        adT h (towerExpectation P N A) (hOmega P) := by
    rw [towerExpectation, towerPi_omega, horizon_gns_map_coe, horizon_gns_pre_tof]
  have hr : Tendsto (fun N => adT h (towerExpectation P N A) (hOmega P))
      atTop (𝓝 (adT h A (hOmega P))) := by
    have ht := expectation_omega_limit (P := P) A
    rw [Metric.tendsto_nhds] at ht ⊢
    intro ε hε
    filter_upwards [ht ε hε] with N hN
    rwa [horizon_gns_dist_factor P h _ A (expectation_mem_factor N A) hA]
  simp only [Function.comp_def, hlocal] at hl
  exact tendsto_nhds_unique hl hr

theorem horizon_gns_map_inverse (P : SiteProfile) (h : TowerHorizon P)
    (x : TowerHilbert P) :
    horizonGNSMap P h.inv (horizonGNSMap P h x) = x := by
  refine Completion.induction_on x (isClosed_eq
    ((horizon_gns_map_continuous P h.inv).comp (horizon_gns_map_continuous P h))
    continuous_id) ?_
  intro a
  obtain ⟨N, A, rfl⟩ := exists_tof a
  rw [horizon_gns_map_coe, horizon_gns_pre_tof,
    horizon_gns_map_apply_factor P h.inv _ (adT_mem h (towerPi_mem_factor A)),
    adT_inv_eq, adTinv_adT, towerPi_omega]

theorem horizon_gns_map_right_inverse (P : SiteProfile) (h : TowerHorizon P)
    (x : TowerHilbert P) :
    horizonGNSMap P h (horizonGNSMap P h.inv x) = x := by
  refine Completion.induction_on x (isClosed_eq
    ((horizon_gns_map_continuous P h).comp (horizon_gns_map_continuous P h.inv))
    continuous_id) ?_
  intro a
  obtain ⟨N, A, rfl⟩ := exists_tof a
  rw [horizon_gns_map_coe, horizon_gns_pre_tof,
    horizon_gns_map_apply_factor P h _ (adT_mem h.inv (towerPi_mem_factor A)),
    adT_inv_eq, adT_adTinv, towerPi_omega]

def horizonGNSUnitary (P : SiteProfile) (h : TowerHorizon P) :
    TowerHilbert P ≃ₗᵢ[ℂ] TowerHilbert P :=
  { horizonGNSIsometry P h with
    invFun := horizonGNSMap P h.inv
    left_inv := horizon_gns_map_inverse P h
    right_inv := horizon_gns_map_right_inverse P h }

theorem horizon_gns_apply_factor (P : SiteProfile) (h : TowerHorizon P)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) (hA : A ∈ theFactorObject P) :
    horizonGNSUnitary P h (A (hOmega P)) = adT h A (hOmega P) :=
  horizon_gns_map_apply_factor P h A hA

theorem horizon_gns_symm_apply (P : SiteProfile) (h : TowerHorizon P)
    (x : TowerHilbert P) :
    (horizonGNSUnitary P h).symm x = horizonGNSUnitary P h.inv x := rfl

theorem horizon_gns_omega (P : SiteProfile) (h : TowerHorizon P) :
    horizonGNSUnitary P h (hOmega P) = hOmega P := by
  have he := horizon_gns_apply_factor P h
    (1 : TowerHilbert P →L[ℂ] TowerHilbert P) (one_mem (theFactorObject P))
  simpa only [one_apply_eq_self, horizon_ad_one] using he

theorem horizon_gns_inner (P : SiteProfile) (h : TowerHorizon P)
    (x y : TowerHilbert P) :
    inner ℂ (horizonGNSUnitary P h x) (horizonGNSUnitary P h y) = inner ℂ x y :=
  (horizonGNSUnitary P h).inner_map_map x y

def realStateGenerators (P : SiteProfile) : Set (TowerHilbert P) :=
  {v | ∃ A : TowerHilbert P →L[ℂ] TowerHilbert P,
    A ∈ theFactorObject P ∧ IsSelfAdjoint A ∧ v = A (hOmega P)}

/-- The one shared real state subspace; no finite-level or abstract replacement is used. -/
def realStateSubspace (P : SiteProfile) : Submodule ℝ (TowerHilbert P) :=
  (Submodule.span ℝ (realStateGenerators P)).topologicalClosure

theorem real_state_generator_mem (P : SiteProfile)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P)
    (hA : A ∈ theFactorObject P) (hsa : IsSelfAdjoint A) :
    A (hOmega P) ∈ realStateSubspace P :=
  (Submodule.le_topologicalClosure _) (Submodule.subset_span ⟨A, hA, hsa, rfl⟩)

theorem real_state_subspace_closed (P : SiteProfile) :
    IsClosed (realStateSubspace P : Set (TowerHilbert P)) :=
  Submodule.isClosed_topologicalClosure _

instance instCompleteSpaceRealStateSubspace (P : SiteProfile) :
    CompleteSpace (realStateSubspace P) :=
  (real_state_subspace_closed P).completeSpace_coe

theorem horizon_gns_real_mem (P : SiteProfile) (h : TowerHorizon P)
    (x : TowerHilbert P) (hx : x ∈ realStateSubspace P) :
    horizonGNSUnitary P h x ∈ realStateSubspace P := by
  let L : TowerHilbert P →ₗ[ℝ] TowerHilbert P :=
    (horizonGNSUnitary P h).toLinearEquiv.toLinearMap.restrictScalars ℝ
  have hs : Submodule.span ℝ (realStateGenerators P) ≤
      (realStateSubspace P).comap L := by
    apply Submodule.span_le.mpr
    rintro v ⟨A, hA, hsa, rfl⟩
    change horizonGNSUnitary P h (A (hOmega P)) ∈ realStateSubspace P
    rw [horizon_gns_apply_factor P h A hA]
    apply real_state_generator_mem P _ (adT_mem h hA)
    change star (adT h A) = adT h A
    rw [← adT_star, hsa.star_eq]
  have hc : IsClosed ((realStateSubspace P).comap L : Set (TowerHilbert P)) :=
    (real_state_subspace_closed P).preimage (horizonGNSUnitary P h).continuous
  exact Submodule.topologicalClosure_minimal _ hs hc hx

theorem horizon_gns_real_image (P : SiteProfile) (h : TowerHorizon P) :
    (horizonGNSUnitary P h) '' (realStateSubspace P : Set (TowerHilbert P)) =
      (realStateSubspace P : Set (TowerHilbert P)) := by
  apply Set.Subset.antisymm
  · rintro y ⟨x, hx, rfl⟩
    exact horizon_gns_real_mem P h x hx
  · intro x hx
    refine ⟨horizonGNSUnitary P h.inv x, horizon_gns_real_mem P h.inv x hx, ?_⟩
    exact horizon_gns_map_right_inverse P h x

/-- The same implementer restricted to the real closed state subspace. -/
def horizonGNSRealUnitary (P : SiteProfile) (h : TowerHorizon P) :
    realStateSubspace P ≃ₗᵢ[ℝ] realStateSubspace P where
  toFun x := ⟨horizonGNSUnitary P h x, horizon_gns_real_mem P h x x.property⟩
  invFun x := ⟨horizonGNSUnitary P h.inv x, horizon_gns_real_mem P h.inv x x.property⟩
  left_inv x := by
    apply Subtype.ext
    exact horizon_gns_map_inverse P h x
  right_inv x := by
    apply Subtype.ext
    exact horizon_gns_map_right_inverse P h x
  map_add' x y := by
    apply Subtype.ext
    exact map_add (horizonGNSUnitary P h) (x : TowerHilbert P) (y : TowerHilbert P)
  map_smul' a x := by
    apply Subtype.ext
    exact ((horizonGNSUnitary P h).toLinearEquiv.toLinearMap.restrictScalars ℝ).map_smul a x
  norm_map' x := (horizonGNSUnitary P h).norm_map x

theorem horizon_gns_real_apply (P : SiteProfile) (h : TowerHorizon P)
    (x : realStateSubspace P) :
    (horizonGNSRealUnitary P h x : TowerHilbert P) =
      horizonGNSUnitary P h (x : TowerHilbert P) := rfl

#print axioms horizon_ad_add
#print axioms horizon_ad_smul
#print axioms horizon_ad_one
#print axioms horizon_gns_inner_factor
#print axioms horizon_gns_norm_factor
#print axioms horizon_gns_dist_factor
#print axioms horizonGNSPre
#print axioms horizon_gns_pre_tof
#print axioms horizon_gns_pre_add
#print axioms horizon_gns_pre_smul
#print axioms horizonGNSPreLinear
#print axioms horizon_gns_pre_norm
#print axioms horizon_gns_pre_isometry
#print axioms horizonGNSMap
#print axioms horizon_gns_map_continuous
#print axioms horizon_gns_map_coe
#print axioms horizon_gns_map_add
#print axioms horizon_gns_map_smul
#print axioms horizon_gns_map_norm
#print axioms horizonGNSIsometry
#print axioms horizon_gns_map_apply_factor
#print axioms horizon_gns_map_inverse
#print axioms horizon_gns_map_right_inverse
#print axioms horizonGNSUnitary
#print axioms horizon_gns_apply_factor
#print axioms horizon_gns_symm_apply
#print axioms horizon_gns_omega
#print axioms horizon_gns_inner
#print axioms realStateGenerators
#print axioms realStateSubspace
#print axioms real_state_generator_mem
#print axioms real_state_subspace_closed
#print axioms instCompleteSpaceRealStateSubspace
#print axioms horizon_gns_real_mem
#print axioms horizon_gns_real_image
#print axioms horizonGNSRealUnitary
#print axioms horizon_gns_real_apply

end
end ChatgptAudit.Covariant053
