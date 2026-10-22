[REAL — inspeção semântica dos dois fornecedores; reprodução isolada ainda pendente]

# Revisão do principal: camada antiunitária

2026-09-14T18:07:22.267605-03:00

A revisão do principal é distinta da autoria anterior declarada pelo sidecar. O replay do sidecar continuará identificado como reprodução computacional. Nenhum P0, P1 ou P2 encontrado na leitura dos tipos e provas. Esta nota não antecipa rc0.

- The conjugation used throughout is J T J.symm, with J the specified semilinear isometric equivalence. J²=I is not assumed or needed in the generic proof.

- The real star-algebra homomorphism conjugates complex scalars. Real CFC transport and real/imaginary decomposition establish the complex CFC formula; no complex-linear automorphism is falsely attributed to J.

- The damped phase satisfies star(g_t(1-x))=g_t(x). Reflection of log((1-x)/x) and scalar conjugation cancel. Endpoint values are zero through damping; no undefined endpoint division is used to infer a nonzero limit.

- Norm-continuity of bounded antiunitary conjugation justifies CFC transport. Self-adjointness follows by adjoint identities. The CFC composition is supplied with its continuity and star-normality conditions.

- T and 1-T are injective positive contractions in the generic imaginary-power theorem. The already proved dense range of T(1-T) permits extension from damped vectors by continuity. No bounded inverse or spectral gap is introduced.

- The concrete specialization uses the original scalarTomitaResolvent and scalarTomitaPolarFactor. The actual polar-resolvent flip is a supplier, not an assumed new covariance. The resulting group is scalarTomitaImaginaryPower in the same ScalarGNSHilbert P.

- Final pointwise and bounded-operator equalities are JU_tJ^{-1}=U_t. Neither claims JU_tJ^{-1}=U_{-t}, nor a KMS theorem, affiliated regular generator, trace, or complete RegularCoreTraceData inhabitant.

- The existing module V350LocalBasePolarCommutation contains same-name add/smul statements. The actual combined import was accepted in a separate DEV check. This inspection does not label the repeated names a demonstrated compilation bug; the standalone delta build remains required.

## Fontes e declarações relidas

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351AntiunitaryResolventPhase.lean` — `4cd800bb6c465a55d6387ecef3517ccb57c2a087cc2e8e6a35ded13273516bd8`

`TGLV350.Regular.resolventPhaseFunction_reflection` :14

```lean
theorem resolventPhaseFunction_reflection (t x : ℝ) :
    star (resolventPhaseFunction t (1-x)) = resolventPhaseFunction t x
```

`TGLV350.Regular.antiunitaryConjugate_star` :28

```lean
theorem antiunitaryConjugate_star (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (T : H →L[ℂ] H) :
    antiunitaryConjugate J (star T) = star (antiunitaryConjugate J T)
```

`TGLV350.Regular.antiunitaryConjugate_add` :44

```lean
theorem antiunitaryConjugate_add (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) (T V : H →L[ℂ] H) :
    antiunitaryConjugate J (T+V) = antiunitaryConjugate J T + antiunitaryConjugate J V
```

`TGLV350.Regular.antiunitaryConjugate_smul` :49

```lean
theorem antiunitaryConjugate_smul (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (c : ℂ) (T : H →L[ℂ] H) :
    antiunitaryConjugate J (c • T) = star c • antiunitaryConjugate J T
```

`TGLV350.Regular.antiunitaryConjugateRealHom` :57

```lean
def antiunitaryConjugateRealHom (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) :
    (H →L[ℂ] H) →⋆ₐ[ℝ] (H →L[ℂ] H)
```

`TGLV350.Regular.antiunitaryConjugate_continuous` :78

```lean
theorem antiunitaryConjugate_continuous (J : H ≃ₛₗᵢ[starRingEnd ℂ] H) :
    Continuous (antiunitaryConjugate J)
```

`TGLV350.Regular.antiunitaryConjugate_selfadjoint` :85

```lean
theorem antiunitaryConjugate_selfadjoint (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (T : H →L[ℂ] H) (hT : IsSelfAdjoint T) : IsSelfAdjoint (antiunitaryConjugate J T)
```

`TGLV350.Regular.antiunitaryConjugate_real_cfc` :89

```lean
theorem antiunitaryConjugate_real_cfc (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (T : H →L[ℂ] H) (hT : IsSelfAdjoint T) (f : ℝ → ℝ) (hf : Continuous f) :
    antiunitaryConjugate J (cfc f T) = cfc f (antiunitaryConjugate J T)
```

`TGLV350.Regular.complex_cfc_real_imaginary` :95

```lean
theorem complex_cfc_real_imaginary (T : H →L[ℂ] H) (hT : IsSelfAdjoint T)
    (f : ℝ → ℂ) (hf : Continuous f) :
    cfc (fun z : ℂ => f z.re) T =
      cfc (fun x : ℝ => (f x).re) T + Complex.I • cfc (fun x : ℝ => (f x).im) T
```

`TGLV350.Regular.antiunitaryConjugate_complex_cfc` :111

```lean
theorem antiunitaryConjugate_complex_cfc (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (T : H →L[ℂ] H) (hT : IsSelfAdjoint T) (f : ℝ → ℂ) (hf : Continuous f) :
    antiunitaryConjugate J (cfc (fun z : ℂ => f z.re) T) =
      cfc (fun z : ℂ => star (f z.re)) (antiunitaryConjugate J T)
```

`TGLV350.Regular.antiunitaryConjugate_resolventPhase` :124

```lean
theorem antiunitaryConjugate_resolventPhase (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (T : H →L[ℂ] H) (hT : IsSelfAdjoint T)
    (hflip : antiunitaryConjugate J T = 1-T) (t : ℝ) :
    antiunitaryConjugate J (resolventPhaseOperator T t) = resolventPhaseOperator T t
```

`TGLV350.Regular.antiunitaryConjugate_resolventDamping` :143

```lean
theorem antiunitaryConjugate_resolventDamping (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (T : H →L[ℂ] H) (hT : IsSelfAdjoint T)
    (hflip : antiunitaryConjugate J T = 1-T) :
    antiunitaryConjugate J (resolventDampingOperator T) = resolventDampingOperator T
```

`TGLV350.Regular.resolventImaginaryPower_antiunitary` :150

```lean
theorem resolventImaginaryPower_antiunitary (J : H ≃ₛₗᵢ[starRingEnd ℂ] H)
    (T : H →L[ℂ] H) (hT : 0 ≤ T) (h1 : T ≤ 1)
    (hi : Function.Injective T) (hj : Function.Injective (1-T : H →L[ℂ] H))
    (hflip : antiunitaryConjugate J T = 1-T) (t : ℝ) (x : H) :
    J (resolventImaginaryPower T hT h1 hi hj t x) =
      resolventImaginaryPower T hT h1 hi hj t (J x)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarTomitaImaginaryConjugation.lean` — `981dda6d5a16272efdbcfa46cd674bb66eaa0179d70634a9a9bcc2c5332b4c9d`

`TGLV350.Regular.scalarTomitaImaginaryPower_polar_commutes` :14

```lean
theorem scalarTomitaImaginaryPower_polar_commutes (P : SiteProfile) (t : ℝ)
    (x : ScalarGNSHilbert P) :
    scalarTomitaPolarFactor P (scalarTomitaImaginaryPower P t x) =
      scalarTomitaImaginaryPower P t (scalarTomitaPolarFactor P x)
```

`TGLV350.Regular.scalarTomitaImaginaryPower_polar_conjugate` :23

```lean
theorem scalarTomitaImaginaryPower_polar_conjugate (P : SiteProfile) (t : ℝ)
    (x : ScalarGNSHilbert P) :
    scalarTomitaPolarFactor P
      (scalarTomitaImaginaryPower P t ((scalarTomitaPolarFactor P).symm x)) =
        scalarTomitaImaginaryPower P t x
```

`TGLV350.Regular.scalarTomitaImaginaryPower_polar_operator` :31

```lean
theorem scalarTomitaImaginaryPower_polar_operator (P : SiteProfile) (t : ℝ) :
    antiunitaryConjugate (scalarTomitaPolarFactor P)
      (scalarTomitaImaginaryPower P t).toLinearIsometry.toContinuousLinearMap =
        (scalarTomitaImaginaryPower P t).toLinearIsometry.toContinuousLinearMap
```

