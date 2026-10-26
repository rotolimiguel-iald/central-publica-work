import CircularPhysicalFieldTransportR1
import PhysicalSmearWavePairingR2
import RegularFockPointStressR4

/-! Candidate R51. Diagonal annihilators on the EXISTING regular coherent
domain, using its proved unique coefficients. No bounded point evaluation on
H1 or Fock is asserted. The specialization to inner f h is proved equal to
the preexisting annihilation operator, and the four-term normally ordered
form is therefore the preexisting Segal Wick form after smearing. -/
set_option Elab.async false
set_option autoImplicit false
set_option maxHeartbeats 400000
set_option synthInstance.maxHeartbeats 500000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Fecho.Exponential
open F1Fecho.Annihilation F1Fecho.CoherentKernel
open MeasureTheory

def regularCoefficientsLM : regularFockDomain →ₗ[ℂ] (RegularLabel →₀ ℂ) where
  toFun := regularCoefficients
  map_add' := regularCoefficients_add
  map_smul' := regularCoefficients_smul

def regularDiagonal (v : RegularLabel → ℂ) : regularFockDomain →ₗ[ℂ] regularFockDomain :=
  (Finsupp.linearCombination ℂ (fun h => v h • regularExponential h)).comp
    regularCoefficientsLM

theorem regularDiagonal_exponential (v : RegularLabel → ℂ) (h : RegularLabel) :
    regularDiagonal v (regularExponential h) = v h • regularExponential h := by
  simp [regularDiagonal, regularCoefficientsLM, regularCoefficients_exponential]

theorem regular_decomposition (ψ : regularFockDomain) :
    (regularCoefficients ψ).sum (fun h z => z • regularExponential h) = ψ := by
  apply Subtype.ext
  simpa only [regularSynthesis, Finsupp.linearCombination_apply, Finsupp.sum,
    Submodule.coe_sum, Submodule.coe_smul, regularExponential] using regularCoefficients_spec ψ

theorem regularLinearMap_expansion {E : Type*} [AddCommMonoid E] [Module ℂ E]
    (L : regularFockDomain →ₗ[ℂ] E) (ψ : regularFockDomain) :
    L ψ = (regularCoefficients ψ).sum (fun h z => z • L (regularExponential h)) := by
  calc
    _ = L ((regularCoefficients ψ).sum (fun h z => z • regularExponential h)) :=
      congrArg L (regular_decomposition ψ).symm
    _ = _ := by simp only [Finsupp.sum, map_sum, map_smul]

theorem regularLinearMap_ext {E : Type*} [AddCommMonoid E] [Module ℂ E]
    (L M : regularFockDomain →ₗ[ℂ] E)
    (h : ∀ k, L (regularExponential k) = M (regularExponential k)) : L = M := by
  ext ψ
  rw [regularLinearMap_expansion L ψ, regularLinearMap_expansion M ψ]
  simp only [h]

theorem regularInner_expansion (L M : regularFockDomain →ₗ[ℂ] F)
    (ψ χ : regularFockDomain) :
    inner ℂ (L ψ) (M χ) =
      finiteKernel (fun h k => inner ℂ (L (regularExponential h)) (M (regularExponential k)))
        (regularCoefficients ψ) (regularCoefficients χ) := by
  rw [regularLinearMap_expansion L ψ, regularLinearMap_expansion M χ]
  simp only [Finsupp.sum, sum_inner, inner_sum, inner_smul_left, inner_smul_right,
    finiteKernel, Finset.mul_sum]
  rw [Finset.sum_comm]
  apply Finset.sum_congr rfl
  intro h _
  apply Finset.sum_congr rfl
  intro k _
  ring

theorem regularDiagonal_annihilation (f : H1) (ψ : regularFockDomain) :
    (regularDiagonal (fun h => inner ℂ f h.val) ψ).val =
      annihilation f (regularDomainInput ψ) := by
  have he : regularFockDomain.subtype.comp (regularDiagonal (fun h => inner ℂ f h.val)) =
      (onDomain f).comp regularDomainInput := by
    apply regularLinearMap_ext
    intro h
    simp only [LinearMap.comp_apply, regularDiagonal_exponential, Submodule.coe_smul]
    exact (annihilation_exponential f h.val).symm
  exact congrArg (fun L : regularFockDomain →ₗ[ℂ] F => L ψ) he

theorem regularDiagonal_invariant (f : H1) (ψ : regularFockDomain) :
    regularDomainInput (regularDiagonal (fun h => inner ℂ f h.val) ψ) =
      onInvariantDomain f (regularDomainInput ψ) := by
  apply Subtype.ext
  exact regularDiagonal_annihilation f ψ

/-- The four normally ordered terms, formed from actual endomorphisms of the
regular domain. Creation at a point is used only through this adjoint form. -/
def regularWick (v w : RegularLabel → ℂ) (ψ χ : regularFockDomain) : ℂ :=
  (1/2 : ℂ) *
    (inner ℂ ψ.val (regularDiagonal v (regularDiagonal w χ)).val +
     inner ℂ (regularDiagonal w ψ).val (regularDiagonal v χ).val +
     inner ℂ (regularDiagonal v ψ).val (regularDiagonal w χ).val +
     inner ℂ (regularDiagonal w (regularDiagonal v ψ)).val χ.val)

theorem regularWick_eq_existing (f g : H1) (ψ χ : regularFockDomain) :
    regularWick (fun h => inner ℂ f h.val) (fun h => inner ℂ g h.val) ψ χ =
      F1Fecho.WickForm.quadratic f g (regularDomainInput ψ) (regularDomainInput χ) := by
  unfold regularWick F1Fecho.WickForm.quadratic F1Fecho.WickForm.doubleAnnihilate
  simp only [regularDiagonal_annihilation, regularDiagonal_invariant]
  rfl

theorem regularWick_exponential (v w : RegularLabel → ℂ) (h k : RegularLabel) :
    regularWick v w (regularExponential h) (regularExponential k) =
      (1/2 : ℂ) * (v k + (starRingEnd ℂ) (v h)) *
        (w k + (starRingEnd ℂ) (w h)) * Complex.exp (inner ℂ h.val k.val) := by
  unfold regularWick
  simp only [regularDiagonal_exponential, map_smul, Submodule.coe_smul]
  simp only [regularExponential, inner_smul_left, inner_smul_right, exponential_inner, map_mul]
  ring

theorem finiteKernel_add_kernel (M N : RegularLabel → RegularLabel → ℂ)
    (c d : RegularLabel →₀ ℂ) :
    finiteKernel (fun h k => M h k + N h k) c d =
      finiteKernel M c d + finiteKernel N c d := by
  simp only [finiteKernel, Finsupp.sum, mul_add, Finset.sum_add_distrib]

theorem finiteKernel_mul_kernel (z : ℂ) (M : RegularLabel → RegularLabel → ℂ)
    (c d : RegularLabel →₀ ℂ) :
    finiteKernel (fun h k => z * M h k) c d = z * finiteKernel M c d := by
  simp only [finiteKernel, Finsupp.sum, Finset.mul_sum]
  apply Finset.sum_congr rfl
  intro h _
  apply Finset.sum_congr rfl
  intro k _
  ring

theorem regularWick_finiteKernel (v w : RegularLabel → ℂ) (ψ χ : regularFockDomain) :
    regularWick v w ψ χ =
      finiteKernel (fun h k => regularWick v w (regularExponential h) (regularExponential k))
        (regularCoefficients ψ) (regularCoefficients χ) := by
  let J := regularFockDomain.subtype
  let V := regularDiagonal v
  let W := regularDiagonal w
  change (1/2 : ℂ) * (inner ℂ (J ψ) ((J.comp (V.comp W)) χ) +
    inner ℂ ((J.comp W) ψ) ((J.comp V) χ) +
    inner ℂ ((J.comp V) ψ) ((J.comp W) χ) +
    inner ℂ ((J.comp (W.comp V)) ψ) (J χ)) = _
  rw [regularInner_expansion, regularInner_expansion, regularInner_expansion,
    regularInner_expansion]
  simp only [← finiteKernel_add_kernel, ← finiteKernel_mul_kernel]
  rfl

/-- Smearing of the point annihilation eigenvalue; upper test indices contract
the lower field with the two fixed Minkowski signs and the original 1/2. -/
def pointSmearEigenvalue (f : SchwartzTensor) (h : RegularLabel) : ℂ :=
  (1/2 : ℂ) * ∑ μ : Fin 4, ∑ ν : Fin 4,
    ∫ x, (starRingEnd ℂ) (f x μ ν) *
      (metricSignC μ * metricSignC ν * lowerProfileWave h.val μ ν x)

theorem raise_lowerProfileWave (h : H1) (μ ν : Fin 4) (x : Spacetime) :
    metricSignC μ * metricSignC ν * lowerProfileWave h μ ν x = profileWave h μ ν x := by
  unfold lowerProfileWave
  have hμ := metricSignC_square μ
  have hν := metricSignC_square ν
  calc
    _ = (metricSignC μ * metricSignC μ) * (metricSignC ν * metricSignC ν) *
        profileWave h μ ν x := by ring
    _ = _ := by rw [hμ, hν, one_mul, one_mul]

theorem pointSmearEigenvalue_eq_inner (f : SchwartzTensor) (h : RegularLabel) :
    pointSmearEigenvalue f h = inner ℂ (physicalSmearCLM f) h.val := by
  simp only [pointSmearEigenvalue, raise_lowerProfileWave]
  exact (physicalSmear_inner_wave f h.val h.property.1).symm

theorem pointSmear_annihilation (f : SchwartzTensor) (ψ : regularFockDomain) :
    (regularDiagonal (pointSmearEigenvalue f) ψ).val =
      annihilation (physicalSmearCLM f) (regularDomainInput ψ) := by
  have he : pointSmearEigenvalue f = (fun h : RegularLabel => inner ℂ (physicalSmearCLM f) h.val) :=
    funext (pointSmearEigenvalue_eq_inner f)
  exact (congrArg (fun v : RegularLabel → ℂ => (regularDiagonal v ψ).val) he).trans
    (regularDiagonal_annihilation (physicalSmearCLM f) ψ)

def normalizedPointSmearEigenvalue (f : SchwartzTensor) (h : RegularLabel) : ℂ :=
  (unitaryFourierFieldAmplitude : ℂ) * pointSmearEigenvalue f h

theorem normalizedPointSmearEigenvalue_eq_inner (f : SchwartzTensor) (h : RegularLabel) :
    normalizedPointSmearEigenvalue f h = inner ℂ (normalizedPhysicalSmearCLM f) h.val := by
  change (unitaryFourierFieldAmplitude : ℂ) * pointSmearEigenvalue f h =
    inner ℂ ((unitaryFourierFieldAmplitude : ℂ) • physicalSmearCLM f) h.val
  rw [inner_smul_left, Complex.conj_ofReal, pointSmearEigenvalue_eq_inner]

theorem normalizedPointSmear_Wick (f g : SchwartzTensor) (ψ χ : regularFockDomain) :
    regularWick (normalizedPointSmearEigenvalue f) (normalizedPointSmearEigenvalue g) ψ χ =
      F1Fecho.WickForm.quadratic (normalizedPhysicalSmearCLM f) (normalizedPhysicalSmearCLM g)
        (regularDomainInput ψ) (regularDomainInput χ) := by
  have hf : normalizedPointSmearEigenvalue f =
      (fun h : RegularLabel => inner ℂ (normalizedPhysicalSmearCLM f) h.val) :=
    funext (normalizedPointSmearEigenvalue_eq_inner f)
  have hg : normalizedPointSmearEigenvalue g =
      (fun h : RegularLabel => inner ℂ (normalizedPhysicalSmearCLM g) h.val) :=
    funext (normalizedPointSmearEigenvalue_eq_inner g)
  calc
    _ = regularWick (fun h => inner ℂ (normalizedPhysicalSmearCLM f) h.val)
        (fun h => inner ℂ (normalizedPhysicalSmearCLM g) h.val) ψ χ :=
      congrArg₂ (fun v w : RegularLabel → ℂ => regularWick v w ψ χ) hf hg
    _ = _ := regularWick_eq_existing _ _ _ _

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.regularDiagonal_exponential
#print axioms F1Fecho.MaxwellGlobal.regular_decomposition
#print axioms F1Fecho.MaxwellGlobal.regularLinearMap_expansion
#print axioms F1Fecho.MaxwellGlobal.regularLinearMap_ext
#print axioms F1Fecho.MaxwellGlobal.regularInner_expansion
#print axioms F1Fecho.MaxwellGlobal.regularDiagonal_annihilation
#print axioms F1Fecho.MaxwellGlobal.regularDiagonal_invariant
#print axioms F1Fecho.MaxwellGlobal.regularWick_eq_existing
#print axioms F1Fecho.MaxwellGlobal.regularWick_exponential
#print axioms F1Fecho.MaxwellGlobal.regularWick_finiteKernel
#print axioms F1Fecho.MaxwellGlobal.raise_lowerProfileWave
#print axioms F1Fecho.MaxwellGlobal.pointSmearEigenvalue_eq_inner
#print axioms F1Fecho.MaxwellGlobal.pointSmear_annihilation
#print axioms F1Fecho.MaxwellGlobal.normalizedPointSmearEigenvalue_eq_inner
#print axioms F1Fecho.MaxwellGlobal.normalizedPointSmear_Wick
