# KIMI 5σ-01 — β_TGL fora da cosmologia: inventário, sensibilidade e custo de 5σ

**Data:** 27/10/2026  
**Estatuto global:** **[DECLARADO pelo Kimi]**, até conferência linha a linha pela gerência.  
**Escopo:** levantamento bibliográfico e desenho; nenhuma execução sobre dados, nenhum download, nenhum ajuste e nenhuma publicação. As únicas contas novas são aritmética de unidades, gaps e escalamento explícito de poder já publicado.  
**Regra:** β = α·√e em runtime; o valor numérico publicado é 0,012031300400803142. Nada neste relatório move o gate, cria selo ou autoriza abertura de dados.

## Resumo — 14 linhas

1. **[DECLARADO pelo Kimi]** A única rota não cosmológica localizada com tempo próprio, observável e função de veredito já fixados é **B1, ringdown ramo B**.
2. **[DECLARADO pelo Kimi]** B1 usa τ★ = k·GM_f/c³, k = 2π/κ̂(χ_f), fonte local e taxa aditiva; a previsão exata é δτ̂₂₂₀ = −x/(1+x), x = β·k·N(χ_f). [R9]
3. **[DECLARADO pelo Kimi]** O poder publicado para A(31) é 11,38σ; o escalamento A-like dá **5,98 ≈ 6 eventos** para não-centralidade 5 e **9,44 ≈ 10** para 90% de poder unilateral com limiar 5. [R9]
4. **[DECLARADO pelo Kimi]** A é calibração `NOT_BLIND`; o único teste cego é D, com 14 elegíveis e 10 sem pendência, cujo N/poder próprio só nasce das σ_i da PE. [R9]
5. **[DECLARADO pelo Kimi]** GWTC-5.0 tem 390 candidatos até O4b; a amostra pSEOBNR útil à combinação de ringdown tem 31 eventos, não 390. [R11][R12]
6. **[DECLARADO pelo Kimi]** B2 não reabre: o observável do ramo B é dephasing do 220; ecos são outro observável e suas nove rotas já foram examinadas. [R1][R9]
7. **[DECLARADO pelo Kimi]** B3–B5 têm horizontes ou contornos físicos e excelentes plataformas, mas **nenhuma ponte TGL pública derivada foi localizada em R2 nem nas portas e consultas públicas auditadas** que ligue seu tempo a τ★ e feche um observável. [R2]
8. **[DECLARADO pelo Kimi]** Assim, para BEC, fibra, água, Unruh e Casimir dinâmico, efeito TGL, gap e N/t de 5σ são **indeterminados**, não zero e não pequenos.
9. **[DECLARADO pelo Kimi]** No ramo canônico τ★ = t_Planck, os gaps são aproximadamente: Sr 13; Th-229 11 na aspiração de 1 mHz ou 18 no resultado em sólido; Fe-57 14; JUNO 40. [R2][R24–R31]
10. **[DECLARADO pelo Kimi]** Sc-45 tem gap 7 pela largura natural, mas >9,64 na condição experimental; Ag-109m daria 4,21 apenas num cenário indireto, não operacional. [R28][R29]
11. **[DECLARADO pelo Kimi]** DUNE n = −2 fica sem gap único: a cota de 10⁻²³ GeV localizada não pertence a esse expoente e não pode ser transplantada. [R30]
12. **[DECLARADO pelo Kimi]** Interferometria atômica permanece [OPEN]: rad/√Hz não é taxa em s⁻¹ e falta o mapa TGL para fase/contraste. [R26][R27]
13. **[DECLARADO pelo Kimi]** Nenhuma rota nova atinge gap ≤ 1; B1 já possui pré-registro congelado, portanto **não há novo pré-registro a redigir** nesta entrega.
14. **[DECLARADO pelo Kimi]** CODATA, ACOM e parâmetros ajustados não contam como evidência natural de β; ACOM permanece **ENGENHARIA**.

## A. Inventário público: onde β aparece em ordem 1

A distinção essencial é entre **identidade formal**, **cálculo no modelo**, **rito contra a natureza** e **engenharia**. A ocorrência de β sem t_Planck não basta para constituir evidência: é preciso um observable físico, novidade de uso e poder estatístico.

| Item | Enunciado e número | Estatuto como está na fonte | Fonte pública |
|---|---|---|---|
| Matriz-S da fronteira | \|R\|² = β, \|T\|² = 1−β, θ_M = arcsin√β; β = α·√e | **Kernel:** θ genérico, unitariedade e sin²θ + cos²θ = 1; β não aparece no arquivo Lean. **Runtime:** identificação θ = θ_M e \|R\|² = β. **Natureza:** transferência finito→fronteira gravitacional permanece `CONJECTURE`. | [R3][R4] |
| Piso dos vazios | ρ_vazio/ρ̄ ≥ β = α·√e ≈ 0,0120313 | `TGL_VOID_FLOOR_NOT_FALSIFIED_POWERED`; rito unilateral. O limite inferior publicado, 0,0588, fica acima do piso, mas o ΛCDM raso também passa; não é discriminação bilateral. | [R5][R6] |
| Razão de Hubble | K = E(z*)^(2β/3), β = α·√e; zero parâmetro livre | Rito + natureza; z_disc = 4,4431 e z_δ = −1,4835. `NOT_FALSIFIED_POWERED`; discriminação abaixo do degrau 5; mecanismo cosmológico `CONJECTURE`; teste não cego. Não se recalcula aqui. | [R1][R7][R35] |
| Entropia da fronteira | S_∂ = ½ nat | `[DER/AX]`: decorre da fronteira auto-conjugada x = 1−x, não apenas de ω(I)=1. Não é observação independente de β. | [R8] |
| Volume mínimo da fronteira | Vol_∂^min = exp(S_∂) = √e | `[REAL]` na verificação de runtime; `[DERIVED; α INPUT]` na cadeia. O degrau S_∂↦e^(S_∂) é identificação física, não teorema de kernel, e não tem falsificador próprio separado. | [R5][R8] |
| Inscrição | 1 = q² + α²; β = α·√e | Identidade térmica tanh² + sech² = 1 `[REAL]`; correspondência SUSY `[KERNEL]`; α_obs = sech é `[ONTO]` e o valor α-livre permanece `[OPEN]`. | [R5][R8] |
| Sombra numérica | Δn_Q = −β + O(β²), β = α·√e | `REAL` como cálculo do estado estacionário no modelo holográfico finito; razões publicadas 0,999825/0,999851/0,999881 para N = 4/5/6. **Não é rito de natureza.** | [R4] |
| Chandrasekhar | 1,40922 M_⊙, residual 0,353% de √2 M_⊙ | **Negativo honesto:** a explicação inicial por Coulomb não se sustenta; √2 não é atrator independente e a proximidade não é predição de precisão. | [R4][R6] |

**Leitura A.** A matriz-S, a Meia-Nat, √e e a inscrição mostram β ou suas estruturas em ordem 1 **dentro da teoria**. O piso e Hubble levam isso à natureza, mas são rotas cosmológicas e não foram tocadas. Δn_Q e Chandrasekhar não suprem um canal local de 5σ. **[DECLARADO pelo Kimi]**

## B. Candidatos fora da cosmologia — tabela de nove colunas

### Convenções

- No ramo canônico, Γ_TGL = ½·β·t_P·ω², β = α·√e; ½βt_P = 3,24318561×10⁻⁴⁶ s. [R2][R23]
- G = log₁₀(Γ_sens/Γ_TGL). Para coerência exponencial, Γ_coh = 1/T₂*; para linha lorentziana de FWHM Δν, Γ_coh = πΔν; decaimento populacional obedece 1/τ = 2πΔν = 2Γ_coh.
- “Indeterminado” significa que falta uma ponte derivada ou um estimador; não significa efeito nulo.
- Toda linha está **[DECLARADO pelo Kimi]** até auditoria da gerência.

| (1) Sistema | (2) Contorno/horizonte; substituto de t_P | (3) Observável TGL | (4) Efeito com zero ajuste | (5) Melhor sensibilidade/resultado público | (6) Gap | (7) N ou tempo para 5σ | (8) Dado público existente | (9) Estatuto |
|---|---|---|---|---|---|---|---|---|
| **B1 — BH ringdown, ramo B** | Horizonte Kerr do remanescente; τ★ = k·GM_f/c³, k = 2π/κ̂(χ_f), fonte local. Kerr χ≠0 `CONJECTURE`; identificação `INPUT/ONTO`. | **DERIVADO no V1:** taxa aditiva no 220; δτ̂₂₂₀ = −x/(1+x), x = β·k·N(χ_f); β = α·√e. [R9] | χ=0/0,68/0,9: δ = −0,19091/−0,37627/−0,63192; em A, média prevista −0,38216. [R9] | A(31): σ_comb = 0,03357; poder exato 11,38σ. GW250114: δτ̂ = −0,01 (+0,10/−0,09), 90%; GWTC-5 combinado: +0,07 (+0,06/−0,05), 90%. [R9][R12][R13] | **≤0** em poder; efeito maior que a resolução A. Não converter intervalo 90% em σ sem modelo. | **A-like:** N₅ = 31(5/11,38)² = 5,98 → 6; N₉₀% = 31[(5+1,2816)/11,38]² = 9,44 → 10. **D:** indeterminado até PE; 14 elegíveis, 10 sem hold. **O5/IR1:** T = N/R_RD, R_RD não publicada. | Sim: A(31), B(10), C(1) para calibração `NOT_BLIND`; D cego aguarda PE. GWTC-5: 390 candidatos; TGR: 168; pSEOBNR combinado: 31. [R9][R11][R12] | V1 `AWAITING_DATA`; pré-registro já congelado. A não decide teste cego. |
| **B2 — ecos GW** | Horizonte usado em rotas antigas de atraso; não é o τ★ do ramo B. | **Não reviver:** ramo B mede dephasing do 220, não cópia atrasada. | Não se aplica ao canal encerrado. | Nove rotas já examinadas: cinco excluídas pelo dado, quatro inconclusivas. [R1] | Não se aplica. | Não se aplica. | Rotas públicas examinadas; não reabrir. | **EXCLUÍDO desta busca**; homônimo KMS não é mesmo observável. |
| **B2 — NANOGrav/PTA, ramo canônico** | τ★ = t_P; nenhum horizonte próprio ou tempo de integração PTA derivado como substituto. | Dephasing de GW na forma geral; **estimador PTA específico [OPEN] não derivado**. | f=10⁻⁸ Hz; ω≈6,3×10⁻⁸ rad/s; Γ≈1,3×10⁻⁶⁰ s⁻¹. | **[OPEN] não localizado limite comparável em s⁻¹**; perda de fase e strain não foram convertidos em taxa TGL. [R36] | **[OPEN] indeterminado; não reter 51 sem fonte.** | **Indeterminado:** falta estatística da taxa TGL. | TOAs/modelos NANOGrav 15 anos: DOI 10.5281/zenodo.7967584; v2.1.0: 10.5281/zenodo.16051178. | **[OPEN]** efeito canônico calculado; sensibilidade/gap não estabelecidos. |
| **B3 — BEC Steinhauer** | Horizonte sônico v = c_s; 2π/κ_s é apenas candidato temporal, sem ligação derivada a τ★. | **[OPEN] não derivado:** espectro, taxa residual ou desvio de T_H sem equação TGL. | Não calculável sem ponte τ★↔κ_s⁻¹. | 2019: T_H = 0,351(4) nK, 7.400 repetições; 2021: 97.000 repetições, 124 dias. [R14][R15] | **Indeterminado.** | **Indeterminado:** estatística da plataforma não é estatística do sinal TGL. | Artigos/suplementos; dado bruto público não localizado. | **[OPEN]**; plataforma analógica, sem previsão TGL fechada. |
| **B3 — fibra Philbin/Leonhardt** | Horizonte de velocidade de grupo; τ₀ ou 2π/κ apenas candidatos, sem ponte pública. | **[OPEN] não derivado:** nenhuma correção TGL a g⁽²⁾, espectro ou backreaction. | Não calculável; perfil δn inteiro pode importar, não só κ local. | 2026: g⁽²⁾(0)=0,106±0,018, CAR=75; backreaction e T_H concordam em 2%, aquisições até 12 h. [R16][R17] | **Indeterminado.** | **Indeterminado.** | Sim para o experimento de um fóton: DOI 10.6084/m9.figshare.32305338; backreaction sob solicitação. | **[OPEN]**; sensibilidade óptica não calibrada para TGL. |
| **B3 — água Weinfurtner/Rousseaux** | Horizonte hidrodinâmico v=c; 2π/κ_w apenas candidato. Em 2016 havia bloqueio dispersivo, não horizonte estrito. | **[OPEN] não derivado:** nenhuma correção TGL de espalhamento ou G₂/g₂. | Não calculável. | 2016: g₂≈0,7±0,1, 80 blocos de 12,5 s; 2020: 800 s, fluxo 147,4±0,7 cm²/s. [R18][R19] | **Indeterminado.** | **Indeterminado.** | Textos/suplementos arXiv; dados brutos independentes não localizados. | **[OPEN]**; canal clássico, não efeito Hawking quântico. |
| **B4 — Unruh acelerado / NA63** | Horizonte Rindler a c²/a; c/a ou 2πc/a são candidatos, sem derivação para τ★. | T_U=κ/2π `[KNOWN]`; **[OPEN] não derivado:** nenhum desvio TGL de T_U ou do balanço detalhado. | Não calculável; T_U padrão não é previsão TGL. | 2025: caudas acima de 25,5 e 7,1 GeV descritas por Unruh/recoil, mas normalização ajustada; 2021: T_FDU=1,80±0,51 PeV. [R20][R21] | **Indeterminado.** | **Indeterminado**; modelos com normalização ajustada violam C3 para este fim. | Sete conjuntos reutilizados de publicações; repositório bruto independente não localizado. | **[OPEN]**; evidência da plataforma não vira teste TGL. |
| **B4 — KMS / Clausius / detector simulado** | Cone de luz ou Rindler; 1/α é candidato. Íon tem T_d=0,2 ms, escala de controle distinta. | T_U=κ/2π `[KNOWN]` e δQ=κδA/(8πG) como balanço formal/condicional; **[OPEN] não derivado:** nenhum desvio ou taxa mensurável TGL associado. | Não calculável. | 2025: íon ⁴⁰Ca⁺, ω_q/2π=200 kHz, g₀/2π=5 kHz, 10⁴ repetições nos pontos tardios. [R22] | **Indeterminado.** | **Indeterminado.** | Texto/suplemento arXiv; dado independente não localizado. | **[OPEN]**; simulação de princípio, não aceleração espacial direta. |
| **B5 — Casimir dinâmico / SQUID** | Contorno elétrico ℓ_e(t), sem necessidade de horizonte; ℓ_e/v_e ou 2π/ω_d são candidatos sem ponte. | **[OPEN] não derivado:** nenhuma taxa extra de fótons, squeezing ou dephasing TGL. | Não calculável; Γ_DCE padrão não contém β = α·√e. | 2011: ω_d/2π≈11 GHz, v_e/c₀≈0,05, 4×10⁷ amostras; 2020: −0,09±0,02 dB. [R32][R33] | **Indeterminado.** | **Indeterminado.** | Artigos/suplementos; dados brutos independentes não localizados. | **[OPEN]**; consulta pública “Casimir” sem rota anterior localizada. |
| **B6 — relógio Sr-87, 429 THz** | **[OPEN] não derivado**; ramo canônico conserva t_P. | Decaimento de contraste; forma geral derivada, aplicação específica sem τ★ novo. | ω=2,6969×10¹⁵; Γ=2,359×10⁻¹⁵ s⁻¹. | T₂*=118(9) s; Γ_sens=8,47×10⁻³ s⁻¹. [R24] | **12,56 ≈ 13.** | **Indeterminado:** bootstrap/CL do relógio não define teste TGL 5σ. | Artigo/figuras; conjunto bruto TGL-ready não localizado. | **UNDERPOWERED** no ramo canônico. |
| **B6 — relógio Th-229, 2,02 PHz** | **[OPEN] não derivado**; nenhum substituto público de t_P. | Perda de coerência nuclear. | ω=1,26946×10¹⁶; Γ=5,226×10⁻¹⁴ s⁻¹. | Aspiração 1 mHz: 3,14×10⁻³ s⁻¹. Realizado em sólido ≈18 kHz: 5,65×10⁴ s⁻¹. [R25] | **10,78 ≈ 11** aspiração; **18,03** realizado. | **Indeterminado:** shot noise do relógio não fornece mapa estatístico de Γ_TGL. | CSVs do relógio com feedback em Zenodo 23341251. | **UNDERPOWERED**; mHz não é desempenho iônico realizado. |
| **B6 — interferometria atômica de grande base** | **[OPEN] não derivado:** L/c e baseline não foram derivados como τ★. | **[OPEN] não derivado:** faltam ω, braços afetados e mapa dephasing→fase/contraste. | Indeterminado. | MAGIS-100: meta inicial 10⁻³ rad/√Hz; protótipo diferencial no limite quântico padrão. [R26][R27] | **Indeterminado** por definição e unidade. | **Indeterminado.** | Documentos de projeto/protótipo; nenhum dado científico TGL localizado. | **[OPEN]**; não importar automaticamente ω do Sr. |
| **B7 — Mössbauer Fe-57, 14,4 keV** | **[OPEN] não derivado**; ramo canônico t_P. | Alargamento/dephasing da ressonância. | ω=2,18964×10¹⁹; Γ=1,555×10⁻⁷ s⁻¹. | τ≈141,1 ns; 1/τ=7,09×10⁶ s⁻¹; coerência equivalente 3,54×10⁶ s⁻¹. [R28] | **13,36** coerência; **13,66** população. | **Indeterminado.** | Medidas publicadas; arquivo TGL-ready não localizado. | **UNDERPOWERED**, ≈14 ordens. |
| **B7 — Sc-45, 12,38959 keV** | **[OPEN] não derivado**; t_P. | Decaimento NFS/coerência nuclear. | ω=1,88231×10¹⁹; Γ=1,149×10⁻⁷ s⁻¹. | Natural: Γ_coh≈1,09 s⁻¹. Experimental: T_coh<2 ms → Γ_coh>500 s⁻¹. [R28] | **6,98 natural**; **>9,64 experimental.** | **Indeterminado.** | Sim: experimento 6536, DOI 10.22003/XFEL.EU-DATA-006536-00. | **UNDERPOWERED**; largura natural não é desempenho em sólido. |
| **B7 — Ag-109m, 88 keV** | **[OPEN] não derivado**; t_P. | Ressonância γ ultrafina. | ω=1,33696×10²⁰; Γ=5,797×10⁻⁶ s⁻¹. | Largura indireta ≈0,1 feV ≈30 mHz → Γ_coh≈9,42×10⁻² s⁻¹. [R29] | **4,21**, somente cenário indireto. | **Indeterminado.** | Nenhum conjunto aberto consolidado localizado. | **UNDERPOWERED/[OPEN]**; não tratar 4,21 como gap operacional. |
| **B8 — DUNE, E=1 GeV, n=−2** | **[OPEN] não derivado**; F7.2 existente; ramo canônico t_P. | Damping de oscilação; expoente espectral fixado, escala não. | Γ=1,17×10⁻³⁹ s⁻¹ = 7,71×10⁻⁶⁴ GeV. | **Sem número único transferível para n=−2.** 1,2×10⁻²³ GeV →18,2 s⁻¹ pertence a outro modelo/energy-independent. [R30] | **Indeterminado para n=−2**; não reter “40” daquela cota. | **Indeterminado**; 6,5+6,5 anos a 90% CL não é descoberta 5σ. | Projeções; sem dados DUNE correspondentes. | **[OPEN] numérico**; F7.2 não se refaz. |
| **B8 — JUNO, E=3 MeV, n=−2** | **[OPEN] não derivado**; F7.2 existente; t_P. | Damping com γ₂₁=γ₃₁, γ₃₂=0 no modelo citado. | Γ=1,17×10⁻³⁷ s⁻¹ = 7,71×10⁻⁶² GeV. | γ₀<4,1×10⁻²⁷ GeV a 90% CL, pivô 1 GeV; a 3 MeV: 4,56×10⁻²² GeV =692 s⁻¹. [R31] | **39,77 ≈ 40.** | **Indeterminado para 5σ**; 59,1 dias geram cota a 90%, não detecção. | Resultados públicos; event-level aberto não localizado. | **UNDERPOWERED**; corrige gap 38 para ≈40. |
| **B9 — ACOM** | Não se aplica. | Nenhum observável físico TGL. | Não se aplica. | Codec contra codec mede desempenho de compressão. | Não se aplica. | Não se aplica. | Benchmarks não são dados da natureza. | **ENGENHARIA**; dossiê BR 10 2025 026951-1, jamais σ físico. |

## B1. Sensibilidade e N: leitura controlada

O pré-registro já fornece o estimador, a nuisance c(σ), a covariância efetiva por pesos, a sistemática de família/início, os controles C1–C9, o cegamento e a função de veredito. Ele também já calcula, sem abrir D, o poder A(31) = 11,38σ e N₉₀ exato = 9,4 sob sua população de planejamento. A aritmética acima apenas explicita o mesmo escalamento: 31·(5/11,38)² = 5,98 e 31·[(5+z₀,₉₀)/11,38]² = 9,44. **[DECLARADO pelo Kimi; R9]**

Esses números têm três limites. Primeiro, pressupõem eventos futuros com a mesma informação média de A e ausência de saturação por sistemática correlacionada. Segundo, A/B/C são `NOT_BLIND`; não convertem o resultado em teste novo. Terceiro, D tem spins e previsões conhecidas, mas não σ_i antes da PE; portanto não se afirma que seus 14 ou 10 eventos bastam. O critério geral é I_N = Σ_i 1/s_i² ≥ 25/Δ² para não-centralidade 5, ou I_N ≥ (z_limiar+z_poder)²/Δ² para poder probabilístico, com s_i² = σ_stat,i²+σ_sys,i² e covariância/sistemática tratadas pelo V1. **[DECLARADO pelo Kimi; R9]**

Para O5/IR1, T_obs ≥ N_req/R_RD somente se R_RD for a taxa de eventos que passam o mesmo corte de ringdown, já incluindo dever de observação e seleção. Os 390 do catálogo, os 168 de TGR e os alertas O4c não são essa taxa. O4c permanece fora do catálogo cumulativo e o cronograma oficial corrente apresenta IR1 como próximo run; O5 não tem data oficial fixada localizada. **[DECLARADO pelo Kimi; R11][R12][R34]**

## C. Exclusões obrigatórias

1. **C1 — identidade CODATA.** β é definido como α·√e; escrever α = β/√e é tautologia. “Infinitos sigmas” é zero evidência natural. Resíduos de ~10⁻¹⁵ são arredondamento de ponto flutuante, não medida independente. A retirada da circularidade BBN permanece como precedente da casa. **[DECLARADO pelo Kimi]**
2. **C2 — ACOM.** Benchmark contra zstd/LZMA mede codec contra codec. Pode integrar o dossiê de engenharia da patente BR 10 2025 026951-1; não mede natureza nem produz σ da TGL. **[DECLARADO pelo Kimi]**
3. **C3 — parâmetro ajustado.** Qualquer rota cuja amplitude, normalização, τ★, k ou escala seja ajustada ao mesmo dado fica fora do teste de zero parâmetro. Parâmetros instrumentais precisam de calibração independente. **[DECLARADO pelo Kimi]**
4. **C4 — creditação.** A máquina reporta somente `NOT_FALSIFIED`, `FALSIFIED`, `INCONCLUSIVE`, `UNDERPOWERED` ou estados equivalentes pré-registrados; creditação é ato do observador humano externo. **[DECLARADO pelo Kimi]**
5. **C5 — forma de β.** Toda ocorrência computacional deve preservar β = α·√e; nenhum literal de β é admitido como definição ou entrada ajustável. **[DECLARADO pelo Kimi]**

## D. Rotas com gap ≤ 1 e pré-registro

**B1 é a única rota localizada com poder/gap ≤ 1, e já possui o pré-registro `PREREG_RAMO_B_RINGDOWN_20261005_V1`, congelado por hash, com função de veredito, alvos, pesos/covariância, vereditos permitidos, controles nulos, cegamento e critério de poder. Não se redige um segundo registro nem se altera o V1.** O estado publicado é `AWAITING_DATA`; A/B/C são calibração `NOT_BLIND` e D é o teste cego. [R9]

**Nenhuma outra rota satisfaz gap ≤ 1.** B3–B5, NANOGrav/PTA e interferometria não têm gap numericamente definido porque falta derivação do observável/tempo ou da sensibilidade comparável; B6–B8 têm gaps de aproximadamente 4 a 40 ordens quando o ramo canônico permite calculá-los. Portanto, pelo critério D da ordem, **não há rascunho adicional de pré-registro a produzir**. Negativo honesto é resultado. **[DECLARADO pelo Kimi]**

Antes que B3–B7 possam virar desenho pré-registrável, faltam cinco peças, nesta ordem: (i) demonstrar que o contorno físico é o K_∂ do gerador; (ii) derivar τ★, incluindo o fator entre 1/κ e 2π/κ; (iii) fechar o mapa para contraste, fase, largura ou taxa; (iv) fixar calibrações sem ajuste ao dado; (v) definir modelo nulo, covariância, sistemáticos, cegamento e poder. Até lá, N ou tempo seriam números sem hipótese estatística. **[DECLARADO pelo Kimi]**

## Referências e portas

**Data de acesso de todas as fontes: 27/10/2026.**

- **R1 — Portal TGL v402 e régua pública:** https://teoriadagravitacaoluminodinamica.com/llms.txt
- **R2 — Dinâmica aberta, GKSL e dephasing; τ★ como INPUT:** https://teoriadagravitacaoluminodinamica.com/secoes/05-dinamica-aberta-gksl-e-dephasing.md
- **R3 — Matriz-S Lean:** https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/Um%20%28absoluto%29%20%E2%80%94%20Grande%20Atrator/Lean/tgl_kernel/TGLExt/SMatrix.lean
- **R4 — Artigo A, fonte TeX:** https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/O%20Custo%20Geom%C3%A9trico%20do%20Zero%20Absoluto%20%E2%80%94%20Haja%20Luz/paper_PT.tex
- **R5 — Forma canônica v402:** https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/Um%20%28absoluto%29%20%E2%80%94%20Grande%20Atrator/um_absoluto_forma_canonica.md
- **R6 — Estado atual e erratas:** https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/ESTADO_ATUAL.md
- **R7 — Pré-registro Fase 9, somente inventário:** https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/Um%20%28absoluto%29%20%E2%80%94%20Grande%20Atrator/preregistro_fase9_hubble_v387/PREREGISTRO_FASE9_RAZAO_DE_HUBBLE_V1.md
- **R8 — Partes 01, 02 e 04:** https://teoriadagravitacaoluminodinamica.com/secoes/01-o-um-absoluto.md ; https://teoriadagravitacaoluminodinamica.com/secoes/02-beta-custo-geometrico.md ; https://teoriadagravitacaoluminodinamica.com/secoes/04-o-gerador-e-o-piso-do-espectro.md
- **R9 — Pré-registro ramo B V1:** https://raw.githubusercontent.com/rotolimiguel-iald/central-publica-work/main/cadeia_de_selo/v386/ramo_b/teste_gerador_v1/PREREGISTRO_RAMO_B_RINGDOWN_V1.md
- **R10 — Manifesto v386:** https://raw.githubusercontent.com/rotolimiguel-iald/central-publica-work/main/cadeia_de_selo/v386_incorporacao_manifesto.json
- **R11 — GWTC-5.0, catálogo:** arXiv:2605.27225, https://arxiv.org/abs/2605.27225
- **R12 — GWTC-5.0, testes de RG:** arXiv:2607.19293, https://arxiv.org/abs/2607.19293
- **R13 — GW250114, espectroscopia:** arXiv:2509.08099; DOI 10.1103/6c61-fm1n; https://arxiv.org/abs/2509.08099
- **R14 — BEC, Steinhauer 2019:** arXiv:1809.00913; DOI 10.1038/s41586-019-1241-0; https://arxiv.org/abs/1809.00913
- **R15 — BEC estacionário 2021:** arXiv:1910.09363; DOI 10.1038/s41567-020-01076-0; https://arxiv.org/abs/1910.09363
- **R16 — Fibra, estímulo de um fóton 2026:** DOI 10.1038/s41467-026-73812-8; dados DOI 10.6084/m9.figshare.32305338.
- **R17 — Fibra, Hawking/backreaction 2026:** arXiv:2607.01118; DOI 10.1038/s41586-026-10720-3; https://arxiv.org/abs/2607.01118
- **R18 — Água, Euvé et al. 2016:** arXiv:1511.08145; DOI 10.1103/PhysRevLett.117.121301; https://arxiv.org/abs/1511.08145
- **R19 — Água, Euvé et al. 2020:** arXiv:1806.05539; DOI 10.1103/PhysRevLett.124.141101; https://arxiv.org/abs/1806.05539
- **R20 — NA63/Unruh 2025:** arXiv:2505.21292; DOI 10.1103/8ynl-xpn4; https://arxiv.org/abs/2505.21292
- **R21 — NA63/Unruh 2021:** arXiv:1903.00043; DOI 10.1103/PhysRevD.104.025015; https://arxiv.org/abs/1903.00043
- **R22 — Detector Unruh “timelike” simulado:** arXiv:2510.24163; DOI 10.48550/arXiv.2510.24163; https://arxiv.org/abs/2510.24163
- **R23 — CODATA 2018:** DOI 10.1103/RevModPhys.93.025010; https://pml.nist.gov/cuu/pdf/RevModPhys.93.025010.pdf
- **R24 — Coerência Sr-87:** arXiv:2505.06444; https://arxiv.org/abs/2505.06444
- **R25 — Th-229, frequência e relógio nuclear:** arXiv:2406.18719; DOI 10.1038/s41586-025-09999-5; feedback arXiv:2606.04997; dados https://zenodo.org/records/23341251
- **R26 — MAGIS-100:** arXiv:2104.02835; https://arxiv.org/abs/2104.02835
- **R27 — Protótipo de interferometria de grande base:** arXiv:2504.09158; https://arxiv.org/abs/2504.09158
- **R28 — Linhas nucleares Fe-57 e Sc-45:** Fe-57, DOI 10.1140/epja/s10050-025-01659-6; Sc-45, arXiv:2508.17538; dados DOI 10.22003/XFEL.EU-DATA-006536-00; https://arxiv.org/abs/2508.17538
- **R29 — Ag-109m:** DOI 10.1134/S0021364009190011.
- **R30 — Decoerência em neutrinos/DUNE:** arXiv:1805.09818; DOI 10.1007/JHEP09(2023)097; https://arxiv.org/abs/1805.09818
- **R31 — JUNO n=−2:** arXiv:2606.13362; primeiros dados arXiv:2511.14593; https://arxiv.org/abs/2606.13362
- **R32 — Casimir dinâmico em SQUID:** arXiv:1105.4714; DOI 10.1038/nature10561; https://arxiv.org/abs/1105.4714
- **R33 — Squeezing por Casimir dinâmico:** arXiv:1802.05529; DOI 10.1103/PhysRevLett.124.140503; https://arxiv.org/abs/1802.05529
- **R34 — Planos oficiais de observação LVK:** https://observing.docs.ligo.org/plan/
- **R35 — Resultado Fase 9 V2, somente inventário:** https://raw.githubusercontent.com/rotolimiguel-iald/the_boundary/main/Um%20%28absoluto%29%20%E2%80%94%20Grande%20Atrator/fontes_pinadas/Central%20de%20Patentes/work/cadeia_de_selo/v397/insumos/fase9/RESULTADO_FASE9_V2_C1_20261023_122926.json
- **R36 — PTA, coerência e dados:** Margalit, Contaldi & Pieroni, arXiv:2004.01727; DOI 10.1103/PhysRevD.102.083506; https://arxiv.org/abs/2004.01727 ; de Kruijf, arXiv:2511.14727; NANOGrav 15 anos, dados DOI 10.5281/zenodo.7967584 e 10.5281/zenodo.16051178; resultado GWB arXiv:2306.16213; DOI 10.3847/2041-8213/acdac6.

---

**Resultado final:** uma rota física não cosmológica já está pronta para teste cego sob registro — B1; nenhuma rota nova alcança gap ≤ 1; as demais ou permanecem [OPEN] por falta de derivação, ou estão UNDERPOWERED por supressão de Planck. Tudo permanece **[DECLARADO pelo Kimi]** até a conferência da gerência.
