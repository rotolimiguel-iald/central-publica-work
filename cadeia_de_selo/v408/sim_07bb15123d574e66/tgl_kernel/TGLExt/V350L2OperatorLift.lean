import Mathlib

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

namespace TGLV350.Regular
open MeasureTheory Filter
noncomputable section
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

abbrev RegularHilbert (H : Type) [NormedAddCommGroup H] :=
  Lp H 2 (volume : Measure ℝ)

/-- Constant-fibre representation on the actual Lebesgue L² space. -/
def fibre (T : H →L[ℂ] H) : RegularHilbert H →L[ℂ] RegularHilbert H :=
  T.compLpL 2 volume

theorem fibre_ae (T : H →L[ℂ] H) (f : RegularHilbert H) :
    fibre T f =ᵐ[volume] fun x : ℝ => T (f x) := T.coeFn_compLpL f

theorem fibre_one : fibre (1 : H →L[ℂ] H) = 1 := by
  ext1 f
  apply Lp.ext
  filter_upwards [fibre_ae (1 : H →L[ℂ] H) f] with x hx
  exact hx

theorem fibre_mul (T S : H →L[ℂ] H) : fibre (T*S) = fibre T * fibre S := by
  ext1 f
  apply Lp.ext
  filter_upwards [fibre_ae (T*S) f, fibre_ae T (fibre S f), fibre_ae S f] with x h1 h2 h3
  change (fibre (T*S) f) x = (fibre T (fibre S f)) x
  rw [h1, h2, h3]
  rfl

theorem fibre_add (T S : H →L[ℂ] H) : fibre (T+S) = fibre T + fibre S :=
  ContinuousLinearMap.add_compLpL T S

theorem fibre_smul (c : ℂ) (T : H →L[ℂ] H) : fibre (c • T) = c • fibre T :=
  ContinuousLinearMap.smul_compLpL c T

theorem fibre_star (T : H →L[ℂ] H) : fibre (star T) = star (fibre T) := by
  ext1 f
  apply ext_inner_left ℂ
  intro g
  simp only [ContinuousLinearMap.star_eq_adjoint]
  rw [ContinuousLinearMap.adjoint_inner_right]
  rw [L2.inner_def, L2.inner_def]
  apply integral_congr_ae
  filter_upwards [fibre_ae (T.adjoint) f, fibre_ae T g] with x hf hg
  rw [hf, hg, ContinuousLinearMap.adjoint_inner_right]

def fibreRepresentation : (H →L[ℂ] H) →⋆ₐ[ℂ] (RegularHilbert H →L[ℂ] RegularHilbert H) where
  toFun := fibre
  map_one' := fibre_one
  map_mul' := fibre_mul
  map_zero' := by
    apply ContinuousLinearMap.ext
    intro f
    apply Lp.ext
    filter_upwards [fibre_ae (0 : H →L[ℂ] H) f, Lp.coeFn_zero H 2 volume] with x hx hz
    simpa only [zero_apply, Pi.zero_apply, hz] using hx
  map_add' := fibre_add
  commutes' c := by
    change fibre (c • (1 : H →L[ℂ] H)) = c • (1 : RegularHilbert H →L[ℂ] RegularHilbert H)
    rw [fibre_smul, fibre_one]
  map_star' := fibre_star

/-- A finite-measure test vector, not a nonintegrable constant function on ℝ. -/
def testVector (v : H) : RegularHilbert H :=
  indicatorConstLp 2 (measurableSet_Ioc (a := (0 : ℝ)) (b := 1)) (by simp) v

theorem testVector_norm (v : H) : ‖testVector v‖ = ‖v‖ := by
  change ‖indicatorConstLp 2 (measurableSet_Ioc (a := (0 : ℝ)) (b := 1)) _ v‖ = ‖v‖
  rw [norm_indicatorConstLp (by norm_num) (by norm_num)]
  simp [measureReal_def]

theorem testVector_sub (v w : H) : testVector (v-w) = testVector v - testVector w :=
  indicatorConstLp_sub.symm

theorem testVector_injective : Function.Injective (testVector : H → RegularHilbert H) := by
  intro v w h
  have hz : ‖v-w‖ = 0 := by
    rw [← testVector_norm, testVector_sub, h, sub_self, norm_zero]
  exact sub_eq_zero.mp (norm_eq_zero.mp hz)

theorem fibre_testVector (T : H →L[ℂ] H) (v : H) :
    fibre T (testVector v) = testVector (T v) := by
  apply Lp.ext
  filter_upwards [fibre_ae T (testVector v),
    indicatorConstLp_coeFn (p := (2 : ENNReal)) (hs := measurableSet_Ioc (a := (0 : ℝ)) (b := 1))
      (hμs := by simp) (c := v),
    indicatorConstLp_coeFn (p := (2 : ENNReal)) (hs := measurableSet_Ioc (a := (0 : ℝ)) (b := 1))
      (hμs := by simp) (c := T v)] with x h1 h2 h3
  rw [h1, show testVector v x = _ from h2, show testVector (T v) x = _ from h3]
  by_cases hx : x ∈ Set.Ioc (0 : ℝ) 1
  · simp only [Set.indicator_of_mem hx]
  · simp only [Set.indicator_of_notMem hx, map_zero]

theorem fibre_injective : Function.Injective (fibre : (H →L[ℂ] H) → _) := by
  intro T S h
  ext v
  apply testVector_injective
  rw [← fibre_testVector, ← fibre_testVector, h]

#print axioms fibreRepresentation
#print axioms fibre_injective
end
end TGLV350.Regular
