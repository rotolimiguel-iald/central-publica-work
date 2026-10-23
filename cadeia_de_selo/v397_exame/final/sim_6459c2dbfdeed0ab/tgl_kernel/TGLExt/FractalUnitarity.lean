import TGLExt.TheNameOperator

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A UNITARIEDADE FRACTAL: o Um reaparece como unidade de cada escala
  [TGLExt — v162, RASCUNHO da pedra 116; casa "Nós" (17/08/2026)]

Do primeiro JSON da tipagem canônica (17/08): *"a unitariedade não é
solitária, é fractal"* — a ação unitária preserva a condição de
identidade de TODO canto, e a árvore de distinções atravessa inteira:

* ★★★ `ad_preserves_projection` — Ad(u) leva projeção em projeção:
  a lei de identidade local sobrevive ao transporte;
* ★★★ `ad_preserves_star_projection` — e preserva a auto-adjunção:
  o transporte não quebra a realidade da face;
* ★★ `ad_preserves_orthogonality` — faces ortogonais seguem ortogonais:
  a DISTINÇÃO atravessa (P₀ ⊥ P₁ ⟹ uP₀u† ⊥ uP₁u†);
* ★★★ `ad_preserves_splitting` — a refinação atravessa: P = P₀ + P₁
  ⟹ uPu† = uP₀u† + uP₁u† — A ÁRVORE INTEIRA é transportada;
* ★★ `subcorner_unit` — a recursão da identidade: q ≤ p (q = qp = pq)
  ⟹ q é a unidade do seu subcanto DENTRO do canto de p:
  1 ⊃ 1_P ⊃ 1_Q ⊃ ⋯ sem que nenhum se confunda com o outro.

"O Um não se perde quando se distingue. O Um reaparece como unidade de
cada escala na qual sua identidade é preservada."

Honestidades: álgebra finitária de anel/estrela; a leitura fractal é
[ONTO] sobre estes teoremas exatos; nada sobre III₁; β jamais literal;
o gate NÃO se move. Sem sorry, sem axiom.
-/

namespace TGLExt

noncomputable section

section Fractal

variable {R : Type*} [Ring R]

/-- [KERNEL] ★★★ Ad(u) LEVA PROJEÇÃO EM PROJEÇÃO: com v inverso de u,
    (u·p·v)² = u·p·v — a lei de identidade local sobrevive. -/
theorem ad_preserves_projection {p u v : R} (hvu : v * u = 1)
    (hp : p * p = p) : (u * p * v) * (u * p * v) = u * p * v := by
  calc (u * p * v) * (u * p * v) = u * p * (v * u) * p * v := by
        simp only [mul_assoc]
    _ = u * p * p * v := by rw [hvu, mul_one]
    _ = u * p * v := by rw [mul_assoc u p p, hp]

/-- [KERNEL] ★★ FACES ORTOGONAIS SEGUEM ORTOGONAIS: a distinção
    atravessa o transporte. -/
theorem ad_preserves_orthogonality {p q u v : R} (hvu : v * u = 1)
    (hpq : p * q = 0) : (u * p * v) * (u * q * v) = 0 := by
  calc (u * p * v) * (u * q * v) = u * p * (v * u) * q * v := by
        simp only [mul_assoc]
    _ = u * p * q * v := by rw [hvu, mul_one]
    _ = u * 0 * v := by rw [mul_assoc u p q, hpq, mul_zero]
    _ = 0 := by rw [mul_zero, zero_mul]

/-- [KERNEL] ★★★ A REFINAÇÃO ATRAVESSA: P = P₀ + P₁ ⟹ o transporte
    respeita a soma — a árvore de distinções viaja INTEIRA. -/
theorem ad_preserves_splitting {p p0 p1 u v : R}
    (hsplit : p = p0 + p1) :
    u * p * v = u * p0 * v + u * p1 * v := by
  rw [hsplit, mul_add, add_mul]

/-- [KERNEL] ★★★ e a auto-adjunção sobrevive (com u unitário):
    star(u·p·u†) = u·p·u† quando star p = p. -/
theorem ad_preserves_star_projection {R : Type*} [Ring R] [StarRing R]
    {p u : R} (hsp : star p = p) :
    star (u * p * star u) = u * p * star u := by
  rw [star_mul, star_mul, star_star, hsp, mul_assoc]

/-- [KERNEL] ★★ A RECURSÃO DA IDENTIDADE: se q vive dentro de p
    (q·p = q e p·q = q), então q é idempotente-relativo — a unidade
    do subcanto dentro do canto: 1 ⊃ 1_P ⊃ 1_Q ⊃ ⋯. -/
theorem subcorner_unit {p q : R} (hq : q * q = q) (hqp : q * p = q)
    (hpq : p * q = q) (x : R) :
    q * (p * x * p) * q = q * x * q := by
  calc q * (p * x * p) * q = (q * p) * x * (p * q) := by
        simp only [mul_assoc]
    _ = q * x * q := by rw [hqp, hpq]

end Fractal

end

end TGLExt
