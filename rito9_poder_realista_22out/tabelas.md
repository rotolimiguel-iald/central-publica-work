### A. n_req (neutrinos detectados necessarios; oraculo) por familia e ell: minimo / mediana / maximo

| familia | ell = 10 km | ell = 20 km | ell = 30 km |
|---|---|---|---|
| P1 | 2 / 6 / 14 | 2 / 3 / 5 | 1 / 2 / 3 |
| P2 | 13 / 69 / 284 | 12 / 50 / 162 | 11 / 42 / 131 |
| P3 | 2 / 3 / 3 | 1 / 2 / 2 | 1 / 1 / 1 |
| REF_ESQUELETO | 2 / 24 / 321 | 1 / 7 / 73 | 1 / 4 / 30 |
| SENS_VETO | 4 / 5 / 8 | 3 / 4 / 7 | 3 / 4 / 7 |
| SENS_ZERO | 9 / 208 / 744 | 3 / 142 / 299 | 2 / 117 / 198 |

### B. P2 (ell = 20 km): n_req min–max sobre as 16 formas de surto, por (tau, f)

| tau (ms) | f = 0.5 | f = 0.8 |
|---|---|---|
| 30 | 28–55 (med 41) | 85–120 (med 109) |
| 100 | 22–51 (med 34) | 87–162 (med 128) |
| 300 | 16–41 (med 25) | 63–142 (med 97) |
| 1000 | 12–32 (med 18) | 42–106 (med 66) |

P2, mesma tabela para ell = 10 e 30 km (min–max sobre a forma do surto):

| ell | tau (ms) | f = 0.5 | f = 0.8 |
|---|---|---|---|
| 10 | 30 | 32–99 | 116–227 |
| 10 | 100 | 23–92 | 95–284 |
| 10 | 300 | 17–77 | 65–247 |
| 10 | 1000 | 13–63 | 44–201 |
| 30 | 30 | 26–43 | 68–85 |
| 30 | 100 | 22–41 | 82–131 |
| 30 | 300 | 16–33 | 63–117 |
| 30 | 1000 | 11–25 | 42–87 |

### C. Melhor e pior caso por familia realista e ell

| familia | ell | melhor caso | n_req | pior caso | n_req |
|---|---|---|---|---|---|
| P1 | 10 | K3_S14_G1_damped | 2 | K4_S14_G2_damped | 14 |
| P1 | 20 | K3_S10_G1_damped | 2 | K4_S14_G2_damped | 5 |
| P1 | 30 | K3_S10_G1_flat | 1 | K3_S14_G2_damped | 3 |
| P2 | 10 | K3_S14_G1_damped_tau1000_f0.5 | 13 | K4_S10_G2_flat_tau100_f0.8 | 284 |
| P2 | 20 | K3_S10_G1_flat_tau1000_f0.5 | 12 | K4_S14_G2_flat_tau100_f0.8 | 162 |
| P2 | 30 | K3_S14_G1_damped_tau1000_f0.5 | 11 | K4_S14_G2_damped_tau100_f0.8 | 131 |

### D. Bancada REF (H0 = N(0, sigma_e) do esqueleto do Kimi): criterio EXATO x CLT do esqueleto

| ell (km) | sigma_e (ms) | n_req exato (este estudo) | n_5sigma LLR-CLT (esqueleto) | n_5sigma media (esqueleto) |
|---|---|---|---|---|
| 10 | 0.5 | 2 | 1 | 27 |
| 10 | 1 | 4 | 1 | 29 |
| 10 | 3 | 24 | 12 | 56 |
| 10 | 10 | 321 | 296 | 359 |
| 20 | 0.5 | 1 | 1 | 26 |
| 20 | 1 | 2 | 1 | 27 |
| 20 | 3 | 7 | 2 | 33 |
| 20 | 10 | 73 | 56 | 109 |
| 30 | 0.5 | 1 | 1 | 26 |
| 30 | 1 | 1 | 1 | 26 |
| 30 | 3 | 4 | 1 | 29 |
| 30 | 10 | 30 | 17 | 63 |

### E. Sensibilidades (fora do veredito)

SENS_VETO (surto K3_S10_G1_damped + cauda tau = 100 ms com fracao f; f = 0 e o P1 puro):

| f (cauda) | ell = 10 | ell = 20 | ell = 30 | q1_sat (H1 em regiao 'impossivel' sob H0), ell = 20 |
|---|---|---|---|---|
| 0 (P1) | 3 | 2 | 2 | 0.207 |
| 0.001 | 4 | 3 | 3 | 0 |
| 0.01 | 5 | 4 | 4 | 0 |
| 0.1 | 8 | 7 | 7 | 0 |

SENS_ZERO (ponto-zero conhecido so a menos de N(0, sigma_off^2) por evento; surto K4_S10_G1_damped):

| sigma_off (ms) | P1-like ell=10 | ell=20 | ell=30 | P2-like (tau=100, f=0.8) ell=10 | ell=20 | ell=30 |
|---|---|---|---|---|---|---|
| 0 (oraculo) | 6 | 3 | 2 | 126 | 107 | 96 |
| 0.5 | 9 | 3 | 2 | 208 | 142 | 117 |
| 1 | 16 | 4 | 3 | 325 | 176 | 134 |
| 2 | 33 | 8 | 4 | 441 | 209 | 151 |
| 4 | 78 | 17 | 8 | 744 | 299 | 198 |

### F. A parede instrumental (Kyutoku–Kashiyama), em funcao de n_req — 1 Mt, R = 1 Mpc^-3 Myr^-1, D_eff = 200 Mpc

| caso | ell | n_req | fusoes ate 200 Mpc | exposicao (Mt ano) | D_max de UM evento (Mpc) | massa p/ 10 eventos (Mt) | fator acima do alcance |
|---|---|---|---|---|---|---|---|
| P1 K3_S14_G1_damped | 10 | 2 | 5.000 | 160 | 1.77 | 500 | 500 |
| P1 K3_S10_G1_damped | 20 | 2 | 5.000 | 160 | 1.77 | 500 | 500 |
| P1 K3_S10_G1_flat | 30 | 1 | 2.500 | 80 | 2.50 | 250 | 250 |
| P2 K3_S14_G1_damped_tau1000_f0.5 | 10 | 13 | 32.500 | 1.040 | 0.69 | 3.250 | 3.250 |
| P2 K3_S10_G1_flat_tau1000_f0.5 | 20 | 12 | 30.000 | 960 | 0.72 | 3.000 | 3.000 |
| P2 K3_S14_G1_damped_tau1000_f0.5 | 30 | 11 | 27.500 | 880 | 0.75 | 2.750 | 2.750 |
| P3 G1 | 10 | 2 | 5.000 | 160 | 1.77 | 500 | 500 |
| P3 G1 | 20 | 1 | 2.500 | 80 | 2.50 | 250 | 250 |
| P3 G1 | 30 | 1 | 2.500 | 80 | 2.50 | 250 | 250 |

(melhor caso = menor n_req dentro de cada familia e ell; P3 mostrado so para registro: o rendimento real e MENOR — ver texto.)

### G. Verificacoes numericas

- Simulacao por amostragem por importancia (M = 200000 por ponto, semente 20261022): 61 pontos em 33 casos; todos dentro da tolerancia: True; max |c_MC - c_rede| = 0.022 (tol 0.35); max |poder_MC - poder_rede| = 0.0026.
- Robustez numerica (cap 60; passo da rede / 2): 66 comparacoes; todas dentro da tolerancia: True; max |n_req - n_req_base| = 0; max |c - c_base| = 0.0050.
- Gates do veredito: testes_nucleo_passaram=True; numero_de_casos=True; sem_falha_numerica=True; poder_monotono=True; massa_residual=True; janela_sem_vazamento=True; limiar_respeita_limite_de_Wald=True; mc_linhas_minimas=True; mc_dentro_da_tolerancia=True; robustez_linhas_minimas=True; robustez_dentro_da_tolerancia=True
