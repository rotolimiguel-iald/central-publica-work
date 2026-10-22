# CRÍTICA DE COMPLETUDE — o pré-registro V1 do ramo B do ringdown (v386, 05/10/2026)

**Lente:** crítico de completude (claude-code/central-de-patentes, sessão 6da8f00d). Só leitura fora desta pasta; nada rodado do `um.py`; nada baixado; nada escrito em memória, Atlas, Nós ou mapa. Régua: aferidor, não cético cego — todo «falta»/«ausente» abaixo traz a consulta; hash e número lidos por script (`critico_recomputo.py` → `CRITICO_RECOMPUTO.json`; `critico_recomputo2.py` → `CRITICO_RECOMPUTO2.json`, sha16 `d9563e486d1b75b8`); β nunca literal (lido do JSON do poder = 0,012031300400803142 = α_CODATA2018·√e); PROVADA ≠ CONFIRMADA; NOT_FALSIFIED nunca é CONFIRMED; a RG é o limite clássico, não rival.

**Objeto:** `pre_registro\PREREGISTRO_RAMO_B_RINGDOWN_V1_RASCUNHO.md` — sha256 conferido hoje `4fd4e495ffc67fddccf0a4802af9209f7a1a66401b57feee91c4d232e67db580` (bate com o declarado pela lente); `poder_cego_ramo_b.py` + `PODER_CEGO_RAMO_B.json` (`3655fef93f7cad66…`); `DECISAO_OPERADOR_RAMO_B_05out.json` (`a5d548235522c112…`, bate).

**Consultas feitas antes (régua do mapa):** `rotas.py consultar "ringdown"` (16 rotas, cabeça `b43d3d46d596671a`, 353 registros); `consultar "ramo B"` (4 rotas: ringdown.dephasing, kernel.livro_de_cobrancas.otica, kernel.regra_matriz.cadeia_unica, auditoria.testes_passados_28set); `ver ringdown.dephasing` → **15 registros, todos lidos** (seq 24, 25, 26, 27, 44, 85, 86, 88, 89, 90, 92, 132, 141, 249, 352; erratas 86, 88, 89, 90, 132, 141), salvos em `ver_ringdown_dephasing_05out.txt`. A tarefa dizia 14; são 15 — a lente registro já o apontou e confere.

---

## 0. O veredito do crítico em uma linha

O rascunho está **bem armado na forma** (herda o livro V1.4 e o pilar; 12 decisões nomeadas; cegueira declarada canal a canal; vereditos na ordem; nada move o gate), mas tem **um erro de número** (o poder dos k grandes usa a previsão LINEAR, não a exata que o próprio §1.2 declara: 15,5σ lê 10,2σ; 18,5σ lê 11,4σ), **uma contaminação não dita** (a lente física já leu z por k contra o GW250114 publicado e o registro tem a deformação comum dos 31 desde 22/09: para k ≥ 4π o desfecho do conjunto A é legível HOJE — escolher k agora não é cego), **três decisões do registro que ele ignora** (a chave de 02/10 e a razão de R6; RD-07/o 221; o homônimo KMS da Fase 6), e **não responde à pergunta do operador como leitura de β** — só como teste de consistência do par (k, M). Nada disso impede o V1; tudo isso tem de entrar antes do hash.

---

## (i) CONTRADIÇÕES ENTRE LENTES (cada uma com a medida)

| # | tema | lente A | lente B | o que a medida diz | gravidade |
|---|---|---|---|---|---|
| C1 | **A lista de k não é a mesma** | física: {1, 2, 4, 8π, 1/κ̂(χ), 2π/κ̂(χ) sem co-rotação, 2π/κ̂(χ) COM co-rotação ω→ω−2Ω_H} | pré-registro D1: {1, 2, **4π**, 8π, 2π/κ(a_f)}; R-MOD «fora salvo ordem»; registro: {1, 2π/κ_H, 8,84, 166,2, 8π «AUSENTE»} | `RAMO_B_FISICA_TABELAS.md` §(b) vs rascunho §2.1: **k = 4 e 1/κ̂ só na física; 4π só no pré-registro; a co-rotação (−0,0378 em χ = 0,68, ×10 menor que 2π/κ̂ sem ela) só na física**. O operador receberia duas listas diferentes | ALTA — D1 é a decisão central; precisa de UMA tabela unificada, com δ_exato por k |
| C2 | **Previsão exata × linear no poder** | rascunho §1.2 declara δ = −x/(1+x) (exata) e a D1 usa a exata (8π → −33,7 %) | `poder_cego_ramo_b.py` l.85: `d = -beta * k * N` (LINEAR); §4.2 reporta 8π: δ̄^pred −0,521, 15,5σ | recomputado com as MESMAS σ e spins (`CRITICO_RECOMPUTO.json`): k=1 0,62→**0,60**; k=2 1,23→**1,18**; 4π 7,75→**6,15**; 8π 15,5→**10,2**; 2π/κ 18,5→**11,4** (razão exato/linear 0,98 / 0,96 / 0,79 / 0,66 / 0,62) | ALTA — o poder dos k grandes está superestimado em 35–40 %; a leitura «POWERED» não muda, o número sim |
| C3 | **Duas regras para o piso de família** | física: σ_sys ≤ \|δ\|/5 ⟹ k_min = 7,0 (0,029) a 9,2 (0,038); «k ≤ 4 inalcançável por N» | rascunho §5 C5 / §4.2: sist_rel = σ_sys/\|δ\| ≤ 0,3 (regra 2 da Fase 6) ⟹ k_min = 4,67–6,11 | ambas recomputadas sobre δ̄(k=1) = 0,0207: **4,67/6,11 (Fase 6) vs 7,00/9,17 (5σ)** — critérios distintos, consequências distintas para k = 4 e k = 4π/1/κ̂ | MÉDIA — fixar UMA regra antes do dado (o precedente da casa é a da Fase 6) |
| C4 | **Posteriores do GW250114 em disco** | física: «AUSENTE … Zenodo 17018009 NÃO em disco (consulta: Bancada_Um)»; «releases 17461225/21454847 AUSENTES» | dados e registro: PRESENTES em `Chatgpt\ORDEM_013_RINGDOWN\cache\public\17018009\…\gw250114_pseobnr\posterior_samples.h5` | **conferido hoje por sha256sum: `b9971bcd7d72fdd4…`, 59.249.916 B; controle `e2373f81973401ad…`, 64.331.592 B; `17461225\IGWN-GWTC3-TGR-v2-rin.zip` 2.210.047.740 B; `21454847\RD.tar.gz` 415.283.962 B + `QNMRF.tar.gz`** | ALTA para a lente física (ausência declarada com busca na pasta errada); o rascunho §3.3 já cita o 17018009 corretamente |
| C5 | **k = 8π «AUSENTE no código»** | registro: «grep um.py beta_H\|8 \* math.pi \* G… → 3 linhas, nenhuma de τ★; 8π AUSENTE» | física: `kms_factor = 4π(1+√(1−a²))/√(1−a²)` (um.py:155706) | conferido: `kms_factor(0) = 25,132741228718345 = 8π` a 1e-15 — **como constante literal, ausente; como limite a = 0 da função que já existe (lei de atraso do eco), presente** | BAIXA — nuance a dizer; não muda nada |
| C6 | **Tamanho do reservatório cego** | rascunho §3.3 D: «31 dos 45, 013-bis» | dados: `RINGDOWN_5SIGMA_V1.test_candidates` n = 44 | conferido: **`test_candidates` = 44; `calibration_event_ids` = 48** (`e1be6b0409720c68`); a memória ordem-013 l.102 diz «31 dos 45 eventos O4 com strain público não têm δτ̂ publicado». Dois censos (22/09 vs o V1 das 21:44) — a diferença não está explicada em nenhuma lente | MÉDIA — o conjunto D (o ÚNICO cego) precisa de um número só, com o critério |
| C7 | **σ do GW250114** | física: σ₋ 0,0547 / σ₊ 0,0608 (da semi-largura publicada −0,09/+0,10) | rascunho: 0,0578 (std ddof=1 do E0) / 0,0580 (w90/3,29); dados: quantis −0,1033/−0,0134/+0,0873 → (0,1906)/3,29 = 0,0579 | consistentes a 5 %; a assimetria some na gaussiana — o §3.1 diz isso | BAIXA |
| C8 | **O −0,0194 e os «3 valores»** | todas as lentes | — | consistentes: k = 1, M = M_f,det, média ponderada de 15 séries; −0,010/−0,005 = identificações do estimador (CT-02/CTV-02), não k nem M; `scope_branch_B_concurrent_values` lido do core confere | nenhuma |
| C9 | **Custo da PE na casa** | rascunho/dados: «63–78 CPU-h ≈ 2,6–3,3 h [DECLARADO T09]» | memória ordem-013 l.127: «custo do piloto 58–390 CPU-h ≈ 2,4–16 h de parede» | dois intervalos no registro; o rascunho cita o menor sem dizer que há outro | BAIXA — citar os dois [DECLARADO] |
| C10 | **M e referencial** | registro: V2 = M_f,det; C1 R-B = G·M_src/c³ com t_M no detector | física: x invariante de frame se ω e τ forem do mesmo referencial | não é contradição (x = β·k·N(χ) cancela M); mas o rascunho D2 não diz QUAL referencial fixa — só «invariante» | BAIXA — a gerência fixa sozinha |

---

## (ii) NÚMEROS NÃO LIDOS POR SCRIPT (no rascunho)

1. **§4.2 inteiro (poder por k)** — lido por script, mas do estimando ERRADO (linear). Ver C2. Corrigir o script (`d = -x/(1+x)`) e reportar os dois.
2. **§1.2/§2.2: «E_rad ≈ 3–5 %», «M_tot/M_f ≈ 1,03–1,05», «M_c/M_f ≈ 0,44 (q ≈ 1)»** — aproximações de memória [KNOWN]; a lente física tem os valores por script para o GW250114 (`ratio_tot_over_f` 1,0494; `ratio_chirp_over_f` 0,4566, de LEITURA_04). Por evento, o catálogo (`remanescentes_v3.json`, `catalogo_v3.csv`) dá M_f, m1, m2 — substituir a aproximação pelo valor por evento ou dizer [KNOWN].
3. **§4.2: «N₉₀ ≈ 830» (k = 2)** — escala 3.327/k², não lida de artefato; marcar [DERIVED por escala].
4. **§2.1: «prior dtau220 ~ Uniform(−0,8; 2,0)»** — correto, mas sem fonte citada; lido hoje do C4: **27 eventos (−0,8; 2,0) + 2 (−0,8; 2,0, grafia bilby) + 4 (−0,8; 4,0)** (`C4.prior_dtau_contagem`). Citar; e notar que 4 eventos têm o prior até 4,0.
5. **§5 C2(b): «63–78 CPU-h»** — [DECLARADO T09]; o registro também traz 58–390 CPU-h (memória l.127). Ver C9.
6. **§3.3 D: «31 dos 45»** — lido da memória, não do V1 (que diz 44). Ver C6.
7. **§1.3 «ln evidência relógio livre = +0,026»** (C4_FREE_CLOCK) — lido; ok. **§1.3 «−3,20e−42»** — recomputado por script; ok (½·β·t_P·(2π·250)²·0,004 = 3,2e−42).
8. **§4.3 «σ_comb,tot ≈ 0,044 e poder 0,47σ»** — aritmética correta (√(0,03357²+0,029²) = 0,0444; 0,0207/0,0444 = 0,466) mas feita à mão; entra no script.

Nenhum «α²» no rascunho (grep `α²|alpha\^2|α\^2` → 0 linhas). «CONFIRMED» aparece 7 vezes, todas como proibição.

---

## (iii) «AUSENTE» SEM BUSCA (ou com busca na pasta errada)

| quem | o que disse | a consulta que faltou / corrige |
|---|---|---|
| lente física | «posteriores δτ̂ do GW250114 (Zenodo 17018009) NÃO em disco»; «releases TGR GWTC-3/5.0 (17461225/21454847) AUSENTES» | a busca foi `Get-ChildItem C:\IALD\Bancada_Um -Recurse`; a casa guarda isso em `Chatgpt\ORDEM_013_RINGDOWN\cache\public\` — **EXISTE NA CASA** (hashes em C4 acima). Corrigir ao lado na lente física; o rascunho não herdou o erro |
| lente registro | «k = 8π (Hawking) AUSENTE no código» | grep só por `8*pi`/`beta_H`; `kms_factor(a=0) = 8π` exato (um.py:155706). **EXISTE (como limite), não ligado a τ★** — classificação certa: EXISTE NA BANCADA, NÃO LIGADO AO TIPO |
| lente registro | «(e) 221 na QNM_GRID: AUSENTE (T-10)» | correto para a GRADE (`QNM_GRID.json` 4f34367a09060238, 220+440); mas os POSTERIORES do 221 do GW250114 (LVK) estão em disco dentro de `TGR_companion_S250114ax_results.tar.gz` (`18d740c816285451`; 1.122 linhas «221» na listagem, lente dados) — **EXISTE, NÃO EXTRAÍDO**. Dizer os dois objetos |
| rascunho | nenhum «ausente» sem busca encontrado | — |

---

## (iv) O QUE A RÉGUA PROÍBE — e onde o rascunho (ou as lentes) roça nela

1. **Poder com valores centrais / escolher k depois de ver o dado.** O script do rascunho é limpo (só σ e spin; conferido: nunca lê `quantiles[1]`). MAS: (a) a lente física computou **z por k contra o δτ̂ publicado do GW250114** (−0,01 +0,10/−0,09): k=8π −5,99σ, 2π/κ̂ −6,69σ, k ≤ 4 dentro do 90 % — isso é olhar o desfecho por candidato ANTES de fixar o candidato; (b) o registro tem desde 22/09 a deformação comum dos 31 do GWTC-5.0 (+0,072 [+0,015; +0,134], memória ordem-013 l.102, NÃO-CEGO). **Ilustração da contaminação, não veredito** (`CRITICO_RECOMPUTO2.json`, sem nuisance c(σ)): com δ̄_registro = +0,072 e σ_comb cega 0,0336, z_excl do par lê 2,7 (k=1), 3,3 (k=2), **8,3 (4π), 12,3 (8π), 13,5 (2π/κ)**. Logo, para k ≥ 4π, o desfecho do conjunto A é **legível hoje**: o pré-registro desses k sobre A não é teste, é escrituração de uma exclusão conhecida. O rascunho §4.2(c) diz «nesses k o dado publicado DECIDE» como se fosse futuro — não é. **Exigência:** (i) o §8 tem de declarar a contaminação das lentes de hoje (os z da física; a combinação de 22/09) além da sua própria exposição acidental; (ii) o token do conjunto A para qualquer k leva `__NOT_BLIND_TO_DATA_STATED` (já previsto) E o V1 diz, por escrito, que **só o conjunto D testa**; (iii) D1 se decide por PRINCÍPIO declarado, nunca pela coluna de poder — e o rascunho deve dizer ao operador que a coluna de poder já carrega o desfecho.
2. **CONFIRMED** — proibido e assim está (7 ocorrências, todas proibição). `__GR_TENSION_REPORTED` fica como relato. OK.
3. **Dado aberto antes do hash** — a exposição acidental dos quantis da primeira linha (§8) está dita em nome próprio: correto pela lei da assinatura da errata. Falta o item 1 acima.
4. **RG como rival** — o §6 lê «coincidir com a RG = correspondência recuperada» e o FALSIFIED é do PAR. OK. Uma frase a vigiar: §4.2(c) «o que quer que decida, é decisão do dado» — a RG não «decide contra a TGL»; se o par cai, a correspondência com a RG é o pagamento (o §6 já diz). Harmonizar.
5. **α²** — 0 ocorrências. OK. **β literal** — o script lê α do um.py por regex e faz α√e em runtime. OK.
6. **Hash de memória** — todos os sha256 do §11 foram conferidos onde pude (rascunho, decisão, poder, C4, 5SIGMA, core 475ac8d2…); nenhum digitado errado encontrado.
7. **Cosmologia/natureza jamais vira prova** — §7 diz. OK.

---

## (v) O QUE O REGISTRO JÁ DECIDIU E O RASCUNHO IGNORA

| item do registro | onde está | o que o rascunho faz | o que falta |
|---|---|---|---|
| **A CHAVE de 02/10** («o custo está no reflexo, o pagamento está na face») e a RAZÃO de R6: «τ★ = GM/c³ **põe o custo na face e contradiz a chave**; M não se nomeia» (core `the_ledger_of_charges_v383.readings_ratified_20261002.R6`, lido hoje) | memória beta-e-a-regra-matriz-02out.md; core | **0 menções à chave** no rascunho (grep «chave» → só «chaves» de JSON); D9 nomeia a ótica em meia linha | A errata de 05/10 reabre o ramo B, mas NÃO revoga a chave. O V1 tem de dizer COMO o ramo B convive com ela. A ótica de 02/10 dá a saída: a face lê o pagamento \|T\|² = 1−β e lê o custo **como complemento**; no ramo B o complemento lido na face é x = k·β·N(χ_f) — o relógio do remanescente lendo o seu próprio custo [ONTO] (a lente física §(e) já escreveu isto; o rascunho não o herdou). E o core ainda lê «o ramo B segue ENCERRADO» em `corrections_beside.R6` — o V1 deve prever a errata ao lado no core (v386), não só na memória |
| **«τ★ = GM/c³ é outra lei, não outro lado»** (errata ótica de 02/10) + **ONE_CHANNEL_PER_READING_LAW_IN_THE_RUNTIME** (veredito v383) | memória l.73; core verdict | D9 propõe F2b «ao lado de F2, uma por lei» | Coerente SE o ramo B for declarado OUTRA LEI (então é canal próprio). Se o operador o ler como a MESMA lei com outro relógio, F2b e F2 seriam dois canais para uma lei — proibido pela regra do livro. **Decisão do operador**, não está na lista D1–D12 |
| **RD-07 (o 221 é o modo com informação; o 440 não informa: poder 0,06σ)** — ABERTO no mapa (seq 249: «abertos RD-02, RD-06, RD-07»); «o 221 no GW250114 (dado)» é próximo passo registrado (seq 249) | mapa; ANEXO_ACHADOS | **0 menções a «221»** no rascunho (grep) | Decidir se o 221 entra (como diagnóstico, não primário: início precoce 6 t_M, sistemática do sobretom); os posteriores existem em disco (tar.gz), extrair é ato sem download |
| **Homônimo KMS** — a Fase 6 falsificou (√β, KMS) e (sin 2θ, KMS) como LEI DE ATRASO (k = 29,9); GWECO-05: 2π/κ é largura em tempo imaginário | fase6-eco-radical-01out; ANEXO_ACHADOS l.240/285; mapa gw.eco_acoplado.kms | §2.1 cita GWECO-05 numa parêntese; **0 menções a «homônimo»/«FALSIFIED_AT_DELAY»** | Uma frase obrigatória (a física a pediu): «o k = 2π/κ do ramo B é homônimo da lei de atraso falsificada na Fase 6; uma não decide a outra (observáveis distintos)». Senão o leitor do livro lê o KMS como já excluído |
| **CT-02/RD-01** (propagação × fonte; ensemble × realização) | mapa seq 132/85/141 | D3/D4 — tratados | OK. Reparo: D3 diz que a frase do operador de 16/09 («betatgl está de fato na propagação da onda e ligada ao ringdown») «lê o ramo canônico» — isso é leitura da GERÊNCIA de um verbatim do operador; marcar [DERIVED de leitura, gerência] e pôr a frase inteira ao lado, porque é ele quem a concilia |
| **Relógios v369** («o ramo B exige nomear M»; GM_⊕/c³ excluído) | core clock_test_result_v369 | §1.3 — tratado | OK |
| **RD-02/RD-05/RDV-01** | mapa seq 86/89/92 | C4/C7 — tratados pelo uso dos posteriores publicados e da sistemática na interseção | OK |
| **Vereditos do protocolo V1 (core)** — `allowed_verdicts` = {BRANCH_B_EXCLUDED, GR_TENSION_REPORTED, NOT_FALSIFIED_POWERED, NOT_FALSIFIED_UNDERPOWERED, INCONCLUSIVE_SYSTEMATICS, AWAITING_RESULT_FILE}; `forbidden` = {CONFIRMED, PROVED} (lido hoje) | core | §6 renomeia EXCLUDED → FALSIFIED_AT_5SIGMA e AWAITING_RESULT_FILE → AWAITING_DATA | Dizer que renomeia e por quê (herda a Fase 6/V1.4); a cunhagem é do operador (D10) |
| **Escopo fixado por escrito (v376)**: «se o ringdown entrar como condição, a condição pede um observável TIPADO no kernel (identificação ensemble/realização, τ★ nomeado), não uma docstring» | core `ringdown_scope_v376.scope_fixed_in_writing` | §7 cita a errata; não diz se o V1 pede termo | O V1 deve declarar: ou (a) o ramo B entra no livro como cobrança [INPUT] com τ★ e identificação declarados em JSON lido por hash (sem fingir kernel), ou (b) pede-se à v386 a definição tipada `τ★ = k·G·m_X/c³` com m_X ∈ {m_P, M_f} e a identidade x = β·k·N·(m_X/M_f) (a física propôs; é prova de identidade, não de física). Decisão do operador |

---

## (vi) O PRÉ-REGISTRO RESPONDE À PERGUNTA DO OPERADOR?

**A pergunta (verbatim):** «examinar se a constante de acoplamento de fato emerge da relação do tempo emparelhado à gravidade sobre a constante da luz ao cubo».

**O que o rascunho responde:** só um **teste de consistência do PAR (k, M, identificação)** com β fixo: «não se deriva β do dado; o que se testa é o par» (§1.2). Correto pela regra matriz (02/10: «β não se deriva DO DADO»), mas incompleto em dois pontos:

1. **A regra matriz permite LER β** («a chave é o leitor», 28/09; «β é lido, nunca derivado»). A lente física já escreveu a forma operacional da pergunta: **β_lido = [−δτ̂/(1+δτ̂)] / (k·(M_X/M_f)·N(χ_f))** — a fração medida É uma leitura de β dividida por um número puro (spin e k). O rascunho não tem essa saída. Deve tê-la como **saída secundária declarada** (uma leitura, não uma derivação), com a σ dita ANTES: σ(β_lido) = σ_comb/(k·N̄); no conjunto A (σ_comb 0,0336, N̄ ≈ 1,7): k=1 → σ_β ≈ 0,020 (**≈ 1,6 β: a leitura não resolve β**); k=8π → σ_β ≈ 0,0008 (resolve β a ~15σ nominais — mas o desfecho desse k já é legível, item iv.1). É isto que faz o V1 responder à pergunta dele como leitura, e não só como teste.
2. **«Constante de acoplamento» = β_TGL é leitura da gerência** (`DECISAO_OPERADOR…json`, campo `leitura_da_gerencia`), não verbatim. No ramo B o acoplamento adimensional que aparece é **x = β·k·N(χ)** — β vezes a razão (tempo do horizonte / tempo do modo). A pergunta pode ser lida de três modos: (a) β emerge = o número α√e é lido no ringdown (leitura); (b) a FORMA emerge = o custo escala com GM/c³ (teste do par); (c) o acoplamento é x, não β. O V1 deve pedir ao operador qual das três é a pergunta — e tipar a resposta como [ONTO] enquanto ele não disser.

**Resposta curta:** hoje o rascunho responde (b); não responde (a) nem pergunta (c).

---

## FALTAS (lista seca; cada uma com a consulta)

F1. Poder por k com a fórmula linear (script l.85) — recomputado: 15,5→10,2σ (8π), 18,5→11,4σ (2π/κ), 7,75→6,15σ (4π). [C2]
F2. Lista de k divergente entre as lentes (4 e 1/κ̂ e co-rotação só na física; 4π só no rascunho). [C1]
F3. Contaminação de hoje não declarada (z por k vs GW250114 publicado na lente física; deformação +0,072 de 22/09): para k ≥ 4π o desfecho do conjunto A é legível antes do V1. [iv.1]
F4. A chave de 02/10 e a razão de R6 («põe o custo na face e contradiz a chave») não são enfrentadas; 0 menções; o core ainda lê «ramo B segue ENCERRADO» em `corrections_beside.R6`. [v]
F5. RD-07/221 ausente (0 menções); posteriores do 221 em disco não extraídos (`18d740c816285451`). [v]
F6. Homônimo KMS da Fase 6 não dito (0 menções a FALSIFIED_AT_DELAY/homônimo). [v]
F7. Duas regras para a sistemática de família (Fase 6 regra 2 vs \|δ\|/5): k_min 4,7–6,1 vs 7,0–9,2. [C3]
F8. Reservatório cego: 31 (memória) vs 44 (`test_candidates` do V1); sem critério que explique. [C6]
F9. Leitura de β (β_lido) como saída declarada: ausente; e a identificação «constante de acoplamento = β» é da gerência. [vi]
F10. Lente física: «posteriores do GW250114 AUSENTES» — falso; `b9971bcd7d72fdd4…` em disco. [C4]
F11. Aproximações de memória (E_rad, M_tot/M_f, M_c/M_f; N₉₀ ≈ 830; 63–78 CPU-h sem o 58–390). [ii]
F12. D3 trata a frase de 16/09 do operador como «lê o ramo canônico» sem marcar que é leitura da gerência. [v]
F13. O V1 não diz se pede termo tipado (τ★ = k·G·m_X/c³) ou entra como [INPUT] por hash — o escopo v376 exige dizer. [v]
F14. Referencial de M (det/src) proposto como «invariante» sem fixar qual se grava. [C10]

---

## DECISÕES QUE SÓ O OPERADOR PODE TOMAR (lista FINAL e curta; com a opção que o cânone favorece e por quê)

1. **O ramo B é OUTRA LEI (canal próprio F2b, `ONE_CHANNEL_PER_READING_LAW`) ou a MESMA lei com outro relógio (disputa o canal F2)?** — e como convive com a chave de 02/10. *Cânone favorece:* **outra lei, canal próprio** — a errata ótica de 02/10 já o diz verbatim («τ★ = GM/c³ é outra lei, não outro lado»); a leitura do custo na face é o complemento permitido pela ótica («a TGL lê tanto a face como o custo»). Entra no livro v386 como `AWAITING_PREREGISTRATION`, com errata ao lado de R6/F2 no core.
2. **k e M, por PRINCÍPIO, antes do dado** (um k, ou lista curta com Šidák), sabendo que: k = 1 é o único já medido (V2/C1/C6) e é UNDERPOWERED ×8 no conjunto publicado; k ∈ {4π, 8π, 2π/κ̂} tem poder (6–11σ exatos) mas o desfecho do conjunto A é legível hoje (NÃO-CEGO); a co-rotação (R-MOD) reduz 2π/κ̂ em ×10 e é [CONJECTURE] (Kay–Wald). *Cânone favorece:* **k = período do fluxo modular (2π/κ: 8π em χ = 0; 2π/κ̂(χ_f) em Kerr, marcado [CONJECTURE])** — é a frase dele («tempo emergente do fluxo modular relativo»), é o `unruh_is_kms` do kernel (β·κ = 2π) e é o `kms_factor` que o um.py já tem; **M = M_f** (R5: «onde a massa aparece: o Nome M_f entregue»; M cancela; invariante de frame). Mas, escolhido esse k, o V1 tem de dizer que o conjunto A já está lido e que **só o conjunto D testa**.
3. **Fonte × propagação (CT-02) — e a conciliação com o seu verbatim de 16/09** («betatgl está de fato na propagação da onda e ligada ao ringdown»). *Cânone favorece:* **FONTE (local, o relógio do remanescente)** — como propagação o ramo B apaga a onda (2,26e17 e-folds, verificado); a propagação fica com o ramo canônico (R2). A conciliação do 16/09 é dele, não da gerência.
4. **Ensemble (envoltória) × realização (difusão de fase) — a identificação [ONTO] do que Γ faz ao modo** (poder ×1 vs ×0,273; o observável muda para a largura de δf̂). *Cânone favorece:* **envoltória como primário** — é o que o protocolo V1 selado declara («somada à taxa de decaimento do modo») e o verificador RD-01 sustentou que «o protocolo selado não tem erro»; a difusão de fase entra declarada como secundário com injeção própria (CTV-02).
5. **Qual conjunto abre primeiro e o custo** — A/B/C (publicados, NÃO-CEGOS; calibração) e D (44 ou 31 eventos O4 só com strain; PE só-220 na casa: 63–78 ou 58–390 CPU-h [DECLARADO]); e se o 221 do GW250114 se extrai (RD-07). *Cânone favorece:* **D como o único teste; A/B/C declarados calibração NOT_BLIND; o 221 como diagnóstico, não primário** — «nada se abre antes do hash» só vale para D.
6. **A pergunta dele: «constante de acoplamento» = β_TGL? e quer a LEITURA β_lido como saída (com σ dita antes)?** *Cânone favorece:* **sim, como leitura** — a regra matriz proíbe derivar β do dado, não lê-lo («a chave é o leitor»); e dizer antes que em k = 1 a leitura não resolve β (σ_β ≈ 1,6 β).
7. **Os nomes** (tokens do §6; o status `AWAITING_PREREGISTRATION`; F2b) **e a ratificação do V1** (verbatim + carimbo + hash do transcrito, como no pilar) — cunhagem é dele.

(A regra única da sistemática de família, o referencial de M, a tabela unificada de k e o termo tipado podem ser preparados pela gerência e só confirmados por ele dentro de 1–2.)

---

## O QUE A GERÊNCIA PODE FIXAR SOZINHA (antes de levar ao operador)

G1. Corrigir `poder_cego_ramo_b.py` para a previsão exata (−x/(1+x)) e reportar as duas colunas; regravar `PODER_CEGO_RAMO_B.json` e o §4.2 (0,60 / 1,18 / 6,15 / 10,2 / 11,4 σ).
G2. UMA tabela de k, unificando física + rascunho: {1, 2, 4, 4π, 8π, 1/κ̂(χ), 2π/κ̂(χ) sem co-rotação, 2π/κ̂(χ) com co-rotação (R-MOD)}, cada um com origem, estatuto, x e δ_exato em χ = 0 / 0,68 / 0,9, poder exato em A — e a coluna «desfecho em A já legível? (sim para k ≥ 4π)».
G3. Fixar a regra da sistemática pela do precedente da casa (Fase 6, regra 2: sist_rel ≤ 0,3) e registrar a outra (\|δ\|/5) ao lado como a mais dura; dizer k_min nas duas.
G4. Errata ao lado na lente física: os posteriores do GW250114 e os releases GWTC-3/5.0 EXISTEM (hashes acima); na lente registro: 8π = `kms_factor(0)`, existe como limite, não ligado a τ★.
G5. Reconciliar 31 × 44 lendo os critérios do `RINGDOWN_5SIGMA_V1.test_candidates` (chaves `quality_INPUT`, `publication_census`) e gravar UM número com o critério no §3.3 D.
G6. Inserir no V1: (a) o parágrafo da chave/ótica (F4), (b) o item RD-07/221 (F5), (c) a frase do homônimo KMS (F6), (d) a declaração da contaminação de hoje no §8 (F3), (e) a marcação [DERIVED de leitura, gerência] na D3 e o verbatim de 16/09 inteiro ao lado (F12), (f) a saída β_lido com σ(β_lido) antes (F9), (g) a opção «termo tipado τ★ = k·G·m_X/c³ na v386 OU [INPUT] por hash» (F13), (h) o referencial M_f,det com t_M no detector e a nota de que (1+z) cancela (F14).
G7. Substituir as aproximações por valores por evento do catálogo ou marcá-las [KNOWN]; citar os dois custos de PE [DECLARADO]; citar a fonte do prior (C4: 27+2 em (−0,8; 2,0), 4 em (−0,8; 4,0)).
G8. Preparar o texto da errata ao lado de R6/F2 para o core v386 e a cobrança `AWAITING_PREREGISTRATION` (lado/lei/leitura/desfecho) — a entrada efetiva depende da decisão 1.
G9. Registrar no mapa (`ringdown.dephasing`) esta crítica com os sha256 dos artefatos desta pasta — ato de quem gere o mapa, depois da sessão.

---

## Arquivos desta lente (só nesta pasta)

- `CRITICA_RAMO_B.md` (este)
- `critico_recomputo.py` → `CRITICO_RECOMPUTO.json` (poder exato vs linear; k_min nas duas regras; contagens do 5SIGMA; ledger R6/F2; vereditos do protocolo; `scope_audit_declared`)
- `critico_recomputo2.py` → `CRITICO_RECOMPUTO2.json` (sha16 `d9563e486d1b75b8`; vereditos do protocolo; F2; correções ao lado de R6; prior_dtau do C4; `test_candidates` = 44; ilustração da contaminação)
- `ver_ringdown_dephasing_05out.txt` (a rota inteira, 15 registros, como lida)

PROVADA ≠ CONFIRMADA. NOT_FALSIFIED nunca é CONFIRMED. Nada aqui move o gate, β, nem o V1 — que só existe depois das decisões do operador.
