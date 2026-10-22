[OPEN — ficha antes dos dois lemas de transporte à esquerda]

# A1(b) — mesma ação no lado esquerdo

2026-09-14T17:38:40.481430-03:00

ADAPTAR os fornecedores existentes; duas composições tipadas, sem definir outro operador, J, GNS, raiz ou peso.

Consumidor: `regular_dual_weight_modular_implementation`, LACUNAS_A1.md:25. Esta é a etapa dos geradores na mesma representação, anterior à extensão para todo o core e identificação com AdLambda. Contrato final: TGLV351.RegularCoreTraceData.

## Tipo exato

```text
For every SiteProfile P,N,i,j,t,x on ScalarGNSHilbert P, with U=scalarTomitaImaginaryPower P, J=scalarTomitaPolarFactor P, R=homogeneousRightGNS(matrixUnitRightData P N i j), A=star(homogeneousRightCoreElement(matrixUnitRightData P N i j)), r=localEigenvalue P N i j:
 U_t (scalarGNSRepresentation P A x)=star(modularPhase t (Real.log r)) • scalarGNSRepresentation P A (U_t x).
For A_s=star(regularRightCoreElement P s):
 U_t (scalarGNSRepresentation P A_s x)=scalarGNSRepresentation P A_s (U_t x).
No premise asserting either conclusion; use J injective, J U=U J, the existing weighted J-left/right relation and right scaling. Two theorems only, no new operator/structure.
```

## Fornecedores

### TGLV350.Regular.matrixUnit_imaginaryPower_right_scaling

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarImaginaryRightTransport.lean:14` · `5442a451387b2c784b74023fea3d6dc31b42e35e3ccdefa8174dbf582eece349`
```lean
theorem matrixUnit_imaginaryPower_right_scaling (P : SiteProfile) (N : ℕ)
    (i j : chainIdx N) (t : ℝ) (x : ScalarGNSHilbert P) :
    scalarTomitaImaginaryPower P t (homogeneousRightGNS (matrixUnitRightData P N i j) x)=
      modularPhase t (Real.log (localEigenvalue P N i j)) •
        homogeneousRightGNS (matrixUnitRightData P N i j) (scalarTomitaImaginaryPower P t x)
```
REUSAR a premissa intermediária; nenhuma recebe a conclusão nova.

### TGLV350.Regular.scalarTomitaImaginaryPower_regular_right_commutes

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarImaginaryRightTransport.lean:27` · `5442a451387b2c784b74023fea3d6dc31b42e35e3ccdefa8174dbf582eece349`
```lean
theorem scalarTomitaImaginaryPower_regular_right_commutes (P : SiteProfile) (s t : ℝ)
    (x : ScalarGNSHilbert P) :
    scalarTomitaImaginaryPower P t (regularRightGNS P s x)=
      regularRightGNS P s (scalarTomitaImaginaryPower P t x)
```
REUSAR a premissa intermediária; nenhuma recebe a conclusão nova.

### TGLV350.Regular.scalarTomitaImaginaryPower_polar_commutes

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V351ScalarTomitaImaginaryConjugation.lean:14` · `981dda6d5a16272efdbcfa46cd674bb66eaa0179d70634a9a9bcc2c5332b4c9d`
```lean
theorem scalarTomitaImaginaryPower_polar_commutes (P : SiteProfile) (t : ℝ)
    (x : ScalarGNSHilbert P) :
    scalarTomitaPolarFactor P (scalarTomitaImaginaryPower P t x) =
      scalarTomitaImaginaryPower P t (scalarTomitaPolarFactor P x)
```
REUSAR a premissa intermediária; nenhuma recebe a conclusão nova.

### TGLV350.Regular.matrixUnit_polar_left_weighted

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350MatrixUnitPolarTransport.lean:56` · `0d800d33855d55cb7c228771610ad0cdb061fb89d387aa3ca56367cf4aa173cb`
```lean
theorem matrixUnit_polar_left_weighted (P : SiteProfile) (N : ℕ) (i j : chainIdx N)
    (z : ScalarGNSHilbert P) :
    scalarTomitaPolarFactor P
      (scalarGNSRepresentation P (star (homogeneousRightCoreElement (matrixUnitRightData P N i j))) z) =
    (Real.sqrt (localEigenvalue P N i j) : ℂ) •
      homogeneousRightGNS (matrixUnitRightData P N i j) (scalarTomitaPolarFactor P z)
```
REUSAR a premissa intermediária; nenhuma recebe a conclusão nova.

### TGLV350.Regular.scalarTomitaPolarFactor_regular_left

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarRegularRightPolar.lean:113` · `cab5601b5e0a1e1ef950638a2025c814488c3f5baa083c14d85028a1ca9d95c9`
```lean
theorem scalarTomitaPolarFactor_regular_left (P : SiteProfile) (t : ℝ)
    (z : ScalarGNSHilbert P) :
    scalarTomitaPolarFactor P
      (scalarGNSRepresentation P (star (regularRightCoreElement P t)) z) =
        regularRightGNS P t (scalarTomitaPolarFactor P z)
```
REUSAR a premissa intermediária; nenhuma recebe a conclusão nova.

### TGLV350.Regular.scalarTomitaPolarFactor

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350ScalarTomitaPolarFactor.lean:44` · `66b8ca1222b639f710ccca3b52f6ab836262b977e023da487057e850a5f415ca`
```lean
def scalarTomitaPolarFactor : ScalarGNSHilbert P ≃ₛₗᵢ[starRingEnd ℂ] ScalarGNSHilbert P
```
REUSAR a premissa intermediária; nenhuma recebe a conclusão nova.

## Buscas e limites

As seis modalidades e os recortes estão nos três JSONs de buscas: kernel local por nome/tipo, notasV350, entregas/outrasbancadas, árvoreA1, TOE e índiceacervo. As leituras recusadas pelo sandbox foram repetidas; o TOE não apresentou ocorrência. O padrão largo Imaginary.*Left encontrou caminhos serializados e foi corrigido; o padrão final de nomes exatos retornou zero em13608arquivos indexados. Não se afirma ausência em todo arquivo do computador.

O sinal conjugado decorre da antilinearidade de J; não pode ser apagado. A comparação da frequência desse gerador com AdLambda precisa de outro lema consumidor, não de homonímia. Não se prova existência de traço nem H3. O delta não altera os sete módulos existentes ou seus resultados; suas reproduções standalone seguem em paralelo.
