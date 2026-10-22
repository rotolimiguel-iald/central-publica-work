[REAL — 6 teoremas e 1 definições verificados no delta por reprodução isolada autoral e revisão independente. A1(b): traço concreto ainda OPEN.]

# ENTREGA 011 / A1 — Os cortes algébricos limitam a perturbação e aproximam a identidade

2026-09-14T23:15:30.796100-03:00

Uma definição q_delta=1-delta B_delta, seis teoremas públicos e quatro auxiliares privados. O corte pertence ao mesmo core e à álgebra polar direita, é uma contração positiva e comuta com os inversos B_epsilon. A identidade resolvente dá a cota B_epsilon q_delta²<=delta^-1 I, uniforme em epsilon. A densidade da imagem de 1-R e a equicontinuidade dos complementos estendem a convergência de q_(1/(n+1)) à identidade para todo vetor do mesmo Hilbert.

Não se afirma convergência em norma de operadores, inversa limitada de h ou gap espectral. Estes são fornecedores concretos da estimativa de domínio finito do peso limite; a densidade do seu domínio e a tracialidade ainda não são conclusões deste delta. Nenhuma raiz/GNS/representação alternativa, contrato completo ou mudança de gate.

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

Autor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\domain_cut_attempts\20260914_230828_363917\run.json`. Comando registrado: `['C:\\Users\\rotol\\.elan\\toolchains\\leanprover--lean4---v4.31.0\\bin\\lake.exe', 'build', 'TGLExt.AuditA1RegularDomainCut']`. Fonte e objeto autorais abaixo. Reutilização somente de objetos próprios previamente produzidos na raiz isolada; os pacotes externos vêm do cache explicitado no relatório. Não é nova compilação integral da biblioteca.

Revisor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_corte_dominio\independent_20260914_231000_688102\run.json`. `688` objetos próprios anteriores; `0` fornecedores antigos recompilados adicionalmente. Zero objetos do autor/DEV herdados; `0` avisos de alvos/auditor. Avisos de fornecedores e diferenças binárias estão preservados em compilation.json. Comparação indisponível não significa igualdade.

As tentativas de desenvolvimento que falharam permanecem em disco. Só o fonte final, as reproduções rc0 e as auditorias aceitas entram nesta conclusão. Controle negativo de uma aplicação adulterada não é um teorema geral de inexistência.

## Fontes e objetos autorais

| Módulo | SHA256 fonte | SHA256 objeto |
|---|---|---|
| `V351RegularDomainCut` | `60ed1575faca04fe95bb7fb208804944a84ac61114eede8ecbb28a67f9bed8e9` | `1e187bbe341f51e03141139fd48dc8d6c974b5aceedf87b2211c3e3616710b02` |

## Tipos completos e axiomas

```lean
TGLV350.Regular.regularDomainCut (P : TGLExt.SiteProfile) (δ : ℝ) :
  ↥(VonNeumannAlgebra.toStarSubalgebra.{0} (TGLV350.Regular.regularCoreAlgebra P))
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.regularDomainCut_right (P : TGLExt.SiteProfile) (δ : ℝ) (hδ : LT.lt.{0} 0 δ) :
  Membership.mem.{0, 0} (TGLV350.Regular.scalarPolarRightAlgebra P) (TGLV350.Regular.regularDomainCut P δ)
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.regularDomainCut_bounds (P : TGLExt.SiteProfile) (δ : ℝ) (hδ : LT.lt.{0} 0 δ) :
  LE.le.{0} 0 ↑(TGLV350.Regular.regularDomainCut P δ) ∧ LE.le.{0} (↑(TGLV350.Regular.regularDomainCut P δ)) 1
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.regularDomainCut_commutes (P : TGLExt.SiteProfile) (ε δ : ℝ) (hε : LT.lt.{0} 0 ε) (hδ : LT.lt.{0} 0 δ) :
  Commute.{0} (TGLV350.Regular.regularInverseGeneratorCutoff P ε) ↑(TGLV350.Regular.regularDomainCut P δ)
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.regularDomainCut_inverse_product (P : TGLExt.SiteProfile) (ε δ : ℝ) (hε : LT.lt.{0} 0 ε)
  (hδ : LT.lt.{0} 0 δ) :
  Eq.{1}
    (HMul.hMul.{0, 0, 0} (TGLV350.Regular.regularInverseGeneratorCutoff P ε) ↑(TGLV350.Regular.regularDomainCut P δ))
    (HSub.hSub.{0, 0, 0} (TGLV350.Regular.regularInverseGeneratorCutoff P δ)
      (HSMul.hSMul.{0, 0, 0} (↑ε)
        (HMul.hMul.{0, 0, 0} (TGLV350.Regular.regularInverseGeneratorCutoff P δ)
          (TGLV350.Regular.regularInverseGeneratorCutoff P ε))))
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.regularDomainCut_product_bound (P : TGLExt.SiteProfile) (ε δ : ℝ) (hε : LT.lt.{0} 0 ε)
  (hδ : LT.lt.{0} 0 δ) :
  LE.le.{0}
    (HMul.hMul.{0, 0, 0}
      (HMul.hMul.{0, 0, 0} (TGLV350.Regular.regularInverseGeneratorCutoff P ε) ↑(TGLV350.Regular.regularDomainCut P δ))
      ↑(TGLV350.Regular.regularDomainCut P δ))
    (HSMul.hSMul.{0, 0, 0} (Inv.inv.{0} ↑δ) 1)
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.regularDomainCut_tendsto_identity (P : TGLExt.SiteProfile)
  (v : ↥(TGLV350.Regular.RegularHilbert (TGLExt.TowerHilbert P))) :
  Filter.Tendsto.{0, 0}
    (fun n => ↑(TGLV350.Regular.regularDomainCut P (HDiv.hDiv.{0, 0, 0} 1 (HAdd.hAdd.{0, 0, 0} (↑n) 1))) v)
    Filter.atTop.{0} (nhds.{0} v)
```

Axiomas: propext, Classical.choice, Quot.sound.

## Custódia e limites

- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\AUDITORIA_CORTE_DOMINIO_A1B.json` — SHA256 `1188962c1cfaf892e15eb4bb48652c9d4eadff6a4847b9b2eddde6412d4190ac`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_corte_dominio\REVIEW_A1_DOMAIN_CUT_FINAL.json` — SHA256 `06490e09974ffb1caec795f4ace19a66aebea6614d6978646a4ac075f7df7b2a`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_corte_dominio\compilation.json` — SHA256 `97e4c7b0aa9f929c8dff0d904e30bfdf4bbbd6740e01c4b887f2730d4530985e`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\ACEITE_DELTA_DOMAIN_CUT.json` — SHA256 `6eb4e71e554a22aac64b82cbeec014d8a63d984b0ad45f6e2c94258d2f32119b`.

O manifesto e o recibo próprios ligam esta entrega aos arquivos efetivamente lidos. Nenhum monólito canônico foi importado ou executado; nenhum dado experimental, D1, sigma, Atlas ou diário canônico foi alterado.

## Revisão independente integral

# Revisão independente — corte de domínio regular

2026-09-14T23:14:04.550675-03:00

**A1_DOMAIN_CUT_REVIEW_ACCEPTED__LIMIT_WEIGHT_SEMIFINITE_TRACIAL_OPEN**

[REAL] **Sem achados P0/P1/P2.** Seis teoremas públicos + uma definição, quatro helpers privados. Módulo completo e auditor próprios rc0; sete #check com universos e axiomas exclusivamente do trio permitido. Aceite delimitado ao enunciado efetivamente compilado.

[REAL — objeto e hipóteses] Sete declarações públicas: regularDomainCut é uma definição no MESMO (regularCoreAlgebra P).toStarSubalgebra; seguem seis teoremas. qδ=1−δBδ usa exatamente regularInverseGeneratorCutoff P δ. A definição é total em δ, mas pertença à álgebra de ação direita, positividade e cotas exigem δ>0; identidades que envolvem Bε exigem também ε>0. Não se introduziu outra realização de h, raiz ou GNS.

[REAL — produto e ordem] A positividade de qδ vem de Bδ≤δ⁻¹I e multiplicação pelo escalar REAL positivo δ; qδ≤I vem de Bδ≥0. A comutação com Bε é deduzida da comutação dos cortes existentes. A identidade Bεqδ=Bδ−εBδBε usa a identidade resolvente antiga, sem divisão por δ−ε e portanto também vale quando os reguladores coincidem. O helper genérico prova Bq²≤Bq por positividade de (Bq)(1−q), demonstrando a comutação necessária. Depois Bεqδ≤Bδ≤δ⁻¹I. Não há multiplicação de desigualdade por operadores não comutantes; a constante depende somente de δ, uniforme em todo ε>0.

[REAL — convergência forte] No mesmo RegularHilbert(TowerHilbert P), R é regularSpectralResolvent P, S=1−R e Dn=δnBδn, δn=1/(n+1). O código prova Dn S=δn R qδn e ||Dn(Sy)||≤δn||y||. A imagem de S é densa pelo fornecedor antigo bounded_graph_domain_dense, cujo domínio é definicionalmente Ran(S), usando S auto-adjunto e a injetividade de 1−R já entregue. As contrações Dn são uniformemente 1-Lipschitz; Equicontinuous.isClosed_setOf_tendsto estende o limite zero da imagem densa a TODO vetor. Finalmente qδn v=v−Dn v→v. Não se troca ponto a ponto por norma de operadores, nem se assume inversa limitada de S ou gap.

[REAL — auxiliares e reuso] Os quatro helpers privados são hilbert_positive_smul, hilbert_contract_norm, hilbert_positive_product e hilbert_commuting_contract_product, todos em Hilbert complexo genérico completo. Suas premissas de positividade/comutação são explicitamente satisfeitas na especialização; o auditor público cobre seus axiomas transitivos. A norma usa CStarAlgebra.norm_le_norm_of_nonneg_of_le e ContinuousLinearMap.norm_id_le, que não exigem que o espaço seja não trivial. As 14 entradas da ficha e os três recortes do adendo foram confrontados com fontes/linhas/pins; as interfaces futuras de finitude/WOT são somente consumidoras previstas, não resultados deste módulo. Em particular V351ScalarWeightSemifiniteness foi lido/pinado em K para a ficha, mas não está na dependência fechada deste delta nem em V; não foi reproduzido nesta revisão.

[REAL — cronologia e evidência] Ficha 23:03:13 e adendo 23:03:55 antecedem a primeira tentativa 23:05:46. Essa tentativa rc1 foi preservada e excluída: o stream mostra norm_one_le ausente, reescrita de produtos, instância CFC concreta, coerção do subtipo e meta final não resolvida. O DEV final 23:07:09 é rc0 sem avisos. Pins históricos apontam para snapshots reais dos respectivos DEV; o caminho vivo antigo fica apenas como localização textual. O autor standalone e o auditor7 passaram; a sonda BadDomainCutProductReversed inverte ≤ e falha por Type mismatch, com imports válidos. O negativo foi relido/pinado, não reexecutado.

[REAL — proveniência] 688 objetos próprios anteriores preservados; construídos somente alvo e auditor, total 690. Nenhum fornecedor antigo recompilado neste delta; cache de pacotes pinado e herdado, sem nova auditoria integral da biblioteca. LEAN_PATH dos traces contém somente V e seus pacotes, nenhum build autoral ou DEV. Run próprio rc0 em 44.423 s; zero avisos do alvo/auditor e 178 mensagens de fornecedores com origem separada no JSON. O stderr preserva ainda o aviso do cache aesop com alterações locais, já presente na base; não é aviso do alvo. A contagem total de jobs do Lake não significa recompilação dessa quantidade de objetos.

| Artefato | SHA256 lido |
|---|---|
| Fonte final (K=cópia própria) | 60ed1575faca04fe95bb7fb208804944a84ac61114eede8ecbb28a67f9bed8e9 |
| .olean próprio | 1e187bbe341f51e03141139fd48dc8d6c974b5aceedf87b2211c3e3616710b02 |
| .olean autoral standalone, apenas comparação | 1e187bbe341f51e03141139fd48dc8d6c974b5aceedf87b2211c3e3616710b02 |

Igualdade binária medida: True.

[OPEN — limites] Delta25 somente: seis teoremas públicos, uma definição, quatro helpers privados transitivos; nenhum fornecedor antigo novo precisou ser construído neste delta. ε>0 e δ>0 nas afirmações de produto; a convergência cobre todo vetor do MESMO Hilbert e a sequência δn=1/(n+1). A cota δ⁻¹ é uniforme em ε, não em δ. Não demonstra norma-operador qδn→I, gap, finitude de (a qδ)*a qδ no peso limite, densidade WOT desse ideal, semifinitude usual ou tracialidade. Esses consumidores permanecem OPEN. O peso/contrato anteriores não são redefinidos, e nenhuma condição do gate ou memória é alterada. O campo autoral sobre ação da raiz é herança do delta CFC aceito, não teorema novo deste arquivo. Objetos próprios anteriores e cache de pacotes reutilizados com pins; nenhum objeto de projeto autoral/DEV usado, nenhum monólito/writer/recorder executado; parecer24 e todos os anteriores intactos.

Artefatos de evidência:

- [compilation](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_corte_dominio\compilation.json>) — SHA256 97e4c7b0aa9f929c8dff0d904e30bfdf4bbbd6740e01c4b887f2730d4530985e.
- [run próprio](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_corte_dominio\independent_20260914_231000_688102\run.json>) — SHA256 a45c0881f1b3a65b8014347d6d01800168e5f2182b8a711c62d6053d2419e7a6.
- [tipos/axiomas](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_corte_dominio\independent_20260914_231000_688102\type_axiom_audit.json>) — SHA256 773a008dbe5af6dbfa24e8c5034668f10390e3826347e34c6ccd6a10066d2269.
- [histórico](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_corte_dominio\history_read.json>) — SHA256 5d23ef305d210eca4048e95647ffc558642e223d10ad068afe56b7eb98a40a26.
- [fornecedores da ficha](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_corte_dominio\provider_checks.json>) — SHA256 90f956066aebb6f1cf6325bd231192bfc0c679549afd81fd4e0a4f7da1c02db5.


## Ficha/adendo integral: REAPROVEITAMENTO_A1B_CORTE_DOMINIO_LIMITE

[OPEN — ficha anterior ao corte de domínio do peso limite]

# A1(b): corte algébrico sem outra raiz

2026-09-14T23:03:13.391858-03:00

Use q_delta=1-delta*B_delta, in the SAME regular core and polar right algebra. Prove positivity/contraction, the uniform product bound B_epsilon*q_delta^2 <= delta^(-1)*I and strong convergence q_(1/(n+1)) to I. Reuse the inverse identity, positivity of commuting products and dense range of 1-R. Consumers: finite-domain cutoff estimate of scalarInverseLimitWeight and WOT density of its square-finite set. This fiche covers that sequential route; it does not assert any new theorem or semifinal contract. No new root, spectral calculus, GNS, traciality or positive finite minorants of the original nontracial weight.

ADAPTAR a rota menor q_delta da consulta independente revisao_consulta_semifinitude_limite/CONSULTA_SEMIFINITUDE_LIMITE. A cota pode depender de delta, mas deve ser uniforme em epsilon antes do supremo. Semifinitude usual e minorantes positivos do contrato são obrigações distintas.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseGeneratorCutoff.lean:24` — `f615a4a8b80a4bf970c719aa9d44fd2d917eb52f01fa1c925cfcab8151adc227`

```lean
theorem regularInverseGeneratorCutoff_nonneg (P : SiteProfile) (ε : ℝ) (hε : 0 < ε) :
    0 ≤ regularInverseGeneratorCutoff P ε
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseGeneratorCutoff.lean:31` — `f615a4a8b80a4bf970c719aa9d44fd2d917eb52f01fa1c925cfcab8151adc227`

```lean
theorem regularInverseGeneratorCutoff_le (P : SiteProfile) (ε : ℝ) (hε : 0 < ε) :
    regularInverseGeneratorCutoff P ε ≤
      (ε⁻¹ : ℂ) • (1 : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P))
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseGeneratorCutoff.lean:43` — `f615a4a8b80a4bf970c719aa9d44fd2d917eb52f01fa1c925cfcab8151adc227`

```lean
theorem regularInverseGeneratorCutoff_one (P : SiteProfile) :
    regularInverseGeneratorCutoff P 1 = regularSpectralResolvent P
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegulatorWeightOrder.lean:22` — `b908f79a4d20ca8f456eb245e2a605a6cc6e611667e1c8a8d6cb1cee2ee4f838`

```lean
theorem regularInverseGeneratorCutoff_commutes (P : SiteProfile)
    (ε η : ℝ) (hε : 0 < ε) (hη : 0 < η) :
    Commute (regularInverseGeneratorCutoff P ε) (regularInverseGeneratorCutoff P η)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegulatorWeightOrder.lean:29` — `b908f79a4d20ca8f456eb245e2a605a6cc6e611667e1c8a8d6cb1cee2ee4f838`

```lean
theorem regularInverseGeneratorCutoff_resolvent_identity (P : SiteProfile)
    (ε η : ℝ) (hε : 0 < ε) (hη : 0 < η) :
    regularInverseGeneratorCutoff P ε - regularInverseGeneratorCutoff P η =
      ((η-ε : ℝ) : ℂ) • (regularInverseGeneratorCutoff P η * regularInverseGeneratorCutoff P ε)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseCutoffCFC.lean:94` — `cbdf10aea749a552b0f47afb3ef59560ed47d6f46cf7dd8064dc963a092c3490`

```lean
theorem regularInverseGeneratorCutoff_right (P : SiteProfile) (ε : ℝ) (hε : 0 < ε) :
    (⟨regularInverseGeneratorCutoff P ε,regularInverseGeneratorCutoff_mem P ε⟩ :
      (regularCoreAlgebra P).toStarSubalgebra) ∈ scalarPolarRightAlgebra P
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarRightActionAlgebra.lean:94` — `68b1b9b84ba21c9c17de246fb69c8c48908e9ca313558b513322d119f66d98af`

```lean
def scalarPolarRightAlgebra (P : SiteProfile) :
    StarSubalgebra ℂ (regularCoreAlgebra P).toStarSubalgebra
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularPositiveGraph.lean:104` — `d56ea107302802ee76d65a3c32c69be9fe41cddb4901a65486ab7f1bfb345390`

```lean
theorem regularSpectralResolvent_complement_injective (P : SiteProfile) :
    Function.Injective (1-regularSpectralResolvent P :
      RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P))
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\BoundedGraphOperator.lean:118` — `4d70d27d25f31fed13b73a7ae60601478718e41bbc38c24c38117b0cc26dc84f`

```lean
theorem bounded_graph_domain_dense [CompleteSpace E] (A B : E →L[ℂ] E) (hAi : Function.Injective A)
    (hA : IsSelfAdjoint A) :
    Dense ((boundedGraphOperator A B hAi).domain : Set E)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Topology\UniformSpace\Equicontinuity.lean:980` — `dd3e8de0798b50489e45f0e117af17473290e2e1c1fc26218e7beccd3cdce692`

```lean
theorem Equicontinuous.isClosed_setOf_tendsto {l : Filter ι} {F : ι → X → α} {f : X → α}
    (hF : Equicontinuous F) (hf : Continuous f) :
    IsClosed {x | Tendsto (F · x) l (𝓝 (f x))}
```

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

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarWeightSemifiniteness.lean:16` — `f5e7e85b034949be6517286f60c692d3d97d29c341aeba42a1f7172b7e610c2a`

```lean
theorem scalarWeight_square_finite_wot_closure (P : SiteProfile) :
    closure {A : RegularHilbert (TowerHilbert P) →WOT[ℂ]
        RegularHilbert (TowerHilbert P) |
      A.toCLM ∈ regularCoreAlgebra P ∧ HasFiniteScalarSquare P A.toCLM} =
    {A : RegularHilbert (TowerHilbert P) →WOT[ℂ]
        RegularHilbert (TowerHilbert P) | A.toCLM ∈ regularCoreAlgebra P}
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350RegularNormality.lean:19` — `bcd49e92800bf99d7770bb9969879be02a9768f129ce842ae2f39cefaca3cc0a`

```lean
theorem strong_tendsto_wot {ι : Type*} {l : Filter ι}
    (T : ι → (H →L[ℂ] H)) (B : H →L[ℂ] H)
    (hstrong : ∀ v, Tendsto (fun i => T i v) l (𝓝 (B v))) :
    Tendsto (fun i => ContinuousLinearMapWOT.ofCLM (T i)) l
      (𝓝 (ContinuousLinearMapWOT.ofCLM B))
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350RegularTopology.lean:39` — `13c92b1d8948bc4d2c3891d4cbfa9bf43ac353a95e9126e2c128b1379db0ebd5`

```lean
theorem regularCore_wot_closed (P : TGLExt.SiteProfile) :
    IsClosed {A : RegularHilbert (TGLExt.TowerHilbert P) →WOT[ℂ]
      RegularHilbert (TGLExt.TowerHilbert P) | A.toCLM ∈ regularCoreAlgebra P}
```

Seis modalidades e outras bancadas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_domain_cut\20260914_230247_301032\searches.json. Ausência nominal nos recortes não é ausência universal.


## Ficha/adendo integral: ADENDO_FICHA_CORTE_DOMINIO_ROTA

[OPEN — rota e APIs antes do código]

2026-09-14T23:03:55.306868-03:00

Use q_delta directly. The first module supplies bounded contractions, membership/right action, inverse-product bound and strong convergence. The next consumer applies the existing right-perturbed weight comparison and WOT closure. This splits algebraic/operator estimates from the scalar finiteness proof, not duplicate definitions. No new root.

Consulta lida integralmente: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_consulta_semifinitude_limite\CONSULTA_SEMIFINITUDE_LIMITE.md

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Topology\MetricSpace\UniformConvergence.lean:94 — 01ed18a99a0f7b7183c033776cddfcd198c3e9b9000809d4c7572d6436c63e3a

```lean
/-- If `f : α → γ → β` is a family of a functions, all of which are Lipschitz with the
same constant, then the family is uniformly equicontinuous. -/
lemma _root_.LipschitzWith.uniformEquicontinuous (f : α → γ → β) (K : ℝ≥0)
    (h : ∀ c, LipschitzWith K (f c)) : UniformEquicontinuous f := by
  rw [uniformEquicontinuous_iff_uniformContinuous]
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Topology\MetricSpace\Lipschitz.lean:45 — eccab81f2b1ff62fdc7dccd4753a2f83dd2725cccabe2cc6e98e6a97147a6eb9

```lean
theorem lipschitzWith_iff_dist_le_mul [PseudoMetricSpace α] [PseudoMetricSpace β] {K : ℝ≥0}
    {f : α → β} : LipschitzWith K f ↔ ∀ x y, dist (f x) (f y) ≤ K * dist x y := by
  simp only [LipschitzWith, edist_nndist, dist_nndist]
  norm_cast

alias ⟨LipschitzWith.dist_le_mul, LipschitzWith.of_dist_le_mul⟩ := lipschitzWith_iff_dist_le_mul

```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\SpecificLimits\Basic.lean:69 — dbbeb301e5b9dacc96ecd233fd05a02846a1fc88c9606f1b1d413d08aff5142e

```lean
theorem tendsto_one_div_add_atTop_nhds_zero_nat {𝕜 : Type*} [DivisionSemiring 𝕜] [CharZero 𝕜]
    [TopologicalSpace 𝕜] [ContinuousSMul ℚ≥0 𝕜] :
    Tendsto (fun n : ℕ ↦ 1 / ((n : 𝕜) + 1)) atTop (𝓝 0) :=
  suffices Tendsto (fun n : ℕ ↦ 1 / (↑(n + 1) : 𝕜)) atTop (𝓝 0) by simpa
  (tendsto_add_atTop_iff_nat 1).2 tendsto_one_div_atTop_nhds_zero_nat

theorem tendsto_algebraMap_inv_atTop_nhds_zero_nat {𝕜 : Type*} (A : Type*)
```

