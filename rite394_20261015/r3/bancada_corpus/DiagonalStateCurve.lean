import DiagonalRelativeEntropy

set_option autoImplicit false
set_option maxHeartbeats 5000000
namespace ChatgptAudit.Micro021
open Matrix Filter Topology Set
noncomputable section
variable {ι : Type} [Fintype ι]

structure DiagonalStateCurve (p : ι → ℝ) where
  weights : ℝ → ι → ℝ
  tangent : ℝ → ι → ℝ
  at_zero : ∀ i, weights 0 i=p i
  trace_one : ∀ t, ∑ i, weights t i=1
  derivative_zero : ∀ i, HasDerivAt (fun t => weights t i) (tangent 0 i) 0
  derivative_past : ∀ᶠ t in 𝓝[<] (0:ℝ), ∀ i,
    HasDerivAt (fun s => weights s i) (tangent t i) t
  tangent_continuous : ∀ i, ContinuousAt (fun t => tangent t i) 0

variable {p : ι → ℝ} (X : DiagonalStateCurve p)

def relativeEntropyRate (t : ℝ) : ℝ :=
  ∑ i, X.tangent t i*(Real.log (X.weights t i)-Real.log (p i))

include X in
theorem state_curve_base_normalized : ∑ i, p i=1 := by
  simpa only [X.at_zero] using X.trace_one 0

theorem state_curve_positive_near (hp : ∀ i, 0<p i) :
    ∀ᶠ t in 𝓝 (0:ℝ), ∀ i, 0<X.weights t i := by
  apply Filter.eventually_all.mpr
  intro i
  apply (X.derivative_zero i).continuousAt.eventually
  exact Ioi_mem_nhds (by change 0<X.weights 0 i; rw [X.at_zero]; exact hp i)

theorem state_curve_tangent_trace (t : ℝ)
    (hd : ∀ i, HasDerivAt (fun s => X.weights s i) (X.tangent t i) t) :
    ∑ i, X.tangent t i=0 := by
  have hs : HasDerivAt (fun s => ∑ i, X.weights s i) (∑ i, X.tangent t i) t := by
    have hh := HasDerivAt.sum (u := Finset.univ) (fun i _ => hd i)
    have hf : (∑ i, fun s => X.weights s i)=(fun s => ∑ i, X.weights s i) := by
      funext s
      simp only [Finset.sum_apply]
    rw [hf] at hh
    exact hh
  have he : (fun s => ∑ i, X.weights s i)=(fun _ : ℝ => 1) := funext X.trace_one
  rw [he] at hs
  exact hs.unique (hasDerivAt_const t (1:ℝ))

theorem relative_curve_derivative (t : ℝ) (hw : ∀ i, 0<X.weights t i)
    (hd : ∀ i, HasDerivAt (fun s => X.weights s i) (X.tangent t i) t) :
    HasDerivAt (fun s => diagonalRelativeEntropy (X.weights s) p) (relativeEntropyRate X t) t := by
  have hterm : ∀ i, HasDerivAt
      (fun s => X.weights s i*(Real.log (X.weights s i)-Real.log (p i)))
      (X.tangent t i*(Real.log (X.weights t i)-Real.log (p i))+X.tangent t i) t := by
    intro i
    have hn : X.weights t i≠0 := ne_of_gt (hw i)
    have hh := (hd i).mul (((hd i).log hn).sub_const (Real.log (p i)))
    convert hh using 1 <;> first | rfl | field_simp [hn]
  have hs := HasDerivAt.sum (u := Finset.univ) (fun i _ => hterm i)
  have hf : (∑ i, fun s => X.weights s i*(Real.log (X.weights s i)-Real.log (p i)))=
      (fun s => ∑ i, X.weights s i*(Real.log (X.weights s i)-Real.log (p i))) := by
    funext s
    simp only [Finset.sum_apply]
  rw [hf] at hs
  simpa only [Finset.sum_apply,Finset.sum_add_distrib,state_curve_tangent_trace X t hd,add_zero,
    diagonalRelativeEntropy,relativeEntropyRate] using hs

theorem relative_curve_derivative_zero (hp : ∀ i, 0<p i) :
    HasDerivAt (fun t => diagonalRelativeEntropy (X.weights t) p) 0 0 := by
  have hh := relative_curve_derivative X 0 (fun i => by rw [X.at_zero]; exact hp i) X.derivative_zero
  simpa only [relativeEntropyRate,X.at_zero,sub_self,mul_zero,Finset.sum_const_zero] using hh

theorem relative_curve_continuous_zero (hp : ∀ i, 0<p i) :
    ContinuousAt (fun t => diagonalRelativeEntropy (X.weights t) p) 0 :=
  (relative_curve_derivative_zero X hp).continuousAt

theorem relative_curve_derivative_past (hp : ∀ i, 0<p i) :
    ∀ᶠ t in 𝓝[<] (0:ℝ),
      HasDerivAt (fun s => diagonalRelativeEntropy (X.weights s) p) (relativeEntropyRate X t) t := by
  filter_upwards [(state_curve_positive_near X hp).filter_mono nhdsWithin_le_nhds,
    X.derivative_past] with t hw hd
  exact relative_curve_derivative X t hw hd

#print axioms state_curve_base_normalized
#print axioms state_curve_positive_near
#print axioms state_curve_tangent_trace
#print axioms relative_curve_derivative
#print axioms relative_curve_derivative_zero
#print axioms relative_curve_continuous_zero
#print axioms relative_curve_derivative_past
end
end ChatgptAudit.Micro021
