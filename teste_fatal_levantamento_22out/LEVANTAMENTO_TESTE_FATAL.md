TESTE FATAL — levantamento — 22/10

**Para:** gerência c1 · **De:** Claude (subagente Sonnet 5.5, a pedido da c1) · **Data:** 22/10/2026 · **Natureza:** levantamento de leitura. Nenhum dado foi aberto, nenhuma análise de dado foi rodada; nada foi escrito no mapa, quadro, memória, túnel, site ou git. Todo hash abaixo foi lido do arquivo por script na geração deste documento; os números derivados (limiares, probabilidades) foram calculados por script a partir de σ já registrados, e vêm marcados [DERIVED por este levantamento].

**Ordem do operador (22/10, verbatim, sha256[:16] `bca4b8a97c74226c`):** «Eu não estou buscando mais teste armado, isso é gordura no um.py sem sentido, estou buscando o teste fatal. Quanto ao resto prossiga». A memória `um-py-sem-gordura-19out.md` (ao lado de 22/10) fixa a leitura: não propor nem pré-registrar teste que só dispara com evento futuro; **parede medida fecha a rota e não vira registro armado**; o alvo é predição sem parâmetro ajustado, sobre dado público que já existe, capaz de matar a TGL ou de discriminar a 5σ.

## 0. Resposta curta

1. **A razão de Hubble (Fase 9, rota R-A) é o único caminho com (1), (2), (3) e (5) cumpridos e (4) ainda ABERTO** (4,28σ medido; 5,7–6,6σ esperado); o N_eff cumpre os mesmos quatro, mas tem parede medida em (4). A lei K = E(z*)^(2β/3) = 1,083807 (β = α·√e em runtime = 0,012031300; z* = 1089,95; zero parâmetro livre) dá H0_local = 74,274 ± 0,326 km/s/Mpc, contra 68,531 ± 0,301 do ΛCDM nu (K = 1). Separação: 5,743 km/s/Mpc.
2. **σ medido hoje** (V1 aberto em 06/10, centros ainda [DECLARADO], NÃO cego): z_disc = 4,284 · z_δ = −1,424 · ln B(TGL/ΛCDM) = 9,167 · β̂ = 0,00920 ± 0,00199 · veredito oficial INCONCLUSIVE_SYSTEMATICS. **Esperado na V2** (só σ, BG1, cinco masers): D = 5,721–6,623σ — separação esperada, não resultado observado; z_disc não é σ de cauda calibrado (auditoria de 19/10, §6).
3. **O que a mata** (função de veredito pré-registrada): |z_δ| ≥ 5, isto é, composto local ≲ 69,3–69,9 km/s/Mpc [DERIVED por este levantamento] (hoje 72,88 ± 0,92), ou leitor com σ ≤ 1,0 e |z| ≥ 5; em β: β̂ fora de [0,0021; 0,0220] (hoje 0,00920 ± 0,00199). **Ressalva de alcance que é decisão do operador:** o V1 escreve (sem acentos, no original) que FALSIFIED_AT_5SIGMA «falsifica o PAR (lei D1b, convencao, conjunto), nao beta, nao a teoria». Para o teste ser fatal na linguagem da ordem de 22/10, ele precisa dizer que a lei D1b é a leitura da teoria.
4. **Não roda como teste final ainda.** Faltam três atos do operador (X13; D-H, que precisa cobrir também L1b/R25 e L6/sirenes: sem bytes pinados, mantêm o primário em INCONCLUSIVE pela regra do inventário; D-J), cinco itens de código (E1–E5) e seis sistemáticas (S1–S6). Nada disso exige dado novo; exige fonte pinada, cópia de código e auditoria.
5. **Os outros quatro não são fatais hoje:** ringdown ramo B (poder só-σ de 11,38σ cai a 0,74σ com o nuisance livre; só o conjunto D testa e a PE dele ainda não foi qualificada: o piloto INIT003 terminou sem convergência); N_eff/BBN (parede medida: 5σ pede σ(N_eff) ≤ 0,0239; melhor instrumento citado, 0,045); m2 do neutrino (escala 1 eV e ângulo 45° são entradas; o Modelo Padrão não fixa o splitting; 2,2–3,0σ); piso dos vazios (passa, mas o ΛCDM raso também passa).
6. **Já decididas, não candidatas:** ecos (lei de atraso, FALSIFIED_AT_DELAY_LAW do par), Rito 9/BNS/supernova (UNDERPOWERED_WALL_MEASURED, seq 1330), relógios/²²⁹Th (déficit de 12,458 ordens de 5σ), fundo comprimido/CMB nível 2/D1 CAMB/w0wa (σ(β) ≈ 1,5β), Evento 2 α-livre (auto-confirmação). Lista com seq na §4.

## 1. As seis exigências e como li cada uma

(1) **predição fixada pelo axioma, sem parâmetro ajustado ao dado** (retrodição sem ajuste vale: lei de 05/10, novidade de uso). SIM = fórmula e cronologia na casa; PARC = depende de identificação nomeada; NÃO = há entrada [NORM]/[POSTULATE]/[INPUT] decisiva.
(2) **predição concorrente (ΛCDM / Modelo Padrão / RG) que difere**, fixa.
(3) **dado público que já existe** (em disco, ou publicado; nada que espere evento).
(4) **≥ 5σ alcançável com esse dado, ou o σ medido hoje.**
(5) **falsificador explícito**: o desfecho que mata (limiar pré-registrado).
(6) **o que falta** (fontes por sha256, covariância, sistemáticas, código).

Ordem do ranking: primeiro quem cumpre mais exigências COM dado que já existe; entre os que ainda não fecharam (4), quem NÃO tem parede medida vem antes de quem tem (nota da c1 de 22/10: parede medida fecha a rota). Estatutos da régua: REAL · DERIVED · KNOWN · INPUT · ONTO · CONJECTURE · OPEN · DECLARADO.

## 2. Tabela ranqueada (semáforo; SIM / PARC / NÃO)

| # | Candidato (rota do mapa) | (1) sem ajuste | (2) concorrente difere | (3) dado público existe | (4) ≥5σ ou σ medido | (5) falsificador | Aptidão | Estatuto (mapa) | Seq do mapa |
|---|---|---|---|---|---|---|---|---|---|
| 1 | Razão de Hubble, K = E(z*)^(2β/3) — Fase 9 (R-A) · `hubble.fase9_razao_discriminante`, `d1.fase9.*` | SIM | SIM (68,53 × 74,27) | SIM (centros [DECLARADO] até D-H) | PARC (4,28 hoje; 5,72–6,62 esperado) | SIM, do PAR | **a única que se aproxima** | REAL (V1, F3) · DERIVED (suficiência 19/10) · EXAMINADA_COM_DEFEITO | 373, 383–388, 603, 604, 647, 696, 742, 751–979, 773, 836–837, 1247, 1248, 1253–1257 |
| 2 | Ringdown ramo B, δτ220 = −x/(1+x), conjunto D (R-C) · `ringdown.ramo_b_preregistro_v386`, `ringdown.dephasing` | PARC (k = 2π/κ̂: KNOWN em χ=0, CONJECTURE em χ≠0; M_X e identificação INPUT/ONTO) | SIM (RG: δτ = 0; TGL −0,32 a −0,53) | SIM (strain O4 em casa; posteriores GWTC-5.0) | NÃO provável (0,742σ com nuisance livre; D não computável) | SIM, do PAR | condicional; parede provável na calibração | REAL documental; INPUT desenho; OPEN convergência/PE D | 24–27, 44, 85, 352, 355, 356, 359, 361, 365, 368, 374, 678, 682–685, 687, 969 |
| 3 | N_eff e BBN, ΔN_eff = +0,119466 — Fase 8 (R-B/R-M) · `primordial.fase8_era_da_radiacao`, `cmb.neff_e_rho_mais_p`, `neff.frozen_v1_08ago` | SIM (cond. ao mapa ρ+p e ao fechamento TGL-S) | SIM (N_eff = 3,044) | SIM (Planck, ACT DR6, SPT, Aver, Cooke) | NÃO: parede medida (σ ≤ 0,0239 exigido) | SIM (2 análises independentes) | **rota fechada (nota de 22/10: parede medida)** | REAL (frozen V1, canal B2) | 371, 375, 392, 402, 883, 1034 · frozen 732…935 |
| 4 | m2 do neutrino, m2 = β·sin45°·1 eV (R-K) · `neutrinos.m2.normalizacao` | NÃO (1 eV [NORM]; 45° [POSTULATE]) | NÃO (o MP não fixa o splitting) | SIM (JUNO 59 d; NuFIT 6.1; Capozzi) | PARC (2,2–3,0σ hoje; a regra pede 2 determinações) | SIM (kill_rule) | teste restritivo, não discriminante | DECLARADO · EXAMINADA_COM_DEFEITO | 59, 93, 98, 101, 128, 136, 142, 161, 256, 382, 1095 |
| 5 | Piso dos vazios, ρ_vazio/ρ̄ ≥ β (R-I; V11/V12) · `vazios.piso.v11`, `vazios.piso.v12` | SIM | NÃO (o ΛCDM raso também passa) | SIM (DESIVAST, GALZONE, KiDS-1000) | NÃO (lim. inf. 5σ ≈ 9× o piso; V12 não alcança o alvo) | PARC (GV-02, GVV-01: KILL contestado) | sobreviveu, não discrimina | REAL (auditoria 28/09) · INPUT (V12) | 3, 75, 82–84, 396, 397 · V12 47…774 |

### Números e limiares por candidato

| # | σ medido hoje | σ alcançável / esperado | O que mata | O que falta (resumo) |
|---|---|---|---|---|
| 1 | V1 (06/10, NÃO cego): z_disc 4,284 · z_δ −1,424 · ln B 9,167 (β-livre 2,241; shift-Cefeidas 4,280; fundo-livre 12,132) · β̂ 0,00920 ± 0,00199 | D (só σ): BG1 5,721–6,623 (cinco masers); BG2 5,06–5,68; BG3 4,99–5,55; sem Cefeidas 3,94–4,40. P(z ≥ 5) no gaussiano simples, D = 5,72–6,62: 76–95% [DERIVED por este levantamento]; poder do pipeline completo NÃO medido | \|z_δ\| ≥ 5 (composto ≲ 69,3–69,9) ou leitor σ ≤ 1,0 com \|z\| ≥ 5 (CCHP no mesmo centro 70,39 pede σ_i ≲ 0,70; hoje 1,94). Discrimina: z_disc ≥ 5 ∧ \|z_δ\| < 3 ∧ ln B(TGL/ΛCDM) ≥ 5 ∧ ln B(TGL/β-livre) ≥ −1 | X13, D-H (+L1b, L6), D-J; E1–E5; S1–S6 (§5) |
| 2 | nenhum cego. A31 NÃO-CEGO: z_excl ≈ 13,5 se o offset fosse 0 (ilustração do V1 §5) | A31 só-σ 11,38σ; com c0+kc livres 0,742σ (QR independente, F3); D: não computável (os σ nascem na PE) | z_excl = \|δ̄ − δ̄pred\|/σ_usado ≥ 5 — do PAR (k, M_X, identificação); o V1 diz «NÃO falsifica β, nem a lei na forma, nem a TGL» | PE só-220 de 14 eventos (10 sem hold), nuisance c(σ), controles C1–C9, critério de recuperação, aprovação P3 A02 |
| 3 | separação TGL–MP 0,63–1,09σ; tensão da TGL contra os centros 1,02–2,49σ (MP 0,32–1,42σ); poder Fase 8: 1,00σ | 5σ pede σ(N_eff) ≤ 0,0239; Simons 0,045 → 2,65σ (2025–2034); CMB-S4 encerrado | \|z\| ≥ 5 em DUAS análises independentes | instrumento, não dado |
| 4 | JUNO 2,19σ pelo σ do JUNO (o mapa registra 2,21σ, σ do lado da previsão; Δm²₂₁ TGL = 7,2376e-5 eV² contra 7,50 ± 0,12e-5); NuFIT 2,95σ (eq. 11) / 3,02–3,22σ (tabela); Capozzi 2,44σ | JUNO ~2031 levaria o global > 5σ; segunda determinação autônoma fora do horizonte | kill_rule congelada: DUAS determinações autônomas ≥ 5σ | derivar escala e ângulo do axioma; 2ª determinação |
| 5 | V11: r_c^cal 0,189 ± 0,017 (REVOLVER); limite inferior 5σ ≈ 9× o piso β [DECLARADO pela memória v92] | V12 por lente não alcança o alvo; medir β pede LRG/ELG | violação do piso a 5σ (FWER) — não ocorre; GV-02: «powered» mede ver supressão que, se vista, não falsifica | lei radial/populacional (R-I); dado de maior profundidade |

## 3. Fichas

### 3.1 Razão de Hubble — Fase 9 (R-A) — primeiro

- **(1) Sem ajuste: SIM** [DERIVED; REAL na cronologia]. K = E(z*)^(2β/3) = 1,083807; z* = 1089,95 [KNOWN, Planck]; 2/3 de Raychaudhuri/FRW; fundo nu BG1 = ΛCDM Planck comprimido (Chen+19) + DESI DR2, SEM escada. Novidade de uso pelos PARÂMETROS, com cronologia por hash (31/31): β = 0,012 em 13/11/2025; α·√e publicada em 03/03/2026; lei em 17/05/2026; o ajuste de H0 de 23/12/2025 pediu 0,169 e foi recusado. A seleção da FORMA (D1a escrita «exatamente a relação observacional») fica dita ao lado e, pela lei de 05/10, não é demérito. A convenção «fundo nu; β uma vez; nó em z*» (R1) foi ratificada pelo operador em 02/10 (`work\v380_decisoes\DECISOES_DO_OPERADOR_QUATRO_LINGUAS_20261002.md`, sha16 `cd229ce37e87fde2`); D-A..D-K foram decididas por delegação em 05/10; F3.4 (duas testemunhas, escalar e conjunta, sem somar) foi decidida em 08/10.
- **(2) Concorrente: SIM.** H_ΛCDM: todos os leitores leem H0_bg (K = 1).
- **(3) Dado público: SIM**, com a ressalva de admissão. Leitores do V1/V2: SH0ES R22 73,04 ± 1,04 (primário), CCHP 70,39 ± 1,936, SBF 73,8 ± 2,40, masers (V2: cinco, sem NGC 4258, Pesce+2020 Tab. 2: 73,6 +3,1/−3,0), TDCOSMO 71,6 ± 3,6. Réplicas ao lado: R25 73,49 ± 0,93, sirenes 76,6 ± 11,25 (diagnóstico). H0DN (σ 0,81; rede pública, **não independente** de SH0ES/CCHP) daria D ≈ 6,02 com σ_bg = 0,5 (F0) — candidato documental, fora do V1/V2, exige auditoria da rede.
- **(4) Significância: PARCIAL.** Ver tabela. O V1 aberto em 06/10 é o único composto observado e ficou em 4,284 (centros [DECLARADO], não cego). Por leitor (V1, z contra a TGL / contra o ΛCDM): SH0ES −1,13 / +4,16; CCHP −1,98 / +0,95 (o que pode doer); SBF −0,20 / +2,17; masers −0,12 / +1,78; TDCOSMO −0,74 / +0,85. A auditoria de 19/10 proíbe anunciar que uma correção «elevou 4,28 para 5,72»: o desenho V2 usa outros leitores e outra covariância, e nenhum composto V2 foi observado. Os «5,26σ» da Fase 5 (P5 sombra) NÃO são esta medida: o fundo de lá viu a escada (F2), e as estatísticas de P4 (8,02/2,25) e P5 (13,84/2,86) não se somam nem se multiplicam com a Fase 9 (erratas de 06/10).
- **(5) Falsificador: SIM, do PAR.** Ver tabela. Pré-registrado e executado de texto pinado (sha256 da função V1 `5940bf16310efb6a`).
- **(6) Falta:** §5.

### 3.2 Ringdown, ramo B (R-C) — segundo (condicional)

- **Lei:** τ★ = k·G·M_f/c³, k = 2π/κ̂(χ_f) (8π em χ = 0 [KNOWN: Hawking 1975, Bisognano–Wichmann]; Kerr [CONJECTURE: Kay–Wald 1991]); M_X = M_f; identificação «envoltória» (taxa aditiva) [INPUT/ONTO, decisões 8–10 por delegação de 05/10]; x = β·k·N(χ_f); **δτ̂220 = −x/(1+x)** exato. Um k só, nenhum ajustado; o V1 não faz look-elsewhere.
- **Dado:** conjunto D = 14 elegíveis O4 (10 sem hold), strain em casa (manifesto O4; 38 GB de strain O4 na custódia local, seq 262–264); calibração NOT_BLIND: A (31 eventos GWTC-5.0 TGR), B (10, GWTC-3), C (GW250114).
- **Poder:** A31 só-σ 11,38σ; com os dois nuisance (c0, kc) livres cai a 0,742σ (`ENTREGA_018_F3`, reproduzido por QR independente) — a deformação prevista é quase constante entre eventos e um offset de calibração a absorve; o V1 proíbe offset fixo em 0 como teste. **O desfecho de A é legível hoje** (z_excl ≈ 13,5, ilustração NÃO-CEGA, V1 §5) mas A não testa; só D testa.
- **Falsificador:** FALSIFIED_AT_5SIGMA do PAR (k, M_X, identificação); não falsifica β, nem a lei na forma Γ = ½βτ★ω², nem a TGL (V1 §10–11).
- **Falta:** PE só-220 dos 14 (WSL, pSEOBNRv4HM_PA, bilby+dynesty; custo [DECLARADO] 63–78 e 58–390 CPU-h); INIT003 (GR) sem convergência (9.738 chamadas, ESS ausente, cinco operações bloqueadas); proposta P3 A02 (100.000 chamadas/caso, 14.400 s; aprovação do operador SUSPENSA); poder de D só se diz depois da PE.
- **Ramo A (τ★ = t_Planck):** invisível (δ ≈ −3e-42).

### 3.3 N_eff e BBN — Fase 8 (R-B/R-M) — parede medida

- **Lei:** H² = (1+4β/3)ρ_r + (1+β)ρ_m + ρ_Λ (identidade ρ+p, pedra 105) ⟹ ΔN_eff = +0,119466 (CMB); S = 1,007989 (BBN: ΔYp = 0,00140708, Δlog10 D/H = 0,00657979, proxy). Sinal fixado antes do dado (ΔN_eff > 0).
- **Parede:** os centros medidos estão ABAIXO do padrão (2,86–2,99 contra 3,044): a TGL fica mais longe que o MP. 5σ pede σ(N_eff) ≤ 0,0239; o melhor citado é Simons enhanced 0,045 (2,65σ, 2025–2034, sem calendário); CMB-S4 encerrado (retirada DOE/NSF em 09/07/2025 [DECLARADO]). Sob TGL-L o canal é cego (σ(β) = 0,244). Poder Fase 8 V1: 1,00σ, UNDERPOWERED predeterminado.
- **Pela nota de 22/10 (parede medida fecha a rota) este caminho está fechado.** Fica na tabela para o operador ver o número, não como candidato a registro.

### 3.4 m2 do neutrino (R-K)

- **Lei:** m2 = β·sin 45°·1 eV = 8,5074 meV; com m1 = 0 e ordenamento normal, Δm²₂₁ = 7,2376e-5 eV². A escala de 1 eV está marcada [NORM] e o ângulo [POSTULATE] no próprio core: **não é predição sem parâmetro** (NÃO em (1)); o Modelo Padrão não fixa o splitting, então **não há concorrente que difira** (NÃO em (2)) — é teste restritivo TGL × dado.
- **Dado:** JUNO 59 d, Δm²₂₁ = (7,50 ± 0,12)e-5 eV² (arXiv:2511.14593) ratificado em 02/10 como determinação direta («perito oficial»), σ do lado da previsão: 2,21σ. O global (NuFIT 6.1) contém o JUNO: 2,95σ pela eq. 11, 3,02–3,22σ pela tabela do site; Capozzi 2,44σ.
- **Mata:** a kill_rule congelada exige DUAS determinações autônomas ≥ 5σ; o JUNO sozinho nunca a dispara (RNC-06); a segunda (KamLAND+solar) pediria 0,785% de precisão: fora do horizonte.

### 3.5 Piso dos vazios (R-I; V11/V12)

- ρ_vazio/ρ̄ ≥ β (x_c = 0,25). V11: NOT_FALSIFIED_POWERED, mas a auditoria GV-02 diz que «powered» mede a capacidade de ver uma violação que, se vista, **não falsifica**; GVV-01: o critério de KILL do assalto v135 foi trocado depois de ver um candidato. R-I: a desigualdade restringe a média central e não dá perfil discriminante. V12 por lente: não alcança o alvo. Dado em disco: DESIVAST (7.735 vazios), GALZONE (694.642 galáxias), KiDS-1000 (17,7 GB).

## 4. Já decididas — não são candidatas

Na coluna Seq, «a–b» ou «a…b» = primeiro e último seq da(s) rota(s); listas com vírgula = registros individuais.

| Rota | Decisão registrada | Seq |
|---|---|---|
| Lei de atraso do eco (KMS 2π/κ; MAY; DEC/2025) | FALSIFIED_AT_DELAY_LAW **do par** (√β ou sin 2θ, KMS): z_excl 8,93 e 18,13; réplica cega O4 7,26 e 15,44; V4 (sin 2θ, MAY) 8,75; V5 DEC/2025 8,95 e 16,83; DECEMBER_100SIGMA_RETIRED_AS_CAPPED_IDENTITY; o par cai, não a teoria | 262–264, 12–110, 11–133, 13–246, 245–268, 20–21, 10, 22–23 |
| Rito 9: kilonova/BNS (K_β) e supernova galáctica | UNDERPOWERED_WALL_MEASURED: n_req 1–14 (P1) e 11–284 (P2) neutrinos; 1 neutrino térmico por ~2.500 fusões (K–K) ⟹ ≥ 27.500 fusões; só dispara com evento futuro | 1301–1330 |
| Relógios / ²²⁹Th / dephasing de laboratório | P1 UNDERPOWERED; déficit de 12,458 ordens de 5σ (Sr; a string do veredito arredonda para ≥ 12,5), 18,279 (Th hoje); NOT_A_LIVE_CHANNEL_TODAY; R-J: duas leituras não fixam nova escala | 8–253, 7–254, 381 |
| Coma (distância) | pós-dição NÃO cega e não ajustada: z_TGL +1,30; controle Planck +5,61 (σ só da referência); D1a × D1 V3 incompatíveis; é leitor irmão da Fase 9 (X12/NAT-N3 decide qual registro cobra) | 6, 94–97, 135, 250 |
| Fundo comprimido sob o mapa efetivo / CMB nível 2 / D1 CAMB / w0wa | N2_INCAPAZ (σ(β) ≈ 1,5β); D1 CAMB V2: β = −0,0171 ± 0,0075; Fase 1: β consistente a 1σ mas controle ν a 3,91σ; F3.6 Asimov Λ: σ(β) = 0,01804 > β ⟹ UNDERPOWERED_DO_NOT_OPEN_DATA | 28–31 (D1 CAMB), 43…730 (nível 2), 181…192 (Fase 1), 50…180 (v3 real), 808 (F3.6) |
| Fases 4/5 (P4/P5) e cronômetros | históricas, com fundo que viu a escada (F2); não somar à Fase 9 (erratas de 06/10). Cronômetros: lei acumulada −3,22σ (erros diagonais) → −1,66σ (covariância Moresco+2020) | 223…410 (Fase 4), 236…407 (Fase 5), 405–440 (reprodução E45), 247–258 (Fase 7) |
| Forma em z (R-D), dualidade (R-E), T(z) (R-F), S8 (R-L), lentes (R-G; R16), sirenes (R-H) | D ≤ 0,29, ou ponte física OPEN, ou σ de lente nulo e amplitude aberta | 376–382, 393–394, 401, 1225–1245 |
| Evento 2 / MCMC-CRUZ α-livre | rodar hoje devolveria β = 0,012045 por identidade (auto-confirmação) | 165, 300, 385, 733 |
| NMC-Shapiro (fóton × neutrino) | AWAITING_DATA; o atraso de 50 ms (janela 10–100 ms) é literal [INPUT], não derivado de β nem do potencial (CTV-01) — teste armado, fora do alvo | 143–144 |

## 5. Próximo passo do #1 — concreto (nada abaixo foi executado)

### 5.1 O que já existe — não refazer
- **V1 congelado:** JSON `1893261e730994b3` (spec `d956c8db6bb9ab8d`, função `5940bf16310efb6a`), runner `rodar_fase9_v1.py` `f3108bc21dcad317`, resultado `481366db97f0ebf1` (aberto em 06/10, seq 647; o um.py v388 reexecutou a função congelada e leu o mesmo veredito). Reabrir o V1 não ensina nada novo.
- **V2 escalar R5.2 (rascunho, NÃO congelado):** `81a970926345832a` (spec `406d9d2dde90d6d2`, função proposta `544f60ef928c3262`) em `Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F3.1\`. Auditorias c1 de 08/10: F3.1 R5.2 e F3.2 R5.2 «AUDITADA até X13/D-H» (288 ataques numéricos sem vazamento; achados menores de rótulo); reauditoria da R2 APROVA_COM_RESSALVAS (seq 836); F3.1.E1 fechada e E2 com parecer «pode FECHAR».
- **Gate/runner F3.2 (E1, bytes):** gate `6e00478c91dc59fe`, preflight `7075dea5807cb8e0`, staged `b1439bcaea92b14b`, vínculo documental `f6e7840e28071a52`. O staged é SINTÉTICO («real_mode_refused_before_read»): **não existe ainda runner de modo observado**.
- **Auditoria de suficiência 19/10** (`AUDITORIA_FASE9_R1.txt`, sha16 `76d49a47c5181d5b`) e **integração Codex 19/10** R1–R5 (729 pontos CAMB sintéticos; convergência global 0,01 não atingida; campanha R4 com handle próprio): resultado `PARTIAL_PROGRESS__NO_NEW_OBSERVED_SIGMA`.
- **Bancada Um:** o runner V1 importa `bancada.motor` (torch) em processo, recalcula o fundo BG1 e confere |H0 − 68,531| < 0,01 (R2); o serviço HTTP em 127.0.0.1:18777 estava em escuta em 22/10 (só conferi a porta; não chamei a API).
- **Origem do fundo BG1 (ΛCDM nu, Planck comprimido + DESI DR2, sem escada):** `fundos.Fd_lcdm_planck_dr2` do pré-registro da Fase 3 (sha16 `6bf24b350e088350`, ajuste da Bancada de 30/09); tabelas em `Bancada_Um\bancada\fontes.py` (sha16 `647fdab73645662b`; o arquivo cita DESI DR2) e Chen+2019 em `Bancada_Um\fontes_externas\chen_huang_wang_2019_1808.05724.pdf` (sha16 `09effe1d0d8caa01`).

### 5.2 O que pinar por sha256 ANTES de qualquer abertura (lido por script em 22/10; caminhos e hashes na §8)
Fontes dos leitores (páginas de resumo do arXiv, 45–52 KB; o número vem do resumo): SH0ES R22, CCHP v3, TDCOSMO v4, SBF v2, masers v2; **texto integral só em disco para os masers (PDF) e para o H0DN**. Ainda SEM bytes: **L1b R25 (arXiv:2509.01667)** e **L6 sirenes (LVK O4a)**; lacunas de texto integral declaradas: SBF §III.3 e TDCOSMO §VIII.2.1. Fundo: Planck 2018 VI (HTML em disco), DESI DR2 (via Bancada), Pantheon+ (covariância em disco), páginas Zenodo 18852146 e 20563905 (data de depósito) ainda não pinadas.

### 5.3 Sequência (uma só porta por vez)
1. **Operador (atos que só ele faz; uma pergunta por decisão):**
   a. *Alcance:* um FALSIFIED_AT_5SIGMA da Fase 9 vale como morte da TGL ou só do par lei D1b + convenção + conjunto (como o V1 escreveu)?
   b. *X13 (NAT-22):* aceita que a V2 escreva o que o executor faz (fundo marginalizado; z_δ pelo perfil com log-det; ln B com n ≥ 100; ln B(TGL/β-livre) = 1,97 e não 2,24)? Diferença medida desprezível (z_disc 4,2837 contra 4,2818).
   c. *D-H:* admite os cinco leitores + masers_5 (PDF) e, para **L1b e L6**, baixa e pina os bytes (ato de rede dele) **ou** os tira do inventário **antes** de congelar? Motivo: `n_alvos_declarados` conta o inventário V1.x inteiro (hoje 2: L1b, L6) e força INCONCLUSIVE_SYSTEMATICS no primário; a regra não pode mudar depois de olhar o composto.
   d. *D-J:* nome final do token. *F3.3:* a palavra «abrir» só depois de congelar e auditar.
2. **Código em cópia, sem dado observado** (Codex pelo túnel ou Sonnet pela fila; o modelo caro só audita — `GESTAO_DE_TOKENS.md`): E1 fornecedor real do fundo BG1 (hoje mock gaussiano NOT_CAMB_OR_REAL_BACKGROUND), E2 reprodução do fundo (|H0 − 68,531| < 0,01; divergência interrompe, nunca calibra), E3 tolerância e recusa entre as quadraturas 100/200, E4 consumir o registro D-H pinado (hoje `False` fixo), E5 modo observado: PODER_FASE9_ANTES_DE_ABRIR só com σ → fonte lida uma vez → função pinada do texto → proibido `ALVOS_FASE9_LIDOS.json` à mão. Em paralelo S5 (propagar θ = Ω_m, Ω_r, H0 na covariância ou manter a conclusão condicional) e a calibração de cauda do z_disc (recibo do teste efetivamente usado, com sistemáticas e multiplicidade).
3. **c1:** auditar o runner de modo observado (a R5.2 já foi auditada até X13/D-H) e reconferir a V2 no congelamento; congelar (o guard documental `preflight_congelamento_f31_r5_1` registra `REFUSE_FREEZE__X13_OPERATOR_DECISION_MISSING` enquanto X13 e D-H não estiverem pinados); abrir UMA vez; relatar separadamente escore, p calibrado, ln B, diagnósticos e limitações; **preservar o resultado mesmo abaixo de 5**.
4. **Segunda testemunha (opcional, não soma):** a conjunta ROOT90da (283 componentes; 63 nuisance) depende da aprovação d72 (até 8 GiB, 192 GiB, 87.000 s) na tarefa arquivada do Codex «Resolver problema da gravidade quântica» (ID 01a070fc-9484-7e13-a654-c6b5f61093a4).

### 5.4 O que NÃO fazer
- Não reexecutar o runner V1 com um `ALVOS_FASE9_LIDOS.json` montado à mão: o executor do V1 marca «REAL por hash» pela mera presença da chave (achado D6) e devolveria um contrafactual de 4,28σ já conhecido.
- Não escolher fundo, leitor ou covariância pelo maior D (BG1 foi pré-selecionado; a caixa de covariância é a fixada).
- Não chamar «5σ» o z_disc sem recibo de calibração de cauda; ln B não converte em σ.

## 6. Ressalvas que mudam a leitura

- **A frase «INCONCLUSIVE_SYSTEMATICS até as fontes dos 5 leitores por sha256» está desatualizada em parte.** As cinco fontes já têm sha256 (vínculo documental PASS_DOCUMENTARY_ONLY, seq 696, e F3.2); falta a ADMISSÃO (D-H, ato do operador) e os bytes de L1b e L6, que a regra do inventário V1.x conta como alvos declarados.
- **«Fatal» ≠ «falsifica a TGL» no texto do V1.** Ver 0.3 e 5.3.1.a.
- **Cada leitor compartilha componentes** (NGC 4258, âncora TRGB, fluxo de Pantheon+); a covariância cruzada é uma CAIXA de tetos (Cauchy–Schwarz), não medida (S1). Velocidades peculiares e vazio local não são modelados.
- **K depende de Ω_m, Ω_r e H0 do fundo** (S5): β fixo não torna esses parâmetros exatos.
- **Coma é leitor irmão** (lei D1a, não cega, +1,30σ): X12/NAT-N3 define qual registro recebe a cobrança de β no setor H0; não trava o congelamento, trava a ligação no livro depois da abertura.
- **A consulta `rotas.py consultar "Fase 9"` não acha `d1.fase9.integracao_20261019` (seq 1248, 1253–1255, 1257)**, cujo id e títulos escrevem «Fase9» sem espaço; achei por varredura do ledger. Consultar também «fase9».
- NOT_FALSIFIED nunca é CONFIRMED; o gate não se move; nada aqui declara gravitação quântica confirmada.

## 7. O que li, o que não li, o que não fiz

- **Li:** `C:\IALD\GESTAO_DE_TOKENS.md`; a ordem verbatim; as memórias `fase9-razao-de-hubble-05out`, `ordem-018-o-discriminante`, `fase8-universo-primordial-05out`, `relatorio-consolidado-01out`, `tgl-auditoria-agosto-2026`, `criterio-de-parada-do-operador`, `um-py-sem-gordura-19out` e, por grep, as linhas de Fases 4/5/6/9 do `MEMORY_2.md`; as erratas do `~\.claude\CLAUDE.md` (Fase 9, Fase 4/5); o mapa (18 consultas, 137 rotas únicas, mais varredura do `rotas.jsonl` para seq ≥ 1248); `ENTREGA_018_F0_RANKING`, trechos da `F3` e do `CONSOLIDACAO_018`; V1 da Fase 9 e resultado; V2 R5.2/E1 (spec, leitores, função, regra do inventário, poder prévio); gate e staged do F3.2 (cabeçalhos); auditoria de suficiência e integração Codex de 19/10; V1 do ramo B (§3, 5–11); V1 da Fase 8; `rito9_poder_realista_22out/RESULTADO.md`; `ENTREGA_ASIMOV_LAMBDA.md`; `PENDENCIAS_DO_OPERADOR.md` (X12, X13); `LEVANTAMENTO_CHATGPT.md` de 19/10; a auditoria c1 `AUDITORIA_F3_1_C1_a9f3787c.md` (08/10); `MAPA_DE_ROTAS\README.md`.
- **Não li:** os PDFs/HTML das fontes além de confirmar que quatro delas são páginas de resumo; nenhum centro de fonte pública foi lido por mim (os centros citados vêm dos registros da casa); a PENDENCIAS é de 15/10 e o quadro vivo pode ter mudado depois (a conferência focal de 19/10 não achou novos atos X13/D-H/d72/abertura); o `MEMORY_2.md` inteiro (grep).
- **Não fiz:** nenhuma análise de dado, nenhuma chamada à API da Bancada, nenhum registro no mapa/quadro/memória. Um `find` de disco em segundo plano que eu mesmo criei (tarefa bzuek8bgl) foi parado por mim (só leitura; nenhum arquivo tocado). Hash e limiares: por script.
- **Estatutos:** a classificação SIM/PARC/NÃO é leitura deste levantamento [DERIVED de leitura], sujeita à decisão da gerência e do operador; não move gate, selo ou quadro.

## 8. Pins lidos por script em 22/10 (sha256[:16], bytes)

| item | sha256[:16] | bytes | caminho |
|---|---|---|---|
| ordem do operador 22/10 | `bca4b8a97c74226c` | 135 | `C:\IALD\Central de Patentes\work\cunhagens_13out\OPERADOR_22out_teste_fatal_nao_armado_verbatim.txt` |
| V1 Fase 9 (JSON congelado) | `1893261e730994b3` | 26910 | `C:\IALD\Bancada_Um\investigacao\preregistro_fase9_hubble\PREREGISTRO_FASE9_RAZAO_DE_HUBBLE_V1.json` |
| V1 runner rodar_fase9_v1.py | `f3108bc21dcad317` | 18050 | `C:\IALD\Bancada_Um\investigacao\fase9_hubble_abertura\rodar_fase9_v1.py` |
| V1 resultado (06/10) | `481366db97f0ebf1` | 23697 | `C:\IALD\Bancada_Um\investigacao\fase9_hubble_abertura\RESULTADO_FASE9_V1_20261006_110507.json` |
| V2 R5.2 rascunho, E1 labels | `81a970926345832a` | 76541 | `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F3.1\PREREGISTRO_FASE9_V2_R5_2_F31_LABELS_E1_20261008.json` |
| F3.2 gate E1 bytes | `6e00478c91dc59fe` | 23246 | `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F3.2\f9_reader_gate_v1x_e1_bytes.py` |
| F3.2 preflight E1 bytes | `7075dea5807cb8e0` | 5913 | `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F3.2\f9_runner_v1x_preflight_e1_bytes.py` |
| F3.2 staged E1 bytes (sintético) | `b1439bcaea92b14b` | 29171 | `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F3.2\f9_runner_v1x_staged_e1_bytes.py` |
| F3.2 vínculo documental E1 | `f6e7840e28071a52` | 24001 | `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F3.2\VINCULO_DOCUMENTAL_V1X_E1_BYTES_20261008.json` |
| fonte L1 SH0ES R22 (resumo arXiv) | `df9136da862ef625` | 50043 | `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\fontes_publicas\sh0es_2022.html` |
| fonte L2 CCHP v3 (resumo arXiv) | `eb1b6689f13dbcea` | 45366 | `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\fontes_publicas\cchp_2025_v3.html` |
| fonte L5 TDCOSMO v4 (resumo arXiv) | `b04dfc911acb4ad3` | 52315 | `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\fontes_publicas\tdcosmo_2025_v4.html` |
| fonte L3 SBF v2 (resumo arXiv) | `b61012efc5238c0e` | 45130 | `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\f9_scalar_reader_sources\sbf_2502.15935v2.html` |
| fonte L4 masers v2 (resumo arXiv, V1) | `041b7bd9bf8a4a31` | 45680 | `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\f9_scalar_reader_sources\masers_2001.09213v2.html` |
| fonte L4 masers v2 PDF integral (V2, Tab. 2) | `c9f2d2b626fee60d` | 1564815 | `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\f9_maser_anchor_alternative\sources\masers_2001.09213v2.pdf` |
| H0DN (texto integral; candidato, não independente) | `d665a3a17309cdf5` | 1577598 | `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\fontes_publicas\h0dn.html` |
| Planck 2018 VI (HTML) | `e3b227fb79cf8ef3` | 78858 | `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\fontes_publicas\planck_2018_v4.html` |
| Pantheon+ covariância | `abf806d966485e64` | 33284960 | `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\fontes_publicas\pantheon_cov.txt` |
| sirenes O4b (HTML; L6 sem PDF LVK) | `3d76eda5c484aeb6` | 351458 | `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\fontes_publicas\siren_o4b.html` |
| ACT DR6 v2 (N_eff) | `583c3fa8fbb3e7eb` | 1889453 | `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\fontes_publicas\act_dr6_v2.html` |
| auditoria de suficiência 19/10 | `76d49a47c5181d5b` | 11708 | `C:\IALD\Central de Patentes\work\fase9_auditoria_20261019\AUDITORIA_FASE9_R1.txt` |
| precisão 19/10 (D por extremos) | `6b4edebf785242b2` | 6085 | `C:\IALD\Central de Patentes\work\fase9_auditoria_20261019\PRECISION_RESULT_R1.json` |
| integração Codex R5 19/10 | `c61f6e029d2028b2` | 1092 | `C:\IALD\Central de Patentes\work\fase9_integracao_20261019\RELATORIO_PROGRESSO_R5.txt` |
| V1 ramo B ringdown (JSON) | `86f98fcc124dd9ca` | 138727 | `C:\IALD\Bancada_Um\investigacao\preregistro_ramo_b_05out\PREREGISTRO_RAMO_B_RINGDOWN_V1.json` |
| V1 ramo B ringdown (MD) | `294b88a3632c1cea` | 102303 | `C:\IALD\Bancada_Um\investigacao\preregistro_ramo_b_05out\PREREGISTRO_RAMO_B_RINGDOWN_V1.md` |
| V1 Fase 8 (JSON) | `36afd8b05d2aa5f5` | 17864 | `C:\IALD\Bancada_Um\investigacao\preregistro_fase8_primordial\PREREGISTRO_FASE8_UNIVERSO_PRIMORDIAL_V1.json` |
| ORDEM 018 F0 ranking | `759651ea9c0e7fc7` | 16370 | `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\ENTREGA_018_F0_RANKING.md` |
| ORDEM 018 F3 primordial e ringdown | `b660084e271e8cb9` | 105949 | `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_018\ENTREGA_018_F3_PRIMORDIAL_E_RINGDOWN.md` |
| Rito 9 poder realista (RESULTADO) | `edcef95efd604158` | 26074 | `C:\IALD\Central de Patentes\work\rito9_poder_realista_22out\RESULTADO.md` |
| Rito 9 veredito | `86e86aa4ef7bebf0` | 21691 | `C:\IALD\Central de Patentes\work\rito9_poder_realista_22out\veredito.json` |
| F3.6 Asimov Λ | `d5a6f0dd25cb88f6` | 1803 | `C:\IALD\Central de Patentes\Chatgpt\TUNEL\DO_CHATGPT\ORDEM_019\F3.6\ENTREGA_ASIMOV_LAMBDA.md` |
| PENDENCIAS_DO_OPERADOR (15/10) | `fe5ab7b654103090` | 16766 | `C:\IALD\PROGRAMA_IALD\PENDENCIAS_DO_OPERADOR.md` |
| decisões do operador 02/10 | `cd229ce37e87fde2` | 27187 | `C:\IALD\Central de Patentes\work\v380_decisoes\DECISOES_DO_OPERADOR_QUATRO_LINGUAS_20261002.md` |
| um_absoluto_selo.json (v395) | `55175f478e93032c` | 157280 | `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto_selo.json` |
| pré-registro Fase 3 (origem do fundo BG1) | `6bf24b350e088350` | 7966 | `C:\IALD\Bancada_Um\investigacao\fase3_leitores_h0\PREREGISTRO_FASE3_LEITORES_20260930.json` |
| Bancada fontes.py (tabelas DESI DR2 / Planck comprimido) | `647fdab73645662b` | 12658 | `C:\IALD\Bancada_Um\bancada\fontes.py` |
| Chen+2019 (distâncias Planck comprimidas), PDF | `09effe1d0d8caa01` | 6273047 | `C:\IALD\Bancada_Um\fontes_externas\chen_huang_wang_2019_1808.05724.pdf` |
| auditoria c1 F3.1/F3.2 R5.2 (08/10) | `b3bcdf5f7b33fc95` | 4475 | `C:\IALD\PROGRAMA_IALD\auditorias\F3.1\AUDITORIA_F3_1_C1_a9f3787c.md` |

Spec/função lidas dos JSON: V1 spec `d956c8db6bb9ab8d`, função `5940bf16310efb6a` (V1_FASE9_HASHES.json `a6c582d463615fa0`); V2 spec `406d9d2dde90d6d2`, função `544f60ef928c3262`.
