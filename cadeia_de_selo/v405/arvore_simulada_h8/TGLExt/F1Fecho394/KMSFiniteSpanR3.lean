import TGLExt.TheImportedSecondQuantization
/-! Bilinear closure of the genuine KMS strip condition. This extends a
proved generator condition to finite linear combinations, without adding an
analyticity premise to the resulting finite-algebra statement. -/
set_option autoImplicit false
set_option maxHeartbeats 1200000
noncomputable section
namespace F1Fecho.KMSFiniteSpan
open TGLExt.ContratoQGv31
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

def Pair (Ω : H) (α : ℝ → H ≃ₗᵢ[ℂ] H) (A B : H →L[ℂ] H) : Prop :=
  ∃ G : ℂ → ℂ, DiffContOnCl ℂ G (kmsStrip 1) ∧
    (∃ C : ℝ, ∀ z : ℂ, 0 ≤ z.im → z.im ≤ 1 → ‖G z‖ ≤ C) ∧
    (∀ t : ℝ, G t = inner ℂ ((star A) Ω) (α t (B Ω))) ∧
    (∀ t : ℝ, G ((t:ℂ)+Complex.I) = inner ℂ ((star B) Ω) (α (-t) (A Ω)))

variable {Ω : H} {α : ℝ → H ≃ₗᵢ[ℂ] H} {A B D : H →L[ℂ] H}

theorem zero_left (B : H →L[ℂ] H) : Pair Ω α 0 B := by
  refine ⟨0,diffContOnCl_const,⟨0,by simp⟩,?_,?_⟩ <;>
    intro t <;> simp

theorem zero_right (A : H →L[ℂ] H) : Pair Ω α A 0 := by
  refine ⟨0,diffContOnCl_const,⟨0,by simp⟩,?_,?_⟩ <;>
    intro t <;> simp

theorem add_left (hA : Pair Ω α A B) (hD : Pair Ω α D B) : Pair Ω α (A+D) B := by
  obtain ⟨G,hG,⟨CG,bG⟩,lG,uG⟩ := hA
  obtain ⟨Q,hQ,⟨CQ,bQ⟩,lQ,uQ⟩ := hD
  refine ⟨G+Q,hG.add hQ,⟨CG+CQ,?_⟩,?_,?_⟩
  · intro z h0 h1
    exact (norm_add_le _ _).trans (add_le_add (bG z h0 h1) (bQ z h0 h1))
  · intro t
    simp only [Pi.add_apply,lG,lQ,star_add,ContinuousLinearMap.add_apply,inner_add_left]
  · intro t
    simp only [Pi.add_apply,uG,uQ,ContinuousLinearMap.add_apply,map_add,inner_add_right]

theorem add_right (hB : Pair Ω α A B) (hD : Pair Ω α A D) : Pair Ω α A (B+D) := by
  obtain ⟨G,hG,⟨CG,bG⟩,lG,uG⟩ := hB
  obtain ⟨Q,hQ,⟨CQ,bQ⟩,lQ,uQ⟩ := hD
  refine ⟨G+Q,hG.add hQ,⟨CG+CQ,?_⟩,?_,?_⟩
  · intro z h0 h1
    exact (norm_add_le _ _).trans (add_le_add (bG z h0 h1) (bQ z h0 h1))
  · intro t
    simp only [Pi.add_apply,lG,lQ,ContinuousLinearMap.add_apply,map_add,inner_add_right]
  · intro t
    simp only [Pi.add_apply,uG,uQ,star_add,ContinuousLinearMap.add_apply,inner_add_left]

theorem smul_left (c : ℂ) (hA : Pair Ω α A B) : Pair Ω α (c • A) B := by
  obtain ⟨G,hG,⟨C,bG⟩,lG,uG⟩ := hA
  refine ⟨c • G,hG.const_smul c,⟨‖c‖*C,?_⟩,?_,?_⟩
  · intro z h0 h1
    simpa only [Pi.smul_apply,norm_smul] using mul_le_mul_of_nonneg_left (bG z h0 h1) (norm_nonneg c)
  · intro t
    simp only [Pi.smul_apply,lG,star_smul,ContinuousLinearMap.smul_apply,inner_smul_left,starRingEnd_apply,star_star,smul_eq_mul]
  · intro t
    simp only [Pi.smul_apply,uG,ContinuousLinearMap.smul_apply,map_smul,inner_smul_right,smul_eq_mul]

theorem smul_right (c : ℂ) (hB : Pair Ω α A B) : Pair Ω α A (c • B) := by
  obtain ⟨G,hG,⟨C,bG⟩,lG,uG⟩ := hB
  refine ⟨c • G,hG.const_smul c,⟨‖c‖*C,?_⟩,?_,?_⟩
  · intro z h0 h1
    simpa only [Pi.smul_apply,norm_smul] using mul_le_mul_of_nonneg_left (bG z h0 h1) (norm_nonneg c)
  · intro t
    simp only [Pi.smul_apply,lG,ContinuousLinearMap.smul_apply,map_smul,inner_smul_right,smul_eq_mul]
  · intro t
    simp only [Pi.smul_apply,uG,star_smul,ContinuousLinearMap.smul_apply,inner_smul_left,starRingEnd_apply,star_star,smul_eq_mul]

theorem span_pair (S : Set (H →L[ℂ] H))
    (h : ∀ A ∈ S, ∀ B ∈ S, Pair Ω α A B)
    (A B : H →L[ℂ] H) (hA : A ∈ Submodule.span ℂ S) (hB : B ∈ Submodule.span ℂ S) :
    Pair Ω α A B := by
  have hg : ∀ a ∈ S, Pair Ω α a B := by
    intro a ha
    induction hB using Submodule.span_induction with
    | mem b hb => exact h a ha b hb
    | zero => exact zero_right a
    | add b c hb hc ihb ihc => exact add_right ihb ihc
    | smul c b hb ih => exact smul_right c ih
  induction hA using Submodule.span_induction with
  | mem a ha => exact hg a ha
  | zero => exact zero_left B
  | add a c ha hc iha ihc => exact add_left iha ihc
  | smul c a ha ih => exact smul_left c ih

end F1Fecho.KMSFiniteSpan

open Lean in
run_cmd do
  let env ← Elab.Command.liftCoreM getEnv
  for (n, ci) in env.constants.map₂.toList do
    if (`F1Fecho.KMSFiniteSpan).isPrefixOf n then
      let axs ← collectAxioms n
      IO.println ("LOCAL_DECL\t" ++ n.toString ++ "\t" ++ String.intercalate "," (axs.toList.map Name.toString))
      unless axs.all (fun a => a == `propext || a == `Classical.choice || a == `Quot.sound) do
        throwError "AXIOM_AUDIT_REFUSED: {n}"
      match ci with
      | .axiomInfo _ => throwError "LOCAL_AXIOM_REFUSED: {n}"
      | _ => pure ()
