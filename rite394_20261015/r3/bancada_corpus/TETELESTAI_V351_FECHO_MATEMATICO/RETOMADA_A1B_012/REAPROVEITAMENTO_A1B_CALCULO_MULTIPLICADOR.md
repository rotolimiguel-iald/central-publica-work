[OPEN — ficha anterior ao cálculo funcional do multiplicador existente]

# A1(b): cálculo funcional no mesmo L²

2026-09-14T19:17:58.427276-03:00

For a continuous scalar g:R->[0,1], use the existing operatorFieldLift to represent C([0,1],C) as bounded operators on RegularHilbert H. Prove this is a unital complex star-algebra homomorphism, equals the existing realScalarMultiplier at the coordinate function, and transports continuous functional calculus. This pays the scalar-multiplier identification needed for resolventPhaseOperator and then regular_unitary_positive_generator. No new L2 space, operator-field machinery or imaginary-power definition.

O homomorfismo tem consumidor concreto: map_cfc e a fase do resolvente. A maquinaria de lift e sua álgebra são reutilizadas, não reprovadas. A busca negativa nos recortes não afirma ausência universal.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350StrongOperatorField.lean:64` — `83fcc9ee4e6cdecee9f130183b7d1e6a0e2436caf40670e4d64dce8933f86a4c`

```lean
def operatorFieldLift (F : StrongIntegral.Family (H := H)) :
    RegularHilbert H →L[ℂ] RegularHilbert H
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350StrongOperatorField.lean:68` — `83fcc9ee4e6cdecee9f130183b7d1e6a0e2436caf40670e4d64dce8933f86a4c`

```lean
theorem operatorFieldLift_ae (F : StrongIntegral.Family (H := H)) (f : RegularHilbert H) :
    operatorFieldLift F f =ᵐ[volume] fun x : ℝ => F.op x (f x)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350OperatorFieldAlgebra.lean:12` — `ccd8bfa143d144167dfe9e395b1c9edd0472cc4f73d94f0d7b32e079b8bb8b2d`

```lean
theorem operatorFieldLift_constant (F : StrongIntegral.Family (H := H))
    (T : H →L[ℂ] H) (h : ∀ x, F.op x = T) :
    operatorFieldLift F = fibre T
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350OperatorFieldAlgebra.lean:20` — `ccd8bfa143d144167dfe9e395b1c9edd0472cc4f73d94f0d7b32e079b8bb8b2d`

```lean
theorem operatorFieldLift_add (F G K : StrongIntegral.Family (H := H))
    (h : ∀ x, K.op x = F.op x + G.op x) :
    operatorFieldLift K = operatorFieldLift F + operatorFieldLift G
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350OperatorFieldAlgebra.lean:33` — `ccd8bfa143d144167dfe9e395b1c9edd0472cc4f73d94f0d7b32e079b8bb8b2d`

```lean
theorem operatorFieldLift_mul (F G K : StrongIntegral.Family (H := H))
    (h : ∀ x, K.op x = F.op x * G.op x) :
    operatorFieldLift K = operatorFieldLift F * operatorFieldLift G
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350OperatorFieldAlgebra.lean:57` — `ccd8bfa143d144167dfe9e395b1c9edd0472cc4f73d94f0d7b32e079b8bb8b2d`

```lean
theorem operatorFieldLift_star (F G : StrongIntegral.Family (H := H))
    (h : ∀ x, G.op x = star (F.op x)) :
    operatorFieldLift G = star (operatorFieldLift F)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350L2PositiveMultiplier.lean:25` — `6e3946aff9964e1a6a59a8dcb99a11b4a3c0026a6b0220f7df4b9901f83f3bdf`

```lean
def realScalarMultiplier (g : ℝ → ℝ) (hg : Continuous g)
    (h0 : ∀ s, 0 ≤ g s) (h1 : ∀ s, g s ≤ 1) :
    RegularHilbert H →L[ℂ] RegularHilbert H
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ResolventPhaseCalculus.lean:15` — `cd207e3a21c50f65fe3b199e201b2b148a0d98fc2e3a3cf7e40a80e61ba4f818`

```lean
def resolventPhaseOperator (T : H →L[ℂ] H) (t : ℝ) : H →L[ℂ] H
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ResolventImaginaryPowers.lean:45` — `0cfc297376410ff6bd259eeaf921a9d6e6ca47829b5d389c6b5c30bf4c5accf5`

```lean
theorem resolventImaginaryPower_damping (t : ℝ) (x : H) :
    resolventImaginaryPower T hT h1 hi hj t (resolventDampingOperator T x)=
      resolventPhaseOperator T t x
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\CStarAlgebra\ContinuousFunctionalCalculus\Unique.lean:486` — `d7103470f12927eb549967928bc1a6bc6e81ba8727997eee113239772ba2e6c1`

```lean
lemma StarAlgHom.map_cfc (φ : A →⋆ₐ[S] B) (f : R → R) (a : A)
    (hf : ContinuousOn f (spectrum R a) := by cfc_cont_tac) (hφ : Continuous φ := by fun_prop)
    (ha : p a := by cfc_tac) (hφa : q (φ a) := by cfc_tac) :
    φ (cfc f a) = cfc f (φ a)
```

Seis modalidades e outras bancadas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_multiplier_calculus\20260914_191706_280714\searches.json.
