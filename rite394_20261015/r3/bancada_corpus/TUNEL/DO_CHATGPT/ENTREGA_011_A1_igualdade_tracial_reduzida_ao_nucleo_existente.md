[REAL — 4 teoremas e 0 definições verificados no delta por reprodução isolada autoral e revisão independente. A1(b): traço concreto ainda OPEN.]

# ENTREGA 011 / A1 — A igualdade tracial no núcleo existente equivale à igualdade em todo o core

2026-09-15T00:17:48.096252-03:00

Quatro teoremas públicos, dois auxiliares privados, nenhuma definição nova. Limites fortes sequenciais preservam cotas dos valores quadráticos do mesmo peso limite por Fatou, mesmo com valor infinito. Média direita e sanduíche original diminuem esses valores. Isso prova que a igualdade tracial no finiteDualStarCore existente equivale à igualdade tracial em todo o regularCoreAlgebra, com a hipótese local explicitamente consumida.

A igualdade no núcleo continua OPEN; a equivalência não a demonstra e não habita o contrato de traço. A consulta anexa é proposta matemática, não prova nova: compara a rota finita com vetores fixos de e_delta*e_delta e a identificação do implementador. A média unilateral e_delta não é auto-adjunta em geral. Não declarar o núcleo todo analítico ou finito-matricial. Normalidade, fidelidade, escala dual e semifinitude usual anteriores são preservadas. Nenhum novo GNS, peso, raiz, monólito, gate ou resultado empírico. Os minorantes positivos finitos são alvo separado ainda não aceito nesta entrega.

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

Autor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\tracial_extension_attempts\20260914_235447_962507\run.json`. Comando registrado: `['C:\\Users\\rotol\\.elan\\toolchains\\leanprover--lean4---v4.31.0\\bin\\lake.exe', 'build', 'TGLExt.AuditA1InverseLimitTracialExtension']`. Fonte e objeto autorais abaixo. Reutilização somente de objetos próprios previamente produzidos na raiz isolada; os pacotes externos vêm do cache explicitado no relatório. Não é nova compilação integral da biblioteca.

Revisor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_extensao_tracial\independent_20260915_000127_955551\run.json`. `695` objetos próprios anteriores; `0` fornecedores antigos recompilados adicionalmente. Zero objetos do autor/DEV herdados; `0` avisos de alvos/auditor. Avisos de fornecedores e diferenças binárias estão preservados em compilation.json. Comparação indisponível não significa igualdade.

As tentativas de desenvolvimento que falharam permanecem em disco. Só o fonte final, as reproduções rc0 e as auditorias aceitas entram nesta conclusão. Controle negativo de uma aplicação adulterada não é um teorema geral de inexistência.

## Fontes e objetos autorais

| Módulo | SHA256 fonte | SHA256 objeto |
|---|---|---|
| `V351InverseLimitTracialExtension` | `b1987ee0746e1f64da3920ac11a44a39f263ccb4108ace1b86e630f4a9d3aeb3` | `42f8748fea7908afd35bd44be945679fbcac2b7937c271e459d3009b48d1a161` |

## Tipos completos e axiomas

```lean
TGLV350.Regular.scalarInverseLimitWeight_square_le_of_strong (P : TGLExt.SiteProfile)
  (A : ℕ → ↥(VonNeumannAlgebra.toStarSubalgebra.{0} (TGLV350.Regular.regularCoreAlgebra P)))
  (S : ↥(VonNeumannAlgebra.toStarSubalgebra.{0} (TGLV350.Regular.regularCoreAlgebra P)))
  (hlim :
    ∀ (v : ↥(TGLV350.Regular.RegularHilbert (TGLExt.TowerHilbert P))),
      Filter.Tendsto.{0, 0} (fun n => ↑(A n) v) Filter.atTop.{0} (nhds.{0} (↑S v)))
  (C : ENNReal)
  (hb : ∀ (n : ℕ), LE.le.{0} (TGLV350.Regular.scalarInverseLimitWeight P (TGLV351.positiveSquare P (A n))) C) :
  LE.le.{0} (TGLV350.Regular.scalarInverseLimitWeight P (TGLV351.positiveSquare P S)) C
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.scalarInverseLimitWeight_right_average_le (P : TGLExt.SiteProfile)
  (A : ↥(VonNeumannAlgebra.toStarSubalgebra.{0} (TGLV350.Regular.regularCoreAlgebra P))) (δ : ℝ) :
  LE.le.{0}
    (TGLV350.Regular.scalarInverseLimitWeight P
      (TGLV351.positiveSquare P (HMul.hMul.{0, 0, 0} A (Subtype.mk.{1} (TGLV350.Regular.regularAverage P δ) ⋯))))
    (TGLV350.Regular.scalarInverseLimitWeight P (TGLV351.positiveSquare P A))
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.scalarInverseLimitWeight_sandwich_le (P : TGLExt.SiteProfile)
  (A : ↥(VonNeumannAlgebra.toStarSubalgebra.{0} (TGLV350.Regular.regularCoreAlgebra P))) (δ : ℝ) :
  LE.le.{0}
    (TGLV350.Regular.scalarInverseLimitWeight P (TGLV351.positiveSquare P (TGLV350.Regular.regularSandwich P A δ)))
    (TGLV350.Regular.scalarInverseLimitWeight P (TGLV351.positiveSquare P A))
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.scalarInverseLimitWeight_tracial_iff_core (P : TGLExt.SiteProfile) :
  (∀ (A : ↥(VonNeumannAlgebra.toStarSubalgebra.{0} (TGLV350.Regular.regularCoreAlgebra P))),
      Eq.{1} (TGLV350.Regular.scalarInverseLimitWeight P (TGLV351.positiveSquare P A))
        (TGLV350.Regular.scalarInverseLimitWeight P (TGLV351.positiveSquare P (star.{0} A)))) ↔
    ∀ (A : ↥(VonNeumannAlgebra.toStarSubalgebra.{0} (TGLV350.Regular.regularCoreAlgebra P))),
      Membership.mem.{0, 0} (TGLV350.Regular.finiteDualStarCore P) A →
        Eq.{1} (TGLV350.Regular.scalarInverseLimitWeight P (TGLV351.positiveSquare P A))
          (TGLV350.Regular.scalarInverseLimitWeight P (TGLV351.positiveSquare P (star.{0} A)))
```

Axiomas: propext, Classical.choice, Quot.sound.

## Custódia e limites

- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\AUDITORIA_EXTENSAO_TRACIAL_A1B.json` — SHA256 `84da8fcfac7b01d2ebf09ab0fc477e2b36376267cc1ba877d30539bdedb997ed`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_extensao_tracial\REVIEW_A1_TRACIAL_EXTENSION_FINAL.json` — SHA256 `21557e52ff15dc506d6e1dba0ccb1356e71bc7dbe41aa931d17ffaa3cf50bc97`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_extensao_tracial\compilation.json` — SHA256 `7db10ad3ce2f2c3dd3ad136d989e02ded791ce6032390313068ab7245b2271ef`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\ACEITE_DELTA_TRACIAL_EXTENSION_FINAL.json` — SHA256 `017f2812f8606780bc24f932b0a8cab21ab5bcbf5c21d49569c0987d2d3c2e5c`.

O manifesto e o recibo próprios ligam esta entrega aos arquivos efetivamente lidos. Nenhum monólito canônico foi importado ou executado; nenhum dado experimental, D1, sigma, Atlas ou diário canônico foi alterado.

## Revisão independente integral

2026-09-15T00:06:54.122591-03:00

**A1_TRACIAL_EXTENSION_REVIEW_ACCEPTED__CORE_TRACIALITY_TRACE_OPEN**

[REAL] **Sem achados P0/P1/P2.** Módulo completo e auditor próprios rc0; quatro #check com universos e quatro #print axioms no trio permitido. Dois helpers privados incluídos transitivamente.

[REAL — tipos] Quatro teoremas públicos, dois helpers privados transitivos, nenhuma definição nova. Todos usam o MESMO scalarInverseLimitWeight e positiveSquare. A primeira conclusão é fechamento de subnível para SEQUÊNCIAS fortemente convergentes A_n, com C : ℝ≥0∞ arbitrário; não se exige C<∞, uniformidade de norma ou convergência dos adjuntos. Não foi promovida a uma afirmação topológica sobre redes arbitrárias ou a uma caracterização completa de LSC além do enunciado compilado.

[REAL — Fatou e Haar] dualSquare_le_of_strong passa A_n→S para θ_s(A_n)v pela conjugação limitada já existente, e daí para os quadrados das normas. Isso evita inferir forte convergência de A_n* ou de A_n*A_n. O integrando incorpora ENNReal.ofReal dualHaarFactor, finito; measurabilidade, continuidade ofReal e multiplicação pelo fator finito dão o limite ponto a ponto. Fatou fornece a desigualdade sem DCT ou finitude de C. Em cada regulador k, usa-se A_n b_k→S b_k, com b_k a raiz ORIGINAL do corte. A identidade de quadrados vem de star_mul/associatividade; o limite τ é obtido por iSup_le. Mesmo vetor, Haar e corte, sem toReal de infinito.

[REAL — média direita] scalarInverseLimitWeight_right_average_le vale para TODO A∈N e todo δ real, incluindo 0, conforme o fornecedor antigo. Para ε=1/(k+1)>0, a raiz b_k pertence a N pelo lema regularInverseGeneratorCutoff_sqrt_right; basta a primeira componente da conclusão, já paga. A comutação usada é b_k eδ=eδ b_k: (A eδ)b_k=(A b_k)eδ. Não se comuta A com b_k ou com eδ. scalarWeight_right_average_le recebe A b_k sem hipótese de quadrado finito. O mesmo índice k é comparado antes dos supremos.

[REAL — sanduíche e ordem] regularSandwich A δ=eδ* A eδ. O helper genérico hilbert_contraction_left_square usa ‖c‖≤1 para c*c≤I e então a*(c*c)a≤a*a. Aplicado a c=eδ* e a=Aeδ, dá a ordem dos QUADRADOS dos dois operadores, seguida da monotonicidade do peso e do bound de média direita. Não usa eδ=eδ*, nenhuma ordem no conjugador de sanduíches e nenhuma tracialidade para permutar fatores.

[REAL — equivalência exata e não circularidade] O sentido global→núcleo é restrição. No outro, o limite forte dos sanduíches com δ_n=1/(n+1)>0 e a primeira conclusão dão τ(A*A)≤τ(AA*) usando hcore em cada sanduíche, regularSandwich_star e o bound para A*. Repetir com A* dá igualdade em ENNReal, inclusive infinito. A hipótese hcore é consumida explicitamente; não se prova esse antecedente nem se declara finiteDualStarCore analítico ou finito-matricial. O tipo global coincide com a forma do campo RegularCoreTraceData.tracial (linha58) quando value é τ, mas não constrói um habitante do contrato.

[REAL — ficha/histórico/controle] Nove fornecedores da ficha e dois do adendo foram conferidos por bytes, linhas e prefixos; tipos completos relevantes relidos. A ficha precede o código. O adendo é explicitamente posterior ao primeiro DEV, corrige linha59 para58 e localiza o fornecedor de pertença real da raiz; não foi reclassificado como anterior a toda implementação. O prefixo de norm_le_one_iff_of_nonneg é documentalmente truncado no binder opcional; o enunciado completo foi lido e é adequado. O primeiro DEV rc1 preservado tem Unknown identifier regularInverseCutoffSqrt_mem e not a positivity goal; foi excluído. O final e standalone estão rc0. O negativo BadTracialCorePremiseRemoved falha por Type mismatch ao tentar usar a equivalência como prova incondicional de tracialidade. Esse controle foi relido/pinado, não reexecutado; não é evidência de impossibilidade do antecedente.

[REAL — proveniência] 695 objetos anteriores de V preservados; 2 objetos novos (alvo e auditor), total 697. Nenhum fornecedor antigo reconstruído e nenhum objeto de K/DEV importado. Run próprio 35.641 s; zero avisos do alvo/auditor; 178 mensagens de fornecedores herdadas discriminadas no JSON. Traces confirmam LEAN_PATH dentro de V/pacotes. Jobs totais Lake não são recompilações novas.

| Artefato | SHA256 lido |
|---|---|
| Fonte K = snapshot = V | b1987ee0746e1f64da3920ac11a44a39f263ccb4108ace1b86e630f4a9d3aeb3 |
| .olean próprio | 42f8748fea7908afd35bd44be945679fbcac2b7937c271e459d3009b48d1a161 |
| .olean autoral standalone, somente comparação | 42f8748fea7908afd35bd44be945679fbcac2b7937c271e459d3009b48d1a161 |

Igualdade binária do alvo medida: True.

[OPEN — limites] Aceite27 restrito à redução formal: quatro alvos, dois auxiliares transitivos; nenhum novo peso, GNS, cone ou contrato. A propriedade de subníveis provada é sequencial/forte; o teorema não tem parâmetro de rede arbitrária nem demanda uma cota de norma. Tracialidade no finiteDualStarCore continua OPEN, assim como a conclusão tracial completa A1(b) e os minorantes positivos finitos exigidos pelo contrato final. Normalidade, fidelidade, escala dual e semifinitude usual já entregues são herdadas; não foram reabertas como novas obrigações. K, OLD, memória, writers e monólito não foram escritos/executados pelo revisor. Só V recebeu o alvo/auditor novos; todos os pins próprios anteriores protegidos permaneceram iguais.

Evidências:

- [compilation](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_extensao_tracial\compilation.json>) — SHA256 7db10ad3ce2f2c3dd3ad136d989e02ded791ce6032390313068ab7245b2271ef.
- [run próprio](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_extensao_tracial\independent_20260915_000127_955551\run.json>) — SHA256 107d82e7ba2fd1fa1397d3314a6d95001332845bba4ac1f2a838ce2c71aac180.
- [tipos e axiomas completos](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_extensao_tracial\independent_20260915_000127_955551\type_axiom_audit.json>) — SHA256 ec54fe6a20b2383981b72f173ee10f60c16cdb2dbd88641a8cabc74b0a4ae99b.
- [histórico DEV](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_extensao_tracial\history_read.json>) — SHA256 dffbbea57809a844803451509158a9052759a4e6b3614118dccb0377a9519695.
- [fornecedores e consumidor](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_extensao_tracial\provider_checks.json>) — SHA256 0bb89c6d1bf01c56be69f07b6e0fc65952810ec5d766ad78ebe0d989637cb49f.


## Ficha/adendo integral: REAPROVEITAMENTO_A1B_EXTENSAO_TRACIAL

[OPEN — ficha anterior à extensão tracial]

# A1(b): o núcleo existente basta para a igualdade tracial

2026-09-14T23:50:30.408996-03:00

ADAPTAR: for the SAME scalarInverseLimitWeight, prove bounded square values survive strong limits, tau(positiveSquare(regularSandwich a delta)) <= tau(positiveSquare a), then traciality on the EXISTING finiteDualStarCore iff traciality on all regularCoreAlgebra. Consumer: RegularCoreTraceData.tracial, V351RegularCoreTraceContract.lean:59 (recheck line). No traciality assumed globally, no new weight/core/GNS, no replacement trace contract. The core equality remains an explicit missing lemma; this extension alone does not inhabit the trace contract. Strong convergence of adjoints is taken from existing sandwich theorem, never presumed for arbitrary strong limits.

A prova usa Fatou em cada corte e a comutação já paga com as médias. Não compara sanduíches por ordem do conjugador. As buscas nominais abaixo são complementadas pela leitura dos enunciados e fontes destes fornecedores. Nenhuma ausência universal é alegada.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseLimitWeight.lean:94` — `cfdced33d3cafdd2782f4d7e8ca77974e0ddee22f19803dfbd36275787c28f1e`

```lean
theorem scalarInverseCutoffWeight_le_limit (P : SiteProfile) (n : ℕ) (X : PositiveCoreInput P) :
    scalarInverseCutoffWeight P (1/((n : ℝ)+1)) X ≤ scalarInverseLimitWeight P X
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseLimitWeight.lean:109` — `cfdced33d3cafdd2782f4d7e8ca77974e0ddee22f19803dfbd36275787c28f1e`

```lean
theorem scalarInverseLimitWeight_mono (P : SiteProfile) (X Y : PositiveCoreInput P) (hXY : X ≤ Y) :
    scalarInverseLimitWeight P X ≤ scalarInverseLimitWeight P Y
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350DualCutNormality.lean:49` — `026f5042bd6adee2fcf90ce1db5b9831ee312b3bccaf4a194b8631936d543d65`

```lean
theorem dualAmbient_tendsto_strong {ι : Type*} {l : Filter ι}
    (A : ι → RegularHilbert H →L[ℂ] RegularHilbert H)
    (S : RegularHilbert H →L[ℂ] RegularHilbert H)
    (hlim : ∀ v, Tendsto (fun i => A i v) l (𝓝 (S v))) (s : ℝ) (v : RegularHilbert H) :
    Tendsto (fun i => dualAmbient s (A i) v) l (𝓝 (dualAmbient s S v))
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarRightAverage.lean:70` — `64d49e1de18504e9e66e7559f48df9f6811c80821524b85324ee0a1305793aed`

```lean
theorem scalarWeight_right_average_le (P : SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra) (h : ℝ) :
    dualQuadraticIntegral (star (A.val * regularAverage P h) * (A.val * regularAverage P h))
      (regularVacuum P) ≤ dualQuadraticIntegral (star A.val * A.val) (regularVacuum P)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351CutoffAverageCommutation.lean:49` — `bc881ee5df7e027859ef14d7379b27bc9c2a27bea3b08cf42d6604805afa2a66`

```lean
theorem regularInverseCutoffSqrt_commutes_average (P : SiteProfile)
    (ε : ℝ) (hε : 0 < ε) (δ : ℝ) :
    Commute (hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε))
      (regularAverage P δ)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350FiniteDualStarCore.lean:55` — `017fd7d4c1efd3c0ddfba91b3a6464fdbc194dce8e4ee0a6ad4580a0a6ac98ce`

```lean
theorem regularSandwich_star (P : SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra) (h : ℝ) :
    star (regularSandwich P A h) = regularSandwich P (star A) h
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350FiniteDualStarCore.lean:63` — `017fd7d4c1efd3c0ddfba91b3a6464fdbc194dce8e4ee0a6ad4580a0a6ac98ce`

```lean
theorem regularSandwich_mem_finiteDualStarCore (P : SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra) (h : ℝ) (hh : 0 < h) :
    regularSandwich P A h ∈ finiteDualStarCore P
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350FiniteDualStarCore.lean:94` — `017fd7d4c1efd3c0ddfba91b3a6464fdbc194dce8e4ee0a6ad4580a0a6ac98ce`

```lean
theorem regularSandwich_tendsto (P : SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra)
    (v : RegularHilbert (TowerHilbert P)) :
    Tendsto (fun h : ℝ => (regularSandwich P A h).val v) (𝓝[>] 0) (𝓝 (A.val v))
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351WeightAverageRecovery.lean:16` — `a72b71ac86bb0b2a5c81d5bfaba3c6ad964bf4a8beffd0a9df89f7ee26391fac`

```lean
theorem scalarWeight_square_eq_iSup_averages (P : SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra) :
    dualQuadraticIntegral (star A.val*A.val) (regularVacuum P) =
      ⨆ n : ℕ, dualQuadraticIntegral
        (star (A.val*regularAverage P (1/((n : ℝ)+1))) *
          (A.val*regularAverage P (1/((n : ℝ)+1)))) (regularVacuum P)
```

Seis modalidades e outras bancadas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_tracial_extension\20260914_235009_395646\searches.json. Ausência nominal nos recortes não é ausência universal.


## Ficha/adendo integral: ADENDO_FICHA_EXTENSAO_TRACIAL

[OPEN — complemento de fornecedores, após o primeiro DEV, antes da aceitação]

{
  "timestamp": "2026-09-14T23:54:39.012601-03:00",
  "status": "FICHE_ADDENDUM_AFTER_FIRST_DEV_BEFORE_ACCEPTANCE",
  "providers": [
    {
      "name": "regularInverseGeneratorCutoff_sqrt_right",
      "source": {
        "path": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\RETOMADA_A1B_012\\k\\TGLExt\\V351InverseCutoffCFC.lean",
        "bytes": 7577,
        "sha256": "cbdf10aea749a552b0f47afb3ef59560ed47d6f46cf7dd8064dc963a092c3490"
      },
      "line": 125,
      "statement": "theorem regularInverseGeneratorCutoff_sqrt_right (P : SiteProfile) (ε : ℝ) (hε : 0 < ε) :\n    ∃ h : hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε) ∈ regularCoreAlgebra P,\n      (⟨hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε),h⟩ :\n        (regularCoreAlgebra P).toStarSubalgebra) ∈ scalarPolarRightAlgebra P"
    },
    {
      "name": "norm_le_one_iff_of_nonneg",
      "source": {
        "path": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\RETOMADA_A1B_012\\k\\.lake\\packages\\mathlib\\Mathlib\\Analysis\\CStarAlgebra\\ContinuousFunctionalCalculus\\Order.lean",
        "bytes": 28173,
        "sha256": "0802a500623d378e8c953961cac3c6391932515a7236d44dbceea11e2eb4611b"
      },
      "line": 245,
      "statement": "lemma norm_le_one_iff_of_nonneg (a : A) (ha : 0 ≤ a"
    }
  ],
  "consumer": {
    "source": {
      "path": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\RETOMADA_A1B_012\\k\\TGLExt\\V351RegularCoreTraceContract.lean",
      "bytes": 5624,
      "sha256": "3694175f8ef5bcf5848d88bd8061abf8546480873964ebfdc19dd41ad05928f0"
    },
    "line": 58,
    "statement": "  tracial : ∀ a, value (positiveSquare P a) = value (positiveSquare P (star a))"
  },
  "first_dev": "dev_tracial_extension/20260914_235244_987632/run.json",
  "scope": "Exact missing membership supplier and generic contraction order adapter; no new root. First six-mode scan failed only at TOE/acervo by sandbox read denial. Preserved error logs. Second scan with authorized read escalation succeeded in all modes and generated the pre-code fiche. Initial tracial consumer line59 corrected to measured line58 here; no older record erased."
}


## Ficha/adendo integral: revisao_consulta_rota_tracial_2/CONSULTA_ROTA_TRACIAL_2_V2

# Consulta: rota finita versus identificação do implementador original

[DERIVED / OPEN — consulta matemática, não revisão DEV]

Data: 2026-09-15T00:00:09.472583-03:00. Objetos: o mesmo ν=scalarDualWeight, τ=scalarInverseLimitWeight, S, F=S†, Δν=FS, J=scalarTomitaPolarFactor e U=scalarTomitaImaginaryPower. Nenhuma compilação, alteração Lean ou atualização de memória nesta consulta. Os fornecedores abaixo foram relidos; seus pins e trechos estão no JSON ao lado. A aceitação anterior das construções é herdada, não uma nova auditoria de axiomas.

A rota finita tem uma expressão candidata concreta que cancela a densidade matricial no MESMO τ. Porém, os fornecedores atuais não entregam automaticamente a leitura espectral desse peso nem a extensão dos níveis à álgebra inteira. O passo menor que identifiquei para a rota Q é provar a ação direita das médias, extrair vetores simultaneamente fixos por S e F e identificar U em um conjunto total. Isso reduz uma obrigação efetiva; a compatibilidade de meias potências/Q e a tracialidade continuam separadas.

## 1. Correção da sugestão das médias

[REAL — fonte] [regularAverage](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350RegularApproximation.lean:36>) define
eδ = δ⁻¹ ∫₀^δ λ_t dt, como integral FORTE de operadores, δ>0.
É uma média unilateral; não é auto-adjunta em geral. O programa não fornece SΛ(eδ)=Λ(eδ), muito menos FΛ(eδ)=Λ(eδ). Pertencer à álgebra das translações ou preservar ν não basta para essas igualdades.

[DERIVED] Use zδ=eδ*eδ. Ele é positivo, é quadrado-finito por eδ∈nν e pela propriedade de ideal à esquerda, e pertence também ao domínio algébrico da estrela. Os fornecedores são [regularAverage_hasFiniteDualSquare](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350DualSemifiniteIdeal.lean:108>), [finiteDualLeftIdeal_le_scalarWeight](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350ScalarWeightDomain.lean:50>) e [scalarClosedTomita_extends_weight_star](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350ScalarWeightTomitaIdentification.lean:71>).

A obrigação nova mais imediata pode ser enunciada matematicamente assim (nomes propostos, não constantes Lean existentes):

• **average_mem_polar_right**: δ>0 ⇒ eδ ∈ scalarPolarRightAlgebra P.
• **average_square_fixed_original_pair**: para ζδ=Λν(zδ), ζδ∈D(S)∩D(F) e Sζδ=Fζδ=ζδ.

Não receber essas conclusões como campos. A segunda segue da primeira e dos pares já construídos, conforme o argumento abaixo.

## 2. Prova menor da identificação U=πλ R₋ₜ

[REAL — fornecedores] [scalarPolarRightAlgebra_regular_mem](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V351ScalarRightActionAlgebra.lean:164>) dá a pertinência das translações à álgebra direita E; [scalarPolarRightAlgebra](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V351ScalarRightActionAlgebra.lean:94>) exige a propriedade direita tanto para b quanto para b*. [scalarRightAction_closed_of_bounded_strongStar](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V351ScalarRightActionLimits.lean:26>) transporta a identidade para uma família uniformemente limitada convergente forte-*; a existência da família não está embutida no teorema.

[OPEN — adaptador efetivo] Para obter eδ∈E, construir somas finitas
b_m = m⁻¹ Σ_{k<m} λ_(δ k/m), m≥1.
Cada b_m está em E, tem norma ≤1 e converge fortemente a eδ; as somas adjuntas convergem a eδ*. A continuidade forte de λ no intervalo compacto paga a aproximação por somas de Riemann em cada vetor. Aplicar o fechamento forte-* duas vezes, para b_m e b_m*. Não invocar integral de Bochner de λ em B(H): a continuidade em norma dos operadores não está disponível. O fechamento EM NORMA de E, isoladamente, também não paga esta passagem. [operatorIntegral_apply](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350StrongOperatorIntegral.lean:51>) e [operatorIntegral_norm_le](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350StrongOperatorIntegral.lean:54>) fornecem a integral e a cota; não localizei nesta consulta um lema pronto que já faça toda a aproximação de E pela média.

[DERIVED] Defina ρ(z)=Jπ(z*)J⁻¹, com os mesmos objetos. Para z=zδ, a propriedade E e [scalarWeightGNSAction_intertwines](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350ScalarWeightAction.lean:38>) dão
ρ(z)Λ(a)=Λ(az)=π(a)Λ(z), para TODO a∈nν.
Como z=z*, ρ(z) é auto-adjunto. Portanto essas duas identidades fornecem os campos reais de [ScalarRightAdjointPair](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350ScalarRightAdjointPair.lean:17>), ambos com vetor Λ(z). [scalarRightAdjointPair_maximal](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350ScalarRightAdjointPair.lean:128>) dá FΛ(z)=Λ(z) no adjunto máximo ORIGINAL. A extensão da estrela dá SΛ(z)=Λ(z). Não se presume continuidade de S nem domínio total.

[DERIVED] Pelo domínio EXATO de [scalarTomitaSquare_domain_iff](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350ScalarTomitaSquare.lean:40>), ζδ∈D(Δν) e Δνζδ=ζδ. Então [scalarTomitaResolvent_inverse](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350ScalarTomitaResolvent.lean:24>) dá Tνζδ=½ζδ, onde Tν=(1+Δν)⁻¹. A igualdade U_tζδ=ζδ pode ser obtida diretamente de [scalarTomitaImaginaryPower_damping](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V351ScalarTomitaImaginaryPowers.lean:29>): b(½)=¼ e g_t(½)=¼. Um adaptador CFC para um autovetor basta; [complex_cfc_selfadjoint_intertwines](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V351ResolventImaginaryIntertwining.lean:15>) permite produzi-lo usando um operador de posto um e (½)I. Tratar ζδ=0 sem pressupor vetor não nulo/separante. Essa aplicação do CFC ainda é obrigação nova, não execução desta consulta.

[REAL — sinal] [scalarTomitaPolar_regular_generator](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350ScalarRegularPolarCommutation.lean:50>) prova Jπ(λ_t)J⁻¹=R₋ₜ, com R_t=regularRightGNS P t. Assim o candidato correto é
W_t=π(λ_t)R₋ₜ=π(λ_t)Jπ(λ_t)J⁻¹.
Não substituir por π(λ_t), nem por π(λ_t)R_t. [regularRightGNS_commutes_left](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350ScalarRegularPolarCommutation.lean:13>) vale para toda a álgebra representada.

[DERIVED] zδ comuta com todas as λ_t, por [operatorIntegral_commutes](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350StrongOperatorIntegral.lean:59>) e a lei de grupo. Logo W_tΛ(zδ)=Λ(zδ). U já implementa a mesma ação no core inteiro por [scalarTomitaImaginaryPower_core_conjugation](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V351ScalarImaginaryCoreAction.lean:47>). Portanto U e W coincidem em π(a)Λ(zδ), para todo a∈N.

Falta apenas uma totalidade que tem fornecedores diretos, sem escolher outro GNS. [regularAverage_tendsto_identity](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350RegularApproximation.lean:68>) e [regularAverage_star_tendsto_identity](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350ContractionAdjointLimit.lean:51>) dão zδ→1 forte, com norma ≤1. [scalarGNSRepresentation_tendsto_of_uniformly_bounded](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350ScalarGNSStrongContinuity.lean:16>) dá π(zδ)→I e, conjugando pelo J limitado, ρ(zδ)→I. Como π(a)Λ(zδ)=ρ(zδ)Λ(a), a densidade de [scalarWeightGNSEmbedding_denseRange](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350ScalarWeightAction.lean:54>) torna a união dessas órbitas total. Não é necessário afirmar que UMA média produz vetor cíclico.

Resultado alvo: igualdade dos operadores limitados U_t=W_t em TODO H_I. Covariância sozinha só coloca W_t⁻¹U_t no comutante; os vetores fixos e a totalidade são o passo que elimina esse resíduo. A unicidade [scalarTomitaImaginaryPower_unique](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V351ScalarTomitaImaginaryPowers.lean:35>) exige a identidade amortecida, não apenas implementar a mesma ação.

[OPEN] Essa identificação não é, sozinha, a identidade quadrática Q do peso perturbado. Ainda se precisa transportar o dado de potências reais para a compatibilidade de domínios/formas de meia potência que compara os limites das normas de a e a*. Não identificar h com Δν. A consulta anterior de tracialidade permanece válida nesse limite.

## 3. O que a rota finita realmente entregaria

[REAL — objetos] Os níveis gerais usam towerW P N, estritamente positivo e de soma 1, não a família estacionária chainWeights l N de outro contexto. [tState](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/TowerDefinite.lean:102>) é Σ_i w_i a_ii; [omegaState_pi](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/TheFactorObject.lean:109>) identifica essa avaliação com o vetor da MESMA torre. [flowLevel_single](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/ModularFlowSpectrum.lean:49>) fornece o peso de E_ij. O nome informal “finiteMatrix” não identifica um fornecedor separado: os objetos encontrados são Matrix, towerPi, tState e rhoMat.

[DERIVED — coordenadas propostas, ainda sem lema Lean] Fixado um nível, escreva ρ=diag(w_i). No subespaço redutor L²(ℝ,levelSpace P N), a Fourier ordinária transforma λ_t, na entrada i,j, em
exp(it(log w_i − log w_j − 2πξ)).
O sinal vem de [fourier_shift](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V351FourierTranslation.lean:47>) e [regularUnitary](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350RegularTowerRepresentation.lean:16>). Faça p=2πξ+log w_j, por coluna j, incluindo o fator (2π)⁻¹/² na mudança unitária de L². Nestas coordenadas as ações esquerdas seriam
π_n(a)=a,  λ_t=ρ^{it} exp(−itp),  h=ρ exp(−p).

O subespaço redutor e a restrição precisam ser identificados efetivamente com as inserções existentes. [project_flow_commutes](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/ExpectationProjection.lean:58>) e a comutação da projeção de nível com a ação esquerda finita fornecem os ingredientes. A absorção [regularFlowAbsorptionUnitary](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V351RegularFlowAbsorption.lean:51>) não pode ser citada como se deixasse a base constante: sua conjugação também move a ação da base. A leitura acima usa Fourier e mudança por coluna explicitamente. Para o MESMO h, transportar [regularPositiveGenerator_graph_iff](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V351RegularSpectralGraph.lean:40>) ou as potências já identificadas, sem nomear um gerador novo e declará-lo igual.

[DERIVED — avaliação candidata a provar] Para um operador positivo do nível representado pelo campo matricial limitado X(p), as identidades alvo são, com valores em ENNReal,
ν(X) = (2π)⁻¹ ∫ Σ_i w_i X_ii(p) dp,
νε(X) = (2π)⁻¹ ∫ Σ_i w_i/(ε+w_i exp(−p)) X_ii(p) dp,
τ(X) = (2π)⁻¹ ∫ exp(p) Tr(X(p)) dp.

A primeira não é uma definição alternativa de ν. Deve seguir de [dualQuadraticIntegral](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350DualWeightForm.lean:62>), [dualHaarFactor](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350DualWeightForm.lean:17>), do vetor [regularVacuum](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350ScalarDualWeightFaithfulness.lean:15>), da norma do indicador testVector, e de Tonelli/Plancherel. A integração na variável dual elimina a densidade espectral do indicador de norma 1. A segunda avalia o corte ORIGINAL por sua identidade de grafo; a terceira usa convergência monótona dos coeficientes, inclusive valor infinito. O fator (2π)⁻¹ não pode ser omitido. A verificação de sinal é θ_sX(p)=X(p+s), compatível com θ_sh=e⁻ˢh e τ∘θ_s=e⁻ˢτ.

A fórmula final daria τ(a*a)=τ(aa*) nesse nível por ciclicidade da matriz finita, sem um novo GNS ou peso. Mas é um ALVO derivado, não teorema encontrado. Nem todo operador do core já vem acompanhado do campo X e da prova dessa avaliação. Mesmo num nível, adjoinar todas as λ_t deixa uma variável espectral contínua; a álgebra resultante não é simplesmente M_d.

O primeiro lema concreto da rota finita seria a avaliação dual normalizada na primeira fórmula, para campos matriciais positivos de uma classe especificada, com a identidade de representação comprovada. Começar por campos contínuos de suporte compacto reduz mensurabilidade, mas deixa explícita sua extensão posterior.

## 4. Expectativas e extensão: limites reais

[REAL] [expectation_preserves_state](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/TowerExpectation.lean:90>) preserva o estado da BASE. [expectation_flow_commutes](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/ExpectationProjection.lean:65>) é equivariância modular dessa expectativa de base. [levelExpectation_strong_tendsto](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350LevelExpectationStrongLimit.lean:16>) e [represented_levelExpectation_strong_tendsto](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350LevelExpectationStrongLimit.lean:44>) dão convergência forte, incluindo a representação escalar. Não localizei no conjunto consultado uma expectativa já transportada para TODO core que preserve ν ou τ e tenha a desigualdade quadrática requerida. Isso é limite da consulta delimitada, não inexistência exaustiva no acervo.

A geração do core por base e λ, e a passagem de COMUTAÇÃO por geradores, não são um teorema de aproximação forte-* uniformemente limitada de todos os operadores por níveis finitos. Para extensão tracial seria necessário construir essa aproximação com controle de peso, ou uma expectativa do core com preservação/Schwarz adequadas. Igualdade em aproximantes mais semicontinuidade, sem controle superior, não basta.

[INPUT — autoria atual, não revisada aqui] O novo delta 27 foi anunciado com redução por sanduíches e Fatou. Sua revisão independente virá após esta consulta. Mesmo que a redução seja aceita, ela entrega “trace em finiteDualStarCore ⇔ trace global”; não identifica finiteDualStarCore com união dos níveis. [regularSandwich_mem_finiteDualStarCore](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350FiniteDualStarCore.lean:63>) admite eδ* a eδ para a arbitrário do core. Portanto esse conjunto não deve ser chamado inteiro de analítico, finito-matricial ou núcleo de autovetores homogêneos.

## 5. Decisão e estatutos

| Próximo passo | Estatuto nesta consulta | Redução real |
|---|---|---|
| eδ∈E por médias fortes-* de λ | OPEN, com fornecedores diretos | Fornece pares para zδ; nenhum peso/GNS novo |
| Sζδ=Fζδ=ζδ → Tνζδ=½ζδ → Uζδ=ζδ | DERIVED, aplicação Lean pendente | Fixa o implementador ORIGINAL em conjunto útil |
| Totalidade conjunta π(N)Λ(zδ), U=πλR₋ₜ | DERIVED após passos anteriores | Elimina resíduo de comutante; não supõe TT |
| Avaliação finita ν/νε/τ nas coordenadas p | DERIVED, ponte espectral integral OPEN | Cancelamento explícito de ρ no mesmo τ |
| Níveis → finiteDualStarCore → todo N | OPEN; segunda seta em revisão autoral separada | Exige aproximação/controladores reais |
| Q, tracialidade e minorantes do traço final | OPEN | Não pagos por isometria J, escala dual ou semifinitude usual |

Minha recomendação de custo é começar por **average_mem_polar_right**, em seguida o par fixo de zδ e a identificação dos implementadores por totalidade. A rota finita permanece alternativa concreta, mas a infraestrutura relida não a torna uma ligação imediata. Nenhuma parte desta consulta cobra novamente normalidade, fidelidade, escala dual ou semifinitude usual já entregues; a propriedade de minorantes positivos finitos continua reservada ao traço final.

Pins, locadores e blocos completos das declarações consultadas: [evidência JSON](./CONSULTA_ROTA_TRACIAL_2.json). A página primária de [Hiai, arXiv:2004.02383](https://arxiv.org/abs/2004.02383) foi consultada apenas como referência bibliográfica; nenhuma identificação local foi importada de TT/PT por citação. A busca foi limitada aos fornecedores indicados e seus imports relevantes. Ausências de nomes adivinhados foram corrigidas por busca; não são ausência de prova. Não houve varredura exaustiva, novo teorema, teste ou promoção de A1(b).


---

Adendo de formato — 2026-09-15T00:09:53.995790-03:00

[REAL] V2 corrige exclusivamente a serialização dos campos path dos 39 pins para str(Path) no Windows. Todos os arquivos foram relidos em bytes; tamanhos e hashes coincidem com os registrados originalmente. ExpectationProjection.lean coincide em K, V e kernel base. A recusa do writer decorreu da comparação literal de C:/... com C:\..., não de mutação Lean. O writer estrito permanece intacto. Nenhuma afirmação matemática, fonte, compilação ou parecer 27 foi alterado. Os documentos originais permanecem preservados.

Para a entrega, utilizar este MD com [CONSULTA_ROTA_TRACIAL_2_V2.json](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_consulta_rota_tracial_2\CONSULTA_ROTA_TRACIAL_2_V2.json>). A remissão original ao JSON anterior no corpo fica mantida como histórico. A [evidência da correção](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_consulta_rota_tracial_2\CORRECAO_CAMINHOS_CONSULTA_ROTA_TRACIAL_2.json>) registra os caminhos anteriores e atuais, sem normalizar bytes ou hashes.
