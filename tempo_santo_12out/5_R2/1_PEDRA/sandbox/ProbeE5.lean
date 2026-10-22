import Mathlib
import TGLExt.LocalBreuerGap
import TGLExt.ModularFlow
import TGLExt.FiniteTomita
import TGLExt.Ergodicity
import TGLExt.PageInformation
import TGLExt.TheSingularExpectation
import TGLExt.TheTraceIsNotErasable
import TGLExt.TheAxiomAndTheFalseWitness
import TGLExt.TheVerbSelectsTheAction
import TGLExt.IALDJones
import TGLExt.TheLivingWord
import TGLExt.BisognanoWichmann
import TGLExt.Fundacao
import TGLExt.AbsoluteOne
import TGLExt.O16.PolarMinimalPeriod_v2
import TGLExt.O16.ProbeNonKMS_v3
import TGLExt.TheImportedSecondQuantization
import TGLExt.V350L2CharacterMultiplier

/-! Sonda da PEDRA R2 (F1.TEMPO, construtor da pedra corrigida): só as construções NOVAS da lista E5, antes de
montar a pedra. Mesmas importações da pedra. Nenhum literal da constante da casa. -/

set_option autoImplicit false
set_option maxHeartbeats 1000000

namespace TGLExt.ProbeE5

open Filter Topology
open scoped Matrix ComplexOrder Pointwise

noncomputable section

-- E5.13 (obrigatória): face finita, a = E₀₁, b = E₁₀ na forma literal do ADENDO
theorem gibbs_rho_two_thirds_E01_E10 :
    gibbs (rhoD ![(2 / 3 : ℝ), 1 / 3]) (!![0, 1; 0, 0] * !![0, 0; 1, 0]) = (2 / 3 : ℂ) := by
  simp [gibbs, rhoD, Matrix.trace, Fin.sum_univ_two, Matrix.mul_apply]

theorem gibbs_rho_two_thirds_E10_E01 :
    gibbs (rhoD ![(2 / 3 : ℝ), 1 / 3]) (!![0, 0; 1, 0] * !![0, 1; 0, 0]) = (1 / 3 : ℂ) := by
  simp [gibbs, rhoD, Matrix.trace, Fin.sum_univ_two, Matrix.mul_apply]

theorem identity_flow_not_kms_finite :
    gibbs (rhoD ![(2 / 3 : ℝ), 1 / 3]) (!![0, 1; 0, 0] * !![0, 0; 1, 0])
      ≠ gibbs (rhoD ![(2 / 3 : ℝ), 1 / 3]) (!![0, 0; 1, 0] * !![0, 1; 0, 0]) := by
  rw [gibbs_rho_two_thirds_E01_E10, gibbs_rho_two_thirds_E10_E01]
  norm_num

theorem identity_flow_not_kms_finite' :
    ¬ ∀ x y : Matrix (Fin 2) (Fin 2) ℂ,
      gibbs (rhoD ![(2 / 3 : ℝ), 1 / 3]) (x * y) = gibbs (rhoD ![(2 / 3 : ℝ), 1 / 3]) (y * x) :=
  fun h => identity_flow_not_kms_finite (h _ _)

example : gibbs (rhoD ![(2 / 3 : ℝ), 1 / 3]) (!![0, 1; 0, 0] * !![0, 0; 1, 0])
      - gibbs (rhoD ![(2 / 3 : ℝ), 1 / 3]) (!![0, 0; 1, 0] * !![0, 1; 0, 0]) = (1 / 3 : ℂ) := by
  rw [gibbs_rho_two_thirds_E01_E10, gibbs_rho_two_thirds_E10_E01]
  norm_num

theorem tracial_state_satisfies_pair_identity :
    gibbs (rhoD ![(1 / 2 : ℝ), 1 / 2]) (!![0, 1; 0, 0] * !![0, 0; 1, 0])
      = gibbs (rhoD ![(1 / 2 : ℝ), 1 / 2]) (!![0, 0; 1, 0] * !![0, 1; 0, 0]) := by
  simp [gibbs, rhoD, Matrix.trace, Fin.sum_univ_two, Matrix.mul_apply]

-- E5.13 (opcional): habitante AQFT (rota da sonda P02 da rodada 2, tentativa preservada)
theorem star_inner_eq_state (W : TGL.SpecificAQFT.TGLSpecificAQFTWitness) (A B : W.H →L[ℂ] W.H) :
    inner ℂ ((star A) W.vac) (B W.vac) = inner ℂ W.vac ((A * B) W.vac) := by
  rw [ContinuousLinearMap.star_eq_adjoint, ContinuousLinearMap.adjoint_inner_left]
  rfl

theorem probe_identity_flow_not_kms_inhabited :
    ¬ TGLExt.ContratoQGv31.KMSAt TGLExt.theSpecificAQFTWitness
      (fun _ => LinearIsometryEquiv.refl ℂ TGLExt.theSpecificAQFTWitness.H) 1 := by
  obtain ⟨A, B, hA, hB, hne⟩ := TGLExt.omega_not_tracial TGLExt.mixProfile (by
    rw [show TGLExt.mixProfile.w 0 = 1 / 3 from rfl]
    norm_num)
  have hnet : TGLExt.theSpecificAQFTWitness.net TGL.SpecificAQFT.rightWedge
      = TGLExt.theFactorObject TGLExt.mixProfile :=
    TGLExt.wedgeNet_M TGLExt.hasRW_rightWedge TGLExt.not_hasLW_rightWedge
  have hA' : A ∈ TGLExt.theSpecificAQFTWitness.net TGL.SpecificAQFT.rightWedge := by
    rw [hnet]; exact hA
  have hB' : B ∈ TGLExt.theSpecificAQFTWitness.net TGL.SpecificAQFT.rightWedge := by
    rw [hnet]; exact hB
  refine ChatgptAudit.NonKMSProbe.identity_flow_not_kms TGLExt.theSpecificAQFTWitness A B hA' hB' ?_
  intro hc
  apply hne
  exact (star_inner_eq_state TGLExt.theSpecificAQFTWitness A B).symm.trans
    (hc.trans (star_inner_eq_state TGLExt.theSpecificAQFTWitness B A))

-- E5.06 (sonda AUD-4 em termo): o enunciado KMS-grupo em ρ = 1
example : ∀ s t a, sigma (1 : Matrix (Fin 2) (Fin 2) ℂ) s (sigma 1 t a) = sigma 1 (s + t) a :=
  fun s t a => sigma_sigma (1 : Matrix (Fin 2) (Fin 2) ℂ) s t a

example : (1 : Matrix (Fin 2) (Fin 2) ℂ).PosDef := Matrix.PosDef.one

-- E5.12: T10.b sem a hipótese κ ≠ 0
theorem clock_reads_modulo_period (κ t : ℝ) :
    Circle.exp (κ * (t + 2 * Real.pi / κ)) = Circle.exp (κ * t) := by
  rcases eq_or_ne κ 0 with rfl | hκ
  · simp
  · have hturn : κ * (2 * Real.pi / κ) = 2 * Real.pi := by field_simp
    exact (ChatgptAudit.PolarPeriod016.one_turn_gives_faithful_period hκ (Or.inl hturn)
      (t + 2 * Real.pi / κ) t).mpr ⟨1, by push_cast; ring⟩

-- E5.08 (opcional): o canal ótico nas populações, genérico em θ, sem a constante da casa
def halfJ : Matrix (Fin 2) (Fin 2) ℝ := !![1 / 2, 1 / 2; 1 / 2, 1 / 2]

def opticalPopulationMap (θ : ℝ) : Matrix (Fin 2) (Fin 2) ℝ :=
  halfJ + (1 - 2 * Real.sin θ ^ 2) • (1 - halfJ)

theorem opticalPopulationMap_mulVec_zero (θ : ℝ) (x : Fin 2 → ℝ) :
    (opticalPopulationMap θ).mulVec x 0 = x 0 - Real.sin θ ^ 2 * (x 0 - x 1) := by
  simp [opticalPopulationMap, halfJ, Matrix.mulVec, dotProduct, Fin.sum_univ_two, Matrix.one_apply]
  ring

theorem opticalPopulationMap_mulVec_one (θ : ℝ) (x : Fin 2 → ℝ) :
    (opticalPopulationMap θ).mulVec x 1 = x 1 + Real.sin θ ^ 2 * (x 0 - x 1) := by
  simp [opticalPopulationMap, halfJ, Matrix.mulVec, dotProduct, Fin.sum_univ_two, Matrix.one_apply]
  ring

theorem optical_channel_fixed_state_is_half_identity {θ : ℝ} (hθ : Real.sin θ ≠ 0) (x : Fin 2 → ℝ) :
    (opticalPopulationMap θ).mulVec x = x ↔ x 0 = x 1 := by
  have hs : Real.sin θ ^ 2 ≠ 0 := pow_ne_zero 2 hθ
  constructor
  · intro h
    have e0 := congrFun h 0
    rw [opticalPopulationMap_mulVec_zero] at e0
    have h2 : Real.sin θ ^ 2 * (x 0 - x 1) = 0 := by linarith
    rcases mul_eq_zero.mp h2 with h' | h'
    · exact absurd h' hs
    · linarith
  · intro hx
    rw [funext_iff, Fin.forall_fin_two, opticalPopulationMap_mulVec_zero, opticalPopulationMap_mulVec_one, hx]
    constructor <;> ring

theorem optical_channel_unique_fixed_population {θ : ℝ} (hθ : Real.sin θ ≠ 0) (x : Fin 2 → ℝ)
    (hfix : (opticalPopulationMap θ).mulVec x = x) (hsum : x 0 + x 1 = 1) : x = ![1 / 2, 1 / 2] := by
  have hx := (optical_channel_fixed_state_is_half_identity hθ x).mp hfix
  rw [funext_iff, Fin.forall_fin_two]
  constructor <;> simp <;> linarith

theorem half_populations_state :
    rhoD (![1 / 2, 1 / 2] : Fin 2 → ℝ) = (1 / 2 : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ) := by
  ext i j
  fin_cases i <;> fin_cases j <;> simp [rhoD] <;> norm_num

-- controle do opcional: em sin θ = 0 o canal é a identidade e TUDO é fixo (a hipótese pesa)
theorem optical_channel_trivial_when_sin_zero {θ : ℝ} (hθ : Real.sin θ = 0) (x : Fin 2 → ℝ) :
    (opticalPopulationMap θ).mulVec x = x := by
  rw [funext_iff, Fin.forall_fin_two, opticalPopulationMap_mulVec_zero, opticalPopulationMap_mulVec_one, hθ]
  constructor <;> ring

-- AUD (copiados dos arquivos da auditoria R1, dentro deste namespace)
def scalarScaling : DualScalingData (Matrix (Fin 2) (Fin 2) ℂ) where
  tau := fun x => ‖x 0 1‖
  theta := fun s x => (((Real.exp (-s)) : ℝ) : ℂ) • x
  scaling := fun s x => by
    show ‖((((Real.exp (-s)) : ℝ) : ℂ) • x) 0 1‖ = Real.exp (-s) * ‖x 0 1‖
    rw [Matrix.smul_apply, smul_eq_mul, norm_mul, Complex.norm_real, Real.norm_eq_abs,
      abs_of_pos (Real.exp_pos _)]

theorem aud_scalar_obeys_agape (x : Matrix (Fin 2) (Fin 2) ℂ) (hx : x 0 1 ≠ 0) :
    let D := scalarScaling
    (∀ s : ℝ, s ≠ 0 → ∀ m' : Matrix (Fin 2) (Fin 2) ℂ, D.theta s m' = m' → D.tau m' = 0) ∧
    (∀ s : ℝ, D.tau (D.theta s x) < D.tau (D.theta (s - 1) x)) ∧
    (∀ B : ℝ, ∃ s : ℝ, B < D.tau (D.theta s x)) ∧
    (∀ s : ℝ, 0 < D.tau (D.theta s x)) ∧
    (∀ ε : ℝ, 0 < ε → ∃ s : ℝ, D.tau (D.theta s x) < ε) ∧
    (∀ a : ℝ, Real.exp (-a) = 1 ↔ a = 0) := by
  intro D
  exact TGLExt.Fundacao.agape D (m := x) (norm_pos_iff.mpr hx)

theorem aud_scalar_erases_the_record :
    (scalarScaling.theta 1 (1 : Matrix (Fin 2) (Fin 2) ℂ)).trace ≠ (1 : Matrix (Fin 2) (Fin 2) ℂ).trace := by
  show ((((Real.exp (-1)) : ℝ) : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ)).trace ≠ (1 : Matrix (Fin 2) (Fin 2) ℂ).trace
  rw [Matrix.trace_smul, Matrix.trace_one, smul_eq_mul]
  intro h
  have h2 : (((Real.exp (-1)) : ℝ) : ℂ) = 1 := by
    have hc : ((Fintype.card (Fin 2) : ℕ) : ℂ) ≠ 0 := by norm_num
    exact mul_right_cancel₀ hc (by rw [h, one_mul])
  have h3 : Real.exp (-1) = 1 := by exact_mod_cast h2
  have h4 := (Real.exp_eq_one_iff (-1)).mp h3
  norm_num at h4

theorem aud_discrete_step_can_be_a_post :
    IsIdempotentElem (!![1 / 2, 1 / 2; 1 / 2, 1 / 2] : Matrix (Fin 2) (Fin 2) ℝ) := by
  unfold IsIdempotentElem
  ext i j
  fin_cases i <;> fin_cases j <;> simp [Matrix.mul_apply, Fin.sum_univ_two] <;> norm_num

theorem aud_attractor_state_has_full_rank :
    ((1 / 2 : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ)).rank = 2 := by
  have hu : IsUnit ((1 / 2 : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ)) := by
    rw [Matrix.isUnit_iff_isUnit_det, Matrix.det_smul, Matrix.det_one, mul_one, isUnit_iff_ne_zero]
    norm_num
  rw [Matrix.rank_of_isUnit _ hu, Fintype.card_fin]

theorem aud_attractor_state_purity_half :
    purityR ((1 / 2 : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ)) = 1 / 2 := by
  unfold purityR
  simp only [Fin.sum_univ_two, Matrix.smul_apply, Matrix.one_apply_eq, smul_eq_mul]
  rw [Matrix.one_apply_ne (by decide : (0 : Fin 2) ≠ 1), Matrix.one_apply_ne (by decide : (1 : Fin 2) ≠ 0)]
  simp [Complex.normSq_apply]
  norm_num

theorem aud_clock_runs_unless_equal_populations (a b : ℝ) (ha : 0 < a) (hb : 0 < b) (hab : a ≠ b) :
    ¬ ∀ t : ℝ, sigma (rhoD ![a, b]) t (!![0, 1; 0, 0] : Matrix (Fin 2) (Fin 2) ℂ) = !![0, 1; 0, 0] := by
  intro h
  have hd : ∀ i, 0 < (![a, b] : Fin 2 → ℝ) i := by
    intro i; fin_cases i <;> simp [ha, hb]
  have hinj : Function.Injective (![a, b] : Fin 2 → ℝ) := by
    intro i j hij
    fin_cases i <;> fin_cases j <;> simp_all
  have hfix := (sigma_fixed_iff_diag ![a, b] hd hinj _).mp h
  have h01 := congrFun (congrFun hfix 0) 1
  simp [diagExpect] at h01

theorem aud_clock_stops_when_equal_populations (a : ℝ) (t : ℝ) (x : Matrix (Fin 2) (Fin 2) ℂ) :
    sigma (rhoD ![a, a]) t x = x := by
  have hc : rhoD ![a, a] = (a : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ) := by
    ext i j
    fin_cases i <;> fin_cases j <;> simp [rhoD]
  exact sigma_fixed_of_commute _ _ (by rw [hc]; exact (Commute.one_left x).smul_left (a : ℂ)) t

theorem aud_two_by_two_symplectic (M : Matrix (Fin 2) (Fin 2) ℝ) :
    Mᵀ * !![0, 1; -1, 0] * M = M.det • !![0, 1; -1, 0] := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [Matrix.mul_apply, Fin.sum_univ_two, Matrix.det_fin_two, Matrix.transpose_apply] <;> ring

theorem aud_boost_is_symplectic (s : ℝ) :
    (TGLExt.boost s)ᵀ * !![0, 1; -1, 0] * TGLExt.boost s = !![0, 1; -1, 0] := by
  rw [aud_two_by_two_symplectic, TGLExt.boost_det, one_smul]

end

end TGLExt.ProbeE5

#print axioms TGLExt.ProbeE5.gibbs_rho_two_thirds_E01_E10
#print axioms TGLExt.ProbeE5.gibbs_rho_two_thirds_E10_E01
#print axioms TGLExt.ProbeE5.identity_flow_not_kms_finite
#print axioms TGLExt.ProbeE5.identity_flow_not_kms_finite'
#print axioms TGLExt.ProbeE5.tracial_state_satisfies_pair_identity
#print axioms TGLExt.ProbeE5.star_inner_eq_state
#print axioms TGLExt.ProbeE5.probe_identity_flow_not_kms_inhabited
#print axioms TGLExt.ProbeE5.clock_reads_modulo_period
#print axioms TGLExt.ProbeE5.optical_channel_fixed_state_is_half_identity
#print axioms TGLExt.ProbeE5.optical_channel_unique_fixed_population
#print axioms TGLExt.ProbeE5.half_populations_state
#print axioms TGLExt.ProbeE5.optical_channel_trivial_when_sin_zero
#print axioms TGLExt.ProbeE5.scalarScaling
#print axioms TGLExt.ProbeE5.aud_scalar_obeys_agape
#print axioms TGLExt.ProbeE5.aud_scalar_erases_the_record
#print axioms TGLExt.ProbeE5.aud_discrete_step_can_be_a_post
#print axioms TGLExt.ProbeE5.aud_attractor_state_has_full_rank
#print axioms TGLExt.ProbeE5.aud_attractor_state_purity_half
#print axioms TGLExt.ProbeE5.aud_clock_runs_unless_equal_populations
#print axioms TGLExt.ProbeE5.aud_clock_stops_when_equal_populations
#print axioms TGLExt.ProbeE5.aud_two_by_two_symplectic
#print axioms TGLExt.ProbeE5.aud_boost_is_symplectic
