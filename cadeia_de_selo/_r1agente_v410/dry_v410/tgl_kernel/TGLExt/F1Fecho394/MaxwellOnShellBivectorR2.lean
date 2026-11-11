import TGLExt.O16.BoostScreenPolarizations_v2
import Mathlib.Tactic

/-! Concrete on-shell Maxwell bivectors from the existing O16 transverse screens.
The metric is (+---). Components of `strength` have upper indices; divergence
contracts the first index with the lowered momentum. This is an algebraic
on-shell construction, not yet a spacetime test-function map or stress tensor. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
namespace F1Fecho.MaxwellOnShell
open Complex Matrix ChatgptAudit.WignerOrbit016 ChatgptAudit.WignerRapidityMeasure016

def pairing (p e : Fin 4 → ℂ) : ℂ := p 0*e 0-p 1*e 1-p 2*e 2-p 3*e 3
def strength (p e : Fin 4 → ℂ) (μ ν : Fin 4) : ℂ := p μ*e ν-p ν*e μ

theorem strength_antisymmetric (p e : Fin 4 → ℂ) (μ ν : Fin 4) :
    strength p e μ ν = -strength p e ν μ := by unfold strength; ring

theorem strength_gauge (p e : Fin 4 → ℂ) (a : ℂ) :
    strength p (e+a • p)=strength p e := by
  funext μ ν
  simp only [strength,Pi.add_apply,Pi.smul_apply,smul_eq_mul]
  ring

theorem strength_bianchi (p e : Fin 4 → ℂ) (μ ν ρ : Fin 4) :
    p μ*strength p e ν ρ+p ν*strength p e ρ μ+p ρ*strength p e μ ν=0 := by
  unfold strength
  ring

theorem strength_divergence (p e : Fin 4 → ℂ) (ν : Fin 4) :
    pairing p (fun μ => strength p e μ ν)=pairing p p*e ν-p ν*pairing p e := by
  unfold pairing strength
  ring

theorem strength_source_free (p e : Fin 4 → ℂ) (hp : pairing p p=0)
    (he : pairing p e=0) (ν : Fin 4) : pairing p (fun μ => strength p e μ ν)=0 := by
  rw [strength_divergence,hp,he]; ring

def momentum (y : MomentumCoordinates) : Fin 4 → ℂ :=
  fun i => (shellMomentum 0 (rapidityChart 0 y) i : ℂ)

theorem momentum_null (y : MomentumCoordinates) (hy : y.1≠0) :
    pairing (momentum y) (momentum y)=0 := by
  have hr := transverseMass_pos_of_ne_zero 0 y.1 hy
  have hsq := transverseMass_sq 0 y.1
  have hc := congrArg (fun x : ℝ => (transverseMass 0 y.1)^2*x)
    (Real.cosh_sq_sub_sinh_sq y.2)
  have hh : orbitPairing (shellMomentum 0 (rapidityChart 0 y))
      (shellMomentum 0 (rapidityChart 0 y))=0 := by
    rw [shellMomentum_chart 0 y hr]
    simp only [orbitPairing,Matrix.cons_val_zero,Matrix.cons_val_one,
      Matrix.cons_val,Matrix.head_cons,Matrix.head_fin_const]
    nlinarith
  simpa [pairing,momentum,orbitPairing] using congrArg Complex.ofReal hh

theorem circular_transverse (h : ℝ) (y : MomentumCoordinates) (hy : y.1≠0) :
    pairing (momentum y) (circularScreen h y)=0 := by
  have h1 := congrArg Complex.ofReal (screenOne_transverse y hy)
  have h2 := congrArg Complex.ofReal (screenTwo_transverse y hy)
  simp only [Complex.ofReal_zero,orbitPairing,Complex.ofReal_sub,Complex.ofReal_mul] at h1 h2
  unfold pairing momentum circularScreen
  linear_combination h1 + (h:ℂ)*I*h2

def circularStrength (h : ℝ) (y : MomentumCoordinates) :=
  strength (momentum y) (circularScreen h y)

theorem circular_source_free (h : ℝ) (y : MomentumCoordinates) (hy : y.1≠0) (ν : Fin 4) :
    pairing (momentum y) (fun μ => circularStrength h y μ ν)=0 :=
  strength_source_free _ _ (momentum_null y hy) (circular_transverse h y hy) ν

theorem circular_bianchi (h : ℝ) (y : MomentumCoordinates) (μ ν ρ : Fin 4) :
    momentum y μ*circularStrength h y ν ρ+
      momentum y ν*circularStrength h y ρ μ+momentum y ρ*circularStrength h y μ ν=0 :=
  strength_bianchi _ _ μ ν ρ

theorem circular_01 (h : ℝ) (y : MomentumCoordinates) (hy : y.1≠0) :
    circularStrength h y 0 1=(transverseMass 0 y.1:ℂ) := by
  have hr := transverseMass_pos_of_ne_zero 0 y.1 hy
  have hc := congrArg Complex.ofReal (Real.cosh_sq_sub_sinh_sq y.2)
  simp only [Complex.ofReal_sub,Complex.ofReal_pow,Complex.ofReal_one] at hc
  unfold circularStrength strength momentum
  rw [shellMomentum_chart 0 y hr]
  simp only [circularScreen,screenOne,screenTwo,Matrix.cons_val_zero,Matrix.cons_val_one,
    Complex.ofReal_zero,mul_zero,add_zero,Complex.ofReal_mul]
  linear_combination (transverseMass 0 y.1:ℂ)*hc

theorem circular_nonzero (h : ℝ) (y : MomentumCoordinates) (hy : y.1≠0) :
    circularStrength h y≠0 := by
  intro he
  have hz := congrFun (congrFun he 0) 1
  rw [circular_01 h y hy] at hz
  have hr := (transverseMass_pos_of_ne_zero 0 y.1 hy).ne'
  exact hr (Complex.ofReal_eq_zero.mp hz)

end F1Fecho.MaxwellOnShell
#print axioms F1Fecho.MaxwellOnShell.strength_gauge
#print axioms F1Fecho.MaxwellOnShell.strength_bianchi
#print axioms F1Fecho.MaxwellOnShell.strength_source_free
#print axioms F1Fecho.MaxwellOnShell.momentum_null
#print axioms F1Fecho.MaxwellOnShell.circular_transverse
#print axioms F1Fecho.MaxwellOnShell.circular_source_free
#print axioms F1Fecho.MaxwellOnShell.circular_01
#print axioms F1Fecho.MaxwellOnShell.circular_nonzero
