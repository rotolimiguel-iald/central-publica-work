import TGLExt.TheWitnessOnTheBoundary
import TGLExt.TheColimitDuality
import TGLExt.RightMult
import TGLExt.TowerAction

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A DUALIDADE NA FRONTEIRA — `J·π(a)·J = ρ(J a)` em `WH`
  [BANCADA — 26/08/2026 · marco M4 · a dualidade no nível dos OPERADORES CONTÍNUOS]

## O passo

A v240 pôs a testemunha em `WH`. A v237 provou a dualidade no colimite. Falta **casar
as duas**: mostrar que a dualidade vale para os **operadores contínuos** de `WH`, e não
apenas para as multiplicações do pré-espaço.

E ela vale **pelo transporte por densidade** (v225): os dois lados são **contínuos** em
`z` — a testemunha é contínua porque é `Completion.map`, e as ações são contínuas por
construção —, e **concordam no subespaço denso** pela dualidade do colimite. Duas
funções contínuas que concordam no denso são iguais.

## O que se prova

* ★★★ **`boundaryDuality`** — `J(π(a)(J z)) = ρ(J a)(z)` para **TODO `z ∈ WH`**:
  a conjugação leva a ação ESQUERDA na ação DIREITA, **em operadores contínuos**;
* ★★★ `boundaryDuality_centralizes` — e a conjugada de uma esquerda **comuta com toda
  esquerda** em `WH` — a face de `J M J ⊆ M′` **nos geradores como operadores**.

## O QUE FALTA — e agora é UMA coisa só
Estender dos **geradores** `π(a)` ao **BICOMUTANTE** `M = {π(torre)}″`. É o teorema de
von Neumann (fecho algébrico = fecho SOT), que **a mathlib não tem** e que este kernel
já identificara como a contribuição-alvo. Tudo o mais está pago. O razonete lê ABERTO
até esse último passo. β jamais entra. Nada move o gate.
-/

namespace TGLExt

open UniformSpace

variable {P : SiteProfile}

/-- ★★ **DIREITA COMUTA COM ESQUERDA EM `WH`** --- por densidade, a partir do lema do
    pré-espaço que já existia na árvore. -/
theorem rTowerPi_comm_towerPi (P : SiteProfile) {N M : ℕ}
    (y : Matrix (chainIdx N) (chainIdx N) ℂ)
    (x : Matrix (chainIdx M) (chainIdx M) ℂ) (z : TowerHilbert P) :
    rTowerPi P y (towerPi P x z) = towerPi P x (rTowerPi P y z) := by
  have h1 : Continuous (fun w : TowerHilbert P => rTowerPi P y (towerPi P x w)) :=
    (rTowerPi P y).continuous.comp (towerPi P x).continuous
  have h2 : Continuous (fun w : TowerHilbert P => towerPi P x (rTowerPi P y w)) :=
    (towerPi P x).continuous.comp (rTowerPi P y).continuous
  have key : ∀ v : TowerPre P,
      rTowerPi P y (towerPi P x (↑v : TowerHilbert P))
        = towerPi P x (rTowerPi P y (↑v : TowerHilbert P)) := by
    intro v
    rw [towerPi_coe, rTowerPi_coe, rTowerPi_coe, towerPi_coe, rmulPre_comm_lmulPre]
  exact congrFun (identities_travel_by_density _ _ h1 h2 key) z

/-- ★★★ **A DUALIDADE NA FRONTEIRA**: `J·π(a)·J = ρ(J a)` em `WH` inteiro. -/
theorem boundaryDuality (P : SiteProfile) {N : ℕ}
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) (z : TowerHilbert P) :
    towerJ P (towerPi P a (towerJ P z)) = rTowerPi P (profileJlevel P N a) z := by
  have hcont : Continuous
      (fun w : TowerHilbert P => towerJ P (towerPi P a (towerJ P w))) :=
    Completion.continuous_map.comp ((towerPi P a).continuous.comp
      Completion.continuous_map)
  have hcont2 : Continuous
      (fun w : TowerHilbert P => rTowerPi P (profileJlevel P N a) w) :=
    (rTowerPi P (profileJlevel P N a)).continuous
  have key : ∀ v : TowerPre P,
      towerJ P (towerPi P a (towerJ P (↑v : TowerHilbert P)))
        = rTowerPi P (profileJlevel P N a) (↑v : TowerHilbert P) := by
    intro v
    rw [towerJ_coe, towerPi_coe, towerJ_coe, rTowerPi_coe,
        profileJpre_conj_lmul]
  exact congrFun (identities_travel_by_density _ _ hcont hcont2 key) z

/-- ★★★ **E ELA CENTRALIZA EM `WH`**: a conjugada de uma esquerda comuta com toda
    esquerda — a face de `J M J ⊆ M′` nos geradores como operadores contínuos. -/
theorem boundaryDuality_centralizes (P : SiteProfile) {N M : ℕ}
    (a : Matrix (chainIdx N) (chainIdx N) ℂ)
    (c : Matrix (chainIdx M) (chainIdx M) ℂ) (z : TowerHilbert P) :
    towerPi P c (towerJ P (towerPi P a (towerJ P z)))
      = towerJ P (towerPi P a (towerJ P (towerPi P c z))) := by
  rw [boundaryDuality, boundaryDuality]
  exact (rTowerPi_comm_towerPi P (profileJlevel P N a) c z).symm

end TGLExt
