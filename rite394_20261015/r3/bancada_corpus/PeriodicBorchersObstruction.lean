import StationaryModularPeriod
import Mathlib.Analysis.SpecificLimits.Basic

set_option autoImplicit false
namespace ChatgptAudit
open TGLExt Filter Topology
noncomputable section
variable {P : SiteProfile}

theorem contraction_invariant_continuous_constant {X : Type*} [TopologicalSpace X] [T2Space X]
    (f : ℝ → X) (hf : ContinuousAt f 0) {c : ℝ} (hc0 : 0≤c) (hc1 : c<1)
    (hinv : ∀ a, f (c*a)=f a) (a : ℝ) : f a=f 0 := by
  have hi (n : ℕ) : f (c^n*a)=f a := by
    induction n with
    | zero => simp
    | succ n ih => rw [pow_succ',mul_assoc,hinv,ih]
  have ht : Tendsto (fun n : ℕ => c^n*a) atTop (𝓝 0) := by
    simpa only [zero_mul] using (tendsto_pow_atTop_nhds_zero_of_lt_one hc0 hc1).mul_const a
  have hl := hf.tendsto.comp ht
  simp only [Function.comp_def,hi] at hl
  exact tendsto_nhds_unique tendsto_const_nhds hl

theorem periodic_borchers_trivial (T : ℝ) (hT : 0<T)
    (hperiod : modularFlow P T=id)
    (V : ℝ → (TowerHilbert P →L[ℂ] TowerHilbert P))
    (hcont : ∀ v, ContinuousAt (fun a => V a v) 0) (hzero : V 0=1)
    (hborchers : ∀ t a, modularConjugation P t (V a)=V (Real.exp (-2*Real.pi*t)*a)) :
    ∀ a, V a=1 := by
  have hU (v : TowerHilbert P) : modularFlow P T v=v := congrFun hperiod v
  have hm (v : TowerHilbert P) : modularFlow P (-T) v=v := by
    have h := modularFlow_inverse (P := P) T v
    rwa [hU] at h
  have hconj (x : TowerHilbert P →L[ℂ] TowerHilbert P) : modularConjugation P T x=x := by
    ext v
    change modularFlow P T (x (modularFlow P (-T) v))=x v
    rw [hU,hm]
  have hi (a : ℝ) : V (Real.exp (-2*Real.pi*T)*a)=V a := by
    rw [← hborchers T a,hconj]
  have hc : Real.exp (-2*Real.pi*T)<1 := Real.exp_lt_one_iff.mpr (by nlinarith [Real.pi_pos])
  intro a
  ext v
  have h := contraction_invariant_continuous_constant (fun a => V a v) (hcont v)
    (le_of_lt (Real.exp_pos _)) hc (fun b => congrArg (fun A => A v) (hi b)) a
  simpa only [hzero,one_apply_eq_self] using h

#print axioms contraction_invariant_continuous_constant
#print axioms periodic_borchers_trivial
end
end ChatgptAudit
