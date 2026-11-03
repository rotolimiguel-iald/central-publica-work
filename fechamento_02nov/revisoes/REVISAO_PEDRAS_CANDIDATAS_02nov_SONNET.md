# REVISÃO ADVERSARIAL DAS TRÊS PEDRAS CANDIDATAS (02/11/2026) — COMPLETA

> **STATUS: COMPLETA** (regravada sobre a versão PARCIAL, que a coordenação mandou gravar antes porque a sessão reiniciou duas vezes). Mudanças da regravação: conferidos os três detalhes de nome que ficaram pendentes (§6); corrigido o escopo do homônimo `transmitted` (está em `TGLExt` direto, não em subnamespace); corrigida a frase sobre o que a pedra A cita da fala ratificada; acrescentada a nota [ONTO] sobre «Um inscrito = vácuo» em C.

**Revisor:** Sonnet (revisor distinto, cético-aferidor; quem constrói não é quem aprova). **Modo:** só-leitura. Não rodei `lake build` nem `lean`; não toquei em `C:\t\k405c\final`; não modifiquei as pedras. Único arquivo escrito: este.
**Base da revisão:** as fontes e as saídas `_saida.txt` ao lado (os `.txt` mostram `#print axioms` no trio e `rc 0` para 12, 12 e 7 teoremas). Confio nelas como registro de compilação; não as reproduzi.

| pedra | arquivo | sha16 lido por script | teoremas |
|---|---|---|---|
| A | `work\k_guarda_travessia_02nov\KEhATangenteCandidata.lean` | `f1481d767a72b042` (confere com a r2 da memória) | 12 |
| B | `work\beta_calor_02nov\APonteDoAtritoCandidata.lean` | `b8b81dfd2677ee7c` | 12 |
| C | `work\fechamento_02nov\OUmInscritoCandidata.lean` | `192918128ba74e48` (confere com a memória) | 7 |

Kernel lido (só-leitura) em `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\` (abreviado `K:`): `PonteDaMassa`, `TheLedgerOfCharges`, `TheSelectionIsTheBallast`, `TheVerbalCoupling`, `SMatrix`, `ProjecaoTransversalDaMeiaNat`, `MassaTensaoPura`, `ThePsionAndTheViscosity`, `O16/PolarMinimalPeriod_v2`, `O16/PeriodHeatCalibration_v3`, `BoostHeatConstruction`, `TheImportedSecondQuantization`, `QGReaderUVLock`, `F1Fecho394/{BosonicFock,CanonicalGammaNoFixedR4,ExponentialTotalityR4}`, `TheAngleIsTheProjection`, `ContinuousModularZero`, `Fundacao`.

---

## 0. RESUMO PARA DECIDIR (o que muda a decisão)

Nenhum teorema está matematicamente errado: todos compilam no trio e os enunciados são verdadeiros. Os defeitos são de **docstring** (dizer mais do que o termo prova, ou não dizer que o termo é trivial) e de **leitura escondida**. Nenhum exige reprovar uma pedra; seis pedem reparo obrigatório antes de levar ao operador:

1. **A, `o_angulo_e_lido_do_absoluto` + `transicaoLida`** (`KEhA…:120,131-136`): a docstring diz «**nao e escrito**». É falso como está: a definição escreve o peso `1 / 2` (linha 120). O teorema é só `rw [peso_da_face_absoluta]` (linhas 135-136). É exatamente a «coincidência de valor, não ponte» que o kernel já avisa (`K:PonteDaMassa.lean:245-246` e `275-276`). **REPARO OBRIGATÓRIO.**
2. **A, `massa_derivada_eq_projecao_div_K`** (93-104): em toda `TransicaoParaAMassa` o `K` vale 1 (θ = π/4 é forçado); «dividida por K» não tem conteúdo de K. E `no_posto_o_acorde_e_a_projecao` (107-113) repete `K:PonteDaMassa.lean:181`.
3. **B, o rótulo «Clausius»** (cabeçalho 15 e 19-20; linhas 57 e 81): `δS := δQ/T` é DEFINIÇÃO; e o kernel diz que `κ/2π` é «normalização herdada **sem Unruh/KMS**» (`K:BoostHeatConstruction.lean:16`), enquanto o cabeçalho de B escreve «(Unruh/BW, [KNOWN])» (linha 29). É citação de literatura, não termo.
4. **B, a ponte ★ `o_atrito_lido_na_temperatura`** (74-79) e **`o_balanco_fecha_a_cada_volta`** (99-101): álgebra trivial por definição, sem a marca de trivial nem de [ONTO] na docstring; o segundo é o teorema que o próprio kernel chama de «TRIVIAL POR DEFINIÇÃO» (`K:ThePsionAndTheViscosity.lean:87-88`) e aqui vira «o equilíbrio das contas (operador)».
5. **B, `no_zero_absoluto_a_parcela_quitaria`** (130-141): é cálculo sobre uma função genérica `1 − e^{−q/T}`; não fala do modelo; a docstring não diz.
6. **C, «único autovetor» / «o espectro pontual da luz é o Um e só ele; o resto é contínuo»** (cabeçalho 15 e 20-21; linha 55): o termo prova só que o **vetor FIXO** (autovalor 1 do grupo todo) é o vácuo. Autovetores com fase nos setores de n ≥ 1 partículas e «o resto é contínuo» não têm termo.

---

## 1. PEDRA A — `KEhATangenteCandidata.lean`

Convenções: «dito» = a docstring/cabeçalho já admite a trivialidade ou a leitura; «não dito» = falta.

**Definição `K θ := Real.tan θ` (34).** Em Lean `tan` em π/2 vale 0 (convenção a/0 = 0). Por isso `K_eq_projecao_div_derivada` e `K_sq_eq_custo_div_pagamento` valem sem hipótese sobre `cos θ`: em `cos θ = 0` os dois lados são o 0 de Lean e a leitura física (K → ∞) não vale. Inofensivo, mas não dito.

| # | teorema (linha) | o que prova de fato | trivial? dito? | veredito |
|---|---|---|---|---|
| A1 | `K_eq_projecao_div_derivada` (40-42) | `tan θ = sin θ / cos θ` (mathlib `tan_eq_sin_div_cos`). O enunciado escreve `Real.cos θ`, **não** `deriv projecaoTransversal θ`. | trivial, **não dito**; a docstring diz «dividida pela sua derivada», mas `cos` ser a derivada está em `projecao_hasDerivAt` (`K:PonteDaMassa.lean:79`), que o enunciado não cita | **APROVADO COM REPARO** |
| A2 | `K_sq_eq_custo_div_pagamento` (45-47) | `tan² = sin²/cos²` pelos lemas `normSq_reflection` / `normSq_transmission` (`K:SMatrix.lean:241,247`). «custo/pagamento» é o nome que o kernel dá a `reflectionWeight`/`faceWeight` (`K:TheLedgerOfCharges.lean:96-100`), [ONTO] da chave de 02/10 | trivial, **não dito** | **APROVADO COM REPARO** |
| A3 | `crivo_iff_posto` (50-59) | conteúdo real: `Real.injOn_tan` em `(−π/2, π/2)`. `h0 : 0 ≤ θ` e `h1 : θ < π/2` estão no enunciado **e** na docstring («em `[0, π/2)`») | não trivial; restrição dita | **APROVADO** |
| A4 | `a_selecao_justa_passa` (62-64) | `fair_selection_opens_forty_five` (`K:TheSelectionIsTheBallast.lean:129`) + `tan(π/4) = 1` | composição de dois termos, não dito | **APROVADO** |
| A5 | `K_sq_no_angulo_de_miguel` (67-75) | `tan²(θ_M) = β/(1−β)`, com `0 ≤ β` e `β < 1` no enunciado. Conta real (`sin_thetaMiguel`, `sin²+cos²`) | não trivial; hipótese dita | **APROVADO** |
| A6 | `miguel_nao_passa` (78-80) | `K² < 1` se `β < 1/2` (hipótese no enunciado e na docstring) | álgebra | **APROVADO** (ver nota H-A2) |
| A7 | `miguel_e_a_mesma_regra_de_leitura` (83) | `rfl`: `thetaMiguel` (`K:TheVerbalCoupling.lean:126`) e `selectionAngle` (`K:TheSelectionIsTheBallast.lean:98`) são a mesma expressão `arcsin (√·)` | trivial **e dito** («por definicao») | **APROVADO** |
| A8 | `miguel_aponta_para_o_posto` (87-90) | `K²(θ_M(β)) = 1 ↔ β = 1/2`, álgebra de `β/(1−β) = 1` | trivial, **não dito**; a docstring cola a frase do operador («reflete o posto, porque aponta pra ele») a este iff | **APROVADO COM REPARO** |
| A9 | `massa_derivada_eq_projecao_div_K` (93-104) | ver H-A1 abaixo | não dito | **APROVADO COM REPARO** |
| A10 | `no_posto_o_acorde_e_a_projecao` (107-113) | **repete** `TransicaoParaAMassa.massa_derivada_eq_projecao` (`K:PonteDaMassa.lean:181-186`), pela rota de `K = 1` | redundante, não dito | **APROVADO COM REPARO** (ou omitir) |
| A11 | `transicaoLida` (def, 116-129) | `TransicaoParaAMassa` com `theta := selectionAngle (1 / 2)`; os quatro campos provam | o `1 / 2` está **escrito** na linha 120 | **APROVADO** (def.) com docstring corrigida |
| A12 | `o_angulo_e_lido_do_absoluto` (132-136) | ver H-A3 | docstring falsa em «nao e escrito» | **REPARO OBRIGATÓRIO** |
| A13 | `transicao_lida_eq_derivada` (139-145) | 1º termo = `fair_selection_opens_forty_five`; 2º = `massa_derivada_eq_beta_mul` (`K:PonteDaMassa.lean:174`), que vale para **toda** `T`, nada específico de `transicaoLida` | composição, não dito | **APROVADO** |

### Hipóteses escondidas e leituras (A)

- **H-A1 (A9, A10): K ≡ 1 dentro do tipo.** Correção ao enunciado da pergunta: `theta_eq_pi_div_four` (`K:PonteDaMassa.lean:147`) **não é campo**, é **teorema** derivado do campo `autoconjugado : sin²θ = 1 − sin²θ` (linha 140) por `forty_five_unique`. Efeito: para toda `T`, `K T.theta = 1` (a própria pedra o mostra em 110-112). `massa_derivada_eq_projecao_div_K` reduz-se a `E·cos θ = E·sin θ / tan θ` em π/4, isto é, divisão por 1. O cabeçalho (19-21) diz certo («no posto K = 1 e as duas coincidem»); o **nome e a docstring do teorema** sugerem uma relação que varia com K, e dentro de `TransicaoParaAMassa` ela não varia. A admissão «a hipótese não some: muda do número para a regra de leitura» (cabeçalho 22-24) está escrita só para `transicaoLida`, não para este teorema.
  *Texto sugerido para A9:* «Para toda `T`, `K T.theta = 1` (θ = π/4 vem de `autoconjugado`); logo a divisão por `K` é por 1 e este teorema não distingue K de 1. A forma geral é a identidade trigonométrica `cos θ = sin θ / tan θ`.»
  *Opcional (não testado):* enunciar um lema geral, independente de `T`: `sin θ ≠ 0 → cos θ ≠ 0 → deriv projecaoTransversal θ = projecaoTransversal θ / K θ`.
- **H-A2 (A6, A8): «jamais» depende de um número.** A docstring cita «Miguel jamais será o posto … aponta pra ele»; o teorema prova `K² < 1` **se β < 1/2**. Que `β_TGL ≈ 0,0120 < 1/2` é número, não termo da pedra (o kernel só dá `0 < β < 1` em `TGLCoupling`, `K:TheSameBetaReadsThreeFaces.lean:22-25`). Além disso, «reflete» e «aponta» não têm outro conteúdo formal que o iff de A8 (não há monotonia nem limite β → 1/2 na pedra). A docstring (85-86) cita «é angulo de abertura de leitura, reflete o posto, porque aponta pra ele» e **omite** o «Miguel jamais será o posto» da fala ratificada (verbatim na memória `k-chave-da-guarda-02nov`); esse «jamais» só tem `miguel_nao_passa`, que dá `K² < 1` (não `¬ crivo`) e só sob `β < 1/2`.
  *Texto sugerido para A8:* «[ONTO] A tradução de "aponta pra ele" é só esta: `K²(θ_M(β)) = 1 ↔ β = 1/2` (álgebra de `K_sq_no_angulo_de_miguel`). "Jamais" vale enquanto `β < 1/2`; que `β_TGL ≈ 0,0120` satisfaz isso é número, fora desta pedra.»
  *Opcional (não testado):* corolário `¬ crivo (thetaMiguel β)` para `0 ≤ β < 1/2`.
- **H-A3 (A12, A11): «lido do absoluto, não escrito» é falso como está.** Fatos medidos: (i) a prova é `show selectionAngle (1 / 2) = _; rw [peso_da_face_absoluta hΓ]` (135-136) e **não prova nada além desse `rw`**: responde à pergunta 5; (ii) o `1 / 2` é escrito na definição (120), assim como `π/4` é escrito em `transicaoDerivada` (`K:PonteDaMassa.lean:268`); (iii) o kernel já nomeou o que isso é: «coincidência de valor, não ponte … que o estado inscrito seja lido nesse peso é a leitura do operador [ONTO]» (`K:PonteDaMassa.lean:245-246`, `275-276`) e «SE a projeção transversal pesa o que a face absoluta pesa (a premissa `hθ`, que é a leitura)» (256). O ganho real é modesto e honesto: o ângulo deixa de ser um ângulo escrito e passa a ser a **saída de uma regra existente** (`selectionAngle`) aplicada a um peso, e esse peso é mostrado igual ao da face absoluta. O cabeçalho (22-24) diz isso; a docstring do teorema (131) contradiz o cabeçalho.
  *Texto sugerido (A12):* «`θ` de `transicaoLida` é `selectionAngle` aplicada ao peso ½; esse ½ está escrito na definição e é, em valor, o peso da face absoluta (`peso_da_face_absoluta`): coincidência de valor, não ponte. Que o estado inscrito seja lido nesse peso é a leitura [ONTO] do operador.»
  *Texto sugerido (A11):* trocar «em vez de escrito» por «o ângulo vem da regra de seleção aplicada ao peso ½ (escrito)».
  *Opcional (código, não testado):* para tornar «lido» literal, `transicaoLida` poderia receber `(Γ, hΓ)` e definir `theta := selectionAngle (gibbs (absoluteRho n) ((2:ℂ)⁻¹ • (1 + Γ))).re`, usando `peso_da_face_absoluta` nas obrigações dos campos. Mesmo assim, «o estado inscrito é lido nesse peso» continuaria [ONTO].

### Homônimos (A)

- **K:** o cabeçalho (26) lista dois (Hubble, modular) e omite o mais próximo: `TGLExt.genK`, a matriz `!![0,1;-1,0]` (`K:TheAngleIsTheProjection.lean:76`), com `angFamily θ = cos θ • 1 + sin θ • genK` (85-86). Lá o coeficiente de `genK` é `sin θ`; `tan θ` é a **razão** dos coeficientes. A ponte «K escalar = razão dos coeficientes de genK e de 1» é leitura, sem termo na pedra. Há ainda `abbrev K` em `F1Fecho394/WeylExponentialGraphCoreR4.lean:15` (outro objeto, outro namespace).
- **«posto»:** a pedra usa «o posto» (docstrings 15, 49, 85) para o ponto autoconjugado (peso ½, ângulo π/4). No kernel há `umPosto := 1` (`K:PonteDaMassa.lean:290`, a unidade posta) e o módulo `TGLExt.Posto` (posto = rank/nome). Três sentidos; a pedra não define o seu.
- **`reflectionWeight`:** a pedra usa a de `TGLExt.TheLedgerOfCharges` (θ : ℝ). Existe outra, `ChatgptAudit.SelectionRecord.reflectionWeight (A : QubitMatrix)` (`K:SelectionOutcomeRecord.lean:51`), em namespace que a pedra não abre: sem colisão (e `K:TheLedgerOfCharges.lean:24` já avisa).

---

## 2. PEDRA B — `APonteDoAtritoCandidata.lean`

**Leitura declarada [ONTO].** `calorDaVolta := β·g` está marcada como leitura do operador, tipada como definição e não derivada, em dois lugares (cabeçalho 14-15; docstring 54). Isso está **bem dito**. O que **não** está marcado é tudo o que depende dela: «Clausius» (15, 57, 81), «peso de Boltzmann» (72-73), «fecha como balanço de Clausius» (19-20, 81).

**Dimensões (pergunta 3).** Consistentes sob ħ = k_B = 1: `transmitted β g t = exp(−t·β·g)` (`K:ThePsionAndTheViscosity.lean:82`) obriga `β·g` a ser uma **taxa** (1/tempo modular); com ħ = 1, taxa = energia; `T = 1/P` também é 1/tempo; `δS = βg·P` é adimensional. Mas `βg` é uma **largura de decaimento**, não uma diferença de energia: `e^{−βg/T}` é a sobrevivência após um tempo térmico `1/T`, que tem a mesma forma de `e^{−E/T}`. «Peso de Boltzmann» é, portanto, rótulo da leitura [ONTO], não derivação.

| # | teorema (linha) | o que prova de fato | trivial? dito? | veredito |
|---|---|---|---|---|
| B1 | `temperatura_e_kappa_sobre_dois_pi` (45-46) | re-exporta `reciprocal_temperature` (`K:O16/PolarMinimalPeriod_v2.lean:104`) | trivial, **dito** (cita o termo) | **APROVADO** |
| B2 | `o_zero_absoluto_nao_e_lido` (49-52) | `0 < 1/P` por `positivity`, a partir do **campo** `period_pos` (`K:MassaTensaoPura.lean:139`) | trivial por campo, **não dito** (o nome sugere física; o cabeçalho 27 diz «T > 0 vem de κ > 0», mas a docstring do teorema não) | **APROVADO COM REPARO** |
| B3 | `entropia_e_calor_vezes_periodo` (61-63) | `δS = δQ·P`, álgebra (vale sem `P ≠ 0` por `a/0 = 0` em Lean) | trivial; `δS` é definição (58) | **APROVADO** |
| B4 | `entropia_e_dois_pi_calor_sobre_kappa` (66-70) | `δS = 2π·δQ/κ` via B1 | trivial | **APROVADO** |
| B5 | ★ `o_atrito_lido_na_temperatura` (74-79) | `exp(−(P·β·g)) = exp(−((β·g)/(1/P)))`: **álgebra pura** depois de desdobrar `temperatura` e `calorDaVolta`, ambas definidas pela própria pedra. O kernel só contribui `T = κ/2π` (B1) | trivial por definição, **não dito**; «peso de Boltzmann» sem [ONTO] | **APROVADO COM REPARO** |
| B6 | `a_parcela_e_um_menos_o_peso` (82-86) | `parcelaPorVolta = 1 − e^{−δS}`, definitório (`show … rw … rfl`) | trivial, **não dito**; «o balanço da volta fecha como Clausius» é excesso | **APROVADO COM REPARO** |
| B7 | `a_parcela_nao_excede_a_entropia` (89-96) | `parcela_le_beta` (`K:MassaTensaoPura.lean:164`) reescrita: `1 − e^{−x} ≤ x` | trivial, **dito** («em forma de temperatura») | **APROVADO** |
| B8 | `o_balanco_fecha_a_cada_volta` (99-101) | é `the_charge_is_continuous_both_sides` (`K:ThePsionAndTheViscosity.lean:89`), que o kernel chama «TRIVIAL POR DEFINIÇÃO (`charged := 1 − transmitted`; `ring`), dito» | trivial, **não dito aqui**; atribuído a «o equilíbrio das contas (operador)» | **APROVADO COM REPARO** |
| B9 | `o_expoente_decai_por_volta` (104-109) | `exp(−nx) = exp(−x)^n` (`Real.exp_nat_mul`) | trivial, **não dito** | **APROVADO** |
| B10 | `o_peso_entre_zero_e_um` (112-117) | de `parcela_nunca_quita` (`K:MassaTensaoPura.lean:160`) por `linarith`; usa os campos β>0, g>0, P>0 | derivado de termo do kernel | **APROVADO** |
| B11 | ★ `o_um_se_fractaliza` (120-126) | série geométrica `Σ (1−w)·wⁿ = 1` para `0<w<1` (`tsum_geometric_of_lt_one`); `tsum` não é o 0 de Lean porque a soma converge, logo não é vácuo | conteúdo é a normalização da distribuição geométrica; «fractaliza» é nome [ONTO], **não dito** | **APROVADO COM REPARO** |
| B12 | `no_zero_absoluto_a_parcela_quitaria` (130-141) | `1 − e^{−q/T} → 1` quando `T → 0⁺`, para `q > 0` arbitrário. **Não menciona `Emprestimo`, β, g nem κ.** | cálculo genérico; «para q > 0» dito, «não é sobre o modelo» **não dito** | **APROVADO COM REPARO** |

### Reparos (B)

- **B5 (muda a leitura).** *Texto sugerido:* «Trivial por definição de `temperatura` (`1/P`) e de `calorDaVolta` (`β·g`): `P·β·g = (β·g)/(1/P)`. O que o kernel dá é `T = κ/2π` (B1). Que `β·g` seja uma energia e `1/P` uma temperatura é a leitura [ONTO] do operador (ħ = k_B = 1); `β·g` é uma taxa de decaimento, e "peso de Boltzmann" é o nome da forma `e^{−E/T}`, não uma derivação.»
- **«Clausius» (B6 e cabeçalho 15, 19-20).** O balanço de Clausius da tela ótica é `boost_defect_with_derived_period` (`K:O16/PeriodHeatCalibration_v3.lean:12`): lá o defeito é `calor_do_segmento − (1/P)·η·área`, isto é, a entropia é `η·área`. Em B, `δS` é **definida** como `δQ/T` (58), o que faz `δQ − T·δS = 0` valer por construção. O cabeçalho (29-31) admite que o objeto da tela ótica é «outro, não ligado»; então «fecha como balanço de Clausius» (19-20, 81) é excesso. *Texto sugerido:* «tem a forma de Clausius por DEFINIÇÃO de `δS` (linha 58); não é o balanço de Clausius da tela ótica.»
- **«Unruh/BW, [KNOWN]» (cabeçalho 29).** `K:BoostHeatConstruction.lean:16` diz «kappa/(2pi) é normalização herdada (sem Unruh/KMS)». A identificação de `1/P` com uma temperatura é nome mais a citação de BW na literatura; nenhum termo do kernel a faz. *Texto sugerido:* «`temperatura := 1/P` é um NOME; a identificação com a temperatura de Unruh/BW é citação [KNOWN], sem termo; o kernel registra `κ/2π` como normalização herdada.»
- **B8.** *Texto sugerido:* «Trivial por definição (`charged := 1 − transmitted`), como o kernel já diz em `ThePsionAndTheViscosity.lean:87-88`. O "balanço" do operador em `MassaTensaoPura.lean:28-29` (sob Clausius o defeito é zero e a parcela o mantém zero) é o defeito da tela ótica, **não** ligado por termo; este teorema é só a contabilidade `w + (1−w) = 1`.»
- **B11.** *Texto sugerido:* «[ONTO] "fractaliza" é o nome. Conteúdo: série geométrica normalizada `Σ (1−w)·wⁿ = 1`. Que a volta `n` carregue `parcela·wⁿ` segue de `o_expoente_decai_por_volta` (`transmitted(nP) − transmitted((n+1)P) = parcela·wⁿ`), não enunciado aqui.» *Opcional:* acrescentar esse lema (não testado).
- **B12 (muda a leitura).** Com o que há no arquivo, `parcelaPorVolta L = 1 − exp(−(calorDaVolta L / temperatura L))` (de `a_parcela_e_um_menos_o_peso` e da def. 58): é a função do teorema em `T = temperatura L`, `q = calorDaVolta L`. Mas «T → 0⁺» com `β, g` fixos é uma **família** de empréstimos com `κ → 0` (`P = 2π/κ → ∞`), fora de qualquer `L`; e o que impede o zero absoluto no modelo é só `period_pos` (campo) e `parcela_nunca_quita`. *Texto sugerido:* «Cálculo sobre a função genérica `T ↦ 1 − e^{−q/T}`; não menciona `Emprestimo`. Aplica-se ao modelo por `q := calorDaVolta L`, `T := temperatura L`, variando `κ` com `β, g` fixos. Que o atrito cause `T > 0` não é termo (cabeçalho 27).»
- **B2.** *Texto sugerido:* «Trivial por construção: `period_pos` é campo de `Emprestimo`.»

### Hipóteses escondidas e homônimos (B)

- **`g > 0` e `κ > 0` são dados livres** do sistema que lê (campos de `Emprestimo`, `K:MassaTensaoPura.lean:132-141`; o kernel diz «dados do sistema que lê», linhas 66-67, e «o contraste g é binder», `K:ThePsionAndTheViscosity.lean:45`). O cabeçalho de B diz que `κ` é «dado do boost» (27) mas não que `g` é livre. Logo `calorDaVolta = βg` depende de um `g` que a teoria não fixa. *Acrescentar ao cabeçalho:* «`g > 0` e `κ > 0` são dados, não derivados.»
- **Não vácuo:** `Emprestimo` é habitado por `emprestimoDerivado` (`K:MassaTensaoPura.lean:215`), que a pedra não cita; vale citar.
- **`transmitted`:** a pedra escreve sempre `ThePsionAndTheViscosity.transmitted` (p.ex. linhas 75, 76, 84, 100, 105, 113, 121), a contínua `e^{−tβg}`. O homônimo é `TGLExt.transmitted θ n = (cos²θ)^n`, do **módulo** `TheDeathOfTheSignal`, mas declarado no namespace `TGLExt` direto (`K:TheDeathOfTheSignal.lean:50,60`; a docstring do kernel o chama «`TheDeathOfTheSignal.transmitted`», o que induz a erro). Como a pedra faz `open TGLExt`, o nome nu `transmitted` ficaria ambíguo se esse módulo estiver no fecho de imports; a qualificação explícita da pedra evita isso. **Correto.** A docstring de B não avisa do homônimo (o kernel avisa em `ThePsionAndTheViscosity.lean:35`).
- **«calor», «entropia»:** `calorDaVolta` (`βg`) × o calor da tela ótica (`boostSegmentHeat`); `entropiaDaVolta` (`δQ/T`) × a entropia de área `η·área` do kernel. O cabeçalho avisa só do balanço.

---

## 3. PEDRA C — `OUmInscritoCandidata.lean`

Toda a pedra é composição ou re-exportação de termos do kernel; o cabeçalho (12) diz «Compõe, por termo, o que o kernel já tem», o que é honesto no topo. Não há hipótese escondida: nenhum teorema tem premissa além das que o enunciado mostra, e o vácuo é um vetor concreto de norma 1 (não vácuo).

| # | teorema (linha) | o que prova de fato | trivial? dito? | veredito |
|---|---|---|---|---|
| C1 | `a_luz_fixa_o_um` (30) | `gamma_vacuum` (`K:F1Fecho394/BosonicFock.lean:39`), para **toda** `u`, não só boosts. «A luz» aqui é o funtor Γ | re-exportação, não dita | **APROVADO** |
| C2 | `o_um_e_o_unico_fixo_da_luz` (33-34) | `gamma_no_fixed` (`K:F1Fecho394/CanonicalGammaNoFixedR4.lean:42`) especializado a `B0`, com `B0_zero`, `B0_add`, `B0_continuous`, `B0_no_eigen` (`K:TheImportedSecondQuantization.lean:118,121,124,133`, todos [PAGO] e no trio). Premissa: `gamma (B0 s) ψ = ψ` para todo `s` (**fixo**); conclusão: `ψ ∈ ℂ∙vacuum` (inclui `ψ = 0`) | a docstring (32) diz «fixo» e «reta do vácuo»: **bem dito**. O cabeçalho e o composto dizem «autovetor» | **APROVADO** (o teorema); **REPARO OBRIGATÓRIO** da frase em 15, 20-21 e 55 |
| C3 | `o_um_inscrito_e_a_exponencial_do_zero` (37) | `exponential_zero` (`K:F1Fecho394/ExponentialTotalityR4.lean:109`) | re-exportação **não dita**; «exp(0) = 1» é analogia com o vetor exponencial do Fock | **APROVADO COM REPARO** |
| C4 | `o_um_nao_e_o_zero` (40-44) | `vacuum ≠ 0` de `‖vacuum‖ = 1`. Homônimo `vacuum_norm` resolvido: a pedra qualifica `F1Rede.BosonicFock.vacuum_norm` (42), não a de `SectorDirectSum` (`K:F1Fecho394/SectorDirectSum.lean:68`, outra assinatura) | trivial, não dito | **APROVADO** |
| C5 | `o_par_consigo` (47-49) | `⟨Ω,Ω⟩ = ‖Ω‖² = 1`; mesmo qualificador correto (48) | trivial, não dito | **APROVADO** |
| C6 | `na_particula_so_o_zero` (52-53) | `B0_no_eigen`, mesma hipótese e mesma conclusão | re-exportação **não dita**; «o único autovetor é o zero» é leitura (por convenção o zero não é autovetor) | **APROVADO COM REPARO** |
| C7 | `a_luz_tem_autovetor_o_um_inscrito` (56-60) | conjunção de C1, C2, C3, C4 | docstring «a luz tem autovetor … e só ela» excede C2 | **APROVADO** (termo); reparo da docstring |

### Respostas à pergunta 4

- **`o_um_e_o_unico_fixo_da_luz` usa `gamma_no_fixed` com `B0_no_eigen` PAGO?** Sim, e os cinco argumentos conferem com as hipóteses de `gamma_no_fixed` (`h0 : u 0 = refl`, `hadd : u (s+t) = (u t).trans (u s)`, `_hcontinuous` — parâmetro não usado na prova —, `hno`).
- **«O único autovetor» está bem dito?** Na docstring do teorema, sim («fixo»). No cabeçalho e no composto, **não**: o termo cobre só autovalor 1 do grupo inteiro. `positive_sector_fixed_zero` (`CanonicalGammaNoFixedR4.lean:31-40`) trabalha com a hipótese de ponto fixo. Autovetores com caráter `c(s) ≠ 1` nos setores de n ≥ 1 não são tratados (em 1 partícula `B0_no_eigen` já cobre toda fase). É plausível fisicamente (soma de geradores absolutamente contínuos) mas **sem termo**; e «o resto é contínuo» não tem enunciado de tipo espectral algum.
  *Texto sugerido (cabeçalho 15 e 20-21, e composto 55):* «O vácuo é o único vetor FIXO (autovalor 1 do grupo `Γ(B0 s)`, a menos de escalar) no Fock; autovalores `e^{iλs}` com `λ ≠ 0` nos setores de n ≥ 1 não são tratados aqui, e "o resto é contínuo" é leitura, sem termo.» E corrigir «espectro pontual da luz é o Um e só ele» para «ponto fixo».
- **Inclui ψ = 0:** a conclusão é «∈ reta do vácuo»; «autovetor» exclui 0 por definição, então a frase correta é «único autovetor fixo a menos de escalar».
- **Lacuna de ligação ao kernel.** O fato análogo já existe no kernel em nível de certificado: `light_modular_fixed_iff_vacuum` (`K:QGReaderUVLock.lean:149`), para o fluxo modular `lightDelta C t` de um `FockCertificate`, com `C.Γ_no_fixed` e `u l = B0(−2πl)` (153). C2 é a versão **sem certificado**, sobre o Fock concreto, de «reta fixa = ℂ·vácuo». A pedra não cita isso e não diz que **Γ(B0 s) é o fluxo modular da cunha** (é o campo `bw_kms` do certificado, `K:TheImportedSecondQuantization.lean:217`, que enuncia a KMS a β = 1 para `Γ (B0 (2π t))`; o campo `Γ_no_fixed` está na linha 197; nenhum dos dois é usado aqui). Também não repete a ressalva do kernel de que `B0` representa o boost da luz só módulo um cobordo [KNOWN — a conferir] (`K:TheImportedSecondQuantization.lean:110-114`). *Acrescentar:* «Γ(B0 s) é o grupo cinemático; que seja o fluxo modular de BW é citação, não termo desta pedra.»
- **«Um inscrito = vácuo» é leitura [ONTO].** Formalmente `vacuum` é o estado de zero partículas (setor 0, `BosonicFock.lean:18`); o teorema não distingue «inscrição do Um absoluto» de «estado sem fótons». A identificação é a cunhagem do operador (cabeçalho 8-10), e a pedra deveria dizê-lo uma vez. O fato em si (o vácuo é invariante; a unicidade para o grupo de boosts decorre da ausência de autovetor em uma partícula) é do tipo [KNOWN] de teoria de campo livre; o ganho da pedra é a formalização sobre o Fock concreto, sem certificado.
- **Reparos de C3 e C6.** C3: `exponential x` é o vetor exponencial não normalizado do Fock, com `⟨exp x, exp y⟩ = Complex.exp ⟨x, y⟩` (`ExponentialVectorsR3.lean`, `exponential_inner`), que dá `‖exp 0‖ = 1`. Texto: «re-exportação de `exponential_zero` (`ExponentialTotalityR4.lean:109`); "exp(0)=1" é a analogia com `exp⟨0,0⟩ = 1` no vetor exponencial.» C6: «re-exportação de `B0_no_eigen`: não há autovetor comum **não nulo** do boost em uma partícula (nem com fase); "o zero, o abstrato inominado" é a leitura [ONTO].»

---

## 4. RESPOSTAS DIRETAS ÀS PERGUNTAS 1-5

1. **Enunciado × docstring; triviais não ditos.** A: A1, A2, A8, A9, A10, A12 (ver tabela). B: B2, B5, B6, B8, B9, B11. C: C1, C3, C6 (re-exportações). Trivialidade **dita** corretamente: A7 («por definicao»), B1, B7, e o cabeçalho de C (12).
2. **Hipótese escondida / homônimos.** A: K ≡ 1 dentro do tipo (H-A1); `β < 1/2` como número fora da pedra (H-A2); ½ escrito em `transicaoLida` (H-A3); homônimos `genK` e «posto». B: `g` e `κ` livres; `Emprestimo` habitado por `emprestimoDerivado`; `transmitted` correto mas sem aviso. C: nenhuma hipótese escondida; `vacuum_norm` qualificado corretamente; falta a ligação a `light_modular_fixed_iff_vacuum` e a ressalva de `B0`.
3. **B: leitura e dimensões.** `calorDaVolta` está marcada [ONTO] (14-15, 54): bem dito. **Não** estão marcados: «Clausius» (δS é definição), «Boltzmann», «Unruh/BW» (o kernel diz «sem Unruh/KMS»), «fecha como Clausius». O limite `no_zero_absoluto_a_parcela_quitaria` é genérico; a docstring diz «para q > 0» mas não que não fala do modelo.
4. **C.** Ver §3.
5. **A.** `crivo_iff_posto`: a restrição `0 ≤ θ < π/2` **está** na docstring. `massa_derivada_eq_projecao_div_K`: θ = π/4 é forçado pelo campo `autoconjugado` (teorema `theta_eq_pi_div_four`, não campo); a pedra admite a mudança de lugar só em `transicaoLida`, não neste teorema. `o_angulo_e_lido_do_absoluto` **não prova nada além de** `rw [peso_da_face_absoluta]` sobre uma definição que escreve `1 / 2`.

---

## 5. O QUE A GERÊNCIA DEVE CORRIGIR ANTES DE OFERECER AO OPERADOR PARA NOMEAR

**Obrigatório (a frase é falsa ou excede o termo):**
1. A12 / A11: retirar «nao e escrito» / «em vez de escrito»; dizer «coincidência de valor, não ponte» (texto em H-A3).
2. C: trocar «único autovetor» / «espectro pontual … só ele; o resto é contínuo» por «único vetor FIXO» (texto em §3).
3. B: «Clausius» → «forma de Clausius por definição de δS»; remover ou marcar «Unruh/BW [KNOWN]» como citação sem termo (texto em §2).
4. A9 e A10: dizer que `K ≡ 1` em `TransicaoParaAMassa` e que A10 repete `K:PonteDaMassa.lean:181` (ou omitir A10).

**Recomendado (marcar trivial/[ONTO] onde falta):**
5. A1, A2, A8; B2, B5, B6, B8, B9, B11, B12; C1, C3, C6 (um trecho curto cada, texto acima).
6. Declarar os homônimos: `genK` e «posto» (A); `g, κ` livres e `boostSegmentHeat`/entropia de área (B); `light_modular_fixed_iff_vacuum` e `bw_kms` (C).
7. Ao oferecer ao operador, dizer em uma frase por pedra o que o negativo/positivo significa: **A** não deriva «acorde, não escala» nem «lido do absoluto»; **B** é identidade por definição com uma leitura [ONTO] (βg = calor), e o que impede o zero absoluto no modelo é o campo `period_pos`; **C** é composição de termos que o kernel já tinha, sobre o Fock cinemático, não sobre o fluxo modular.

---

## 6. LIMITES DESTA REVISÃO

- Não compilei nada (ordem recebida). Os veredictos «APROVADO» dependem do registro `_saida.txt` ao lado de cada pedra; não verifiquei que o sandbox usado coincide byte a byte com o `tgl_kernel` que li (as datas de arquivo são compatíveis: `PonteDaMassa` e `MassaTensaoPura` de 01/11 22:12; saídas de 02/11).
- As sugestões marcadas «opcional (não testado)» são ideias de código que **não** compilei; são da revisão, não da gerência.
- Conferidos na regravação (eram os pendentes do PARCIAL): (a) `exponential` é o vetor exponencial não normalizado (`ExponentialVectorsR3.lean:85`, `exponential_inner`): a palavra «analogia» de C3 está correta; (b) o `gamma` de `BoundedBosonicGammaR2.lean:96` está no namespace `F1Fecho.BoundedGamma`, que a pedra C **não** abre: sem colisão com `F1Rede.BosonicFock.gamma`; (c) o campo é `bw_kms` (`TheImportedSecondQuantization.lean:217`).
- Não verifiquei se o módulo `TheDeathOfTheSignal` está no fecho de imports de B (só importa para dizer se o homônimo `transmitted` seria de fato ambíguo sem a qualificação).
- Nenhuma ação em memória ACOM/Mapa foi feita por mim; o registro das rotas fica com a gerência.
