FASE 9 V2 — O TESTE DA ÚNICA PALAVRA — preparada, não aberta

**Natureza:** preparação (gerência c1, 23/10/2026). Nada foi aberto: nenhum composto observado da V2, nenhum veredito, nenhum recibo de congelamento ou de abertura emitido, nada escrito no túnel, no Nós, no um.py, no mapa, no quadro, na memória, no site ou no git. Pasta: `C:\IALD\Central de Patentes\work\fase9_v2_c1_23out`. Estatutos: [REAL] medido aqui · [DERIVED] · [INPUT] decisão do operador · [DECLARADO] afirmado na origem. NOT_FALSIFIED nunca é CONFIRMED; o gate não se move.

## 0. Resposta curta

1. A V2 R5.2-E1 (`81a970926345832a`) ganhou as quatro decisões do operador de 23/10 e virou `46b329d8c86e96b3` (spec canônico `c9f9fec83d10dd4f`); **a lógica e os limiares da função de veredito são os da R5.2** (4000 entradas aleatórias dão a mesma classe e o mesmo sufixo). Token: `TGL_FASE9_V2_A_UNICA_PALAVRA_BETA_TGL`.
2. L1b (Riess+2025, arXiv:2509.01667: 73,49 ± 0,93) e L6 (LVK O4a, arXiv:2509.04348 v1/v2: 76,6 +13,0/−9,5) foram **baixados e pinados**; os 8 leitores têm regra de extração testada contra os bytes (igual ao declarado a 1e-9). `n_alvos_declarados` passa de 2 para **0**.
3. Runner do modo observado em cópia (E1–E5, S5, calibração de cauda) e **trava**: recusa sem recibo de congelamento e sem recibo de abertura. **48/48 testes sintéticos e controles negativos passam.**
4. **Fundo BG1 real** (não mock) reproduz o pino: H0 = 68.53106 (Δ = 6.4e-05), σ = 0.30140.
5. **Poder esperado só pelas incertezas** (BG1, 5 maseres): D = 5.721 (extremo de maior σ) a 6.623 (menor σ); sem Cefeidas 3.938 a 4.395. Reproduz os pinos da R5.2 a 1e-9.
6. **O que a calibração mostrou e a gerência precisa decidir (reversível até o congelamento):** o `|z_δ| ≥ 5` bruto equivale a z calibrado **3.94** com a pior covariância da caixa (p = 8.078e-05, não 5,7e-07) e a **4.98** com a covariância do ponto; para um 5σ calibrado o bruto tem de ser **6.37** (caixa) ou **5.02** (ponto). Com o modo padrão `sup_caixa`, se a ΛCDM for a verdadeira a função devolve FALSIFIED em 42.7% a 47.1% dos casos (TENSION em 37.6% a 42.6%); com o escore bruto, 75.5% a 80.8%. E a regra de dispersão herdada do V1 dá INCONCLUSIVE em 9.1% a 19.5% mesmo com tudo consistente.

## 1. Entregas (sha256[:16], lidos dos arquivos)

| arquivo | sha256[:16] | papel |
|---|---|---|
| `spec/PREREGISTRO_FASE9_V2_C1_A_UNICA_PALAVRA.json` | `46b329d8c86e96b3` | a spec V2-c1 (alcance, X13, D-H, D-J, S5, calibração, trava) |
| `spec/veredito_fase9_v2_c1.py` | `383961aa796d68b5` | a função de veredito pinada |
| `spec/REGISTRO_DH_V2_C1.json` | `3e25ac3431c62887` | registro D-H: 8 fontes por sha256 + regras de extração |
| `spec/DIFF_R52_PARA_V2C1.md` | `9afc1f13cc9de1e6` | diff contra a R5.2, cada mudança atribuída |
| `spec/DIFF_R52_PARA_V2C1.patch` | `ade71cdc4a5d57dc` | o mesmo, linha a linha |
| `runner/f9v2_runner.py` | `48a52268bd58a12e` | runner do modo observado |
| `runner/f9v2_stats.py` | `0e581e392f44e430` | estatística do executor (X13, S5, E3) |
| `runner/f9v2_calibration.py` | `9400c4e04f7f4cf9` | calibração de cauda |
| `runner/f9v2_freeze.py` | `12b6ab030a1ee122` | a trava (recibos) |
| `runner/f9v2_background.py` | `69b6d8d842d7ac02` | E1/E2: fornecedor real do fundo |
| `runner/f9v2_extract.py` | `57ad640ed193f50f` | extração dos centros das fontes (E5) |
| `runner/f9v2_text.py` | `ab020e146dc0deb2` | leitura de fonte como dado não confiável |
| `runner/f9v2_verdict.py` | `6e8d7736510a3a4a` | carrega a função pinada em espaço restrito |
| `calibracao/CALIBRACAO_CAUDA_RECIBO.json` | `89d17a6759d727e0` | recibo da calibração |
| `calibracao/MC_VALIDACAO.json` | `a8a5ef9060b21377` | MC × analítico |
| `poder/PODER_ESPERADO_V2C1.json` | `4c976dbc5cd3ac46` | poder esperado só por incertezas |
| `testes/RESULTADO_TESTES.json` | `24da6ea47642b349` | resultado dos testes |
| `testes/QUALIFICACAO_FORNECEDOR_REAL.json` | `29b5f023ac597bda` | fundo BG1 real (sem H0 local) |
| `PEDIDO_DE_CONGELAMENTO.json` | `9f379998b8aad5f7` | o que a gerência confere e assina |
| `registro_mapa_fase9_v2_c1.json` | `ee888df58ce20a54` | registro para o mapa (olhou_dados=false) |

## 2. Fontes baixadas e pinadas (D-H)

| leitor | H0 ± σ (extraído da fonte) | arquivo | sha256[:16] |
|---|---|---|---|
| L1_sh0es_r22 | 73.04 ± 1.04 | `fontes/L1_sh0es_r22_arxiv_2112.04510/sh0es_2022.html` | `df9136da862ef625` |
| L1b_sh0es_r25 | 73.49 ± 0.93 | `fontes/L1b_riess2025_arxiv_2509.01667/abs_2509.01667.html` | `302b0a42572723e7` |
| L2_cchp | 70.39 ± 1.936 | `fontes/L2_cchp_arxiv_2408.06153v3/cchp_2025_v3.html` | `eb1b6689f13dbcea` |
| L3_sbf | 73.8 ± 2.404 | `fontes/L3_sbf_arxiv_2502.15935v2/sbf_2502.15935v2.html` | `b61012efc5238c0e` |
| L4_masers_5 | 73.6 ± 3.05 | `fontes/L4_masers_arxiv_2001.09213v2/masers_2001.09213v2.pdf` | `c9f2d2b626fee60d` |
| L4_masers_6 | 73.9 ± 3 | `fontes/L4_masers_arxiv_2001.09213v2/masers_2001.09213v2.pdf` | `c9f2d2b626fee60d` |
| L5_tdcosmo | 71.6 ± 3.6 | `fontes/L5_tdcosmo_arxiv_2506.03023v4/tdcosmo_2025_v4.html` | `b04dfc911acb4ad3` |
| L6_sirenes | 76.6 ± 11.25 | `fontes/L6_lvk_o4a_arxiv_2509.04348/abs_2509.04348v1.html` | `1b728822339026c4` |

Baixados em 23/10/2026 por `curl` (download autorizado à gerência), lidos como dado não confiável (`python -P -E`, caminho como argumento): L1b `abs_2509.01667.html`; L6 `abs_2509.04348v1.html` (admitido), v2, v3 e o PDF v3 (ao lado, **não admitidos**: a v3 publicada diz 75,4 +12,8/−9,1; L6 está fora do composto, a troca não muda o veredito). Os outros seis arquivos são cópias byte a byte do ORDEM_018 (hashes idênticos aos do levantamento). Limites: SBF §III.3 e TDCOSMO §VIII.2.1 seguem só como resumo; BG2/BG3 seguem [KNOWN]/[DECLARADO].

## 3. O que mudou da R5.2 (resumo; `spec/DIFF_R52_PARA_V2C1.md` tem cada linha)

- **OP-a ALCANCE:** `alcance` novo — FALSIFIED_AT_5SIGMA = β_TGL refutado na natureza, a lei K é a voz única, sem saída posterior; a validade do kernel não está em jogo; o pré-registro é o devido processo. `nao_decide` reescrito.
- **OP-b X13 SIM:** `estatisticas_do_executor` descreve o que o executor faz (fundo marginalizado; z_δ pelo perfil com log-det; ln B com n ≥ 100; ln B(TGL/β-livre) = 1,97).
- **OP-c D-H:** registro pinado; L1b e L6 entram com os papéis tipados que a V2 já dava; `n_alvos_declarados` 2 → 0.
- **OP-d D-J:** token `TGL_FASE9_V2_A_UNICA_PALAVRA_BETA_TGL` + a ordem do sufixo (INCONCLUSIVE_SYSTEMATICS · FALSIFIED_AT_5SIGMA · TENSION_3_TO_5_SIGMA · NOT_FALSIFIED_UNDERPOWERED · DISCRIMINATES · NOT_FALSIFIED_POWERED).
- **C1 (ordem da gerência, reversível):** E1–E5, S5, calibração de cauda, trava. Acréscimos que o operador não pediu e a gerência pode recusar: σ do fundo também conferido (|σ−0,301|<0,005); `beta_livre_no_limite` vale se QUALQUER extremo estiver na borda; ln B decisório n = 100 com conferência n = 200.

## 4. O runner — o que ele faz e o que recusa

Ordem do modo observado: (0) recibos e pinos, bytes lidos **uma vez**; (1) β = α·√e em runtime com o α do um.py instalado, K recalculado = K congelado (1e-12); (2) **E1/E2** fundo BG1 real, |H0−68,531|<0,01 — diverge, interrompe, nunca calibra; (3) **PODER_FASE9_ANTES_DE_ABRIR.json** com só σ, gravado e hasheado, com os centros num cofre lacrado (acesso antecipado = KeyError/recusa); (4) **E4/E5** centros extraídos das fontes pelo registro D-H pinado; `ALVOS_FASE9_LIDOS.json` em qualquer lugar do pacote = recusa; (5) estatística do executor, **E3** (|ln Z₁₀₀ − ln Z₂₀₀| > 1e-6 ⇒ recusa sem veredito), **S5**, calibração; (6) função pinada executada do texto; resultado inteiro gravado, também abaixo de 5σ.

**S5 fechada por propagação:** a variância da previsão muda -2.1% e a média, por Ω_m do próprio fundo (0,3011 contra 0,3023 pré-registrado), -0.0012 km/s/Mpc — desprezíveis frente a σ_comb 0,80–0,95.

**Sistemáticas do levantamento:** S5 propagada (acima); S1 (a covariância cruzada é uma caixa de tetos) entra na calibração como `sup_caixa`; velocidades peculiares e vazio local, covariâncias SN/Pantheon (L1–L2, L1–L5) e a origem do fator 0,031 do SBF seguem [OPEN]/declarados na spec — não os fechei.

## 5. Calibração de cauda

Redução exata (fundo marginalizado, f = 1): z_δ é função determinística de u = m − K·μ (m = média GLS); z_disc, de x = m − μ, em forma fechada. Verificado contra o pipeline completo: máx |Δz_δ| = 9.0e-08, máx |Δz_disc| = 5.1e-14 (400 sorteios). O MC sob as nulas concorda com o analítico (`calibracao/MC_VALIDACAO.json`).

| z_δ bruto | p gaussiano (bilateral) | p_cal (ponto) | z_cal (ponto) | p_cal (caixa) | z_cal (caixa) |
|---|---|---|---|---|---|
| 2 | 0.0455 | 0.04546 | 2.000 | 0.1141 | 1.580 |
| 3 | 0.0027 | 0.002701 | 3.000 | 0.01778 | 2.370 |
| 4 | 6.334e-05 | 6.462e-05 | 3.995 | 0.001586 | 3.158 |
| 5 | 5.733e-07 | 6.339e-07 | 4.981 | 8.078e-05 | 3.942 |
| 6 | 1.973e-09 | 2.69e-09 | 5.949 | 2.401e-06 | 4.716 |

| z_disc bruto | p gaussiano (unilateral) | p_cal (ponto) | z_cal (ponto) | p_cal (caixa) | z_cal (caixa) |
|---|---|---|---|---|---|
| 2 | 0.02275 | 0.0006358 | 3.222 | 0.0006886 | 3.199 |
| 3 | 0.00135 | 0.000127 | 3.658 | 0.0001405 | 3.632 |
| 4 | 3.167e-05 | 9.868e-06 | 4.268 | 1.13e-05 | 4.237 |
| 5 | 2.867e-07 | 2.206e-07 | 5.050 | 2.66e-07 | 5.014 |
| 6 | 9.866e-10 | 9.586e-10 | 6.005 | 1.246e-09 | 5.962 |

(z_disc é unilateral e assimétrico: sob ΛCDM, z_disc ≥ 2 é raríssimo porque o p é calculado sobre a região de Δχ² ≥ z², onde a previsão TGL, de variância maior, pode vencer só nas caudas; só o limiar de 5 decide.)

Limiares brutos equivalentes: 3σ → z_δ 3.00 (ponto) / 3.80 (caixa), z_disc 1.21 / 1.30; 5σ → z_δ 5.02 / 6.37, z_disc 4.94 / 4.98. O pior caso da caixa é λ_N = λ_T = 1 (τ_f 1.096 contra 0.866 do ponto). O z_disc já é quase calibrado a 5σ; o z_δ não, porque a covariância entre leitores é uma caixa, não uma medida.

## 6. Poder esperado (pipeline completo, função pinada, 100000 sorteios por cenário; centros sintéticos, nenhum observado)

**β_TGL (TGL) verdadeira:**

| covariância verdadeira | modo | FALSIFIED | TENSION | INCONCLUSIVE | UNDERPOWERED | DISCRIMINATES | POWERED_NOT_DISCRIMINATED |
|---|---|---|---|---|---|---|---|
| indep(0,0) | bruto | 0.0% | 0.2% | 19.3% | 0.0% | 62.0% | 18.5% |
| indep(0,0) | proprio | 0.0% | 0.2% | 19.3% | 0.0% | 63.2% | 17.3% |
| indep(0,0) | sup_caixa | 0.0% | 0.0% | 19.3% | 0.0% | 62.4% | 18.3% |
| max_sigma(1,0.25) | bruto | 0.0% | 1.4% | 9.3% | 0.0% | 68.3% | 21.0% |
| max_sigma(1,0.25) | proprio | 0.0% | 1.4% | 9.3% | 0.0% | 69.6% | 19.6% |
| max_sigma(1,0.25) | sup_caixa | 0.0% | 0.2% | 9.3% | 0.0% | 69.2% | 21.2% |
| pior_caixa(1,1) | bruto | 0.0% | 1.4% | 9.3% | 0.0% | 68.1% | 21.1% |
| pior_caixa(1,1) | proprio | 0.0% | 1.4% | 9.3% | 0.0% | 69.5% | 19.7% |
| pior_caixa(1,1) | sup_caixa | 0.0% | 0.2% | 9.3% | 0.0% | 69.1% | 21.3% |

**ΛCDM verdadeira:**

| covariância verdadeira | modo | FALSIFIED | TENSION | INCONCLUSIVE | UNDERPOWERED | DISCRIMINATES | POWERED_NOT_DISCRIMINATED |
|---|---|---|---|---|---|---|---|
| indep(0,0) | bruto | 75.5% | 5.0% | 19.5% | 0.0% | 0.0% | 0.0% |
| indep(0,0) | proprio | 75.3% | 5.3% | 19.5% | 0.0% | 0.0% | 0.0% |
| indep(0,0) | sup_caixa | 42.7% | 37.6% | 19.5% | 0.0% | 0.0% | 0.2% |
| max_sigma(1,0.25) | bruto | 80.7% | 9.7% | 9.4% | 0.0% | 0.0% | 0.1% |
| max_sigma(1,0.25) | proprio | 80.4% | 10.0% | 9.4% | 0.0% | 0.0% | 0.1% |
| max_sigma(1,0.25) | sup_caixa | 46.8% | 42.6% | 9.4% | 0.0% | 0.0% | 1.1% |
| pior_caixa(1,1) | bruto | 80.8% | 9.9% | 9.1% | 0.0% | 0.0% | 0.2% |
| pior_caixa(1,1) | proprio | 80.5% | 10.2% | 9.1% | 0.0% | 0.0% | 0.2% |
| pior_caixa(1,1) | sup_caixa | 47.1% | 42.6% | 9.1% | 0.0% | 0.0% | 1.1% |

Taxa de INCONCLUSIVE pela dispersão quando tudo é consistente (sob a nula): TGL_verdadeira / indep(0,0): χ²/(n−1)>2 em algum extremo e/ou p<0,01 → 19.3% (só p<0,01 → 4.5%); TGL_verdadeira / max_sigma(1,0.25): χ²/(n−1)>2 em algum extremo e/ou p<0,01 → 9.3% (só p<0,01 → 1.0%); TGL_verdadeira / pior_caixa(1,1): χ²/(n−1)>2 em algum extremo e/ou p<0,01 → 9.3% (só p<0,01 → 1.1%).

## 7. Testes e controles negativos (só sintéticos)

`testes/run_tests.py`: **48/48**. Controles: congelamento ausente · abertura ausente · spec adulterada · **fonte adulterada** · .py a mais no runner · módulo do runner alterado · **fundo divergente** (H0 e σ) · **ALVOS manual** · pacote REAL com fornecedor não real · Bancada adulterada · α diferente · extração ≠ declarado · autohash corrompido · abertura de outro congelamento · token diferente · função diferente · tolerância de quadratura diferente · recibo de calibração diferente · poder ≠ pino · **quadratura instável** (estatística e runner) · CLI sobre este pacote (recusa sem ler nada) · NaN. Ponta a ponta: pacote fabricado (TGL-like, ΛCDM-like, borda do prior), ordem de acesso, cofre, 7 diagnósticos, **E2E com o fundo REAL e locais fabricados**.

## 8. O que a gerência decide e confere (detalhe em `PEDIDO_DE_CONGELAMENTO.json`)

- **G01** modo da calibração (padrão `sup_caixa`; alternativas `proprio`, `bruto`) — muda a letalidade do teste (§0.6, §6). **G02** regra de dispersão (mantida como na R5.2; ~9–20% de INCONCLUSIVE indevido). G03 BG2/BG3 sem fonte pinada. G04 versão do L6. G05 acréscimos da c1.
- Antes do recibo: **auditoria c1 do runner** (a R5.2 foi auditada até X13/D-H; o runner do modo observado, não). Depois: recibo de congelamento (gerência) → recibo de abertura (ato próprio) → abrir UMA vez → relatar escore, p calibrado, ln B, diagnósticos e limitações separados → **preservar o resultado mesmo abaixo de 5σ**.
- d72 (testemunha conjunta ROOT90da) é outra testemunha; não soma, não empresta poder.

## 9. Mapa consultado e o que examinei

`rotas.py consultar` com "fase9" (23 rotas), "razao de Hubble" (1), "F3.1" (9) e "F3.2" (12): `d1.fase9.auditoria_suficiencia_20261019` (separação esperada condicional, V2 observada em aberto), `d1.fase9.f3_1_reauditoria_v2r2_c1_08out` (APROVA_COM_RESSALVAS), `d1.fase9.f3_1_semantica_v1x_leitores`, `d1.fase9.f3_2_r1_hash_gate` (harness sintético), `d1.fase9.razao_de_hubble.lentes_05out`. Nada do que o mapa manda não refazer foi refeito: gate/harness/pinos F3.2 foram lidos, não repetidos; a estatística do executor é a do F3.2 estendida (S5, calibração) e a reprodução do fundo é a do R2 do V1. Registro proposto: `registro_mapa_fase9_v2_c1.json` (`olhou_dados=false`).

## 10. O que NÃO foi feito (e por quê)

- Não calculei o composto observado da V2 nem abri o veredito; os centros publicados só foram usados para **verificar** as regras de extração contra o declarado (igualdade a 1e-9), e o fundo BG1 (Planck+DESI) foi recalculado para qualificar o fornecedor. Os testes usam centros fabricados.
- Não emiti recibo de congelamento nem de abertura; não rodei `emitir_recibo_*`; não toquei o serviço da Bancada (porta 18777): o fornecedor roda em processo, como o runner V1; o código do pacote não faz chamada de rede (teste F3).
- Não mudei nenhum limiar da função; os acréscimos da c1 estão listados (G05) e são reversíveis.
- Pendentes: auditoria c1 do runner; decisões G01/G02; pinar fontes de BG2/BG3 se a gerência quiser fundos diagnósticos [REAL]; texto integral do SBF §III.3 e do TDCOSMO §VIII.2.1.

## 11. Como refazer (ordem; tudo com `python -P -E -X utf8`, a partir de qualquer cwd)

1. `ferramentas/build_funcao.py` → `ferramentas/build_registro_dh.py` → `ferramentas/build_spec.py` (spec, função, registro, diff).
2. `testes/qualifica_fornecedor_real.py` (fundo BG1 real; só Planck+DESI) — se o fundo mudar, refazer o passo 3.
3. `calibracao/rodar_calibracao.py --n-por-cenario 100000 --workers 40` (recibo da calibração, MC, poder esperado).
4. `testes/run_tests.py` (48 casos). 5. `ferramentas/build_entregas.py` (pedido, registro do mapa, este RESULTADO).
6. Só depois da auditoria c1: `ferramentas/emitir_recibo_de_congelamento.py ... --escrever`, depois `ferramentas/emitir_recibo_de_abertura.py ... --escrever`, depois `runner/f9v2_runner.py --package-root . --mode observed`.
7. `ferramentas/conferir_consistencia.py` (só leitura; sai com 1 se spec, função, registro, runner, recibo de calibração, testes e pedido divergirem).
