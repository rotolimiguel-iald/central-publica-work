[OPEN — ficha anterior ao consumidor de semifinitude usual]

2026-09-14T23:10:26.452078-03:00

Consumer of the previously searched domain-cut route: for a in the ORIGINAL n_nu, show tau((a q_delta)* (a q_delta)) <= ofReal(delta^-1) nu(a*a) < infinity, then use q_n -> I strongly and the OLD WOT closure of n_nu to prove WOT closure of the square-finite set of the SAME tau is the same N. No new weight, square-root or cone. No traciality or finite-positive-minorant contract asserted. The old WOT theorem is imported from source, not re-proved.

Reaproveita as seis modalidades e outras bancadas da ficha do corte de domínio, cujo alvo já incluía este consumidor. Não repete a varredura integral nem cria outra raiz. Consulta independente foi lida inteira.

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularDomainCut.lean:33 — 60ed1575faca04fe95bb7fb208804944a84ac61114eede8ecbb28a67f9bed8e9

```lean
theorem regularDomainCut_right (P : SiteProfile) (δ : ℝ) (hδ : 0 < δ) :
    regularDomainCut P δ ∈ scalarPolarRightAlgebra P
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularDomainCut.lean:93 — 60ed1575faca04fe95bb7fb208804944a84ac61114eede8ecbb28a67f9bed8e9

```lean
theorem regularDomainCut_product_bound (P : SiteProfile) (ε δ : ℝ)
    (hε : 0 < ε) (hδ : 0 < δ) :
    regularInverseGeneratorCutoff P ε * (regularDomainCut P δ).val *
      (regularDomainCut P δ).val ≤ (δ⁻¹ : ℂ) • 1
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351RegularDomainCut.lean:113 — 60ed1575faca04fe95bb7fb208804944a84ac61114eede8ecbb28a67f9bed8e9

```lean
theorem regularDomainCut_tendsto_identity (P : SiteProfile)
    (v : RegularHilbert (TowerHilbert P)) :
    Tendsto (fun n : ℕ => (regularDomainCut P (1/((n : ℝ)+1))).val v) atTop (𝓝 v)
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseLimitWeight.lean:87 — cfdced33d3cafdd2782f4d7e8ca77974e0ddee22f19803dfbd36275787c28f1e

```lean
def scalarInverseLimitWeight (P : SiteProfile) (X : PositiveCoreInput P) : ℝ≥0∞
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351InverseCutoffCFC.lean:125 — cbdf10aea749a552b0f47afb3ef59560ed47d6f46cf7dd8064dc963a092c3490

```lean
theorem regularInverseGeneratorCutoff_sqrt_right (P : SiteProfile) (ε : ℝ) (hε : 0 < ε) :
    ∃ h : hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε) ∈ regularCoreAlgebra P,
      (⟨hilbertPositiveSqrt (regularInverseGeneratorCutoff P ε),h⟩ :
        (regularCoreAlgebra P).toStarSubalgebra) ∈ scalarPolarRightAlgebra P
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351PerturbedWeightOrder.lean:29 — 9af750ad0099449655e5350b76219d51986849e434584359bd09de475fe936d6

```lean
theorem scalarWeight_right_perturbed_mono (P : SiteProfile)
    (b c : (regularCoreAlgebra P).toStarSubalgebra)
    (hb : b ∈ scalarPolarRightAlgebra P) (hc : c ∈ scalarPolarRightAlgebra P)
    (hbc : b * star b ≤ c * star c) (A : scalarWeightLeftIdeal P) :
    dualQuadraticIntegral (star b.val * (star A.val.val*A.val.val) * b.val)
      (regularVacuum P) ≤
    dualQuadraticIntegral (star c.val * (star A.val.val*A.val.val) * c.val)
      (regularVacuum P)
```

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarWeightSemifiniteness.lean:16 — f5e7e85b034949be6517286f60c692d3d97d29c341aeba42a1f7172b7e610c2a

```lean
theorem scalarWeight_square_finite_wot_closure (P : SiteProfile) :
    closure {A : RegularHilbert (TowerHilbert P) →WOT[ℂ]
        RegularHilbert (TowerHilbert P) |
      A.toCLM ∈ regularCoreAlgebra P ∧ HasFiniteScalarSquare P A.toCLM} =
    {A : RegularHilbert (TowerHilbert P) →WOT[ℂ]
        RegularHilbert (TowerHilbert P) | A.toCLM ∈ regularCoreAlgebra P}
```

