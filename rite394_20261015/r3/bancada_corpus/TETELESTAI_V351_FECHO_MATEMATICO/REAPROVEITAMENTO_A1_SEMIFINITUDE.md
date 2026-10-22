[REAPROVEITAMENTO — ANTES DO CÓDIGO FORMAL]

# A1: semifinitude pelo domínio do peso

A1(b), LACUNAS_A1.md item 1: semi-finitude usual de scalarDualWeight; não usar o campo de minorantes do contrato tracial para um peso não tracial.

Alvo exato:
```lean
closure {A : RegularHilbert (TowerHilbert P) →WOT[ℂ] RegularHilbert (TowerHilbert P) | A.toCLM ∈ regularCoreAlgebra P ∧ HasFiniteScalarSquare P A.toCLM} = {A | A.toCLM ∈ regularCoreAlgebra P}
```

ADAPTAR: aplicar strong_tendsto_wot à aproximação forte já paga, e a clausura WOT ao outro sentido. Não reconstruir médias.

## def HasFiniteScalarSquare

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350ScalarWeightDomain.lean:14 · SHA256 e83ada9b5abbf2c179c28b03d3c020be83861681ba3ae450999c1c64ea8e2f0f

```lean
def HasFiniteScalarSquare (P : SiteProfile)
    (A : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P)) : Prop :=
```

## def scalarWeightLeftIdeal

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350ScalarWeightDomain.lean:43 · SHA256 e83ada9b5abbf2c179c28b03d3c020be83861681ba3ae450999c1c64ea8e2f0f

```lean
def scalarWeightLeftIdeal (P : SiteProfile) :
    Submodule ℂ (regularCoreAlgebra P).toStarSubalgebra where
```

## theorem scalarDualWeight_square_finite_strong_density

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350ScalarDualWeight.lean:66 · SHA256 e20dc5262ec98b62c8a6797fd07492e584a03fefefd0dd87b1666484dd72bc53

```lean
theorem scalarDualWeight_square_finite_strong_density (P : SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra) :
    (∀ h : ℝ, 0 < h → dualQuadraticIntegral
      (star (A.val * regularAverage P h) * (A.val * regularAverage P h)) (regularVacuum P) < ⊤) ∧
    (∀ h : ℝ, A.val * regularAverage P h ∈ regularCoreAlgebra P) ∧
    (∀ v, Tendsto (fun h : ℝ => (A.val * regularAverage P h) v) (𝓝[>] 0) (𝓝 (A.val v))) := by
```

## theorem strong_tendsto_wot

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350RegularNormality.lean:19 · SHA256 bcd49e92800bf99d7770bb9969879be02a9768f129ce842ae2f39cefaca3cc0a

```lean
theorem strong_tendsto_wot {ι : Type*} {l : Filter ι}
    (T : ι → (H →L[ℂ] H)) (B : H →L[ℂ] H)
    (hstrong : ∀ v, Tendsto (fun i => T i v) l (𝓝 (B v))) :
    Tendsto (fun i => ContinuousLinearMapWOT.ofCLM (T i)) l
      (𝓝 (ContinuousLinearMapWOT.ofCLM B)) := by
```

## theorem regularCore_wot_closed

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350RegularTopology.lean:39 · SHA256 13c92b1d8948bc4d2c3891d4cbfa9bf43ac353a95e9126e2c128b1379db0ebd5

```lean
theorem regularCore_wot_closed (P : TGLExt.SiteProfile) :
    IsClosed {A : RegularHilbert (TGLExt.TowerHilbert P) →WOT[ℂ]
      RegularHilbert (TGLExt.TowerHilbert P) | A.toCLM ∈ regularCoreAlgebra P} :=
```

## theorem baseDualWeight_unit_infinite

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V351ExtendedBaseDualWeight.lean:126 · SHA256 1ea9226e3fe1ee75bc66178f575f47c0207e80dca34a0113efd0c0f099b7cd87

```lean
theorem baseDualWeight_unit_infinite (P : SiteProfile) (v : TowerHilbert P) (hv : v ≠ 0) :
    (baseDualWeight P (positiveUnit P)).value v = ⊤ := by
```

A ficha inicial de A1 guarda as seis modalidades de busca. Consulta independente: revisao/CONSULTA_A1_RESTRICAO_FORMAS_BASE.md. A distinção peso/traço é verificada na definição 7.1 de Hiai, https://arxiv.org/pdf/2004.02383. Não se declara aqui densidade na topologia de norma nem construção do traço.
