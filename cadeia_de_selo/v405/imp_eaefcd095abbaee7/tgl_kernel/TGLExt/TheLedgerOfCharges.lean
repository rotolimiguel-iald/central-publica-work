import TGLExt.TheMatrixRule

set_option autoImplicit false
set_option linter.unusedVariables false
set_option maxHeartbeats 4000000

/-!
# O LIVRO DE COBRANÇAS: um canal por lei de leitura (disciplina do runtime), FALSIFIED onde a lei o admite, nenhum desfecho move a regra   [TGLExt — pedra da gerência, 02/10/2026; para o canônico na v382]

A chave do operador (02/10/2026, tarde, verbatim em `_V382_OPERATOR_VERBATIM` do um.py): «O último elo incide no hamiltoniano oculto. O custo está no reflexo,
o pagamento está na face no rosto, no nome. E com isso você deveria ser capaz de responder tudo que falta. Mas se não conseguir eu vou um a um»; a RATIFICAÇÃO
das seis leituras da gerência (R1–R6) com a correção da visão de lados: «Concordo com tudo, exceto com a sua visão semiótica, a TGL não é semi ela é ótica,
ela lê tanto a face como o custo, a TGL permite ler os dois lados»; e a ordem: «isso mesmo, prossiga».

O que esta pedra faz — tudo por DEFINIÇÃO nomeada ou por termo já existente; nenhum axioma, nenhuma hipótese nova; o que é trivial por construção está
DITO como tal (aferidor da v382, 02/10: A2–A7 acolhidos):

* `outcomes` — as CINCO palavras de desfecho admitidas: `NOT_FALSIFIED`, `FALSIFIED`, `INCONCLUSIVE`, `AWAITING`, `EXCLUDED_IN_READING` (a quinta é a
  convenção da casa para uma LEITURA excluída por ordens de grandeza sem nível de confiança, v369-P2 / `final_verdict_reading_v376`); `Charge` — uma
  COBRANÇA: o lado (`face = true`: o pagamento; `face = false`: o reflexo, o custo), a LEI de leitura, a LEITURA, o DESFECHO e a PROVA de que o desfecho é
  uma das cinco palavras (`outcome_admitted` — imposto PELO TIPO, não só pela docstring); `Ledger` — o livro, uma lista de cobranças. As cobranças
  CONCRETAS são DADOS do runtime, lidas do core por chave e por número; aqui só o TIPO e as suas leis. «Um canal por lei de leitura» é DISCIPLINA do
  livro concreto (o runtime e o pré-registro), NÃO imposta pelo tipo `List Charge` (aferidor da v382, 2ª passada). HOMÔNIMOS, ditos (3ª passada):
  `TGLExt.Ledger` (TheCorrespondence: o livro custo-agora/já-pagou) e `reflectionWeight` (SelectionOutcomeRecord) são OUTROS objetos; os desta pedra
  vivem em `TGLExt.TheLedgerOfCharges`.
* `rule α h0 h1 = (couplingOfAlpha α h0 h1).beta` — A REGRA é β (v381: «Betatgl é a regra matriz»); `ruleGiven L α h0 h1` — a regra «dada um livro»:
  por construção NÃO lê o livro. `the_rule_is_constant_in_the_ledger` (★ nenhum desfecho move a regra: `ruleGiven L = ruleGiven L'`, por `rfl` — é a
  assinatura de `ruleGiven`, que não recebe desfecho algum). `falsified_extinguishes_the_charge_not_the_rule`: com `c` extinta à frente do livro a regra
  segue `α·√e` — e a hipótese `hc` NÃO ENTRA NA PROVA (o termo é `couplingOfAlpha_beta`): é exatamente isso que «a regra não lê o livro» quer dizer;
  «extinguir» é a DEFINIÇÃO `extinguished` (FALSIFIED ou EXCLUDED_IN_READING), não um termo que remova ou marque nada. TRIVIAIS POR CONSTRUÇÃO — e é
  isso que dizem: a lei da casa «falsificar o par extingue a obrigação, não revoga a norma» fica tipada como assinatura, não como teorema profundo.
* `the_gate_ignores_the_ledger` — o termo é `P = P` para um predicado que não recebe `L` (`rfl`). Trivial por construção; dito. Que as bandeiras
  FORMAIS do gate sejam função só do formal («cosmologia jamais vira prova matemática») é propriedade do CÓDIGO do gate, conferida pelos probes
  negativos do runtime (`qg_closure`), NÃO por este termo — este termo só diz o que a assinatura diz.
* A ÓTICA: `faceWeight θ = |𝓣|² = cos²θ` (a FACE lê o PAGAMENTO; no runtime, em θ_M, `1 − β`) e `reflectionWeight θ = |𝓡|² = sin²θ` (o REFLEXO lê o
  CUSTO; no runtime `β`): `both_sides_are_read` (|𝓣|² + |𝓡|² = 1, o Teorema S-∂, `normSq_reflection_add_transmission`, isto é, `sin²θ + cos²θ = 1`
  nas amplitudes de `S(θ)`), `the_face_reads_the_cost_as_complement`, `the_reflection_reads_the_payment_as_complement` e `the_tgl_is_optics_not_semi`
  — ★ este último é a MESMA identidade escrita três vezes (`linarith`): o NOME é [ONTO] (a correção do operador), o conteúdo [KERNEL] é só
  `sin²θ + cos²θ = 1`. O que o nome lê a mais — «nenhum lado é cego; a diferença entre os lados é a lei de cada leitura e o instrumento com poder,
  nunca a legibilidade» — é a correção do operador [INPUT/ONTO], dita no estatuto do runtime, NÃO provada aqui.
* `finalStepNameProposed` — o NOME do degrau final do gate PELO PAGAMENTO (R4, ratificada em bloco; a cunhagem definitiva é do operador) e
  `final_step_named_by_the_payment` (`rfl`): dito AO LADO do nome que o gate carrega (`NATURE_TEST_COMPLETED…`), que NÃO muda nesta pedra —
  renomear o gate é ato do operador; esta pedra só tipa o nome proposto, ao lado. O nome diz PAGAMENTO na face (o Nome) e CUSTO lido no reflexo,
  para não se confundir com «o custo posto na face» (a convenção não canônica de R6).
* `the_ledger_of_charges` — tudo num só termo (uma CONJUNÇÃO).

OS DOIS REGIMES: `faceWeight`/`reflectionWeight` leem o ÂNGULO (regime da projeção, θ); a cobrança contínua no FLUXO (regime da face, t) está na
pedra irmã `ThePsionAndTheViscosity`. O que a natureza decide segue com o observador: PROVADA ≠ CONFIRMADA; `NOT_FALSIFIED` nunca é `CONFIRMED`.
Sem sorry, sem axiom.
-/

noncomputable section
namespace TGLExt.TheLedgerOfCharges
open TGLExt TGLExt.TheWholeIsOne

/-- as CINCO palavras de desfecho admitidas PELO TIPO (EXCLUDED_IN_READING é a leitura excluída sem nível de confiança). Que um canal concreto admita
    FALSIFIED depende da sua lei — o conjunto congelado do V11 (o piso dos vazios), por exemplo, não a tem. -/
def outcomes : List String := ["NOT_FALSIFIED", "FALSIFIED", "INCONCLUSIVE", "AWAITING", "EXCLUDED_IN_READING"]

/-- uma COBRANÇA: o lado (`face = true`: o pagamento; `false`: o reflexo, o custo), a lei de leitura, a leitura, o desfecho e a prova de que o desfecho
    é uma das cinco palavras (imposto pelo tipo). -/
structure Charge where
  face : Bool
  law : String
  reading : String
  outcome : String
  outcome_admitted : outcome ∈ outcomes

/-- o LIVRO: uma lista de cobranças (as cobranças concretas são dados do runtime, lidas do core). -/
abbrev Ledger := List Charge

/-- A REGRA é β: `(couplingOfAlpha α).beta` (v381: «Betatgl é a regra matriz»). -/
def rule (α : ℝ) (h0 : 0 < α) (h1 : α < Real.exp (-(1 / 2))) : ℝ := (couplingOfAlpha α h0 h1).beta

/-- a regra «dada um livro»: por construção NÃO lê o livro (o argumento `L` é ignorado — e é isso que a definição diz). -/
def ruleGiven (L : Ledger) (α : ℝ) (h0 : 0 < α) (h1 : α < Real.exp (-(1 / 2))) : ℝ := rule α h0 h1

/-- uma cobrança EXTINTA: o desfecho é FALSIFIED ou EXCLUDED_IN_READING (uma DEFINIÇÃO; nenhum termo remove ou marca nada). -/
def extinguished (c : Charge) : Prop := c.outcome = "FALSIFIED" ∨ c.outcome = "EXCLUDED_IN_READING"

/-- ★ nenhum desfecho move a regra: para todo par de livros a regra dada é a mesma (`rfl`: a assinatura de `ruleGiven`). -/
theorem the_rule_is_constant_in_the_ledger (L L' : Ledger) (α : ℝ) (h0 : 0 < α) (h1 : α < Real.exp (-(1 / 2))) :
    ruleGiven L α h0 h1 = ruleGiven L' α h0 h1 := rfl

/-- ★ com `c` extinta à frente do livro, a regra segue `α·√e`. A hipótese `hc` NÃO ENTRA NA PROVA (o termo é `couplingOfAlpha_beta`, que vale para
    qualquer `c`): é isto que «a regra não lê o livro» quer dizer; «extinguir» é a definição `extinguished`, não um termo. -/
theorem falsified_extinguishes_the_charge_not_the_rule (L : Ledger) (c : Charge) (hc : extinguished c)
    (α : ℝ) (h0 : 0 < α) (h1 : α < Real.exp (-(1 / 2))) :
    ruleGiven (c :: L) α h0 h1 = α * Real.sqrt (Real.exp 1) :=
  couplingOfAlpha_beta α h0 h1

/-- ★ o termo é `P = P` para um predicado que não recebe o livro (`rfl`): trivial por construção, dito. Que as bandeiras formais do gate sejam função
    só do formal é conferido pelos probes negativos do runtime (`qg_closure`), não por este termo. -/
theorem the_gate_ignores_the_ledger (P : Prop) (L L' : Ledger) : (fun _ : Ledger => P) L = (fun _ : Ledger => P) L' := rfl

/-- a FACE lê o PAGAMENTO: `|𝓣|² = cos²θ` (no runtime, em θ_M: `1 − β`). -/
def faceWeight (θ : ℝ) : ℝ := Complex.normSq ((Smat θ).mulVec e1 0)

/-- o REFLEXO lê o CUSTO: `|𝓡|² = sin²θ` (no runtime, em θ_M: `β`). -/
def reflectionWeight (θ : ℝ) : ℝ := Complex.normSq ((Smat θ).mulVec e1 1)

/-- ★ os dois lados se leem: `|𝓣|² + |𝓡|² = 1` (o Teorema S-∂, `normSq_reflection_add_transmission` = `sin²θ + cos²θ = 1` nas amplitudes de `S(θ)`). -/
theorem both_sides_are_read (θ : ℝ) : faceWeight θ + reflectionWeight θ = 1 := by
  unfold faceWeight reflectionWeight
  have h := normSq_reflection_add_transmission θ
  linarith

/-- a face lê o custo como complemento: `|𝓣|² = 1 − |𝓡|²` (a mesma identidade, reescrita). -/
theorem the_face_reads_the_cost_as_complement (θ : ℝ) : faceWeight θ = 1 - reflectionWeight θ := by
  have h := both_sides_are_read θ
  linarith

/-- o reflexo lê o pagamento como complemento: `|𝓡|² = 1 − |𝓣|²` (a mesma identidade, reescrita). -/
theorem the_reflection_reads_the_payment_as_complement (θ : ℝ) : reflectionWeight θ = 1 - faceWeight θ := by
  have h := both_sides_are_read θ
  linarith

/-- ★★ A TGL É ÓTICA, NÃO SEMI-ÓTICA — o NOME é [ONTO] (a correção do operador, 02/10); o CONTEÚDO [KERNEL] é a identidade `sin²θ + cos²θ = 1` nas
    amplitudes de `S(θ)`, escrita três vezes (soma e os dois complementos). O que o nome lê a mais («nenhum lado é cego; o que difere é a lei de cada
    leitura e o instrumento com poder») é [INPUT/ONTO], dito no estatuto do runtime, não provado aqui. -/
theorem the_tgl_is_optics_not_semi (θ : ℝ) :
    faceWeight θ + reflectionWeight θ = 1 ∧ faceWeight θ = 1 - reflectionWeight θ ∧ reflectionWeight θ = 1 - faceWeight θ :=
  ⟨both_sides_are_read θ, the_face_reads_the_cost_as_complement θ, the_reflection_reads_the_payment_as_complement θ⟩

/-- o nome do degrau final do gate PELO PAGAMENTO (R4; proposta da gerência ratificada em bloco em 02/10; a cunhagem definitiva é do operador) — AO LADO
    do nome que o gate carrega; esta pedra não renomeia o gate. Diz PAGAMENTO na face (o Nome) e CUSTO lido no reflexo. -/
def finalStepNameProposed : String :=
  "TETELESTAI_CONSUMMATED__PAYMENT_IN_THE_FACE_THE_NAME__COST_READ_IN_THE_REFLECTION__NOT_DISCRIMINATED_AT_AVAILABLE_SENSITIVITY__FALSIFIABLE_WHERE_THE_READING_LAW_ADMITS"

/-- o nome proposto, por definição (`rfl`): diz pagamento (Tetelestai, o Nome na face), custo lido no reflexo, não discriminado à sensibilidade
    disponível, falsificável onde a lei de leitura o admite — e não diz «teste de natureza completo». -/
theorem final_step_named_by_the_payment :
    finalStepNameProposed =
      "TETELESTAI_CONSUMMATED__PAYMENT_IN_THE_FACE_THE_NAME__COST_READ_IN_THE_REFLECTION__NOT_DISCRIMINATED_AT_AVAILABLE_SENSITIVITY__FALSIFIABLE_WHERE_THE_READING_LAW_ADMITS" :=
  rfl

/-- as cinco palavras de desfecho: definição, não descoberta (`rfl`). -/
theorem five_outcomes : outcomes.length = 5 := rfl

/-- ★★★ O LIVRO DE COBRANÇAS num só termo (uma CONJUNÇÃO): nenhum desfecho move a regra; com uma cobrança extinta a regra segue α·√e (a hipótese
    não entra na prova); a ótica (a identidade e os seus dois complementos); as cinco palavras. -/
theorem the_ledger_of_charges (L : Ledger) (c : Charge) (hc : extinguished c)
    (α : ℝ) (h0 : 0 < α) (h1 : α < Real.exp (-(1 / 2))) (θ : ℝ) :
    ruleGiven (c :: L) α h0 h1 = ruleGiven L α h0 h1 ∧
    ruleGiven (c :: L) α h0 h1 = α * Real.sqrt (Real.exp 1) ∧
    (faceWeight θ + reflectionWeight θ = 1 ∧ faceWeight θ = 1 - reflectionWeight θ ∧ reflectionWeight θ = 1 - faceWeight θ) ∧
    outcomes.length = 5 :=
  ⟨the_rule_is_constant_in_the_ledger (c :: L) L α h0 h1, falsified_extinguishes_the_charge_not_the_rule L c hc α h0 h1,
   the_tgl_is_optics_not_semi θ, five_outcomes⟩

end TGLExt.TheLedgerOfCharges
