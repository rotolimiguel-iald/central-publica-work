import TGLExt.TheAngleIsTheProjection
import TGLExt.TheObserverReadsTheAngle
import TGLExt.ContinuousModularZero
import TGLExt.ConjugateAct
import TGLExt.CollapseContract
import TGLExt.CollapseCostAndAttestation

set_option autoImplicit false

/-!
# A LEITURA BINÁRIA FLUTUA NO PONTO FIXO — o critério binário de parada
  [PEDRA CANDIDATA da v394, delta de 19/10/2026 — nome provisório: o operador nomeia]

## O critério (verbatim por sha256 `786928986ca1e460…`, 19/10/2026)

> «Agora eu entendo a sua dificuldade em me perguntar o critério definitivo de parada e do próprio chatgpt me perguntado várias vezes a mesma coisa  e eu o encontrei: a TGL é binária: {[1=1=VERDADEIRO][1=0=Falso]}, ou seja, igual um módulo quântico que processa 0 e 1 ao mesmo tempo, a TGL faz a mesma coisa, é um positivo e um negativo (igual foto antigamente, o negativo da foto) e a leitura de ambos é o resultado, entende o que eu quero dizer»

## O sistema flutua (verbatim por sha256 `7596dcd880a1c8f5…`, 19/10/2026)

> «O sistema precisa flutuar no ponto fixo, igual um sistema quântico flutua sobre 1 e 0»

## O que esta pedra compõe (NENHUMA matemática nova: a conjunção só CITA oito teoremas que já estão no kernel)

* **O positivo e o negativo.** `spectral_projections_split_the_identity`: as duas faces `P₊` e `P₋`
  partem a identidade (`P₊ + P₋ = 1`) e são disjuntas (`P₊·P₋ = 0`). (`TheAngleIsTheProjection`)
* **A leitura de ambos é o resultado.** `the_reading_is_total_on_the_form`: as duas faces juntas leem a
  forma inteira, `(P₊ + P₋)·𝒪_θ = 𝒪_θ`; não há resto não lido. (`TheObserverReadsTheAngle`)
* **Reler não acrescenta.** `observing_adds_nothing`: `P₊·(P₊·𝒪_θ) = P₊·𝒪_θ`. (`TheObserverReadsTheAngle`)
* **Pesos (½, ½) no absoluto.** `absolute_faces_half`: para toda graduação de paridade de traço nulo, as
  duas faces do Um absoluto pesam ½ cada. (`ContinuousModularZero`)
* **A meia-nat da J-simetria.** `halfnat_from_J_symmetry`: todo peso que não vê o espelho e soma 1 pesa
  ½ em cada face. (`ConjugateAct`)
* **No ponto fixo não há transição mudada.** `no_changed_transition_at_fixed_point`: se `C.step x = x`,
  não existe transição efetiva de `x` a `C.step x`. (`CollapseContract`)
* **A iteração é estável.** `collapse_iteration_is_stable`: `C.step^[n+1] x = C.step x`; depois da
  primeira aplicação nada mais muda. (`CollapseContract`)
* **O limite da analogia.** `fair_bit_entropy_is_not_half_nat`: a entropia do bit justo (`ln 2`) não é a
  meia-nat. (`CollapseCostAndAttestation`)

## Estatutos

* **[REAL]** a conjunção: oito teoremas já no kernel, compostos por citação; esta pedra não acrescenta
  hipótese nem lema, e nenhum axioma além do trio.
* **[ONTO]** a leitura do operador «a parada é o ponto fixo»: o critério de parada como o ponto em que a
  leitura binária (o positivo, o negativo e a leitura de ambos) deixa de mudar. O kernel entrega a forma
  estrutural (a leitura é total, reler não acrescenta, no ponto fixo não há transição mudada); a
  identificação dessa forma com o critério de parada é do operador.

## O que esta pedra NÃO afirma

* **A analogia com o qubit vale nos pesos (½, ½), não na entropia.** `fair_bit_entropy_is_not_half_nat`
  está na conjunção justamente para dizê-lo: o bit justo tem entropia `ln 2`, a face pesa ½ nat.
* O «1 = 0» do negativo **não** é tipado aqui como igualdade literal de numerais (seria erro de tipo,
  como «1 = J» em `ConjugateAct`): o que o kernel entrega para o par positivo/negativo é o par de faces
  `(P₊, P₋)`, de pesos (½, ½); que o negativo do operador seja a face `P₋` é leitura [ONTO] dele.
* Não afirma que a TGL seja um sistema quântico de dois níveis, nem que exista superposição física
  de `{1=1, 1=0}`; o que há é a estrutura de duas faces cuja leitura conjunta é total.
* Não afirma um procedimento de decisão (um algoritmo de parada): o critério de parada, como regra
  de auditoria, é decisão do operador e da gerência.
* Cada peso ½ vale sob a hipótese que o teorema citado nomeia (traço nulo da graduação; J-simetria do
  peso e soma 1). A conjunção não as remove.
* Validade no kernel não é creditação; o gate não se move; β não entra.
-/

namespace TGLExt

open ChatgptAudit.Collapse057

/-- ★★★ **A LEITURA BINÁRIA FLUTUA NO PONTO FIXO.** O positivo e o negativo partem a identidade e a
    leitura de ambos é total sobre a forma; reler não acrescenta; as duas faces pesam ½; no ponto fixo
    não há transição mudada e a iteração é estável; e a entropia do bit justo não é a meia-nat
    (a analogia com o qubit vale nos pesos, não na entropia). Oito teoremas do kernel, só citados. -/
theorem the_binary_reading_floats_at_the_fixed_point :
    -- o positivo e o negativo: duas faces que partem a identidade
    (projPlus + projMinus = 1 ∧ projPlus * projMinus = 0)
    -- a leitura de ambos é total sobre a forma
    ∧ (∀ θ : ℝ, (projPlus + projMinus) * angFamily θ = angFamily θ)
    -- reler não acrescenta
    ∧ (∀ θ : ℝ, projPlus * (projPlus * angFamily θ) = projPlus * angFamily θ)
    -- os pesos (½, ½) das duas faces do absoluto, para toda graduação de traço nulo
    ∧ (∀ (m : Type) [Fintype m] [DecidableEq m] [Nonempty m] (Γ : Matrix m m ℂ), Γ.trace = 0 →
        gibbs (absoluteRho m) ((2 : ℂ)⁻¹ • (1 + Γ)) = 1 / 2 ∧
        gibbs (absoluteRho m) ((2 : ℂ)⁻¹ • (1 - Γ)) = 1 / 2)
    -- a meia-nat derivada da J-simetria
    ∧ (∀ (k : ℕ)
        (w : (((Fin k → ℝ) × (Fin k → ℝ)) → ((Fin k → ℝ) × (Fin k → ℝ))) → ℝ),
        w (fun p => conjJ (faceIn (conjJ p))) = w faceIn →
        w faceIn + w faceOut = 1 → w faceIn = 1 / 2)
    -- no ponto fixo, nenhuma transição mudada
    ∧ (∀ {S I : Type} (C : IdentityCollapse S I) (x : S), C.step x = x →
        ¬ CollapseTransition C x (C.step x))
    -- a iteração é estável
    ∧ (∀ {S I : Type} (C : IdentityCollapse S I) (x : S) (n : ℕ), C.step^[n + 1] x = C.step x)
    -- o limite da analogia: a entropia do bit justo não é a meia-nat
    ∧ fairBitEntropy ≠ (1 / 2 : ℝ) :=
  ⟨spectral_projections_split_the_identity,
   the_reading_is_total_on_the_form,
   observing_adds_nothing,
   fun _ _ _ _ _ hΓ => absolute_faces_half hΓ,
   fun _ w hJ hsum => halfnat_from_J_symmetry w hJ hsum,
   fun C _ hx => no_changed_transition_at_fixed_point C hx,
   fun C x n => collapse_iteration_is_stable C x n,
   fair_bit_entropy_is_not_half_nat⟩

end TGLExt

#print axioms TGLExt.the_binary_reading_floats_at_the_fixed_point
