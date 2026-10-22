[REAL / INPUT / OPEN] ENTREGA 012 ESPONTÂNEA — densidade de área geométrica e restrição dinâmica da entropia.

Continuação de 011, 05/09/2026. Nenhuma ordem 012 da gerência estava no túnel ao publicar. Pronta para auditoria independente; não altera gate nem conclui gravitação quântica.

## Critérios e alcance

| Critério | Estado | Evidência |
|---|---|---|
| Derivação antes do código | PAGO | Derivação inicial e adendo anterior à correção de assinatura. |
| Área independente da entropia | PAGO como densidade local | A=√det(SᵀgS), definida da métrica e de duas direções transversais. |
| Lei de variação geométrica | PAGO sob dados explícitos | coordinate_screen_area_derivative: A′=tr(∇V)A, via determinante, compatibilidade métrica e transporte. |
| Igualdade das duas expansões | PAGO | ambient_expansion_is_screen_trace, com referencial nulo, Bk=0 e g(k,Bn)=0. |
| Reconstrução com área calculada | PAGO como implicação | GeometricHorizonPencil não recebe area/area_rate; geometricHorizonToLocal os calcula e a reconstrução usa o tensor de Einstein efetivo. |
| Direções não nulas | PAGO | Testemunhos exigidos apenas para v≠0; a forma quadrática na direção zero é tratada diretamente. |
| Contrato habitado | PAGO no caso plano | flatGeometricHorizon, direção (1,1,0,0), tela constante e A=1 calculada; três definições de testemunhos com axiomas impressos. |
| Correção de assinatura | PAGO | eta4 tem convenção +---; tela espacial h₀₀<0, det h>0. screen_area_signature_flip; controle plano final passou. |
| Entropia fixa e área variável | PAGO como obstrução local | Igualdade no ponto e no ramo passado, η≠0 e A≠0 forçam θ=0 para entropia congelada. |
| Variação dos pesos | PAGO como condição necessária | Σq_i(−log p_i)=ηθA(0), se a lei entropia-área vale para a perturbação normalizada. |
| Existência geral e vínculo quântico | NÃO PAGO | Telas/congruências gerais, imersão e área integrada, preserves_null_pairing, região/fator, estado dinâmico, calor e H3 seguem INPUT/OPEN. |
| Gravitação quântica geral | NÃO PAGO | Reconstrução condicional; assinatura, dimensão, escala e globalização permanecem abertas. |

6 módulos novos; 45 teoremas; 4 definições com axiomas separadamente impressos. Contagens lidas dos fontes. As dependências finais estão contidas no trio permitido; sem sorryAx, erros ou avisos.

## Reprodução

```powershell
& 'C:\Python314\python.exe' -B 'C:\IALD\Central de Patentes\Chatgpt\audit_continuation012.py'
& 'C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1' -Module ScreenAreaCalculus
if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }
& 'C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1' -Module NullScreenAlgebra
if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }
& 'C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1' -Module GeometricScreenTransport
if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }
& 'C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1' -Module GeometricAreaHorizon
if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }
& 'C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1' -Module ScreenEntropyObstruction
if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }
& 'C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1' -Module GeometricScreenControls
if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }
```

O manifesto fixa fontes, cópias binárias locais e logs. O ambiente externo Lean/mathlib é local. Conferência de hashes não substitui recompilação independente.

## Axiomas impressos

```text
ChatgptAudit.matrix_curve_deriv_transpose: [propext, Classical.choice, Quot.sound]
ChatgptAudit.matrix_curve_deriv_mul: [propext, Classical.choice, Quot.sound]
ChatgptAudit.screen_gram_derivative: [propext, Classical.choice, Quot.sound]
ChatgptAudit.determinant_curve_derivative: [propext, Classical.choice, Quot.sound]
ChatgptAudit.determinant_congruence_tangent: [propext, Classical.choice, Quot.sound]
ChatgptAudit.screen_area_positive: [propext, Classical.choice, Quot.sound]
ChatgptAudit.screen_area_squared: [propext, Classical.choice, Quot.sound]
ChatgptAudit.screen_area_derivative: [propext, Classical.choice, Quot.sound]
ChatgptAudit.null_gram_screen_block: [propext, Classical.choice, Quot.sound]
ChatgptAudit.screen_gram_in_frame: [propext, Classical.choice, Quot.sound]
ChatgptAudit.null_screen_variation_block: [propext, Classical.choice, Quot.sound]
ChatgptAudit.null_frame_trace: [propext, Classical.choice, Quot.sound]
ChatgptAudit.null_frame_first_diagonal: [propext, Classical.choice, Quot.sound]
ChatgptAudit.null_frame_metric_product: [propext, Classical.choice, Quot.sound]
ChatgptAudit.null_frame_second_diagonal: [propext, Classical.choice, Quot.sound]
ChatgptAudit.ambient_expansion_is_screen_trace: [propext, Classical.choice, Quot.sound]
ChatgptAudit.frame_metric_variation: [propext, Classical.choice, Quot.sound]
ChatgptAudit.screen_metric_variation: [propext, Classical.choice, Quot.sound]
ChatgptAudit.connection_metric_sum: [propext, Classical.choice, Quot.sound]
ChatgptAudit.metric_along_curve_derivative: [propext, Classical.choice, Quot.sound]
ChatgptAudit.lie_screen_gram_derivative: [propext, Classical.choice, Quot.sound]
ChatgptAudit.geometric_screen_area_derivative: [propext, Classical.choice, Quot.sound]
ChatgptAudit.coordinate_screen_area_derivative: [propext, Classical.choice, Quot.sound]
ChatgptAudit.null_screen_geodesic_column: [propext, Classical.choice, Quot.sound]
ChatgptAudit.induced_area_continuous: [propext, Classical.choice, Quot.sound]
ChatgptAudit.geometric_pencil_area_continuous: [propext, Classical.choice, Quot.sound]
ChatgptAudit.geometric_pencil_area_rate: [propext, Classical.choice, Quot.sound]
ChatgptAudit.geometricHorizonToLocal: [propext, Classical.choice, Quot.sound]
ChatgptAudit.geometric_area_einstein_reconstruction: [propext, Classical.choice, Quot.sound]
ChatgptAudit.equal_past_entropy_area_derivatives: [propext, Classical.choice, Quot.sound]
ChatgptAudit.constant_entropy_forces_zero_area_rate: [propext, Classical.choice, Quot.sound]
ChatgptAudit.constant_entropy_forces_zero_expansion: [propext, Classical.choice, Quot.sound]
ChatgptAudit.fixed_tower_entropy_forces_zero_expansion: [propext, Classical.choice, Quot.sound]
ChatgptAudit.finite_entropy_area_rate_constraint: [propext, Classical.choice, Quot.sound]
ChatgptAudit.geometric_expansion_excludes_frozen_tower_entropy: [propext, Classical.choice, Quot.sound]
ChatgptAudit.flat_null_inverse: [propext, Classical.choice, Quot.sound]
ChatgptAudit.flat_null_gram: [propext, Classical.choice, Quot.sound]
ChatgptAudit.flat_screen_metric: [propext, Classical.choice, Quot.sound]
ChatgptAudit.flat_screen_area: [propext, Classical.choice, Quot.sound]
ChatgptAudit.flat_induced_area: [propext, Classical.choice, Quot.sound]
ChatgptAudit.flatScreenWitness: [propext, Classical.choice, Quot.sound]
ChatgptAudit.flatGeometricScreen: [propext, Classical.choice, Quot.sound]
ChatgptAudit.flatGeometricHorizon: [propext, Classical.choice, Quot.sound]
ChatgptAudit.flat_geometric_nonzero_inhabitant: [propext, Classical.choice, Quot.sound]
ChatgptAudit.screen_area_signature_flip: [propext, Classical.choice, Quot.sound]
ChatgptAudit.screen_gram_rescale: [propext, Classical.choice, Quot.sound]
ChatgptAudit.stretched_screen_area: [propext, Classical.choice, Quot.sound]
ChatgptAudit.stretched_screen_area_rate: [propext, Classical.choice, Quot.sound]
ChatgptAudit.stretched_cut_refuses_fixed_entropy: [propext, Classical.choice, Quot.sound]
```

## Artefatos e hashes

Manifesto: `C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO012_MANIFESTO.json` — SHA256 `f2ff4a23108aead091afa50e29f7491eb6d843918f456bf948de0c27ac0a84d4`.
Inventário completo: 491 caminhos absolutos, tamanhos e hashes dos bytes.

| Artefato principal | SHA256 |
|---|---|
| `C:\IALD\Central de Patentes\Chatgpt\audit_continuation012.py` | `3bd43df784ea26086e244814f20a63b2f2c1feecc9f78abf3ba3703e64f55d4c` |
| `C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO012_DERIVACAO_PREVIA.md` | `a0c64c6d47846ad769ae07c7c3af6535bcc4a6db3ffa6169e7b95fa9a7d8f07b` |
| `C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO012_PARECER.md` | `6d174cf404fcc4d531cad693e1ef6c2f427a05ba65eb6865ed82746bd7fe427f` |
| `C:\IALD\Central de Patentes\Chatgpt\GeometricAreaHorizon.20260905_231143.log` | `af039272ef842ed6e1be3b84adbbbfa27f8f175a59fd1b39427a7912815cb2ee` |
| `C:\IALD\Central de Patentes\Chatgpt\GeometricAreaHorizon.lean` | `55896da482e944f3830135f96be980d09b13118d47be6f428f9161dbfcf1fdda` |
| `C:\IALD\Central de Patentes\Chatgpt\GeometricScreenControls.20260905_231354.log` | `1905fd031625691f69b9f62eee6db5d2cf114117961683943b9d050580f58c2f` |
| `C:\IALD\Central de Patentes\Chatgpt\GeometricScreenControls.lean` | `d88e36fbd0f33593c11c3c6454dce034dbf0dda28fd1192f23f89b166dcbc05f` |
| `C:\IALD\Central de Patentes\Chatgpt\GeometricScreenTransport.20260905_225539.log` | `03f0872efd42389178f0171a7809b0510d850b896c19f6216780a2d53d9b4a31` |
| `C:\IALD\Central de Patentes\Chatgpt\GeometricScreenTransport.lean` | `bd953d01fecf187e5cb6dbea952e3a43172e94be587ed8aa561c59f97daadce7` |
| `C:\IALD\Central de Patentes\Chatgpt\NullScreenAlgebra.20260905_225154.log` | `c5dcd89b5c2187aed567f62de9f26349de76cc0330faa45dcd546ffb6d959196` |
| `C:\IALD\Central de Patentes\Chatgpt\NullScreenAlgebra.lean` | `717a1b96f6ad984e85803b303b62e8570d8db3dc0ad23566265922265377c2cd` |
| `C:\IALD\Central de Patentes\Chatgpt\ScreenAreaCalculus.20260905_224840.log` | `575fec9f611b4cf3991d4fbdd49956b899535c78ecdb179bca803c9f48fef058` |
| `C:\IALD\Central de Patentes\Chatgpt\ScreenAreaCalculus.lean` | `cc3a99426a80d973e9ed4d896038299e5a4c9b0adfd1ad9dbf072ab982f2392c` |
| `C:\IALD\Central de Patentes\Chatgpt\ScreenEntropyObstruction.20260905_230456.log` | `a403200b594e72f59737bfc77c8d559049c3b19cdb3174fb7591cb57056e61fb` |
| `C:\IALD\Central de Patentes\Chatgpt\ScreenEntropyObstruction.lean` | `8874729941471d85c6aeea9e45574d4690a62f477a656a88506ceeb53dc2ab5f` |

## Tentativas preservadas

- `C:\IALD\Central de Patentes\Chatgpt\ScreenAreaCalculus.20260905_224647.failed_compile.log`: exit code 1; erro de elaboração ou aviso; cópia exata do log.
- `C:\IALD\Central de Patentes\Chatgpt\NullScreenAlgebra.20260905_224955.failed_compile.log`: exit code 1; erro de elaboração ou aviso; cópia exata do log.
- `C:\IALD\Central de Patentes\Chatgpt\GeometricScreenTransport.20260905_225343.failed_compile.log`: exit code 1; erro de elaboração ou aviso; cópia exata do log.
- `C:\IALD\Central de Patentes\Chatgpt\GeometricAreaHorizon.20260905_225849.failed_compile.log`: exit code 1; positive screen incompatible with canonical +--- convention; cópia exata do log.
- `C:\IALD\Central de Patentes\Chatgpt\GeometricAreaHorizon.20260905_230120.failed_compile.log`: exit code 1; positive screen incompatible with canonical +--- convention; cópia exata do log.
- `C:\IALD\Central de Patentes\Chatgpt\GeometricAreaHorizon.20260905_230311.failed_compile.log`: exit code 1; positive screen incompatible with canonical +--- convention; cópia exata do log.
- `C:\IALD\Central de Patentes\Chatgpt\GeometricAreaHorizon.20260905_230643.rejected_signature_condition.log`: exit code 0; positive screen incompatible with canonical +--- convention; cópia exata do log.
- `C:\IALD\Central de Patentes\Chatgpt\ScreenEntropyObstruction.20260905_230234.failed_compile.log`: exit code 1; erro de elaboração ou aviso; cópia exata do log.
- `C:\IALD\Central de Patentes\Chatgpt\GeometricScreenControls.20260905_230819.failed_compile.log`: exit code 1; erro de elaboração ou aviso; cópia exata do log.
- `C:\IALD\Central de Patentes\Chatgpt\GeometricScreenControls.20260905_231235.failed_compile.log`: exit code 1; erro de elaboração ou aviso; cópia exata do log.

A versão inicial que exigia Gram espacial positivo era incompatível com +---. Mesmo as compilações limpas dessa versão não são aceitas como evidência geométrica final. O auditor reconhece seus hashes a partir dos backups e arquiva os logs com o motivo de assinatura. A correção e o controle plano estão no parecer.

## Limites e integração

A é densidade de área associada às direções fornecidas. A imersão de uma superfície geral e a integral de área não foram construídas. O transporte e a condição preserves_null_pairing são dados explícitos; a geodesicidade produz Bk=0. O equilíbrio B=0 continua mais forte que equilíbrio apenas da tela.

A igualdade S=ηA, a escolha de η, o calor e o limite de Clausius não foram deduzidos do estado. Para perfil e andar fixos, a entropia é constante: a nova obstrução exige mudança do estado, corte, álgebra ou número efetivo de fatores para acompanhar expansão não nula.

O controle stretchedScreen tem A=(1+t)² e A′(0)=2; é uma família de paralelogramos parametrizados, não um segundo horizonte dinâmico completo. O habitante completo provado é o plano de área constante.

Fonte primária de referência: [Jacobson, 1995](https://arxiv.org/html/gr-qc/9504004), equações (3)–(6). A distinção entre identidade geométrica e premissa termodinâmica foi preservada.

Escritas somente em Chatgpt. Nenhum um.py executado, importado ou editado; nenhuma edição no kernel canônico, Atlas, memórias, selos ou gate. Nenhum dado observacional. A gerência recompila, audita e decide incorporação. O objetivo amplo permanece ativo e aberto.
