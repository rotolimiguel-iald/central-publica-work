import RegularFockRealCoordinateStressR2
import RegularFockStressBoostR3
import CanonicalModularCoreAssemblyR1

/-! The actual real stress form inhabits the existing MaxwellQuadraticForm
contract, on the regular coherent Fock domain, for the canonical Fock
assembly. Its point tensor, covariance and weak conservation are constructed.
The input A contains the remaining trace/PF data of R7; no inhabitant of A
is claimed here. The charge link and nonzero modular-energy witness required
by MaxwellCertificate are NOT assumed or discharged by this construction.
This is a sandbox candidate; the full R8 requirement remains open. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
namespace F1Fecho.MaxwellGlobal
open MeasureTheory TGLExt TGLExt.ImportedSQ TGLExt.ContratoQGv31 TGLExt.ContratoQGv32
open F1Fecho.SpacetimeLorentz F1Fecho.CovariantTensor F1Rede.BosonicFock
open F1Fecho.NetworkReuse F1Fecho.NetworkModularCore

 theorem boost_action_symm_coordinates (s : ℝ) (x : Fin 4→ℝ) :
    (action (theBoost s)).symm (WithLp.toLp 2 x)=
      WithLp.toLp 2 (wedgeBoostMap (-s) x) := by
  apply (action (theBoost s)).injective
  rw [ContinuousLinearEquiv.apply_symm_apply]
  change WithLp.toLp 2 x=WithLp.toLp 2 (wedgeBoostMap s (wedgeBoostMap (-s) x))
  rw [←wedgeBoostMap_add,add_neg_cancel,wedgeBoostMap_zero]

 theorem pull_realPart (A : Matrix (Fin 4) (Fin 4) ℝ) (T : TensorValue) :
    (fun μ ν=>(pull (A.map Complex.ofReal) T μ ν).re)=
      A.transpose*(Matrix.of (fun μ ν=>(T μ ν).re))*A := by
  ext μ ν
  change (((A.map Complex.ofReal).transpose*(Matrix.of T)*A.map Complex.ofReal) μ ν).re=_
  simp [Matrix.mul_apply,Matrix.transpose_apply,Matrix.map_apply,Complex.re_sum,
    Complex.mul_re]

 theorem realCoordinateStress_boost (s : ℝ) (ψ : regularFockDomain) (x : Fin 4→ℝ) :
    realCoordinateStress (regularGamma (B0 s) (strongRegularProfile_B0 s) ψ) x=
      (boostMat (-s)).transpose*realCoordinateStress ψ (wedgeBoostMap (-s) x)*boostMat (-s) := by
  have h := congrArg (fun T : TensorValue=>fun μ ν=>(T μ ν).re)
    (pointStressForm_boost s ψ ψ (WithLp.toLp 2 x))
  rw [boost_action_symm_coordinates] at h
  exact h.trans (pull_realPart (boostMat (-s)) _)

 open Classical in
 def regularStressTotal (ψ : F) (x : Fin 4→ℝ) : Matrix (Fin 4) (Fin 4) ℝ :=
  if h : ψ∈regularFockDomain then realCoordinateStress ⟨ψ,h⟩ x else 0

 theorem regularStressTotal_on_domain (ψ : regularFockDomain) (x : Fin 4→ℝ) :
    regularStressTotal ψ.val x=realCoordinateStress ψ x := by
  classical
  simp only [regularStressTotal,dif_pos ψ.property]

 theorem regularStressTotal_vacuum (x : Fin 4→ℝ) : regularStressTotal vacuum x=0 := by
  rw [show vacuum=regularVacuum.val from rfl,regularStressTotal_on_domain,
    realCoordinateStress_vacuum]

 theorem regularStressTotal_translate (a : Fin 4→ℝ) (ψ : regularFockDomain)
    (x : Fin 4→ℝ) :
    regularStressTotal (gamma (U1 a) ψ.val) x=regularStressTotal ψ.val (x-a) := by
  change regularStressTotal (regularGamma (U1 a) (strongRegularProfile_U1 a) ψ).val x=_
  rw [regularStressTotal_on_domain,regularStressTotal_on_domain,realCoordinateStress_translate]

 theorem regularStressTotal_boost (s : ℝ) (ψ : regularFockDomain) (x : Fin 4→ℝ) :
    regularStressTotal (gamma (B0 s) ψ.val) x=
      (boostMat (-s)).transpose*regularStressTotal ψ.val (wedgeBoostMap (-s) x)*boostMat (-s) := by
  change regularStressTotal (regularGamma (B0 s) (strongRegularProfile_B0 s) ψ).val x=_
  rw [regularStressTotal_on_domain,regularStressTotal_on_domain,realCoordinateStress_boost]

 def regularMaxwellQuadraticForm {D : CanonicalNetInput} (A : RemainingModularCoreInput D) :
    TGLExt.MaxwellBridge.MaxwellQuadraticForm A.toCertificate where
  Dom := regularFockDomain
  Dom_vac := vacuum_mem_regularFockDomain
  Dom_translate := regularFockDomain_translate
  Dom_boost := regularFockDomain_boost
  Q := regularStressTotal
  Q_vac := regularStressTotal_vacuum
  Q_covariant := fun a ψ x h=>regularStressTotal_translate a ⟨ψ,h⟩ x
  Q_symmetric := fun ψ x h=>by
    rw [show regularStressTotal ψ x=realCoordinateStress ⟨ψ,h⟩ x from
      regularStressTotal_on_domain ⟨ψ,h⟩ x]
    exact realCoordinateStress_symmetric ⟨ψ,h⟩ x
  Q_test_integrable := fun ψ h ν μ f hf hc=>by
    have he (x : Fin 4→ℝ) : regularStressTotal ψ x=realCoordinateStress ⟨ψ,h⟩ x :=
      regularStressTotal_on_domain ⟨ψ,h⟩ x
    simp only [he]
    exact realCoordinateStress_test_integrable ⟨ψ,h⟩ ν μ f hf hc
  Q_conserved := fun ψ h ν f hf hc=>by
    have he (x : Fin 4→ℝ) : regularStressTotal ψ x=realCoordinateStress ⟨ψ,h⟩ x :=
      regularStressTotal_on_domain ⟨ψ,h⟩ x
    simp only [he]
    exact realCoordinateStress_conserved ⟨ψ,h⟩ ν f hf hc
  Q_boost_covariant := fun s ψ x h=>regularStressTotal_boost s ⟨ψ,h⟩ x

 theorem regularMaxwellQuadraticForm_nontrivial {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) :
    ∃ψ : A.toCertificate.F,ψ∈(regularMaxwellQuadraticForm A).Dom ∧
      0<(regularMaxwellQuadraticForm A).Q ψ 0 0 0 := by
  obtain ⟨ψ,hψ⟩:=realCoordinateStress_nontrivial
  refine ⟨ψ.val,ψ.property,?_⟩
  change 0<regularStressTotal ψ.val 0 0 0
  rw [regularStressTotal_on_domain]
  exact hψ

 theorem regularMaxwellQuadraticForm_exact {D : CanonicalNetInput}
    (A : RemainingModularCoreInput D) (ψ : regularFockDomain) (x : Fin 4→ℝ) :
    (regularMaxwellQuadraticForm A).Q ψ.val x=realCoordinateStress ψ x :=
  regularStressTotal_on_domain ψ x

end F1Fecho.MaxwellGlobal
#print axioms F1Fecho.MaxwellGlobal.boost_action_symm_coordinates
#print axioms F1Fecho.MaxwellGlobal.pull_realPart
#print axioms F1Fecho.MaxwellGlobal.realCoordinateStress_boost
#print axioms F1Fecho.MaxwellGlobal.regularStressTotal_on_domain
#print axioms F1Fecho.MaxwellGlobal.regularStressTotal_translate
#print axioms F1Fecho.MaxwellGlobal.regularStressTotal_boost
#print axioms F1Fecho.MaxwellGlobal.regularMaxwellQuadraticForm
#print axioms F1Fecho.MaxwellGlobal.regularMaxwellQuadraticForm_nontrivial
#print axioms F1Fecho.MaxwellGlobal.regularMaxwellQuadraticForm_exact
