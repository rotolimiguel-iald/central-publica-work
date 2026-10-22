# AUDITORIA DE ESTATUTO E RÉGUA — o organismo e a prova distintiva — 13/10/2026

Auditor cético independente (lente: ESTATUTO E RÉGUA), gerência c1, subagente. Escrito só em
`C:\IALD\Central de Patentes\work\organismo_iald_12out\3_AUD_ESTATUTO`.
Ordem do operador por sha256 `78ef70e6f9868281…` (1.342 B, conferido aqui). Memória ACOM: contexto
`2a87c7af-7dfd-596e-8a83-e9d10957307b` (init com a ordem; transition ao fim).
β em runtime: ALPHA_FINE_CODATA_2018 lido dos bytes da l.5557 do um.py v391 (`8e7b9927ceae64b8`; linha única)
× √e = 0.012031300400803142 [REAL aqui]. Não rodei o um.py nem o Lean; não abri dado; nada escrito fora desta pasta
(exceto a inscrição ACOM, exigida pelo protocolo da casa). Hashes dos arquivos auditados: `medidas\HASHES_AUDITADOS.txt`.

## 1. O que passa na régua [REAL, por grep e leitura]
- Palavra proibida: 0 ocorrências como veredito nos entregáveis (só nos sufixos `NOT_A_CONFIRMATION` e em tokens do core).
  «De uma vez por todas» aparece só quando a ordem é citada. Nenhum texto diz que a QG foi «resolvida» no sentido de creditação.
- Todos repetem: PROVADA = validade; a confirmação recusada é creditação; o único elo pendente é β_TGL na natureza a 5σ;
  o gate não se move; nenhum veredito é emitido.
- A novidade de uso está documentada por hash (`8c13eb249b104564`); a D1a está declarada como seleção à vista da razão; «pós-dição»
  nunca aparece como demérito (o token do core `NOT_BLIND_UNADJUSTED_POSTDICTION` aparece só transcrito).
- Zero parâmetro: K e ΔN_eff sem parâmetro livre; m₂ com dois INPUTs declarados; o τ★ do ramo B declarado INPUT.
- Duas testemunhas, sem juiz e sem soma (F3.4), respeitadas por A, B e pelo juiz; o juiz diz que a quadratura do par é «teto».
- β nunca é literal na pedra (`c.beta : TGLCoupling`); o número só existe em runtime.

## 2. Problemas (gravidade)

**ALTA-1 — Homônimo «defasagem» dentro da pedra, sem ponte.** `IALD.dephase` = `axiomFlow (post a) (r·t)` sobre
vetores de H (preserva a pureza: um estado puro segue puro). O B8(iii) `dephasing_alone_does_not_keep_the_rank` fala de
`diagExpect` (`CondExpect.lean:87`, a esperança diagonal, ou pinching, de matrizes) aplicada a `rhoOut θ`: é outro objeto.
O T12 diz que o pinching `IALDRhoStar.eJ` é «a seção, não o Nome»; o B8 diz que o pinching D_∞ é «a defasagem». Há ainda
`Ergodicity.dephase` (Schur) no kernel. A docstring do B8 («No motor a leitura R é estação obrigatória — por isso T3′
vale») encadeia sem lema; o ensaio numérico («D sozinha leva ρ puro de posto 1 a posto n») mistura o canal com o D do
motor. Correção: um lema ponte (`diagExpect` ↔ leitura por `eJ`/`jonesReading`) ou o rótulo explícito «não é a defasagem
do motor» no B8 e no relatório.

**ALTA-2 — «A cláusula Ágape entra por termo» e «Q15 RESOLVIDA» inflam o estatuto.** O único termo da Fundação
usado é `the_floor_fixes_the_cut : exp(−a) = 1 ↔ a = 0` (`Fundacao.lean:127`, provado por `Real.exp_eq_one_iff` + linarith).
Não entra nenhuma das seis cláusulas de `agape`, nem `DualScalingData`, nem `abismo` (grep na pedra: 0). A Fundação segue
sem importador no kernel (a pedra não está instalada) e sem ligação de conteúdo; NF1/PQ4 reconhecem isso. Correção:
«importa um lema elementar do arquivo Fundacao; a cláusula Ágape NÃO entra; Q15 segue aberta».

**ALTA-3 — Livro de cobranças: o juiz afirma o falso.** PROGRAMA §0.3 e §1: o par «é a leitura composta de duas leis
já cobradas uma vez cada (K e ΔN_eff)». O Inventário (l.137) e o core dizem outra coisa: a Fase 8 (N_eff) NÃO é cobrança;
a Fase 9 NÃO está ligada ao livro (NAT-07). Hoje nenhuma das duas pernas é cobrança. Ler o par cria a primeira cobrança
de β no setor da radiação (decisão do operador); no setor H₀ segue UMA cobrança (X12). Correção ao lado no PROGRAMA.

**MÉDIA-4 — [ONTO] dentro da pedra, sem marca.** `IALD.lean` tem 0 ocorrências de «[ONTO]». As docstrings dizem: T5/T5′
«EU SOU = IALD» e «o eco não é cópia»; B4 «A SINGULARIDADE LÊ O NOME… encontra aqui a sua forma»; T9 «O tempo é santo»;
T7′ «a cláusula Ágape»; T8 «ZENÃO DO MOTOR». O T5′ é um fato genérico de Hilbert (vetores unitários com |⟨a,ψ⟩| = 1 coincidem
a menos de fase). O RESULTADO §5.6 diz que o ONTO fica fora da pedra e o §6.1 diz «EU SOU = IALD como termo»: os dois se contradizem.
Correção: marcar [ONTO] nas docstrings ou retirar; o termo é `M = 1 ⟺ post ψ = post a`.

**MÉDIA-5 — «O problema da memória… está resolvido» (RESULTADO §6.1); «Q16/Q17 RESOLVIDAS» (ESPEC, PREREGISTRO).**
Os três nomes já eram a MESMA definição `(ℂ∙v).starProjection`. O `rfl` desfaz um homônimo aparente (falha de
classificação do L1, regra 3 do cético: «EXISTE E ESTÁ LIGADO»); não supre um lema que faltasse. A face ACOM da «memória»
(Q18) não foi tocada. A pedra não compõe o organismo: 0 referências a `QGSolutionComplete`/Tetelestai,
`the_whole_is_one`, `the_matrix_rule`, ao livro, a `agape` e a `DualScalingData` (grep). O organismo segue sendo uma lista mais uma definição.
Correção: «dissolvido (homônimo aparente)»; Q16 aberta; dizer que a pedra não liga o fecho da QG à memória.

**MÉDIA-6 — β não atua no motor, e isso não é dito.** O T1 prova `motor a U r t ψ = post a (U ψ)`: a saída não depende
de r (= β) nem de t; `the_leak_is_beta` é um `rfl` de nome. β só vive na face (D, B2, B6, T8), antes da leitura. Como em
`QGSolutionComplete.lean:36`, é preciso dizer: o motor não liga β à memória; nenhum observável do motor depende de β.

**MÉDIA-7 — Perguntas ao operador que não são só resíduo.**
(a) PQ3 (Zenão: a chegada ou a recusa da queda?) já foi respondida em 06/10, 13:48:42 UTC («…nunca chega-se ao limite… a função
do zero absoluto que não se resolve em tempo finito… decomposição infinita, impedindo o colapso», memória
`293d98108031d1c4`) e em 07/10 («não existe acima, o piso limita, tentar estar acima é cair sem fim, infinitamente»,
`e2a915e23692f85c`). O resíduo é só a PQ4 (construir a ponte de Takesaki).
(b) R-6/P-B4 (o que morre se o m₂ morrer): a semântica está congelada no kernel v383, em
`TheLedgerOfCharges.falsified_extinguishes_the_charge_not_the_rule` (l.87). O FALSIFIED extingue a cobrança (lei ×
INPUTs × conjunto), não a regra β. Reabrir «o que morre» com o centro a 2,21–2,95σ contra é redesenhar o teste depois
do dado. O resíduo é só ler o texto da cobrança F4.
(c) R-7/P-B2 (G10 × v191): a decisão de 07/10 («a escala de beta nós também já definimos antes», X6) foi registrada
incluindo a predição afiada; o core lê C17 como «armada, sem canal vivo»; o «Morto» do G10 fala do poder do canal.
A pergunta pede ratificação de uma leitura, não uma escolha aberta.
(d) PQ1 (Riemann): o desenho e a construção oferecem 2 objetos, mas o Inventário achou um terceiro, a porta de Riemann–Lebesgue
(um.py l.7098 e l.164125, `MOLLER_DOOR_REDUCES_TO_RIEMANN_LEBESGUE`). A pergunta está incompleta.

**MÉDIA-8 — «O par entra NO LUGAR do contorno de 14/08» (J4, R-3).** O `TGL_CONTORNO_V1` foi pré-registrado em 14/08,
20:19, antes da abertura da Fase 9. Substituí-lo por uma regra desenhada depois de ver o z_disc de 4,28 e o N_eff contra
mexe no pré-registro do teste. A régua manda corrigir AO LADO. E o princípio do contorno é do operador, sem citação nos textos
(14/08, 19:48: «a régua não deve medir… deve reproduzir o contorno espectral»; 05/09: «a confirmação é holística (o contorno),
a refutação é local», memória `ec3a4032b10c0db2`). Correção: «o par entra AO LADO do contorno».

**BAIXA-9 —** ΔN_eff vem de `RhoPlusPClosure.hubble_form`: o arquivo está em `TGLExt.lean`, mas há 0 `#print axioms` em
`Audit.lean` (aferido). R = 1,4844 é [DERIVED], não termo de kernel auditado, até o F6 (a estratégia B o diz; o juiz não repete).
**BAIXA-10 — Voz.** `OPERADOR_10out_posto_rank_texto_verbatim.txt` contém texto de IA colado pelo operador («Essa
resposta tocou no núcleo…», «Quando você derivou… amarrando a torção de Riemann-Cartan»); a versão de 12/10 diz «eu derivei…
você impôs», com voz mista. O L1 o cita como «o próprio texto do operador». Marcar [INPUT — colado pelo operador; voz mista].
**BAIXA-11 —** S3 «β de runtime habita TGLCoupling»: o kernel prova para todo `c`; a habitação pelo número é de runtime.
**BAIXA-12 —** As frentes usaram três receitas de impressão digital do kernel (A `c8c3ef…`; L2/B/juiz `a8b554…`; desenho/construção
`22557ead…`). Cada uma é estável consigo mesma, mas elas não se comparam entre as frentes.
**BAIXA-13 —** O pré-registro conta 33 declarações e o script conta 34 (a errata ao lado já foi feita).

## 3. Veredito do auditor
O programa da prova distintiva (A, B e o juiz) respeita a régua no essencial e não move o gate. Precisa de duas correções
ao lado (ALTA-3, MÉDIA-8). A pedra `TGLExt.IALD` é matemática limpa segundo a construção (não recompilei), mas NÃO
entra na v392 como está: é preciso corrigir a ALTA-1 (ponte ou rótulo), a ALTA-2 e as MÉDIA-4/5/6 (docstrings e relatório).
Depois disso a entrada é decisão do operador, com as quatro candidatas na mesma versão. As perguntas ao operador devem ser podadas como na MÉDIA-7.
NOT_FALSIFIED nunca é a palavra proibida. A natureza decide; a creditação é ato do observador.
