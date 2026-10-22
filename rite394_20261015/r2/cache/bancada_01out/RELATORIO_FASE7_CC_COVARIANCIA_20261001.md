# Fase 7 (01/10/2026) — os cronômetros cósmicos com a COVARIÂNCIA COMPLETA de Moresco+2020

**Pré-registro** sha256 `36e354d547895d1d3d72637e4eb10c599a4a0b937d090453e72d64d435e746fa` · **Resultado** sha256 `4f2671cbce7576f6139b97e01297dc7d4f7a9b9c6f69d9680ed4245334a39f96` · 634 s de rodada · β_TGL = α√e em runtime = 0.0120313004.

**O que mudou:** as Fases 4 e 5 leram os 32 cronômetros com erros DIAGONAIS (ressalva declarada: poder sobrestimado). Hoje a Bancada ganhou a opção `cc_cov`: `diagonal` (o que havia), `moresco2020` (os 15 pontos de Moresco 2012/2015/2016 com (z, H, σ) DA FONTE e os termos de IMF e de modelo SPS (odd-one-out) totalmente correlacionados, Cov_ij = H_i η_i H_j η_j, como no notebook do repositório gitlab.com/mmoresco/CCcovariance; os 17 pontos de outros autores ficam diagonais — o repositório não traz a sistemática deles) e `moresco2020_todos` (a sistemática correlacionada em todos os 32: faixa conservadora, não estimativa). **Ressalva:** o repositório descreve também componentes de metalicidade, população jovem, SFH e biblioteca estelar; a receita do notebook (e a daqui) soma só IMF + SPS-ooo aos erros publicados (que já trazem estat. + metalicidade).

**Poder prévio dos relógios (Fisher de β, fundo fixo; prova de fumaça, hasheada antes):** diagonal 3.49σ · moresco2020 2.33σ · todos 1.66σ (razão 0.67 e 0.47).

## Veredito (pré-registrado)

`TGL_FASE7_CC_COVARIANCE__Q1_TENSION_1_TO_3_SIGMA_WEAKENS__T_LAW_GAIN_Z_M1P66_VS_DIAG_M3P22__Q2_WEAK_FOR_SHADOW_WEAKENS__LNB_1P62_VS_DIAG_5P35__Q3_DEVIATION_1_TO_3_SIGMA__S_DELTA_Z_M1P71__BAND_TODOS_T_Z_M1P54__NOT_A_CONFIRMATION`

## Tabela — por família, leitura e covariância (modo artigo, núcleo D1b)

| família | leitura | cc_cov | χ² ΛCDM / TGL / livre | δ̂ ± σ | z_δ | z ganho da lei | ln B TGL/ΛCDM | ln Z TGL |
|---|---|---|---|---|---|---|---|---|
| S_dr2_escada_cc | acumulada | diagonal | 46.360 / 40.496 / 33.352 | -0.00502 ± 0.00191 | **-2.63** | +2.42 | 2.93 | -33.44 |
| S_dr2_escada_cc | acumulada | moresco2020 | 46.470 / 33.140 / 30.159 | -0.00352 ± 0.00206 | **-1.71** | +3.65 | 6.66 | -29.76 |
| S_dr2_escada_cc | acumulada | moresco2020_todos | 46.541 / 32.771 / 30.432 | -0.00324 ± 0.00214 | **-1.52** | +3.71 | 6.88 | -29.57 |
| T_dr2_cc | acumulada | diagonal | 29.017 / 39.410 / 28.946 | -0.01108 ± 0.00355 | **-3.12** | -3.22 | -5.20 | -32.85 |
| T_dr2_cc | acumulada | moresco2020 | 29.161 / 31.916 / 28.823 | -0.00895 ± 0.00524 | **-1.71** | -1.66 | -1.38 | -29.10 |
| T_dr2_cc | acumulada | moresco2020_todos | 29.158 / 31.523 / 29.144 | -0.01113 ± 0.00748 | **-1.49** | -1.54 | -1.18 | -28.90 |
| U_dr2_sh0es_cc | acumulada | diagonal | 1511.705 / 1494.733 / 1490.687 | -0.00364 ± 0.00183 | **-1.99** | +4.12 | 8.49 | -760.57 |
| U_dr2_sh0es_cc | acumulada | moresco2020 | 1511.817 / 1487.432 / 1486.355 | -0.00204 ± 0.00198 | **-1.03** | +4.94 | 12.19 | -756.92 |
| U_dr2_sh0es_cc | acumulada | moresco2020_todos | 1511.884 / 1487.072 / 1486.400 | -0.00168 ± 0.00205 | **-0.82** | +4.98 | 12.41 | -756.73 |
| U_dr2_sh0es_cc | sombra | diagonal | 1511.705 / 1484.033 / 1483.891 | -0.00080 ± 0.00213 | **-0.38** | +5.26 | 13.84 | -755.22 |
| U_dr2_sh0es_cc | sombra | moresco2020 | 1511.817 / 1484.187 / 1484.043 | -0.00081 ± 0.00213 | **-0.38** | +5.26 | 13.82 | -755.29 |
| U_dr2_sh0es_cc | sombra | moresco2020_todos | 1511.884 / 1484.154 / 1484.017 | -0.00079 ± 0.00213 | **-0.37** | +5.27 | 13.87 | -755.28 |

## Q2 — sombra vs acumulada (família U: Pantheon+SH0ES + relógios)

| cc_cov | ln B(sombra / acumulada) | Δχ²(acumulada − sombra) → σ |
|---|---|---|
| diagonal | +5.35 | +3.27 |
| moresco2020 | +1.62 | +1.80 |
| moresco2020_todos | +1.46 | +1.71 |

**Posterior de T sob moresco2020 (ensemble GPU 256 × 3000):** δ mediana -0.00919 (16–84: -0.01445 / -0.00402); fração β ≥ α√e 0.037; fração β > 0 0.707.


## Leitura

1. **Q1 (só os registros intermediários, T):** z do ganho da lei acumulada: diagonal -3.22 → moresco2020 -1.66 → todos -1.54; δ̂ = -0.00895 ± 0.00524 (z -1.71) sob moresco2020. A banda e SURVIVES/WEAKENS/STRENGTHENS estão no veredito.
2. **Q2 (sombra vs acumulada, U):** ln B diagonal +5.35 → moresco2020 +1.62 → todos +1.46.
3. **Q3 (escada + relógios, S):** δ̂ diagonal -0.00502 ± 0.00191 (z -2.63) → moresco2020 -0.00352 ± 0.00206 (z -1.71).

**O que não muda:** nada aqui confirma; NOT_FALSIFIED ≠ CONFIRMED; a RG é o limite clássico; a leitura «sombra» segue [OPEN/ONTO]; a diagonal já tinha sido vista (Fases 4–5): a novidade desta fase é a covariância, declarada no pré-registro. A variante «todos» é faixa, não estimativa.

*Gerado por `relatorio_fase7.py`; resultado sha256 `4f2671cbce7576f6139b97e01297dc7d4f7a9b9c6f69d9680ed4245334a39f96`.*
