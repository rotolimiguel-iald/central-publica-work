[REAL — 3 teoremas e 0 definições verificados no delta por reprodução isolada autoral e revisão independente. A1(b): traço concreto ainda OPEN.]

# ENTREGA 011 / A1 — Os cortes identificam o limite da inscrição GNS no ideal completo

2026-09-14T20:41:59.639388-03:00

A identidade dos cortes é estendida de finiteDualLeftIdeal para todo nν. Todos os cortes naturais identificam a órbita a.e. e recuperam a pertinência ao ideal. Se A_i são uniformemente limitados, convergem fortemente a A, e Λν(A_i) converge em norma a v, então A pertence a nν e Λν(A)=v. O filtro NeBot é explícito. São duas convergências distintas; a segunda não é inferida da primeira.

A família aproximante do resolvente, a ação direita de seus cortes e a tracialidade continuam posteriores. Não há novos Hilbert, GNS, estado ou traço. O rótulo auxiliar antigo INVERSE_CUTOFF no validador não seleciona a evidência: relatório e nomes dos três teoremas foram conferidos. A1(b) completo aberto; gate intacto.

## Critérios

| Critério | Resultado |
|---|---|
| Ficha anterior e consumidor nomeado | PAGO; fichas integrais anexas, fornecedores pinados. |
| Mesmos espaços e fornecedores | PAGO no alcance dos tipos abaixo; fontes antigas preservadas. |
| Lake isolado e tipos completos | PAGO; autor e revisor rc0, sem herança de objetos DEV. |
| Axiomas | PAGO; somente propext, Classical.choice e Quot.sound, ou subconjuntos. |
| Adulteração | PAGO; controles autorais recusados por TypeMismatch; alcance e eventual leitura do revisor discriminados em seu parecer. |
| Revisão distinta da autoria | PAGO; nenhuma pendência P0/P1/P2 no delta. |
| Habitante do contrato do traço | NÃO PAGO por esta entrega. |
| Incorporação ao um.py / mudança de gate | NÃO EXECUTADA; escopo da gerência. |

## Reprodução

Autor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\gns_closedness_attempts\20260914_203153_377757\run.json`. Comando registrado: `['C:\\Users\\rotol\\.elan\\toolchains\\leanprover--lean4---v4.31.0\\bin\\lake.exe', 'build', 'TGLExt.AuditA1GNSClosedness']`. Fonte e objeto autorais abaixo. Reutilização somente de objetos próprios previamente produzidos na raiz isolada; os pacotes externos vêm do cache explicitado no relatório. Não é nova compilação integral da biblioteca.

Revisor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_fechamento_gns\independent_20260914_203300_093571\run.json`. `652` objetos próprios anteriores; `5` fornecedores antigos recompilados adicionalmente. Zero objetos do autor/DEV herdados; `0` avisos de alvos/auditor. Avisos de fornecedores e diferenças binárias estão preservados em compilation.json. Comparação indisponível não significa igualdade.

As tentativas de desenvolvimento que falharam permanecem em disco. Só o fonte final, as reproduções rc0 e as auditorias aceitas entram nesta conclusão. Controle negativo de uma aplicação adulterada não é um teorema geral de inexistência.

## Fontes e objetos autorais

| Módulo | SHA256 fonte | SHA256 objeto |
|---|---|---|
| `V351ScalarGNSClosedness` | `13a1e9e22229c905922b94bc56c6fedc24dd80ea5072544934ffad2fa33e8bc8` | `be2da58e27670921dc50a1edf8c79f7b9ca94ea38c282d56fd03dd9f1cb8c335` |

## Tipos completos e axiomas

```lean
TGLV350.Regular.scalarGNSCutMap_weight_embedding (P : TGLExt.SiteProfile) (r : ℝ)
  (A : ↥(TGLV350.Regular.scalarWeightLeftIdeal P)) :
  Eq.{1} ((TGLV350.Regular.scalarGNSCutMap P r) ((TGLV350.Regular.scalarWeightGNSEmbedding P) A))
    ((TGLV350.Regular.dualOrbitRepresentation ↑↑A) (TGLV350.Regular.scalarCutVacuum P r))
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.scalarWeightGNSEmbedding_of_cut_actions (P : TGLExt.SiteProfile)
  (A : ↥(VonNeumannAlgebra.toStarSubalgebra.{0} (TGLV350.Regular.regularCoreAlgebra P)))
  (v : ↥(TGLV350.Regular.ScalarGNSHilbert P))
  (hcut :
    ∀ (n : ℕ),
      Eq.{1} ((TGLV350.Regular.scalarGNSCutMap P ↑n) v)
        ((TGLV350.Regular.dualOrbitRepresentation ↑A) (TGLV350.Regular.scalarCutVacuum P ↑n))) :
  ∃ (hA : Membership.mem.{0, 0} (TGLV350.Regular.scalarWeightLeftIdeal P) A),
    Eq.{1} ((TGLV350.Regular.scalarWeightGNSEmbedding P) (Subtype.mk.{1} A hA)) v
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.scalarWeightGNSEmbedding_closed_of_bounded_strong.{u_1} (P : TGLExt.SiteProfile) {ι : Type u_1}
  {l : Filter.{u_1} ι} [Filter.NeBot.{u_1} l] (T : ι → ↥(TGLV350.Regular.scalarWeightLeftIdeal P))
  (A : ↥(VonNeumannAlgebra.toStarSubalgebra.{0} (TGLV350.Regular.regularCoreAlgebra P)))
  (v : ↥(TGLV350.Regular.ScalarGNSHilbert P)) (C : ℝ) (hbound : ∀ (i : ι), LE.le.{0} (norm.{0} ↑↑(T i)) C)
  (hstrong :
    ∀ (x : ↥(TGLV350.Regular.RegularHilbert (TGLExt.TowerHilbert P))),
      Filter.Tendsto.{u_1, 0} (fun i => ↑↑(T i) x) l (nhds.{0} (↑A x)))
  (hgns : Filter.Tendsto.{u_1, 0} (fun i => (TGLV350.Regular.scalarWeightGNSEmbedding P) (T i)) l (nhds.{0} v)) :
  ∃ (hA : Membership.mem.{0, 0} (TGLV350.Regular.scalarWeightLeftIdeal P) A),
    Eq.{1} ((TGLV350.Regular.scalarWeightGNSEmbedding P) (Subtype.mk.{1} A hA)) v
```

Axiomas: propext, Classical.choice, Quot.sound.

## Custódia e limites

- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\AUDITORIA_FECHAMENTO_GNS_A1B.json` — SHA256 `3738c2bfb12e40e1fb58a328da1e88cce1bd3796a2d2689686ccbdeb98f76fdf`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_fechamento_gns\REVIEW_A1_GNS_CLOSEDNESS_FINAL.json` — SHA256 `accdeae4b0238b5e8c16d7682dbe7bf32f545c9591234d32a6946e253f30f2e7`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_fechamento_gns\compilation.json` — SHA256 `c2467b1050a3daf7be793feef2fde41c658133810d207d0649c773e3703059d6`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\ACEITE_DELTA_GNS_CLOSEDNESS.json` — SHA256 `d7b85d1b95afc26543b97b7897cdea00ec1b1429e749c159982f9d83577abe18`.

O manifesto e o recibo próprios ligam esta entrega aos arquivos efetivamente lidos. Nenhum monólito canônico foi importado ou executado; nenhum dado experimental, D1, sigma, Atlas ou diário canônico foi alterado.

## Revisão independente integral

# Revisão independente — fechamento da inscrição GNS do peso

2026-09-14T20:36:04.666344-03:00

**A1_GNS_CLOSEDNESS_REVIEW_ACCEPTED__RIGHT_ACTION_TRACE_OPEN**

[REAL] Sem P0, P1 ou P2 no delta delimitado. 3 declarações (3 teoremas, 0 definições), relidas integralmente e reproduzidas pelo Lake próprio; #check com universos e #print axioms separados, somente propext/Classical.choice/Quot.sound.

[REAL] Delta delimitado de três teoremas, zero definições. Fonte e ficha MD/JSON foram lidas integralmente. Os objetos são scalarWeightLeftIdeal, scalarWeightGNSEmbedding e ScalarGNSHilbert já existentes; o resultado não substitui o ideal completo por finiteDualLeftIdeal nem cria outro GNS.

[REAL] scalarGNSCutMap_weight_embedding estende de fato a identidade dos cortes a TODO a∈nν. A prova mantém scalarCutVacuum com sqrt(dualHaarFactor), o mesmo regularVacuum e dualOrbitRepresentation. Usa eventos a.e. finitos para cada corte e linearidade complexa; não normaliza artificialmente um vetor de corte nem o declara separante.

[REAL] scalarWeightGNSEmbedding_of_cut_actions usa somente os índices n naturais. A união de Ioc(−n,n) cobre ℝ; ae_all_iff é aplicado à família contável, sem uniformização sobre todos os vetores ou um filtro não enumerável. Da igualdade a.e. com v∈L² e sqrt(dualHaarFactor)>0, recupera MemLp da órbita pela escala inversa. hasFiniteScalarSquare_iff_memLp dá a pertinência real de A ao ideal completo, e scalarWeightOrbit_ae identifica a inscrição no mesmo H_I.

[REAL] scalarWeightGNSEmbedding_closed_of_bounded_strong tem índice de universo arbitrário, filtro l e [NeBot l] explícito. A cota uniforme é de norma de operadores; hstrong e hgns são premissas separadas. A continuidade de cada scalarGNSCutMap e dualOrbit_tendsto_of_uniformly_bounded dão dois limites do MESMO vetor cortado; tendsto_nhds_unique usa a não trivialidade. Não se deduz convergência GNS de forte isolada, nem se requer convergência dos adjuntos para este teorema.

[REAL] Cinco fornecedores antigos estavam ausentes em v: V350ScalarGNSCutMaps, V350DualCutLinearMap, V350ScalarBoundedCuts, V350ScalarGNSCutNorm e V350ScalarCutVacuum. Foram copiados em bytes de OLD/kernel após comparação com K e recompilados pelo Lake próprio. Os nomes/pins individuais estão em snapshot e compilation. O build de fornecedores do autor não foi importado nem contado como reprodução própria.

[REAL] Histórico medido: 20260914_202656_437844: rc1; 20260914_202921_830010: rc1; 20260914_203030_719820: rc0. O primeiro rc1 é ausência do objeto ScalarCutVacuum, não refutação matemática; o segundo contém erro de coerção real/complexa e uso inválido de MemLp.congr, com sorryAx transitivo, e está excluído. Só a fonte final rc0 sem avisos é aceita. [history_read.json](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_fechamento_gns\history_read.json>), SHA256 `4cb65d43723733b46c5245e873d8523a891e2d96c784e0f025b59c848a3d0216`.

[REAL] Auditoria autoral e negativo BadGNSCutNormalization relidos com hashes, sem execução pela revisão: acrescentar fator 2 à identidade do corte produz Type mismatch, não falha de importação ou ambiente. Um rótulo auxiliar do script validate_gns_closedness menciona INVERSE_CUTOFF; não foi usado para identificar/aceitar este delta. A evidência selecionada é AUDITORIA_FECHAMENTO_GNS_A1B com os três nomes exatos e streams correspondentes; essa observação de rótulo não altera o resultado formal.

[REAL] A ficha antecede o código e aponta consumidor específico: extensão da ação direita para os cortes na perturbação do peso. O fechamento remove uma obrigação real dessa rota, mas não fornece por si uma família de aproximantes nem a segunda convergência exigida.

[REAL] Execução própria rc0 em 124.13 s. 652 objetos próprios anteriores preservados; 5 fornecedores antigos adicionais precisaram de reprodução de fonte, além dos módulos deste delta e auditor. Zero objetos autorais/de DEV herdados. Os pacotes externos são cache copiado e pinado da revisão própria anterior, sem recompilação nesta chamada; essa herança não é uma nova auditoria integral da biblioteca. 0 avisos de alvo/auditor; 178 mensagens de fornecedores registradas no JSON (inclui mensagens de objetos anteriores). O aviso de cache aesop com alterações locais, quando presente, permanece no stderr.

Pins lidos dos fontes e objetos próprios:

| Módulo | SHA256 fonte | SHA256 .olean próprio | Igual ao cold build autoral disponível |
|---|---|---|---|
| TGLExt.V351ScalarGNSClosedness | `13a1e9e22229c905922b94bc56c6fedc24dd80ea5072544934ffad2fa33e8bc8` | `be2da58e27670921dc50a1edf8c79f7b9ca94ea38c282d56fd03dd9f1cb8c335` | True |

Comparações de bytes não são forçadas; objeto autoral ausente é comparação indisponível, não falha formal.

Controles: AUTHOR_CONTROLS_READ_AND_HASH_VERIFIED__TYPE_MISMATCH_NOT_ENVIRONMENT. A execução ou leitura correspondente está discriminada em compilation.json; nenhum controle autoral foi reexecutado por esta revisão.

[OPEN / limites] Ação direita de elementos além dos fornecedores já pagos, geração forte limitada e passagem a sqrt(Bε) são obrigações posteriores. Nenhuma monotonicidade de sanduíches ou de avaliações perturbadas, tracialidade, novo predual ou pagamento completo de A1(b). Sem cobrança de minorantes positivos para ν, sem mudança de J, gate ou memória. Consulta posterior por grafos/projeções é separada, sem alvos Lean adicionais.

Artefatos próprios:

- [run](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_fechamento_gns\independent_20260914_203300_093571\run.json>) — SHA256 `15b46bb3014f9fa0b223c8167d2c7607b2280ce39cc04046ee0d1072acb66926`.
- [compilation](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_fechamento_gns\compilation.json>) — SHA256 `c2467b1050a3daf7be793feef2fde41c658133810d207d0649c773e3703059d6`.
- [tipos/axiomas](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_fechamento_gns\independent_20260914_203300_093571\type_axiom_audit.json>) — SHA256 `3e498a672b2bf74a7e75b14a73644613058e7c1b698d8841c9d7ba5559c3f1e2`.


## Ficha/adendo integral: REAPROVEITAMENTO_A1B_FECHAMENTO_GNS

[OPEN — ficha anterior ao fechamento do mapa GNS do peso]

# A1(b): fechamento da inscrição GNS do peso sob duas convergências

2026-09-14T20:25:13.984148-03:00

Closedness of the EXISTING full weight GNS embedding: for any nontrivial filter l, A_i in n_nu uniformly bounded in operator norm, A_i converging strongly to A in the same core, and Lambda_nu(A_i) converging in GNS norm to v, prove A in n_nu and Lambda_nu(A)=v. Both convergences are hypotheses; strong convergence alone does not imply GNS convergence. Reuse existing finite cut maps and the dualOrbit factorization for arbitrary nets, and hasFiniteScalarSquare_iff_memLp. Consumer: extension of the already constructed right action of regular unitaries to bounded centralizer elements sqrt(B_epsilon) in pedersen_takesaki_inverse_generator_trace, LACUNAS_A1 item4. No new Hilbert space, state, trace or abstract predual.

O ideal, os cortes e a representação são os existentes. O lema só fecha o grafo da inscrição; não produz convergência GNS a partir da convergência forte. A entrada consumidora é a ação direita dos cortes inversos na fórmula de τ do item4 de LACUNAS_A1.md. As propriedades do traço seguem pendentes.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarHomogeneousRightOrbit.lean:14` — `dea570f1f1d43c026874d322b44fbf7e9c30856c2fac17e252319d799085c730`

```lean
theorem hasFiniteScalarSquare_iff_memLp (P : SiteProfile)
    (A : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P)) :
    HasFiniteScalarSquare P A ↔ MemLp (fun s : ℝ => dualAmbient s A (regularVacuum P)) 2
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarWeightCompletion.lean:90` — `b8a87c9b03f233e8e0a04a92aaa7c6cd4499fb8421746902f2b0b90feb883d7c`

```lean
def scalarWeightGNSEmbedding (P : SiteProfile) : scalarWeightLeftIdeal P →ₗ[ℂ] ScalarGNSHilbert P
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarWeightOrbit.lean:57` — `9d170b4b28f7ad8da5cce31e9d2e1b7b7216ccef6519a626e42be39ef0b27255`

```lean
theorem scalarWeightOrbit_ae (P : SiteProfile) (A : scalarWeightLeftIdeal P) :
    (scalarWeightOrbit P A : ℝ → RegularHilbert (TowerHilbert P)) =ᵐ[volume]
      fun s => (Real.sqrt dualHaarFactor : ℝ) • dualAmbient s A.val.val (regularVacuum P)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarGNSCutMaps.lean:50` — `2daee56a03944695f137e54fa8a0f76883cbd453d707aa626e5d201700286b5e`

```lean
def scalarGNSCutMap (P : SiteProfile) (R : ℝ) :
    ScalarGNSHilbert P →L[ℂ] RegularHilbert (RegularHilbert (TowerHilbert P))
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarCutVacuum.lean:20` — `524ca91fbe926c9cca9d556da92933d7b1ba037cf57dfd572250a7f12770c24e`

```lean
theorem scalarCutVacuum_ae (P : SiteProfile) (R : ℝ) :
    (scalarCutVacuum P R : ℝ → RegularHilbert (TowerHilbert P)) =ᵐ[volume]
      (Set.Ioc (-R) R).indicator (fun _ => (Real.sqrt dualHaarFactor : ℝ) • regularVacuum P)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarCutVacuum.lean:35` — `524ca91fbe926c9cca9d556da92933d7b1ba037cf57dfd572250a7f12770c24e`

```lean
theorem scalarGNSCutMap_embedding_eq_action (P : SiteProfile) (R : ℝ)
    (A : finiteDualLeftIdeal P) :
    scalarGNSCutMap P R (scalarGNSEmbedding P A) =
      dualOrbitRepresentation A.val.val (scalarCutVacuum P R)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350DualOrbitStrongLimits.lean:45` — `a1c944185a25d4fe2c57491cae8f063845c2ae0d9c64d536ddfb7e4e797b15a3`

```lean
theorem dualOrbit_tendsto_of_uniformly_bounded {ι : Type*} {l : Filter ι}
    (T : ι → (RegularHilbert H →L[ℂ] RegularHilbert H))
    (S : RegularHilbert H →L[ℂ] RegularHilbert H) (C : ℝ)
    (hbound : ∀ i, ‖T i‖ ≤ C)
    (hT : ∀ v, Tendsto (fun i => T i v) l (𝓝 (S v)))
    (f : RegularHilbert (RegularHilbert H)) :
    Tendsto (fun i => dualOrbitRepresentation (T i) f) l
      (𝓝 (dualOrbitRepresentation S f))
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarRegularRightGNS.lean:98` — `92ac2b64b81b6389a2900ddd63dceabcc2f150a05bab59ce8e903352a7fa12fa`

```lean
theorem regularRightGNS_intertwines (P : SiteProfile) (t : ℝ) (A : scalarWeightLeftIdeal P) :
    regularRightGNS P t (scalarWeightGNSEmbedding P A) =
      scalarWeightGNSEmbedding P (scalarRegularRightProduct P t A)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarRegularRightPolar.lean:105` — `cab5601b5e0a1e1ef950638a2025c814488c3f5baa083c14d85028a1ca9d95c9`

```lean
theorem scalarTomitaPolar_conjugate_regular_right (P : SiteProfile) (t : ℝ) :
    antiunitaryConjugate (scalarTomitaPolarFactor P) (regularRightGNS P t) =
      scalarGNSRepresentation P (star (regularRightCoreElement P t))
```

Seis modalidades e outras bancadas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_gns_closedness\20260914_202444_467404\searches.json. Ausência nominal nos recortes não é ausência universal.
