import Mathlib.Data.Set.Basic
/-! Abstract cut recognition, isolating logical witness handling from the
large concrete Fock carrier. Recovery remains an explicit premise. -/
set_option autoImplicit false
namespace F1Fecho.GenericCutRecognition
variable {A B H E : Type}
theorem forall_embedding_iff_cuts
    (L : A → Prop) (embedding : Subtype L → H)
    (cut : ℕ → H → E) (action : ℕ → A → E)
    (he : ∀ n (a : Subtype L), cut n (embedding a) = action n a)
    (hr : ∀ a v, (∀ n, cut n v = action n a) → ∃ ha : L a, embedding ⟨a,ha⟩ = v)
    (product : B → A) (read : B → H) :
    (∀ b, ∃ ha : L (product b), embedding ⟨product b,ha⟩ = read b) ↔
      ∀ b n, cut n (read b) = action n (product b) := by
  constructor
  · intro h b n
    obtain ⟨ha,hv⟩ := h b
    exact (congrArg (cut n) hv).symm.trans (he n ⟨product b,ha⟩)
  · intro h b
    exact hr (product b) (read b) (h b)
end F1Fecho.GenericCutRecognition
#print axioms F1Fecho.GenericCutRecognition.forall_embedding_iff_cuts
