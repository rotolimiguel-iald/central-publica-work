[REAL — 3 teoremas e 0 definições verificados no delta por reprodução isolada autoral e revisão independente. A1(b): traço concreto ainda OPEN.]

# ENTREGA 011 / A1 — O domínio de quadrados finitos do peso limite é denso no core

2026-09-14T23:34:45.689426-03:00

Três teoremas públicos e um auxiliar privado, sem definições. Para a no domínio finito do peso dual original e delta>0, o peso limite de (a q_delta)*(a q_delta) é limitado por delta^-1 nu(a*a), portanto finito. A prova usa a comparação existente de perturbações direitas e a cota uniforme do corte. A convergência forte q_n->I e a densidade WOT antiga de n_nu dão densidade WOT dos quadrados finitos do mesmo scalarInverseLimitWeight.

Semifinitude usual pelo domínio denso. Não afirma ainda o campo de minorantes positivos finitos do contrato de traço nem a tracialidade; essas obrigações continuam abertas. A consulta tracial anexa é proposta anterior a este aceite, sem prova Lean nova: localiza a compatibilidade da forma ponderada Q com a estrela e a extensão por Fatou/sanduíches. Não pedir novamente normalidade, fidelidade, escala dual ou densidade usual aqui entregues, nem receber a conclusão tracial como hipótese nova. Os fornecedores antigos foram compilados sem alteração e não são novos teoremas. Nenhum outro peso, cone, raiz, GNS, monólito ou gate.

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

Autor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\inverse_limit_semifinite_attempts\20260914_232127_032597\run.json`. Comando registrado: `['C:\\Users\\rotol\\.elan\\toolchains\\leanprover--lean4---v4.31.0\\bin\\lake.exe', 'build', 'TGLExt.AuditA1InverseLimitSemifiniteness']`. Fonte e objeto autorais abaixo. Reutilização somente de objetos próprios previamente produzidos na raiz isolada; os pacotes externos vêm do cache explicitado no relatório. Não é nova compilação integral da biblioteca.

Revisor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_semifinitude_peso_limite\independent_20260914_232652_905782\run.json`. `690` objetos próprios anteriores; `3` fornecedores antigos recompilados adicionalmente. Zero objetos do autor/DEV herdados; `0` avisos de alvos/auditor. Avisos de fornecedores e diferenças binárias estão preservados em compilation.json. Comparação indisponível não significa igualdade.

As tentativas de desenvolvimento que falharam permanecem em disco. Só o fonte final, as reproduções rc0 e as auditorias aceitas entram nesta conclusão. Controle negativo de uma aplicação adulterada não é um teorema geral de inexistência.

## Fontes e objetos autorais

| Módulo | SHA256 fonte | SHA256 objeto |
|---|---|---|
| `V351InverseLimitSemifiniteness` | `0af32fbe3a7f0a36ef61f8e247c24a6117fab4f2b2b778890492b21e13f2f7a1` | `2cdab1103e507815974946e215d6fea11ed5c4c54ecd9808d0bd9c57fb1f453c` |

## Tipos completos e axiomas

```lean
TGLV350.Regular.scalarInverseLimitWeight_domainCut_bound (P : TGLExt.SiteProfile) (δ : ℝ) (hδ : LT.lt.{0} 0 δ)
  (a : ↥(TGLV350.Regular.scalarWeightLeftIdeal P)) :
  LE.le.{0}
    (TGLV350.Regular.scalarInverseLimitWeight P
      (TGLV351.positiveSquare P (HMul.hMul.{0, 0, 0} (↑a) (TGLV350.Regular.regularDomainCut P δ))))
    (HMul.hMul.{0, 0, 0} (ENNReal.ofReal (Inv.inv.{0} δ))
      (TGLV350.Regular.dualQuadraticIntegral (HMul.hMul.{0, 0, 0} (star.{0} ↑↑a) ↑↑a)
        (TGLV350.Regular.regularVacuum P)))
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.scalarInverseLimitWeight_domainCut_finite (P : TGLExt.SiteProfile) (δ : ℝ) (hδ : LT.lt.{0} 0 δ)
  (a : ↥(TGLV350.Regular.scalarWeightLeftIdeal P)) :
  LT.lt.{0}
    (TGLV350.Regular.scalarInverseLimitWeight P
      (TGLV351.positiveSquare P (HMul.hMul.{0, 0, 0} (↑a) (TGLV350.Regular.regularDomainCut P δ))))
    Top.top.{0}
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.scalarInverseLimitWeight_square_finite_wot_closure (P : TGLExt.SiteProfile) :
  Eq.{1}
    (closure.{0}
      (setOf.{0} fun A =>
        ∃ (h :
          Membership.mem.{0, 0} (TGLV350.Regular.regularCoreAlgebra P) (ContinuousLinearMapWOT.toCLM.{0, 0, 0, 0} A)),
          LT.lt.{0}
            (TGLV350.Regular.scalarInverseLimitWeight P
              (TGLV351.positiveSquare P (Subtype.mk.{1} (ContinuousLinearMapWOT.toCLM.{0, 0, 0, 0} A) h)))
            Top.top.{0}))
    (setOf.{0} fun A =>
      Membership.mem.{0, 0} (TGLV350.Regular.regularCoreAlgebra P) (ContinuousLinearMapWOT.toCLM.{0, 0, 0, 0} A))
```

Axiomas: propext, Classical.choice, Quot.sound.

## Custódia e limites

- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\AUDITORIA_SEMIFINITUDE_PESO_LIMITE_A1B.json` — SHA256 `9817ee5e5bd1f1fe9597fba1840db9cea5a06dd4d7714d7f40d7268711842373`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_semifinitude_peso_limite\REVIEW_A1_INVERSE_LIMIT_SEMIFINITE_FINAL.json` — SHA256 `cb8ba687892217793a3546a1d284c40a9096f5e2c0f3b9657da3bc3e72526f2c`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_semifinitude_peso_limite\compilation.json` — SHA256 `91b40c91a49aedb81dcb6dbbea20f1365fb4b00b029f459d78e18af30d5318f4`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\ACEITE_DELTA_INVERSE_LIMIT_SEMIFINITE_FINAL.json` — SHA256 `31918de94dcbaaa20a128b130b280e2616c5c0db3d69617d380f88471f3514c4`.

O manifesto e o recibo próprios ligam esta entrega aos arquivos efetivamente lidos. Nenhum monólito canônico foi importado ou executado; nenhum dado experimental, D1, sigma, Atlas ou diário canônico foi alterado.

## Revisão independente integral

2026-09-14T23:34:20.794691-03:00

**A1_INVERSE_LIMIT_SEMIFINITE_REVIEW_ACCEPTED__TRACIAL_FINITE_MINORANTS_OPEN**

[REAL] **Sem achados P0/P1/P2.** Três teoremas públicos + um helper privado; módulo completo e auditor próprios rc0. Três #check com universos e axiomas exclusivamente do trio permitido. Aceite limitado aos tipos efetivamente verificados.

[REAL — tipos e objeto] Três teoremas públicos, nenhum def novo. O domínio inicial é a : scalarWeightLeftIdeal P do MESMO ν; δ>0 é explícito. A primeira conclusão avalia scalarInverseLimitWeight P (TGLV351.positiveSquare P (a.val * regularDomainCut P δ)) e fornece a cota ENNReal.ofReal(δ⁻¹)·ν(a*a), uniforme no regulador ε da definição do limite. A segunda conclui <⊤. A terceira identifica o fecho WOT do conjunto de operadores de N com quadrado finito para esse MESMO peso limite com N inteiro, sem antecedente extra sobre P.

[REAL — ordem correta] Para cada ε=1/(n+1), s é a raiz ORIGINAL hilbertPositiveSqrt(Bε), q=qδ e b=q s. A pertença b∈E usa as pertenças já provadas de q e s, e c=√(δ⁻¹)I também pertence a E. O cálculo é bb*=q(ss*)q=q Bε q=Bε q²≤δ⁻¹I=cc*. Usa apenas q auto-adjunto e sua comutação com Bε; não comuta a com q ou s, não supõe comutação de a com Bε e nem necessita provar q s=s q neste argumento. scalarWeight_right_perturbed_mono recebe precisamente bb*≤cc* e a∈nν. A desigualdade de pesos não é inferida por ordem falsa dos sanduíches.

[REAL — supremum, finitude e Haar] A igualdade entre o corte do quadrado de aq e ν(b* a*a b) é associatividade/estrela no CLM, transportada por congrArg explícito de dualQuadraticIntegral. Para c, homogeneidade existente e δ>0 dão o fator real δ⁻¹; ←Complex.ofReal_inv resolve a coerção, sem trocar ℝ por uma ordem complexa indevida. A cota é independente de n, logo iSup_le a passa ao limite. ENNReal.mul_lt_top consome ofReal finito e a.property; não converte valor infinito com toReal. Mesmo dualQuadraticIntegral, regularVacuum e normalização Haar herdados, sem redefinição ou fator novo.

[REAL — densidade WOT e não circularidade] Para cada a∈nν, aq_(1/(n+1)) pertence ao conjunto square-finite de τ pela segunda conclusão e converge fortemente a a pelo teorema de q_n já entregue; a multiplicação à esquerda usa apenas continuidade do CLM fixo a. strong_tendsto_wot e mem_closure_of_tendsto colocam todo nν no fecho WOT desse conjunto. closure_mono, o ANTIGO scalarWeight_square_finite_wot_closure de ν e closure_closure dão N⊆fecho. O sentido contrário usa somente a WOT-fechadura de N. Não se pressupõe semifinitude de τ, não se identifica nτ com nν e não se postula uma família de minorantes positivos finitos de ν.

[REAL — auxiliar e fornecedores antigos] O único helper privado hilbert_sqrt_mul_star é genérico em Hilbert complexo completo e consome CFC.sqrt_nonneg/sqrt_mul_sqrt_self para ss*=B. Seus axiomas são auditados transitivamente pelas três conclusões. V350FixedBaseEquivalence, V351ExtendedBaseDualWeight e V351ScalarWeightSemifiniteness foram copiados de OLD/kernel após igualdade de bytes OLD=K; construídos do fonte em V, com 5+14+2 prints antigos, todos permitidos. São três fornecedores adicionais, não novos resultados. Não se instalou objeto autoral ou DEV nem se refez o GNS.

[REAL — ficha e histórico] Ficha 23:10:26 antecede a primeira tentativa e reutiliza a busca de seis modalidades da ficha25, cujo consumidor já era a densidade do domínio de τ. As sete entradas de fornecedores foram verificadas por linha, enunciado e hash. O adendo 23:14:09 documenta a reprodução antiga já feita e é posterior ao primeiro DEV; não foi apresentado aqui como anterior a todo código. Quatro DEV rc1 foram preservados/excluídos: congr1/timeout, tentativa instrumentada, homogeneidade/isDefEq e cast de inverso complexo; o final 23:20:29 passou limpo. Os pins históricos apontam a snapshots reais, com localização viva apenas como texto. A auditoria autoral standalone rc0 e a recusa Type mismatch do negativo BadLimitSemifiniteInfiniteCut foram relidas/pinadas, sem reexecutar o negativo.

[REAL — proveniência] 690 objetos próprios anteriores preservados; 5 novos objetos construídos (três fornecedores antigos + alvo + auditor), total 695. Run próprio rc0 em 86.683 s; zero avisos do alvo/auditor, 178 mensagens de fornecedores com origem separada no JSON. Traces de compilação restringem LEAN_PATH a V e seus pacotes. Cache de pacotes pinado/herdado; quantidade total de jobs do Lake não é quantidade de recompilações. Stderr completo preservado, inclusive aviso herdado do pacote aesop, se presente.

| Artefato | SHA256 lido |
|---|---|
| Fonte final (K=cópia própria) | 0af32fbe3a7f0a36ef61f8e247c24a6117fab4f2b2b778890492b21e13f2f7a1 |
| .olean próprio | 2cdab1103e507815974946e215d6fea11ed5c4c54ecd9808d0bd9c57fb1f453c |
| .olean autoral standalone (só comparação) | 2cdab1103e507815974946e215d6fea11ed5c4c54ecd9808d0bd9c57fb1f453c |

Igualdade binária medida do alvo: True.

| Fornecedor antigo | Igualdade fonte OLD=K=V | .olean próprio = autoral |
|---|---|---|
| TGLExt.V350FixedBaseEquivalence | True | True |
| TGLExt.V351ExtendedBaseDualWeight | True | True |
| TGLExt.V351ScalarWeightSemifiniteness | True | True |

[OPEN — limites] Aceite26: três teoremas públicos, um helper privado transitivo, zero definições; os três fornecedores antigos e seus 21 prints são contados separadamente. P é o mesmo SiteProfile; δ>0 e a∈nν são hipóteses da estimativa/finitude, descarregadas na sequência usada para a densidade. A cota depende de δ, não de ε; não se afirma finitude de τ(a*a) para todo a∈nν. Com as leis de peso/normalidade anteriormente aceitas, o fecho WOT aqui provado é o critério usual de semifinitude do MESMO scalarInverseLimitWeight. Não é prova de tracialidade nem do campo finite-positive-minorants de RegularCoreTraceData; não é entrega do traço completo A1(b). Nenhuma afirmação de convergência em norma de operadores, gap, novo GNS, igualdade de domínios algébricos ou núcleo analítico inteiro. Não foram examinadas novas rotas de tracialidade nesta revisão. Somente V e esta pasta de revisão receberam novas saídas. K, OLD, pareceres/pins anteriores, memórias, writers e monólito preservados; pacote Mathlib e objetos próprios anteriores herdados com limites explícitos.

Artefatos de evidência:

- [compilation](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_semifinitude_peso_limite\compilation.json>) — SHA256 91b40c91a49aedb81dcb6dbbea20f1365fb4b00b029f459d78e18af30d5318f4.
- [run próprio](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_semifinitude_peso_limite\independent_20260914_232652_905782\run.json>) — SHA256 816fe0b6669b3e30f365779cafe82ad51c5a84b45d0342e746d0a5d2dfd9b86b.
- [tipos/axiomas](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_semifinitude_peso_limite\independent_20260914_232652_905782\type_axiom_audit.json>) — SHA256 6dd36b1a81acc1a54c1793183047eb9fc7adf609737818eca270888f285d7e2f.
- [histórico](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_semifinitude_peso_limite\history_read.json>) — SHA256 0b92dbba85ebc8c0b08188914c94d7f69fec84ab12d3c2be139c657623576658.
- [fornecedores](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_semifinitude_peso_limite\old_suppliers_read_v2.json>) — SHA256 fb48b14b2a255b21a9baca04a1b8b9d30bf7c04250ae60639820bd256c4a4279.


## Ficha/adendo integral: REAPROVEITAMENTO_A1B_SEMIFINITUDE_LIMITE

[OPEN — ficha anterior ao consumidor de semifinitude usual]

2026-09-14T23:10:26.452078-03:00

Consumer of the previously searched domain-cut route: for a in the ORIGINAL n_nu, show tau((a q_delta)* (a q_delta)) <= ofReal(delta^-1) nu(a*a) < infinity, then use q_n -> I strongly and the OLD WOT closure of n_nu to prove WOT closure of the square-finite set of the SAME tau is the same N. No new weight, square-root or cone. No traciality or finite-positive-minorant contract asserted. The old WOT theorem is imported from source, not re-proved.

Reaproveita as seis modalidades e outras bancadas da ficha do corte de domínio, cujo alvo já incluía este consumidor. Não repete a varredura integral nem cria outra raiz. Consulta independente foi lida inteira.

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularDomainCut.lean:33 — 60ed1575faca04fe95bb7fb208804944a84ac61114eede8ecbb28a67f9bed8e9

```lean
theorem regularDomainCut_right (P : SiteProfile) (δ : ℝ) (hδ : 0 < δ) :
    regularDomainCut P δ ∈ scalarPolarRightAlgebra P
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularDomainCut.lean:93 — 60ed1575faca04fe95bb7fb208804944a84ac61114eede8ecbb28a67f9bed8e9

```lean
theorem regularDomainCut_product_bound (P : SiteProfile) (ε δ : ℝ)
    (hε : 0 < ε) (hδ : 0 < δ) :
    regularInverseGeneratorCutoff P ε * (regularDomainCut P δ).val *
      (regularDomainCut P δ).val ≤ (δ⁻¹ : ℂ) • 1
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularDomainCut.lean:113 — 60ed1575faca04fe95bb7fb208804944a84ac61114eede8ecbb28a67f9bed8e9

```lean
theorem regularDomainCut_tendsto_identity (P : SiteProfile)
    (v : RegularHilbert (TowerHilbert P)) :
    Tendsto (fun n : ℕ => (regularDomainCut P (1/((n : ℝ)+1))).val v) atTop (𝓝 v)
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseLimitWeight.lean:87 — cfdced33d3cafdd2782f4d7e8ca77974e0ddee22f19803dfbd36275787c28f1e

```lean
def scalarInverseLimitWeight (P : SiteProfile) (X : PositiveCoreInput P) : ℝ≥0∞
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseCutoffCFC.lean:125 — cbdf10aea749a552b0f47afb3ef59560ed47d6f46cf7dd8064dc963a092c3490

```lean
theorem regularInverseGeneratorCutoff_sqrt_right (P : SiteProfile) (ε : ℝ) (hε : 0 < ε) :
    ∃ h : hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε) ∈ regularCoreAlgebra P,
      (⟨hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε),h⟩ :
        (regularCoreAlgebra P).toStarSubalgebra) ∈ scalarPolarRightAlgebra P
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351PerturbedWeightOrder.lean:29 — 9af750ad0099449655e5350b76219d51986849e434584359bd09de475fe936d6

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

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarWeightSemifiniteness.lean:16 — f5e7e85b034949be6517286f60c692d3d97d29c341aeba42a1f7172b7e610c2a

```lean
theorem scalarWeight_square_finite_wot_closure (P : SiteProfile) :
    closure {A : RegularHilbert (TowerHilbert P) →WOT[ℂ]
        RegularHilbert (TowerHilbert P) |
      A.toCLM ∈ regularCoreAlgebra P ∧ HasFiniteScalarSquare P A.toCLM} =
    {A : RegularHilbert (TowerHilbert P) →WOT[ℂ]
        RegularHilbert (TowerHilbert P) | A.toCLM ∈ regularCoreAlgebra P}
```



## Ficha/adendo integral: ADENDO_FICHA_SEMIFINITUDE_FORNECEDOR

[REAL — fornecedor antigo reproduzido]

2026-09-14T23:14:09.335698-03:00

The old WOT closure of the ORIGINAL dual-weight domain is imported, not re-proved. Lake reproduced three existing source modules, unchanged, for this dependency. They do not establish semifiniteness of the new limit by themselves, and do not count as new results. No author/DEV objects may be used for independent acceptance.

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350FixedBaseEquivalence.lean — 6b4cda490d27efc86fdac21e57b91c30778477221d08ff9c90f31a1bf8b8f278

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ExtendedBaseDualWeight.lean — 1ea9226e3fe1ee75bc66178f575f47c0207e80dca34a0113efd0c0f099b7cd87

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarWeightSemifiniteness.lean — f5e7e85b034949be6517286f60c692d3d97d29c341aeba42a1f7172b7e610c2a

Run: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\existing_semifinite_dependency_attempts\20260914_231037_491709\run.json


## Ficha/adendo integral: revisao_consulta_tracialidade_limite/CONSULTA_TRACIALIDADE_LIMITE

# Consulta — tracialidade do MESMO peso limite

[DERIVED / OPEN] Consulta de leitura, sem código Lean novo, sem compilação e sem aceite do DEV26. Pareceres 1–25, fontes, objetos e memórias permanecem intactos.

A rota curta na literatura é a perturbação de Pedersen–Takesaki: para ν NSF e h não singular afiliado, com σν_t=Ad(h^{it}), a perturbação por h⁻¹ tem grupo modular trivial e é tracial. A regularização é exatamente (h+ε)⁻¹. A prova e suas hipóteses estão em Hiai, Prop.9.3, Teo.9.4 e prova do Teo.9.9, pp.83–88. Isso é [KNOWN], não fornecedor Lean localizado. [Fonte primária relida](https://arxiv.org/pdf/2004.02383#page=84).

[REAL — alcance do mapa] LACUNAS_A1.md é um mapa histórico, não fotografia atual de cada entrega. A ação de Δν^{it} em π(N) já é fornecida por scalarTomitaImaginaryPower_core_conjugation; h^{it}=λ_t e a afiliação pertencem a outros módulos já entregues. A forma do supremo dos cortes, sua ordem, leis, fidelidade e escala também já têm fontes. Não pedir novamente esses pagamentos, nem identificação h=Δν: h atua no Hilbert regular e Δν no GNS original. O que falta aqui é a passagem modular/estrela que torna TRACIAL o mesmo scalarInverseLimitWeight.

[REAL — hipótese sugerida versus resultado existente] Ponha U_t=scalarTomitaImaginaryPower P t, J=scalarTomitaPolarFactor P, L_t=π(regularRightCoreElement P t). O resultado core5 é
U_t π(a)=π(λ_t a λ_t*) U_t.
Não localizei, na busca delimitada das fontes V350/V351 pertinentes, a igualdade adicional
(**U**) U_t=L_t · antiunitaryConjugate J L_t = L_t regularRightGNS P (−t).
O sinal −t na ação direita é determinado por scalarTomitaPolarFactor_regular_left; J é antilinear e J²=I. A fórmula proposta J U_t J=U_t está paga, não J U_t J=U_−t.

A ação direita nas inscrições e a ação esquerda existentes já identificam o segundo membro de (**U**) como Λν(a)↦Λν(λ_t a λ_t*). Para fechar (**U**) falta demonstrar essa mesma identidade para U_t nas inscrições densas, ou sua igualdade amortecida exigida por scalarTomitaImaginaryPower_unique. Este último NÃO é unicidade de quem implementa a mesma conjugação: sua premissa exata é W b(Tν)=g_t(Tν), para Tν=scalarTomitaResolvent P. Covariância sozinha só coloca a diferença dos implementadores no comutante; não a torna identidade. Não receber (**U**) como campo novo. Ela pode servir à via espectral, mas não é pré-requisito extra da via PT se a lei de perturbação for provada diretamente para a ação modular já identificada.

[DERIVED — alvo vetorial mínimo sem novo GNS] Para δn=1/(n+1), escreva s_n=hilbertPositiveSqrt(Bδn), L_n=π(⟨s_n,mem⟩), e, APENAS como notação desta consulta,
Q(v)=sup_n ENNReal.ofReal(||L_n v||²).
Não se afirma Q finito em todo Hν e não se cria operador h⁻¹/² na representação por decreto. Por scalarWeight_inverseCutoff_perturbed_norm, para a∈nν:
τ(a*a)=Q(J⁻¹Λν(a))=Q(JΛν(a)).
Para a∈scalarWeightStarCore P, seja x=Λν(a). O MESMO S estende estrela e S=J Bν, Bν=scalarTomitaPositiveRoot P, D(Bν)=D(S); portanto
τ(aa*)=Q(J Sx)=Q(Bν x).

Assim uma meta concreta, suficiente já sobre o núcleo finiteDualStarCore (não é necessário começar por TODO D(S)), é
(**Q**) Q(Bν Λν(a)) = Q(J Λν(a)).
A aplicação de Bν usa a inclusão de domínio fornecida por scalarWeightStar_mem_closedTomitaDomain e scalarClosedTomitaDomain_le_root. Igualdade em ENNReal deve incluir ∞. S=J Bν e a isometria de J NÃO provam (**Q**): Q não é a norma original e L_n não comuta com J em geral. Esta é precisamente a nova compatibilidade do peso perturbado com a estrela, não algo aceito por renomear τ.

Se for escolhida a via (**U**), ainda se deve transportar a identidade dos grupos para a forma/domínio de meia potência e identificar os cortes representados L_n. O cancelamento escrito informalmente Δν=π(h)·Jπ(h⁻¹)J envolve operadores não limitados; igualdade dos grupos não autoriza multiplicá-los em domínio não declarado. O menor consumidor é (**Q**) nos vetores do núcleo. Evita construir GNS de τ, mas o passo de cálculo funcional/continuação modular que prova (**Q**) continua real e aberto. Alternativa equivalente: prova KMS na faixa para elementos regularizados, com ação no tempo imaginário identificada; só invariância em tempos reais não basta. A nota não decide que uma dessas adaptações já esteja compilada.

[DERIVED — extensão econômica do núcleo a TODO a∈N] Este passo tem fornecedores concretos e não exige minorantes positivos finitos de ν nem graph-core de τ. Tome e_m=regularAverage P(1/(m+1)), a_m=e_m* a e_m=regularSandwich P a(1/(m+1)).
1. finiteDualStarCore_strongStar_approximation já dá a_m no núcleo, ||a_m||≤||a|| e convergência forte de a_m E a_m*. Não é hipótese nova de continuidade forte da estrela.
2. Para cada corte fixo ε, regularInverseCutoffSqrt_commutes_average e scalarWeight_right_average_le dão
   Wε((a e_m)*(a e_m))≤Wε(a*a):
   (a e_m)sε=(a sε)e_m. O fornecedor de média vale para TODO operador do core, mesmo com peso infinito.
   À esquerda, e_m e_m*≤I porque ||e_m||≤1; logo
   (e_m* a e_m)*(e_m* a e_m)≤(a e_m)*(a e_m).
   A monotonicidade já provada de Wε/τ conclui τ(a_m*a_m)≤τ(a*a). Aplicar a mesma construção a a* dá a estimativa correspondente. Não se ordenam sanduíches por sε≤sη.
3. Para cada ε, a_m sε→a sε fortemente. Para cada parâmetro dual s, dualAmbient s é conjugação por unidade, portanto a órbita aplicada a Ω converge. O integrando é ofReal(dualHaarFactor) vezes uma norma ao quadrado: Fatou, como em scalarWeight_square_eq_iSup_averages, dá
   Wε(a*a)≤liminf_m Wε(a_m*a_m)≤liminf_m τ(a_m*a_m).
   Passando ao supremo ε=δn: τ(a*a)≤liminf_m τ(a_m*a_m).
   Idem para aa*. Measurabilidade e Haar são os existentes; não se usa normalidade só para uma sequência não monótona.
4. Se (**Q**) foi provado no núcleo, então τ(a_m*a_m)=τ(a_m a_m*). A semicontinuidade do passo3 e a cota do passo2 dão τ(aa*)≤τ(a*a); repetir com a* dá igualdade, inclusive ∞.

Logo uma vez paga (**Q**), este adaptador Fatou+sanduíches fecha o campo exato
∀ a:(regularCoreAlgebra P).toStarSubalgebra,
scalarInverseLimitWeight P (TGLV351.positiveSquare P a)
=scalarInverseLimitWeight P (TGLV351.positiveSquare P (star a)).
Não depende da conclusão ainda DEV26. Semifinitude usual e o campo de minorantes do contrato continuam separados.

[REAL — fornecedores de perturbação examinados] BoundedPerturbationCocycle constrói cociclos de operadores limitados na torre; sua própria introdução marca Araki como analítico/não Lean. RelativeTomitaClosure usa TowerHilbert thirdThermalReference e filtro limitado invertível: não o peso ν no regularCore nem h⁻¹ sem gap. Seus padrões de transporte podem inspirar uma adaptação, mas nenhum é um exact para (**Q**) ou para o campo tracial deste candidato. A busca foi nominal e pelos tipos desses arquivos e da cadeia atual, não exaustiva no acervo inteiro.

Próximo alvo recomendado: compatibilidade (**Q**) no núcleo original, com escolha explícita da ponte modular que a prova; em seguida o adaptador do passo1–4. Não abrir predual, GNS novo ou nova definição de traço. Esta consulta não declara nenhum desses enunciados como teorema existente.


Leitura/pins: 2026-09-14T23:22:30.389311-03:00

Fornecedores principais (os enunciados completos e hashes lidos estão no JSON):

| Nome | Fonte/linha | Papel |
|---|---|---|
| scalarTomitaImaginaryPower_core_conjugation | [V351ScalarImaginaryCoreAction.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V351ScalarImaginaryCoreAction.lean:47>) | Covariância pelo grupo do Δν original, todo a. |
| scalarTomitaImaginaryPower | [V351ScalarTomitaImaginaryPowers.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V351ScalarTomitaImaginaryPowers.lean:24>) | Grupo definido pelo resolvente do S†S original. |
| scalarTomitaImaginaryPower_unique | [V351ScalarTomitaImaginaryPowers.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V351ScalarTomitaImaginaryPowers.lean:35>) | Unicidade somente mediante identidade amortecida, não mera covariância. |
| scalarTomitaImaginaryPower_polar_commutes | [V351ScalarTomitaImaginaryConjugation.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V351ScalarTomitaImaginaryConjugation.lean:14>) | J U_t = U_t J, com J antilinear original. |
| scalarTomitaPolarFactor_regular_left | [V350ScalarRegularRightPolar.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350ScalarRegularRightPolar.lean:113>) | Jπ(λ_t*)=R_t J, portanto Jπ(λ_t)J=R_-t. |
| regularRightGNS_intertwines | [V350ScalarRegularRightGNS.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350ScalarRegularRightGNS.lean:98>) | Ação direita na inscrição completa. |
| scalarWeightGNSAction_intertwines | [V350ScalarWeightAction.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350ScalarWeightAction.lean:38>) | Ação esquerda na inscrição completa. |
| scalarClosedTomita_graph_eq_weight | [V350ScalarWeightTomitaIdentification.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350ScalarWeightTomitaIdentification.lean:58>) | Mesmo S é o fecho do grafo do peso completo. |
| scalarWeightStar_mem_closedTomitaDomain | [V350ScalarWeightTomitaIdentification.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350ScalarWeightTomitaIdentification.lean:65>) | Domínio original para Λ(a), a no núcleo estrela do peso. |
| scalarClosedTomita_extends_weight_star | [V350ScalarWeightTomitaIdentification.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350ScalarWeightTomitaIdentification.lean:71>) | SΛ(a)=Λ(a*). |
| scalarTomitaPolarFactor_factorization | [V350ScalarTomitaPolarFactor.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350ScalarTomitaPolarFactor.lean:54>) | S=J√Δν no domínio completo original. |
| scalarTomitaPositiveRoot_domain_eq | [V350ScalarTomitaRootDomain.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350ScalarTomitaRootDomain.lean:51>) | Domínios √Δν e S coincidem. |
| scalarWeight_inverseCutoff_perturbed_norm | [V351PerturbedWeightNorm.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V351PerturbedWeightNorm.lean:37>) | Norma ponderada no mesmo Hν com J original. |
| scalarInverseLimitWeight | [V351InverseLimitWeight.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V351InverseLimitWeight.lean:87>) | Supremo de cortes atual; não suposto traço. |
| finiteDualStarCore_strongStar_approximation | [V350FiniteDualStarCore.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V350FiniteDualStarCore.lean:108>) | Sanduíches no núcleo, limite forte-* e cota uniforme. |
| regularInverseCutoffSqrt_commutes_average | [V351CutoffAverageCommutation.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V351CutoffAverageCommutation.lean:49>) | Comuta a raiz original do corte com a média. |
| scalarWeight_square_eq_iSup_averages | [V351WeightAverageRecovery.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V351_FECHO_MATEMATICO/RETOMADA_A1B_012/k/TGLExt/V351WeightAverageRecovery.lean:16>) | Modelo já compilado de Fatou, Haar e recuperação. |
