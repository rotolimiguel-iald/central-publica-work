import TGLExt.TheProfileConjugation
import TGLExt.TheTowerInnerProduct
import TGLExt.TowerDefinite

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A ISOMETRIA DO PERFIL — a quinta cláusula, com a densidade certa
  [BANCADA — 26/08/2026 · marco M4 · ordem «pague»]

## O passo

A v231 corrigiu a torção (a densidade do PERFIL, não a uniforme) e provou que a
conjugação do perfil **atravessa o degrau**. Falta gastar a correção: descer ao
colimite e provar a **ISOMETRIA** — a cláusula que descobriu o erro e que agora pode
ser paga.

A chave é uma identificação: o estado da torre **É** o traço contra a densidade
diagonal dos pesos, e `profileRoot² = ` essa densidade. Logo o produto interno da torre
**é exatamente** o produto GNS da v224 com `h = profileRoot` — e a antiisometria de lá
se aplica **sem adaptação**.

## O que se prova

* ★★ `profileRoot_sq` — `√ρ · √ρ = ρ` (a diagonal dos pesos);
* ★★★ **`tState_eq_trace`** — o estado da torre É o traço contra a densidade;
* ★★★ **`tInner_eq_towerInner`** — **o produto interno da torre É o produto GNS** com
  `h = profileRoot`: a ponte que faz a v224 valer aqui;
* ★★★ **`profileJ_is_anti_isometric`** — **A ISOMETRIA**: `⟨Ja,Jb⟩ = conj⟨a,b⟩` no
  andar, contra o produto interno DA TORRE;
* ★★★ `profileJ_commutes_with_tPush` — e a conjugação do perfil comuta com o empurrão;
* ★★★ **`profileJpre`** — **desce ao colimite**, com `profileJpre_involutive` e
  `profileJpre_fixes_omega`.

## O QUE FALTA
A isometria **no colimite** (segue da do andar + boa definição do `innerPre`), a
extensão ao completamento (mecanismo v225) e as **duas cláusulas de comutante**. O
razonete lê ABERTO. β jamais entra. Nada move o gate.
-/

namespace TGLExt

open Matrix

variable {P : SiteProfile}

/-- ★★ **A RAIZ DO PERFIL AO QUADRADO É A DENSIDADE**. -/
theorem profileRoot_sq (P : SiteProfile) (N : ℕ) :
    profileRoot P N * profileRoot P N
      = diagonal fun k => ((towerW P N k : ℝ) : ℂ) := by
  unfold profileRoot
  rw [diagonal_mul_diagonal]
  congr 1
  funext k
  rw [← Complex.ofReal_mul, Real.mul_self_sqrt (le_of_lt (towerW_pos P N k))]

/-- ★★★ **O ESTADO DA TORRE É O TRAÇO CONTRA A DENSIDADE**. -/
theorem tState_eq_trace (P : SiteProfile) (N : ℕ)
    (c : Matrix (chainIdx N) (chainIdx N) ℂ) :
    tState P N c = ((diagonal fun k => ((towerW P N k : ℝ) : ℂ)) * c).trace := by
  unfold tState Matrix.trace
  simp [Matrix.diagonal_mul, Matrix.diag]

/-- ★★★ **O PRODUTO INTERNO DA TORRE É O PRODUTO GNS** com `h = profileRoot` —
    a ponte que faz a antiisometria da v224 valer aqui, sem adaptação. -/
theorem tInner_eq_towerInner (P : SiteProfile) (N : ℕ)
    (a b : Matrix (chainIdx N) (chainIdx N) ℂ) :
    tInner P N a b = towerInner (profileRoot P N) a b := by
  unfold tInner towerInner
  rw [tState_eq_trace, pow_two, profileRoot_sq]
  congr 1
  noncomm_ring

/-- ★★★ **A ISOMETRIA**: `⟨Ja, Jb⟩ = conj⟨a,b⟩` contra o produto interno DA TORRE. -/
theorem profileJ_is_anti_isometric (P : SiteProfile) (N : ℕ)
    (a b : Matrix (chainIdx N) (chainIdx N) ℂ) :
    tInner P N (profileJlevel P N a) (profileJlevel P N b)
      = star (tInner P N a b) := by
  rw [tInner_eq_towerInner, tInner_eq_towerInner]
  exact towerInner_stateJG_conj (profileRoot P N) (profileRootInv P N)
    (profileRoot_isHermitian P N) (profileRoot_mul_inv P N)
    (by
      have h := profileRoot_mul_inv P N
      unfold profileRoot profileRootInv at h ⊢
      rw [diagonal_mul_diagonal, ← diagonal_one]
      congr 1
      funext i
      have hp : (0:ℝ) < Real.sqrt (towerW P N i) :=
        Real.sqrt_pos.mpr (towerW_pos P N i)
      rw [← Complex.ofReal_mul, one_div, inv_mul_cancel₀ (ne_of_gt hp), Complex.ofReal_one])
    a b

/-- ★★★ **A CONJUGAÇÃO DO PERFIL COMUTA COM O EMPURRÃO**. -/
theorem profileJ_commutes_with_tPush (P : SiteProfile) :
    ∀ {N M : ℕ} (h : N ≤ M) (a : Matrix (chainIdx N) (chainIdx N) ℂ),
      tPush h (profileJlevel P N a) = profileJlevel P M (tPush h a) := by
  intro N M h a
  induction M, h using Nat.le_induction with
  | base => rw [tPush_self, tPush_self]
  | succ M hNM ih =>
      rw [tPush_succ hNM, tPush_succ hNM, ih, profileJ_commutes_with_step]

/-- ★★★ **A CONJUGAÇÃO DO PERFIL DESCE AO COLIMITE** — com a densidade CERTA. -/
noncomputable def profileJpre (P : SiteProfile) : TowerPre P → TowerPre P :=
  Quotient.map (fun x : TowerPt => (⟨x.1, profileJlevel P x.1 x.2⟩ : TowerPt))
    (by
      rintro x y ⟨K, hx, hy, e⟩
      refine ⟨K, hx, hy, ?_⟩
      show tPush hx (profileJlevel P x.1 x.2) = tPush hy (profileJlevel P y.1 y.2)
      rw [profileJ_commutes_with_tPush, profileJ_commutes_with_tPush, e])

theorem profileJpre_tof (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    profileJpre P (tof P N a) = tof P N (profileJlevel P N a) := rfl

/-- ★★★ **INVOLUTIVA NO COLIMITE**, com a densidade certa. -/
theorem profileJpre_involutive (P : SiteProfile) (x : TowerPre P) :
    profileJpre P (profileJpre P x) = x := by
  obtain ⟨N, a, rfl⟩ := exists_tof x
  rw [profileJpre_tof, profileJpre_tof]
  congr 1
  exact stateJG_involutive (profileRoot P N) (profileRootInv P N) a
    (profileRoot_isHermitian P N) (profileRoot_mul_inv P N)

/-- ★★★ **O VÁCUO DO NOME É J-FIXO**, com a densidade certa. -/
theorem profileJpre_fixes_omega (P : SiteProfile) :
    profileJpre P (towerOmega P) = towerOmega P := by
  unfold towerOmega
  rw [profileJpre_tof]
  congr 1
  unfold profileJlevel stateJG
  rw [conjTranspose_one, mul_one, profileRoot_mul_inv]

end TGLExt
