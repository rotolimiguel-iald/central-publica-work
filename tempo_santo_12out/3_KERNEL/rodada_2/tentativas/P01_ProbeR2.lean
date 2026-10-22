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

/-! Sonda da rodada 2 (F1.TEMPO, construtor do kernel): só as construções NOVAS, antes de montar a pedra. -/

set_option autoImplicit false
set_option maxHeartbeats 1000000

namespace TGLExt.ProbeR2

open Filter Topology
open scoped Matrix ComplexOrder

noncomputable section

-- 0. as constantes estão no fecho das importações (sem linha de import nova)
#check @TGLExt.theSpecificAQFTWitness
#check @TGLExt.omega_not_tracial
#check @TGLExt.wedgeNet_M
#check @TGLExt.mixProfile

-- 1. habitante AQFT de T3.b(iii): o fluxo identidade NÃO é KMS para a testemunha concreta
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
  rw [ContinuousLinearMap.star_eq_adjoint, ContinuousLinearMap.star_eq_adjoint,
    ContinuousLinearMap.adjoint_inner_left, ContinuousLinearMap.adjoint_inner_left] at hc
  exact hc

-- 2. face finita: o fluxo identidade satisfaz a forma KMS no par (E₀₁, E₁₀) ⟺ estado tracial
def E01 : Matrix (Fin 2) (Fin 2) ℂ := Matrix.single 0 1 1
def E10 : Matrix (Fin 2) (Fin 2) ℂ := Matrix.single 1 0 1

theorem gibbs_E01_E10 (d : Fin 2 → ℝ) : gibbs (rhoD d) (E01 * E10) = (d 0 : ℂ) := by
  simp [E01, E10, gibbs, rhoD, Matrix.trace, Fin.sum_univ_two]

theorem gibbs_E10_E01 (d : Fin 2 → ℝ) : gibbs (rhoD d) (E10 * E01) = (d 1 : ℂ) := by
  simp [E01, E10, gibbs, rhoD, Matrix.trace, Fin.sum_univ_two]

theorem identity_flow_kms_pair_iff (d : Fin 2 → ℝ) :
    gibbs (rhoD d) (E01 * E10) = gibbs (rhoD d) (E10 * E01) ↔ d 0 = d 1 := by
  rw [gibbs_E01_E10, gibbs_E10_E01]
  exact Complex.ofReal_inj

theorem finite_face_identity_flow_not_kms :
    gibbs (rhoD ![(2 / 3 : ℝ), 1 / 3]) (E01 * E10) ≠ gibbs (rhoD ![(2 / 3 : ℝ), 1 / 3]) (E10 * E01) := by
  rw [Ne, identity_flow_kms_pair_iff]
  norm_num

example : gibbs (rhoD ![(1 : ℝ), 1]) (E01 * E10) = gibbs (rhoD ![(1 : ℝ), 1]) (E10 * E01) :=
  (identity_flow_kms_pair_iff _).mpr rfl

-- 3. sonda L2 com ENUNCIADO (T2.b em M₂(ℂ), norma de operador L2)
theorem no_bounded_spectral_translation {A : Type*} [NormedRing A] [NormedAlgebra ℂ A]
    [CompleteSpace A] [Nontrivial A] (V : Aˣ) (H : A) {s : ℂ} (hs : s ≠ 0) :
    (↑V⁻¹ : A) * H * ↑V ≠ H + algebraMap ℂ A s := by
  intro h
  have hσ : spectrum ℂ H = spectrum ℂ H + {s} := by
    have h1 : spectrum ℂ ((↑V⁻¹ : A) * H * ↑V) = spectrum ℂ H := spectrum.units_conjugate'
    rw [h, ← spectrum.add_singleton_eq] at h1
    exact h1.symm
  have hcont : Continuous fun w : ℂ => (w * (starRingEnd ℂ) s).re :=
    Complex.continuous_re.comp (continuous_id.mul continuous_const)
  obtain ⟨z, hz, hmax⟩ :=
    (spectrum.isCompact H).exists_isMaxOn (spectrum.nonempty H) hcont.continuousOn
  have hzs : z + s ∈ spectrum ℂ H := by
    rw [hσ]; exact Set.add_mem_add hz (Set.mem_singleton s)
  have hle : ((z + s) * (starRingEnd ℂ) s).re ≤ (z * (starRingEnd ℂ) s).re :=
    isMaxOn_iff.mp hmax (z + s) hzs
  have hpos : 0 < Complex.normSq s := Complex.normSq_pos.mpr hs
  have hexp : ((z + s) * (starRingEnd ℂ) s).re = (z * (starRingEnd ℂ) s).re + Complex.normSq s := by
    rw [add_mul, Complex.add_re, Complex.mul_conj, Complex.ofReal_re]
  linarith

section L2Probe
open scoped Matrix.Norms.L2Operator

set_option maxHeartbeats 4000000 in
theorem probe_bounded_spectral_translation :
    (((1 : (Matrix (Fin 2) (Fin 2) ℂ)ˣ)⁻¹ : (Matrix (Fin 2) (Fin 2) ℂ)ˣ) : Matrix (Fin 2) (Fin 2) ℂ) * 0
        * ((1 : (Matrix (Fin 2) (Fin 2) ℂ)ˣ) : Matrix (Fin 2) (Fin 2) ℂ)
      ≠ 0 + algebraMap ℂ (Matrix (Fin 2) (Fin 2) ℂ) 1 := by
  haveI : CompleteSpace (Matrix (Fin 2) (Fin 2) ℂ) := FiniteDimensional.complete ℂ _
  exact no_bounded_spectral_translation (A := Matrix (Fin 2) (Fin 2) ℂ) 1 0 one_ne_zero

end L2Probe

-- 4. o estado ½·1 tem posto 2 (pleno) e pureza ½ (achado AUD-6/M7)
theorem half_identity_has_full_rank : ((1 / 2 : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ)).rank = 2 := by
  have hu : IsUnit ((1 / 2 : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ)) := by
    refine (Matrix.isUnit_iff_isUnit_det _).mpr ?_
    rw [Matrix.det_smul, Matrix.det_one]
    simp
  rw [Matrix.rank_of_isUnit _ hu, Fintype.card_fin]

theorem half_identity_purity : purityR ((1 / 2 : ℂ) • (1 : Matrix (Fin 2) (Fin 2) ℂ)) = 1 / 2 := by
  simp [purityR, Fin.sum_univ_two, Matrix.one_apply, Complex.normSq]
  norm_num

-- 5. hipóteses sem peso removidas
theorem no_finite_instant_is_the_post {A : Type*} [Ring A] [Algebra ℂ A] {P : A} (hP1 : P ≠ 1) (t : ℝ) :
    TheAxiomAndTheFalseWitness.axiomFlow P t ≠ P := by
  intro h
  unfold TheAxiomAndTheFalseWitness.axiomFlow at h
  have h2 : ((Real.exp (-t) : ℝ) : ℂ) • ((1 : A) - P) = 0 := add_left_cancel (h.trans (add_zero P).symm)
  have hc : ((Real.exp (-t) : ℝ) : ℂ) ≠ 0 := by exact_mod_cast (Real.exp_pos _).ne'
  have h3 : (1 : A) - P = 0 := by
    calc (1 : A) - P = (((Real.exp (-t) : ℝ) : ℂ)⁻¹ * ((Real.exp (-t) : ℝ) : ℂ)) • ((1 : A) - P) := by
          rw [inv_mul_cancel₀ hc, one_smul]
      _ = ((Real.exp (-t) : ℝ) : ℂ)⁻¹ • (((Real.exp (-t) : ℝ) : ℂ) • ((1 : A) - P)) := by rw [mul_smul]
      _ = 0 := by rw [h2, smul_zero]
  exact hP1 (sub_eq_zero.mp h3).symm

theorem clock_reads_modulo_period (κ t : ℝ) :
    Circle.exp (κ * (t + 2 * Real.pi / κ)) = Circle.exp (κ * t) := by
  rcases eq_or_ne κ 0 with rfl | hκ
  · simp
  · have hturn : κ * (2 * Real.pi / κ) = 2 * Real.pi := by field_simp
    exact (ChatgptAudit.PolarPeriod016.one_turn_gives_faithful_period hκ (Or.inl hturn)
      (t + 2 * Real.pi / κ) t).mpr ⟨1, by push_cast; ring⟩

-- 6. AUD-4 em termo: o enunciado KMS-grupo vale também para o fluxo congelado do estado tracial
example : (∀ (t : ℝ) (a : Matrix (Fin 2) (Fin 2) ℂ), sigma (absoluteRho (Fin 2)) t a = a) ∧
    (∀ a b : Matrix (Fin 2) (Fin 2) ℂ,
      gibbs (absoluteRho (Fin 2)) (a * b) = gibbs (absoluteRho (Fin 2)) (b * Delta (absoluteRho (Fin 2)) a)) :=
  ⟨fun t a => absoluteOne_flow_trivial (Region := Unit) () t a,
    fun a b => gibbs_kms (absoluteRho (Fin 2)) absoluteRho_posDef a b⟩

end

end TGLExt.ProbeR2

#print axioms TGLExt.ProbeR2.probe_identity_flow_not_kms_inhabited
#print axioms TGLExt.ProbeR2.gibbs_E01_E10
#print axioms TGLExt.ProbeR2.identity_flow_kms_pair_iff
#print axioms TGLExt.ProbeR2.finite_face_identity_flow_not_kms
#print axioms TGLExt.ProbeR2.probe_bounded_spectral_translation
#print axioms TGLExt.ProbeR2.half_identity_has_full_rank
#print axioms TGLExt.ProbeR2.half_identity_purity
#print axioms TGLExt.ProbeR2.no_finite_instant_is_the_post
#print axioms TGLExt.ProbeR2.clock_reads_modulo_period
