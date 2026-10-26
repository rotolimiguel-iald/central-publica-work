import Mathlib

set_option autoImplicit false

/-!
Probe de diagnostico (NAO importado pela biblioteca TGL, nao entra em selo).

RESULTADO DA INVESTIGACAO (mathlib v4.31.0):
  - `inner_self_eq_norm_sq_to_K : inner 𝕜 x x = (‖x‖ : 𝕜) ^ 2`  usa `RCLike.ofReal`;
    misturar isso com `Complex.ofReal` no enunciado da a dois ATOMOS distintos e
    `ring`/`rfl` nao fecham. Solucao: ficar em ℝ via `RCLike.re`.
  - `inner_self_eq_norm_sq : RCLike.re (inner 𝕜 x x) = ‖x‖ ^ 2`  <-- a rota usada.
  - `inner_self_nonneg : 0 ≤ RCLike.re (inner 𝕜 x x)`.
-/

#check @inner_self_eq_norm_sq_to_K
#check @inner_self_eq_norm_sq
#check @inner_self_nonneg
#check @inner_self_eq_zero

-- a forma SEM coercao (compila)
example (n : ℕ) (D : EuclideanSpace ℂ (Fin n) →ₗ[ℂ] EuclideanSpace ℂ (Fin n))
    (x : EuclideanSpace ℂ (Fin n)) :
    inner ℂ x (LinearMap.adjoint D (D x)) = inner ℂ (D x) (D x) := by
  rw [LinearMap.adjoint_inner_right]

-- a forma REAL, que evita a coercao ℝ→ℂ (compila)
example (n : ℕ) (D : EuclideanSpace ℂ (Fin n) →ₗ[ℂ] EuclideanSpace ℂ (Fin n))
    (x : EuclideanSpace ℂ (Fin n)) :
    RCLike.re (inner ℂ (D x) (D x)) = ‖D x‖ ^ 2 :=
  inner_self_eq_norm_sq (D x)
