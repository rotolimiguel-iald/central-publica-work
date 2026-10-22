# Fase 1 (30/09/2026) — H₀ e o D1 com o mapa de R EFETIVO ratificado: resultado

**Protocolo** `FASE1_EFF_20260930` · pré-registro sha256 `f0133c95a32d2dffa3d208fe6fc1374137e7880d50eb7d89b5b8105132e0238e` · confirmação do operador sha256 `8b39abe9ba748b8e601cd43ebced284938effb9b979c951e42b31caed52be4ca` · resultado sha256 `165e3715d8c5d58f5dc1748ce3d63672e8d2bd4fdf06ef17b1f9365f67f13ad4` · rodada 2026-09-30 09:06:29 → 2026-09-30 09:38:14 (431 s)

**β_TGL em runtime** = α_CODATA2018·√e = 0.012031300400803 (nunca literal). **Motor:** Bancada Um (GPU), modo `tgl` = corrigido (Chen+2019 cov 3×3; DR1 correlacionado; D_M(z*) por razão TGL/ΛCDM sobre o CAMB; neutrino contado uma vez) + mapa de R efetivo (1+β)Ω_m; controle `nu` = o mapa do D1 V3 selado.

## VEREDITO

`TGL_FASE1_EFF__BETA_CONSISTENT_WITHIN_1SIGMA__BAYES_INCONCLUSIVE__CONTROL_NU_Z_3P91__NOT_A_CONFIRMATION`

**Estatuto:** `[REAL — medido nesta rodada]`; NOT_FALSIFIED ≠ CONFIRMED; nada aqui confirma; a RG é o limite clássico (a correção é β contra σ).

**Regra de leitura pré-registrada:** o veredito principal vem da família A no modo tgl (z de perfil de β = α√e contra β livre): < 1σ consistente; 1–3σ tensão; > 3σ tensão forte; o sufixo de evidência vem de ln B(TGL/ΛCDM) em A; o controle nu é reportado ao lado e NUNCA somado; E é a leitura conjunta com o estatuto de que SH0ES e Pantheon não são independentes de H₀ (dito). Nada aqui confirma: NOT_FALSIFIED ≠ CONFIRMED; a RG é o limite clássico.

## Tabela 1 — χ², perfil de β e evidência bayesiana, por família e mapa

| família | mapa | n | χ² ΛCDM / TGL / livre | Δχ² T−L | Δχ² T−F | z perfil (α√e) | β̂ livre ± σ | ln B TGL/ΛCDM | ln B livre/ΛCDM | ln B TGL/livre | H₀ TGL |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A_planck_dr2 | **tgl (eff)** | 16 | 14.293 / 13.929 / 13.233 | -0.365 | +0.695 | **0.83** | +0.04995 ± 0.0617 ⚠limite | +0.20 (inconclusivo) | -0.02 | +0.22 (SD +0.24) | 69.20 |
| A_planck_dr2 | controle nu | 16 | 14.293 / 25.475 / 10.165 | +11.181 | +15.310 | **3.91** | -0.01280 ± 0.0062 | -5.56 (forte) | +0.18 | -5.75 (SD -5.30) | 69.06 |
| B_planck_dr1 | **tgl (eff)** | 15 | 16.286 / 15.888 / 14.845 | -0.399 | +1.042 | **1.02** | +0.04995 ± 0.0872 ⚠limite | +0.21 (inconclusivo) | -0.03 | +0.24 (SD -0.46) | 68.98 |
| B_planck_dr1 | controle nu | 15 | 16.286 / 24.616 / 12.829 | +8.330 | +11.787 | **3.43** | -0.01405 ± 0.0075 | -4.13 (moderado) | +0.02 | -4.16 (SD -3.94) | 68.51 |
| C_planck_dr2_sh0es | **tgl (eff)** | 17 | 31.627 / 26.478 / 15.814 | -5.149 | +10.664 | **3.27** | +0.04995 ± 0.0188 ⚠limite | +2.59 (moderado) | +5.33 | -2.74 (SD -2.72) | 69.51 |
| C_planck_dr2_sh0es | controle nu | 17 | 31.627 / 38.994 / 30.747 | +7.367 | +8.247 | **2.87** | -0.00578 ± 0.0061 | -3.66 (moderado) | -1.44 | -2.21 (SD -2.01) | 69.37 |
| D_planck_dr2_pantheon | **tgl (eff)** | 1596 | 1403.647 / 1403.868 / 1403.526 | +0.221 | +0.342 | **0.58** | -0.01763 ± 0.0487 | -0.10 (inconclusivo) | -0.16 | +0.06 (SD -0.33) | 69.08 |
| D_planck_dr2_pantheon | controle nu | 1596 | 1403.647 / 1414.641 / 1399.741 | +10.994 | +14.900 | **3.86** | -0.01243 ± 0.0062 | -5.47 (forte) | +0.07 | -5.54 (SD -5.11) | 68.95 |
| E_todos | **tgl (eff)** | 1597 | 1421.887 / 1417.256 / 1408.365 | -4.631 | +8.891 | **2.98** | +0.04995 ± 0.0186 ⚠limite | +2.33 (fraco) | +4.44 | -2.11 (SD -2.09) | 69.38 |
| E_todos | controle nu | 1597 | 1421.887 / 1428.939 / 1421.160 | +7.053 | +7.779 | **2.79** | -0.00524 ± 0.0061 | -3.50 (moderado) | -1.52 | -1.98 (SD -1.79) | 69.26 |

Δχ² T−L = χ²(TGL) − χ²(ΛCDM); Δχ² T−F = χ²(TGL) − χ²(β livre); z perfil = √max(Δχ² T−F, 0) (Wilks, 1 g.l.). ln Z por quadratura em grade (n = 25; erro por n = 35), priors uniformes nos limites do pipeline; SD = Savage–Dickey. «⚠limite» = o β livre encostou no limite do prior (a σ de JᵀJ não vale como intervalo).

## Tabela 2 — a lei D1a (dois setores de H₀): H₀_local = H₀_CMB·(1+z*)^β, z* = 1089,95 [INPUT]; lei [CONJECTURE]

| família (modo tgl) | H₀_CMB (melhor ajuste TGL) | H₀_local pela D1a | z vs SH0ES (D1a) | z vs SH0ES (H₀ direto, um setor) |
|---|---|---|---|---|
| A_planck_dr2 | 69.20 | 75.28 | +2.15 | -3.69 |
| E_todos | 69.38 | 75.47 | +2.34 | -3.52 |

SH0ES = 73.04 ± 1.04 (R22, como no pipeline selado).

## Tabela 3 — posteriores (modo tgl; ensemble afim-invariante na GPU, 256 × 3000, queima 600, semente 42)

| família | β mediana [16, 84] | H₀ mediana | fração ≥ α√e | fração ≥ 0 | z pela cauda | τ máx |
|---|---|---|---|---|---|---|
| A_planck_dr2 | +0.01763 [-0.01724, +0.04059] | 69.50 | 0.569 | 0.697 | 0.17 | 53 |
| E_todos | +0.04288 [+0.03323, +0.04808] | 70.89 | 0.995 | 1.000 | 2.58 | 47 |

## Leitura da gerência (condicionada às bandeiras calculadas pelo script)

1. **Veredito pré-registrado (família A, modo tgl):** `TGL_FASE1_EFF__BETA_CONSISTENT_WITHIN_1SIGMA__BAYES_INCONCLUSIVE__CONTROL_NU_Z_3P91__NOT_A_CONFIRMATION`. O ponto β = α√e fica a **0.83σ** do melhor ajuste com β livre (Δχ²(TGL − livre) = +0.695) e ln B(TGL/ΛCDM) = +0.20 (inconclusivo (|ln B| < 1)).
2. **O número corrige a frase — «consistente» aqui lê-se «não constrangido»:** no modo tgl o β livre **encostou no limite do prior** em A_planck_dr2, B_planck_dr1, C_planck_dr2_sh0es, E_todos, e σ_β (JᵀJ) é maior ou igual à meia-largura do prior em A_planck_dr2, B_planck_dr1. Sob o mapa efetivo, o fundo comprimido (Planck + BAO) sozinho **não mede β**: a direção de β é quase plana (degenerada com Ω_m h² e H₀). Logo A não está em tensão com α√e, mas também não o testa; a evidência é inconclusiva porque o dado não discrimina.
3. **O controle nu (o mapa do D1 V3 selado) reproduz a tensão de 28/09:** em A, β̂ = -0.01280 ± 0.0062, z de perfil 3.91σ, ln B(TGL/ΛCDM) = -5.56 (forte (|ln B| ≥ 5)). A tensão do D1 é **condicional ao mapa de R**, como a errata de 28/09 disse; o operador ratificou o efetivo em 30/09 (permanência é verbo). O controle fica AO LADO, nunca somado.
4. **Família C (SH0ES como prior direto sobre o H₀ de fundo — leitura de UM setor):** o β livre corre para +0.04995 (no limite do prior) e α√e fica a 3.27σ dele; ln B(TGL/ΛCDM) = +2.59 (moderado (2,5 ≤ |ln B| < 5)), mas ln B(TGL/livre) = -2.74 — a escada local pede, pelo mapa efetivo sozinho, **mais** que α√e dá. Isso não é o teste da TGL de dois setores: na TGL o H₀ da escada é o local, H₀_local = H₀_CMB·(1+z*)^β (lei D1a, [CONJECTURE]), e esse teste é a linha D1a abaixo.
5. **A lei D1a (dois setores) em A:** H₀_CMB(TGL) = 69.20 ⟹ H₀_local = 75.28 contra SH0ES 73.04 ± 1.04: **z = +2.15**; o H₀ direto (um setor) daria z = -3.69. A lei D1a deixa o setor local a 2.15σ: a reconciliação é parcial.
6. **Posterior de A (modo tgl, ensemble na GPU):** β mediana +0.01763 [-0.01724, +0.04059] (16–84); fração do posterior acima de α√e = 0.569; z pela cauda 0.17; τ máximo 53 (o posterior de um parâmetro quase plano é largo por construção).
7. **E (tudo; SH0ES e Pantheon+ não são independentes de H₀, dito):** z de perfil 2.98σ; ln B(TGL/ΛCDM) = +2.33 (fraco (1 ≤ |ln B| < 2,5)); ln B(TGL/livre) = -2.11. D1a em E: H₀_local = 75.47, z = +2.34.

## Estatuto, multiplicidade e pendências

- **Cego/não-cego:** A_planck_dr2: cego até esta rodada; B_planck_dr1: NÃO-CEGO; C_planck_dr2_sh0es: cego até esta rodada; D_planck_dr2_pantheon: cego até esta rodada; E_todos: cego até esta rodada.
- **Multiplicidade (livro da Bancada, Šidák sobre as famílias já testadas), família A modo tgl:** `{"p_local": 0.4043590694556555, "z_local": 0.8338614380738246, "n_familias": 18, "p_global": 0.9999109320202192, "z_global": 0.00011163015847326332, "metodo": "Šidák sobre as famílias de teste do livro"}`.
- **Pendência dita no pré-registro:** a identidade do arquivo de covariância do Pantheon+ contra o STAT+SYS oficial (razão mediana diag/err_DIAG² = 0,52): verificar por sha256 contra o DataRelease; o controle externo de Ω_m bateu
- **Pendência FECHADA (2026-09-30 09:16:29):** o arquivo local É byte-idêntico ao `Pantheon+SH0ES_STAT+SYS.cov` oficial — local sha256 `abf806d966485e64`, oficial sha256 `abf806d966485e64` (33284960 bytes). o arquivo local É o Pantheon+SH0ES_STAT+SYS.cov oficial (byte a byte). A razão mediana diag(C)/MU_SH0ES_ERR_DIAG² = 0,52 é propriedade do próprio release (a coluna ERR_DIAG é «para uso aproximado», não a diagonal de C), não defeito do arquivo. Pendência do pré-registro da Fase 1 FECHADA.
- **O que este resultado NÃO diz:** não confirma β; não resolve a tensão de Hubble; não move o gate matemático (cosmologia jamais vira prova matemática). O que diz: sob o mapa efetivo, o fundo comprimido não está em tensão com α√e porque não o mede; a tensão de 3–4σ do D1 pertence ao mapa nu.

## Próximo passo (a pré-registrar antes de abrir número)

- **Fase 2 — o modelo de DOIS setores na verossimilhança:** SH0ES como prior sobre H₀_local = H₀·(1+z*)^β (não sobre o H₀ de fundo), com Pantheon+ (cov completa, M profilado) e DR2; evidência ln B contra ΛCDM e contra β livre; o posterior conjunto. É o teste em que a TGL pode perder: se a D1a não fecha com SH0ES, o setor local falsifica a lei.
- **Fase 3 — quebrar a degenerescência de β no fundo:** o espectro completo do CMB (não comprimido) e o full-shape do DESI; só assim o fundo mede β sob o mapa efetivo.
- Registrar cada família no MAPA DE ROTAS (feito pelo runner: RESULTADO por família em `d1.fase1_eff_30set`).

---
*Gerado por `relatorio_fase1.py` em 2026-09-30 09:38:22 a partir de `RESULTADO_FASE1_EFF_20260930.json` (sha256 `165e3715d8c5d58f5dc1748ce3d63672e8d2bd4fdf06ef17b1f9365f67f13ad4`). Números lidos do JSON; nenhum digitado.*
