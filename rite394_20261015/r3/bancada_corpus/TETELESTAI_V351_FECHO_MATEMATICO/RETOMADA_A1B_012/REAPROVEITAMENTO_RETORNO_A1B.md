[OPEN — ficha anterior à reprodução standalone; fontes matemáticas existentes, sem alteração]

# Retomada A1(b) após B6

2026-09-14T17:31:00.813331-03:00

REUSAR sete módulos já presentes no snapshot v353, todos idênticos em bytes à bancada A1. Não criar outro teorema ou camada para repetir seus resultados. Produto: auditoria de40 declarações, reprodução Lake, revisão independente e entrega própria que faltavam.

Consumidor: regular_dual_weight_modular_implementation, em LACUNAS_A1.md:25; contrato final TGLV351.RegularCoreTraceData, V351RegularCoreTraceContract.lean:43. Estas pontes tratam o grupo do MESMO resolvente/GNS e J polar, sem provar por si a implementação modular integral ou o traço.

## Fornecedores e tipos exatos

### V351ResolventImaginaryIntertwining

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V351ResolventImaginaryIntertwining.lean` · `789f68095379e02a203191b258c359787c12b24c1282f34d39835dc5347c76d5` · REUSAR, sem editar.

Linha 15: `TGLV350.Regular.complex_cfc_selfadjoint_intertwines`
```lean
theorem complex_cfc_selfadjoint_intertwines (A B R : H →L[ℂ] H)
    (hA : IsSelfAdjoint A) (hB : IsSelfAdjoint B) (h : A*R=R*B)
    (f : ℂ → ℂ) (hf : Continuous f) : cfc f A * R = R * cfc f B
```
Linha 51: `TGLV350.Regular.resolventDampingOperator_intertwines`
```lean
theorem resolventDampingOperator_intertwines (T Q R : H →L[ℂ] H)
    (h : T*R=R*Q) : resolventDampingOperator T * R = R * resolventDampingOperator Q
```
Linha 57: `TGLV350.Regular.resolventPhaseOperator_intertwines`
```lean
theorem resolventPhaseOperator_intertwines (T Q R : H →L[ℂ] H)
    (hT : IsSelfAdjoint T) (hQ : IsSelfAdjoint Q) (h : T*R=R*Q) (t : ℝ) :
    resolventPhaseOperator T t * R = R * resolventPhaseOperator Q t
```
Linha 64: `TGLV350.Regular.resolventImaginaryPower_intertwines`
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
### V351ScaledResolventFunctions

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V351ScaledResolventFunctions.lean` · `1195b42b9581167d977137f6a8757e3446010f1b18f6d3eb5843f4a49f10adcb` · REUSAR, sem editar.

Linha 11: `TGLV350.Regular.scaledResolventCoordinate`
```lean
def scaledResolventCoordinate (r x : ℝ) : ℝ
```
Linha 12: `TGLV350.Regular.scaledResolventDampingFactor`
```lean
def scaledResolventDampingFactor (r x : ℝ) : ℝ
```
Linha 14: `TGLV350.Regular.scaledResolventDenominator_scalar_pos`
```lean
theorem scaledResolventDenominator_scalar_pos (r : ℝ) (hr : 0<r) (x : ℝ)
    (hx : x ∈ Set.Icc (0 : ℝ) 1) : 0<r+(1-r)*x
```
Linha 21: `TGLV350.Regular.scaledResolventCoordinate_complement`
```lean
theorem scaledResolventCoordinate_complement (r x : ℝ) (hd : r+(1-r)*x ≠ 0) :
    1-scaledResolventCoordinate r x = r*(1-x)/(r+(1-r)*x)
```
Linha 28: `TGLV350.Regular.scaledResolventCoordinate_ratio`
```lean
theorem scaledResolventCoordinate_ratio (r x : ℝ) (hx : x≠0) (hd : r+(1-r)*x ≠ 0) :
    (1-scaledResolventCoordinate r x)/scaledResolventCoordinate r x = r*((1-x)/x)
```
Linha 36: `TGLV350.Regular.scaledResolventCoordinate_damping`
```lean
theorem scaledResolventCoordinate_damping (r x : ℝ) (hd : r+(1-r)*x ≠ 0) :
    resolventDamping (scaledResolventCoordinate r x)=
      resolventDamping x * scaledResolventDampingFactor r x
```
Linha 45: `TGLV350.Regular.scaledResolventCoordinate_phase`
```lean
theorem scaledResolventCoordinate_phase (r : ℝ) (hr : 0<r) (t x : ℝ)
    (hd : r+(1-r)*x ≠ 0) :
    resolventPhaseFunction t (scaledResolventCoordinate r x)=
      modularPhase t (Real.log r) * resolventPhaseFunction t x *
        (scaledResolventDampingFactor r x : ℂ)
```
### V351ScaledResolventCalculus

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V351ScaledResolventCalculus.lean` · `89cac33fa016460aaeb44b0de83d296137f2d3d7f826491be6361bb1e2ad8a32` · REUSAR, sem editar.

Linha 14: `TGLV350.Regular.positive_contraction_spectrum_bounds`
```lean
theorem positive_contraction_spectrum_bounds (T : H →L[ℂ] H)
    (hT : 0 ≤ T) (h1 : T ≤ 1) {x : ℝ} (hx : x ∈ spectrum ℝ T) :
    x ∈ Set.Icc (0 : ℝ) 1
```
Linha 21: `TGLV350.Regular.scaledResolventDenominator_real_cfc`
```lean
theorem scaledResolventDenominator_real_cfc (T : H →L[ℂ] H) (hT : IsSelfAdjoint T) (r : ℝ) :
    cfc (fun x : ℝ => r+(1-r)*x) T = scaledResolventDenominator T r
```
Linha 27: `TGLV350.Regular.scaledResolventCoordinate_cfc`
```lean
theorem scaledResolventCoordinate_cfc (T : H →L[ℂ] H) (hT : 0 ≤ T) (h1 : T ≤ 1)
    (r : ℝ) (hr : 0<r) :
    cfc (fun z : ℂ => (scaledResolventCoordinate r z.re : ℂ)) T = scaledPositiveResolvent T r
```
Linha 39: `TGLV350.Regular.scaledResolventCoordinate_continuousOn_spectrum`
```lean
theorem scaledResolventCoordinate_continuousOn_spectrum (T : H →L[ℂ] H)
    (hT : 0 ≤ T) (h1 : T ≤ 1) (r : ℝ) (hr : 0<r) :
    ContinuousOn (fun z : ℂ => (scaledResolventCoordinate r z.re : ℂ)) (spectrum ℂ T)
```
Linha 49: `TGLV350.Regular.scaledResolventDampingFactor_continuousOn_spectrum`
```lean
theorem scaledResolventDampingFactor_continuousOn_spectrum (T : H →L[ℂ] H)
    (hT : 0 ≤ T) (h1 : T ≤ 1) (r : ℝ) (hr : 0<r) :
    ContinuousOn (fun z : ℂ => (scaledResolventDampingFactor r z.re : ℂ)) (spectrum ℂ T)
```
Linha 61: `TGLV350.Regular.scaledResolventDampingOperator`
```lean
def scaledResolventDampingOperator (T : H →L[ℂ] H) (r : ℝ) : H →L[ℂ] H
```
Linha 64: `TGLV350.Regular.scaledResolventDampingOperator_isUnit`
```lean
theorem scaledResolventDampingOperator_isUnit (T : H →L[ℂ] H)
    (hT : 0 ≤ T) (h1 : T ≤ 1) (r : ℝ) (hr : 0<r) :
    IsUnit (scaledResolventDampingOperator T r)
```
Linha 74: `TGLV350.Regular.scaledPositiveResolvent_damping`
```lean
theorem scaledPositiveResolvent_damping (T : H →L[ℂ] H)
    (hT : 0 ≤ T) (h1 : T ≤ 1) (r : ℝ) (hr : 0<r) :
    resolventDampingOperator (scaledPositiveResolvent T r) =
      resolventDampingOperator T * scaledResolventDampingOperator T r
```
Linha 98: `TGLV350.Regular.scaledPositiveResolvent_phase`
```lean
theorem scaledPositiveResolvent_phase (T : H →L[ℂ] H)
    (hT : 0 ≤ T) (h1 : T ≤ 1) (r : ℝ) (hr : 0<r) (t : ℝ) :
    resolventPhaseOperator (scaledPositiveResolvent T r) t =
      modularPhase t (Real.log r) • (resolventPhaseOperator T t * scaledResolventDampingOperator T r)
```
### V351ImaginaryPowerScaling

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V351ImaginaryPowerScaling.lean` · `fbb31118edeb1863430be521e7dde573c2cf29ce8ad5df556ccfeed49ca12a69` · REUSAR, sem editar.

Linha 13: `TGLV350.Regular.scaledResolventDamping_denseRange`
```lean
theorem scaledResolventDamping_denseRange (T : H →L[ℂ] H)
    (hT : 0 ≤ T) (h1 : T ≤ 1) (hi : Function.Injective T)
    (hj : Function.Injective (1-T : H →L[ℂ] H)) (r : ℝ) (hr : 0<r) :
    DenseRange (resolventDampingOperator (scaledPositiveResolvent T r))
```
Linha 28: `TGLV350.Regular.resolventImaginaryPower_scaled_intertwining`
```lean
theorem resolventImaginaryPower_scaled_intertwining (T R : H →L[ℂ] H)
    (hT : 0 ≤ T) (h1 : T ≤ 1) (hi : Function.Injective T)
    (hj : Function.Injective (1-T : H →L[ℂ] H)) (r : ℝ) (hr : 0<r)
    (hR : T*R=R*scaledPositiveResolvent T r) (t : ℝ) (x : H) :
    resolventImaginaryPower T hT h1 hi hj t (R x)=
      modularPhase t (Real.log r) • R (resolventImaginaryPower T hT h1 hi hj t x)
```
### V351ScalarImaginaryRightTransport

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V351ScalarImaginaryRightTransport.lean` · `5442a451387b2c784b74023fea3d6dc31b42e35e3ccdefa8174dbf582eece349` · REUSAR, sem editar.

Linha 14: `TGLV350.Regular.matrixUnit_imaginaryPower_right_scaling`
```lean
theorem matrixUnit_imaginaryPower_right_scaling (P : SiteProfile) (N : ℕ)
    (i j : chainIdx N) (t : ℝ) (x : ScalarGNSHilbert P) :
    scalarTomitaImaginaryPower P t (homogeneousRightGNS (matrixUnitRightData P N i j) x)=
      modularPhase t (Real.log (localEigenvalue P N i j)) •
        homogeneousRightGNS (matrixUnitRightData P N i j) (scalarTomitaImaginaryPower P t x)
```
Linha 27: `TGLV350.Regular.scalarTomitaImaginaryPower_regular_right_commutes`
```lean
theorem scalarTomitaImaginaryPower_regular_right_commutes (P : SiteProfile) (s t : ℝ)
    (x : ScalarGNSHilbert P) :
    scalarTomitaImaginaryPower P t (regularRightGNS P s x)=
      regularRightGNS P s (scalarTomitaImaginaryPower P t x)
```
### V351AntiunitaryResolventPhase

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V351AntiunitaryResolventPhase.lean` · `4cd800bb6c465a55d6387ecef3517ccb57c2a087cc2e8e6a35ded13273516bd8` · REUSAR, sem editar.

Linha 14: `TGLV350.Regular.resolventPhaseFunction_reflection`
```lean
theorem resolventPhaseFunction_reflection (t x : ℝ) :
    star (resolventPhaseFunction t (1-x)) = resolventPhaseFunction t x
```
Linha 28: `TGLV350.Regular.antiunitaryConjugate_star`
```lean
theorem antiunitaryConjugate_star (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (T : H →L[ℂ] H) :
    antiunitaryConjugate J (star T) = star (antiunitaryConjugate J T)
```
Linha 44: `TGLV350.Regular.antiunitaryConjugate_add`
```lean
theorem antiunitaryConjugate_add (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (T V : H →L[ℂ] H) :
    antiunitaryConjugate J (T+V) = antiunitaryConjugate J T + antiunitaryConjugate J V
```
Linha 49: `TGLV350.Regular.antiunitaryConjugate_smul`
```lean
theorem antiunitaryConjugate_smul (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (c : ℂ) (T : H →L[ℂ] H) :
    antiunitaryConjugate J (c • T) = star c • antiunitaryConjugate J T
```
Linha 57: `TGLV350.Regular.antiunitaryConjugateRealHom`
```lean
def antiunitaryConjugateRealHom (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) :
    (H →L[ℂ] H) →⋆ₐ[ℝ] (H →L[ℂ] H)
```
Linha 78: `TGLV350.Regular.antiunitaryConjugate_continuous`
```lean
theorem antiunitaryConjugate_continuous (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) :
    Continuous (antiunitaryConjugate J)
```
Linha 85: `TGLV350.Regular.antiunitaryConjugate_selfadjoint`
```lean
theorem antiunitaryConjugate_selfadjoint (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (T : H →L[ℂ] H) (hT : IsSelfAdjoint T) : IsSelfAdjoint (antiunitaryConjugate J T)
```
Linha 89: `TGLV350.Regular.antiunitaryConjugate_real_cfc`
```lean
theorem antiunitaryConjugate_real_cfc (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (T : H →L[ℂ] H) (hT : IsSelfAdjoint T) (f : ℝ → ℝ) (hf : Continuous f) :
    antiunitaryConjugate J (cfc f T) = cfc f (antiunitaryConjugate J T)
```
Linha 95: `TGLV350.Regular.complex_cfc_real_imaginary`
```lean
theorem complex_cfc_real_imaginary (T : H →L[ℂ] H) (hT : IsSelfAdjoint T)
    (f : ℝ → ℂ) (hf : Continuous f) :
    cfc (fun z : ℂ => f z.re) T =
      cfc (fun x : ℝ => (f x).re) T + Complex.I • cfc (fun x : ℝ => (f x).im) T
```
Linha 111: `TGLV350.Regular.antiunitaryConjugate_complex_cfc`
```lean
theorem antiunitaryConjugate_complex_cfc (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (T : H →L[ℂ] H) (hT : IsSelfAdjoint T) (f : ℝ → ℂ) (hf : Continuous f) :
    antiunitaryConjugate J (cfc (fun z : ℂ => f z.re) T) =
      cfc (fun z : ℂ => star (f z.re)) (antiunitaryConjugate J T)
```
Linha 124: `TGLV350.Regular.antiunitaryConjugate_resolventPhase`
```lean
theorem antiunitaryConjugate_resolventPhase (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (T : H →L[ℂ] H) (hT : IsSelfAdjoint T)
    (hflip : antiunitaryConjugate J T = 1-T) (t : ℝ) :
    antiunitaryConjugate J (resolventPhaseOperator T t) = resolventPhaseOperator T t
```
Linha 143: `TGLV350.Regular.antiunitaryConjugate_resolventDamping`
```lean
theorem antiunitaryConjugate_resolventDamping (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (T : H →L[ℂ] H) (hT : IsSelfAdjoint T)
    (hflip : antiunitaryConjugate J T = 1-T) :
    antiunitaryConjugate J (resolventDampingOperator T) = resolventDampingOperator T
```
Linha 150: `TGLV350.Regular.resolventImaginaryPower_antiunitary`
```lean
theorem resolventImaginaryPower_antiunitary (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (T : H →L[ℂ] H) (hT : 0 ≤ T) (h1 : T ≤ 1)
    (hi : Function.Injective T) (hj : Function.Injective (1-T : H →L[ℂ] H))
    (hflip : antiunitaryConjugate J T = 1-T) (t : ℝ) (x : H) :
    J (resolventImaginaryPower T hT h1 hi hj t x) =
      resolventImaginaryPower T hT h1 hi hj t (J x)
```
### V351ScalarTomitaImaginaryConjugation

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V351ScalarTomitaImaginaryConjugation.lean` · `981dda6d5a16272efdbcfa46cd674bb66eaa0179d70634a9a9bcc2c5332b4c9d` · REUSAR, sem editar.

Linha 14: `TGLV350.Regular.scalarTomitaImaginaryPower_polar_commutes`
```lean
theorem scalarTomitaImaginaryPower_polar_commutes (P : SiteProfile) (t : ℝ)
    (x : ScalarGNSHilbert P) :
    scalarTomitaPolarFactor P (scalarTomitaImaginaryPower P t x) =
      scalarTomitaImaginaryPower P t (scalarTomitaPolarFactor P x)
```
Linha 23: `TGLV350.Regular.scalarTomitaImaginaryPower_polar_conjugate`
```lean
theorem scalarTomitaImaginaryPower_polar_conjugate (P : SiteProfile) (t : ℝ)
    (x : ScalarGNSHilbert P) :
    scalarTomitaPolarFactor P
      (scalarTomitaImaginaryPower P t ((scalarTomitaPolarFactor P).symm x)) =
        scalarTomitaImaginaryPower P t x
```
Linha 31: `TGLV350.Regular.scalarTomitaImaginaryPower_polar_operator`
```lean
theorem scalarTomitaImaginaryPower_polar_operator (P : SiteProfile) (t : ℝ) :
    antiunitaryConjugate (scalarTomitaPolarFactor P)
      (scalarTomitaImaginaryPower P t).toLinearIsometry.toContinuousLinearMap =
        (scalarTomitaImaginaryPower P t).toLinearIsometry.toContinuousLinearMap
```

## Aproveitamento, buscas e limites

As fichas anteriores e BUSCAS_A1 registram as seis modalidades: fontes embutidos por nomes/tipos; notasV350; entregas/bancadas; árvore; TOE; índice do acervo. Seus arquivos e hashes constam no JSON. A retomada acrescenta comparação em bytes contra o snapshot v353, que já contém os sete. Não se anuncia varredura nova exaustiva.

Os 19V351 originais, relatórios e quatro entregas anteriores ficam intactos. O contrato forte e as provas anteriores não são refeitos. A cópia Lake nesta subpasta usa fontes da bancada antiga, caches Mathlib/pacotes pinados da bancada B e nenhum objeto de projeto autoral herdado. Falhas de compilação da manhã permanecem na casa antiga e não são confundidas com esta reprodução. A auditoria histórica antiunitária era autoral do sidecar: a nova revisão será separada.

A1(b) continua OPEN: nenhuma instância de RegularCoreTraceData é prometida por esta entrega documental. O próximo consumidor matemático é o transporte à esquerda dos geradores, pela ponte polar já existente; qualquer novo código exige sua própria ficha.
