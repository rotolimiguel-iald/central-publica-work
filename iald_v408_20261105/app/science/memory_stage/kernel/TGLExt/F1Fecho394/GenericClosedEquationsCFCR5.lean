import Mathlib.Analysis.CStarAlgebra.ContinuousLinearMap
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Basic
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Instances
import Mathlib.Analysis.CStarAlgebra.ContinuousFunctionalCalculus.Range
import Mathlib.Analysis.InnerProductSpace.Adjoint

/-! Closed equations and CFC in an ambient closed star subalgebra, established
before substituting the concrete GNS carrier. All closedness is explicit. -/
set_option autoImplicit false
noncomputable section
namespace F1Fecho.GenericClosedEquationsCFC

theorem isClosed_of_equations {X Y I N : Type*}
    [TopologicalSpace X] [TopologicalSpace Y] [T2Space Y]
    (P : X → Prop) (f g : I → N → X → Y)
    (he : ∀ x, P x ↔ ∀ i n, f i n x = g i n x)
    (hf : ∀ i n, Continuous (f i n)) (hg : ∀ i n, Continuous (g i n)) :
    IsClosed {x | P x} := by
  have hset : {x | P x} = ⋂ i, ⋂ n, {x | f i n x = g i n x} := by
    ext x
    simpa only [Set.mem_iInter,Set.mem_setOf_eq] using he x
  rw [hset]
  exact isClosed_iInter (fun i => isClosed_iInter (fun n => isClosed_eq (hf i n) (hg i n)))

variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

theorem closed_subalgebra_cfc (N : StarSubalgebra ℂ (H →L[ℂ] H))
    (hN : IsClosed (N : Set (H →L[ℂ] H)))
    (B : StarSubalgebra ℂ N) (hB : IsClosed (B : Set N))
    (b : N) (hb : b ∈ B) (f : ℂ → ℂ) :
    ∃ hf : cfc f b.val ∈ N, (⟨cfc f b.val,hf⟩ : N) ∈ B := by
  let E := B.map N.subtype
  have hE : IsClosed (E : Set (H →L[ℂ] H)) := hN.isClosedMap_subtype_val _ hB
  letI := hE
  have hbE : b.val ∈ E := ⟨b,hb,rfl⟩
  have hc : cfc f b.val ∈ E := cfc_mem (𝕜' := ℂ) f hbE
  obtain ⟨d,hd,he⟩ := hc
  have hm : cfc f b.val ∈ N := he ▸ d.property
  refine ⟨hm,?_⟩
  have heq : d = (⟨cfc f b.val,hm⟩ : N) := Subtype.ext he
  exact heq ▸ hd


theorem continuous_left_mul (A : H →L[ℂ] H) :
    Continuous (fun B : H →L[ℂ] H => A*B) := by fun_prop

theorem closed_subalgebra_cfc_of_eq (N : StarSubalgebra ℂ (H →L[ℂ] H))
    (hN : IsClosed (N : Set (H →L[ℂ] H)))
    (B : StarSubalgebra ℂ N) (hB : IsClosed (B : Set N))
    (b : N) (hb : b ∈ B) (f : ℂ → ℂ) (c : H →L[ℂ] H)
    (he : c = cfc f b.val) :
    ∃ hc : c ∈ N, (⟨c,hc⟩ : N) ∈ B := by
  rw [he]
  exact closed_subalgebra_cfc N hN B hB b hb f

theorem closed_subalgebra_mem_of_eq_cfc (N : StarSubalgebra ℂ (H →L[ℂ] H))
    (hN : IsClosed (N : Set (H →L[ℂ] H)))
    (B : StarSubalgebra ℂ N) (hB : IsClosed (B : Set N))
    (b : N) (hb : b ∈ B) (f : ℂ → ℂ) (c : N)
    (he : c.val = cfc f b.val) : c ∈ B := by
  obtain ⟨hc,hm⟩ := closed_subalgebra_cfc_of_eq N hN B hB b hb f c.val he
  exact hm

end F1Fecho.GenericClosedEquationsCFC
#print axioms F1Fecho.GenericClosedEquationsCFC.isClosed_of_equations
#print axioms F1Fecho.GenericClosedEquationsCFC.closed_subalgebra_cfc

#print axioms F1Fecho.GenericClosedEquationsCFC.continuous_left_mul
#print axioms F1Fecho.GenericClosedEquationsCFC.closed_subalgebra_cfc_of_eq
#print axioms F1Fecho.GenericClosedEquationsCFC.closed_subalgebra_mem_of_eq_cfc
