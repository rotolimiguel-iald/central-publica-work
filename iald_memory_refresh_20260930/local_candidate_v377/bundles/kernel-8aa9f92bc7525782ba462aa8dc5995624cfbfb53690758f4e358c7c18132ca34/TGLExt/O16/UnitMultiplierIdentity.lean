import Lean
import Mathlib.MeasureTheory.Function.Holder
import Mathlib.MeasureTheory.Function.L2Space
import Mathlib.MeasureTheory.Function.LpSpace.Indicator
import Mathlib.Tactic

set_option autoImplicit false
noncomputable section
open MeasureTheory Filter
open scoped ENNReal
namespace ChatgptAudit.UnitMultiplier016

variable {X E : Type*} [MeasurableSpace X]
  [NormedAddCommGroup E] [NormedSpace ℂ E]

/-- The same Holder multiplication construction already used by
ContinuousModularMultipliers, generalized to a measurable base and a complex fiber. -/
def unitWeight (μ : Measure X) (u : X → ℂ) (hu : Measurable u)
    (hn : ∀ x, ‖u x‖ = 1) : Lp ℂ ∞ μ :=
  (memLp_top_of_bound hu.aestronglyMeasurable 1
    (ae_of_all _ fun x => (hn x).le)).toLp u

theorem unitWeight_ae (μ : Measure X) (u : X → ℂ) (hu : Measurable u)
    (hn : ∀ x, ‖u x‖ = 1) : unitWeight μ u hu hn =ᵐ[μ] u :=
  MemLp.coeFn_toLp _

def unitMultiplier (μ : Measure X) (u : X → ℂ) (hu : Measurable u)
    (hn : ∀ x, ‖u x‖ = 1) : Lp E 2 μ →L[ℂ] Lp E 2 μ :=
  (ContinuousLinearMap.lsmul ℂ ℂ).holderL μ ∞ 2 2 (unitWeight μ u hu hn)

theorem unitMultiplier_ae (μ : Measure X) (u : X → ℂ) (hu : Measurable u)
    (hn : ∀ x, ‖u x‖ = 1) (f : Lp E 2 μ) :
    unitMultiplier μ u hu hn f =ᵐ[μ] fun x => u x • f x := by
  have h := (ContinuousLinearMap.lsmul ℂ ℂ).coeFn_holder
    (r := 2) (unitWeight μ u hu hn) f
  filter_upwards [h, unitWeight_ae μ u hu hn] with x hx hux
  simpa only [unitMultiplier, ContinuousLinearMap.holderL_apply_apply,
    ContinuousLinearMap.lsmul_apply, hux] using hx

theorem unitMultiplier_norm (μ : Measure X) (u : X → ℂ) (hu : Measurable u)
    (hn : ∀ x, ‖u x‖ = 1) (f : Lp E 2 μ) :
    ‖unitMultiplier μ u hu hn f‖ = ‖f‖ := by
  apply le_antisymm
  · apply Lp.norm_le_norm_of_ae_le
    filter_upwards [unitMultiplier_ae μ u hu hn f] with x hx
    simp [hx, norm_smul, hn]
  · apply Lp.norm_le_norm_of_ae_le
    filter_upwards [unitMultiplier_ae μ u hu hn f] with x hx
    simp [hx, norm_smul, hn]

/-- Indicators on the countable finite-measure cover detect the multiplier.
No pointwise conclusion is extracted from a measure-zero set. -/
theorem scalar_action_identity_ae [Nontrivial E] (μ : Measure X) [SigmaFinite μ]
    (u : X → ℂ)
    (h : ∀ f : Lp E 2 μ, (fun x => u x • f x) =ᵐ[μ] f) :
    u =ᵐ[μ] fun _ => 1 := by
  obtain ⟨v, hv⟩ := exists_ne (0 : E)
  have hlocal (n : ℕ) : ∀ᵐ x ∂μ, x ∈ spanningSets μ n → u x = 1 := by
    let f : Lp E 2 μ := indicatorConstLp 2 (measurableSet_spanningSets μ n)
      (measure_spanningSets_lt_top μ n).ne v
    have hf : ∀ᵐ x ∂μ, x ∈ spanningSets μ n → f x = v :=
      indicatorConstLp_coeFn_mem
    filter_upwards [h f, hf] with x hx hfx
    intro hxn
    apply smul_left_injective ℂ hv
    simpa [hfx hxn] using hx
  filter_upwards [ae_all_iff.2 hlocal] with x hx
  exact hx (spanningSetsIndex μ x) (mem_spanningSetsIndex μ x)

theorem unitMultiplier_identity_iff [Nontrivial E] (μ : Measure X) [SigmaFinite μ]
    (u : X → ℂ) (hu : Measurable u) (hn : ∀ x, ‖u x‖ = 1) :
    (∀ f : Lp E 2 μ, unitMultiplier μ u hu hn f = f) ↔
      u =ᵐ[μ] fun _ => 1 := by
  constructor
  · intro h
    apply scalar_action_identity_ae (E := E) μ u
    intro f
    have hf := unitMultiplier_ae μ u hu hn f
    rw [h f] at hf
    exact hf.symm
  · intro h f
    apply Lp.ext
    filter_upwards [unitMultiplier_ae μ u hu hn f, h] with x hx hux
    simpa [hux] using hx

#print axioms unitWeight_ae
#print axioms unitMultiplier_ae
#print axioms unitMultiplier_norm
#print axioms scalar_action_identity_ae
#print axioms unitMultiplier_identity_iff
end ChatgptAudit.UnitMultiplier016


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
