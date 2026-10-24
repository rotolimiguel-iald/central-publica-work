import Mathlib

set_option autoImplicit false

/-!
# Probe3 -- descoberta de API para a rigidificacao (FASE B)   [DIAGNOSTICO]

Verifica o que EXISTE na mathlib v4.31.0 antes de escrever a estrutura rigida:
von Neumann algebras, star/adjoint em `H →L[ℂ] H`, SetLike, Dense+span,
pecas de Minkowski. NAO importado por TGL.lean.
-/

namespace TGL.Probe3

-- (1) VonNeumannAlgebra existe? membership? coercao a Set?
#check @VonNeumannAlgebra
example (H : Type) [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (A : VonNeumannAlgebra H) (a : H →L[ℂ] H) : Prop := a ∈ A
example (H : Type) [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (A : VonNeumannAlgebra H) : Set (H →L[ℂ] H) := (A : Set (H →L[ℂ] H))

-- (2) star (adjunto) em H →L[ℂ] H
example (H : Type) [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (a : H →L[ℂ] H) : H →L[ℂ] H := star a

-- (3) mul = composicao; unidade
example (H : Type) [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (a b : H →L[ℂ] H) : H →L[ℂ] H := a * b
example (H : Type) [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H] :
    H →L[ℂ] H := 1

-- (4) Commute em H →L[ℂ] H
example (H : Type) [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (a b : H →L[ℂ] H) : Prop := Commute a b

-- (5) Dense do span (ciclicidade enunciavel)
example (H : Type) [NormedAddCommGroup H] [InnerProductSpace ℂ H] (s : Set H) : Prop :=
  Dense ((Submodule.span ℂ s : Submodule ℂ H) : Set H)

-- (6) pecas de Minkowski em Fin 4 → ℝ
example (v : Fin 4 → ℝ) : ℝ := v 0 ^ 2 - v 1 ^ 2 - v 2 ^ 2 - v 3 ^ 2
example (x : Fin 4 → ℝ) : Prop := |x 0| < x 1
example (x y : Fin 4 → ℝ) : Fin 4 → ℝ := x - y
example (v : Fin 4 → ℝ) (a : Fin 4 → ℝ) : Set (Fin 4 → ℝ) → Set (Fin 4 → ℝ) :=
  fun O => (fun x => x + a) '' O

-- (7) aplicacao de operador a vetor (imagem do vacuo)
example (H : Type) [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
    (a : H →L[ℂ] H) (v : H) : H := a v

#eval IO.println "PROBE3_OK"

end TGL.Probe3
