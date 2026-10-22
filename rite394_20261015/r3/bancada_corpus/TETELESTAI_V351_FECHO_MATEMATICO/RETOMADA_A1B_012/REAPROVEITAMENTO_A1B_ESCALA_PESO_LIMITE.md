[OPEN — ficha anterior à escala dual do peso limite]

# A1(b): ação dual no mesmo candidato

2026-09-14T22:53:53.037290-03:00

Prove dual scaling of the SAME scalarInverseLimitWeight on existing TGLV351.positiveDual: tau(theta_s X)=ofReal(exp(-s))*tau(X). Adapt positive-square uniqueness for the existing hilbertPositiveSqrt, actual inverse-cutoff dual identity, original dual weight invariance and real homogeneity; no new root/GNS/cone. Then prove cofinality of r/(n+1) for r>0 using two supremum inequalities and existing regulator antitonicity, including infinite values. Four consumer-linked targets: root transport, cutoff weight transport, scaled sequence cofinality, limit dual scaling. Consumer is the exact dual_scaling field of RegularCoreTraceData, not a substitute trace contract. Semifinitude and traciality remain open.

ADAPTAR. A escala do peso tem sinal MENOS, obtida transportando o sanduíche por theta_(-s). A sequência de reguladores muda e sua cofinalidade precisa ser paga. Não confundir invariância do peso dual com tracialidade.

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseGeneratorCutoff.lean:81` — `f615a4a8b80a4bf970c719aa9d44fd2d917eb52f01fa1c925cfcab8151adc227`

```lean
theorem regularInverseGeneratorCutoff_dual (P : SiteProfile) (ε : ℝ) (hε : 0 < ε)
    (s : ℝ) :
    dualAmbient s (regularInverseGeneratorCutoff P ε) =
      (Real.exp s : ℂ) • regularInverseGeneratorCutoff P (ε*Real.exp s)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseGeneratorCutoff.lean:24` — `f615a4a8b80a4bf970c719aa9d44fd2d917eb52f01fa1c925cfcab8151adc227`

```lean
theorem regularInverseGeneratorCutoff_nonneg (P : SiteProfile) (ε : ℝ) (hε : 0 < ε) :
    0 ≤ regularInverseGeneratorCutoff P ε
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350DualWeightCuts.lean:40` — `cad8c916c67f1329afbac42658d13e8930e065e8f6a69152d4c9caf93cedd91b`

```lean
theorem dualAmbient_nonneg (s : ℝ)
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A) :
    0 ≤ dualAmbient s A
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350RegularDualAction.lean:42` — `e7c3628d969c0dae2a971c156200acb88f6bf4286a9c648a2ad3da08c468040c`

```lean
theorem dualAmbient_symm (s : ℝ) :
    (dualAmbient (H := H) s).symm = dualAmbient (-s)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350DualWeightForm.lean:87` — `3a233c43934c915774c68c23f0fca752d1c9dfc95679178c714394fe666a24b4`

```lean
theorem dualQuadraticIntegral_dual_invariant (r : ℝ)
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (v : RegularHilbert H) :
    dualQuadraticIntegral (dualAmbient r A) v = dualQuadraticIntegral A v
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350DualQuadraticLaws.lean:61` — `7085d5ad460720e87ea5e1e3cc8bcbf5b55193be77b2ba283988fbf03120c1f3`

```lean
theorem dualQuadraticIntegral_smul_operator (r : ℝ) (hr : 0 ≤ r)
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (v : RegularHilbert H) :
    dualQuadraticIntegral (r • A) v = ENNReal.ofReal r * dualQuadraticIntegral A v
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularCoreTraceContract.lean:15` — `3694175f8ef5bcf5848d88bd8061abf8546480873964ebfdc19dd41ad05928f0`

```lean
def positiveDual (P : SiteProfile) (s : ℝ) (A : PositiveCoreInput P) :
    PositiveCoreInput P
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseLimitWeight.lean:71` — `cfdced33d3cafdd2782f4d7e8ca77974e0ddee22f19803dfbd36275787c28f1e`

```lean
theorem scalarInverseCutoffWeight_antitone (P : SiteProfile)
    (ε η : ℝ) (hε : 0 < ε) (hη : 0 < η) (hεη : ε ≤ η) (X : PositiveCoreInput P) :
    scalarInverseCutoffWeight P η X ≤ scalarInverseCutoffWeight P ε X
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseLimitWeight.lean:87` — `cfdced33d3cafdd2782f4d7e8ca77974e0ddee22f19803dfbd36275787c28f1e`

```lean
def scalarInverseLimitWeight (P : SiteProfile) (X : PositiveCoreInput P) : ℝ≥0∞
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Analysis\SpecialFunctions\ContinuousFunctionalCalculus\Rpow\Basic.lean:294` — `ef03c823cc3798b288a7f00a2902b1fae092f1181bd44cb8b41ef133db389d5f`

```lean
lemma mul_self_eq_mul_self_iff (a b : A) (ha : 0 ≤ a := by cfc_tac) (hb : 0 ≤ b := by cfc_tac) :
    a * a = b * b ↔ a = b
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Algebra\Order\Archimedean\Basic.lean:213` — `e2b942510a5b1f8853dc1cb14e5d40d286a0b0dd3cc8434ad0dfbd5f81c25518`

```lean
lemma exists_nat_one_div_lt (hε : 0 < ε) : ∃ n : ℕ, 1 / (n + 1 : K) < ε
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\.lake\packages\mathlib\Mathlib\Data\ENNReal\Inv.lean:807` — `261c1dfb4e4f5f56462686c82a762fb3c1f4f9d2e5af144c94f64bb7aefadb89`

```lean
lemma mul_iSup (a : ℝ≥0∞) (f : ι → ℝ≥0∞) : a * ⨆ i, f i = ⨆ i, a * f i
```

Seis modalidades e outras bancadas: C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\search_inverse_limit_scaling\20260914_225331_852277\searches.json. Ausência nominal nos recortes não é ausência universal.
