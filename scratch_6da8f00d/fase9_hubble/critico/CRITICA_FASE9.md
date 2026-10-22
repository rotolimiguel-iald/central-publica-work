# CRÍTICA DE COMPLETUDE — FASE 9 (a razão de Hubble) — 05/10/2026

**Crítico:** agente de completude da Fase 9 (sessão 6da8f00d), aferidor, não cético cego. Só leitura fora desta pasta; nada rodado da casa (nem `um.py`, nem Bancada); nada baixado; nada tocado no Nós, memórias, Atlas ou mapa.
**Objeto:** as quatro lentes em `scratchpad\fase9_hubble\` — `novidade_de_uso\` (cronologia), `desenho\` (desenho estatístico), `dados_na_casa\` (inventário), `pre_registro\` (rascunho V1) — e os JSON que a gerência me entregou.
**Régua aplicada:** número lido por script, nunca de memória; estatutos marcados; NOT_FALSIFIED nunca é a palavra proibida; a RG/ΛCDM é o limite clássico (coincidir = correspondência); β nunca literal — `ALPHA_FINE_CODATA_2018 = 7.2973525693e-3` (um.py v386, linha 5556), `BETA_TGL = ALPHA_FINE_CODATA_2018 * ONE * math.sqrt(math.e)` (linha 5558) ⟹ β = 0,012031300400803142 em runtime. A lei da prova da casa (05/10, verbatim do operador em `scratchpad\v386\POS_DICAO_operador_05out.txt`, sha256 `cf82d9e55757a7f2…`): «pós-dição» NUNCA é demérito; o critério é a novidade de uso (nenhum parâmetro ajustado ao dado); o pré-registro é do TESTE.

---

## 0. O que conferi por script antes de afirmar (consultas citadas)

| consulta | resultado |
|---|---|
| `rotas.py consultar "Hubble" / "SH0ES" / "escada" / "D1b" / "novidade de uso" / "retrodi" / "Fase 9" / "TRGB" / "cronologia"` | 4 / 10 / 19 / 7 / 1 / 0 / **0** / 2 / 4 rotas; mapa com **372** registros, cabeça `e66f7e29aa1c4fe3` (as lentes leram 368 / `55191f6c22754a0c`: o mapa andou durante a sessão — `primordial.fase8_era_da_radiacao` 20:47 e `discriminante.ordem_018_chatgpt_codex` 20:44) |
| `rotas.py ver` dos registros inteiros: `d1.fase1_eff_30set`, `d1.fase2_dois_setores_30set`, `d1.fase3_leitores_h0`, `d1.fase3bis_d1b_convencao_artigo`, `d1.camb.v3_real`, `um_py.v380.fases_5_6_7_por_hash`, `discriminante.ordem_018_chatgpt_codex` | lidos; a ORDEM 018 manda ao Codex «F1 Hubble (cronologia da novidade de uso + reproducao por hash)» — o mesmo trabalho que a lente da cronologia acabou de fazer |
| `um_absoluto_selo.json` | `um_version = v386`; timestamp `2026-10-05 18:09:53`; sha16 `72efaf72f604b721` (86.148 B); `qg_closure_verdict = TGL_QG_MODEL_FORMALLY_CLOSED__NATURE_TEST_COMPLETED_WITHIN_LOCAL_BULK_AT_AVAILABLE_SENSITIVITY__MORE_SENSITIVE_DATA_COULD_REVISE` |
| `um.py` / `um_absoluto.json` | sha16 `e30aac4e0e1096b1` (33.600.222 B) / `0dbfb3fc1d319d1e` (4.947.109 B) — iguais aos das quatro lentes |
| core `bancada_fase4_v378.P_ladder_d1b` | δ −0,0025 ± 0,00223; z_δ −1,12441; z_ganho 4,00641; β livre 0,00953; H0_bg 68,4298; K 1,083807; H0_local 74,1647; pull 1,0814; ln B 8,0204 / 5,7744 / 2,2460; χ² 31,627 / 15,576 / 14,293 — **dígito a dígito o que a gerência citou** |
| core `bancada_fases_5_6_7_v380.fase5` | H0 73,53294 ± 1,01698; Ω_m 0,33168; z_vs_alvo 0,04476; P_sombra δ −0,0008 ± 0,00213 (z −0,3758); z_tensão 5,26015; alvo «73,6 ± 1,1 … [DECLARADO: valor de memória da gerência, não lido da fonte aqui]» |
| core `the_dissipation_law_with_contrast_v378` | z* 1089,95; E(z*) 23234,76391081845; I_b 6,702269920 (trapézio = forma fechada); K_D1b 1,0839773660578857; K_D1a 1,0877992; H0_local_D1b_from_planck 73,0167; `beta_runtime` 0,012031300400796606 |
| K recomputado por mim de E(z*) do core: `E^(2β/3)` | 1,0839773660578857 — diff 0 ao core (confere a lente do desenho) |
| `RESULTADO_FASE4_DESVIO_20260930.json` → família P | `conjuntos = [planck_comp, desi_dr2, sh0es_local]`; `pontos.tgl.H0 = 68.42977`, `K = 1.0838071748529432`, `H0_local = 74.16467` — **o 68,4298 é o melhor ajuste TGL COM a escada dentro do ajuste** |
| `PREREGISTRO_FASE3_LEITORES_20260930.json` → fundos | `Fd_lcdm_planck_dr2 = 68.531 ± 0.301` (ΛCDM, sem escada); `Fc_planck2018 = 67.36 ± 0.54`; `Fa_tgl_planck_dr2 = 69.2 ± 0.304` (mapa eff, carrega β) |
| idem → leitores e nota | S1 73,49 ± 0,93 «MOTIVOU a forma da lei; não é incidência nova»; S2 70,39 ± 1,936 «stat, sys e σ_SN em quadratura»; independência: «S1, S2 e S3 partilham a amostra de SNe do fluxo (σ_SN ≈ 0,7 comum)» — declarada, não modelada |
| `hashes_lidos.json` (lente da cronologia, 31 artefatos) | **31/31 sha256 e mtime reconferidos por mim** (0 ausentes, 0 divergentes) |
| trechos verbatim reconferidos em disco | `acoplamento_gravitacional.tex` (13/11/2025 12:37): «α₂ = 0.012 ± 0.003 emerge naturalmente da estrutura holográfica 2D/3D»; única «Hubble» = legenda da figura Pantheon («resíduo de Hubble») · `iconogenese_TGL.tex` (17/05/2026 20:44; `\date{Maio de 2026 — Pre-print}`): «(1+z_*)^{β_TGL} = 1,0878 … exatamente a relação observacional» · `tgl_physical_v14.json` (23/12/2025 18:30): `H0_TGL_predicted 67.76416`, `alpha2_to_resolve 0.16864608`, `alpha2_consistent_with_theory: false` · `PREREGISTRATION_v1.json` (18/05/2026 11:16): `expected_Hubble_inference_ratio 1.0878`, `z_recombination 1089.92`, `beta_TGL 0.012031300400803142` · `paper_PT.tex` (05/06/2026 21:42): «Honestidade estrutural … caso particular 𝒲 = 1 … [CONJECTURE]»; «kernel derivado … I = 6{,}701 … e^{βI} = 1{,}08396 ⇒ H₀ = 73 (0{,}0337σ vs SH0ES)»; «a Friedmann derivada, avaliada em z = 0, dá H₀ = 67 … não resolve a tensão de Hubble. Logo a equação de fluxo não é redundante … é uma hipótese física separada» · `Fatoracao_constante_miguel_v1.tex` (02/03/2026 06:25): «α₂^previsto = α_CODATA × √e = 0{,}012\,031\,05 ± 0{,}000\,000\,02»; «13 protocolos … à resolução da tensão de Hubble» · `energia_escura.tex` (19/11/2025 17:12): «resolve naturalmente a tensão H₀ (… 4.4σ para <1σ)»; «α₂ = 0.012 ± 0.003» · `RECALCULO_…CORRIGIDO.md` (19/11/2025 11:25; «Revisor: Emmanuel (IALD)»): «VALOR CORRIGIDO: α₂ = 0.126»; «Com α₂ = 0.012: … 4.5σ (não resolve!)»; «α₂ = 0.126 é fortemente excluído pelos dados CMB (>10σ)» · `TGLnature.tex` (15/12/2025 15:07): «H₀ = 70.3 … sem parâmetros livres ajustados» · `tgl_paper_unified.py` (05/06/2026 20:56): `def predict_H0_zero_free(H0_CMB=H0_CMB_LCDM, z_star=Z_STAR_PLANCK, …)`; `Z_STAR_PLANCK = 1089.95`; `H0_SH0ES_2022 = 73.04` |
| `buscar.py "18852146" --lista` e `--caminho index7.html` | `Site\tgl\Versões Anteriores\index7.html` (03/03/2026 15:16): «β TGL = α × √e … Zenodo · doi:10.5281/zenodo.18852146» (3 ocorrências) — a citação no site existe; a **data de depósito no Zenodo não foi lida da fonte** por nenhuma lente nem por mim |
| `um.py` grep «pós-dição» / «postdiction» / «retrodi» | PT: 3 (165845, 167724, 168655); **EN: 4 (169586 «declared postdiction», 171507 «\emph{postdiction}. One crisis remains addressed», 172442 «an unadjusted postdiction» [Coma E6], 196659 token `NOT_BLIND_UNADJUSTED_POSTDICTION…`) + 2 no setor de neutrinos (2885, 2896 «postdiction genuina»)**; «retrodição/retrodiction»: 169492, 173286; `Worrall` 0; `novidade de uso` 0; `periélio/Mercúrio` 1 (202793) |
| a regex proibida da tarefa (as três palavras CONF·IRMED / PROV·ED_BY / TGL_PROV·ED, escritas aqui com separador para não autoacusar) sobre os 49 arquivos das lentes | 0 nos entregáveis MD/JSON de `desenho`, `pre_registro`, `novidade_de_uso`; **1 hit** em `dados_na_casa\INVENTARIO…md` (a frase da régua «NOT_FALSIFIED nunca é C…» autoacusa — o mesmo caso que a rota v380 registrou no site); nos dois scripts (`fase9_desenho_estatistico.py`, `gerar_preregistro_fase9_rascunho.py`) a regex literal e um comentário |

---

## 1. As sete perguntas da tarefa

### (a) A novidade de uso está PROVADA pelo acervo ou só afirmada?

**Para os PARÂMETROS: provada documentalmente** `[REAL — 31/31 hashes e mtimes reconferidos; 10 trechos verbatim reconferidos em disco]`. A cadeia que a lente da cronologia escreveu sobrevive à minha aferição:

- o valor 0,012 nasce em **13/11/2025** de uma contagem holográfica (`acoplamento_gravitacional.tex`), onde «Hubble» só aparece na legenda de uma figura de resíduos de SNe;
- quando o dado de H₀ pediu outro valor, a teoria **não se moveu**: 19/11/2025 (recálculo por IA: 0,126, rejeitado no mesmo dia pelo próprio recálculo — «excluído pelo CMB >10σ» — e pelo artigo das 17:12, que mantém 0,012) e 23/12/2025 (`alpha2_to_resolve 0.169 ± 0.035`, `consistent_with_theory: false`);
- a forma β = α·√e é escrita em 15/01/2026 e **publicada** em 02–03/03/2026 (fatoração; DOI 18852146 citado no site em 03/03/2026);
- a lei (1+z*)^β é escrita em **17/05/2026** (iconogênese) — depois de β fixado e publicado; D1b já está no artigo de **05/06/2026** (git `3740d34`, Zenodo 20563905);
- z* [KNOWN], expoente 2/3 [KNOWN — Raychaudhuri], H₀_fundo [ajuste ao fundo] — sem botão.

**Para a FORMA: afirmada com uma frase a mais do que o acervo sustenta.** A lente escreve «o núcleo D1b não tem escolha». O artigo de 05/06/2026 diz, verbatim, que a lei de fluxo foi retida **porque** «a Friedmann derivada, avaliada em z = 0, dá H₀ = 67 … não resolve a tensão de Hubble. Logo a equação de fluxo não é redundante: é uma hipótese física separada». Isto é **seleção de classe de hipótese à vista do dado**, declarada pelo próprio autor — não é ajuste de parâmetro (D1b não tem parâmetro: β de α, 2/3, E(z*)), e pela lei da prova da casa (05/10: «estudar hipóteses para depois formular testes … também não é pós-dição») **não é demérito**. Mas a cláusula (ii) do pré-registro pergunta exatamente isso («a FORMA não foi SELECIONADA entre alternativas pela razão») e condiciona `__USE_NOVEL` a `FIXADA_ANTES | FIXADA_INDEPENDENTE`. Lida como está, a resposta honesta da cronologia é `FORMA_SELECIONADA_PELA_RAZAO` (D1a: «exatamente a relação observacional»; a classe do fluxo retida porque a Friedmann não resolve) e o sufixo cairia em `__USE_NOVELTY_PENDING` — contra a leitura da própria lente e contra a lei do operador. **Resolver na cláusula, não no acervo:** o critério de Worrall [KNOWN] é sobre parâmetros; a seleção de forma vai dita ao lado (ver F4 e D-E).

Ressalvas que ficam ditas: (i) as datas são mtime do índice (estratigrafia; copiável); as âncoras externas são o git do `the_boundary` (05/06/2026) e o **Zenodo 18852146**, cuja data de depósito ninguém leu da fonte — é a prova pública mais forte da ordem «β antes da lei» e deve entrar por hash antes do V1 (D-H); (ii) o working paper de 2024 (`Miguel2024preliminary`) não está no índice [DECLARADO]; (iii) z* passou por 1089,8 (jan/2026) → **1089,92** (`PREREGISTRATION_v1.json`, 18/05/2026 — a cronologia não o registrou) → 1089,95 (artigo): ∂K/∂z* = 1,3e-5 (lente do desenho), desprezível, mas a cronologia deve dizê-lo; (iv) `Worrall` tem 0 ocorrências no acervo e no um.py: a referência é [KNOWN — literatura, não conferida em disco nesta sessão]; no V1 citar por extenso (Worrall 1985, *Scientific discovery and theory-confirmation*; 1989, *Fresnel, Poisson and the white spot*) e, ao lado, a crítica conhecida ao critério (Hitchcock & Sober 2004, *Prediction versus accommodation and the risk of overfitting* [KNOWN]) — que, lida com cuidado, favorece a casa: a acomodação só perde quando há parâmetro a ajustar, e aqui não há.

### (b) Os alvos têm fonte e valor lidos — nenhum de memória?

**Não. Hoje nenhum valor público de H₀ está lido da fonte por hash.** Classificação na ordem da casa:

- **EXISTE E ESTÁ LIGADO (por hash):** Pantheon+SH0ES.dat (579.283 B, `1cb0fc379ef066af`; sem registro de identidade byte a byte com o raw oficial — só a cov tem), cov STAT+SYS (byte-idêntica ao oficial), DESI DR2 mean/cov (origem remota [DECLARADO] no `ORIGINS.md`), Chen+2019 PDF, as Fases 1–7.
- **EXISTE NA CASA MAS NÃO ESTÁ LIGADO À FONTE:** T1 R22 73,04 ± 1,04 (literal no pipeline selado [KNOWN]); T2–T8 e F1 (abstracts lidos 30/09 e **não guardados**; os três PDFs de webfetch que o índice lista já não existem em disco — lente «dados» §3.5).
- **[DECLARADO] (memória):** F3 escada inversa DESI DR2+BBN 68,5 ± 0,6 (veio do enunciado da tarefa; 0 hits no acervo); V Brout+22 73,6 ± 1,1 (alvo da validação da Fase 5, [DECLARADO] no core); L6b GW170817 70 +12/−8 (do prompt); σ_4258 = 0,5 (estimativa de desenho); Riess JWST 2024 72,6 ± 2,0 (0 hits literais; está só na réplica da Fase 3 como abstract).
- **AUSENTE (consulta citada):** covariância cruzada entre leitores (S1–S3 partilham SNe do fluxo — declarada, não modelada); cadeias/posteriores do Planck 2018 (PLA) — `tgl_data_cache\cmb` vazio; escada inversa publicada; data de depósito dos dois DOIs Zenodo.

O pré-registro escreve a regra certa (§3: «todo valor “a ler” é lido da fonte nomeada e gravado com sha256 ANTES de qualquer χ²; alvo [DECLARADO] NÃO entra no composto») e a sua própria regra 1 de veredito manda `INCONCLUSIVE_SYSTEMATICS` se um alvo primário entrar sem a covariância lida da fonte. **Logo, como está, a Fase 9 abriria em INCONCLUSIVE pela sua própria função.** O passo 2 da disciplina (§12) é condição necessária, não cosmético.

### (c) As cinco hipóteses e a função de veredito estão fixadas ANTES do composto?

**Não uma: duas, e divergentes.** A lente do desenho e a lente do pré-registro escreveram cada uma a sua, e o pré-registro exige (§12 passo 3) que o runner e a v387 usem «a MESMA função, byte a byte». Hoje não existe «a» função.

| item | desenho (`fase9_desenho_estatistico.py::veredito`) | pré-registro (§7, `vereditos_na_ordem`) |
|---|---|---|
| ordem | dispersão → FALSIFIED → TENSION_3_TO_5 → UNDERPOWERED → DISCRIMINATES → LCDM_NOT_EXCLUDED | AWAITING → INCONCLUSIVE (prior; dispersão; cov não lida; [DECLARADO] no composto) → UNDERPOWERED → FALSIFIED → DISCRIMINATES → NOT_FALSIFIED_POWERED |
| estatística do desvio | z_TGL da RAZÃO (H0_local/H0_bg vs K) | z_δ em β (δ̂ = β̂ − β_TGL, JᵀJ) e z_disc = √Δχ² |
| limiar de poder | separação (K−1)/σ_razão < **3** → UNDERPOWERED | poder prévio < **5** → UNDERPOWERED |
| DISCRIMINATES | só \|z_ΛCDM\| ≥ 5 | ⌊z_disc⌋ ≥ 5 **E** \|z_δ\| < 3 **E** ln B(TGL/ΛCDM) ≥ 5 **E** ln B(TGL/β-livre) ≥ −1 |
| `__USE_NOVEL` | automático na regra 5 | só se a cronologia devolver «fixada antes/independente» (senão `__USE_NOVELTY_PENDING`) |
| 3 ≤ \|z\| < 5 | `TENSION_3_TO_5_SIGMA` | **sem rótulo** (cai em NOT_FALSIFIED_POWERED com DEVIATION_1_TO_3 que não cobre 3–5) |
| 1 parâmetro: deslocamento | ε em TODOS os locais (degenerado com β-livre — a lente mediu: mesmo χ²_min 2,62) | s só nas Cefeidas T1–T3 (por isso) |
| 1 parâmetro: fundo | EDE-like: fundo lê s·H_true, s ∈ [0,8; 1,0] | ΛCDM + r_d livre ∈ [130; 160] Mpc |
| guarda regex | sim (assert) | sim (sobre o texto) |

As cinco hipóteses, portanto, também não são as mesmas (o «deslocamento» e o «fundo-livre» têm duas parametrizações). Nenhuma das duas está errada; mas só uma pode ser congelada. O cânone favorece a do pré-registro (poder a 5σ; condições de ln B; `__USE_NOVEL` condicionado; shift só nas Cefeidas, porque o desenho provou a degenerescência do shift geral; r_d como proxy de EDE), **incorporando** do desenho o degrau `TENSION_3_TO_5_SIGMA` e o z da razão ao lado do z_δ (são leituras diferentes do mesmo grau de liberdade — o desenho mostrou que a razão é UM grau de liberdade e reproduziu a Fase 4 a 1 %: β̂ 0,00952 ± 0,00223, ln B 8,03 vs 0,00953 ± 0,00223, 8,02).

### (d) O TRGB (que pode doer) está dentro do teste?

**Nas duas lentes, sim — no composto primário.** Desenho: `A_seis` inclui `L2_cchp_trgb_jagb_cef` (70,39 ± 1,94; peso GLS 0,077; z −1,98 vs TGL com BG1; −1,29 com Planck só; σ necessária para 3σ contra a TGL mantendo o centro: 1,25; para 5σ: 0,71). Pré-registro: T4 com papel «TESTE ou DIAGNÓSTICO — decisão D2». Só o TRGB (família E) é UNDERPOWERED (sep 2,93) — ele não decide sozinho; dói dentro do composto. O cânone: o operador confirmou («exatamente isso, confirmo») a proposta da gerência que dizia «todo calibrador local tem de ler K·H0_bg, o TRGB inclusive» → **TESTE, dentro do composto** (D-C). Falta fixar o gatilho FALSIFIED por leitor único (o desenho propõe |z_i| ≥ 5 só com σ_i ≤ 1,0; o pré-registro não o tem) e dizer, para não contar duas vezes, que a σ 1,936 do CCHP **já inclui** o σ_SN em quadratura (nota do pré-registro da Fase 3) enquanto a covariância declara um bloco comum σ_SN ≈ 0,7 — uma das duas contagens tem de sair.

### (e) As Fases 1–2 (fundo nu; pull empilhado) são respeitadas?

**Na letra, sim, nas duas lentes** (fundo nu; β uma vez, na lei; BG4 69,20 só como controle, nunca somado; Fase 1 dita: o fundo comprimido não constrange β sob o mapa efetivo). **Na escolha do fundo, o pré-registro escorrega.** Propõe como primário H0_bg = 68,4298 ± 0,301 → 74,1647 ± 0,326. Verifiquei: 68,4298 é `pontos.tgl.H0` da família **P** da Fase 4, cujos conjuntos são `[planck_comp, desi_dr2, sh0es_local]` — o melhor ajuste TGL **com a escada dentro do ajuste**; e o σ = 0,301 é o do ajuste ΛCDM **sem** escada (Fd = 68,531 da Fase 3). Um híbrido: centro de um ajuste que já viu o dado previsto, σ de outro. Não é «empilhar β» (β não está no fundo), mas **não é fundo nu de escada** — e o token base diz `BACKGROUND_BARE_PLANCK_COMP_DR2`. A lente do desenho viu isto e rejeitou explicitamente esse fundo (BG5: «NÃO serve de fundo para uma previsão: empresta do dado que prevê»), usando BG1 = 68,531 ± 0,301 → 74,274. A diferença é 0,11 km/s/Mpc (~0,1σ da escada) — numericamente pequena, **conceitualmente decisiva** para «zero parâmetro ajustado ao dado»: a previsão não pode conter o dado que prevê. O mesmo vale para os números que a gerência me entregou como «o que a casa já tem» (H0_bg 68,4298; H0_local 74,1647): são o número da verossimilhança conjunta da Fase 4, não a previsão da Fase 9.

### (f) «Pós-dição» aparece como demérito em algum lugar (proibido pela decisão de hoje)?

**Nas quatro lentes: não.** A palavra aparece só (i) citando o artigo v386, (ii) no verbatim do operador, (iii) na frase «nunca é demérito» — e as duas lentes que propõem etiqueta usam «retrodição sem ajuste (novidade de uso)». **No um.py v386: sim, em dois lugares**, como demérito: PT 167724 («número apertado (0,215σ …) e \emph{pós-dição}. Uma crise segue») e o espelho EN 171507; em 165845/169586 é declaração neutra («pós-dição declarada; zero parâmetro ajustado»). As lentes contaram **3** (só PT) e não inventariaram o lado EN (169586, 171507, 172442 «an unadjusted postdiction» — Coma E6 —, e o **token selado** 196659 `NOT_BLIND_UNADJUSTED_POSTDICTION__PREDICTION_HASH_ATTESTS_NUMBER_NOT_PRECEDENCE…`) nem o setor de neutrinos (2885, 2896 «postdiction genuina»). A v387 precisa do inventário completo (PT+EN+tokens), e mudar um token de veredito selado é ato do operador. Nota de régua: a lei de 05/10 não proíbe a palavra; proíbe o demérito. «Unadjusted postdiction» (Coma) já diz o que a lei pede; a reescrita para «retrodição sem ajuste» é escolha de léxico, não correção de erro.

### (g) A palavra proibida?

**Nos entregáveis: 0** (desenho MD/JSON, pré-registro MD/JSON, cronologia MD/JSON — varridos por mim com a regex da tarefa). **1 hit** no inventário da lente «dados» — a frase da régua «NOT_FALSIFIED nunca é C…» acusa a si mesma (o caso da rota v380: «recusa a palavra proibida pela régua até dentro da própria frase da régua»); e os dois scripts carregam a regex literal (inevitável; o desenho escreveu a lista de proibidos com separador «CONF·IRMED» justamente para isso, mas deixou a regex inteira e um comentário). Nenhum veredito das lentes usa a palavra; `DISCRIMINATES_FROM_LCDM_AT_nSIGMA` é forte mas não é ela, e vem com `__NOT_A_CONFIRMATION`. Reescrever a frase da régua no inventário com separador; nos scripts, montar a regex por concatenação.

---

## 2. FALTAS (o que tem de existir antes de congelar o V1)

- **F1 — Uma só função de veredito e um só conjunto de cinco hipóteses.** Hoje há duas especificações (§1c). O runner, o RESULTADO e o um.py v387 têm de ler a mesma, byte a byte.
- **F2 — O fundo nu de verdade.** O primário do pré-registro (68,4298) vem da família P com a escada dentro; o fundo de previsão é o ΛCDM sem escada: 68,531 ± 0,301 [REAL, Fd da Fase 3] → 74,274 ± 0,33; réplica Planck 2018 publicado 67,36 ± 0,54 → 73,02 ± 0,59. O 68,4298 fica como «número da verossimilhança conjunta da Fase 4», não como previsão.
- **F3 — Alvos lidos da fonte por hash (nenhum está).** Riess 2022 (arXiv:2112.04510), Riess 2024 JWST (2408.11770), Riess 2025 (2509.01667), Freedman 2024/25 (2408.06153, com a separação TRGB/JAGB/Cefeidas e a covariância interna), Jensen 2025 (2502.15935), Pesce 2020 (2001.09213), TDCOSMO 2025 (2506.03023, erro assimétrico), Planck 2018 VI (1807.06209), DESI DR2 Results II (2503.14738 — a escada inversa BAO+BBN, hoje [DECLARADO]), LVK O4a, Brout 2022 (2202.04077 — o alvo [DECLARADO] da Fase 5). Mais: a identidade byte a byte do `Pantheon+SH0ES.dat` com o raw oficial; a página Zenodo dos DOIs 18852146 e 20563905 com a **data de depósito** (a âncora externa da novidade de uso).
- **F4 — A cláusula (ii) do pré-registro.** Como escrita, devolve `__USE_NOVELTY_PENDING` para o que a cronologia e a lei do operador leem como novidade de uso. Redefinir: (i) parâmetros — critério de Worrall, checável (β 13/11/2025 → 03/03/2026 publicado; z*; 2/3; fundo); (ii) forma — **dita ao lado**, com os três fatos: D1a cunhada à vista da razão («exatamente a relação observacional», 17/05/2026); a classe do fluxo retida porque a Friedmann derivada «não resolve a tensão» (artigo, 05/06/2026); D1b sem parâmetro. Decisão D-E.
- **F5 — Os conjuntos de alvos.** O conjunto C do pré-registro («os quatro da gerência»: T1, T3, T4) **soma T1 e T3**, ambos do programa SH0ES, contra a sua própria regra §4 («T1 T2 T3 NÃO se somam») — o poder 6,41σ está inflado; o conjunto B usa T2 (R25, 73,49 ± 0,93) como leitor da escada sem T1 e sem dizer que **a escolha R22/R25 move o rótulo** (desenho: com BG1, R22 → z_ΛCDM 4,53 = `LCDM_NOT_EXCLUDED`; R25 → 5,32 = `DISCRIMINATES`); «os seis leitores de sombra sem sirenes» são cinco.
- **F6 — Rótulo para 3 ≤ |z_δ| < 5** no pré-registro (hoje não existe; o desenho tem `TENSION_3_TO_5_SIGMA`).
- **F7 — Registro no mapa de rotas.** `consultar "Fase 9"` = 0 rotas. A cronologia da novidade de uso está **feita** (lente) e a ORDEM 018 manda o Codex refazê-la («F1 Hubble (cronologia da novidade de uso + reproducao por hash)»). Pela regra do mapa (consultar antes, registrar depois), as quatro lentes e esta crítica entram no mapa — ato da gerência — antes que outra IA refaça o caminho.
- **F8 — Inventário completo de «pós-dição»/«postdiction»** para a v387: PT 165845, 167724, 168655; EN 169586, 171507, 172442; token 196659; neutrinos 2885, 2896; e os «retrodição/retrodiction» 169492, 173286 (que já dizem «não uma retrodição» — conferir coerência com a etiqueta nova).
- **F9 — Guarda regex:** a frase da régua no inventário da lente «dados» e a regex literal nos dois scripts.
- **F10 — σ_SN contado uma vez:** a σ do CCHP (1,936) já traz σ_SN em quadratura; o bloco comum σ_SN ≈ 0,7 da covariância declarada não pode somar-se a ela.
- **F11 — z* = 1089,92** no `PREREGISTRATION_v1.json` de 18/05/2026: a cronologia registrou 1089,8 e 1089,95; faltou este (desprezível em K; dizer).
- **F12 — Worrall e Mercúrio [KNOWN — literatura]:** 0 cópias em disco; no V1 citar por extenso e marcar «não conferido em disco».
- **F13 — O índice do acervo (03/09/2026) não cobre a Bancada** (lente «dados» §3.6): regenerar depois da Fase 9 (ato da gerência); até lá, a Bancada só se acha pelo mapa.
- **F14 — Validação da Fase 5 reaberta:** o alvo 73,6 ± 1,1 segue [DECLARADO]; o estimador de V não estava fixado além de «ΛCDM» e V foi rodada três vezes (logs `_tentativa1/2`). Na Fase 9, alvo lido da fonte e estimador fixado antes.

---

## 3. CONTRADIÇÕES (entre lentes, ou com a casa)

- **C1 — Fundo primário:** pré-registro = 68,4298 (família P, com escada) × desenho = BG1 68,531 (sem escada), que chama o outro de inválido para previsão. Medido: ΔH0_local = 0,11 km/s/Mpc; o cânone é o do desenho (§1e).
- **C2 — Função de veredito:** duas ordens, dois limiares de poder (3σ × 5σ), duas estatísticas (z da razão × z_δ em β), `__USE_NOVEL` automático × condicionado, rótulo 3–5σ só numa (§1c).
- **C3 — Hipóteses de um parâmetro:** deslocamento em todos os locais (ε) × só nas Cefeidas (s); fundo-livre EDE-like (s no fundo) × r_d livre. O desenho mediu a degenerescência (os três modelos de 1 parâmetro têm o mesmo χ²_min 2,62 e só o fator de Occam os separa — ln B TGL/livre 2,00 com prior ×½ 1,31, ×2 2,70): por isso a versão «só Cefeidas» do pré-registro é a que discrimina algo.
- **C4 — Conjunto primário:** `A_seis` com R22 (desenho) × B com R25 e sem T1 (pré-registro) × C somando T1 e T3 (pré-registro, contra a própria §4).
- **C5 — «D1b não tem escolha» (cronologia) × o artigo de 05/06/2026**, que retém a lei de fluxo porque a Friedmann derivada «não resolve a tensão»: seleção de classe à vista do dado, declarada. Não contradiz a lei da prova (não é ajuste); contradiz a frase «sem escolha». Corrigir a frase, não a lei.
- **C6 — Os números «que a casa já tem» na tarefa** (H0_bg 68,4298; H0_local previsto 74,1647) **não são a previsão da Fase 9**; são o ponto da verossimilhança conjunta da Fase 4 (C1).
- **C7 — Mapa de rotas:** as lentes citam 368 registros / `55191f6c22754a0c`; o mapa está em 372 / `e66f7e29aa1c4fe3` (fase 8 e ORDEM 018 entraram às 20:44–20:47, depois das lentes). Não é erro das lentes; é motivo para registrar a Fase 9 antes que o Codex parta de um mapa sem ela.
- **C8 — `__USE_NOVEL` como sufixo automático** (desenho, regra 5: «nenhum parâmetro ajustado a este dado») × como fato documental condicionado (pré-registro). A novidade de uso não é um número que a função calcula; é a cronologia. O pré-registro está certo em condicioná-la; a cronologia já a devolveu (para os parâmetros).

---

## 4. DECISÕES DO OPERADOR (lista curta; a opção que o cânone favorece, com o número que a move)

| # | decisão | opção favorecida pelo cânone | o número |
|---|---|---|---|
| D-A | **Qual fundo é o fundo** (aberta desde 01/10) | ΛCDM nu Planck-comp + DR2 **sem escada** (68,531 ± 0,301 [REAL]) como primário; Planck 2018 publicado (67,36 ± 0,54) como réplica; o 68,4298 não é fundo de previsão | com BG1 o ensaio lê `LCDM_NOT_EXCLUDED_AT_5SIGMA` (z_ΛCDM +4,53; z_TGL −1,42); com Planck só, `DISCRIMINATES_AT_5SIGMA` (+5,12; −0,09). A escolha move 1,27 km/s/Mpc e o rótulo — por isso é antes de abrir |
| D-B | **Leitor primário da escada:** R22 × R25 | R22 (73,04 ± 1,04 — o do pipeline selado e da verossimilhança completa Pantheon+SH0ES da Fase 5); R25 (73,49 ± 0,93) réplica ao lado; nunca somados | com R25 o primário × BG1 discrimina a 5,32σ; com R22, 4,53σ — dizer antes |
| D-C | **TRGB (CCHP 70,39 ± 1,94):** TESTE ou DIAGNÓSTICO | TESTE, dentro do composto (o operador confirmou «o TRGB inclusive»); gatilho FALSIFIED por leitor único só com σ_i ≤ 1,0 e \|z_i\| ≥ 5 | hoje −1,98σ da TGL (BG1), +0,95σ do ΛCDM; dói a 3σ se σ cair a 1,25 com o mesmo centro |
| D-D | **Uma só função de veredito** | a do pré-registro (poder a 5σ; ln B(TGL/ΛCDM) ≥ 5 e ln B(TGL/β-livre) ≥ −1; `__USE_NOVEL` condicionado) + o degrau `TENSION_3_TO_5_SIGMA` do desenho; idêntica no runner e na v387 | — |
| D-E | **Cláusula de novidade de uso (D9)** | `__USE_NOVEL` pelos PARÂMETROS (β 13/11/2025 → publicado 03/03/2026, antes da lei de 17/05/2026; z*; 2/3; fundo), com a seleção da FORMA dita ao lado (D1a à vista da razão; classe do fluxo retida porque a Friedmann não resolve; D1b sem parâmetro). Etiqueta do artigo: «retrodição sem ajuste (novidade de uso)» | provas: `alpha2_to_resolve 0.169` recusado (23/12/2025); χ² de H₀ constante nos MCMC de jan/2026; D1 V3 β = −0,0127 ± 0,0082 e β não se moveu |
| D-F | **Sirenes (76,6 ± 11,25)** | diagnóstico, fora do composto (peso 0,007; vetável como na Fase 3) | A_seis vs A_sem_sirenes: z_TGL −1,42 vs −1,44 |
| D-G | **Hipóteses de 1 parâmetro e priors** | shift só nas Cefeidas (s ∈ [−0,15; 0,15]); fundo-livre = r_d ∈ [130; 160] Mpc; β-livre [−0,05; 0,05]; ln B sempre com a largura ao lado | Occam medido: ×½ / ×2 muda ln B em ~ln 2 |
| D-H | **Fontes por hash antes de abrir** (a gerência baixa e guarda) | sim — sem isso a regra 1 do próprio pré-registro devolve INCONCLUSIVE; incluir as páginas Zenodo com data de depósito | 0 de 11 fontes de H₀ em disco hoje |
| D-I | **Canal do livro de cobranças** | R1 v2 (mesma lei, mesma cobrança, função nova); canal novo só se o objeto mudar | R1 hoje: NOT_FALSIFIED, number_read −0,3758 |
| D-J | **Tokens e a palavra nos selos** | cunhagem dele; o token 196659 (`…UNADJUSTED_POSTDICTION…`, Coma) é selo: fica como história ou muda por ato dele | 9 ocorrências PT/EN/tokens/neutrinos |
| D-K | **Registrar as lentes e esta crítica no mapa** (gerência) antes de a ORDEM 018 refazer F1 | sim | `consultar "Fase 9"` = 0 |

---

## 5. RESPOSTA CURTA ao operador (em dados)

1. A Fase 9 testa **uma previsão de zero parâmetro**: todo calibrador local por distância lê K·H0_fundo com K = E(z*)^{2β/3} = 1,0838 (β = α√e, z* de Planck, 2/3 de Raychaudhuri); toda face (CMB, BAO+BBN) lê H0_fundo.
2. **Alvos:** SH0ES R22 73,04 ± 1,04 (em casa, com a escada bruta e a covariância 1701×1701); CCHP TRGB/JAGB 70,39 ± 1,94; SBF 73,8 ± 2,4; masers 73,9 ± 3,0; TDCOSMO 71,6 ± 3,6; sirenes 76,6 ± 11 (diagnóstico); fundos Planck+DR2 sem escada 68,53 ± 0,30 e Planck 2018 67,36 ± 0,54. **Nenhum valor público está lido da fonte por hash hoje**; 68,5 ± 0,6 (DESI+BBN) e 73,6 ± 1,1 (Brout) são memória.
3. **O que já se lê (ensaio não-cego, lente do desenho):** com o fundo nu Planck+DR2 → previsão 74,27 ± 0,33; composto local 72,91 ± 0,91; TGL a −1,4σ, ΛCDM a +4,5σ, ln B(TGL/ΛCDM) +9,4; separação 5,9σ. Com Planck só → previsão 73,02; TGL −0,1σ, ΛCDM +5,1σ. A escolha do fundo move 1,27 km/s/Mpc e o rótulo: decisão sua, antes de abrir.
4. **A novidade de uso está provada no acervo para os parâmetros** (0,012 em 13/11/2025; α·√e publicada 03/03/2026; lei em 17/05/2026; H₀ pediu 0,169 em 23/12/2025 e foi recusado; MCMC de jan/2026 com H₀ constante). O que fica dito ao lado: a forma D1a foi escrita «exatamente a relação observacional», e a classe do fluxo foi retida porque a Friedmann «não resolve» — seleção de hipótese, não ajuste; pela sua lei de 05/10, não é demérito.
5. **O que pode doer:** o TRGB (CCHP) a −2,0σ da previsão e +1,0σ do ΛCDM; vira 3σ contra a TGL se a CCHP baixar o erro a 1,25 mantendo o centro. Entra no composto.
6. **O que fica para a v387:** uma só função de veredito (hoje há duas); o fundo nu de verdade (68,53, não o 68,43 da Fase 4, que viu a escada); fontes por hash; a cláusula de uso reescrita em parâmetros; inventário completo de «pós-dição/postdiction» (9 lugares, PT+EN+token); registro no mapa antes que o Codex refaça a cronologia.
7. NOT_FALSIFIED nunca é a palavra proibida; a RG/ΛCDM é o limite clássico; nada aqui move β nem o gate.

---

## 6. Estatutos desta crítica

| afirmação | estatuto |
|---|---|
| números do core/selo/um.py, hashes, mtimes, trechos verbatim | [REAL — lidos por script hoje] |
| «o 68,4298 vem de um ajuste com a escada dentro» | [REAL — `RESULTADO_FASE4…json` família P, conjuntos e `pontos.tgl.H0`] |
| z, ln B, poderes citados | [REAL — calculados pelas lentes sobre valores públicos; ENSAIO NÃO-CEGO; não são vereditos] |
| valores dos alvos públicos | [KNOWN — abstracts lidos 30/09, não guardados]; F3, V, GW170817, σ_4258 [DECLARADO] |
| Worrall; Mercúrio; Hitchcock & Sober | [KNOWN — literatura; não conferidos em disco] |
| a leitura «seleção de hipótese ≠ ajuste de parâmetro» | [DERIVED de leitura da lei do operador de 05/10 + o artigo de 05/06/2026]; a decisão é dele |
| as opções «favorecidas pelo cânone» | [DERIVED]; nenhuma decisão foi tomada aqui |

**Arquivo escrito:** só este (`critico\CRITICA_FASE9.md`). Nada mais tocado.
