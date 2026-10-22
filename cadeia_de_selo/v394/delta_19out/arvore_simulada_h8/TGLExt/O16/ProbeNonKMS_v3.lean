import Lean
import TGLExt.O16.ContratoQG_v31_Minimal
import TGLExt.O16.AnalyticBoundaryControl_v2

set_option autoImplicit false
set_option maxHeartbeats 1000000

namespace ChatgptAudit.NonKMSProbe
open Complex Set
open TGL.SpecificAQFT TGLExt.ContratoQGv31 ChatgptAudit.AnalyticBoundary
open scoped InnerProductSpace
noncomputable section

theorem horizontal_zero_on_closed_strip {f : ℂ → ℂ} {b : ℝ} (hb : 0 < b)
    (hd : DiffContOnCl ℂ f {z : ℂ | 0 < z.im ∧ z.im < b})
    (hbound : ∃ M : ℝ, ∀ z : ℂ, 0 ≤ z.im → z.im ≤ b → ‖f z‖ ≤ M)
    (hedge : ∀ z : ℂ, z.im = 0 → f z = 0)
    {z : ℂ} (hz0 : 0 ≤ z.im) (hzb : z.im ≤ b) : f z = 0 := by
  have heq : EqOn f (fun _ => 0) {z : ℂ | 0 < z.im ∧ z.im < b} := by
    intro w hw
    exact horizontal_zero_of_zero_edge hb hd hbound hedge hw.1.le hw.2
  have hclosed := heq.of_subset_closure hd.continuousOn continuousOn_const
    subset_closure (by intro w hw; exact hw)
  apply hclosed
  change z ∈ closure (Complex.im ⁻¹' Ioo 0 b)
  rw [Complex.closure_preimage_im, closure_Ioo hb.ne]
  exact ⟨hz0, hzb⟩

theorem identity_kms_forces_tracial_boundary (W : TGLSpecificAQFTWitness)
    (hkms : KMSAt W (fun _ => LinearIsometryEquiv.refl ℂ W.H) 1)
    (A B : W.H →L[ℂ] W.H) (hA : A ∈ W.net rightWedge) (hB : B ∈ W.net rightWedge) :
    ⟪(star A) W.vac, B W.vac⟫_ℂ = ⟪(star B) W.vac, A W.vac⟫_ℂ := by
  obtain ⟨F, hd, hM, hlo, hhi⟩ := hkms A hA B hB
  let c : ℂ := ⟪(star A) W.vac, B W.vac⟫_ℂ
  have hbnd : ∃ M : ℝ, ∀ z : ℂ, 0 ≤ z.im → z.im ≤ 1 → ‖F z - c‖ ≤ M := by
    obtain ⟨M, hM⟩ := hM
    exact ⟨M + ‖c‖, fun z h0 h1 => (norm_sub_le _ _).trans (add_le_add (hM z h0 h1) (le_refl ‖c‖))⟩
  have hedge : ∀ z : ℂ, z.im = 0 → F z - c = 0 := by
    intro z hz
    have he : z = (z.re : ℂ) := by apply Complex.ext <;> simp [hz]
    rw [he, hlo]
    simp [c]
  have htop := horizontal_zero_on_closed_strip (b := 1) (by norm_num)
    (hd.sub_const c) hbnd hedge (z := I) (by simp) (by simp)
  have heq : F I = c := sub_eq_zero.mp htop
  have hu := hhi 0
  simpa [c, heq] using hu

/-- An explicit flow (identity), rejected by the actual KMSAt field when the state is nontracial. -/
theorem identity_flow_not_kms (W : TGLSpecificAQFTWitness)
    (A B : W.H →L[ℂ] W.H) (hA : A ∈ W.net rightWedge) (hB : B ∈ W.net rightWedge)
    (hcontrast : ⟪(star A) W.vac, B W.vac⟫_ℂ ≠ ⟪(star B) W.vac, A W.vac⟫_ℂ) :
    ¬ KMSAt W (fun _ => LinearIsometryEquiv.refl ℂ W.H) 1 := by
  intro hkms
  exact hcontrast (identity_kms_forces_tracial_boundary W hkms A B hA hB)

#print axioms horizontal_zero_on_closed_strip
#print axioms identity_kms_forces_tracial_boundary
#print axioms identity_flow_not_kms
end
end ChatgptAudit.NonKMSProbe


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
