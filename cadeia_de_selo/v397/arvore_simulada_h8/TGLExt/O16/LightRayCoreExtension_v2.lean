import Lean
import TGLExt.O16.LightRayCoreMembership

set_option autoImplicit false
set_option maxHeartbeats 1600000
noncomputable section
open MeasureTheory Filter Complex
open ChatgptAudit.Continuous049 ChatgptAudit.FourierBridge016 FormaInscrita.RetaDeLuz

namespace ChatgptAudit.LightRayCore016

local instance instModuleRealSHCoreExt : Module ℝ SpectralHilbert := NormedSpace.complexToReal.toModule
local instance instNormedSpaceRealSHCoreExt : NormedSpace ℝ SpectralHilbert := NormedSpace.complexToReal

theorem product_core_ae (a b r : ℝ) (ha : 0 ≤ a) (hb : 0 < b) :
    productCore a b r ha hb =ᵐ[volume]
      fun x : ℝ => multiplier a (x : ℂ) * twistedGaussian b r (x : ℂ) := by
  exact MemLp.coeFn_toLp _

theorem multiplier_eq_transSymbol (a x : ℝ) : multiplier a (x : ℂ) = transSymbol a x := by
  unfold multiplier transSymbol nullMomentum
  rw [← ofReal_exp]
  push_cast
  congr 1
  ring

theorem U_gaussian_core (a b r : ℝ) (ha : 0 ≤ a) (hb : 0 < b) :
    U a (productCore 0 b r le_rfl hb) = productCore a b r ha hb := by
  apply Lp.ext
  filter_upwards [U_ae a (productCore 0 b r le_rfl hb),
    product_core_ae 0 b r le_rfl hb, product_core_ae a b r ha hb] with x hu hz ha'
  rw [hu, hz, ha']
  simp only [multiplier_eq_transSymbol]
  simp [transSymbol]

/-- Only density is assumed here; the core action, weighted domain and closed extension are proved. -/
theorem halfline_isotony_of_gaussian_density (b : ℝ) (hb : 0 < b)
    (hdensity : ((rapidityStandardSubspace (2*Real.pi^2)).toClosedSubmodule : Set SpectralHilbert) ⊆
      closure ((Submodule.span ℝ (Set.range (fun r : ℝ => productCore 0 b r le_rfl hb))) : Set SpectralHilbert))
    (a : ℝ) (ha : 0 ≤ a) (f : SpectralHilbert)
    (hf : f ∈ (rapidityStandardSubspace (2*Real.pi^2)).toClosedSubmodule) :
    U a f ∈ (rapidityStandardSubspace (2*Real.pi^2)).toClosedSubmodule := by
  let K := (rapidityStandardSubspace (2*Real.pi^2)).toClosedSubmodule
  let C : ClosedSubmodule ℝ SpectralHilbert := K.comap ((U a).restrictScalars ℝ)
  have hs : Submodule.span ℝ (Set.range (fun r : ℝ => productCore 0 b r le_rfl hb)) ≤
      C.toSubmodule := by
    apply Submodule.span_le.mpr
    rintro g ⟨r, rfl⟩
    change U a (productCore 0 b r le_rfl hb) ∈ K
    rw [U_gaussian_core a b r ha hb]
    exact product_core_mem_rapidity_standard a b r ha hb
  exact (closure_minimal hs C.isClosed) (hdensity hf)

#print axioms product_core_ae
#print axioms multiplier_eq_transSymbol
#print axioms U_gaussian_core
#print axioms halfline_isotony_of_gaussian_density

end ChatgptAudit.LightRayCore016


-- Engineering audit: all declarations introduced by this compilation unit.
open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    let axs ← collectAxioms n
    let kind := match ci with
      | .axiomInfo _ => "axiom"
      | .thmInfo _ => "theorem"
      | .defnInfo _ => "definition"
      | _ => "generated_or_type"
    IO.println ("BENCH_DECL\t" ++ n.toString ++ "\t" ++ kind ++ "\t" ++
      String.intercalate "," (axs.toList.map Name.toString))
    unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
      throwError "AXIOM_AUDIT_REFUSED: {n}"
    if kind == "axiom" then throwError "NEW_AXIOM_REFUSED: {n}"
