[OPEN — ficha anterior ao consumidor da ação em todo o core]

# A1(b): ação modular na mesma representação

2026-09-14T17:57:39.355325-03:00

Consumidor: `regular_dual_weight_modular_implementation`, LACUNAS_A1.md:25. A entrega anterior de potências imaginárias, linha69, já nomeia este próximo uso.

```text
For all SiteProfile P, t : Real, A : (regularCoreAlgebra P).toStarSubalgebra, x : ScalarGNSHilbert P:
scalarTomitaImaginaryPower P t (scalarGNSRepresentation P A x) =
scalarGNSRepresentation P (regularRightCoreElement P t * A * star (regularRightCoreElement P t)) (scalarTomitaImaginaryPower P t x).
No additional covariance, density, normality, or trace hypothesis. This proves an operator relation on the whole actual represented core, not yet a faithful normal semifinite trace.
```

Use ordinary matrix-unit phase by reversing indices in the left-adjoint theorem. Compare U_t with V_t=pi(lambda_t) via D=V_t* U_t (star on V_t). D commutes with matrix units, hence with finite matrices; pass to the base by the existing represented strong limit; use existing generator-to-core commutation; cancel V_t with its adjoint. No new representation, flow, GNS, weight, normality or density construction.

## Fornecedores e tipos

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarImaginaryLeftTransport.lean:14` — `748f06367b522924203ca2904b0c2bac0a61dbf4df26790903453e7786bf749b` — DEV_NOT_YET_REVIEWED

```lean
theorem matrixUnit_imaginaryPower_left_scaling (P : SiteProfile) (N : ℕ)
    (i j : chainIdx N) (t : ℝ) (x : ScalarGNSHilbert P) :
    scalarTomitaImaginaryPower P t
        (scalarGNSRepresentation P
          (star (homogeneousRightCoreElement (matrixUnitRightData P N i j))) x) =
      star (modularPhase t (Real.log (localEigenvalue P N i j))) •
        scalarGNSRepresentation P
          (star (homogeneousRightCoreElement (matrixUnitRightData P N i j)))
          (scalarTomitaImaginaryPower P t x)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarImaginaryLeftTransport.lean:33` — `748f06367b522924203ca2904b0c2bac0a61dbf4df26790903453e7786bf749b` — DEV_NOT_YET_REVIEWED

```lean
theorem scalarTomitaImaginaryPower_regular_left_commutes (P : SiteProfile)
    (s t : ℝ) (x : ScalarGNSHilbert P) :
    scalarTomitaImaginaryPower P t
        (scalarGNSRepresentation P (star (regularRightCoreElement P s)) x) =
      scalarGNSRepresentation P (star (regularRightCoreElement P s))
        (scalarTomitaImaginaryPower P t x)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350MatrixUnitRightSquare.lean:51` — `27403f0368e77e9e8e9c1de5dfdb71e6ccd740a280c13afcbc6c6f68e43a07b9` — EXISTING_SUPPLIER

```lean
theorem matrixUnit_rightCore_star (P : SiteProfile) (N : ℕ) (i j : chainIdx N) :
    homogeneousRightCoreElement (matrixUnitRightData P N j i) =
      star (homogeneousRightCoreElement (matrixUnitRightData P N i j))
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350MatrixUnitRightSquare.lean:11` — `27403f0368e77e9e8e9c1de5dfdb71e6ccd740a280c13afcbc6c6f68e43a07b9` — EXISTING_SUPPLIER

```lean
theorem localEigenvalue_reverse_log (P : SiteProfile) (N : ℕ) (i j : chainIdx N) :
    -Real.log (localEigenvalue P N j i) = Real.log (localEigenvalue P N i j)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350RegularTowerRepresentation.lean:54` — `21638dcca0d86b6a62050dee85212ee74cf07d783e43bdf6fecd28a04fb5b41f` — EXISTING_SUPPLIER

```lean
theorem regular_covariance (P : SiteProfile) (t : ℝ)
    (A : TowerHilbert P →L[ℂ] TowerHilbert P) :
    regularUnitary P t * fibre A * star (regularUnitary P t) =
      fibre (modularConjugation P t A)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350RegularTowerRepresentation.lean:42` — `21638dcca0d86b6a62050dee85212ee74cf07d783e43bdf6fecd28a04fb5b41f` — EXISTING_SUPPLIER

```lean
theorem regular_unitary (P : SiteProfile) (t : ℝ) :
    star (regularUnitary P t) * regularUnitary P t = 1 ∧
      regularUnitary P t * star (regularUnitary P t) = 1
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\ModularFlowAlgebra.lean:67` — `28901cdfdd69d05df6828fd92ba55499de97f4cb93cf919e61077cd5f3e8679c` — EXISTING_SUPPLIER

```lean
theorem modularConjugation_local (t : ℝ) {N : ℕ}
    (a : Matrix (chainIdx N) (chainIdx N) ℂ) :
    modularConjugation P t (towerPi P a) = towerPi P (flowLevel P t N a)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\ModularFlowSpectrum.lean:49` — `49eaf5a1556de26c4c5ba45a5ced7b5a4b454cce8446158aeb10b9bd12109606` — EXISTING_SUPPLIER

```lean
theorem flowLevel_single (t : ℝ) (N : ℕ) (i j : chainIdx N) :
    flowLevel P t N (Matrix.single i j 1) =
      modularPhase t (Real.log (localEigenvalue P N i j)) • Matrix.single i j 1
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350LocalBasePolarCommutation.lean:29` — `6a81d480bf6997282bdd5734b99e8d50ac17e532ad390ae108866130b94046a4` — EXISTING_SUPPLIER

```lean
def localBaseCore (P : SiteProfile) (N : ℕ) :
    Matrix (chainIdx N) (chainIdx N) ℂ →ₗ[ℂ] (regularCoreAlgebra P).toStarSubalgebra
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350LevelExpectationStrongLimit.lean:44` — `c5030991cc5894f56885c612b0fbcd1502de9c0f0d68e6740fd50227054eb165` — EXISTING_SUPPLIER

```lean
theorem represented_levelExpectation_strong_tendsto (P : SiteProfile)
    (A : (theFactorObject P).toStarSubalgebra) (v : ScalarGNSHilbert P) :
    Tendsto (fun N => scalarGNSRepresentation P (levelCoreApproximation P N A) v) atTop
      (𝓝 (scalarGNSRepresentation P (regularCoreEmbedding P A) v))
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350BasePolarStrongLimit.lean:23` — `2c3ac3e1ddf59dff0db486d2bcc26e4507a014f3c7ee651fb54ce6dd77b13268` — EXISTING_SUPPLIER

```lean
theorem commute_of_strong_tendsto {H : Type} [NormedAddCommGroup H]
    [InnerProductSpace ℂ H] [CompleteSpace H]
    {ι : Type*} {l : Filter ι} [NeBot l] (T : ι → H →L[ℂ] H) (A B : H →L[ℂ] H)
    (hT : ∀ v, Tendsto (fun n => T n v) l (𝓝 (A v)))
    (hc : ∀ n, Commute (T n) B) : Commute A B
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarGNSGeneratorTransport.lean:68` — `ed7ce8c1e5693f28277f3de7d7fcb0c3a43359d0fe02903a7922280bfcb858af` — EXISTING_SUPPLIER

```lean
theorem scalarGNS_commutation_from_generators (P : SiteProfile)
    (T : ScalarGNSHilbert P →L[ℂ] ScalarGNSHilbert P)
    (hT : ∀ A ∈ scalarCoreGenerators P, Commute T (scalarGNSRepresentation P A)) :
    ∀ A : (regularCoreAlgebra P).toStarSubalgebra,
      Commute T (scalarGNSRepresentation P A)
```

## Buscas e critério

Seis modalidades em BUSCAS_A1B_ACAO_CORE.json: kernel, notas, entregas/outras bancadas, árvore, TOE, índice do acervo. As buscas acharam os fornecedores acima, e não um teorema com o tipo final nos recortes consultados. O índice retornou zero em13608arquivos; isso não demonstra ausência fora do índice.

Os dois lemas à esquerda estão em desenvolvimento aceito pelo compilador, ainda não em entrega auditada. São dependências explicitamente pendentes. A aceitação do novo consumidor exige Lake isolado, axiomas no trio, controles negativos pertinentes e revisão independente. Depois dele, a construção do traço continua aberta nos endereços nomeados no JSON. Nenhuma nova camada de GNS, fluxo, normalidade ou peso é autorizada por esta ficha.
