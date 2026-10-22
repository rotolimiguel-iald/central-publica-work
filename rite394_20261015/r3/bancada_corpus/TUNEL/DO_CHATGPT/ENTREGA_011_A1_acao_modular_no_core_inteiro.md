[REAL — 5 teoremas e 0 definições verificados no delta por reprodução isolada autoral e revisão independente. A1(b): traço concreto ainda OPEN.]

# ENTREGA 011 / A1 — A ação das potências do mesmo Tomita no core inteiro

2026-09-14T19:39:42.636771-03:00

O mesmo U_t, construído do resolvente de S†S no GNS do peso escalar, satisfaz U_t π(A)x=π(Λ_t A Λ_t*)U_t x para todo A no core concreto. A prova passa das unidades matriciais aos níveis, à base e ao core usando os fornecedores existentes. A fase do transporte esquerdo é conjugada por J. Não se afirma U_t=π(Λ_t): o operador relativo pode estar no comutante.

Não constrói o gerador regular positivo afiliado nem o traço. Não acrescenta uma formalização separada da condição analítica KMS.

## Critérios

| Critério | Resultado |
|---|---|
| Ficha anterior e consumidor nomeado | PAGO; fichas integrais anexas, fornecedores pinados. |
| Mesmos espaços e fornecedores | PAGO no alcance dos tipos abaixo; fontes antigas preservadas. |
| Lake isolado e tipos completos | PAGO; autor e revisor rc0, sem herança de objetos DEV. |
| Axiomas | PAGO; somente propext, Classical.choice e Quot.sound, ou subconjuntos. |
| Adulteração | PAGO; controles autorais recusados por TypeMismatch; alcance e eventual leitura do revisor discriminados em seu parecer. |
| Revisão distinta da autoria | PAGO; nenhuma pendência P0/P1/P2 no delta. |
| Habitante do contrato do traço | NÃO PAGO por esta entrega. |
| Incorporação ao um.py / mudança de gate | NÃO EXECUTADA; escopo da gerência. |

## Reprodução

Autor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\core_attempts\20260914_184033_714941\run.json`. Comando registrado: `['C:\\Users\\rotol\\.elan\\toolchains\\leanprover--lean4---v4.31.0\\bin\\lake.exe', 'build', 'TGLExt.AuditA1CoreAction']`. Fonte e objeto autorais abaixo. Reutilização somente de objetos próprios previamente produzidos na raiz isolada; os pacotes externos vêm do cache explicitado no relatório. Não é nova compilação integral da biblioteca.

Revisor: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_core\independent_20260914_190209_340717\run.json`. `470` objetos próprios anteriores; `161` fornecedores antigos recompilados adicionalmente. Zero objetos do autor/DEV herdados; `0` avisos de alvos/auditor. Avisos de fornecedores e diferenças binárias estão preservados em compilation.json. Comparação indisponível não significa igualdade.

As tentativas de desenvolvimento que falharam permanecem em disco. Só o fonte final, as reproduções rc0 e as auditorias aceitas entram nesta conclusão. Controle negativo de uma aplicação adulterada não é um teorema geral de inexistência.

## Fontes e objetos autorais

| Módulo | SHA256 fonte | SHA256 objeto |
|---|---|---|
| `V351ScalarImaginaryLeftTransport` | `748f06367b522924203ca2904b0c2bac0a61dbf4df26790903453e7786bf749b` | `46d35f205a3e17a636866c31aa34ab2866e19e3d72600da4532bc03ba40fe0f9` |
| `V351ScalarImaginaryCoreAction` | `db4109dceeab1e948d7d5e664e8d76b347c719b00e62031761aaf5e924862a83` | `dc34632ca6e44ec80181992a3f00fb42a1f98cbe79502c670b70e9a739981a19` |

## Tipos completos e axiomas

```lean
TGLV350.Regular.matrixUnit_imaginaryPower_left_scaling (P : TGLExt.SiteProfile) (N : ℕ) (i j : TGLExt.chainIdx N)
  (t : ℝ) (x : ↥(TGLV350.Regular.ScalarGNSHilbert P)) :
  Eq.{1}
    ((TGLV350.Regular.scalarTomitaImaginaryPower P t)
      (((TGLV350.Regular.scalarGNSRepresentation P)
          (star.{0} (TGLV350.Regular.homogeneousRightCoreElement (TGLV350.Regular.matrixUnitRightData P N i j))))
        x))
    (HSMul.hSMul.{0, 0, 0} (star.{0} (ChatgptAudit.modularPhase t (Real.log (ChatgptAudit.localEigenvalue P N i j))))
      (((TGLV350.Regular.scalarGNSRepresentation P)
          (star.{0} (TGLV350.Regular.homogeneousRightCoreElement (TGLV350.Regular.matrixUnitRightData P N i j))))
        ((TGLV350.Regular.scalarTomitaImaginaryPower P t) x)))
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.scalarTomitaImaginaryPower_regular_left_commutes (P : TGLExt.SiteProfile) (s t : ℝ)
  (x : ↥(TGLV350.Regular.ScalarGNSHilbert P)) :
  Eq.{1}
    ((TGLV350.Regular.scalarTomitaImaginaryPower P t)
      (((TGLV350.Regular.scalarGNSRepresentation P) (star.{0} (TGLV350.Regular.regularRightCoreElement P s))) x))
    (((TGLV350.Regular.scalarGNSRepresentation P) (star.{0} (TGLV350.Regular.regularRightCoreElement P s)))
      ((TGLV350.Regular.scalarTomitaImaginaryPower P t) x))
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.matrixUnit_regular_core_conjugation (P : TGLExt.SiteProfile) (N : ℕ) (i j : TGLExt.chainIdx N) (t : ℝ) :
  Eq.{1}
    (HMul.hMul.{0, 0, 0}
      (HMul.hMul.{0, 0, 0} (TGLV350.Regular.regularRightCoreElement P t)
        ((TGLV350.Regular.localBaseCore P N) (Matrix.single.{0, 0, 0} i j 1)))
      (star.{0} (TGLV350.Regular.regularRightCoreElement P t)))
    (HSMul.hSMul.{0, 0, 0} (ChatgptAudit.modularPhase t (Real.log (ChatgptAudit.localEigenvalue P N i j)))
      ((TGLV350.Regular.localBaseCore P N) (Matrix.single.{0, 0, 0} i j 1)))
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.matrixUnit_imaginaryPower_base_scaling (P : TGLExt.SiteProfile) (N : ℕ) (i j : TGLExt.chainIdx N)
  (t : ℝ) (x : ↥(TGLV350.Regular.ScalarGNSHilbert P)) :
  Eq.{1}
    ((TGLV350.Regular.scalarTomitaImaginaryPower P t)
      (((TGLV350.Regular.scalarGNSRepresentation P)
          ((TGLV350.Regular.localBaseCore P N) (Matrix.single.{0, 0, 0} i j 1)))
        x))
    (HSMul.hSMul.{0, 0, 0} (ChatgptAudit.modularPhase t (Real.log (ChatgptAudit.localEigenvalue P N i j)))
      (((TGLV350.Regular.scalarGNSRepresentation P)
          ((TGLV350.Regular.localBaseCore P N) (Matrix.single.{0, 0, 0} i j 1)))
        ((TGLV350.Regular.scalarTomitaImaginaryPower P t) x)))
```

Axiomas: propext, Classical.choice, Quot.sound.

```lean
TGLV350.Regular.scalarTomitaImaginaryPower_core_conjugation (P : TGLExt.SiteProfile) (t : ℝ)
  (A : ↥(VonNeumannAlgebra.toStarSubalgebra.{0} (TGLV350.Regular.regularCoreAlgebra P)))
  (x : ↥(TGLV350.Regular.ScalarGNSHilbert P)) :
  Eq.{1} ((TGLV350.Regular.scalarTomitaImaginaryPower P t) (((TGLV350.Regular.scalarGNSRepresentation P) A) x))
    (((TGLV350.Regular.scalarGNSRepresentation P)
        (HMul.hMul.{0, 0, 0} (HMul.hMul.{0, 0, 0} (TGLV350.Regular.regularRightCoreElement P t) A)
          (star.{0} (TGLV350.Regular.regularRightCoreElement P t))))
      ((TGLV350.Regular.scalarTomitaImaginaryPower P t) x))
```

Axiomas: propext, Classical.choice, Quot.sound.

## Custódia e limites

- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\AUDITORIA_ACAO_CORE_A1B.json` — SHA256 `3d9ae54a045b2b4b1bd63036a49dfec9a0f427a0369ed865ebdeceb91ac9e691`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_core\REVIEW_A1_CORE_FINAL.json` — SHA256 `736fd42f0928546d60f144c314ccac47e019de7d12ed76ed5809c615257feba5`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_core\compilation.json` — SHA256 `4c7d2dafbad2582bfe4a129cf6027a7f61658a6e0fddf1c10fd906c44f0b0b7e`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\ACEITE_DELTA_CORE.json` — SHA256 `bc69ee73c7a77a147d6ba9182dd80833fb201cccd3c0f80ed4c3f44809064b27`.

O manifesto e o recibo próprios ligam esta entrega aos arquivos efetivamente lidos. Nenhum monólito canônico foi importado ou executado; nenhum dado experimental, D1, sigma, Atlas ou diário canônico foi alterado.

## Revisão independente integral

# A1: transporte esquerdo e ação no core inteiro — revisão independente

2026-09-14T19:38:08.990973-03:00

**A1_CORE_ACTION_REVIEW_ACCEPTED__TRACE_OPEN**

[REAL] Sem P0, P1 ou P2 no delta delimitado. 5 declarações (5 teoremas, 0 definições), relidas integralmente e reproduzidas pelo Lake próprio; #check com universos e #print axioms separados, somente propext/Classical.choice/Quot.sound.

[REAL — exame dos enunciados e provas] Os dois teoremas de V351ScalarImaginaryLeftTransport transportam as relações já obtidas à esquerda pelo MESMO J e U_t. A conjugação da fase no gerador adjunto é necessária: J é antilinear. A relação regular usa o elemento adjunto e depois o parâmetro −s. As provas não identificam J com um objeto auxiliar nem impõem uma hipótese nova de covariância.

[REAL] V351ScalarImaginaryCoreAction reverte os índices matriciais para recuperar a fase ordinária. Compara U_t e V_t=π(λ_t) através de D=V_t*U_t: as duas ações matriciais têm a mesma fase, portanto D comuta com as unidades matriciais. A indução matricial cobre cada nível; represented_levelExpectation_strong_tendsto passa à álgebra-base. A comutação com as translações usa a lei abeliana regular e o primeiro módulo. scalarGNS_commutation_from_generators recebe as duas famílias explicitamente; nenhum hgen fica como antecedente residual.

[REAL] O último enunciado quantifica todos P,t,A no core efetivo e x no H_I original: U_t π(A)x=π(λ_t A λ_t*)U_t x. O cancelamento usa as duas identidades unitárias de V_t. É a implementação concreta de Adλ no mesmo GNS, e não apenas invariância do peso ou comutação com uma subfamília. Não se conclui U_t=π(λ_t): a diferença relativa está no comutante.

[REAL — documentação e limites] As fichas ESQUERDA e ACAO_CORE foram lidas integralmente; seus fornecedores e pins são confrontados ao disco, e as buscas históricas são referências delimitadas, não uma alegação de busca exaustiva refeita. O código novo foi construído pelo principal; esta revisão faz o replay e exame independentes. Os dois auxiliares antiunitários antigos conservam a ressalva de autoria e a inspeção independente do principal já seladas na revisão40. Opções do fonte: maxHeartbeats=1500000 no transporte e 6000000 no core; synthInstance.maxHeartbeats=200000 no core. Nenhum limite foi alterado pelo revisor.

[REAL] Execução própria rc0 em 2101.32 s. 470 objetos próprios anteriores preservados; 161 fornecedores antigos adicionais precisaram de reprodução de fonte, além dos módulos deste delta e auditor. Zero objetos autorais/de DEV herdados. Os pacotes externos são cache copiado e pinado da revisão própria anterior, sem recompilação nesta chamada; essa herança não é uma nova auditoria integral da biblioteca. 0 avisos de alvo/auditor; 178 mensagens de fornecedores registradas no JSON (inclui mensagens de objetos anteriores). O aviso de cache aesop com alterações locais, quando presente, permanece no stderr.

Pins lidos dos fontes e objetos próprios:

| Módulo | SHA256 fonte | SHA256 .olean próprio | Igual ao cold build autoral disponível |
|---|---|---|---|
| TGLExt.V351ScalarImaginaryCoreAction | `db4109dceeab1e948d7d5e664e8d76b347c719b00e62031761aaf5e924862a83` | `dc34632ca6e44ec80181992a3f00fb42a1f98cbe79502c670b70e9a739981a19` | True |
| TGLExt.V351ScalarImaginaryLeftTransport | `748f06367b522924203ca2904b0c2bac0a61dbf4df26790903453e7786bf749b` | `46d35f205a3e17a636866c31aa34ab2866e19e3d72600da4532bc03ba40fe0f9` | True |

Comparações de bytes não são forçadas; objeto autoral ausente é comparação indisponível, não falha formal.

Controles: AUTHOR_CONTROLS_READ_AND_HASH_VERIFIED__TYPE_MISMATCH_NOT_ENVIRONMENT. A execução ou leitura correspondente está discriminada em compilation.json; nenhum controle autoral foi reexecutado por esta revisão.

[OPEN / limites] O delta paga a relação de implementação modular impressa, consumindo a construção anterior das potências do Tomita original. Não constrói o gerador positivo afiliado do grupo regular, sua perturbação, nem um habitante de RegularCoreTraceData; A1(b)/traço permanece aberto. Não há nova formalização de condição analítica KMS, nem alteração de gate, monólito, memórias ou escopos selados. Absorção, Fourier e grafo positivo serão aceitos ou recusados em relatórios separados; suas contagens não integram estas cinco declarações.

Artefatos próprios:

- [run](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_core\independent_20260914_190209_340717\run.json>) — SHA256 `ef2da91c5cc0096262fd88fe30854918d623655152b99ac7dc572f39ec24c14b`.
- [compilation](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_core\compilation.json>) — SHA256 `4c7d2dafbad2582bfe4a129cf6027a7f61658a6e0fddf1c10fd906c44f0b0b7e`.
- [tipos/axiomas](<C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\revisao_core\independent_20260914_190209_340717\type_axiom_audit.json>) — SHA256 `3444d3933fe96c1b1c5880b8d55379cfe7b84f9664e4c6cc3224ab58d67f5e05`.


## Ficha/adendo integral: REAPROVEITAMENTO_A1B_ESQUERDA

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


## Ficha/adendo integral: REAPROVEITAMENTO_A1B_ACAO_CORE

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
