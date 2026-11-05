import Lean
import TGLExt.O16.ContratoQG_v31_Minimal
import TGLExt.O16.AnalyticBoundaryControl_v2

set_option autoImplicit false
set_option maxHeartbeats 1000000

namespace ChatgptAudit.PositiveEnergyProbe
open Complex Set MeasureTheory
open TGL.SpecificAQFT TGLExt.ContratoQGv31 ChatgptAudit.AnalyticBoundary
open scoped InnerProductSpace
noncomputable section

theorem bounded_upper_extension_unique_negative_phase {F : ℂ → ℂ}
    (hd : DiffContOnCl ℂ F upperHalf)
    (hM : ∃ M : ℝ, ∀ z : ℂ, 0 ≤ z.im → ‖F z‖ ≤ M)
    (hedge : ∀ t : ℝ, F t = Complex.exp (-I * (t : ℂ)))
    {z : ℂ} (hz : 0 ≤ z.im) : F z = Complex.exp (-I * z) := by
  let b : ℝ := z.im + 1
  have hb : 0 < b := by dsimp [b]; linarith
  have hzb : z.im < b := by dsimp [b]; linarith
  have hdiff : DiffContOnCl ℂ (fun w : ℂ => F w - Complex.exp (-I * w))
      {w : ℂ | 0 < w.im ∧ w.im < b} := by
    exact (hd.mono (fun w hw => hw.1)).sub
      (differentiable_id.const_mul (-I)).cexp.diffContOnCl
  have hbound : ∃ M : ℝ, ∀ w : ℂ, 0 ≤ w.im → w.im ≤ b →
      ‖F w - Complex.exp (-I * w)‖ ≤ M := by
    obtain ⟨M, hM⟩ := hM
    refine ⟨M + Real.exp b, ?_⟩
    intro w hw0 hwb
    apply (norm_sub_le _ _).trans
    apply add_le_add (hM w hw0)
    rw [Complex.norm_exp]
    apply Real.exp_le_exp.mpr
    simpa [mul_re] using hwb
  have hzero : ∀ w : ℂ, w.im = 0 → F w - Complex.exp (-I * w) = 0 := by
    intro w hw
    have he : w = (w.re : ℂ) := by apply Complex.ext <;> simp [hw]
    rw [he, hedge]
    exact sub_self _
  exact sub_eq_zero.mp (horizontal_zero_of_zero_edge hb hdiff hbound hzero hz hzb)

theorem negative_phase_has_no_bounded_upper_extension :
    ¬ ∃ F : ℂ → ℂ, DiffContOnCl ℂ F upperHalf ∧
      (∃ M : ℝ, ∀ z : ℂ, 0 ≤ z.im → ‖F z‖ ≤ M) ∧
      (∀ t : ℝ, F t = Complex.exp (-I * (t : ℂ))) := by
  rintro ⟨F, hd, hbound, hedge⟩
  obtain ⟨M, hM⟩ := hbound
  let y : ℝ := max M 0 + 1
  have hy : 0 ≤ y := by dsimp [y]; have := le_max_right M 0; linarith
  have hm := hM ((y : ℂ) * I) (by simpa using hy)
  rw [bounded_upper_extension_unique_negative_phase hd ⟨M, hM⟩ hedge
    (by simpa using hy), Complex.norm_exp] at hm
  have he : (-I * ((y : ℂ) * I)).re = y := by simp [mul_re, mul_im]
  rw [he] at hm
  have hexy := Real.add_one_le_exp y
  have hMy : M < y := by dsimp [y]; have := le_max_left M 0; linarith
  linarith

/-- A genuine consumer of the PositiveEnergy field; the eigenmode assumption is explicit. -/
theorem positive_energy_excludes_negative_unit_mode
    (W : TGLSpecificAQFTWitness) (hE : PositiveEnergy W)
    (a : Fin 4 → ℝ) (ha : a ∈ forwardCone) (ψ : W.H) (hψ : ‖ψ‖ = 1)
    (hmode : ∀ t : ℝ, W.U (t • a) ψ = Complex.exp (-I * (t : ℂ)) • ψ) : False := by
  obtain ⟨F, hd, hM, hboundary⟩ := hE a ha ψ
  apply negative_phase_has_no_bounded_upper_extension
  refine ⟨F, hd, hM, ?_⟩
  intro t
  rw [hboundary, hmode]
  simp [inner_smul_right, inner_self_eq_norm_sq_to_K, hψ]

#print axioms bounded_upper_extension_unique_negative_phase
#print axioms negative_phase_has_no_bounded_upper_extension
#print axioms positive_energy_excludes_negative_unit_mode
end
end ChatgptAudit.PositiveEnergyProbe


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
