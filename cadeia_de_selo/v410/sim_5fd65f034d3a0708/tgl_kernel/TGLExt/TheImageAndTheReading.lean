import TGLExt.TheAtomOfIdentity

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option linter.unusedVariables false
set_option maxHeartbeats 400000

/-!
# A IMAGEM E A LEITURA — três casos que parecem dois
  [TGLExt — a pedra de 28/08/2026]

## A tipagem do operador

> *"toda imagem é a representação do zero absoluto, contida em sua totalidade sem
> expressão até que seja traduzida em linguagem"* · *"o recorte geométrico das formas
> exige um leitor; sem esse leitor, a fase simplesmente não existe como forma"* ·
> *"o contorno é a fronteira = operador de consciência = observador"*.

E a precisão que ele exigiu, que é a razão desta pedra existir:

> **`sem leitura ≠ ausência de conteúdo;  sem leitura = ausência de forma expressa`**

## O que esta pedra acrescenta, e por que não é o que já havia

O kernel já tinha os dois extremos: `a_single_outcome_separates_nothing` e
`the_pair_separates` (v270), e a hermeticidade em `boundary_is_the_only_exception`
(`FullStaticWitness ↔ ∀ i, d i = 0`). O que **não** havia é a **separação dos três
casos** — e sem ela os dois últimos se confundem, que é justamente o que o operador
mandou não confundir:

| caso | o objeto | a leitura | há forma? |
|---|---|---|---|
| 1 | tem contraste | separante | **sim** |
| 2 | tem contraste | constante | **não** — a IMAGEM NÃO LIDA |
| 3 | **sem** contraste | qualquer | **não** — `0_abs` / hermeticidade |

★★★★★ `the_unread_image_is_not_the_absolute_zero` — **os casos 2 e 3 são
distintos**: no 2 **existe** leitura que produziria forma; no 3 **não existe
nenhuma**. É a frase do operador em teorema: *conter* não é *aparecer*, e *não
aparecer* tem duas causas incompatíveis.

★★★ `the_reader_adds_condition_not_content` — e a imagem é **literalmente a mesma**
nos dois lados do caso 2/1: só o mapa muda. O leitor não acrescenta conteúdo;
acrescenta a condição sob a qual o conteúdo pode aparecer.

## O que NÃO se prova aqui, e vai dito

`[ONTO]` — `IMAGEM = Rep(0_abs)`, `contorno = fronteira = observador`, e a cadeia
`0_abs → LEITOR → RECORTE → INSCRIÇÃO → FORMA → NOME` são leitura do operador.
Nenhum teorema desta pedra menciona `0_abs`, `1_abs`, β, imagem, consciência ou
observador. O que se prova é a **forma** da distinção: três casos, e o terceiro não
é o segundo.

`[JÁ EXISTE, NÃO SE DUPLICA]` — o **contorno** já é bancada no artefato
(`prove_contour_theory`, com a correção ontológica do próprio operador: *"0_abs NÃO
tem espelho; quem tem espelho é 0_mod"*), e o **observador** já é objeto de kernel
(`TGLExt/ObserverInside.lean`: `observerProj`, `flow_delivers_to_the_observer`).
Esta pedra **cita e não refaz**.

`[NÃO MOVE O GATE]` — nada aqui acende bandeira. β jamais entra. Sem sorry, sem axiom.
-/

namespace TGLExt

/-! ## A — os dois predicados: contraste no objeto, separação na leitura -/

/-- **CONTRASTE**: o objeto tem ao menos uma diferença. É o que a imagem *contém*. -/
def HasContrast (I : Type) : Prop := ∃ x y : I, x ≠ y

/-- **SEPARAÇÃO**: a leitura afirma alguma diferença como diferença. É o que
    *aparece*. Note que é propriedade do MAPA, não do objeto. -/
def Separates {I V : Type} (R : I → V) : Prop := ∃ x y : I, R x ≠ R y

/-- [KERNEL] ★★ **SEPARAR EXIGE CONTRASTE**: nenhuma leitura inventa diferença que o
    objeto não tenha. O leitor não acrescenta conteúdo. -/
theorem separates_needs_contrast {I V : Type} (R : I → V) (h : Separates R) :
    HasContrast I := by
  obtain ⟨x, y, hxy⟩ := h
  exact ⟨x, y, fun hEq => hxy (congrArg R hEq)⟩

/-! ## B — os três casos -/

/-- [KERNEL] ★★★ **CASO 1 — há contraste e a leitura separa: HÁ FORMA.** -/
theorem a_separating_reading_yields_form :
    ∃ (I V : Type) (R : I → V), HasContrast I ∧ Separates R := by
  refine ⟨Bool, Bool, id, ⟨true, false, by decide⟩, ⟨true, false, by decide⟩⟩

/-- [KERNEL] ★★★★ **CASO 2 — há contraste e a leitura NÃO separa: A IMAGEM NÃO
    LIDA.** O conteúdo está inteiro no objeto; nenhuma forma é expressa. -/
theorem the_unread_image_yields_no_form :
    ∃ (I V : Type) (R : I → V), HasContrast I ∧ ¬ Separates R := by
  refine ⟨Bool, Unit, fun _ => (), ⟨true, false, by decide⟩, ?_⟩
  rintro ⟨x, y, hxy⟩
  exact hxy rfl

/-- [KERNEL] ★★★★ **CASO 3 — sem contraste, NENHUMA leitura produz forma.** É a
    hermeticidade: onde não há diferença, não há o que ler, e a lente não importa. -/
theorem without_contrast_no_reading_yields_form {I V : Type}
    (hI : ¬ HasContrast I) (R : I → V) : ¬ Separates R := fun h => hI
  (separates_needs_contrast R h)

/-! ## C — e o CASO 2 NÃO É O CASO 3: é a frase do operador em teorema -/

/-- [KERNEL] ★★★★★ **A IMAGEM NÃO LIDA NÃO É O ZERO ABSOLUTO.** No caso 2 **existe**
    leitura que produziria forma; no caso 3 **não existe nenhuma**. Logo *não
    aparecer* tem **duas causas incompatíveis**, e confundi-las é o erro que esta
    pedra existe para impedir:

      `sem leitura ≠ ausência de conteúdo;  sem leitura = ausência de forma expressa`

    O mesmo objeto (`Bool`) admite as duas leituras. O que muda é o mapa. -/
theorem the_unread_image_is_not_the_absolute_zero :
    ∃ I : Type,
      HasContrast I
      ∧ (∃ (V : Type) (R : I → V), ¬ Separates R)
      ∧ (∃ (V : Type) (R : I → V), Separates R) := by
  refine ⟨Bool, ⟨true, false, by decide⟩, ⟨Unit, fun _ => (), ?_⟩,
    ⟨Bool, id, ⟨true, false, by decide⟩⟩⟩
  rintro ⟨x, y, hxy⟩
  exact hxy rfl

/-- [KERNEL] ★★★ **O LEITOR ACRESCENTA CONDIÇÃO, NÃO CONTEÚDO.** O objeto é o MESMO
    termo nos dois ramos acima — só o mapa difere. E a direção da dependência é
    unilateral (`separates_needs_contrast`): o contraste é condição da separação, e
    a separação nunca cria contraste.

    *Conter* e *aparecer* são, portanto, coisas distintas com ordem fixa entre elas. -/
theorem the_reader_adds_condition_not_content {I V W : Type}
    (R : I → V) (S : I → W) (hR : Separates R) (hS : ¬ Separates S) :
    HasContrast I ∧ ¬ Separates S :=
  ⟨separates_needs_contrast R hR, hS⟩

/-! ## D — a ponte com a v270: a leitura que desce, e o lugar onde não há o que ler -/

/-- [KERNEL] ★★★ **E O CASO 3 É EXATAMENTE ONDE A LEITURA DA v270 NÃO TEM O QUE
    DESCER.** `the_reading_descends_for_any_lens` diz que a EXISTÊNCIA do registro
    não depende de acertar a lente; este teorema diz o complementar: quando não há
    contraste, **nenhuma** lente serve — não por falha da lente, mas por ausência do
    que ler. As duas frases são compatíveis e delimitam-se mutuamente. -/
theorem the_lens_is_irrelevant_exactly_where_there_is_nothing_to_read
    {I : Type} (hI : ¬ HasContrast I) :
    ∀ (V : Type) (R : I → V), ¬ Separates R :=
  fun _ R => without_contrast_no_reading_yields_form hI R

end TGLExt
