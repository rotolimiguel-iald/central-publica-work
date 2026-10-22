[REAL — 10 teoremas e 2 definições verificados no delta por reprodução isolada autoral e revisão independente. A1(b): traço concreto ainda OPEN.]

# ENTREGA 011 / A1 — A identidade direita forma uma álgebra fechada e atravessa o CFC

2026-09-14T21:08:03.742649-03:00

A propriedade sobre TODO nν é equivalente às equações dos cortes. Suas leis algébricas preservam a ordem inversa da ação direita; a álgebra exige explicitamente as propriedades de b e b*. O fechamento em norma é demonstrado pelas equações dos cortes. Sua imagem fechada no ambiente permite consumir cfc_mem, levando a identidade direita ao CFC ambientado, no mesmo core e com o mesmo J. Todas as translações regulares pertencem a essa álgebra.

O CFC é totalizado: a pertença vale inclusive no ramo padrão zero. Identificações espectrais dos consumidores exigem continuidade e normalidade efetivas. Este delta ainda não produz R_n, a ação de R ou sqrt(Bε), nem perturbação e tracialidade. A1(b) permanece aberto, sem mudança de gate.

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

Autor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\right_action_algebra_attempts\20260914_210203_478781\run.json`. Comando registrado: `['C:\\Users\\rotol\\.elan\\toolchains\\leanprover--lean4---v4.31.0\\bin\\lake.exe', 'build', 'TGLExt.AuditA1RightActionAlgebra']`. Fonte e objeto autorais abaixo. Reutilização somente de objetos próprios previamente produzidos na raiz isolada; os pacotes externos vêm do cache explicitado no relatório. Não é nova compilação integral da biblioteca.

Revisor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_algebra_direita\independent_20260914_210431_947693\run.json`. `661` objetos próprios anteriores; `0` fornecedores antigos recompilados adicionalmente. Zero objetos do autor/DEV herdados; `0` avisos de alvos/auditor. Avisos de fornecedores e diferenças binárias estão preservados em compilation.json. Comparação indisponível não significa igualdade.

As tentativas de desenvolvimento que falharam permanecem em disco. Só o fonte final, as reproduções rc0 e as auditorias aceitas entram nesta conclusão. Controle negativo de uma aplicação adulterada não é um teorema geral de inexistência.

## Fontes e objetos autorais

| Módulo | SHA256 fonte | SHA256 objeto |
|---|---|---|
| `V351ScalarRightActionAlgebra` | `68b1b9b84ba21c9c17de246fb69c8c48908e9ca313558b513322d119f66d98af` | `6df95ceec07c0c09d5626abad15921883c2beeddfc64c2671787226d5840491e` |

## Tipos completos e axiomas

```lean
TGLV350.Regular.ScalarPolarRight (P : TGLExt.SiteProfile)
  (b : ↥(VonNeumannAlgebra.toStarSubalgebra.{0} (TGLV350.Regular.regularCoreAlgebra P))) : Prop
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.scalarPolarRight_iff_cuts (P : TGLExt.SiteProfile)
  (b : ↥(VonNeumannAlgebra.toStarSubalgebra.{0} (TGLV350.Regular.regularCoreAlgebra P))) :
  TGLV350.Regular.ScalarPolarRight P b ↔
    ∀ (A : ↥(TGLV350.Regular.scalarWeightLeftIdeal P)) (n : ℕ),
      Eq.{1}
        ((TGLV350.Regular.scalarGNSCutMap P ↑n)
          ((TGLV350.Regular.antiunitaryConjugate (TGLV350.Regular.scalarTomitaPolarFactor P)
              ((TGLV350.Regular.scalarGNSRepresentation P) (star.{0} b)))
            ((TGLV350.Regular.scalarWeightGNSEmbedding P) A)))
        ((TGLV350.Regular.dualOrbitRepresentation (HMul.hMul.{0, 0, 0} ↑↑A ↑b)) (TGLV350.Regular.scalarCutVacuum P ↑n))
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.scalarPolarRight_zero (P : TGLExt.SiteProfile) : TGLV350.Regular.ScalarPolarRight P 0
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.scalarPolarRight_one (P : TGLExt.SiteProfile) : TGLV350.Regular.ScalarPolarRight P 1
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.scalarPolarRight_add (P : TGLExt.SiteProfile)
  (b c : ↥(VonNeumannAlgebra.toStarSubalgebra.{0} (TGLV350.Regular.regularCoreAlgebra P)))
  (hb : TGLV350.Regular.ScalarPolarRight P b) (hc : TGLV350.Regular.ScalarPolarRight P c) :
  TGLV350.Regular.ScalarPolarRight P (HAdd.hAdd.{0, 0, 0} b c)
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.scalarPolarRight_smul (P : TGLExt.SiteProfile)
  (b : ↥(VonNeumannAlgebra.toStarSubalgebra.{0} (TGLV350.Regular.regularCoreAlgebra P)))
  (hb : TGLV350.Regular.ScalarPolarRight P b) (c : ℂ) : TGLV350.Regular.ScalarPolarRight P (HSMul.hSMul.{0, 0, 0} c b)
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.scalarPolarRight_mul (P : TGLExt.SiteProfile)
  (b c : ↥(VonNeumannAlgebra.toStarSubalgebra.{0} (TGLV350.Regular.regularCoreAlgebra P)))
  (hb : TGLV350.Regular.ScalarPolarRight P b) (hc : TGLV350.Regular.ScalarPolarRight P c) :
  TGLV350.Regular.ScalarPolarRight P (HMul.hMul.{0, 0, 0} b c)
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.scalarPolarRightAlgebra (P : TGLExt.SiteProfile) :
  StarSubalgebra.{0, 0} ℂ ↥(VonNeumannAlgebra.toStarSubalgebra.{0} (TGLV350.Regular.regularCoreAlgebra P))
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.scalarPolarRight_isClosed (P : TGLExt.SiteProfile) :
  IsClosed.{0} (setOf.{0} fun b => TGLV350.Regular.ScalarPolarRight P b)
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.scalarPolarRightAlgebra_isClosed (P : TGLExt.SiteProfile) :
  IsClosed.{0} ↑(TGLV350.Regular.scalarPolarRightAlgebra P)
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.scalarPolarRightAlgebra_regular_mem (P : TGLExt.SiteProfile) (t : ℝ) :
  Membership.mem.{0, 0} (TGLV350.Regular.scalarPolarRightAlgebra P) (TGLV350.Regular.regularRightCoreElement P t)
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.scalarRightAction_cfc (P : TGLExt.SiteProfile)
  (b : ↥(VonNeumannAlgebra.toStarSubalgebra.{0} (TGLV350.Regular.regularCoreAlgebra P)))
  (hb : Membership.mem.{0, 0} (TGLV350.Regular.scalarPolarRightAlgebra P) b) (f : ℂ → ℂ) :
  ∃ (hf : Membership.mem.{0, 0} (TGLV350.Regular.regularCoreAlgebra P) (cfc.{0, 0} f ↑b)),
    Membership.mem.{0, 0} (TGLV350.Regular.scalarPolarRightAlgebra P) (Subtype.mk.{1} (cfc.{0, 0} f ↑b) hf)
```

Axiomas: propext, Classical.choice, Quot.sound.

## Custódia e limites

- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\AUDITORIA_ALGEBRA_ACAO_DIREITA_A1B.json` — SHA256 `0e9d2b7420662ab53f81a767e40f729f68b3dbc4bb8642fad928221769138db7`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_algebra_direita\REVIEW_A1_RIGHT_ACTION_ALGEBRA_FINAL.json` — SHA256 `ea8f57005bdbe95621d8d99944cc6541d7fc41ca0a2d253cb564a6c3609cefb2`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_algebra_direita\compilation.json` — SHA256 `ed8a1ce06af9070d34119e4b6041873729c1aca07e3c17544dd0456a48320285`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\ACEITE_DELTA_RIGHT_ACTION_ALGEBRA.json` — SHA256 `dca19821d301b28d4a919095fd689a5309ef13837386428b68c78467a0848b5e`.

O manifesto e o recibo próprios ligam esta entrega aos arquivos efetivamente lidos. Nenhum monólito canônico foi importado ou executado; nenhum dado experimental, D1, sigma, Atlas ou diário canônico foi alterado.

## Revisão independente integral

# Revisão independente — álgebra fechada da ação direita e CFC

2026-09-14T21:06:46.209115-03:00

**A1_RIGHT_ACTION_ALGEBRA_REVIEW_ACCEPTED__RESOLVENT_RIGHT_ACTION_TRACE_OPEN**

[REAL] Sem P0, P1 ou P2 no delta delimitado. 12 declarações (10 teoremas, 2 definições), relidas integralmente e reproduzidas pelo Lake próprio; #check com universos e #print axioms separados, somente propext/Classical.choice/Quot.sound.

[REAL] Delta de 12 declarações: dez teoremas e duas definições, ScalarPolarRight e scalarPolarRightAlgebra. Fonte e ficha MD/JSON lidas integralmente. O domínio é TODO scalarWeightLeftIdeal P, o peso e a inscrição GNS anteriores, com scalarTomitaPolarFactor P original. Não há novo GNS, novo operador J ou hipótese de traço.

[REAL] scalarPolarRight_iff_cuts é uma equivalência efetiva. No sentido direto usa a identidade já obtida de Λ(Ab) e scalarGNSCutMap_weight_embedding; no reverso os cortes naturais identificam o vetor previamente fixado Jπ(b*)J⁻¹Λ(A) por scalarWeightGNSEmbedding_of_cut_actions. Portanto a pertença Ab∈nν é concluída, não assumida como consequência de uma igualdade entre expressões indefinidas.

[REAL] As leis zero/um/soma/escala/produto têm a orientação correta. Na escala complexa as conjugações de b* e de J se cancelam. No produto, a aplicação de b a A antecede a de c a Ab: ρ(bc)=ρ(c)ρ(b), com ρ(b)=Jπ(b*)J⁻¹. A prova não comuta b e c. Provas de pertença ao ideal são transportadas por Subtype.ext, sem mudar o elemento subjacente.

[REAL] scalarPolarRightAlgebra exige EXPLICITAMENTE as duas propriedades, de b e de b*. A condição estrelada do produto usa c*b* nessa ordem. Assim star_mem é descarregada por involução da estrela; não se infere fechamento pela estrela de uma hipótese de ação direita unilateral. A unidade pertence à álgebra; scalarPolarRightAlgebra_regular_mem põe cada elemento regular λ_t na mesma álgebra usando o lema já reproduzido para t e −t. O empacotamento não é vazio ou meramente nominal.

[REAL] scalarPolarRight_isClosed demonstra continuidade na NORMA: π é 1-Lipschitz pela cota do operador ambiente e sua restrição; dualOrbitRepresentation é limitada por ||b||. As equações dos cortes são igualdades de mapas contínuos; sua interseção topológica sobre todo A e todo n é fechada. Isso não é uma interseção a.e. não enumerável, nem continuidade forte geral de star. A álgebra é a interseção dessa propriedade fechada com sua pré-imagem pela estrela contínua.

[REAL] scalarRightAction_cfc faz CFC no B(H_regular) AMBIENTE. O core é fechado por sua igualdade com o duplo centralizador e Set.isClosed_centralizer. Sua inclusão é um mapa fechado de subtipo; isso torna fechada a imagem da álgebra direita. O IsClosed local necessário a cfc_mem é provado, não postulado. Nenhuma instância CompleteSpace ou CFC do subtipo N é presumida. O elemento da imagem é transportado de volta pela igualdade de valores e injetividade de Subtype.val.

[REAL] O último enunciado recebe f:ℂ→ℂ sem hipótese de continuidade ou normalidade de b porque afirma pertença do cfc totalizado da Mathlib, que também vale no ramo padrão zero. Ele NÃO identifica por si a ação pontual de uma função arbitrária ou um cálculo espectral fora de suas hipóteses. Para os consumidores R_n e sqrt(Bε), continuidade no espectro, normalidade/auto-adjunção e igualdade com os operadores existentes continuam obrigações concretas. Esse alcance é compatível com a ficha.

[REAL] A ficha precede o código, aponta nove fornecedores e liga o empacotamento ao uso de cfc_mem para a ação dos cortes na perturbação do peso. Os pins desses fornecedores e da busca são confrontados aos bytes no finalizador. Quatro tentativas autorais rc1 foram preservadas e excluídas (20:46:24, 20:49:26, 20:52:33, 20:59:15); incluem falhas de elaboração/coerção, constante inexistente, timeout e prints com sorryAx. Somente 20260914_210039_263478 rc0 sem avisos é aceito. O histórico completo está em history_read.json; não se supõe que os pins dos fontes antigos correspondam ao fonte final.

[REAL] Auditoria autoral relida e pinada, sem reexecução: BadRightActionProductOrder troca star(b*c) por star(c*b), mantendo o produto Abc na esquerda, e falha por Type mismatch com imports válidos. Este resultado certifica a rejeição da adulteração testada, não uma alegação de contraexemplo numérico a toda comutatividade possível.

[REAL] Execução própria rc0 em 86.69 s. 661 objetos próprios anteriores preservados; 0 fornecedores antigos adicionais precisaram de reprodução de fonte, além dos módulos deste delta e auditor. Zero objetos autorais/de DEV herdados. Os pacotes externos são cache copiado e pinado da revisão própria anterior, sem recompilação nesta chamada; essa herança não é uma nova auditoria integral da biblioteca. 0 avisos de alvo/auditor; 178 mensagens de fornecedores registradas no JSON (inclui mensagens de objetos anteriores). O aviso de cache aesop com alterações locais, quando presente, permanece no stderr.

Pins lidos dos fontes e objetos próprios:

| Módulo | SHA256 fonte | SHA256 .olean próprio | Igual ao cold build autoral disponível |
|---|---|---|---|
| TGLExt.V351ScalarRightActionAlgebra | `68b1b9b84ba21c9c17de246fb69c8c48908e9ca313558b513322d119f66d98af` | `6df95ceec07c0c09d5626abad15921883c2beeddfc64c2671787226d5840491e` | True |

Comparações de bytes não são forçadas; objeto autoral ausente é comparação indisponível, não falha formal.

Controles: AUTHOR_CONTROLS_READ_AND_HASH_VERIFIED__TYPE_MISMATCH_NOT_ENVIRONMENT. A execução ou leitura correspondente está discriminada em compilation.json; nenhum controle autoral foi reexecutado por esta revisão.

[OPEN / limites] Nenhum aproximante R_n ou limite forte-* concreto é construído neste delta; não se conclui R∈scalarPolarRightAlgebra. A identificação racional do corte existente Bε e sua raiz, a ação desses cortes, a perturbação e a tracialidade permanecem abertas. Sem nova condição para gate, sem cobrança de minorantes para ν, sem atualização de memórias ou programas. Consultas CFC/seno e DCT são propostas separadas e não contam como teoremas compilados.

Artefatos próprios:

- [run](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_algebra_direita\independent_20260914_210431_947693\run.json>) — SHA256 `509a9b8b9f052c82ce231518c7230fe9a42b0dde6e474c74e89932d0498de1db`.
- [compilation](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_algebra_direita\compilation.json>) — SHA256 `ed8a1ce06af9070d34119e4b6041873729c1aca07e3c17544dd0456a48320285`.
- [tipos/axiomas](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_algebra_direita\independent_20260914_210431_947693\type_axiom_audit.json>) — SHA256 `35877c9a8cb9eecbc10dc09b3c48fae218c4d81c77d8f8d47c39db3ec295cb99`.


## Ficha/adendo integral: REAPROVEITAMENTO_A1B_ALGEBRA_ACAO_DIREITA

[OPEN — ficha anterior à passagem da ação direita por CFC]

# A1(b): a álgebra fechada que permite consumir cfc_mem

2026-09-14T20:43:21.434382-03:00

Construct a norm-closed star subalgebra of the EXISTING core, consisting of b and b* for which the actual original polar right identity holds on ALL n_nu. Characterize the property by the existing natural cut equations (of_cut_actions), so closedness follows from equality of continuous maps, without a new GNS or trace. Map this algebra by the same core inclusion into ambient bounded operators; the ambient image is closed since the core is a norm-closed bicommutant. Consume mathlib cfc_mem in the ambient CFC to pass the right identity to continuous functions. Consumer: (a) R_n=sigmoid(n sin(k/n)), with k determined by Lambda, to obtain the right action of actual R by bounded strong limits; (b) sqrt(B_epsilon) as an identified continuous function of R. Do not assume a CFC or CompleteSpace instance on N and do not claim that R_n convergence, identification of sqrt(B_epsilon), the trace or traciality are proved by this step.

O novo empacotamento algébrico tem consumidor preciso: cfc_mem exige uma subálgebra estrela fechada, e transportará a identidade direita já produzida. Não é nova realização do core ou novo operador. O fechamento GNS foi aceito; os limites da ação direita têm auditoria autoral rc0 e aguardam revisão neste instante.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarGNSClosedness.lean:35` — `13a1e9e22229c905922b94bc56c6fedc24dd80ea5072544934ffad2fa33e8bc8`

```lean
theorem scalarWeightGNSEmbedding_of_cut_actions (P : SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra) (v : ScalarGNSHilbert P)
    (hcut : ∀ n : ℕ, scalarGNSCutMap P (n : ℝ) v =
      dualOrbitRepresentation A.val (scalarCutVacuum P (n : ℝ))) :
    ∃ hA : A ∈ scalarWeightLeftIdeal P, scalarWeightGNSEmbedding P ⟨A,hA⟩ = v
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarGNSClosedness.lean:14` — `13a1e9e22229c905922b94bc56c6fedc24dd80ea5072544934ffad2fa33e8bc8`

```lean
theorem scalarGNSCutMap_weight_embedding (P : SiteProfile) (r : ℝ)
    (A : scalarWeightLeftIdeal P) :
    scalarGNSCutMap P r (scalarWeightGNSEmbedding P A) =
      dualOrbitRepresentation A.val.val (scalarCutVacuum P r)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarRightActionLimits.lean:15` — `ab55b5a1e05d6f8317bc61e0a303b960dc7e9888999e03cbb1c63287e4b37b9d`

```lean
theorem scalarRightAction_regular (P : SiteProfile) (t : ℝ)
    (A : scalarWeightLeftIdeal P) :
    scalarWeightGNSEmbedding P (scalarRegularRightProduct P t A) =
      antiunitaryConjugate (scalarTomitaPolarFactor P)
        (scalarGNSRepresentation P (star (regularRightCoreElement P t)))
          (scalarWeightGNSEmbedding P A)
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

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarGNSAction.lean:25` — `529982d9d3489dd900c8259599cede7cbf866525e4001e8196054679fae8f65a`

```lean
theorem scalarGNSAmbientAction_norm_le (P : SiteProfile)
    (B : (regularCoreAlgebra P).toStarSubalgebra) :
    ‖scalarGNSAmbientAction P B‖ ≤ ‖B.val‖
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350DualOrbitRepresentation.lean:14` — `01d61dbe3b2f4193dc48b345a1e765f017964a73a9e05070bf4e34e0510753dd`

```lean
def dualOrbitRepresentation : (RegularHilbert H →L[ℂ] RegularHilbert H) →⋆ₐ[ℂ]
    (RegularHilbert (RegularHilbert H) →L[ℂ] RegularHilbert (RegularHilbert H))
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350AntiunitaryPositiveConjugation.lean:28` — `83be0cf3f811bd6fd429c7705fdb1a00b27fdd6496ee971b9ca5f355c00d6f36`

```lean
theorem antiunitaryConjugate_mul (T V : H →L[ℂ] H) :
    antiunitaryConjugate U (T*V)=antiunitaryConjugate U T * antiunitaryConjugate U V
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Topology\Algebra\Group\Basic.lean:49` — `486110e92d9149d3a9fadef92c8f7d2cb5907fbe534452f88844996135f52526`

```lean
lemma Set.isClosed_centralizer {M : Type*} (s : Set M) [Mul M] [TopologicalSpace M]
    [SeparatelyContinuousMul M] [T2Space M] : IsClosed (centralizer s)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\CStarAlgebra\ContinuousFunctionalCalculus\Range.lean:96` — `07acc928827e7fafe0ac6baa7cea89010f8e74854cd2f77ba0d5314e1823c388`

```lean
lemma cfc_mem {𝕜' S : Type*} [Monoid 𝕜'] [MulAction 𝕜' A] [SetLike S A] [SubringClass S A]
    [SMul 𝕜 𝕜'] [IsScalarTower 𝕜 𝕜' A] [SMulMemClass S 𝕜' A] [StarMemClass S A] {s : S}
    [hs : IsClosed (s : Set A)] (f : 𝕜 → 𝕜) {a : A} (has : a ∈ s) :
    cfc f a ∈ s
```

Seis modalidades e outras bancadas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_right_action_algebra\20260914_204252_823508\searches.json. Ausência nominal nos recortes não é ausência universal.
