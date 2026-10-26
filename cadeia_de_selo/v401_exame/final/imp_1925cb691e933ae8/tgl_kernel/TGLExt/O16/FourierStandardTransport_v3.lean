import Lean
import TGLExt.O16.FourierLightRayBridge

set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
open MeasureTheory Filter
open ChatgptAudit.Continuous049 ChatgptAudit.Continuous050
open FormaInscrita.RetaDeLuz

namespace ChatgptAudit.FourierBridge016

local instance instLocalFourierStandardTransportv31 : Module ℝ SpectralHilbert := NormedSpace.complexToReal.toModule
local instance instLocalFourierStandardTransportv32 : NormedSpace ℝ SpectralHilbert := NormedSpace.complexToReal

abbrev inverseFourierReal : SpectralHilbert ≃L[ℝ] SpectralHilbert :=
  fourierUnitary.symm.toContinuousLinearEquiv.restrictScalars ℝ

theorem inverseFourier_mulI (S : ClosedSubmodule ℝ SpectralHilbert) :
    S.mulI.mapEquiv inverseFourierReal = (S.mapEquiv inverseFourierReal).mulI := by
  ext x
  change x ∈ S.mulI.mapEquiv inverseFourierReal ↔ x ∈ (S.mapEquiv inverseFourierReal).mulI
  simp only [ClosedSubmodule.mulI, ClosedSubmodule.mem_mapEquiv_iff,
    scalarSMulCLE_symm_apply, Units.smul_def, Units.val_inv_eq_inv_val,
    Complex.val_UnitI, Complex.inv_I]
  change (-Complex.I) • fourierUnitary x ∈ S ↔
    fourierUnitary ((-Complex.I) • x) ∈ S
  rw [map_smul]

def rapidityStandardSubspace (c : ℝ) : StandardSubspace SpectralHilbert where
  toClosedSubmodule := (continuousStandardSubspace c).toClosedSubmodule.mapEquiv inverseFourierReal
  IsSeparating := by
    rw [← inverseFourier_mulI, ← ClosedSubmodule.mapEquiv_inf_eq,
      (continuousStandardSubspace c).IsSeparating, ClosedSubmodule.mapEquiv_bot_eq_bot]
  IsCyclic := by
    rw [← inverseFourier_mulI, ← ClosedSubmodule.mapEquiv_sup_eq,
      (continuousStandardSubspace c).IsCyclic, ClosedSubmodule.mapEquiv_top_eq_top]

theorem rapidity_standard_mem (c : ℝ) (f : SpectralHilbert) :
    f ∈ (rapidityStandardSubspace c).toClosedSubmodule ↔
      fourierUnitary f ∈ (continuousStandardSubspace c).toClosedSubmodule := by
  exact ClosedSubmodule.mem_mapEquiv_iff _ _ _

theorem rapidity_standard_fixed (c : ℝ) (f : SpectralHilbert) :
    f ∈ (rapidityStandardSubspace c).toClosedSubmodule ↔
      ∃ hf : fourierUnitary f ∈ (continuousModularOperator c).domain,
        continuousModularTomita c ⟨fourierUnitary f, hf⟩ = fourierUnitary f := by
  rw [rapidity_standard_mem, standard_membership_fourier]

/-- Full unbounded graph transported by the actual Fourier equivalence. -/
def rapidityDeltaGraph (c : ℝ) : Set (SpectralHilbert × SpectralHilbert) :=
  {fg | (fourierUnitary fg.1, fourierUnitary fg.2) ∈ (continuousModularDelta c).graph}

theorem rapidity_delta_graph (c : ℝ) (f g : SpectralHilbert) :
    (f, g) ∈ rapidityDeltaGraph c ↔
      fourierUnitary g =ᵐ[volume]
        fun x => (deltaSymbol c x : ℂ) * fourierUnitary f x := by
  exact delta_graph_symbol c (fourierUnitary f) (fourierUnitary g)

theorem rapidity_delta_domain (c : ℝ) (f : SpectralHilbert) :
    (∃ g, (f, g) ∈ rapidityDeltaGraph c) ↔
      fourierUnitary f ∈ (continuousModularDelta c).domain := by
  constructor
  · rintro ⟨g, hg⟩
    change (fourierUnitary f, fourierUnitary g) ∈ (continuousModularDelta c).graph at hg
    rw [LinearPMap.mem_graph_iff] at hg
    obtain ⟨v, hv, _⟩ := hg
    have hv2 : (v : SpectralHilbert) = fourierUnitary f := hv
    rw [← hv2]
    exact v.property
  · intro hf
    refine ⟨fourierUnitary.symm (continuousModularDelta c ⟨fourierUnitary f, hf⟩), ?_⟩
    change (fourierUnitary f, fourierUnitary (fourierUnitary.symm (continuousModularDelta c ⟨fourierUnitary f, hf⟩))) ∈ (continuousModularDelta c).graph
    rw [fourierUnitary.apply_symm_apply]
    exact (continuousModularDelta c).mem_graph ⟨fourierUnitary f, hf⟩

#print axioms inverseFourier_mulI
#print axioms rapidityStandardSubspace
#print axioms rapidity_standard_mem
#print axioms rapidity_standard_fixed
#print axioms rapidity_delta_graph
#print axioms rapidity_delta_domain

end ChatgptAudit.FourierBridge016


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
