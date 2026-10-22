[REAL — 7 teoremas e 1 definições verificados no delta por reprodução isolada autoral e revisão independente. A1(b): traço concreto ainda OPEN.]

# ENTREGA 011 / A1 — Os cortes do inverso pertencem ao mesmo core e invertem o mesmo grafo

2026-09-14T20:24:24.128186-03:00

Bε=ε^-1 θ_(log ε)(R), para ε>0. Construção no mesmo core, positividade, cota ε^-1 I, B1=R e equivalência (x,y)∈graph(h) ↔ Bε(y+εx)=x. A escala dual é θ_s Bε=e^s B_(εe^s), com o mesmo h afiliado e mesmo domínio. ε é regulador; não é parâmetro físico nem uma inversa limitada de h.

O peso perturbado, sua monotonicidade e tracialidade permanecem abertos. A1(b) não está completo. Não se infere ordem de sanduíches da ordem de operadores positivos; nenhum gate é alterado.

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

Autor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\inverse_cutoff_attempts\20260914_201528_636569\run.json`. Comando registrado: `['C:\\Users\\rotol\\.elan\\toolchains\\leanprover--lean4---v4.31.0\\bin\\lake.exe', 'build', 'TGLExt.AuditA1InverseCutoff']`. Fonte e objeto autorais abaixo. Reutilização somente de objetos próprios previamente produzidos na raiz isolada; os pacotes externos vêm do cache explicitado no relatório. Não é nova compilação integral da biblioteca.

Revisor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_cortes_inverso\independent_20260914_201637_202511\run.json`. `650` objetos próprios anteriores; `0` fornecedores antigos recompilados adicionalmente. Zero objetos do autor/DEV herdados; `0` avisos de alvos/auditor. Avisos de fornecedores e diferenças binárias estão preservados em compilation.json. Comparação indisponível não significa igualdade.

As tentativas de desenvolvimento que falharam permanecem em disco. Só o fonte final, as reproduções rc0 e as auditorias aceitas entram nesta conclusão. Controle negativo de uma aplicação adulterada não é um teorema geral de inexistência.

## Fontes e objetos autorais

| Módulo | SHA256 fonte | SHA256 objeto |
|---|---|---|
| `V351InverseGeneratorCutoff` | `f615a4a8b80a4bf970c719aa9d44fd2d917eb52f01fa1c925cfcab8151adc227` | `e9301f745f1e598bc57f0f2d5e64c78dc19fdb8713d4981cce1bc3fe872b1e03` |

## Tipos completos e axiomas

```lean
TGLV350.Regular.regularInverseGeneratorCutoff (P : TGLExt.SiteProfile) (ε : ℝ) :
  ContinuousLinearMap.{0, 0, 0, 0} (RingHom.id.{0} ℂ) ↥(TGLV350.Regular.RegularHilbert (TGLExt.TowerHilbert P))
    ↥(TGLV350.Regular.RegularHilbert (TGLExt.TowerHilbert P))
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.regularInverseGeneratorCutoff_mem (P : TGLExt.SiteProfile) (ε : ℝ) :
  Membership.mem.{0, 0} (TGLV350.Regular.regularCoreAlgebra P) (TGLV350.Regular.regularInverseGeneratorCutoff P ε)
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.regularInverseGeneratorCutoff_nonneg (P : TGLExt.SiteProfile) (ε : ℝ) (hε : LT.lt.{0} 0 ε) :
  LE.le.{0} 0 (TGLV350.Regular.regularInverseGeneratorCutoff P ε)
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.regularInverseGeneratorCutoff_le (P : TGLExt.SiteProfile) (ε : ℝ) (hε : LT.lt.{0} 0 ε) :
  LE.le.{0} (TGLV350.Regular.regularInverseGeneratorCutoff P ε) (HSMul.hSMul.{0, 0, 0} (Inv.inv.{0} ↑ε) 1)
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.regularInverseGeneratorCutoff_one (P : TGLExt.SiteProfile) :
  Eq.{1} (TGLV350.Regular.regularInverseGeneratorCutoff P 1) (TGLV350.Regular.regularSpectralResolvent P)
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.regularInverseGeneratorCutoff_graph (P : TGLExt.SiteProfile) (ε : ℝ) (hε : LT.lt.{0} 0 ε)
  (x : ↥(TGLV350.Regular.RegularHilbert (TGLExt.TowerHilbert P))) :
  Membership.mem.{0, 0} (LinearPMap.graph.{0, 0, 0} (TGLV350.Regular.regularPositiveGenerator P))
    (Prod.mk.{0, 0} ((TGLV350.Regular.regularInverseGeneratorCutoff P ε) x)
      (HSub.hSub.{0, 0, 0} x (HSMul.hSMul.{0, 0, 0} (↑ε) ((TGLV350.Regular.regularInverseGeneratorCutoff P ε) x))))
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.regularInverseGeneratorCutoff_dual (P : TGLExt.SiteProfile) (ε : ℝ) (hε : LT.lt.{0} 0 ε) (s : ℝ) :
  Eq.{1} ((TGLV350.Regular.dualAmbient s) (TGLV350.Regular.regularInverseGeneratorCutoff P ε))
    (HSMul.hSMul.{0, 0, 0} (↑(Real.exp s))
      (TGLV350.Regular.regularInverseGeneratorCutoff P (HMul.hMul.{0, 0, 0} ε (Real.exp s))))
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.regularInverseGeneratorCutoff_graph_iff (P : TGLExt.SiteProfile) (ε : ℝ) (hε : LT.lt.{0} 0 ε)
  (x y : ↥(TGLV350.Regular.RegularHilbert (TGLExt.TowerHilbert P))) :
  Membership.mem.{0, 0} (LinearPMap.graph.{0, 0, 0} (TGLV350.Regular.regularPositiveGenerator P)) (Prod.mk.{0, 0} x y) ↔
    Eq.{1} ((TGLV350.Regular.regularInverseGeneratorCutoff P ε) (HAdd.hAdd.{0, 0, 0} y (HSMul.hSMul.{0, 0, 0} (↑ε) x)))
      x
```

Axiomas: propext, Classical.choice, Quot.sound.

## Custódia e limites

- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\AUDITORIA_CORTES_INVERSO_A1B.json` — SHA256 `7eb32c3d7a81c7fdb27ff9d53f43888ebe9f6f3178a94b6e8829590c7548bd50`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_cortes_inverso\REVIEW_A1_INVERSE_CUTOFF_FINAL.json` — SHA256 `7e7273ee544eb35880e8f936abb46c82dc353e7d649aedc6f477c1d3f3bf5d9c`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_cortes_inverso\compilation.json` — SHA256 `262af9f2cd8d1622cf2938757e3eff07500062cf1f0adf3c9167a1d248018f13`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\ACEITE_DELTA_INVERSE_CUTOFF.json` — SHA256 `3aa37e7790c638715da579b782fb386adca9b08d68fa9006e7fb745e44777b81`.

O manifesto e o recibo próprios ligam esta entrega aos arquivos efetivamente lidos. Nenhum monólito canônico foi importado ou executado; nenhum dado experimental, D1, sigma, Atlas ou diário canônico foi alterado.

## Revisão independente integral

# Revisão independente — cortes do inverso do gerador regular

2026-09-14T20:18:35.747142-03:00

**A1_INVERSE_CUTOFF_REVIEW_ACCEPTED__WEIGHT_PERTURBATION_TRACE_OPEN**

[REAL] Sem P0, P1 ou P2 no delta delimitado. 8 declarações (7 teoremas, 1 definições), relidas integralmente e reproduzidas pelo Lake próprio; #check com universos e #print axioms separados, somente propext/Classical.choice/Quot.sound.

[REAL] Escopo único: V351InverseGeneratorCutoff, sete teoremas e uma definição. Fonte, ficha MD/JSON e adendo bilateral MD/JSON lidos integralmente. A definição usa exatamente o R, h e a ação dual já revisados; nenhum novo cálculo funcional ou gerador é introduzido. O consumidor indicado é pedersen_takesaki_inverse_generator_trace em LACUNAS_A1, ainda aberto.

[REAL] regularInverseGeneratorCutoff é uma definição total em ε real; membership em N vale para todo ε. As afirmações de positividade, cota, inversão e escala exigem explicitamente ε>0. Não se interpreta o valor formal em ε=0 ou ε<0 como resolvente positivo. regularInverseGeneratorCutoff_le prova a desigualdade de ordem Bε≤ε⁻¹I; o módulo não acrescenta um teorema separado de norma.

[REAL] Afiliação anterior fornece R∈N, e regularDualAction fornece sua imagem em N. A positividade e a cota usam a ordem usual dos operadores no Hilbert, conjugação unitária e escalar real positivo. Não há CompleteSpace do subtipo N assumido, nem comutação genérica de sanduíches. O controle B₁=R respeita Real.log_one e a ação identidade.

[REAL] A equação (Bεx,x−εBεx)∈graph(h) transporta (Rz,z−Rz) pelo caráter com s=log ε e z=C_(−s)x, depois escala ambas as componentes por ε⁻¹. Real.exp_log recebe a hipótese estrita correta. Isso prova imagem no domínio e (h+ε)Bε=I no mesmo grafo, sem identificar apenas um operador homônimo.

[REAL] A escala θ_sBε=e^s B_(εe^s) usa dualAmbient_add, log(εe^s)=log ε+s e cancelamento do escalar não nulo. O fator e^s e o parâmetro εe^s são consistentes com Ad(C_s)h=e^(−s)h. Nenhuma hipótese de comutação com C_s foi introduzida.

[REAL] O último iff é bilateral para quaisquer x,y no Hilbert: (x,y)∈graph(h) ↔ Bε(y+εx)=x. Na ida, subtraem-se dois pares do mesmo grafo; a positividade aplicada a (u−x,−ε(u−x)) força ε‖u−x‖²≤0 e u=x. A volta substitui na equação do grafo já paga. Não há domínio total de h, inversa limitada de h, gap ou premissa oculta de unicidade.

[REAL] Histórico autoral medido: 20260914_200800_436723: rc1; 20260914_200930_786636: rc1; 20260914_201051_634827: rc0; 20260914_201238_097443: rc1; 20260914_201337_906102: rc1; 20260914_201442_615970: rc0. Somente a fonte final sem avisos é selecionada para reprodução. Qualquer rc1 e seus prints parciais/sorryAx são excluídos. Os DEV rc0 anteriores são histórico, não substituem o Lake independente nem fornecem objetos. [history_read.json](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_cortes_inverso\history_read.json>), SHA256 `28b663e3d83f7108ea551331a1d2054978b5ea8e4ad2c23a2c7438b043ef1813`.

[REAL] O negativo autoral BadInverseCutoffSign foi lido e pinado, não reexecutado: trocar a segunda componente x−εBεx por x+εBεx causa Type mismatch com imports válidos. Não é falha de ambiente. Ficha antecedente e complemento pré-iff são preservados; a busca declarada é delimitada, sem alegação de inexistência global de fornecedores.

[REAL] Execução própria rc0 em 39.26 s. 650 objetos próprios anteriores preservados; 0 fornecedores antigos adicionais precisaram de reprodução de fonte, além dos módulos deste delta e auditor. Zero objetos autorais/de DEV herdados. Os pacotes externos são cache copiado e pinado da revisão própria anterior, sem recompilação nesta chamada; essa herança não é uma nova auditoria integral da biblioteca. 0 avisos de alvo/auditor; 178 mensagens de fornecedores registradas no JSON (inclui mensagens de objetos anteriores). O aviso de cache aesop com alterações locais, quando presente, permanece no stderr.

Pins lidos dos fontes e objetos próprios:

| Módulo | SHA256 fonte | SHA256 .olean próprio | Igual ao cold build autoral disponível |
|---|---|---|---|
| TGLExt.V351InverseGeneratorCutoff | `f615a4a8b80a4bf970c719aa9d44fd2d917eb52f01fa1c925cfcab8151adc227` | `e9301f745f1e598bc57f0f2d5e64c78dc19fdb8713d4981cce1bc3fe872b1e03` | True |

Comparações de bytes não são forçadas; objeto autoral ausente é comparação indisponível, não falha formal.

Controles: AUTHOR_CONTROLS_READ_AND_HASH_VERIFIED__TYPE_MISMATCH_NOT_ENVIRONMENT. A execução ou leitura correspondente está discriminada em compilation.json; nenhum controle autoral foi reexecutado por esta revisão.

[OPEN / limites] Construção e identificação bilateral dos cortes aceitas; nenhuma nova definição abstrata de h⁻¹. Monotonicidade de avaliações perturbadas, ação direita GNS dos cortes, limite do peso perturbado e tracialidade não são afirmados neste delta. A1(b) completo permanece aberto. Não se infere ordem de sanduíches da ordem dos cortes; nenhuma cobrança de minorantes positivos para a semifinitude usual de ν. Nenhum monólito, recorder, memória ou arquivo selado anterior foi alterado; zero promoção de gate.

Artefatos próprios:

- [run](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_cortes_inverso\independent_20260914_201637_202511\run.json>) — SHA256 `9252ca53f705eb15380ae104ec0750e5638caa028f4288cc019c8874585f7611`.
- [compilation](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_cortes_inverso\compilation.json>) — SHA256 `262af9f2cd8d1622cf2938757e3eff07500062cf1f0adf3c9167a1d248018f13`.
- [tipos/axiomas](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_cortes_inverso\independent_20260914_201637_202511\type_axiom_audit.json>) — SHA256 `0464e8e74d94a89ae6123777224a2cdd82427e87a475326efcd9f8375603e2c8`.


## Ficha/adendo integral: REAPROVEITAMENTO_A1B_CORTES_INVERSO

[OPEN — ficha anterior aos cortes do inverso do mesmo gerador]

# A1(b): cortes limitados para a perturbação do peso

2026-09-14T20:05:51.744458-03:00

Construct the actual bounded inverse-generator cutoffs B_epsilon=(h+epsilon)^(-1) for epsilon>0 as epsilon^(-1) theta_(log epsilon)(R), with the SAME R=(1+h)^(-1). Prove core membership, positivity, bound by epsilon^(-1), graph equation h(B_epsilon x)=x-epsilon B_epsilon x, and dual transport theta_s B_epsilon=exp(s) B_(epsilon exp(s)). Consumer: the existing inverse-generator trace formula in LACUNAS_A1 item4. Reuse dual action and graph scaling; no new CFC, generator, base L2 or substitute trace. No assertion of additivity or traciality of a supremum before its monotonicity is established.

R é o resolvente já pago; a escala dual fornece os demais parâmetros sem uma segunda construção espectral. ε é regulador positivo do limite, não parâmetro físico. A entrada consumidora é a fórmula de τ no item4 de LACUNAS_A1.md. As propriedades do traço seguem pendentes.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularPositiveGraph.lean:78` — `d56ea107302802ee76d65a3c32c69be9fe41cddb4901a65486ab7f1bfb345390`

```lean
def regularSpectralResolvent (P : SiteProfile) :
    RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularPositiveGraph.lean:84` — `d56ea107302802ee76d65a3c32c69be9fe41cddb4901a65486ab7f1bfb345390`

```lean
theorem regularSpectralResolvent_nonneg (P : SiteProfile) :
    0 ≤ regularSpectralResolvent P
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularPositiveGraph.lean:89` — `d56ea107302802ee76d65a3c32c69be9fe41cddb4901a65486ab7f1bfb345390`

```lean
theorem regularSpectralResolvent_le_one (P : SiteProfile) :
    regularSpectralResolvent P ≤ 1
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularGeneratorAffiliation.lean:32` — `9e172df5174e9b2b9c5315825a4a487f0fb04b34ba68dcecffd11e8d2684690e`

```lean
theorem regularSpectralResolvent_mem (P : SiteProfile) :
    regularSpectralResolvent P ∈ regularCoreAlgebra P
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularGeneratorDualScaling.lean:102` — `2bd647d5a4c6526780853e16b5ef1ee8f1acddc36570ebdcdc8d74f230e08d50`

```lean
theorem regularPositiveGenerator_dual_graph (P : SiteProfile) (s : ℝ)
    (x y : RegularHilbert (TowerHilbert P))
    (hxy : (x,y) ∈ (regularPositiveGenerator P).graph) :
    (characterMultiplier s x,(Real.exp s : ℂ) • characterMultiplier s y) ∈
      (regularPositiveGenerator P).graph
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350RegularDualAction.lean:30` — `e7c3628d969c0dae2a971c156200acb88f6bf4286a9c648a2ad3da08c468040c`

```lean
theorem dualAmbient_add (s t : ℝ) :
    dualAmbient (H := H) (s+t) = (dualAmbient (H := H) s).trans (dualAmbient (H := H) t)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350RegularDualAction.lean:76` — `e7c3628d969c0dae2a971c156200acb88f6bf4286a9c648a2ad3da08c468040c`

```lean
def regularDualAction (P : SiteProfile) (s : ℝ) :
    (regularCoreAlgebra P).toStarSubalgebra ≃⋆ₐ[ℂ] (regularCoreAlgebra P).toStarSubalgebra
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ResolventGraph.lean:89` — `3ae1a2b72b10989741f27ab8521d6c8a51c0e2fc650896a694605ad53225675b`

```lean
theorem resolvent_graph_resolvent_equation (R : H →L[ℂ] H) (hi : Function.Injective R)
    (u : H) : ∃ x : (resolventGraphOperator R hi).domain,
      (x : H) = R u ∧ (x : H) + resolventGraphOperator R hi x = u
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350L2CharacterMultiplier.lean:124` — `2f7c413ee9ebd5ba93d1222bb596da11972a0b6b4efa1a71a04becb6ff856ca3`

```lean
theorem characterMultiplier_inverse (s : ℝ) (f : RegularHilbert H) :
    characterMultiplier s (characterMultiplier (-s) f) = f
```

Seis modalidades e outras bancadas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_inverse_cutoff\20260914_200529_560958\searches.json. Ausência nominal nos recortes não é ausência universal.


## Ficha/adendo integral: ADENDO_FICHA_INVERSO_BILATERAL

[OPEN — complemento da ficha antes da equivalência bilateral]

2026-09-14T20:12:34.780350-03:00

(x,y) in graph h iff B_epsilon(y+epsilon x)=x. The converse and uniqueness use positivity of the same h. No new definition.

Fornecedor: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularPositiveGraph.lean:138; sha256 d56ea107302802ee76d65a3c32c69be9fe41cddb4901a65486ab7f1bfb345390

```lean
theorem regularPositiveGenerator_positive (P : SiteProfile)
    (x : (regularPositiveGenerator P).domain) :
    0 ≤ (inner ℂ (x : RegularHilbert (TowerHilbert P)) (regularPositiveGenerator P x)).re
```

O alvo inicial já tinha a identificação como inverso. A equivalência explicita a unicidade pela positividade, em vez de deixar essa inferência somente na frase. O antecedente escalar continuous_resolvent_unique vive em outro espaço; não é aplicado por homonímia. Mesmas buscas da ficha original, cujo padrão inclui o nome-base do corte; nenhum novo objeto.
