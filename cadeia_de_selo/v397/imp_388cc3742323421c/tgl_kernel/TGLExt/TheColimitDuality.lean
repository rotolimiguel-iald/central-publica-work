import TGLExt.TheProfileDuality
import TGLExt.RightMult

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A DUALIDADE NO COLIMITE — a dobra executada um andar acima
  [BANCADA — 26/08/2026 · marco M4 · ordem «pague»]

## O passo

A v235 provou a dualidade no ANDAR: a conjugação leva multiplicação à esquerda em
multiplicação à direita. Esta pedra **executa a dobra**: leva o enunciado ao COLIMITE,
onde as multiplicações já existem na árvore (`lmulPre`, `rmulPre`) e onde já estava
provado que **direita comuta com esquerda** (`rmulPre_comm_lmulPre`).

## O que se prova

* ★★★ **`profileJpre_conj_lmul`** — no colimite: `J(L_a(J v)) = R_b(v)` com
  `b = √ρ·aᴴ·√ρ⁻¹` — a conjugação leva a ESQUERDA na DIREITA, na torre inteira;
* ★★★ **`profileJpre_conj_lmul_centralizes`** — e a conjugada de uma esquerda **comuta
  com toda esquerda** no colimite (usando o lema de comutação já na árvore): a face
  de `J M J ⊆ M′` **no pré-espaço**, não mais só no andar.

## O QUE FALTA (sem suavizar)
Isto vive no **pré-espaço** `TowerPre`. O certificado fala de operadores contínuos no
**completamento** `WH` e do **bicomutante**. A dobra que resta é a última: transportar
por densidade (mecanismo v225, e agora com `lmulCLM`/`rmulCLM` que já são contínuos) e
o argumento de bicomutante. As duas cláusulas seguem ABERTAS. β jamais entra. Nada
move o gate.
-/

namespace TGLExt

open Matrix

variable {P : SiteProfile}

/-- o fator direito É a própria conjugação de `a` (definição desdobrada). -/
theorem profileJlevel_eq (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    profileJlevel P N a = profileRoot P N * aᴴ * profileRootInv P N := rfl

/-- ★★★ **A DUALIDADE NO COLIMITE**: `J(L_a(J v)) = R_{J a}(v)` --- a conjugação leva a
    ESQUERDA na DIREITA na torre inteira, e o fator direito é a conjugada de `a`. -/
theorem profileJpre_conj_lmul (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) (v : TowerPre P) :
    profileJpre P (lmulPre P a (profileJpre P v))
      = rmulPre P (profileJlevel P N a) v := by
  obtain ⟨M, z, rfl⟩ := exists_tof v
  have hN : N ≤ N ⊔ M := le_sup_left
  have hM : M ≤ N ⊔ M := le_sup_right
  rw [profileJpre_tof, lmulPre_tof_at hN hM, profileJpre_tof, rmulPre_tof_at hN hM]
  congr 1
  rw [profileJ_commutes_with_tPush P hM z, profileJ_commutes_with_tPush P hN a,
      profileJ_conj_left_is_right P (N ⊔ M) (tPush hN a) (tPush hM z),
      profileJlevel_eq]

/-- ★★★ **E ELA CENTRALIZA NO COLIMITE**: a conjugada de uma esquerda comuta com toda
    esquerda --- a face de `J M J ⊆ M′` no pré-espaço. -/
theorem profileJpre_conj_lmul_centralizes (P : SiteProfile) {N M : ℕ}
    (a : Matrix (chainIdx N) (chainIdx N) ℂ)
    (c : Matrix (chainIdx M) (chainIdx M) ℂ) (v : TowerPre P) :
    lmulPre P c (profileJpre P (lmulPre P a (profileJpre P v)))
      = profileJpre P (lmulPre P a (profileJpre P (lmulPre P c v))) := by
  rw [profileJpre_conj_lmul, profileJpre_conj_lmul, rmulPre_comm_lmulPre]

end TGLExt
