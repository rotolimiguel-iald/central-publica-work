import TGLExt.F1Fecho394.MaxwellChartSmearingR4

/-! Linearity of the explicit on-shell tensor-to-H1 map on its stated compact
regular-chart test domain. Proof witnesses only certify support, not physics. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
namespace F1Fecho.MaxwellSmearing
open MeasureTheory Filter Matrix
open ChatgptAudit.WignerRapidityMeasure016 TGLExt.ImportedSQ F1Fecho.MaxwellOnShell
open scoped CompactlySupported

theorem coefficient_add (f g : TestTensor) : coefficient (f+g)=coefficient f+coefficient g := by
  funext y
  apply PiLp.ext
  intro j
  simp [coefficient,mul_add,Finset.sum_add_distrib]

theorem coefficient_smul (c : ℂ) (f : TestTensor) : coefficient (c • f)=c • coefficient f := by
  funext y
  apply PiLp.ext
  intro j
  change (1/2:ℂ)*(∑ μ,∑ ν,strength (momentum y) (realLift (screen y j)) μ ν*
    (c*f y μ ν))=c*((1/2:ℂ)*(∑ μ,∑ ν,strength (momentum y) (realLift (screen y j)) μ ν*f y μ ν))
  have he : (∑ μ,∑ ν,strength (momentum y) (realLift (screen y j)) μ ν*(c*f y μ ν))=
      c*(∑ μ,∑ ν,strength (momentum y) (realLift (screen y j)) μ ν*f y μ ν) := by
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro μ _
    rw [Finset.mul_sum]
    apply Finset.sum_congr rfl
    intro ν _
    ring
  rw [he]
  ring

theorem smear_add (f g : TestTensor) (hf : ∀ y∈tsupport f,y.1≠0)
    (hg : ∀ y∈tsupport g,y.1≠0) (hfg : ∀ y∈tsupport (f+g),y.1≠0) :
    smear (f+g) hfg=smear f hf+smear g hg := by
  apply (orbitalL2Pullback 0).injective
  simp only [map_add,smear,orbitalL2Pullback_inverse]
  apply Lp.ext
  filter_upwards [(coefficient_memLp (f+g) hfg).coeFn_toLp,
    (coefficient_memLp f hf).coeFn_toLp,(coefficient_memLp g hg).coeFn_toLp,
    Lp.coeFn_add ((coefficient_memLp f hf).toLp _) ((coefficient_memLp g hg).toLp _)] with y h1 h2 h3 h4
  rw [h1,h4]
  simp only [Pi.add_apply]
  rw [h2,h3]
  exact congrFun (coefficient_add f g) y

theorem smear_smul (c : ℂ) (f : TestTensor) (hf : ∀ y∈tsupport f,y.1≠0)
    (hcf : ∀ y∈tsupport (c • f),y.1≠0) : smear (c • f) hcf=c • smear f hf := by
  apply (orbitalL2Pullback 0).injective
  simp only [map_smul,smear,orbitalL2Pullback_inverse]
  apply Lp.ext
  filter_upwards [(coefficient_memLp (c • f) hcf).coeFn_toLp,
    (coefficient_memLp f hf).coeFn_toLp,
    Lp.coeFn_smul c ((coefficient_memLp f hf).toLp _)] with y h1 h2 h3
  rw [h1,h3]
  simp only [Pi.smul_apply]
  rw [h2]
  exact congrFun (coefficient_smul c f) y

end F1Fecho.MaxwellSmearing
#print axioms F1Fecho.MaxwellSmearing.coefficient_add
#print axioms F1Fecho.MaxwellSmearing.coefficient_smul
#print axioms F1Fecho.MaxwellSmearing.smear_add
#print axioms F1Fecho.MaxwellSmearing.smear_smul
