import TGLExt.TheTowerWitnessLinear
import TGLExt.TheTowerInnerProduct

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A CONJUGAÇÃO DO PERFIL — a correção que a isometria exigiu
  [BANCADA — 26/08/2026 · marco M4 · ordem «pague» · ERRATA de construção]

## O achado (e ele é do tipo que a régua existe para pegar)

Ao atacar a cláusula da ISOMETRIA descobriu-se que o produto interno da torre,
`tInner P N a b = tState P N (aᴴ·b) = Σ_k towerW P N k · (aᴴ·b)_kk`, é dado pelos pesos
do **PERFIL** `P` — e o perfil do certificado (`mixProfile`) tem pesos **alternados**
(1/3 e 1/4), **não uniformes**.

A conjugação construída nas ondas v227–v230 é torcida por `chainDensity l`, que usa o
**mesmo** λ em todo sítio. Os teoremas provados lá continuam **verdadeiros** — eles
falam de `chainDensity l` —, mas **não servem ao certificado**, porque a isometria só
vale quando a torção usa **a densidade que define o produto interno**. Registrado sem
suavizar: a construção estava torcida pela densidade errada para este fim.

## A correção

`towerW P (N+1) (p₁,p₂) = towerW P N p₁ · siteW (P.w (N+1)) p₂` — a **mesma** recursão
produto. Logo a raiz do perfil se fatora em Kronecker a cada degrau, e o entrelaçamento
do Ato II volta a aplicar-se, agora com a densidade CERTA.

## O que se prova

* ★★ `profileRoot_isHermitian` — a raiz do perfil é hermitiana (diagonal real);
* ★★ `profileRoot_mul_inv` — e inverte (os pesos são estritamente positivos);
* ★★★ **`profileRoot_succ`** — **a raiz FATORA no degrau**: `√ρ_{N+1} = √ρ_N ⊗ₖ √σ`;
* ★★★ **`profileJ_commutes_with_step`** — a conjugação do PERFIL atravessa o degrau —
  e é ela, não a anterior, que serve ao certificado.

## O QUE FALTA (sem suavizar)
Descer esta conjugação ao colimite (mecânica idêntica à da v229, agora com a densidade
certa), provar a isometria contra `innerPre`, estender ao completamento e as duas
cláusulas de comutante. O razonete lê ABERTO. β jamais entra. Nada move o gate.
-/

namespace TGLExt

open Matrix
open scoped Kronecker

/-- a raiz da densidade do PERFIL no andar N (diagonal das raízes dos pesos). -/
noncomputable def profileRoot (P : SiteProfile) (N : ℕ) :
    Matrix (chainIdx N) (chainIdx N) ℂ :=
  diagonal fun i => ((Real.sqrt (towerW P N i) : ℝ) : ℂ)

/-- a inversa da raiz do perfil. -/
noncomputable def profileRootInv (P : SiteProfile) (N : ℕ) :
    Matrix (chainIdx N) (chainIdx N) ℂ :=
  diagonal fun i => ((1 / Real.sqrt (towerW P N i) : ℝ) : ℂ)

/-- a raiz do sítio elementar. -/
noncomputable def siteRoot (t : ℝ) : Matrix (Fin 2) (Fin 2) ℂ :=
  diagonal fun i => ((Real.sqrt (siteW t i) : ℝ) : ℂ)

noncomputable def siteRootInv (t : ℝ) : Matrix (Fin 2) (Fin 2) ℂ :=
  diagonal fun i => ((1 / Real.sqrt (siteW t i) : ℝ) : ℂ)

/-- ★★ a raiz do perfil é hermitiana. -/
theorem profileRoot_isHermitian (P : SiteProfile) (N : ℕ) :
    (profileRoot P N)ᴴ = profileRoot P N := by
  unfold profileRoot
  rw [diagonal_conjTranspose]
  congr 1
  funext i
  simp [Complex.conj_ofReal]

/-- ★★ a raiz do perfil inverte (pesos estritamente positivos). -/
theorem profileRoot_mul_inv (P : SiteProfile) (N : ℕ) :
    profileRoot P N * profileRootInv P N = 1 := by
  unfold profileRoot profileRootInv
  rw [diagonal_mul_diagonal, ← diagonal_one]
  congr 1
  funext i
  have hp : (0:ℝ) < Real.sqrt (towerW P N i) :=
    Real.sqrt_pos.mpr (towerW_pos P N i)
  rw [← Complex.ofReal_mul, mul_one_div, div_self (ne_of_gt hp), Complex.ofReal_one]

theorem siteRoot_mul_inv (t : ℝ) (h0 : 0 < t) (h1 : t < 1) :
    siteRoot t * siteRootInv t = 1 := by
  unfold siteRoot siteRootInv
  rw [diagonal_mul_diagonal, ← diagonal_one]
  congr 1
  funext i
  have hp : (0:ℝ) < Real.sqrt (siteW t i) := Real.sqrt_pos.mpr (siteW_pos h0 h1 i)
  rw [← Complex.ofReal_mul, mul_one_div, div_self (ne_of_gt hp), Complex.ofReal_one]

/-- ★★★ **A RAIZ DO PERFIL FATORA NO DEGRAU**: `√ρ_{N+1} = √ρ_N ⊗ₖ √σ_{N+1}`. -/
theorem profileRoot_succ (P : SiteProfile) (N : ℕ) :
    profileRoot P (N + 1) = profileRoot P N ⊗ₖ siteRoot (P.w (N + 1)) := by
  unfold profileRoot siteRoot
  rw [diagonal_kronecker_diagonal]
  congr 1
  funext p
  show ((Real.sqrt (towerW P N p.1 * siteW (P.w (N + 1)) p.2) : ℝ) : ℂ)
    = ((Real.sqrt (towerW P N p.1) : ℝ) : ℂ) * ((Real.sqrt (siteW (P.w (N+1)) p.2) : ℝ) : ℂ)
  rw [← Complex.ofReal_mul, Real.sqrt_mul (le_of_lt (towerW_pos P N p.1))]

theorem profileRootInv_succ (P : SiteProfile) (N : ℕ) :
    profileRootInv P (N + 1) = profileRootInv P N ⊗ₖ siteRootInv (P.w (N + 1)) := by
  unfold profileRootInv siteRootInv
  rw [diagonal_kronecker_diagonal]
  congr 1
  funext p
  have hA : (0:ℝ) ≤ towerW P N p.1 := le_of_lt (towerW_pos P N p.1)
  show ((1 / Real.sqrt (towerW P N p.1 * siteW (P.w (N + 1)) p.2) : ℝ) : ℂ)
    = ((1 / Real.sqrt (towerW P N p.1) : ℝ) : ℂ)
      * ((1 / Real.sqrt (siteW (P.w (N+1)) p.2) : ℝ) : ℂ)
  rw [← Complex.ofReal_mul, Real.sqrt_mul hA]
  norm_num
  ring

/-- **A CONJUGAÇÃO DO PERFIL NO ANDAR N** — a que serve ao certificado. -/
noncomputable def profileJlevel (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) : Matrix (chainIdx N) (chainIdx N) ℂ :=
  stateJG (profileRoot P N) (profileRootInv P N) a

/-- ★★★ **A CONJUGAÇÃO DO PERFIL ATRAVESSA O DEGRAU** — com a densidade CERTA. -/
theorem profileJ_commutes_with_step (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    profileJlevel P (N + 1) (towerStep a) = towerStep (profileJlevel P N a) := by
  unfold profileJlevel towerStep
  rw [profileRoot_succ, profileRootInv_succ]
  exact the_tower_interlaces (profileRoot P N) (profileRootInv P N)
    (siteRoot (P.w (N + 1))) (siteRootInv (P.w (N + 1)))
    (siteRoot_mul_inv _ (P.pos (N + 1)) (P.lt_one (N + 1))) a

end TGLExt
