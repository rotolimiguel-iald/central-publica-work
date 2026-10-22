[REAL — 2 teoremas e 0 definições verificados no delta por reprodução isolada autoral e revisão independente. A1(b): traço concreto ainda OPEN.]

# ENTREGA 011 / A1 — A ordem dos valores perturbados alcança todo o cone positivo

2026-09-14T22:31:46.228123-03:00

Dois teoremas públicos e um auxiliar privado, zero definições. A comparação em nν estende-se a todos A do mesmo core por recuperação dos valores de Ab e Ac pelas médias originais. O mesmo hilbertPositiveSqrt de cada positivo X pertence ao core e tem quadrado estrela igual a X, permitindo comparar em todo PositiveCoreInput, com valores ENNReal inclusive infinitos. A composição não usa minorantes positivos finitos de ν.

Permanecem explícitas as hipóteses b,c na álgebra direita, bb*≤cc* e comutação de ambos com todas as médias. A comparação é no cone positivo limitado de N, sem alegar extensão a operadores afiliados não limitados. As raízes dos cortes já têm os fornecedores de pertença/comutação; a ordem em ε é outro delta. Traço completo e tracialidade ainda abertos. Nenhum gate alterado.

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

Autor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\all_positive_weight_order_attempts\20260914_222021_908055\run.json`. Comando registrado: `['C:\\Users\\rotol\\.elan\\toolchains\\leanprover--lean4---v4.31.0\\bin\\lake.exe', 'build', 'TGLExt.AuditA1AllPositiveWeightOrder']`. Fonte e objeto autorais abaixo. Reutilização somente de objetos próprios previamente produzidos na raiz isolada; os pacotes externos vêm do cache explicitado no relatório. Não é nova compilação integral da biblioteca.

Revisor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_ordem_todos_positivos\independent_20260914_222456_726686\run.json`. `676` objetos próprios anteriores; `0` fornecedores antigos recompilados adicionalmente. Zero objetos do autor/DEV herdados; `0` avisos de alvos/auditor. Avisos de fornecedores e diferenças binárias estão preservados em compilation.json. Comparação indisponível não significa igualdade.

As tentativas de desenvolvimento que falharam permanecem em disco. Só o fonte final, as reproduções rc0 e as auditorias aceitas entram nesta conclusão. Controle negativo de uma aplicação adulterada não é um teorema geral de inexistência.

## Fontes e objetos autorais

| Módulo | SHA256 fonte | SHA256 objeto |
|---|---|---|
| `V351AllPositiveWeightOrder` | `e91306108a0a296b320907a2899f5776747869dffae14f65fe3fe45197bf07bb` | `29e1b88569f8ca3f0b27f7f5ddc3e8d901a61598df26b3d34ad245c1c7957af2` |

## Tipos completos e axiomas

```lean
TGLV350.Regular.scalarWeight_right_perturbed_mono_all_squares (P : TGLExt.SiteProfile)
  (b c : ↥(VonNeumannAlgebra.toStarSubalgebra.{0} (TGLV350.Regular.regularCoreAlgebra P)))
  (hb : Membership.mem.{0, 0} (TGLV350.Regular.scalarPolarRightAlgebra P) b)
  (hc : Membership.mem.{0, 0} (TGLV350.Regular.scalarPolarRightAlgebra P) c)
  (hbc : LE.le.{0} (HMul.hMul.{0, 0, 0} b (star.{0} b)) (HMul.hMul.{0, 0, 0} c (star.{0} c)))
  (hbe : ∀ (δ : ℝ), Commute.{0} (↑b) (TGLV350.Regular.regularAverage P δ))
  (hce : ∀ (δ : ℝ), Commute.{0} (↑c) (TGLV350.Regular.regularAverage P δ))
  (A : ↥(VonNeumannAlgebra.toStarSubalgebra.{0} (TGLV350.Regular.regularCoreAlgebra P))) :
  LE.le.{0}
    (TGLV350.Regular.dualQuadraticIntegral
      (HMul.hMul.{0, 0, 0} (HMul.hMul.{0, 0, 0} (star.{0} ↑b) (HMul.hMul.{0, 0, 0} (star.{0} ↑A) ↑A)) ↑b)
      (TGLV350.Regular.regularVacuum P))
    (TGLV350.Regular.dualQuadraticIntegral
      (HMul.hMul.{0, 0, 0} (HMul.hMul.{0, 0, 0} (star.{0} ↑c) (HMul.hMul.{0, 0, 0} (star.{0} ↑A) ↑A)) ↑c)
      (TGLV350.Regular.regularVacuum P))
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.scalarWeight_right_perturbed_mono_all_positive (P : TGLExt.SiteProfile)
  (b c : ↥(VonNeumannAlgebra.toStarSubalgebra.{0} (TGLV350.Regular.regularCoreAlgebra P)))
  (hb : Membership.mem.{0, 0} (TGLV350.Regular.scalarPolarRightAlgebra P) b)
  (hc : Membership.mem.{0, 0} (TGLV350.Regular.scalarPolarRightAlgebra P) c)
  (hbc : LE.le.{0} (HMul.hMul.{0, 0, 0} b (star.{0} b)) (HMul.hMul.{0, 0, 0} c (star.{0} c)))
  (hbe : ∀ (δ : ℝ), Commute.{0} (↑b) (TGLV350.Regular.regularAverage P δ))
  (hce : ∀ (δ : ℝ), Commute.{0} (↑c) (TGLV350.Regular.regularAverage P δ)) (X : TGLV350.Regular.PositiveCoreInput P) :
  LE.le.{0}
    (TGLV350.Regular.dualQuadraticIntegral (HMul.hMul.{0, 0, 0} (HMul.hMul.{0, 0, 0} (star.{0} ↑b) ↑X) ↑b)
      (TGLV350.Regular.regularVacuum P))
    (TGLV350.Regular.dualQuadraticIntegral (HMul.hMul.{0, 0, 0} (HMul.hMul.{0, 0, 0} (star.{0} ↑c) ↑X) ↑c)
      (TGLV350.Regular.regularVacuum P))
```

Axiomas: propext, Classical.choice, Quot.sound.

## Custódia e limites

- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\AUDITORIA_ORDEM_TODOS_POSITIVOS_A1B.json` — SHA256 `0376b03930ddc40491799ace965586bf10cd418957ef425d430fde37edca1363`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_ordem_todos_positivos\REVIEW_A1_ALL_POSITIVE_WEIGHT_ORDER_FINAL.json` — SHA256 `150f490a0480c424267a3e3e36f85a864782c3d69fbf1a9b185dfd609861e622`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_ordem_todos_positivos\compilation.json` — SHA256 `7745819031950aeef64e2597386f489dba9f352c1421704bfefe66d1af4bb72b`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\ACEITE_DELTA_ALL_POSITIVE_WEIGHT_ORDER.json` — SHA256 `c1f682be6e48d0eccf0adec337f1607c7a33054922f537d3da765754c2c3eb7a`.

O manifesto e o recibo próprios ligam esta entrega aos arquivos efetivamente lidos. Nenhum monólito canônico foi importado ou executado; nenhum dado experimental, D1, sigma, Atlas ou diário canônico foi alterado.

## Revisão independente integral

# Revisão independente — ordem do peso em todos os positivos

2026-09-14T22:28:48.172097-03:00

**A1_ALL_POSITIVE_WEIGHT_ORDER_REVIEW_ACCEPTED__REGULATOR_ORDER_TRACE_OPEN**

[REAL] **Sem achados P0/P1/P2.** Dois teoremas públicos + um helper privado, zero definições. Módulo completo e auditor próprios rc0; dois #check com universos e axiomas exclusivamente do trio permitido. Aceite delimitado ao enunciado efetivamente compilado.

[REAL — alvo e hipóteses] scalarWeight_right_perturbed_mono_all_squares recebe TODO A do mesmo regularCoreAlgebra P, sem A∈nν. Recebe explicitamente b,c∈scalarPolarRightAlgebra P, b b*≤c c* e comutação de b,c com regularAverage P δ para TODO δ real. A conclusão compara valores em ENNReal do MESMO dualQuadraticIntegral no MESMO regularVacuum P; a definição antiga scalarDualWeight é exatamente essa avaliação. Não há troca para outro peso, ideal uniforme ou GNS.

[REAL — extensão por valores] d_n=1/(n+1)>0 torna T_n=A e_n membro do ideal scalarWeightLeftIdeal pela finitude e pertença fornecidas por scalarDualWeight_square_finite_strong_density. A igualdade (A b)e_n=(A e_n)b usa somente a comutação explícita b e_n=e_n b; idem c. A comparação finita anterior é aplicada a T_n. iSup_le seguido de le_iSup_of_le no MESMO índice transporta a comparação aos supremos, e a recuperação já provada é usada para A b e A c. Não se postula monotonicidade dos quadrados, minorantes positivos finitos de ν, nem valor finito dos supremos. O ramo de convergência forte do fornecedor não é usado como substituto da recuperação de valores.

[REAL — cone inteiro e raiz efetiva] PositiveCoreInput P é o subtipo de operadores do core positivos, sem campo de finitude escalar. O helper privado hilbertPositiveSqrt_core_square trabalha numa Hilbert complexa completa abstrata. vonNeumann_norm_closed fornece fechamento do mesmo subobjeto; cfcₙ_mem com s=N.toStarSubalgebra e 𝕜′=ℂ mantém a raiz no core. hilbertPositiveSqrt continua o wrapper existente de CFC.sqrt; sqrt_eq_real_sqrt, sqrt_nonneg e sqrt_mul_sqrt_self provam exatamente star(sqrt X)*sqrt X=X. Aplicar o primeiro teorema a essa raiz produz o segundo para TODO X≥0, inclusive ν(X)=∞. Não há instalação de uma ordem alternativa nem suposição de CompleteSpace do subtipo N.

[REAL — axiomas, histórico e controle] O auditor próprio imprime os DOIS tipos completos com pp.universes e os axiomas transitivos. O helper privado é compilado e está coberto transitivamente, sem alegar print privado independente. Axiomas permitidos: propext, Classical.choice, Quot.sound, com universos normalizados apenas no parser; os streams brutos permanecem pinados. Duas tentativas DEV rc1 foram relidas e excluídas: SMulMemClass/iSup_le_iSup e coerções, depois StarSubalgebra.coe_mul e aviso de binder. A fonte final usa o subobjeto explícito, iSup_le/le_iSup_of_le e change, maxHeartbeats 1400000. O negativo autoral inverte a conclusão mantendo as hipóteses; o stream acusa Type mismatch com imports resolvidos. Trata-se de controle de aplicação do teorema, não demonstração de falsidade para toda instância especial.

[REAL — fichas] Ficha e adendo de raiz foram lidos por inteiro; os sete e cinco fornecedores tiveram bytes, linha e enunciado confrontados com os arquivos e com as cópias próprias. Registros datados 22:14:00 e 22:15:22 antecedem a primeira tentativa DEV 22:16:43. Reaproveitamento da finitude das médias, ordem finita e recuperação está efetivamente consumido. A aplicação às raízes dos cortes usa fornecedores anteriores para pertença em E e comutação; sua ordem em ε permanece obrigação separada, não antecedente silencioso quitado neste delta.

[REAL — proveniência] 676 objetos próprios anteriores preservados; somente módulo e auditor novos, total 678. Zero fornecedor antigo recompilado; cache de pacotes pinado e herdado, sem nova auditoria integral da biblioteca. LEAN_PATH dos traces contém somente V e seus pacotes, nenhum build autoral ou DEV. Run próprio rc0 em 36.334 s; zero avisos do alvo/auditor e 178 mensagens históricas de fornecedores separadas no JSON. A contagem total de jobs do Lake não significa recompilação dessa quantidade de objetos.

| Artefato | SHA256 lido |
|---|---|
| Fonte final (K=cópia própria) | e91306108a0a296b320907a2899f5776747869dffae14f65fe3fe45197bf07bb |
| .olean próprio | 29e1b88569f8ca3f0b27f7f5ddc3e8d901a61598df26b3d34ad245c1c7957af2 |
| .olean autoral standalone, apenas comparação | 29e1b88569f8ca3f0b27f7f5ddc3e8d901a61598df26b3d34ad245c1c7957af2 |

Igualdade binária medida: True.

[OPEN — limites] Aceite restrito a dois teoremas públicos e um helper privado; nenhuma definição nova. As hipóteses b,c∈E, b b*≤c c* e comutação com médias permanecem explícitas; não se afirma comparação para b,c arbitrários. Todos os positivos significa o cone de operadores limitados do mesmo core; valores do peso podem ser infinitos. Não se estende aqui a todos os operadores positivos afiliados não limitados. Ordem dos reguladores em ε, peso limite perturbado e tracialidade permanecem abertos neste delta; A1(b) não concluído. Nenhuma execução de monólito, recorder, writer ou memória; controle negativo autoral apenas relido. Nenhum objeto de projeto autoral/DEV utilizado.

Artefatos de evidência:

- [compilation](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_ordem_todos_positivos\compilation.json>) — SHA256 7745819031950aeef64e2597386f489dba9f352c1421704bfefe66d1af4bb72b.
- [run próprio](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_ordem_todos_positivos\independent_20260914_222456_726686\run.json>) — SHA256 bf89e4db9c9ed5e29084fa266e27a120ab14cb24b20e41a504aebd08b8916be4.
- [tipos/axiomas](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_ordem_todos_positivos\independent_20260914_222456_726686\type_axiom_audit.json>) — SHA256 9d03cda6d63ac4a509b5372fb401512619c9d419480d344d94ef177175b8c1a1.
- [histórico](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_ordem_todos_positivos\history_read.json>) — SHA256 1de28661a97b16b3585b7ca23d1a6a49b121090f2bc8153d0bcef40c5934f987.
- [fornecedores da ficha](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_ordem_todos_positivos\provider_checks.json>) — SHA256 66f1a7c943802f562521257cc93b1e9742356edeb2325c469f46755ab27e1d26.


## Ficha/adendo integral: REAPROVEITAMENTO_A1B_ORDEM_TODOS_POSITIVOS

[OPEN — ficha anterior à extensão de ordem]

# A1(b): ordem em todos os positivos do mesmo core

2026-09-14T22:14:00.904198-03:00

Extend scalarWeight_right_perturbed_mono from A in n_nu to EVERY A in N, using exact average recovery for A*b and A*c, finite averages A*e_n, and explicit hypotheses that b and c commute with the SAME regularAverage P delta. Then for EVERY positive X in the SAME N instantiate A as the EXISTING hilbertPositiveSqrt(X), proving its membership in N by norm closure and existing real CFC membership, and A*A=X by existing sqrt identity. Keep b b* <= c c*, membership in scalarPolarRightAlgebra and average commutation explicit. No new definition of weight, root, GNS, core or regularizer. The actual cutoff roots discharge those hypotheses via existing suppliers; regulator-order B_epsilon <= B_eta itself is a separate consumer/obligation. Infinite values allowed. This does not prove traciality, final semifinitude, or completion of A1(b).

ADAPTAR: compor os três fornecedores já provados; não criar outro ideal ou peso. A aproximação é dos VALORES e não de minorantes positivos. Reusar CFC.sqrt_eq_real_sqrt, cfcₙ_mem e CFC.sqrt_mul_sqrt_self para o mesmo wrapper de raiz. O adendo dos fornecedores mathlib será anexado antes do alvo.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351PerturbedWeightOrder.lean:29` — `9af750ad0099449655e5350b76219d51986849e434584359bd09de475fe936d6`

```lean
theorem scalarWeight_right_perturbed_mono (P : SiteProfile)
    (b c : (regularCoreAlgebra P).toStarSubalgebra)
    (hb : b ∈ scalarPolarRightAlgebra P) (hc : c ∈ scalarPolarRightAlgebra P)
    (hbc : b * star b ≤ c * star c) (A : scalarWeightLeftIdeal P) :
    dualQuadraticIntegral (star b.val * (star A.val.val*A.val.val) * b.val)
      (regularVacuum P) ≤
    dualQuadraticIntegral (star c.val * (star A.val.val*A.val.val) * c.val)
      (regularVacuum P)
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

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarDualWeight.lean:66` — `e20dc5262ec98b62c8a6797fd07492e584a03fefefd0dd87b1666484dd72bc53`

```lean
theorem scalarDualWeight_square_finite_strong_density (P : SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra) :
    (∀ h : ℝ, 0 < h → dualQuadraticIntegral
      (star (A.val * regularAverage P h) * (A.val * regularAverage P h)) (regularVacuum P) < ⊤) ∧
    (∀ h : ℝ, A.val * regularAverage P h ∈ regularCoreAlgebra P) ∧
    (∀ v, Tendsto (fun h : ℝ => (A.val * regularAverage P h) v) (𝓝[>] 0) (𝓝 (A.val v)))
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351CutoffAverageCommutation.lean:49` — `bc881ee5df7e027859ef14d7379b27bc9c2a27bea3b08cf42d6604805afa2a66`

```lean
theorem regularInverseCutoffSqrt_commutes_average (P : SiteProfile)
    (ε : ℝ) (hε : 0 < ε) (δ : ℝ) :
    Commute (hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε))
      (regularAverage P δ)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseCutoffCFC.lean:125` — `cbdf10aea749a552b0f47afb3ef59560ed47d6f46cf7dd8064dc963a092c3490`

```lean
theorem regularInverseGeneratorCutoff_sqrt_right (P : SiteProfile) (ε : ℝ) (hε : 0 < ε) :
    ∃ h : hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε) ∈ regularCoreAlgebra P,
      (⟨hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε),h⟩ :
        (regularCoreAlgebra P).toStarSubalgebra) ∈ scalarPolarRightAlgebra P
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350AntiunitaryPositiveConjugation.lean:15` — `83be0cf3f811bd6fd429c7705fdb1a00b27fdd6496ee971b9ca5f355c00d6f36`

```lean
def hilbertPositiveSqrt (T : H →L[ℂ] H) : H →L[ℂ] H
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

Seis modalidades e outras bancadas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_all_positive_weight_order\20260914_221338_858806\searches.json. Ausência nominal nos recortes não é ausência universal.


## Ficha/adendo integral: ADENDO_FICHA_ORDEM_POSITIVA_RAIZ

[OPEN — fornecedores recuperados antes do código]

2026-09-14T22:15:22.996428-03:00

Reusar vonNeumann_norm_closed no MESMO core. O corpo de vonNeumann_starOrdered já mostra a pertença da raiz por cfcₙ_mem e sua identidade quadrática; adaptar somente o empacotamento do hilbertPositiveSqrt, sem nova raiz e sem nova demonstração de fechamento. Não inferir que StarOrderedRing abstrato sozinho fornece uma única raiz. Os fornecedores mathlib abaixo foram lidos antes do alvo.

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350LevelExpectationUniformBound.lean:57

```lean
theorem vonNeumann_norm_closed {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H] (M : VonNeumannAlgebra H) :
    IsClosed (M : Set (H →L[ℂ] H))
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350LevelExpectationUniformBound.lean:65

```lean
theorem vonNeumann_starOrdered {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H] (M : VonNeumannAlgebra H) :
    StarOrderedRing M.toStarSubalgebra
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\CStarAlgebra\ContinuousFunctionalCalculus\Range.lean:205

```lean
lemma cfcₙ_mem {𝕜' S : Type*} [Monoid 𝕜'] [MulAction 𝕜' A] [SetLike S A] [NonUnitalSubringClass S A]
    [SMul 𝕜 𝕜'] [IsScalarTower 𝕜 𝕜' A] [SMulMemClass S 𝕜' A] [StarMemClass S A] {s : S}
    [hs : IsClosed (s : Set A)] (f : 𝕜 → 𝕜) {a : A} (has : a ∈ s) :
    cfcₙ f a ∈ s
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\SpecialFunctions\ContinuousFunctionalCalculus\Rpow\Basic.lean:302

```lean
lemma sqrt_eq_real_sqrt (a : A) (ha : 0 ≤ a := by cfc_tac) :
    CFC.sqrt a = cfcₙ Real.sqrt a
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\SpecialFunctions\ContinuousFunctionalCalculus\Rpow\Basic.lean:265

```lean
lemma sqrt_mul_sqrt_self (a : A) (ha : 0 ≤ a := by cfc_tac) : sqrt a * sqrt a = a
```

