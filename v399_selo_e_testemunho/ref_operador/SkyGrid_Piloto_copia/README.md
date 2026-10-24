# SkyGrid-Sim — gêmeo digital do "sistema de sistemas" TGL/IALD (v3)

Protótipo de software da patente agregadora **SkyGrid** (BR 10 2026 004850-0): grafo distribuído
de nós (v1/v2, plano de DADOS) + **gêmeo digital físico-energético [SIM]** (v3, plano de ENERGIA).
Não é alegação de energia física — o modelo computa o que o mecanismo produziria SE as hipóteses
[CONJ] da TGL valerem, com conservação fail-closed, e diz explicitamente que **o que resta é a bancada**.

## v3 — o gêmeo de energia (Estágios F→J, 03/07/2026)

```bash
python tests/run_tests_v3.py                    # BLOCO 9 (44) + v2 (43) + v1 (69) fail-closed
python skygrid_energy_app.py twin               # reservatório→acoplamento OH→dípolo→Ψ→célula→carga
python skygrid_energy_app.py scale              # 144×48: ~24 kW médios [SIM], balanço fecha
python skygrid_energy_app.py sweeps             # famílias de curvas de projeto
python prototype/build_dossier.py               # dossiê de engenharia vivo
python serve_dashboard.py                       # painéis: / (dados) e /energy.html (energia)
python visuals/make_energy_figures.py           # fig5-fig8 (sistema, Sankey, sweeps, séries)
python visuals/make_energy_video.py             # skygrid_energy.mp4
```

Física [SIM]: acoplamento ressonante OH (f₀=1667,359 MHz) com abertura modular **1−β** (Teorema
S-∂, runtime) e **piso Meia-Nat** ½·k_B·T por ato; conservação obrigatória (`BalanceError`/
`OverUnityError` travam); placebo sem β = 0 W por construção; energia gated pelo duplo trilho +
quórum do plano de dados. Relatório: `SKYGRID_v3_ENERGIA_FINAL.md` · Dossiê:
`prototype/DOSSIE_ENGENHARIA.md` · Selo: `SKYGRID_V3_SELO.json`.

## v2 — a aplicação completa (Estágios A→E, 03/07/2026)

```bash
cd SkyGrid_Piloto
python tests/run_tests_v2.py                      # BLOCO 8 (43) + suite v1 (69) fail-closed
python skygrid_app.py run --sats 12 --bases 12    # rodada end-to-end (telemetria real HESE)
python skygrid_app.py run --sats 8 --bases 6 --faults dead,tamper,noise   # resiliência
python skygrid_app.py scale                       # reivindicação 2: 144 sats x 48 bases
python skygrid_app.py run --gpu ...               # caminho torch/CUDA (RTX 5090; fallback numpy)
python skygrid_app.py status                      # memória psiônica persistente entre sessões
python serve_dashboard.py                         # painel local: http://localhost:8137
python visuals/make_figures.py                    # 4 PNGs data-driven da última rodada
python visuals/make_video.py                      # MP4 da grade operando (requer ffmpeg)
```

Pipeline por transferência: **telemetria [DATA/PILOTO-DET] → ACOM Crypto (3 shares,
fail-closed) → TGL Tensor (Verb Floor 1−β, GPU-ready) → Ψ-NET (endereço angular) →
DUPLO TRILHO (Ψ×E) → quórum Proof of Phase (≥67%) → Célula de Reversão → base**, sob
controle IALD/GKSL (orçamento ⌈100/β⌉), kernel ontológico ligado ao kernel IALD real
(SHA-256 selado) e memória psiônica persistente. Placebo (sem β) rejeitado por construção;
falhas injetadas (dead/tamper/noise) detectadas por construção.

## v1 — o piloto original (preservado intocado)

```bash
python tests/run_tests.py        # suite fail-closed v1 (69 testes) + selo SHA-256
python run_skygrid.py 12 12      # grafo v1 (duplo trilho + placebo) + manifesto
```

Requer apenas `numpy` (matplotlib/ffmpeg só para `visuals/`; torch é opcional, só p/ `--gpu`).

## Disciplina (a régua)

- **β nunca literal:** `beta = ALPHA_FINE_CODATA_2018 * sqrt(e)` em runtime (`skygrid_sim/tgl_core.py`).
  α é o Nome medido (CODATA 2018); √e é derivado da Meia-Nat. Auditoria anti-hardcode é um teste.
- **Fail-closed:** toda identidade recomputada ao vivo; qualquer falha trava a suíte.
- **Duplo trilho:** cada transferência confirmada por Trilha-Ψ (holográfica) + Trilha-E (convencional);
  nó **placebo** (sem β) é obrigatoriamente rejeitado; bloco forjado é rejeitado 0/5 pelo quórum.
- **Sem veredito físico:** `physical_verdict_allowed=False` em toda saída (manifesto, painel, vídeo).
- **Estatutos:** [REAL] código verificado · [DATA] dado real com proveniência · [PILOTO] simulação ·
  [HARDWARE] mock sem alegação física · [LEGAL] organização, não parecer.

## Mapa dos módulos (`skygrid_sim/`)

`tgl_core` (fundação) · `acom`/`acom_mirror`/`acom_crypto` (trilho de dados) · `tgl_tensor`
(compressão + `TGLTensorAccel` GPU) · `iald_gksl`/`psionic_memory`/`kernel_ontologico`/`kernel_link`
(controle + aprendizado contínuo) · `psi_net` (comunicação + quórum) · `telemetry` (dados reais
HESE/IceCube + gerador orbital) · `mqc`/`dipolo`/`celula_reversao` (máquinas de estado) ·
`hardware_mocks` (camada física) · `skygrid` (grafo v1) · `orchestrator` (aplicação v2).

Relatórios: `SKYGRID_PROTOTIPO_v2_FINAL.md` (v2, este ciclo) · `SKYGRID_PROTOTIPO_v2_PLANO.md` ·
`SKYGRID_PILOTO_FASE3_4_FINAL.md` (v1) · `SKYGRID_PILOTO_FASE1.md` (integração TGL/UM + 16 patentes).
Selos: `SKYGRID_V2_SELO.json` · `SKYGRID_SIM_SELO.json`.

**TGL = haja luz. Tetelestai é o ponto de partida, não o fim.**
