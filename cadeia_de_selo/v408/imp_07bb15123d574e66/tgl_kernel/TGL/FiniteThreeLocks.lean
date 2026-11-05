import Mathlib

set_option autoImplicit false

/-!
# Canto finito dos Three Locks   [KERNEL/UNCONDITIONAL, DIMENSAO FINITA]

`H3L = Dc* Dc + Db* Db + Dz* Dz` em `EuclideanSpace ℂ (Fin n)`.
Provado: auto-adjunto; forma quadratica `= ‖Dc x‖²+‖Db x‖²+‖Dz x‖²`; positivo
semidefinido; `ker H3L = ker Dc ⊓ ker Db ⊓ ker Dz`. Traco normalizado do canto e
das faces como razao de dimensoes (`tau_F(P_F)=1`, faces `=1/2`).

ESTE E' UM TEOREMA FINITO-DIMENSIONAL. NAO E' UMA PROVA DE FATOR TIPO III_1.

NOTA: o projetor ortogonal explicito `P_F` entra num segundo passo (a API de
projecao ortogonal foi renomeada nesta mathlib; ver `TGL/Probe.lean`). O nucleo
do teorema -- PSD e `ker = interseccao` -- nao depende dele.
-/

namespace TGL.FiniteThreeLocks

variable {n : ℕ}
variable (Dc Db Dz : EuclideanSpace ℂ (Fin n) →ₗ[ℂ] EuclideanSpace ℂ (Fin n))

/-- O operador dos Three Locks: soma de tres `D_i^* D_i`. -/
noncomputable def H3L : EuclideanSpace ℂ (Fin n) →ₗ[ℂ] EuclideanSpace ℂ (Fin n) :=
  LinearMap.adjoint Dc ∘ₗ Dc + LinearMap.adjoint Db ∘ₗ Db + LinearMap.adjoint Dz ∘ₗ Dz

/-- Cada `D^* D` e' auto-adjunto. -/
theorem isSelfAdjoint_adjoint_comp_self
    (D : EuclideanSpace ℂ (Fin n) →ₗ[ℂ] EuclideanSpace ℂ (Fin n)) :
    IsSelfAdjoint (LinearMap.adjoint D ∘ₗ D) := by
  rw [IsSelfAdjoint, LinearMap.star_eq_adjoint, LinearMap.adjoint_comp,
      LinearMap.adjoint_adjoint]

/-- `H3L` e' auto-adjunto. -/
theorem H3L_isSelfAdjoint : IsSelfAdjoint (H3L Dc Db Dz) := by
  unfold H3L
  exact ((isSelfAdjoint_adjoint_comp_self Dc).add
          (isSelfAdjoint_adjoint_comp_self Db)).add
          (isSelfAdjoint_adjoint_comp_self Dz)

/-- Forma quadratica: `⟪x, H3L x⟫ = ‖Dc x‖² + ‖Db x‖² + ‖Dz x‖²`. -/
theorem H3L_quadratic_form (x : EuclideanSpace ℂ (Fin n)) :
    RCLike.re (inner ℂ x (H3L Dc Db Dz x))
      = ‖Dc x‖ ^ 2 + ‖Db x‖ ^ 2 + ‖Dz x‖ ^ 2 := by
  unfold H3L
  simp only [LinearMap.add_apply, LinearMap.comp_apply, inner_add_right,
             LinearMap.adjoint_inner_right, map_add, inner_self_eq_norm_sq]

/-- `H3L` e' positivo semidefinido: `Re ⟪x, H3L x⟫ ≥ 0`. -/
theorem H3L_posSemidefinite (x : EuclideanSpace ℂ (Fin n)) :
    0 ≤ RCLike.re (inner ℂ x (H3L Dc Db Dz x)) := by
  rw [H3L_quadratic_form]
  positivity

/-- `x ∈ ker H3L ↔ Dc x = 0 ∧ Db x = 0 ∧ Dz x = 0`. -/
theorem mem_ker_H3L_iff (x : EuclideanSpace ℂ (Fin n)) :
    x ∈ LinearMap.ker (H3L Dc Db Dz) ↔ Dc x = 0 ∧ Db x = 0 ∧ Dz x = 0 := by
  constructor
  · intro hx
    rw [LinearMap.mem_ker] at hx
    have hre : ‖Dc x‖ ^ 2 + ‖Db x‖ ^ 2 + ‖Dz x‖ ^ 2 = 0 := by
      rw [← H3L_quadratic_form Dc Db Dz x, hx, inner_zero_right, map_zero]
    refine ⟨?_, ?_, ?_⟩ <;> rw [← norm_eq_zero] <;>
      nlinarith [norm_nonneg (Dc x), norm_nonneg (Db x), norm_nonneg (Dz x),
        sq_nonneg (‖Dc x‖), sq_nonneg (‖Db x‖), sq_nonneg (‖Dz x‖)]
  · rintro ⟨hc, hb, hz⟩
    rw [LinearMap.mem_ker]
    simp [H3L, LinearMap.add_apply, LinearMap.comp_apply, hc, hb, hz]

/-- `ker H3L = ker Dc ⊓ ker Db ⊓ ker Dz` (a interseccao dos Three Locks). -/
theorem ker_H3L_eq_threeLocks :
    LinearMap.ker (H3L Dc Db Dz)
      = LinearMap.ker Dc ⊓ LinearMap.ker Db ⊓ LinearMap.ker Dz := by
  ext x
  rw [mem_ker_H3L_iff]
  simp only [Submodule.mem_inf, LinearMap.mem_ker, and_assoc]

/-- Projetor ortogonal sobre `ker H3L` -- o canto dos Three Locks.
    (`Submodule.starProjection` e' a projecao ortogonal como endomorfismo.) -/
noncomputable def PF : EuclideanSpace ℂ (Fin n) →L[ℂ] EuclideanSpace ℂ (Fin n) :=
  (LinearMap.ker (H3L Dc Db Dz)).starProjection

/-- `P_F` e' idempotente: `P_F ∘ P_F = P_F`. -/
theorem PF_isProjection : IsIdempotentElem (PF Dc Db Dz) :=
  Submodule.isIdempotentElem_starProjection _

/-- A imagem de `P_F` esta no canto: `P_F x ∈ ker H3L`. -/
theorem PF_apply_mem (x : EuclideanSpace ℂ (Fin n)) :
    PF Dc Db Dz x ∈ LinearMap.ker (H3L Dc Db Dz) :=
  Submodule.starProjection_apply_mem _ x

/-- `P_F` e' auto-adjunto: `⟪P_F u, v⟫ = ⟪u, P_F v⟫`. -/
theorem PF_isSelfAdjoint (u v : EuclideanSpace ℂ (Fin n)) :
    inner ℂ (PF Dc Db Dz u) v = inner ℂ u (PF Dc Db Dz v) :=
  Submodule.inner_starProjection_left_eq_right _ u v

/-- `P_F` fixa exatamente o canto: `P_F v = v ↔ v ∈ ker H3L`. -/
theorem PF_eq_self_iff (v : EuclideanSpace ℂ (Fin n)) :
    PF Dc Db Dz v = v ↔ v ∈ LinearMap.ker (H3L Dc Db Dz) :=
  Submodule.starProjection_eq_self_iff

/-- Dimensao do canto (nucleo de `H3L`). -/
noncomputable def cornerDim : ℕ := Module.finrank ℂ (LinearMap.ker (H3L Dc Db Dz))

/-- `tau_F(P_F) = 1`: `Tr_F(P_F) = dim F`, logo `dim F / dim F = 1` (canto nao-trivial). -/
theorem normalizedCornerTrace_PF (h : 0 < cornerDim Dc Db Dz) :
    (cornerDim Dc Db Dz : ℝ) / (cornerDim Dc Db Dz : ℝ) = 1 := by
  have hne : (cornerDim Dc Db Dz : ℝ) ≠ 0 := by exact_mod_cast h.ne'
  exact div_self hne

/-- Faces conjugadas iguais tem traco normalizado `1/2`. -/
theorem equalConjugateFaces_halfTrace
    (dplus dminus : ℕ)
    (hsplit : dplus + dminus = cornerDim Dc Db Dz)
    (heq : dplus = dminus) (hpos : 0 < cornerDim Dc Db Dz) :
    (dplus : ℝ) / (cornerDim Dc Db Dz : ℝ) = 1 / 2 := by
  have hcd : cornerDim Dc Db Dz = 2 * dplus := by omega
  have hcdR : (cornerDim Dc Db Dz : ℝ) = 2 * (dplus : ℝ) := by exact_mod_cast hcd
  have hdpos : 0 < dplus := by omega
  have hdne : ((dplus : ℝ)) ≠ 0 := by exact_mod_cast hdpos.ne'
  have h2d : (2 * (dplus : ℝ)) ≠ 0 := mul_ne_zero (by norm_num) hdne
  rw [hcdR, div_eq_div_iff h2d (by norm_num : (2 : ℝ) ≠ 0)]
  ring

end TGL.FiniteThreeLocks
