import Mathlib

set_option autoImplicit false

/-!
# Probe4 -- API do exponencial de Banach para o Verbo (v25)   [DIAGNOSTICO]

O teorema do especialista: `a * p = 0  ⟹  exp(a) * p = p`. Precisa de:
exp em algebra de Banach, exp_eq_tsum, tsum_mul_right, tsum_eq_single.
NAO importado por TGL.lean.
-/

namespace TGL.Probe4

-- (1) exp em algebra de Banach: nome e tipo
#check @NormedSpace.exp
noncomputable example {A : Type} [NormedRing A] [NormedAlgebra ℂ A] [CompleteSpace A]
    (a : A) : A := NormedSpace.exp ℂ a

-- (2) exp como tsum
#check @NormedSpace.exp_eq_tsum

-- (3) tsum vezes elemento a direita
#check @tsum_mul_right

-- (4) tsum de suporte unico
#check @tsum_eq_single

-- (5) smul e mul associam
example {A : Type} [Ring A] [Algebra ℂ A] (c : ℂ) (a p : A) :
    (c • a) * p = c • (a * p) := smul_mul_assoc c a p

-- (6) potencia mata: a^(n+1) * p = a^n * (a * p)
example {A : Type} [Ring A] (a p : A) (n : ℕ) :
    a ^ (n + 1) * p = a ^ n * (a * p) := by
  rw [pow_succ, mul_assoc]

#eval IO.println "PROBE4_OK"

end TGL.Probe4
