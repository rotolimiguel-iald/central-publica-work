[OPEN — adendo anterior ao código do balanço espectral]

2026-09-15T01:33:06.753698-03:00

Delta32 já aceito e entregue. O balanço limitado e Q permanecem abertos. Estratégia em exame: usar a álgebra comutativa fechada gerada pelos três resolventes originais, transportar as fases amortecidas por map_cfc e aplicar os caracteres. A separação das frequências JÁ ESTÁ em modular_phase_frequency_separation: não refazer sua derivada. A igualdade escalar deve valer após multiplicação pelos amortecimentos, cobrindo os extremos 0 e 1 sem cancelamento falso. Só depois se cancela o operador com imagem densa, quando esta estiver provada na representação original. A conversão para cortes gerais é racional; não se introduz h=Delta_nu nem se assume o balanço desejado. Fornecedores abaixo relidos integralmente ou no trecho do enunciado antes de editar Lean33. Ausência em buscas não é prova de ausência universal.

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\PhaseFrequencySeparation.lean:58
```lean
theorem modular_phase_frequency_separation (a b : ℝ) (c : ℂ) (hc : c≠0)
    (h : ∀ s : ℝ, modularPhase s a*c=modularPhase s b*c) :
    a=b := by
  apply phase_frequency_separation a b c hc
  intro s
  simpa only [modular_phase_exponential] using h s

```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ResolventPhaseFunctions.lean:14
```lean
def resolventDamping (x : ℝ) : ℝ := x * (1-x)

/-- Only this damped function is fed to bounded continuous functional calculus. -/
def resolventPhaseFunction (t x : ℝ) : ℂ :=
  (resolventDamping x : ℂ) * modularPhase t (Real.log ((1-x)/x))
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\CStarAlgebra\GelfandDuality.lean:144
```lean
theorem gelfandTransform_isometry : Isometry (gelfandTransform ℂ A) := by
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Algebra\Star\Subalgebra.lean:588
```lean
theorem isMulCommutative_adjoin {s : Set A} (hcomm : ∀ x ∈ s, ∀ y ∈ s, x * y = y * x)
    (hcomm_star : ∀ a ∈ s, ∀ b ∈ s, a * star b = star b * a) :
    IsMulCommutative (adjoin R s) := by
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Topology\Algebra\StarSubalgebra.lean:137
```lean
abbrev commRingTopologicalClosure {R A} [CommRing R] [StarRing R] [TopologicalSpace A] [Ring A]
    [Algebra R A] [StarRing A] [StarModule R A] [IsSemitopologicalRing A] [ContinuousStar A]
    [T2Space A] (s : StarSubalgebra R A) (hs : ∀ x y : s, x * y = y * x) :
    CommRing s.topologicalClosure :=
  fast_instance% s.toSubalgebra.commRingTopologicalClosure hs
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\CStarAlgebra\ContinuousFunctionalCalculus\Unique.lean:461
```lean
lemma StarAlgHomClass.map_cfc (φ : F) (f : R → R) (a : A)
    (hf : ContinuousOn f (spectrum R a) := by cfc_cont_tac)
    (hφ : Continuous φ := by fun_prop) (ha : p a := by cfc_tac) (hφa : q (φ a) := by cfc_tac) :
    φ (cfc f a) = cfc f (φ a) := by
  let ψ : A →⋆ₐ[R] B := (φ : A →⋆ₐ[S] B).restrictScalars R
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarRegularRightPolar.lean:14
```lean
theorem scalarTomitaResolvent_regular_right_commutes (P : SiteProfile) (t : ℝ) :
    Commute (scalarTomitaResolvent P) (regularRightGNS P t) := by
  apply ContinuousLinearMap.ext
  intro z
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350CorePolarInclusion.lean:52
```lean
theorem scalarTomitaPolar_core_commutes (P : SiteProfile)
    (A B : (regularCoreAlgebra P).toStarSubalgebra) :
    Commute (antiunitaryConjugate (scalarTomitaPolarFactor P)
      (scalarGNSRepresentation P A)) (scalarGNSRepresentation P B) :=
  scalarGNS_commutation_from_generators P _ (scalarTomitaPolar_commutes_generators P A) B
```

