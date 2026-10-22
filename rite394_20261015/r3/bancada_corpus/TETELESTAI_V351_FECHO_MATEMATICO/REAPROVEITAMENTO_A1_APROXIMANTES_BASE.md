[REAPROVEITAMENTO — ANTES DO CÓDIGO]

# A1: aproximantes positivos na base

2026-09-14T08:54:01.909739-03:00

A1(b), ponte 1: valores preduais do peso dual; depois ponte 4 para RegularCoreTraceData

Para P, A∈N positivo e c>0: produzir D_c∈M, 0≤D_c≤c I, cujo valor amplificado é inf_w(q_A(w)+c||w-v||²); depois crescimento e sup_c q_Dc=q_A. Nenhum traço é prometido por este lema.

ADAPTAR resolvente do input A/c, formar c(1-R_c) no fixo F e usar a equivalência concreta F=M. NOVO apenas as identidades variacionais e aproximação necessárias para o predual; não reconstruir resolvente ou integral.

## structure RegularCoreTraceData

CONSUMIDOR

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V351RegularCoreTraceContract.lean:43

SHA256 `3694175f8ef5bcf5848d88bd8061abf8546480873964ebfdc19dd41ad05928f0`

```lean
structure RegularCoreTraceData (P : SiteProfile) where
```

## def baseDualWeight

ADAPTAR: aproximação por operadores positivos da mesma base

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V351ExtendedBaseDualWeight.lean:39

SHA256 `1ea9226e3fe1ee75bc66178f575f47c0207e80dca34a0113efd0c0f099b7cd87`

```lean
def baseDualWeight (P : SiteProfile) (A : PositiveCoreInput P) :
    AffiliatedPositiveForm (theFactorObject P) :=
```

## theorem exists_dualResolvent_fixed

REUSAR

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350DualResolventFixed.lean:78

SHA256 `1d1805ed2f6544c3a11cdfecf503258448681ef49376af4409d80de7d8570056`

```lean
theorem exists_dualResolvent_fixed (P : TGLExt.SiteProfile)
    (A : RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ]
      RegularHilbert (TGLExt.TowerHilbert P))
    (hA : A ∈ regularCoreAlgebra P) (hpos : 0 ≤ A) :
    ∃ R : RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ]
      RegularHilbert (TGLExt.TowerHilbert P),
      R ∈ regularCoreAlgebra P ∧ 0 ≤ R ∧ R ≤ 1 ∧
      (∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v))) ∧
      (∀ s : ℝ, dualAmbient s R = R) := by
```

## theorem dualResolvent_limit_minimizes_energy

REUSAR

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350DualVariational.lean:76

SHA256 `c375e63d7cc8415d90c8663e9230b9696171ba3138f8b1fe250bb5898938cee0`

```lean
theorem dualResolvent_limit_minimizes_energy
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v)))
    (v w : RegularHilbert H) : dualEnergy A v (R v) ≤ dualEnergy A v w := by
```

## theorem dualResolvent_limit_energy_identity

REUSAR

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350DualEnergyOnResolvent.lean:56

SHA256 `020b86bf18e19388c8716b046fc0276fde43216a2782d52de6c27dfabc941c5d`

```lean
theorem dualResolvent_limit_energy_identity
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v)))
    (v : RegularHilbert H) :
    (dualQuadraticIntegral A (R v)).toReal = (inner ℂ (R v) (v-R v)).re := by
```

## theorem dualQuadraticIntegral_smul_operator

REUSAR

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350DualQuadraticLaws.lean:61

SHA256 `7085d5ad460720e87ea5e1e3cc8bcbf5b55193be77b2ba283988fbf03120c1f3`

```lean
theorem dualQuadraticIntegral_smul_operator (r : ℝ) (hr : 0 ≤ r)
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (v : RegularHilbert H) :
    dualQuadraticIntegral (r • A) v = ENNReal.ofReal r * dualQuadraticIntegral A v := by
```

## theorem dualFixedCore_eq_amplified_base

REUSAR

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350FixedCoreBaseIdentification.lean:21

SHA256 `0454ce14669be84c8384143a8ace33b7e795bc5b262355afc97284d1a963f4a1`

```lean
theorem dualFixedCore_eq_amplified_base (P : SiteProfile)
    (B : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P)) :
    B ∈ dualFixedCore P ↔ ∃ C ∈ theFactorObject P, B = fibre C := by
```

## def fixedBaseOrderIso

REUSAR

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350FixedBaseEquivalence.lean:44

SHA256 `6b4cda490d27efc86fdac21e57b91c30778477221d08ff9c90f31a1bf8b8f278`

```lean
def fixedBaseOrderIso (P : SiteProfile) :
    (theFactorObject P).toStarSubalgebra ≃o (dualFixedCore P).toStarSubalgebra where
```

## theorem exists_dual_form_representation

não usar por homônimo

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350DualFormRepresentation.lean:?

SHA256 `842848ee7e13c1ab8d7c0d189e33db5a5e459f76dde0ab54c0265719043a487c`

```lean
NAO_LOCALIZADO_POR_ESSE_NOME
```

Busca adicional e seis modalidades prévias: comandos, resultados e hashes no JSON. Não se afirma ausência universal de fornecedor. A dependência imediata é a representação no predual; a aceitação A1(b) continua aberta até existir o traço.
