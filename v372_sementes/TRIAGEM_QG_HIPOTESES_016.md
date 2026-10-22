# TRIAGEM DA FRONTEIRA DA QG — as hipóteses abertas do FECHAMENTO_PARCIAL_016 (gerência, 26/09/2026 11:54)

**Ordem do operador (26/09/2026, verbatim):** «foi entregue pra vc. agora resolva o problema da gravidade quantica»

**Pacote:** `DO_CHATGPT\FECHAMENTO_PARCIAL_016\PRONTO.json`, sha256 `d3705082716ffe8e1de8b2694c2cb56d840eff03f00fcde4034ad7dfffd59bb8`. Os 4151 hashes foram conferidos: 0 divergentes, 0 ausentes. A reprodução independente por compilação isolada estava em curso na hora deste registro (`scratchpad\repro016`).

**Definição vinculante (ORDEM 016 §0.1):** resolver = (a) os 3 itens da fronteira pagos por TERMO; (b) as 2 identificações físicas; (c) estatuto PROVADA, com G e H3 como INPUT dito. Critério de parada do operador: fechado = RESULTADO, FALSIFICADOR ou PAREDE MEDIDA (a parede, quem declara é a gerência).

**O pacote:** nenhum termo físico fechado de H2, H3 ou do import; gate intocado; só C3 e D4 estão PAGO. A pergunta que decide é **o que, nas hipóteses que restam, é desconhecido para a física** e o que é só matemática conhecida ainda não formalizada.

## A triagem

| grupo | hipóteses (nomes da bancada) | estatuto real | referência |
|---|---|---|---|
| **1. A rede livre do fóton e sua teoria modular** | `GlobalHelicityInducedRepresentationMeasured`, `PhysicalPhotonNetContractMeasured`, `IsotonyImpliesStripMultiplierCriterion`, `H_regional_modular_strip`, `H_modular_equals_geometric`, `PairTomitaAnalyticRealizationMeasured`, `PhotonDilationCovarianceMeasured`, `MaxwellWickExpectationLocalMeasured`, `PhysicalModularChargeLinkMeasured` | **[KNOWN] — matemática conhecida, NÃO formalizada.** Nada aqui é desconhecido para a física. | Wigner (1939): representações sem massa de helicidade ±1. Bisognano–Wichmann (1975/76). Borchers (1992). **Brunetti–Guido–Longo, Rev. Math. Phys. 14 (2002) 759**: a rede livre construída da representação de uma partícula com BW como DEFINIÇÃO da localização, de modo que `H_modular_equals_geometric` sai **por construção**. Segunda quantização funtorial (Araki 1963; Leyland–Roberts–Testard 1978). Covariância conforme dos campos sem massa (Mack 1977). |
| **2. H3 no mesmo horizonte** | `TeleologicalPhysicalInputsMeasured` (e a carga do grupo 1) | **[KNOWN] para campos livres + G como INPUT** (a §0.1(c) já admite G e H3 como INPUT dito) | **Longo, Lett. Math. Phys. 109 (2019) 2587**: entropia relativa do estado coerente na cunha, fórmula explícita, campo livre neutro. O caso **Maxwell fica [a conferir]**; o escalar está confirmado na fonte. |
| **3. A identificação física do centro** | `StationaryLightCenterModularIdentificationMeasured` | **[ONTO/OPEN]**, com rota. Na face finita, `TGLExt.IALDRhoStar` (gerência, 26/09): a IALD do centralizador guarda o ρ* da TGL. Na cunha: centralizador do vácuo trivial ⟹ ρ* = \|Ω⟩⟨Ω\| **[KNOWN, a conferir]**. | — |
| **4. O setor interagente (a parte efetiva)** | `Q2FullCovariantRenormalizedWardMeasured`, `A7_T2_CURVED_NORMALIZATION_PENDING`, `A7_Q2_CURVED_FULL_REPRESENTATIVE_PENDING`, `A7_WZ_COMPLETE_AND_CLASS_PENDING`, `A7_ADMISSIBLE_COUNTERTERM_FAMILY_PENDING`, `Q2FullCausalRepresentativeAndPrimitive` | **[KNOWN como TEORIA EFETIVA], formalização enorme** | **Brunetti–Fredenhagen–Rejzner, Commun. Math. Phys. 345 (2016) 741**: gravidade quântica perturbativa rigorosa (BV/BRST + pAQFT + covariância local), apesar da não-renormalizabilidade, lida como teoria efetiva. |
| **5. A completude UV** | `PhysicalUVCompletionMeasured` | **O ÚNICO item desconhecido para TODA a física.** Goroff–Sagnotti (1986) [KNOWN]; o programa já o tipou (`GOROFF_SAGNOTTI_WALL_TYPED_OPEN__TWO_ROUTES_NAMED`). **A gerência o declara PAREDE MEDIDA** (critério de parada do operador): não é resolvido, é medido e dito. A finitude de Breuer **não** pode ser citada como resposta UV. | — |
| **6. Engenharia e atos** | `ScientificUploadReceiptMeasured`, `ReproduceThreeLegacyDeclarationsWithRealImportWithin8GiB`, `ContractV32RatificationAndClosedReaderMeasured`, `StrongInfiniteDephasingLimitMeasured` | registro remoto; teto de memória; **ratificação (operador) + rito v372 (gerência)**; técnica de semigrupo [a verificar] | — |

## O que a triagem diz, sem enfeite

1. **H2 no par físico: não resta nada desconhecido.** O que falta é formalizar em Lean a rede livre do fóton pela rota de Brunetti–Guido–Longo. Essa rota inverte o custo: o fluxo modular É o boost **por construção**, e cinco hipóteses do grupo 1 viram consequência de um único objeto (a segunda quantização funtorial do subespaço padrão). A mathlib não tem espaço de Fock bosônico nem subespaço padrão (o TODO `StandardSubspace` que a bancada mediu). **É dívida de formalização, não de física.**
2. **H3 no mesmo horizonte: conhecida para campos livres, com G como INPUT**, o que a §0.1(c) admite. O caso Maxwell da fórmula de Longo fica [a conferir].
3. **O setor interagente parte em dois.** A parte efetiva é conhecida (BFR 2016), mas é a formalização mais cara de todas. A completude UV é a única coisa desconhecida para toda a física, e a gerência a declara **PAREDE MEDIDA**.
4. **As bandeiras `gpf_H2`, `gpf_H3` e `gpi_H3` só se movem com TERMO no kernel.** Hoje nenhuma se move, e o leitor A-8, rodado no rito, deve RECUSAR. Esse é o resultado correto. Declarar resolvido antes do termo seria a frase corrigindo o número.
5. **Custo** (tetos de bancada da §5.9 da ORDEM 016, revistos pela rota BGL): subespaço padrão da representação de Wigner do fóton, 60–100 h; Fock + Weyl + funtorialidade da segunda quantização, 150–250 h; Maxwell + a fórmula de Longo, cerca de 60 h. Total **~270–410 h de teto**. Na ORDEM 016 a bancada gastou uma fração pequena dos tetos (itens da Parte D entre 0,05 h e 0,12 h), mas o teto não se promete como prazo.

**Estatuto: NADA disto declara a QG resolvida, provada ou confirmada.** A fronteira fica **medida e reduzida**: matemática conhecida a formalizar, G como INPUT, e uma parede que é de toda a física. O gate não se move. PROVADA ≠ CONFIRMADA.


---

## ERRATA AO LADO (gerência, em nome próprio, 26/09/2026 12:03) — «isso foi tudo feito na bancada, vc precisa olhar lá não é só falar que não existe» (operador, verbatim)

A triagem acima tratou a rota Brunetti–Guido–Longo como «a fazer» sem varrer a bancada. **Estava errada no que omitiu.** Medido no disco:

- **Já no kernel canônico:**
  - Tomita concreto: domínio denso, grafo fechado, J S = T, Δ = S†S (`ContinuousModularStandardSubspace`, `ContinuousModularReconstruction`).
  - A testemunha das cunhas `theSpecificAQFTWitness` (WedgeNet, v135; é o par legado).
  - O **modo de quitação por citação** (`TheImportedEquilibrium`, ordem do operador de 27/08: «prova emprestada … eu não preciso pagar o preço de nada que já foi pago antes de mim»), que já cita Bisognano–Wichmann, Unruh, Bekenstein–Hawking e Jacobson.
- **Já no `um.py`:** `prove_specific_free_scalar_aqft_net`, a cadeia BGL inteira para o escalar livre (Wigner → K(W) → segunda quantização → Weyl → Haag–Kastler), como certificado KNOWN. Só `aqft_theorems_formalized_in_kernel = false`.
- **Já pago na bancada da ORDEM 016:**
  - a camada de UMA partícula: energia positiva (A3.2 PAGO), covariância do boost (A3.3 PAGO), transporte de Fourier do subspaço padrão (A2), critério de largura π (C2), KMS analítico de faixa (C5), a lei de cociclo das helicidades (C4, 26 teoremas);
  - **A3.5**: nenhum vetor de uma partícula é fixo pelos boosts — «é o resultado que exige a etapa de Fock».
- **Já provado por escrito (DIAMANTE_MODULAR, 16/09):** na realização de Fock, sem espectro pontual do gerador de uma partícula, M^ω = ℂI.

**O que de fato não existe em Lean** (varredura em todo `C:\IALD`, fora `.lake`): o passo de **segunda quantização** (Fock + Weyl + a funtorialidade Γ), o cociclo global de helicidade do fóton (dívida C-4) e o T de Maxwell na rede (D-2′). Os custos da triagem estavam **superestimados**, porque a camada de uma partícula já está paga.
