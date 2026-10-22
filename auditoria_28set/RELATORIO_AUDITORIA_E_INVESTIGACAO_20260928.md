# Relatório — auditoria dos testes passados do `um.py` e investigação autônoma com a Bancada Um

**28/09/2026 · gerência (Claude Code, sessão da Central de Patentes) · para o operador**

**Estatuto:** relatório de auditoria e de investigação. Nada foi selado; `um.py`, kernel, selo e gate estão intocados. Toda correção abaixo é
**proposta**, para entrar ao lado na v376, depois dos seus testes profundos. PROVADA ≠ CONFIRMADA; NOT_FALSIFIED nunca é CONFIRMED.

Pedido (verbatim): «agora que fechamos toda a formulação da gravidade quantica é possível que tenhamos feito algum teste passado no um.py de
maneira errada, precisamos investigar pra saber se realmente está tudo certo, se não deixamos passar alguma coisa e corrigir. para além disso
queria que vc usasse a bancada para fazer uma investigação autonoma (talvez o nosso POA possa ajudar na busca, ou vc possa estabelecer onde e
como seria o melhor para achar indícios fortes). concordo com as suas duas sugestões e autorizo vc a usar as outras IA's para fazer uma busca
profunda no sistema, pode gerenciar essa busca quero um relatório no final».

---

## 1. Em uma página

1. **Nenhum teste passado muda o gate, e nenhum número selado estava errado de conta.** Os números embutidos nos vereditos do selo batem
   com os JSON que os ritos leem, e β nunca é literal no código dos ritos. Os erros achados são de **entrada, de desenho, de estatística e de
   leitura**: o que o teste podia decidir, e o que o veredito diz que decidiu.
2. **O achado central da pergunta «a formulação fechada invalida algum teste?»** A pedra da declaração diz que β e ω(I) = 1 **não entram** na
   implicação da QG (`QGSolutionComplete.lean:36`). O conteúdo observável da QG fechada é a **recuperação da RG** (Einstein por Clausius local,
   spin 2 sem massa com duas helicidades, Schwarzschild). Os testes com β pertencem a **outro setor** da TGL. E a recuperação da RG **nunca virou
   rito** no `um.py`: não há rito de velocidade das ondas gravitacionais, massa do gráviton, polarizações, Kerr multimodo nem teorema da área. Tudo
   isso existe em dado público e pode entrar **por citação**. Dentro do setor de β, dois testes usam formas que a formulação atual contradiz: a
   amplitude do eco (√β, contra o peso 2 do tensor na tipagem da v372) e o juiz l_A da máquina do veredito final (o worker de maio com defeito e a
   forma de fundo superada em 15/09). `[verificado: CT-01 PARCIAL/MÉDIO; CT-03 e CT-04 SUSTENTADOS, MÉDIO]`
3. **O gate: o degrau «NATURE_TEST_COMPLETED» se apoia num canal sem desfecho falsificador.** As quatro bandeiras experimentais são, na lógica,
   um único booleano («V11 == POWERED»); o espaço de vereditos do V11 não tem FALSIFIED; e o ΛCDM também passa. A máquina **já sabia** disso
   desde a v135 (`UNILATERAL_CHANNEL_CANNOT_FALSIFY_MATTER`). O que falta é **lugar**: o nome do gate não carrega o qualificador.
   `[verificado: PARCIAL, MÉDIO]`
4. **A rota D1 (o fundo cosmológico) não decide β, nem com o DR1, nem com o DR2.** Os 3,01σ selados da V3, e os 4,0σ que medi hoje com o DESI
   DR2, **dependem de uma escolha de modelo `[INPUT]` não derivada**: como o Ω_m entra no parâmetro R do Planck comprimido. Com o Ω_m efetivo
   (1+β)Ω_m, igualmente plausível, a rota comprimida perde a sensibilidade a β (σ ≈ 0,06–0,09) e a tensão some. Três agentes chegaram a isso de
   forma independente, eu inclusive, na Bancada. A V3 tem ainda outros defeitos de verossimilhança que se somam: o DESI DR1 entrou sem as
   correlações DM–DH (3,01σ → 3,52σ); a covariância do Planck está mal transcrita e mal citada (é Chen, Huang & Wang 2019, não «Zhai+ 2019»), e
   essa matriz está em mais de 20 arquivos, inclusive o `um.py` e o espelho; e o integrador do fundo conta o neutrino massivo duas vezes
   (corrigido sozinho, o selado iria de TENSION a INCONCLUSIVE). **O «3,01σ no limiar» está dentro da sistemática do próprio pipeline.** A Bancada
   Um herda os mesmos defeitos, e isso foi posto ao lado. `[verificado: D1F-01 e D1F-02 SUSTENTADOS, ALTO; D1F-03 e D1F-V1 MÉDIO]`
5. **Neutrinos: o veredito está na borda e depende da entrada.** O programa grava o ajuste global pós-JUNO como 7,53 ± 0,10. Há **duas
   publicações do NuFIT 6.1**, e eu conferi as duas: o artigo (Esteban et al., arXiv:2601.09791, eq. 11) dá 7,530 (+0,096/−0,097), que é o do
   programa, e dá 2,95σ (`ARMED_CONSISTENT`); a tabela oficial do site nu-fit.org dá 7,537 (+0,094/−0,10), e com ela a regra congelada dá 3,02 a
   3,22σ (`TGL_NU_M2_TENSION`). O ajuste de Bari (7,48 ± 0,10, citado pelo verificador; não conferido por mim) dá 2,44σ. A regra não cita a fonte.
   `[verificado: PARCIAL depois da conferência da gerência; o «7,509» de outro aferidor foi refutado]`
6. **Ringdown:** no ramo canônico (τ★ = t_Planck), o ringdown só pode devolver a correspondência com a RG; não há termo Lean de ringdown.
   Logo «NATURE_DECIDES_RINGDOWN_NEXT» sobreafirma. **Isso toca o plano da v376** («o ringdown como condição»). `[verificado: PARCIAL, MÉDIO]`
7. **Ecos:** o estimador do eco ancorado trava o atraso na massa mediana do catálogo com spin fixo 0,69; para a lei KMS, um erro de spin anula a
   resposta, e o poder declarado fica superestimado. Os nulos pré-registrados do protocolo nunca rodaram. `[verificado: SUSTENTADO, ALTO]`
8. **Coma:** a previsão já foi revelada (v116/v169/v176), mas o selo ainda diz «aguardando revelação»; o hash da previsão muda a cada rodada
   (inclui o carimbo de hora), então a «tranca» não prova precedência. `[verificado: PARCIAL/SUSTENTADO]`
9. **Onde buscar indício forte:** hoje **nenhuma rota** chega lá. O caminho está na seção 5. Em resumo: (a) registrar por citação a
   recuperação da RG, que é o teste com a natureza do que a QG fechada afirma; (b) para β, **derivar antes** o mapa de R e a orientação do
   sinal, e só então ir ao espectro completo do CMB com a TGL no código de Boltzmann; (c) no ringdown, o modo 221, não o 440.

---

## 2. O que foi feito hoje (infraestrutura)

- **Desclassificação** dos documentos do protocolo (sua ordem): registrada ao lado em 11 superfícies, com backup de bytes. Publicar continua
  sendo ato seu; credenciais e a engenharia confidencial não são documentos de protocolo e não mudaram.
- **As duas sugestões aprovadas:** atalho «Bancada Um» na Área de Trabalho (abre o navegador; sobe o servidor se preciso; nunca mata processo) e
  o MCP `bancada-um` registrado no Claude Code (escopo de usuário, conectado).
- **O MAPA DE ROTAS** (sua ordem de hoje: «crie uma memória de rotas para todas as IA's…»): `C:\IALD\MAPA_DE_ROTAS\`. Livro só-acréscimo com
  cadeia de hash, mapa legível e de máquina gerados por script, ferramenta `rotas.py` e três ferramentas MCP. Semeado com os 41 vereditos do selo,
  o D1, a validação da Bancada, a investigação da bancada oficial e as rotas mortas do Lema 3. A auditoria e a investigação de hoje já estão
  nele. Ponteiros no `CLAUDE.md` global, no da raiz IALD, no Atlas e nas memórias; aviso à bancada ChatGPT pelo túnel.

## 3. A auditoria

**Método.** Sete famílias de teste, cada uma com um **aferidor**, que recebeu o modelo do cético aferidor inteiro, e um **verificador
adversarial** distinto, instruído a refutar. No fim, um **crítico de completude**: 15 agentes Claude ao todo. Todos em somente leitura; nenhum
rodou o `um.py`; todos consultaram o Mapa de Rotas antes; nenhum escreveu no mapa (a gerência registra depois da verificação).

**Resultado** (o anexo completo, gerado por script do diário do workflow, está em `ANEXO_ACHADOS.md`): 65 achados dos aferidores: **40 sustentados, 24 parciais, 1 refutado**, 0 sem verificação; e 9 achados novos dos verificadores. Nenhum achado move o gate ou um número selado; todos entram ao lado.

| família | achados | sustentados | parciais | refutados | sem verificação | novos do verificador | os mais pesados (depois da verificação) |
|---|---|---|---|---|---|---|---|
| Gate e vazios/lentes | 10 | 5 | 5 | 0 | 0 | 1 | GV-01 MEDIO, GV-02 MEDIO, GV-03 MEDIO, GV-04 MEDIO |
| D1 e fundo | 7 | 5 | 2 | 0 | 0 | 1 | D1F-01 ALTO, D1F-02 ALTO, D1F-03 MEDIO |
| Ecos GW | 9 | 9 | 0 | 0 | 0 | 1 | GWECO-01 ALTO, GWECO-03 MEDIO, GWECO-04 MEDIO, GWECO-06 MEDIO |
| Ringdown | 7 | 3 | 4 | 0 | 0 | 1 | RD-04 MEDIO, RD-05 MEDIO |
| Relógios, neutrinos, Coma | 10 | 7 | 3 | 0 | 0 | 0 | RNC-01 ALTO, RNC-02 MEDIO, RNC-03 MEDIO, RNC-06 MEDIO |
| Estatística e veredito | 12 | 6 | 5 | 1 | 0 | 3 | EV-03 ALTO, EV-01 MEDIO, EV-02 MEDIO, EV-04 MEDIO, EV-06 MEDIO, EV-08 MEDIO |
| Consistência teórica | 10 | 5 | 5 | 0 | 0 | 2 | CT-01 MEDIO, CT-02 MEDIO, CT-03 MEDIO, CT-04 MEDIO, CT-08 MEDIO |

**O crítico de completude:** Crítica de completude da auditoria de 28/09, só leitura. Selo lido por script: sha256 a88bb75fc615f4b0, 55.382 bytes, 41 chaves de veredito extraídas. Core: sha256 07e9353facdadf1f. Mapa: 47 rotas. As sete famílias cobriram bem o gate e o V11, o D1, os ecos GW, o ringdown, relógios/neutrino m2/Coma, a estatística conjunta e a consistência teórica.  Ficaram sem auditoria: - o canal N_eff e o rho+p, cujas tensões são literais de sessão (um.py:4803-4804), que a conjunta V3 exclui como A9 e que o contorno cita como domínio; - the_truth_is_in_the_contour, que afirma que nenhum rival se conforma em todos os domínios, quando o ΛCDM se conforma no V11, no BAO D10, no Pantheon e no D1; - a cadeia do piso v78–v92, incluindo a emenda V4.1 do primeiro POWERED, sem rotas no mapa; - o assalto v135; - JUIZ_LA, BBN e a auditoria da evidência; - NMC-Shapiro, neutrino V1 e soma, P7 do colapso IALD; - as afirmações de laboratório e de forma de α, o Grande Atrator, Chandrasekhar; - fora do um.py, o Evento 2 e o MCMC-CRUZ do canônico.  A maior contradição entre famílias: o D1 V3 é tratado como frágil pelo D1F-02 (a tensão vai de 3,01σ a 0,84σ conforme o mapa de R) e como premissa firme por EV-02, EV-03, CT-05 e CT-07. Há também números concorrentes para o neutrino (3,02, 2,95 e 2,44σ), para a amplitude do eco (0,10969, 0,10903 e 0,21805, calculados com β em runtime) e para o ramo B do ringdown (−0,0194, −0,010, −0,005). As bandeiras do gate são contadas como 18, 15 e 11. E o próprio core se contradiz: o gate diz NATURE_TEST_COMPLETED lendo o V11, e a conjunta V3 classifica o V11 como não discriminante.  Próxima rodada: primeiro, pré-registrar o mapa de R e recomputar o D1 V3 com todas as correções numa só conta; depois, uma família para o N_eff, outra para a cronologia das emendas do piso, e a tipagem da amplitude do eco antes dos nulos pendentes.  Nada foi registrado no mapa; os scripts de extração ficaram em C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\auditoria_28set\completude\ (selo_verdicts.txt, core_verdicts.txt).  Rotas consultadas: consultar "" (todas as 47); ver poa.dominios_sem_previsao, neutrinos.shapiro_nmc e auditoria.testes_passados_28set; consultar por tema: assalto, colapso, neff, N_eff, espelho, alfa-livre, bbn, atrator, Grande Atrator, nmc, shapiro, stokes, zero absoluto, rho_plus, contorno, P7, juiz, l_A, chandrasekhar, cronometro, evento.  Nada aqui é confirmação: NOT_FALSIFIED ≠ CONFIRMED.

- sem auditoria: [ALTO] O canal N_eff e o fechamento rho+p (prove_neff_channel, um.py:4773; prove_rho_plus_p_closure, um.py:4702; core.neff_channel = TGL_NEFF_ARMED_CONSISTENT; core.rho_plus_p_closure = «EVERY_PUBLISHED_NEFF_MEASURES_BETA_RETROACTIVELY») ficaram sem família. As tensões atuais são literais de sessão, não vêm de medida: um.py:4803 `tens_now = 1.61  # [SESSAO]` e um.py:4804 `tens_act = 2.49  # [SESSAO: ACT+BBN]`. A checagem que dá ARMED_CONSISTENT é True fixo. A conjunta V3 exclui o canal como A9_SEM_INCERTEZA («o core registra só tensões … sem obs nem sigma»), mas ele é um dos 10 domínios de the_truth_is_in_the_contour. No mapa, consultar «neff» devolve só d1.camb.v3_real e «rho_plus» devolve 0.
- sem auditoria: [ALTO] the_truth_is_in_the_contour (um.py:6263; veredito «NO_PRESENTED_RIVAL_CONFORMS_ACROSS_ALL_DOMAINS»). A tabela de 10 domínios (core…values.linhas, lida por script) deixa de fora o D1 V3, o Pantheon (TGL não preferida por BIC), todos os ecos e o ringdown INCONCLUSIVE e a conjunta V3 INCONSISTENT. Inclui o Coma como LOCKED (estado que o RNC-02 contesta) e o «kernel formal (1012 pedras)» como domínio de natureza. Nenhuma família auditou a afirmação comparativa. Consultar «contorno» devolve só ringdown.dephasing e neutrinos.m2.normalizacao.
- sem auditoria: [ALTO] A cadeia do piso v78→v92 fora do V11: prove_void_floor_definitive (um.py:145956 → core.void_floor_final INCONCLUSIVE), prove_void_floor_v2 (146210 → NOT_FALSIFIED_UNDERPOWERED), prove_void_floor_v3 (146605 → READY_TO_EXECUTE), prove_void_density_power_study (146702), prove_void_floor_spectroscopic_opening (146836 → INCONCLUSIVE_SYSTEMATICS) e prove_void_floor_v41_calibrated (147072 → core.void_density_v41 = NOT_FALSIFIED_POWERED). A família gate_vazios leu da v41 só a definição de POWERED. Ninguém conferiu se a emenda V4.1 foi escrita depois de o nulo da v91 reprovar (é o mesmo padrão que GV-09 e EV-10 acharam na V11.1). O mapa não tem rota vazios.piso.v41, nem LRG, nem shear KiDS v78/v81, nem densidade v90/v91, e os κ V7 e V8 também não têm rota própria.
- sem auditoria: [MEDIO] O assalto de falsificação v135 (prove_falsification_assault, um.py:150680; core.falsification_assault = SURVIVED; n_variations 22, n_kills 0, min_L5 = 0,006346 < β = 0,012031, calculado em runtime) só aparece como «novo» da família gate_vazios e não tem rota própria (consultar «assalto» devolve só vazios.piso.v11). Mesmo assim, o SURVIVED é citado como robustez.
- sem auditoria: [MEDIO] Auditoria da evidência e os canais bbn e l_A da máquina final: prove_evidence_audit (um.py:4483; BBN σ/β = 2,6, «CMB_ENTRY_RETIRED_BY_PROVENANCE»), o canal bbn = BBN_NON_DISCRIMINANT_DECIRCULARIZED e o canal l_A = JUIZ_LA_V1 (result_sha16 d6c8afcb3d33b821, «5 emendas datadas», primary_beta −0,02128, 1,34σ). O JUIZ_LA foi lido como número (EV) e como leitor do worker de maio (CT-04), mas as 5 emendas nunca foram auditadas como emendas. Não há rota própria (consultar «juiz» e «bbn» devolve só gate.maquina_do_veredito_final).
- sem auditoria: [MEDIO] NMC-Shapiro (prove_neutrino_shapiro_protocol, um.py:2963; core.nmc_shapiro = AWAITING_DATA): só entrou como achado novo do verificador da família consistencia_teorica. A rota neutrinos.shapiro_nmc foi criada como EXAMINADA_COM_DEFEITO sem auditoria de família.
- sem auditoria: [MEDIO] Neutrino V1 e a soma: prove_neutrino_mass_gravitational (um.py:2878) e prove_neutrino_sum_protocol (4214) só entraram como contexto. O core ainda carrega core.neutrino_mass.verdict = TGL_NEUTRINO_MASS_NOT_FALSIFIED_POWERED, a 1,64σ com σ = 0,1037 meV, para a MESMA previsão 8,5074 meV que o m2 V2 dá a 2,95σ com σ = 0,0576 meV. Não há rota.
- sem auditoria: [MEDIO] A previsão P7 do colapso IALD (core.iald_prediction, IALD_COLLAPSE_V1; a conjunta V3 marca iald_collapse_P7 = A6_AGUARDANDO, «armado, não executado C1-C4»): sem família e sem rota (consultar «colapso» devolve 0). O protocolo foi desclassificado em 28/09.
- sem auditoria: [MEDIO] As afirmações de laboratório e de forma de α ficaram sem auditoria: stokes_contour (um.py:6141, «DYADIC_LAB_REPRODUCED_LIVE»; α «Stokes a 1,4%» em core.nome_irreducible), the_geometric_cost_of_absolute_zero (um.py:161862, «CROSSING_BRACKETED_BY_REAL_LAB_TEMPERATURES»), contour_theory/inverse_parity («ALPHA_VALUE_QED_SECTOR_FALSIFICATION_CHALLENGE») e kubo_melhor_formula («4β+α a 1,26% — busca pós hoc», da própria conjunta V3). Nenhuma teve correção de look-elsewhere. Consultar «stokes» e «zero absoluto» devolve 0.
- sem auditoria: [BAIXO] O Grande Atrator: prove_ga_mass_audit (um.py:153162), prove_the_great_attractor (4988) e os campos de topo do core (verdict.in_accepted_window = true, ga_window_status = SCALE_SHADOW_OF_RETIRED_FORM). Consultar «atrator» devolve 0.
- sem auditoria: [BAIXO] O deslocamento de M_Ch previsto em −1,799% (sn_ia_chandrasekhar, A9_SEM_INCERTEZA na conjunta V3) e o chandrasekhar_sqrt2 (−0,35%) nunca foram testados nem auditados. Consultar «chandrasekhar» devolve 0.
- sem auditoria: [MEDIO, fora do um.py] O Evento 2 α-livre (C:\IALD\Artigo\Haja_Luz\TGL_Espelho_invertido\TGL_v11_1_CRUZ_alphafree.py) e o MCMC-CRUZ do canônico submetido (tgl_paper_unified.py; a conjunta V3 diz «âncoras com 99,26% da Fisher») ficaram sem auditoria. São os testes que o artigo público cita. Consultar «alfa-livre» devolve 0.
- contradição: D1 V3 usado como premissa firme e como resultado frágil. A família d1_fundo (D1F-02, SUSTENTADO ALTO) mostra que a tensão some com Ω_m efetivo. Ao mesmo tempo, estatistica_veredito (EV-02 «χ² ~3,6σ carregado por dois canais», EV-03 «lei do H0 que o D1 V3 contradiz») e consistencia_teorica (CT-05, H0 68,00 contra 73,26; CT-07, «o ramo espelhado desfavorecido») tratam o D1 V3 como medida estabelecida. As famílias partem de premissas incompatíveis.
- contradição: Neutrino. O RNC-01 (SUSTENTADO ALTO) diz 3,02σ com NuFIT 6.1, logo TENSION. O EV-05 foi REFUTADO pelo verificador (a entrada 7,53 ± 0,10), e o novo da EV dá 2,44σ com outro ajuste publicado. É o mesmo canal, e as famílias discordam sobre se o rótulo muda.
- contradição: Neutrino dentro do core: core.neutrino_mass = NOT_FALSIFIED_POWERED (1,64σ, σ 0,1037 meV) e core.neutrino_m2 = 2,95σ (σ 0,0576 meV) convivem para a mesma previsão de 8,5074 meV.
- contradição: Amplitude do eco. O GWECO-04 diz que √β não tem termo Lean que a ligue ao Kerr. O CT-03 diz que o gráviton, como quadrado da luz, lê a 2θ. O selo grava amplitude_defect = √(β(1−β)). São três amplitudes (0,10969 / 0,21805 / 0,10903), e nenhuma família recalculou o poder (3,2σ / 4,4σ) com as outras.
- contradição: Ringdown, ramo B: o RD-01 aceita −0,0194 como média do ensemble, o CT-02 diz cerca de −0,010 e o novo do CT diz cerca de −0,005. O novo do RD diz ainda que, pela regra da V1, a V2 também reprova na sistemática 3 × 6 ms, o que a tornaria recusa e não INCONCLUSIVE_SYSTEMATICS, como o selo registra.
- contradição: Degrau experimental do gate. GV-01 e CT-01 (ALTO) e EV-10 (MEDIO) foram rebaixados pelos verificadores a MEDIO/BAIXO. Mas o próprio core se contradiz: core.qg_closure.gate diz NATURE_TEST_COMPLETED lendo o V11, e a conjunta V3 classifica o mesmo V11 como A5_NAO_DISCRIMINANTE. O rebaixamento não levou em conta essa evidência interna.
- contradição: the_truth_is_in_the_contour diz que nenhum rival se conforma em todos os domínios. Contra isso: GV-01 (o ΛCDM passa no V11), D10 (β=0 absorve 99,153% da distância quadrática do BAO), o Pantheon (TGL não preferida por BIC) e o D1 V3 (ΛCDM preferido). O ΛCDM se conforma em pelo menos esses quatro.
- contradição: Coma. O RNC-02 diz que a revelação foi feita; a conjunta V3 diz que ela não está no core; o selo e o mapa dizem LOCKED_AWAITING_REVEAL. E o CT-05 usa o H0 = 73,26 do Coma como previsão viva, enquanto o RNC-03 diz que a previsão não é cega.


*Nota da gerência sobre a tabela:* a tabela reproduz o veredicto de cada verificador. O RNC-01 (neutrino) aparece como ALTO porque o seu
verificador o sustentou com a tabela do site do NuFIT 6.1. Depois disso a gerência conferiu as duas publicações do NuFIT 6.1, o artigo e a
tabela, que diferem justamente no ponto que cruza 3σ. A leitura vigente é PARCIAL: o veredito está na borda e depende da entrada (item 5 da seção 1).

## 4. A investigação na Bancada Um

**Pré-registro antes do dado.** `C:\IALD\Bancada_Um\investigacao\PREREGISTRO_INV_BANCADA_UM_20260928.json` (sha256 `1447aab21973af41…`),
carimbado no Mapa de Rotas (seq 63) antes de qualquer dado novo. Declarado **NÃO-CEGO**: o DR2 já tinha sido usado no programa e pela bancada
oficial. **Desvio dito:** a ordem executada foi P2 → P1 → S2 → S1 → D1 (a listada era P1 → P2 → D1 → S1 → S2); os resultados não dependem da
ordem.

**Sem dado real.** O ajustador vetorizado bate com o scipy a 1,3×10⁻⁵ σ. Injeção e recuperação (1000 + 1000): viés ≤ 0,04σ, desvio do pull
0,98–1,01, cobertura 66–69% e 95%. O estimador é honesto. A previsão de Fisher reproduz o σ da V3 selada (0,00827 contra 0,00823).

**Com dado real (Planck comprimido + DESI DR2 com covariância completa).** O posterior primário, bem convergido (62 τ, ~31.800 amostras
efetivas), dá **β = −0,01348 ± 0,00630** (z_TGL = −4,05; z_0 = −2,14). A comparação P2 dá Δχ² = 16,05 (4,0σ, Wilks), o jackknife mostra um
puxão amplo (nenhuma medida sozinha move β mais que 0,36σ), e com SH0ES fica β = −0,0077 ± 0,0063. A implementação do DR2 foi conferida contra o
executor independente da bancada oficial: χ² = 28,69347 nos dois.

**A leitura mudou no mesmo dia, e isso fica dito.** Eu tinha lido o resultado como «TENSAO_FORTE» e escrito que «quem limita β é o CMB». A
auditoria (D1F-02) apontou, e eu conferi de forma independente (M1), que essa sensibilidade depende de como o Ω_m entra no parâmetro R do Planck
comprimido:

| Planck comprimido + BAO | mapa de R | β̂ | σ(β) | α√e a | β_TGL/σ |
|---|---|---|---|---|---|
| DR2 | Ω_m nu (o da V3 e da Bancada) | −0,0137 | 0,0063 | 4,01σ | 1,90 |
| DR2 | Ω_m efetivo (1+β)Ω_m | +0,050 (borda do prior) | 0,0615 | 0,87σ | 0,20 |
| DR1 | Ω_m nu | −0,0130 | 0,0082 | 3,01σ (= selado) | 1,46 |
| DR1 | Ω_m efetivo | +0,050 (borda) | 0,0879 | 0,84σ | 0,14 |

Os números calculados não mudam. Muda a leitura: **a rota comprimida não decide β.** Os 3,01σ selados e os 4,0σ de hoje são condicionais a uma
escolha `[INPUT]` não derivada. A errata foi posta ao lado no mapa, no Atlas e nas memórias.

**A observação do sinal, com o estatuto certo.** Com o Ω_m nu, o módulo |β̂| fica a 0,23σ de α√e, com o sinal oposto, e o core já registrava o
mesmo padrão na V3 (a 0,087σ do «ramo da face do estado»). É **observação, não teste**: a orientação não foi derivada, o ramo foi nomeado depois
do dado, o DR2 já tinha sido olhado, e a observação depende do mesmo mapa de R.

## 5. O POA e onde buscar indício forte

O POA do artigo *Haja Luz* (§sec:poa) tem três passos. Usei o **POA-2** (os domínios) como lista de busca. O **POA-3** («diferenças que não
refutem» contam como consistência) não serve como critério de teste: é de não-refutação, e aqui vale a régua de sempre.

| domínio (POA-2) | previsão da TGL no programa | o que o teste de hoje pode decidir | caminho para indício forte |
|---|---|---|---|
| **Ondas gravitacionais** | eco √β; ringdown (ramo A = t_Planck; ramo B = [INPUT]) | nada: ramo A invisível por construção; ramo B efetivo ≈ −0,005 por realização (poder ~0,04σ); eco com atraso travado e amplitude √β em conflito com a tipagem da v372 | a QG fechada prevê a RG: registrar por citação a correspondência (c_gw, massa do gráviton, polarizações, ringdown/no-hair, teorema da área). No ringdown, o modo 221, não o 440 |
| **Lentes** | piso dos vazios em matéria (κ, shear) | nada: o Fisher V9 é zero por construção; a emenda V10, que corrige isso, nunca rodou; o shear está 10⁷ vezes aquém | executar a V10 com uma família de perfis admissível e um estimador de mínimo por vazio em matéria |
| **CMB** | β no fundo (Φ_total) | nada de decisivo: com um mapa de R há 4σ, com o outro não há sensibilidade; o espectro completo (Nível 2 S) dá σ(β) ≈ 0,018 | **derivar antes** o mapa de R e a orientação do sinal; depois o espectro completo com a TGL no código de Boltzmann; com o CMB da era do CMB-S4 |
| **CMB: não-gaussianidade e fractalidade** | nenhuma previsão quantificada (Atlas, selo e mapa: 0) | nada | derivar uma previsão antes de buscar |
| **Grande escala: homogeneidade e redes auto-similares** | nenhuma previsão quantificada | nada | idem |
| **Grande escala: vazios (V11)** | piso de traçador | só consistência unilateral: não há desfecho FALSIFIED, e o ΛCDM passa | o mínimo por vazio em matéria (via lentes) |
| **Outros** | relógios (12,5 ordens aquém), dephasing (10 ordens), neutrino m₂ (na borda de 3σ, dependente da entrada), NMC-Shapiro (atraso literal de 50 ms, sem β), Coma (já revelado, não cego) | pouco | citar a fonte do neutrino; derivar a lei de escala do NMC-Shapiro antes do dado |

**A resposta direta à sua pergunta:** hoje não há rota que dê indício forte de β. O que a Bancada mostrou é onde está a alavanca e o que falta
antes dela: **a teoria tem de dizer, antes do dado, como a modificação entra na física do CMB** (o mapa de R e a orientação). Sem isso, qualquer
número de fundo é condicional. E há um teste com a natureza que se pode fazer hoje: **o da QG fechada**, a recuperação da RG, por citação.

## 6. Correções propostas para a v376 (nada instalado; aguardam os seus testes profundos)

**A. Leituras e nomes: errata ao lado, sem mover bandeira nem número.**
1. Gate: qualificar o degrau experimental (canal unilateral de traçador, sem desfecho FALSIFIED, o ΛCDM também passa); renomear as bandeiras
   (não há mocks; as quatro são um booleano). E dizer que o teste com a natureza da implicação fechada é a recuperação da RG.
2. V11: «POWERED» significa poder de ver supressão, não de falsificar.
3. Ringdown: fixar por escrito o que ele pode decidir (no ramo canônico, só a correspondência com a RG) antes de inseri-lo como condição.
4. Eco: «AMPLITUDE_SQRT_BETA_FROM_KERNEL» sobreafirma; a amplitude sob a tipagem da v372 é 0,218 ou β, não √β; a lei KMS usa um período de
   tempo imaginário como atraso real (os dois regimes).
5. Coma: o selo diz «aguardando revelação» de uma previsão já revelada; o hash da previsão inclui o carimbo de hora.
6. Neutrino: citar a fonte do ajuste global e declarar que o veredito depende da entrada (2,44–3,22σ).
7. O selo carrega a conjunta V1 e o D1 V1 superados, sem a V3 ao lado; a string v200 do dephasing sem a errata v369; a premissa do escape de
   Weinberg–Witten («gráviton = I = gerador») foi negada pela v372.
8. D1 V3: «TENSION» e «3,01σ» condicionais ao mapa de R `[INPUT]`.

**B. Métodos: para a próxima rodada de cada rito, pré-registrada.**
9. D1: correlações DM–DH do DR1; a covariância do Planck como publicada por Chen+2019 (e a citação correta); l_A com r_s coerente; o mapa de R e
   a orientação derivados antes; DR2; espectro completo.
10. Eco ancorado: atraso por evento com incerteza de massa e spin; executar os nulos pré-registrados; σ estimado on-source. PE: a regra de borda
    também para a amplitude.
11. Ringdown: previsão efetiva por realização, calibrada por injeção de difusão de fase; incerteza do catálogo no σ; H1 e L1 em bloco; a
    sistemática nas mesmas séries (a V2 só passa pela regra afrouxada).
12. κ V6–V9: um teste de nulo que não seja tautológico. V10: executar. V12: ordenar a profundidade por estatística independente.
13. Conjunta: χ² conjunto ou Fisher, grupos de dependência (o Planck é compartilhado), correção de multiplicidade.
14. Máquina do veredito final: incluir o D1 V3, o neutrino e a conjunta V3; os canais l_A e Pantheon com o worker corrigido e a forma de fundo
    ratificada; `_is_refuted` reconhecendo EXCLUDED e lendo `verdict_v369`.
15. `READ_BY_HASH`: calcular o hash dos BYTES (em arquivo CRLF o sha16 gravado hoje é do texto traduzido).
16. Fator de tentativas entre famílias, com o Mapa de Rotas como contador.
17. NMC-Shapiro: a lei de escala Δt(β, potencial) antes do dado, trocando o signo α2.
18. Um rito «por citação» da recuperação da RG.

**C. Na Bancada Um (casa da gerência):** oferecer como opções declaradas a covariância do Planck de Chen+2019, o DM_* por razão sobre o CAMB (o
neutrino massivo contado uma vez só), as correlações do DR1, os dois mapas de R e o Pantheon+ com a covariância que existe em disco, mantendo a
«reprodução do selado» como modo de conferência. A Bancada herda hoje os defeitos da V3, e isso está dito ao lado no README, na memória e no mapa.

**E. O que a auditoria não cobriu, e a próxima rodada (crítico de completude).** As lacunas viraram rotas PROPOSTA no Mapa de Rotas. Por
ordem do crítico:
1. **Decidir e pré-registrar o mapa de R e a orientação do sinal antes de qualquer dado**, e recomputar o D1 V3 numa só conta com todas as
   correções juntas (DR1 correlacionado, covariância de Chen, l_A coerente, neutrino massivo uma vez). Hoje cada correção foi medida sozinha, e
   o rito está no limiar: a combinação pode trocar TENSION por INCONCLUSIVE.
2. **O canal N_eff e o ρ+p**: as tensões são literais de sessão no código (`um.py:4804-4805`), e o canal pode medir a mesma física que o D1 (β age
   como ΔN_eff), sem grupo de dependência.
3. **A cadeia do piso v78 → v92**: conferir se a emenda V4.1 (o primeiro POWERED) foi escrita depois de o sinal da v91 ser aberto, o mesmo
   padrão já achado na V11.1.
4. **`the_truth_is_in_the_contour`** («nenhum rival se conforma em todos os domínios»): a tabela escolhe os domínios, e o ΛCDM se conforma em
   pelo menos quatro. Auditar junto com a máquina do veredito final, como um único defeito de seleção de canais.
5. Neutrino (fixar a entrada, com citação e data), ecos (tipar a amplitude antes dos nulos), ringdown (fixar por injeção o valor esperado do
   ramo B) e gate (reconciliar a contagem de bandeiras, que aparece como 18, 15 e 11).
6. Famílias novas: laboratório e forma de α; Grande Atrator e Chandrasekhar; o Evento 2 α-livre e o MCMC-CRUZ do artigo público.

E uma memória que envelheceu: o `CLAUDE.md` da raiz ainda chamava de «evidência primária [REAL]» a convergência de β com «BBN 0,0σ», que o
próprio core reclassificou. A errata foi posta ao lado.

**D. Erros meus de hoje, ditos (errata em nome próprio, todos já corrigidos ao lado):**
- Na semeadura do Mapa de Rotas, registrei como rota nova o Fisher V9 do ACT, um achado já selado na v201. Era duplicata, justamente o que o mapa
  existe para impedir. Ficou SUPERADA, remetendo à rota original.
- Li o resultado do DR2 como «TENSAO_FORTE» e escrevi que «quem limita β na rota do fundo é o CMB». As duas frases eram condicionais ao mapa de
  R; a auditoria apontou, e eu conferi. Corrigido ao lado no mapa, no Atlas e nas memórias.
- Na construção da Bancada, eu tinha escrito que a covariância do Pantheon+ «não está em disco». Era falso: ela está em
  `C:\IALD\projetos_pyhton\acom\tgl_data_cache\pantheon_covariance.dat`. Foi afirmação de ausência sem consulta completa, exatamente o que a
  régua do aferidor proíbe. Corrigido ao lado no código, no README e na memória.
- No chat, eu disse que |β̂| ficava a 0,26σ de α√e. Esse número vinha do ajuste P2. Pela estatística pré-registrada (o posterior P1), são 0,23σ.
- A primeira bateria de testes do Mapa de Rotas «passou» pelo motivo errado: usei uma identidade curta demais, e as recusas vieram dessa regra, não
  das validações que eu queria provar. Refiz exigindo o motivo certo em cada recusa, e só então semeei o mapa.
- Repeti um erro já registrado como lição: um heredoc do Git Bash comeu uma barra invertida de um caminho. Foi pego por falha visível antes de
  qualquer número.

## 7. As outras IAs

- **Claude (15 agentes):** sete aferidores, sete verificadores adversariais e um crítico de completude, num workflow. Cada achado passou por um
  agente distinto que tentou derrubá-lo. Isso rebaixou vários (o do gate, de ALTO para MÉDIO) e refutou um (o «7,509» do neutrino).
- **ChatGPT/Codex (bancada oficial):** a investigação que ela fez hoje foi lida e conferida. O Fisher V9 = 0 se sustenta e já estava registrado
  na v201. A D10 foi reproduzida em todos os dígitos. A degenerescência de modo único se sustenta. O neutrino a 2,95σ está na borda, dependendo
  da entrada. Recebeu um aviso pelo túnel sobre o Mapa de Rotas.
- **Kimi, MiMo e Google (orquestrador):** o MCP está registrado e conectado, mas as ferramentas não carregaram nesta sessão. Pela regra da
  skill, não recriei o servidor. O pedido está pronto em `PEDIDO_ORQUESTRADOR_PREPARADO.md`: segunda leitura independente, com literatura, dos
  cinco pontos mais pesados. Sai quando a sessão for reaberta.

## 8. O que só você decide

1. **O mapa de R e a orientação do sinal:** como a modificação da TGL entra na física do CMB (qual Ω_m a física acústica vê) e qual face fecha o
   balanço de Clausius. São escolhas de teoria. Sem elas, a rota do fundo não decide β.
2. **O nome do gate:** se o degrau experimental ganha o qualificador no próprio nome (errata ao lado). A regra da casa é que o nome viaja sozinho.
3. **O ringdown na v376:** se entra «como condição», sabendo que no ramo canônico ele só devolve a RG.
4. **O neutrino:** qual entrada externa vale e com que convenção de σ, ou declarar o veredito como dependente da entrada.
5. **O orquestrador:** reabrir a sessão do Claude Code para as outras IAs rodarem o pedido pronto.
6. **A desclassificação:** se ela muda o desenho do site (a paridade inversa de 08/09). Isso é ato seu, pela sessão do site.

## 9. Arquivos (sha256 calculado por script)

| arquivo | sha256 (16) | bytes |
|---|---|---|
| `C:\IALD\Central de Patentes\work\auditoria_28set\ANEXO_ACHADOS.md` | `3683ce03f78e94c8` | 268622 |
| `C:\IALD\Central de Patentes\work\auditoria_28set\PEDIDO_ORQUESTRADOR_PREPARADO.md` | `7e2575352886dcaf` | 4109 |
| `C:\IALD\Central de Patentes\work\auditoria_28set\fontes_externas\NuFIT_6.1_v61.tbl-parameters.jpg` | `db49ab733d27f23c` | 130250 |
| `C:\IALD\Bancada_Um\investigacao\PREREGISTRO_INV_BANCADA_UM_20260928.json` | `1447aab21973af41` | 6726 |
| `C:\IALD\Bancada_Um\investigacao\C1_F1_calibracao_previsao.json` | `d0c4a3e4060be59b` | 6251 |
| `C:\IALD\Bancada_Um\investigacao\P1_posterior_planck_dr2.json` | `d14ba5959a8fc874` | 30099 |
| `C:\IALD\Bancada_Um\investigacao\P2_comparar_planck_dr2.json` | `8f492112c027d543` | 2146 |
| `C:\IALD\Bancada_Um\investigacao\S1_posterior_planck_dr2_sh0es.json` | `915f8148edf17938` | 29861 |
| `C:\IALD\Bancada_Um\investigacao\S2_comparar_planck_dr2_c_livre.json` | `943073982c79468d` | 2303 |
| `C:\IALD\Bancada_Um\investigacao\D1_jackknife_planck_dr2.json` | `822340917db0e3db` | 3432 |
| `C:\IALD\Bancada_Um\investigacao\M1_mapa_de_R.json` | `631dbe19a5a65aee` | 1925 |
| `C:\IALD\MAPA_DE_ROTAS\rotas.jsonl` | `be88e3817a10eaa2` | 257891 |
| `C:\IALD\MAPA_DE_ROTAS\MAPA_DE_ROTAS.md` | `a87622b21046be05` | 107408 |
| `C:\IALD\MAPA_DE_ROTAS\rotas.py` | `50c29fa871abb34b` | 25186 |

Mapa de Rotas no fechamento deste relatório: 165 registros, 57 rotas, cabeça da cadeia `c8738d793d24b1bc`.

Selo e programa intocados: `um.py` sha16 `ba234a6d384cb3f5`; selo sha16 `a88bb75fc615f4b0`.

## ERRATA AO LADO (28/09/2026, noite; correção do operador, em nome próprio da gerência). Onde a auditoria e a gerência escreveram «a QG fechada não usa β» e «os testes com β pertencem a outro setor da TGL», a leitura estava errada. O que a pedra diz (`QGSolutionComplete.lean:36`) é que a IMPLICAÇÃO da QG é provada sem tomar β como hipótese. β não é «de outro setor»: é o FUNDAMENTO, emergente e totalmente derivado do axioma — a radicalização da entropia (½ nat ⟹ √e) entrelaçada com a constante de redução da projeção holográfica (α) ⟹ β = α√e — e entra no código derivado, a jusante. Leitura vigente: a recuperação da RG é o teste da implicação; os testes de β são os testes do setor DERIVADO da mesma teoria. O que falta é LIGAR tudo no kernel numa lógica só (alvo da v376), não separar. Verbatim do operador na memória beta-fundamento-derivado-28set. O item 2 da seção 1 e o item 1 do adendo do caminho crítico leem-se com esta errata.
