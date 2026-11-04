# PARTITURA DO TESTE D, 03/11/2026 — a ler ao operador ANTES de lançar qualquer análise em evento real
**O que o teste é:** 10 eventos reais do O4 (os que ninguém analisou assim), análise pesada (PE) cega, uma única pergunta: o amortecimento do ringdown cai do jeito que o PAR do ramo B manda (τ★ = 2π/κ̂ · G·M_f/c³, massa do remanescente, leitura por envoltória)?
**O que decide:** só esse par. Se der FALSIFIED (a 5σ), cai o par (esse k, esse M, essa leitura), nunca a lei, nem β, nem a TGL, nem o gate. Rodar não é publicar.
**O que NÃO decide:** β na natureza a 5σ; o eco; o ramo A (τ★ = t_Planck), onde D é invisível. A calibração A (não cega) já contraria o par (+0,072 contra −0,38); D seria o único teste cego.
**O que um negativo significaria — são quatro negativos diferentes e eu te digo qual saiu:**
1. NOT_FALSIFIED_UNDERPOWERED = **parede medida**, não falsificação: os 10 eventos (SNR 12 a 17) dão capacidade de decidir (poder) de 3,7 a 3,9σ, abaixo de 5σ; com o poder < 5 a regra congelada devolve isto QUALQUER que seja o valor achado. Medindo o viés do aparelho por poucas injeções, o poder cai para 2,1–3,2σ.
2. FALSIFIED_AT_5SIGMA = o par cai; só é alcançável se as incertezas reais saírem uns 25 % menores que o projetado, ou mais se contar o erro do viés (poder ≥ 5). Provado em sintético que a função PODE falsificar com informação suficiente.
3. INCONCLUSIVE_SYSTEMATICS = o aparelho reprovou num controle (viés das injeções, forma da incerteza, χ²): parede do instrumento, não da natureza.
4. AWAITING_DATA / INSUFFICIENT_SAMPLE = menos de 10 análises convergiram. É custo: nenhuma análise completa convergiu na casa até hoje (as 2 da GW250114 pararam em teto).
**Escolhas do desenho que o V1 não fecha e eu tive de fazer (diga se discorda; depois de lançar não se muda; lista completa em ESCOLHAS_DO_DESENHO_03nov.json):**
a. Valor de cada evento = média do posterior. Só a deformação do amortecimento do 220 fica livre (o resto fixo em zero; os modos GR superiores ficam). Distância até 10.000 Mpc (5 dos 10 passam de 2.000), tempo ±0,1 s, janela de 16 s, ruído medido em 256 s limpos.
b. O viés do aparelho é medido por injeções no ruído real fora do evento (uma sem desvio, uma com o desvio do par), SUBTRAÍDO, e a incerteza dessa medida entra no erro: isso só pode baixar o poder, nunca criar falsificação.
c. A regra «viés ≤ 20 % da previsão» é lida estatisticamente: ao pé da letra, com 5 injeções, ela reprovaria um aparelho PERFEITO 57 % das vezes por acaso (medido em sintético; na leitura que adotei, 2 %).
d. Incerteza sistemática 0,038 (a maior da família do V1); afastar-se do par em QUALQUER direção conta como falsificar; controle obrigatório não rodado = não sai veredito físico; abertura UMA vez, com autorização ligada ao hash do estágio cego; relógio novo de 21 dias (ainda fechado).
e. Aberto: fixar δf = 0 pode apertar as incertezas (poder real maior que o projetado) — só o estágio cego mostra.
**Custo** (máquina inteira, 48 núcleos; [DERIVED] do plano de 29/10, **sem garantia de convergência**): uma análise ≈ 170 horas-CPU (faixa 51–517), 11–13 h de parede; a conta central abaixo.
**As três opções:**
(a) Cadeia completa — 2 sintéticas + 10 eventos + 10 injeções (mínima): central 5–6 dias (3.750 h-CPU; otimista 1,5 dia; pessimista 15–17 dias); com 20 injeções 7–8 dias, com 50, 14–16 dias. Dá veredito físico, mas o poder fica abaixo de 5σ em qualquer tamanho (2,1; 2,6; 3,2σ): o provável é a parede (1).
(c) As 10 análises cegas só até o estágio cego (+ 1 sintética de 11–13 h se quiser medir a escala antes): central 2,3–2,6 dias (1.700 h-CPU; otimista 17–19 h; pessimista 7–8 dias). Sai o poder REAL com hash e você decide abrir ou não. Se o poder real der < 5σ, abrir só devolveria o negativo (1).
(b) Não rodar: registrar a parede medida (poder 3,7–3,9σ < 5, custo de dias sem garantia de convergir); D fica cego, para combinar depois com mais eventos (GWTC-5 final / O5) por combinação pré-registrada.
**Nada foi lançado:** zero análise, zero dado de D aberto, relógio fechado. Sua recusa pesa como ratificação.
