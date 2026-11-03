import Mathlib.MeasureTheory.Integral.IntervalIntegral.LebesgueDifferentiationThm
import Mathlib.MeasureTheory.Function.AEEqOfIntegral
import Mathlib.MeasureTheory.Function.L2Space
import Mathlib.MeasureTheory.Function.LocallyIntegrable
import Mathlib.Analysis.InnerProductSpace.Projection.Submodule
/-! Interval vectors are total in the actual vector-valued L2 space.
Lebesgue differentiation supplies the missing analytic density argument;
no totality or separability hypothesis is inserted for the value space. -/
set_option autoImplicit false
set_option maxErrors 3
set_option maxHeartbeats 600000
noncomputable section
namespace F1Fecho.LpIntervalTotality
open MeasureTheory Filter
open scoped Topology ENNReal

theorem real_ae_zero {f : ℝ → ℝ} (hf : LocallyIntegrable f volume)
    (hz : ∀ a b, (∫ t : ℝ in a..b, f t)=0) : f =ᵐ[volume] 0 := by
  have hp : (fun x => ∫ t : ℝ in (0 : ℝ)..x, f t) = fun _ => (0 : ℝ) := funext (hz 0)
  filter_upwards [_root_.LocallyIntegrable.ae_hasDerivAt_integral hf] with x hx
  have hd := hx 0
  rw [hp] at hd
  exact hd.unique (hasDerivAt_const x (0 : ℝ))

variable {E : Type} [NormedAddCommGroup E] [NormedSpace ℝ E] [CompleteSpace E]

theorem vector_eq_zero_of_intervals (f : Lp E 2 (volume : Measure ℝ))
    (hz : ∀ a b, (∫ t : ℝ in a..b, f t)=0) : f=0 := by
  have hl := (Lp.memLp f).locallyIntegrable (by norm_num : (1 : ℝ≥0∞) ≤ 2)
  have hi (a b : ℝ) : IntervalIntegrable f volume a b :=
    intervalIntegrable_iff.mpr ((hl.integrableOn_isCompact isCompact_uIcc).mono_set Set.uIoc_subset_uIcc)
  obtain ⟨s,hs,hfs⟩ := (Lp.memLp f).1.isSeparable_ae_range
  have ha : (f : ℝ → E) =ᵐ[volume] 0 := by
    apply ae_eq_zero_of_forall_dual_of_isSeparable ℝ hs ?_ hfs
    intro c
    apply real_ae_zero ((c.comp_memLp f).locallyIntegrable (by norm_num : (1 : ℝ≥0∞) ≤ 2))
    intro a b
    exact (c.intervalIntegral_comp_comm (hi a b)).trans (by rw [hz,map_zero])
  apply Lp.ext
  exact ha.trans (Lp.coeFn_zero E 2 volume).symm

variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

def intervalVector (a b : ℝ) (v : H) : Lp H 2 (volume : Measure ℝ) :=
  indicatorConstLp (s:=Set.Ioc a b) 2 measurableSet_Ioc (by simp [Real.volume_Ioc]) v

theorem intervalVector_inner (a b : ℝ) (v : H) (f : Lp H 2 (volume : Measure ℝ)) :
    inner ℂ (intervalVector a b v) f = inner ℂ v (∫ t in Set.Ioc a b, f t) :=
  L2.inner_indicatorConstLp_eq_inner_setIntegral (s:=Set.Ioc a b) ℂ measurableSet_Ioc
    (by simp [Real.volume_Ioc]) v f

theorem eq_zero_of_interval_orthogonal (f : Lp H 2 (volume : Measure ℝ))
    (hf : ∀ a b v, inner ℂ (intervalVector a b v) f=0) : f=0 := by
  have hi (a b : ℝ) : (∫ t in Set.Ioc a b, f t)=0 := by
    apply (inner_self_eq_zero (𝕜:=ℂ)).mp
    rw [← intervalVector_inner]
    exact hf a b _
  apply vector_eq_zero_of_intervals f
  intro a b
  simp only [intervalIntegral,hi,sub_self]

theorem closed_submodule_eq_top
    (S : Submodule ℂ (Lp H 2 (volume : Measure ℝ))) (hs : IsClosed (S : Set (Lp H 2 (volume : Measure ℝ))))
    (hi : ∀ a b v, intervalVector a b v ∈ S) : S=⊤ := by
  letI : CompleteSpace S := hs.completeSpace_coe
  apply Submodule.orthogonal_eq_bot_iff.mp
  apply le_antisymm ?_ bot_le
  intro f hf
  change f=0
  apply eq_zero_of_interval_orthogonal
  intro a b v
  exact Submodule.inner_right_of_mem_orthogonal (hi a b v) hf

end F1Fecho.LpIntervalTotality
#print axioms F1Fecho.LpIntervalTotality.real_ae_zero
#print axioms F1Fecho.LpIntervalTotality.vector_eq_zero_of_intervals
#print axioms F1Fecho.LpIntervalTotality.intervalVector_inner
#print axioms F1Fecho.LpIntervalTotality.eq_zero_of_interval_orthogonal

#print axioms F1Fecho.LpIntervalTotality.closed_submodule_eq_top
