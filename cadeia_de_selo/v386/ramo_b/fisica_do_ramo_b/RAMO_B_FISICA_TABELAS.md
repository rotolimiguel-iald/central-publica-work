# A FISICA DO RAMO B — tabelas por script (05/10/2026)

β_TGL = α·√e lido do fonte (um.py `SEALED_CODATA_ALPHA`) em runtime = 0.0120313004008031 (core V2: 0.0120313004008031; diff rel 0.0e+00). t_Planck = 5.391125e-44 s. GM☉/c³ = 4.926533e-06 s.

Entradas por hash: um.py d406ae5725105145; ringdown_dephasing_v2.py 0793c58d6995194b; um_absoluto.json 475ac8d218b3a5c8; leaver_kerr_result.json b6e4d88c95243e46; C6_RESULTS_GW250114.json 781a3741a68875eb; RINGDOWN_DEPHASING_V2_RESULT.json ff15f023dd91d8c7

## (a)/(b) O numero puro N(χ) = F·Q = F²/(2F_I) do modo 220 (BCW 2006 lido do pipeline V2; Leaver lido por hash)

| χ_f | F=Mω_R (BCW) | F_I=M/τ (BCW) | Q (BCW) | N=F·Q (BCW) | N (Leaver) | erro N % | κ̂ | Ω̂_H | 2π/κ̂ | (F−2Ω̂_H)/F |
|---|---|---|---|---|---|---|---|---|---|---|
| 0.00 | 0.3683 | 0.08692 | 2.1187 | 0.7803 | 0.7848 | -0.57 | 0.25000 | 0.00000 | 25.13 | 1.000 |
| 0.50 | 0.4674 | 0.08640 | 2.7050 | 1.2643 | 1.2577 | +0.53 | 0.23205 | 0.13397 | 27.08 | 0.427 |
| 0.60 | 0.4975 | 0.08457 | 2.9411 | 1.4631 | 1.4569 | +0.42 | 0.22222 | 0.16667 | 28.27 | 0.330 |
| 0.65 | 0.5150 | 0.08319 | 3.0955 | 1.5943 | 1.5893 | +0.31 | 0.21590 | 0.18467 | 29.10 | 0.283 |
| 0.68 | 0.5267 | 0.08216 | 3.2051 | 1.6880 | 1.6841 | +0.23 | 0.21152 | 0.19617 | 29.71 | 0.255 |
| 0.69 | 0.5307 | 0.08178 | 3.2451 | 1.7223 | — | — | 0.20994 | 0.20014 | 29.93 | 0.246 |
| 0.70 | 0.5349 | 0.08137 | 3.2871 | 1.7584 | 1.7555 | +0.17 | 0.20831 | 0.20418 | 30.16 | 0.237 |
| 0.80 | 0.5855 | 0.07570 | 3.8672 | 2.2642 | 2.2704 | -0.27 | 0.18750 | 0.25000 | 33.51 | 0.146 |
| 0.90 | 0.6660 | 0.06433 | 5.1760 | 3.4471 | 3.4767 | -0.85 | 0.15178 | 0.31339 | 41.40 | 0.059 |
| 0.95 | 0.7396 | 0.05263 | 7.0256 | 5.1959 | 5.2399 | -0.84 | 0.11898 | 0.36197 | 52.81 | 0.021 |

Schwarzschild exato (Leaver): Mω_R = 0.37367, Mω_I = -0.08896 (1/τ = 0.0890 c³/GM), Q = 2.1002, N = 0.7848. Ajuste BCW em χ=0: F = 0.3683 (erro -1.44%, limite BCW 1,85%), Q = 2.1187 (erro +0.88%, limite BCW 0,88%); F_I = F/(2Q) combina os dois: 0.08692 (-2.30%); N = F·Q cancela parte: -0.57%.

## (b) δτ̂_220 = −x/(1+x), x = β·k·N(χ) por candidato a k (τ★ = k·GM_f/c³; M_X = M_f)

| χ_f | k (origem) | k | ω usado | N puro = x/β | x = Γτ | δ_lin | δ_exato |
|---|---|---|---|---|---|---|---|
| 0.00 | k=1 | 1.0000 | ω | 0.7803 | 0.00939 | -0.00939 | -0.00930 |
| 0.00 | k=2 | 2.0000 | ω | 1.5606 | 0.01878 | -0.01878 | -0.01843 |
| 0.00 | k=4 | 4.0000 | ω | 3.1213 | 0.03755 | -0.03755 | -0.03619 |
| 0.00 | k=8π | 25.1327 | ω | 19.6115 | 0.23595 | -0.23595 | -0.19091 |
| 0.00 | k=1/κ̂(χ) | 4.0000 | ω | 3.1213 | 0.03755 | -0.03755 | -0.03619 |
| 0.00 | k=2π/κ̂(χ) | 25.1327 | ω | 19.6115 | 0.23595 | -0.23595 | -0.19091 |
| 0.00 | k=2π/κ̂(χ) com co-rotacao ω→ω−2Ω_H | 25.1327 | ω−2Ω_H | 19.6115 | 0.23595 | -0.23595 | -0.19091 |
| 0.68 | k=1 | 1.0000 | ω | 1.6880 | 0.02031 | -0.02031 | -0.01990 |
| 0.68 | k=2 | 2.0000 | ω | 3.3759 | 0.04062 | -0.04062 | -0.03903 |
| 0.68 | k=4 | 4.0000 | ω | 6.7519 | 0.08123 | -0.08123 | -0.07513 |
| 0.68 | k=8π | 25.1327 | ω | 42.4234 | 0.51041 | -0.51041 | -0.33793 |
| 0.68 | k=1/κ̂(χ) | 4.7277 | ω | 7.9803 | 0.09601 | -0.09601 | -0.08760 |
| 0.68 | k=2π/κ̂(χ) | 29.7052 | ω | 50.1415 | 0.60327 | -0.60327 | -0.37627 |
| 0.68 | k=2π/κ̂(χ) com co-rotacao ω→ω−2Ω_H | 29.7052 | ω−2Ω_H | 3.2616 | 0.03924 | -0.03924 | -0.03776 |
| 0.69 | k=1 | 1.0000 | ω | 1.7223 | 0.02072 | -0.02072 | -0.02030 |
| 0.69 | k=2 | 2.0000 | ω | 3.4446 | 0.04144 | -0.04144 | -0.03979 |
| 0.69 | k=4 | 4.0000 | ω | 6.8892 | 0.08289 | -0.08289 | -0.07654 |
| 0.69 | k=8π | 25.1327 | ω | 43.2862 | 0.52079 | -0.52079 | -0.34245 |
| 0.69 | k=1/κ̂(χ) | 4.7632 | ω | 8.2036 | 0.09870 | -0.09870 | -0.08983 |
| 0.69 | k=2π/κ̂(χ) | 29.9278 | ω | 51.5448 | 0.62015 | -0.62015 | -0.38277 |
| 0.69 | k=2π/κ̂(χ) com co-rotacao ω→ω−2Ω_H | 29.9278 | ω−2Ω_H | 3.1147 | 0.03747 | -0.03747 | -0.03612 |
| 0.70 | k=1 | 1.0000 | ω | 1.7584 | 0.02116 | -0.02116 | -0.02072 |
| 0.70 | k=2 | 2.0000 | ω | 3.5168 | 0.04231 | -0.04231 | -0.04059 |
| 0.70 | k=4 | 4.0000 | ω | 7.0336 | 0.08462 | -0.08462 | -0.07802 |
| 0.70 | k=8π | 25.1327 | ω | 44.1935 | 0.53171 | -0.53171 | -0.34713 |
| 0.70 | k=1/κ̂(χ) | 4.8006 | ω | 8.4413 | 0.10156 | -0.10156 | -0.09220 |
| 0.70 | k=2π/κ̂(χ) | 30.1628 | ω | 53.0384 | 0.63812 | -0.63812 | -0.38954 |
| 0.70 | k=2π/κ̂(χ) com co-rotacao ω→ω−2Ω_H | 30.1628 | ω−2Ω_H | 2.9696 | 0.03573 | -0.03573 | -0.03450 |
| 0.90 | k=1 | 1.0000 | ω | 3.4471 | 0.04147 | -0.04147 | -0.03982 |
| 0.90 | k=2 | 2.0000 | ω | 6.8941 | 0.08295 | -0.08295 | -0.07659 |
| 0.90 | k=4 | 4.0000 | ω | 13.7883 | 0.16589 | -0.16589 | -0.14229 |
| 0.90 | k=8π | 25.1327 | ω | 86.6343 | 1.04232 | -1.04232 | -0.51036 |
| 0.90 | k=1/κ̂(χ) | 6.5883 | ω | 22.7104 | 0.27324 | -0.27324 | -0.21460 |
| 0.90 | k=2π/κ̂(χ) | 41.3956 | ω | 142.6935 | 1.71679 | -1.71679 | -0.63192 |
| 0.90 | k=2π/κ̂(χ) com co-rotacao ω→ω−2Ω_H | 41.3956 | ω−2Ω_H | 0.4939 | 0.00594 | -0.00594 | -0.00591 |

Convencao que reproduz o «−0,0194» do registro: **k = 1, M = M_f,det, δ_lin = −β·F·Q por serie** (GW250114-like χ=0,68: δ_lin = -0.02031, δ_exato = -0.01990; o −0,0194 selado e a media ponderada das 15 series da V2 com os seus spins). Reproducao por serie: n=169, max|diff| (20 primeiras) = 6.938893903907228e-18.

## (c) A identidade exata (a pergunta do operador em forma operacional)

- **lei**: Γ_ω = ½ β τ★ ω²  com  τ★ = k · G M_X / c³  (ramo B)  [lei: REAL na forma (dephasing_reach); τ★ do ramo B: INPUT]
- **observavel**: δτ̂_220 ≡ τ_obs/τ_RG − 1  com  1/τ_obs = 1/τ_RG + Γ  ⟹  δτ̂_220 = −x/(1+x),  x = Γ·τ_RG
- **x**: x = ½ β k (M_X/M_f) (M_f ω_c)² / (M_f ω_I) = β · k · (M_X/M_f) · N(χ_f),  N(χ) = F(χ)·Q(χ) = F²/(2F_I),  F = M_f ω_R, F_I = M_f ω_I = M_f/τ, Q = ω_R τ/2;  com co-rotacao F → F − 2Ω̂_H
- **leitura_de_beta**: β_lido = x / (k · (M_X/M_f) · N(χ_f))  com  x = −δτ̂/(1+δτ̂)  ⟹  a fracao medida e uma leitura de β dividida por um numero puro conhecido (so spin e k)
- **independencia_da_massa**: x NAO depende de M quando τ★ ∝ M_f (unidade geometrica): depende so de χ_f, de k e da razao M_X/M_f — por isso «qual M» so entra como fator M_X/M_f
- **sinal**: dephasing extra ⟹ 1/τ_obs > 1/τ_RG ⟹ τ_obs < τ_RG ⟹ δτ̂_220 < 0 (linha MAIS LARGA); os catalogos puxam δτ̂ > 0 (linha mais estreita) [KNOWN]
- **GW250114 (χ_f = 0,68)**: N = 1.6880 (BCW) / 1.6841 (Leaver); k=1: x = 0.02031, δ = -0.01990; k=8π: x = 0.5104, δ = -0.3379. Leitura de β: β_lido = −δτ̂/(1+δτ̂) / (k·N).

## (a) QUAL M — GW250114 [KNOWN]: M_f,src 62,7; M_f,det 68,1; m1+m2 = 65.8 (M_tot/M_f = 1.049); M_chirp = 28.6 (M_c/M_f = 0.457); 1+z = 1.09

## (d) GW250114 por k e M: δ previsto vs δτ̂_220 publicado = −0,01 (+0,10/−0,09) 90% [KNOWN]; σ₋ ≈ 0.0547, σ₊ ≈ 0.0608 (gauss. aprox.); leitura NAO-CEGA, sem veredito

| k | M_X | x | δ_exato (envoltoria, por realizacao) | z vs mediana | dentro do 90%? | δ_eff difusao de fase (×0,273 [DECLARADO RD-01]) | z_eff | σ p/ 5σ |
|---|---|---|---|---|---|---|---|---|
| k=1 | M_f,det | 0.0203 | -0.0199 | -0.18 | sim | -0.0054 | +0.08 | 0.0040 |
| k=1 | M_f,src | 0.0203 | -0.0199 | -0.18 | sim | -0.0054 | +0.08 | 0.0040 |
| k=1 | M_tot,src | 0.0213 | -0.0209 | -0.20 | sim | -0.0057 | +0.07 | 0.0042 |
| k=1 | M_chirp,src | 0.0093 | -0.0092 | +0.01 | sim | -0.0025 | +0.12 | 0.0018 |
| k=2 | M_f,det | 0.0406 | -0.0390 | -0.53 | sim | -0.0107 | -0.01 | 0.0078 |
| k=2 | M_f,src | 0.0406 | -0.0390 | -0.53 | sim | -0.0107 | -0.01 | 0.0078 |
| k=2 | M_tot,src | 0.0426 | -0.0409 | -0.56 | sim | -0.0112 | -0.02 | 0.0082 |
| k=2 | M_chirp,src | 0.0185 | -0.0182 | -0.15 | sim | -0.0050 | +0.08 | 0.0036 |
| k=4 | M_f,det | 0.0812 | -0.0751 | -1.19 | sim | -0.0205 | -0.19 | 0.0150 |
| k=4 | M_f,src | 0.0812 | -0.0751 | -1.19 | sim | -0.0205 | -0.19 | 0.0150 |
| k=4 | M_tot,src | 0.0853 | -0.0786 | -1.25 | sim | -0.0214 | -0.21 | 0.0157 |
| k=4 | M_chirp,src | 0.0371 | -0.0358 | -0.47 | sim | -0.0098 | +0.00 | 0.0072 |
| k=8π | M_f,det | 0.5104 | -0.3379 | -5.99 | NAO | -0.0923 | -1.50 | 0.0676 |
| k=8π | M_f,src | 0.5104 | -0.3379 | -5.99 | NAO | -0.0923 | -1.50 | 0.0676 |
| k=8π | M_tot,src | 0.5356 | -0.3488 | -6.19 | NAO | -0.0952 | -1.56 | 0.0698 |
| k=8π | M_chirp,src | 0.2331 | -0.1890 | -3.27 | NAO | -0.0516 | -0.76 | 0.0378 |
| k=1/κ̂(χ) | M_f,det | 0.0960 | -0.0876 | -1.42 | sim | -0.0239 | -0.25 | 0.0175 |
| k=1/κ̂(χ) | M_f,src | 0.0960 | -0.0876 | -1.42 | sim | -0.0239 | -0.25 | 0.0175 |
| k=1/κ̂(χ) | M_tot,src | 0.1008 | -0.0915 | -1.49 | sim | -0.0250 | -0.27 | 0.0183 |
| k=1/κ̂(χ) | M_chirp,src | 0.0438 | -0.0420 | -0.58 | sim | -0.0115 | -0.03 | 0.0084 |
| k=2π/κ̂(χ) | M_f,det | 0.6033 | -0.3763 | -6.69 | NAO | -0.1027 | -1.69 | 0.0753 |
| k=2π/κ̂(χ) | M_f,src | 0.6033 | -0.3763 | -6.69 | NAO | -0.1027 | -1.69 | 0.0753 |
| k=2π/κ̂(χ) | M_tot,src | 0.6331 | -0.3877 | -6.90 | NAO | -0.1058 | -1.75 | 0.0775 |
| k=2π/κ̂(χ) | M_chirp,src | 0.2755 | -0.2160 | -3.76 | NAO | -0.0590 | -0.89 | 0.0432 |
| k=2π/κ̂(χ) com co-rotacao ω→ω−2Ω_H co-rot | M_f,det | 0.0392 | -0.0378 | -0.51 | sim | -0.0103 | -0.01 | 0.0076 |
| k=2π/κ̂(χ) com co-rotacao ω→ω−2Ω_H co-rot | M_f,src | 0.0392 | -0.0378 | -0.51 | sim | -0.0103 | -0.01 | 0.0076 |
| k=2π/κ̂(χ) com co-rotacao ω→ω−2Ω_H co-rot | M_tot,src | 0.0412 | -0.0396 | -0.54 | sim | -0.0108 | -0.01 | 0.0079 |
| k=2π/κ̂(χ) com co-rotacao ω→ω−2Ω_H co-rot | M_chirp,src | 0.0179 | -0.0176 | -0.14 | sim | -0.0048 | +0.09 | 0.0035 |

**A familia unificada** τ★ = k·G·m_X/c³ ⟹ x = β·k·N(χ_f)·(m_X/M_f): m_X = m_P da' o ramo A (G·m_P/c³ = t_P, residuo 0.0e+00), m_X = M_f o ramo B. GW250114: m_P/M_f,det = 1.607e-40 ⟹ x_A(k=1) = 3.263e-42 (δ = -3.263e-42; V2 empilhada: -2.153e-42), x_A(k=8π) = 8.202e-41 — invisivel em qualquer k.


QNM de conferencia (BCW, M_f,det 68,1, χ 0,68): f_220 = 249.8 Hz, τ_220 = 4.083 ms, Q = 3.205 — pSEOB publica f = 251.7 Hz, τ = 4.09 ms [KNOWN].

Catalogos [KNOWN, lidos na casa]: GWTC-3 hier. δτ̂_220 = +0,13 (+0,21/−0,22); melhor evento isolado GW200129 = +0,11 ± 0,23 (SNR 26,5); GWTC-4.0 pSEOB conj. +0,17 ± 0,11; hier. +0,16 (+0,18/−0,16); pyRing hier. +0,18 (+0,27/−0,26). GW150914 isolado: a ler da fonte. Sinal dos catalogos: δτ̂ > 0 (linha mais ESTREITA) — oposto ao dephasing.

## (d) Poder: N eventos para 5σ por k (σ_1 por evento; lei √N so sem correlacao e sem piso comum)

| k | |δ| | σ p/ 5σ | N (σ₁=0.055 GW250114-like) | N (σ₁=0.140 GW200129-like) | N (σ₁=0,20) | N (σ₁=0,30) | piso 0,029 (013-bis): atingivel? | N com piso 0,029 e σ₁ 0,058 |
|---|---|---|---|---|---|---|---|---|
| k=1 | 0.0199 | 0.0040 | 189 | 1234 | 2525 | 5680 | NAO | impossivel por N: |δ|/5 < piso |
| k=2 | 0.0390 | 0.0078 | 50 | 321 | 657 | 1477 | NAO | impossivel por N: |δ|/5 < piso |
| k=4 | 0.0751 | 0.0150 | 14 | 87 | 178 | 399 | NAO | impossivel por N: |δ|/5 < piso |
| k=8π | 0.3379 | 0.0676 | 1 | 5 | 9 | 20 | sim | 21 |
| k=1/κ̂(χ) | 0.0876 | 0.0175 | 10 | 64 | 131 | 294 | NAO | impossivel por N: |δ|/5 < piso |
| k=2π/κ̂(χ) | 0.3763 | 0.0753 | 1 | 4 | 8 | 16 | sim | 16 |
| k=2π/κ̂(χ) com co-rotacao ω→ω−2Ω_H | 0.0378 | 0.0076 | 53 | 343 | 702 | 1579 | NAO | impossivel por N: |δ|/5 < piso |

Registro ja na casa [DERIVED; NAO-CEGO, 013-bis 22/09]: N₉₀(5σ, k=1) = 335 eventos GW250114-like ou ≈ 3.300 de mistura O4; O5 inteiro 2,2–3,1σ com sistematica zero; 3G fecha por contagem (~207 eventos SNR_RD ≥ 50) so com modelo validado a 0,40%% de τ₂₂₀; condicao sistematica VERMELHA (familia 0,029 = 7× o piso 0,0040 do k=1).

## (f) Falsificar / nao falsificar

- **FALSIFICA_o_par**: (k, M_X, ω_c, local-na-fonte, realizacao-ou-ensemble) fixados ANTES; fracao medida δτ̂ (ou a largura populacional de δf̂, se o mecanismo for difusao de fase) incompativel com −x/(1+x), x = β k (M_X/M_f) N(χ_f), a ≥ 5σ com σ_sys da familia de forma de onda e do inicio da janela CONTROLADA (< |δ|/5) ⟹ FALSIFIED_AT_(k,M) — cai o PAR, nao a lei nem β
- **NAO_falsifica**: coincidir com a RG (δτ̂ = 0 dentro de σ) com |δ| < 5σ ⟹ NOT_FALSIFIED_UNDERPOWERED (correspondencia recuperada: a RG e o limite classico, nao rival); sistematica > limiar ⟹ INCONCLUSIVE_SYSTEMATICS; um unico modo 220 com (M_f, χ_f) livres e NAO identificavel (Kerr 1,25% mais leve imita o k=1) — sem (M_f,χ_f) da inspiral (IMR) ou 2º modo o teste e vazio por construcao [REAL, ORDEM 013]
- **vereditos_permitidos**: ['TGL_RINGDOWN_BRANCH_B_EXCLUDED_AT_(k,M)', 'TGL_RINGDOWN_NOT_FALSIFIED_POWERED', 'TGL_RINGDOWN_NOT_FALSIFIED_UNDERPOWERED', 'TGL_RINGDOWN_INCONCLUSIVE_SYSTEMATICS', 'TGL_RINGDOWN_GR_TENSION_REPORTED']
- **vereditos_proibidos**: ['CONFIRMED', 'PROVED']

## Decisoes que so o operador pode tomar (o pre-registro V1 do ramo B as fixa ANTES de abrir dado)

1. k em τ★ = k·GM/c³: 1 (unidade geometrica, V2) · 2 (r_s/c) · 4 (1/κ) · 8π (β_H = 2π/κ, periodo KMS/modular de Schwarzschild — a leitura «tempo emergente do fluxo modular»: 1 unidade modular = β_H) · 2π/κ̂(χ_f) de Kerr com ou sem co-rotacao ω→ω−2Ω_H (para χ≠0 e' [CONJECTURE]: Kay–Wald 1991 — nao ha Hartle–Hawking de Kerr)
2. qual M: M_f,det (fixa os QNMs observados; convencao da V2) · M_f,src (repouso; x identico se tudo no mesmo referencial) · M_tot (×1,05) · M_chirp (×0,46) — e o referencial declarado (misturar custa (1+z)^±1)
3. onde a lei age: LOCAL na fonte (durante o ringdown; τ★ e' propriedade do remanescente) — na propagacao o ramo B apaga a onda (Γ_B·D/c ~ 2e17 e-folds: erro de tipo, nao teste) [REAL, auditoria 28/09]
4. mecanismo/estimando: amortecimento da envoltoria por realizacao (δτ̂ le x inteiro) OU difusao de fase (ensemble; por realizacao so ~0,27x e o estimando passa a ser a largura populacional de δf̂) — identificacao [ONTO] que fixa a previsao efetiva e o poder
5. o observavel e a fonte: δτ̂_220 publicado (pSEOBNR IMR; posteriores Zenodo 17018009 — NAO esta em disco: so o strain 32 s do GW250114 na Bancada) vs reanalise propria (so-220 com (M_f,χ_f) da inspiral; a parede do pSEOBNRv4HM_PA do lalsuite 7.26 e a receita R0–R9 da ORDEM 015)
6. o piso sistematico aceito (familia SEOB×Phenom 0,029 [DECLARADO 013-bis]; inicio da janela): com ele k ≤ 4 e a co-rotacao sao inalcancaveis por N; so k ~ 8π/2π/κ̂ sem co-rotacao supera o piso — e esses ja leem ~6σ contra o δτ̂ publicado do GW250114 na leitura por envoltoria (NAO-CEGO; sem veredito)
7. vereditos e cegueira: EXCLUDED_AT_(k,M) / NOT_FALSIFIED_POWERED / UNDERPOWERED / INCONCLUSIVE_SYSTEMATICS / GR_TENSION_REPORTED; CONFIRMED proibido; declarar NAO-CEGO quanto ao GW250114 publicado e quanto aos 89 eventos da V2

os z contra o GW250114 sao leitura NAO-CEGA de um numero PUBLICADO (aprox. gaussiana da semi-largura 90%); nenhum veredito; PROVADA ≠ CONFIRMADA; NOT_FALSIFIED ≠ CONFIRMED
