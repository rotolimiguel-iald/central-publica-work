import Lean
import TGLExt.O16.OrbitalBoostTransport
import TGLExt.O16.VectorRapiditySpectrum

set_option autoImplicit false
set_option maxHeartbeats 1000000
noncomputable section
open MeasureTheory Filter Set
open scoped ENNReal
namespace ChatgptAudit.WignerRapidityMeasure016

/-- Existing integer-tile argument, factored out without changing its proof. -/
theorem integer_periodic_lintegral_zero (g : ℝ → ℝ≥0∞)
    (hfin : ∫⁻ x, g x < ∞)
    (hper : ∀ n : ℤ, (fun x => g (x+n)) =ᵐ[volume] g) : ∫⁻ x, g x = 0 := by
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
  exact hzero

variable {E : Type*} [NormedAddCommGroup E] [NormedSpace ℂ E]

theorem product_norm_periodic_zero (f : Lp E 2 momentumMeasure)
    (hper : ∀ n : ℤ,
      (fun y : MomentumCoordinates => ‖f (y.1,y.2+n)‖ₑ) =ᵐ[momentumMeasure]
        (fun y => ‖f y‖ₑ)) : f=0 := by
  let F : MomentumCoordinates → ℝ≥0∞ := fun y => ‖f y‖ₑ ^ ((2 : ℝ≥0∞).toReal)
  have hFm : AEMeasurable F momentumMeasure :=
    ((Lp.aestronglyMeasurable f).enorm).pow_const _
  have hfin : ∫⁻ y, F y ∂momentumMeasure < ∞ :=
    lintegral_rpow_enorm_lt_top_of_eLpNorm_lt_top (p := 2) two_ne_zero ENNReal.ofNat_ne_top
      (Lp.eLpNorm_lt_top f)
  let g : ℝ → ℝ≥0∞ := fun x => ∫⁻ q : Transverse, F (q,x)
  have htonelli : (∫⁻ y, F y ∂momentumMeasure) = ∫⁻ x, g x :=
    lintegral_prod_symm F hFm
  have hgf : ∫⁻ x, g x < ∞ := by rw [← htonelli]; exact hfin
  have hgp : ∀ n : ℤ, (fun x => g (x+n)) =ᵐ[volume] g := by
    intro n
    have hn := (Measure.measurePreserving_swap (μ := (volume : Measure ℝ))
      (ν := (volume : Measure Transverse))).quasiMeasurePreserving.ae (hper n)
    have hna := Measure.ae_ae_of_ae_prod hn
    filter_upwards [hna] with x hx
    apply lintegral_congr_ae
    filter_upwards [hx] with q hq
    exact congrArg (fun z : ℝ≥0∞ => z ^ ((2 : ℝ≥0∞).toReal)) hq
  have hz : ∫⁻ y, F y ∂momentumMeasure = 0 :=
    htonelli.trans (integer_periodic_lintegral_zero g hgf hgp)
  have hzae : F =ᵐ[momentumMeasure] 0 := (lintegral_eq_zero_iff' hFm).mp hz
  apply Lp.ext
  filter_upwards [hzae, Lp.coeFn_zero E 2 momentumMeasure] with y hy hzero
  rw [hzero]
  change ‖f y‖ₑ ^ ((2 : ℝ≥0∞).toReal) = 0 at hy
  have hpos : (0 : ℝ) < (2 : ℝ≥0∞).toReal := by norm_num
  rw [ENNReal.rpow_eq_zero_iff] at hy
  rcases hy with ⟨h0,_⟩ | ⟨_,hneg⟩
  · simpa using h0
  · exact absurd hneg (not_lt.mpr hpos.le)

theorem productRapidityShift_no_eigen (f : Lp E 2 momentumMeasure)
    (h : ∀ s : ℝ, ∃ c : ℂ, ‖c‖=1 ∧ productRapidityShift s f = c • f) : f=0 := by
  apply product_norm_periodic_zero f
  intro n
  obtain ⟨c,hc,he⟩ := h (-(n : ℝ))
  have h1 := productRapidityShift_ae (-(n : ℝ)) f
  rw [he] at h1
  have h2 := Lp.coeFn_smul c f
  have hce : ‖c‖ₑ=1 := by rw [← ofReal_norm, hc, ENNReal.ofReal_one]
  filter_upwards [h1,h2] with y e1 e2
  simp only [coordinateShift, neg_neg] at e1
  rw [← e1, e2, Pi.smul_apply, enorm_smul, hce, one_mul]

theorem orbitalScalarBoost_no_eigen (m : ℝ) (f : Lp E 2 (orbitalMeasure m))
    (h : ∀ s : ℝ, ∃ c : ℂ, ‖c‖=1 ∧ orbitalScalarBoost m s f = c • f) : f=0 := by
  have hz : orbitalL2Pullback m f = 0 := by
    apply productRapidityShift_no_eigen
    intro s
    obtain ⟨c,hc,he⟩ := h s
    refine ⟨c,hc,?_⟩
    rw [← orbitalScalarBoost_intertwines, he, map_smul]
  apply (orbitalL2Pullback m).injective
  simpa using hz

#print axioms integer_periodic_lintegral_zero
#print axioms product_norm_periodic_zero
#print axioms productRapidityShift_no_eigen
#print axioms orbitalScalarBoost_no_eigen
end ChatgptAudit.WignerRapidityMeasure016


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
