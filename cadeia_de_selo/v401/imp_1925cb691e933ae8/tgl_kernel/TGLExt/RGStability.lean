import TGLExt.CornerFamily

set_option autoImplicit false
set_option linter.unusedSectionVars false

/-!
# A estabilidade do canto sob renormalização — o gate 8 tipado   [TGLExt — v51]

A pergunta crucial do roadmap: "o canto P_F·C·P_F é estável sob o fluxo
de renormalização?" — e a conjectura "β_RG ↔ fluxo modular ou sua
projeção". O que este arquivo PROVA [KERNEL]:

* ★ **O CANTO É PONTO FIXO DA COARSE-GRAINING** (`Ecomp_fixes_cornerProj`):
  a esperança condicional do produto cruzado (o passo de
  renormalização por blocos) FIXA a família do canto;
* ★ **O CANTO É PONTO FIXO DO FLUXO DISSIPATIVO**
  (`dephase_fixes_cornerProj`): o dephasing (v43, o semigrupo de
  Davies da casa) NÃO move o canto — composição limpa de
  `dephase_fixes_diagonal` (v43) com a diagonalidade do canto (v46);
* junto com `cornerProj_comm_modPow` (v46: o canto comuta com o fluxo
  modular do peso dual), o canto é ESTÁVEL sob as TRÊS dinâmicas da
  casa: coarse-graining, dissipação e fluxo modular — a resposta
  finita à pergunta do gate 8 é SIM;
* ★ **O PASSO DE RG DOBRA O ANIQUILADOR MODULAR**
  (`rg_step_doubles_annihilator`): um refinamento diádico da escada
  (v45) leva s_n = 2π·2ⁿ em s_{n+1} = 2·s_n — a primeira âncora TIPADA
  da conjectura "β_RG ↔ fluxo modular": o passo de escala É um passo
  na torre dos aniquiladores modulares.

**HONESTIDADE.** É a face FINITA da estabilidade de RG. O que segue
OPEN (nomeado): matéria INTERAGENTE genuína (campos de gauge, férmions,
anomalias) e a estabilidade do tipo III₁ sob o fluxo de renormalização
— pesquisa de contínuo. Nota estrutural [leitura]: os teoremas do
produto cruzado (v44) e do canto (v46) valem para G GENÉRICO — a
uniformidade sob extensão de grupo (Z₂ → S₃ → ...) é a forma finita da
estabilidade sob acréscimo de sabor. β JAMAIS entra. Sem sorry, sem
axiom. Negativo honesto é resultado.
-/

namespace TGLExt

open Matrix

noncomputable section

variable {G : Type} [Group G] [Fintype G] [DecidableEq G]
variable {n : Type} [Fintype n] [DecidableEq n]

/-! ## A — o canto é ponto fixo da coarse-graining e da dissipação -/

/-- [KERNEL] ★ A COARSE-GRAINING FIXA O CANTO: `E(P(S)) = P(S)` — a
    esperança condicional por blocos (o passo de renormalização do
    produto cruzado) não move a família do canto. -/
theorem Ecomp_fixes_cornerProj (S : Finset G) :
    Ecomp (cornerProj (n := n) S) = cornerProj S := by
  ext p q
  rcases eq_or_ne p q with h | h
  · subst h
    simp [Ecomp_apply]
  · have hzero : cornerProj (n := n) S p q = 0 := by
      simp [cornerProj_apply, h]
    simp only [Ecomp_apply, hzero, ite_self]

/-- [KERNEL] ★ A DISSIPAÇÃO FIXA O CANTO: `D_t(P(S)) = P(S)` — o
    dephasing (o semigrupo de Davies da casa, v43) não move o canto:
    composição de `dephase_fixes_diagonal` (v43) com a diagonalidade da
    família (v46). Com `cornerProj_comm_modPow` (v46), o canto é estável
    sob coarse-graining + dissipação + fluxo modular: a resposta finita
    ao gate 8 é SIM. -/
theorem dephase_fixes_cornerProj (g : (G × n) → (G × n) → ℝ)
    (hg0 : ∀ p, g p p = 0) (t : ℝ) (S : Finset G) :
    dephase g t (cornerProj (n := n) S) = cornerProj S := by
  have h : cornerProj (n := n) S
      = diagExpect (cornerProj (n := n) S) := by
    unfold cornerProj
    rw [diagExpect_diagonal]
  rw [h, dephase_fixes_diagonal g hg0 t]

/-! ## B — o passo de RG na torre dos aniquiladores -/

/-- [KERNEL] ★ O PASSO DE RG DOBRA O ANIQUILADOR: `s_n·2 = s_{n+1}` para
    `s_n = 2π·2ⁿ` — um refinamento diádico da escada (v45) é um passo na
    torre dos aniquiladores modulares: a primeira âncora TIPADA da
    conjectura β_RG ↔ fluxo modular. -/
theorem rg_step_doubles_annihilator (m : ℕ) :
    (2 * Real.pi * 2 ^ m) * 2 = 2 * Real.pi * 2 ^ (m + 1) := by
  rw [pow_succ]
  ring

end

end TGLExt
