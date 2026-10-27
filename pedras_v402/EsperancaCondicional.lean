import TGLExt.CondExpect
import TGLExt.TheNameOperator
import TGLExt.PostoAdendo
import TGL.NameIndex
import TGLExt.TheObserverReadsTheAngle
import TGLExt.IALDJones
import TGLExt.IALD

set_option autoImplicit false
set_option linter.unusedSectionVars false

/-!
# ESPERANÇA CONDICIONAL = NOME  [TGLExt — pedra candidata da v402, 26/10/2026; sandbox `k402`; NADA instalado]
# CONDITIONAL EXPECTATION = NAME

Nome PROVISÓRIO (o operador nomeia). No código vai sem acento: `EsperancaCondicional`.

Ordem do operador (26/10/2026; `work\cunhagens_13out\OPERADOR_26out_e_isso_faca_a_prova_prossiga_verbatim.txt`,
sha256 `a1c4bae4a87aa173251fef9015cb74d67d361829db4c3807a7c27ff409723a05`, sha16 `a1c4bae4a87aa173`):
«é isso, faça a prova, prossiga.»

## A fala [INPUT] (trechos EXATOS por bytes)

Arquivo `work\cunhagens_13out\OPERADOR_26out_esperanca_condicional_e_nome_verbatim.txt`,
sha256 `5d3976cd0cc10dc8e1eeb8bdc5049dd7ac1372d0c92f18ef5eae20eb58f35b52` (sha16 `5d3976cd0cc10dc8`).
A linha da equação: «esperança condicional=nome». A pergunta dele: «ainda não sei se fizemos a tipagem».

## A RESPOSTA À PERGUNTA (a tipagem): SIM, EM GRANDE PARTE — o que já estava no kernel

Levantamento antes de construir (consultas por `grep` no sandbox `k402`, byte-igual ao kernel do Nós v401):

* `TheNameOperator.nameOp p x = p x p + (1−p) x (1−p)` — o OPERADOR DO NOME (v162, 17/08/2026), com
  `name_op_unital` (𝒩(1) = 1, «o Nome não destrói a identidade»), `name_op_idem` (𝒩∘𝒩 = 𝒩, «o que foi lido
  não pode ser deslido») e `name_op_fix_mul` (a memória, o conjunto dos fixos, é subálgebra);
* `PostoAdendo.A1c_nameOp_rhoStar_eq_diagExpect` (v392) — em `M₂(ℂ)` o Operador do Nome da unidade `ρ*` É a
  esperança condicional diagonal `diagExpect` (`D_∞`); `TimeGravitonMatrix.Eg_as_nameOp` usa a mesma ponte;
* `CondExpect` (Degrau 1) — `trExpect` (unital, idempotente, preserva o traço) e `diagExpect` (unital,
  idempotente, D-bimodular, preserva o traço, positiva), e a RELAÇÃO DE JONES `eD_Lmul_eD`; `TGL.TransportData.ConditionalExpectationData` — a estrutura de Tomiyama;
* `TGL.NameIndex` (v27) — «e_Nome = projecao de Jones = espelho» (grafia do kernel) e o ÍNDICE DO NOME (`ppIndex = 1/ppBest`,
  `name_index_mul_sin_sq`); `IALDJones.iald_reads_the_expectation` — a leitura de Jones É a esperança
  condicional; `IALD.the_name_has_rank_one`, `the_name_reads_one` — o Nome como `post a`, de posto 1.

O que NÃO existia: a identificação dita COMO UMA CLÁUSULA (as propriedades do Nome lidas na esperança, na
mesma face `M₂`, com a lei de Jones do Nome e o índice `1/b` juntos) e o liame explícito entre o reler não
acrescenta da esperança e o `observing_adds_nothing` do observador. Esta pedra é essa composição; não
refaz nenhum dos termos acima (consulta ao Mapa de Rotas: `esperanca condicional` devolveu só a rota do
inventário GKLS da v384, nenhuma sobre esta identificação).

## O Nome: TRÊS FACES DE UM OBJETO FIXO, não três definições (decisão da gerência, 26/10/2026)

(a) O OPERADOR: `nameOp`, a esperança condicional que LÊ (unital, idempotente, memória-subálgebra;
`PostoAdendo.A1c`: `nameOp ρ* = diagExpect`). (b) O PROJETOR: o projetor de Jones `e_Nome`
(`NameIndex`: «e_Nome = projecao de Jones = espelho») é a MESMA coisa vista como projetor no espaço GNS: a
compressão pelo espelho (`eD_Lmul_eD`; aqui `the_mirror_compression_is_the_name`). (c) O PESO: o posto `a`
(`IALD.post a`, de posto 1; `Posto.rhoStar_unit`: `Tr ρ* = posto ρ* = 1`) é o PESO que a esperança preserva,
`E(1) = 1` (`the_name_preserves_the_one`). É a régua da casa para β, aplicada ao Nome: «Faces de um objeto
fixo, não definições concorrentes — o número é cravado, os nomes são leituras». O kernel prova as LIGAÇÕES
entre as faces (A1c: operador = esperança diagonal; Jones: projetor ↔ operador; `E(1) = 1`: o peso), não uma
igualdade de TIPOS (operador, projetor e posto vivem em tipos distintos); que sejam faces de um só é a
leitura [ONTO] da gerência, decidida em 26/10/2026.

## O que a pedra tipa (composição por citação; a única matemática nova são lemas de COLA, declarados)

1. ★★ `the_name_preserves_the_one` — `𝒩(1) = 1`: `nameOp p 1 = 1` para todo idempotente `p` de um anel
   (`name_op_unital`) e em `M₂(ℂ)` para `ρ*`; `diagExpect 1 = 1`, `trExpect 1 = 1`; e todo
   `ConditionalExpectationData` tem `E 1 = 1` (campo `E_unital`), a média de paridade também
   (`ParityData.average_unital`). O Um posto, ω(I) = 1, ATRAVESSA o Nome.
2. ★★ `rereading_the_name_adds_nothing` — `E∘E = E`: `name_op_idem`, `diagExpect_idem`, `trExpect_idem`,
   `ParityData.average_idem`; e o LIAME: tudo isso são instâncias da MESMA forma `RereadAddsNothing R`
   (`∀ x, R (R x) = R x`), da qual o `observing_adds_nothing` do observador
   (`P₊·(P₊·𝒪_θ) = P₊·𝒪_θ`) é outra instância (`R x = P₊ x`, `P₊` idempotente). Mesma FORMA, nenhuma
   EQUAÇÃO entre os operadores: a esperança age na álgebra, o observador no ângulo (regra dos dois regimes).
   O kernel já tinha a conjunção análoga para a memória do Nome no espaço de Hilbert
   (`IALD.rereading_adds_nothing`, `IALD.rereading_adds_nothing_in_both_regimes`: face do motor e ângulo da
   PALAVRA); esta pedra estende a forma às esperanças.
3. ★★ `the_mirror_compression_is_the_expectation` — a relação de Jones: `e_D·L_x·e_D = L_{E_D(x)}·e_D`
   (`eD_Lmul_eD`) e a escalar `e·L_x·e = (Tr x/n)·e` (`eTr_Lmul_eTr`); em `M₂(ℂ)`, por A1c,
   `e_D·L_x·e_D = L_{𝒩_{ρ*}(x)}·e_D`: a compressão pelo espelho É o Operador do Nome.
4. ★★ `the_index_of_the_name_is_one_over_beta` — de `name_index_eq_csc_sq`/`name_index_mul_sin_sq`, com
   `hb : sin θ ^ 2 = b` e `b > 0` (VARIÁVEL; em `θ_M`, `b = β`, em runtime): `ppIndex D = 1/b` e
   `ppIndex D · b = 1`. É CONDICIONAL às duas hipóteses do kernel (`sin²θ` cota de Pimsner–Popa válida e
   ÓTIMA da esperança do contorno): NENHUMA instância é construída aqui nem no kernel (`NameIndex`:
   «Nenhuma instancia e' construida»); que o `θ_M` do TGL realize isso é [OPEN].
5. ★★★ `esperanca_condicional_e_nome` — a composição, em `M₂(ℂ)` com a unidade `ρ*`.

## As quatro línguas dele, como LETRA [INPUT da gerência — o operador ratifica ou corrige]

Probabilidade: `E[X | 𝒢]`, a esperança condicional de `X` dada a álgebra do observador `𝒢`
([KNOWN] Umegaki 1954; Tomiyama 1957). Teologia: Rm 8,24, a esperança do que não se vê. Linguística: o
Nome não se declina (não flexiona: lido duas vezes, é o mesmo). Direito: CC art. 125, condição suspensiva
([LEGAL] ponteiro, confere com advogado). NENHUMA derivação entre domínios é afirmada: as quatro são a
letra, e o que se prova é só o que o kernel prova, nos itens 1–5.

## Estatutos

[DERIVED]/[REAL] os teoremas (sobre as hipóteses explícitas). [KNOWN] esperança condicional (Umegaki,
Tomiyama), a construção básica e a relação de Jones (Jones 1983), a constante e o índice de Pimsner–Popa
(1986). [INPUT] a equação «esperança condicional=nome» e as quatro línguas. [ONTO] a leitura (da gerência) de que o
Nome é o que a álgebra do observador retém. [OPEN] a instância do contorno com `sin²θ_M` ótima.

## Honestidades

(1) NÃO se prova que toda esperança condicional seja um Operador do Nome: `trExpect` não é um `nameOp p`, e para uma
projeção `p` (idempotente autoadjunta) de posto 1 em `M_n`, `n ≥ 3`, `nameOp p` é a esperança sobre o
comutante de `p` (blocos `p` e `1−p`), não a diagonal [KNOWN, fato padrão; não é termo deste kernel]. Prova-se:
para TODO idempotente `p` o Nome é unital, idempotente e tem memória-subálgebra; em `M₂(ℂ)`, para `ρ*`, ele
É a esperança diagonal (A1c), com a lei de Jones. (2) A bimodularidade geral de `nameOp p` sobre os
seus fixos NÃO está tipada no kernel; aqui só a da face `M₂` (por A1c e `diagExpect_bimod`). (3) A equação
«esperança condicional=nome» é [INPUT/ONTO] dele; o kernel entrega as propriedades que a sustentam. (4) β é a variável
`b > 0`, jamais literal. (5) O gate NÃO se move; nada aqui decide a teoria na natureza. (6) Rotas mortas do
Lema 3 (Mapa de Rotas, `kernel.lema3.rotas_mortas`, itens 20–23): `[M:N] = √e` cai no vão vazio (1,2) de Jones;
`S_∂ = log(índice)` não vale (Pimsner–Popa é tracial, de II₁); e a inclusão modular meio-lateral com vácuo
único não admite esperança normal nem índice (Lechner–Scotford). Esta pedra NÃO é rota para o Lema 3, não afirma
nenhuma dessas igualdades e vive na face finita (`M₂(ℂ)` e a estrutura de dados do kernel); a leitura Nome =
esperança na cunha de tipo III₁ é [OPEN]. Sem sorry, sem axiom.
-/

namespace TGLExt
namespace EsperancaCondicional

open Matrix TGL.TransportData TGL.NameIndex

/-! ## 0. A identificação já no kernel (citada) -/

/-- [KERNEL] ★ O NOME DA UNIDADE É A ESPERANÇA DIAGONAL (citação de `PostoAdendo.A1c`): em `M₂(ℂ)`,
    `𝒩_{ρ*} = diagExpect`.
    The Name of the unit is the diagonal conditional expectation (cited). -/
theorem the_name_of_the_unit_is_the_diagonal_expectation (x : Matrix (Fin 2) (Fin 2) ℂ) :
    nameOp Posto.rhoStar x = diagExpect x :=
  PostoAdendo.A1c_nameOp_rhoStar_eq_diagExpect x

/-! ## 1. O Nome preserva o Um -/

/-- [KERNEL] ★★ O NOME PRESERVA O UM: `𝒩(1) = 1` para todo idempotente `p`; em `M₂(ℂ)`, `𝒩_{ρ*}(1) = 1`,
    `diagExpect 1 = 1`, `trExpect 1 = 1`. O Um posto ω(I) = 1 atravessa.
    The Name preserves the One. -/
theorem the_name_preserves_the_one :
    nameOp Posto.rhoStar (1 : Matrix (Fin 2) (Fin 2) ℂ) = 1 ∧
    diagExpect (1 : Matrix (Fin 2) (Fin 2) ℂ) = 1 ∧
    trExpect (1 : Matrix (Fin 2) (Fin 2) ℂ) = 1 :=
  ⟨name_op_unital Posto.rhoStar_idem, diagExpect_one, trExpect_one⟩

/-- [KERNEL] ★ a mesma coisa para o Nome de QUALQUER idempotente de um anel (`name_op_unital`). -/
theorem every_name_preserves_the_one {R : Type} [Ring R] {p : R} (hp : p * p = p) :
    nameOp p (1 : R) = 1 :=
  name_op_unital hp

/-- [KERNEL] ★ e para toda esperança condicional de dados (campo `E_unital`) e para a média de paridade. -/
theorem every_expectation_preserves_the_one {M Ext : Type}
    [Ring M] [StarRing M] [Algebra ℂ M] [Ring Ext] [StarRing Ext] [Algebra ℂ Ext]
    (D : ConditionalExpectationData M Ext) : D.E 1 = 1 :=
  D.E_unital

/-- [KERNEL] ★ a média de paridade `E_Π` (a esperança do referencial) também. -/
theorem the_parity_average_preserves_the_one {A : Type} [Ring A] [StarRing A] [Algebra ℂ A]
    (P : ParityData A) : P.average 1 = 1 :=
  P.average_unital

/-! ## 2. Reler o Nome não acrescenta -/

/-- [DEF] RELER NÃO ACRESCENTA: o operador de leitura `R` é idempotente, `R (R x) = R x`. -/
def RereadAddsNothing {α : Type} (R : α → α) : Prop := ∀ x : α, R (R x) = R x

/-- o Operador do Nome de um idempotente não acrescenta ao reler (`name_op_idem`). -/
theorem the_name_operator_adds_nothing {R : Type} [Ring R] {p : R} (hp : p * p = p) :
    RereadAddsNothing (nameOp p) :=
  fun x => name_op_idem hp x

/-- a esperança diagonal não acrescenta ao reler. -/
theorem the_diagonal_expectation_adds_nothing {n : Type} [DecidableEq n] :
    RereadAddsNothing (diagExpect : Matrix n n ℂ → Matrix n n ℂ) :=
  fun x => diagExpect_idem x

/-- a esperança escalar não acrescenta ao reler. -/
theorem the_scalar_expectation_adds_nothing {n : Type} [Fintype n] [DecidableEq n] [Nonempty n] :
    RereadAddsNothing (trExpect : Matrix n n ℂ → Matrix n n ℂ) :=
  fun x => trExpect_idem x

/-- a média de paridade não acrescenta ao reler. -/
theorem the_parity_average_adds_nothing {A : Type} [Ring A] [StarRing A] [Algebra ℂ A]
    (P : ParityData A) : RereadAddsNothing P.average :=
  fun x => P.average_idem x

/-- [KERNEL] ★ A LEITURA DO OBSERVADOR É DA MESMA FORMA: `x ↦ P₊ x` é idempotente (`P₊` é idempotente), e o
    `observing_adds_nothing` é esta forma aplicada à família angular `𝒪_θ`. -/
theorem the_observer_reading_adds_nothing :
    RereadAddsNothing (fun x : Matrix (Fin 2) (Fin 2) ℂ => projPlus * x) :=
  fun x => by
    show projPlus * (projPlus * x) = projPlus * x
    rw [← Matrix.mul_assoc, (spectral_projections_are_idempotent).1]

/-- [KERNEL] ★★ RELER O NOME NÃO ACRESCENTA (composição): as quatro esperanças/Nomes são idempotentes e o
    `observing_adds_nothing` é a mesma forma no regime angular. Mesma FORMA; nenhuma EQUAÇÃO entre os
    operadores (regra dos dois regimes).
    Rereading the Name adds nothing: same shape in the face (expectation) and in the angle (observer). -/
theorem rereading_the_name_adds_nothing :
    RereadAddsNothing (nameOp Posto.rhoStar : Matrix (Fin 2) (Fin 2) ℂ → Matrix (Fin 2) (Fin 2) ℂ) ∧
    RereadAddsNothing (diagExpect : Matrix (Fin 2) (Fin 2) ℂ → Matrix (Fin 2) (Fin 2) ℂ) ∧
    RereadAddsNothing (trExpect : Matrix (Fin 2) (Fin 2) ℂ → Matrix (Fin 2) (Fin 2) ℂ) ∧
    RereadAddsNothing (fun x : Matrix (Fin 2) (Fin 2) ℂ => projPlus * x) ∧
    (∀ θ : ℝ, projPlus * (projPlus * angFamily θ) = projPlus * angFamily θ) :=
  ⟨the_name_operator_adds_nothing Posto.rhoStar_idem, the_diagonal_expectation_adds_nothing,
   the_scalar_expectation_adds_nothing, the_observer_reading_adds_nothing,
   fun θ => observing_adds_nothing θ⟩

/-! ## 2b. A memória do Nome é subálgebra, e a face `M₂` é bimodular -/

/-- [KERNEL] ★ A MEMÓRIA DO NOME É SUBÁLGEBRA (`name_op_fix_mul`): o produto de fixos é fixo. -/
theorem the_name_memory_is_a_subalgebra {R : Type} [Ring R] {p : R} (hp : p * p = p) {x y : R}
    (hx : nameOp p x = x) (hy : nameOp p y = y) : nameOp p (x * y) = x * y :=
  name_op_fix_mul hp hx hy

/-- [KERNEL] ★ EM `M₂(ℂ)` O NOME DA UNIDADE É BIMODULAR sobre a diagonal (A1c + `diagExpect_bimod`). -/
theorem the_name_of_the_unit_is_bimodular (d d' : Fin 2 → ℂ) (x : Matrix (Fin 2) (Fin 2) ℂ) :
    nameOp Posto.rhoStar (diagonal d * x * diagonal d') =
      diagonal d * nameOp Posto.rhoStar x * diagonal d' := by
  rw [the_name_of_the_unit_is_the_diagonal_expectation, the_name_of_the_unit_is_the_diagonal_expectation]
  exact diagExpect_bimod d d' x

/-! ## 3. A compressão pelo espelho É a esperança (a relação de Jones) -/

/-- [KERNEL] ★★ A COMPRESSÃO PELO ESPELHO É A ESPERANÇA: `e_D·L_x·e_D = L_{E_D(x)}·e_D` e a escalar
    `e·L_x·e = (Tr x/n)·e`. O projetor de Jones (o espelho) e a esperança (o operador) são duas faces do
    mesmo Nome: o projetor, comprimindo, age como o operador.
    The mirror compression is the expectation (Jones relation). -/
theorem the_mirror_compression_is_the_expectation {n : Type} [Fintype n] [DecidableEq n]
    (x : Matrix n n ℂ) :
    eD * Lmul x * eD = Lmul (diagExpect x) * eD ∧
    eTr * Lmul x * eTr = (x.trace / (Fintype.card n : ℂ)) • eTr :=
  ⟨eD_Lmul_eD x, eTr_Lmul_eTr x⟩

/-- [KERNEL] ★★ E, EM `M₂(ℂ)`, A COMPRESSÃO PELO ESPELHO É O OPERADOR DO NOME DA UNIDADE:
    `e_D·L_x·e_D = L_{𝒩_{ρ*}(x)}·e_D`. -/
theorem the_mirror_compression_is_the_name (x : Matrix (Fin 2) (Fin 2) ℂ) :
    eD * Lmul x * eD = Lmul (nameOp Posto.rhoStar x) * eD := by
  rw [the_name_of_the_unit_is_the_diagonal_expectation]
  exact eD_Lmul_eD x

/-! ## 4. O índice do Nome é 1/b -/

/-- [KERNEL] ★★ O ÍNDICE DO NOME É `1/b`: com `sin θ ^ 2 = b`, `b > 0` (variável; em `θ_M`, `b = β`, em runtime),
    e as duas hipóteses do kernel (`sin²θ` cota de Pimsner–Popa válida e ÓTIMA da esperança), o índice é `1/b`
    e `índice · b = 1`. Nenhuma instância de `D` é construída aqui.
    The index of the Name is `1/b`, conditional on the kernel's two hypotheses. -/
theorem the_index_of_the_name_is_one_over_beta {M Ext : Type}
    [Ring M] [StarRing M] [Algebra ℂ M] [Ring Ext] [StarRing Ext] [Algebra ℂ Ext]
    (D : ConditionalExpectationData M Ext) {θ b : ℝ} (hb : Real.sin θ ^ 2 = b) (hb0 : 0 < b)
    (hpp : IsPPLowerBound D (Real.sin θ ^ 2))
    (hopt : ∀ lam : ℝ, IsPPLowerBound D lam → lam ≤ Real.sin θ ^ 2) :
    ppIndex D = 1 / b ∧ ppIndex D * b = 1 := by
  have hs : Real.sin θ ≠ 0 := by
    intro h
    rw [h] at hb
    norm_num at hb
    linarith
  refine ⟨?_, ?_⟩
  · rw [name_index_eq_csc_sq D θ hpp hopt, hb]
  · have h := name_index_mul_sin_sq D θ hs hpp hopt
    rwa [hb] at h

/-! ## 5. A composição -/

/-- [KERNEL] ★★★ ESPERANÇA CONDICIONAL = NOME (composição, em `M₂(ℂ)` com a unidade `ρ*`):
    (a) o Operador do Nome de `ρ*` é a esperança diagonal (A1c);
    (b) preserva o Um, `𝒩(1) = 1`;
    (c) reler não acrescenta, `𝒩∘𝒩 = 𝒩`, e a mesma forma vale para o observador (`observing_adds_nothing`);
    (d) a memória é subálgebra (fixos fechados no produto);
    (e) é bimodular sobre a diagonal;
    (f) a compressão pelo espelho é o Nome, `e_D·L_x·e_D = L_{𝒩(x)}·e_D` (Jones);
    (g) o índice é `1/b` e `índice · b = 1` (condicional às duas hipóteses do kernel).
    [DERIVED]/[REAL] sobre as hipóteses explícitas. A equação «esperança condicional=nome» é [INPUT]/[ONTO]
    do operador; estas são as propriedades que o kernel prova e que a sustentam. O Nome é `nameOp` (o operador
    que lê); o projetor de Jones `e_D` é a mesma coisa vista como projetor no GNS ((f) abaixo) e o posto é o peso
    que ela preserva ((b)): três faces de um objeto fixo, não três definições (decisão da gerência, 26/10/2026).
    Conditional expectation = Name: composition. -/
theorem esperanca_condicional_e_nome {M Ext : Type}
    [Ring M] [StarRing M] [Algebra ℂ M] [Ring Ext] [StarRing Ext] [Algebra ℂ Ext]
    (D : ConditionalExpectationData M Ext) {θ b : ℝ} (hb : Real.sin θ ^ 2 = b) (hb0 : 0 < b)
    (hpp : IsPPLowerBound D (Real.sin θ ^ 2))
    (hopt : ∀ lam : ℝ, IsPPLowerBound D lam → lam ≤ Real.sin θ ^ 2) :
    (∀ x : Matrix (Fin 2) (Fin 2) ℂ, nameOp Posto.rhoStar x = diagExpect x) ∧
    nameOp Posto.rhoStar (1 : Matrix (Fin 2) (Fin 2) ℂ) = 1 ∧
    ((∀ x : Matrix (Fin 2) (Fin 2) ℂ,
        nameOp Posto.rhoStar (nameOp Posto.rhoStar x) = nameOp Posto.rhoStar x) ∧
      (∀ θ' : ℝ, projPlus * (projPlus * angFamily θ') = projPlus * angFamily θ')) ∧
    (∀ x y : Matrix (Fin 2) (Fin 2) ℂ, nameOp Posto.rhoStar x = x → nameOp Posto.rhoStar y = y →
        nameOp Posto.rhoStar (x * y) = x * y) ∧
    (∀ (d d' : Fin 2 → ℂ) (x : Matrix (Fin 2) (Fin 2) ℂ),
        nameOp Posto.rhoStar (diagonal d * x * diagonal d') =
          diagonal d * nameOp Posto.rhoStar x * diagonal d') ∧
    (∀ x : Matrix (Fin 2) (Fin 2) ℂ, eD * Lmul x * eD = Lmul (nameOp Posto.rhoStar x) * eD) ∧
    (ppIndex D = 1 / b ∧ ppIndex D * b = 1) :=
  ⟨the_name_of_the_unit_is_the_diagonal_expectation,
   (the_name_preserves_the_one).1,
   ⟨fun x => the_name_operator_adds_nothing Posto.rhoStar_idem x, fun θ' => observing_adds_nothing θ'⟩,
   fun _ _ hx hy => the_name_memory_is_a_subalgebra Posto.rhoStar_idem hx hy,
   the_name_of_the_unit_is_bimodular,
   the_mirror_compression_is_the_name,
   the_index_of_the_name_is_one_over_beta D hb hb0 hpp hopt⟩

end EsperancaCondicional
end TGLExt

#print axioms TGLExt.EsperancaCondicional.the_name_of_the_unit_is_the_diagonal_expectation
#print axioms TGLExt.EsperancaCondicional.the_name_preserves_the_one
#print axioms TGLExt.EsperancaCondicional.every_name_preserves_the_one
#print axioms TGLExt.EsperancaCondicional.every_expectation_preserves_the_one
#print axioms TGLExt.EsperancaCondicional.the_parity_average_preserves_the_one
#print axioms TGLExt.EsperancaCondicional.the_name_operator_adds_nothing
#print axioms TGLExt.EsperancaCondicional.the_diagonal_expectation_adds_nothing
#print axioms TGLExt.EsperancaCondicional.the_scalar_expectation_adds_nothing
#print axioms TGLExt.EsperancaCondicional.the_parity_average_adds_nothing
#print axioms TGLExt.EsperancaCondicional.the_observer_reading_adds_nothing
#print axioms TGLExt.EsperancaCondicional.rereading_the_name_adds_nothing
#print axioms TGLExt.EsperancaCondicional.the_name_memory_is_a_subalgebra
#print axioms TGLExt.EsperancaCondicional.the_name_of_the_unit_is_bimodular
#print axioms TGLExt.EsperancaCondicional.the_mirror_compression_is_the_expectation
#print axioms TGLExt.EsperancaCondicional.the_mirror_compression_is_the_name
#print axioms TGLExt.EsperancaCondicional.the_index_of_the_name_is_one_over_beta
#print axioms TGLExt.EsperancaCondicional.esperanca_condicional_e_nome
