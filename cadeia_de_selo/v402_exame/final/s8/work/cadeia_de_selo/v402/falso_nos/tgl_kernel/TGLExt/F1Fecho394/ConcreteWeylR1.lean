import TGLExt.F1Fecho394.ExponentialTotalityR4
import TGLExt.F1Fecho394.WeylCovarianceR1
import TGLExt.F1Fecho394.WeylNetWiringR1
import TGLExt.F1Fecho394.WeylFlowWiringR4
/-!
Concrete Weyl operators on the original canonical bosonic Fock, constructed
from its total exponential vectors. No Weyl/CCR, covariance or totality fields
are assumed. R(K), isotony, locality and covariance are instantiated here.
The global vacuum cyclicity below concerns K=top; it is NOT wedge cyclicity.
The restricted boost flow still takes a LightNetData as the localization input.
-/
set_option autoImplicit false
set_option maxHeartbeats 1500000
noncomputable section
namespace F1Fecho.ConcreteWeyl
open TGLExt.ImportedSQ F1Rede.BosonicFock F1Fecho.Exponential
open F1Fecho.WeylCoefficients F1Fecho.GramExtension

def D (f : H1) : F ≃ₗᵢ[ℂ] F :=
  F1Fecho.WeylConstruction.D exponential exponential_inner exponential_total f

def W (f : H1) : F →L[ℂ] F :=
  F1Fecho.WeylConstruction.W exponential exponential_inner exponential_total f

theorem W_exponential (f g : H1) : W f (exponential g) =
    amplitude f g • exponential (g+f) :=
  F1Fecho.WeylConstruction.W_apply _ _ _ f g

theorem W_zero : W 0 = 1 := F1Fecho.WeylConstruction.W_zero _ _ _

theorem W_ccr (f g : H1) : W f * W g = phase f g • W (f+g) :=
  F1Fecho.WeylConstruction.W_add _ _ _ f g

theorem W_star (f : H1) : star (W f) = W (-f) :=
  F1Fecho.WeylConstruction.W_star _ _ _ f

theorem W_local (f g : H1) (h : (inner ℂ f g).im = 0) : Commute (W f) (W g) :=
  F1Fecho.WeylConstruction.W_local _ _ _ f g h

theorem W_covariance (u : H1 ≃ₗᵢ[ℂ] H1) (f : H1) :
    (gamma u).conjStarAlgEquiv (W f) = W (u f) :=
  F1Fecho.WeylConstruction.W_covariance _ _ _ u (gamma u) (gamma_exponential u) f

theorem W_vacuum (f : H1) : W f vacuum = amplitude f 0 • exponential f := by
  rw [← exponential_zero, W_exponential, zero_add]

theorem vacuum_characteristic (f : H1) :
    inner ℂ vacuum (W f vacuum) = Complex.exp (-((‖f‖ : ℂ)^2)/2) := by
  rw [W_vacuum, ← exponential_zero, inner_smul_right, exponential_inner]
  simp [amplitude_norm_form, inner_zero_left, inner_zero_right]

theorem vacuum_orbit_total :
    (Submodule.span ℂ (Set.range (fun f : H1 => W f vacuum))).topologicalClosure = ⊤ := by
  have ht := total_weighted_reindex exponential (fun f => amplitude f 0) id
    (fun f => amplitude_ne_zero f 0) Function.surjective_id exponential_total
  simpa only [W_vacuum, id_eq] using ht

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

theorem global_vacuum_cyclic :
    (Submodule.span ℂ ((fun a : F →L[ℂ] F => a vacuum) ''
      (R ⊤ : Set (F →L[ℂ] F)))).topologicalClosure = ⊤ := by
  apply eq_top_iff.mpr
  rw [← vacuum_orbit_total]
  apply Submodule.topologicalClosure_mono
  apply Submodule.span_mono
  rintro x ⟨f,rfl⟩
  exact ⟨W f,W_mem_R ⊤ f (Submodule.mem_top),rfl⟩

def wedgeFlow (L : TGLExt.QGSolution.LightNetData) (t : ℝ) :
    (R (L.K TGL.SpecificAQFT.rightWedge)).toStarSubalgebra ≃⋆ₐ[ℂ]
    (R (L.K TGL.SpecificAQFT.rightWedge)).toStarSubalgebra :=
  F1Fecho.WeylFlow.wedgeFlow W W_star W_covariance L t

theorem wedgeFlow_zero (L : TGLExt.QGSolution.LightNetData) :
    wedgeFlow L 0 = StarAlgEquiv.refl := F1Fecho.WeylFlow.wedgeFlow_zero W W_star W_covariance L

theorem wedgeFlow_add (L : TGLExt.QGSolution.LightNetData) (s t : ℝ) :
    wedgeFlow L (s+t) = (wedgeFlow L s).trans (wedgeFlow L t) :=
  F1Fecho.WeylFlow.wedgeFlow_add W W_star W_covariance L s t

end F1Fecho.ConcreteWeyl

open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    if (`F1Fecho.ConcreteWeyl).isPrefixOf n then
      let axs ← collectAxioms n
      IO.println ("LOCAL_DECL\t" ++ n.toString ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
      unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
        throwError "AXIOM_AUDIT_REFUSED: {n}"
      match ci with
      | .axiomInfo _ => throwError "LOCAL_AXIOM_REFUSED: {n}"
      | _ => pure ()
