import TGLExt.F1Fecho394.MaxwellOnShellBivectorR2
import TGLExt.O16.TransverseCocycle_v3

/-! The concrete O16 screen cocycle intertwines the physical bivector p wedge
 epsilon. The longitudinal gauge remainder is eliminated algebraically.
 No global Lorentz representation, test-function map or stress tensor is assumed. -/
set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
namespace F1Fecho.MaxwellOnShell
open Matrix ChatgptAudit.WignerOrbit016 ChatgptAudit.WignerRapidityMeasure016

def realStrength (p e : Fin 4 → ℝ) (μ ν : Fin 4) : ℝ := p μ*e ν-p ν*e μ

theorem real_strength_screen_transport
    (g : (Fin 4 → ℝ) →ₗ[ℝ] (Fin 4 → ℝ)) (x y : MomentumCoordinates)
    (hx : x.1≠0) (hy : y.1≠0)
    (gp : g (shellMomentum 0 (rapidityChart 0 x))=shellMomentum 0 (rapidityChart 0 y))
    (gm : ∀ a b,orbitPairing (g a) (g b)=orbitPairing a b) (j : Fin 2) (μ ν : Fin 4) :
    realStrength (g (shellMomentum 0 (rapidityChart 0 x))) (g (screen x j)) μ ν =
      screenCoefficient g x y 0 j*realStrength (shellMomentum 0 (rapidityChart 0 y)) (screen y 0) μ ν+
      screenCoefficient g x y 1 j*realStrength (shellMomentum 0 (rapidityChart 0 y)) (screen y 1) μ ν := by
  have ht : orbitPairing (g (screen x j)) (shellMomentum 0 (rapidityChart 0 y))=0 := by
    rw [←gp,gm]
    exact screen_transverse x hx j
  have hd := transverse_decomposition y hy (g (screen x j)) ht
  rw [gp]
  unfold realStrength
  rw [congrFun hd ν,congrFun hd μ]
  simp only [Pi.sub_apply,Pi.smul_apply,smul_eq_mul]
  simp only [screenCoefficient,screen,Matrix.cons_val_zero,Matrix.cons_val_one,Matrix.cons_val_fin_one]
  rw [orbitPairing_symm (screenOne y) (g (![screenOne x,screenTwo x] j)),
    orbitPairing_symm (screenTwo y) (g (![screenOne x,screenTwo x] j))]
  ring

def realLift (p : Fin 4 → ℝ) : Fin 4 → ℂ := fun i => (p i:ℂ)

theorem strength_of_real (p e : Fin 4 → ℝ) (μ ν : Fin 4) :
    strength (realLift p) (realLift e) μ ν=(realStrength p e μ ν:ℂ) := by
  simp [strength,realStrength,realLift]

theorem strength_screen_transport
    (g : (Fin 4 → ℝ) →ₗ[ℝ] (Fin 4 → ℝ)) (x y : MomentumCoordinates)
    (hx : x.1≠0) (hy : y.1≠0)
    (gp : g (shellMomentum 0 (rapidityChart 0 x))=shellMomentum 0 (rapidityChart 0 y))
    (gm : ∀ a b,orbitPairing (g a) (g b)=orbitPairing a b) (j : Fin 2) (μ ν : Fin 4) :
    strength (realLift (g (shellMomentum 0 (rapidityChart 0 x)))) (realLift (g (screen x j))) μ ν =
      (screenCoefficient g x y 0 j:ℂ)*strength (momentum y) (realLift (screen y 0)) μ ν+
      (screenCoefficient g x y 1 j:ℂ)*strength (momentum y) (realLift (screen y 1)) μ ν := by
  have hh := congrArg Complex.ofReal (real_strength_screen_transport g x y hx hy gp gm j μ ν)
  simpa only [momentum,realLift,strength,realStrength,Complex.ofReal_add,Complex.ofReal_sub,
    Complex.ofReal_mul] using hh

end F1Fecho.MaxwellOnShell
#print axioms F1Fecho.MaxwellOnShell.real_strength_screen_transport
#print axioms F1Fecho.MaxwellOnShell.strength_of_real
#print axioms F1Fecho.MaxwellOnShell.strength_screen_transport
