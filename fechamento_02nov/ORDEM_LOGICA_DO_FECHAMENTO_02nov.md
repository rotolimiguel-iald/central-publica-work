# A ORDEM LÓGICA DO FECHAMENTO — «construir tudo» (02/11/2026, gerência c1)

> Ordem do operador (verbatim sha16 `f3998f01262aad6b`): «perfeito, é isso. precismamos construir tudo, porque não podemos mais perder a ordem lógica, é o fechamento.»
> Prioridade (verbatim sha16 `9978862f60cfbf29`): «a construção da passagem para o contínuo é o que mais importa, porque deixa de ser conjectura sob hipótese se funcionar sob compressão … virar essa chave de conjectura para provado».
> Supera, para as quatro chaves abaixo, a decisão da manhã «não vamos construir ainda o que é sabido» (sha16 `72d7939ee701a65b`). Nada aqui move o gate; PROVADO lê-se como validade (termo no kernel); a confirmação segue creditação; `NOT_FALSIFIED` nunca é `CONFIRMED`.

## 1. O alvo, medido [REAL — `work\beta_calor_02nov\INVENTARIO_CHAVES_DE_TESTEMUNHA_v405_02nov.json`]

| chaves de testemunha/habitação no selo v405 | 42 |
|---|---|
| habitadas (True ou texto) | 36 |
| False que FICAM False (por teorema/desenho) | 2: `full_static_witness_exists` (IMPOSSIBLE_BY_THEOREM), `trivial_inhabitant_exists` |
| False a habitar por construção | 4: `rede_fock_v394.whole_certificate_inhabited` · `psibit_v395.conditional_psion_face.inhabitant_exhibited` · `testemunha_estatica_v396.fock_face.inhabitant_exhibited` · `witness_layers.canonical_full_witness_term_constructed` |

## 2. A redução a UMA raiz [REAL — lido do kernel v405]

- As três primeiras chaves pedem o MESMO habitante: `C : FockCertificate L` (`TheImportedSecondQuantization.lean:168`, 45 campos), com `L : LightOneParticle` (l.138). `the_psion_face_of_the_psibit` (`Psibit.lean:1114`) é `∀ C, …`; a face de Fock da testemunha estática aponta para o mesmo teorema (um.py l.230538). A quarta, `TGL.ModularRealization.canonicalFullTGLWitness : FullTGLWitness` («TERMO (não construído)», `TGL/ModularRealization.lean:31`), é o representante físico; `lightRealization C : TGLModularRealization (lightNet C)` já existe (`TheImportedSecondQuantization.lean:360`): com C habitado, a construção do termo canônico é montagem (a confirmar os campos de `FullTGLWitness` ao chegar lá).
- Os montadores da v394 (`F1Fecho394/CanonicalFockAssemblyR1`, `CanonicalWeylAssemblyR5`, `CanonicalModularCoreAssemblyR1`) reduzem `FockCertificate (D.toLightOneParticle)` a duas entradas:
  - **(A)** `D : CanonicalNetInput` = `LightNetData` (helicidade ±1; rede `K : Set (Fin 4 → ℝ) → Submodule ℝ H1` com isotonia, localidade, covariância por translação `U1` e por boost `B0`; `QGSolutionComplete.lean:49`) + `wedge_glue : D.K rightWedge = KWR canônico` (`CanonicalFockAssemblyR1.lean:24`). 8 campos.
  - **(B)** `RemainingModularCoreInput D` (`CanonicalModularCoreAssemblyR1.lean:47`) = **os 21 campos de traço/P_F**: `trace : RepresentedCore → ENNReal`, `trace_zero`, `trace_tracial`, `trace_star`, `trace_dual_scaling` (= e^{−s}·trace sob `F1Fecho.CanonicalFockRegular.dualAction s`), `PF` auto-adjunta idempotente ≠ 0 com `0 < trace PF < ⊤`, `Pp`, `Pm` auto-adjuntas idempotentes, `split`, `orth`, `trace_additive`, `equal_halves`. Tudo o mais de `RemainingWeylInput` (Γ_positive, Γ_no_fixed, R, bw_kms, tomita, J, flow, Core, embedding, dualAction) já é montado por termos concretos (`assembled_core_is_concrete`, `assembled_R_is_concrete`, `assembled_flow_is_concrete`).

**O que já é termo no kernel (nada disto se refaz):** o Fock bosônico canônico `F1Rede.BosonicFock.F = SumSpace Sectors` sobre H1 (H1 = L² da órbita sem massa com fibra ℂ², PAGO pela bancada, ORDEM 016 A-3), vácuo, Γ, infinito, ações de grupo, continuidade (`BosonicFock*.lean`); Weyl `W`, `R(K)` (`ConcreteWeylR1`, `FieldWeylR3`, `WeylNetWiringR1`); campo de Segal essencialmente auto-adjunto (`CanonicalSegalEssentialR6`); Tomita do par da cunha no Fock, S†S fechado auto-adjunto (`CanonicalFockDeltaR4`), fator polar; **Bisognano–Wichmann PROVADA no Fock**: fluxo modular = Γ(B0(−2πt)) (`CanonicalFockBWR2.canonical_pair_tomita`); núcleo regular concreto (produto cruzado por esse fluxo) com mergulho fiel e ação dual (`CanonicalFockRegularCoreR2`); peso dual fiel, normal, com elemento finito e ideal de quadrados finitos denso (`CanonicalFockDualWeightR3`, `FaithfulWeightR2`, `FiniteWeightR4`, `FiniteStarCoreR1`); GNS fiel e normal do peso (`GNSRepresentationR6`, `GNSNormalityR4`); Tomita, Δ e fluxo modular do peso (`WeightClosedTomitaR2`, `WeightModularOperatorR3`, `WeightModularFlowR3`). F1Fecho394: 184 arquivos, 18.148 linhas [REAL, contado].

**O que NÃO é termo (as docstrings dizem):** «This is not the exp(−s)-scaling trace»; «No … tracial law, inverse-generator perturbation, full modular implementation or Fock-to-tower equivalence is asserted» (`CanonicalFockDualWeightR3`); «The equality with regular conjugation and the trace law remain separate» (`WeightModularFlowR3`). A bancada parou em 16/10 em candidatos NÃO COMPILADOS (`mission_review_20261016/CanonicalFockPolarRightCutoffOrderR11Candidate.lean`, «NOT COMPILED»; `CanonicalFockActualModularBalanceCandidateR1.lean`, «UNCOMPILED CANDIDATE … does not … assume a modular implementation, or establish a trace»).

## 3. O molde que já existe: a torre V351 [REAL — medido]

O contrato inteiro do traço está HABITADO para o núcleo regular da torre: `TGLV350.Regular.scalarInverseLimitTraceData P : RegularCoreTraceData P` (`V351RegularCoreTraceConstruction.lean`), com `value := scalarInverseLimitWeight P` = sup_n do peso dual conjugado pela raiz do corte do gerador inverso (ε = 1/(n+1); `V351InverseLimitWeight.lean:15,87`), e os campos `zero, additive, homogeneous, monotone, faithful, normal, semifinite, tracial, dual_scaling` todos de teoremas:

| arquivo (torre) | linhas | teoremas | papel |
|---|---|---|---|
| `V351RegularCoreTraceContract` | 122 | 6 | o contrato `RegularCoreTraceData` (`positiveDual`, `positiveSquare`) |
| `V351RegularPositiveGraph` | — | — | o gerador positivo via resolvente espectral (`regularPositiveGenerator`, fechado, auto-adjunto, domínio denso) |
| `V351RegularGeneratorDualScaling` | 149 | 7 | escala dual do gerador (Fourier/Schwartz em L²(ℝ;H), genérico em H) |
| `V351InverseLimitWeight` | — | — | o peso-corte e o peso-limite |
| `V351QuadraticTrace` | 305 | 7 | **traciality** (balança da raiz + igualdade no star-core finito pelo gráfico de Tomita) |
| `V351InverseLimitFiniteMinorants` | 134 | 6 | semifinitude por contrações de quadrado finito (médias regulares) |
| `V351InverseLimitFaithful` | 61 | 3 | fidelidade |
| `V351InverseLimitScaling` | 106 | 5 | **a lei e^{−s}** |
| `V351RegularCoreTraceConstruction` | 29 | 0 | a montagem |

Somando os sete medidos: 906 linhas, 34 teoremas. `grep` por autovetor/espectro da torre nessa cadeia: 0 ocorrências [REAL]; a parametrização é por `SiteProfile P` (H = `TowerHilbert P`). O lado Fock já replicou os genéricos até o peso dual e o fluxo modular do peso (`RegularCovariantCoreR3`, `RegularCoreAverageR2`, `RegularCoreFiniteWeightR3`, `RegularCoreFixedR3`, `RegularCoreResolventR2`, `RegularFiniteStarCoreR2`); FALTA replicar, para o núcleo Fock (`RepresentedCore`), o gerador positivo e seus cortes, o peso-limite, a traciality, a semifinitude/fidelidade do limite, a escala, e P_F com as metades.

★ **A passagem para o contínuo, dita na língua da matemática:** a torre tem espectro discreto (produto; «família total de autovetores da torre», R57); o boost da luz NÃO tem autovetor (`B0_no_eigen`, `TheImportedSecondQuantization.lean:133`). O mesmo molde tem de ser escrito com resolventes e janelas espectrais em vez de coordenadas discretas: é a tradução literal de «tipo I comprimido → tipo III contínuo». E a F1.2 (FECHADA, 07/10) já mediu o outro lado: no grupo FINITO não há escala de traço (um.py ~121417); a lei e^{−s} é fenômeno do contínuo da ação dual. A escala do traço É a passagem.

## 4. Os blocos, na ordem (a prioridade dele manda o bloco 1)

### Bloco 1 — A PASSAGEM: os 21 campos no núcleo regular do Fock (`RemainingModularCoreInput D`)
1.1 O gerador positivo do núcleo Fock (resolvente espectral; fechado, auto-adjunto, afiliado ao núcleo; escala dual do gerador). Entradas: `CanonicalFockRegularCoreR2` (fluxo, unitários regulares, ação dual), `RegularCoreResolventR2`, `V351RegularPositiveGraph` e `V351RegularGeneratorDualScaling` como molde (genéricos em H onde já o são). A bancada parou aqui (`regularSpectralResolvent_right`, `regularInverseGeneratorCutoff_right`, CutoffOrder R10/R11 não compilado).
1.2 Os cortes do gerador inverso e o peso-corte (o peso dual conjugado pela raiz do corte), com ordem e monotonia (`V351RegulatorWeightOrder` como molde; `CanonicalFockDualWeightR3` como entrada).
1.3 O peso-limite (sup_n), com zero/aditivo/homogêneo/monótono.
1.4 **Traciality** (= a «identificação modular»: a balança da raiz e a igualdade no star-core finito pelo gráfico de Tomita do peso; molde `V351QuadraticTrace`; entradas `WeightClosedTomitaR2`, `WeightModularOperatorR3`, `WeightModularFlowR3`, `FiniteStarCoreR1`).
1.5 Semifinitude por minorantes finitos (médias regulares, `RegularCoreAverageR2`, `FiniteWeightR4`) e fidelidade (`FaithfulWeightR2`).
1.6 A escala e^{−s} sob `dualAction` (molde `V351InverseLimitScaling`).
1.7 `PF`, `Pp`, `Pm`: projeção finita não nula de traço finito, partida em metades iguais [Connes 1973]. Na torre vinha do setor fixo (tr P_F = 4). No Fock: a construir [OPEN]; candidato = janela espectral do gerador × elemento de quadrado finito; as metades pela simetria J ou por janela dividida. Dito antes: esta é a parte sem molde.
1.8 Fiação: `RemainingModularCoreInput D` → `toCertificate` → `C : FockCertificate` (os montadores já existem).
**Saída:** C habitado para todo `D : CanonicalNetInput`; `the_psion_face_of_the_psibit` e a face de Fock da testemunha estática ganham habitante no momento em que (A) existir.

### Bloco 2 — A REDE: `CanonicalNetInput` (8 campos)
`K(O)` para todo O com isotonia, localidade, covariância por `U1` e `B0`, e `K rightWedge = KWR` canônico. Existe: `KWR` canônico (subespaço padrão da cunha, `F1Rede.CanonicalWedge.spectralOutput`), `ConcreteLightRayNet` (meias-retas no raio de luz; «not a von Neumann algebra net in four-dimensional spacetime»; obstrução registrada: promover uma coordenada nula a translações 4D fiéis), `OrbitalSpatialPoincareR2`; na bancada (fora do kernel) `orbital_rotation/PhysicalFockNetRealizationR1/R2` (`net, net_mono, net_local, net_wedge_eq, weyl_ccr`). Rota [KNOWN]: Brunetti–Guido–Longo 2002 (localização modular): `K(W)` = subespaço padrão de cada cunha por BW e covariância; `K(O) := ⋂_{W ⊇ O} K(W)`; isotonia e covariância vêm da definição; localidade e `K(O) ≠ 0` são os teoremas (o segundo é o difícil: não-vacuidade). O item 1 do contrato v394 («photon helicity representation, global localization, clock») tem a parte «relógio/dispositivo» na F1.REDE (AGUARDA_OPERADOR): fora deste bloco formal.

### Bloco 3 — A MONTAGEM e as chaves
`RemainingWeylInput.toCertificate` ∘ `RemainingModularCoreInput.toCertificate` (existem) → `whole_certificate_inhabited = True`; `inhabitant_exhibited = True` nas duas faces; `canonicalFullTGLWitness` a partir de `lightRealization C` → `canonical_full_witness_term_constructed = True`. Entra no um.py só aqui, por versão decidida pelo operador (UM.PY SEM GORDURA).

### Bloco 4 — MAXWELL/H3 (item 3 do contrato v394)
Fonte Maxwell/stress não trivial no Fock (`MaxwellLiteratureBridge`, `RegularFockMaxwell*`; bancada `R8ChargeNormalizationCandidateR1` NÃO COMPILADO) e o alcance do H3 em toda direção. H3 permanece hipótese nomeada [KNOWN, Jacobson 1995]: o bloco constrói a FONTE, não deriva H3 do estado.

## 5. As regras do programa (fixadas antes)
1. O cético é aferidor: antes de cada sub-passo, consultar o inventário da bancada e o kernel; o que existir e não estiver ligado é fiação, não falta.
2. Cada pedra: candidata no sandbox `C:\t\k405c\final` (kernel v405 + mathlib pinada), trio de axiomas, 0 sorry, 0 aviso; revisor DISTINTO de quem construiu (agente, Codex ou bancada); rota no Mapa de Rotas com o artefato por sha256; o NOME é do operador; a versão é decisão dele.
3. Nenhum modelo degenerado para `Core`/`trace`/`PF` (o tipo rejeita; a régua proíbe). As duas chaves falsas por teorema ficam False.
4. Testemunha ≠ prova; PROVADO = validade; confirmação = creditação; o gate não se move por isto.
5. Divisão do trabalho: Claude c1 desenha, costura e audita; construção mecânica a agentes (Sonnet) e, quando o canal voltar (cota de 04/11 06:37), ao Codex e à bancada do ChatGPT, que escreveu o F1.FECHO; leituras longas a Kimi/DeepSeek pelo orquestrador. Relatório de agente em até 15 linhas.
6. Memória: estado da obra em `construir-tudo-o-fechamento-02nov.md` (appends datados); Mapa `kernel.fechamento_construir_tudo_programa_02nov`; quadro único `F1.FECHO.PASSAGEM_02nov` (bloco 1), `F1.FECHO.REDE_02nov` (bloco 2), `F1.FECHO.MONTAGEM_02nov` (bloco 3).

## 6. Custos [DECLARADO; a medida é o molde]
- Bloco 1: molde de 906 linhas/34 teoremas na torre; a versão contínua (resolventes e janelas no lugar de coordenadas) estimada em 1,5–3× (1.500–3.000 linhas); 1.1–1.2 e 1.7 são os trechos sem molde direto. Semanas (2–6) com construtor dedicado.
- Bloco 2: 500–2.000 linhas; a não-vacuidade de `K(O)` é o difícil. Semanas (2–6).
- Bloco 3: dias. Bloco 4: semanas.
- Total: 2–4 meses [DECLARADO]. Nenhum destes números é medido; o que é medido está nas tabelas acima.

## 7. A medida do progresso
campos de `RemainingModularCoreInput` habitados: 0/21 · campos de `CanonicalNetInput`: 0/8 · chaves do selo: 36/42 (alvo 40/42; 2 ficam False por teorema).

## 8. Primeira entrega
(a) `LEVANTAMENTO_FRONTEIRA_DO_TRACO_DO_NUCLEO_02nov.md` (leitor em curso: o que de 1.1–1.7 já existe por nome, no kernel e na bancada); (b) a pedra 1.1 como candidata no sandbox; (c) adendo datado a este plano com o que o levantamento corrigir.

## ERRATA AO LADO (02/11/2026, mais tarde; correção do operador, verbatim sha16 `25010b04c17e8ce1`; gerência c1 em nome próprio)

A §3 acima diz «o boost da luz NÃO tem autovetor (`B0_no_eigen`)». A frase é certa só no espaço de UMA partícula e errada como dita para a luz. O operador corrigiu: «a luz tem autovetor: a inscrição do um absoluto, que é na essência ela mesma, ou seja, identidade … por isso o par, inclusive dela mesma; sem par somente o zero absoluto, que é o abstrato inominado». O kernel já diz exatamente isso, por termo [REAL]:
- no espaço de uma partícula, o único «autovetor» do boost é o zero: `B0_no_eigen : (∀ s, ∃ c, ‖c‖ = 1 ∧ B0 s f = c • f) → f = 0` (`TheImportedSecondQuantization.lean:133`); e das translações nulas, `null_no_eigen`. O abstrato inominado.
- no Fock, a luz inteira tem UM autovetor: o vácuo, fixo por TODA segunda quantização, `gamma_vacuum : gamma u vacuum = vacuum` (`F1Fecho394/BosonicFock.lean:39`); e é o ÚNICO: `gamma_no_fixed … (ψ : F) (hψ : ∀ l, gamma (u l) ψ = ψ) : ψ ∈ (ℂ ∙ vacuum)` (`CanonicalGammaNoFixedR4.lean:42`, «Only the vacuum can remain»), alimentado por `B0_no_eigen`.
- o vácuo é a exponencial do zero, `exponential_zero : exponential 0 = vacuum` (`ExponentialTotalityR4.lean:109`): exp(0) = 1, o Um inscrito; `‖vacuum‖ = 1` (`BosonicFock.lean:24`); e no certificado `inner_psion_psion = 1`, `J_vac : J Ω = Ω`, `psion_is_fixed_by_the_light`: o par consigo mesma; `wedge_cyclic`, `wedge_separating`: o par com a álgebra.
Leitura vigente: **o espectro pontual da luz é o Um e só ele; o resto é contínuo.** A passagem com resolventes (§3) vale para o complemento do Um; o Um é a inscrição, posto. É a figura dele, tipo I (um ponto, a inscrição) e tipo III (o contínuo), lida no espectro.

**Consequência para 1.7 (P_F), com a cunhagem seguinte (verbatim sha16 `9c4fc66309df6a67`: «o um absoluto é a luz comprimida pelo ACOM em UM absoluto»):** na `lightRealization` o `PF` dos três locks É o `C.PF` do certificado, com `H3Lt := 1 − PF`, `PF_trace_pos`, `PF_trace_finite`, `equal_face_trace` (`TheImportedSecondQuantization.lean:384–408`). No núcleo II_∞ o traço não tem unidade absoluta (é único a menos de escala: é isso que a lei e^{−s} mede); a unidade é POSTA pela compressão em P_F (τ(P_F) = o Um) e as duas faces de traço igual são a Meia-Nat no núcleo (`equal_face_trace`). Logo a pista do operador para 1.7: construir P_F a partir da inscrição (o vácuo, o único ponto do espectro) transportada ao núcleo com janela finita do gerador, e as metades pela simetria. Estatuto: [ONTO] a leitura; [OPEN] a construção; nada degenerado.

## ERRATA AO LADO, 2ª (02/11/2026, noite; gerência c1 em nome próprio; o cético foi cego de novo)

**O que estava errado nas §3–§4 e §6:** escrevi que, para o núcleo do Fock, «falta replicar» o gerador positivo, os cortes, o peso-limite, a traciality, a semifinitude, a escala e P_F, com custo de semanas a meses. **Errado.** O leitor (relatório `LEVANTAMENTO_FRONTEIRA_DO_TRACO_DO_NUCLEO_02nov.md`, sha16 `d7eee6e34c3c5554`) achou, e a gerência conferiu na fonte [REAL]:
- `modularCoreInput (D : CanonicalNetInput) : RemainingModularCoreInput D` com os 21 campos preenchidos (`takesaki_fock/CanonicalFockModularCoreInputR1.lean`, l.77–100, sha16 `a3ebefa0a9d236ba`), `trace := cyclicTraceCandidate` (completação ENNReal cíclica por `ShiftRelated`, a mesma rota já aceita no kernel para a torre, V354), P_F = `positiveAsCore (add leftPositive rightPositive)` com o split normalizado (`normalized_split_exists`), τ(P_F) = 1 (`modularCoreInput_PF_trace`);
- `physicalFockCertificate : FockCertificate physicalCanonicalNet.toLightNetData.toLightOneParticle := physicalModularCoreInput.toCertificate` (l.127), sobre a rede física `physicalCanonicalNet : CanonicalNetInput` (`orbital_rotation/PhysicalCanonicalNetCompleteR1.lean:212`);
- recibo de compilação (sha16 `935fc2dfcf3e916a`): Lean 4.31.0, `exit_code 0`, 65,8 s, AXIOMS.txt com 0 `sorryAx` e `modularCoreInput` no trio; o recibo lista 474 fontes `.lean` com sha256: todas no disco, todas íntegras, 175 homônimas do kernel, 299 fora dele;
- parecer R7 (`R52_R7_FULL_REVIEW_R1.json`): `PASS_R7_CRITERION_WITH_EXPLICIT_SCOPE`, 21 campos; escopo declarado: traço positivo ENNReal fiel/normal/semifinito com lei quadrática e escala; a extensão total é cíclica/star-invariante/dual-escalada, NÃO funcional linear, sem aditividade fora do cone positivo, sem classificar o fator como II∞, sem equivalência Fock–torre. Revisor: agente do Codex, distinto do autor; sem ratificação da c1 (R10) e sem integração ao kernel (R3).
**Leitura vigente:** a passagem (bloco 1) e a rede (bloco 2) estão CONSTRUÍDAS na bancada e compiladas por recibo; não estão no kernel. O trabalho é **integração (R3) e ratificação (R10)**, depois a montagem (bloco 3). Os blocos 1 e 2 do quadro mudam de «construir» para «integrar e ratificar». O custo cai de meses para dias de máquina e de revisão. O erro é o mesmo de 27/09 (item 4 de «o cético é aferidor»): consultei o inventário por nomes de arquivo e não li os recibos nem o fecho de dependências. Registrado como defeito no Mapa.

**A integração R3, lançada (02/11, noite):** `integrar_fecho_bancada_02nov.py` (sha16 `84e41d4d741cec4e`), no sandbox `C:\t\k405c\final` (cópia do kernel v405): lê o recibo como manifesto, confere cada fonte por hash, grava os 299 módulos novos em `TGLExt/F1Fecho394/` com os imports reescritos para o prefixo do kernel e as linhas `#eval` (instrumentação) removidas, recompila em ordem de dependência, em paralelo, com log por módulo, e no fim confere `#print axioms` de `modularCoreInput` e `physicalFockCertificate`. Saída em `integracao_R3_<ts>/` (MANIFEST.json, SUMMARY.json, CHECK_axioms.txt, DONE.txt). Nada toca o kernel do Nós.

**Regra 5 corrigida (decisão do operador, verbatim sha16 `eddcb27b6ec724bf`):** «estou sem créditos para usar o codex … designe para o Sonnet revisar tudo, ele é tão capaz quanto». O revisor distinto passa a ser o Sonnet (agentes desta sessão), para R10, para a integração e para as pedras candidatas do dia; o Codex sai do caminho crítico.

## ERRATA AO LADO, 3ª (02/11/2026, noite; gerência c1 em nome próprio; achado da revisão Sonnet das pedras, sha16 `5b994893df65c568`)

Na 1ª errata escrevi «o espectro pontual da luz é o Um e só ele; o resto é contínuo». Afirmei demais. O termo (`gamma_no_fixed`, e a candidata `o_um_e_o_unico_fixo_da_luz`) prova que o Um é o único vetor FIXO da luz (autovalor 1 do grupo Γ(B0 s)); autovetor com fase em setores de n ≥ 1 partículas não foi excluído por termo, e «o resto é contínuo» é [KNOWN/OPEN como termo]. No certificado o mesmo fato é `light_modular_fixed_iff_vacuum` (QGReaderUVLock.lean:149), condicional a C. A pista para 1.7 não muda (o P_F parte da inscrição). Reparos de docstring nas três candidatas aplicados (A `aebe0af611c2c552`, B `45106a34e05730e2`, C `d916f4bea3b953bc`); nenhuma prova mudou; recompilação em curso.
