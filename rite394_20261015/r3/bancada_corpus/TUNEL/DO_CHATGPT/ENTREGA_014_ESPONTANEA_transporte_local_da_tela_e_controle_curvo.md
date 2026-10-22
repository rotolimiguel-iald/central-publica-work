[REAL / INPUT / OPEN] ENTREGA 014 ESPONTÂNEA — construção local da tela transportada e controle curvo.

06/09/2026. Continuação de 013. Ordens gerenciais 001–007 presentes no túnel; auditoria independente pendente. Nenhuma alteração de gate.

## Critérios e alcance

| Critério | Estado | Evidência |
|---|---|---|
| Derivação anterior ao código | PAGO | CONTINUACAO014_DERIVACAO_PREVIA.md e adendo do controle curvo anterior à sua implementação. |
| Integração 012/013 | PAGO nas cópias | Três cópias mecânicas com namespace Screen013; previous_and_constructed_frames_coexist e compilação conjunta do módulo final. |
| Existência local de curva e matriz transportada | PAGO | localFrameFlow aplica a existência de ODE da mathlib ao campo (V,KF), após provar C¹. |
| Preservação de g(V,W) e g(V,S) | PAGO | Derivadas efetivas e constância no intervalo aberto da solução. |
| Certificado nulo com tela variável | PAGO | completedNullScreen corrige somente o vetor auxiliar; mantém S e prova o Gram e a inversa. |
| Habitante de GeometricScreenAlong | PAGO sob INPUT | local_levi_civita_transported_screen constrói curva e tela a partir de solda e campo nulo geodésico suave. |
| Lei de área | PAGO | A=sqrt(det(SᵀgS)); A′=θA perto de zero pelo lado passado; derivada efetiva também em zero. |
| Controles | PAGO | Tela plana constante; controle curvo com A(0)=1, A′(0)=2, área não localmente constante e componente de curvatura igual a 1. |
| Campo nulo geodésico e horizonte geral | NÃO PAGO | O campo é recebido; não se constrói horizonte imerso, família transversal ou equilíbrio geral. |
| Entropia microscópica e gravitação quântica geral | NÃO PAGO | Vínculo entropia-área, coeficiente físico, calor, H3, ponte modular e globalização permanecem abertos. |

9 módulos; 62 teoremas; 11 definições com axiomas separadamente impressos.
Separação da contagem: 14 teoremas e 6 definições copiados de 013; 1 teorema de integração; 47 teoremas e 5 definições da nova construção e seus controles.
As contagens vêm dos fontes. Dependências finais restritas a propext, Classical.choice e Quot.sound; sem erros, avisos ou sorryAx.

## Reprodução

```powershell
& 'C:\Python314\python.exe' -B 'C:\IALD\Central de Patentes\Chatgpt\audit_continuation014.py'
```

O comando acima só lê e confere a custódia. A gerência deve recompilar em sua cópia independente; os comandos abaixo recompilam os módulos novos no caminho local atual e escrevem os respectivos binários/logs:

```powershell
& 'C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1' -Module Screen013NullFrame
if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }
& 'C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1' -Module Screen013Constructed
if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }
& 'C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1' -Module Screen013Controls
if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }
& 'C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1' -Module ScreenImportIntegration
if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }
& 'C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1' -Module ScreenTransportODE
if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }
& 'C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1' -Module ScreenPairTransport
if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }
& 'C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1' -Module ScreenFrameCompletion
if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }
& 'C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1' -Module TransportedScreenExistence
if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }
& 'C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1' -Module TransportedScreenControls
if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }
```

O último módulo importa conjuntamente toda a árvore nova e os controles anteriores. A ordem completa das fontes locais está em bench_source_build_order no manifesto. As fontes/binários locais estão fixados; Lean 4.31.0/mathlib são dependências externas. A bancada não alega uma recompilação independente da cadeia nem um pacote portátil.

## Axiomas impressos

```text
ChatgptAudit.Screen013.minkowski_pair_lift: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen013.null_frame_matrix_gram: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen013.normalized_null_gram_squared: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen013.flatNullFrame: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen013.invertible_solder_nonzero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen013.solderedNullFrame: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen013.normalized_frame_screen_gram: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen013.negative_identity_screen_area: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen013.assembleNormalizedScreen: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen013.solderedScreenAtPoint: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen013.leviCivitaScreenAtPoint: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen013.normalized_screen_at_point_area: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen013.levi_civita_null_screen_exists: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen013.zero_direction_has_no_null_screen: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen013.off_axis_vector_nonzero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen013.off_axis_vector_null: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen013.offAxisNullFrame: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen013.off_axis_frame_verified: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen013.normalized_family_area_constant: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen013.normalized_family_expansion_obstruction: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.previous_and_constructed_frames_coexist: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.transport_generator_smooth: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.coupled_frame_field_c1: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.eventually_symmetric_interval: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.matrix_derivative_components: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.localFrameFlow: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.local_frame_flow_continuous_zero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.ordinary_velocity_generator: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.velocity_along_flow_derivative: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.vector_column_pair: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.pair_curve_derivative: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.generator_pair_cancellation: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.frame_column_transport: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.transported_null_pair_derivative: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.frame_flow_pair_preserved: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.raw_gram_shape: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.completion_coefficients_solve: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.completed_gram_coefficients: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.completed_gram: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.completion_first_column: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.completion_keeps_screen: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.null_screen_gram_determinant: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.frame_det_nonzero_from_null_gram: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.completedNullScreen: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.velocity_frame_first: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.velocity_frame_screen: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.screen_gram_symmetric: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.screen_gram_continuous_components: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.normalized_initial_pair: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.flow_raw_gram_row: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.flowScreenCertificate: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.flow_screen_positive_near_zero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.geometricScreenFromFlow: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.flow_screen_area_derivative_zero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.geometric_screen_area_rate: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.local_levi_civita_transported_screen: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.zero_generator_frames_constant: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.flat_frame_flow_control: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.expanding_factor_partial: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.expanding_velocity_partial: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.expanding_velocity_gradient: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.expanding_velocity_null: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.expanding_velocity_geodesic: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.expanding_velocity_expansion: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.expanding_velocity_smooth: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.expanding_metric_smooth: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.expanding_connection_smooth: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.expanding_metric_symmetric: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.expanding_metric_inverse: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.expanding_connection_compatible: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.expandingInitialFrame: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.expanding_screen_nonconstant: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen014.expanding_background_curvature: [propext, Classical.choice, Quot.sound]
```

## Artefatos e hashes

Manifesto: `C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO014_MANIFESTO.json` — SHA256 `c1cb1efbded34c56cb1b6db3b2cae8bb4a1ba9d3d66ec0295fb165cd0b52ab32`.
Inventário: 527 caminhos absolutos com tamanho e hash dos bytes.

| Artefato principal | SHA256 |
|---|---|
| `C:\IALD\Central de Patentes\Chatgpt\audit_continuation014.py` | `62aaee27759343ebbd003d6be799030eb797e0a24b347cc2597461cf82f865c1` |
| `C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO014_DERIVACAO_PREVIA.md` | `c5bac79c9c4ce9d5d31bb4e5823f167b58da464bd62eac41cf9ec316283600e9` |
| `C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO014_PARECER.md` | `7f6f545dbb357d89c6a8c864a1b4831368afbad7f688eb76636995d43c12e1ca` |
| `C:\IALD\Central de Patentes\Chatgpt\Screen013Constructed.20260905_235700.log` | `c7b1457c8f1d9583e7d5bf04609f1a99e10556943f45e608d6e8500770c8325f` |
| `C:\IALD\Central de Patentes\Chatgpt\Screen013Constructed.lean` | `77c7dac822ef58ce0b84742f4f64db5ef117e374d6560d687aa2e75350e13375` |
| `C:\IALD\Central de Patentes\Chatgpt\Screen013Controls.20260905_235914.log` | `9739b2eba0b25f7930f60f65544110175dfc0a03434aa5803734213d651a619a` |
| `C:\IALD\Central de Patentes\Chatgpt\Screen013Controls.lean` | `af3bfec185fa96388345c829d2672c7f4f825a329934f8f7a570d2c7c7e4ba9e` |
| `C:\IALD\Central de Patentes\Chatgpt\Screen013NullFrame.20260905_235602.log` | `d5e65ae677a86a1940e7ea8361b878edfb180e031f6ddb0536a2aab56270215a` |
| `C:\IALD\Central de Patentes\Chatgpt\Screen013NullFrame.lean` | `5a8d55856e3722c652379424ec3bc07d1f611da18e8b356884c058e8ab40672c` |
| `C:\IALD\Central de Patentes\Chatgpt\ScreenFrameCompletion.20260906_001701.log` | `4e6385de6fa71591eb6f3ba78fe24f16b73ed9cad25b347c0f2d363c82b77233` |
| `C:\IALD\Central de Patentes\Chatgpt\ScreenFrameCompletion.lean` | `aaf36a0a2b811af99a7ef40a63c5ac4bcf7173445a5a49b8820e8e04832a89bb` |
| `C:\IALD\Central de Patentes\Chatgpt\ScreenImportIntegration.20260906_000124.log` | `88bf23cd7750dc84dfbfdaacf7ebf9c7d51bc9284212c612b811c803627de27f` |
| `C:\IALD\Central de Patentes\Chatgpt\ScreenImportIntegration.lean` | `dfc1607a005713be14aa498d009668a4b1a14df134edcf08d0f39c9e0527d981` |
| `C:\IALD\Central de Patentes\Chatgpt\ScreenPairTransport.20260906_000604.log` | `8e11afc58739bdd4739a8dac21d163e6598ab199bd8159c384e7bafb189c6f71` |
| `C:\IALD\Central de Patentes\Chatgpt\ScreenPairTransport.lean` | `68d9107f2b56db708f55f4bf5ba379f7053a2582d95ac53326dbcc8c4b9d489c` |
| `C:\IALD\Central de Patentes\Chatgpt\ScreenTransportODE.20260906_000424.log` | `0bb2e2161e7b0b61ef4920bdb46e11bf129c98cde171237fbcc465f3512a612c` |
| `C:\IALD\Central de Patentes\Chatgpt\ScreenTransportODE.lean` | `78a29b3cc6c00a61a27d0a1b62d1f2cb33a111035d495b23da0da607e44f73a5` |
| `C:\IALD\Central de Patentes\Chatgpt\TransportedScreenControls.20260906_003002.log` | `81d57db36ccf551a51efe069e100728749255730ae85af9547e97c1937ef98c5` |
| `C:\IALD\Central de Patentes\Chatgpt\TransportedScreenControls.lean` | `ce170d05ed9e5c7b27843f7630afe10659b0070c16ecd6f8b331b5aa5e7d8cdb` |
| `C:\IALD\Central de Patentes\Chatgpt\TransportedScreenExistence.20260906_002245.log` | `f351bb4b8ee2a4534c7543f11e572b12eb2a8ab0b1087c39303acfa31a397513` |
| `C:\IALD\Central de Patentes\Chatgpt\TransportedScreenExistence.lean` | `dcbccb0742052fc70e4017d921e4fd48561ab066fa469ff86d942ec549916c15` |

## Cópias corrigidas de 013

| Original | Cópia | SHA256 original | SHA256 cópia |
|---|---|---|---|
| `C:\IALD\Central de Patentes\Chatgpt\NullFrameConstruction.lean` | `C:\IALD\Central de Patentes\Chatgpt\Screen013NullFrame.lean` | `07cfa22cc187b3bb236797fd4542e4ca09f45c8cbbe29ea20e5b6788aa4c7fc9` | `5a8d55856e3722c652379424ec3bc07d1f611da18e8b356884c058e8ab40672c` |
| `C:\IALD\Central de Patentes\Chatgpt\ConstructedScreenAtPoint.lean` | `C:\IALD\Central de Patentes\Chatgpt\Screen013Constructed.lean` | `1c9f184f1a22b2739d234a39ce1c92a81ccbe74bd1853f0dc95209898a456143` | `77c7dac822ef58ce0b84742f4f64db5ef117e374d6560d687aa2e75350e13375` |
| `C:\IALD\Central de Patentes\Chatgpt\NullScreenConstructionControls.lean` | `C:\IALD\Central de Patentes\Chatgpt\Screen013Controls.lean` | `e2ff51d93084bcdc739b467ddba8a97428de2ab3ce6b773ca9d80cd841f66391` | `af3bfec185fa96388345c829d2672c7f4f825a329934f8f7a570d2c7c7e4ba9e` |

O auditor verifica que somente namespace/end namespace e nomes de imports locais foram substituídos. A colisão de nomes flatNullFrame foi identificada pela leitura dos dois fontes originais; não foi rodada uma sonda conjunta desses originais. A compilação conjunta das cópias corrigidas foi executada e passou.

## Tentativas preservadas

- `C:\IALD\Central de Patentes\Chatgpt\ScreenTransportODE.20260905_235852.failed_compile.log`: exit code 1; erro de elaboração ou aviso; cópia exata do log.
- `C:\IALD\Central de Patentes\Chatgpt\ScreenTransportODE.20260906_000014.failed_compile.log`: exit code 1; erro de elaboração ou aviso; cópia exata do log.
- `C:\IALD\Central de Patentes\Chatgpt\ScreenTransportODE.20260906_000207.failed_compile.log`: exit code 1; erro de elaboração ou aviso; cópia exata do log.
- `C:\IALD\Central de Patentes\Chatgpt\ScreenFrameCompletion.20260906_000747.failed_compile.log`: exit code 1; erro de elaboração ou aviso; cópia exata do log.
- `C:\IALD\Central de Patentes\Chatgpt\ScreenFrameCompletion.20260906_001236.failed_compile.log`: exit code 1; erro de elaboração ou aviso; cópia exata do log.
- `C:\IALD\Central de Patentes\Chatgpt\ScreenFrameCompletion.20260906_001422.failed_compile.log`: exit code 1; erro de elaboração ou aviso; cópia exata do log.
- `C:\IALD\Central de Patentes\Chatgpt\TransportedScreenExistence.20260906_001817.failed_compile.log`: exit code 1; erro de elaboração ou aviso; cópia exata do log.
- `C:\IALD\Central de Patentes\Chatgpt\TransportedScreenExistence.20260906_001949.failed_compile.log`: exit code 1; erro de elaboração ou aviso; cópia exata do log.
- `C:\IALD\Central de Patentes\Chatgpt\TransportedScreenControls.20260906_002405.failed_compile.log`: exit code 1; erro de elaboração ou aviso; cópia exata do log.
- `C:\IALD\Central de Patentes\Chatgpt\TransportedScreenControls.20260906_002921.rejected_warning.log`: exit code 0; erro de elaboração ou aviso; cópia exata do log.

Revisões conservam backups dos bytes. Falhas de elaboração de ODE, filtros, diferenciação, expansão matricial, denominadores e avisos de táticas redundantes foram corrigidos sem apagar os registros. A custódia das entregas anteriores permanece imutável.

## Limites e encaminhamento

A construção recebe V suave, nulo e geodésico numa vizinhança, V(x)≠0, e uma solda suave invertível. Produz uma curva e uma tela ao longo dela, não uma superfície imersa ou um horizonte geral. O contrato GeometricScreenAlong é local no parâmetro passado de zero.

O controle curvo tem expansão inicial 2; portanto não satisfaz B(0)=0. Ele não é uma construção completa do horizonte de equilíbrio ou de Clausius. A(0)=1 é normalização da base, não uma unidade física deduzida.

Entropia-área microscópica, calor/H3, coeficiente físico, seleção de assinatura/dimensão, ponte modular e globalização permanecem OPEN. Não há prova ou confirmação de gravidade quântica geral.

Escritas exclusivamente em Chatgpt. Nenhum um.py executado, importado ou editado; kernel canônico, Atlas, memórias, selos e gate intocados. Sem dados observacionais. Parecer detalhado: C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO014_PARECER.md. A gerência audita independentemente antes de incorporar.
