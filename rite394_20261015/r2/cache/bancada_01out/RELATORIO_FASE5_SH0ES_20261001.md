# Fase 5 (01/10/2026) — SH0ES na Bancada: o Pantheon+SH0ES completo e as três leituras da lei

**Pré-registro** sha256 `f9fbf497c90c0a66730d8d87bc6d0a9eb46478889b80908eedef7cea95c7cc63` (hash conferido pelo runner antes de abrir qualquer número) · **Resultado** sha256 `851d1076b85f12f671bfbe018f67e8291a2c83686bb98fb2251a4ed3c254eca2` · 646 s de rodada · β_TGL = α√e em runtime = 0.0120313004.
**A amostra:** 1657 SNe = 1580 de cosmologia (zHD > 0,01) + 77 calibradores Cefeida em 37 hospedeiras (μ = CEPH_DIST), covariância STAT+SYS 1701×1701 restrita, M profilado (Brout+22 / Riess+22). **A convenção:** a do artigo 1 (β só na lei; fundo ΛCDM ajustado; núcleo D1b). **As leituras:** nenhuma (ΛCDM com a escada dentro: a tensão nua); sombra (D_M/K em todo z; relógios sem fator); acumulada (K(z) na integral de D_M; relógios com K(z)).

## Vereditos (pré-registrados)

- **Base (família P, sombra, d1b):** `TGL_FASE5_SH0ES__LADDER_DEVIATION_CONSISTENT_WITH_ZERO_WITHIN_1SIGMA__TENSION_LCDM_Z_5P26__BAYES_STRONG_FOR_TGL__ACUMULADA_DELTA_Z_M0P40__SNE_SOMBRA_VS_ACUMULADA_UNDERPOWERED_LNB_0P29__JOINT_WITH_CLOCKS_LNB_SOMBRA_VS_ACUMULADA_5P35_DCHI2_Z_3P27__ZSPLIT_CONSTANT_SHIFT_CHI2_8P95_GL_5__ZSPLIT_SHIFT_Z_5P38_VS_SOMBRA_M0P49__VALIDATION_Z_0P04__CC_DIAGONAL_ERRORS_ONLY__NOT_A_CONFIRMATION`
- **Validação (família V):** `TGL_FASE5_VALIDATION__H0_WITHIN_1SIGMA_OF_PUBLISHED__Z_0P04`

## V — validação: SNe + calibradores sozinhos, ΛCDM

H₀ = 73.53 ± 1.02, Ω_m = 0.332 (Bancada) contra H₀ = 73,6 ± 1,1 e Ω_m = 0,334 ± 0,018 de Brout+22 [DECLARADO: valores de memória da gerência, não lidos da fonte aqui] e 73,04 ± 1,04 de R22 [KNOWN]: z = 0.04 contra o alvo. Diferenças de pipeline ditas no pré-registro (corte zHD > 0,01 OU calibrador; M profilado; sem o tratamento SH0ES completo dos ancoradouros).

## Tabela — por família e leitura (modo artigo, d1b)

| família | leitura | χ² ΛCDM / TGL / livre (gl) | H₀ ΛCDM → H₀ TGL (fundo) | H₀ local TGL | Ω_m TGL | M̂ TGL | δ̂ ± σ | z_δ | z tensão (ΛCDM vs leitura) | ln B TGL/ΛCDM · ln Z TGL |
|---|---|---|---|---|---|---|---|---|---|---|
| P_dr2_sh0es | nenhuma | 1496.977 / 1496.977 / 1496.977 (1670) | 68.85 → 68.85 | 74.62 | 0.297 | -19.3957 | -0.01203 ± n/d | **n/d** | +0.00 | n/d · n/d |
| P_dr2_sh0es | sombra | 1496.977 / 1469.308 / 1469.166 (1670) | 68.85 → 68.39 | 74.13 | 0.303 | -19.2362 | -0.00080 ± 0.00213 | **-0.38** | +5.26 | 13.84 · -747.85 |
| P_dr2_sh0es | acumulada | 1496.977 / 1469.887 / 1469.726 (1670) | 68.85 → 68.38 | 74.12 | 0.303 | -19.2373 | -0.00086 ± 0.00214 | **-0.40** | +5.20 | 13.55 · -748.14 |
| P_dr2_sh0es | sombra_d1a | 1496.977 / 1469.567 / 1469.166 (1670) | 68.85 → 68.37 | 74.37 | 0.303 | -19.2289 | -0.00129 ± 0.00204 | **-0.63** | +5.24 | n/d · n/d |
| Q_dr1_sh0es | sombra | 1499.589 / 1470.487 / 1470.480 (1669) | 68.90 → 68.09 | 73.80 | 0.307 | -19.2441 | -0.00018 ± 0.00219 | **-0.08** | +5.39 | 14.56 · -748.13 |
| Q_dr1_sh0es | acumulada | 1499.589 / 1470.998 / 1470.990 (1669) | 68.90 → 68.08 | 73.79 | 0.307 | -19.2455 | -0.00020 ± 0.00221 | **-0.09** | +5.35 | 14.30 · -748.39 |
| S_dr2_sh0es_cc | nenhuma | 1511.705 / 1511.705 / 1511.705 (1702) | 68.85 → 68.85 | 74.61 | 0.297 | -19.3957 | -0.01203 ± n/d | **n/d** | +0.00 | n/d · n/d |
| S_dr2_sh0es_cc | sombra | 1511.705 / 1484.033 / 1483.891 (1702) | 68.85 → 68.39 | 74.13 | 0.303 | -19.2361 | -0.00080 ± 0.00213 | **-0.38** | +5.26 | 13.84 · -755.22 |
| S_dr2_sh0es_cc | acumulada | 1511.705 / 1494.733 / 1490.687 (1702) | 68.85 → 68.30 | 74.03 | 0.304 | -19.2395 | -0.00364 ± 0.00183 | **-1.99** | +4.12 | 8.49 · -760.57 |

**ln B(sombra / acumulada)** — P (só distâncias): +0.29 (declarado UNDERPOWERED: as SNe não discriminam; poder prévio 0,19σ) · S (distâncias + relógios): +5.35, Δχ²(acumulada − sombra) → +3.27σ (o poder vem dos relógios, já vistos na Fase 4: consistência, não teste cego).

## Posteriores (sombra, d1b; ensemble GPU 256 × 3000)

- **P_dr2_sh0es:** δ mediana -0.00078 (16–84: -0.00291 / +0.00135); H₀ fundo = 68.42; fração β ≥ α√e 0.357; fração β > 0 1.000.
- **S_dr2_sh0es_cc:** δ mediana -0.00082 (16–84: -0.00293 / +0.00129); H₀ fundo = 68.43; fração β ≥ α√e 0.349; fração β > 0 1.000.

## O teste em bins de z (GLS com a covariância completa; θ_fundo = ΛCDM de Planck + DR2 sem SNe: H₀ = 68.53, K = 1.08379)

| bin | n | s_b medido (mag) | σ | sombra (5 log10 K) | acumulada ⟨5 log10 K(z)⟩ |
|---|---|---|---|---|---|
| 0.01–0.05 | 524 | +0.1512 | 0.0304 | 0.1747 | 0.1746 |
| 0.05–0.15 | 181 | +0.1575 | 0.0312 | 0.1747 | 0.1743 |
| 0.15–0.30 | 381 | +0.1759 | 0.0306 | 0.1747 | 0.1738 |
| 0.30–0.60 | 365 | +0.1652 | 0.0312 | 0.1747 | 0.1730 |
| 0.60–1.00 | 104 | +0.1940 | 0.0354 | 0.1747 | 0.1717 |
| 1.00–2.30 | 25 | +0.0903 | 0.0586 | 0.1747 | 0.1690 |

M̂ = -19.2446 ± 0.0296 mag. χ² das hipóteses (gl 6): sem lei 37.9 · sombra 9.2 · acumulada 9.5. **Deslocamento comum** s = 0.1601 ± 0.0297 mag: 5.4σ de zero; -0.49σ de 5 log10 K = 0.1747 (sombra). **Constância em z:** χ² = 8.95 (gl 5). As SNe medem o deslocamento e a sua constância em z ao nível de 0,03 mag; NÃO discriminam sombra de acumulada (diferença ≤ 0,006 mag).

## Leitura

1. **Validação:** o H₀ que a Bancada tira de SNe + calibradores Cefeida é o número acima; a comparação com o publicado está na seção V.
2. **A escada com a verossimilhança completa (P, sombra):** δ e o pull estão na tabela — é a Fase 4 refeita com o SH0ES de verdade (calibradores + covariância), no lugar do número 73,04 ± 1,04.
3. **A tensão nua (nenhuma vs sombra):** z_tensão diz quanto o ΛCDM com a escada dentro ajusta pior que a lei com K.
4. **Sombra vs acumulada:** nas SNe, indiscriminável (declarado antes); no conjunto com os relógios, a verossimilhança conjunta prefere a leitura que a tabela mostra — consistência com a Fase 4, não teste cego.
5. **Constância em z:** o deslocamento por bin contra a hipótese de um s comum; a premissa comum às duas leituras (um deslocamento uniforme dos leitores por distância) é medida ao nível de 0,03 mag por bin.

**O que não muda:** nada aqui confirma; NOT_FALSIFIED ≠ CONFIRMED; PROVADA ≠ CONFIRMADA; a RG é o limite clássico; a leitura «sombra» segue [OPEN/ONTO] — decisão do operador. Erros dos cronômetros diagonais. **Visto antes** declarado no pré-registro.

*Gerado por `relatorio_fase5.py`; resultado sha256 `851d1076b85f12f671bfbe018f67e8291a2c83686bb98fb2251a4ed3c254eca2`.*
