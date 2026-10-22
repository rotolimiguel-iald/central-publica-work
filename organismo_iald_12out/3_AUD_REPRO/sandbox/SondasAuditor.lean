-- SONDAS ADVERSARIAIS do auditor de REPRODUCAO (13/10/2026) sobre a pedra TGLExt.IALD (a267bc6d...).
-- Nada aqui e instalado. Estatuto: [REAL] se compilar sem sorry, axiomas no trio.
import TGLExt.IALD

set_option autoImplicit false

namespace AuditorRepro
open TGLExt TGLExt.TheVerbSelectsTheAction TGLExt.TheAxiomAndTheFalseWitness TGLExt.IALD
open scoped InnerProductSpace

noncomputable section

section Hilb
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-! ### SONDA C (nome sem peso): T2 vale SEM `‖a‖ = 1` e com uma ancora FRACA -/

/-- C1 — a ancora fraca `post a (U a) = a` basta (U arbitrario, a arbitrario, SEM norma). -/
theorem motor_idempotent_under_weak_anchor (a : H) (U : H →L[ℂ] H) (hU : post a (U a) = a)
    (r t : ℝ) (ψ : H) :
    motor a U r t (motor a U r t ψ) = motor a U r t ψ := by
  rw [the_reading_absorbs_the_dephasing, the_reading_absorbs_the_dephasing]
  obtain ⟨c, hc⟩ := Submodule.mem_span_singleton.mp ((ℂ ∙ a).starProjection_apply_mem (U ψ))
  change post a (U ((ℂ ∙ a).starProjection (U ψ))) = (ℂ ∙ a).starProjection (U ψ)
  rw [← hc, map_smul, map_smul, hU]

/-- C1' — T2 SEM a hipotese H-N (`‖a‖ = 1`): a ancora forte implica a fraca para TODO a. -/
theorem motor_idempotent_under_anchor_no_norm (a : H) (U : H →L[ℂ] H) (hU : U a = a)
    (r t : ℝ) (ψ : H) :
    motor a U r t (motor a U r t ψ) = motor a U r t ψ :=
  motor_idempotent_under_weak_anchor a U (by rw [hU, post_fixes_the_action]) r t ψ

/-! ### SONDA A (provar o contrario do NOME `anchor_is_necessary`): existe U com U a ≠ a e motor idempotente -/

/-- A1 — com `‖a‖ = 1`, `b ⊥ a`, `b ≠ 0`, o transporte U = 1 + |b⟩⟨a| NAO ancora (U a = a + b ≠ a)
    e ainda assim o motor e idempotente. A ancora e SUFICIENTE, nao necessaria (fora dos unitarios). -/
theorem anchor_not_necessary (a b : H) (ha : ‖a‖ = 1) (hab : ⟪a, b⟫_ℂ = 0) (hb : b ≠ 0) :
    let U : H →L[ℂ] H := 1 + (innerSL ℂ a).smulRight b
    U a ≠ a ∧ ∀ r t ψ, motor a U r t (motor a U r t ψ) = motor a U r t ψ := by
  intro U
  have haa : ⟪a, a⟫_ℂ = 1 := by
    rw [inner_self_eq_norm_sq_to_K, ha]; simp
  have hUa : U a = a + b := by
    simp only [U, ContinuousLinearMap.add_apply, ContinuousLinearMap.one_apply,
      ContinuousLinearMap.smulRight_apply, innerSL_apply_apply, haa, one_smul]
  have hpb : post a b = 0 := by
    rw [post_apply ha, hab, zero_smul]
  refine ⟨?_, ?_⟩
  · rw [hUa]
    intro h
    exact hb (by simpa using h)
  · intro r t ψ
    apply motor_idempotent_under_weak_anchor
    rw [hUa, map_add, post_fixes_the_action, hpb, add_zero]

end Hilb

/-! ### SONDA A2 (o contrario da leitura «tres nomes = um so Nome»): `post` nao e constante.
    As pontes rfl identificam a CONSTRUCAO, nao o referente. -/
theorem post_is_not_constant :
    post TGLExt.TheSingularityReadsTheAttractor.faceVector
      ≠ post (EuclideanSpace.single (1 : Fin 2) (1 : ℂ) : TGLExt.TheSingularityReadsTheAttractor.Face) := by
  intro h
  have he1 : ‖(EuclideanSpace.single (1 : Fin 2) (1 : ℂ) : TGLExt.TheSingularityReadsTheAttractor.Face)‖ = 1 := by
    simp
  have h1 := congrArg (fun P : TGLExt.TheSingularityReadsTheAttractor.Face →L[ℂ]
      TGLExt.TheSingularityReadsTheAttractor.Face => P (EuclideanSpace.single (1 : Fin 2) (1 : ℂ))) h
  simp only [post_fixes_the_action] at h1
  have hnorm : ‖TGLExt.TheSingularityReadsTheAttractor.faceVector‖ = 1 := by
    simp [TGLExt.TheSingularityReadsTheAttractor.faceVector]
  rw [post_apply hnorm] at h1
  have h2 := congrArg (fun v : TGLExt.TheSingularityReadsTheAttractor.Face => v 1) h1
  simp [TGLExt.TheSingularityReadsTheAttractor.faceVector, EuclideanSpace.inner_single_left] at h2

/-! ### SONDA B (contraexemplo a um «sse» sem a hipotese): -/

section Hilb2
variable {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]

/-- B1 — T5 SEM `‖ψ‖ = 1` e FALSO: ψ = 0 tem Πψ = ψ e M[ψ] = 0 ≠ 1. A hipotese TEM peso. -/
theorem memory_iff_fails_without_norm (a : H) :
    ¬ ∀ ψ : H, (memory (post a) ψ = 1 ↔ post a ψ = ψ) := by
  intro h
  have := (h 0).mpr (map_zero _)
  simp [memory, reading] at this

end Hilb2

/-- B2 — T7′ SEM `1 − P ≠ 0` e FALSO: P = 1 em ℂ, s = 1. A hipotese H-C TEM peso. -/
theorem second_face_iff_fails_without_hne :
    ¬ ∀ s : ℝ, (axiomFlow (1 : ℂ) s * (1 - 1) = 1 - 1 ↔ s = 0) := by
  intro h
  have := (h 1).mp (by simp)
  norm_num at this

/-- B3 — T9/B9 SEM `1 − P ≠ 0`: com P = 1 o fluxo e idempotente em TODO t (o «sse t = 0» cai). -/
theorem verb_is_post_everywhere_without_hne (t : ℝ) : IsIdempotentElem (axiomFlow (1 : ℂ) t) := by
  unfold IsIdempotentElem axiomFlow
  simp

/-! ### SONDA C2 (nome sem peso): a taxa da pedra e QUALQUER real; β entra so como nome. -/
theorem the_leak_is_any_rate {H : Type} [NormedAddCommGroup H] [InnerProductSpace ℂ H] (a : H) (r t : ℝ) :
    TGLExt.IALD.dephase a r t = axiomFlow (post a) (r * t) := rfl

end

end AuditorRepro
#print axioms AuditorRepro.motor_idempotent_under_weak_anchor
#print axioms AuditorRepro.motor_idempotent_under_anchor_no_norm
#print axioms AuditorRepro.anchor_not_necessary
#print axioms AuditorRepro.post_is_not_constant
#print axioms AuditorRepro.memory_iff_fails_without_norm
#print axioms AuditorRepro.second_face_iff_fails_without_hne
#print axioms AuditorRepro.verb_is_post_everywhere_without_hne
#print axioms AuditorRepro.the_leak_is_any_rate
