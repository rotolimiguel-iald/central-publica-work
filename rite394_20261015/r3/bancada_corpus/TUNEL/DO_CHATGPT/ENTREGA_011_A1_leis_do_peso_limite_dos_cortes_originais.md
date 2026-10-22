[REAL — 13 teoremas e 2 definições verificados no delta por reprodução isolada autoral e revisão independente. A1(b): traço concreto ainda OPEN.]

# ENTREGA 011 / A1 — O peso limite dos cortes originais é aditivo, homogêneo, monótono e normal

2026-09-14T22:51:56.628998-03:00

Dois objetos definidos no cone positivo existente: scalarInverseCutoffWeight avalia o dualQuadraticIntegral original após conjugação pela raiz do corte original; scalarInverseLimitWeight é o supremo da sequência ε_n=1/(n+1). Treze teoremas, sem auxiliares privados: leis de zero, soma, homogeneidade NNReal, monotonia no input, normalidade em supremos positivos dirigidos, antitonia nos reguladores positivos, monotonia da sequência e dominação de cada corte. A normalidade é obtida de limites fortes internos já construídos; a soma do limite usa monotonia no mesmo índice, e os valores podem ser infinitos.

Essas leis não implicam fidelidade, semifinitude, tracialidade ou escala dual do limite. Não há habitante de RegularCoreTraceData nesta entrega. Não se instala inversibilidade do conjugador nem se afirma que pertencer ao cone torna o peso finito. Os reguladores são matemáticos, sem novo acoplamento físico ou alteração do gate.

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

Autor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\inverse_limit_weight_attempts\20260914_223753_531727\run.json`. Comando registrado: `['C:\\Users\\rotol\\.elan\\toolchains\\leanprover--lean4---v4.31.0\\bin\\lake.exe', 'build', 'TGLExt.AuditA1InverseLimitWeight']`. Fonte e objeto autorais abaixo. Reutilização somente de objetos próprios previamente produzidos na raiz isolada; os pacotes externos vêm do cache explicitado no relatório. Não é nova compilação integral da biblioteca.

Revisor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_leis_peso_limite\independent_20260914_224354_013292\run.json`. `680` objetos próprios anteriores; `0` fornecedores antigos recompilados adicionalmente. Zero objetos do autor/DEV herdados; `0` avisos de alvos/auditor. Avisos de fornecedores e diferenças binárias estão preservados em compilation.json. Comparação indisponível não significa igualdade.

As tentativas de desenvolvimento que falharam permanecem em disco. Só o fonte final, as reproduções rc0 e as auditorias aceitas entram nesta conclusão. Controle negativo de uma aplicação adulterada não é um teorema geral de inexistência.

## Fontes e objetos autorais

| Módulo | SHA256 fonte | SHA256 objeto |
|---|---|---|
| `V351InverseLimitWeight` | `cfdced33d3cafdd2782f4d7e8ca77974e0ddee22f19803dfbd36275787c28f1e` | `9ec83875d0e3314d78d2f0cc23fe22fc6d572a573561f3fddfd9a9e8f918aecf` |

## Tipos completos e axiomas

```lean
TGLV350.Regular.scalarInverseCutoffWeight (P : TGLExt.SiteProfile) (ε : ℝ) (X : TGLV350.Regular.PositiveCoreInput P) :
  ENNReal
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.scalarInverseCutoffWeight_zero (P : TGLExt.SiteProfile) (ε : ℝ) :
  Eq.{1} (TGLV350.Regular.scalarInverseCutoffWeight P ε (TGLV350.Regular.PositiveCoreInput.zero P)) 0
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.scalarInverseCutoffWeight_add (P : TGLExt.SiteProfile) (ε : ℝ)
  (X Y : TGLV350.Regular.PositiveCoreInput P) :
  Eq.{1} (TGLV350.Regular.scalarInverseCutoffWeight P ε (X.add Y))
    (HAdd.hAdd.{0, 0, 0} (TGLV350.Regular.scalarInverseCutoffWeight P ε X)
      (TGLV350.Regular.scalarInverseCutoffWeight P ε Y))
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.scalarInverseCutoffWeight_scale (P : TGLExt.SiteProfile) (ε : ℝ) (r : NNReal)
  (X : TGLV350.Regular.PositiveCoreInput P) :
  Eq.{1} (TGLV350.Regular.scalarInverseCutoffWeight P ε (TGLV350.Regular.PositiveCoreInput.scale r X))
    (HMul.hMul.{0, 0, 0} (↑r) (TGLV350.Regular.scalarInverseCutoffWeight P ε X))
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.scalarInverseCutoffWeight_mono (P : TGLExt.SiteProfile) (ε : ℝ)
  (X Y : TGLV350.Regular.PositiveCoreInput P) (hXY : LE.le.{0} X Y) :
  LE.le.{0} (TGLV350.Regular.scalarInverseCutoffWeight P ε X) (TGLV350.Regular.scalarInverseCutoffWeight P ε Y)
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.scalarInverseCutoffWeight_normal.{u_1} (P : TGLExt.SiteProfile) (ε : ℝ) {ι : Type u_1}
  [Preorder.{u_1} ι] [IsDirectedOrder.{u_1} ι] [Nonempty.{u_1 + 1} ι]
  (A : ι → ↥(VonNeumannAlgebra.toStarSubalgebra.{0} (TGLV350.Regular.regularCoreAlgebra P)))
  (S : ↥(VonNeumannAlgebra.toStarSubalgebra.{0} (TGLV350.Regular.regularCoreAlgebra P)))
  (hpos : ∀ (i : ι), LE.le.{0} 0 (A i)) (hmono : Monotone.{u_1, 0} A) (hS : IsLUB.{0} (Set.range.{0, u_1 + 1} A) S) :
  Eq.{1} (TGLV350.Regular.scalarInverseCutoffWeight P ε (Subtype.mk.{1} ↑S ⋯))
    (⨆ i, TGLV350.Regular.scalarInverseCutoffWeight P ε (Subtype.mk.{1} ↑(A i) ⋯))
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.scalarInverseCutoffWeight_antitone (P : TGLExt.SiteProfile) (ε η : ℝ) (hε : LT.lt.{0} 0 ε)
  (hη : LT.lt.{0} 0 η) (hεη : LE.le.{0} ε η) (X : TGLV350.Regular.PositiveCoreInput P) :
  LE.le.{0} (TGLV350.Regular.scalarInverseCutoffWeight P η X) (TGLV350.Regular.scalarInverseCutoffWeight P ε X)
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.scalarInverseCutoffWeight_sequence_mono (P : TGLExt.SiteProfile)
  (X : TGLV350.Regular.PositiveCoreInput P) :
  Monotone.{0, 0} fun n =>
    TGLV350.Regular.scalarInverseCutoffWeight P (HDiv.hDiv.{0, 0, 0} 1 (HAdd.hAdd.{0, 0, 0} (↑n) 1)) X
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.scalarInverseLimitWeight (P : TGLExt.SiteProfile) (X : TGLV350.Regular.PositiveCoreInput P) : ENNReal
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.scalarInverseLimitWeight_zero (P : TGLExt.SiteProfile) :
  Eq.{1} (TGLV350.Regular.scalarInverseLimitWeight P (TGLV350.Regular.PositiveCoreInput.zero P)) 0
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.scalarInverseCutoffWeight_le_limit (P : TGLExt.SiteProfile) (n : ℕ)
  (X : TGLV350.Regular.PositiveCoreInput P) :
  LE.le.{0} (TGLV350.Regular.scalarInverseCutoffWeight P (HDiv.hDiv.{0, 0, 0} 1 (HAdd.hAdd.{0, 0, 0} (↑n) 1)) X)
    (TGLV350.Regular.scalarInverseLimitWeight P X)
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.scalarInverseLimitWeight_add (P : TGLExt.SiteProfile) (X Y : TGLV350.Regular.PositiveCoreInput P) :
  Eq.{1} (TGLV350.Regular.scalarInverseLimitWeight P (X.add Y))
    (HAdd.hAdd.{0, 0, 0} (TGLV350.Regular.scalarInverseLimitWeight P X) (TGLV350.Regular.scalarInverseLimitWeight P Y))
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.scalarInverseLimitWeight_scale (P : TGLExt.SiteProfile) (r : NNReal)
  (X : TGLV350.Regular.PositiveCoreInput P) :
  Eq.{1} (TGLV350.Regular.scalarInverseLimitWeight P (TGLV350.Regular.PositiveCoreInput.scale r X))
    (HMul.hMul.{0, 0, 0} (↑r) (TGLV350.Regular.scalarInverseLimitWeight P X))
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.scalarInverseLimitWeight_mono (P : TGLExt.SiteProfile) (X Y : TGLV350.Regular.PositiveCoreInput P)
  (hXY : LE.le.{0} X Y) :
  LE.le.{0} (TGLV350.Regular.scalarInverseLimitWeight P X) (TGLV350.Regular.scalarInverseLimitWeight P Y)
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.scalarInverseLimitWeight_normal.{u_1} (P : TGLExt.SiteProfile) {ι : Type u_1} [Preorder.{u_1} ι]
  [IsDirectedOrder.{u_1} ι] [Nonempty.{u_1 + 1} ι]
  (A : ι → ↥(VonNeumannAlgebra.toStarSubalgebra.{0} (TGLV350.Regular.regularCoreAlgebra P)))
  (S : ↥(VonNeumannAlgebra.toStarSubalgebra.{0} (TGLV350.Regular.regularCoreAlgebra P)))
  (hpos : ∀ (i : ι), LE.le.{0} 0 (A i)) (hmono : Monotone.{u_1, 0} A) (hS : IsLUB.{0} (Set.range.{0, u_1 + 1} A) S) :
  Eq.{1} (TGLV350.Regular.scalarInverseLimitWeight P (Subtype.mk.{1} ↑S ⋯))
    (⨆ i, TGLV350.Regular.scalarInverseLimitWeight P (Subtype.mk.{1} ↑(A i) ⋯))
```

Axiomas: propext, Classical.choice, Quot.sound.

## Custódia e limites

- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\AUDITORIA_LEIS_PESO_LIMITE_A1B.json` — SHA256 `8ab173581b511fd6e63bd4e3f0fdc1b455c89aa7c0abaac2e45d65e612417523`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_leis_peso_limite\REVIEW_A1_INVERSE_LIMIT_WEIGHT_FINAL.json` — SHA256 `48d510be3ceb613923c74b285bc71f52d9db8a2ceab15a648191d266009d7e24`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_leis_peso_limite\compilation.json` — SHA256 `f6cd83f17218d3876bf6e703a614933979d6b7d25d11cff2cc3cf9589b6776c7`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\ACEITE_DELTA_INVERSE_LIMIT_WEIGHT.json` — SHA256 `28a2f6eb5815eec7c633b65a75b51b2ba1b449c8715bcd47d87043542d228b99`.

O manifesto e o recibo próprios ligam esta entrega aos arquivos efetivamente lidos. Nenhum monólito canônico foi importado ou executado; nenhum dado experimental, D1, sigma, Atlas ou diário canônico foi alterado.

## Revisão independente integral

# Revisão independente — leis do peso limite

2026-09-14T22:46:05.542271-03:00

**A1_INVERSE_LIMIT_WEIGHT_REVIEW_ACCEPTED__FAITHFUL_SEMIFINITE_TRACIAL_SCALING_OPEN**

[REAL] **Sem achados P0/P1/P2.** Treze teoremas públicos + duas definições, zero privados. Módulo completo e auditor próprios rc0; quinze #check com universos e axiomas exclusivamente do trio permitido. Aceite delimitado ao enunciado efetivamente compilado.

[REAL — objetos e domínio] As duas definições usam o mesmo PositiveCoreInput P, hilbertPositiveSqrt(Bε), dualQuadraticIntegral e regularVacuum P. Wε(X)=ν(sε* X sε) e o candidato limite é sup_n W_(1/(n+1))(X). O domínio é o cone positivo limitado do core; não exige finitude do valor. A expressão é definida para todo ε real, mas a interpretação como corte inverso positivo e a ordem entre reguladores usam ε>0. Não se afirma que os cortes são fixos pela ação dual; PositiveCoreInput.conjugate, restrito ao core fixo, não é aplicado indevidamente.

[REAL — leis dos cortes] Zero, aditividade, homogeneidade por r:NNReal e monotonia em X são transportadas das leis integrais existentes. A positividade de star b X b e a ordem sob conjugador FIXO vêm das leis de estrela. Não se deduz ordem de sanduíches a partir da ordem de conjugadores. Todos os valores são ENNReal; não se elimina infinito nem se divide por um valor de peso.

[REAL — normalidade] Para qualquer universo do índice ι, com Preorder, IsDirectedOrder e Nonempty, A é uma rede crescente de positivos no core e S seu supremo INTERNO limitado. A cota ||A_i||≤||S|| é deduzida. vonNeumann_exists_positive_isLUB constrói um limite forte D no core; unicidade do supremo dá D=S. A continuidade do CLM star b produz o limite forte dos sanduíches em todos os vetores, que alimenta a normalidade integral antiga. Não se recebe continuidade forte como premissa nem se pressupõe que conjugação preserve supremos internos.

[REAL — limite comum] A antitonia em ε é o alvo já entregue do módulo21. Para n≤m, 1/(m+1)≤1/(n+1), logo as avaliações crescem. ENNReal.iSup_add_iSup_of_monotone é usado nas DUAS famílias com o mesmo índice natural; não se aplica a igualdade falsa entre soma de supremos e supremo diagonal para famílias arbitrárias. Homogeneidade usa mul_iSup (inclusive zero e infinito), monotonia usa le_iSup no mesmo índice. A normalidade final troca os supremos n/i por iSup_comm, após a normalidade de cada corte. Não é argumento de convergência sequencial que restrinja a rede A a índices contáveis.

[REAL — documentos e evidências] Ficha 22:30:29 e adendo 22:31:48 foram lidos integralmente antes da conclusão desta revisão; ambos precedem o primeiro DEV 22:33:31. Nove fornecedores mais cinco do adendo foram confrontados com suas fontes, linhas, tipos, hashes e cópias próprias. Módulo e auditor independentes passaram; os 15 tipos com universos e respectivos axiomas foram lidos e reparsados. Não há helpers privados, sorry, axioma novo, native_decide ou trustCompiler.

[REAL — histórico e negativo] Duas tentativas autorais rc1 (22:33:31 e 22:35:54) ficam excluídas, mesmo que tenham prints parciais. Seus pins apontam a snapshots históricos reais, nunca à fonte viva. A final 22:36:37 está rc0. O negativo autoral substitui a soma por produto na conclusão de scalarInverseLimitWeight_add e é recusado por Type mismatch, com imports resolvidos. Fonte e streams desse controle foram relidos e pinados; nenhum controle autoral foi executado nesta revisão.

[REAL — proveniência] 680 objetos próprios anteriores preservados; somente módulo e auditor novos, total 682. Zero fornecedor antigo recompilado; cache de pacotes pinado e herdado, sem nova auditoria integral da biblioteca. LEAN_PATH dos traces contém somente V e seus pacotes, nenhum build autoral ou DEV. Run próprio rc0 em 37.249 s; zero avisos do alvo/auditor e 178 mensagens históricas de fornecedores separadas no JSON. O stderr preserva ainda o aviso do cache aesop com alterações locais, já presente na base; não é aviso do alvo. A contagem total de jobs do Lake não significa recompilação dessa quantidade de objetos.

| Artefato | SHA256 lido |
|---|---|
| Fonte final (K=cópia própria) | cfdced33d3cafdd2782f4d7e8ca77974e0ddee22f19803dfbd36275787c28f1e |
| .olean próprio | 9ec83875d0e3314d78d2f0cc23fe22fc6d572a573561f3fddfd9a9e8f918aecf |
| .olean autoral standalone, apenas comparação | 9ec83875d0e3314d78d2f0cc23fe22fc6d572a573561f3fddfd9a9e8f918aecf |

Igualdade binária medida: True.

[OPEN — limites] Aceite exclusivo de 15 declarações: 13 teoremas e duas definições, zero privados. Normalidade provada para redes positivas crescentes, dirigidas e não vazias, com supremo interno no core; não afirma completude do cone de afiliados nem cobertura de todo predual. Fidelidade, semifinitude, tracialidade e escala dual deste peso limite permanecem OPEN neste delta. A consulta anterior é proposta independente, não prova Lean desses campos. Nenhum novo GNS, gap, minorantes positivos finitos de ν ou promoção de A1(b)/gate. O módulo23 é separado e não está aceito por este relatório. Reuso apenas de objetos próprios anteriores e cache de pacotes pinado. Nenhum objeto autoral/DEV, monólito, recorder, writer ou memória executado/modificado.

Artefatos de evidência:

- [compilation](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_leis_peso_limite\compilation.json>) — SHA256 f6cd83f17218d3876bf6e703a614933979d6b7d25d11cff2cc3cf9589b6776c7.
- [run próprio](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_leis_peso_limite\independent_20260914_224354_013292\run.json>) — SHA256 dd5e804970a5dfff7fe57332ec0379a0c938f7e94813fbdae75ee85d13dd41ee.
- [tipos/axiomas](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_leis_peso_limite\independent_20260914_224354_013292\type_axiom_audit.json>) — SHA256 e5d0bcc95cbd216dc9e929d06c7cd645289046c8ad50e62f38e7490c031db83d.
- [histórico](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_leis_peso_limite\history_read.json>) — SHA256 849f895602d8a079a2e7c98a5222dc1ebf4b32d306a7e518447ca1cd694972a9.
- [fornecedores da ficha](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_leis_peso_limite\provider_checks.json>) — SHA256 b7a278164a1016fb2b377f96e858067574dab79ab8a782845caf4bd5b7a58daa.


## Ficha/adendo integral: REAPROVEITAMENTO_A1B_LEIS_PESO_LIMITE

[OPEN — ficha anterior às leis do peso limite]

# A1(b): o peso limite pelos cortes já construídos

2026-09-14T22:30:29.369753-03:00

Define scalarInverseCutoffWeight P epsilon on the EXISTING PositiveCoreInput as nu(star sqrt(B_epsilon) X sqrt(B_epsilon)). Prove zero, addition, NNReal homogeneity, input monotonicity and normality for internal positive directed suprema, using the old strong operator limit and old normality of dualQuadraticIntegral. Read scalarWeight_inverseCutoff_antitone as regulator order, and prove the natural-number sequence epsilon_n=1/(n+1) gives monotone weights. Define scalarInverseLimitWeight as that SAME sequence supremum; prove zero/add/homogeneous/monotone/normal and domination of each sequence cutoff. All values ENNReal, no finiteness premise. No separate GNS, trace structure inhabitant, final semifinitude, faithfulness, traciality or dual scaling claimed by these laws. Explicit two definitions are consumers of already constructed cutoffs and of the final RegularCoreTraceData value field. Existing PositiveCoreInput.conjugate is NOT usable directly: requires dualFixedCore; use raw integral laws without asserting that cuts are theta-fixed.

ADAPTAR: leis integrais e supremos existentes; não criar outro espaço de estados. A normalidade do sanduíche segue por limite forte de redes positivas, não por presumir que uma conjugação não invertível preserva qualquer supremo. Fornecedores ENNReal serão registrados em adendo antes do alvo.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegulatorWeightOrder.lean:66` — `b908f79a4d20ca8f456eb245e2a605a6cc6e611667e1c8a8d6cb1cee2ee4f838`

```lean
theorem scalarWeight_inverseCutoff_antitone (P : SiteProfile)
    (ε η : ℝ) (hε : 0 < ε) (hη : 0 < η) (hεη : ε ≤ η)
    (X : PositiveCoreInput P) :
    dualQuadraticIntegral
      (star (hilbertPositiveSqrt (regularInverseGeneratorCutoff P η)) * X.val *
        hilbertPositiveSqrt (regularInverseGeneratorCutoff P η)) (regularVacuum P) ≤
    dualQuadraticIntegral
      (star (hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε)) * X.val *
        hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε)) (regularVacuum P)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350DualWeightForm.lean:66` — `3a233c43934c915774c68c23f0fca752d1c9dfc95679178c714394fe666a24b4`

```lean
theorem dualQuadraticIntegral_zero (v : RegularHilbert H) :
    dualQuadraticIntegral (0 : RegularHilbert H →L[ℂ] RegularHilbert H) v = 0
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350DualWeightForm.lean:74` — `3a233c43934c915774c68c23f0fca752d1c9dfc95679178c714394fe666a24b4`

```lean
theorem dualQuadraticIntegral_add
    (A B : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) (hB : 0 ≤ B)
    (v : RegularHilbert H) :
    dualQuadraticIntegral (A+B) v = dualQuadraticIntegral A v + dualQuadraticIntegral B v
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350DualQuadraticLaws.lean:61` — `7085d5ad460720e87ea5e1e3cc8bcbf5b55193be77b2ba283988fbf03120c1f3`

```lean
theorem dualQuadraticIntegral_smul_operator (r : ℝ) (hr : 0 ≤ r)
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (v : RegularHilbert H) :
    dualQuadraticIntegral (r • A) v = ENNReal.ofReal r * dualQuadraticIntegral A v
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350DualFormFaithfulness.lean:79` — `6fca7648f9345bd4e83ed364bc0f551d587b99651b1c7c86574b1d0b090bea83`

```lean
theorem dualQuadraticIntegral_mono
    (A B : RegularHilbert H →L[ℂ] RegularHilbert H) (hAB : A ≤ B)
    (v : RegularHilbert H) : dualQuadraticIntegral A v ≤ dualQuadraticIntegral B v
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350DualFormNormality.lean:18` — `feace23e31954e69de8103646211acd6d59a1b859e3b9ec109c142b1c994fdaa`

```lean
theorem dualQuadraticIntegral_of_monotone_strong_limit
    (A : ι → RegularHilbert H →L[ℂ] RegularHilbert H)
    (S : RegularHilbert H →L[ℂ] RegularHilbert H)
    (hpos : ∀ i, 0 ≤ A i) (hmono : Monotone A)
    (hlim : ∀ v, Tendsto (fun i => A i v) atTop (𝓝 (S v)))
    (v : RegularHilbert H) :
    dualQuadraticIntegral S v = ⨆ i, dualQuadraticIntegral (A i) v
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350RegularNormality.lean:52` — `bcd49e92800bf99d7770bb9969879be02a9768f129ce842ae2f39cefaca3cc0a`

```lean
theorem vonNeumann_exists_positive_isLUB (N : VonNeumannAlgebra H)
    {ι : Type*} [Preorder ι] [IsDirectedOrder ι] [Nonempty ι]
    (T : ι → N.toStarSubalgebra) (hpos : ∀ i, 0 ≤ T i) (hmono : Monotone T)
    (C : ℝ) (hC : 0 ≤ C) (hbound : ∀ i, ‖(T i : H →L[ℂ] H)‖ ≤ C) :
    ∃ B : N.toStarSubalgebra, 0 ≤ B ∧ ‖(B : H →L[ℂ] H)‖ ≤ C ∧
      (∀ v, Tendsto (fun i => (T i : H →L[ℂ] H) v) atTop
        (𝓝 ((B : H →L[ℂ] H) v))) ∧
      IsLUB (Set.range (fun i => (T i : H →L[ℂ] H))) (B : H →L[ℂ] H) ∧
      IsLUB (Set.range T) B
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350DualFixedWeightLaws.lean:38` — `93fda2f3b9a2c519d13e1356de7fcebd2f273d3d0078eeac6d505af795ae9c75`

```lean
def PositiveCoreInput.conjugate {P : TGLExt.SiteProfile}
    (A : PositiveCoreInput P)
    (B : (dualFixedCore P).toStarSubalgebra) : PositiveCoreInput P
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350DualFixedWeightLaws.lean:118` — `93fda2f3b9a2c519d13e1356de7fcebd2f273d3d0078eeac6d505af795ae9c75`

```lean
theorem positive_internal_isLUB_nonneg (P : TGLExt.SiteProfile)
    (A : ι → (regularCoreAlgebra P).toStarSubalgebra)
    (S : (regularCoreAlgebra P).toStarSubalgebra)
    (hpos : ∀ i, 0 ≤ A i) (hS : IsLUB (Set.range A) S) : 0 ≤ S
```

Seis modalidades e outras bancadas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_limit_weight\20260914_223003_335432\searches.json. Ausência nominal nos recortes não é ausência universal.


## Ficha/adendo integral: ADENDO_FICHA_PESO_LIMITE_SUPREMOS

[OPEN — fornecedores antes do código]

2026-09-14T22:31:48.401781-03:00

A ordem de conjugação refere-se ao input X com conjugador fixo; não compara conjugadores ordenados. A soma de supremos usa MONOTONIA no mesmo índice natural (fornecedor ENNReal), evitando a igualdade falsa para duas famílias arbitrárias não dirigidas conjuntamente. Homogeneidade usa mul_iSup, inclusive nos valores infinitos. Normalidade do limite é troca de supremos do peso construído. Nenhuma lei deste delta implica tracialidade ou semifinitude.

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Algebra\Order\Star\Basic.lean:214

```lean
theorem star_left_conjugate_nonneg {a : R} (ha : 0 ≤ a) (c : R) : 0 ≤ star c * a * c
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Algebra\Order\Star\Basic.lean:239

```lean
theorem star_left_conjugate_le_conjugate {a b : R} (hab : a ≤ b) (c : R) :
    star c * a * c ≤ star c * b * c
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Algebra\Order\Field\Basic.lean:69

```lean
theorem one_div_le_one_div_of_le (ha : 0 < a) (h : a ≤ b) : 1 / b ≤ 1 / a
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Data\ENNReal\Operations.lean:686

```lean
lemma iSup_add_iSup_of_monotone {ι : Type*} [Preorder ι] [IsDirectedOrder ι] {f g : ι → ℝ≥0∞}
    (hf : Monotone f) (hg : Monotone g) : iSup f + iSup g = ⨆ a, f a + g a
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Data\ENNReal\Inv.lean:807

```lean
lemma mul_iSup (a : ℝ≥0∞) (f : ι → ℝ≥0∞) : a * ⨆ i, f i = ⨆ i, a * f i
```

