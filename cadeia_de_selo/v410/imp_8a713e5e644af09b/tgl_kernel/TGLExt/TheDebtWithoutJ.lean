import TGLExt.TheFoldThroughJ
import TGLExt.TheMatrixAndTheModulator

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 1000000

/-!
# A DÍVIDA SEM `J` — a oitava cláusula na forma clássica
  [TGLExt — a pedra de 28/08/2026]

## O que esta pedra faz

A oitava cláusula do certificado condicional fala de `J`. Esta pedra **tira `J` do
enunciado da dívida**, deixando-a na forma canônica do teorema de comutação:

> **o comutante da ação à DIREITA cabe no bicomutante da ESQUERDA.**

A rota tem duas pernas, e nenhuma delas existia:

* ★★★ `profileJlevel_involutive` — `J(Ja) = a` **no andar**. O kernel tinha
  `towerJ_involutive` (no completamento) e `conjByJ_involutive` (nos operadores), mas
  **não** a involutividade da conjugação de nível, que é o que a segunda inclusão pede;
* ★★★ `rTowerImage` — a **imagem da ação à direita** como conjunto. Não existia: havia
  `rTowerPi` (o operador) e a pertinência ao comutante, mas nunca o conjunto.

Com as duas:

* ★★★★★ `conjByJ_towerImage_eq_rTowerImage` — **`J·M·J = R` exatamente**, as duas
  inclusões. Mais forte que `conjByJ_towerImage_in_commutant` (v243), que só dava
  `J·M·J ⊆ M′`. A conjugada da ação à esquerda **É** a ação à direita, nem mais nem
  menos;
* ★★★★★ `the_eighth_clause_without_J` — e então a cláusula **equivale** a
  `R′ ⊆ M″`, **sem `J` nenhum**.

## ⚠ O QUE ISTO É, e o que NÃO É

**É** uma reformulação **exata** — equivalência, não implicação. O valor não é encurtar
a dívida (ela não encolhe), é **removê-la do vocabulário modular** e pô-la na forma em
que a literatura a reconhece: *comutante da direita dentro do bicomutante da esquerda*.
Quem for pagá-la — aqui ou por importação — passa a poder citar o teorema pelo nome.

**NÃO É** prova da cláusula. `red_clause_JMJ_contains` continua apagada, e
`qgConverse_JMJ_contains_commutant` continua sem referente.

⚠ E a metade fácil continua sendo a metade fácil: `M″ ⊆ R′` já sai de esquerda e direita
comutarem (`rTowerPi_comm_towerPi`). O que falta é a **outra** inclusão, e ela é o
teorema de comutação — analítico, `[KNOWN]`, não conjuntista.

β jamais literal. Sem sorry, sem axiom. Nada aqui acende bandeira nem move o gate.
-/

namespace TGLExt

open Matrix

noncomputable section

/-! ## A — a involutividade que faltava, no ANDAR -/

/-- [KERNEL] ★★★ **`J(Ja) = a` NO ANDAR.** O kernel tinha a involutividade no
    completamento (`towerJ_involutive`) e nos operadores (`conjByJ_involutive`), mas não
    esta — e é ela que a segunda inclusão de §B exige.

    Conta exata: as duas diagonais são hermitianas e se cancelam aos pares. -/
theorem profileJlevel_involutive (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    profileJlevel P N (profileJlevel P N a) = a := by
  rw [profileJlevel_eq, profileJlevel_eq]
  rw [conjTranspose_mul, conjTranspose_mul, profileRootInv_isHermitian,
    profileRoot_isHermitian, conjTranspose_conjTranspose]
  simp only [← Matrix.mul_assoc]
  rw [profileRoot_mul_inv, Matrix.one_mul]
  simp only [Matrix.mul_assoc]
  rw [profileRoot_mul_inv, Matrix.mul_one]

/-! ## B — a imagem da ação à DIREITA, e a igualdade exata -/

/-- **A IMAGEM DA AÇÃO À DIREITA** — o espelho de `towerImage`. Não existia como
    conjunto: havia o operador `rTowerPi` e a pertinência ao comutante, nunca o objeto. -/
def rTowerImage (P : SiteProfile) :
    Set (TowerHilbert P →L[ℂ] TowerHilbert P) :=
  {T | ∃ (N : ℕ) (y : Matrix (chainIdx N) (chainIdx N) ℂ), T = rTowerPi P y}

/-- [KERNEL] ★★★★★ **`J·M·J = R`, EXATAMENTE.** A conjugada da ação à esquerda **É** a
    ação à direita — as duas inclusões, não uma.

    Mais forte que `conjByJ_towerImage_in_commutant` (v243), que dava apenas
    `J·M·J ⊆ M′`. A volta usa `profileJlevel_involutive`: dado `r(y)`, o pré-imagem é
    `π(Jy)`. -/
theorem conjByJ_towerImage_eq_rTowerImage (P : SiteProfile) :
    conjByJ P '' (towerImage P) = rTowerImage P := by
  ext T
  constructor
  · rintro ⟨_, ⟨N, x, rfl⟩, rfl⟩
    exact ⟨N, profileJlevel P N x, conjByJ_towerPi P x⟩
  · rintro ⟨N, y, rfl⟩
    refine ⟨towerPi P (profileJlevel P N y), ⟨N, profileJlevel P N y, rfl⟩, ?_⟩
    rw [conjByJ_towerPi, profileJlevel_involutive]

/-! ## C — a dívida, sem `J` -/

/-- [KERNEL] ★★★★★ **A OITAVA CLÁUSULA, SEM `J`**: ela **equivale** a dizer que o
    comutante da ação à DIREITA cabe no bicomutante da ESQUERDA.

    Equivalência, não implicação: a dívida **não encolhe**. O que muda é o vocabulário —
    ela sai da linguagem modular e entra na forma clássica do teorema de comutação, em
    que a literatura a reconhece pelo nome. -/
theorem the_eighth_clause_without_J (P : SiteProfile) :
    (commutantSet (towerImage P)
        ⊆ conjByJ P '' (commutantSet (commutantSet (towerImage P))))
      ↔ commutantSet (rTowerImage P)
        ⊆ commutantSet (commutantSet (towerImage P)) := by
  rw [fold_through_an_involution (conjByJ P) (conjByJ_involutive P)]
  rw [conjByJ_commutant, conjByJ_towerImage_eq_rTowerImage]

/-- [KERNEL] ★★★ **E A METADE FÁCIL CONTINUA FÁCIL**: `M″ ⊆ R′` sai de esquerda e
    direita comutarem. Registrado ao lado para que a dívida fique nítida: **falta a
    outra inclusão, e só ela.** -/
theorem the_easy_half_without_J (P : SiteProfile) :
    commutantSet (commutantSet (towerImage P)) ⊆ commutantSet (rTowerImage P) := by
  rw [← conjByJ_towerImage_eq_rTowerImage]
  exact the_paid_half_of_the_eighth_clause P

/-- [KERNEL] ★★★★ **A DÍVIDA É UMA IGUALDADE DE COMUTANTES, SEM `J`.** Juntando: a
    cláusula equivale a `R′ = M″`, e uma das inclusões já é teorema.

    Esta é a forma final da oitava cláusula depois do trabalho de hoje: **nem `J`, nem
    bicomutante do lado errado — apenas o comutante da direita contra o bicomutante da
    esquerda, com metade paga.** -/
theorem the_debt_is_an_equality_without_J (P : SiteProfile) :
    (commutantSet (towerImage P)
        ⊆ conjByJ P '' (commutantSet (commutantSet (towerImage P))))
      ↔ commutantSet (rTowerImage P) = commutantSet (commutantSet (towerImage P)) := by
  rw [the_eighth_clause_without_J]
  constructor
  · intro h
    exact Set.Subset.antisymm h (the_easy_half_without_J P)
  · intro h
    rw [h]

end

end TGLExt
