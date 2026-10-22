[REAL — 2 teoremas e 0 definições verificados no delta por reprodução isolada autoral e revisão independente. A1(b): traço concreto ainda OPEN.]

# ENTREGA 011 / A1 — A média original pertence à álgebra da ação direita polar

2026-09-15T00:37:48.997907-03:00

Dois teoremas públicos, três auxiliares privados globais, zero definições. Uma partição exata da integral vetorial existente constrói combinações finitas de translações, limitadas por um, que convergem forte-* à média unilateral original. O fechamento já pago da ação direita transporta para essa média e sua estrela a identidade no ideal inteiro do mesmo peso, com o mesmo GNS e J.

Não afirma que a média é auto-adjunta, nem produz nesta entrega vetores fixos S/F, identificação dos implementadores, compatibilidade Q ou tracialidade. O próximo consumidor usará e_delta*e_delta. O controle negativo recusa confundir pertinência à álgebra direita com auto-adjunção; não classifica todas as médias. Nenhum novo integral, peso, GNS, monólito ou gate.

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

Autor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\average_polar_right_attempts\20260915_002918_832206\run.json`. Comando registrado: `['C:\\Users\\rotol\\.elan\\toolchains\\leanprover--lean4---v4.31.0\\bin\\lake.exe', 'build', 'TGLExt.AuditA1AveragePolarRight']`. Fonte e objeto autorais abaixo. Reutilização somente de objetos próprios previamente produzidos na raiz isolada; os pacotes externos vêm do cache explicitado no relatório. Não é nova compilação integral da biblioteca.

Revisor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_media_acao_direita\independent_20260915_003308_093413\run.json`. `699` objetos próprios anteriores; `0` fornecedores antigos recompilados adicionalmente. Zero objetos do autor/DEV herdados; `0` avisos de alvos/auditor. Avisos de fornecedores e diferenças binárias estão preservados em compilation.json. Comparação indisponível não significa igualdade.

As tentativas de desenvolvimento que falharam permanecem em disco. Só o fonte final, as reproduções rc0 e as auditorias aceitas entram nesta conclusão. Controle negativo de uma aplicação adulterada não é um teorema geral de inexistência.

## Fontes e objetos autorais

| Módulo | SHA256 fonte | SHA256 objeto |
|---|---|---|
| `V351AveragePolarRight` | `9a982e09a318e7c306c20a9c5baf0d07a6354b34d3cf2e6cc3cf168968f334cc` | `c8e2ec1647c3a69fd5e9586dbee4363a072e30c2a1b6bbc97cd064607dff7572` |

## Tipos completos e axiomas

```lean
TGLV350.Regular.regularAverage_polar_approximants (P : TGLExt.SiteProfile) (δ : ℝ) (hδ : LT.lt.{0} 0 δ) :
  ∃ b,
    (∀ (n : ℕ), Membership.mem.{0, 0} (TGLV350.Regular.scalarPolarRightAlgebra P) (b n)) ∧
      (∀ (n : ℕ), LE.le.{0} (norm.{0} ↑(b n)) 1) ∧
        (∀ (v : ↥(TGLV350.Regular.RegularHilbert (TGLExt.TowerHilbert P))),
            Filter.Tendsto.{0, 0} (fun n => ↑(b n) v) Filter.atTop.{0}
              (nhds.{0} ((TGLV350.Regular.regularAverage P δ) v))) ∧
          ∀ (v : ↥(TGLV350.Regular.RegularHilbert (TGLExt.TowerHilbert P))),
            Filter.Tendsto.{0, 0} (fun n => ↑(star.{0} (b n)) v) Filter.atTop.{0}
              (nhds.{0} ((star.{0} (TGLV350.Regular.regularAverage P δ)) v))
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.regularAverage_mem_scalarPolarRightAlgebra (P : TGLExt.SiteProfile) (δ : ℝ) (hδ : LT.lt.{0} 0 δ) :
  Membership.mem.{0, 0} (TGLV350.Regular.scalarPolarRightAlgebra P)
    (Subtype.mk.{1} (TGLV350.Regular.regularAverage P δ) ⋯)
```

Axiomas: propext, Classical.choice, Quot.sound.

## Custódia e limites

- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\AUDITORIA_MEDIA_ACAO_DIREITA_A1B.json` — SHA256 `4a0e9e7c54c70f87b0a850a642c785e5b0d3d4060957de28c71655e4b4434d14`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_media_acao_direita\REVIEW_A1_AVERAGE_POLAR_RIGHT_FINAL.json` — SHA256 `7f8a5e0fe852e30f066c2f97eb7097c9df65ca3f95fd28a17137960ef53c3d86`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_media_acao_direita\compilation.json` — SHA256 `84479368c983b2e712d52c71dd15157bfda87b1005426c88eaa494f3ef0bcace`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\ACEITE_DELTA_AVERAGE_POLAR_RIGHT.json` — SHA256 `4e50dc786aafac67de1f17ebe54326eb7e784036d2fec1fb36a4ca67a8736bf4`.

O manifesto e o recibo próprios ligam esta entrega aos arquivos efetivamente lidos. Nenhum monólito canônico foi importado ou executado; nenhum dado experimental, D1, sigma, Atlas ou diário canônico foi alterado.

## Revisão independente integral

2026-09-15T00:36:52.822755-03:00

**A1_AVERAGE_POLAR_RIGHT_REVIEW_ACCEPTED__FIXED_VECTORS_TRACE_OPEN**

[REAL] **Sem achados P0/P1/P2.** Módulo e auditor próprios rc0; dois tipos completos com universos, axiomas do trio. Controle negativo próprio rc1 por Type mismatch.

[REAL — tipos e objetos] regularAverage_polar_approximants recebe o mesmo P e δ>0, constrói b_n na álgebra direita existente E, norma≤1 e limites fortes b_n→eδ e b_n*→eδ*. regularAverage_mem_scalarPolarRightAlgebra conclui a pertença de eδ a E. A definição de E inclui as identidades direitas para b e b* em TODO o ideal escalar nν, com o J/GNS originais. A família aproximante exigida no fornecedor de fechamento é construída, não recebida como campo.

[REAL — partição exata] O helper average_partition traduz cada integral em [0,h] por k h usando a lei de grupo e integral_comp_add_right. sum_integral_adjacent_intervals, com μ=volume explicitado, soma os intervalos adjacentes e fornece b_N e_h=e_(N h), com normalização N⁻¹h⁻¹=(Nh)⁻¹. É uma identidade finita da integral vetorial existente, não uma afirmação assintótica de Riemann. O helper admite N=0 ou h=0 pela convenção de inverso zero; o consumidor usa N=n+1>0 e h=d_n>0.

[REAL — construção e convergência forte] b_n é a combinação finita (n+1)⁻¹Σ_{k<n+1}λ_(k d_n), d_n=δ/(n+1). Pertence a E por soma e escala dos geradores já existentes. A cota≤1 vem das normas das λ e da cardinalidade da soma. d_n tende a zero no filtro perfurado, pois δ>0. A identidade b_n e_(d_n)=eδ e a cota dão ‖b_n v−eδ v‖≤‖v−e_(d_n)v‖→0. O bound_limit local é um argumento de contração no corpo da prova, não uma quarta declaração privada/global.

[REAL — adjunto, ponto crítico] average_commutes_regular demonstra comutação da média com cada λ por transporte da integral vetorial e abelianidade da lei regular. Da soma resulta b_n e_(d_n)=e_(d_n)b_n. A prova estrelará e_(d_n)b_n=eδ, e não somente a identidade na ordem anterior: assim obtém b_n* e_(d_n)*=eδ*. Reaplica bound_limit usando ‖b_n*‖≤1 e regularAverage_star_tendsto_identity, já provado para contrações. Não usa continuidade geral de star para SOT e não afirma eδ=eδ*.

[REAL — fechamento e domínio] O primeiro uso de scalarRightAction_closed_of_bounded_strongStar recebe b_n, as duas convergências e a primeira componente da pertença b_n∈E. O segundo recebe b_n*, com o limite adjunto e star_star, além da segunda componente dessa pertença. Produz a ação para eδ e eδ* em todos A∈nν. A passagem da inscrição GNS é responsabilidade do fornecedor já aceito; não se presume continuidade forte irrestrita de Λ nem se constrói outro GNS.

[REAL — auxiliares, ficha e histórico] Três helpers privados globais: average_commutes_regular, average_partition e finite_regular_average_norm, auditados transitivamente pelos dois alvos. Nove fornecedores da ficha relidos por linha e pin. O excerto operatorIntegral_commutes está truncado no binder; o tipo completo foi relido, e o adendo explica o adaptador concreto via integral vetorial. A ficha antecede o código; o adendo declara posterioridade ao DEV. Dois DEV rc1 preservados e excluídos: timeouts/coerções/ext/rewrite e depois medida/filtro/metavariáveis. As três versões usam os mesmos limites 2200000/200000; o final rc0 está limpo.

[REAL — controle] BadAverageMembershipIsSelfAdjoint foi reproduzido em V/ReviewControls com cópia de bytes e objetos próprios. A tentativa de usar pertença em E como prova de eδ*=eδ retorna rc1 por Type mismatch, com imports funcionais. O controle autoral também foi relido/pinado. Essa recusa prova apenas a inadequação do termo adulterado, não uma classificação de todas as médias por auto-adjunção.

[REAL — proveniência] 699 objetos próprios preservados; 2 novos (alvo+auditor), total 701. Nenhum fornecedor antigo recompilado, nenhum objeto K/DEV herdado. Run 41.531 s; negativo 21.701 s. Zero avisos do alvo/auditor; 178 mensagens de fornecedores herdadas discriminadas. all_accepted_builds_exit_zero=True; all_attempts_exit_zero=False inclui o negativo esperado. LEAN_PATH dos traces restrito a V/pacotes.

| Artefato | SHA256 lido |
|---|---|
| Fonte K=snapshot=V | 9a982e09a318e7c306c20a9c5baf0d07a6354b34d3cf2e6cc3cf168968f334cc |
| .olean próprio | c8e2ec1647c3a69fd5e9586dbee4363a072e30c2a1b6bbc97cd064607dff7572 |
| .olean autoral, só comparação | c8e2ec1647c3a69fd5e9586dbee4363a072e30c2a1b6bbc97cd064607dff7572 |

Igualdade binária medida: True.

[OPEN] Aceite29: dois teoremas públicos, três helpers privados globais e zero defs; bound_limit é prova local incluída transitivamente. Pertença da média e da sua estrela na álgebra direita original. Não declara auto-adjunção da média, vetor fixo S/F, igualdade dos implementadores, Q ou tracialidade. 19 V351 são subconjunto das 940 entradas da base (937 Lean e três configurações), não 959 arquivos; pins relidos. Somente esta pasta e novas saídas em V. Fontes K/OLD/V353, memórias, monólito, writers e pareceres anteriores preservados.

Tipos lidos:

~~~lean
theorem regularAverage_polar_approximants (P : SiteProfile) (δ : ℝ) (hδ : 0 < δ) :
    ∃ b : ℕ → (regularCoreAlgebra P).toStarSubalgebra,
      (∀ n, b n ∈ scalarPolarRightAlgebra P) ∧
      (∀ n, ‖(b n).val‖ ≤ 1) ∧
      (∀ v, Tendsto (fun n => (b n).val v) atTop (𝓝 (regularAverage P δ v))) ∧
      (∀ v, Tendsto (fun n => (star (b n)).val v) atTop
        (𝓝 (star (regularAverage P δ) v)))
~~~

Axiomas próprios: propext, Classical.choice, Quot.sound.

~~~lean
theorem regularAverage_mem_scalarPolarRightAlgebra (P : SiteProfile)
    (δ : ℝ) (hδ : 0 < δ) :
    (⟨regularAverage P δ,regularAverage_mem P δ⟩ :
      (regularCoreAlgebra P).toStarSubalgebra) ∈ scalarPolarRightAlgebra P
~~~

Axiomas próprios: propext, Classical.choice, Quot.sound.

Evidências:

- [compilation](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_media_acao_direita\compilation.json>) — SHA256 84479368c983b2e712d52c71dd15157bfda87b1005426c88eaa494f3ef0bcace.
- [run próprio](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_media_acao_direita\independent_20260915_003308_093413\run.json>) — SHA256 a5de8e79ce0fce0bd20c5eaf4591af8235455c3350318025b5f966ba269776b0.
- [tipos/axiomas](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_media_acao_direita\independent_20260915_003308_093413\type_axiom_audit.json>) — SHA256 e6c3d69fb64320cc340e296fa3c4d7fe11860d6e8f7bcd9282bad4cde82cf121.
- [negativo próprio](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_media_acao_direita\negative_20260915_003500_293603\run.json>) — SHA256 3a38cfb3185539120692c9d51efb5c61e5e93dd0aa793ac4ae84634d24a7bed0.
- [preservação19/940](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_media_acao_direita\preservation_19_940.json>) — SHA256 76f0a8e413b80773fca360c4a5acb7dbd211302a46b3fa2d42b745b672db0929.
- [histórico](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_media_acao_direita\history_read.json>) — SHA256 faf46fa257a2088f9bb2dd441be697089eb3d65f316b61e50a276258a6d17d3f.


## Ficha/adendo integral: REAPROVEITAMENTO_A1B_MEDIA_ACAO_DIREITA

[OPEN — ficha anterior à pertença da média à álgebra direita]

2026-09-15T00:20:30.703642-03:00

ADAPTAR: prove the EXISTING regularAverage delta (delta>0) belongs to the EXISTING scalarPolarRightAlgebra, supplying the right action for z=e*e needed by ScalarRightAdjointPair with the same weight/GNS/S/F. Construct bounded finite sums of the existing regular unitaries b_n=(n+1)^(-1) sum_{k<n+1} lambda_(delta*k/(n+1)). Exact interval partition gives e_delta=b_n e_(delta/(n+1)), so contraction bounds and existing small-average convergence give strong convergence; commuting factors and the existing adjoint convergence give strong-star. Apply already proved bounded strong-star closure twice. This avoids a new generic Riemann-integral framework, operator-norm continuity, Bochner integration in B(H), alternate average, GNS or trace. The fixed S/F vector, modular implementator identity, Q and traciality remain later obligations. No claim average is selfadjoint; use e*e for later fixed vector.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarRightActionAlgebra.lean:164` — `68b1b9b84ba21c9c17de246fb69c8c48908e9ca313558b513322d119f66d98af`

```lean
theorem scalarPolarRightAlgebra_regular_mem (P : SiteProfile) (t : ℝ) :
    regularRightCoreElement P t ∈ scalarPolarRightAlgebra P
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarRightActionLimits.lean:26` — `ab55b5a1e05d6f8317bc61e0a303b960dc7e9888999e03cbb1c63287e4b37b9d`

```lean
theorem scalarRightAction_closed_of_bounded_strongStar (P : SiteProfile)
    {ι : Type*} {l : Filter ι} [NeBot l]
    (b : ι → (regularCoreAlgebra P).toStarSubalgebra)
    (B : (regularCoreAlgebra P).toStarSubalgebra) (C : ℝ)
    (hbound : ∀ i, ‖(b i).val‖ ≤ C)
    (hstrong : ∀ x, Tendsto (fun i => (b i).val x) l (𝓝 (B.val x)))
    (hadjoint : ∀ x, Tendsto (fun i => (star (b i)).val x) l (𝓝 ((star B).val x)))
    (A : scalarWeightLeftIdeal P)
    (hact : ∀ i, ∃ hi : A.val * b i ∈ scalarWeightLeftIdeal P,
      scalarWeightGNSEmbedding P ⟨A.val*b i,hi⟩ =
        antiunitaryConjugate (scalarTomitaPolarFactor P)
          (scalarGNSRepresentation P (star (b i))) (scalarWeightGNSEmbedding P A)) :
    ∃ hAB : A.val * B ∈ scalarWeightLeftIdeal P,
      scalarWeightGNSEmbedding P ⟨A.val*B,hAB⟩ =
        antiunitaryConjugate (scalarTomitaPolarFactor P)
          (scalarGNSRepresentation P (star B)) (scalarWeightGNSEmbedding P A)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350RegularApproximation.lean:41` — `d8e7830989e0ba3d71f0e8495f54414cedc12a9eac16b1bc0501f15342b8bb44`

```lean
theorem regularAverage_apply (P : TGLExt.SiteProfile) (h : ℝ)
    (v : RegularHilbert (TGLExt.TowerHilbert P)) :
    regularAverage P h v = h⁻¹ • ∫ t in 0..h, regularUnitary P t v
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350RegularApproximation.lean:68` — `d8e7830989e0ba3d71f0e8495f54414cedc12a9eac16b1bc0501f15342b8bb44`

```lean
theorem regularAverage_tendsto_identity (P : TGLExt.SiteProfile)
    (v : RegularHilbert (TGLExt.TowerHilbert P)) :
    Tendsto (fun h : ℝ => regularAverage P h v) (𝓝[≠] 0) (𝓝 v)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ContractionAdjointLimit.lean:51` — `75c191ec2110441b6554ca7beddfc7806f3e3aac6e879e8461f7632cfa78eaa5`

```lean
theorem regularAverage_star_tendsto_identity (P : TGLExt.SiteProfile)
    (v : RegularHilbert (TGLExt.TowerHilbert P)) :
    Tendsto (fun h : ℝ => star (regularAverage P h) v) (𝓝[≠] 0) (𝓝 v)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350StrongOperatorIntegral.lean:59` — `7ee0e23dc3319a72734ce420f540251f59a27561fa61221d6ab5f98b2989dfa7`

```lean
theorem operatorIntegral_commutes (F : Family (H
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350RegularTowerRepresentation.lean:23` — `21638dcca0d86b6a62050dee85212ee74cf07d783e43bdf6fecd28a04fb5b41f`

```lean
theorem regular_mul (P : SiteProfile) (s t : ℝ) :
    regularUnitary P s * regularUnitary P t = regularUnitary P (s+t)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\MeasureTheory\Integral\IntervalIntegral\Basic.lean:1115` — `c71e2f79bad2a043032169e58b596779588df187470be980e5198b9bafe5be18`

```lean
theorem sum_integral_adjacent_intervals {a : ℕ → ℝ} {n : ℕ}
    (hint : ∀ k < n, IntervalIntegrable f μ (a k) (a <| k + 1)) :
    ∑ k ∈ Finset.range n, ∫ x in a k..a <| k + 1, f x ∂μ = ∫ x in (a 0)..(a n), f x ∂μ
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\MeasureTheory\Integral\IntervalIntegral\Basic.lean:954` — `c71e2f79bad2a043032169e58b596779588df187470be980e5198b9bafe5be18`

```lean
theorem integral_comp_add_right (d) : (∫ x in a..b, f (x + d)) = ∫ x in a + d..b + d, f x
```

Buscas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_average_polar_right\20260915_002009_898046\searches.json. Ausência nominal não é ausência universal. Consulta2 corrigida V2 já lida; rota reduzida à partição exata da integral e limites existentes.


## Ficha/adendo integral: ADENDO_FICHA_MEDIA_ACAO_DIREITA

[OPEN — complemento posterior ao DEV e anterior ao aceite]

{
  "timestamp": "2026-09-15T00:29:17.387887-03:00",
  "status": "ADDENDUM_AFTER_DEV_BEFORE_ACCEPTANCE",
  "decision": "Exact partition replaces a generic Riemann-sum framework as proposed before coding. Two public theorems, three private helpers, no global definitions. The contraction-bound argument is local within the approximation theorem.",
  "corrections": "First DEV timeouts from incomplete scalar coercions and broad ext descending into Lp; explicit real-to-complex casts and ext1 resolve without raising heartbeats. Second DEV had unresolved measure/filter/metavariables and fixed with actual volume, atTop and typed limits. Third DEV rc0 clean. Original operatorIntegral commutation provider remains adequate mathematically; its concrete instance wrapper needed the already used vector-integral transport shape from V351CutoffAverageCommutation, not another integral.",
  "adapter": {
    "path": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\RETOMADA_A1B_012\\k\\TGLExt\\V351CutoffAverageCommutation.lean",
    "bytes": 3148,
    "sha256": "bc881ee5df7e027859ef14d7379b27bc9c2a27bea3b08cf42d6604805afa2a66"
  },
  "final_dev": {
    "path": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\RETOMADA_A1B_012\\dev_average_polar_right\\20260915_002754_463277\\run.json",
    "bytes": 3120,
    "sha256": "8acd6a5bd7c2253b66fcc0cf76d173c896d0b5867bd0c7674ab5bf2131d6c446"
  },
  "limitations": "The average is one-sided and is not claimed selfadjoint. Negative control deliberately confuses algebra membership with selfadjointness. No fixed S/F vector, U=pi(lambda)R_-t, Q, traciality or trace contract is proved in this delta."
}
