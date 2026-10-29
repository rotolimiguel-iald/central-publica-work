import TGLExt.TowerModular
import TGLExt.TheIALDInTheTowerActII

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A CONJUGAÇÃO MODULAR DA TORRE REAL — o pagamento da dívida começa aqui
  [BANCADA — 26/08/2026 · ordem do operador: «pague» · marco M4, item 4 da dívida]

## O que a reconhecimento revelou

A torre **já está inteira** nesta árvore: `TowerPre` (o colimite), `TowerHilbert =
Completion (TowerPre)`, `hOmega` com `‖Ω‖=1`, a densidade `chainDensity`, o **fluxo
modular** `towerFlow` e KMS. **Faltava a CONJUGAÇÃO `J`** — e faltava porque ela exige
a RAIZ da densidade, que ninguém tinha construído.

E há uma coincidência que não é coincidência: `towerStep a = a ⊗ₖ 1` é **exatamente** a
inclusão do Ato II (v216), e `chainDensity (N+1) = chainDensity N ⊗ₖ powersDensity` é
**exatamente** o andar composto do estado-produto. O teorema do entrelaçamento aplica-se
**direto** à torre real.

## O que esta pedra constrói e prova

* `powersRoot` / `powersRootInv` — a raiz da densidade de Powers e sua inversa,
  diagonais explícitas, com `powersRoot_sq` (raiz² = densidade) e o par inverso;
* `chainRoot` / `chainRootInv` — a raiz em TODO andar, pela MESMA recursão da
  densidade (`⊗ₖ` a cada degrau), com `chainRoot_sq` por indução;
* ★★ `chainRoot_isHermitian` — a raiz é hermitiana em todo andar (indução);
* ★★★ **`towerJ_commutes_with_step`** — **A CONJUGAÇÃO ATRAVESSA O DEGRAU**:
  `J_{N+1}(towerStep a) = towerStep (J_N a)`. É ESTA a condição que faz `J` descer ao
  quociente `TowerPre` — sem ela não há `J` no colimite, e sem `J` no colimite não há
  habitante. O Ato II (v216) era exatamente isto, em forma abstrata.

## O QUE AINDA FALTA (dito, sem véu)
Descer ao quociente (`Quotient.map` com esta compatibilidade), estender ao completamento
(v225 dá o mecanismo), e provar as duas cláusulas de comutante contra `theFactorObject`
e `commAlg`. A dívida só se paga quando o `ModularRealizationCertificate` for HABITADO —
até lá o razonete lê ABERTO, e deve. β jamais entra. Nada move o gate.
-/

namespace TGLExt

open Matrix
open scoped Kronecker

/-- a RAIZ da densidade de Powers: diagonal das raízes dos pesos. -/
noncomputable def powersRoot (l : ℝ) : Matrix (Fin 2) (Fin 2) ℂ :=
  diagonal fun i =>
    if i = 0 then ((Real.sqrt (l / (1 + l)) : ℝ) : ℂ)
    else ((Real.sqrt (1 / (1 + l)) : ℝ) : ℂ)

/-- a inversa da raiz. -/
noncomputable def powersRootInv (l : ℝ) : Matrix (Fin 2) (Fin 2) ℂ :=
  diagonal fun i =>
    if i = 0 then ((1 / Real.sqrt (l / (1 + l)) : ℝ) : ℂ)
    else ((1 / Real.sqrt (1 / (1 + l)) : ℝ) : ℂ)

/-- ★ **A RAIZ AO QUADRADO É A DENSIDADE**. -/
theorem powersRoot_sq (l : ℝ) (hl : 0 < l) :
    powersRoot l * powersRoot l = powersDensity l := by
  have h1 : (0:ℝ) < 1 + l := by linarith
  have ha : (0:ℝ) ≤ l / (1 + l) := le_of_lt (div_pos hl h1)
  have hb : (0:ℝ) ≤ 1 / (1 + l) := le_of_lt (div_pos one_pos h1)
  unfold powersRoot powersDensity
  rw [diagonal_mul_diagonal]
  congr 1
  funext i
  by_cases h : i = 0
  · simp only [h, eq_self_iff_true, if_true]
    rw [← Complex.ofReal_mul, Real.mul_self_sqrt ha]
  · simp only [if_neg h]
    rw [← Complex.ofReal_mul, Real.mul_self_sqrt hb]

/-- ★ **O PAR INVERSO DA RAIZ**. -/
theorem powersRoot_mul_inv (l : ℝ) (hl : 0 < l) :
    powersRoot l * powersRootInv l = 1 := by
  have h1 : (0:ℝ) < 1 + l := by linarith
  have ha : (0:ℝ) < Real.sqrt (l / (1 + l)) := Real.sqrt_pos.mpr (div_pos hl h1)
  have hb : (0:ℝ) < Real.sqrt (1 / (1 + l)) := Real.sqrt_pos.mpr (div_pos one_pos h1)
  unfold powersRoot powersRootInv
  rw [diagonal_mul_diagonal, ← diagonal_one]
  congr 1
  funext i
  by_cases h : i = 0
  · simp only [h, eq_self_iff_true, if_true]
    rw [← Complex.ofReal_mul, mul_one_div, div_self (ne_of_gt ha),
        Complex.ofReal_one]
  · simp only [if_neg h]
    rw [← Complex.ofReal_mul, mul_one_div, div_self (ne_of_gt hb),
        Complex.ofReal_one]

/-- ★ a raiz de Powers é hermitiana (diagonal real). -/
theorem powersRoot_isHermitian (l : ℝ) : (powersRoot l)ᴴ = powersRoot l := by
  unfold powersRoot
  rw [diagonal_conjTranspose]
  congr 1
  funext i
  by_cases h : i = 0 <;> simp [h, Complex.conj_ofReal]

/-- a RAIZ da densidade em todo andar — MESMA recursão da densidade. -/
noncomputable def chainRoot (l : ℝ) : (N : ℕ) → Matrix (chainIdx N) (chainIdx N) ℂ
  | 0 => powersRoot l
  | N + 1 => chainRoot l N ⊗ₖ powersRoot l

/-- a inversa da raiz em todo andar. -/
noncomputable def chainRootInv (l : ℝ) : (N : ℕ) → Matrix (chainIdx N) (chainIdx N) ℂ
  | 0 => powersRootInv l
  | N + 1 => chainRootInv l N ⊗ₖ powersRootInv l

/-- ★★ **A RAIZ AO QUADRADO É A DENSIDADE, EM TODO ANDAR** (indução). -/
theorem chainRoot_sq (l : ℝ) (hl : 0 < l) :
    ∀ N : ℕ, chainRoot l N * chainRoot l N = chainDensity l N
  | 0 => powersRoot_sq l hl
  | N + 1 => by
      show (chainRoot l N ⊗ₖ powersRoot l) * (chainRoot l N ⊗ₖ powersRoot l)
        = chainDensity l N ⊗ₖ powersDensity l
      rw [← mul_kronecker_mul, chainRoot_sq l hl N, powersRoot_sq l hl]

/-- ★★ **O PAR INVERSO, EM TODO ANDAR** (indução). -/
theorem chainRoot_mul_inv (l : ℝ) (hl : 0 < l) :
    ∀ N : ℕ, chainRoot l N * chainRootInv l N = 1
  | 0 => powersRoot_mul_inv l hl
  | N + 1 => by
      show (chainRoot l N ⊗ₖ powersRoot l) * (chainRootInv l N ⊗ₖ powersRootInv l) = 1
      rw [← mul_kronecker_mul, chainRoot_mul_inv l hl N, powersRoot_mul_inv l hl,
          one_kronecker_one]

/-- ★★ **A RAIZ É HERMITIANA EM TODO ANDAR** (indução). -/
theorem chainRoot_isHermitian (l : ℝ) :
    ∀ N : ℕ, (chainRoot l N)ᴴ = chainRoot l N
  | 0 => powersRoot_isHermitian l
  | N + 1 => by
      show (chainRoot l N ⊗ₖ powersRoot l)ᴴ = chainRoot l N ⊗ₖ powersRoot l
      rw [conjTranspose_kronecker, chainRoot_isHermitian l N, powersRoot_isHermitian l]

/-- **A CONJUGAÇÃO MODULAR NO ANDAR N**: `J_N(a) = ρ_N^{1/2} · aᴴ · ρ_N^{-1/2}`. -/
noncomputable def towerJlevel (l : ℝ) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) : Matrix (chainIdx N) (chainIdx N) ℂ :=
  stateJG (chainRoot l N) (chainRootInv l N) a

/-- ★★★ **A CONJUGAÇÃO ATRAVESSA O DEGRAU DA TORRE**:
    `J_{N+1}(towerStep a) = towerStep (J_N a)`.
    É ESTA compatibilidade que faz `J` descer ao quociente `TowerPre` — o Ato II (v216)
    em forma abstrata, agora aplicado à torre CONCRETA de Araki–Woods. -/
theorem towerJ_commutes_with_step (l : ℝ) (hl : 0 < l) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    towerJlevel l (N + 1) (towerStep a) = towerStep (towerJlevel l N a) := by
  unfold towerJlevel towerStep
  show stateJG (chainRoot l N ⊗ₖ powersRoot l) (chainRootInv l N ⊗ₖ powersRootInv l)
      (a ⊗ₖ (1 : Matrix (Fin 2) (Fin 2) ℂ))
    = stateJG (chainRoot l N) (chainRootInv l N) a ⊗ₖ (1 : Matrix (Fin 2) (Fin 2) ℂ)
  exact the_tower_interlaces (chainRoot l N) (chainRootInv l N) (powersRoot l)
    (powersRootInv l) (powersRoot_mul_inv l hl) a

end TGLExt
