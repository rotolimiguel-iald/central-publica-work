Todos os números estão na mesa. Montando o dossiê final.

# O CASO COMA — dossiê TGL (montagem: 3 frentes + aritmética verificada)

**Régua aplicada: o número corrige a frase. β = α·√e computado em runtime = 0,012031300 (nunca literal). Reprodução: `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6cf86791-e33f-42fd-bd3b-241a68be6ebc\scratchpad\caso_coma_calc.py` (motor transcrito do selado com proveniência de linha).**

---

## 0. Veredito executivo (números primeiro)

1. **O caso existe e não foi refutado (07/2026):** Coma medida a 98,5 ± 2,2 Mpc (12 SNe Ia) contra 111,8 ± 1,8 Mpc exigidos por Planck+ΛCDM via FP-DESI — 4,6σ (0,28 ± 0,06 mag). Confirmado por vias independentes; moderado (não desfeito) pelo DESI DR1.
2. **A tese do operador fecha em direção, e em magnitude fecha PARCIALMENTE:** a fração de z que precisaria ser não-expansiva é **8,5–11,9%** conforme a formulação. A TGL selada oferece, na camada [CONJECTURE] da lei de fluxo, **f = 8,07%** (D1a) / **7,75%** (D1b) — **bate o caso DESI DR1 a 0,35σ** e o SH0ES, mas fica **1,6σ curta do caso FP-EDR extremo** de Scolnic.
3. **A camada [REAL] da TGL não explica Coma:** a fórmula sobrevivente H²_TGL = H²_ΛCDM·[1+β|1+w_eff|] move a distância **−0,193% (−0,21 Mpc)** dos 13,3 Mpc de gap. Para fechar sozinha precisaria β_eff = 70–76×β. Número na mesa; frase corrigida.
4. **Curiosidade registrada e contida:** √β = 0,10969 coincide com a fração requerida da rota ingênua (10,90% ± 1,99 p.p.) a **+0,03σ** — sem mecanismo selado; proibido virar motor sem derivação.
5. **Degenerescência declarada:** para Coma sozinha, "vazamento modular de 8%" e "H0 local = 73,26" são numericamente indistinguíveis. Coma não prova TGL; testa o par (Planck-H0 + defasagem) contra (Planck-H0 sem defasagem).

---

## 1. O CASO EM NÚMEROS

### 1.1 Redshift de Coma (Abell 1656)

| Grandeza | Valor | Fonte |
|---|---|---|
| z heliocêntrico (membros DESI) | ≈ 0,0232 (cz ≈ 6.956 km/s; σ_membros ≈ 0,003) | Scolnic et al. 2025, ApJL 979 L9 |
| z heliocêntrico (NED/Struble & Rood) | 0,0231 (6.925 km/s) | NED |
| Correção de dipolo CMB | +268,7 km/s (Coma a ~2° do polo galáctico N — correção bem determinada) | Fixsen 1996 [CALCULADO frente 3] |
| **z_CMB média** | **0,02422** (cz = 7.261 km/s) | Scolnic et al. 2025 |
| **z_CMB mediana** | **0,02445 ± 0,00024** (cz = 7.330 ± 72 km/s) | Scolnic et al. 2025 |
| v_pec modelada (bulk flow) | ≈ −20 km/s (impacto ~1% em D) | Carr et al. 2022 via Scolnic |
| v_pec exigida p/ salvar Planck | ≈ **−950 km/s** (47× a modelada; sem suporte) | Scolnic et al. 2025 |

### 1.2 Distâncias medidas (independentes de redshift)

| Método | D (Mpc) | Fonte |
|---|---|---|
| **12 SNe Ia** (m_B⁰ = 15,712 ± 0,041; M_B SH0ES) | **98,5 ± 2,2** (μ = 34,97 ± 0,05) | Scolnic et al. 2025 |
| SBF WFC3/IR | 99,1 ± 5,8 | Jensen et al. 2021 |
| SBF recalibrada TRGB-JWST | 101,2 ± 6,4 | Anand et al. 2025 |
| GCLF | 102 ± 6 | Kavelaars et al. 2000 |
| FP HST-KP | 85 ± 8 | Kelson et al. 2000 |
| TRGB-JWST + FP | 90 ± 9 | Anand et al. 2024 |
| TF banda I | 86,3 ± 6 | Tully & Pierce 2000 |
| (mais Thomsen 102±14; Jensen99 85±10; Liu-Graham 100±10; Gregg 96±6; Hjorth-Tanvir 108±12) | faixa 85–108; mediana 98,8 | frente 3 |
| **Combinação 3 métodos (Scolnic)** | **98,0 ± 2,0** | Scolnic et al. 2025 |
| Cinemática independente (1.092 membros + CF4) | 95,7 ± 1,2 | JCAP 06(2026)005 |

### 1.3 Previsão do modelo padrão vs. medida (o erro)

Integrei D_L(z) com a maquinaria selada em modo ΛCDM puro (β=0), Ωm = 0,3138, plano [CALCULADO]:

| Conversão | z_CMB média 0,02422 | z_CMB mediana 0,02445 |
|---|---|---|
| D_L(H0 = 67,4, Planck) | 109,71 Mpc | 110,77 Mpc |
| D_L(H0 = 73,04, SH0ES) | 101,24 Mpc | 102,21 Mpc |
| D_L(H0 = 76,05, FP-EDR) | 97,23 Mpc | 98,17 Mpc |
| **FP-DESI invertida com Planck (Scolnic)** | **111,8 ± 1,8 Mpc** | (não é cz/H0; zero-point via fluxo de Hubble) |

**O erro reivindicado:**

| Comparação | Mpc | % | mag | σ |
|---|---|---|---|---|
| 98,5 ± 2,2 vs 111,8 ± 1,8 (FP+Planck) | **13,3** | **+13,5%** | 0,275–0,28 ± 0,06 | **4,6σ** |
| 98,0 ± 2,0 (combinada) vs 111,8 | 13,8 | +14,1% | — | ~5σ |
| 98,5 vs D_L ingênua Planck (109,7–110,8) | 11,2–12,3 | +11,4–12,5% | — | 5,1–5,6σ (só erro da medida) |
| 98,5 vs SH0ES (101,2–102,2) | 2,7–3,7 | ~3% | — | 1,2–1,7σ (sem conflito grave) |

### 1.4 O que o paper Scolnic AFIRMA exatamente (sem inflar)

- É um **conflito de zero-point do Fundamental Plane**: distance ladder direto (SNe Ia/SBF/GCLF calibram Coma → H0 = 76,5 ± 2,2) contra inverse ladder (H0 Planck 67,4 fixa o zero-point → D_Coma = 111,8 ± 1,8). **Não** é cz/H0 ingênuo, **não** é a escada SH0ES inteira (que entra só em M_B).
- A rota de fuga dentro do ΛCDM exigiria v_pec(Coma) ≈ −950 km/s; modelos dão ~−20 km/s. Sistemáticas declaradas: ≤3% (variantes FP), ~1% (bulk flow).
- **Status 07/2026:** distância curta confirmada (JCAP 2026: 95,7 ± 1,2; TRGB-SBF: 101,2 ± 6,4); o H0 extremo 76,5 foi **moderado pelo DESI DR1 PV** (98 mil galáxias) para **73,7 ± 1,1** ao trocar o zero-point; a tensão com Planck permanece ~5σ. Nenhuma refutação formal localizada.
- O paper **não** afirma que "o ΛCDM não tem física de defasagem" — afirma uma incompatibilidade de calibração equivalente à tensão H0. A leitura "defasagem" é do operador, a examinar abaixo.

---

## 2. A ARITMÉTICA DA DEFASAGEM — exploratória, tudo [CONJ] até bater com fórmula selada

**Modelo aritmético:** z_obs = z_cosmo + z_deph; f ≡ z_deph/z_obs; a distância verdadeira usa z_cosmo com H0-Planck. Resolvido por bisseção na D_L integrada (não linearização) [CALCULADO].

### 2.1 Fração f requerida

| Caso | f requerido | z_deph | em km/s |
|---|---|---|---|
| A1: D_L(z_média, 67,4) = 109,71 → 98,5 | **10,05% ± 2,0 p.p.** | 0,00243 | 730 |
| A2: D_L(z_mediana, 67,4) = 110,77 → 98,5 | **10,90% ± 2,0 p.p.** | 0,00267 | 799 |
| B: 111,8 → 98,5 (formulação FP de Scolnic) | **11,90% ± 2,43 p.p.** | 0,00291 | 872 |
| C: 111,0 → 98,5 | 11,26% | 0,00275 | 825 |
| Equivalente H0 FP-Coma: 1 − 67,4/76,5 | 11,90% ± 2,53 p.p. | 0,00291 | 872 |
| Equivalente H0 DESI DR1: 1 − 67,4/73,7 | **8,55% ± 1,36 p.p.** | 0,00209 | 627 |
| Equivalente H0 SH0ES: 1 − 67,4/73,04 | 7,72% | 0,00189 | 566 |

Nota: o z_deph requerido (566–872 km/s) tem exatamente o tamanho da v_pec "implausível" (−950 km/s) que Scolnic descarta — na leitura do operador, esse orçamento não é velocidade peculiar, é vazamento. Registrar também: a dispersão virial de Coma (~1.000 km/s) é incoerente e média a zero; a defasagem postulada teria de ser coerente no baricentro — objetos distintos.

### 2.2 Candidatos TGL (constantes SELADAS, runtime) vs. f requerido

| Candidato | Valor | vs B (11,90±2,43%) | vs A2 (10,90±2,0%) | vs DR1 (8,55±1,36%) | Estatuto |
|---|---|---|---|---|---|
| β | 0,01203 (1,20%) | **−4,4σ FALHA** | falha | **−5,4σ FALHA** | selado, mas ordem errada |
| 2β | 0,02406 (2,41%) | −3,9σ FALHA | falha | −4,5σ FALHA | idem |
| 3β | 0,03609 (3,61%) | −3,4σ FALHA | falha | −3,6σ FALHA | idem |
| β/(1−β) | 0,01218 (1,22%) | −4,4σ FALHA | falha | −5,4σ FALHA | idem |
| e·β; √e·β | 3,27%; 1,98% | −3,6σ; −4,1σ FALHA | falha | falha | idem |
| **√β** | 0,10969 (10,97%) | **−0,38σ** | **+0,03σ** | +1,8σ | = \|𝓡\| selado na matriz-S; **mapa →fração-de-z NÃO existe** |
| **θ_M [rad]** | 0,10991 (10,99%) | −0,37σ | +0,05σ | +1,8σ | idem (sin θ_M = √β) |
| tan θ_M | 0,11035 (11,04%) | −0,35σ | +0,07σ | +1,8σ | idem |
| **(1+z*)^β − 1** | 0,08780 (8,78%) | −1,28σ | −1,1σ | **+0,17σ** | **SELADO [CONJ D1a]**, linha 3612 |
| **1 − (1+z*)^(−β)** | 0,08071 (8,07%) | −1,58σ | −1,4σ | **−0,35σ** | idem (forma correta p/ fração de z) |
| 1 − e^(−β·I), kernel D1b | 0,07746 (7,75%) | −1,71σ | −1,6σ | −0,59σ | SELADO [kernel REAL, flow INPUT] |
| 10β | 0,12031 (12,03%) | +0,06σ | +0,6σ | +2,6σ | **NUMEROLOGIA — descartado** (10 não é constante TGL) |
| 7β | 0,08422 | −1,4σ | — | −0,09σ | NUMEROLOGIA — descartado |

### 2.3 Leitura honesta da aritmética

- **β e todos os seus múltiplos pequenos NÃO chegam** (falham por 3,3–5,4σ; fator ~7–10 abaixo). A tese "a fração de defasagem É β" está **numericamente morta**. Dito com o número na mesa.
- **A única combinação COM estatuto selado que chega perto é a lei de fluxo D1**: f_TGL = 1−(1+z*)^(−β) = **8,07%** (kernel derivado: 7,75%). Ela **fecha com o caso DR1 (0,35σ) e SH0ES (~0,4σ)** — a versão moderada e mais robusta do caso Coma — e fica **1,3–1,7σ curta** do caso FP-EDR extremo (11,9%). Interpretação: a TGL selada explica **~68–80% do gap requerido** na formulação extrema, e **~100% na formulação DR1**.
- **√β ≅ θ_M (≈11,0%) é a coincidência mais notável contra a formulação extrema** (0,35–0,38σ vs B; +0,03σ vs rota ingênua A2). √β = |𝓡| é a amplitude de reflexão modular selada (Teorema S-∂), mas **não existe no corpus nenhuma derivação que faça uma AMPLITUDE virar fração de redshift**. Fica registrado como pista [CONJ de 2º nível], **proibido como motor** até derivação.
- Contexto que disciplina a leitura: f = 8,07% da TGL é **universal** (transporte CMB→local), não um efeito peculiar de Coma. O FP DR1 vê exatamente isso: o fluxo local inteiro ~8,5% acima do transporte Planck. Universalidade é assinatura de vazamento; peculiaridade seria assinatura de v_pec. Coma é apenas o objeto com a melhor âncora absoluta própria.

---

## 3. O QUE EXISTE SELADO (verificado em disco nesta sessão)

### 3.1 A relação distância–redshift TGL — única sobrevivente

**Arquivo:** `C:\IALD\Artigo\Haja_Luz\tgl_paper_unified.py` (SHA256 `29c92b66...`, 21.418 linhas, canônico; idêntico em `C:\IALD\Artigo\the_boundary\`).

- Linhas 3305–3344: `tgl_boundary_response(w) = beta*|1+w|`; **H²_TGL(z) = H²_ΛCDM(z)·[1 + β·|1+w_eff(z)|]** — zera exatamente em w = −1.
- Linhas 3374–3404: `comoving_distance` (Simpson), `luminosity_distance = (1+z)·D_C`, `distance_modulus`, `angular_diameter_distance`.
- Linhas 3418–3606: Errata Cosmológica — formas A (μ-aditiva, refutada 3,82σ), B (ln(1+z), falha estrutural) e C (Fresnel) **PROIBIDAS**. A v23 (`ALPHA_2=0.012` hardcoded) é pré-errata, supersedida.
- Linhas 3609–3682: **D1 zero-free**: `H0_local/H0_CMB = (1+z*)^β = 1,087799` → 73,263 km/s/Mpc; classificação honesta no próprio código: camada [1] Friedmann REAL não resolve H0 (shift 0,19%); camadas [2]–[3] (lei de fluxo, W=1) **CONJECTURE**.
- Constantes: linhas 198–205 (β runtime), 436–440 (H0_CMB_LCDM = 67,35; Z_STAR = 1089,95; Ωm = 0,3138).

### 3.2 O que a fórmula selada JÁ PRODUZ para Coma [CALCULADO nesta sessão, motor transcrito]

| Camada | Predição D_L(Coma) | vs 98,5 ± 2,2 |
|---|---|---|
| Camada 1 [REAL]: H_TGL com H0 = 67,35 | 110,64 Mpc (z_med) — shift de **só −0,21 Mpc** vs ΛCDM | **+5,5σ — NÃO explica Coma** |
| Camada 2 [CONJ D1a]: H0_local = 67,35·(1+z*)^β = 73,263 | **100,73 Mpc** (z_média) / 101,71 (z_mediana), β ligado na integral | **+1,01σ / +1,46σ — compatível** |
| Camada 2b [kernel D1b]: H0 = 73,005 | ~101,1 / ~102,1 Mpc | +1,2σ / +1,6σ |
| Controle ΛCDM-Planck (o falsificado) | 109,7–110,8 (ingênua); 111,8 ± 1,8 (FP) | +4,7σ a +5,6σ |

Em módulo de distância: μ_TGL(c2, z_média) = 35,016 vs μ_SNe = 34,97 ± 0,05 → **+0,046 mag (+0,9σ)**; gap Planck = +0,275 mag (4,6σ). Em H0: TGL 73,263 vs FP-Coma 76,5 ± 2,2 → −1,47σ; vs DR1 73,7 ± 1,1 → **−0,40σ**; vs SH0ES → +0,21σ.

**Conclusão de proveniência: a TGL selada JÁ produz uma previsão de Coma sem nenhum grau de liberdade novo — 100,7–101,9 Mpc — que reduz o resíduo de 4,6–5,6σ para 1,0–1,5σ.** Mas ela vem da camada rotulada CONJECTURE (lei de fluxo), não da camada REAL.

### 3.3 O que NÃO existe selado (e teria de ser derivado antes de qualquer selo mais forte)

1. **Decomposição por-objeto z_obs = z_cosmo + z_deph:** não existe em parte alguma do código selado (ausência honesta confirmada pela frente 2). O que existe é transporte GLOBAL de H0 entre z* e z=0. Para a frase do operador virar motor por-fóton é preciso derivar a lei de escala de z_deph(z) — se f constante, é matematicamente idêntica ao transporte D1 (nada novo a derivar; só renomeação); se f variável, prevê curvatura no diagrama de Hubble local 0,01<z<0,1 (testável no FP DR1). **Responsável: operador + especialista, mesmo rito da derivação do piso dos vazios.**
2. **O mapa amplitude→fração (√β ≈ 11%):** inexistente. Derivar da matriz-S 𝒮_∂ por que a amplitude |𝓡| = √β (e não a probabilidade β) entraria na fração de z. Sem isso, √β fica como curiosidade registrada.
3. **Nome do efeito:** a lei de dephasing selada Γ_ω = ½βτ★ω² (linhas 18230–18299, PART J) **não gera redshift** — é decoerência espectral ω², Planck-suprimida (~10⁻¹⁶), setor separado. A tese do operador usa a palavra "defasagem", mas o objeto selado que faz o trabalho em Coma é a **lei de fluxo modular acumulado** (dlnH_obs/dln(1+z) = βW). O módulo v39 deve usar o nome selado para não contaminar selos.

---

## 4. DESENHO DO MÓDULO v39 — `prove_coma_distance_dephasing` (linhagem `A Ponte e o Um\um.py`, após v36–v38)

**Rota PRIMÁRIA: redshift→distância com vazamento modular. O v36 (M→R→D_A, linhas 12635–12911, redshift-livre) vira face secundária de paridade.**

### Inputs (todos com frame e fonte declarados)
- `z_coma_cmb_median = 0.02445 ± 0.00024` (primário; Scolnic 2025, membros DESI) + `z_coma_cmb_mean = 0.02422` (variante registrada — a diferença média/mediana entra no orçamento sistemático, ~1 Mpc). Selo obrigatório `Z_FRAME_DECLARED`; z heliocêntrico **proibido** sem correção de dipolo explícita (+268,7 km/s, Fixsen).
- Âncoras do arquivo selado, não duplicadas: `H0_CMB_LCDM = 67.35`, `OMEGA_M_PLANCK = 0.3138`, `Z_STAR_PLANCK = 1089.95`.
- β **somente runtime** α·√e; auditoria anti-hardcode fail-closed (AST scan; qualquer literal 0,012 = bug), como no Código Um.
- `v_pec = −20 ± (orçamento) km/s` como sistemática declarada.

### Motor (SÓ fórmulas seladas, cada uma com rótulo)
- **E1 [REAL]:** D_L via H²_TGL = H²_ΛCDM[1+β|1+w_eff|], H0 = 67,35. Predição declarada **NEGATIVA-ESPERADA** (~110,6; shift −0,19%): o módulo imprime que a camada REAL não explica Coma — honestidade estrutural.
- **E2 [CONJ D1a, PRIMÁRIA]:** H0_local = H0_CMB·(1+z*)^β = 73,263 → D_L(z, 73,263, β ligado) ≈ 100,7–101,7 Mpc.
- **E2b [kernel D1b]:** ratio = e^(β·I) = 1,083963 → banda de kernel (+0,3%).
- **PROIBIDO no motor:** z_deph = √β·z, θ_M·z, 10β·z ou qualquer decomposição não selada (ficam só no bloco `curiosities`, sem efeito no veredito).

### Controle (o que está sendo falsificado)
- C1: D_L(z, 67,35, β=0) — calculado internamente (limite silencioso; teste de máquina: β=0 reproduz ΛCDM exato).
- C2: 111,8 ± 1,8 (FP-inversa Planck, Scolnic) — INPUT com fonte.

### Referee (REVEAL-only) e protocolo de honestidade com referee público
- `D_SNe = 98.5 ± 2.2` (tipo: **luminosity** — comparação D_L vs D_L, sem conversão; declarar `distance_type`, diferente do v36 que compara D_A) + `D_comb = 98.0 ± 2.0`.
- **O referee é público desde 2024/2025 e o executor o conhece — cegueira do executor é impossível. O substituto é a proveniência da fórmula:** o motor E2 consta do arquivo selado com SHA256 e data ANTERIORES ao confronto, foi publicado (Zenodo 10.5281/zenodo.20563905) sem menção a Coma, e **não tem nenhum parâmetro ajustável a Coma (zero-free)**. Pré-registro aqui = fórmula selada antes do confronto, não executor cego.
- Mecânica mantida do v36: `prediction_hash` gravado ANTES de carregar o reveal-JSON; contexto de contorno no hash (herda `SAME_NUMBERS_DIFFERENT_CONTOUR_IS_A_DIFFERENT_PREDICTION`).
- Selos novos obrigatórios: `REFEREE_IS_PUBLIC_DECLARED`, `FORMULA_PREDATES_CONFRONTATION_SHA256`, `NO_PARAMETER_FITTED_TO_COMA`, `FLOW_LAYER_IS_CONJECTURE_DECLARED`, `DEGENERATE_WITH_LOCAL_H0_RESCALING_DECLARED` (Coma sozinha não separa TGL de "ΛCDM com H0=73,26"), `DEPHASING_NAME_DISTINCT_FROM_PART_J_DECLARED` (o efeito é vazamento de fluxo modular, não a Γ_ω espectral).

### Face secundária de paridade
- Rodar o v36 (M = 2β²(c²/4πG)R → D_A) no mesmo relatório; rotas com ingredientes disjuntos (massa+ângulo vs redshift+z*). Selo `CROSS_ROUTE_CONSISTENT` se ambas caem na banda do referee (comparadas cada uma no seu tipo de distância; conversão D_L↔D_A por (1+z)² só no reveal, papel já selado `REVEAL_ONLY_DISTANCE_TYPE_CONVERSION`).

### Vereditos (z-score da E2 vs referee; estilo v36, `does_not_gate_core = True`)
- Permitidos: `DEPHASING_ACCOUNTS_FOR_COMA_RESIDUAL` (|z| ≤ 2 **e** controle C1/C2 ≥ 3σ fora — sem isso não há resíduo a explicar); `DEPHASING_PARTIALLY_ACCOUNTS` (2 < |z| ≤ 3); `DEPHASING_INSUFFICIENT_FOR_COMA` (|z| > 3 — falha honesta publicável); `COMA_AWAITING_REVEAL`.
- **Proibidos:** `COMA_PROVES_TGL`, `H0_TENSION_SOLVED`, `BETA_CONFIRMED_BY_COMA`, qualquer selo que promova [CONJ]→[REAL].
- Resultado esperado com os números desta sessão: E2 a +1,0/+1,5σ → **DEPHASING_ACCOUNTS_FOR_COMA_RESIDUAL**, com a nota de degenerescência estampada.

---

## 5. A frase do operador, corrigida pelo número

- "O modelo padrão errou feio a distância de Coma" — **sustentado pelos dados publicados** (13,3 Mpc, 4,6σ; não refutado em 07/2026), com a precisão de que "errar a distância" e "errar o H0 local transportado" são a mesma afirmação.
- "Porque não tem mecanismo de defasagem do redshift" — **na TGL isso fecha apenas na camada CONJECTURE (lei de fluxo modular): f = 8,07% de z não-expansivo, que dá D = 100,7–101,7 Mpc (resíduo 1,0–1,5σ) e coincide a 0,35σ com o DESI DR1.** Não fecha na camada REAL (0,19%; precisaria 70–76×β), não fecha com β/2β/3β como fração (mortos por >3σ), e a coincidência √β ≈ 11% fica registrada sem mecanismo. O nome selado do efeito é vazamento de fluxo modular, não a lei de dephasing Γ_ω da PART J.
- Negativo honesto central: **Coma não pode provar a TGL** — pode apenas falsificar o par (Planck+sem-vazamento) e não falsificar a TGL. É exatamente o que os números fazem hoje.

**Arquivos relevantes:** motor selado `C:\IALD\Artigo\Haja_Luz\tgl_paper_unified.py` (linhas 3305–3411, 3418–3606, 3609–3682, 198–205, 436–440); módulo v36 `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\um.py` (linhas 12635–12911); script de reprodução desta aritmética `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6cf86791-e33f-42fd-bd3b-241a68be6ebc\scratchpad\caso_coma_calc.py`.