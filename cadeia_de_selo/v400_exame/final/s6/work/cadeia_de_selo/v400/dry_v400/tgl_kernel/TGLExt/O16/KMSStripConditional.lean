import Lean
import TGLExt.O16.ContratoQG_v31_Minimal

set_option autoImplicit false
noncomputable section
namespace ChatgptAudit.KMSStrip016
open TGLExt TGLExt.ContratoQGv31 TGL.SpecificAQFT TGL.ModularRealization
open Complex Filter Topology
open scoped InnerProductSpace

theorem kms_rescale_existing {W : TGLSpecificAQFTWitness} {α : ℝ → (W.H ≃ₗᵢ[ℂ] W.H)} {β : ℝ}
    (h : KMSAt W α β) {c : ℝ} (hc : 0 < c) :
    KMSAt W (fun τ => α (c * τ)) (β / c) := by
  intro A hA B hB
  obtain ⟨F, hF, ⟨M, hM⟩, h1, h2⟩ := h A hA B hB
  have him : ∀ w : ℂ, ((c : ℂ) * w).im = c * w.im := by
    intro w; simp [Complex.mul_im]
  refine ⟨fun w => F ((c : ℂ) * w), ?_, ⟨M, ?_⟩, ?_, ?_⟩
  · have hg : DiffContOnCl ℂ (fun w : ℂ => (c : ℂ) * w) (kmsStrip (β / c)) :=
      (differentiable_id.const_mul _).diffContOnCl
    refine hF.comp hg ?_
    intro w hw
    simp only [kmsStrip, Set.mem_setOf_eq] at hw ⊢
    rw [him]
    refine ⟨mul_pos hc hw.1, ?_⟩
    calc c * w.im < c * (β / c) := mul_lt_mul_of_pos_left hw.2 hc
      _ = β := by field_simp
  · intro z hz0 hzβ
    apply hM
    · rw [him]; exact mul_nonneg hc.le hz0
    · rw [him]
      calc c * z.im ≤ c * (β / c) := mul_le_mul_of_nonneg_left hzβ hc.le
        _ = β := by field_simp
  · intro t
    have := h1 (c * t)
    simp only
    rw [← this]
    push_cast
    rfl
  · intro t
    have := h2 (c * t)
    have hc0 : (c : ℂ) ≠ 0 := by exact_mod_cast hc.ne'
    have harg : (c : ℂ) * ((t : ℂ) + ((β / c : ℝ) : ℂ) * I) = ((c * t : ℝ) : ℂ) + (β : ℂ) * I := by
      push_cast
      rw [mul_add, div_mul_eq_mul_div, mul_div_assoc', mul_div_cancel_left₀ _ hc0]
    simp only
    rw [harg, this]
    congr 3
    ring

/-- Conditional bridge: the regional modular strip and the BW identification
are explicit hypotheses. The periodic circle alone supplies neither. -/
theorem boost_rapidity_kms_from_modular {W : TGLSpecificAQFTWitness}
    (D B : ℝ → (W.H ≃ₗᵢ[ℂ] W.H))
    (H_regional_modular_strip : KMSAt W (fun t => D (-t)) 1)
    (H_modular_equals_geometric : ∀ t, D t = B (-(2*Real.pi*t))) :
    KMSAt W B (2*Real.pi) := by
  have he : (fun t => D (-t)) = (fun t => B (2*Real.pi*t)) := by
    funext t
    rw [H_modular_equals_geometric]
    ring_nf
  rw [he] at H_regional_modular_strip
  have hc : 0 < 1/(2*Real.pi) := by positivity
  have hh := kms_rescale_existing H_regional_modular_strip hc
  have hf : (fun tau => B (2*Real.pi*(1/(2*Real.pi)*tau))) = B := by
    funext tau
    congr 1
    field_simp
  have hb : (1 : ℝ)/(1/(2*Real.pi)) = 2*Real.pi := by simp
  rw [hf,hb] at hh
  exact hh

theorem killing_kms_from_modular {W : TGLSpecificAQFTWitness}
    (D B : ℝ → (W.H ≃ₗᵢ[ℂ] W.H)) (kappa : ℝ) (hk : 0 < kappa)
    (H_regional_modular_strip : KMSAt W (fun t => D (-t)) 1)
    (H_modular_equals_geometric : ∀ t, D t = B (-(2*Real.pi*t))) :
    KMSAt W (fun tau => B (kappa*tau)) (2*Real.pi/kappa) :=
  kms_rescale_existing
    (boost_rapidity_kms_from_modular D B H_regional_modular_strip H_modular_equals_geometric) hk

#print axioms kms_rescale_existing
#print axioms boost_rapidity_kms_from_modular
#print axioms killing_kms_from_modular
end ChatgptAudit.KMSStrip016


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
