import Mathlib

set_option autoImplicit false

/-!
# Canto continuo abstrato   [KERNEL/CONDITIONAL ON EXPLICIT WITNESS]

NAO se implementa Tomita--Takesaki aqui. Define-se uma INTERFACE minima como uma
`structure` cujos campos sao as hipoteses (nenhum axioma global). Os teoremas sao
incondicionais como LOGICA: para toda testemunha que satisfaz os campos, a
conclusao segue. Mas NAO provam que a testemunha existe.
-/

namespace TGL.ContinuousCorner

/-- Testemunha abstrata do canto continuo: core (anel com estrela), traco em
    `ℝ≥0∞`, projetor `P` auto-adjunto idempotente partido em duas faces
    ortogonais de traco igual, com `trace P` positivo e finito.
    As HIPOTESES sao CAMPOS -- nunca axiomas globais. -/
structure ContinuousCornerWitness where
  Core : Type
  [instRing : Ring Core]
  [instStar : StarRing Core]
  P : Core
  Pplus : Core
  Pminus : Core
  trace : Core → ENNReal
  P_selfAdjoint : star P = P
  P_idempotent : P * P = P
  Pplus_selfAdjoint : star Pplus = Pplus
  Pplus_idempotent : Pplus * Pplus = Pplus
  Pminus_selfAdjoint : star Pminus = Pminus
  Pminus_idempotent : Pminus * Pminus = Pminus
  split : Pplus + Pminus = P
  orthogonal : Pplus * Pminus = 0
  trace_additive_on_split : trace P = trace Pplus + trace Pminus
  trace_P_pos : 0 < trace P
  trace_P_finite : trace P < ⊤
  equal_face_trace : trace Pplus = trace Pminus

namespace ContinuousCornerWitness

variable (W : ContinuousCornerWitness)

/-- Traco normalizado: `trace X / trace P`. -/
noncomputable def normalizedTrace (X : W.Core) : ENNReal := W.trace X / W.trace W.P

/-- `normalizedTrace(P) = 1` (traco de `P` sobre traco de `P`, positivo e finito). -/
theorem normalizedTrace_P_eq_one : W.normalizedTrace W.P = 1 := by
  unfold normalizedTrace
  exact ENNReal.div_self W.trace_P_pos.ne' W.trace_P_finite.ne

/-- Fato auxiliar em `ℝ≥0∞`: `a/(2a) = 1/2` para `a ≠ 0`, `a ≠ ⊤`. -/
private theorem enn_self_div_two_self (a : ENNReal) (ha0 : a ≠ 0) (hat : a ≠ ⊤) :
    a / (2 * a) = 1 / 2 := by
  have h2 : (2 : ENNReal) ≠ 0 := by norm_num
  have h2t : (2 : ENNReal) ≠ ⊤ := by norm_num
  rw [div_eq_mul_inv, ENNReal.mul_inv (Or.inl h2) (Or.inl h2t)]
  calc a * ((2 : ENNReal)⁻¹ * a⁻¹) = (2 : ENNReal)⁻¹ * (a * a⁻¹) := by ring
    _ = (2 : ENNReal)⁻¹ * 1 := by rw [ENNReal.mul_inv_cancel ha0 hat]
    _ = 1 / 2 := by rw [mul_one, one_div]

/-- As duas faces conjugadas tem traco normalizado `1/2`. -/
theorem equalFaces_normalizedTrace_half :
    W.normalizedTrace W.Pplus = 1 / 2 ∧ W.normalizedTrace W.Pminus = 1 / 2 := by
  have hsum_top : W.trace W.Pplus + W.trace W.Pminus < ⊤ := by
    rw [← W.trace_additive_on_split]; exact W.trace_P_finite
  have hplus_top : W.trace W.Pplus ≠ ⊤ := (ENNReal.add_lt_top.mp hsum_top).1.ne
  have hminus_top : W.trace W.Pminus ≠ ⊤ := (ENNReal.add_lt_top.mp hsum_top).2.ne
  have hP2 : W.trace W.P = 2 * W.trace W.Pplus := by
    rw [W.trace_additive_on_split, W.equal_face_trace]; ring
  have hplus_ne : W.trace W.Pplus ≠ 0 := by
    intro h0
    have hz : W.trace W.P = 0 := by rw [hP2, h0, mul_zero]
    exact W.trace_P_pos.ne' hz
  have hminus_ne : W.trace W.Pminus ≠ 0 := by
    rw [← W.equal_face_trace]; exact hplus_ne
  have hPm : W.trace W.P = 2 * W.trace W.Pminus := by
    rw [W.trace_additive_on_split, ← W.equal_face_trace]; ring
  refine ⟨?_, ?_⟩
  · unfold normalizedTrace; rw [hP2]; exact enn_self_div_two_self _ hplus_ne hplus_top
  · unfold normalizedTrace; rw [hPm]; exact enn_self_div_two_self _ hminus_ne hminus_top

end ContinuousCornerWitness

end TGL.ContinuousCorner
