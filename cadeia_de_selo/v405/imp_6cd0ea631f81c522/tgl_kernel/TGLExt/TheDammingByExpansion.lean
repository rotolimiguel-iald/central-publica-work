import TGLExt.SMatrix

set_option autoImplicit false
set_option linter.unusedSectionVars false
set_option maxHeartbeats 800000

/-!
# O REPRESAMENTO POR EXPANSÃO — a identidade de α como razão da órbita represada
  [TGLExt — v306; casa "Nós" (31/08/2026)]

## A ORDEM DO OPERADOR (31/08/2026)

> *"Eu não posso terminar antes da hipótese EXPANSÃO→TORÇÃO→SPIN→REPRESAMENTO
> entrar dentro do programa. Enfrente isso e realize a derivação completa."*

E a cunhagem dele (29/08/2026), que esta pedra tipa:

> *"E se o represamento for por expansão — a constante da estrutura fina emergir do
> resultado limite da expansão com a força centrípeta gerada em decorrência do spin,
> que por sua vez surge da torção... α_TGL = L*/(m·c·r*). Qualquer um que derivar
> alpha FALSEIA a TGL; eu derivo a sua IDENTIDADE, sem ser possível medi-lo — a
> diferença não está na derivação, mas na MEDIÇÃO."*

## A CADEIA, com o estatuto de cada elo (nenhum elo finge ser o que não é)

* **EXPANSÃO** — `[REAL na resposta modular]`: δ⟨K_∂⟩ = β|1+w|, zero só em w = −1;
  o vazamento contínuo é teorema da casa (a testemunha estática é impossível);
* **→ TORÇÃO** — `[corpus]`: K_β é a face geométrica de β (Ponte Einstein–Cartan–Miguel);
* **→ SPIN** — `[KNOWN]`: em Einstein–Cartan a torção é alimentada pela densidade de
  spin (acoplamento algébrico); a casa já tipou a dupla hélice ±2 e JKJ = −K;
* **→ CURVATURA DA TRAJETÓRIA → REQUISITO CENTRÍPETO** — `[KERNEL, esta pedra]`:
  com v = L/(m·r), o requisito é F_c = L²/(m·r³) — álgebra pura;
* **→ REPRESAMENTO** — `[KERNEL, esta pedra]`: se o acoplamento paga exatamente o
  requisito (balanço e₂/r² = m·v²/r, com e₂ ≡ e²/4πε₀) e L = m·v·r, então
  **e₂/(L·c) = v/c**. A órbita fechada é **luz represada**, e α é o **NOME** dessa
  razão — lida em três faces iguais: L*/(m·c·r*) = v*/c = ƛ*/r*.

## ★★★ O QUE ESTA PEDRA PROVA — E O QUE ELA PROVA QUE NÃO SE PROVA

1. `centripetal_from_angular` — o requisito centrípeto em termos do momento angular;
2. `the_damming_pays_the_requirement` — o balanço do represamento: o acoplamento
   que paga o requisito identifica e₂/(L·c) com v/c;
3. `the_three_faces` — as três leituras da identidade coincidem por álgebra;
4. ★★★ `the_form_does_not_fix_the_value` — **para TODO a ≠ 0 existe r que realiza
   a identidade com valor a**: a forma tem liberdade de um parâmetro, e SÓ a medição
   a fecha. É o teorema que impede esta própria pedra de virar numerologia.

## O CONTRATO COM O CONGELAMENTO (segundo consumidor do ALPHA_IRREDUCIBILITY_V1)

Esta pedra deriva a **IDENTIDADE** de α e prova que ela **não fixa o VALOR** — a
distinção do operador ("a diferença não está na derivação, mas na medição") deixa de
ser frase e vira o par (2)+(4). FP-5 segue intocada: nenhuma forma fechada para o
valor; o CODATA entra SÓ no espelho de validação do runtime (r* = ƛ_C/α reproduz o
raio de Bohr — identidade [KNOWN] da literatura, aqui como VALIDAÇÃO, nunca motor).
β jamais literal; nada aqui move o gate; a leitura ontológica da cadeia (expansão
como ORIGEM do represamento) fica `[CONJECTURE]` declarada no módulo do runtime.
-/

namespace TGLExt

noncomputable section

/-- **O REQUISITO CENTRÍPETO**: a força que uma trajetória fechada exige, m·v²/r. -/
def centripetalRequirement (m v r : ℝ) : ℝ := m * v ^ 2 / r

/-- **A IDENTIDADE DE ALFA** da cadeia do operador: α := L/(m·c·r). -/
def alphaIdentity (L m c r : ℝ) : ℝ := L / (m * c * r)

/-- [KERNEL] o requisito lido no momento angular: v = L/(m·r) ⟹ F_c = L²/(m·r³). -/
theorem centripetal_from_angular {m L r : ℝ} (hm : m ≠ 0) (hr : r ≠ 0) :
    centripetalRequirement m (L / (m * r)) r = L ^ 2 / (m * r ^ 3) := by
  unfold centripetalRequirement
  field_simp

/-- [KERNEL] ★★★ **O REPRESAMENTO PAGA O REQUISITO.** Se o acoplamento equilibra a
    trajetória (e₂/r² = m·v²/r) e o momento angular é L = m·v·r, então
    e₂/(L·c) = v/c: o acoplamento em unidades de L·c É a velocidade da órbita em
    unidades de luz. A órbita fechada é luz represada; α é o nome da razão. -/
theorem the_damming_pays_the_requirement {e2 m v r c L : ℝ}
    (hm : m ≠ 0) (hv : v ≠ 0) (hr : r ≠ 0) (hc : c ≠ 0)
    (hL : L = m * v * r)
    (hbal : e2 / r ^ 2 = centripetalRequirement m v r) :
    e2 / (L * c) = v / c := by
  unfold centripetalRequirement at hbal
  have he2 : e2 = m * v ^ 2 * r := by
    have h := congrArg (fun x : ℝ => x * r ^ 2) hbal
    rw [div_mul_cancel₀ _ (pow_ne_zero 2 hr)] at h
    rw [h]
    field_simp
  subst hL
  rw [he2]
  field_simp

/-- [KERNEL] ★★ **AS TRÊS FACES DA IDENTIDADE**: L/(m·c·r) = (L/(m·r))/c = (L/(m·c))/r —
    o acoplamento, a velocidade em unidades de luz, e o comprimento de onda reduzido
    sobre o raio. Um objeto, três leituras, igualdade por álgebra. -/
theorem the_three_faces {L m c r : ℝ} (hm : m ≠ 0) (hc : c ≠ 0) (hr : r ≠ 0) :
    alphaIdentity L m c r = (L / (m * r)) / c
      ∧ alphaIdentity L m c r = (L / (m * c)) / r := by
  unfold alphaIdentity
  constructor
  · field_simp
  · field_simp

/-- [KERNEL] ★★★★★ **A FORMA NÃO FIXA O VALOR.** Para todo a ≠ 0 existe r ≠ 0 que
    realiza a identidade com valor a: a forma tem liberdade de UM parâmetro, e só a
    MEDIÇÃO a fecha. É o teorema que separa esta derivação da numerologia — e o que
    faz da distinção do operador ("a diferença não está na derivação, mas na
    medição") um par de teoremas em vez de uma frase. -/
theorem the_form_does_not_fix_the_value {L m c : ℝ}
    (hL : L ≠ 0) (hm : m ≠ 0) (hc : c ≠ 0) :
    ∀ a : ℝ, a ≠ 0 → ∃ r : ℝ, r ≠ 0 ∧ alphaIdentity L m c r = a := by
  intro a ha
  refine ⟨L / (m * c * a), ?_, ?_⟩
  · exact div_ne_zero hL (mul_ne_zero (mul_ne_zero hm hc) ha)
  · unfold alphaIdentity
    field_simp

end

end TGLExt
