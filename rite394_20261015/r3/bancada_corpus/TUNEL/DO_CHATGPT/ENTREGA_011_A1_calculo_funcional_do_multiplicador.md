[REAL — 3 teoremas e 2 definições verificados no delta por reprodução isolada autoral e revisão independente. A1(b): traço concreto ainda OPEN.]

# ENTREGA 011 / A1 — O cálculo funcional do multiplicador existente

2026-09-14T20:00:11.652459-03:00

O levantamento pontual existente é reunido num homomorfismo complexo unital de álgebras estrela em C([0,1],ℂ). Sua continuidade vem da cota de norma já provada. A naturalidade de CFC dá cfc(f,M_g)u=f(g)u quase em toda parte, para g contínua real entre zero e um e f globalmente contínua. O consumidor é a fase amortecida já usada nas potências imaginárias; nenhum L² nem grupo de potências é redefinido.

O delta é a ponte de cálculo funcional. A identificação das potências, afiliação, escala dual e traço têm entregas ou obrigações próprias; este módulo não fornece RegularCoreTraceData.

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

Autor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\multiplier_calculus_attempts\20260914_192602_618607\run.json`. Comando registrado: `['C:\\Users\\rotol\\.elan\\toolchains\\leanprover--lean4---v4.31.0\\bin\\lake.exe', 'build', 'TGLExt.AuditA1MultiplierCalculus']`. Fonte e objeto autorais abaixo. Reutilização somente de objetos próprios previamente produzidos na raiz isolada; os pacotes externos vêm do cache explicitado no relatório. Não é nova compilação integral da biblioteca.

Revisor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_calculo\independent_20260914_195430_882359\run.json`. `642` objetos próprios anteriores; `0` fornecedores antigos recompilados adicionalmente. Zero objetos do autor/DEV herdados; `0` avisos de alvos/auditor. Avisos de fornecedores e diferenças binárias estão preservados em compilation.json. Comparação indisponível não significa igualdade.

As tentativas de desenvolvimento que falharam permanecem em disco. Só o fonte final, as reproduções rc0 e as auditorias aceitas entram nesta conclusão. Controle negativo de uma aplicação adulterada não é um teorema geral de inexistência.

## Fontes e objetos autorais

| Módulo | SHA256 fonte | SHA256 objeto |
|---|---|---|
| `V351ScalarMultiplierCalculus` | `4dfa6cbd81aa481d695c2eec89985eb06487e7ba32432528d06c62ee7147f06c` | `fa92f73a97fe654b3ee92401218ef18602913f1bdc11df5b0ac5a2144f82c81b` |

## Tipos completos e axiomas

```lean
TGLV350.Regular.compactScalarField {H : Type} [NormedAddCommGroup.{0} H] [InnerProductSpace.{0, 0} ℂ H]
  (g : ℝ → ↑unitInterval) (hg : Continuous.{0, 0} g) (f : ContinuousMap.{0, 0} ↑unitInterval ℂ) :
  TGLV350.StrongIntegral.Family
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.compactScalarRepresentation {H : Type} [NormedAddCommGroup.{0} H] [InnerProductSpace.{0, 0} ℂ H]
  [CompleteSpace.{0} H] (g : ℝ → ↑unitInterval) (hg : Continuous.{0, 0} g) :
  StarAlgHom.{0, 0, 0} ℂ (ContinuousMap.{0, 0} ↑unitInterval ℂ)
    (ContinuousLinearMap.{0, 0, 0, 0} (RingHom.id.{0} ℂ) ↥(TGLV350.Regular.RegularHilbert H)
      ↥(TGLV350.Regular.RegularHilbert H))
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.compactScalarRepresentation_ae {H : Type} [NormedAddCommGroup.{0} H] [InnerProductSpace.{0, 0} ℂ H]
  [CompleteSpace.{0} H] (g : ℝ → ↑unitInterval) (hg : Continuous.{0, 0} g) (f : ContinuousMap.{0, 0} ↑unitInterval ℂ)
  (u : ↥(TGLV350.Regular.RegularHilbert H)) :
  ↑↑(((TGLV350.Regular.compactScalarRepresentation g hg) f) u) =ᵐ[MeasureTheory.volume.{0}] fun x =>
    HSMul.hSMul.{0, 0, 0} (f (g x)) (↑↑u x)
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.compactScalarRepresentation_coordinate {H : Type} [NormedAddCommGroup.{0} H]
  [InnerProductSpace.{0, 0} ℂ H] [CompleteSpace.{0} H] (g : ℝ → ↑unitInterval) (hg : Continuous.{0, 0} g) :
  Eq.{1} ((TGLV350.Regular.compactScalarRepresentation g hg) (ContinuousMap.mk.{0, 0} (fun a => ↑↑a) ⋯))
    (TGLV350.Regular.realScalarMultiplier (fun x => ↑(g x)) ⋯ ⋯ ⋯)
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.realScalarMultiplier_cfc_ae {H : Type} [NormedAddCommGroup.{0} H] [InnerProductSpace.{0, 0} ℂ H]
  [CompleteSpace.{0} H] (g : ℝ → ℝ) (hg : Continuous.{0, 0} g) (h0 : ∀ (x : ℝ), LE.le.{0} 0 (g x))
  (h1 : ∀ (x : ℝ), LE.le.{0} (g x) 1) (f : ℂ → ℂ) (hf : Continuous.{0, 0} f) (u : ↥(TGLV350.Regular.RegularHilbert H)) :
  ↑↑((cfc.{0, 0} f (TGLV350.Regular.realScalarMultiplier g hg h0 h1)) u) =ᵐ[MeasureTheory.volume.{0}] fun x =>
    HSMul.hSMul.{0, 0, 0} (f ↑(g x)) (↑↑u x)
```

Axiomas: propext, Classical.choice, Quot.sound.

## Custódia e limites

- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\AUDITORIA_CALCULO_MULTIPLICADOR_A1B.json` — SHA256 `6d3840d82d8e8ea19e9e1f4835c81a6d384ecf32896d4e87362f0e13ba271c94`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_calculo\REVIEW_A1_MULTIPLIER_CALCULUS_FINAL.json` — SHA256 `c03d6561e316b604831f69f902e371406fab9c25b71884be7867d19556e2aa2f`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_calculo\compilation.json` — SHA256 `d9d909970d267ef260d10d6c2e40ad576eb61f8724cbcb83a00bb5f967dfa089`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\ACEITE_DELTA_CALCULUS.json` — SHA256 `bcd2b2a78d19ea36bf5824194095d474860a3f2a78b5075b643162df23b7c1a0`.

O manifesto e o recibo próprios ligam esta entrega aos arquivos efetivamente lidos. Nenhum monólito canônico foi importado ou executado; nenhum dado experimental, D1, sigma, Atlas ou diário canônico foi alterado.

## Revisão independente integral

# Revisão independente — cálculo funcional do multiplicador

2026-09-14T19:55:56.215280-03:00

**A1_MULTIPLIER_CALCULUS_REVIEW_ACCEPTED__POWERS_AFFILIATION_TRACE_OPEN**

[REAL] Sem P0, P1 ou P2 no delta delimitado. 5 declarações (3 teoremas, 2 definições), relidas integralmente e reproduzidas pelo Lake próprio; #check com universos e #print axioms separados, somente propext/Classical.choice/Quot.sound.

[REAL] Fonte e ficha foram lidas integralmente. compactScalarField usa a família fortemente contínua existente, com cota uniforme ‖f‖ para f contínua no intervalo compacto. compactScalarRepresentation é um homomorfismo complexo unital de álgebras estrela, construído com as leis já existentes de operatorFieldLift; não é uma representação nova do core nem um novo L².

[REAL] A igualdade da coordenada com realScalarMultiplier é provada nos representantes quase em toda parte e depois em L². A continuidade do homomorfismo é justificada pela cota de norma do lift, não assumida. A naturalidade map_cfc e a avaliação pontual no domínio C([0,1],ℂ) dão cfc(f,M_g)u=f(g)u quase em toda parte.

[REAL] As hipóteses são explícitas: H Hilbert complexo completo, g contínua real com 0≤g≤1 e f:ℂ→ℂ globalmente contínua. A imagem de g está contida no intervalo compacto [0,1]; não se exige f limitada em todo ℂ. As instâncias de normalidade dos elementos usadas por CFC são fornecidas pela álgebra de funções e pela positividade do multiplicador, sem hipótese física adicional.

[REAL] A ficha precede o DEV e identifica como consumidor resolventPhaseOperator, que já usa a função amortecida composta com parte real. A representação e o teorema de CFC são uma ponte efetiva para esse consumidor. Os recortes de busca não são promovidos a comparação exaustiva do acervo. O controle autoral de fator 2 é relido e pinado separadamente; não foi reexecutado pela revisão.

[REAL] Execução própria rc0 em 41.62 s. 642 objetos próprios anteriores preservados; 0 fornecedores antigos adicionais precisaram de reprodução de fonte, além dos módulos deste delta e auditor. Zero objetos autorais/de DEV herdados. Os pacotes externos são cache copiado e pinado da revisão própria anterior, sem recompilação nesta chamada; essa herança não é uma nova auditoria integral da biblioteca. 0 avisos de alvo/auditor; 178 mensagens de fornecedores registradas no JSON (inclui mensagens de objetos anteriores). O aviso de cache aesop com alterações locais, quando presente, permanece no stderr.

Pins lidos dos fontes e objetos próprios:

| Módulo | SHA256 fonte | SHA256 .olean próprio | Igual ao cold build autoral disponível |
|---|---|---|---|
| TGLExt.V351ScalarMultiplierCalculus | `4dfa6cbd81aa481d695c2eec89985eb06487e7ba32432528d06c62ee7147f06c` | `fa92f73a97fe654b3ee92401218ef18602913f1bdc11df5b0ac5a2144f82c81b` | True |

Comparações de bytes não são forçadas; objeto autoral ausente é comparação indisponível, não falha formal.

Controles: AUTHOR_CONTROLS_READ_AND_HASH_VERIFIED__TYPE_MISMATCH_NOT_ENVIRONMENT. A execução ou leitura correspondente está discriminada em compilation.json; nenhum controle autoral foi reexecutado por esta revisão.

[OPEN / limites] Aceite separado de três teoremas e duas definições, sem incluir os quatro teoremas posteriores de potências. Não conclui neste módulo identificação das potências com regularUnitary, afiliação, escala dual ou traço. Nenhuma fonte anterior, memória, gate ou programa terminal foi alterado.

Artefatos próprios:

- [run](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_calculo\independent_20260914_195430_882359\run.json>) — SHA256 `ce5c55d2f1b2f2ed9983168204365adc1ba466f927e283087d3a48aad278b351`.
- [compilation](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_calculo\compilation.json>) — SHA256 `d9d909970d267ef260d10d6c2e40ad576eb61f8724cbcb83a00bb5f967dfa089`.
- [tipos/axiomas](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_calculo\independent_20260914_195430_882359\type_axiom_audit.json>) — SHA256 `26950fc9de39ee021310283d87b84b1d632e9fdcb070230931ad484708cb791d`.


## Ficha/adendo integral: REAPROVEITAMENTO_A1B_CALCULO_MULTIPLICADOR

[OPEN — ficha anterior ao cálculo funcional do multiplicador existente]

# A1(b): cálculo funcional no mesmo L²

2026-09-14T19:17:58.427276-03:00

For a continuous scalar g:R->[0,1], use the existing operatorFieldLift to represent C([0,1],C) as bounded operators on RegularHilbert H. Prove this is a unital complex star-algebra homomorphism, equals the existing realScalarMultiplier at the coordinate function, and transports continuous functional calculus. This pays the scalar-multiplier identification needed for resolventPhaseOperator and then regular_unitary_positive_generator. No new L2 space, operator-field machinery or imaginary-power definition.

O homomorfismo tem consumidor concreto: map_cfc e a fase do resolvente. A maquinaria de lift e sua álgebra são reutilizadas, não reprovadas. A busca negativa nos recortes não afirma ausência universal.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350StrongOperatorField.lean:64` — `83fcc9ee4e6cdecee9f130183b7d1e6a0e2436caf40670e4d64dce8933f86a4c`

```lean
def operatorFieldLift (F : StrongIntegral.Family (H := H)) :
    RegularHilbert H →L[ℂ] RegularHilbert H
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350StrongOperatorField.lean:68` — `83fcc9ee4e6cdecee9f130183b7d1e6a0e2436caf40670e4d64dce8933f86a4c`

```lean
theorem operatorFieldLift_ae (F : StrongIntegral.Family (H := H)) (f : RegularHilbert H) :
    operatorFieldLift F f =ᵐ[volume] fun x : ℝ => F.op x (f x)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350OperatorFieldAlgebra.lean:12` — `ccd8bfa143d144167dfe9e395b1c9edd0472cc4f73d94f0d7b32e079b8bb8b2d`

```lean
theorem operatorFieldLift_constant (F : StrongIntegral.Family (H := H))
    (T : H →L[ℂ] H) (h : ∀ x, F.op x = T) :
    operatorFieldLift F = fibre T
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350OperatorFieldAlgebra.lean:20` — `ccd8bfa143d144167dfe9e395b1c9edd0472cc4f73d94f0d7b32e079b8bb8b2d`

```lean
theorem operatorFieldLift_add (F G K : StrongIntegral.Family (H := H))
    (h : ∀ x, K.op x = F.op x + G.op x) :
    operatorFieldLift K = operatorFieldLift F + operatorFieldLift G
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350OperatorFieldAlgebra.lean:33` — `ccd8bfa143d144167dfe9e395b1c9edd0472cc4f73d94f0d7b32e079b8bb8b2d`

```lean
theorem operatorFieldLift_mul (F G K : StrongIntegral.Family (H := H))
    (h : ∀ x, K.op x = F.op x * G.op x) :
    operatorFieldLift K = operatorFieldLift F * operatorFieldLift G
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350OperatorFieldAlgebra.lean:57` — `ccd8bfa143d144167dfe9e395b1c9edd0472cc4f73d94f0d7b32e079b8bb8b2d`

```lean
theorem operatorFieldLift_star (F G : StrongIntegral.Family (H := H))
    (h : ∀ x, G.op x = star (F.op x)) :
    operatorFieldLift G = star (operatorFieldLift F)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350L2PositiveMultiplier.lean:25` — `6e3946aff9964e1a6a59a8dcb99a11b4a3c0026a6b0220f7df4b9901f83f3bdf`

```lean
def realScalarMultiplier (g : ℝ → ℝ) (hg : Continuous g)
    (h0 : ∀ s, 0 ≤ g s) (h1 : ∀ s, g s ≤ 1) :
    RegularHilbert H →L[ℂ] RegularHilbert H
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ResolventPhaseCalculus.lean:15` — `cd207e3a21c50f65fe3b199e201b2b148a0d98fc2e3a3cf7e40a80e61ba4f818`

```lean
def resolventPhaseOperator (T : H →L[ℂ] H) (t : ℝ) : H →L[ℂ] H
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ResolventImaginaryPowers.lean:45` — `0cfc297376410ff6bd259eeaf921a9d6e6ca47829b5d389c6b5c30bf4c5accf5`

```lean
theorem resolventImaginaryPower_damping (t : ℝ) (x : H) :
    resolventImaginaryPower T hT h1 hi hj t (resolventDampingOperator T x)=
      resolventPhaseOperator T t x
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\CStarAlgebra\ContinuousFunctionalCalculus\Unique.lean:486` — `d7103470f12927eb549967928bc1a6bc6e81ba8727997eee113239772ba2e6c1`

```lean
lemma StarAlgHom.map_cfc (φ : A →⋆ₐ[S] B) (f : R → R) (a : A)
    (hf : ContinuousOn f (spectrum R a) := by cfc_cont_tac) (hφ : Continuous φ := by fun_prop)
    (ha : p a := by cfc_tac) (hφa : q (φ a) := by cfc_tac) :
    φ (cfc f a) = cfc f (φ a)
```

Seis modalidades e outras bancadas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_multiplier_calculus\20260914_191706_280714\searches.json.
