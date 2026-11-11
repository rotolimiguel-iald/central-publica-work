import TGLExt.TheProfileIsometry

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A DUALIDADE DO PERFIL — o núcleo algébrico das duas cláusulas de comutante
  [BANCADA — 26/08/2026 · marco M4 · ordem «pague»]

## O que as duas cláusulas pedem, e o que esta pedra entrega

O certificado pede `J M J ⊆ M′` e `J M J ⊇ M′`, com `M` = o **bicomutante** da imagem
da torre e `M′` o seu centralizador. Esta pedra entrega o **núcleo algébrico** de
ambas, com a densidade CERTA (a do perfil):

* a conjugação leva **multiplicação à ESQUERDA** em multiplicação à **DIREITA**;
* e é **SOBRE** as multiplicações à direita (dada uma, existe a esquerda que a produz);
* e multiplicações à direita **comutam com TODAS as esquerdas** — por pura
  associatividade. Logo `J·L_a·J` está no centralizador dos geradores.

## O que se prova

* ★★★ **`profileJ_conj_left_is_right`** — `J(a·J z) = z·(√ρ·aᴴ·√ρ⁻¹)`: esquerda ↦ direita;
* ★★★ **`profileJ_onto_right`** — ∀ direita, ∃ esquerda que a produz (a recíproca);
* ★★★ **`right_commutes_with_left`** — direita comuta com toda esquerda (associatividade);
* ★★★ **`profileJ_conj_left_centralizes`** — **a conjugada de uma esquerda comuta com
  TODA esquerda**: `J M J` no centralizador dos GERADORES, em ato.

## O QUE FALTA, DITO COM EXATIDÃO (e não é pouco)
Isto é o nível dos **GERADORES** e das **matrizes do andar**. As cláusulas do
certificado falam de operadores contínuos no completamento `WH` e do **BICOMUTANTE** —
levantar daqui até lá exige (a) transportar a dualidade para o completamento (o
mecanismo da v225, ainda não aplicado a estes objetos) e (b) o argumento de bicomutante
de von Neumann, que a mathlib não entrega pronto. **Enquanto isso não estiver escrito,
as duas cláusulas seguem ABERTAS e o razonete lê ABERTO.** Nível de gerador não é
nível de álgebra — e confundir os dois seria pagar-se na própria moeda. β jamais entra.
Nada move o gate.
-/

namespace TGLExt

open Matrix

variable {P : SiteProfile}

/-- ★★ **ESQUERDA VIRA DIREITA (forma generalizada)** — a versão do Ato I com a
    inversa como DADO do andar. -/
theorem stateJG_conj_Lmul {n : Type} [Fintype n] [DecidableEq n]
    (h hi : Matrix n n ℂ) (hherm : hᴴ = h) (h1 : h * hi = 1) (a z : Matrix n n ℂ) :
    stateJG h hi (a * stateJG h hi z) = z * (h * aᴴ * hi) := by
  have hhi : hiᴴ = hi := floor_inv_isHermitian h hi hherm h1
  unfold stateJG
  simp only [conjTranspose_mul, hhi, hherm, conjTranspose_conjTranspose]
  calc h * (hi * (z * h) * aᴴ) * hi
      = (h * hi) * z * (h * aᴴ * hi) := by noncomm_ring
    _ = z * (h * aᴴ * hi) := by rw [h1, one_mul]

/-- ★★ **E SOBRE AS DIREITAS (forma generalizada)**. -/
theorem stateJG_onto_commutant {n : Type} [Fintype n] [DecidableEq n]
    (h hi : Matrix n n ℂ) (hherm : hᴴ = h) (h1 : h * hi = 1) (b : Matrix n n ℂ) :
    ∃ a : Matrix n n ℂ, ∀ z, stateJG h hi (a * stateJG h hi z) = z * b := by
  have hhi : hiᴴ = hi := floor_inv_isHermitian h hi hherm h1
  refine ⟨h * bᴴ * hi, fun z => ?_⟩
  rw [stateJG_conj_Lmul h hi hherm h1]
  congr 1
  simp only [conjTranspose_mul, hhi, hherm, conjTranspose_conjTranspose]
  calc h * (hi * (b * h)) * hi
      = (h * hi) * b * (h * hi) := by noncomm_ring
    _ = b := by rw [h1, one_mul, mul_one]

/-- ★★★ **ESQUERDA VIRA DIREITA**: a conjugação do perfil leva `L_a` em `R_b`, com
    `b = √ρ · aᴴ · √ρ⁻¹` explícito. -/
theorem profileJ_conj_left_is_right (P : SiteProfile) (N : ℕ)
    (a z : Matrix (chainIdx N) (chainIdx N) ℂ) :
    profileJlevel P N (a * profileJlevel P N z)
      = z * (profileRoot P N * aᴴ * profileRootInv P N) :=
  stateJG_conj_Lmul (profileRoot P N) (profileRootInv P N)
    (profileRoot_isHermitian P N) (profileRoot_mul_inv P N) a z

/-- ★★★ **E É SOBRE AS DIREITAS**: dada uma multiplicação à direita, existe a esquerda
    cuja conjugada é ela. -/
theorem profileJ_onto_right (P : SiteProfile) (N : ℕ)
    (b : Matrix (chainIdx N) (chainIdx N) ℂ) :
    ∃ a : Matrix (chainIdx N) (chainIdx N) ℂ,
      ∀ z, profileJlevel P N (a * profileJlevel P N z) = z * b :=
  stateJG_onto_commutant (profileRoot P N) (profileRootInv P N)
    (profileRoot_isHermitian P N) (profileRoot_mul_inv P N) b

/-- ★★★ **DIREITA COMUTA COM TODA ESQUERDA** — associatividade pura: é isto que faz o
    lado direito ser o comutante. -/
theorem right_commutes_with_left {n : Type} [Fintype n] [DecidableEq n]
    (a b z : Matrix n n ℂ) : a * (z * b) = (a * z) * b :=
  (mul_assoc a z b).symm

/-- ★★★ **A CONJUGADA DE UMA ESQUERDA COMUTA COM TODA ESQUERDA**: `J·L_a·J` está no
    centralizador dos geradores — a face algébrica de `J M J ⊆ M′`, em ato. -/
theorem profileJ_conj_left_centralizes (P : SiteProfile) (N : ℕ)
    (a c z : Matrix (chainIdx N) (chainIdx N) ℂ) :
    c * profileJlevel P N (a * profileJlevel P N z)
      = profileJlevel P N (a * profileJlevel P N (c * z)) := by
  rw [profileJ_conj_left_is_right, profileJ_conj_left_is_right, ← mul_assoc]

end TGLExt
