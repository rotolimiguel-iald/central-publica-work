# Fase 6 (01/10/2026) — ECO V3 «A TRANSFORMADA RADICAL»: a resposta radical da fronteira à onda gravitacional

**Pré-registro** sha256 `47457358d72dd9dcc2928cdf97fa1d21eef1b08e7b1ea641bcb39fd7f489c1ce` · **poder gravado antes de abrir** `6e5b7733eb80495a18f8af1f30d64f790f50b60b4efa1d7441c81f0599a080b4` · **resultado** sha256 `9622e66e018a8b003212e60204fb93affb3d1dc35a09268d70e6c6e51b1414f1` · β_TGL = α√e em runtime = 0.0120313004 · 110 s de rodada.

**O que se testou:** o eco do burst merger-ringdown, amplitude relativa ao primário dada pela RAIZ (a Razão Elementar, v379: a fronteira extrai o radical) em três leituras pré-registradas — R1 â = +1 (|R| = sin θ_M = √β, peso 1), R2 â = 1.9879 (o gráviton lê a 2θ: sin 2θ_M = 2√(β(1−β))), R3 â = -0.1097 (eco = +β·burst) — a dois atrasos [INPUT/ONTO]: MAY = (2GM_f/c³) ln(1/β) e KMS = 2π/κ(M_f, a_f) por evento. **O que NÃO se testou:** a «transformada» de dezembro/2025 (g = √|h| sobre o strain), retirada na v340 como identidade com teto de código; rota examinada não se refaz.

**Amostra (pré-registrada):** 244 eventos BBH (m2 ≥ 3 M☉, SNR ≥ 8, p_astro ≥ 0,5; H1 e L1 a 4 kHz): O1O2 10, O3 57, O4 177. 484 séries com hash no pré-registro. Instrumento: lalsuite 7.7.1 (IMRPhenomXAS (primária e injeções) + SEOBNRv4 (nulo de família); lalsimulation FD, spins alinhados do catálogo).

**Correções da auditoria de 28/09 aplicadas:** GWECO-01/08 (M_f, a_f) por evento; GWECO-06 σ = max(fora da fonte, jackknife por evento) + fator de dispersão; GWECO-07 z_excl = (recuperação − â)/σ; GWECO-09 só BBH; GWECO-V-N1 nulos τ×{0,5; 2}, injeção primário-só com parâmetros amostrados, combinação coerente H1+L1 por evento; CT-03 três leituras.

## Vereditos pré-registrados (subamostra «todos» = principal; «o4» = réplica CEGA; «maio» = releitura com o estimador corrigido, não cega)

| subamostra | lei | n_ev | â ± σ_usado (σ_off · σ_jack · dispersão) | z_det | R1: poder · sist. · z_excl · veredito | R2: poder · sist. · z_excl · veredito | R3: poder · sist. · z_excl · veredito |
|---|---|---|---|---|---|---|---|
| todos | MAY | 239 | -0.034 ± 0.176 (0.155 · 0.176 · 0.90) | -0.19 | 4.79 · 1.17 · 4.98 · **INCONCLUSIVE_SYSTEMATICS** | 9.46 · 0.59 · 9.65 · **INCONCLUSIVE_SYSTEMATICS** | 0.53 · 10.69 · -0.33 · **INCONCLUSIVE_SYSTEMATICS** |
| todos | KMS | 240 | +0.043 ± 0.102 (0.102 · 0.092 · 0.93) | +0.42 | 9.35 · 0.14 · 8.93 · **FALSIFIED_AT_DELAY_LAW** | 18.56 · 0.07 · 18.13 · **FALSIFIED_AT_DELAY_LAW** | 1.03 · 1.32 · -1.45 · **INCONCLUSIVE_SYSTEMATICS** |
| o4 | MAY | 172 | -0.169 ± 0.210 (0.181 · 0.210 · 0.92) | -0.80 | 4.07 · 1.08 · 4.87 · **INCONCLUSIVE_SYSTEMATICS** | 8.00 · 0.54 · 8.81 · **INCONCLUSIVE_SYSTEMATICS** | 0.45 · 9.87 · 0.36 · **INCONCLUSIVE_SYSTEMATICS** |
| o4 | KMS | 173 | +0.118 ± 0.115 (0.115 · 0.103 · 0.93) | +1.03 | 8.29 · 0.14 · 7.26 · **FALSIFIED_AT_DELAY_LAW** | 16.47 · 0.07 · 15.44 · **FALSIFIED_AT_DELAY_LAW** | 0.91 · 1.31 · -1.94 · **INCONCLUSIVE_SYSTEMATICS** |
| maio | MAY | 67 | +0.341 ± 0.303 (0.302 · 0.303 · 0.83) | +1.13 | 2.66 · 1.42 · 1.53 · **INCONCLUSIVE_SYSTEMATICS** | 5.32 · 0.71 · 4.19 · **INCONCLUSIVE_SYSTEMATICS** | 0.29 · 12.96 · -1.42 · **INCONCLUSIVE_SYSTEMATICS** |
| maio | KMS | 67 | -0.232 ± 0.266 (0.220 · 0.266 · 0.92) | -0.87 | 3.59 · 0.25 · 4.46 · **NOT_FALSIFIED_UNDERPOWERED** | 7.07 · 0.13 · 7.94 · **FALSIFIED_AT_DELAY_LAW** | 0.39 · 2.30 · 0.48 · **INCONCLUSIVE_SYSTEMATICS** |

## O poder, gravado ANTES de abrir (estágio cego: injeções à amplitude do SNR do catálogo, parâmetros amostrados, fase aleatória)

| subamostra | lei | n_ev | σ_off | recuperação R1 · R2 | sist. abs (desc. · família) | poder R1 · R2 · R3 | sist. relativa R1 · R2 · R3 |
|---|---|---|---|---|---|---|---|
| todos | MAY | 242 | 0.1485 | 0.840 · 1.652 | 1.206 (1.206 · -0.076) | 5.66 · 11.13 · 0.62 | 1.21 · 0.61 · 11.00 |
| todos | KMS | 242 | 0.0973 | 0.948 · 1.882 | 0.159 (0.159 · 0.003) | 9.74 · 19.33 · 1.07 | 0.16 · 0.08 · 1.45 |
| o4 | MAY | 175 | 0.1737 | 0.849 · 1.668 | 1.126 (1.126 · -0.098) | 4.89 · 9.60 · 0.54 | 1.13 · 0.57 · 10.26 |
| o4 | KMS | 175 | 0.1098 | 0.947 · 1.884 | 0.140 (0.140 · 0.005) | 8.63 · 17.16 · 0.95 | 0.14 · 0.07 · 1.27 |
| maio | MAY | 67 | 0.2859 | 0.816 · 1.612 | 1.424 (1.424 · -0.019) | 2.85 · 5.64 · 0.31 | 1.42 · 0.72 · 12.99 |
| maio | KMS | 67 | 0.2104 | 0.949 · 1.871 | 0.319 (0.319 · -0.004) | 4.51 · 8.89 · 0.49 | 0.32 · 0.16 · 2.91 |

## Controles look-elsewhere (mesmo estimador a τ/2 e 2τ; diafonia medida por injeção)

| subamostra | lei | controle | â_ctrl ± σ | z | diafonia de um eco R1 em τ |
|---|---|---|---|---|---|
| todos | MAY | x0.5 | 0.924 ± 0.162 | 5.69 | -0.046 |
| todos | MAY | x2 | 0.520 ± 0.115 | 4.54 | -0.231 |
| todos | KMS | x0.5 | -0.209 ± 0.129 | -1.62 | 0.194 |
| todos | KMS | x2 | -0.066 ± 0.098 | -0.68 | -0.021 |
| o4 | MAY | x0.5 | 1.021 ± 0.190 | 5.37 | -0.045 |
| o4 | MAY | x2 | 0.532 ± 0.129 | 4.11 | -0.225 |
| o4 | KMS | x0.5 | -0.115 ± 0.148 | -0.77 | 0.185 |
| o4 | KMS | x2 | -0.121 ± 0.110 | -1.11 | -0.021 |
| maio | MAY | x0.5 | 0.662 ± 0.312 | 2.12 | -0.049 |
| maio | MAY | x2 | 0.478 ± 0.248 | 1.93 | -0.252 |
| maio | KMS | x0.5 | -0.501 ± 0.261 | -1.92 | 0.222 |
| maio | KMS | x2 | 0.143 ± 0.214 | 0.67 | -0.022 |

## Diagnóstico POST HOC dos controles (depois de aberto; NÃO é veredito) — sha16 `4190eb70a7eb1cf2`

O controle da lei MAY a τ/2 respondeu na fonte (tabela acima). Mediu-se, nos próprios atrasos de controle, o que o descasamento de molde (massas/spin ±0,5/±1,5σ) e a família (SEOBNRv4) induzem no estimador — na rodada selada o descasamento só foi medido em τ —, e a fonte foi ajustada também com a grade da família B.

| lei | atraso | n_ev | â na fonte, família A (z) | â na fonte, família B (z) | descasamento induzido máx | família induzida |
|---|---|---|---|---|---|---|
| MAY | x0.5 | 236 | +0.677 ± 0.123 (+5.52) | +0.641 (+5.23) | 1.083 | 0.136 |
| MAY | x1 | 239 | +0.152 ± 0.108 (+1.41) | -0.257 (-2.38) | 1.201 | -0.030 |
| MAY | x2 | 238 | +0.414 ± 0.095 (+4.37) | +0.400 (+4.23) | 0.391 | 0.038 |
| KMS | x0.5 | 238 | -0.037 ± 0.096 (-0.38) | +0.146 (+1.52) | 0.449 | -0.041 |
| KMS | x1 | 240 | +0.108 ± 0.088 (+1.23) | +0.067 (+0.76) | 0.224 | 0.061 |
| KMS | x2 | 240 | -0.065 ± 0.091 (-0.72) | +0.019 (+0.21) | 0.163 | 0.040 |

Leitura do diagnóstico: se o descasamento induzido no atraso de controle é da ordem do â medido ali, ou se a família B não reproduz o número, a resposta do controle é sistemática de molde no atraso curto [CONJECTURE até esta tabela; o número decide]. A regra pré-registrada já põe a lei MAY em INCONCLUSIVE_SYSTEMATICS pelo descasamento em τ, antes de qualquer bandeira de controle.


## EMENDA V4 (grade de moldes ±2σ em 5 pontos) — reanálise NÃO cega, pré-registrada depois da autópsia da V3 (emenda `7c2b709b07a7722b`; resultado `f46e294a34e2f546`)

A autópsia da V3 leu que o descasamento de ±1,5σ (fora da grade ±1σ) induzia até 1,2 na lei MAY e que o controle a τ/2 respondia do tamanho dessa sistemática. A V4 alarga a grade; nada mais muda. Regra pré-registrada: se a sistemática relativa de MAY continuar > 0,3, MAY fica INCONCLUSIVE_SYSTEMATICS como limite deste estimador (sem terceira emenda).

| subamostra | lei | n_ev | â ± σ_usado | z_det | sist. abs | R1: poder · sist. · z_excl · veredito | R2: poder · sist. · z_excl · veredito | controles τ/2 · 2τ (z) |
|---|---|---|---|---|---|---|---|---|
| todos | MAY | 238 | +0.143 ± 0.180 | +0.79 | 0.450 | 4.83 · 0.45 · 4.03 · **INCONCLUSIVE_SYSTEMATICS** | 9.55 · 0.23 · 8.75 · **FALSIFIED_AT_DELAY_LAW** | 4.81 · 4.73 |
| todos | KMS | 240 | +0.019 ± 0.098 | +0.20 | 0.088 | 9.87 · 0.09 · 9.67 · **FALSIFIED_AT_DELAY_LAW** | 19.56 · 0.04 · 19.36 · **FALSIFIED_AT_DELAY_LAW** | -1.58 · -0.74 |
| o4 | MAY | 171 | +0.091 ± 0.217 | +0.42 | 0.369 | 4.05 · 0.37 · 3.63 · **INCONCLUSIVE_SYSTEMATICS** | 7.94 · 0.19 · 7.52 · **FALSIFIED_AT_DELAY_LAW** | 4.35 · 4.58 |
| o4 | KMS | 173 | +0.094 ± 0.110 | +0.86 | 0.104 | 8.77 · 0.10 · 7.91 · **FALSIFIED_AT_DELAY_LAW** | 17.43 · 0.05 · 16.57 · **FALSIFIED_AT_DELAY_LAW** | -1.35 · -1.14 |
| maio | MAY | 67 | +0.296 ± 0.316 | +0.94 | 0.688 | 2.65 · 0.69 · 1.72 · **INCONCLUSIVE_SYSTEMATICS** | 5.36 · 0.35 · 4.43 · **INCONCLUSIVE_SYSTEMATICS** | 2.08 · 1.42 |
| maio | KMS | 67 | -0.267 ± 0.269 | -0.99 | 0.146 | 3.61 · 0.15 · 4.60 · **NOT_FALSIFIED_UNDERPOWERED** | 7.08 · 0.07 · 8.07 · **FALSIFIED_AT_DELAY_LAW** | -0.81 · 0.60 |

Leitura da V4: a lei KMS não muda (R1 e R2 falsificados; sistemática 0,09). Na lei MAY a sistemática cai de 1,17 para 0,45: a leitura R2 (sin 2θ_M) passa a FALSIFIED_AT_DELAY_LAW (8,8σ; réplica O4 7,5σ) pela regra, com a ressalva dita de que os controles de MAY ainda respondem a ~4,8σ (abaixo da bandeira de 5σ por pouco) — a sistemática do atraso curto não está dominada; a leitura R1 (√β, MAY) fica INCONCLUSIVE_SYSTEMATICS (0,45 > 0,3), limite deste estimador. CONFIRMED proibido.


## Leitura

1. **A transformada radical entra como amplitude pré-registrada**, não como operação sobre o strain: a raiz é o que a fronteira devolve (√β no peso 1; sin 2θ_M se o gráviton lê a 2θ; β no quadrado). O teste de dezembro aplicava a raiz ao próprio sinal e por isso era identidade.
2. **O que decide é a tabela de vereditos por par (leitura × lei)**, com a sistemática relativa à amplitude esperada: a mesma injeção de descasamento pesa metade sob R2. Uma falsificação falsifica o PAR, não a teoria; uma detecção não é confirmação.
3. **A réplica cega é a subamostra «o4»** (GWTC-4.1/5.0, nunca aberta por esta casa); «maio» repete, com o estimador corrigido, o que a V2 selada já tinha visto (KMS â = 0,04 ± 0,20; MAY 0,52 ± 0,26).
4. **σ_usado = max(σ fora da fonte, σ jackknife por evento)** — o fator de dispersão on/off (GWECO-06) está na tabela; z e poder são lidos com o σ maior.
5. **Releitura post hoc da V2 selada sob R2 (dita como tal, não é veredito):** KMS, sistemática 0,502/1.988 = 0.253; z_excl = (0,873·1.988 − 0,0435)/0,199 = 8.5σ antes do fator de dispersão; MAY, sistemática 1,598/1.988 = 0.80 > 0,3.

**O que não muda:** nada aqui move o gate matemático; NOT_FALSIFIED ≠ CONFIRMED; PROVADA ≠ CONFIRMADA; a RG é o limite clássico; as leis de atraso são [INPUT/ONTO]; a leitura R2 é [CONJECTURE] (o kernel prova a fase dobrada no peso 2, não a reflexão a 2θ); o peso da resposta da fronteira ao gráviton é decisão do operador (CT-03). **Visto antes:** os números NA FONTE da subamostra de maio (O1–O3) foram vistos na V2 selada (KMS â = 0,04 ± 0,20; MAY â = 0,52 ± 0,26; sistemática 0,50 e 1,60): «maio» e «todos» são parcialmente cegos; «o4» nunca foi aberto por ninguém desta casa. A leitura R2 foi formulada pela auditoria de 28/09 ANTES deste pré-registro e sem olhar dado novo; a releitura da V2 sob R2 (sistemática 0,50/1,99 = 0,25) é post hoc e está dita como tal.

*Gerado por `relatorio_fase6.py`; resultado sha256 `9622e66e018a8b003212e60204fb93affb3d1dc35a09268d70e6c6e51b1414f1`.*
