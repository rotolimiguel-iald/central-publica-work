# SKYGRID PROTÓTIPO v2 — PLANO DE EXECUÇÃO (Estágios A→E)

> IALD Ltda. (CNPJ 62.757.606/0001-23) — Luiz Antonio Rotoli Miguel — 03/07/2026.
> Continuação do piloto computacional da patente agregadora **SkyGrid** (BR 10 2026 004850-0).
> Régua: β nunca literal (α·√e em runtime, ponto único `tgl_core`); fail-closed; só o arquivo é prova;
> `physical_verdict_allowed=False` em toda saída. Piloto ≠ hardware ≠ energia ≠ parecer jurídico.

---

## 0. Estado atual VERIFICADO (FASE 0, 03/07/2026) [REAL]

| Verificação | Resultado | Selo |
|---|---|---|
| `python tests/run_tests.py` | **69/69 PASS** (66 + 3 regressões adversariais) | `invariants_hash 0ba134d49ce833918b36418600eca7fdd9192099f5f45095ad7b10f24f3b6e7b` |
| `python run_skygrid.py 12 12` | **12/12 aceitas, placebo rejeitado, ARCHITECTURE_CLOSES** | `seal 50920f32fb86068ec49e299a34f2cd54231c3e51bb1407771fb88655fe8057ba` |
| `um.py` (1 inscrito) | **1=1=VERDADEIRO=HAJA_LUZ**, resíduo 0.0e+00 | β=0.012031300401 |
| β cross-check | `tgl_core.beta() = 0.012031300400803142` == um.py, θ_M=6.297289° | `verify_chain()` todos resíduos ~0 |

Ambiente sandbox: numpy+matplotlib+PIL+ffmpeg presentes; **torch AUSENTE** (o caminho GPU
será opcional com fallback numpy; a rodada GPU real ocorre na máquina do operador, RTX 5090).

## 1. ESTÁGIO A — Robustez e completude funcional [PILOTO]

| # | Entrega | Fonte legada | Critério de pronto |
|---|---|---|---|
| A1 | `skygrid_sim/telemetry.py` — payloads REAIS: HESE 7-year IceCube (102 eventos, `recoDepositedEnergy`/`recoZenith` [DATA]) + gerador determinístico de telemetria orbital realista (órbita, eclipse, térmica) [PILOTO-DET] | `acom/icecube_data/.../HESE_data.json` (sha256 registrado) | teste: payload real carrega, proveniência selada; fallback determinístico reproduzível |
| A2 | `tgl_tensor.py` GPU-ready: caminho torch opcional (import guardado), semântica idêntica ao numpy; fallback automático | `tgl-tensor/tgl_tensor_v4.py` (BitPackerTorch, linhas 137-262) | teste: sem torch → fallback PASS; com torch → roundtrip idêntico (roda na máquina do operador) |
| A3 | `psi_net.py` quórum: `PhaseValidator.vote_on_block` + `QuorumPhaseChain` (MIN_VALIDATORS=3, THRESHOLD=0.67, tolerância fase 1e-9) | `acom/Psi_net_protocol_v1.py` linhas 1046-1080, 104-105 | testes: bloco honesto aceito ≥67%; bloco forjado rejeitado mesmo com validador bizantino; single-miner antigo intacto |
| A4 | Aprendizado Contínuo real: `PsionicMemory` persistente entre execuções da grade (`SKYGRID_PSIONIC_STATE.json`) + `KernelProfile` ancorado no kernel IALD real (sha256 do `IALD_Kernel_v11.txt`, filtro verbal β aplicado ao sumário) | `IALD/IALD_Kernel_v11.txt` | teste: estado sobrevive save/load entre rodadas, tamper trava; filtro manifesta ≤ fração β |
| A5 | Orçamento de estabilização = **ceil(100/β) ≈ 8312 passos** (achado BLOCO 3: par modular mais lento ~0,06/β; 3/β insuficiente) | `iald_gksl.py` | orquestrador usa 100/β; teste de regressão do orçamento |

## 2. ESTÁGIO B — Integração ponta-a-ponta

| # | Entrega | Critério de pronto |
|---|---|---|
| B1 | `skygrid_sim/orchestrator.py` — pipeline completo por transferência: telemetria → ACOM/Crypto (3 shares) → TGL Tensor (Verb Floor 1−β) → Ψ-NET (endereço angular + hops) → duplo trilho → quórum Proof of Phase → Célula de Reversão (retenção) → base → distribuição; controle IALD (orçamento 100/β) + Kernel + memória psiônica; placebo obrigatório | rodada 12×12 end-to-end ACEITA + placebo rejeitado + manifesto/selo |
| B2 | `skygrid_app.py` — CLI: `run`, `scale` (144×48, reivindicação 2), `--faults dead,tamper,noise`, `--telemetry real\|synthetic`, `--seed` | 144 sats roda; throughput/tempo medidos; falhas injetadas DETECTADAS (dead → reroteado/logado; tamper → fail-closed; noise → rejeitado) |
| B3 | Métricas consolidadas em JSON (`dashboard/data/latest.json`): aceitação, corr, compressão, retenção, quórum, defasagem, falhas, timing | JSON completo gerado por rodada; sem gráficos ainda |

## 3. ESTÁGIO C — Interface e persistência

| # | Entrega | Critério |
|---|---|---|
| C1 | `dashboard/index.html` (HTML+JS estático, zero dependências) + `serve_dashboard.py` (stdlib http.server) lendo os JSON | dashboard abre e mostra estado da grade da última rodada |
| C2 | Persistência entre sessões: memória psiônica da grade acumulada (EMA taxa β) por rodada | contador de sessões cresce; métricas EMA evoluem; tamper trava |

## 4. ESTÁGIO D — Visualização (SÓ após A–C verdes)

| # | Entrega |
|---|---|
| D1 | `visuals/make_figures.py` — topologia do grafo, mapa satélites/bases (projeção orbital), fluxo do duplo trilho, curvas de métricas (matplotlib → PNG) |
| D2 | `visuals/make_video.py` — animação da grade operando (transferências, selagem de fase, rejeição do placebo, escala 144) → MP4 (ffmpeg presente) |

## 5. ESTÁGIO E — Fechamento

- `tests/run_tests.py` ampliado (BLOCO 8: telemetria/quórum/GPU-fallback/orquestrador/falhas/persistência) — tudo verde.
- `README.md` + `SKYGRID_PROTOTIPO_v2_FINAL.md` + selos atualizados.
- Roadmap `[HARDWARE]` separado (o que fica para bancada física).

## 6. Invariantes desta sessão (a régua)

1. Os 69 testes existentes NUNCA quebram (mudanças aditivas; `skygrid.py` v1 preservado).
2. β importado só de `tgl_core`; nenhum literal 0.012… em código novo.
3. Todo módulo novo com marcadores de estatuto no docstring.
4. Controles negativos por construção (placebo, tamper, bizantino) — não por sorte.
5. Nenhuma alegação física de energia; vereditos só estruturais.
