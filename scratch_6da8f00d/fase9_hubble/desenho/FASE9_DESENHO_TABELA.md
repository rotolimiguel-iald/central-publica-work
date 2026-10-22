# FASE 9 — a razão de Hubble: o DESENHO ESTATÍSTICO do teste discriminante (lente «desenho», 2026-10-05T20:39)

ENSAIO NÃO-CEGO (alvos públicos). β = α√e = 0.012031300400803 (α lido do um.py por regex). z* = 1089.95 [INPUT]. Selo lido: v386 (`72efaf72f604b721`).

## (a) K = E(z*)^{2β/3} — reproduzido, não copiado

| quantidade | recomputado | lido do disco | diff |
|---|---|---|---|
| K (Planck 2018, core v386 `/core/the_dissipation_law_with_contrast_v378/K_D1b_runtime`) | 1.083977366 | 1.083977366 | 4.8e-14 |
| K (θ̂_TGL Fase 4: H0 68.4298, ω_b 0.022501, ω_c 0.118433) | 1.083807175 | 1.083807175 | 2.1e-14 |
| K (reanálise D1b, og = 2.469e-5/T⁴) | 1.083975727 | 1.083975713 | 1.4e-08 |
| E(z*) Planck | 23234.763911 | 23234.763911 | 0.0e+00 |
| β runtime vs Fase 4 | 0.012031300400803 | 0.012031300400803 | 0.0e+00 |
| H0_local previsto (Fase 4) | 74.1647 | 74.1647 | 1.4e-12 |

Sensibilidade (em θ̂ da Bancada; Ω_m = 0.3023, Ω_r = 8.934e-05, f_m = 0.756, f_r = 0.244 no nó): ∂lnK/∂lnΩ_m = 0.00303; ∂lnK/∂ln(1+z*) = 0.01301; ∂K/∂Ω_m = 0.01087; ∂K/∂z* = 1.29e-05; ∂K/∂N_eff = 1.42e-04; ∂lnK/∂β = I_b = 6.6892. ΔH0_local: por ΔΩ_m = 0,01 → 0.0074; por Δz* = 1 → 0.00088; por σ(z*) = 0,21 → 0.000186; por ΔN_eff = 0,1 → 0.0010.

| Ω_m | K | H0_local @ 68,531 |
|---|---|---|
| 0.2900 | 1.083671 | 74.265 |
| 0.3000 | 1.083782 | 74.273 |
| 0.3023 | 1.083807 | 74.274 |
| 0.3100 | 1.083890 | 74.280 |
| 0.3152 | 1.083945 | 74.284 |
| 0.3200 | 1.083995 | 74.287 |
| 0.3300 | 1.084098 | 74.294 |
| 0.3400 | 1.084198 | 74.301 |

| nó z | K | ΔK vs z* |
|---|---|---|
| 1059.94 (z_drag Planck 2018 [KNOWN — a ler; só como sistemática de «qual registro»]) | 1.083414 | -3.93e-04 |
| 1088.0 (−2) | 1.083782 | -2.52e-05 |
| 1089.8 (z* Planck 2018 TT,TE,EE+lowE+lensing (1089,80 ± 0,21) [KNOWN — a ler]) | 1.083805 | -1.94e-06 |
| 1089.95 (z* [INPUT] do um.py) | 1.083807 | +0.00e+00 |
| 1091.0 (+1) | 1.083821 | +1.36e-05 |
| 1100.0 (+10) | 1.083937 | +1.29e-04 |

## (b) Os alvos

| id | H0 | σ | tipo | fonte | estatuto | combinar? |
|---|---|---|---|---|---|---|
| L1_sh0es_r22 | 73.04 | 1.04 | Cefeidas (HST), anchors NGC 4258 + LMC + MW | Riess et al. 2022, ApJL 934, L7 (SH0ES; R22) [KNOWN] | [KNOWN — lido do disco da casa] | sim |
| L1b_sh0es_r25_cefeidas | 73.49 | 0.93 | Cefeidas (HST+JWST) | Riess et al. 2025, arXiv:2509.01667 (abstract lido 30/09) [KNOWN] | [KNOWN — lido do disco da casa] | não |
| L1c_sh0es_r25_mais_trgb | 73.18 | 0.88 | Cefeidas + TRGB (SH0ES) | arXiv:2509.01667 [KNOWN] | [KNOWN — lido do disco da casa] | não |
| L1d_riess_jwst_2024_tres_metodos | 72.60 | 2.00 | JWST Cefeidas+TRGB+JAGB (subamostra SH0ES) | Riess et al. 2024, ApJ 977, 120; arXiv:2408.11770 (abstract lido 30/09) [KNOWN] | [KNOWN — lido do disco da casa] | não |
| L2_cchp_trgb_jagb_cef | 70.39 | 1.94 | CCHP JWST: TRGB + JAGB + Cefeidas (combinado) | Freedman et al. 2024/2025, ApJ 985, 203; Freedman et al. 2025, arXiv:2408.06153v3 (abstract lido 30/09) [KNOWN] | [KNOWN — lido do disco da casa] | sim |
| L2a_cchp_trgb_so | 68.81 | 2.22 | TRGB JWST (CCHP) | arXiv:2408.06153v3 (TRGB só) [KNOWN] | [KNOWN — lido do disco da casa] | não |
| L2b_cchp_jagb_so | 67.80 | 2.72 | JAGB JWST (CCHP) | arXiv:2408.06153v3 (JAGB só) [KNOWN] | [KNOWN — lido do disco da casa] | não |
| L2c_cchp_cefeidas_so | — | — | Cefeidas JWST (CCHP) | Freedman et al. 2024/2025 (CCHP JWST Cefeidas só) [KNOWN — A LER DA FONTE] | [KNOWN — a ler da fonte] | não |
| L3_sbf_jwst | 73.80 | 2.40 | SBF calibrado por TRGB (JWST) | Jensen et al. 2025, arXiv:2502.15935 (abstract lido 30/09) [KNOWN] | [KNOWN — lido do disco da casa] | sim |
| L4_masers | 73.90 | 3.00 | megamasers (geométrico, sem SNe) | Pesce et al. 2020, arXiv:2001.09213 (abstract lido 30/09) [KNOWN] | [KNOWN — lido do disco da casa] | sim |
| L5_tdcosmo_2025 | 71.60 | 3.60 | lentes com atraso temporal (geométrico) | TDCOSMO 2025, arXiv:2506.03023 (abstract lido 30/09) [KNOWN] | [KNOWN — lido do disco da casa] | sim |
| L6_sirenes_o4a | 76.60 | 11.25 | sirenes padrão (LVK O4a) | LVK O4a cosmology summary (ligo.org, PDF lido 30/09) [KNOWN] | [KNOWN — lido do disco da casa] | sim |
| L6b_gw170817 | 70.00 | 10.00 | sirene única | Abbott et al. 2017, Nature 551, 85 (GW170817, 70 +12/−8) [KNOWN — A LER DA FONTE; valor do prompt, simetrizado 10] | [KNOWN — a ler da fonte] | não |
| V_bancada_sh0es_so | 73.53 | 1.02 | escada completa reproduzida na casa | Bancada Fase 5 (Pantheon+SH0ES completo, ΛCDM, SNe + 77 calibradores) [REAL] | [REAL — casa] | não |
| BG1_bancada_lcdm_planck_dr2 | 68.53 | 0.30 | FUNDO NU (ΛCDM) Planck comprimido Chen+2019 + DESI DR2, SEM escada | Bancada: ajuste ΛCDM de Planck comprimido + DR2 [REAL] | [REAL — casa] | não |
| BG2_planck2018 | 67.36 | 0.54 | FUNDO NU (ΛCDM) Planck só, publicado | Planck 2018 VI, TT,TE,EE+lowE+lensing, ΛCDM [KNOWN] | [KNOWN — lido do disco da casa] | não |
| BG3_desi_dr2_bbn | 68.50 | 0.60 | escada INVERSA, sem CMB | DESI Collaboration 2025, DR2 Results II (arXiv:2503.14738), BAO + BBN, sem CMB [KNOWN — A LER DA FONTE; valor do prompt] | [KNOWN — a ler da fonte] | não |
| BG4_CONTROLE_tgl_efetivo | 69.20 | 0.30 | fundo TGL EFETIVO (mapa + E1): JÁ carrega β | Bancada: ajuste TGL (β = α√e, mapa eff) de Planck comprimido (Chen+2019) + DESI DR2; σ por JᵀJ; 30/09 [REAL] | [REAL — casa] | não |
| BG5_ref_tgl_bestfit_fase4 | 68.43 | 0.30 | fundo ajustado COM o leitor previsto | Bancada Fase 4, θ̂_TGL com a escada DENTRO do ajuste [REAL] | [REAL — casa] | não |

Covariância declarada: σ_SN(fluxo) = 0.7 comum a L1/L2/L3 (e réplicas da escada); σ_4258 = 0.5 comum L1×L2 [DECLARADO — a conferir]. Réplicas do mesmo programa nunca se somam.

## (c)+(d) Hipóteses, estatística, poder e a função de veredito — ensaio sobre os alvos públicos

| família × fundo | n | H0_bg | previsto TGL | local comb. | razão ± σ | z_TGL | z_ΛCDM | disp/gl (p) | Δχ²(TGL−ΛCDM) | lnB TGL/ΛCDM | lnB TGL/livre | lnB TGL/shift | lnB TGL/EDE | β̂ ± σ (z_δ) | sep (σ) | veredito (ensaio) |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| A_seis × BG1_bancada_lcdm_planck_dr2 | 6 | 68.531 ± 0.301 | 74.274 | 72.906 ± 0.912 | 1.0638 ± 0.0141 | -1.42 | +4.53 | 0.53 (0.757) | -18.76 | +9.38 | +2.00 | +1.43 | +0.86 | 0.00925 ± 0.00198 (-1.40) | 5.94 | `TGL_FASE9_HUBBLE__NOT_FALSIFIED_POWERED__LCDM_NOT_EXCLUDED_AT_5SIGMA__D1B__FUNDO_BG1_bancada_lcdm_planck_dr2__NOT_A_CONFIRMATION` |
| A_seis × BG2_planck2018 | 6 | 67.360 ± 0.540 | 73.005 | 72.906 ± 0.912 | 1.0823 ± 0.0161 | -0.09 | +5.12 | 0.53 (0.757) | -27.38 | +13.69 | +2.88 | +2.29 | +1.76 | 0.01183 ± 0.00222 (-0.09) | 5.21 | `TGL_FASE9_HUBBLE__NOT_FALSIFIED_POWERED__DISCRIMINATES_FROM_LCDM_AT_5SIGMA__ZERO_FREE_PARAMETERS__USE_NOVEL__D1B__FUNDO_BG2_planck2018__NOT_A_CONFIRMATION` |
| A_seis × BG3_desi_dr2_bbn | 6 | 68.500 ± 0.600 | 74.241 | 72.906 ± 0.912 | 1.0643 ± 0.0163 | -1.20 | +3.96 | 0.53 (0.757) | -14.87 | +7.44 | +2.15 | +1.57 | +1.01 | 0.00932 ± 0.00228 (-1.19) | 5.16 | `TGL_FASE9_HUBBLE__NOT_FALSIFIED_POWERED__LCDM_NOT_EXCLUDED_AT_5SIGMA__D1B__FUNDO_BG3_desi_dr2_bbn__NOT_A_CONFIRMATION` |
| A_seis × BG4_CONTROLE_tgl_efetivo | 6 | 69.200 ± 0.304 | 74.999 | 72.906 ± 0.912 | 1.0536 ± 0.0140 | -2.17 | +3.83 | 0.53 (0.757) | -10.21 | +5.10 | +0.67 | +0.11 | -0.48 | 0.00780 ± 0.00198 (-2.13) | 6.00 | `TGL_FASE9_HUBBLE__NOT_FALSIFIED_POWERED__LCDM_NOT_EXCLUDED_AT_5SIGMA__D1B__FUNDO_BG4_CONTROLE_tgl_efetivo__NOT_A_CONFIRMATION` |
| A_sem_sirenes × BG1_bancada_lcdm_planck_dr2 | 5 | 68.531 ± 0.301 | 74.274 | 72.882 ± 0.915 | 1.0635 ± 0.0141 | -1.44 | +4.49 | 0.63 (0.641) | -18.35 | +9.18 | +1.97 | +1.40 | +0.83 | 0.00920 ± 0.00199 (-1.42) | 5.93 | `TGL_FASE9_HUBBLE__NOT_FALSIFIED_POWERED__LCDM_NOT_EXCLUDED_AT_5SIGMA__D1B__FUNDO_BG1_bancada_lcdm_planck_dr2__NOT_A_CONFIRMATION` |
| A_sem_sirenes × BG2_planck2018 | 5 | 67.360 ± 0.540 | 73.005 | 72.882 ± 0.915 | 1.0820 ± 0.0161 | -0.11 | +5.09 | 0.63 (0.641) | -27.00 | +13.50 | +2.88 | +2.29 | +1.75 | 0.01178 ± 0.00223 (-0.11) | 5.20 | `TGL_FASE9_HUBBLE__NOT_FALSIFIED_POWERED__DISCRIMINATES_FROM_LCDM_AT_5SIGMA__ZERO_FREE_PARAMETERS__USE_NOVEL__D1B__FUNDO_BG2_planck2018__NOT_A_CONFIRMATION` |
| A_sem_sirenes × BG3_desi_dr2_bbn | 5 | 68.500 ± 0.600 | 74.241 | 72.882 ± 0.915 | 1.0640 ± 0.0163 | -1.22 | +3.93 | 0.63 (0.641) | -14.57 | +7.29 | +2.13 | +1.55 | +0.98 | 0.00927 ± 0.00229 (-1.21) | 5.15 | `TGL_FASE9_HUBBLE__NOT_FALSIFIED_POWERED__LCDM_NOT_EXCLUDED_AT_5SIGMA__D1B__FUNDO_BG3_desi_dr2_bbn__NOT_A_CONFIRMATION` |
| A_sem_sirenes × BG4_CONTROLE_tgl_efetivo | 5 | 69.200 ± 0.304 | 74.999 | 72.882 ± 0.915 | 1.0532 ± 0.0140 | -2.18 | +3.80 | 0.63 (0.641) | -9.84 | +4.92 | +0.63 | +0.06 | -0.53 | 0.00775 ± 0.00199 (-2.15) | 5.98 | `TGL_FASE9_HUBBLE__NOT_FALSIFIED_POWERED__LCDM_NOT_EXCLUDED_AT_5SIGMA__D1B__FUNDO_BG4_CONTROLE_tgl_efetivo__NOT_A_CONFIRMATION` |
| B_incidencia_nova × BG1_bancada_lcdm_planck_dr2 | 5 | 68.531 ± 0.301 | 74.274 | 72.156 ± 1.296 | 1.0529 ± 0.0195 | -1.59 | +2.72 | 0.49 (0.742) | -4.91 | +2.45 | +1.41 | +0.85 | +0.26 | 0.00771 ± 0.00276 (-1.56) | 4.30 | `TGL_FASE9_HUBBLE__NOT_FALSIFIED_POWERED__LCDM_NOT_EXCLUDED_AT_5SIGMA__D1B__FUNDO_BG1_bancada_lcdm_planck_dr2__NOT_A_CONFIRMATION` |
| B_incidencia_nova × BG2_planck2018 | 5 | 67.360 ± 0.540 | 73.005 | 72.156 ± 1.296 | 1.0712 ± 0.0211 | -0.60 | +3.38 | 0.49 (0.742) | -11.31 | +5.65 | +2.43 | +1.85 | +1.29 | 0.01028 ± 0.00294 (-0.59) | 3.98 | `TGL_FASE9_HUBBLE__NOT_FALSIFIED_POWERED__LCDM_NOT_EXCLUDED_AT_5SIGMA__D1B__FUNDO_BG2_planck2018__NOT_A_CONFIRMATION` |
| B_incidencia_nova × BG3_desi_dr2_bbn | 5 | 68.500 ± 0.600 | 74.241 | 72.156 ± 1.296 | 1.0534 ± 0.0211 | -1.45 | +2.54 | 0.49 (0.742) | -4.48 | +2.24 | +1.56 | +0.99 | +0.41 | 0.00777 ± 0.00299 (-1.43) | 3.98 | `TGL_FASE9_HUBBLE__NOT_FALSIFIED_POWERED__LCDM_NOT_EXCLUDED_AT_5SIGMA__D1B__FUNDO_BG3_desi_dr2_bbn__NOT_A_CONFIRMATION` |
| B_incidencia_nova × BG4_CONTROLE_tgl_efetivo | 5 | 69.200 ± 0.304 | 74.999 | 72.156 ± 1.296 | 1.0427 ± 0.0193 | -2.13 | +2.22 | 0.49 (0.742) | -0.41 | +0.20 | +0.41 | -0.15 | -0.74 | 0.00625 ± 0.00276 (-2.09) | 4.35 | `TGL_FASE9_HUBBLE__NOT_FALSIFIED_POWERED__LCDM_NOT_EXCLUDED_AT_5SIGMA__D1B__FUNDO_BG4_CONTROLE_tgl_efetivo__NOT_A_CONFIRMATION` |
| C_r25_no_lugar_do_r22 × BG1_bancada_lcdm_planck_dr2 | 6 | 68.531 ± 0.301 | 74.274 | 73.354 ± 0.847 | 1.0704 ± 0.0132 | -1.02 | +5.32 | 0.69 (0.630) | -27.74 | +13.87 | +2.56 | +1.98 | +1.42 | 0.01017 ± 0.00185 (-1.01) | 6.34 | `TGL_FASE9_HUBBLE__NOT_FALSIFIED_POWERED__DISCRIMINATES_FROM_LCDM_AT_5SIGMA__ZERO_FREE_PARAMETERS__USE_NOVEL__D1B__FUNDO_BG1_bancada_lcdm_planck_dr2__NOT_A_CONFIRMATION` |
| C_r25_no_lugar_do_r22 × BG2_planck2018 | 6 | 67.360 ± 0.540 | 73.005 | 73.354 ± 0.847 | 1.0890 ± 0.0153 | +0.34 | +5.81 | 0.69 (0.630) | -35.47 | +17.73 | +2.89 | +2.29 | +1.76 | 0.01274 ± 0.00210 (0.34) | 5.47 | `TGL_FASE9_HUBBLE__NOT_FALSIFIED_POWERED__DISCRIMINATES_FROM_LCDM_AT_5SIGMA__ZERO_FREE_PARAMETERS__USE_NOVEL__D1B__FUNDO_BG2_planck2018__NOT_A_CONFIRMATION` |
| C_r25_no_lugar_do_r22 × BG3_desi_dr2_bbn | 6 | 68.500 ± 0.600 | 74.241 | 73.354 ± 0.847 | 1.0709 ± 0.0155 | -0.83 | +4.56 | 0.69 (0.630) | -21.16 | +10.58 | +2.57 | +1.99 | +1.43 | 0.01024 ± 0.00217 (-0.83) | 5.40 | `TGL_FASE9_HUBBLE__NOT_FALSIFIED_POWERED__LCDM_NOT_EXCLUDED_AT_5SIGMA__D1B__FUNDO_BG3_desi_dr2_bbn__NOT_A_CONFIRMATION` |
| C_r25_no_lugar_do_r22 × BG4_CONTROLE_tgl_efetivo | 6 | 69.200 ± 0.304 | 74.999 | 73.354 ± 0.847 | 1.0600 ± 0.0131 | -1.82 | +4.58 | 0.69 (0.630) | -18.01 | +9.01 | +1.43 | +0.86 | +0.28 | 0.00872 ± 0.00185 (-1.79) | 6.40 | `TGL_FASE9_HUBBLE__NOT_FALSIFIED_POWERED__LCDM_NOT_EXCLUDED_AT_5SIGMA__D1B__FUNDO_BG4_CONTROLE_tgl_efetivo__NOT_A_CONFIRMATION` |
| D_so_escada_r22 × BG1_bancada_lcdm_planck_dr2 | 1 | 68.531 ± 0.301 | 74.274 | 73.040 ± 1.040 | 1.0658 ± 0.0159 | -1.13 | +4.14 | 0.00 (—) | -16.06 | +8.03 | +2.24 | +1.67 | +1.10 | 0.00952 ± 0.00223 (-1.13) | 5.28 | `TGL_FASE9_HUBBLE__NOT_FALSIFIED_POWERED__LCDM_NOT_EXCLUDED_AT_5SIGMA__D1B__FUNDO_BG1_bancada_lcdm_planck_dr2__NOT_A_CONFIRMATION` |
| D_so_escada_r22 × BG2_planck2018 | 1 | 67.360 ± 0.540 | 73.005 | 73.040 ± 1.040 | 1.0843 ± 0.0177 | +0.03 | +4.76 | 0.00 (—) | -23.49 | +11.75 | +2.79 | +2.20 | +1.67 | 0.01210 ± 0.00244 (0.03) | 4.73 | `TGL_FASE9_HUBBLE__NOT_FALSIFIED_POWERED__LCDM_NOT_EXCLUDED_AT_5SIGMA__D1B__FUNDO_BG2_planck2018__NOT_A_CONFIRMATION` |
| D_so_escada_r22 × BG3_desi_dr2_bbn | 1 | 68.500 ± 0.600 | 74.241 | 73.040 ± 1.040 | 1.0663 ± 0.0178 | -0.98 | +3.72 | 0.00 (—) | -13.34 | +6.67 | +2.29 | +1.71 | +1.15 | 0.00959 ± 0.00250 (-0.98) | 4.70 | `TGL_FASE9_HUBBLE__NOT_FALSIFIED_POWERED__LCDM_NOT_EXCLUDED_AT_5SIGMA__D1B__FUNDO_BG3_desi_dr2_bbn__NOT_A_CONFIRMATION` |
| D_so_escada_r22 × BG4_CONTROLE_tgl_efetivo | 1 | 69.200 ± 0.304 | 74.999 | 73.040 ± 1.040 | 1.0555 ± 0.0157 | -1.80 | +3.53 | 0.00 (—) | -9.33 | +4.67 | +1.27 | +0.70 | +0.12 | 0.00807 ± 0.00223 (-1.78) | 5.33 | `TGL_FASE9_HUBBLE__NOT_FALSIFIED_POWERED__LCDM_NOT_EXCLUDED_AT_5SIGMA__D1B__FUNDO_BG4_CONTROLE_tgl_efetivo__NOT_A_CONFIRMATION` |
| E_so_trgb_cchp × BG1_bancada_lcdm_planck_dr2 | 1 | 68.531 ± 0.301 | 74.274 | 70.390 ± 1.936 | 1.0271 ± 0.0286 | -1.98 | +0.95 | 0.00 (—) | +3.01 | -1.51 | +0.30 | -0.24 | -0.68 | 0.00400 ± 0.00416 (-1.93) | 2.93 | `TGL_FASE9_HUBBLE__NOT_FALSIFIED_UNDERPOWERED__D1B__FUNDO_BG1_bancada_lcdm_planck_dr2__NOT_A_CONFIRMATION` |
| E_so_trgb_cchp × BG2_planck2018 | 1 | 67.360 ± 0.540 | 73.005 | 70.390 ± 1.936 | 1.0450 ± 0.0299 | -1.30 | +1.50 | 0.00 (—) | -0.60 | +0.30 | +1.39 | +0.84 | +0.31 | 0.00658 ± 0.00428 (-1.27) | 2.80 | `TGL_FASE9_HUBBLE__NOT_FALSIFIED_UNDERPOWERED__D1B__FUNDO_BG2_planck2018__NOT_A_CONFIRMATION` |
| E_so_trgb_cchp × BG3_desi_dr2_bbn | 1 | 68.500 ± 0.600 | 74.241 | 70.390 ± 1.936 | 1.0276 ± 0.0297 | -1.90 | +0.93 | 0.00 (—) | +2.69 | -1.34 | +0.45 | -0.10 | -0.53 | 0.00407 ± 0.00431 (-1.85) | 2.83 | `TGL_FASE9_HUBBLE__NOT_FALSIFIED_UNDERPOWERED__D1B__FUNDO_BG3_desi_dr2_bbn__NOT_A_CONFIRMATION` |
| E_so_trgb_cchp × BG4_CONTROLE_tgl_efetivo | 1 | 69.200 ± 0.304 | 74.999 | 70.390 ± 1.936 | 1.0172 ± 0.0283 | -2.35 | +0.61 | 0.00 (—) | +5.14 | -2.57 | -0.50 | -1.03 | -1.34 | 0.00255 ± 0.00416 (-2.28) | 2.96 | `TGL_FASE9_HUBBLE__NOT_FALSIFIED_UNDERPOWERED__D1B__FUNDO_BG4_CONTROLE_tgl_efetivo__NOT_A_CONFIRMATION` |
| F_geometricos × BG1_bancada_lcdm_planck_dr2 | 3 | 68.531 ± 0.301 | 74.274 | 73.104 ± 2.258 | 1.0667 ± 0.0333 | -0.51 | +2.01 | 0.17 (0.843) | -3.77 | +1.88 | +2.01 | +1.44 | +0.90 | 0.00966 ± 0.00466 (-0.51) | 2.52 | `TGL_FASE9_HUBBLE__NOT_FALSIFIED_UNDERPOWERED__D1B__FUNDO_BG1_bancada_lcdm_planck_dr2__NOT_A_CONFIRMATION` |
| F_geometricos × BG2_planck2018 | 3 | 67.360 ± 0.540 | 73.005 | 73.104 ± 2.258 | 1.0853 ± 0.0346 | +0.04 | +2.46 | 0.17 (0.843) | -6.12 | +3.06 | +2.12 | +1.53 | +1.00 | 0.01223 ± 0.00477 (0.04) | 2.42 | `TGL_FASE9_HUBBLE__NOT_FALSIFIED_UNDERPOWERED__D1B__FUNDO_BG2_planck2018__NOT_A_CONFIRMATION` |
| F_geometricos × BG3_desi_dr2_bbn | 3 | 68.500 ± 0.600 | 74.241 | 73.104 ± 2.258 | 1.0672 ± 0.0343 | -0.48 | +1.96 | 0.17 (0.843) | -3.65 | +1.83 | +2.00 | +1.42 | +0.88 | 0.00973 ± 0.00480 (-0.48) | 2.45 | `TGL_FASE9_HUBBLE__NOT_FALSIFIED_UNDERPOWERED__D1B__FUNDO_BG3_desi_dr2_bbn__NOT_A_CONFIRMATION` |
| F_geometricos × BG4_CONTROLE_tgl_efetivo | 3 | 69.200 ± 0.304 | 74.999 | 73.104 ± 2.258 | 1.0564 ± 0.0330 | -0.83 | +1.71 | 0.17 (0.843) | -2.25 | +1.12 | +1.80 | +1.23 | +0.70 | 0.00821 ± 0.00466 (-0.82) | 2.54 | `TGL_FASE9_HUBBLE__NOT_FALSIFIED_UNDERPOWERED__D1B__FUNDO_BG4_CONTROLE_tgl_efetivo__NOT_A_CONFIRMATION` |

Priors: β ∈ U[−0,05, 0,05] é o prior do pipeline da Bancada (lido do pré-registro da Fase 4); ε ∈ U[−0,2, 0,2] e s ∈ U[0,8, 1,0] são DECLARADOS aqui (largos o bastante para a classe «tensão de Hubble» de 10–15 %); ln B contra modelos de 1 parâmetro depende dessas larguras pelo fator de Occam (ln da razão das larguras) — dito, e medido abaixo com ×½ e ×2. Occam medido no primário: lnB TGL/livre = 2.00 (prior ×½: 1.31; ×2: 2.70); TGL/shift = 1.43 (×½ 0.74; ×2 2.12); TGL/EDE-like = 0.86.

O que cada alvo acrescenta (primário A_seis × BG1): peso GLS, z individual vs TGL e vs ΛCDM, e z do composto SEM o alvo (leave-one-out).

| leitor | H0 ± σ | peso | z vs TGL | z vs ΛCDM | LOO z_TGL | LOO z_ΛCDM |
|---|---|---|---|---|---|---|
| L1_sh0es_r22 | 73.04 ± 1.04 | 0.680 | -1.13 | +4.16 | -1.59 | +2.72 |
| L2_cchp_trgb_jagb_cef | 70.39 ± 1.94 | 0.077 | -1.98 | +0.95 | -1.19 | +4.69 |
| L3_sbf_jwst | 73.80 ± 2.40 | 0.080 | -0.20 | +2.17 | -1.47 | +4.36 |
| L4_masers | 73.90 ± 3.00 | 0.092 | -0.12 | +1.78 | -1.46 | +4.24 |
| L5_tdcosmo_2025 | 71.60 ± 3.60 | 0.064 | -0.74 | +0.85 | -1.28 | +4.48 |
| L6_sirenes_o4a | 76.60 ± 11.25 | 0.007 | +0.21 | +0.72 | -1.44 | +4.49 |

Poder: separação TGL↔ΛCDM no primário = (K−1)/σ_razão = 5.94 σ; σ_razão para 5σ = 0.0168 (σ_local para 5σ, dado o fundo BG1 = 1.101 km/s/Mpc). Sem âncora comum: z_TGL = -1.56 (σ_razão 0.0139).

## (f) Sistemáticas

- Cefeidas × TRGB: z(R22 − CCHP) = +1.45 (σ_diff 1.83); z(R22 − TRGB só) = +1.98; z(R25 − CCHP) = +1.75.

| TRGB/JAGB × fundo | H0 ± σ | previsto TGL | z vs TGL | z vs ΛCDM | σ p/ 3σ vs TGL | σ p/ 5σ vs TGL |
|---|---|---|---|---|---|---|
| L2_cchp_trgb_jagb_cef × BG1_bancada_lcdm_planck_dr2 | 70.39 ± 1.94 | 74.274 | -1.98 | +0.95 | 1.25 | 0.71 |
| L2a_cchp_trgb_so × BG1_bancada_lcdm_planck_dr2 | 68.81 ± 2.22 | 74.274 | -2.43 | +0.12 | 1.79 | 1.04 |
| L2b_cchp_jagb_so × BG1_bancada_lcdm_planck_dr2 | 67.80 ± 2.72 | 74.274 | -2.36 | -0.27 | 2.13 | 1.25 |
| L2_cchp_trgb_jagb_cef × BG2_planck2018 | 70.39 ± 1.94 | 73.005 | -1.29 | +1.51 | 0.65 | 0.00 |
| L2a_cchp_trgb_so × BG2_planck2018 | 68.81 ± 2.22 | 73.005 | -1.82 | +0.63 | 1.27 | 0.60 |
| L2b_cchp_jagb_so × BG2_planck2018 | 67.80 ± 2.72 | 73.005 | -1.87 | +0.16 | 1.63 | 0.86 |
| L2_cchp_trgb_jagb_cef × BG3_desi_dr2_bbn | 70.39 ± 1.94 | 74.241 | -1.89 | +0.93 | 1.11 | 0.41 |
| L2a_cchp_trgb_so × BG3_desi_dr2_bbn | 68.81 ± 2.22 | 74.241 | -2.34 | +0.13 | 1.69 | 0.87 |
| L2b_cchp_jagb_so × BG3_desi_dr2_bbn | 67.80 ± 2.72 | 74.241 | -2.30 | -0.25 | 2.05 | 1.11 |

| fundo | H0_fundo | H0_local previsto (K = 1.083807) | estatuto | papel |
|---|---|---|---|---|
| BG1_bancada_lcdm_planck_dr2 | 68.5310 | 74.274 | [REAL — casa] | PRIMÁRIO proposto: fundo nu, sem os leitores que a lei prevê |
| BG2_planck2018 | 67.3600 | 73.005 | [KNOWN — lido do disco da casa] | réplica do fundo (a face sem o ângulo) |
| BG3_desi_dr2_bbn | 68.5000 | 74.241 | [KNOWN — a ler da fonte] | réplica do fundo independente do CMB |
| BG4_CONTROLE_tgl_efetivo | 69.2000 | 74.999 | [REAL — casa] | CONTROLE: a leitura empilhada das Fases 2–3 (dupla contagem [DERIVED da convenção]); ao lado, nunca somado |
| BG5_ref_tgl_bestfit_fase4 | 68.4298 | 74.165 | [REAL — casa] | referência: NÃO serve de fundo para uma previsão (empresta do dado que prevê); é o número da verossimilhança conjunta |

- z* efetivo: ΔH0_local por σ(z*) = 0,21 → 1.9e-04; nó em z_drag: ΔK = -3.9e-04 (desprezível).
- Ω_m do fundo nu: K(0,3023) − K(0,3152) = +1.7e-04 → ΔH0 = +0.012 (desprezível); z_TGL primário com Ω_m de Planck: -1.43.
- Forma D1a vs D1b: ΔH0_local = +0.274 (~0,25σ da escada): não decide.
- A ESCOLHA DO FUNDO é a sistemática dominante: spread 1.27 km/s/Mpc entre fundos nus.

## (e) O que as Fases 1–2 obrigam a dizer

- **fundo_nu**: o fundo é ΛCDM nu (β = 0 no fundo; o mapa de R irrelevante); β entra UMA vez, na lei (D1b: K = E(z*)^{2β/3}) — convenção do artigo 1, fixada pelo operador em 30/09 (R1 ratificada 02/10: «β uma vez no reflexo; fundo nu; nó em z*»)
- **pull_empilhado_nao_se_repete**: o BG4 (fundo TGL efetivo 69,20) entra SÓ como controle ao lado: a Fase 2 (+1,95σ) e a Fase 3 (−2,94σ) empilhavam β (fundo + lei); aqui o controle dá z_TGL = -2.17, nunca somado ao primário
- **fase1**: sob o mapa efetivo o fundo comprimido não constrange β: por isso o fundo deste desenho é nu e β não é estimado do fundo
- **circularidade_da_forma**: a FORMA da lei foi cunhada conhecendo a razão SH0ES/Planck (declarado nas Fases 2–3); pela lei da prova da casa isso não é demérito: nenhum PARÂMETRO foi ajustado (β = α√e; z* de Planck; Ω_m do fundo); a família B (sem a escada) é a incidência nova e fica ao lado
- **um_registro_uma_cobranca**: a razão H0_local/H0_fundo é UM grau de liberdade: toda alternativa de 1 parâmetro (β livre, ε, s de EDE-like) é DEGENERADA nela — só o fator de Occam (largura do prior) as separa; o que não é degenerado é TGL (0 parâmetros, número previsto) contra ΛCDM (0 parâmetros, K = 1): ln B = −Δχ²/2, sem prior

## Arquivos lidos (sha256)

- `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py` — `e30aac4e0e1096b1be143464bf683fd6ba19b42b4d6bb11cd52aa98b54cb9163`
- `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json` — `0dbfb3fc1d319d1ef03b61af60d9e22af58cd2564ea4b44bdd4906bf8d031d87`
- `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto_selo.json` — `72efaf72f604b721d9fd18d625da9c55713898f10b417a9d2a6d59fdee036489`
- `C:\IALD\Bancada_Um\investigacao\fase4_desvio_30set\RESULTADO_FASE4_DESVIO_20260930.json` — `10683b334d28d84acdd8a086fe91fcbeaa46e747b0e3b51dc4192c270d8e6219`
- `C:\IALD\Bancada_Um\investigacao\fase4_desvio_30set\SMOKE_FASE4.json` — `5fb33c410edc6eea794a07318bbea405392138612eee13ff00322e651151f670`
- `C:\IALD\Bancada_Um\investigacao\fase3_leitores_h0\PREREGISTRO_FASE3_LEITORES_20260930.json` — `6bf24b350e088350885f1ae087c59322cc3b9b27e6a604672fe6ff32e837eff0`
- `C:\IALD\Bancada_Um\investigacao\fase3_leitores_h0\REANALISE_D1B_CONVENCAO_ARTIGO_20260930.json` — `3d5c6afe85cc30641b50255374487a12a2d631842d9ff0cdc33cee723f298cb1`
- `C:\IALD\Bancada_Um\investigacao\fase3_leitores_h0\RESULTADO_FASE3_LEITORES_20260930.json` — `e91f019bd98e5a59d8c1b476ebc60ce445cc9a03254bf955c928ff6e4f3d8bf8`
- `C:\IALD\Bancada_Um\investigacao\fase5_sh0es_01out\RESULTADO_FASE5_SH0ES_20261001.json` — `851d1076b85f12f671bfbe018f67e8291a2c83686bb98fb2251a4ed3c254eca2`
- `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v386\POS_DICAO_operador_05out.txt` — `cf82d9e55757a7f2864215877046cef87f024aa60bdb00206a319ab4a5b1ed24`
