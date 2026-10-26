import TGLExt.F1Fecho394.SymmetricClosureR1
import TGLExt.F1Fecho394.BoundedScalarGrowthR2
import Mathlib.Analysis.Calculus.Deriv.Shift
/-! A symmetric generator on an invariant dense domain is essentially
self-adjoint when its actual norm-preserving group has the stated derivative.
The proof eliminates adjoint deficiency vectors by bounded scalar growth. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.DeficiencyCriterion
open Complex
variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable (A : H →ₗ.[ℂ] H) (U : ℝ → H →L[ℂ] H) (c : ℝ)
variable (hzero : ∀ x : H, U 0 x=x)
variable (hadd : ∀ s t : ℝ, ∀ x : H, U (s+t) x=U s (U t x))
variable (hnorm : ∀ t : ℝ, ∀ x : H, ‖U t x‖=‖x‖)
variable (hinv : ∀ t : ℝ, ∀ x : A.domain, U t (x:H) ∈ A.domain)
variable (hder : ∀ x : A.domain, HasDerivAt (fun t : ℝ => U t (x:H))
  ((I*(c:ℂ)) • A x) 0)

include hadd hder in
theorem invariant_orbit_derivative (x : A.domain) (t : ℝ) :
    HasDerivAt (fun s : ℝ => U s (x:H))
      ((I*(c:ℂ)) • A ⟨U t (x:H),hinv t x⟩) t := by
  have hh := hder ⟨U t (x:H),hinv t x⟩
  have hh' : HasDerivAt (fun s : ℝ => U s (U t (x:H)))
      ((I*(c:ℂ)) • A ⟨U t (x:H),hinv t x⟩) (t-t) := by simpa using hh
  have hs := hh'.comp_sub_const t t
  convert! hs using 1
  funext s
  rw [← hadd,sub_add_cancel]

include hzero hadd hnorm hinv hder in
theorem adjoint_imaginary_eigen_zero (hd : Dense (A.domain : Set H)) (hc : c≠0)
    (y : A.adjoint.domain) (a : ℝ) (ha : a≠0)
    (he : A.adjoint y=(I*(a:ℂ)) • (y:H)) : (y:H)=0 := by
  apply hd.eq_zero_of_inner_left ℂ
  intro x hx
  let v : A.domain := ⟨x,hx⟩
  let f : ℝ → ℂ := fun t => inner ℂ (y:H) (U t x)
  have hf (t : ℝ) : HasDerivAt f (((c*a:ℝ):ℂ)*f t) t := by
    have ht := invariant_orbit_derivative A U c hadd hinv hder v t
    have hp := (((innerSL ℂ (y:H)).restrictScalars ℝ).hasFDerivAt).comp_hasDerivAt t ht
    have hpair := LinearPMap.adjoint_isFormalAdjoint hd y ⟨U t x,hinv t v⟩
    rw [he,inner_smul_left] at hpair
    change HasDerivAt f (inner ℂ (y:H) ((I*(c:ℂ)) • A ⟨U t x,hinv t v⟩)) t at hp
    rw [inner_smul_right,← hpair] at hp
    convert! hp using 1
    simp only [map_mul,Complex.conj_I,Complex.conj_ofReal,Complex.ofReal_mul]
    simp only [f]
    ring_nf
    simp
  have hb (t : ℝ) : ‖f t‖ ≤ ‖(y:H)‖*‖x‖ := by
    calc
      ‖f t‖ ≤ ‖(y:H)‖*‖U t x‖ := norm_inner_le_norm _ _
      _=‖(y:H)‖*‖x‖ := by rw [hnorm]
  have hz := bounded_growth_zero f (c*a) (‖(y:H)‖*‖x‖) (mul_ne_zero hc ha) hf hb
  simpa only [f,hzero] using hz

include hzero hadd hnorm hinv hder in
theorem invariant_unitary_essentialSelfAdjoint (hd : Dense (A.domain : Set H))
    (hs : A.IsFormalAdjoint A) (hc : c≠0) : IsSelfAdjoint A.closure := by
  have hn (a : ℝ) (ha : a≠0) (x : H)
      (h : (x,(I*(a:ℂ)) • x) ∈ A.adjoint.graph) : x=0 := by
    obtain ⟨y,hy⟩ := A.adjoint.mem_graph_iff'.mp h
    have hy1 : (y:H)=x := congrArg Prod.fst hy
    have hy2 : A.adjoint y=(I*(a:ℂ)) • x := congrArg Prod.snd hy
    have hz := adjoint_imaginary_eigen_zero A U c hzero hadd hnorm hinv hder hd hc
      y a ha (by rw [hy1]; exact hy2)
    exact hy1.symm.trans hz
  apply essentialSelfAdjoint_of_no_deficiency A hd hs
  · simpa only [Complex.ofReal_one,mul_one] using hn 1 one_ne_zero
  · simpa only [Complex.ofReal_neg,Complex.ofReal_one,mul_neg,mul_one] using hn (-1) (by norm_num)

end F1Fecho.DeficiencyCriterion
#print axioms F1Fecho.DeficiencyCriterion.invariant_orbit_derivative
#print axioms F1Fecho.DeficiencyCriterion.adjoint_imaginary_eigen_zero
#print axioms F1Fecho.DeficiencyCriterion.invariant_unitary_essentialSelfAdjoint
