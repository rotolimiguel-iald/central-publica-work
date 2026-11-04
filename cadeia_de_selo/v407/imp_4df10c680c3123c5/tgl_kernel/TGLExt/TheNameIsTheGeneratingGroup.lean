import TGLExt.MixedLadder
import TGLExt.NoNormalTrace

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 800000

/-!
# O NOME É O GRUPO GERADOR — o comprimento de onda e a cauda são do Nome, não da fronteira
  [TGLExt — v294; casa "Nós" (29/08/2026)]

## A cunhagem do operador (29/08/2026)

> *"NOME = estado maximamente misturado = `I/d`… Eu não apagaria isso; eu o **rebaixaria de
> definição para representação**. A estrutura fundamental passa a ser
> `NOME = Γ_Nome := ⟨log λ₁, log λ₂⟩_ℤ` com `closure(Γ_Nome) = ℝ`, enquanto `ρ_Nome = I/d`
> é uma **realização** do Nome no regime de estados/densidades."*
>
> *"E agora eu identifico a cauda e o comprimento de onda: **não são pertencentes à
> fronteira, mas ao Nome**."*
>
> *"Nome é a identidade **antes de escolher uma face**."*

## ⚠ O REBAIXAMENTO NÃO É ESCOLHA DE ESTILO — ELE É FORÇADO POR TEOREMA DESTA CASA

`I/d` **é** o estado tracial normalizado: `τ(A) = Tr(A)/d`, tracial e unital. E
`the_dead_weight` (`TGLExt/NoNormalTrace.lean:523`) prova que, no objeto completado com
`mixProfile`, **não existe estado tracial normal**. Logo:

    NOME = I/d NÃO PODE SER A DEFINIÇÃO — na fronteira esse objeto NÃO EXISTE.

Ele existe **na face finita**, onde `d < ∞` e o traço vive. A frase do operador fica exata
por medida: *na face aparece `I/d`; antes da face, só há Γ.*

## ★★ E A INVERSÃO QUE ISSO ENTREGA

O comprimento de onda são os **geradores** (`log λ₁`, `log λ₂` — as escadas discretas); a
cauda é a **densidade** em ℝ. Os dois pertencem ao **Nome**.

`mixed_log_dense` (`MixedLadder.lean:59`) e `the_mixing_mark` (`:141`) já provavam a
densidade; o que faltava era o **nome** do objeto que ela descreve.

## ⚠⚠ ERRATA v295 — AO LADO, NUNCA POR CIMA

A primeira redação desta pedra concluía **"A FRONTEIRA É III₁ *PORQUE* O NOME É DENSO"**.
**Essa inferência é FALSA, e a refutação é teorema:** `the_mark_does_not_separate_the_types`
e `the_mark_is_fed_by_a_type_I_factor` (`TheMarkIsNotATypeMark.lean`) exibem `M₂(ℂ)` — um
fator de **tipo I₂, finito-dimensional** — realizando as razões **2** e **3**, cujos
logaritmos geram subgrupo **denso em ℝ**. A densidade log é satisfeita por um fator de
tipo I; logo **ela não separa III₁ de III_λ e não infere o tipo da fronteira**.

O erro foi do escriba, no mesmo dia, e a causa é nomeável: o predicado da "marca" toma
`A` e `B` **arbitrários da álgebra**, nunca autovetores do fluxo modular — logo a densidade
mede a **não-tracialidade do estado**, não o espectro modular.

**O que sobrevive intacto:** tudo o mais nesta pedra. Os geradores estão no Nome, o fecho é
denso, `I/d` é representação de face e não existe na fronteira. **O que cai é só a seta que
ia do Nome ao tipo.** O que o Nome denso diz é sobre o **Nome**.

## O QUE ESTA PEDRA PROVA

* `nameGroup` — o Nome como objeto: `AddSubgroup.closure {log λ₁, log λ₂}`;
* `the_wavelength_is_in_the_generators` — os geradores **pertencem** ao Nome: o comprimento
  de onda é dado discreto **dentro** dele;
* `the_name_is_dense` — e o fecho é **tudo**: a cauda. Discreto na geração, denso no fecho;
* `faceName` + `faceName_is_tracial`/`faceName_one` — na **face finita** o Nome se realiza
  como `I/d`: o estado tracial normalizado existe e é unital;
* ★★★ `no_maximally_mixed_state_on_the_tower` — e **na fronteira ele não existe**, por
  `the_dead_weight`. O rebaixamento é forçado;
* ★★★ `the_wavelength_and_the_tail_belong_to_the_name` — as duas faces num enunciado só.

## ⚠ O QUE ESTA PEDRA NÃO FAZ

Não decide o tipo por conta própria: `mixProfile` é uma **escolha** de perfil, não uma
derivação, e o que *fixa* o perfil segue `[OPEN]`. Não move o gate. A leitura
*"Nome é a identidade antes de escolher uma face"* é `[ONTO]`; a estrutura é teorema.
-/

namespace TGLExt

noncomputable section

/-! ## A — o Nome como objeto: o grupo gerado -/

/-- **O NOME**, como estrutura: o subgrupo aditivo de ℝ gerado pelos logaritmos das duas
    razões. É o `⟨log λ₁, log λ₂⟩_ℤ` do operador, no tipo que o kernel já usava. -/
def nameGroup (l1 l2 : ℝ) : AddSubgroup ℝ :=
  AddSubgroup.closure {Real.log l1, Real.log l2}

/-- [KERNEL] ★★ **O COMPRIMENTO DE ONDA ESTÁ NOS GERADORES**: as duas escadas discretas
    pertencem ao Nome. É dado **dentro** dele, não fora. -/
theorem the_wavelength_is_in_the_generators (l1 l2 : ℝ) :
    Real.log l1 ∈ nameGroup l1 l2 ∧ Real.log l2 ∈ nameGroup l1 l2 :=
  ⟨AddSubgroup.subset_closure (Set.mem_insert _ _),
   AddSubgroup.subset_closure (Set.mem_insert_of_mem _ rfl)⟩

/-- [KERNEL] ★★★ **E A CAUDA É O FECHO**: no par concreto do perfil da casa, o Nome é
    **denso** em ℝ. Discreto na geração, denso no fecho — as duas coisas ao mesmo tempo,
    que é exatamente o que a leitura do operador pedia. -/
theorem the_name_is_dense :
    Dense ((nameGroup ((1 : ℝ) / 2) ((1 : ℝ) / 3) : AddSubgroup ℝ) : Set ℝ) :=
  the_mixing_mark

/-! ## B — a face finita: onde `I/d` existe -/

variable {n : Type} [Fintype n] [DecidableEq n]

/-- **O NOME NA FACE**: o estado tracial normalizado `A ↦ Tr(A)/d` — a forma funcional do
    estado maximamente misturado `ρ = I/d`. -/
def faceName (A : Matrix n n ℂ) : ℂ :=
  Matrix.trace A / (Fintype.card n : ℂ)

/-- [KERNEL] o Nome na face é **aditivo**. -/
theorem faceName_add (A B : Matrix n n ℂ) :
    faceName (A + B) = faceName A + faceName B := by
  unfold faceName
  rw [Matrix.trace_add, add_div]

/-- [KERNEL] o Nome na face é **homogêneo**. -/
theorem faceName_smul (c : ℂ) (A : Matrix n n ℂ) :
    faceName (c • A) = c * faceName A := by
  unfold faceName
  rw [Matrix.trace_smul, smul_eq_mul, mul_div_assoc]

/-- [KERNEL] ★★ o Nome na face é **TRACIAL** — não distingue a ordem. -/
theorem faceName_is_tracial (A B : Matrix n n ℂ) :
    faceName (A * B) = faceName (B * A) := by
  unfold faceName
  rw [Matrix.trace_mul_comm]

/-- [KERNEL] ★★ e é **unital**: o Nome da identidade é 1 — `ω(I) = 1`, na face. -/
theorem faceName_one [Nonempty n] : faceName (1 : Matrix n n ℂ) = 1 := by
  unfold faceName
  rw [Matrix.trace_one]
  have : (Fintype.card n : ℂ) ≠ 0 := Nat.cast_ne_zero.mpr Fintype.card_ne_zero
  field_simp

/-! ## C — a fronteira: onde `I/d` NÃO existe -/

/-- [KERNEL] ★★★★★ **NA FRONTEIRA NÃO HÁ ESTADO MAXIMAMENTE MISTURADO.**

    `I/d` é o estado tracial normalizado, e `the_dead_weight` prova que no objeto completado
    com `mixProfile` **nenhum** funcional aditivo, homogêneo, unital, tracial e normal
    existe. Logo o Nome **não pode ser definido** como `I/d`: essa forma é realização de
    FACE, não a estrutura.

    ⚠ Este é o teorema que torna o rebaixamento do operador **obrigatório**, e não
    estilístico. -/
theorem no_maximally_mixed_state_on_the_tower :
    ∀ τ : (TowerHilbert mixProfile →L[ℂ] TowerHilbert mixProfile) → ℂ,
      (∀ A B, τ (A + B) = τ A + τ B) →
      (∀ (c : ℂ) A, τ (c • A) = c * τ A) →
      τ 1 = 1 →
      (∀ A B, A ∈ theFactorObject mixProfile →
        B ∈ theFactorObject mixProfile → τ (A * B) = τ (B * A)) →
      SeqWOTContinuous (theFactorObject mixProfile) τ → False :=
  the_dead_weight.2

/-- [KERNEL] ★★★★★ **O COMPRIMENTO DE ONDA E A CAUDA PERTENCEM AO NOME.**

    ⚠⚠ **ERRATA v298 — AO LADO, E AGORA NO PONTO DE LEITURA.** A redação da v294 seguia
    aqui: *"— e por isso a fronteira é III₁"*. **Essa seta é FALSA**, e a refutação é
    teorema desta mesma casa: `the_mark_does_not_separate_the_types`
    (`TheMarkIsNotATypeMark.lean`) exibe `M₂(ℂ)` — fator de tipo **I₂, finito-dimensional** —
    realizando razões cujos logaritmos geram subgrupo **denso em ℝ**. Logo a densidade log
    **não separa III₁ de III_λ** e não infere o tipo.

    ⚠ **O defeito da correção anterior, dito:** a errata existia desde a v295, mas **só no
    cabeçalho do arquivo**. Quem chega pelo índice da IALD chega **pelo nome e pelo
    docstring** — e recebia a frase refutada, sem a refutação. Corrigir "ao lado" não basta
    se o lado escolhido não é o lado que se lê.

    Num enunciado só: (i) os geradores discretos estão **dentro** do Nome — o comprimento de
    onda; (ii) o fecho do Nome é **tudo** — a cauda; (iii) e na fronteira o estado
    maximamente misturado **não existe**, logo `I/d` é representação de face e não a
    definição.

    ⚠ **A frase refutada, preservada e marcada** (v294, refutada na v295): *"a ordem da
    leitura inverte-se: a fronteira é III₁ porque o Nome é denso"* — **FALSA**. O que o Nome
    denso diz é sobre o **Nome**. O tipo da fronteira segue
    `TGL_BOUNDARY_TYPE_UNDECIDED_IN_KERNEL`. -/
theorem the_wavelength_and_the_tail_belong_to_the_name :
    (Real.log ((1 : ℝ) / 2) ∈ nameGroup ((1 : ℝ) / 2) ((1 : ℝ) / 3)
      ∧ Real.log ((1 : ℝ) / 3) ∈ nameGroup ((1 : ℝ) / 2) ((1 : ℝ) / 3))
    ∧ Dense ((nameGroup ((1 : ℝ) / 2) ((1 : ℝ) / 3) : AddSubgroup ℝ) : Set ℝ)
    ∧ (∀ τ : (TowerHilbert mixProfile →L[ℂ] TowerHilbert mixProfile) → ℂ,
        (∀ A B, τ (A + B) = τ A + τ B) →
        (∀ (c : ℂ) A, τ (c • A) = c * τ A) →
        τ 1 = 1 →
        (∀ A B, A ∈ theFactorObject mixProfile →
          B ∈ theFactorObject mixProfile → τ (A * B) = τ (B * A)) →
        SeqWOTContinuous (theFactorObject mixProfile) τ → False) :=
  ⟨the_wavelength_is_in_the_generators _ _,
   the_name_is_dense,
   no_maximally_mixed_state_on_the_tower⟩

end

end TGLExt
