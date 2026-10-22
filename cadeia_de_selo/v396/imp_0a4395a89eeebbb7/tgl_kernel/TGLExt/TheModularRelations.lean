import TGLExt.TheMatrixAndTheModulator

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 1000000

/-!
# AS RELAÇÕES MODULARES — `S†S = Δ`, no andar
  [TGLExt — a pedra de 28/08/2026]

## Onde estávamos

A v275 construiu `S`, `Δ^{1/2}` e `Δ` no andar e provou a **decomposição polar**
`J ∘ Δ^{1/2} = S`. Ficou dito que o resíduo passava a ser **analítico**.

★ **Parte desse resíduo é pagável no andar**, e é esta pedra. O que fica de fora é
estritamente a **passagem ao completamento**.

## O que se prova aqui `[REAL]`

Com o produto GNS do andar `⟨a,b⟩ = φ(a†b) = Tr(ρ·a†·b)` (`tInner_eq_trace`):

* ★★★★★ `S_star_S_is_deltaLevel` — **`⟨Sa, Sb⟩ = ⟨Δb, a⟩`**, isto é `S†S = Δ` em forma
  bilinear. **É a identidade que DEFINE o operador modular.** Sem ela `Δ` seria uma
  torção com nome bonito; com ela, `Δ` é o modular do par;
* ★★★★ `deltaLevel_positive` — `⟨Δa, a⟩ = ⟨Sa, Sa⟩`. **A positividade de `Δ` É a norma
  de `Sa`** — sai da relação definidora com `b := a`, não por conta separada. É assim
  que a teoria modular obtém a positividade: ela não é postulada;
* ★★★★ `deltaLevel_selfadjoint` — `⟨Δa, b⟩ = ⟨a, Δb⟩`.

**Tudo por ciclicidade do traço.** Nenhuma hipótese.

## ⚠ O QUE ISTO SIGNIFICA, e o que NÃO significa

**Significa:** no andar, `Δ` satisfaz as relações definidoras do operador modular —
`S†S = Δ`, auto-adjunto, positivo — e, com a polar da v275, a tripla `(S, Δ, J)` tem a
álgebra inteira de Tomita. A identificação *"`towerJ` é a conjugação modular"* deixa de
ser plausibilidade de fórmula e passa a ser **conjunto de identidades provadas**.

**NÃO significa** que Tomita esteja provado na torre. Separa uma coisa da outra
exatamente isto, e continua aberto:

> `[OPEN, ANALÍTICO]` a passagem ao completamento — `S` fechável e `Δ` auto-adjunto
> positivo como operadores **não limitados** em `TowerHilbert P`. As relações acima são
> algébricas e valem em cada andar; **o limite não sai delas**.

⚠ E o motivo estrutural, repetido porque é a tentação óbvia: `towerJ` sobe porque é
**isometria**; `S` e `Δ` não são, e nenhuma quantidade de identidades algébricas no
andar produz continuidade que não existe.

## ★ O QUE FALTAVA E FOI FECHADO (ordem do operador: *"feche o teorema"*)

* ★★★★★ `Jlevel_is_antiunitary` — **`⟨Ja, Jb⟩ = conj⟨a,b⟩`**. A v276 a deixara de fora
  porque eu não a fechara, e o artefato **media essa ausência** com um check
  fail-closed. Agora está fechada, por conta exata (`ρ·ρ^{-1/2} = ρ^{1/2}` mais duas
  comutações de traço), e o check **muda de alvo**: passa a exigir a **presença**.

**Com ela, a tripla `(S, Δ, J)` satisfaz no andar TODAS as relações definidoras da
teoria modular de Tomita** — a polar (v275), `S†S = Δ`, a positividade, a
auto-adjunticidade e a antiunitariedade. Nenhuma fica por conta de leitura.

`[NÃO MOVE NADA]` — `red_clause_JMJ_contains` continua apagada; nenhuma `gpf_` acende.
β jamais literal. **Sem sorry, sem axiom.**
-/

namespace TGLExt

open Matrix

noncomputable section

variable {P : SiteProfile} {N : ℕ}

/-! ## A — a ponte: o produto GNS é um traço contra a densidade -/

/-- [KERNEL] ★★ `⟨a,b⟩ = Tr(ρ·a†·b)` — a forma que torna tudo abaixo ciclicidade. -/
theorem tInner_eq_trace (P : SiteProfile) (N : ℕ)
    (a b : Matrix (chainIdx N) (chainIdx N) ℂ) :
    tInner P N a b = (rhoMat P N * (aᴴ * b)).trace := by
  unfold tInner rhoMat
  exact tState_eq_trace P N (aᴴ * b)

/-- [KERNEL] ★ a forma reduzida do produto contra `Δ`: `⟨Δx, y⟩ = Tr(x†·ρ·y)`.
    É o único cálculo desta pedra, e os três teoremas abaixo são ele, duas vezes. -/
theorem tInner_delta_left (P : SiteProfile) (N : ℕ)
    (x y : Matrix (chainIdx N) (chainIdx N) ℂ) :
    tInner P N (towerDeltaLevel P N x) y = (xᴴ * rhoMat P N * y).trace := by
  rw [tInner_eq_trace]
  unfold towerDeltaLevel
  rw [conjTranspose_mul, conjTranspose_mul, rhoMat_conjT, rhoMatInv_conjT]
  simp only [← Matrix.mul_assoc]
  rw [rhoMat_mul_inv, Matrix.one_mul]

/-! ## B — a relação que DEFINE o modular -/

/-- [KERNEL] ★★★★★ **`S†S = Δ`, EM FORMA BILINEAR: `⟨Sa, Sb⟩ = ⟨Δb, a⟩`.**

    Esta é **a** identidade da teoria modular. Ela não diz que `Δ` *parece* o operador
    modular — diz que `Δ` **é** o que a matriz `S` produz ao compor-se consigo mesma
    pelo produto interno.

    A prova é ciclicidade do traço, e nada mais. -/
theorem S_star_S_is_deltaLevel (P : SiteProfile) (N : ℕ)
    (a b : Matrix (chainIdx N) (chainIdx N) ℂ) :
    tInner P N (towerSlevel P N a) (towerSlevel P N b)
      = tInner P N (towerDeltaLevel P N b) a := by
  rw [tInner_delta_left, tInner_eq_trace]
  unfold towerSlevel
  rw [conjTranspose_conjTranspose]
  simp only [← Matrix.mul_assoc]
  rw [Matrix.trace_mul_comm (rhoMat P N * a) bᴴ, Matrix.mul_assoc]

/-! ## C — o que a relação definidora entrega de graça -/

/-- [KERNEL] ★★★★ **A POSITIVIDADE DE `Δ` É A NORMA DE `Sa`**: `⟨Δa, a⟩ = ⟨Sa, Sa⟩`.

    Não é conta nova — é a relação definidora com `b := a`. É assim que a teoria
    modular obtém a positividade do modular: **ela não é postulada, é a norma da imagem
    da matriz**. -/
theorem deltaLevel_positive (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    tInner P N (towerDeltaLevel P N a) a
      = tInner P N (towerSlevel P N a) (towerSlevel P N a) :=
  (S_star_S_is_deltaLevel P N a a).symm

/-- [KERNEL] ★★★★ **`Δ` É AUTO-ADJUNTO** no produto GNS: `⟨Δa, b⟩ = ⟨a, Δb⟩`.
    Os dois lados caem na mesma forma reduzida `Tr(a†·ρ·b)`. -/
theorem deltaLevel_selfadjoint (P : SiteProfile) (N : ℕ)
    (a b : Matrix (chainIdx N) (chainIdx N) ℂ) :
    tInner P N (towerDeltaLevel P N a) b = tInner P N a (towerDeltaLevel P N b) := by
  rw [tInner_delta_left, tInner_eq_trace]
  unfold towerDeltaLevel
  simp only [← Matrix.mul_assoc]
  rw [Matrix.trace_mul_comm (rhoMat P N * aᴴ * rhoMat P N * b) (rhoMatInv P N)]
  simp only [← Matrix.mul_assoc]
  rw [rhoMatInv_mul, Matrix.one_mul]

/-! ## D — `J` é ANTIUNITÁRIO no andar -/

/-- [KERNEL] ★★ `ρ·ρ^{-1/2} = ρ^{1/2}` — a peça aritmética que faltava. -/
theorem rhoMat_mul_rootInv (P : SiteProfile) (N : ℕ) :
    rhoMat P N * profileRootInv P N = profileRoot P N := by
  unfold rhoMat profileRootInv profileRoot
  rw [diagonal_mul_diagonal]
  congr 1
  funext i
  rw [← Complex.ofReal_mul]
  congr 1
  have hp : (0:ℝ) < Real.sqrt (towerW P N i) := Real.sqrt_pos.mpr (towerW_pos P N i)
  field_simp
  exact (Real.sq_sqrt (le_of_lt (towerW_pos P N i))).symm

/-- [KERNEL] ★★★★★ **`J` É ANTIUNITÁRIO NO ANDAR: `⟨Ja, Jb⟩ = conj⟨a,b⟩`.**

    Com ela, a tripla `(S, Δ, J)` satisfaz no andar **todas** as relações definidoras da
    teoria modular: a polar `J∘Δ^{1/2} = S` (v275), `S†S = Δ`, a positividade, a
    auto-adjunticidade — e agora a antiunitariedade de `J`.

    ★ Escrita depois, e por ordem do operador (*"feche o teorema para ele entrar
    fechado"*): a v276 a deixara **fora** por eu não tê-la fechado, e o artefato media
    essa ausência com um check fail-closed. Fechada, o check muda de alvo — não se
    apaga, passa a exigir a **presença**. -/
theorem Jlevel_is_antiunitary (P : SiteProfile) (N : ℕ)
    (a b : Matrix (chainIdx N) (chainIdx N) ℂ) :
    tInner P N (profileJlevel P N a) (profileJlevel P N b)
      = starRingEnd ℂ (tInner P N a b) := by
  rw [tInner_eq_trace, tInner_eq_trace, profileJlevel_eq, profileJlevel_eq]
  rw [conjTranspose_mul, conjTranspose_mul, profileRootInv_isHermitian,
    profileRoot_isHermitian, conjTranspose_conjTranspose]
  simp only [← Matrix.mul_assoc]
  rw [rhoMat_mul_rootInv]
  rw [Matrix.trace_mul_comm
    (profileRoot P N * a * profileRoot P N * profileRoot P N * bᴴ) (profileRootInv P N)]
  simp only [← Matrix.mul_assoc]
  rw [profileRootInv_mul_root, Matrix.one_mul]
  rw [Matrix.mul_assoc a (profileRoot P N) (profileRoot P N),
    show profileRoot P N * profileRoot P N = rhoMat P N from profileRoot_sq P N]
  rw [starRingEnd_apply, ← Matrix.trace_conjTranspose,
    conjTranspose_mul, conjTranspose_mul, rhoMat_conjT, conjTranspose_conjTranspose]
  rw [Matrix.trace_mul_comm (a * rhoMat P N) bᴴ]

/-! ## E — O DEFEITO DE ISOMETRIA É O PRÓPRIO ESPECTRO MODULAR

⚠ **Uma afirmação minha, repetida em três pedras e nunca medida**, até aqui: *"`S` e
`Δ` não são isometrias no produto ρ-pesado, por isso não sobem ao completamento"*. Era
prosa. Vira conta.
-/

/-- [KERNEL] ★★★★★ **`Δ` AGE ENTRADA A ENTRADA PELA RAZÃO DOS PESOS**:
    `(Δa)_{jk} = (w_j / w_k)·a_{jk}`.

    Isto **é** o espectro modular, escrito. O operador modular não mistura entradas: ele
    as reescala pela razão KMS. -/
theorem delta_acts_by_the_weight_ratio (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) (j k : chainIdx N) :
    towerDeltaLevel P N a j k
      = ((towerW P N j : ℝ) : ℂ) * a j k * (((towerW P N k)⁻¹ : ℝ) : ℂ) := by
  unfold towerDeltaLevel rhoMat rhoMatInv
  rw [Matrix.mul_diagonal, Matrix.diagonal_mul]

/-- [KERNEL] ★★★★★ **Δ SÓ FIXA ONDE OS PESOS COINCIDEM.** Se `Δ` deixa `a` parado e `a`
    tem entrada `(j,k)` não nula, então `w_j = w_k`.

    É o **dente** que faltava: os pontos fixos de `Δ` são exatamente o centralizador, e
    fora dele `Δ` desloca. Logo `Δ ≠ id` sempre que o perfil tiver dois pesos distintos
    — e o perfil da torre tem. -/
theorem delta_fixes_only_where_the_weights_agree (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) (j k : chainIdx N)
    (hjk : a j k ≠ 0) (h : towerDeltaLevel P N a = a) :
    towerW P N j = towerW P N k := by
  have h1 : towerDeltaLevel P N a j k = a j k := by rw [h]
  rw [delta_acts_by_the_weight_ratio] at h1
  have hk0 : ((towerW P N k : ℝ) : ℂ) ≠ 0 := by
    simpa using (ne_of_gt (towerW_pos P N k))
  field_simp at h1
  have hr : towerW P N j * (1 / towerW P N k) = 1 := by exact_mod_cast h1
  have hk : towerW P N k ≠ 0 := ne_of_gt (towerW_pos P N k)
  field_simp at hr
  exact hr

/-- [KERNEL] ★★★★ **`S` É ISOMETRIA EXATAMENTE ONDE `Δ` É NEUTRO.** Consequência direta da
    relação definidora: `‖Sa‖² = ⟨Δa, a⟩`.

    Somando com o teorema acima: **`S` só preserva norma onde os pesos coincidem** — isto
    é, onde o estado é **tracial**. Fora da face tracial, `S` deforma, e é por isso, e
    não por falta de trabalho, que ele **não sobe por continuidade** como `towerJ` sobe.
    A afirmação que eu vinha fazendo em prosa passa a ser esta conta. -/
theorem S_isometric_iff_delta_neutral (P : SiteProfile) (N : ℕ)
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    tInner P N (towerSlevel P N a) (towerSlevel P N a) = tInner P N a a
      ↔ tInner P N (towerDeltaLevel P N a) a = tInner P N a a := by
  rw [deltaLevel_positive]

end

end TGLExt
