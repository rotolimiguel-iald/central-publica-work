[REAL / INPUT / OPEN] ENTREGA 010 ESPONTÂNEA — Raychaudhuri e balanço local de Clausius ligados à reconstrução com o tensor de Einstein geométrico.

Continuação de 009, 05/09/2026. Nenhuma ordem 010 da gerência estava no túnel ao publicar. Pronta para auditoria independente; não altera gate nem conclui gravitação quântica.

## Critérios e alcance

| Critério | Estado | Evidência |
|---|---|---|
| Derivação antes do código | PAGO | Derivação geral e adendo prévio ao habitante plano; controle curvo reutiliza o cálculo prévio de 009. |
| Derivadas vetoriais e curvatura | PAGO | Derivadas de Fréchet; comutador covariante igual à curvatura efetiva. |
| Identidade de Raychaudhuri | PAGO | D_Vθ = div a − tr(B²) − Ric(V,V), para campos suaves e conexão sem torção na carta. |
| Focalização de equilíbrio | PAGO como implicação | Campo geodésico em vizinhança e B=0 no ponto; derivada transportada para curva tangente. |
| Balanço analítico local | PAGO como implicação | Resíduo integrado F/λ²→0 no ramo passado, leis de área e calor, continuidade e fatores não nulos forçam o balanço nulo de Ricci. |
| Reconstrução geométrica | PAGO como implicação | horizon_einstein_reconstruction: testemunhos para todas as direções nulas e T conservado dão G_geom+Λg=(2π/η)T, Λ constante. |
| Contrato não vazio | PAGO no controle plano | flatHorizonPencil e flat_nonzero_pencil_exists: direção nula (1,1,0,0), não zero, Γ=0, T=0, A=1, Q=0. |
| Controle curvo incompatível | PAGO | Ric(v,v)=2 em x=0; com T=0 e η≠0 não existe o testemunho exigido. |
| KMS e vinculação física | NEGATIVO DELIMITADO | KMS canônico coexiste com o par independente incompatível; não implica o balanço para geometria e matéria arbitrárias. |
| Testemunhos físicos gerais e área de tela | NÃO PAGO | Existência geral, interpretação geométrica de A, entropia-área e calor oriundos do estado continuam INPUT/OPEN. |
| H3 dinâmico, assinatura, quatro dimensões e globalização | NÃO PAGO | Permanecem obrigações do objetivo amplo. |

6 módulos novos; 42 teoremas e 1 definição com axiomas impressos. Contagens lidas dos fontes. Logs finais limpos, sem sorryAx; somente o trio permitido.

## Reprodução

```powershell
& 'C:\Python314\python.exe' -B 'C:\IALD\Central de Patentes\Chatgpt\audit_continuation010.py'
& 'C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1' -Module CovariantVectorCalculus
if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }
& 'C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1' -Module VectorCurvatureCommutator
if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }
& 'C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1' -Module CoordinateRaychaudhuri
if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }
& 'C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1' -Module LocalHorizonBalance
if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }
& 'C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1' -Module HorizonEinsteinReconstruction
if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }
& 'C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1' -Module HorizonBalanceControls
if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }
```

A ordem de fontes e as dependências locais estão no manifesto. O ambiente externo Lean/mathlib é local. A conferência de hashes não substitui recompilação independente.

## Axiomas impressos

```text
ChatgptAudit.smooth_vector_differentiableAt: [propext, Classical.choice, Quot.sound]
ChatgptAudit.vectorPartial_smooth: [propext, Classical.choice, Quot.sound]
ChatgptAudit.vectorPartial_add: [propext, Classical.choice, Quot.sound]
ChatgptAudit.vectorPartial_mulVec: [propext, Classical.choice, Quot.sound]
ChatgptAudit.matrix_mulVec_smooth: [propext, Classical.choice, Quot.sound]
ChatgptAudit.covariantVectorDerivative_smooth: [propext, Classical.choice, Quot.sound]
ChatgptAudit.covariantVectorGradient_smooth: [propext, Classical.choice, Quot.sound]
ChatgptAudit.vectorPartial_commute: [propext, Classical.choice, Quot.sound]
ChatgptAudit.scalarAlong_eq_fderiv: [propext, Classical.choice, Quot.sound]
ChatgptAudit.vectorPartial_congr_on: [propext, Classical.choice, Quot.sound]
ChatgptAudit.covariant_vector_commutator: [propext, Classical.choice, Quot.sound]
ChatgptAudit.mixed_gradient_component: [propext, Classical.choice, Quot.sound]
ChatgptAudit.mixed_gradient_commutator: [propext, Classical.choice, Quot.sound]
ChatgptAudit.covariant_vector_matrix_product: [propext, Classical.choice, Quot.sound]
ChatgptAudit.mixed_covariant_trace: [propext, Classical.choice, Quot.sound]
ChatgptAudit.sum_three_reverse: [propext, Classical.choice, Quot.sound]
ChatgptAudit.curvature_vector_contraction: [propext, Classical.choice, Quot.sound]
ChatgptAudit.expansion_of_acceleration: [propext, Classical.choice, Quot.sound]
ChatgptAudit.along_expansion_eq_mixed_trace: [propext, Classical.choice, Quot.sound]
ChatgptAudit.coordinate_raychaudhuri: [propext, Classical.choice, Quot.sound]
ChatgptAudit.vector_expansion_zero_on: [propext, Classical.choice, Quot.sound]
ChatgptAudit.equilibrium_ricci_focusing: [propext, Classical.choice, Quot.sound]
ChatgptAudit.horizon_primitive_flux: [propext, Classical.choice, Quot.sound]
ChatgptAudit.horizon_primitive_zero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.heat_area_clausius_implies_local: [propext, Classical.choice, Quot.sound]
ChatgptAudit.curve_expansion_focusing: [propext, Classical.choice, Quot.sound]
ChatgptAudit.horizon_flux_residual_limit: [propext, Classical.choice, Quot.sound]
ChatgptAudit.local_clausius_forces_ricci: [propext, Classical.choice, Quot.sound]
ChatgptAudit.primitive_quadratic_limit: [propext, Classical.choice, Quot.sound]
ChatgptAudit.integrated_clausius_implies_local: [propext, Classical.choice, Quot.sound]
ChatgptAudit.tensor_quad_field_continuous: [propext, Classical.choice, Quot.sound]
ChatgptAudit.pencil_ricci_balance: [propext, Classical.choice, Quot.sound]
ChatgptAudit.horizon_einstein_reconstruction: [propext, Classical.choice, Quot.sound]
ChatgptAudit.entropy_density_einstein_coefficient: [propext, Classical.choice, Quot.sound]
ChatgptAudit.flat_constant_gradient: [propext, Classical.choice, Quot.sound]
ChatgptAudit.flat_constant_expansion: [propext, Classical.choice, Quot.sound]
ChatgptAudit.flatHorizonPencil: [propext, Classical.choice, Quot.sound]
ChatgptAudit.flat_nonzero_pencil_exists: [propext, Classical.choice, Quot.sound]
ChatgptAudit.balanced_flux_control: [propext, Classical.choice, Quot.sound]
ChatgptAudit.balanced_local_control: [propext, Classical.choice, Quot.sound]
ChatgptAudit.curved_control_direction_null: [propext, Classical.choice, Quot.sound]
ChatgptAudit.curved_control_no_vacuum_pencil: [propext, Classical.choice, Quot.sound]
ChatgptAudit.kms_with_incompatible_geometric_data: [propext, Classical.choice, Quot.sound]
```

## Artefatos e hashes

Manifesto: `C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO010_MANIFESTO.json` — SHA256 `f3a746b597191754dc4810bcba241e526028a0ec69da77c5f0ec6eb6afd78f9b`.
Inventário completo: 394 caminhos absolutos, tamanhos e hashes dos bytes.

| Artefato principal | SHA256 |
|---|---|
| `C:\IALD\Central de Patentes\Chatgpt\audit_continuation010.py` | `a9acfb945973e83c01724827bf8d52ebb113710f01d4cf3ea38b2a38f7d8595f` |
| `C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO010_DERIVACAO_PREVIA.md` | `b8f9a8ddbb8e95c263286f61e6a759bdcc20befdcc8ab865a74b56835dc395ab` |
| `C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO010_PARECER.md` | `1c64bbbad6386a6d113ce2b47a61e9c9454ac9d3a4265254a42b4878bd407272` |
| `C:\IALD\Central de Patentes\Chatgpt\CoordinateRaychaudhuri.20260905_215005.log` | `8d1ac22265a0ab694844c5fda42679acc0bed2305aceb033446a5bedff5216ce` |
| `C:\IALD\Central de Patentes\Chatgpt\CoordinateRaychaudhuri.lean` | `1fae0f275b2ca9b09f9806a0ed2fb80ef4ec0e674b75d2b142903f41b7da15e2` |
| `C:\IALD\Central de Patentes\Chatgpt\CovariantVectorCalculus.20260905_214418.log` | `38bd74e35243c6a56cde787e94f0d88df7c0f58e48b534eb48b5cdefb448f7de` |
| `C:\IALD\Central de Patentes\Chatgpt\CovariantVectorCalculus.lean` | `bb674cbd4d4ec704905000d89b8b4034f84f57a3822a5fcd49fbfe33df4da327` |
| `C:\IALD\Central de Patentes\Chatgpt\HorizonBalanceControls.20260905_220659.log` | `f1b6ee8596c249108238f2fb974293227c6413ef0517aa650852c2573484e656` |
| `C:\IALD\Central de Patentes\Chatgpt\HorizonBalanceControls.lean` | `39059f4b059af860e51d0e7712b9f044a1c0745c73a55da8ab8c3961f7c00fce` |
| `C:\IALD\Central de Patentes\Chatgpt\HorizonEinsteinReconstruction.20260905_220027.log` | `9622aad8dc788445c05448fc4b73123e643dd3762dc53c2899d605dbdd24d8f5` |
| `C:\IALD\Central de Patentes\Chatgpt\HorizonEinsteinReconstruction.lean` | `17071f1c61ffb2a897f06669358579c306940f3b3d2c1a332d53ab8e2778283c` |
| `C:\IALD\Central de Patentes\Chatgpt\LocalHorizonBalance.20260905_215846.log` | `00f8b2f15634c46e4d192631852185c81858ceee88a4d9eefda91c50b90918e4` |
| `C:\IALD\Central de Patentes\Chatgpt\LocalHorizonBalance.lean` | `308a63b959f18c80194b659feba3e2a0ff83be49020c17ca4c168ef72b8d0fca` |
| `C:\IALD\Central de Patentes\Chatgpt\VectorCurvatureCommutator.20260905_214706.log` | `df6f136ba29f54776701de894ad18fca2ca0ff0467455c1fcd5f960b41f1321b` |
| `C:\IALD\Central de Patentes\Chatgpt\VectorCurvatureCommutator.lean` | `fd44aec8cad4c8d3fa19ed4dc04e76ca3ea078d8f568ff0f5381a5b7bb9e94ae` |

## Tentativas preservadas

- `C:\IALD\Central de Patentes\Chatgpt\VectorCurvatureCommutator.20260905_214606.failed_compile.log`: cópia dos bytes do log; exit code 1; problemas e metadados no manifesto.
- `C:\IALD\Central de Patentes\Chatgpt\CoordinateRaychaudhuri.20260905_214848.failed_compile.log`: cópia dos bytes do log; exit code 1; problemas e metadados no manifesto.
- `C:\IALD\Central de Patentes\Chatgpt\LocalHorizonBalance.20260905_215243.failed_compile.log`: cópia dos bytes do log; exit code 1; problemas e metadados no manifesto.
- `C:\IALD\Central de Patentes\Chatgpt\LocalHorizonBalance.20260905_215433.failed_compile.log`: cópia dos bytes do log; exit code 1; problemas e metadados no manifesto.
- `C:\IALD\Central de Patentes\Chatgpt\LocalHorizonBalance.20260905_215802.failed_compile.log`: cópia dos bytes do log; exit code 1; problemas e metadados no manifesto.
- `C:\IALD\Central de Patentes\Chatgpt\HorizonBalanceControls.20260905_220438.failed_compile.log`: cópia dos bytes do log; exit code 1; problemas e metadados no manifesto.

Tentativas com erros de representação funcional, inferência ou avisos não contam como compilação final. Fontes intermediários e os bytes dos logs foram preservados.

## Limites e integração

O equilíbrio B=0 usado no ponto é mais forte que expansão e cisalhamento de tela nulos. A curva é especificada pelo ponto e pela tangente necessários ao limite; não se construiu o fluxo geodésico completo. A lei A'=θA é entrada, e a identificação de A com área de tela ainda não está provada. O contrato não contém a igualdade de Ricci e matéria como campo: essa igualdade é deduzida. Sua existência física geral continua aberta.

A fonte primária de referência foi [Jacobson, 1995](https://arxiv.org/html/gr-qc/9504004); as hipóteses termodinâmicas da referência não foram promovidas a consequência de KMS.

Escritas somente em Chatgpt. Nenhum um.py executado, importado ou editado; kernel canônico, Atlas, memórias, selos e gate intocados. Nenhum dado observacional. A gerência recompila, audita e decide incorporação. O objetivo amplo permanece ativo e aberto.
