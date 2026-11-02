import TGLExt.TheAngleIsTheProjection

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 800000

/-!
# A INTERFACE DA LUZ — a escada fatora as faces; o quadrado da luz é o gráviton
  [BANCADA — 24/08/2026 · P1 + P1b do PLANO DA PROVA FINAL]

## A cunhagem do operador

> *"**GRÁVITON = GERADOR DA LUZ** … agora é a luz que deriva da partícula fundamental da
> gravidade, gerando a geometria em consequência disso."*
> *"**LUZ = interface do gráviton em 3D.**"*

## O que se mede antes de se provar (numpy, 24/08)

`ε_± ⊗ ε_± = (h₊ ± i·h×)/2` a resíduo `2,2e−16`; sob rotação do plano transversal o vetor ganha
fase `e^{iθ}` e o tensor ganha `e^{2iθ}` — resíduo máximo `2,5e−16` em 200 ângulos. **O ângulo
DOBRA do vetor para o tensor; a interface toma a raiz do ângulo.**

## ⚠ A DELIMITAÇÃO, antes de qualquer prova

* **NÃO se constrói aqui o fóton físico** — não há campo de Maxwell, não há calibre `U(1)`, não
  há dinâmica. `lightPlus`/`lightMinus` são os **vetores de peso 1** do gerador transversal; a
  identificação com a polarização do fóton é **[KNOWN] em QFT** (os tensores TT do gráviton são
  quadrados dos vetores de polarização do fóton) e **[ONTO]** na leitura do operador.
* `genK` é o gerador da rotação transversal (`SO(2)`), **não** o `J` modular antilinear — o
  kernel expressamente não estende (`TheRecordOfJ`).
* A leitura em regimes de potências de `c` (`c⁰ → c¹ → c² → c³`) é **[CONJ/ONTO]** e **não
  aparece em enunciado nenhum** desta pedra.
* β jamais entra no Lean. Sem sorry, sem axiom. **Nada aqui move o gate.**

## ★★★ OS TEOREMAS

**ATO I — A ESCADA (P1):** com `h_± := h₊ ± i·h×` (raízes de peso `±2i` do gerador):

    genK·h_± − h_±·genK = ±2i·h_±        (o peso 2 — o spin 2 legível como número)
    h_±² = 0                              (cada raiz é nilpotente)
    h₊·h₋ = 4·P₊   e   h₋·h₊ = 4·P₋      (★ A ESCADA FATORA AS PROJEÇÕES do gerador)

*Liga `GravitonPolarization` (as polarizações) a `TheAngleIsTheProjection` (as faces `P±`) —
duas pedras até hoje desligadas.*

**ATO II — A INTERFACE (P1b):** com `ε_± := (1, ±i)` (os vetores da luz):

    ε_± ⊗ ε_± = h_±                       (★ O QUADRADO DA LUZ É O GRÁVITON)
    genK·ε_± = ±i·ε_±                     (o gerador lê a luz a peso 1 — a METADE)
    𝒪_θ·ε₊ = e^{iθ}·ε₊                   (a interface carrega o ângulo…)
    𝒪_θ·h₊·𝒪_θᵀ = (e^{iθ})²·h₊          (…e o tensor carrega o QUADRADO do ângulo)

> **A luz é a interface: o objeto vetorial (3D-legível) cujo quadrado é o tensor do gráviton,
> e cuja fase é a raiz da fase dele.** A equação publicada `g = √|L|` sobrevive intacta —
> só a seta de leitura inverte (a luz como raiz do gráviton, o gráviton como quadrado da luz).

## O que fica provado e o que não

**PROVA-SE:** a fatoração da escada pelas projeções; a fatoração do tensor pelo vetor; os pesos
`1` e `2` do mesmo gerador (a duplicação do ângulo como teorema, infinitesimal e finito).
**NÃO SE PROVA:** que o fóton físico exista, que a luz "venha" do gráviton na natureza, ou
qualquer dinâmica. É a face algébrica da tipagem — exata, e só ela.
-/

namespace TGLExt

open Matrix Complex

noncomputable section

/-- a polarização `+` do gráviton, sobre ℂ (o lift de `polPlus`). -/
def hPlusC : Matrix (Fin 2) (Fin 2) ℂ := !![1, 0; 0, -1]

/-- a polarização `×` do gráviton, sobre ℂ (o lift de `polCross`). -/
def hCrossC : Matrix (Fin 2) (Fin 2) ℂ := !![0, 1; 1, 0]

/-- a raiz de peso `+2i`: `h₊ + i·h×`. -/
def rootPlus : Matrix (Fin 2) (Fin 2) ℂ := hPlusC + Complex.I • hCrossC

/-- a raiz de peso `−2i`: `h₊ − i·h×`. -/
def rootMinus : Matrix (Fin 2) (Fin 2) ℂ := hPlusC - Complex.I • hCrossC

/-- a luz `+`: o vetor `(1, i)` do plano transversal. -/
def lightPlus : Fin 2 → ℂ := ![1, Complex.I]

/-- a luz `−`: o vetor `(1, −i)`. -/
def lightMinus : Fin 2 → ℂ := ![1, -Complex.I]

/-- tática desta pedra, face matricial: conta entrada a entrada em `Fin 2`, `I² = −1` à mão. -/
macro "faces" : tactic =>
  `(tactic| (ext i j; fin_cases i <;> fin_cases j <;>
      simp [hPlusC, hCrossC, rootPlus, rootMinus, lightPlus, lightMinus, genK, projPlus,
            projMinus, angFamily, Matrix.mul_apply, Fin.sum_univ_two, Matrix.one_apply,
            Matrix.add_apply, Matrix.sub_apply, Matrix.smul_apply, Matrix.zero_apply,
            Matrix.transpose_apply, Matrix.vecMulVec, Matrix.of_apply,
            Matrix.cons_val_zero, Matrix.cons_val_one, Matrix.head_cons, Fin.isValue,
            pow_two, Complex.ext_iff, Complex.I_re, Complex.I_im] <;>
      (repeat' constructor) <;> (first | ring | trivial)))

/-- tática desta pedra, face vetorial. -/
macro "feixe" : tactic =>
  `(tactic| (funext i; fin_cases i <;>
      simp [hPlusC, hCrossC, rootPlus, rootMinus, lightPlus, lightMinus, genK, angFamily,
            Matrix.mulVec, dotProduct, Fin.sum_univ_two, Matrix.one_apply, Matrix.add_apply,
            Matrix.sub_apply, Matrix.smul_apply, Matrix.cons_val_zero, Matrix.cons_val_one,
            Matrix.head_cons, Fin.isValue, Pi.smul_apply, smul_eq_mul,
            Complex.ext_iff, Complex.I_re, Complex.I_im] <;>
      (repeat' constructor) <;> (first | ring | trivial)))

/-! ### ATO I — A ESCADA (P1) -/

/-- ★★ **AS DUAS RAÍZES SÃO AS DUAS POLARIZAÇÕES**, sem resto:
    `h₊ = (root₊ + root₋)/2` e `h× = (root₊ − root₋)/2i` — aqui na forma sem divisão. -/
theorem the_two_roots_are_the_two_polarizations :
    rootPlus + rootMinus = (2 : ℂ) • hPlusC
    ∧ rootPlus - rootMinus = (2 * Complex.I) • hCrossC := by
  constructor <;> faces

/-- ★★★ **OS PESOS SÃO `±2i` — o spin 2 legível como número.**
    `[genK, root₊] = +2i·root₊` e `[genK, root₋] = −2i·root₋`. *É a forma infinitesimal do
    `e^{±2iθ}` que `GravitonPolarization` prova na forma finita.* -/
theorem the_ladder_weights_are_plus_minus_two :
    genK * rootPlus - rootPlus * genK = (2 * Complex.I) • rootPlus
    ∧ genK * rootMinus - rootMinus * genK = (-(2 * Complex.I)) • rootMinus := by
  constructor <;> faces

/-- ★★ **CADA RAIZ É NILPOTENTE:** `root_±² = 0`. *Subir duas vezes não há para onde: o setor
    tem exatamente dois pesos.* -/
theorem the_roots_are_nilpotent :
    rootPlus * rootPlus = 0 ∧ rootMinus * rootMinus = 0 := by
  constructor <;> faces

/-- ★★★ **A ESCADA FATORA AS PROJEÇÕES.**

    `root₊ · root₋ = 4·P₊`   e   `root₋ · root₊ = 4·P₋`

    As faces espectrais do gerador (`TheAngleIsTheProjection`) **fatoram-se pelas polarizações
    do gráviton** — as duas pedras eram uma. -/
theorem the_ladder_factors_the_projections :
    rootPlus * rootMinus = (4 : ℂ) • projPlus
    ∧ rootMinus * rootPlus = (4 : ℂ) • projMinus := by
  constructor <;> faces

/-! ### ATO II — A INTERFACE (P1b) -/

/-- ★★★ **O QUADRADO DA LUZ É O GRÁVITON.**

    `ε_± ⊗ ε_± = root_±`

    O tensor de polarização do gráviton **fatora como o quadrado do vetor da luz** — sem
    normalização escondida, igualdade exata de matrizes. -/
theorem the_light_squares_to_the_graviton :
    Matrix.vecMulVec lightPlus lightPlus = rootPlus
    ∧ Matrix.vecMulVec lightMinus lightMinus = rootMinus := by
  constructor <;> faces

/-- ★★★ **O GERADOR LÊ A LUZ A PESO 1 — a metade do peso do gráviton.**
    `genK·ε_± = ±i·ε_±`. *O vetor carrega peso 1; o seu quadrado (o gráviton) carrega peso 2:
    a duplicação do ângulo é teorema.* -/
theorem the_generator_reads_the_light_at_half_weight :
    genK.mulVec lightPlus = Complex.I • lightPlus
    ∧ genK.mulVec lightMinus = (-Complex.I) • lightMinus := by
  constructor <;> feixe

/-- ★★ **A INTERFACE CARREGA O ÂNGULO** (forma finita, vetorial):
    `𝒪_θ · ε₊ = e^{iθ} · ε₊`. -/
theorem the_interface_reads_the_angle (θ : ℝ) :
    (angFamily θ).mulVec lightPlus = Complex.exp (θ * Complex.I) • lightPlus := by
  have hp : Complex.exp ((θ : ℂ) * Complex.I)
      = (Real.cos θ : ℂ) + (Real.sin θ : ℂ) * Complex.I := by
    rw [Complex.exp_mul_I, ← Complex.ofReal_cos, ← Complex.ofReal_sin]
  rw [hp]
  feixe

/-- ★★★ **O TENSOR CARREGA O QUADRADO DO ÂNGULO** (forma finita, tensorial):

    `𝒪_θ · root₊ · 𝒪_θᵀ = (e^{iθ})² · root₊`

    *A fase do gráviton é o QUADRADO da fase da luz — a equação publicada `g = √|L|` lida na
    direção inversa: a luz é a raiz.* -/
theorem the_tensor_squares_the_phase (θ : ℝ) :
    angFamily θ * rootPlus * (angFamily θ).transpose
      = (Complex.exp (θ * Complex.I)) ^ 2 • rootPlus := by
  have hp : Complex.exp ((θ : ℂ) * Complex.I)
      = (Real.cos θ : ℂ) + (Real.sin θ : ℂ) * Complex.I := by
    rw [Complex.exp_mul_I, ← Complex.ofReal_cos, ← Complex.ofReal_sin]
  rw [hp]
  faces

/-- ★ o fecho, num enunciado: **a luz é a interface do gráviton** — o quadrado do vetor é o
    tensor, o gerador lê o vetor à metade do peso com que lê o tensor. -/
theorem the_light_is_the_interface_of_the_graviton :
    Matrix.vecMulVec lightPlus lightPlus = rootPlus
    ∧ genK.mulVec lightPlus = Complex.I • lightPlus
    ∧ genK * rootPlus - rootPlus * genK = (2 * Complex.I) • rootPlus :=
  ⟨the_light_squares_to_the_graviton.1,
   the_generator_reads_the_light_at_half_weight.1,
   the_ladder_weights_are_plus_minus_two.1⟩

end

end TGLExt
