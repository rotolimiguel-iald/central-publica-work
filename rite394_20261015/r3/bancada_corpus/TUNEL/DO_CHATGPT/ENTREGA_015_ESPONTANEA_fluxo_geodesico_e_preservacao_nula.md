[REAL / INPUT / OPEN] ENTREGA 015 ESPONTÂNEA — fluxo geodésico local e preservação da nulidade.

06/09/2026. Continuação de 014. Ordens gerenciais 001–007 presentes no túnel; auditoria independente pendente. Nenhuma alteração de gate.

## Critérios e alcance

| Critério | Estado | Evidência |
|---|---|---|
| Derivação antes do código | PAGO | CONTINUACAO015_DERIVACAO_PREVIA.md. |
| Campo geodésico no espaço de fases | PAGO | geodesic_spray_smooth e geodesic_spray_c1; campo (v,−Γ(v,v)). |
| Existência para dados iniciais próximos | PAGO | localPhaseFlow e localGeodesicFlow; intervalo e bola comuns; continuidade conjunta. |
| Equação geodésica efetiva | PAGO | x′=v e v′=−Γ(v,v), expressas com HasDerivAt. |
| Preservação da nulidade | PAGO | geodesic_energy_derivative e geodesic_flow_energy_conserved; energia nula inicial continua nula. |
| Habitante sob solda geral | PAGO sob INPUT | local_levi_civita_null_geodesics recebe solda suave invertível e velocidade não nula; não recebe um campo V. |
| Suavidade no tempo | PAGO | geodesic_flow_smooth_time, posição e velocidade C∞ em todo o intervalo aberto. |
| Controles | PAGO | Caso plano afim; caso curvo nulo com aceleração inicial −2(1,1,0,0) e curvatura não nula. |
| Fluxo de fase versus campo espacial | PAGO, negativo preciso | phase_flow_cannot_assign_one_field: a família completa contém velocidades distintas na mesma posição. |
| Congruência suave no espaço-tempo | NÃO PAGO | Suavidade nos dados iniciais, escolha transversal, inversão local e primeiro jato de equilíbrio ainda faltam. |
| Reconstrução gravitacional geral | NÃO PAGO | H3, entropia-área microscópica, coeficiente físico, calor, ponte modular e globalização permanecem OPEN. |

5 módulos; 29 teoremas declarados e 3 definições com axiomas impressos separadamente. Contagens lidas dos fontes.
O teorema curved_flow_background_nonzero reutiliza a componente de curvatura já provada em 014; não é contado como uma nova descoberta de curvatura. As demais declarações e os detalhes estão no manifesto.
Todos os módulos finais têm compilação limpa da fonte fixada; os axiomas impressos ficam no trio propext, Classical.choice, Quot.sound, sem sorryAx.

## Reprodução

```powershell
& 'C:\Python314\python.exe' -B 'C:\IALD\Central de Patentes\Chatgpt\audit_continuation015.py'
```

O comando acima só lê. A gerência deve recompilar em sua cópia independente; os comandos a seguir indicam a ordem dos módulos novos e escrevem binários/logs no caminho especificado:

```powershell
& 'C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1' -Module GeodesicSpray
if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }
& 'C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1' -Module LocalGeodesicFlow
if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }
& 'C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1' -Module NullGeodesicConservation
if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }
& 'C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1' -Module GeodesicFlowRegularity
if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }
& 'C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1' -Module GeodesicFlowControls
if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }
```

GeodesicFlowControls importa toda a árvore nova e TransportedScreenControls da entrega 014. A ordem completa de fontes locais está no manifesto. Lean 4.31.0/mathlib são dependências externas; não se declara um pacote portátil ou uma recompilação independente da cadeia.

## Axiomas impressos

```text
ChatgptAudit.Screen015.phase_domain_open: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen015.geodesic_spray_smooth: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen015.geodesic_spray_c1: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen015.spray_position_component: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen015.spray_zero_velocity: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen015.geodesic_energy_algebra: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen015.eventually_phase_rectangle: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen015.localPhaseFlow: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen015.regular_phase_domain_open: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen015.localGeodesicFlow: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen015.geodesic_flow_position_derivative: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen015.geodesic_flow_velocity_derivative: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen015.geodesic_flow_regular: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen015.geodesic_energy_derivative: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen015.geodesic_flow_energy_conserved: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen015.geodesic_flow_null_preserved: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen015.leviCivitaGeodesicFlow: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen015.local_levi_civita_null_geodesics: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen015.geodesic_flow_smooth_Icc: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen015.geodesic_flow_smooth_time: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen015.geodesic_flow_position_smooth: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen015.geodesic_flow_velocity_smooth: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen015.phase_flow_jointly_continuous_at: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen015.phase_initial_data_obstruction: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen015.zero_connection_velocity_constant: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen015.zero_connection_position_affine: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen015.flat_geodesic_flow_control: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen015.phase_flow_cannot_assign_one_field: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen015.conformal_spray_acceleration_zero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen015.conformal_spray_acceleration_nonzero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen015.curved_null_geodesic_flow_control: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Screen015.curved_flow_background_nonzero: [propext, Classical.choice, Quot.sound]
```

## Artefatos e hashes

Manifesto: `C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO015_MANIFESTO.json` — SHA256 `fc0210cfb3d238649fa72e887459f1b3c0a32f5b8cc7e0578a3e255b180bfd50`.
Inventário: 518 caminhos absolutos com tamanho e hash dos bytes.

| Artefato principal | SHA256 |
|---|---|
| `C:\IALD\Central de Patentes\Chatgpt\audit_continuation015.py` | `d51814c1e8db03074a1bf17a77fe85664c9ef7b1d445381540d1a3d9deefe446` |
| `C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO015_DERIVACAO_PREVIA.md` | `711aa2de76208b2d5bd204476e419da6c308cd128612a93659fb066201172053` |
| `C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO015_PARECER.md` | `bcfbe623e9212c94124ba1522f2df80f8a5b2aa86d1177a145bcbdda115017de` |
| `C:\IALD\Central de Patentes\Chatgpt\GeodesicFlowControls.20260906_005722.log` | `db2afec404d7fdc7475b4068f44b25a579d20346df3fe91216783859f1a2d6df` |
| `C:\IALD\Central de Patentes\Chatgpt\GeodesicFlowControls.lean` | `008557723625fc95ebdcb54691c88af938b0029131db3255edc6ab91c7d68c54` |
| `C:\IALD\Central de Patentes\Chatgpt\GeodesicFlowRegularity.20260906_005032.log` | `7ecf685b0724833a91e5e34069206ee4d443b08c7e2cfb93e36ef677d88bbe32` |
| `C:\IALD\Central de Patentes\Chatgpt\GeodesicFlowRegularity.lean` | `1f7d818b57d153e86f446608488ea1298b10443844f900ea6fa19f8431235669` |
| `C:\IALD\Central de Patentes\Chatgpt\GeodesicSpray.20260906_004244.log` | `a7ba7634419dc902c0f4641c6b3a962a05cacbbcb1ee6e3f543c38d9fda2bf65` |
| `C:\IALD\Central de Patentes\Chatgpt\GeodesicSpray.lean` | `dcb1bc16bc792fa6edbb50ff89ec4b27d602dc93515ab5ac7d654361d26ac161` |
| `C:\IALD\Central de Patentes\Chatgpt\LocalGeodesicFlow.20260906_004541.log` | `16b08fbab6ad2f100e7bc51d24048063700430c7fab4f0acc2e63c4975e1593a` |
| `C:\IALD\Central de Patentes\Chatgpt\LocalGeodesicFlow.lean` | `3a703eefa6aefa039a0a96cfbd62df4f668c6ab5e85022b79a4691247a87078d` |
| `C:\IALD\Central de Patentes\Chatgpt\NullGeodesicConservation.20260906_004716.log` | `5d4ec3ae0431ce6ebfb395589e3d4345832be9de49b52ea6e97c2388b989dd52` |
| `C:\IALD\Central de Patentes\Chatgpt\NullGeodesicConservation.lean` | `1cf3d8461b94a4683749eacec386c51b99deacc98b28301ff527180e3af03bb2` |

## Tentativas preservadas

- `C:\IALD\Central de Patentes\Chatgpt\GeodesicSpray.20260906_004022.failed_compile.log`: exit code 1; erro de elaboração ou aviso; cópia exata do log.
- `C:\IALD\Central de Patentes\Chatgpt\GeodesicSpray.20260906_004108.failed_compile.log`: exit code 1; erro de elaboração ou aviso; cópia exata do log.
- `C:\IALD\Central de Patentes\Chatgpt\LocalGeodesicFlow.20260906_004311.failed_compile.log`: exit code 1; erro de elaboração ou aviso; cópia exata do log.
- `C:\IALD\Central de Patentes\Chatgpt\LocalGeodesicFlow.20260906_004458.failed_compile.log`: exit code 1; erro de elaboração ou aviso; cópia exata do log.
- `C:\IALD\Central de Patentes\Chatgpt\GeodesicFlowRegularity.20260906_004814.failed_compile.log`: exit code 1; erro de elaboração ou aviso; cópia exata do log.
- `C:\IALD\Central de Patentes\Chatgpt\GeodesicFlowControls.20260906_005123.failed_compile.log`: exit code 1; erro de elaboração ou aviso; cópia exata do log.
- `C:\IALD\Central de Patentes\Chatgpt\GeodesicFlowControls.20260906_005250.failed_compile.log`: exit code 1; erro de elaboração ou aviso; cópia exata do log.
- `C:\IALD\Central de Patentes\Chatgpt\GeodesicFlowControls.20260906_005416.failed_compile.log`: exit code 1; erro de elaboração ou aviso; cópia exata do log.

Revisões conservam backups dos bytes. Falhas de elaboração das somas matriciais, intervalos, tipos de derivação e avisos de argumentos redundantes foram corrigidos sem apagar os registros. A custódia anterior permanece imutável.

## Parede exata e encaminhamento

O resultado constrói geodésicas no espaço de fases e prova suavidade no tempo e continuidade conjunta. Não prova suavidade nos dados iniciais nem produz um campo suave V em uma região do espaço-tempo. O negativo sobre a família completa não proíbe congruências: mostra que é necessário selecionar os dados iniciais apropriados.

Para usar diretamente o construtor de tela de 014, ainda se precisa de uma seção transversal de dados iniciais, da regularidade conjunta suficiente e da inversa local da projeção para a posição; o equilíbrio demanda controle do primeiro jato. A construção de GeometricHorizonPencil, Clausius/H3 e a ligação microscópica entropia-área continuam abertas.

Fonte primária de contexto: [Jacobson, 1995](https://arxiv.org/html/gr-qc/9504004). O artigo usa horizontes locais de equilíbrio e assume a relação entropia-área e Clausius; não é uma prova das hipóteses microscópicas.

Escritas exclusivamente em Chatgpt. Nenhum um.py executado, importado ou editado; kernel canônico, Atlas, memórias, selos e gate intocados. Sem dados observacionais. Parecer: C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO015_PARECER.md. Auditoria independente pendente; o objetivo amplo continua ativo e OPEN.
