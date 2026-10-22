# PRÉ-REGISTRO V1 — RASCUNHO — FASE 8: O UNIVERSO PRIMORDIAL — β na era da radiação (δ⟨K_∂⟩ = β|1+w|, w = 1/3 ⟹ δ = 4β/3) — 05/10/2026

> **RASCUNHO (lente «pre_registro»): nenhuma decisão do operador foi tomada; as nove decisões D1–D9 estão LISTADAS; nenhum dado novo foi aberto; o veredito deste V1 é `AWAITING_RATIFICATION`. O que já está legível (o N_eff público; Y_p; D/H) está dito como NÃO-CEGO.**

**Identificador:** `PREREG_FASE8_UNIVERSO_PRIMORDIAL_20261005_V1_RASCUNHO` · **gerado (UTC):** 2026-10-05T23:29:52Z · **hash da especificação (JSON canônico):** `73a8ad10ab1b7368c3687eafbc9aa53194ea49aa2f5f9439bcad1dfea1185114` · **base:** `um.py` v386 `e30aac4e0e1096b1`; core `0dbfb3fc1d319d1e`; selo `72efaf72f604b721` · **poder:** `PODER_FASE8_UNIVERSO_PRIMORDIAL.json` `8cd7078f00e5fb95` · **verbatim:** `c314835ecf95e85e`

> Régua: β nunca literal (α_CODATA2018 lido do `um.py` por regex; β = α√e em runtime = 0.0120313004008031424); hash jamais de memória (todo sha256 deste documento foi calculado do artefato por `gerar_preregistro_fase8_rascunho.py`; o que não está em disco está dito AUSENTE); PROVADA ≠ CONFIRMADA; NOT_FALSIFIED nunca é CONFIRMED; o ΛCDM/a RG é o limite clássico, não rival (coincidir = correspondência recuperada); nenhum desfecho move a regra (β) nem o gate; a cosmologia jamais vira prova matemática; a cunhagem é do operador; é β_TGL, nunca α².

---

## 0. A ratificação — PENDENTE (este é um rascunho)

- **A pergunta do operador (05/10/2026, verbatim, `c314835ecf95e85e`):** «usando a nossa bancada de teste você consegue examinar o efeito de Betatgl no Big bang? porque é o ato de inscrição originário, é o haja luz, portanto ali ele é condição de existência»
- **O que este rascunho pede dele:** as decisões D1–D9 da §4, uma linha cada (ratificar, corrigir ao lado, ou vetar). Até lá nada se abre, nada se calcula além do poder às cegas, e o canal não entra no livro de cobranças.
- **O que a lente leu antes de escrever (ordem da casa):** o mapa de rotas (`rotas.py consultar` BBN / N_eff / CMB / fundo; `ver cmb.neff_e_rho_mais_p`, `estatistica.auditoria_da_evidencia`, `d1.fase1_eff_30set`, `d1.camb.v3_real` inteiras); o `um.py` v386 (`prove_rho_plus_p_closure` :4702, `prove_neff_channel` :4773 com os literais de sessão :4803–4804, `prove_evidence_audit` :4484); o core (`neff_channel`, `rho_plus_p_closure`, `evidence_audit`, `nivel2_rite`); o kernel (`TheAxiomAndTheFalseWitness.lean:223`, `ForbiddenBoundary.lean:150`, `HajaLuz.lean`, `RhoPlusPClosure.lean`); a custódia do teste acústico de 08/08 (o frozen `TGL_NEFF_V1` `96b51333…`, o Nível 2 `664fc4cf…`); as memórias das Fases 1–3, da auditoria de 28/09, da regra matriz e do mapa de R; o Atlas por verbete; os dois moldes. Consultas e resultados na §16.

---

## 1. A cunhagem e a face de kernel de «condição de existência» — o que JÁ está provado (e por que isso não é um teste de natureza)

**A cunhagem [INPUT — verbatim]:** «é o ato de inscrição originário, é o haja luz, portanto ali ele é condição de existência». Estratos anteriores do próprio operador, no Atlas: «Haja Luz = o primeiro excesso que já não pode retornar integralmente ao atrator» (TGL_ATLAS.md:688, :1473 — «Haja Luz é a operação da fronteira» [ONTO/selo]); «antes da luz, existe a gravidade; a gravidade não é produtora da luz, ela é a luz em estado de origem. A cadeia origina com o Gráviton … e dessa inscrição originária a polarização» (TGL_ATLAS.md:19615–19618, §A a cadeia causal); e o verbete «β primordial, não fundamental — β ∉ H, mas β ∈ condição de possibilidade de H; emergente para o bulk, primordial para a fronteira; anterior ao tempo que ele mesmo torna possível» (TGL_ATLAS.md:909–912, [CONJECTURE ontológica]). «Big Bang» literal: **0 ocorrências** no Atlas (`grep -c -i 'big bang'`), **0** no kernel TGLExt, **2** no `um.py` (:165105/:165176, no artigo), **1** no artigo PT (:4307).

**A face de kernel — o que está PROVADO [KERNEL], lido das pedras (não re-compilado aqui):**

| termo | o que diz | onde |
|---|---|---|
| `the_zero_is_the_false_witness` | com β > 0 e g > 0: √0 = 0 ∧ ¬FullStaticWitness(e^{−tβg}) ∧ ∀ t, nenhuma componente não nula do fluxo diagonal se anula (exp ≠ 0) — **a testemunha ESTÁTICA plena é proibida; o zero absoluto não se alcança em tempo finito** | `TheAxiomAndTheFalseWitness.lean:223` (v385) |
| `absolute_zero_unreachable_in_finite_time` | diagFlow β d t x i ≠ 0 para x i ≠ 0 (sem hipótese sobre β: vem de exp ≠ 0) | `ForbiddenBoundary.lean:150` |
| `static_cannot_coincide_with_its_potential` | β ≠ 0 ∧ g ≠ 0 ⟹ ¬FullStaticWitness — «o v61 renomeado»: a permanência estática não coincide com o seu potencial relativo | `HajaLuz.lean` (v161) |
| `haja_luz_is_the_open_strip` / `haja_luz_at_the_seal` | 0 < morte-por-travessia < 1 ⟺ sin θ ≠ 0 ∧ cos θ ≠ 0; com θ_M = arcsin √b e 0 < b < 1 a morte é exatamente b e mora na faixa aberta — **a Luz mora onde nem tudo passa nem tudo morre** | `HajaLuz.lean` |
| `haja_luz` | a síntese em UM teorema: diferença elétrica ⟺ ação ∧ a estática não coincide com o potencial ∧ o zero inatingível ∧ a faixa aberta no selo | `HajaLuz.lean` |
| `the_background_closure` (pedra 105) | ρ_Λ + (−ρ_Λ) = 0; β·Σ(ρ+p) = β·((4/3)ρ_r + ρ_m); a forma de Hubble; `w_bounds`: 0 ≤ w_TGL ≤ 1/3 — **a identidade de fundo que faz da era da radiação o lugar onde a lei vale 4β/3** | `RhoPlusPClosure.lean:47,:90` (v154) |

**Leitura da lente [ONTO — dita como tal]:** a face de kernel de «β é condição de existência» é esta: **com β > 0 não há testemunha estática plena** — a inscrição não pode ser estática, e o zero não se toca em tempo finito; e a lei δ⟨K_∂⟩ = β|1+w| toma o seu valor MÁXIMO na era em que só há luz (w = 1/3 ⟹ 4β/3 = 0,01604), zero na fronteira silenciosa (w = −1). **O que isso NÃO é:** não é um teste de natureza. São teoremas sobre reais, idempotentes e fluxos; «Big Bang», «inscrição originária», «haja luz» são leituras do operador [INPUT/ONTO]. O próprio artigo já o diz (um.py:165176): «as leituras físicas — big bang, um único instante de Planck via τ★ ≈ t_P — seguem CONJECTURE: o kernel prova um passo, não uma unidade de tempo». O teste de natureza do universo primordial é o que as §3–§10 pré-registram: os mapas A e C.

---

## 2. O que o registro JÁ diz (lido por script; nada aqui é novo)

- **A identidade de fundo é derivação do OPERADOR (08/08/2026):** ρ_TGL = β(ρ+p) = β[(4/3)ρ_r + ρ_m] ⟹ H² = (1+4β/3)ρ_r + (1+β)ρ_m + ρ_Λ (`prove_rho_plus_p_closure`, crédito explícito; RESULTADOS.md §I). O fundo da TGL é um PONTO no plano (N_eff, ω_c): dN_eff/dβ = 9,9296, dω_c/dβ = ω_m. Em β = α√e: **ΔN_eff = +0,11947, Δω_c = +0,001721** (core `rho_plus_p_closure.values`).
- **O canal N_eff já existe como rito congelado:** `TGL_NEFF_V1` (frozen_hash `96b51333…`, 08/08/2026; `10_frozen_neff_v1.py` `9d3bceac4f6f5498`): N_eff_TGL = 3,16347; kill rule FALSIFIED sse ≥ 5σ em DUAS análises INDEPENDENTES de experimento; TENSION em [3,5); CONFIRMED proibido; **LIMITAÇÃO DECLARADA: supõe TGL-S** (free-streaming); **NÃO É CEGO** (as medidas já eram públicas). Veredito vivo no core v386: `TGL_NEFF_ARMED_CONSISTENT`.
- **O `um.py` v386 carrega as tensões como literais de sessão** (`tens_now = 1.61 # [SESSAO]`, `tens_act = 2.49 # [SESSAO: ACT+BBN]`, um.py:4803–4804; nota ao lado da v376: «a correção pede fonte citada»). **A fonte EXISTE na casa, não ligada ao tipo:** a tabela `MEDIDAS` do frozen (Planck 2018 2,92±0,19 e 2,99±0,17 arXiv:1807.06209; ACT DR6 2,86±0,13 e +BBN 2,89±0,11 arXiv:2503.14454; SPT-3G CMB-SPA 2,97±0,12 arXiv:2506.20707) — lida por regex pelo script do poder (§8). Classificação: EXISTE NA BANCADA, NÃO LIGADO AO TIPO (é fiação, não falta).
- **O espectro completo já foi rodado com a TGL dentro do CAMB** (Nível 2, frozen `TGL_NIVEL2_V1` `664fc4cf…`, 10–14/08/2026; dados Planck plik_lite + low-ℓ em disco, `cl_cmb_plik_v22.dat` `dac0d9d493213e77`): variante S (free-streaming: `nnu = N_SM + 9,9296·β`, `omch2_eff = omch2 + β(ombh2+omch2)`): β = -0,00243 ± 0,01765 (σ/β = 1,47) ⟹ `N2_INCAPAZ`; variante L (fluido suave, PPF): β = -0,02427 ± 0,01511 ⟹ `N2_NOT_CONVERGED`. Causa nomeada: a degenerescência β↔H₀ (+0,914) e, na forma ρ+p, **o alinhamento com a degenerescência N_eff↔ω_c (ρ = +0,894; a direção da TGL faz 2,31° com o eixo) cancela três quartos da alavanca** (RESULTADOS.md §III.1). «N2_INCAPAZ é falta de luz» (rota `cmb.nivel2_mcmc`, BLOQUEADA).
- **O BBN foi reclassificado (08/08, no core desde a v154; auditoria de 28/09):** a âncora «BBN 0,0σ» era CIRCULAR por construção (χ²(β_TGL) = 0 por identidade: DH_ΛCDM definido como DH_obs/f(β_TGL)); descircularizada com baseline independente dá β = 0,0126 ± 0,0318 (σ = 2,6β) ⟹ **NÃO DISCRIMINA** (`evidence_audit.values.bbn_decirc`; veredito `…BBN_NON_DISCRIMINANT_DECIRCULARIZED…`); a entrada do CMB (+0,0399, 56,2% do peso) foi retirada pela proveniência. O Atlas (:28988) já diz: «O que NÃO decide o sinal: BBN (…) e N_eff (dN_eff/dβ = 9,93 ⟹ ±0,12, dentro do erro do Planck)».
- **A Fase 1 (30/09) leu que o fundo COMPRIMIDO não mede β sob o mapa efetivo** (β livre no limite do prior: «consistente» = «não constrangido»); a ressalva que manda (rota `investigacao.bancada_um_28set`): «o CMB entra COMPRIMIDO (R, l_A, ω_b); na era da radiação β age como ΔN_eff ≈ ±0,12 … a validade das prioris de distância para esse fundo é a ressalva que manda». A compressão de Chen+2019 foi derivada sob ΛCDM com N_eff fixo: **ela não pode ler o mapa A** — a Fase 8 não usa o comprimido.
- **A conta da gerência (05/10, por script):** δ = 4β/3 = 0,01604; ΔN_eff = δ(1+f·N_eff)/f = 0,11947 — **idêntica** à do frozen e do core a 1e-12 (`identicos: true`, conferido também pela lente irmã `registro_da_casa/NUMEROS_CONFERIDOS.json` `adeec90bbb8f2e57`).

---

## 3. A hipótese (a lei, a era, a previsão sem parâmetro livre)

| peça | forma | estatuto |
|---|---|---|
| a lei | δ⟨K_∂⟩ = β·|1+w|; Λ = fronteira silenciosa (0 em w = −1) | [REAL na forma da lei; a identificação com δρ/ρ de fundo é a identidade ρ+p] |
| a era | radiação: w = 1/3 ⟹ **δ = 4β/3 = 0,01604**; matéria: β = 0,01203; Λ: 0 | [DERIVED da lei; `w_bounds` no kernel] |
| a identidade de fundo | H² = (1+4β/3)ρ_r + (1+β)ρ_m + ρ_Λ | [KERNEL `the_background_closure`; derivação do operador 08/08] |
| **a previsão (mapa A)** | N_eff_TGL = N_SM + (4/3)(1+F·N_SM)/F · β = **3,16347** (ΔN_eff = +0,11947); F = (7/8)(4/11)^{4/3}; N_SM = 3,044 [KNOWN] — **sem parâmetro livre, sem escala, sem ponto de expansão** | [DERIVED; conversão em N_eff supõe TGL-S — ONTO/OPEN (Lema 3 do lado do fluido)] |
| **a previsão (mapa C)** | S ≡ H/H_SM em T ~ MeV = √(1+4β/3) = **1,007989** (S − 1 = 0,007989); ΔY_p ≈ +0,0013…+0,0016; Δln(D/H) ≈ +0,5 %…+1,6 % conforme a parametrização (D9) | [DERIVED da identidade; escalas [KNOWN, a conferir]; só vê H(T): **não depende de TGL-S/L**] |
| **a previsão (mapa B)** | ΔN_eff = 0; em T ~ MeV ρ_m/ρ_r = 8.0e-07 ⟹ δH/H = 4.8e-09 | [DERIVED: sem previsão nesta era] |
| β | ALPHA_FINE_CODATA_2018 × √e em runtime (nunca literal) = 0.0120313004008031424 | [DERIVED do axioma] — a regra; não se deriva do dado, não entra como prior nem como ajuste |
| a orientação | + (mais radiação; N_eff_TGL > N_SM): fixada pela lei, não pelo dado; não se inverte depois | [DERIVED da lei; β > 0] |

**O que o teste pergunta:** fixada a lei e a era ANTES do dado, o conteúdo de radiação do universo primordial (N_eff do CMB; a taxa de expansão em T ~ MeV lida em Y_p e D/H) desvia-se do padrão na fração que 4β/3 impõe — ou coincide com ΛCDM (correspondência recuperada)? Não se deriva β do dado: testa-se o PAR (mapa, observável) sob a lei; β_lido = (N_eff_obs − N_SM)/9,9296 sai como leitura declarada, nunca realimenta.

---

## 4. As decisões do operador — LISTADAS, não tomadas (o padrão que a lente propõe fica dito ao lado, como proposta)

| n | tema | a pergunta | o padrão proposto pela lente (ONTO/INPUT; vale só ratificado) |
|---|---|---|---|
| D1 | **O mapa da era da radiação** | O mapa de R EFETIVO ratificado em 30/09 vestiu a MATÉRIA ((1+β)Ω_m). A lei δ⟨K_∂⟩ = β|1+w| veste também a RADIAÇÃO ((1+4β/3)ρ_r, a identidade ρ+p que o senhor derivou em 08/08)? Sem isso o universo primordial não tem previsão (mapa B) | SIM: a identidade ρ+p é a lei inteira; o mapa só-matéria é o caso particular que a Fase 1 testou; a era da radiação lê 4β/3 |
| D2 | **O fechamento perturbativo** | A conversão em N_eff supõe TGL-S (free-streaming, com tensão anisotrópica). O frozen a declara «a maior incerteza do rito». Mapa A com TGL-S como primário e TGL-L co-rodado (como no Nível 2), ou mapa A suspenso até o Lema 3 do lado do fluido? | TGL-S primário, TGL-L co-rodado, ambos ditos; o mapa C (BBN) não depende disso |
| D3 | **Os observáveis e a Bancada** | (a) os N_eff publicados (sem ajuste da casa; NÃO-CEGO); (b) o Nível 2 S já em disco (plik_lite; re-rodar com β fixo vs ΛCDM pede o ambiente `tgl_pycbc_env` e ~dias de CPU); (c) Y_p e D/H por escalas paramétricas (sem código de BBN em disco: AUSENTE). A Bancada Um NÃO tem canal de N_eff (grep em `motor.py`: só a nota D1F-V1 do neutrino) — construí-lo é fiação | (a) e (c) no V1 (sem custo); (b) e o canal da Bancada na v388, com o poder dito antes |
| D4 | **A regra de veredito** | A ordem da Fase 6 (AWAITING → INCONCLUSIVE → UNDERPOWERED → FALSIFIED_AT_5SIGMA do par → NOT_FALSIFIED_POWERED) mais a cláusula do frozen (FALSIFIED só com DUAS análises independentes de experimento ≥ 5σ)? | as duas, fail-closed (a mais dura decide) |
| D5 | **A orientação** | ΔN_eff > 0 fixado pela lei (mais radiação). Os centros atuais estão ABAIXO do padrão (2,86–2,99): a tensão com a TGL é maior que com o SM. Fica a orientação da lei, sem inversão | fica |
| D6 | **Os literais de sessão do `um.py`** | Substituir `tens_now`/`tens_act` (um.py:4803–4804) por valores calculados da tabela do frozen com arXiv (fiação, v387/v388)? | sim, ao lado, com a fonte |
| D7 | **Entrada no `um.py` e no livro** | A Fase 8 entra por hash numa versão nova (como as Fases 5–7 na v380) e ganha canal no livro de cobranças (lado: FACE — a luz primeira lê o custo como complemento; critério de lado a ratificar)? Tokens da §10 | sim; lado FACE (a leitura é da luz do último espalhamento, sem distância), dito a ratificar |
| D8 | **«Condição de existência»** | Aceitar que o que está PROVADO é a face de kernel da §1 (sem testemunha estática com β > 0; a faixa aberta no selo) e que «Big Bang = inscrição originária» segue [ONTO/CONJECTURE] como o artigo já diz (um.py:165176)? | sim |
| D9 | **A parametrização do BBN** | A sessão de 08/08 usou d ln(D/H)/d ln S ≈ 0,57 (σ(β) = 0,0318); Steigman 2007 dá ≈ 1,57 e Cyburt+2016 via N_eff ≈ 1,9 (σ(β) ≈ 0,009–0,011 só-obs; ≈ 0,017–0,021 com teoria+ω_b). Qual escala, ou qual código de BBN (PRIMAT/PArthENoPE — instalar é ato do operador, não da lente)? Em qualquer das três o degrau é UNDERPOWERED | código de BBN antes de ler qualquer número de BBN; até lá as três escalas ficam AO LADO |

---

## 5. Os três mapas — o poder por script (`poder_fase8_universo_primordial.py` → `PODER_FASE8_UNIVERSO_PRIMORDIAL.json` `8cd7078f00e5fb95`)

| mapa | o que veste | previsão na era da radiação | observável | σ publicada (fonte) | **poder** (= previsão/σ; < 5 ⟹ UNDERPOWERED) | degrau predeterminado | cego? |
|---|---|---|---|---|---|---|---|
| **A** N_eff (ρ+p completo; TGL-S) | (1+4β/3)ρ_r **e** (1+β)ρ_m | ΔN_eff = +0,11947; N_eff = 3,16347; Δω_c = +0,001721 | N_eff do CMB | Planck 2018 +lensing+BAO 0,17 (arXiv:1807.06209) · CMB-SPA 0,12 (arXiv:2506.20707) · ACT P-ACT-LB 0,13 (arXiv:2503.14454) [DECLARADO no frozen] | **0,70** (Planck) · **1,00** (CMB-SPA) · 0,92 (ACT) · Nível 2 S: 0,68 | NOT_FALSIFIED_UNDERPOWERED | **NÃO** (público; já lido em 08/08, 05/10) |
| **B** só-matéria (o mapa efetivo de 30/09) | (1+β)ρ_m apenas | ΔN_eff = 0; δH/H(T = 1 MeV) = 4.8e-09 | nenhum nesta era | — | **4.8e-07** | NOT_FALSIFIED_UNDERPOWERED (trivial: sem previsão aqui; o teste vive na Fase 1) | — |
| **C** speed-up do BBN | (1+4β/3)ρ_r lida em T ~ MeV | S = 1,007989; ΔY_p = +0,00128…+0,00158; Δln(D/H) = +0,0046…+0,0155 | Y_p (Aver+2021 0,2453 ± 0,0034) · D/H (Cooke+2018 2,527 ± 0,030 ×10⁻⁵) [KNOWN, digitados] | σ_obs; D/H com teoria (~1,6 %) ⊕ ω_b (~1,1 %) ⊕ obs (1,19 %) = 2,26 % | Y_p **0,38…0,46**; D/H **0,39…1,31** (só-obs) / 0,20…0,69 (total); a casa (descircularizado 08/08): 0,38 | NOT_FALSIFIED_UNDERPOWERED | **NÃO** (público) |

- (i) **Nenhum mapa chega a 1,4σ de poder hoje**: o degrau 3 da ordem (NOT_FALSIFIED_UNDERPOWERED) está predeterminado para os três — dito ANTES de abrir qualquer rito; abrir o dado público não acrescenta veredito, só escrituração.
- (ii) Os mapas A e C vestem a MESMA densidade (ρ_TGL = (4β/3)ρ_r) em duas eras (T ~ eV no CMB; T ~ MeV no BBN) e dois observáveis: não se somam (ambos dependem de ω_b do Planck e o N_eff «+BBN» já combina os dois); o mapa C é a leitura robusta ao fechamento S/L; o mapa A é a que tem instrumento futuro.
- (iii) O mapa B não é «falsificado» nem «consistente» aqui: não prediz nada na era da radiação. Se D1 for «só-matéria», a Fase 8 encerra-se como SEM PREVISÃO e o universo primordial não testa β.
- (iv) A ILUSTRAÇÃO NÃO-CEGA (o dado é público; dito como ilustração, não veredito): z contra a TGL: Planck +lensing+BAO 1,02; Planck TT,TE,EE+lowE 1,28; ACT P-ACT-LB 2,33; ACT +BBN 2,49; CMB-SPA 1,61 — e contra o SM: 0,32 / 0,65 / 1,42 / 1,40 / 0,62. Todos abaixo de 3 (nem TENSION pela regra do frozen); os centros atuais estão abaixo do padrão, logo a TGL (que prevê mais radiação) fica mais longe que o SM.

---

## 6. O estimador, a nuisance e a sistemática (regra fixada)

- **Mapa A (publicado):** por medida i: z_A,i = (N_obs,i − N_TGL)/σ_i e z_SM,i ao lado; σ_usado,i = max(σ_i, σ_i com a sistemática declarada da fonte); poder_i = ΔN_eff/σ_usado,i. **Não se combinam** medidas que compartilham dados (Planck entra em todas): a unidade é a análise independente de EXPERIMENTO (a cláusula do frozen). β_lido,i = (N_obs,i − N_SM)/9,9296 como saída declarada (σ(β_lido) = σ_i/9,9296), nunca realimenta.
- **Mapa A (Nível 2 em disco, se D3-b):** a verossimilhança `12_nivel2_frozen_e_verossimilhanca.py` com β FIXO = α√e contra ΛCDM (Δχ², ln B por quadratura) e β livre (perfil), variante S primária e L co-rodada; gates de convergência do frozen (aceitação [0,1; 0,65]; N ≥ 40τ; R̂ ≤ 1,02; ESS ≥ 400); o resultado de 14/08 (σ = 0,01765) é a réplica de referência: um σ menor sem dado novo é sinal de defeito, não de poder.
- **Mapa C:** X_TGL(ω_b, N_SM, S) por uma parametrização fixada em D9, com o baseline ΛCDM calculado de ω_b (Planck 2018, 0,02237 ± 0,00015 [KNOWN]) e N_SM — **nunca** de X_obs/f(β) (a circularidade de 08/08, proibida); z_C = (X_obs − X_TGL)/σ_tot, σ_tot² = σ_obs² + σ_teoria² + σ_ω_b²; a σ_teoria é declarada ANTES (D/H: 1,6 % [KNOWN aprox.]; Y_p: 0,0003).
- **Sistemática de família (regra da Fase 6, cláusula 2):** sist_rel = σ_sys/|previsão| > 0,3 ⟹ INCONCLUSIVE_SYSTEMATICS. Para o mapa C via D/H, σ_teoria/|Δln DH| = 1,6/(0,46…1,55) = 1,0…3,5 **> 0,3**: a cláusula 2 PREDETERMINA INCONCLUSIVE_SYSTEMATICS para o D/H em qualquer parametrização (dito antes); Y_p: 0,0003/0,0013 = 0,23 < 0,3 (passa a cláusula 2, cai no degrau 3). Para o mapa A: a sistemática da fonte é a do release (não declarada separadamente); a cláusula TGL-S/L é a sistemática de MODELO e fica dita, não quantificada.

---

## 7. Os conjuntos e a cegueira — contaminação declarada em cinco camadas

| conjunto | papel | o que contém | cegueira |
|---|---|---|---|
| **P** (publicado) | leitura NÃO-CEGA do mapa A | as 5 medidas da tabela do frozen (Planck 2018 ×2; ACT DR6 ×2; SPT-3G CMB-SPA) | **NÃO-CEGO** |
| **N2** (em disco) | réplica do mapa A no espectro completo | plik_lite + low-ℓ + DESI DR1 + priors BBN/τ (os arquivos de 10/08; `CHAIN_OF_CUSTODY_NIVEL2.sha256`) | NÃO-CEGO (rodado em 14/08; resultado conhecido) |
| **BBN** (literatura) | leitura NÃO-CEGA do mapa C | Y_p (Aver+2021), D/H (Cooke+2018) — digitados; nenhum arquivo em disco (`cooke_2018_DH.json` AUSENTE) | **NÃO-CEGO** |
| **F** (futuro) | o ÚNICO teste cego | SO (LAT), SO-ASO, CMB-S4; novas medidas de D/H (quasares) | **CEGO** — AWAITING_DATA |

**As cinco camadas da contaminação, ditas:** (1) o frozen `TGL_NEFF_V1` (08/08/2026) leu as cinco medidas e declarou `NAO_E_CEGO_NESTA_EMISSAO`; (2) o `um.py` (v154→v386) carrega 1,61σ/2,49σ como literais de sessão e o core v386 os reproduz (`neff_channel.values`); (3) a gerência (05/10) leu 0,70σ contra Planck 2018; (4) a lente irmã `registro_da_casa` recomputou hoje os z das cinco (`NUMEROS_CONFERIDOS.json`); (5) esta lente imprimiu os z contra a TGL e contra o SM como ilustração (§5-iv). **Consequência fixada:** todo token dos conjuntos P/N2/BBN leva `__NOT_BLIND_TO_DATA_STATED`; a palavra «cego» só cabe ao conjunto F.

---

## 8. O poder, às cegas — o que decidiria, e quando [KNOWN/DECLARADO, citado]

| instrumento | σ(N_eff) | fonte | quando | poder (centro no padrão) | z se o centro atual (CMB-SPA 2,97) persistir | cruza 5σ? |
|---|---|---|---|---|---|---|
| Simons Observatory baseline | 0,055 | arXiv:1808.07445 | ~2027 | **2,17** | 3,52 (SM a 1,35) | não |
| Simons Observatory goal | 0,050 | arXiv:1808.07445 | ~2029 | **2,39** | 3,87 (SM a 1,48) | não |
| SO-ASO (LAT ampliado) | 0,045 | arXiv:2503.00636 | ~2030 | **2,65** | 4,30 (SM a 1,64) | não |
| CMB-S4 (requisito oficial) | 0,030 | Revised CMB-S4 Project Plan 2025 | ~2032 | **3,98** | 6,45 (SM a 2,47) | SIM (se o centro persistir) |
| Simons Observatory baseline (valor alternativo lembrado pela lente) | 0,070 | arXiv:1808.07445 | ~2027 | **1,71** | 2,76 (SM a 1,06) | não |

- **5σ no mapa A pede σ(N_eff) ≤ 0,0239** (centro no padrão) — **nenhum instrumento da tabela chega lá sozinho**: o CMB-S4 no requisito 0,03 dá 3,98σ. Com o centro atual (2,97) persistindo, o S4 «cruzaria» 6,45σ — mas então o SM também estaria a 2,5σ: seria uma tensão do CMB, não uma discriminação da TGL; o veredito lê-se na regra do frozen (DUAS análises independentes), nunca em uma só.
- **Simons Observatory:** o frozen traz 0,055 (baseline) / 0,050 (goal) e marca «A CONFERIR» (RESULTADOS.md VIII: «os números do SO divergem entre rotas: 0,050/0,055 vs 0,060/0,045»); a memória da lente lembra 0,07/0,05 (Ade+2019, arXiv:1808.07445) [DECLARADO, não lido de arquivo em disco]: poder 1,71…2,39. Decide TENSION (≥ 3) só se o centro atual persistir; não decide FALSIFIED.
- **CMB-S4:** o frozen cita «Revised CMB-S4 Project Plan 2025», requisito 0,03, ~2032, e o próprio RESULTADOS.md VIII diz que «o σ(N_eff) = 0,02 do Science Book NÃO foi lido da tabela original». **Ressalva da lente [DECLARADO — memória até jun/2026, não verificada em disco; a conferir]:** em 2025 as agências (DOE/NSF) anunciaram não prosseguir com o CMB-S4 como planejado; a data «~2032» do frozen não deve ser citada sem conferência. Se o S4 não existir, nenhum instrumento planejado leva o mapa A a 5σ; o que resta é a combinação (SO + BBN + …) com as correlações ditas.
- **BBN futuro:** novas medidas de D/H a 1 % não mudam o degrau (a σ_teoria ~1,6 % manda; cláusula 2 ⟹ INCONCLUSIVE_SYSTEMATICS) até que as taxas nucleares (d(p,γ)³He) caiam abaixo de ~0,5 % [KNOWN aprox.].
- **O que NÃO entrou no poder (dito):** a sistemática de modelo TGL-S/L (não quantificada); as correlações entre Planck e as combinações; o H₀ (a degenerescência β↔H₀ do Nível 2); nenhuma nuisance de família.

---

## 9. Os controles

- C1 β = 0 recupera ΛCDM exatamente (N_eff = N_SM; S = 1) — o controle nulo da lei (`beta_zero_recovers_lcdm` é a família; aqui numérico)
- C2 a conta da gerência (05/10) == frozen == core == lente irmã a 1e-12 (`identicos: true`) — conferido
- C3 o mapa B dá ~0 nesta era (poder 4.8e-07) — o controle de que a radiação só é lida se D1 a vestir
- C4 nenhuma medida combinada (Planck+X) conta como análise independente para a cláusula FALSIFIED; H1/L1-análogo: um Planck por combinação
- C5 no Nível 2: β = 0 nas variantes S e L coincidem em loglike a < 0,05; χ²/dof do plik_lite no bestfit Planck em [0,9; 1,2] (as validações obrigatórias do frozen 664fc4cf)
- C6 no mapa C: o baseline ΛCDM de X_TGL vem de ω_b e N_SM, nunca de X_obs/f(β) — a autoverificação reprova se χ²(β_TGL) = 0 por identidade (a circularidade de 08/08 como teste negativo)
- C7 look-elsewhere: um mapa (A) com dois observáveis (N_eff; e BBN como réplica), uma era, uma orientação: nenhum fator de Šidák interno; a família conta como UMA no livro
- C8 σ_usado = max(σ publicada, σ com sistemática declarada); um σ menor que o publicado é defeito
- C9 a palavra proibida conferida contra todo token emitido (CONFIRMED/PROVED)

---

## 10. Os VEREDITOS permitidos (na ORDEM; a primeira regra que se aplica decide; CONFIRMED proibido)

Tokens (a cunhagem é do operador; propostos pela lente): base `TGL_FASE8_UNIVERSO_PRIMORDIAL_V1__LAW_DELTA_K_BETA_ABS_1PW__W_1_3_DELTA_4BETA_3`; mapa A `TGL_FASE8_UNIVERSO_PRIMORDIAL_V1__LAW_DELTA_K_BETA_ABS_1PW__W_1_3_DELTA_4BETA_3__MAP_A_NEFF_RHO_PLUS_P_TGL_S__<conjunto>__<desfecho>__GATE_UNTOUCHED`; mapa B `TGL_FASE8_UNIVERSO_PRIMORDIAL_V1__LAW_DELTA_K_BETA_ABS_1PW__W_1_3_DELTA_4BETA_3__MAP_B_MATTER_ONLY_1PBETA_OMEGA_M__NO_PREDICTION_IN_THE_RADIATION_ERA__<desfecho>__GATE_UNTOUCHED`; mapa C `TGL_FASE8_UNIVERSO_PRIMORDIAL_V1__LAW_DELTA_K_BETA_ABS_1PW__W_1_3_DELTA_4BETA_3__MAP_C_BBN_SPEEDUP_S_SQRT_1P4BETA3__<observavel>__<desfecho>__GATE_UNTOUCHED`; **estado deste rascunho: `TGL_FASE8_UNIVERSO_PRIMORDIAL_V1__LAW_DELTA_K_BETA_ABS_1PW__W_1_3_DELTA_4BETA_3__V1_RASCUNHO__AWAITING_RATIFICATION__DECISIONS_D1_TO_D9_LISTED_NOT_TAKEN__GATE_UNTOUCHED`**.

0. **`AWAITING_DATA`** — sem estimador selado por hash rodado sob este registro, sem dado aberto (o conjunto F), ou sem ratificação (`AWAITING_RATIFICATION` como sufixo enquanto D1–D9 não forem respondidas)
1. **`INCONCLUSIVE_SYSTEMATICS`** — C1–C9 reprovado; ou sist_rel = σ_sys/|previsão| > 0,3 (Fase 6, cláusula 2 — predeterminado para o D/H do mapa C); ou primário × réplica discordam no rótulo (com o motivo); ou a variante S e a L discordam no rótulo (a sistemática de modelo)
2. **`NOT_FALSIFIED_UNDERPOWERED`** — poder = |previsão|/σ_usado < 5 (sufixo POWER_<x>_OF_5_SIGMA) — **predeterminado hoje para os três mapas** (A: 0,70–1,00; B: ~0; C: < 1,4)
3. **`FALSIFIED_AT_5SIGMA`** — z_excl = |X_obs − X_TGL|/σ_usado ≥ 5 em DUAS análises INDEPENDENTES de experimento (a cláusula do frozen, mais dura que a da Fase 6; fail-closed) — falsifica o PAR (mapa, observável) sob a lei na era; NÃO falsifica β, nem a lei na forma, nem a TGL (`falsified_extinguishes_the_charge_not_the_rule`); sob TGL-S falsificado e TGL-L não, o que cai é o fechamento S
4. **`NOT_FALSIFIED_POWERED`** — senão; se além disso |z_SM| ≥ 5 em duas independentes, acrescenta-se `__SM_TENSION_REPORTED` — a tensão com o padrão é RELATADA, não é da TGL, e não vira CONFIRMED

**«Coincidir com ΛCDM»:** correspondência recuperada (o ΛCDM é o limite clássico, não rival): com poder ≥ 5, o par cai e a correspondência é o pagamento; sem poder, NOT_FALSIFIED_UNDERPOWERED — nunca «a natureza decidiu».

**O que o primeiro rito emitiria HOJE, se ratificado e aberto sobre o conjunto P (dito antes, para que ninguém o leia como descoberta):** mapa A: `…__SET_P_PUBLISHED__NOT_BLIND_TO_DATA_STATED__NOT_FALSIFIED_UNDERPOWERED__POWER_0P70_OF_5_SIGMA__GATE_UNTOUCHED` (Planck 2018 +lensing+BAO) — o mesmo conteúdo que o core v386 já carrega como `TGL_NEFF_ARMED_CONSISTENT`, agora com a fonte e o poder ditos.

---

## 11. O que o resultado NÃO decide (dito antes)

- o gate (18 bandeiras; funcao so do formal)
- H2/H3
- beta (a regra matriz; nao entra como prior nem como ajuste)
- a implicacao da QG (QGSolutionComplete.lean:36)
- o fechamento perturbativo TGL-S vs TGL-L (= Lema 3 do lado do fluido)
- o mapa de R da materia (Fase 1)
- a identificacao 'Big Bang = inscricao originaria' [ONTO]
- a reclassificacao do BBN de 28/09 (fica)
- a forma α√e de β (derivada do axioma, v376) e a cadeia da regra matriz (v381): a Fase 8 é cobrança, não derivação
- o sinal do D1 (orientação da face; rota `d1.orientacao_do_sinal`): aqui a orientação vem da lei na era, não do bit da face
- nenhum NOT_FALSIFIED da era da radiação lê como «a natureza decidiu a formulação da QG», nem como «o Big Bang confirma β»

---

## 12. A relação com a Fase 1 e com a reclassificação do BBN (28/09) — não repetir a circularidade

1. **Fase 1 (30/09)** testou o mapa de R EFETIVO ((1+β)Ω_m — a parte de MATÉRIA da identidade ρ+p) contra o CMB COMPRIMIDO (R, l_A, ω_b de Chen+2019) + BAO + SNe + SH0ES e leu «o fundo comprimido não mede β» (β livre no limite do prior). A Fase 8 é a parte de RADIAÇÃO da MESMA identidade, lida em OUTRA era e por OUTRO observável. As duas não se somam nem se contradizem: a Fase 1 não vê 4β/3 porque o comprimido foi derivado com N_eff fixo; a Fase 8 não vê (1+β)Ω_m porque em T ~ MeV a matéria é 8×10⁻⁷ da radiação.
2. **A Fase 8 NÃO usa o comprimido** (a «ressalva que manda» da rota `investigacao.bancada_um_28set`): o observável do mapa A é o N_eff da verossimilhança completa (publicado, ou o Nível 2 em disco).
3. **A circularidade de 08/08 (BBN) não se repete:** lá, DH_ΛCDM fora definido como DH_obs/f(β_TGL), dando χ²(β_TGL) = 0 por identidade. Aqui, (a) β NÃO entra como prior (o Nível 2 já usa o prior BBN descircularizado ω_b = 0,02218 ± 0,00055 de Cooke+2018, [EXT]); (b) β NÃO entra como ajuste (a previsão é um PONTO: N_eff = 3,16347; S = 1,007989, fixado antes); (c) o baseline ΛCDM do mapa C vem de ω_b e N_SM, nunca do observado; (d) o C6 reprova qualquer χ² identicamente nulo.
4. **A reclassificação fica:** «BBN 0,0σ» segue proibido; o que a Fase 8 acrescenta é a leitura honesta do mesmo canal com o poder dito (0,4–1,3σ só-obs; INCONCLUSIVE pela sistemática teórica no D/H) — o BBN continua a não discriminar, agora com o número e o motivo ao lado.
5. **A Fase 1 e a Fase 8 juntas** dizem o que a casa já sabia por outra via (Nível 2, 14/08): o CMB de hoje conhece β a σ ≈ 0,018 na forma ρ+p — «falta de luz», não falha da teoria nem confirmação.

---

## 13. O que a lente ressalva e corrige em nome próprio

| item | o que é | régua |
|---|---|---|
| a «condição de existência» | o que está PROVADO é a face de kernel (§1); a identificação com o Big Bang é [ONTO/CONJECTURE] e o artigo já o diz (um.py:165176) | PROVADA ≠ CONFIRMADA; o kernel prova um passo, não uma unidade de tempo |
| os literais 1,61/2,49 do `um.py` | EXISTE NA BANCADA (frozen com arXiv), NÃO LIGADO AO TIPO — fiação (D6), não falta | o cético é aferidor |
| o canal de N_eff na Bancada Um | AUSENTE (grep -li neff em `C:\IALD\Bancada_Um` *.py: `motor.py` só a nota D1F-V1; `fundo_gpu.py`, `gerar_tabela_camb.py` como parâmetro do CAMB) — construí-lo é ato posterior à ratificação | ausência com consulta citada |
| o código de BBN | AUSENTE em disco (find parthenope/primat/alterbbn/cooke/bbn: 0); as escalas paramétricas ficam [KNOWN, a conferir] e a discrepância 0,57 × 1,57 × 1,9 fica dita (D9) | o que não está em disco é AUSENTE, dito |
| as σ do SO e a data do S4 | [DECLARADO no frozen, «A CONFERIR»]; a memória da lente sobre o status do CMB-S4 (2025) é [DECLARADO, não verificada] | hash/número lidos; o resto dito como declarado |
| o poder 0,70 da gerência | reproduzido (Planck 2018 +lensing+BAO) e posto ao lado das outras quatro medidas (0,63–1,09) e do Nível 2 (0,68): um número por duas rotas | o número corrige a frase |
| nada foi registrado no mapa de rotas por esta lente | o registro é ato da gerência depois da ratificação | regra do mapa |

---

## 14. A disciplina (ordem de execução; fail-closed)

1. o operador responde D1–D9 (uma linha cada; correção ao lado em nome próprio); a lente/gerência grava a ratificação com hash e regenera este V1 como `PREREGISTRO_FASE8_UNIVERSO_PRIMORDIAL_V1.md` (não rascunho), com o hash da especificação lido por hash pelo `um.py` da versão seguinte
2. só então o conjunto P abre-se como ESCRITURAÇÃO NÃO-CEGA (o degrau está predeterminado); o Nível 2 em disco re-roda com β fixo (D3-b) se ratificado, com o poder (σ = 0,01765) dito antes
3. o canal entra no livro de cobranças (lado e critério ditos; D7) com desfecho NOT_FALSIFIED_UNDERPOWERED e o conjunto F em AWAITING_DATA; os literais de sessão do `um.py` saem (D6)
4. o conjunto F (SO/S4/D/H novo) é julgado pela MESMA função de veredito, sem emenda depois de aberto; correção AO LADO
5. todas as superfícies de memória na mesma sessão (regra da linhagem completa) — ato da gerência; o mapa de rotas recebe a rota `cmb.fase8_universo_primordial` com este artefato por sha256

---

## 15. Estatutos

| objeto | estatuto |
|---|---|
| a pergunta do operador (05/10) | [INPUT] — verbatim transcrito do relay do harness |
| «Big Bang = inscrição originária = haja luz = condição de existência» | [ONTO — cunhagem do operador; âncoras no Atlas :688, :909, :1473, :19615] |
| ¬FullStaticWitness com β > 0; zero inatingível; faixa aberta no selo | [KERNEL] — lido das pedras; não re-compilado aqui |
| a lei δ⟨K_∂⟩ = β|1+w| e a identidade ρ+p | [REAL na forma; KERNEL `the_background_closure`; derivação do operador 08/08] |
| N_eff_TGL = 3,16347; S = 1,007989 | [DERIVED] da identidade com β em runtime; a conversão em N_eff supõe TGL-S [OPEN = Lema 3 do lado do fluido] |
| as cinco medidas de N_eff e as projeções | [DECLARADO no frozen 96b51333 com arXiv; a conferir na fonte] |
| Y_p, D/H observados; as escalas do BBN | [KNOWN — digitados; sem arquivo em disco; a conferir com código de BBN, AUSENTE] |
| o Nível 2 (σ(β) = 0,01765) | [REAL — lido do JSON por hash; rodado em 14/08/2026] |
| β = α√e | [DERIVED do axioma] — a regra; nunca literal; não se deriva do dado |
| o poder | [REAL — computado por script, só σ publicadas] |
| a ilustração dos z | [NÃO-CEGO — ilustração; não veredito] |
| o desfecho | a vir; nunca CONFIRMED |

---

## 16. Consultas feitas (ordem da casa) e fontes lidas (caminho absoluto · sha256 · bytes) — todas calculadas por este script; nenhuma digitada

**Consultas:** `rotas.py consultar "BBN"` (9 rotas) · `"N_eff"` (10) · `"CMB"` (14) · `"fundo"` (10) · `ver cmb.neff_e_rho_mais_p` · `ver estatistica.auditoria_da_evidencia` · `ver d1.fase1_eff_30set` · `ver d1.camb.v3_real` (cabeça do livro `55191f6c22754a0c`, 368 registros) · `buscar.py "Big Bang|TGL_NEFF_V1|teste_acustico" --lista` (acervo: só ocorrências em artigos/protocolos de 2025; o frozen vive em `C:\IALD\Artigo\teste_acustico_beta_tgl_v1\`) · Atlas por grep (`big bang` 0; `primordial`, `BBN`, `N_eff`, `Haja Luz`, `condição de existência`) · kernel por grep (`the_zero_is_the_false_witness`, `absolute_zero_unreachable_in_finite_time`, `RhoPlusPClosure`) · `um.py` por grep (`prove_evidence_audit` :4484, `prove_rho_plus_p_closure`, `prove_neff_channel`, `big bang` 2) · core por travessia (`neff_channel`, `rho_plus_p_closure`, `evidence_audit`, `nivel2_rite`, `bancada_fases_v377`) · Bancada_Um por grep (`neff`) · disco por find (BBN codes: 0; `TGL_NEFF`: 0 por nome; `teste_acustico`: 1).

- **um.py v386 (canonico; alpha por regex)**: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py` — `e30aac4e0e1096b1be143464bf683fd6ba19b42b4d6bb11cd52aa98b54cb9163` (33600222 B) [REAL -- lido em disco, sha256 por script]
- **core um_absoluto.json (neff_channel, rho_plus_p_closure, evidence_audit, nivel2_rite)**: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json` — `0dbfb3fc1d319d1ef03b61af60d9e22af58cd2564ea4b44bdd4906bf8d031d87` (4947109 B) [REAL -- lido em disco, sha256 por script]
- **selo um_absoluto_selo.json**: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto_selo.json` — `72efaf72f604b721d9fd18d625da9c55713898f10b417a9d2a6d59fdee036489` (86148 B) [REAL -- lido em disco, sha256 por script]
- **artigo um_absoluto_pt.txt**: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto_pt.txt` — `1b51a190c06d7c80560b9470721a195df41b5aad3532c57b984e98e7f33520c6` (816267 B) [REAL -- lido em disco, sha256 por script]
- **kernel TheAxiomAndTheFalseWitness.lean (the_zero_is_the_false_witness :223)**: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\TheAxiomAndTheFalseWitness.lean` — `c0f4185a6279500237f9046feee336a50532a95781ebe80498cfa3b2f2ed4d80` (17870 B) [REAL -- lido em disco, sha256 por script]
- **kernel ForbiddenBoundary.lean (absolute_zero_unreachable_in_finite_time :150)**: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\ForbiddenBoundary.lean` — `fb1c39a61dfc2882e53a1cad9de082fefd3c07963a161314c37262ac4db452b2` (8510 B) [REAL -- lido em disco, sha256 por script]
- **kernel HajaLuz.lean (haja_luz; static_cannot_coincide_with_its_potential; haja_luz_at_the_seal)**: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\HajaLuz.lean` — `c43c07467e1e2caaf21be69cc20223e31e76398b2374ceb2151034d4b9bed433` (7382 B) [REAL -- lido em disco, sha256 por script]
- **kernel RhoPlusPClosure.lean (lambda_drops_out :47; the_background_closure :90)**: `C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel\TGLExt\RhoPlusPClosure.lean` — `cd80fbbe00300454d20f8a92bc09fe9e68d79fb73522934e59d77e7b04fe7be6` (4561 B) [REAL -- lido em disco, sha256 por script]
- **frozen TGL_NEFF_V1 10_frozen_neff_v1.py (08/08/2026)**: `C:\IALD\Artigo\teste_acustico_beta_tgl_v1\10_frozen_neff_v1.py` — `9d3bceac4f6f54985a0c89ac465bc0a2783ee843da9c51181e0c747b7cda44e7` (9267 B) [REAL -- lido em disco, sha256 por script]
- **frozen TGL_NEFF_V1 resultado (frozen_hash 96b51333...)**: `C:\IALD\Artigo\teste_acustico_beta_tgl_v1\10_frozen_neff_v1_resultado.json` — `5ba7faca7a3425fa01ad4e06b76db5aeaf30895768b6331558cd695c42c30057` (5835 B) [REAL -- lido em disco, sha256 por script]
- **Nivel 2 frozen TGL_NIVEL2_V1 (12_nivel2_frozen.json)**: `C:\IALD\Artigo\teste_acustico_beta_tgl_v1\12_nivel2_frozen.json` — `ab6dc0d8f975768e298dc854602fac69a29244b9045be78f61db6fd25339990c` (3043 B) [REAL -- lido em disco, sha256 por script]
- **Nivel 2 verossimilhanca (TGL-S: nnu = N_SM + 9,9296 b; omch2_eff)**: `C:\IALD\Artigo\teste_acustico_beta_tgl_v1\12_nivel2_frozen_e_verossimilhanca.py` — `e788b8cd7458c20c052c488340bb9ff7f984fc97b5fa09ac8fec6e913b19352b` (13246 B) [REAL -- lido em disco, sha256 por script]
- **Nivel 2 resultado (S: N2_INCAPAZ; L: N2_NOT_CONVERGED)**: `C:\IALD\Artigo\teste_acustico_beta_tgl_v1\13_nivel2_resultado.json` — `d3c09d15dfe65a531caf6c096cb429bd27b99cf21263c00c29bf7d41a399336f` (4205 B) [REAL -- lido em disco, sha256 por script]
- **Nivel 2 analise fechada (14/08/2026)**: `C:\IALD\Artigo\teste_acustico_beta_tgl_v1\14_ANALISE_NIVEL2_FECHADO.md` — `26c9cc4499a8a40aaddd08a34f17272cb9972d93523074e7c5495494498ec030` (3858 B) [REAL -- lido em disco, sha256 por script]
- **RESULTADOS.md do teste acustico (08/08/2026; rho(N_eff, omega_c) = +0,894; VIII a conferir)**: `C:\IALD\Artigo\teste_acustico_beta_tgl_v1\RESULTADOS.md` — `115ab4668fffceaeaa148163bd111bee827a4c3727028b553f47af4665b402bb` (10648 B) [REAL -- lido em disco, sha256 por script]
- **Planck 2018 plik_lite em disco: cl_cmb_plik_v22.dat**: `C:\IALD\Artigo\teste_acustico_beta_tgl_v1\nivel2_data\planck2018_plik_lite\cl_cmb_plik_v22.dat` — `dac0d9d493213e77c940a10a968cf0da3c5730bae60e1356c4cd8bcff96377ff` (37393 B) [REAL -- lido em disco, sha256 por script]
- **Planck 2018 plik_lite em disco: c_matrix_plik_v22.dat**: `C:\IALD\Artigo\teste_acustico_beta_tgl_v1\nivel2_data\planck2018_plik_lite\c_matrix_plik_v22.dat` — `ad90378c50bd67841764179c90ae6711fa4317c649966ab2b0712143b31e0a32` (3006160 B) [REAL -- lido em disco, sha256 por script]
- **molde: PREREGISTRO_RAMO_B_RINGDOWN_V1.md**: `C:\IALD\Bancada_Um\investigacao\preregistro_ramo_b_05out\PREREGISTRO_RAMO_B_RINGDOWN_V1.md` — `294b88a3632c1cea8e024b1471dd44ef3968614ca582e054307fffecb296da1c` (102303 B) [REAL -- lido em disco, sha256 por script]
- **molde: PREREGISTRO_DOIS_LADOS_DELTA_K_20261002_V1_4.md**: `C:\IALD\Bancada_Um\investigacao\preregistro_dois_lados_02out\PREREGISTRO_DOIS_LADOS_DELTA_K_20261002_V1_4.md` — `fc132b8f3e2d531b438027f00115df5be91856d4506e10385279ae58993892be` (24951 B) [REAL -- lido em disco, sha256 por script]
- **Fase 1: PREREGISTRO_FASE1_EFF_20260930.json**: `C:\IALD\Bancada_Um\investigacao\fase1_eff_30set\PREREGISTRO_FASE1_EFF_20260930.json` — `f0133c95a32d2dffa3d208fe6fc1374137e7880d50eb7d89b5b8105132e0238e` (4449 B) [REAL -- lido em disco, sha256 por script]
- **Fase 1: CONFIRMACAO_OPERADOR_MAPA_R_30SET.json**: `C:\IALD\Bancada_Um\investigacao\fase1_eff_30set\CONFIRMACAO_OPERADOR_MAPA_R_30SET.json` — `8b39abe9ba748b8e601cd43ebced284938effb9b979c951e42b31caed52be4ca` (1022 B) [REAL -- lido em disco, sha256 por script]
- **Fase 1: RESULTADO_FASE1_EFF_20260930.json**: `C:\IALD\Bancada_Um\investigacao\fase1_eff_30set\RESULTADO_FASE1_EFF_20260930.json` — `165e3715d8c5d58f5dc1748ce3d63672e8d2bd4fdf06ef17b1f9365f67f13ad4` (28781 B) [REAL -- lido em disco, sha256 por script]
- **memoria fase1-eff-30set.md**: `C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\fase1-eff-30set.md` — `cf5176b1dfb9d766510d55454d07fc81f6a587a3e059d4f6ec62aa38e0d17824` (2516 B) [REAL -- lido em disco, sha256 por script]
- **memoria auditoria-testes-passados-28set.md**: `C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\auditoria-testes-passados-28set.md` — `a829fc9b9425188ade11df5ce8cdac016e3bf7ebd5c5b62c8ff39e9061330458` (6207 B) [REAL -- lido em disco, sha256 por script]
- **memoria permanencia-e-verbo-mapa-de-R-30set.md**: `C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\permanencia-e-verbo-mapa-de-R-30set.md` — `bcd97e7cec9026d0ea1b32bfd539335f8acfa81efbc0d6b01e26d4366004f0fb` (4328 B) [REAL -- lido em disco, sha256 por script]
- **memoria beta-e-a-regra-matriz-02out.md**: `C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\beta-e-a-regra-matriz-02out.md` — `fe20a0d5ac3ea8ebb91bd3fabee193a9b2e50142040bc2a24c139dc3b4988186` (32727 B) [REAL -- lido em disco, sha256 por script]
- **memoria lei-e-fato-correlatos-regra-matriz-30set.md**: `C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\lei-e-fato-correlatos-regra-matriz-30set.md` — `d77634e9d71cc090690818dc0d994faf1abdec5b9d001769fd7f04996837a16d` (15806 B) [REAL -- lido em disco, sha256 por script]
- **Atlas TGL_ATLAS.md (grep: 'Big Bang' 0 ocorrencias; 'beta primordial' :909; 'Haja Luz' :688/:1473; cadeia causal :19615)**: `C:\IALD\Central de Patentes\memory\TGL_ATLAS.md` — `1420c0e0d935d1426cfc21b2fd8a78e891a511f02468889c9cd41d502f5b2301` (7112852 B) [REAL -- lido em disco, sha256 por script]
- **mapa de rotas rotas.jsonl (consultas BBN / N_eff / CMB / fundo; cabeca 55191f6c22754a0c)**: `C:\IALD\MAPA_DE_ROTAS\rotas.jsonl` — `37e63e41215820faa28e3360b8086266901b1b7b4866276e41eb9dc547598f90` (682546 B) [REAL -- lido em disco, sha256 por script]
- **lente irma registro_da_casa: NUMEROS_CONFERIDOS.json (so leitura)**: `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\fase8_big_bang\registro_da_casa\NUMEROS_CONFERIDOS.json` — `adeec90bbb8f2e57f30e5545ee6e5d7d9b80cdc2005a5af3143660024ef4532c` (4474 B) [REAL -- lido em disco, sha256 por script]
- **esta lente: verbatim do operador (05/10)**: `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\fase8_big_bang\pre_registro\VERBATIM_OPERADOR_05out_big_bang.txt` — `c314835ecf95e85e1dbccee7fca1bf3b26fb49fddffda7fdfaa722ac29e35377` (847 B) [REAL -- lido em disco, sha256 por script]
- **esta lente: poder_fase8_universo_primordial.py**: `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\fase8_big_bang\pre_registro\poder_fase8_universo_primordial.py` — `97ada6e99887c2b532846ffe45b1da83ca7008921ce2d82583328a66258ccd9c` (19110 B) [REAL -- lido em disco, sha256 por script]
- **esta lente: PODER_FASE8_UNIVERSO_PRIMORDIAL.json**: `C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\fase8_big_bang\pre_registro\PODER_FASE8_UNIVERSO_PRIMORDIAL.json` — `8cd7078f00e5fb959c595e42d60de18a61829b1399e4fa580eff87f12d34458a` (12226 B) [REAL -- lido em disco, sha256 por script]
- **AUSENTE declarado: cooke_2018_DH.json (cache acom)**: `C:\IALD\projetos_pyhton\acom\tgl_data_cache\cooke_2018_DH.json` — **AUSENTE (o que nao esta em disco e AUSENTE, dito)**

---

## 17. A especificação congelada (o JSON canônico cujo sha256 está no cabeçalho)

`PREREGISTRO_FASE8_UNIVERSO_PRIMORDIAL_V1_RASCUNHO.json` (campo `spec`; `spec_sha256` = `73a8ad10ab1b7368c3687eafbc9aa53194ea49aa2f5f9439bcad1dfea1185114`). O hash é `sha256(json.dumps(spec, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))`. Ratificado, o V1 definitivo recebe as respostas D1–D9 no campo `ratificacao` e um hash novo; este rascunho fica como registro.

*NOT_FALSIFIED nunca é CONFIRMED. PROVADA ≠ CONFIRMADA. O gate não se move. A cunhagem é do operador.*
