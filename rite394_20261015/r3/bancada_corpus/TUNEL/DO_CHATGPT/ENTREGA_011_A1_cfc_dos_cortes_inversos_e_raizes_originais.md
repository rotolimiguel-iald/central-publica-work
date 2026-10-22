[REAL — 6 teoremas e 1 definições verificados no delta por reprodução isolada autoral e revisão independente. A1(b): traço concreto ainda OPEN.]

# ENTREGA 011 / A1 — Os mesmos cortes inversos e suas raízes positivas possuem a ação direita

2026-09-14T21:36:19.879509-03:00

Seis teoremas e uma definição públicos, mais dois teoremas auxiliares privados. A extensão racional tem denominador positivo em todo ℂ quando ε>0; no espectro de R é 1/(ε+exp(-κ)). O CFC satisfaz a equação inversa do grafo já provada e é identificado com o Bε existente. A propriedade direita passa por essa igualdade. A raiz é hilbertPositiveSqrt, o empacotamento antigo da CFC.sqrt com instâncias de Hilbert fixadas; uma igualdade genérica por conversores padrão de CFC a liga ao cálculo complexo. Assim Bε e a raiz original pertencem à mesma álgebra direita.

Não foram construídos o limite de avaliações perturbadas, sua ordem, tracialidade ou o traço final. A ação dos cortes é a entrada da próxima etapa. ε>0 é essencial e permanece explícito. Nenhum novo h, J, GNS, inverso ou raiz; gate inalterado.

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

Autor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\cutoff_cfc_attempts\20260914_212415_500106\run.json`. Comando registrado: `['C:\\Users\\rotol\\.elan\\toolchains\\leanprover--lean4---v4.31.0\\bin\\lake.exe', 'build', 'TGLExt.AuditA1CutoffCFC']`. Fonte e objeto autorais abaixo. Reutilização somente de objetos próprios previamente produzidos na raiz isolada; os pacotes externos vêm do cache explicitado no relatório. Não é nova compilação integral da biblioteca.

Revisor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_cfc_cortes\independent_20260914_212646_190543\run.json`. `665` objetos próprios anteriores; `0` fornecedores antigos recompilados adicionalmente. Zero objetos do autor/DEV herdados; `0` avisos de alvos/auditor. Avisos de fornecedores e diferenças binárias estão preservados em compilation.json. Comparação indisponível não significa igualdade.

As tentativas de desenvolvimento que falharam permanecem em disco. Só o fonte final, as reproduções rc0 e as auditorias aceitas entram nesta conclusão. Controle negativo de uma aplicação adulterada não é um teorema geral de inexistência.

## Fontes e objetos autorais

| Módulo | SHA256 fonte | SHA256 objeto |
|---|---|---|
| `V351InverseCutoffCFC` | `cbdf10aea749a552b0f47afb3ef59560ed47d6f46cf7dd8064dc963a092c3490` | `6c4f489bd40b3654a2b1e9e22e4344d58c16c6d831e460d5754d13e5aedba0db` |

## Tipos completos e axiomas

```lean
TGLV350.Regular.inverseCutoffFunction (ε : ℝ) (z : ℂ) : ℂ
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.inverseCutoffFunction_continuous (ε : ℝ) (hε : LT.lt.{0} 0 ε) :
  Continuous.{0, 0} (TGLV350.Regular.inverseCutoffFunction ε)
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.inverseCutoffFunction_sigmoid (ε a : ℝ) (hε : LT.lt.{0} 0 ε) :
  Eq.{1} (TGLV350.Regular.inverseCutoffFunction ε ↑a.sigmoid)
    ↑(Inv.inv.{0} (HAdd.hAdd.{0, 0, 0} ε (Real.exp (Neg.neg.{0} a))))
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.regularInverseGeneratorCutoff_cfc (P : TGLExt.SiteProfile) (ε : ℝ) (hε : LT.lt.{0} 0 ε) :
  Eq.{1} (TGLV350.Regular.regularInverseGeneratorCutoff P ε)
    (cfc.{0, 0} (TGLV350.Regular.inverseCutoffFunction ε) (TGLV350.Regular.regularSpectralResolvent P))
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.regularInverseGeneratorCutoff_right (P : TGLExt.SiteProfile) (ε : ℝ) (hε : LT.lt.{0} 0 ε) :
  Membership.mem.{0, 0} (TGLV350.Regular.scalarPolarRightAlgebra P)
    (Subtype.mk.{1} (TGLV350.Regular.regularInverseGeneratorCutoff P ε) ⋯)
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.scalarRightAction_sqrt (P : TGLExt.SiteProfile)
  (b : ↥(VonNeumannAlgebra.toStarSubalgebra.{0} (TGLV350.Regular.regularCoreAlgebra P)))
  (hb : Membership.mem.{0, 0} (TGLV350.Regular.scalarPolarRightAlgebra P) b) (h0 : LE.le.{0} 0 ↑b) :
  ∃ (h : Membership.mem.{0, 0} (TGLV350.Regular.regularCoreAlgebra P) (TGLV350.Regular.hilbertPositiveSqrt ↑b)),
    Membership.mem.{0, 0} (TGLV350.Regular.scalarPolarRightAlgebra P)
      (Subtype.mk.{1} (TGLV350.Regular.hilbertPositiveSqrt ↑b) h)
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.regularInverseGeneratorCutoff_sqrt_right (P : TGLExt.SiteProfile) (ε : ℝ) (hε : LT.lt.{0} 0 ε) :
  ∃ (h :
    Membership.mem.{0, 0} (TGLV350.Regular.regularCoreAlgebra P)
      (TGLV350.Regular.hilbertPositiveSqrt (TGLV350.Regular.regularInverseGeneratorCutoff P ε))),
    Membership.mem.{0, 0} (TGLV350.Regular.scalarPolarRightAlgebra P)
      (Subtype.mk.{1} (TGLV350.Regular.hilbertPositiveSqrt (TGLV350.Regular.regularInverseGeneratorCutoff P ε)) h)
```

Axiomas: propext, Classical.choice, Quot.sound.

## Custódia e limites

- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\AUDITORIA_CFC_CORTES_A1B.json` — SHA256 `d7e1bf54a12715ea6352c43fc61bda932f1d2c871a5e31c6fd49570afd129b93`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_cfc_cortes\REVIEW_A1_CUTOFF_CFC_FINAL.json` — SHA256 `45ac16aa2052bd9b254f7fd41e2cb9cfe39a4eb74cebb2efaaaa6a28832eb43f`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_cfc_cortes\compilation.json` — SHA256 `8e5fdce08194bf6141f37d7a00ff732aa799e96dbeec6738dcd5d4207499d856`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\ACEITE_DELTA_CUTOFF_CFC.json` — SHA256 `078c51855679ef14314d573a06e9b7f6875e843d15b71e7047a2086c14cbb6bc`.

O manifesto e o recibo próprios ligam esta entrega aos arquivos efetivamente lidos. Nenhum monólito canônico foi importado ou executado; nenhum dado experimental, D1, sigma, Atlas ou diário canônico foi alterado.

## Revisão independente integral

# Revisão independente — CFC dos cortes inversos e raízes originais

2026-09-14T21:30:42.564513-03:00

**A1_CUTOFF_CFC_REVIEW_ACCEPTED__PERTURBED_WEIGHT_TRACE_OPEN**

[REAL] Sem P0, P1 ou P2 no delta delimitado. 7 declarações (6 teoremas, 1 definições), relidas integralmente e reproduzidas pelo Lake próprio; #check com universos e #print axioms separados, somente propext/Classical.choice/Quot.sound.

[REAL] REAPROVEITAMENTO_A1B_CFC_CORTES MD/JSON e ADENDO_FICHA_CFC_RAIZ_HILBERT MD/JSON foram lidos integralmente e seus pins conferidos. A ficha antecede o código. O adendo declara honestamente ser posterior ao DEV e anterior ao aceite: explicita o fornecedor hilbertPositiveSqrt já existente. GeneralExpectationCP é apenas um molde numa álgebra distinta, não um teorema usado como se tivesse o mesmo tipo.

[REAL] São 7 declarações públicas (6 teoremas + 1 definição) com auditor próprio #check/pp.universes e #print axioms. Há separadamente 2 teoremas privados, regularResolvent_cfc_coordinate e hilbertPositiveSqrt_complex_cfc, lidos integralmente e compilados no módulo. Seus axiomas são incluídos transitivamente nos alvos públicos consumidores; não se alegam dois prints privados adicionais. A fonte inteira tem 8 teoremas e 1 definição.

[REAL] inverseCutoffFunction é uma função escalar total; os teoremas de continuidade, identificação e consumo exigem explicitamente ε>0. O denominador max(min(1,ε),1+(ε−1)Re z) é ≥min(1,ε)>0 em todo ℂ. No símbolo sigmoid a, a combinação convexa limita o denominador inferiormente e permite retirar max. A identidade final é ofReal((ε+exp(−a))⁻¹), com o sinal negativo correto e sem hipótese de gap de h.

[REAL] O helper de coordenadas usa o MESMO regularSpectralCoordinates e regularSpectralResolvent. A naturalidade CFC é aplicada com continuidade global e normalidade descarregada por positividade do multiplicador. realScalarMultiplier_cfc_ae continua recebendo o símbolo sigmoid em [0,1]; o corte completo não é indevidamente tratado como contração quando ε<1.

[REAL] Para Y=cfc Fε R e todo x, a prova obtém (Yx,x−εYx) no grafo do MESMO regularPositiveGenerator pela identificação espectral já existente. As igualdades a.e. de subtração/escala são usadas apenas para esse vetor fixo. O iff bilateral de regularInverseGeneratorCutoff, aplicado ao par, produz Bε((x−εYx)+εYx)=Yx e portanto Bεx=Yx. Não se redefine o inverso, não se assume a igualdade desejada, não se exige x∈D(h), e não se trata h como limitado.

[REAL] regularInverseGeneratorCutoff_right consome a ação direita de R que foi reproduzida e aceita no parecer seno11, aplica scalarRightAction_cfc e transporta a pertinência pela igualdade exata de operadores. A ação é na mesma scalarPolarRightAlgebra, cuja propriedade herdada quantifica todo A∈nν e usa o GNS/π/J originais. Não há família aproximante ou pertinência à álgebra direita como premissa residual do teorema concreto.

[REAL] A raiz é exatamente hilbertPositiveSqrt do fornecedor V350AntiunitaryPositiveConjugation:15, cuja definição é CFC.sqrt com instâncias fixadas em Hilbert genérico. O helper genérico usa CFC.sqrt_eq_real_sqrt com h0, cfcₙ_eq_cfc com continuidade de Real.sqrt e sqrt(0)=0, e cfc_real_eq_complex com autoadjunção derivada de h0. Assim não introduz raiz concorrente nem postula positividade. scalarRightAction_sqrt recebe b∈E e b≥0; o corolário concreto descarrega ambos usando o corte existente e ε>0.

[REAL] Histórico em history_read.json: dois DEV rc1 excluídos (cast/equações e ajuste de instâncias), seguidos do final 20260914_212240_170889 rc0 sem avisos, com os mesmos bytes do snapshot próprio e do Lake autoral. Nenhum print de tentativa falha foi aceito. A auditoria autoral e os streams foram relidos: BadCutoffCFCMirror é recusado por Type mismatch ao substituir R por I−R no CFC. É controle autoral relido, não reexecutado nesta revisão.

[REAL] Execução própria rc0 em 39.97 s. 665 objetos próprios anteriores preservados; 0 fornecedores antigos adicionais precisaram de reprodução de fonte, além dos módulos deste delta e auditor. Zero objetos autorais/de DEV herdados. Os pacotes externos são cache copiado e pinado da revisão própria anterior, sem recompilação nesta chamada; essa herança não é uma nova auditoria integral da biblioteca. 0 avisos de alvo/auditor; 178 mensagens de fornecedores registradas no JSON (inclui mensagens de objetos anteriores). O aviso de cache aesop com alterações locais, quando presente, permanece no stderr.

Pins lidos dos fontes e objetos próprios:

| Módulo | SHA256 fonte | SHA256 .olean próprio | Igual ao cold build autoral disponível |
|---|---|---|---|
| TGLExt.V351InverseCutoffCFC | `cbdf10aea749a552b0f47afb3ef59560ed47d6f46cf7dd8064dc963a092c3490` | `6c4f489bd40b3654a2b1e9e22e4344d58c16c6d831e460d5754d13e5aedba0db` | True |

Comparações de bytes não são forçadas; objeto autoral ausente é comparação indisponível, não falha formal.

Controles: AUTHOR_CONTROLS_READ_AND_HASH_VERIFIED__TYPE_MISMATCH_NOT_ENVIRONMENT. A execução ou leitura correspondente está discriminada em compilation.json; nenhum controle autoral foi reexecutado por esta revisão.

[OPEN / limites] Este delta paga Bε=cfc Fε R e a ação direita do corte e da sua raiz positiva ORIGINAL para ε>0. Não constrói peso perturbado, limite/ordem das avaliações, tracialidade ou o traço final. Não há novo h, inverso, J, GNS ou condição do gate; nenhum monólito, memória, fonte autoral ou parecer anterior foi modificado. A1(b) completo permanece aberto.

Artefatos próprios:

- [run](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_cfc_cortes\independent_20260914_212646_190543\run.json>) — SHA256 `c8cd3b958b79bbc2df94c212c67e904f42634992363a5979492172e62f08843b`.
- [compilation](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_cfc_cortes\compilation.json>) — SHA256 `8e5fdce08194bf6141f37d7a00ff732aa799e96dbeec6738dcd5d4207499d856`.
- [tipos/axiomas](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_cfc_cortes\independent_20260914_212646_190543\type_axiom_audit.json>) — SHA256 `8f3e6391f4cdc802288073fd985e55300bd0f7bfaad10eb3edd7a5643e1fd846`.


## Ficha/adendo integral: REAPROVEITAMENTO_A1B_CFC_CORTES

[OPEN — ficha anterior à identificação CFC dos cortes existentes]

# A1(b): o mesmo Bε, sua raiz positiva e a ação direita

2026-09-14T21:18:11.581799-03:00

For epsilon>0 identify the EXISTING regularInverseGeneratorCutoff P epsilon with cfc F_epsilon (regularSpectralResolvent P), F_epsilon(z)=ofReal(z.re / max(min(1,epsilon),1+(epsilon-1)*z.re)). Prove global continuity from the positive clamped denominator and equality to 1/(epsilon+exp(-kappa)) at z=sigmoid(kappa). Use original graph_iff and inverse-cutoff graph_iff to identify candidate Y through (Yx,x-epsilonYx) in the SAME graph. This avoids a new inverse of I+(epsilon-1)R or a new shifted scalar multiplier. Then consume the already proved P(R), cfc membership and standard CFC.sqrt bridges to obtain the SAME CFC.sqrt B_epsilon right action on ALL n_nu. Consumer: norm identity for the bounded positive cut perturbations of the SAME scalar weight. Do not claim their limit, monotonicity or traciality in this target.

ADAPTAR: o inverso regular, seu grafo e P(R) já estão produzidos. A ponte é identidade escalar/CFC com a equação inversa existente, sem novo h, J ou GNS. factor_positive_sqrt_mem é molde somente: seu tipo é o fator da torre, não a álgebra da ação direita. Serão usados os conversores CFC existentes. Os aproximantes têm auditoria autoral rc0 e revisão pendente neste instante.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseGeneratorCutoff.lean:13` — `f615a4a8b80a4bf970c719aa9d44fd2d917eb52f01fa1c925cfcab8151adc227`

```lean
def regularInverseGeneratorCutoff (P : SiteProfile) (ε : ℝ) :
    RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseGeneratorCutoff.lean:99` — `f615a4a8b80a4bf970c719aa9d44fd2d917eb52f01fa1c925cfcab8151adc227`

```lean
theorem regularInverseGeneratorCutoff_graph_iff (P : SiteProfile) (ε : ℝ) (hε : 0 < ε)
    (x y : RegularHilbert (TowerHilbert P)) :
    (x,y) ∈ (regularPositiveGenerator P).graph ↔
      regularInverseGeneratorCutoff P ε (y+(ε : ℂ) • x) = x
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularSpectralGraph.lean:40` — `2a859d88def186591e98f2a0594bc95ae0a9c6eb74c17ea1124ce5844be1b642`

```lean
theorem regularPositiveGenerator_graph_iff (P : SiteProfile)
    (x y : RegularHilbert (TowerHilbert P)) :
    (x,y) ∈ (regularPositiveGenerator P).graph ↔
      ∀ᵐ ξ ∂volume, ((regularSpectralCoordinates P).symm y) ξ =
        (Real.exp (-(2*Real.pi*ξ)) : ℂ) •
          ((regularSpectralCoordinates P).symm x) ξ
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351SineResolventApprox.lean:231` — `a1c6f5e77916ee527da3716f634431ddaf1f36c9dd80376ceee83aeb63c20c01`

```lean
theorem regularSpectralResolvent_right (P : SiteProfile) :
    (⟨regularSpectralResolvent P,regularSpectralResolvent_mem P⟩ :
      (regularCoreAlgebra P).toStarSubalgebra) ∈ scalarPolarRightAlgebra P
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarRightActionAlgebra.lean:173` — `68b1b9b84ba21c9c17de246fb69c8c48908e9ca313558b513322d119f66d98af`

```lean
theorem scalarRightAction_cfc (P : SiteProfile)
    (b : (regularCoreAlgebra P).toStarSubalgebra)
    (hb : b ∈ scalarPolarRightAlgebra P) (f : ℂ → ℂ) :
    ∃ hf : cfc f b.val ∈ regularCoreAlgebra P,
      (⟨cfc f b.val,hf⟩ : (regularCoreAlgebra P).toStarSubalgebra) ∈
        scalarPolarRightAlgebra P
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarMultiplierCalculus.lean:73` — `4dfa6cbd81aa481d695c2eec89985eb06487e7ba32432528d06c62ee7147f06c`

```lean
theorem realScalarMultiplier_cfc_ae (g : ℝ → ℝ) (hg : Continuous g)
    (h0 : ∀ x, 0 ≤ g x) (h1 : ∀ x, g x ≤ 1)
    (f : ℂ → ℂ) (hf : Continuous f) (u : RegularHilbert H) :
    cfc f (realScalarMultiplier g hg h0 h1) u =ᵐ[volume]
      fun x => f (g x : ℂ) • u x
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\GeneralExpectationCP.lean:55` — `698dd6c7d5d2125671b3a3c0cf70a27c144e3dc2d845ab54e093bea018d18aee`

```lean
theorem factor_positive_sqrt_mem (P : SiteProfile)
    (A : (theFactorObject P).toStarSubalgebra) (hA : 0 ≤ A) :
    CFC.sqrt (A : TowerHilbert P →L[ℂ] TowerHilbert P) ∈
      (theFactorObject P).toStarSubalgebra
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\SpecialFunctions\ContinuousFunctionalCalculus\Rpow\Basic.lean:302` — `ef03c823cc3798b288a7f00a2902b1fae092f1181bd44cb8b41ef133db389d5f`

```lean
lemma sqrt_eq_real_sqrt (a : A) (ha : 0 ≤ a := by cfc_tac) :
    CFC.sqrt a = cfcₙ Real.sqrt a
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\CStarAlgebra\ContinuousFunctionalCalculus\NonUnital.lean:870` — `61fe6bca314e50e5408d7f3e5b30c22f6dc7184924a203bfb545e799a9ad3c8d`

```lean
lemma cfcₙ_eq_cfc [ContinuousFunctionalCalculus R A p] [ContinuousMapZero.UniqueHom R A] {f : R → R}
    {a : A} (hf : ContinuousOn f (σₙ R a) := by cfc_cont_tac) (hf0 : f 0 = 0 := by cfc_zero_tac) :
    cfcₙ f a = cfc f a
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\CStarAlgebra\ContinuousFunctionalCalculus\Instances.lean:352` — `f05652edd12f24ddd2aa058ceb8762cceabda14a4580d7d237dcde26aaf8d6f4`

```lean
lemma cfc_real_eq_complex {a : A} (f : ℝ → ℝ) (ha : IsSelfAdjoint a := by cfc_tac) :
    cfc f a = cfc (fun x ↦ f x.re : ℂ → ℂ) a
```

Seis modalidades e outras bancadas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_cutoff_cfc\20260914_211744_334623\searches.json. Ausência nominal nos recortes não é ausência universal.


## Ficha/adendo integral: ADENDO_FICHA_CFC_RAIZ_HILBERT

[REAL — esclarecimento de fornecedor após DEV, antes da aceitação]

2026-09-14T21:24:15.159308-03:00

Existing generic Hilbert CFC.sqrt wrapper fixes canonical instances before specialization. Direct CFC.sqrt on the specialized Lp type caused an instance diamond in first DEV. The target uses the EXISTING wrapper, whose definition is literally CFC.sqrt, and an explicit generic real/complex CFC equality. No new square root or root hypothesis. GeneralExpectationCP was only a reuse model on a different algebra.

A ficha anterior cobre o alvo da raiz original e os conversores CFC; este adendo fixa o empacotamento já existente de V350AntiunitaryPositiveConjugation.lean:15. A consulta confirma a rota pelo grafo e é registrada separadamente.
