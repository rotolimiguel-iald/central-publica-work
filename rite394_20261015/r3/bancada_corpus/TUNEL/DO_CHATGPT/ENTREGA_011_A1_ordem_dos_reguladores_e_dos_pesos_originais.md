[REAL — 4 teoremas e 0 definições verificados no delta por reprodução isolada autoral e revisão independente. A1(b): traço concreto ainda OPEN.]

# ENTREGA 011 / A1 — A redução do regulador aumenta os cortes e seus pesos

2026-09-14T22:34:24.301625-03:00

Quatro teoremas públicos e dois auxiliares privados, zero definições. Os cortes originais comutam por serem CFC do mesmo R. A identidade Bε−Bη=(η−ε)BηBε é provada pelo grafo original; a positividade do produto comutante implica Bη≤Bε para 0<ε≤η. A comparação dos pesos vale para todo positivo limitado X no core, incluindo valores infinitos, com pertença das raízes na álgebra direita e comutação com as médias descarregadas pelos fornecedores. A identidade resolvente também será consumida nos produtos dos cortes do domínio finito do limite.

Não cobre ε=0 nem operadores positivos afiliados não limitados. Não compara os sanduíches em ordem de operadores; compara suas avaliações pelo peso. O peso limite e suas propriedades de traço são obrigações seguintes. Não há novo gerador, parâmetro físico, monólito ou mudança de gate.

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

Autor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\regulator_weight_order_attempts\20260914_222729_943495\run.json`. Comando registrado: `['C:\\Users\\rotol\\.elan\\toolchains\\leanprover--lean4---v4.31.0\\bin\\lake.exe', 'build', 'TGLExt.AuditA1RegulatorWeightOrder']`. Fonte e objeto autorais abaixo. Reutilização somente de objetos próprios previamente produzidos na raiz isolada; os pacotes externos vêm do cache explicitado no relatório. Não é nova compilação integral da biblioteca.

Revisor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_ordem_reguladores\independent_20260914_222944_958643\run.json`. `678` objetos próprios anteriores; `0` fornecedores antigos recompilados adicionalmente. Zero objetos do autor/DEV herdados; `0` avisos de alvos/auditor. Avisos de fornecedores e diferenças binárias estão preservados em compilation.json. Comparação indisponível não significa igualdade.

As tentativas de desenvolvimento que falharam permanecem em disco. Só o fonte final, as reproduções rc0 e as auditorias aceitas entram nesta conclusão. Controle negativo de uma aplicação adulterada não é um teorema geral de inexistência.

## Fontes e objetos autorais

| Módulo | SHA256 fonte | SHA256 objeto |
|---|---|---|
| `V351RegulatorWeightOrder` | `b908f79a4d20ca8f456eb245e2a605a6cc6e611667e1c8a8d6cb1cee2ee4f838` | `dffb577a426a8156f48a671ba92401a912208c3053c5a2b5c4c8f2d326863fff` |

## Tipos completos e axiomas

```lean
TGLV350.Regular.regularInverseGeneratorCutoff_commutes (P : TGLExt.SiteProfile) (ε η : ℝ) (hε : LT.lt.{0} 0 ε)
  (hη : LT.lt.{0} 0 η) :
  Commute.{0} (TGLV350.Regular.regularInverseGeneratorCutoff P ε) (TGLV350.Regular.regularInverseGeneratorCutoff P η)
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.regularInverseGeneratorCutoff_resolvent_identity (P : TGLExt.SiteProfile) (ε η : ℝ) (hε : LT.lt.{0} 0 ε)
  (hη : LT.lt.{0} 0 η) :
  Eq.{1}
    (HSub.hSub.{0, 0, 0} (TGLV350.Regular.regularInverseGeneratorCutoff P ε)
      (TGLV350.Regular.regularInverseGeneratorCutoff P η))
    (HSMul.hSMul.{0, 0, 0} (↑(HSub.hSub.{0, 0, 0} η ε))
      (HMul.hMul.{0, 0, 0} (TGLV350.Regular.regularInverseGeneratorCutoff P η)
        (TGLV350.Regular.regularInverseGeneratorCutoff P ε)))
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.regularInverseGeneratorCutoff_antitone (P : TGLExt.SiteProfile) (ε η : ℝ) (hε : LT.lt.{0} 0 ε)
  (hη : LT.lt.{0} 0 η) (hεη : LE.le.{0} ε η) :
  LE.le.{0} (TGLV350.Regular.regularInverseGeneratorCutoff P η) (TGLV350.Regular.regularInverseGeneratorCutoff P ε)
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.scalarWeight_inverseCutoff_antitone (P : TGLExt.SiteProfile) (ε η : ℝ) (hε : LT.lt.{0} 0 ε)
  (hη : LT.lt.{0} 0 η) (hεη : LE.le.{0} ε η) (X : TGLV350.Regular.PositiveCoreInput P) :
  LE.le.{0}
    (TGLV350.Regular.dualQuadraticIntegral
      (HMul.hMul.{0, 0, 0}
        (HMul.hMul.{0, 0, 0}
          (star.{0} (TGLV350.Regular.hilbertPositiveSqrt (TGLV350.Regular.regularInverseGeneratorCutoff P η))) ↑X)
        (TGLV350.Regular.hilbertPositiveSqrt (TGLV350.Regular.regularInverseGeneratorCutoff P η)))
      (TGLV350.Regular.regularVacuum P))
    (TGLV350.Regular.dualQuadraticIntegral
      (HMul.hMul.{0, 0, 0}
        (HMul.hMul.{0, 0, 0}
          (star.{0} (TGLV350.Regular.hilbertPositiveSqrt (TGLV350.Regular.regularInverseGeneratorCutoff P ε))) ↑X)
        (TGLV350.Regular.hilbertPositiveSqrt (TGLV350.Regular.regularInverseGeneratorCutoff P ε)))
      (TGLV350.Regular.regularVacuum P))
```

Axiomas: propext, Classical.choice, Quot.sound.

## Custódia e limites

- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\AUDITORIA_ORDEM_REGULADORES_A1B.json` — SHA256 `64964244befbc7418898f11a845aaf5ebb9d149c0ae045307c33bcc27b0bb648`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_ordem_reguladores\REVIEW_A1_REGULATOR_WEIGHT_ORDER_FINAL.json` — SHA256 `061ade2a30c2f315cda66e0447a76ebbe023267b695620bf9d6f4aa8c5c9e672`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_ordem_reguladores\compilation.json` — SHA256 `94d8f48a968dc984c5263b0ada838f4cc0e80d4d967fdea88a4296b120e1c099`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\ACEITE_DELTA_REGULATOR_WEIGHT_ORDER.json` — SHA256 `fcc1a71c9a658b402e4e8a1089d558d403e43229fa92ad958edffb73de9426dd`.

O manifesto e o recibo próprios ligam esta entrega aos arquivos efetivamente lidos. Nenhum monólito canônico foi importado ou executado; nenhum dado experimental, D1, sigma, Atlas ou diário canônico foi alterado.

## Revisão independente integral

# Revisão independente — ordem dos reguladores e dos pesos

2026-09-14T22:32:16.956572-03:00

**A1_REGULATOR_WEIGHT_ORDER_REVIEW_ACCEPTED__LIMIT_WEIGHT_TRACE_OPEN**

[REAL] **Sem achados P0/P1/P2.** Quatro teoremas públicos + dois helpers privados, zero definições. Módulo completo e auditor próprios rc0; quatro #check com universos e axiomas exclusivamente do trio permitido. Aceite delimitado ao enunciado efetivamente compilado.

[REAL — objetos e comutação] Quatro teoremas públicos e dois helpers privados, zero definições. A identificação já paga Bε=cfc(Fε)(R), com ε>0, é usada para os DOIS cortes do MESMO regularSpectralResolvent P. cfc_commute_cfc fornece comutação de funções desse único operador. Não há outro h, inverso, raiz, realização espectral ou hipótese de comutação recebida pelo novo teorema.

[REAL — identidade e domínio] Para todo vetor x do Hilbert regular, graph coloca (Bεx,x−εBεx) no grafo do mesmo regularPositiveGenerator P. graph_iff com η implica Bη(x−εBεx+ηBεx)=Bεx. Linearidade, extensionalidade e abel dão exatamente Bε−Bη=(η−ε)•(BηBε). Não se divide por η−ε, logo ε=η está incluído; não se aplica h a vetor fora de seu domínio nem se pressupõe h limitado/inversível com gap.

[REAL — antitonia] O helper hilbert_commuting_positive_product é genérico numa Hilbert complexa completa e consome Commute.mul_nonneg. Bη,Bε são positivos e sua comutação vem do primeiro alvo. A diferença é positiva porque η−ε≥0: a passagem pela positividade dos CLM e IsPositive.smul_of_nonneg conserva o coeficiente REAL embutido em ℂ, com exact_mod_cast. Assim 0<ε≤η implica Bη≤Bε. Não se usa produto positivo de operadores não comutantes nem uma hipótese de ordem disfarçada como conclusão.

[REAL — peso em todo positivo] O último alvo usa b=sqrt(Bη), c=sqrt(Bε), sempre o wrapper antigo hilbertPositiveSqrt. O segundo helper prova b b*=Bη e c c*=Bε por positividade/auto-adjunção da raiz e sqrt_mul_sqrt_self. A pertença dessas raízes em E e no core, e a comutação com TODAS as médias, são descarregadas pelos fornecedores já provados. scalarWeight_right_perturbed_mono_all_positive recebe então a ordem b b*≤c c* e entrega νη(X)≤νε(X) para TODO X:PositiveCoreInput P, inclusive valores infinitos. Não resta hipótese A∈nν, comutação ou pertença em E no tipo público final. Isso compara avaliações do peso, não afirma sη X sη≤sε X sε.

[REAL — proveniência documental e autoria] Ficha 22:22:49 e adendo 22:23:56 foram lidos integralmente e antecedem o primeiro DEV 22:25:47. Oito fornecedores da ficha e três do adendo foram confrontados por bytes, nomes, linhas e enunciados com K e V. A identidade pelo grafo é escolha e construção do agente principal, registrada com consumidor para produtos dos cortes; a consulta independente comparou alternativas e não é alegada como origem da prova. A rota CFC real alternativa não foi recodificada.

[REAL — axiomas e controle] Módulo completo e auditor próprios passaram. Quatro tipos com universos e prints transitivos contêm somente propext, Classical.choice e Quot.sound; universos são normalizados no parser, sem alterar streams. Os dois helpers foram lidos e compilados, cobertos transitivamente pelos alvos públicos, sem print privado separado. O único DEV localizado é rc0 sem avisos; não se importou seu objeto. O negativo autoral mantém 0<ε≤η e tenta usar o teorema na ordem inversa; falha por Type mismatch com imports resolvidos. Controle relido, não reexecutado; não é prova de desigualdade estrita, e a igualdade ε=η permanece possível.

[REAL — proveniência] 678 objetos próprios anteriores preservados; somente módulo e auditor novos, total 680. Zero fornecedor antigo recompilado; cache de pacotes pinado e herdado, sem nova auditoria integral da biblioteca. LEAN_PATH dos traces contém somente V e seus pacotes, nenhum build autoral ou DEV. Run próprio rc0 em 36.169 s; zero avisos do alvo/auditor e 178 mensagens históricas de fornecedores separadas no JSON. O stderr preserva ainda o aviso do cache aesop com alterações locais, já presente na base; não é aviso do alvo. A contagem total de jobs do Lake não significa recompilação dessa quantidade de objetos.

| Artefato | SHA256 lido |
|---|---|
| Fonte final (K=cópia própria) | b908f79a4d20ca8f456eb245e2a605a6cc6e611667e1c8a8d6cb1cee2ee4f838 |
| .olean próprio | dffb577a426a8156f48a671ba92401a912208c3053c5a2b5c4c8f2d326863fff |
| .olean autoral standalone, apenas comparação | dffb577a426a8156f48a671ba92401a912208c3053c5a2b5c4c8f2d326863fff |

Igualdade binária medida: True.

[OPEN — limites] Aceite restrito a quatro teoremas públicos mais dois helpers privados, sem nova definição. ε>0 e η>0 são hipóteses explícitas; ε≤η é necessária para as duas conclusões de ordem. Não se cobre ε=0. X pertence ao cone positivo LIMITADO do mesmo core, sem restrição de finitude do peso; não se amplia aqui o domínio para todos os afiliados não limitados. Não foi definido peso limite nem provadas suas leis/semifinitude/tracialidade. A1(b) e gate permanecem sem promoção. Nenhum objeto autoral/DEV utilizado, nenhum monólito/recorder/writer ou memória executado/modificado; controle negativo autoral somente relido.

Artefatos de evidência:

- [compilation](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_ordem_reguladores\compilation.json>) — SHA256 94d8f48a968dc984c5263b0ada838f4cc0e80d4d967fdea88a4296b120e1c099.
- [run próprio](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_ordem_reguladores\independent_20260914_222944_958643\run.json>) — SHA256 9a4840920a2c53498e902df87de0a3fae58a93778fb744f8d2f7747ba14fc5f5.
- [tipos/axiomas](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_ordem_reguladores\independent_20260914_222944_958643\type_axiom_audit.json>) — SHA256 8530bcc2c7b9e845082a4e0e0e4121bf1d6a1a34ec465a10d871cced582e0454.
- [histórico](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_ordem_reguladores\history_read.json>) — SHA256 7e716bc4f8a36e1fee9a138410a6165f4846f680a798c30f4dcfa3fa77ab0558.
- [fornecedores da ficha](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_ordem_reguladores\provider_checks.json>) — SHA256 0c5993ad9236a9c492f47385e193abd00651829ced382a9d48788b5adb7fa62d.


## Ficha/adendo integral: REAPROVEITAMENTO_A1B_ORDEM_REGULADORES

[OPEN — ficha anterior à ordem dos reguladores]

# A1(b): os cortes originais crescem quando o regulador diminui

2026-09-14T22:22:49.061721-03:00

For epsilon,eta>0 derive the resolvent identity B_epsilon-B_eta=(eta-epsilon) smul (B_eta*B_epsilon) directly from the SAME graph and inverse equation. CFC of the same R proves the cuts commute, so their positive product is nonnegative. If epsilon<=eta, obtain B_eta<=B_epsilon. Then discharge membership, square-root norm products and original-average commutation to instantiate the already constructed all-positive weight comparison for sqrt(B_eta) and sqrt(B_epsilon), for EVERY X in PositiveCoreInput P. No finite-weight premise, new resolvent, spectral coordinates, trace definition or physics coupling. The regulator epsilon is mathematical, not beta_TGL. Consumer: define monotone cutoff weights and their supremum on the same cone. Trace and semifinitude of its limit remain obligations.

ADAPTAR: consumir graph_iff e positividade já provadas. Mathlib cfc_commute_cfc e Commute.mul_nonneg foram lidos nas fontes pinadas; adendo anterior ao alvo. Não redefinir o inverso ou instalar hipótese de ordem como resultado.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseGeneratorCutoff.lean:50` — `f615a4a8b80a4bf970c719aa9d44fd2d917eb52f01fa1c925cfcab8151adc227`

```lean
theorem regularInverseGeneratorCutoff_graph (P : SiteProfile) (ε : ℝ) (hε : 0 < ε)
    (x : RegularHilbert (TowerHilbert P)) :
    (regularInverseGeneratorCutoff P ε x,
      x-(ε : ℂ) • regularInverseGeneratorCutoff P ε x) ∈
        (regularPositiveGenerator P).graph
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseGeneratorCutoff.lean:99` — `f615a4a8b80a4bf970c719aa9d44fd2d917eb52f01fa1c925cfcab8151adc227`

```lean
theorem regularInverseGeneratorCutoff_graph_iff (P : SiteProfile) (ε : ℝ) (hε : 0 < ε)
    (x y : RegularHilbert (TowerHilbert P)) :
    (x,y) ∈ (regularPositiveGenerator P).graph ↔
      regularInverseGeneratorCutoff P ε (y+(ε : ℂ) • x) = x
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseGeneratorCutoff.lean:24` — `f615a4a8b80a4bf970c719aa9d44fd2d917eb52f01fa1c925cfcab8151adc227`

```lean
theorem regularInverseGeneratorCutoff_nonneg (P : SiteProfile) (ε : ℝ) (hε : 0 < ε) :
    0 ≤ regularInverseGeneratorCutoff P ε
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseCutoffCFC.lean:62` — `cbdf10aea749a552b0f47afb3ef59560ed47d6f46cf7dd8064dc963a092c3490`

```lean
theorem regularInverseGeneratorCutoff_cfc (P : SiteProfile) (ε : ℝ) (hε : 0 < ε) :
    regularInverseGeneratorCutoff P ε =
      cfc (inverseCutoffFunction ε) (regularSpectralResolvent P)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351AllPositiveWeightOrder.lean:73` — `e91306108a0a296b320907a2899f5776747869dffae14f65fe3fe45197bf07bb`

```lean
theorem scalarWeight_right_perturbed_mono_all_positive (P : SiteProfile)
    (b c : (regularCoreAlgebra P).toStarSubalgebra)
    (hb : b ∈ scalarPolarRightAlgebra P) (hc : c ∈ scalarPolarRightAlgebra P)
    (hbc : b * star b ≤ c * star c)
    (hbe : ∀ δ : ℝ, Commute b.val (regularAverage P δ))
    (hce : ∀ δ : ℝ, Commute c.val (regularAverage P δ))
    (X : PositiveCoreInput P) :
    dualQuadraticIntegral (star b.val * X.val * b.val) (regularVacuum P) ≤
      dualQuadraticIntegral (star c.val * X.val * c.val) (regularVacuum P)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseCutoffCFC.lean:125` — `cbdf10aea749a552b0f47afb3ef59560ed47d6f46cf7dd8064dc963a092c3490`

```lean
theorem regularInverseGeneratorCutoff_sqrt_right (P : SiteProfile) (ε : ℝ) (hε : 0 < ε) :
    ∃ h : hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε) ∈ regularCoreAlgebra P,
      (⟨hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε),h⟩ :
        (regularCoreAlgebra P).toStarSubalgebra) ∈ scalarPolarRightAlgebra P
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351CutoffAverageCommutation.lean:49` — `bc881ee5df7e027859ef14d7379b27bc9c2a27bea3b08cf42d6604805afa2a66`

```lean
theorem regularInverseCutoffSqrt_commutes_average (P : SiteProfile)
    (ε : ℝ) (hε : 0 < ε) (δ : ℝ) :
    Commute (hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε))
      (regularAverage P δ)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350AntiunitaryPositiveConjugation.lean:15` — `83be0cf3f811bd6fd429c7705fdb1a00b27fdd6496ee971b9ca5f355c00d6f36`

```lean
def hilbertPositiveSqrt (T : H →L[ℂ] H) : H →L[ℂ] H
```

Seis modalidades e outras bancadas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_regulator_order\20260914_222228_030596\searches.json. Ausência nominal nos recortes não é ausência universal.


## Ficha/adendo integral: ADENDO_FICHA_REGULADORES_PRODUTO_POSITIVO

[OPEN — fornecedores antes do código]

2026-09-14T22:23:56.003280-03:00

Usar CFC somente para comutação de funções do mesmo R. A ordem vem da identidade resolvente e da positividade do PRODUTO de cortes que comutam; não da ordem de sanduíches. A comparação de sanduíches sob o peso usa o teorema all_positive já compilado com suas hipóteses explícitas. Aplicar o fornecedor genérico Commute.mul_nonneg em Hilbert antes da especialização fixa as instâncias. A raiz original satisfaz sqrt(B)*sqrt(B)=B e é autoadjunta por positividade.

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\CStarAlgebra\ContinuousFunctionalCalculus\Unital.lean:377

```lean
lemma cfc_commute_cfc (f g : R → R) (a : A) : Commute (cfc f a) (cfc g a)
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\CStarAlgebra\ContinuousFunctionalCalculus\Instances.lean:292

```lean
lemma Commute.mul_nonneg {a b : A} (ha : 0 ≤ a) (hb : 0 ≤ b) (h : Commute a b) :
    0 ≤ a * b
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\SpecialFunctions\ContinuousFunctionalCalculus\Rpow\Basic.lean:265

```lean
lemma sqrt_mul_sqrt_self (a : A) (ha : 0 ≤ a := by cfc_tac) : sqrt a * sqrt a = a
```

