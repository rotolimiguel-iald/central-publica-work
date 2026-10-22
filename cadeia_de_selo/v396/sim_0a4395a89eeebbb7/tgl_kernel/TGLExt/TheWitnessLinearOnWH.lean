import TGLExt.TheWitnessOnTheBoundary

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1000000

/-!
# A TESTEMUNHA É ADITIVA E ANTILINEAR EM `WH` — o transporte das duas leis
  [BANCADA — 26/08/2026 · marco M4 · pré-requisito da instanciação]

## O passo

A v242 mostrou que o bicomutante **cai sem von Neumann**, desde que a conjugação por
`J` seja exibida como **mapa multiplicativo involutivo dos operadores contínuos**. Para
construir esse mapa é preciso, antes, que `J` seja **aditiva e antilinear em `WH`** — e
não apenas no pré-espaço, onde já estava provado.

E elas **viajam por densidade**, pelo mesmo lema de sempre: os dois lados são
contínuos, concordam no denso, logo são iguais. É a quinta vez que este lema paga.

## O que se prova

* ★★★ **`towerJ_add`** — aditiva em `WH` inteiro;
* ★★★ **`towerJ_conj_smul`** — **ANTIlinear** em `WH`: `J(c·z) = c̄·J(z)`;
* ★★ `towerJ_zero` — zero em zero;
* ★★ `towerJ_continuous` — contínua (o que permite compor e transportar).

## O QUE ISTO AUTORIZA
Construir `T ↦ J∘T∘J` como aplicação **linear** (duas antilineares compõem em linear) e
**contínua** dos operadores de `WH` — a hipótese `Φ` do teorema da v242. β jamais entra;
nada move o gate.
-/

namespace TGLExt

open UniformSpace

variable {P : SiteProfile}

theorem towerJ_continuous (P : SiteProfile) :
    Continuous (towerJ P) := Completion.continuous_map

/-- ★★★ **ADITIVA EM `WH`** — por densidade. -/
theorem towerJ_add (P : SiteProfile) (z w : TowerHilbert P) :
    towerJ P (z + w) = towerJ P z + towerJ P w := by
  have h1 : Continuous (fun p : TowerHilbert P × TowerHilbert P =>
      towerJ P (p.1 + p.2)) :=
    (towerJ_continuous P).comp continuous_add
  have h2 : Continuous (fun p : TowerHilbert P × TowerHilbert P =>
      towerJ P p.1 + towerJ P p.2) :=
    ((towerJ_continuous P).comp continuous_fst).add
      ((towerJ_continuous P).comp continuous_snd)
  refine Completion.induction_on₂ z w (isClosed_eq h1 h2) ?_
  intro a b
  rw [← Completion.coe_add, towerJ_coe, towerJ_coe, towerJ_coe,
      profileJpre_add, Completion.coe_add]

/-- ★★★ **ANTILINEAR EM `WH`**: `J(c·z) = c̄·J(z)` — por densidade. -/
theorem towerJ_conj_smul (P : SiteProfile) (c : ℂ) (z : TowerHilbert P) :
    towerJ P (c • z) = (starRingEnd ℂ) c • towerJ P z := by
  have h1 : Continuous (fun w : TowerHilbert P => towerJ P (c • w)) :=
    (towerJ_continuous P).comp (continuous_const_smul c)
  have h2 : Continuous (fun w : TowerHilbert P =>
      (starRingEnd ℂ) c • towerJ P w) :=
    (continuous_const_smul _).comp (towerJ_continuous P)
  refine Completion.induction_on z (isClosed_eq h1 h2) ?_
  intro a
  rw [← Completion.coe_smul, towerJ_coe, towerJ_coe, profileJpre_conj_smul,
      Completion.coe_smul]

/-- ★★ **ZERO EM ZERO**. -/
theorem towerJ_zero (P : SiteProfile) :
    towerJ P (0 : TowerHilbert P) = 0 := by
  rw [← Completion.coe_zero, towerJ_coe, profileJpre_zero, Completion.coe_zero]

end TGLExt
