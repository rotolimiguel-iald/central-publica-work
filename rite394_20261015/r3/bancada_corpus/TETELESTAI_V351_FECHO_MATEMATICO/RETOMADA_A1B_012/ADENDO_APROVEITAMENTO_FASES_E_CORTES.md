[OPEN] Refinamento de aproveitamento — fases concretas e cortes

Sem mudança de escopo nem novo modelo. Complementa a ficha de sete canais já registrada.

A conjugação antiunitária preserva positividade por lema anterior. A identidade J pi(lambda_t) J^-1 = R_-t já existe; não deve ser reprovada. Transportar somente a identidade amortecida das potências imaginárias regulares pela pi existente e conjugar com o J existente.

[DERIVED — plano algébrico, ainda não compilado] Para o balanço de cortes, aproveitar B_1=R e a identidade de resolventes. Ela dá A p_e=(1-A) C_e e B q_h=(1-B) D_h. Com as comutações correspondentes, multiplicar a diferença desejada por A B reduz ao balanço básico (1-T) A (1-B)=T (1-A) B. Cancelar A B por injetividade vetorial, nunca por inversa limitada ou separação espectral uniforme. Isso dispensa construir um novo cálculo espectral para cada regulador. As hipóteses de comutação têm de ser descarregadas nos objetos originais.

[OPEN] Cinco auxiliares privados passaram apenas DEV. A sexta aplicação concreta ainda está sob correção de elaboração; não há entrega33, compilação independente33 ou tracialidade. Nenhum gate alterado.

2026-09-15T02:18:39.281217-03:00

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350AntiunitaryPositiveConjugation.lean:33
```lean
theorem antiunitaryConjugate_nonneg (T : H →L[ℂ] H) (hT : 0 ≤ T) :
    0 ≤ antiunitaryConjugate U T := by
  apply (ContinuousLinearMap.nonneg_iff_isPositive _).mpr
  apply (ContinuousLinearMap.isPositive_iff_complex _).mpr
  intro x
  have hinner : inner ℂ (antiunitaryConjugate U T x) x =
      star (inner ℂ (T (U.symm x)) (U.symm x)) := by
    have h := antiunitary_inner_conj U (T (U.symm x)) (U.symm x)
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarRegularPolarCommutation.lean:50
```lean
theorem scalarTomitaPolar_regular_generator (P : SiteProfile) (t : ℝ) :
    antiunitaryConjugate (scalarTomitaPolarFactor P)
      (scalarGNSRepresentation P (regularRightCoreElement P t)) =
        regularRightGNS P (-t) := by
  have h := scalarTomitaPolar_conjugate_regular_left P (-t)
  simpa only [regularRightCoreElement_star,neg_neg] using h

theorem scalarTomitaPolar_regular_generator_commutes (P : SiteProfile) (t : ℝ)
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularImaginaryPowers.lean:90
```lean
theorem regularPositiveGenerator_imaginaryPower (P : SiteProfile) (t : ℝ)
    (u : RegularHilbert (TowerHilbert P)) :
    resolventImaginaryPower (regularSpectralResolvent P)
      (regularSpectralResolvent_nonneg P) (regularSpectralResolvent_le_one P)
      (regularSpectralResolvent_injective P) (regularSpectralResolvent_complement_injective P)
      t u = regularUnitary P t u := by
  let g : ℝ → ℝ := fun ξ => Real.sigmoid (2*Real.pi*ξ)
  have hg : Continuous g := by fun_prop
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ResolventImaginaryPowers.lean:45
```lean
theorem resolventImaginaryPower_damping (t : ℝ) (x : H) :
    resolventImaginaryPower T hT h1 hi hj t (resolventDampingOperator T x)=
      resolventPhaseOperator T t x :=
  denseLinearEquiv_apply _ _ _ _ _ x

theorem resolventImaginaryPower_zero (x : H) :
    resolventImaginaryPower T hT h1 hi hj 0 x = x := by
  refine (resolventDampingOperator_denseRange T hT h1 hi hj).induction ?_
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseGeneratorCutoff.lean:43
```lean
theorem regularInverseGeneratorCutoff_one (P : SiteProfile) :
    regularInverseGeneratorCutoff P 1 = regularSpectralResolvent P := by
  simp only [regularInverseGeneratorCutoff, Complex.ofReal_one, inv_one, Real.log_one,
    dualAmbient_zero, one_smul]
  rfl

/-- The image belongs to the domain of the same h and solves (h+epsilon)y=x. -/
theorem regularInverseGeneratorCutoff_graph (P : SiteProfile) (ε : ℝ) (hε : 0 < ε)
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularDomainCut.lean:58
```lean
theorem regularDomainCut_inverse_product (P : SiteProfile) (ε δ : ℝ)
    (hε : 0 < ε) (hδ : 0 < δ) :
    regularInverseGeneratorCutoff P ε * (regularDomainCut P δ).val =
      regularInverseGeneratorCutoff P δ - (ε : ℂ) •
        (regularInverseGeneratorCutoff P δ * regularInverseGeneratorCutoff P ε) := by
  have he := regularInverseGeneratorCutoff_resolvent_identity P ε δ hε hδ
  have hc := (regularInverseGeneratorCutoff_commutes P ε δ hε hδ).eq
  change regularInverseGeneratorCutoff P ε * (1-(δ : ℂ) • regularInverseGeneratorCutoff P δ) = _
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularDomainCut.lean:49
```lean
theorem regularDomainCut_commutes (P : SiteProfile) (ε δ : ℝ)
    (hε : 0 < ε) (hδ : 0 < δ) :
    Commute (regularInverseGeneratorCutoff P ε) (regularDomainCut P δ).val := by
  have hc := (regularInverseGeneratorCutoff_commutes P ε δ hε hδ).eq
  change regularInverseGeneratorCutoff P ε * (1-(δ : ℂ) • regularInverseGeneratorCutoff P δ) =
    (1-(δ : ℂ) • regularInverseGeneratorCutoff P δ) * regularInverseGeneratorCutoff P ε
  simp only [mul_sub,sub_mul,mul_one,one_mul,mul_smul_comm,smul_mul_assoc,hc]

```
