import TGLExt.TheSelectorCanRefuse

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 1600000

/-!
# AS DUAS DOBRAS — `so(4) ≅ su(2) ⊕ su(2)`, e a forma quadrática em 4D que parte em duas
  [BANCADA — 22/08/2026; teste da conjectura do operador]

## A conjectura, verbatim

> *"eu vejo o campo psiônico como um **cubo**, cuja projeção em 3D dentro dele é um **globo**,
> portanto eu vejo uma **forma quadrática em 4D** que forma um globo em 3D."*
>
> *"a **primeira dobra** é a do gráviton, a **segunda** é a do ângulo… o gráviton é a ligação
> do condensado psiônico… o gráviton é a ligação de **dois psions**."*

Esta pedra testa a face **algébrica** dessa tipagem, e só ela. O resultado é exato.

## O que fica provado

* ★★★ `the_two_folds_commute` — **os NOVE comutadores `[L_i, R_j]` são ZERO.** A álgebra das
  rotações em 4D **parte em duas metades que não se falam**: `so(4) = su(2)_L ⊕ su(2)_R`.
  ***Duas rotações 3D independentes dentro de uma forma quadrática 4D*** — que é, letra por
  letra, a conjectura do operador;
* ★★★ `the_left_fold_closes` / `the_right_fold_closes` — cada metade **fecha em si mesma**:
  `[L₁,L₂] = −2L₃` e `[R₁,R₂] = +2R₃`. **Duas cópias de `su(2)`;**
* ★★★ `the_folds_have_opposite_chirality` — e os sinais são **opostos**. As duas dobras não são
  duas cópias iguais: são **as duas faces**, com orientações contrárias. *É a quiralidade da
  cisão, e ela não foi posta: apareceu;*
* ★★★ `the_planes_are_the_sum_and_difference_of_the_folds` — **`P = (L₁+R₁)/2` e
  `Q = (L₁−R₁)/2`**, onde `P` e `Q` giram os dois planos ortogonais do 4D. *A rotação de um
  plano **é** a soma das duas dobras; a do outro, a diferença.* **A "ligação" de que o operador
  fala tem forma exata: é a soma.**
* ★★ `each_fold_is_a_complex_structure` — **todos os seis geradores elevam ao quadrado `−1`**.
  Cada dobra carrega o seu **próprio ângulo**, pela mesma razão de `TheAngleIsTheBridge`;
* ★★ `the_two_planes_commute` — `[P,Q] = 0`: a rotação 4D genérica tem **DOIS ângulos
  independentes**, `θ₁` e `θ₂`. *A família deixa de ser a um parâmetro e passa a ser a dois —
  e são exatamente as duas dobras.*

## A CONTAGEM, continuando `TheSelectorCanRefuse`

| face | equações (`dim so(n)`) | incógnitas | sobredeterminação |
|---|---|---|---|
| 2×2 | 1 | 1 (`θ`) | **0** — mostrador livre |
| 3×3 | 3 | 1 (`θ`) | 2 |
| **4×4** | **6** | **2** (`θ₁`, `θ₂`) | **4** |

A face 4D **continua sobredeterminada** mesmo com o segundo ângulo — e agora com uma
**estrutura** que o 3D não tinha: as duas incógnitas **não são arbitrárias**, são as duas
dobras, e o setor **isoclínico** (`θ₁ = θ₂`) vive **inteiramente numa** delas.

## O QUE ESTA PEDRA NÃO FAZ — a fronteira, dita sem rodeio

Prova-se a **cisão algébrica** de `so(4)` e a forma exata da ligação (`P = (L₁+R₁)/2`).
**Não** se prova que o psion **seja** um fator `su(2)`; **não** se prova que o gráviton **seja**
a ligação; **não** se deriva `θ_M`; e **nada** aqui diz respeito a `c³`, a buracos negros, ou a
qualquer objeto físico.

A identificação `dobra ↔ psion`, `ligação ↔ gráviton`, e a leitura do gráviton como ponto único
inscritor são **[ONTO] do operador**, assinadas por ele, e **não aparecem em enunciado nenhum**.
O que o kernel entrega é que a **forma da conjectura existe e é exata**: uma forma quadrática em
4D **de fato** parte em duas rotações 3D independentes, de quiralidades opostas, cuja **soma**
gira um plano e cuja **diferença** gira o outro.

β jamais entra no Lean. Sem sorry, sem axiom. Nada aqui move o gate.
-/

namespace TGLExt

open Matrix

noncomputable section

/-! ### Os seis geradores: três da dobra esquerda, três da direita -/

/-- Dobra ESQUERDA, gerador 1 (auto-dual). -/
def foldL1 : Matrix (Fin 4) (Fin 4) ℝ := !![0,1,0,0; -1,0,0,0; 0,0,0,1; 0,0,-1,0]
/-- Dobra ESQUERDA, gerador 2. -/
def foldL2 : Matrix (Fin 4) (Fin 4) ℝ := !![0,0,1,0; 0,0,0,-1; -1,0,0,0; 0,1,0,0]
/-- Dobra ESQUERDA, gerador 3. -/
def foldL3 : Matrix (Fin 4) (Fin 4) ℝ := !![0,0,0,1; 0,0,1,0; 0,-1,0,0; -1,0,0,0]

/-- Dobra DIREITA, gerador 1 (anti-auto-dual). -/
def foldR1 : Matrix (Fin 4) (Fin 4) ℝ := !![0,1,0,0; -1,0,0,0; 0,0,0,-1; 0,0,1,0]
/-- Dobra DIREITA, gerador 2. -/
def foldR2 : Matrix (Fin 4) (Fin 4) ℝ := !![0,0,1,0; 0,0,0,1; -1,0,0,0; 0,-1,0,0]
/-- Dobra DIREITA, gerador 3. -/
def foldR3 : Matrix (Fin 4) (Fin 4) ℝ := !![0,0,0,1; 0,0,-1,0; 0,1,0,0; -1,0,0,0]

/-- O gerador da rotação no **primeiro** plano (coordenadas 1–2). -/
def planeP : Matrix (Fin 4) (Fin 4) ℝ := !![0,1,0,0; -1,0,0,0; 0,0,0,0; 0,0,0,0]
/-- O gerador da rotação no **segundo** plano (coordenadas 3–4), ortogonal ao primeiro. -/
def planeQ : Matrix (Fin 4) (Fin 4) ℝ := !![0,0,0,0; 0,0,0,0; 0,0,0,1; 0,0,-1,0]

/-- abreviação do comutador. -/
def comm4 (A B : Matrix (Fin 4) (Fin 4) ℝ) : Matrix (Fin 4) (Fin 4) ℝ := A * B - B * A

/-- tática única desta pedra: tudo é conta entrada a entrada em `Fin 4`. -/
macro "quatro" : tactic =>
  `(tactic| (ext i j; fin_cases i <;> fin_cases j <;>
      simp [foldL1, foldL2, foldL3, foldR1, foldR2, foldR3, planeP, planeQ, comm4,
            Matrix.mul_apply, Fin.sum_univ_four, Matrix.one_apply, Matrix.neg_apply] <;> ring))

/-! ### ★★★ A CISÃO: as duas dobras não se falam -/

/-- ★★★ **OS NOVE COMUTADORES CRUZADOS SÃO ZERO.**
    `[L_i, R_j] = 0` para todo `i, j`. A álgebra das rotações em 4D **parte em duas metades
    independentes** — `so(4) = su(2)_L ⊕ su(2)_R`.

    **Duas rotações 3D independentes dentro de uma forma quadrática 4D.** -/
theorem the_two_folds_commute :
    comm4 foldL1 foldR1 = 0 ∧ comm4 foldL1 foldR2 = 0 ∧ comm4 foldL1 foldR3 = 0
    ∧ comm4 foldL2 foldR1 = 0 ∧ comm4 foldL2 foldR2 = 0 ∧ comm4 foldL2 foldR3 = 0
    ∧ comm4 foldL3 foldR1 = 0 ∧ comm4 foldL3 foldR2 = 0 ∧ comm4 foldL3 foldR3 = 0 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_, ?_⟩ <;> quatro

/-! ### ★★★ Cada dobra fecha em si mesma — e com quiralidades OPOSTAS -/

/-- ★★★ **A DOBRA ESQUERDA FECHA:** `[L₁,L₂] = −2L₃`, e ciclicamente. É uma cópia de `su(2)`. -/
theorem the_left_fold_closes :
    comm4 foldL1 foldL2 = (-2 : ℝ) • foldL3
    ∧ comm4 foldL2 foldL3 = (-2 : ℝ) • foldL1
    ∧ comm4 foldL3 foldL1 = (-2 : ℝ) • foldL2 := by
  refine ⟨?_, ?_, ?_⟩ <;> quatro

/-- ★★★ **A DOBRA DIREITA FECHA:** `[R₁,R₂] = +2R₃`, e ciclicamente. Outra cópia de `su(2)`. -/
theorem the_right_fold_closes :
    comm4 foldR1 foldR2 = (2 : ℝ) • foldR3
    ∧ comm4 foldR2 foldR3 = (2 : ℝ) • foldR1
    ∧ comm4 foldR3 foldR1 = (2 : ℝ) • foldR2 := by
  refine ⟨?_, ?_, ?_⟩ <;> quatro

/-- ★★★ **AS DUAS DOBRAS TÊM QUIRALIDADE OPOSTA.** Os sinais `−2` e `+2` não são convenção:
    são o conteúdo. As duas metades **não são duas cópias iguais** — são **as duas faces**, com
    orientações contrárias. *A quiralidade não foi posta: apareceu.* -/
theorem the_folds_have_opposite_chirality :
    comm4 foldL1 foldL2 = (-2 : ℝ) • foldL3 ∧ comm4 foldR1 foldR2 = (2 : ℝ) • foldR3 :=
  ⟨the_left_fold_closes.1, the_right_fold_closes.1⟩

/-! ### ★★★ A LIGAÇÃO tem forma exata: soma e diferença -/

/-- ★★★ **OS DOIS PLANOS SÃO A SOMA E A DIFERENÇA DAS DUAS DOBRAS.**

    `P = (L₁ + R₁)/2` e `Q = (L₁ − R₁)/2`.

    A rotação de um plano **é a soma** das duas dobras; a do outro plano, **a diferença**.
    *A "ligação" de que o operador fala tem, aqui, forma fechada: é a soma.* -/
theorem the_planes_are_the_sum_and_difference_of_the_folds :
    planeP = (1/2 : ℝ) • (foldL1 + foldR1)
    ∧ planeQ = (1/2 : ℝ) • (foldL1 - foldR1) := by
  constructor <;> quatro

/-- ★★ **OS DOIS PLANOS COMUTAM:** `[P,Q] = 0`. Portanto a rotação 4D genérica tem **DOIS
    ângulos independentes**. *A família deixa de ser a um parâmetro e passa a ser a dois — e
    são exatamente as duas dobras.* -/
theorem the_two_planes_commute : comm4 planeP planeQ = 0 := by quatro

/-! ### ★★ Cada dobra é uma estrutura complexa -/

/-- ★★ **TODOS OS SEIS GERADORES ELEVAM AO QUADRADO `−1`.** Cada dobra carrega o **seu próprio
    ângulo**, pela mesma razão que `TheAngleIsTheBridge` deu para a face 2×2. -/
theorem each_fold_is_a_complex_structure :
    foldL1 * foldL1 = -1 ∧ foldL2 * foldL2 = -1 ∧ foldL3 * foldL3 = -1
    ∧ foldR1 * foldR1 = -1 ∧ foldR2 * foldR2 = -1 ∧ foldR3 * foldR3 = -1 := by
  refine ⟨?_, ?_, ?_, ?_, ?_, ?_⟩ <;> quatro

/-- ★★ o fecho: **cisão**, **quiralidade oposta** e **a ligação como soma** — os três num
    enunciado. A forma da conjectura do operador existe, e é exata. -/
theorem the_quadratic_form_splits_in_two :
    comm4 foldL1 foldR1 = 0
    ∧ (comm4 foldL1 foldL2 = (-2 : ℝ) • foldL3 ∧ comm4 foldR1 foldR2 = (2 : ℝ) • foldR3)
    ∧ planeP = (1/2 : ℝ) • (foldL1 + foldR1) :=
  ⟨the_two_folds_commute.1, the_folds_have_opposite_chirality,
   the_planes_are_the_sum_and_difference_of_the_folds.1⟩

end

end TGLExt
