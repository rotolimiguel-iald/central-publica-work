# SMOKE 03/11/2026 — parametrização do teste D (ramo B do ringdown, V1 sha16 86f98fcc124dd9ca)

Estatutos: **[REAL]** rodado e medido hoje; **[DERIVED]** conta minha sobre entradas declaradas; **[DESENHO]** escolha da gerência (lista em `ESCOLHAS_DO_DESENHO_03nov.json`); **[OPEN]** não medido. NOT_FALSIFIED nunca é CONFIRMED.

**Em uma linha:** o guarda novo, a semente, o desenho C2, o estimador, o estágio cego, a abertura e o veredito existem, estão pinados por hash e passam em 20 de 20 testes sintéticos e numa fumaça no WSL; **nenhum dado real foi aberto, nenhuma PE foi lançada, o relógio novo NÃO foi aberto.**

## O que rodou, com tempos

| onde | o que | resultado | tempo |
|---|---|---|---|
| Windows `C:\Python314` | `testes_sinteticos.py`, T01–T20 (resposta conhecida) | **20/20 passam** [REAL] | 4,2 s no total |
| Windows | hash sha256 dos 20 HDF5 de D (2,29 GB, só bytes; nenhuma amostra aberta) contra o manifesto O4 | 20/20 iguais; conferido por `sha256sum` independente em um arquivo (`9d475654fd2ed79d`) [REAL] | 1,5 s |
| WSL `/opt/lal_env` (py 3.12.3) | pinos + `checked_registration` + `check_runtime` | passam; runtime pinado: bilby 2.8.2, dynesty 3.1.0, lalsuite 7.26.15, numpy 2.5.3, scipy 1.18.1, h5py 3.16.0, gwpy 4.0.2, astropy 8.0.1 [REAL] | 0,35 s + 0,52 s |
| WSL | anti-CLI: `validate_launch` chamado por um processo que não é o controlador | **recusado** (GuardError: o runner deve ser líder de novo grupo sob o controlador) [REAL] | — |
| WSL | injeção C2 pelo `injection_design.py` ORIGINAL (cópia somente-leitura, 2 trocas em memória) em ruído gaussiano sintético, 4 injeções (GW250104 e GW241210, GR e RB) | SNR injetado = SNR alvo (12,1 e 13,4) com 6 casas; `dtau220` injetado = 0 ou o δ_pred do V1 (−0,4117; −0,3895); d_L reescalado cai dentro do prior [100, 10000] [REAL] | 0,81 s a 1ª (carga do LAL), 0,07 s as demais |
| WSL | fatia de verossimilhança em ruído ZERO ao longo de `dtau220` (27 pontos, passo 0,05) | GR: pico em 0,00 (injetado 0); RB: pico em −0,40 (injetado −0,4117); ΔlnL(−0,40 vs 0) = 3,22 [REAL] (confere a fiação injeção → verossimilhança → `dtau220`) | — |
| WSL | total da fumaça | | 7,3 s |

Saídas: `TESTES_03nov_resultado.json`, `SMOKE_WSL_saida.json`.

## O que os testes sintéticos mostraram (números do `TESTES_03nov_resultado.json`)

- **Estimador calibrado** (T03/T04, 1500 realizações, viés do instrumento c = 0,03 + 0,08σ medido por 25 injeções/classe): z_RG sob RG média −0,02, desvio 0,98; z_B sob B média 0,04, desvio 1,01. Sem corrigir o viés (T05), z_B sob B sai 1,50 de média; com C2, 0,10. **O viés do instrumento importa tanto quanto o sinal.**
- **Com o desenho do plano (poder < 5), "D como A" (+0,072)** (T06, 1000 realizações): NOT_FALSIFIED_UNDERPOWERED em 999; 1 INCONCLUSIVE por χ²/dof > 3 ao acaso (esperado ~0,14 %). Nunca FALSIFIED, nunca POWERED. [REAL, sintético]
- **Com informação ~5× maior** (σ × 0,45; T07, 400 realizações por verdade): verdade +0,072 → FALSIFIED_AT_5SIGMA 400/400; verdade B → NOT_FALSIFIED_POWERED__GR_TENSION_REPORTED 400/400; verdade RG → FALSIFIED 390, NOT_FALSIFIED_POWERED 9, UNDERPOWERED 1. **A função PODE falsificar o par; só não pode com a informação de D tal como projetada.**
- **Ordem do veredito** (T08, 12 casos): n=9 → `AWAITING_DATA__INSUFFICIENT_SAMPLE` antes de tudo; controle obrigatório não rodado → `AWAITING_DATA__CONTROLS_NOT_RUN`; controle reprovado/sist_rel>0,3/χ²/dof>3/discordância → INCONCLUSIVE; poder<5 → UNDERPOWERED (qualquer z); z_excl ≥ 5 → FALSIFIED; senão POWERED (+ tensão com a RG se |z_RG| ≥ 5). Nenhum token contém CONFIRMED/PROVED.
- **C2 literal × estatístico** (T10, 2000 sorteios, J = 5 por classe, instrumento PERFEITO): a leitura ao pé da letra do V1 (viés estimado ≤ 20 % da previsão) reprova **57,5 %** por puro acaso; a estatística (E6), 2,1 %. Daí a escolha E6.
- **Cegueira** (T02/T11): offset em (−1, 1); σ e W90 invariantes; o estágio cego dá o MESMO resultado com outra semente; desvelar devolve o bruto a 1e-12; compromisso errado recusa.
- **Abertura** (T12/T13): só com autorização ligada aos hashes; abre UMA vez (2ª tentativa → FileExistsError, hash errado e gate falso recusam ANTES de travar); σ desvelado == σ do estágio cego; sem C2 → AWAITING_DATA__CONTROLS_NOT_RUN; C2 com viés enorme → INCONCLUSIVE.
- **Guarda** (T15–T17, T19): sem relógio, relógio vencido, no futuro ou ligado a outros pinos → recusa; evento com hold/pendente/fora de D10 em qualquer modo → recusa (14 eventos testados); árvore de código alterada, cópia somente-leitura alterada, pino de strain ou GPS divergente do manifesto, V1 alterado → recusa; 12 jobs ruins (prior de distância antigo, janela deslocada, injeção em job cego, 440 livre, sha de strain errado, strain fora da raiz, janela C2 encostada no evento, `dtau220` arbitrário, ruído não-offsource, SNR alvo diferente, workers>28, evento com hold) → recusa; 30 jobs bons passam no `validate_job_D` **e** no `validate_config` do `pe_runner.py` original.
- **Desenho C2** (T18): 3 tamanhos (10/20/50 PE); toda janela termina ≥ 76 s antes do evento e cabe na maior corrida limpa nos dois detectores; GR e RB pareadas na mesma janela; massas dentro do prior; verdade suportada.
- **Canônico C1** (T20): |z_A − z_RG| = 9,9e−40 < 1e−30 com os M_f,det de D; o controle reprova se a previsão canônica for "ligada".

## Dois impedimentos da NOTA_CONJUNTO_D.md resolvidos sem editar nada em `Chatgpt\`

- `validate_truth_support` exigia prior em forma de dicionário até para parâmetro FIXO → `validate_truth_support_D` (aceita o escalar fixo = verdade).
- O gerador do injetor não encaminhava `generation_sample_rate_hz`/`generation_maximum_frequency_hz`, que o `pseob_source` vigente exige → envoltório de mesma assinatura (8192/4096 Hz). Ambos por troca em memória sobre a cópia somente-leitura (sha256 pinado em `copias_somente_leitura.SHA256.txt`).

## O que NÃO rodou (dito, para ninguém supor)

- **Nenhuma PE** (nem sintética completa): o custo até convergir segue **[OPEN]**; as 2 PE reais da casa (GW250114) pararam em maxcall com Δlogz 425 e 177. A fumaça só prova que injeção, guarda, estimador e veredito se ligam.
- `pe_runner_D.py`, `run_controlled_D.py`, o lançador de fila e o ato de congelamento (`JOBS_D_V1.json` + `CONGELAMENTO_D.json`) **não existem ainda**. O `guard_D` tem a API do `registration_guard`, então as cópias são troca mecânica de import (+ `injecao_c2` no lugar de `injection_design`, `blinding_D` no lugar de `blinding`) — **não testadas**. Regra D5 (repetição) está escrita, não implementada.
- Nenhum posterior, nenhuma amostra de strain, nenhum valor de deformação de evento real de D foi aberto. O relógio novo (`RELOGIO_D.json`) **não foi aberto**: sem ele o guarda recusa tudo.
- A PE com `domega220` fixo pode dar σ_i menor que o do plano (o ajuste σ(SNR) vem de análises com δf e δτ livres) — **[OPEN]**, só o estágio cego mostra.
