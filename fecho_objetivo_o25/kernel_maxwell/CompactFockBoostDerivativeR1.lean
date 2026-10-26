import CompactBoostMixedNullMomentR1
import RegularFockPointStressR4
import Mathlib.Analysis.Calculus.Deriv.Star
import Mathlib.Analysis.SpecialFunctions.ExpDeriv

/-! Actual boost matrix-element derivatives in the existing bosonic Fock space.
The finite sums use the unique coefficients of regularFockDomain. AxisCompact
is required only for the labels that occur in the differentiated vector.
The mixed H1 coefficient is the actual derivative and is identified with null
Schwartz integrals by the preceding module. No stress-charge equality is input.
The final energy is an actual HasBoostEnergy for VF, not a full certificate.
Translation invariance and density of the named compact core, and equality to
the normalized Fock stress moment, are separate subsequent obligations. -/
set_option autoImplicit false
set_option maxHeartbeats 2200000
noncomputable section

namespace F1Fecho.CoherentKernel
variable {ι : Type*}

/-- Only coefficients in the two finite supports need differentiation. -/
theorem finiteKernel_hasDerivAt_on_support (M : ι → ι → ℝ → ℂ) (D : ι → ι → ℂ)
    (c d : ι →₀ ℂ) (x : ℝ)
    (hM : ∀ i ∈ c.support, ∀ j ∈ d.support, HasDerivAt (M i j) (D i j) x) :
    HasDerivAt (fun t => finiteKernel (fun i j => M i j t) c d)
      (finiteKernel D c d) x := by
  have ht := HasDerivAt.sum (u := c.support) (fun i hi =>
    HasDerivAt.sum (u := d.support) (fun j hj =>
      (hM i hi j hj).const_mul ((starRingEnd ℂ) (c i) * d j)))
  convert! ht using 1 <;> first | rfl |
    (ext t; simp only [finiteKernel, Finsupp.sum, Finset.sum_apply])

end F1Fecho.CoherentKernel

namespace F1Fecho.MaxwellGlobal
open Set Filter MeasureTheory SchwartzMap
open TGLExt.ImportedSQ TGLExt.ContratoQGv31
open F1Rede.BosonicFock F1Rede.BosonicFockGroupActions
open F1Fecho.Exponential F1Fecho.CoherentKernel F1Fecho.NullFrequency
open scoped Topology ContDiff LineDeriv

def coherentBoostPair (h k : H1) : ℂ :=
  Complex.exp (inner ℂ h k) * oneParticleBoostPair h k

theorem axisCompact_coherent_boost_hasDerivAt (h k : H1) (hk : AxisCompactProfile k) :
    HasDerivAt (fun s : ℝ => inner ℂ (exponential h) (VF s (exponential k)))
      (coherentBoostPair h k) 0 := by
  simpa only [VF, gamma_exponential, exponential_inner, coherentBoostPair,
    B0_zero, LinearIsometryEquiv.coe_refl, id_eq] using
    (axisCompact_mixed_hasDerivAt h k hk).cexp

theorem axisCompact_coherentBoostPair_null_integrals (h k : H1)
    (hh : AxisCompactProfile h) (hk : AxisCompactProfile k) :
    coherentBoostPair h k = Complex.exp (inner ℂ h k) *
      ((∫ p, inner ℂ ((axisCompactNullData h hh 0).profile p)
        ((∂_{nullFrequencyDirection} (axisCompactNullData k hk 0).profile) p)) +
       (∫ p, inner ℂ ((axisCompactNullData h hh 1).profile p)
        ((∂_{nullFrequencyDirection} (axisCompactNullData k hk 1).profile) p))) := by
  rw [coherentBoostPair, axisCompact_oneParticleBoostPair_null_integrals h k hh hk]

/-- A condition on the actual, unique finite coefficient support. -/
def AxisCompactCoefficients (c : RegularLabel →₀ ℂ) : Prop :=
  ∀ h ∈ c.support, AxisCompactProfile h.val

def AxisCompactFock (ψ : regularFockDomain) : Prop :=
  AxisCompactCoefficients (regularCoefficients ψ)

def regularFockBoostPair (ψ χ : regularFockDomain) : ℂ :=
  finiteKernel (fun h k : RegularLabel => coherentBoostPair h.val k.val)
    (regularCoefficients ψ) (regularCoefficients χ)

theorem regularSynthesis_inner_boost (c d : RegularLabel →₀ ℂ) (s : ℝ) :
    inner ℂ (regularSynthesis c) (VF s (regularSynthesis d)) =
      finiteKernel (fun h k : RegularLabel =>
        inner ℂ (exponential h.val) (VF s (exponential k.val))) c d := by
  simp only [regularSynthesis, Finsupp.linearCombination_apply, Finsupp.sum,
    map_sum, map_smul]
  rw [sum_inner]
  simp only [inner_sum, inner_smul_left, inner_smul_right,
    finiteKernel, Finsupp.sum, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro h _
  apply Finset.sum_congr rfl
  intro k _
  ring

theorem regularFock_inner_boost (ψ χ : regularFockDomain) (s : ℝ) :
    inner ℂ ψ.val (VF s χ.val) =
      finiteKernel (fun h k : RegularLabel =>
        inner ℂ (exponential h.val) (VF s (exponential k.val)))
        (regularCoefficients ψ) (regularCoefficients χ) := by
  rw [← regularCoefficients_spec ψ, ← regularCoefficients_spec χ]
  exact regularSynthesis_inner_boost _ _ s

theorem axisCompact_regularFock_boost_hasDerivAt (ψ χ : regularFockDomain)
    (hχ : AxisCompactFock χ) :
    HasDerivAt (fun s : ℝ => inner ℂ ψ.val (VF s χ.val)) (regularFockBoostPair ψ χ) 0 := by
  have ht := finiteKernel_hasDerivAt_on_support
    (fun h k : RegularLabel => fun s : ℝ =>
      inner ℂ (exponential h.val) (VF s (exponential k.val)))
    (fun h k : RegularLabel => coherentBoostPair h.val k.val)
    (regularCoefficients ψ) (regularCoefficients χ) 0
    (fun h _ k hk => axisCompact_coherent_boost_hasDerivAt h.val k.val (hχ k hk))
  simpa only [← regularFock_inner_boost, regularFockBoostPair] using ht

theorem VF_neg_eq_symm (s : ℝ) : VF (-s) = (VF s).symm := by
  have he : B0 (-s) = (B0 s).symm := by
    ext h
    exact (ChatgptAudit.WignerRapidityMeasure016.orbitalBoostUnitary_symm_apply 0 s h).symm
  rw [VF, he, gamma_symm]
  rfl

theorem fock_boost_expectation_neg (ψ : F) (s : ℝ) :
    inner ℂ ψ (VF (-s) ψ) = (starRingEnd ℂ) (inner ℂ ψ (VF s ψ)) := by
  rw [VF_neg_eq_symm, ← (VF s).inner_map_eq_flip ψ ψ]
  exact (inner_conj_symm (𝕜 := ℂ) (VF s ψ) ψ).symm

theorem axisCompact_regularFockBoostPair_re_zero (ψ : regularFockDomain)
    (hψ : AxisCompactFock ψ) : (regularFockBoostPair ψ ψ).re = 0 := by
  have hd := axisCompact_regularFock_boost_hasDerivAt ψ ψ hψ
  have hneg : HasDerivAt (fun s : ℝ => inner ℂ ψ.val (VF (-s) ψ.val))
      (-regularFockBoostPair ψ ψ) 0 := by
    have hc := (show HasDerivAt (fun s : ℝ => inner ℂ ψ.val (VF s ψ.val))
      (regularFockBoostPair ψ ψ) (-(0 : ℝ)) from by simpa using hd).scomp 0
      (hasDerivAt_id (0 : ℝ)).neg
    simpa only [Function.comp_def, neg_one_smul] using hc
  have hconj : HasDerivAt (fun s : ℝ => (starRingEnd ℂ)
      (inner ℂ ψ.val (VF s ψ.val))) ((starRingEnd ℂ) (regularFockBoostPair ψ ψ)) 0 :=
    hd.star
  have he : (fun s : ℝ => inner ℂ ψ.val (VF (-s) ψ.val)) =
      fun s : ℝ => (starRingEnd ℂ) (inner ℂ ψ.val (VF s ψ.val)) :=
    funext (fock_boost_expectation_neg ψ.val)
  rw [he] at hneg
  have hr := congrArg Complex.re (hneg.unique hconj)
  change -(regularFockBoostPair ψ ψ).re = (regularFockBoostPair ψ ψ).re at hr
  linarith

/-- The energy is derived from VF's actual matrix element on a finite smooth core.
Identifying it with the normalized Fock stress moment is a further theorem. -/
theorem axisCompact_regularFock_hasBoostEnergy (ψ : regularFockDomain)
    (hψ : AxisCompactFock ψ) :
    HasBoostEnergy VF ψ.val (regularFockBoostPair ψ ψ).im := by
  have hz := axisCompact_regularFockBoostPair_re_zero ψ hψ
  have he : regularFockBoostPair ψ ψ = Complex.I * ((regularFockBoostPair ψ ψ).im : ℂ) := by
    apply Complex.ext <;> simp [hz]
  unfold HasBoostEnergy
  rw [← he]
  exact axisCompact_regularFock_boost_hasDerivAt ψ ψ hψ

theorem axisCompactFock_exponential (h : RegularLabel) (hh : AxisCompactProfile h.val) :
    AxisCompactFock (regularExponential h) := by
  intro k hk
  rw [regularCoefficients_exponential] at hk
  have he : k = h := by simpa using hk
  simpa only [he] using hh

theorem regularFockBoostPair_exponential (h k : RegularLabel) :
    regularFockBoostPair (regularExponential h) (regularExponential k) =
      coherentBoostPair h.val k.val := by
  simp only [regularFockBoostPair, regularCoefficients_exponential, finiteKernel_single,
    map_one, one_mul]

end F1Fecho.MaxwellGlobal

#print axioms F1Fecho.CoherentKernel.finiteKernel_hasDerivAt_on_support
#print axioms F1Fecho.MaxwellGlobal.axisCompact_coherent_boost_hasDerivAt
#print axioms F1Fecho.MaxwellGlobal.axisCompact_coherentBoostPair_null_integrals
#print axioms F1Fecho.MaxwellGlobal.regularSynthesis_inner_boost
#print axioms F1Fecho.MaxwellGlobal.regularFock_inner_boost
#print axioms F1Fecho.MaxwellGlobal.axisCompact_regularFock_boost_hasDerivAt
#print axioms F1Fecho.MaxwellGlobal.VF_neg_eq_symm
#print axioms F1Fecho.MaxwellGlobal.fock_boost_expectation_neg
#print axioms F1Fecho.MaxwellGlobal.axisCompact_regularFockBoostPair_re_zero
#print axioms F1Fecho.MaxwellGlobal.axisCompact_regularFock_hasBoostEnergy
#print axioms F1Fecho.MaxwellGlobal.axisCompactFock_exponential
#print axioms F1Fecho.MaxwellGlobal.regularFockBoostPair_exponential
