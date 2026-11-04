import TGLExt.RightMult
import TGLExt.TheProfileConjugation
import TGLExt.TheProfileIsometry
import TGLExt.TheColimitDuality

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 1000000

/-!
# A MATRIZ E O MODULADOR DA TORRE — `S` e `Δ` sobre o perfil
  [TGLExt — a pedra de 28/08/2026]

## A ordem do operador

> *"construa a matriz e o modulador da torre — `S` e `Δ` sobre `TowerHilbert P`."*

E o motivo, medido na v274: sem `S` e `Δ` na torre, as frases *"`towerJ` é o J modular
do par"* e *"para esse J, `J M J = M′"`* **não são separáveis no vocabulário da árvore**
— e por isso a importação de Tomita teve de carregar as duas juntas num campo só.

## O que esta pedra constrói `[REAL]`

Os três objetos, **no andar** (matrizes finitas), com a fórmula do perfil:

| objeto | definição | papel |
|---|---|---|
| `towerSlevel` | `a ↦ aᴴ` | **A MATRIZ** — o operador `S` de Tomita |
| `towerDeltaHalfLevel` | `a ↦ ρ^{1/2}·a·ρ^{-1/2}` | **O MODULADOR** — `Δ^{1/2}` |
| `towerDeltaLevel` | `a ↦ ρ·a·ρ^{-1}` | `Δ`, o operador modular |

e as **quatro relações que os amarram**:

* ★★ `profileRoot_sq` — `ρ^{1/2}·ρ^{1/2} = ρ`. A raiz é raiz: sem isto nada abaixo fecha;
* ★★★★★ `the_polar_decomposition_at_the_level` — **`J ∘ Δ^{1/2} = S`**. A decomposição
  polar de Tomita, no andar, por conta exata. É ela que faz de `towerJ` o candidato
  legítimo a conjugação modular — e não uma torção qualquer com o nome certo;
* ★★★ `delta_is_the_square_of_its_half` — `Δ = Δ^{1/2} ∘ Δ^{1/2}`;
* ★★★★★ `modTwist_is_delta_after_S` — **`modTwist = Δ ∘ S`**, e isto **fecha o
  descompasso que a v274 registrou em aberto**: `towerJ` usa `√ρ`, `modTwist` usa `ρ`
  cheio, e até agora **zero teoremas os relacionavam**. Agora relacionam-se: o adjunto
  modular da ação à direita é o modulador composto com a matriz.

## ⚠ O ESCOPO, dito antes que alguém o alargue

`S` e `Δ` são construídos **NO ANDAR** — matrizes finitas — e **não se estendem
continuamente** a `TowerHilbert P`. A razão é estrutural e não é falta de trabalho:

* `towerJ` **estende** porque é **isometria** (`towerJ_norm`), e isometria é
  uniformemente contínua;
* `S` e `Δ` **não são isometrias** no produto ρ-pesado: `‖aᴴ‖² = Tr(ρ·a·aᴴ)` contra
  `‖a‖² = Tr(ρ·aᴴ·a)`, e as duas diferem quando `ρ` não é escalar. São operadores
  **não limitados**, definidos no **subespaço denso** (a imagem da torre), como manda a
  teoria modular — Tomita constrói `S` como operador **fechável densamente definido**,
  nunca como contínuo.

`[RESÍDUO NOMEADO]` — o que falta para a separação completa: a **fechabilidade** de `S`
no denso e a **auto-adjunticidade positiva** de `Δ`. Isso é conteúdo **analítico**
`[KNOWN]` na literatura, e é a próxima porta. Esta pedra entrega a **álgebra** dessa
porta, exata e no andar.

`[NÃO MOVE NADA]` — `red_clause_JMJ_contains` continua apagada; o certificado continua
condicional; nenhuma bandeira `gpf_` acende aqui. β jamais literal. Sem sorry, sem axiom.
-/

namespace TGLExt

open Matrix

noncomputable section

variable {P : SiteProfile} {N : ℕ}

/-! ## A — a raiz é raiz -/

/-! ★ `profileRoot_sq` (`ρ^{1/2}·ρ^{1/2} = ρ`) **JÁ EXISTE** em
`TheProfileIsometry.lean:50` — achado pela varredura de colisões ANTES de compilar
(lição v259/v274, aplicada a tempo). Não se reescreve: importa-se e usa-se. -/

/-- [KERNEL] ★★ a inversa da raiz também é hermitiana (é diagonal real). -/
theorem profileRootInv_isHermitian (P : SiteProfile) (N : ℕ) :
    (profileRootInv P N)ᴴ = profileRootInv P N := by
  unfold profileRootInv
  rw [diagonal_conjTranspose]
  congr 1
  funext i
  simp [Complex.conj_ofReal]

/-- [KERNEL] ★★ e ela inverte pelo outro lado também. -/
theorem profileRootInv_mul_root (P : SiteProfile) (N : ℕ) :
    profileRootInv P N * profileRoot P N = 1 := by
  unfold profileRoot profileRootInv
  rw [diagonal_mul_diagonal, ← diagonal_one]
  congr 1
  funext i
  have hp : (0:ℝ) < Real.sqrt (towerW P N i) :=
    Real.sqrt_pos.mpr (towerW_pos P N i)
  rw [← Complex.ofReal_mul, one_div, inv_mul_cancel₀ (ne_of_gt hp), Complex.ofReal_one]

/-! ## B — A MATRIZ e O MODULADOR -/

/-- **A MATRIZ**: o operador `S` de Tomita no andar — `S(a) = a†`.
    É a operação que a decomposição polar fatora. -/
def towerSlevel (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    Matrix (chainIdx N) (chainIdx N) ℂ := aᴴ

/-- **O MODULADOR, meia potência**: `Δ^{1/2}(a) = ρ^{1/2}·a·ρ^{-1/2}`. -/
def towerDeltaHalfLevel (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    Matrix (chainIdx N) (chainIdx N) ℂ :=
  profileRoot P N * a * profileRootInv P N

/-- **O MODULADOR**: `Δ(a) = ρ·a·ρ^{-1}` — o operador modular do perfil. -/
def towerDeltaLevel (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    Matrix (chainIdx N) (chainIdx N) ℂ :=
  rhoMat P N * a * rhoMatInv P N

/-! ## C — as relações: a decomposição polar, e o descompasso que se fecha -/

/-- [KERNEL] ★★★★★ **A DECOMPOSIÇÃO POLAR NO ANDAR: `J ∘ Δ^{1/2} = S`.**

    Conta exata, sem hipótese: `J(ρ^{1/2}·a·ρ^{-1/2})` desdobra-se, pelas
    hermitianidades das duas diagonais, em `a†`.

    É esta identidade que torna `towerJ` o **candidato legítimo** a conjugação modular
    do par — e não uma torção qualquer que por acaso leva o nome. A fórmula
    `ρ^{1/2}·a†·ρ^{-1/2}` **é** a conjugação modular na convenção GNS com `Ω = [1]` e
    produto `Tr(ρ·a†·b)`; aqui isso deixa de ser leitura e passa a ser conta. -/
theorem the_polar_decomposition_at_the_level (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    profileJlevel P N (towerDeltaHalfLevel P N a) = towerSlevel P N a := by
  rw [profileJlevel_eq]
  unfold towerDeltaHalfLevel towerSlevel
  rw [conjTranspose_mul, conjTranspose_mul, profileRootInv_isHermitian,
    profileRoot_isHermitian]
  simp only [← Matrix.mul_assoc]
  rw [profileRoot_mul_inv, Matrix.one_mul]
  simp only [Matrix.mul_assoc]
  rw [profileRoot_mul_inv, Matrix.mul_one]

/-- [KERNEL] ★★★ **`Δ = Δ^{1/2} ∘ Δ^{1/2}`** — o modulador é o quadrado da sua meia
    potência. É o que autoriza chamar `towerDeltaHalfLevel` de *meia*. -/
theorem delta_is_the_square_of_its_half (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    towerDeltaHalfLevel P N (towerDeltaHalfLevel P N a) = towerDeltaLevel P N a := by
  unfold towerDeltaHalfLevel towerDeltaLevel
  have hinv : profileRootInv P N * profileRootInv P N = rhoMatInv P N := by
    unfold profileRootInv rhoMatInv
    rw [diagonal_mul_diagonal]
    congr 1
    funext i
    rw [← Complex.ofReal_mul]
    congr 1
    rw [div_mul_div_comm, one_mul,
      Real.mul_self_sqrt (le_of_lt (towerW_pos P N i)), one_div]
  simp only [← Matrix.mul_assoc]
  rw [show profileRoot P N * profileRoot P N = rhoMat P N from profileRoot_sq P N]
  simp only [Matrix.mul_assoc]
  rw [hinv]

/-- [KERNEL] ★★★★★ **`modTwist = Δ ∘ S` — E ISTO FECHA O DESCOMPASSO DA v274.**

    A v274 registrou, como buraco aberto e medido: *"`towerJ` usa `√ρ`; `modTwist` usa
    `ρ` cheio — **zero teoremas os relacionam**"*.

    Agora relacionam-se, e por identidade exata: o **adjunto modular da ação à direita**
    (`rTowerPi_star`) é o **modulador composto com a matriz**. As duas torções não eram
    rivais — eram duas etapas da mesma decomposição. -/
theorem modTwist_is_delta_after_S (P : SiteProfile) (N : ℕ)
    (y : Matrix (chainIdx N) (chainIdx N) ℂ) :
    modTwist P y = towerDeltaLevel P N (towerSlevel P N y) := rfl

/-- [KERNEL] ★★★★ **E A CADEIA INTEIRA NUMA LINHA**: `modTwist = Δ ∘ J ∘ Δ^{1/2}`.
    O adjunto da direita fatora-se pelo J da casa. -/
theorem modTwist_factors_through_J (P : SiteProfile) (N : ℕ)
    (y : Matrix (chainIdx N) (chainIdx N) ℂ) :
    modTwist P y
      = towerDeltaLevel P N (profileJlevel P N (towerDeltaHalfLevel P N y)) := by
  rw [the_polar_decomposition_at_the_level]
  exact modTwist_is_delta_after_S P N y

/-! ## D — o dente: por que `S` e `Δ` NÃO sobem, e `J` sobe -/

/-- [KERNEL] ★★★ **`S` É INVOLUTIVA, como `J`** — mas isso **não basta** para subir ao
    completamento. O que faz `towerJ` subir é a **isometria** (`towerJ_norm`), não a
    involutividade; e `S` não é isometria no produto ρ-pesado.

    Registrado para que a semelhança não seja lida como equivalência: involução é
    álgebra, extensão é topologia. -/
theorem towerSlevel_involutive (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    towerSlevel P N (towerSlevel P N a) = a := by
  unfold towerSlevel
  exact conjTranspose_conjTranspose a

/-- [KERNEL] ★★★ **E O MODULADOR TAMBÉM É INVERTÍVEL NO ANDAR** — `Δ^{1/2}` desfaz-se
    pela torção oposta. No andar tudo é finito e reversível; é ao subir que a
    não-limitação aparece. -/
theorem towerDeltaHalfLevel_inverse (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    profileRootInv P N * (towerDeltaHalfLevel P N a) * profileRoot P N = a := by
  unfold towerDeltaHalfLevel
  calc profileRootInv P N * (profileRoot P N * a * profileRootInv P N) * profileRoot P N
      = (profileRootInv P N * profileRoot P N) * a *
        (profileRootInv P N * profileRoot P N) := by simp only [Matrix.mul_assoc]
    _ = a := by
        rw [profileRootInv_mul_root]
        rw [Matrix.one_mul, Matrix.mul_one]

end

end TGLExt
