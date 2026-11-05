import TGLExt.F1Fecho394.ConcreteWeylR1
import TGLExt.F1Fecho394.ConcreteWeylContinuityR2
/-!
Field convention W(f)=D(i f), with D the previously constructed displacement.
Thus W(k)Omega is proportional to e(i k). If one-particle Tomita fixes k in K,
its antilinearity sends i k to -i k, matching W(k)*Omega. This file establishes
the phase change and its algebraic consequences, not the Tomita identification.
There is no 1/sqrt(2) in this convention: the cocycle is exp(-i Im inner(f,g)).
The earlier displacement construction remains unchanged.
-/
set_option autoImplicit false
set_option maxHeartbeats 1500000
noncomputable section
namespace F1Fecho.FieldWeyl
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Fecho.Exponential
open F1Fecho.WeylCoefficients

def rotate (f : H1) : H1 := Complex.I • f

theorem rotate_inner (f g : H1) : inner ℂ (rotate f) (rotate g) = inner ℂ f g := by
  simp only [rotate,inner_smul_left,inner_smul_right,Complex.conj_I]
  calc
    Complex.I * (-Complex.I * inner ℂ f g) = -(Complex.I * Complex.I) * inner ℂ f g := by ring
    _ = inner ℂ f g := by simp

theorem rotate_add (f g : H1) : rotate (f+g) = rotate f + rotate g := by simp [rotate,smul_add]

theorem rotate_neg (f : H1) : rotate (-f) = -rotate f := by simp [rotate]

def W (f : H1) : F →L[ℂ] F := ConcreteWeyl.W (rotate f)

theorem W_zero : W 0 = 1 := by simp [W,rotate,ConcreteWeyl.W_zero]

theorem W_strongly_continuous (v : F) : Continuous (fun f : H1 => W f v) :=
  (ConcreteWeyl.W_strongly_continuous v).comp (continuous_const.smul continuous_id)


theorem W_star (f : H1) : star (W f) = W (-f) := by
  simp only [W,ConcreteWeyl.W_star,rotate_neg]

theorem W_ccr (f g : H1) : W f * W g = phase f g • W (f+g) := by
  simp only [W,ConcreteWeyl.W_ccr,phase,rotate_inner,rotate_add]

theorem W_local (f g : H1) (h : (inner ℂ f g).im = 0) : Commute (W f) (W g) := by
  apply ConcreteWeyl.W_local
  simpa only [rotate_inner] using h

theorem W_covariance (u : H1 ≃ₗᵢ[ℂ] H1) (f : H1) :
    (gamma u).conjStarAlgEquiv (W f) = W (u f) := by
  simp only [W,ConcreteWeyl.W_covariance,rotate,map_smul]

theorem W_vacuum (f : H1) : W f vacuum = amplitude (rotate f) 0 • exponential (rotate f) :=
  ConcreteWeyl.W_vacuum (rotate f)

theorem vacuum_characteristic (f : H1) :
    inner ℂ vacuum (W f vacuum) = Complex.exp (-((‖f‖ : ℂ)^2)/2) := by
  rw [W,ConcreteWeyl.vacuum_characteristic]
  simp [rotate,norm_smul]

def R (K : Submodule ℝ H1) : VonNeumannAlgebra F := F1Fecho.WeylNet.R W K

theorem R_mono (K K' : Submodule ℝ H1) (h : K ≤ K') :
    (R K : Set (F →L[ℂ] F)) ⊆ R K' := F1Fecho.WeylNet.R_mono W W_star K K' h

theorem R_local (K K' : Submodule ℝ H1)
    (h : ∀ f ∈ K, ∀ g ∈ K', (inner ℂ f g).im = 0) :
    ∀ x ∈ R K, ∀ y ∈ R K', Commute x y := F1Fecho.WeylNet.R_local W W_star W_local K K' h

theorem R_covariance (u : H1 ≃ₗᵢ[ℂ] H1) (K K' : Submodule ℝ H1)
    (h : ∀ f, f ∈ K ↔ u f ∈ K') (x : F →L[ℂ] F) :
    x ∈ R K ↔ (gamma u).conjStarAlgEquiv x ∈ R K' :=
  F1Fecho.WeylNet.R_cov W W_star u (gamma u).conjStarAlgEquiv (W_covariance u) K K' h x

theorem W_mem_R (K : Submodule ℝ H1) (f : H1) (hf : f ∈ K) : W f ∈ R K :=
  F1Fecho.WeylNet.generators_mem _ (F1Fecho.WeylNet.generators_star_closed W W_star K) ⟨f,hf,rfl⟩

def wedgeFlow (L : TGLExt.QGSolution.LightNetData) (t : ℝ) :
    (R (L.K TGL.SpecificAQFT.rightWedge)).toStarSubalgebra ≃⋆ₐ[ℂ]
    (R (L.K TGL.SpecificAQFT.rightWedge)).toStarSubalgebra :=
  F1Fecho.WeylFlow.wedgeFlow W W_star W_covariance L t

theorem wedgeFlow_zero (L : TGLExt.QGSolution.LightNetData) :
    wedgeFlow L 0 = StarAlgEquiv.refl := F1Fecho.WeylFlow.wedgeFlow_zero W W_star W_covariance L

theorem wedgeFlow_add (L : TGLExt.QGSolution.LightNetData) (s t : ℝ) :
    wedgeFlow L (s+t) = (wedgeFlow L s).trans (wedgeFlow L t) :=
  F1Fecho.WeylFlow.wedgeFlow_add W W_star W_covariance L s t

theorem wedgeFlow_is_Ad (L : TGLExt.QGSolution.LightNetData) (t : ℝ)
    (a : (R (L.K TGL.SpecificAQFT.rightWedge)).toStarSubalgebra) :
    ((wedgeFlow L t) a).val = (gamma (B0 (-(2*Real.pi*t)))).conjStarAlgEquiv a.val := rfl

end F1Fecho.FieldWeyl
open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    if (`F1Fecho.FieldWeyl).isPrefixOf n then
      let axs ← collectAxioms n
      IO.println ("LOCAL_DECL\t" ++ n.toString ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
      unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
        throwError "AXIOM_AUDIT_REFUSED: {n}"
      match ci with
      | .axiomInfo _ => throwError "LOCAL_AXIOM_REFUSED: {n}"
      | _ => pure ()
