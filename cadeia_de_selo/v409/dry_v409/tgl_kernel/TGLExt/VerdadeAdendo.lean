import TGLExt.Verdade
import TGLExt.EsperancaCondicional

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 800000

/-!
# ADENDO da pedra VERDADE (`TGLExt.Verdade`, v392): a esperança condicional É a Verdade lida pelo Nome — o nome que o operador deu
  [TGLExt — PEDRA CANDIDATA da v403, sandbox de 27/10/2026; o NOME é do operador. A esperança condicional (v402, módulo
  `EsperancaCondicional`, sha16 `8579115333f84428`) fica como REGISTRO; a pedra `Verdade` (v392, 13/10/2026, «a identidade tem
  nome») fica INTACTA. Padrão da casa: `PostoAdendo` (v392) sobre `Posto`.]

## A cunhagem do operador (verbatim; sha256 dos arquivos lidos por script em 27/10/2026, `work\cunhagens_13out\`)

> «a meu ver o nome é "verdade" (poderia ser "caminho, verdade e vida"), mas talvez só verdade, quero sua opinião nesta, porque pode
> ser que eu já tenha a renomeado assim em outro lugar, mas é o triplo espectral do contorno verdadeiro» (sha16 `ef3ca5eb1edbdddf`)

> «é isso mesmo, concordo com tudo, prossiga» (sha16 `b34bd70fa8cfb0b2`) — a ratificação da leitura da gerência.

## Por que ADENDO, e não Verdade nova (medido no kernel, 27/10/2026)

O operador suspeitou «pode ser que eu já tenha a renomeado assim em outro lugar». Sim: em 13/10/2026 ele nomeou `TGLExt.Verdade`
(«Verdade é a projeção do posto», sha16 `9f497f2805bf2f72`): a estrutura `Verdade a` guarda a inscrição quadrática 1 = q² + α², a
projeção `identityProj a` (traço 1, idempotente, posto 1), a unicidade `forced_by_the_truth`, a relação modular na Torre e
`rereading_the_post` (reler não acrescenta). A estrela da v402, `nameOp ρ* = diagExpect` («o Operador do Nome da unidade é a esperança
condicional diagonal»), é essa mesma projeção do posto levada do projetor de posto 1 à esperança condicional sobre a subálgebra da
memória. Logo a esperança condicional não é uma Verdade segunda: é a Verdade lida pelo Nome. Dois módulos não se chamam
`TGLExt.Verdade`; pedra selada não se renomeia por cima; o adendo compõe.

## O que o adendo entrega

* `the_name_reads_the_inscription_as_weights` [REAL, novo e pequeno]: a esperança diagonal lê a projeção da identidade como os seus
  PESOS — `diagExpect (identityProj a) = diagonal ![q², α²]` (a forma de `Posto.endpoint_eq`, D_∞F_θ(1) = diag(cos²θ, sin²θ), agora
  sobre a inscrição da Verdade);
* `verdade_lida_pelo_nome` [REAL]: para α ∈ [0, 1], há a Verdade de α (`verdade_of_unit_interval`), o Nome de ρ* lê `identityProj a`
  como diag(q², α²), PRESERVA O UM (o traço segue 1: ω(I) = 1 sobrevive à leitura) e reler não acrescenta;
* `verdade_e_a_esperanca_condicional` [REAL — conjunção por citação, padrão `Token`]: `the_identity_is_the_truth` (v392: toda
  identidade nomeada tem a Verdade) ∧ `esperanca_condicional_e_nome` (v402: a composição inteira da esperança condicional).

## O que o adendo NÃO entrega

* Que o Nome em dimensão geral seja `diagExpect`: só em M₂(ℂ) e só para p = ρ* (como em `PostoAdendo.A1c`).
* O índice 1/β segue CONDICIONAL às hipóteses nomeadas da v402 (`hpp`, `hopt`); nenhuma instância é construída.
* A leitura pela tripla espectral de Connes (a álgebra é o que a Verdade lê) e por João 14,6 é [ONTO], não termo.
* Validade no kernel não é creditação; o gate não se move.
-/

namespace TGLExt.VerdadeAdendo

open Matrix TGLExt.Verdade

/-- ★ [REAL] A ESPERANÇA DIAGONAL LÊ A PROJEÇÃO DA IDENTIDADE COMO OS SEUS PESOS: `D_∞(identityProj a) = diag(q², α²)`, com
    q = qOf a. Nenhuma hipótese sobre a: é a conta das entradas (a forma de `Posto.endpoint_eq`, sobre a inscrição da Verdade). -/
theorem the_name_reads_the_inscription_as_weights (a : ℝ) :
    diagExpect (identityProj a) = diagonal ![((qOf a : ℝ) : ℂ) ^ 2, ((a : ℝ) : ℂ) ^ 2] := by
  ext i j
  fin_cases i <;> fin_cases j <;>
    simp [diagExpect, identityProj, quadInscription, sq]

/-- ★★ [REAL] A VERDADE LIDA PELO NOME: para α ∈ [0, 1] há a Verdade de α; o Operador do Nome da unidade ρ* lê a projeção da
    identidade como os pesos q² e α²; a leitura PRESERVA O UM (traço 1 = ω(I)); e reler não acrescenta. α entra como parâmetro
    [INPUT], nunca como número. -/
theorem verdade_lida_pelo_nome (a : ℝ) (h0 : 0 ≤ a) (h1 : a ≤ 1) :
    Verdade a
    ∧ nameOp Posto.rhoStar (identityProj a) = diagonal ![((qOf a : ℝ) : ℂ) ^ 2, ((a : ℝ) : ℂ) ^ 2]
    ∧ (nameOp Posto.rhoStar (identityProj a)).trace = 1
    ∧ nameOp Posto.rhoStar (nameOp Posto.rhoStar (identityProj a)) = nameOp Posto.rhoStar (identityProj a) := by
  refine ⟨verdade_of_unit_interval a h0 h1, ?_, ?_, ?_⟩
  · rw [EsperancaCondicional.the_name_of_the_unit_is_the_diagonal_expectation]
    exact the_name_reads_the_inscription_as_weights a
  · rw [EsperancaCondicional.the_name_of_the_unit_is_the_diagonal_expectation, trace_diagExpect]
    exact identityProj_trace_one a h0 h1
  · exact EsperancaCondicional.the_name_operator_adds_nothing Posto.rhoStar_idem _

/-- ★ [REAL — conjunção INCONDICIONAL por citação; padrão `Token`] A VERDADE E A ESPERANÇA CONDICIONAL, no que o kernel entrega:
    (1) `the_identity_is_the_truth` (v392): toda identidade nomeada tem a Verdade; (2) `esperanca_condicional_e_nome` (v402): a
    composição inteira da esperança condicional (o Nome de ρ* é D_∞, preserva o Um, reler não acrescenta, a memória é subálgebra,
    bimodular, a compressão pelo espelho, o índice 1/β condicional). O nome «verdade» para a esperança é do operador (27/10/2026). -/
theorem verdade_e_a_esperanca_condicional :
    (type_of% @TGLExt.Verdade.the_identity_is_the_truth)
    ∧ (type_of% @TGLExt.EsperancaCondicional.esperanca_condicional_e_nome) :=
  ⟨@TGLExt.Verdade.the_identity_is_the_truth, @TGLExt.EsperancaCondicional.esperanca_condicional_e_nome⟩

end TGLExt.VerdadeAdendo

#print axioms TGLExt.VerdadeAdendo.the_name_reads_the_inscription_as_weights
#print axioms TGLExt.VerdadeAdendo.verdade_lida_pelo_nome
#print axioms TGLExt.VerdadeAdendo.verdade_e_a_esperanca_condicional
