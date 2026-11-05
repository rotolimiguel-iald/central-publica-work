import Mathlib

set_option autoImplicit false

/-!
# Comutante: a semente do Degrau 1   [TGLExt -- frente experimental]

O comutante de um conjunto de operadores, com os fatos básicos que a mathlib
não empacota nesta forma: e' subálgebra unital fechada por estrela (quando o
conjunto e' fechado por estrela), a antitonia, e a inclusão no bicomutante
`S ⊆ S′′`. Puramente algébrico -- vale em qualquer anel-* (em particular nas
álgebras de matrizes e em B(H)). E' o primeiro tijolo do bicomutante finito
(Degrau 1) e, adiante, do Tomita-Takesaki finito (Degrau 0).
Sem sorry, sem axiom. Negativo honesto e' resultado.
-/

namespace TGLExt

variable {A : Type} [Ring A]

/-- O comutante de um conjunto: tudo que comuta com todos os elementos. -/
def commutantSet (S : Set A) : Set A := {x : A | ∀ s ∈ S, s * x = x * s}

theorem mem_commutantSet {S : Set A} {x : A} :
    x ∈ commutantSet S ↔ ∀ s ∈ S, s * x = x * s := Iff.rfl

/-- [KERNEL] `1` está em todo comutante. -/
theorem one_mem_commutant (S : Set A) : (1 : A) ∈ commutantSet S :=
  fun s _ => by rw [mul_one, one_mul]

/-- [KERNEL] `0` está em todo comutante. -/
theorem zero_mem_commutant (S : Set A) : (0 : A) ∈ commutantSet S :=
  fun s _ => by rw [mul_zero, zero_mul]

/-- [KERNEL] O comutante é fechado por soma. -/
theorem add_mem_commutant {S : Set A} {x y : A}
    (hx : x ∈ commutantSet S) (hy : y ∈ commutantSet S) :
    x + y ∈ commutantSet S :=
  fun s hs => by rw [mul_add, add_mul, hx s hs, hy s hs]

/-- [KERNEL] O comutante é fechado por produto. -/
theorem mul_mem_commutant {S : Set A} {x y : A}
    (hx : x ∈ commutantSet S) (hy : y ∈ commutantSet S) :
    x * y ∈ commutantSet S := by
  intro s hs
  rw [← mul_assoc, hx s hs, mul_assoc, hy s hs, ← mul_assoc]

/-- [KERNEL] O comutante é fechado por negação. -/
theorem neg_mem_commutant {S : Set A} {x : A} (hx : x ∈ commutantSet S) :
    -x ∈ commutantSet S :=
  fun s hs => by rw [mul_neg, neg_mul, hx s hs]

/-- [KERNEL] Se `S` é fechado por estrela, o comutante também é
    (o primeiro passo rumo a `S′` como álgebra de von Neumann). -/
theorem star_mem_commutant [StarRing A] {S : Set A} (hS : ∀ s ∈ S, star s ∈ S)
    {x : A} (hx : x ∈ commutantSet S) :
    star x ∈ commutantSet S := by
  intro s hs
  have h := hx (star s) (hS s hs)
  calc s * star x = star (x * star s) := by rw [star_mul, star_star]
    _ = star (star s * x) := by rw [h]
    _ = star x * s := by rw [star_mul, star_star]

/-- [KERNEL] ANTITONIA: conjunto maior, comutante menor. -/
theorem commutant_antitone {S T : Set A} (h : S ⊆ T) :
    commutantSet T ⊆ commutantSet S :=
  fun _ hx s hs => hx s (h hs)

/-- [KERNEL] `S ⊆ S′′`: todo elemento comuta com o que comuta com ele.
    O primeiro meio-passo do bicomutante. -/
theorem subset_bicommutant (S : Set A) :
    S ⊆ commutantSet (commutantSet S) :=
  fun s hs _ hx => (hx s hs).symm

/-- [KERNEL] `S′ = S′′′`: o comutante estabiliza no terceiro passo.
    (Consequência formal de antitonia + `S ⊆ S′′` — o fecho de Galois.) -/
theorem commutant_triple (S : Set A) :
    commutantSet (commutantSet (commutantSet S)) = commutantSet S := by
  apply Set.Subset.antisymm
  · exact commutant_antitone (subset_bicommutant S)
  · exact subset_bicommutant (commutantSet S)

/-- [KERNEL] Ponte para a mathlib: nosso comutante É `Set.centralizer`, na
    mesma ordem `s * x = x * s`. Auditoria honesta (recon 11/07/2026): os dez
    teoremas acima têm análogos em `Set.*_centralizer`; o que a mathlib NÃO
    tem é o teorema do bicomutante como TEOREMA (em `VonNeumannAlgebra` ele é
    campo estrutural) — essa é a contribuição-alvo desta frente. -/
theorem commutantSet_eq_centralizer (S : Set A) :
    commutantSet S = Set.centralizer S := rfl

end TGLExt
