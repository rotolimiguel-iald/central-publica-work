import TGLExt.TheTowerWitness

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A TESTEMUNHA É ADITIVA E ANTILINEAR NO COLIMITE
  [BANCADA — 26/08/2026 · marco M4, item 4 da dívida · ordem «pague»]

## O passo

A v229 fez `J` descer ao colimite e provou ali a involução e o vácuo J-fixo. Faltavam
duas das cláusulas do certificado: **aditividade** e **ANTIlinearidade** — e elas não
são automáticas, porque as operações do colimite passam por **supremos de andares**:
somar `[a]_N` com `[b]_M` empurra ambos ao andar `N ⊔ M`. A prova, portanto, precisa
que `J` comute com o empurrão — que é exatamente o que a v229 estabeleceu.

## O que se prova

* ★★ `stateJG_add` / `stateJG_conj_smul` — aditiva e antilinear no andar;
* ★★★ **`towerJpre_add`** — **aditiva no colimite** (atravessa o supremo de andares);
* ★★★ **`towerJpre_conj_smul`** — **ANTILINEAR no colimite**: `J(c·x) = c̄·J(x)`;
* ★★ `towerJpre_zero` — leva zero em zero.

## O QUE FALTA (sem suavizar)
A **isometria** no colimite (contra o produto interno `innerPre`), a **extensão ao
completamento** (mecanismo da v225) e as **duas cláusulas de comutante**. Só então o
`ModularRealizationCertificate` se habita — e o razonete lê ABERTO até lá. β jamais
entra. Nada move o gate.
-/

namespace TGLExt

open Matrix

variable {P : SiteProfile}

/-- ★★ **ADITIVA NO ANDAR**. -/
theorem stateJG_add {n : Type} [Fintype n] [DecidableEq n]
    (h hi a b : Matrix n n ℂ) :
    stateJG h hi (a + b) = stateJG h hi a + stateJG h hi b := by
  unfold stateJG
  rw [conjTranspose_add, Matrix.mul_add, Matrix.add_mul]

/-- ★★ **ANTILINEAR NO ANDAR**. -/
theorem stateJG_conj_smul {n : Type} [Fintype n] [DecidableEq n]
    (h hi : Matrix n n ℂ) (c : ℂ) (a : Matrix n n ℂ) :
    stateJG h hi (c • a) = (starRingEnd ℂ) c • stateJG h hi a := by
  unfold stateJG
  rw [conjTranspose_smul]
  simp [Matrix.mul_smul, Matrix.smul_mul]

theorem towerJlevel_add (l : ℝ) (N : ℕ)
    (a b : Matrix (chainIdx N) (chainIdx N) ℂ) :
    towerJlevel l N (a + b) = towerJlevel l N a + towerJlevel l N b :=
  stateJG_add _ _ a b

theorem towerJlevel_conj_smul (l : ℝ) (N : ℕ) (c : ℂ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    towerJlevel l N (c • a) = (starRingEnd ℂ) c • towerJlevel l N a :=
  stateJG_conj_smul _ _ c a

/-- ★★★ **ADITIVA NO COLIMITE**: a soma atravessa o supremo de andares. -/
theorem towerJpre_add (l : ℝ) (hl : 0 < l) (x y : TowerPre P) :
    towerJpre l hl P (x + y) = towerJpre l hl P x + towerJpre l hl P y := by
  obtain ⟨N, a, rfl⟩ := exists_tof x
  obtain ⟨M, b, rfl⟩ := exists_tof y
  rw [tof_add_hetero, towerJpre_tof, towerJpre_tof, towerJpre_tof, tof_add_hetero]
  congr 1
  rw [towerJlevel_add, ← towerJ_commutes_with_tPush l hl,
      ← towerJ_commutes_with_tPush l hl]

/-- ★★★ **ANTILINEAR NO COLIMITE**: `J(c·x) = c̄·J(x)`. -/
theorem towerJpre_conj_smul (l : ℝ) (hl : 0 < l) (c : ℂ) (x : TowerPre P) :
    towerJpre l hl P (c • x) = (starRingEnd ℂ) c • towerJpre l hl P x := by
  obtain ⟨N, a, rfl⟩ := exists_tof x
  rw [tof_smul, towerJpre_tof, towerJpre_tof, tof_smul, towerJlevel_conj_smul]

/-- ★★ **LEVA ZERO EM ZERO**. -/
theorem towerJpre_zero (l : ℝ) (hl : 0 < l) :
    towerJpre l hl P (0 : TowerPre P) = 0 := by
  show towerJpre l hl P (tof P 0 0) = tof P 0 0
  rw [towerJpre_tof]
  congr 1
  unfold towerJlevel stateJG
  simp

end TGLExt
