[REAL — 3 teoremas e 0 definições verificados no delta por reprodução isolada autoral e revisão independente. A1(b): traço concreto ainda OPEN.]

# ENTREGA 011 / A1 — As raízes dos cortes comutam com as médias originais

2026-09-14T22:15:20.767060-03:00

Três teoremas públicos, um auxiliar privado e zero definições. O mesmo resolvente R comuta com regularUnitary por suas coordenadas espectrais e a lei dos caracteres; CFC e a raiz original transportam a comutação para sqrt(Bε), ε>0. O integral orientado que define regularAverage transfere a identidade às médias para todo δ real, incluindo zero. Nenhuma nova realização, raiz ou média foi construída. O P2 de localizador CFC foi corrigido ao lado, com preservação da ficha e do parecer histórico; a revisão V2 encerrou o achado sem recompilação.

O resultado não afirma comutação de todo membro da álgebra direita com as médias. A extensão da ordem dos valores perturbados a todos os positivos é o próximo consumidor. Traço completo e tracialidade continuam abertos; nenhum gate ou monólito é alterado.

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

Autor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\cutoff_average_commutation_attempts\20260914_220459_834157\run.json`. Comando registrado: `['C:\\Users\\rotol\\.elan\\toolchains\\leanprover--lean4---v4.31.0\\bin\\lake.exe', 'build', 'TGLExt.AuditA1CutoffAverageCommutation']`. Fonte e objeto autorais abaixo. Reutilização somente de objetos próprios previamente produzidos na raiz isolada; os pacotes externos vêm do cache explicitado no relatório. Não é nova compilação integral da biblioteca.

Revisor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_comutacao_cortes_medias\independent_20260914_220558_290545\run.json`. `674` objetos próprios anteriores; `0` fornecedores antigos recompilados adicionalmente. Zero objetos do autor/DEV herdados; `0` avisos de alvos/auditor. Avisos de fornecedores e diferenças binárias estão preservados em compilation.json. Comparação indisponível não significa igualdade.

As tentativas de desenvolvimento que falharam permanecem em disco. Só o fonte final, as reproduções rc0 e as auditorias aceitas entram nesta conclusão. Controle negativo de uma aplicação adulterada não é um teorema geral de inexistência.

## Fontes e objetos autorais

| Módulo | SHA256 fonte | SHA256 objeto |
|---|---|---|
| `V351CutoffAverageCommutation` | `bc881ee5df7e027859ef14d7379b27bc9c2a27bea3b08cf42d6604805afa2a66` | `93d331fab3cea3f6b87e159ff5237f010a9cd98c0f36f8e974010d1544b1cc8d` |

## Tipos completos e axiomas

```lean
TGLV350.Regular.regularSpectralResolvent_commutes_regular (P : TGLExt.SiteProfile) (t : ℝ) :
  Commute.{0} (TGLV350.Regular.regularSpectralResolvent P) (TGLV350.Regular.regularUnitary P t)
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.regularInverseCutoffSqrt_commutes_regular (P : TGLExt.SiteProfile) (ε : ℝ) (hε : LT.lt.{0} 0 ε)
  (t : ℝ) :
  Commute.{0} (TGLV350.Regular.hilbertPositiveSqrt (TGLV350.Regular.regularInverseGeneratorCutoff P ε))
    (TGLV350.Regular.regularUnitary P t)
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.regularInverseCutoffSqrt_commutes_average (P : TGLExt.SiteProfile) (ε : ℝ) (hε : LT.lt.{0} 0 ε)
  (δ : ℝ) :
  Commute.{0} (TGLV350.Regular.hilbertPositiveSqrt (TGLV350.Regular.regularInverseGeneratorCutoff P ε))
    (TGLV350.Regular.regularAverage P δ)
```

Axiomas: propext, Classical.choice, Quot.sound.

## Custódia e limites

- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\AUDITORIA_COMUTACAO_CORTES_MEDIAS_A1B.json` — SHA256 `57ce44712c1b3f14bde4a2ea6a55296f856a97a8c7afe1a775ca706094e9137e`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_comutacao_cortes_medias\REVIEW_A1_CUTOFF_AVERAGE_COMMUTATION_FINAL_V2.json` — SHA256 `22ca3dca484de8e61e8b3660a765a125171d1280885d26ef605fbad4d31e9047`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_comutacao_cortes_medias\compilation_v2.json` — SHA256 `dd0c49b6ce2e47e19e2de7d10f08cd082e2a62bae43b2eecc5f84e88e0e42eb2`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\ACEITE_DELTA_CUTOFF_AVERAGE_COMMUTATION.json` — SHA256 `aa17849e88a0288073a87abe6e4095156732ebe9250b220a5569258140620e3f`.

O manifesto e o recibo próprios ligam esta entrega aos arquivos efetivamente lidos. Nenhum monólito canônico foi importado ou executado; nenhum dado experimental, D1, sigma, Atlas ou diário canônico foi alterado.

## Revisão independente integral

# Revisão independente V2 — comutação de cortes e médias

2026-09-14T22:13:54.020466-03:00

**A1_CUTOFF_AVERAGE_COMMUTATION_REVIEW_ACCEPTED__ALL_POSITIVE_WEIGHT_ORDER_TRACE_OPEN**

[REAL] **Sem P0, P1 ou P2 pendente. P2-CFC-PROVIDER-LOCATOR encerrado.** Três teoremas públicos + um helper privado, zero definições. Esta V2 preserva integralmente o parecer/compilation anteriores e reaproveita o Lake e auditor próprios rc0; nenhuma recompilação foi executada para a correção documental.

[REAL — realização e sinal] O primeiro alvo usa exatamente regularSpectralCoordinates P, o multiplicador por sigmoid e o caráter de parâmetro +2πt. A comutação com todos os caracteres é descarregada pela lei aditiva existente. character_commutation_realScalarMultiplier fornece M C=C M, e o transporte pela equivalência estrela de V entrega o MESMO R e regularUnitary P t, sem hipótese residual nem nova transformação espectral.

[REAL — CFC e raiz] R≥0 fornece IsSelfAdjoint para commute_cfc; a igualdade já provada Bε=cfc(fε)(R), sob ε>0, identifica o corte original. O helper hilbertPositiveSqrt_commutes é genérico em Hilbert complexa completa e consome Commute.cfcₙ_nnreal NNReal.sqrt com as instâncias do wrapper antigo. Nenhuma raiz nova é definida. O helper foi relido e compilado; seus axiomas entram transitivamente nos prints dos alvos públicos, sem alegar #print privado separado.

[REAL — integral e domínio] A última identidade vale para TODO δ real, inclusive zero e negativo; somente ε>0 é exigido. regularAverage_apply mantém δ⁻¹ e o integral orientado de 0 a δ. O CLM B comuta com o escalar e atravessa o integral por intervalIntegral_comp_comm, usado na orientação inversa. A integrabilidade é descarregada pela continuidade forte de λ_t em cada vetor. Integral_congr usa a comutação pontual já provada; nenhuma continuidade em norma do grupo, separabilidade ou seleção de eventos a.e. sobre conjunto não enumerável foi pressuposta.

[REAL — histórico e negativo] A tentativa DEV 220259_446252 rc1 permanece excluída: a reescrita procurava o lado errado do lema de integral. A final 220350_353915 rc0 coincide com a fonte reproduzida, sem avisos; maxHeartbeats 1600000 está explícito. A auditoria autoral standalone e os streams foram relidos com pins. O negativo insere sinal menos na conclusão e é recusado por Type mismatch, com imports resolvidos; não foi reexecutado nesta revisão. A recusa não exclui coincidências especiais, como δ=0.

[REAL — P2 encerrado] A correção MD/JSON foi lida integralmente e confrontada com Commute.lean nas árvores K e V, byte a byte iguais: IsSelfAdjoint.commute_cfc, linha 87, enunciado exato. O adendo histórico permanece intacto e a correção declara ser posterior ao código. O fornecedor Commute.cfcₙ_nnreal permanece inalterado. Nenhuma fonte, objeto ou run Lean foi alterado; esta V2 apenas encerra o achado documental e inclui sua evidência.

[REAL — reprodução herdada] 674 objetos próprios anteriores preservados; somente módulo e auditor acrescentados (total 676). Nenhum objeto autoral/DEV herdado, nenhum fornecedor antigo reconstruído. Pacotes externos: cache pinado da reprodução anterior. O run próprio original concluiu rc0 em 38.387 s, zero avisos do alvo/auditor, trio propext/Classical.choice/Quot.sound com #check de universos. As 178 mensagens históricas de fornecedores e stderr permanecem no compilation.

| Artefato | SHA256 lido |
|---|---|
| Fonte final inalterada | `bc881ee5df7e027859ef14d7379b27bc9c2a27bea3b08cf42d6604805afa2a66` |
| .olean próprio inalterado | `93d331fab3cea3f6b87e159ff5237f010a9cd98c0f36f8e974010d1544b1cc8d` |
| .olean cold autoral, comparação somente | `93d331fab3cea3f6b87e159ff5237f010a9cd98c0f36f8e974010d1544b1cc8d` |

Igualdade binária medida: True.

[OPEN — limites] Não se afirma que qualquer b∈E comuta com as médias; o resultado é para as raízes dos cortes originais. Extensão da ordem dos pesos a todos os positivos e tracialidade permanecem abertas; nenhum gate é promovido. Nenhuma consulta adicional, edição de fontes autorais/memórias ou execução de monólito/recorder.

Artefatos desta V2:

- [compilation V2](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_comutacao_cortes_medias\compilation_v2.json>) — SHA256 `dd0c49b6ce2e47e19e2de7d10f08cd082e2a62bae43b2eecc5f84e88e0e42eb2`.
- [resolução documental](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_comutacao_cortes_medias\documentary_resolution_v2.json>) — SHA256 `bf82d2286f99cbdcfc963408aecf8050c6fb0e0a7c4890a76bb023c46712bda8`.
- [correção MD](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\ADENDO_FICHA_COMUTACAO_CFC_CORRECAO.md>) — SHA256 `124d015df887ea513b530827388fd59a3016cdde68dcef0c5d058462009a2890`.
- [correção JSON](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\ADENDO_FICHA_COMUTACAO_CFC_CORRECAO.json>) — SHA256 `1bac2f6466c438300494762e14efecb7f3e4a4341839bf0e5c2a3806116bb4b3`.
- [run próprio preservado](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_comutacao_cortes_medias\independent_20260914_220558_290545\run.json>) — SHA256 `0614e4067d8ad71dc7a0fb1a119aa6ed793791acecdd25bb977ee2bde9d20c6d`.
- [tipos/axiomas preservados](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_comutacao_cortes_medias\independent_20260914_220558_290545\type_axiom_audit.json>) — SHA256 `0ef359012b34425e3a5fff9e1e9fb496516053eb29416bb8f55c479ddc6471f4`.


## Ficha/adendo integral: REAPROVEITAMENTO_A1B_COMUTACAO_CORTES_MEDIAS

[OPEN — ficha anterior à comutação dos cortes com as médias]

# A1(b): as médias comutam com as raízes dos cortes originais

2026-09-14T22:01:48.045934-03:00

For P,t prove Commute(regularSpectralResolvent P)(regularUnitary P t), using SAME spectral coordinates and commuting characters. For epsilon>0 use existing cutoff CFC identity and existing hilbertPositiveSqrt=CFC.sqrt to deduce Commute(sqrt(B_epsilon))(regularUnitary P t). Integrate the actual regularUnitary using regularAverage_apply to prove Commute(sqrt(B_epsilon))(regularAverage P delta) for EVERY real delta. No new spectral transform, resolvent, average, square root or weight. Consumer: use the already established average recovery on a sqrt(B_epsilon) to extend perturbed-weight order to all positive inputs. This does not infer commutation of arbitrary b in the right algebra with the averages. Mathematical helper is generic CFC commutation instantiated on Hilbert operators.

ADAPTAR: coordenação espectral, comutação de caracteres, CFC e integral das translações existentes. Não reconstruir as coordenadas nem o resolvente. A consulta TODOS_POSITIVOS nomeia esta ponte como necessária. Mathlib Commute.cfc/IsSelfAdjoint.commute_cfc e Commute.cfcₙ_nnreal foram lidos no fornecedor ContinuousFunctionalCalculus/Commute.lean.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularGeneratorAffiliation.lean:13` — `9e172df5174e9b2b9c5315825a4a487f0fb04b34ba68dcecffd11e8d2684690e`

```lean
theorem character_commutation_realScalarMultiplier
    (B : RegularHilbert H →L[ℂ] RegularHilbert H)
    (hB : ∀ s : ℝ, characterMultiplier s * B = B * characterMultiplier s)
    (g : ℝ → ℝ) (hg : Continuous g) (h0 : ∀ x, 0 ≤ g x) (h1 : ∀ x, g x ≤ 1) :
    realScalarMultiplier g hg h0 h1 * B = B * realScalarMultiplier g hg h0 h1
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularImaginaryPowers.lean:65` — `066b9cb14426365807ead587ca90ad28e3703a0f9efc0ce359519da7c5243b9a`

```lean
theorem regularSpectralCoordinates_character (P : SiteProfile) (t : ℝ)
    (u : RegularHilbert (TowerHilbert P)) :
    regularSpectralCoordinates P (characterMultiplier (2*Real.pi*t) u) =
      regularUnitary P t (regularSpectralCoordinates P u)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350L2CharacterMultiplier.lean:114` — `2f7c413ee9ebd5ba93d1222bb596da11972a0b6b4efa1a71a04becb6ff856ca3`

```lean
theorem characterMultiplier_mul (s t : ℝ) :
    characterMultiplier (H := H) s * characterMultiplier t = characterMultiplier (s+t)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseCutoffCFC.lean:62` — `cbdf10aea749a552b0f47afb3ef59560ed47d6f46cf7dd8064dc963a092c3490`

```lean
theorem regularInverseGeneratorCutoff_cfc (P : SiteProfile) (ε : ℝ) (hε : 0 < ε) :
    regularInverseGeneratorCutoff P ε =
      cfc (inverseCutoffFunction ε) (regularSpectralResolvent P)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350AntiunitaryPositiveConjugation.lean:15` — `83be0cf3f811bd6fd429c7705fdb1a00b27fdd6496ee971b9ca5f355c00d6f36`

```lean
def hilbertPositiveSqrt (T : H →L[ℂ] H) : H →L[ℂ] H
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350RegularApproximation.lean:41` — `d8e7830989e0ba3d71f0e8495f54414cedc12a9eac16b1bc0501f15342b8bb44`

```lean
theorem regularAverage_apply (P : TGLExt.SiteProfile) (h : ℝ)
    (v : RegularHilbert (TGLExt.TowerHilbert P)) :
    regularAverage P h v = h⁻¹ • ∫ t in 0..h, regularUnitary P t v
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularPositiveGraph.lean:84` — `d56ea107302802ee76d65a3c32c69be9fe41cddb4901a65486ab7f1bfb345390`

```lean
theorem regularSpectralResolvent_nonneg (P : SiteProfile) :
    0 ≤ regularSpectralResolvent P
```

Seis modalidades e outras bancadas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_cutoff_average_commutation\20260914_220124_359580\searches.json. Ausência nominal nos recortes não é ausência universal.


## Ficha/adendo integral: ADENDO_FICHA_COMUTACAO_CFC

[OPEN — fornecedores CFC, antes do código]

2026-09-14T22:02:12.332613-03:00

A comutação do CFC complexo e da raiz NNReal será consumida diretamente. A raiz é o empacotamento hilbertPositiveSqrt antigo; nenhum cálculo funcional novo.

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\CStarAlgebra\ContinuousFunctionalCalculus\Commute.lean:67

protected theorem IsSelfAdjoint.commute_cfcHom {a b : A} (ha : p a)
    (ha' : IsSelfAdjoint a) (hb : Commute a b) (f : C(spectrum 𝕜 a, 𝕜)) :
    Commute (cfcHom ha f) b

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\CStarAlgebra\ContinuousFunctionalCalculus\Commute.lean:200

protected theorem Commute.cfcₙ_nnreal {a b : A} (hb : Commute a b) (f : ℝ≥0 → ℝ≥0) :
    Commute (cfcₙ f a) b

## Ficha/adendo integral: ADENDO_FICHA_COMUTACAO_CFC_CORRECAO

[REAL — correção documental ao lado; sem mudança Lean]

# Correção da referência de comutação CFC

2026-09-14T22:12:12.674131-03:00

O adendo anterior nomeava commute_cfc mas transcrevia commute_cfcHom. Corrigidos localizador e enunciado; os bytes anteriores são preservados como histórico. Nenhuma fonte ou compilação Lean foi alterada.

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\CStarAlgebra\ContinuousFunctionalCalculus\Commute.lean:87

```lean
protected theorem IsSelfAdjoint.commute_cfc {a b : A}
    (ha : IsSelfAdjoint a) (hb₁ : Commute a b) (f : 𝕜 → 𝕜) :
    Commute (cfc f a) b
```

O segundo fornecedor, Commute.cfcₙ_nnreal, permanece como no adendo anterior. O P2 foi documental; a construção já usava commute_cfc. Esta correção não é uma alegação de ficha anterior ao código: a ficha histórica permanece visível.
