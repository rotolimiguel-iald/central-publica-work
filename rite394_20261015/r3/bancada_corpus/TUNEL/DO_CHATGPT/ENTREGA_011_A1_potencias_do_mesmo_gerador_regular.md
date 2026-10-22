[REAL — 4 teoremas e 0 definições verificados no delta por reprodução isolada autoral e revisão independente. A1(b): traço concreto ainda OPEN.]

# ENTREGA 011 / A1 — As potências do mesmo gerador são o grupo regular inteiro

2026-09-14T20:00:13.470025-03:00

A fase do resolvente sigmoid(2πξ), o CFC pontual e a imagem densa do amortecimento identificam resolventImaginaryPower com os caracteres negativos. V=W F⁻¹ transporta esses caracteres para Λ_t. O teorema final vale para todo SiteProfile, tempo e vetor, usando o MESMO R=(1+h)⁻¹, com suas condições de positividade e injetividade provadas. Nenhuma definição nova iguala grupos por decreto; h não é confundido com o operador modular do peso no GNS.

Esta entrega identifica h^it=Λ_t através da construção por resolvente. Afiliação e escala dual são obrigações separadas; a construção do traço ainda não está concluída.

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

Autor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\regular_powers_attempts\20260914_193359_191807\run.json`. Comando registrado: `['C:\\Users\\rotol\\.elan\\toolchains\\leanprover--lean4---v4.31.0\\bin\\lake.exe', 'build', 'TGLExt.AuditA1RegularPowers']`. Fonte e objeto autorais abaixo. Reutilização somente de objetos próprios previamente produzidos na raiz isolada; os pacotes externos vêm do cache explicitado no relatório. Não é nova compilação integral da biblioteca.

Revisor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_potencias\independent_20260914_195640_056744\run.json`. `644` objetos próprios anteriores; `0` fornecedores antigos recompilados adicionalmente. Zero objetos do autor/DEV herdados; `0` avisos de alvos/auditor. Avisos de fornecedores e diferenças binárias estão preservados em compilation.json. Comparação indisponível não significa igualdade.

As tentativas de desenvolvimento que falharam permanecem em disco. Só o fonte final, as reproduções rc0 e as auditorias aceitas entram nesta conclusão. Controle negativo de uma aplicação adulterada não é um teorema geral de inexistência.

## Fontes e objetos autorais

| Módulo | SHA256 fonte | SHA256 objeto |
|---|---|---|
| `V351RegularImaginaryPowers` | `066b9cb14426365807ead587ca90ad28e3703a0f9efc0ce359519da7c5243b9a` | `392ec0633d892ed00901a5b5ac2d6c4b6e1a10a8d5093fb324b9622dd3182cc2` |

## Tipos completos e axiomas

```lean
TGLV350.Regular.resolventPhaseFunction_sigmoid (t a : ℝ) :
  Eq.{1} (TGLV350.Regular.resolventPhaseFunction t a.sigmoid)
    (HMul.hMul.{0, 0, 0} (↑(TGLV350.Regular.resolventDamping a.sigmoid)) (ChatgptAudit.modularPhase t (Neg.neg.{0} a)))
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.sigmoidMultiplier_imaginaryPower {H : Type} [NormedAddCommGroup.{0} H] [InnerProductSpace.{0, 0} ℂ H]
  [CompleteSpace.{0} H]
  (T :
    ContinuousLinearMap.{0, 0, 0, 0} (RingHom.id.{0} ℂ) ↥(TGLV350.Regular.RegularHilbert H)
      ↥(TGLV350.Regular.RegularHilbert H))
  (hT :
    Eq.{1} T
      (TGLV350.Regular.realScalarMultiplier (fun ξ => (HMul.hMul.{0, 0, 0} (HMul.hMul.{0, 0, 0} 2 Real.pi) ξ).sigmoid) ⋯
        ⋯ ⋯))
  (h0 : LE.le.{0} 0 T) (h1 : LE.le.{0} T 1) (hi : Function.Injective.{1, 1} ⇑T)
  (hj : Function.Injective.{1, 1} ⇑(HSub.hSub.{0, 0, 0} 1 T)) (t : ℝ) (u : ↥(TGLV350.Regular.RegularHilbert H)) :
  Eq.{1} ((TGLV350.Regular.resolventImaginaryPower T h0 h1 hi hj t) u)
    ((TGLV350.Regular.characterMultiplier (HMul.hMul.{0, 0, 0} (HMul.hMul.{0, 0, 0} 2 Real.pi) t)) u)
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.regularSpectralCoordinates_character (P : TGLExt.SiteProfile) (t : ℝ)
  (u : ↥(TGLV350.Regular.RegularHilbert (TGLExt.TowerHilbert P))) :
  Eq.{1}
    ((TGLV350.Regular.regularSpectralCoordinates P)
      ((TGLV350.Regular.characterMultiplier (HMul.hMul.{0, 0, 0} (HMul.hMul.{0, 0, 0} 2 Real.pi) t)) u))
    ((TGLV350.Regular.regularUnitary P t) ((TGLV350.Regular.regularSpectralCoordinates P) u))
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.regularPositiveGenerator_imaginaryPower (P : TGLExt.SiteProfile) (t : ℝ)
  (u : ↥(TGLV350.Regular.RegularHilbert (TGLExt.TowerHilbert P))) :
  Eq.{1} ((TGLV350.Regular.resolventImaginaryPower (TGLV350.Regular.regularSpectralResolvent P) ⋯ ⋯ ⋯ ⋯ t) u)
    ((TGLV350.Regular.regularUnitary P t) u)
```

Axiomas: propext, Classical.choice, Quot.sound.

## Custódia e limites

- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\AUDITORIA_POTENCIAS_REGULARES_A1B.json` — SHA256 `7daecd69d2da33ba9805924bdbc35f1730d922127c48a4063cb4d8c4fb766874`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_potencias\REVIEW_A1_REGULAR_POWERS_FINAL.json` — SHA256 `cc54acde48d220e406898c896ba76acf9805e2776e27a1c4681114fa2907b0b3`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_potencias\compilation.json` — SHA256 `e9c33584fa841df8e817c7e68f2f87634f2f52eaf5a99bbaa70af7d037c4d98d`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\ACEITE_DELTA_POWERS.json` — SHA256 `5a116e980376f2e7ea10ae26610a7167e1af99b0a434266e556de220f5dd3172`.

O manifesto e o recibo próprios ligam esta entrega aos arquivos efetivamente lidos. Nenhum monólito canônico foi importado ou executado; nenhum dado experimental, D1, sigma, Atlas ou diário canônico foi alterado.

## Revisão independente integral

# Revisão independente — potências do gerador regular existente

2026-09-14T19:58:07.113285-03:00

**A1_REGULAR_POWERS_REVIEW_ACCEPTED__AFFILIATION_TRACE_OPEN**

[REAL] Sem P0, P1 ou P2 no delta delimitado. 4 declarações (4 teoremas, 0 definições), relidas integralmente e reproduzidas pelo Lake próprio; #check com universos e #print axioms separados, somente propext/Classical.choice/Quot.sound.

[REAL] A fonte inteira e a ficha foram confrontadas com resolventImaginaryPower, seu lema de amortecimento e seu transporte por entrelaçamento, já reproduzidos. O delta contém quatro teoremas e nenhuma definição: não substitui o grupo de potências por uma definição igual a regularUnitary.

[REAL] O cálculo log((1−sigmoid a)/sigmoid a)=−a dá a fase de sinal negativo. Com a convenção characterPhase(s,ξ)=exp(−i s ξ), modularPhase(t,−2πξ) é precisamente characterPhase(2πt,ξ). O controle de tempo oposto testa essa distinção.

[REAL] sigmoidMultiplier_imaginaryPower exige explicitamente T igual ao multiplicador, positividade, T≤1 e injetividade de T e 1−T. No teorema final essas condições são provadas para o multiplicador e para regularSpectralResolvent; hT é descarregada por rfl. A igualdade é primeiro estabelecida na imagem densa do amortecimento T(1−T), usando CFC pontual e somente eventos AE finitos, e estendida pela continuidade dos operadores limitados. Não se inverte o amortecimento como operador limitado.

[REAL] V=W·Fourier⁻¹ é a coordenada existente. Fourier/shift e W·shift·W*=regularUnitary dão V·character=regularUnitary·V. O entrelaçamento R·V=V·M e resolventImaginaryPower_intertwines transportam as potências para o mesmo R. O resultado final vale para todo SiteProfile, t e vetor, sem antecedente adicional de identificação.

[REAL] regularPositiveGenerator continua sendo o grafo resolvente de R=(1+h)⁻¹, com identificação exponencial já aceita separadamente. Neste sentido preciso, o teorema identifica as potências construídas por esse resolvente com a família regular inteira. Não identifica h com o operador modular do peso, nem troca a ação esquerda regular por um implementador GNS por homonímia.

[REAL] Execução própria rc0 em 37.91 s. 644 objetos próprios anteriores preservados; 0 fornecedores antigos adicionais precisaram de reprodução de fonte, além dos módulos deste delta e auditor. Zero objetos autorais/de DEV herdados. Os pacotes externos são cache copiado e pinado da revisão própria anterior, sem recompilação nesta chamada; essa herança não é uma nova auditoria integral da biblioteca. 0 avisos de alvo/auditor; 178 mensagens de fornecedores registradas no JSON (inclui mensagens de objetos anteriores). O aviso de cache aesop com alterações locais, quando presente, permanece no stderr.

Pins lidos dos fontes e objetos próprios:

| Módulo | SHA256 fonte | SHA256 .olean próprio | Igual ao cold build autoral disponível |
|---|---|---|---|
| TGLExt.V351RegularImaginaryPowers | `066b9cb14426365807ead587ca90ad28e3703a0f9efc0ce359519da7c5243b9a` | `392ec0633d892ed00901a5b5ac2d6c4b6e1a10a8d5093fb324b9622dd3182cc2` | True |

Comparações de bytes não são forçadas; objeto autoral ausente é comparação indisponível, não falha formal.

Controles: AUTHOR_CONTROLS_READ_AND_HASH_VERIFIED__TYPE_MISMATCH_NOT_ENVIRONMENT. A execução ou leitura correspondente está discriminada em compilation.json; nenhum controle autoral foi reexecutado por esta revisão.

[OPEN / limites] Aceite separado dos quatro teoremas, herdando explicitamente as provas anteriores do resolvente e de seu grupo. Afiliação, escala dual e traço não são conclusões deste delta; nenhuma promoção de gate ou alteração de memória. O negativo autoral de t→−t é apenas relido com pins e diagnóstico de elaboração; não há alegação de nova execução desse controle pelo revisor.

Artefatos próprios:

- [run](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_potencias\independent_20260914_195640_056744\run.json>) — SHA256 `afa1bfdaeaf2023814a956139fad94bca032a4ee7554e4ac872334a5b3c8f0ee`.
- [compilation](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_potencias\compilation.json>) — SHA256 `e9c33584fa841df8e817c7e68f2f87634f2f52eaf5a99bbaa70af7d037c4d98d`.
- [tipos/axiomas](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_potencias\independent_20260914_195640_056744\type_axiom_audit.json>) — SHA256 `e3d7adb5ac13798a5449ae7d85e29a3f1743db57047993d6ec07189e280363e6`.


## Ficha/adendo integral: REAPROVEITAMENTO_A1B_POTENCIAS_REGULARES

[OPEN — ficha anterior à identificação das potências do mesmo gerador regular]

# A1(b): as potências existentes geram Λ_t

2026-09-14T19:28:18.315946-03:00

For every SiteProfile P,t and x on the actual regular Hilbert space: resolventImaginaryPower (regularSpectralResolvent P), with its already proved positive contraction and injectivity certificates, maps x exactly to regularUnitary P t x. Prove from CFC on the sigmoid multiplier, damping density, existing resolvent intertwining, Fourier and absorption. Do not define a replacement imaginary-power group equal to Lambda by decree. Affiliation, dual scaling and trace remain distinct obligations.

A identificação usa exatamente resolventImaginaryPower e regularSpectralResolvent. Não há novo grupo definido como Λ_t; o grafo fechado anterior é h=(1−R)/R. Os módulos predecessores permanecem intactos.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarMultiplierCalculus.lean:73` — `4dfa6cbd81aa481d695c2eec89985eb06487e7ba32432528d06c62ee7147f06c`

```lean
theorem realScalarMultiplier_cfc_ae (g : ℝ → ℝ) (hg : Continuous g)
    (h0 : ∀ x, 0 ≤ g x) (h1 : ∀ x, g x ≤ 1)
    (f : ℂ → ℂ) (hf : Continuous f) (u : RegularHilbert H) :
    cfc f (realScalarMultiplier g hg h0 h1) u =ᵐ[volume]
      fun x => f (g x : ℂ) • u x
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ResolventImaginaryPowers.lean:38` — `0cfc297376410ff6bd259eeaf921a9d6e6ca47829b5d389c6b5c30bf4c5accf5`

```lean
def resolventImaginaryPower (t : ℝ) : H ≃ₗᵢ[ℂ] H
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ResolventImaginaryPowers.lean:45` — `0cfc297376410ff6bd259eeaf921a9d6e6ca47829b5d389c6b5c30bf4c5accf5`

```lean
theorem resolventImaginaryPower_damping (t : ℝ) (x : H) :
    resolventImaginaryPower T hT h1 hi hj t (resolventDampingOperator T x)=
      resolventPhaseOperator T t x
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ResolventImaginaryPowers.lean:20` — `0cfc297376410ff6bd259eeaf921a9d6e6ca47829b5d389c6b5c30bf4c5accf5`

```lean
theorem resolventDampingOperator_denseRange : DenseRange (resolventDampingOperator T)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ResolventImaginaryIntertwining.lean:64` — `789f68095379e02a203191b258c359787c12b24c1282f34d39835dc5347c76d5`

```lean
theorem resolventImaginaryPower_intertwines (T Q R : H →L[ℂ] H)
    (hT : 0 ≤ T) (h1T : T ≤ 1) (hiT : Function.Injective T)
    (hjT : Function.Injective (1-T : H →L[ℂ] H))
    (hQ : 0 ≤ Q) (h1Q : Q ≤ 1) (hiQ : Function.Injective Q)
    (hjQ : Function.Injective (1-Q : H →L[ℂ] H)) (h : T*R=R*Q)
    (t : ℝ) (x : H) :
    resolventImaginaryPower T hT h1T hiT hjT t (R x) =
      R (resolventImaginaryPower Q hQ h1Q hiQ hjQ t x)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ResolventPhaseCalculus.lean:18` — `cd207e3a21c50f65fe3b199e201b2b148a0d98fc2e3a3cf7e40a80e61ba4f818`

```lean
theorem resolventDampingOperator_cfc (T : H →L[ℂ] H) (hT : IsSelfAdjoint T) :
    cfc (fun z : ℂ => (resolventDamping z.re : ℂ)) T = resolventDampingOperator T
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351FourierTranslation.lean:47` — `a0fe8f689855aebeefcc6d1d1a7ece3314bf5dcd65d74017569597dd7df1a9b2`

```lean
theorem fourier_shift (t : ℝ) (f : RegularHilbert H) :
    Lp.fourierTransformₗᵢ ℝ H (shift t f) =
      characterMultiplier (2 * Real.pi * t) (Lp.fourierTransformₗᵢ ℝ H f)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularFlowAbsorption.lean:60` — `4760792d98c8d625e9109bd7d0b2a97713bd236dcb7d6db1a4f07251cdc0c9f9`

```lean
theorem regularUnitary_shift_conjugate (P : SiteProfile) (t : ℝ) :
    (regularFlowAbsorptionUnitary P).val * shift t *
        star (regularFlowAbsorptionUnitary P).val = regularUnitary P t
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularPositiveGraph.lean:78` — `d56ea107302802ee76d65a3c32c69be9fe41cddb4901a65486ab7f1bfb345390`

```lean
def regularSpectralResolvent (P : SiteProfile) :
    RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P)
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

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350L2CharacterMultiplier.lean:98` — `2f7c413ee9ebd5ba93d1222bb596da11972a0b6b4efa1a71a04becb6ff856ca3`

```lean
theorem characterMultiplier_ae (s : ℝ) (f : RegularHilbert H) :
    characterMultiplier s f =ᵐ[volume]
      fun x : ℝ => Complex.exp (-Complex.I * (s : ℂ) * (x : ℂ)) • f x
```

Seis modalidades e outras bancadas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_regular_powers\20260914_192752_671120\searches.json. Ausência nominal nos recortes não é ausência universal.
