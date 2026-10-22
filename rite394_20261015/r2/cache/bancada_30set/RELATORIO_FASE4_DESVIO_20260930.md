# Fase 4 (30/09/2026, noite) — O DESVIO δ = β̂ − β_TGL na convenção do artigo 1, com o núcleo derivado D1b

**Pré-registro** sha256 `22b4c440d8ad844d7dd4071734d10c2776da3a7e1587709cb10f5e7987f4acf9` (hash conferido pelo runner antes de abrir qualquer número) · **Resultado** sha256 `10683b334d28d84acdd8a086fe91fcbeaa46e747b0e3b51dc4192c270d8e6219` · 801 s de rodada · β_TGL = α√e em runtime = 0.0120313004 · z* = 1089.95 · cronômetros: 32 pontos (json sha256 `530db89807c02723`, importados do artigo 1 sha256 `29c92b66b2fd6b4d`).

**A convenção:** a lei da dissipação transporta a calibração ΛCDM de Planck — β entra SÓ na lei, o fundo é ΛCDM (Planck comprimido Chen+2019 + BAO ajustados). **O núcleo primário:** D1b, 𝒲 = |1+w_eff|, K = E_ΛCDM(z*)^{2β/3} (I_b = ∫|1+w| dN = (2/3)·ln E(z*): forma fechada conferida na grade a 1,8e-12; min(1+w) = 0.3153). D1a (𝒲 = 1) ao lado. **O foco:** o desvio δ = β̂ − β_TGL, com β_TGL como assíntota e a função de aproximação FIXADA pelo núcleo derivado (sem parâmetro livre). **Dois registros:** a escada (SH0ES R22, registro inteiro) e os 32 cronômetros de Moresco+ 2022 (registros intermediários, lidos com a lei acumulada de z* até z como em C.5b do artigo 1) — o teste que podia perder, poder prévio 3.49σ (erros DIAGONAIS: poder sobrestimado).

## Vereditos (pré-registrados)

- **Base (família P, d1b):** `TGL_FASE4_DEVIATION__DEVIATION_1_TO_3_SIGMA__LADDER_PULL_1P08__BAYES_STRONG_FOR_TGL__D1A_DELTA_Z_M1P37__INTERMEDIATE_CC_DELTA_Z_M3P12__INTERMEDIATE_CC_LAW_GAIN_M3P22__STACKED_CONTROL_Z_M1P75__CC_DIAGONAL_ERRORS_ONLY__NOT_A_CONFIRMATION`
- **Registros intermediários (família T, d1b):** `ACCUMULATED_FLOW_READING_AT_INTERMEDIATE_REGISTERS__DISFAVORED_ABOVE_3_SIGMA__DELTA_CC_Z_M3P12__LAW_GAIN_Z_M3P22__DIAGONAL_ERRORS_ONLY__NOT_A_CONFIRMATION`

## Tabela — por família e núcleo (modo artigo)

| família | núcleo | χ² ΛCDM / TGL / livre | δ̂ ± σ (por nat) | z_δ | z perfil | ganho da lei | pull escada (ΛCDM / TGL / livre) | H₀ fundo → K → H₀ local | ln B TGL/ΛCDM · TGL/livre |
|---|---|---|---|---|---|---|---|---|---|
| P_dr2_escada | d1b | 31.627 / 15.576 / 14.293 | -0.00250 ± 0.00223 | **-1.12** | 1.13 | +4.01 | -4.00 / 1.08 / -0.00 | 68.43 → 1.08381 → 74.16 | 8.02 · 2.25 |
| P_dr2_escada | d1a | 31.627 / 16.206 / 14.293 | -0.00292 ± 0.00213 | **-1.37** | 1.38 | +3.93 | -4.00 / 1.32 / -0.00 | 68.41 → 1.08780 → 74.41 | 7.70 · 1.97 |
| Q_dr2_escada_pantheon | d1b | 1421.887 / 1404.703 / 1403.647 | -0.00227 ± 0.00222 | **-1.02** | 1.03 | +4.15 | -4.11 / 0.98 / 0.00 | 68.33 → 1.08382 → 74.06 | 8.59 · 2.36 |
| Q_dr2_escada_pantheon | d1a | 1421.887 / 1405.278 / 1403.647 | -0.00269 ± 0.00213 | **-1.27** | 1.28 | +4.08 | -4.11 / 1.22 / -0.00 | 68.31 → 1.08780 → 74.31 | n/d · n/d |
| R_dr1_escada | d1b | 34.172 / 17.028 / 16.286 | -0.00199 ± 0.00232 | **-0.86** | 0.86 | +4.14 | -3.92 / 0.79 / 0.00 | 68.15 → 1.08386 → 73.86 | 8.57 · 2.48 |
| R_dr1_escada | d1a | 34.172 / 17.491 / 16.286 | -0.00242 ± 0.00222 | **-1.09** | 1.10 | +4.08 | -3.92 / 1.00 / -0.00 | 68.11 → 1.08780 → 74.08 | n/d · n/d |
| S_dr2_escada_cc | d1b | 46.360 / 40.496 / 33.352 | -0.00502 ± 0.00191 | **-2.63** | 2.67 | +2.42 | -4.00 / 1.00 / -1.12 | 68.35 → 1.08382 → 74.08 | 2.93 · -0.52 |
| S_dr2_escada_cc | d1a | 46.360 / 41.470 / 33.159 | -0.00522 ± 0.00184 | **-2.84** | 2.88 | +2.21 | -4.00 / 1.23 / -1.07 | 68.32 → 1.08780 → 74.32 | n/d · n/d |
| T_dr2_cc | d1b | 29.017 / 39.410 / 28.946 | -0.01108 ± 0.00355 | **-3.12** | 3.23 | -3.22 | — | 68.44 → 1.08380 → 74.17 | -5.20 · -2.82 |
| T_dr2_cc | d1a | 29.017 / 39.812 / 28.948 | -0.01111 ± 0.00350 | **-3.18** | 3.30 | -3.29 | — | 68.43 → 1.08780 → 74.44 | n/d · n/d |
| P_empilhado (CONTROLE, modo tgl: fundo efetivo + lei — a dupla contagem, não-cego) | d1b | 31.627 / 17.142 / 14.028 | -0.00347 ± 0.00199 | **-1.75** | 1.76 | +3.81 | -4.00 / 1.71 / 0.03 | 69.04 → 1.08375 → 74.82 | — |

## Posteriores (ensemble GPU 256 × 3000, queima 600, semente 42; núcleo d1b)

- **P_dr2_escada:** δ mediana -0.00250 (16–84: -0.00474 / -0.00030); H₀ = 68.53; fração β ≥ α√e 0.129; fração β > 0 1.000; z pela cauda 1.13; τ_max 39.
- **T_dr2_cc:** δ mediana -0.01117 (16–84: -0.01476 / -0.00767); H₀ = 68.52; fração β ≥ α√e 0.001; fração β > 0 0.596; z pela cauda 3.28; τ_max 41.

## Leitura

1. **A escada (o registro inteiro), na convenção do artigo e com D1b:** δ = -0.00250 ± 0.00223 por nat (-1.12σ) — o desvio é consistente com zero dentro de ~1σ; em β = α√e a escada fica a +1.08σ do fundo transportado pela lei (contra −4,00σ no ΛCDM); ln B(TGL/ΛCDM) = +8.02 (forte), ln B(TGL/β livre) = +2.25. O modelo sem parâmetro livre paga a parcimônia. As replicações (Pantheon+, DR1) dão o mesmo.
2. **Os registros intermediários (os 32 cronômetros, sem a escada) — o teste que podia perder, PERDEU para a leitura de fluxo acumulado:** os relógios em z = 0,07–1,97 leem β̂ = +0.00095 ± 0.00355 (δ = -0.01108: 3.12σ abaixo de β_TGL; posterior: fração β ≥ α√e = 0.001), a lei acumulada ajusta os cronômetros PIOR que o ΛCDM (ganho -3.22σ; ln B = -5.20, forte contra), com o fundo (H₀, ω_b, ω_c) fixado por Planck + DR2. Erros diagonais (sem a covariância sistemática de Moresco+ 2020): a significância está sobrestimada por fator não medido aqui.
3. **Juntos (escada + cronômetros):** δ = -0.00502 ± 0.00191 (-2.63σ): os dois registros puxam em sentidos opostos e a verossimilhança conjunta acusa a tensão entre eles.
4. **O controle empilhado** (fundo efetivo + lei, o que as Fases 2–3 fizeram): δ = -0.00347 ± 0.00199 (-1.75σ) — a dupla contagem de β puxa o desvio para baixo; na convenção do artigo o puxão some.
5. **O que isso significa (leitura [OPEN/ONTO] da gerência, NÃO adotada; a decisão é do operador):** a sombra (os leitores locais por distância: a escada) lê o fator do vazamento; os relógios intermediários (idade diferencial, sem distância) NÃO leem o fator acumulado — leem a face. Se a leitura vale, a lei da dissipação é uma lei da LEITURA por distância (do registro inteiro, de z* até hoje), não uma modificação de H(z) ponto a ponto; a forma «H(z) acumulada» do C.5b do artigo 1 fica desfavorecida pelos dados atuais. A leitura inversa (a lei está errada e a escada tem um sistemático de 8%) é igualmente admissível pelos dados desta Fase — é a incidência da natureza que decide.

**O que não muda:** nada aqui confirma; NOT_FALSIFIED ≠ CONFIRMED; PROVADA ≠ CONFIRMADA; a RG é o limite clássico; o gate matemático não se move. **O que foi visto antes** está declarado no pré-registro (`visto_antes`). Pendente do operador: qual fundo é o fundo (a pergunta do ângulo); a forma da camada E1; e se a leitura do item 5 vira tipo.

*Gerado por `relatorio_fase4.py`; resultado sha256 `10683b334d28d84acdd8a086fe91fcbeaa46e747b0e3b51dc4192c270d8e6219`.*


## Errata ao lado (30/09/2026, noite — aferidor independente da v378, C7/B2)

No item 2, «PERDEU» é mais forte do que o veredito: os cronômetros sozinhos **desfavorecem** a leitura de fluxo acumulado em β_TGL a −3,22σ (ganho da lei) e −3,12σ (δ), com erros diagonais (significância sobrestimada por fator não medido) e posterior P(β > 0) = 0,60 — consistentes com β = 0; a direção já fora vista na prova de fumaça (declarado em `visto_antes`: cego parcial). No item 4, «dupla contagem» é leitura da gerência sob a convenção do artigo 1 [DERIVED da convenção], não medida.
