import Lean
import Mathlib.MeasureTheory.Function.L2Space
import Mathlib.MeasureTheory.Measure.Haar.Unique
import Mathlib.MeasureTheory.Group.Measure
import Mathlib.Algebra.Order.Interval.Set.Group
import Mathlib.Algebra.Order.ToIntervalMod
import Mathlib.MeasureTheory.Group.LIntegral
import Mathlib.Tactic

set_option autoImplicit false
noncomputable section
open MeasureTheory Filter Set
open scoped ENNReal
namespace ChatgptAudit.WignerRapidity016
variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℂ E]

/- Adaptation of RetaDeLuzEspectro.D_no_eigen to arbitrary fibers E.
This does not itself identify the invariant orbit measure with rapidity measure. -/
def rapidityShift (s : ℝ) :
    Lp E 2 (volume : Measure ℝ) →ₗᵢ[ℂ] Lp E 2 (volume : Measure ℝ) :=
  Lp.compMeasurePreservingₗᵢ ℂ (fun x : ℝ => x + -s)
    (measurePreserving_add_right volume (-s))

theorem rapidityShift_ae (s : ℝ) (f : Lp E 2 (volume : Measure ℝ)) :
    rapidityShift s f =ᵐ[volume] fun x => f (x + -s) :=
  Lp.coeFn_compMeasurePreserving f (measurePreserving_add_right volume (-s))

theorem rapidityShift_no_eigen (f : Lp E 2 (volume : Measure ℝ)) (h : ∀ s : ℝ, ∃ c : ℂ, ‖c‖ = 1 ∧ rapidityShift s f = c • f) : f = 0 := by
  set g : ℝ → ℝ≥0∞ := fun ξ => ‖f ξ‖ₑ ^ ((2 : ℝ≥0∞).toReal) with hg
  have hfin : ∫⁻ ξ, g ξ < ∞ :=
    lintegral_rpow_enorm_lt_top_of_eLpNorm_lt_top (p := 2) two_ne_zero ENNReal.ofNat_ne_top
      (Lp.eLpNorm_lt_top f)
  -- |f|^2 e invariante por translacao inteira, q.t.p.
  have hper : ∀ n : ℤ, (fun ξ => g (ξ + n)) =ᵐ[volume] g := by
    intro n
    obtain ⟨c, hc, hD⟩ := h (-(n : ℝ))
    have h1 := rapidityShift_ae (-(n : ℝ)) f
    rw [hD] at h1
    have h2 := Lp.coeFn_smul c f
    have hce : ‖c‖ₑ = 1 := by rw [← ofReal_norm, hc, ENNReal.ofReal_one]
    filter_upwards [h1, h2] with ξ e1 e2
    simp only [hg]
    rw [neg_neg] at e1
    rw [← e1, e2, Pi.smul_apply, enorm_smul, hce, one_mul]
  -- cada ladrilho [n, n+1) pesa o mesmo que [0, 1)
  have hpiece : ∀ n : ℤ, ∫⁻ ξ in Ico (n : ℝ) (n + 1), g ξ = ∫⁻ ξ in Ico (0 : ℝ) 1, g ξ := by
    intro n
    rw [← lintegral_indicator measurableSet_Ico, ← lintegral_indicator measurableSet_Ico]
    calc ∫⁻ ξ, (Ico (n : ℝ) (n + 1)).indicator g ξ
        = ∫⁻ ξ, (Ico (n : ℝ) (n + 1)).indicator g (ξ + n) :=
          (lintegral_add_right_eq_self _ (n : ℝ)).symm
      _ = ∫⁻ ξ, (Ico (0 : ℝ) 1).indicator g ξ := by
          apply lintegral_congr_ae
          filter_upwards [hper n] with ξ hξ
          by_cases hm : ξ ∈ Ico (0 : ℝ) 1
          · have hm' : ξ + n ∈ Ico (n : ℝ) (n + 1) := ⟨by linarith [hm.1], by linarith [hm.2]⟩
            rw [indicator_of_mem hm', indicator_of_mem hm, hξ]
          · have hm' : ξ + n ∉ Ico (n : ℝ) (n + 1) := fun h' =>
              hm ⟨by linarith [h'.1], by linarith [h'.2]⟩
            rw [indicator_of_notMem hm', indicator_of_notMem hm]
  -- a integral total e a soma dos ladrilhos
  have htot : ∫⁻ ξ, g ξ = ∑' _n : ℤ, ∫⁻ ξ in Ico (0 : ℝ) 1, g ξ := by
    rw [← setLIntegral_univ, ← iUnion_Ico_intCast (α := ℝ),
      lintegral_iUnion (fun n => measurableSet_Ico) (pairwise_disjoint_Ico_intCast (α := ℝ)) g]
    exact tsum_congr hpiece
  have hC : ∫⁻ ξ in Ico (0 : ℝ) 1, g ξ = 0 := by
    by_contra hne
    have htop := ENNReal.tsum_const_eq_top_of_ne_zero (α := ℤ) hne
    rw [htot, htop] at hfin
    exact lt_irrefl _ hfin
  have hzero : ∫⁻ ξ, g ξ = 0 := by rw [htot, hC, tsum_zero]
  have hgm : AEMeasurable g volume :=
    ((Lp.aestronglyMeasurable f).enorm).pow_const _
  have hgae : g =ᵐ[volume] 0 := (lintegral_eq_zero_iff' hgm).mp hzero
  apply Lp.ext
  filter_upwards [hgae, Lp.coeFn_zero E 2 (volume : Measure ℝ)] with ξ hξ hz
  rw [hz]
  simp only [hg, Pi.zero_apply] at hξ
  have hpos : (0 : ℝ) < (2 : ℝ≥0∞).toReal := by norm_num
  rw [ENNReal.rpow_eq_zero_iff] at hξ
  rcases hξ with ⟨h0, _⟩ | ⟨_, hneg⟩
  · simpa using h0
  · exact absurd hneg (not_lt.mpr hpos.le)


#print axioms rapidityShift_ae
#print axioms rapidityShift_no_eigen
end ChatgptAudit.WignerRapidity016


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
