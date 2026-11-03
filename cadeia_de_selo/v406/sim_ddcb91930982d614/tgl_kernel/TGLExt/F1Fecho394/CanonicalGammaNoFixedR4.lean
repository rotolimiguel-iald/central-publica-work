import TGLExt.F1Fecho394.TensorNoFixedR2
import Lean
import TGLExt.F1Fecho394.BosonicFock
import TGLExt.F1Fecho394.CanonicalWedge
import Mathlib.Analysis.Normed.Module.FiniteDimension
/-! The general no-projective-eigenvector hypothesis is propagated through
the actual completed symmetric tensor sectors. Only the vacuum can remain. -/
set_option autoImplicit false
set_option maxHeartbeats 1800000
noncomputable section
open UniformSpace
open scoped TensorProduct
namespace F1Fecho.CanonicalGammaNoFixed
open TGLExt.ImportedSQ F1Rede.BosonicSectors F1Rede.BosonicFock
open F1Rede.CanonicalWedge F1Rede.SectorDirectSum

theorem zero_sector_span (x : Sector 0) : ∃ c : ℂ, c • vacuumSector = x := by
  have hs : ∀ z : Completion ℂ, z ∈ (ℂ ∙ ((1 : ℂ) : Completion ℂ)) := by
    intro z
    refine Completion.induction_on z
      (ℂ ∙ ((1 : ℂ) : Completion ℂ)).closed_of_finiteDimensional ?_
    intro c
    apply Submodule.mem_span_singleton.mpr
    refine ⟨c,?_⟩
    rw [← Completion.coe_smul]
    simp
  obtain ⟨c,hc⟩ := Submodule.mem_span_singleton.mp (hs (x : TensorHilbert 0))
  refine ⟨c,Subtype.ext ?_⟩
  exact hc

theorem positive_sector_fixed_zero
    (u : ℝ → H1 ≃ₗᵢ[ℂ] H1) (h0 : u 0 = LinearIsometryEquiv.refl ℂ H1)
    (hadd : ∀ s t, u (s+t) = (u t).trans (u s))
    (hno : ∀ f : H1, (∀ l : ℝ, ∃ c : ℂ, ‖c‖ = 1 ∧ u l f = c • f) → f = 0)
    (n : ℕ) (x : Sector (n+1)) (hx : ∀ l, gammaSector (u l) (n+1) x = x) : x = 0 := by
  apply Subtype.ext
  apply F1Fecho.TensorNoFixed.tensor_fixed_eq_zero Jcandidate u h0 hadd hno
    (fun l => algebraicGamma (u l) n) (x : TensorHilbert (n+1))
  intro l
  exact congrArg Subtype.val (hx l)

theorem gamma_no_fixed
    (u : ℝ → H1 ≃ₗᵢ[ℂ] H1) (h0 : u 0 = LinearIsometryEquiv.refl ℂ H1)
    (hadd : ∀ s t, u (s+t) = (u t).trans (u s))
    (_hcontinuous : ∀ ξ, Continuous (fun s => u s ξ))
    (hno : ∀ f : H1, (∀ l : ℝ, ∃ c : ℂ, ‖c‖ = 1 ∧ u l f = c • f) → f = 0)
    (ψ : F) (hψ : ∀ l, gamma (u l) ψ = ψ) : ψ ∈ (ℂ ∙ vacuum) := by
  have hpos (n : ℕ) : ψ (n+1) = 0 := by
    apply positive_sector_fixed_zero u h0 hadd hno n
    intro l
    exact congrArg (fun q : F => q (n+1)) (hψ l)
  obtain ⟨c,hc⟩ := zero_sector_span (ψ 0)
  apply Submodule.mem_span_singleton.mpr
  refine ⟨c,?_⟩
  apply lp.ext
  funext n
  cases n with
  | zero =>
    change c • (lp.single 2 0 vacuumSector) 0 = ψ 0
    simpa only [lp.single_apply_self] using hc
  | succ n =>
    change c • vacuum (n+1) = ψ (n+1)
    rw [hpos n]
    simp [vacuum,sectorEmbedding_apply,lp.single_apply_ne]

end F1Fecho.CanonicalGammaNoFixed
#print axioms F1Fecho.CanonicalGammaNoFixed.zero_sector_span
#print axioms F1Fecho.CanonicalGammaNoFixed.positive_sector_fixed_zero
#print axioms F1Fecho.CanonicalGammaNoFixed.gamma_no_fixed

open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  let roots : List Name := [`TGLExt.F1Fecho394.TensorContractionR5, `TGLExt.F1Fecho394.TensorContractionPropertiesR3, `TGLExt.F1Fecho394.TensorNoFixedR2, `TGLExt.F1Fecho394.FiniteCommutingEigenR3, `TGLExt.F1Fecho394.NoFiniteInvariantR3, `TGLExt.F1Fecho394.UnitaryNoFiniteInvariantR1]
  let indices := roots.filterMap env.getModuleIdx?
  unless indices.length == roots.length do throwError "MISSING_MODULE_REFUSED"
  let mut count := 0
  for (n, ci) in env.constants.toList do
    if (env.getModuleIdxFor? n).any (fun i => indices.contains i) then
      count := count + 1
      let axs ← collectAxioms n
      IO.println ("LOCAL_DECL\t" ++ n.toString ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
      unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
        throwError "AXIOM_AUDIT_REFUSED: {n}"
      match ci with
      | .axiomInfo _ => throwError "LOCAL_AXIOM_REFUSED: {n}"
      | _ => pure ()
  for (n, ci) in env.constants.map₂.toList do
    count := count + 1
    let axs ← collectAxioms n
    IO.println ("LOCAL_DECL\t" ++ n.toString ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
    unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
      throwError "AXIOM_AUDIT_REFUSED: {n}"
    match ci with
    | .axiomInfo _ => throwError "LOCAL_AXIOM_REFUSED: {n}"
    | _ => pure ()
  if count == 0 then throwError "EMPTY_AUDIT_REFUSED"
  IO.println ("AUDITED_COUNT\t" ++ toString count)
