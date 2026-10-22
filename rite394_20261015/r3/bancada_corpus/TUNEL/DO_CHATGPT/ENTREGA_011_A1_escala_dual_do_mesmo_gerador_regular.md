[REAL — 7 teoremas e 0 definições verificados no delta por reprodução isolada autoral e revisão independente. A1(b): traço concreto ainda OPEN.]

# ENTREGA 011 / A1 — A escala dual conserva o domínio do mesmo gerador regular

2026-09-14T20:11:45.322378-03:00

Fourier inversa e translação dão a lei F C_s=S_(-s/(2π)) F em todo L². O campo operador que define W comuta com caracteres escalares; V=W F⁻¹ transforma C_s na mesma translação espectral. No grafo existente h=e^(-2πξ), isso prova h C_s=e^s C_s h. A equivalência, usando também −s, inclui a igualdade de domínios e dá Ad(C_s)h=e^(-s)h. Nenhum gerador, grupo ou objeto afiliado novo é definido.

Esta entrega paga a escala dual do gerador regular e preserva todas as entregas anteriores. Ainda não constrói o traço da perturbação por h⁻¹ nem um habitante de RegularCoreTraceData. A1(b) completo permanece aberto.

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

Autor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\regular_dual_scaling_attempts\20260914_200223_782189\run.json`. Comando registrado: `['C:\\Users\\rotol\\.elan\\toolchains\\leanprover--lean4---v4.31.0\\bin\\lake.exe', 'build', 'TGLExt.AuditA1RegularDualScaling']`. Fonte e objeto autorais abaixo. Reutilização somente de objetos próprios previamente produzidos na raiz isolada; os pacotes externos vêm do cache explicitado no relatório. Não é nova compilação integral da biblioteca.

Revisor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_escala_dual\independent_20260914_200357_657003\run.json`. `648` objetos próprios anteriores; `0` fornecedores antigos recompilados adicionalmente. Zero objetos do autor/DEV herdados; `0` avisos de alvos/auditor. Avisos de fornecedores e diferenças binárias estão preservados em compilation.json. Comparação indisponível não significa igualdade.

As tentativas de desenvolvimento que falharam permanecem em disco. Só o fonte final, as reproduções rc0 e as auditorias aceitas entram nesta conclusão. Controle negativo de uma aplicação adulterada não é um teorema geral de inexistência.

## Fontes e objetos autorais

| Módulo | SHA256 fonte | SHA256 objeto |
|---|---|---|
| `V351RegularGeneratorDualScaling` | `2bd647d5a4c6526780853e16b5ef1ee8f1acddc36570ebdcdc8d74f230e08d50` | `b8e254850037cebfa3129f551c2068b2bfb875b37d97d4961dc5d385d014ebc2` |

## Tipos completos e axiomas

```lean
TGLV350.Regular.fourierInv_shift_schwartz {H : Type} [NormedAddCommGroup.{0} H] [InnerProductSpace.{0, 0} ℂ H]
  [CompleteSpace.{0} H] (t : ℝ) (f : SchwartzMap.{0, 0} ℝ H) :
  Eq.{1}
    (FourierTransformInv.fourierInv.{0, 0}
      ((TGLV350.Regular.shift t) (SchwartzMap.toLp.{0, 0} f 2 MeasureTheory.volume.{0})))
    ((TGLV350.Regular.characterMultiplier (Neg.neg.{0} (HMul.hMul.{0, 0, 0} (HMul.hMul.{0, 0, 0} 2 Real.pi) t)))
      (FourierTransformInv.fourierInv.{0, 0} (SchwartzMap.toLp.{0, 0} f 2 MeasureTheory.volume.{0})))
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.fourierInv_shift {H : Type} [NormedAddCommGroup.{0} H] [InnerProductSpace.{0, 0} ℂ H]
  [CompleteSpace.{0} H] (t : ℝ) (f : ↥(TGLV350.Regular.RegularHilbert H)) :
  Eq.{1}
    ((LinearIsometryEquiv.symm.{0, 0, 0, 0} (MeasureTheory.Lp.fourierTransformₗᵢ.{0, 0} ℝ H))
      ((TGLV350.Regular.shift t) f))
    ((TGLV350.Regular.characterMultiplier (Neg.neg.{0} (HMul.hMul.{0, 0, 0} (HMul.hMul.{0, 0, 0} 2 Real.pi) t)))
      ((LinearIsometryEquiv.symm.{0, 0, 0, 0} (MeasureTheory.Lp.fourierTransformₗᵢ.{0, 0} ℝ H)) f))
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.fourier_characterMultiplier {H : Type} [NormedAddCommGroup.{0} H] [InnerProductSpace.{0, 0} ℂ H]
  [CompleteSpace.{0} H] (s : ℝ) (f : ↥(TGLV350.Regular.RegularHilbert H)) :
  Eq.{1} ((MeasureTheory.Lp.fourierTransformₗᵢ.{0, 0} ℝ H) ((TGLV350.Regular.characterMultiplier s) f))
    ((TGLV350.Regular.shift (HDiv.hDiv.{0, 0, 0} (Neg.neg.{0} s) (HMul.hMul.{0, 0, 0} 2 Real.pi)))
      ((MeasureTheory.Lp.fourierTransformₗᵢ.{0, 0} ℝ H) f))
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.operatorFieldLift_commutes_character {H : Type} [NormedAddCommGroup.{0} H]
  [InnerProductSpace.{0, 0} ℂ H] [CompleteSpace.{0} H] (F : TGLV350.StrongIntegral.Family) (s : ℝ) :
  Eq.{1} (HMul.hMul.{0, 0, 0} (TGLV350.Regular.operatorFieldLift F) (TGLV350.Regular.characterMultiplier s))
    (HMul.hMul.{0, 0, 0} (TGLV350.Regular.characterMultiplier s) (TGLV350.Regular.operatorFieldLift F))
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.regularSpectralCoordinates_dual (P : TGLExt.SiteProfile) (s : ℝ)
  (x : ↥(TGLV350.Regular.RegularHilbert (TGLExt.TowerHilbert P))) :
  Eq.{1}
    ((LinearIsometryEquiv.symm.{0, 0, 0, 0} (TGLV350.Regular.regularSpectralCoordinates P))
      ((TGLV350.Regular.characterMultiplier s) x))
    ((TGLV350.Regular.shift (HDiv.hDiv.{0, 0, 0} (Neg.neg.{0} s) (HMul.hMul.{0, 0, 0} 2 Real.pi)))
      ((LinearIsometryEquiv.symm.{0, 0, 0, 0} (TGLV350.Regular.regularSpectralCoordinates P)) x))
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.regularPositiveGenerator_dual_graph (P : TGLExt.SiteProfile) (s : ℝ)
  (x y : ↥(TGLV350.Regular.RegularHilbert (TGLExt.TowerHilbert P)))
  (hxy :
    Membership.mem.{0, 0} (LinearPMap.graph.{0, 0, 0} (TGLV350.Regular.regularPositiveGenerator P))
      (Prod.mk.{0, 0} x y)) :
  Membership.mem.{0, 0} (LinearPMap.graph.{0, 0, 0} (TGLV350.Regular.regularPositiveGenerator P))
    (Prod.mk.{0, 0} ((TGLV350.Regular.characterMultiplier s) x)
      (HSMul.hSMul.{0, 0, 0} (↑(Real.exp s)) ((TGLV350.Regular.characterMultiplier s) y)))
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.regularPositiveGenerator_dual_scaling (P : TGLExt.SiteProfile) (s : ℝ)
  (x y : ↥(TGLV350.Regular.RegularHilbert (TGLExt.TowerHilbert P))) :
  Membership.mem.{0, 0} (LinearPMap.graph.{0, 0, 0} (TGLV350.Regular.regularPositiveGenerator P)) (Prod.mk.{0, 0} x y) ↔
    Membership.mem.{0, 0} (LinearPMap.graph.{0, 0, 0} (TGLV350.Regular.regularPositiveGenerator P))
      (Prod.mk.{0, 0} ((TGLV350.Regular.characterMultiplier s) x)
        (HSMul.hSMul.{0, 0, 0} (↑(Real.exp s)) ((TGLV350.Regular.characterMultiplier s) y)))
```

Axiomas: propext, Classical.choice, Quot.sound.

## Custódia e limites

- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\AUDITORIA_ESCALA_DUAL_REGULAR_A1B.json` — SHA256 `dccec3972522c4e1229f4cf3ace471881f75ea409a75225c1508ff07ea816fc3`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_escala_dual\REVIEW_A1_REGULAR_DUAL_SCALING_FINAL.json` — SHA256 `b3ff3bbeb889c8e0a3f87a49c678603d2fcfffcdeaca30f35e3113c80c6dbef6`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_escala_dual\compilation.json` — SHA256 `2ea267f0889505291e68b38bd92772fe94f66ef845957aa7f0dbf9fb47733454`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\ACEITE_DELTA_DUAL_SCALING.json` — SHA256 `1d46ef0d09be9bf712fde579eee807b42d84ea3015171b9f72f6b8dbb89b3a71`.

O manifesto e o recibo próprios ligam esta entrega aos arquivos efetivamente lidos. Nenhum monólito canônico foi importado ou executado; nenhum dado experimental, D1, sigma, Atlas ou diário canônico foi alterado.

## Revisão independente integral

# Revisão independente — escala dual do gerador regular

2026-09-14T20:09:36.682572-03:00

**A1_REGULAR_DUAL_SCALING_REVIEW_ACCEPTED__TRACE_OPEN**

[REAL] Sem P0, P1 ou P2 no delta delimitado. 7 declarações (7 teoremas, 0 definições), relidas integralmente e reproduzidas pelo Lake próprio; #check com universos e #print axioms separados, somente propext/Classical.choice/Quot.sound.

[REAL] Delta único: V351RegularGeneratorDualScaling, sete teoremas, nenhuma definição. Ficha e adendo foram lidos integralmente; seus fornecedores são verificados por bytes. As oito entregas anteriores são base reutilizada e permanecem preservadas, sem somar seus alvos a este aceite.

[REAL] Convenções verificadas: Fourier inversa transporta shift(t) para characterMultiplier(−2πt); Fourier transporta characterMultiplier(s) para shift(−s/(2π)). A primeira prova usa SchwartzMap.fourierInv_coe explicitamente, a passagem ao L² usa densidade e continuidade de operadores limitados. Não há hipótese de separabilidade de H nem interseção a.e. não enumerável.

[REAL] operatorFieldLift_commutes_character decorre de linearidade complexa ponto a ponto e eventos a.e. finitos. A aplicação usa o V=WF⁻¹ já construído, no mesmo espaço regular, e não supõe W∈N. regularSpectralCoordinates_dual produz V⁻¹C_s=shift(−s/(2π))V⁻¹.

[REAL] O grafo é o mesmo regularPositiveGenerator. A translação das coordenadas exp(−2πξ) dá h C_s x=e^s C_s h x para todo x no domínio. A implicação inversa usa −s, characterMultiplier_inverse e e^(−s)e^s=1. Assim a igualdade de domínios é efetiva e a leitura de conjugação é Ad(C_s)h=e^(−s)h. Não se supõe domínio total, inversa limitada de h, gap, ou uma nova identificação espectral.

[REAL] Histórico relido: DEV 19:55:13 rc1 contém erro de change/coerção de Fourier inversa, erro de simplificação e sorryAx; está excluído. DEV 19:59:17 é rc0 COM um aviso de tática inútil; não foi contado como rc1 nem usado como fonte final. O candidato 20:00:33 é rc0 sem avisos. history_read.json registra os streams e a correção de uma expectativa preliminar incorreta do revisor sobre essa contagem, sem repetir compilação.

[DECLARADO / documentação conferida] A primeira preparação da ficha usou caminho de fornecedor inexistente; a ficha registra correção para V350StrongOperatorField antes do código. Isto é falha de preparação, não negativo matemático. O adendo explicita o fornecedor SchwartzMap.fourierInv_coe. A busca foi delimitada: não alego exaustividade do acervo.

[REAL] O controle autoral BadRegularDualScalingSign foi relido com hashes de fonte/streams: substituir e^s por e^(−s) na segunda componente do grafo produz Type mismatch, com imports válidos. Esta revisão executou seu próprio Lake e auditor; não reexecutou o negativo autoral.

[REAL] Execução própria rc0 em 40.66 s. 648 objetos próprios anteriores preservados; 0 fornecedores antigos adicionais precisaram de reprodução de fonte, além dos módulos deste delta e auditor. Zero objetos autorais/de DEV herdados. Os pacotes externos são cache copiado e pinado da revisão própria anterior, sem recompilação nesta chamada; essa herança não é uma nova auditoria integral da biblioteca. 0 avisos de alvo/auditor; 178 mensagens de fornecedores registradas no JSON (inclui mensagens de objetos anteriores). O aviso de cache aesop com alterações locais, quando presente, permanece no stderr.

Pins lidos dos fontes e objetos próprios:

| Módulo | SHA256 fonte | SHA256 .olean próprio | Igual ao cold build autoral disponível |
|---|---|---|---|
| TGLExt.V351RegularGeneratorDualScaling | `2bd647d5a4c6526780853e16b5ef1ee8f1acddc36570ebdcdc8d74f230e08d50` | `b8e254850037cebfa3129f551c2068b2bfb875b37d97d4961dc5d385d014ebc2` | True |

Comparações de bytes não são forçadas; objeto autoral ausente é comparação indisponível, não falha formal.

Controles: AUTHOR_CONTROLS_READ_AND_HASH_VERIFIED__TYPE_MISMATCH_NOT_ENVIRONMENT. A execução ou leitura correspondente está discriminada em compilation.json; nenhum controle autoral foi reexecutado por esta revisão.

[OPEN / limites] A escala dual do mesmo grafo é aceita neste delta. Não há construção de τ, prova de tracialidade ou pagamento de A1(b) completo. A proposta posterior de cortes por escala dual é consulta separada, não alvo Lean destes sete teoremas. Nenhum monólito, recorder, memória, fonte autoral ou relatório anterior foi alterado; nenhuma promoção de gate.

Artefatos próprios:

- [run](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_escala_dual\independent_20260914_200357_657003\run.json>) — SHA256 `342135140bdc78277949e3298a8a4c957f44a773d1d615b59fcee33cd16d39e2`.
- [compilation](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_escala_dual\compilation.json>) — SHA256 `2ea267f0889505291e68b38bd92772fe94f66ef845957aa7f0dbf9fb47733454`.
- [tipos/axiomas](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_escala_dual\independent_20260914_200357_657003\type_axiom_audit.json>) — SHA256 `e3edab754647b23f719d36ae0b2278c4a186bc4d49c15d7717e065a6066103e3`.


## Ficha/adendo integral: REAPROVEITAMENTO_A1B_ESCALA_DUAL_REGULAR

[OPEN — ficha anterior à escala dual do mesmo gerador regular]

# A1(b): transformação do domínio e do grafo

2026-09-14T19:53:41.130187-03:00

Prove dual scaling of the SAME existing closed regular positive generator h: (x,y) in graph h iff (C_s x, exp(s) C_s y) in graph h, equivalently theta_s(h)=exp(-s)h with theta_s=Ad(C_s). Reuse V=W F^-1, the exact spectral graph e^(-2pi xi), operatorFieldLift and Fourier translation. Add inverse Fourier translation and Fourier modulation only as consumed lemmas; do not create another Fourier transform, group, generator or affiliated object. Domain transformation must be proved, not just formal exponentials. The inverse-generator trace is separate.

A convenção C_s(x)=exp(-isx) dá F C_s = S_(-s/(2pi)) F. Portanto h C_s=exp(s) C_s h e Ad(C_s)h=exp(-s)h. O sinal será conferido pela identidade de grafos e por controle adulterado. Nenhum traço é definido nesta etapa.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351FourierTranslation.lean:14` — `a0fe8f689855aebeefcc6d1d1a7ece3314bf5dcd65d74017569597dd7df1a9b2`

```lean
theorem shift_schwartz_toLp (t : ℝ) (f : 𝓢(ℝ, H)) :
    shift t (f.toLp 2) = (f.compSubConstCLM ℂ t).toLp 2
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351FourierTranslation.lean:26` — `a0fe8f689855aebeefcc6d1d1a7ece3314bf5dcd65d74017569597dd7df1a9b2`

```lean
theorem fourier_shift_schwartz (t : ℝ) (f : 𝓢(ℝ, H)) :
    𝓕 (shift t (f.toLp 2)) =
      characterMultiplier (2 * Real.pi * t) (𝓕 (f.toLp 2))
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\Fourier\FourierTransform.lean:475` — `96d179f52654504228b5f536ed5076fbe33f2e1ddd333bfda576c7ffef88324a`

```lean
lemma fourierInv_eq_fourier_neg (f : V → E) (w : V) :
    𝓕⁻ f w = 𝓕 f (-w)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\Fourier\LpSpace.lean:111` — `82b647b1998edea8d60ac8f986fd5735d697044e586464a05d71d0a346522cfe`

```lean
theorem SchwartzMap.toLp_fourierInv_eq (f : 𝓢(E, F)) : 𝓕⁻ (f.toLp 2) = (𝓕⁻ f).toLp 2
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350L2CharacterMultiplier.lean:98` — `2f7c413ee9ebd5ba93d1222bb596da11972a0b6b4efa1a71a04becb6ff856ca3`

```lean
theorem characterMultiplier_ae (s : ℝ) (f : RegularHilbert H) :
    characterMultiplier s f =ᵐ[volume]
      fun x : ℝ => Complex.exp (-Complex.I * (s : ℂ) * (x : ℂ)) • f x
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350L2CharacterMultiplier.lean:124` — `2f7c413ee9ebd5ba93d1222bb596da11972a0b6b4efa1a71a04becb6ff856ca3`

```lean
theorem characterMultiplier_inverse (s : ℝ) (f : RegularHilbert H) :
    characterMultiplier s (characterMultiplier (-s) f) = f
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350StrongOperatorField.lean:68` — `83fcc9ee4e6cdecee9f130183b7d1e6a0e2436caf40670e4d64dce8933f86a4c`

```lean
theorem operatorFieldLift_ae (F : StrongIntegral.Family (H := H)) (f : RegularHilbert H) :
    operatorFieldLift F f =ᵐ[volume] fun x : ℝ => F.op x (f x)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularPositiveGraph.lean:72` — `d56ea107302802ee76d65a3c32c69be9fe41cddb4901a65486ab7f1bfb345390`

```lean
def regularSpectralCoordinates (P : SiteProfile) :
    RegularHilbert (TowerHilbert P) ≃ₗᵢ[ℂ] RegularHilbert (TowerHilbert P)
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

Seis modalidades e outras bancadas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_regular_dual_scaling\20260914_195057_334158\searches.json. Ausência nominal nos recortes não é ausência universal.


## Ficha/adendo integral: ADENDO_FICHA_ESCALA_DUAL

[REAL — fornecedor de coerção localizado durante elaboração]

2026-09-14T20:01:26.234405-03:00

Fourier inversa de Schwartz não é definição redutível da integral inversa; fourierInv_coe é a ponte já existente. O primeiro DEV falhou visivelmente no change. Nenhum novo alvo, objeto ou hipótese.

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\Distribution\SchwartzSpace\Fourier.lean:118 — a0e9969eb2c71ec922cd48614748cd9b741d992d2d54e9712eeeeab07455c741

```lean
lemma fourierInv_coe (f : 𝓢(V, E)) : 𝓕⁻ f = 𝓕⁻ (f : V → E)
```

A primeira preparação da ficha terminou com erro de caminho V350OperatorFieldLift.lean. As sete buscas já concluídas foram preservadas e conferidas; finish_regular_dual_scaling_fiche.py terminou a ficha com o caminho real V350StrongOperatorField.lean, antes da criação do alvo. Não houve repetição da busca nem sucesso presumido.
