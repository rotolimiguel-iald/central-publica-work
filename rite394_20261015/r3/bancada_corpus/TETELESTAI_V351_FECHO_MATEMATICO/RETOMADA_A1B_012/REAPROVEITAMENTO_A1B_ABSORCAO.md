[OPEN — ficha anterior à equivalência do grupo regular com a translação]

# A1(b): absorção do fluxo pela coordenada regular

2026-09-14T18:20:06.336840-03:00

Consumidor: `regular_unitary_positive_generator`, LACUNAS_A1.md:31. A rota explícita está em ROTA_GERADOR_REGULAR_A1B.

```text
Build W : unitary (RegularHilbert (TowerHilbert P) →L[Complex] RegularHilbert (TowerHilbert P)) from the existing field x ↦ modularFlowCLM P x. For every P,t, prove W.val * shift t * star W.val = regularUnitary P t. Use operatorFieldLift; prove its adjoint/group/zero identities with field argument scale a only to supply W and its inverse. No new L2, Fourier, modular flow, or GNS. W need not belong to the regular core; do not assert this.
```

O campo é uma instanciação do operatorFieldLift já existente. a é argumento auxiliar da composição de campos; não é parâmetro físico, nem beta. Duas definições (família, unitário) e quatro lemas usados na construção e no consumo. W não é presumido elemento de N. Sem declarar Fourier, traço ou gerador como construídos.

## Fornecedores

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350OperatorFieldAlgebra.lean:57` — `ccd8bfa143d144167dfe9e395b1c9edd0472cc4f73d94f0d7b32e079b8bb8b2d`

```lean
theorem operatorFieldLift_star (F G : StrongIntegral.Family (H
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350OperatorFieldAlgebra.lean:33` — `ccd8bfa143d144167dfe9e395b1c9edd0472cc4f73d94f0d7b32e079b8bb8b2d`

```lean
theorem operatorFieldLift_mul (F G K : StrongIntegral.Family (H
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350OperatorFieldAlgebra.lean:12` — `ccd8bfa143d144167dfe9e395b1c9edd0472cc4f73d94f0d7b32e079b8bb8b2d`

```lean
theorem operatorFieldLift_constant (F : StrongIntegral.Family (H
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350StrongOperatorField.lean:68` — `83fcc9ee4e6cdecee9f130183b7d1e6a0e2436caf40670e4d64dce8933f86a4c`

```lean
theorem operatorFieldLift_ae (F : StrongIntegral.Family (H
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350RegularTowerRepresentation.lean:16` — `21638dcca0d86b6a62050dee85212ee74cf07d783e43bdf6fecd28a04fb5b41f`

```lean
def regularUnitary (P : SiteProfile) (t : ℝ) :
    RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350L2Translation.lean:19` — `1fc45298e186caf37d2b04779e64f3e000e7384511bede3bdce57ab9b429b267`

```lean
theorem shift_ae (t : ℝ) (f : RegularHilbert H) :
    shift t f =ᵐ[volume] fun x : ℝ => f (x-t)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\TheModularFlowIsAHorizon.lean:29` — `df9dac92716643a471172afce44a2a158736b2988d51c42ff814505d339b3e7d`

```lean
theorem modularFlowCLM_mul (s t : ℝ) :
    modularFlowCLM P s * modularFlowCLM P t = modularFlowCLM P (s + t)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\TheModularFlowIsAHorizon.lean:40` — `df9dac92716643a471172afce44a2a158736b2988d51c42ff814505d339b3e7d`

```lean
theorem modularFlowCLM_star (t : ℝ) : star (modularFlowCLM P t) = modularFlowCLM P (-t)
```

`C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\RETOMADA_A1B_012\k\TGLExt\V350RegularTowerRepresentation.lean:68` — `21638dcca0d86b6a62050dee85212ee74cf07d783e43bdf6fecd28a04fb5b41f`

```lean
theorem modularFlowCLM_isometry (P : SiteProfile) (t : ℝ) :
    modularFlowCLM P t = (modularFlowIsometry P t).toContinuousLinearMap
```

## Buscas

Seis modalidades e recorte adicional em outras bancadas nos JSONs pinados. Foram localizados os fornecedores genéricos e o alvo nomeado nas entregas, não a identidade completa nos recortes consultados. O alcance do índice não é todo o computador. Nenhum fornecedor antigo será alterado. A aceitação exige compilação própria, axiomas e revisão, em entrega separada dos5lemas de ação no core.
