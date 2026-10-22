# Entrega autoral — A2 SUSY 012

[REAL] Ponte construída no mesmo regularCoreAlgebra P e traço A1. Quatro módulos rc0 no Lean 4.31.0; 29 declarações novas e cinco fornecedores auditados, todos apenas no trio propext / Classical.choice / Quot.sound. Três mutações recusadas com refutações formais rc0/trio. Revisão independente pendente.

O polar fornece a comparação de projeções para provar subaditividade de tauA1. O reticulado contém todas as projeções de N, com pertinência e identificação de ordem concretas. regularSusyData usa PF de A2: D=1-PF, D0=1, ker=gapD=diff=PF e gapD0=bottom. regularSusy_gives_breuer aplica diretamente TGLExt.susy_relative_gives_breuer. As identificações de operadores e o gap já pago em A2 acompanham o certificado.

[OPEN] Proposta gpf_H1_internal_susy_relative_gap_discharged apenas para esse representante matemático. Nenhuma identificação microscópica ou física; nenhuma edição de flag, gate, A2, Atlas ou túnel. O traço total e ThreeLocks permanecem com a bancada principal.

## Fontes e objetos

| Módulo | Fonte SHA256 lido | Objeto SHA256 lido | rc |
|---|---|---|---|
| TGLExt.V354BoundedPolar | 65ec2d9b95bba9281c2d30ab94632339021d6257a73fc86a493ac4f7d7469dd6 | 15a1e357711dfe5c084037ed54545c6c874f396b4b261930e56cb3aa4239307a | 0 |
| TGLExt.V354CoreProjectionLattice | 4f801a61c0b97048158888485326ed4ff871e822978fc5ba5e6904ea41dfa452 | c518f072289f2331a7c69a0fb998db7c1b2d91ed8ebec5b991bf1e776d27e35e | 0 |
| TGLExt.V354ProjectionTraceSubadditivity | c8bb9cf8626ececad4a104aa6e3de28ee51f38844f4d4562c1bc9524c14e9ce2 | 8cca254b1cedb1e00ca71a32d2c8b699865724c6cf63fe321b2d3da4520c0eb8 | 0 |
| TGLExt.V354RegularSusy | 8cdb715ac6b6daa2151a36f4b67d120bb2297eedefee32b8600e57b691c12d4f | c21ee3039d71b319f68eb019ec6fafdbf5baa109401558f9bfd02310b760fb07 | 0 |

Fontes pequenas para revisão em src/TGLExt; fontes compiladas em k/TGLExt. Bytes idênticos verificados. Sondas e auditoria em audit/TGLExt, com cópias compiladas em k/TGLExt. Os recibos de cada tentativa preservam snapshot, comando, saída e objeto.

## Comandos efetivamente executados

AUDITORIA.json guarda cada argv completo, cwd e todos os diretórios LEAN_PATH, além do SHA256 do compilador. run_lean.py reproduz a invocação em uma nova tentativa própria; não é necessário repetir os builds para ler esta entrega.

### TGLExt.V354BoundedPolar

```powershell
Set-Location -LiteralPath 'C:\IALD\Central de Patentes\Chatgpt\A2_SUSY_012'
python .\run_lean.py TGLExt.V354BoundedPolar
```

Resultado observado: rc0. Tentativa: C:\IALD\Central de Patentes\Chatgpt\A2_SUSY_012\attempts\20260915_171055_751369.
Invocação do Lean registrada: ["C:\\Users\\rotol\\.elan\\toolchains\\leanprover--lean4---v4.31.0\\bin\\lean.exe", "--root=C:\\IALD\\Central de Patentes\\Chatgpt\\A2_SUSY_012\\k", "-o", "C:\\IALD\\Central de Patentes\\Chatgpt\\A2_SUSY_012\\attempts\\20260915_171055_751369\\V354BoundedPolar.olean", "C:\\IALD\\Central de Patentes\\Chatgpt\\A2_SUSY_012\\k\\TGLExt\\V354BoundedPolar.lean"].

### TGLExt.V354CoreProjectionLattice

```powershell
Set-Location -LiteralPath 'C:\IALD\Central de Patentes\Chatgpt\A2_SUSY_012'
python .\run_lean.py TGLExt.V354CoreProjectionLattice
```

Resultado observado: rc0. Tentativa: C:\IALD\Central de Patentes\Chatgpt\A2_SUSY_012\attempts\20260915_171546_565375.
Invocação do Lean registrada: ["C:\\Users\\rotol\\.elan\\toolchains\\leanprover--lean4---v4.31.0\\bin\\lean.exe", "--root=C:\\IALD\\Central de Patentes\\Chatgpt\\A2_SUSY_012\\k", "-o", "C:\\IALD\\Central de Patentes\\Chatgpt\\A2_SUSY_012\\attempts\\20260915_171546_565375\\V354CoreProjectionLattice.olean", "C:\\IALD\\Central de Patentes\\Chatgpt\\A2_SUSY_012\\k\\TGLExt\\V354CoreProjectionLattice.lean"].

### TGLExt.V354ProjectionTraceSubadditivity

```powershell
Set-Location -LiteralPath 'C:\IALD\Central de Patentes\Chatgpt\A2_SUSY_012'
python .\run_lean.py TGLExt.V354ProjectionTraceSubadditivity
```

Resultado observado: rc0. Tentativa: C:\IALD\Central de Patentes\Chatgpt\A2_SUSY_012\attempts\20260915_171606_165772.
Invocação do Lean registrada: ["C:\\Users\\rotol\\.elan\\toolchains\\leanprover--lean4---v4.31.0\\bin\\lean.exe", "--root=C:\\IALD\\Central de Patentes\\Chatgpt\\A2_SUSY_012\\k", "-o", "C:\\IALD\\Central de Patentes\\Chatgpt\\A2_SUSY_012\\attempts\\20260915_171606_165772\\V354ProjectionTraceSubadditivity.olean", "C:\\IALD\\Central de Patentes\\Chatgpt\\A2_SUSY_012\\k\\TGLExt\\V354ProjectionTraceSubadditivity.lean"].

### TGLExt.V354RegularSusy

```powershell
Set-Location -LiteralPath 'C:\IALD\Central de Patentes\Chatgpt\A2_SUSY_012'
python .\run_lean.py TGLExt.V354RegularSusy
```

Resultado observado: rc0. Tentativa: C:\IALD\Central de Patentes\Chatgpt\A2_SUSY_012\attempts\20260915_171624_314873.
Invocação do Lean registrada: ["C:\\Users\\rotol\\.elan\\toolchains\\leanprover--lean4---v4.31.0\\bin\\lean.exe", "--root=C:\\IALD\\Central de Patentes\\Chatgpt\\A2_SUSY_012\\k", "-o", "C:\\IALD\\Central de Patentes\\Chatgpt\\A2_SUSY_012\\attempts\\20260915_171624_314873\\V354RegularSusy.olean", "C:\\IALD\\Central de Patentes\\Chatgpt\\A2_SUSY_012\\k\\TGLExt\\V354RegularSusy.lean"].

### TGLExt.AuditA2Susy

```powershell
Set-Location -LiteralPath 'C:\IALD\Central de Patentes\Chatgpt\A2_SUSY_012'
python .\run_lean.py TGLExt.AuditA2Susy
```

Resultado observado: rc0. Tentativa: C:\IALD\Central de Patentes\Chatgpt\A2_SUSY_012\attempts\20260915_171802_438822.
Invocação do Lean registrada: ["C:\\Users\\rotol\\.elan\\toolchains\\leanprover--lean4---v4.31.0\\bin\\lean.exe", "--root=C:\\IALD\\Central de Patentes\\Chatgpt\\A2_SUSY_012\\k", "-o", "C:\\IALD\\Central de Patentes\\Chatgpt\\A2_SUSY_012\\attempts\\20260915_171802_438822\\AuditA2Susy.olean", "C:\\IALD\\Central de Patentes\\Chatgpt\\A2_SUSY_012\\k\\TGLExt\\AuditA2Susy.lean"].

### TGLExt.ProbePolarSupports

```powershell
Set-Location -LiteralPath 'C:\IALD\Central de Patentes\Chatgpt\A2_SUSY_012'
python .\run_lean.py TGLExt.ProbePolarSupports
```

Resultado observado: rc0. Tentativa: C:\IALD\Central de Patentes\Chatgpt\A2_SUSY_012\attempts\20260915_171258_876292.
Invocação do Lean registrada: ["C:\\Users\\rotol\\.elan\\toolchains\\leanprover--lean4---v4.31.0\\bin\\lean.exe", "--root=C:\\IALD\\Central de Patentes\\Chatgpt\\A2_SUSY_012\\k", "-o", "C:\\IALD\\Central de Patentes\\Chatgpt\\A2_SUSY_012\\attempts\\20260915_171258_876292\\ProbePolarSupports.olean", "C:\\IALD\\Central de Patentes\\Chatgpt\\A2_SUSY_012\\k\\TGLExt\\ProbePolarSupports.lean"].

### TGLExt.ProbeRegularSusy

```powershell
Set-Location -LiteralPath 'C:\IALD\Central de Patentes\Chatgpt\A2_SUSY_012'
python .\run_lean.py TGLExt.ProbeRegularSusy
```

Resultado observado: rc0. Tentativa: C:\IALD\Central de Patentes\Chatgpt\A2_SUSY_012\attempts\20260915_171919_024764.
Invocação do Lean registrada: ["C:\\Users\\rotol\\.elan\\toolchains\\leanprover--lean4---v4.31.0\\bin\\lean.exe", "--root=C:\\IALD\\Central de Patentes\\Chatgpt\\A2_SUSY_012\\k", "-o", "C:\\IALD\\Central de Patentes\\Chatgpt\\A2_SUSY_012\\attempts\\20260915_171919_024764\\ProbeRegularSusy.olean", "C:\\IALD\\Central de Patentes\\Chatgpt\\A2_SUSY_012\\k\\TGLExt\\ProbeRegularSusy.lean"].

### TGLExt.BadPolarIdentity

```powershell
Set-Location -LiteralPath 'C:\IALD\Central de Patentes\Chatgpt\A2_SUSY_012'
python .\run_lean.py TGLExt.BadPolarIdentity
```

Resultado observado: rc1. Tentativa: C:\IALD\Central de Patentes\Chatgpt\A2_SUSY_012\attempts\20260915_171407_779703.
Invocação do Lean registrada: ["C:\\Users\\rotol\\.elan\\toolchains\\leanprover--lean4---v4.31.0\\bin\\lean.exe", "--root=C:\\IALD\\Central de Patentes\\Chatgpt\\A2_SUSY_012\\k", "-o", "C:\\IALD\\Central de Patentes\\Chatgpt\\A2_SUSY_012\\attempts\\20260915_171407_779703\\BadPolarIdentity.olean", "C:\\IALD\\Central de Patentes\\Chatgpt\\A2_SUSY_012\\k\\TGLExt\\BadPolarIdentity.lean"].

### TGLExt.BadSusyDifference

```powershell
Set-Location -LiteralPath 'C:\IALD\Central de Patentes\Chatgpt\A2_SUSY_012'
python .\run_lean.py TGLExt.BadSusyDifference
```

Resultado observado: rc1. Tentativa: C:\IALD\Central de Patentes\Chatgpt\A2_SUSY_012\attempts\20260915_171919_195550.
Invocação do Lean registrada: ["C:\\Users\\rotol\\.elan\\toolchains\\leanprover--lean4---v4.31.0\\bin\\lean.exe", "--root=C:\\IALD\\Central de Patentes\\Chatgpt\\A2_SUSY_012\\k", "-o", "C:\\IALD\\Central de Patentes\\Chatgpt\\A2_SUSY_012\\attempts\\20260915_171919_195550\\BadSusyDifference.olean", "C:\\IALD\\Central de Patentes\\Chatgpt\\A2_SUSY_012\\k\\TGLExt\\BadSusyDifference.lean"].

### TGLExt.BadSusyZeroTrace

```powershell
Set-Location -LiteralPath 'C:\IALD\Central de Patentes\Chatgpt\A2_SUSY_012'
python .\run_lean.py TGLExt.BadSusyZeroTrace
```

Resultado observado: rc1. Tentativa: C:\IALD\Central de Patentes\Chatgpt\A2_SUSY_012\attempts\20260915_171919_345394.
Invocação do Lean registrada: ["C:\\Users\\rotol\\.elan\\toolchains\\leanprover--lean4---v4.31.0\\bin\\lean.exe", "--root=C:\\IALD\\Central de Patentes\\Chatgpt\\A2_SUSY_012\\k", "-o", "C:\\IALD\\Central de Patentes\\Chatgpt\\A2_SUSY_012\\attempts\\20260915_171919_345394\\BadSusyZeroTrace.olean", "C:\\IALD\\Central de Patentes\\Chatgpt\\A2_SUSY_012\\k\\TGLExt\\BadSusyZeroTrace.lean"].

## Recibos e limites

- RECIBO.json: estatuto, propostas e pins das evidências.
- AUDITORIA.json e AUDIT_NAMES.json: builds e axiomas efetivamente lidos.
- CONTROLES.json: alterações exatas, erros e teoremas que refutam as mutações.
- FICHA_REAPROVEITAMENTO.md/json: ficha anterior ao código; adendos e REAPROVEITAMENTO_EFETIVO.json documentam decisões e consumidores.
- COPIA_A1.json, COPIA_A2.json, REUSO_OBJETOS_A2.json e REUSO_CORE_SUPPORT.json: proveniência da base reutilizada.
- PRESERVACAO_FONTES.json: 1014 fontes comparadas ao hash da cópia, todas preservadas.
- TENTATIVAS.json e FALHAS_E_LIMITES.md: erros anteriores, alcance e limites.
- MANIFESTO.json: inventário dos artefatos de revisão; SELOS.json: hashes lidos dos recibos principais.

Os saneamentos b,c,d,f,g,h e B1-prime pertencem às entregas anteriores; não foram reabertos por esta tarefa.
