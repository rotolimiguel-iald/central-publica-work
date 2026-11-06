import TGLExt.F1Fecho394.CanonicalFockFaithfulWeightR2
import TGLExt.F1Fecho394.RegularCoreFiniteWeightR3
/-! Actual Fock weight: order normality, an explicit finite positive element
of weight one, and a strongly dense finite-square left ideal. These statements
are on the already constructed core. No trace or modular identification follows
merely from the terminology of a dual weight. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
set_option synthInstance.maxHeartbeats 1000000
noncomputable section
namespace F1Fecho.CanonicalFockFiniteWeight
open TGLExt.ImportedSQ F1Rede.BosonicFock TGLV350.Regular Filter
open F1Fecho.CanonicalFockRegular F1Fecho.CanonicalFockWeight
open F1Fecho.RegularCoreAverage F1Fecho.RegularCoreFiniteWeight
open scoped Topology ENNReal NNReal

theorem weight_internal_normal
    {ι : Type*} [Preorder ι] [IsDirectedOrder ι] [Nonempty ι]
    (A : ι → core.toStarSubalgebra) (S : core.toStarSubalgebra)
    (hpos : ∀ i, 0 ≤ A i) (hmono : Monotone A) (hS : IsLUB (Set.range A) S)
    (hSpos : 0 ≤ S) :
    weight ⟨S.val,S.property,hSpos⟩ =
      ⨆ i, weight ⟨(A i).val,(A i).property,hpos i⟩ :=
  dualQuadraticIntegral_preserves_internal_isLUB core A S hpos hmono hS regularFockVacuum

def averageSquare (h : ℝ) : PositiveInput :=
  ⟨star (F1Fecho.RegularCoreAverage.regularAverage fockFlow h) * F1Fecho.RegularCoreAverage.regularAverage fockFlow h,
    core.mul_mem (core.toStarSubalgebra.star_mem' (F1Fecho.RegularCoreAverage.regularAverage_mem fockFlow M h))
      (F1Fecho.RegularCoreAverage.regularAverage_mem fockFlow M h),star_mul_self_nonneg (F1Fecho.RegularCoreAverage.regularAverage fockFlow h)⟩

theorem weight_averageSquare (h : ℝ) (hh : 0 < h) :
    weight (averageSquare h) = ENNReal.ofReal h⁻¹ := by
  change dualQuadraticIntegral (star (F1Fecho.RegularCoreAverage.regularAverage fockFlow h) * F1Fecho.RegularCoreAverage.regularAverage fockFlow h)
    regularFockVacuum = _
  rw [F1Fecho.RegularCoreFiniteWeight.regularAverage_dualQuadraticIntegral fockFlow h hh, regularFockVacuum_norm]
  simp

theorem exists_positive_finite_weight : ∃ A : PositiveInput, 0 < weight A ∧ weight A < ⊤ := by
  refine ⟨averageSquare 1, ?_, ?_⟩ <;> rw [weight_averageSquare 1 zero_lt_one] <;> norm_num

theorem finiteSquare_scalar_finite
    (A : RegularHilbert F →L[ℂ] RegularHilbert F) (hf : HasFiniteDualSquare A) :
    dualQuadraticIntegral (star A * A) regularFockVacuum < ⊤ := by
  obtain ⟨C,hC⟩ := hf
  have he := hC regularFockVacuum
  rw [regularFockVacuum_norm, one_pow, ENNReal.ofReal_one, mul_one] at he
  exact he.trans_lt ENNReal.coe_lt_top

def finiteLeftIdeal : Submodule ℂ core.toStarSubalgebra where
  carrier := {A | HasFiniteDualSquare A.val}
  zero_mem' := HasFiniteDualSquare.zero
  add_mem' := fun hA hB => HasFiniteDualSquare.add _ _ hA hB
  smul_mem' := fun c _ hA => HasFiniteDualSquare.smul c _ hA

theorem finiteLeftIdeal_left_mul (B A : core.toStarSubalgebra)
    (hA : A ∈ finiteLeftIdeal) : B*A ∈ finiteLeftIdeal :=
  HasFiniteDualSquare.left_mul B.val A.val hA

theorem finite_square_strong_density (A : core.toStarSubalgebra) :
    (∀ h : ℝ, 0 < h → dualQuadraticIntegral
      (star (A.val * F1Fecho.RegularCoreAverage.regularAverage fockFlow h) * (A.val * F1Fecho.RegularCoreAverage.regularAverage fockFlow h))
      regularFockVacuum < ⊤) ∧
    (∀ h : ℝ, A.val * F1Fecho.RegularCoreAverage.regularAverage fockFlow h ∈ core) ∧
    (∀ v, Tendsto (fun h : ℝ => (A.val * F1Fecho.RegularCoreAverage.regularAverage fockFlow h) v)
      (𝓝[>] 0) (𝓝 (A.val v))) := by
  refine ⟨?_, ?_, ?_⟩
  · intro h hh
    exact finiteSquare_scalar_finite _ (HasFiniteDualSquare.left_mul A.val _
      (F1Fecho.RegularCoreFiniteWeight.regularAverage_hasFiniteDualSquare fockFlow h hh))
  · intro h
    exact core.mul_mem A.property (F1Fecho.RegularCoreAverage.regularAverage_mem fockFlow M h)
  · intro v
    exact (F1Fecho.RegularCoreAverage.regularAverage_mul_tendsto fockFlow A.val v).mono_left
      (nhdsWithin_mono _ (by intro h hh; exact ne_of_gt hh))


end F1Fecho.CanonicalFockFiniteWeight
open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    if (`F1Fecho.CanonicalFockFiniteWeight).isPrefixOf n then
      let axs ← collectAxioms n
      IO.println ("LOCAL_DECL\t" ++ n.toString ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
      unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
        throwError "AXIOM_AUDIT_REFUSED: {n}"
      match ci with
      | .axiomInfo _ => throwError "LOCAL_AXIOM_REFUSED: {n}"
      | _ => pure ()
