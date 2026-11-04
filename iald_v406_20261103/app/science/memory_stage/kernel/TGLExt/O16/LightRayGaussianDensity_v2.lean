import Lean
import TGLExt.O16.LightRayGaussianOrthogonality_v2
import Mathlib.Analysis.InnerProductSpace.Projection.Basic

set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open MeasureTheory Filter Complex
open ChatgptAudit.Continuous049 ChatgptAudit.FourierBridge016 FormaInscrita.RetaDeLuz

namespace ChatgptAudit.LightRayCore016
local instance instLocalLightRayGaussianDensityv21 : Module ℝ SpectralHilbert := NormedSpace.complexToReal.toModule
local instance instLocalLightRayGaussianDensityv22 : NormedSpace ℝ SpectralHilbert := NormedSpace.complexToReal
local instance instLocalLightRayGaussianDensityv23 : InnerProductSpace ℝ SpectralHilbert := InnerProductSpace.complexToReal

/-- Density in the real standard subspace, not merely complex totality. -/
theorem gaussian_core_real_dense (b : ℝ) (hb : 0 < b) :
    ((rapidityStandardSubspace (2*Real.pi^2)).toClosedSubmodule : Set SpectralHilbert) ⊆
      closure ((Submodule.span ℝ (Set.range (fun r : ℝ => productCore 0 b r le_rfl hb))) : Set SpectralHilbert) := by
  let K := (rapidityStandardSubspace (2*Real.pi^2)).toClosedSubmodule
  let S := Submodule.span ℝ (Set.range (fun r : ℝ => productCore 0 b r le_rfl hb))
  let L := S.topologicalClosure
  have hs : S ≤ K.toSubmodule := by
    apply Submodule.span_le.mpr
    rintro f ⟨r,rfl⟩
    exact product_core_mem_rapidity_standard 0 b r le_rfl hb
  have hL : L ≤ K.toSubmodule := S.topologicalClosure_minimal hs K.isClosed
  intro h hh
  have hd : h - L.starProjection h ∈ K :=
    K.sub_mem hh (hL (L.starProjection_apply_mem h))
  have hz : h - L.starProjection h = 0 := by
    apply gaussian_core_real_orthogonal_separates b hb _ hd
    intro r
    have hc : productCore 0 b r le_rfl hb ∈ L :=
      S.le_topologicalClosure (Submodule.subset_span ⟨r,rfl⟩)
    have ho := L.starProjection_inner_eq_zero h (productCore 0 b r le_rfl hb) hc
    exact ho
  have hm : h ∈ L := by
    rw [sub_eq_zero] at hz
    rw [hz]
    exact L.starProjection_apply_mem h
  exact hm

/-- Half-sided isotony for the actual U and actual Fourier-transported standard subspace. -/
theorem halfline_isotony (a : ℝ) (ha : 0 ≤ a) (f : SpectralHilbert)
    (hf : f ∈ (rapidityStandardSubspace (2*Real.pi^2)).toClosedSubmodule) :
    U a f ∈ (rapidityStandardSubspace (2*Real.pi^2)).toClosedSubmodule := by
  exact halfline_isotony_of_gaussian_density 1 (by norm_num)
    (gaussian_core_real_dense 1 (by norm_num)) a ha f hf

#print axioms gaussian_core_real_dense
#print axioms halfline_isotony
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
