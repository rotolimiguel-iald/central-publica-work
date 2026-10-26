import TGLExt.LeftRight

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 400000

/-!
# A BIRREFERENCIALIDADE DO VÁCUO — duas referências, um vácuo, e J entre elas
  [BANCADA — 24/08/2026 · a face finita do P4 do PLANO]

## A cunhagem do operador

> *"…a inscrição do vácuo como **separador da fronteira** e **conjugador modular**… a
> **birreferencialidade do vácuo**…"*

## ⚠ A DELIMITAÇÃO, antes de qualquer prova

Esta é a **face finita** (`Mₙ(ℂ)` na forma GNS do traço). A rede de cunhas do canônico
(`WedgeNet` sobre a torre `WH`) tem o comutante **por definição** (`commAlg` = centralizador)
e **nenhum J** — a cláusula `JMJ = M′` no nível da torre segue **[OPEN]**, pré-requisito da
flag `modular_realization_constructed`. O que se prova aqui é o CONTEÚDO que aquela cláusula
exigirá, no único nível onde ele é hoje demonstrável. A identificação com o vácuo físico é
**[ONTO]** do operador. Nada aqui move o gate.

## ★★★ OS TEOREMAS — a palavra "birreferencialidade" vira enunciado

Com `Ω := 1` (o vetor GNS do traço), `L`/`R` as duas multiplicações e `J z = zᴴ`:

    Ω separa a referência esquerda:   L_a Ω = 0  ⟹  a = 0
    Ω é cíclico para a direita:       ∀ z, ∃ b, R_b Ω = z      (EXATO, não só denso)
    (e simetricamente: separa R, cíclico para L — o MESMO vácuo, DUAS referências)
    dualidade de Haag da mini-rede:   net(dir)′ = net(esq)      (TEOREMA, não fiat)
    J troca as referências:           ∀ b, ∃ a, J L_a J = R_b
    o vácuo é J-fixo:                 J Ω = Ω

> **O separador é o mesmo objeto que sustenta as duas referências, e o conjugador que ele
> define é o dicionário entre elas.** A frase do operador, lida na face finita, é teorema.
-/

namespace TGLExt

open Matrix

variable {n : Type} [Fintype n] [DecidableEq n]

/-- a mini-rede de duas cunhas: a direita carrega `L`, a esquerda carrega `R`. -/
def miniNet : Bool → Set (Module.End ℂ (Matrix n n ℂ))
  | true => Set.range (Lmul (n := n))
  | false => Set.range (Rmul (n := n))

/-- ★★★ **O VÁCUO SEPARA A REFERÊNCIA ESQUERDA**: `L_a Ω = 0 ⟹ a = 0`. -/
theorem vacuum_separates_left (a : Matrix n n ℂ)
    (h : Lmul a (1 : Matrix n n ℂ) = 0) : a = 0 := by
  simpa using h

/-- ★★★ **O MESMO VÁCUO É CÍCLICO PARA A DIREITA** — exatamente, não só denso. -/
theorem vacuum_cyclic_right (z : Matrix n n ℂ) :
    ∃ b, Rmul b (1 : Matrix n n ℂ) = z :=
  ⟨z, by simp⟩

/-- ★★ o par simétrico: o vácuo separa a direita… -/
theorem vacuum_separates_right (b : Matrix n n ℂ)
    (h : Rmul b (1 : Matrix n n ℂ) = 0) : b = 0 := by
  simpa using h

/-- ★★ …e é cíclico para a esquerda. **Um vácuo, duas referências.** -/
theorem vacuum_cyclic_left (z : Matrix n n ℂ) :
    ∃ a, Lmul a (1 : Matrix n n ℂ) = z :=
  ⟨z, by simp⟩

/-- ★★★ **A DUALIDADE DE HAAG DA MINI-REDE É TEOREMA** (na rede da torre ela é
    definição — aqui ela se PROVA): `net(dir)′ = net(esq)`. -/
theorem mini_haag_duality_right :
    commutantSet (miniNet (n := n) true) = miniNet (n := n) false := by
  show commutantSet (Set.range (Lmul (n := n))) = Set.range (Rmul (n := n))
  exact commutant_range_Lmul

/-- ★★ o simétrico: `net(esq)′ = net(dir)`. **Cada referência é o comutante da outra.** -/
theorem mini_haag_duality_left :
    commutantSet (miniNet (n := n) false) = miniNet (n := n) true := by
  show commutantSet (Set.range (Rmul (n := n))) = Set.range (Lmul (n := n))
  exact commutant_range_Rmul

/-- ★★★ **J TROCA AS REFERÊNCIAS** — a metade de Tomita lida como fato da REDE. -/
theorem J_exchanges_the_references (b : Matrix n n ℂ) :
    ∃ a, ∀ z, Jconj (Lmul a (Jconj z)) = Rmul b z :=
  exists_Jconj_conj_Lmul b

/-- ★ **O VÁCUO É J-FIXO**: o conjugador não move o separador. -/
theorem vacuum_J_fixed : Jconj (1 : Matrix n n ℂ) = (1 : Matrix n n ℂ) := by
  simp [Jconj]

/-- ★★★ **A BIRREFERENCIALIDADE DO VÁCUO**, num enunciado só: o mesmo `Ω` separa uma
    referência e é cíclico para a outra; as duas são mutuamente comutantes por TEOREMA;
    `J` — definido do próprio par `(M, Ω)` — leva uma na outra e fixa `Ω`. -/
theorem the_bireference_of_the_vacuum :
    (∀ a : Matrix n n ℂ, Lmul a (1 : Matrix n n ℂ) = 0 → a = 0)
    ∧ (∀ z : Matrix n n ℂ, ∃ b, Rmul b (1 : Matrix n n ℂ) = z)
    ∧ commutantSet (miniNet (n := n) true) = miniNet (n := n) false
    ∧ (∀ b : Matrix n n ℂ, ∃ a, ∀ z, Jconj (Lmul a (Jconj z)) = Rmul b z)
    ∧ Jconj (1 : Matrix n n ℂ) = (1 : Matrix n n ℂ) :=
  ⟨vacuum_separates_left, vacuum_cyclic_right, mini_haag_duality_right,
   J_exchanges_the_references, vacuum_J_fixed⟩

end TGLExt
