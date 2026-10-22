RITO 9 — PODER REALISTA — 22/10

**Estatuto: SYNTHETIC_DIAGNOSTIC_ONLY.** Nenhum dado observacional; `observed_sigma = null`; nada aqui afirma coisa alguma sobre a natureza (sintético ≠ observado). Etiquetas: [REAL] calculado aqui · [KNOWN] literatura citada · [DECLARADO] afirmado na fonte, não verificado aqui · [INPUT] escolha pré-registrada · [OPEN] em aberto. Ordem: gerência c1 (22/10, «falta rodarmos o teste agora, coisa que é com você»). Feito por Claude (subagente Sonnet 5.5), só em `work\rito9_poder_realista_22out`; fontes, Nós, `um.py`, caderno do Kimi, mapa, quadro, memória, túnel, site e git: só leitura ou intocados.

## 1. Veredito

**`UNDERPOWERED_WALL_MEASURED`** — aplicado o `veredito.py` pinado (sha256 `741453da779d3c4bd747623e206d278bc250d6aca7eb4bf715be33dcaeaf63ff`), sem mudar limiar. [REAL]

- Regra pré-registrada: `POWERED_BNS` só se alguma família realista (P1/P2) tiver n_req ≤ N_alcançável = 10 eventos ÷ 2.500 fusões por neutrino esperado = **0,004** neutrino esperado (Kyutoku–Kashiyama, detector de 1 Mt, até 200 Mpc).
- Menor n_req medido (oráculo): **1** no perfil idealizado P1 («só o surto») e **11** nas curvas P2 (surto + resfriamento) — **250× e 2.750× acima do alcance**. Intervalos: P1 = 1–14; P2 = 11–284 (mediana em ℓ = 20 km: 50); P3 (fora do veredito) = 1–3.
- Portas numéricas: 11 de 11 passaram (testes analíticos, 0 falhas em 483 casos, monotonia, massa, limite de Wald, simulação por importância, robustez).

**Em uma linha:** mesmo com o oráculo (H0 totalmente conhecido = limite superior do poder), a arena BNS precisa de ≥ 11 neutrinos detectados com a emissão realista (≥ 1 só no perfil idealizado), e a projeção K–K entrega 1 neutrino térmico por ~2.500 fusões: ≥ 27.500 fusões até 200 Mpc (≈ 880 anos de detector de 1 Mt) ou UM evento a ≤ 0,75 Mpc. A parede está medida: a dominante é instrumental (taxa × massa — já n = 1 custa 2.500 fusões), e a estatística da emissão realista a multiplica por 11–284.

## 2. O que foi pré-registrado antes de rodar (PREREGISTRO.json sha256 `720f3dbcbcb04a383f567e3022c05022a5fadecaa52a2773225f93c835cbfbd2`; PINS.json sha256 `af3dfda1675dab694687fd8e83b58383263a0f1f973e07bf20dbeb3c4a328115`)

- **H1 = H0 ⊛ K_β(ℓ)**, K_β = espera geométrica do excesso, atraso (N−1)·ℓ/c, N ~ Geom(β); ℓ ∈ {10, 20, 30} km [INPUT]; **β = SEALED_CODATA_ALPHA·√e lido por script** do `um.py` instalado no Nós (só leitura; linha 95, `SEALED_CODATA_ALPHA = 7.2973525693e-3`; sha256 do `um.py` na leitura `8918b17803792cf2725e69221718a974a15ebb7e6dc77aac008d609782bdd8fb`): β = 0,012031300400803142 (runtime; nunca literal). Média do atraso = ℓ(1−β)/(cβ) = 2,74 / 5,48 / 8,22 ms para ℓ = 10 / 20 / 30 km.
- **Discretização exata:** células de largura τ₀ = ℓ/c; como o atraso é múltiplo de τ₀, P1ᵢ = Σₖ β(1−β)ᵏ P0ᵢ₋ₖ vale exatamente (filtro de 1ª ordem). Resolução temporal ideal (τ₀ = 33–100 µs).
- **H0 (perfil de chegada de um neutrino detectado ∝ luminosidade × seção de choque; ⟨E⟩ ≈ constante):** famílias fixadas agora, envolvendo Cusinato et al. 2022 [KNOWN]: *3–4 picos bem definidos nos primeiros 10–15 ms* (p. 8), *primeiro pico sempre o mais alto* (p. 9), Γ típico ≈ 1 ms (p. 12), *PC: um pico baixo entre a fusão e 1 ms* (p. 8), decaimento exponencial β_ν ≈ 100 ms (e 100–400 ms para ν_x) (p. 14), resfriamento do MNS de vários segundos (p. 9), ventos ~100 ms (p. 2).
  - **P1** (só o surto): K ∈ {3,4} picos gaussianos de 1 ms até S ∈ {10, 14} ms, largura FWHM Γ ∈ {1, 2} ms, amplitudes decrescentes (r = 0,6) ou iguais — 16 perfis.
  - **P2** (surto + resfriamento): (1−f)·P1 + f·exp(−t/τ)/τ, τ ∈ {30, 100, 300, 1000} ms, f ∈ {0,5; 0,8} — 128 perfis. O balanço de energia de Cusinato (≈ 6×10⁵⁰ erg por pico, p. 12, contra ~10⁵²–10⁵³ erg no resfriamento, p. 9 e 14) sugere f ≈ 0,9–0,99: **f = 0,5 e 0,8 são generosos** (menos cauda = mais poder).
  - **P3** (colapso imediato): um pico em 0,5 ms, Γ ∈ {1, 2} ms. **Rendimento BAIXO** [KNOWN, Cusinato p. 8 e 12: pico de luminosidade até ~6× menor, E_peak «very low»]: as fusões reais para P3 seriam **mais** do que 2.500·n_req. Fora do veredito.
  - Bancadas **fora do veredito:** REF (H0 = N(0, σ_e) do esqueleto do Kimi, com o critério exato), SENS_VETO (cauda mínima sobre o surto), SENS_ZERO (ponto-zero conhecido só a menos de N(0, σ_off²) por evento).
- **Estatística:** LLR de forma completa com H0 conhecido (oráculo); limiar c_n = menor v com P0(Λ_n ≥ v) ≤ 1−Φ(5) = 2,8665×10⁻⁷, distribuição de Λ_n obtida por convolução n-vezes exata na rede de λ (FFT) **e verificada por simulação com amostragem por importância** (identidade exata P0(A) = E1[e^{−Λ}; A]; é o que torna possível estimar um quantil de 2,9×10⁻⁷ por simulação); n_req = menor n com P1(Λ_n ≥ c_n) ≥ 0,5 (mediana do LLR sob H1 ≥ limiar).
- **Veredito, exposição declarada e taxa** (K–K, arXiv:1710.05922v3, p. 1, 4, 5 [KNOWN]): 2.500 fusões ≤ 200 Mpc e ~80 Mt·ano por neutrino esperado, R = 1 Mpc⁻³ Myr⁻¹, detector de 1 Mt; N_ν(D) = 6,25×10⁻⁴·(M_T/1 Mt)·(100 Mpc/D)² (Eq. 6 com fE·fse·fosc = 0,625). Vereditos permitidos: POWERED_BNS · UNDERPOWERED_WALL_MEASURED · INCONCLUSIVE.
- **Antes do pino** (desenvolvimento, declarado): testes analíticos do núcleo (gaussiana de translação com solução fechada, filtro × pente, enumeração exata, exata × janela, invariantes, offset, simulação × exato); **4 rodadas do pipeline** (`dev_dry/saida1`, `saida2` ×2, `saida3`) e **1 cronometragem** de caso pesado, todas em perfis **fora** das famílias (K=2, S=7, Γ=1,5, τ=50, f=0,65, ℓ=15, σ_e=2; K=4, S=13, Γ=1,8, flat, τ=900, f=0,85, ℓ=11). *Errata ao lado:* o `PREREGISTRO.json` (já pinado) diz «dois ensaios do pipeline»; a contagem correta é a desta linha. O código também ganhou, nessa fase e antes do pino, as bancadas SENS_*, a porta do limite de Wald, a tabela de derivados K–K, a conferência do alfa lido e a guarda contra dobra de janela; e houve dois ajustes por falha de teste (a métrica de vazamento de janela passou a valer só no modo janela; a tolerância do teste de offset foi fixada em 10⁻⁴ do pico, erro esperado de O((τ₀/σ)²)). O único membro pré-registrado tocado antes do pino foi `P2|K4_S14_G2_damped_tau100_f0.8|ell20`, no teste de invariantes (massa, cota P1 ≥ βP0, média do atraso) — sem n_req nem poder. A rodada oficial correu **uma vez** (log em `rodada_oficial_stdout.txt`).

## 3. Resultados (dados crus: `saida_rodada/*.csv`; derivados K–K: `derivados_KK_por_caso.csv`)

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


## 4. As duas paredes [REAL, sintético]

1. **Parede estatística (o oráculo):** com a emissão realista (P2), o melhor caso (3 picos estreitos, Γ = 1 ms, + resfriamento de τ = 1 s, f = 0,5) já exige **11** neutrinos; a mediana em ℓ = 20 km é **50** e o pior caso chega a **284**. A razão é a informação por neutrino: em **todos os 384 casos P2, n_req · KL(H1‖H0) = 12,5–13,6** (≈ 5²/2 = 12,5, a relação de sinal fraco para 5σ com poder de 50%), e a cauda de resfriamento dilui KL por (1−f). O perfil P1 («só o surto») dá n_req = 1–14, mas isso é a **barreira de cauda gaussiana**: chegadas nos vales entre os picos e depois do último pico são «impossíveis» sob H0 (0,9%–40% da massa de H1, mediana 14%, cai em regiões onde H0 tem densidade < e⁻⁴⁰ da de H1); basta uma cauda de 0,1% do surto (SENS_VETO) para o n_req sair de 2 para 3, e de 10%, para 7 (ℓ = 20 km).
2. **Parede instrumental (K–K):** 1 neutrino térmico esperado exige ~2.500 fusões ≤ 200 Mpc (80 Mt·ano). Para o menor n_req realista em P2 (P2|K3_S14_G1_damped_tau1000_f0.5|ell30): **27.500 fusões**, **880 Mt·ano** (≈ 880 anos com 1 Mt), um detector de **2.750 Mt** para fechar em 10 eventos, ou **um único evento a ≤ 0,75 Mpc** (≈ a distância de M31, ~0,78 Mpc [KNOWN]); a taxa K–K dá ~1,8×10⁻⁴ evento por século dentro desse raio. Para a mediana de P2 em ℓ = 20 km (50 neutrinos): 125.000 fusões. Mesmo o caso idealizado P1 de menor n_req (P1|K3_S10_G1_flat|ell30, n = 1) pede 2.500 fusões (250× o alcance de 10 eventos).
3. **Leitura:** a arena BNS **não discrimina** no horizonte instrumental projetado (K–K 2018, [KNOWN] como projeção, não como inventário de 2026). Aumentar a precisão do modelo de emissão não remove a parede de taxa × massa; reduzi-la exige detector (ou tempo de exposição) ≳ 10³× maior, porque a incerteza na taxa de fusões é de ordem 1, não 10³ (K–K usam R = 1 Mpc⁻³ Myr⁻¹, abaixo da estimativa LVK de 2018, 1,54 +3,2/−1,22 [KNOWN, K–K p. 4]: mesmo o extremo superior (~4,7) ganharia ≲ 5×). O que o rito pode ainda dizer a partir de BNS é um limite de viabilidade registrado ex-ante, não um teste de 5σ.

## 5. O que o esqueleto do Kimi acertou e o que era artefato do CLT (tabela D)

[REAL] O **poder está na forma** (a média precisa de 26–359 neutrinos; a forma completa, de 1–321), como o esqueleto dizia. Mas o critério CLT do esqueleto **subestimou** n: com o limiar exato de 5σ, «1–2 neutrinos bastam» vale só para σ_e ≲ 0,5–1 ms e ℓ ≥ 20–30 km (n_exato = 1–2); em ℓ = 10 km sobe a 2–4, e para σ_e = 3 ms o esqueleto dizia 12 / 2 / 1 (ℓ = 10 / 20 / 30 km) enquanto o exato é 24 / 7 / 4. Conferência analítica independente do caso σ_e = 1 ms, ℓ = 20 km: o limiar de 5σ no tempo é t* = 5σ_e = 5 ms e P(atraso ≥ 5 ms) ≈ e^{−5/5,48} = 0,40 < 0,5 ⇒ n = 1 falha e n_req = 2 (a tabela D reproduz o valor).

## 6. Sensibilidades (fora do veredito; tabela E)

- **SENS_VETO:** o n_req do P1 é fortemente dependente da hipótese «não há emissão fora dos picos»; 0,1% de cauda já soma +1 neutrino; 10%, +5. P1 é a borda otimista, não uma previsão.
- **SENS_ZERO:** um ponto-zero (fusão × emissão) conhecido só a menos de σ_off por evento — o regime K–K tem < 1 neutrino por fusão, então cada neutrino vem de um evento diferente e o desvio é independente entre neutrinos — multiplica n_req por ~1,3–2,8 (σ_off = 0,5–4 ms, P2-like, ℓ = 20 km) e por até 5,9 em ℓ = 10 km (126 → 744); o P1-like cresce de 3 para 17 (ℓ = 20 km). O oráculo é, portanto, um piso: nuisance reais só encarecem.

## 7. Verificações e limites

- **Núcleo vs. solução fechada:** teste gaussiano de translação (H0 = N(0,1), H1 = N(d,1); n_analítico = ⌈25/d²⌉) reproduzido (n = 26, 101 e 7 contra 25, 100 e 7 analíticos para d = 1; 0,5; 2 — os +1 são empates exatos em que o limiar da rede arredonda para cima; limiar a ≤ 0,015 do analítico). Filtro × pente geométrico, enumeração exata, janela × exata, offset e simulação × exato: todos passaram (`saida_rodada/testes_nucleo.json`).
- **Simulação por amostragem por importância** (61 pontos em 33 casos, M = 200.000, semente 20261022): máx |c_MC − c_rede| = 0,022; máx |poder_MC − poder_rede| = 0,0026; todos dentro da tolerância pré-registrada.
- **O `veredito.py` pinado foi exercitado em dados falsos** (saída do ensaio fora das famílias; `dev_dry/cenarios_veredito.json`, `dev_dry/testar_cenarios_veredito.py`): devolve UNDERPOWERED_WALL_MEASURED no caso-base, POWERED_BNS se a taxa fosse 1 fusão por neutrino, INCONCLUSIVE com uma linha de simulação adulterada, e **recusa** (erro) CSV adulterado sem refazer o manifesto e `veredito.py` alterado (PIN_CHANGED).
- **Robustez** (teto de λ 40→60; passo da rede ÷ 2): 66 comparações; Δn_req máx = 0; Δc máx = 0,0050.
- **Checagem independente do modelo** (feita DEPOIS da rodada, sem alterar nada; `checagem_continua.json`): KL(H1‖H0) por integração no tempo contínuo (kernel exponencial) × células: diferenças de 0,5–1,5% (até 3,9% em KL(H0‖H1) num caso), como esperado de O(τ₀/σ).
- **Limites declarados:** oráculo (H0 e ponto-zero conhecidos); P1 com veto gaussiano; resolução ideal, sem fundo, sem massa do neutrino (só importa para D ≳ 2 Mpc: atraso ≈ (D/2c)(mc²/E)²), sem desvio para o vermelho; sem multiplicidade (3 valores de ℓ) nem marginalização de nuisance no veredito; **H-KN, H-SEQ, H-DECOH, H-BRANCH e GW-CLOCK seguem [CONJECTURE] e não foram testadas** (o kernel K_β é dado); n_req é neutrinos **esperados** (sem flutuação de Poisson); ℓ, larguras, amplitudes e frações são escolhas [INPUT] dentro de faixas [KNOWN], não ajustadas a dado algum nem à GW170817. Nada da Fase 9, do gate ou do kernel foi tocado.
- **Processo:** o `um.py` mudou desde a custódia de 21/10 (sha256 `972e81f2…` → `8918b178…`), com `SEALED_CODATA_ALPHA` idêntico; o mapa passou de 1.328 para 1.329 registros entre a minha 1ª consulta e o pino (outra sessão registrou). O aviso «failed» da tarefa em segundo plano foi só o `cat` final do shell de lançamento; o log da rodada termina em `FIM` com 0 falhas.

## 8. Nota fora do veredito — a arena alternativa: supernova galáctica com relógio GW do colapso [DECLARADO/KNOWN; NÃO é pré-registro]

*A borda de subida mede ms?* Ordem de grandeza:
- **Estatística sobra.** ~10⁴ neutrinos (Super-K: ~4–8 mil IBD a 10 kpc, SNEWS 2.0, arXiv:2011.00035; um trabalho de 2025 cita O(10³); Hyper-K: dezenas de milhares, arXiv:2203.02029 — todos [DECLARADO, via busca]) contra n_req(oráculo) = 11–284 nas curvas P2 e até 744 (P2-like, ℓ = 10 km) com ponto-zero incerto de 4 ms (SENS_ZERO) [REAL, mas a curva de emissão de SN é outra].
- **O relógio é duro.** O flash de ν_e da neutronização e o máximo da amplitude de GW estão sincronizados com o *bounce* «numa escala melhor que 1 ms»: Δt(ν_e−bounce) = (3,5 ± 0,5) ms; Δt(pico GW−bounce) = (0,1 ± 0,4) ms (78 formas de onda de Zwerger–Müller com rotação e EOS variadas) — Arnaud et al. 2001, arXiv:hep-ph/0109027v1, p. 1, 3, 4 e 8 [KNOWN, simulação; PDF sha256 `bf6a61806de24833…`]. O atraso ν−GW padrão é ~3,4 ± 0,6 ms: **o atraso médio do kernel K_β (2,7–8,2 ms, cauda exponencial) seria ~4–13× a incerteza de modelo** — em princípio mensurável na borda do flash.
- **Mas o flash é ν_e**, que a água só vê por espalhamento elástico (poucas dezenas de eventos; ~9 numa janela de 10 ms no Hyper-K, via busca do Design Report [DECLARADO]); o grosso (~10⁴) é ν̄e por decaimento beta inverso, cuja *borda de subida* tem escala de dezenas de ms. A precisão publicada do instante do *bounce* só pelo sinal de ν̄e é **~10 ms** (classe Super-K; Pagliaroli et al., PRL 103, 031102 [KNOWN, resumo]) e **±3,5 ms a 95% CL** no IceCube a 10 kpc, escalando com D² (Halzen & Raffelt, PRD 80, 087301 [KNOWN, resumo]) — comparável à média do atraso. Então, em ordem de grandeza: **ms só com estatística tipo IceCube (e, por extrapolação [DECLARADO], Hyper-K) mais um relógio GW**; sub-ms só no flash de ν_e (argônio) [DECLARADO].
- **Evento único:** taxa galáctica 1,63 ± 0,46 por século (um a cada ~61 anos) (Rozwadowska–Vissani–Cappellaro 2021, New Astron. 83, 101498 [KNOWN, resumo]). O relógio GW do *bounce* depende da rotação do núcleo e as amplitudes «anormais» são menos detectáveis (Arnaud p. 4).
- **Em aberto antes de qualquer pré-registro:** o ℓ da proto-estrela de nêutrons não está derivado (neutrinosfera ~90 km no flash segundo Arnaud p. 3, contra ~20 km em BNS — se ℓ escalasse com ela, hipótese NÃO derivada, o atraso médio seria ~25 ms, mais fácil); o perfil de emissão da SN (subida suave, sem estrutura sub-ms) exige outra família; a sistemática do ponto-zero domina, não o número de neutrinos. A gerência decide se vale um pré-registro separado.

## 9. Examinado no mapa, ato do operador e artefatos

- **Mapa consultado (só leitura):** `consultar "kilonova"` e `"rito9"` → rota `d7.kilonova_fronteira_aguda`, seqs 1301, 1305, 1307, 1309, 1310, 1311, 1312, 1313, 1314, 1315, 1316, 1317, 1321 (a pedida 1305/1307/1309/1311 e as seguintes: 1310 M1/Wigner, 1312–1314 handoff e revisão do Codex, 1315–1317 respostas e RT1/provas, 1321 esqueleto de poder) e `infra.bancada_um_modo_uso_kimi`. Cabeça na 1ª consulta: 1.328 registros, `ebf8060f671e5d03`; no pino: 1.329 registros, `44c8f71fde07efde`. *nao_refazer* respeitado: média não é estatística primária; nenhum 5σ declarado de simulação; nada ajustado à GW170817; H0 gaussiana tratada como bancada, não como modelo.
- **Ato do operador/gerência (não feito aqui):** registrar `registro_mapa_rito9_poder_realista.json` (`rotas.py registrar`), decidir se a arena de supernova ganha pré-registro separado e se a parede de BNS entra como registro ex-ante no Rito 9. Nada foi escrito no mapa, quadro, memória, túnel, site ou git.
- **Reprodução:** `python ferramentas/gerar_prereg.py <work>` (já feito; pinos) → `python ferramentas/rodar_estudo.py PREREGISTRO.json PINS.json saida_rodada --workers 14` → `python veredito.py PREREGISTRO.json PINS.json saida_rodada veredito.json`.

## Artefatos (sha256 lidos por script; 16 primeiros hex)

| arquivo | sha256[:16] | papel |
|---|---|---|
| `ANCORAS_LITERATURA.json` | `94e5c12f090b2d39` | frases-ancora localizadas por script (pagina + trecho) |
| `PINS.json` | `af3dfda1675dab69` | pinos (sha256 do pre-registro e dos 4 scripts); a rodada e o veredito recusam divergencia |
| `PREREGISTRO.json` | `720f3dbcbcb04a38` | pre-registro (familias, estatistica, numerica, taxa K-K, veredito, limites) |
| `PREREGISTRO.sha256` | `508d78b6d50332db` | sha256 de PREREGISTRO.json e veredito.py |
| `checagem_continua.json` | `3db9d40a7c906e9e` | checagem independente KL tempo continuo x celulas (pos-rodada, sem alterar nada) |
| `derivados_KK_por_caso.csv` | `e655891fd5b1eba5` | fusoes, exposicao, D_max, massa, eventos/seculo por caso (formulas pinadas em veredito.py) |
| `ferramentas/ancoras_literatura.py` | `a066468a1200bf41` | script/modelo |
| `ferramentas/checagem_continua.py` | `8be4cf9636fd0fa0` | script/modelo |
| `ferramentas/extrair_trechos_pdf.py` | `04d2c5ce65332f7b` | script/modelo |
| `ferramentas/gerar_prereg.py` | `a84bc74a8a1e6ffc` | script/modelo |
| `ferramentas/gerar_tabelas.py` | `12c0dac7a30520c1` | script/modelo |
| `ferramentas/montar_registro_mapa.py` | `bef4debf0db0fc92` | script/modelo |
| `ferramentas/montar_resultado.py` | `b81513480b8c83db` | script/modelo |
| `ferramentas/mostrar_prereg.py` | `613c49e053f29eaf` | script/modelo |
| `ferramentas/nucleo_poder.py` | `cccfa405a1f6bd1f` | script/modelo |
| `ferramentas/resultado_modelo.md` | `74450b97c67df3ca` | script/modelo |
| `ferramentas/rodar_estudo.py` | `10186d2b5624bb97` | script/modelo |
| `ferramentas/teste_nucleo.py` | `c164a186277623dd` | script/modelo |
| `ferramentas/validar_registro_mapa.py` | `b3b91cc714a4fe27` | script/modelo |
| `fontes_baixadas/kk_1710.05922/1710.05922v3.pdf` | `df423d09a5c16f1b` | PDF baixado (K-K, arXiv:1710.05922v3) |
| `fontes_extraidas/cusinato2022_texto.txt` | `1c914738a05ea6fc` | texto extraido de PDF (dado nao confiavel, lido com pypdf em python -I) |
| `fontes_extraidas/hep-ph_0109027_texto.txt` | `6ac9c06fc0879e0c` | texto extraido de PDF (dado nao confiavel, lido com pypdf em python -I) |
| `fontes_extraidas/kyutoku_kashiyama_texto.txt` | `75c505364738c1d0` | texto extraido de PDF (dado nao confiavel, lido com pypdf em python -I) |
| `registro_mapa_rito9_poder_realista.json` | `89fbd409cb0a36d2` | registro PRONTO para o mapa (nao registrado) |
| `rodada_oficial_stdout.txt` | `dbeb20b1587c8030` | log da rodada oficial |
| `saida_rodada/AMBIENTE_RODADA.json` | `9f1de657f8235141` | ambiente, um.py lido, semente, amostra |
| `saida_rodada/MANIFEST_RODADA.json` | `f0ae65efadbfaafa` | sha256 de cada saida da rodada |
| `saida_rodada/n_req_por_caso.csv` | `e2ae5aba5ce5e1bb` | DADOS CRUS: n_req e diagnosticos por caso (483) |
| `saida_rodada/perfis.csv` | `fa3a39a72375bf03` | definicao dos perfis (picos w, mu, sigma) |
| `saida_rodada/robustez_numerica.csv` | `f78d41b3f2073181` | DADOS CRUS: variantes numericas |
| `saida_rodada/testes_nucleo.json` | `7475c1f94c6ba6b7` | testes analiticos do nucleo |
| `saida_rodada/varredura_n.csv` | `b87c2eecd37dba0b` | DADOS CRUS: c_n, poder, mediana por (caso, n) avaliado |
| `saida_rodada/verificacao_mc.csv` | `96255d47d72cb73b` | DADOS CRUS: simulacao por importancia x rede |
| `tabelas.md` | `8338d20ad09e6824` | tabelas A-G geradas dos dados crus |
| `veredito.json` | `86e86aa4ef7bebf0` | veredito aplicado + portas + resumos |
| `veredito.py` | `741453da779d3c4b` | veredito pinado (sem limiar proprio) |

Pino: PREREGISTRO.json = `720f3dbcbcb04a383f567e3022c05022a5fadecaa52a2773225f93c835cbfbd2`; veredito.py = `741453da779d3c4bd747623e206d278bc250d6aca7eb4bf715be33dcaeaf63ff`.
PDF Cusinato (tool-results, dado nao confiavel) = `3aca87c7c57b627617dd24a95aa12051b4f127dc95fac5eb98321f0017313664`; PDF Arnaud et al. = `bf6a61806de248333a409b5a271945f0f1758e0726c4fc4652b54581a55d44d6`. `dev_dry/` guarda so os ensaios do pipeline em perfis FORA das familias (nao fazem parte do estudo).
