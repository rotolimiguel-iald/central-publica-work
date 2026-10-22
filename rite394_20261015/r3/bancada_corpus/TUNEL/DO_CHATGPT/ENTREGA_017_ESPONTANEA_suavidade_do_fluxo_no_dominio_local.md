[REAL / INPUT / OPEN] ENTREGA 017 ESPONTÂNEA — suavidade conjunta do fluxo no domínio local original.

06/09/2026. Continuação de 016. Auditoria independente pendente. Nenhuma alteração de gate.

## Critérios e alcance

| Critério | Estado | Evidência |
|---|---|---|
| Derivação anterior ao código | PAGO | CONTINUACAO017_DERIVACAO_PREVIA.md, preservada em backup antes do adendo posterior. |
| Unicidade entre escolhas | PAGO | flow_germ_eq_at_initial: igualdade perto do mesmo dado e do tempo zero, com centros e domínios possivelmente diferentes. |
| Todas as ordens finitas | PAGO | exists_finite_regular_flow, por indução no campo variacional; o diferencial efetivo vem de 016. |
| Uma única escolha de fluxo | PAGO | flow_finite_regular_at_initial e flow_smooth_at_initial; igualdade local transfere todas as ordens para a função recebida. |
| Propagação temporal | PAGO | flow_finite_regular_nearby_transfer e conexão do intervalo; a transição usa a ODE recomeçada. |
| C∞ no domínio fixo | PAGO | flow_smooth_on_domain: mesmo raio, mesma bola e mesmo intervalo do fluxo original. |
| Aplicação geodésica | PAGO sob INPUT | c1_geodesic_flow_smooth fortalece a própria escolha de 016; local_smooth_levi_civita_null_geodesics reúne suavidade e nulidade preservada sob solda suave invertível. |
| Controles | PAGO | Campo zero, fórmula plana polinomial independente e fluxo curvo suave com aceleração inicial não nula. |
| Campo nulo suave no espaço-tempo | NÃO PAGO | Falta selecionar dados transversais e construir a inversa local do mapa de posição; o fluxo atual vive no espaço de fases. |
| Reconstrução gravitacional geral | NÃO PAGO | Primeiro jato de equilíbrio, horizonte, H3, entropia-área microscópica, coeficiente físico, calor, ponte modular e globalização permanecem OPEN. |

6 módulos; 18 teoremas declarados; 1 definição com axiomas impressos separadamente. Contagens lidas dos fontes.
A prova chega a ContDiffOn ℝ ∞ no aberto original. Não infere um raio positivo de uma interseção de raios decrescentes. A contagem é de declarações e inclui aplicações de resultados anteriores; não é uma contagem de descobertas novas.
As compilações finais da fonte fixada não têm erros, avisos ou sorryAx. As dependências impressas ficam no trio propext, Classical.choice, Quot.sound.

## Reprodução

```powershell
& 'C:\Python314\python.exe' -B 'C:\IALD\Central de Patentes\Chatgpt\audit_continuation017.py'
```

O comando só lê e verifica custódia e evidências registradas. A recompilação independente da gerência deve preservar os artefatos entregues. Ordem dos módulos novos:
- FlowGermUniqueness.lean
- FlowRegularityInduction.lean
- FlowSmoothGerm.lean
- FlowTimePropagation.lean
- SmoothGeodesicFlow.lean
- SmoothFlowControls.lean

SmoothFlowControls importa toda a árvore 017 e a entrega 016. A ordem local completa está no manifesto. O wrapper verify_stage.ps1 e seus metadados documentam Lean 4.31.0/mathlib; não se declara um pacote portátil integral.

## Axiomas impressos

```text
ChatgptAudit.Flow017.flow_germ_eq_at_initial: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow017.projectedVariationalFlow: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow017.variational_projection_contDiffAt: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow017.variational_regular_flow_successor: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow017.exists_finite_regular_flow: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow017.flow_finite_regular_at_initial: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow017.flow_smooth_at_initial: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow017.flow_finite_regular_times_open: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow017.flow_finite_regular_on_domain: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow017.flow_smooth_on_domain: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow017.eventually_flow_time_box: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow017.flow_finite_regular_nearby_transfer: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow017.phase_flow_of_variational_smooth: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow017.c1_geodesic_flow_smooth: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow017.local_smooth_metric_null_geodesics: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow017.local_smooth_levi_civita_null_geodesics: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow017.zero_field_smooth_flow_control: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow017.flat_geodesic_smooth_control: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow017.curved_smooth_null_flow_control: [propext, Classical.choice, Quot.sound]
```

## Artefatos e hashes

Manifesto: `C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO017_MANIFESTO.json` — SHA256 `f4d43879abf8fd0b437a7f749ba8f0ffc2e3c4a2448a4feb93c645ae388e295b`.
Inventário: 536 caminhos absolutos com tamanho e hash dos bytes.

| Artefato principal | SHA256 |
|---|---|
| `C:\IALD\Central de Patentes\Chatgpt\audit_continuation017.py` | `17c032ceca9cf6bd14a0a02f2b41ef5e465d7617be67f55c618456ac4b06d6c0` |
| `C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO017_DERIVACAO_PREVIA.md` | `ceacd90b7e3821aae70b8657639a89836154aa82d56a82b224160d0bac1a06c0` |
| `C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO017_PARECER.md` | `3624746b051123424842151cf31f14cd29ec27bcebbdc4e67c249adfe58cc4e9` |
| `C:\IALD\Central de Patentes\Chatgpt\FlowGermUniqueness.20260906_014746.log` | `850f1c1c88c25d6d372c6d548bdb85d0eae09203cdd0e58fff9b5b1f4eea7ecf` |
| `C:\IALD\Central de Patentes\Chatgpt\FlowGermUniqueness.lean` | `56d58175a69f4bbc2d24537538e28690e58353b6b46c64fda97122afd5e8fa80` |
| `C:\IALD\Central de Patentes\Chatgpt\FlowRegularityInduction.20260906_015338.log` | `0ce5ad9da59adfcbbf9defe57bf95afbaef72ddd5648207ce175e36649cc6990` |
| `C:\IALD\Central de Patentes\Chatgpt\FlowRegularityInduction.lean` | `7a602877fa9c06fc52a4cac12914f35cc2dea1c094e15b4ffd447fe6360d9ad7` |
| `C:\IALD\Central de Patentes\Chatgpt\FlowSmoothGerm.20260906_015408.log` | `3f658cc9574a07cf6b53d7b4080e744d06af01db3c5eb36423fc1d4d9df8fc89` |
| `C:\IALD\Central de Patentes\Chatgpt\FlowSmoothGerm.lean` | `b2abb3d9659f1f6c621652011f5e1cb214d41ecd796adf98e80006529e6074d4` |
| `C:\IALD\Central de Patentes\Chatgpt\FlowTimePropagation.20260906_015923.log` | `04e6a81364fddbf3e69739bf98b4deeb8411085998296a2d3ef8354416dc30a2` |
| `C:\IALD\Central de Patentes\Chatgpt\FlowTimePropagation.lean` | `1d6237a5bf4df19545b66960686a4beae743b2029a53a7fb4609df7d862bd039` |
| `C:\IALD\Central de Patentes\Chatgpt\SmoothFlowControls.20260906_020212.log` | `6efce1506a0a6f4ee7e291cff8177940007a8ea384dbb20958f687032c792238` |
| `C:\IALD\Central de Patentes\Chatgpt\SmoothFlowControls.lean` | `211ee7979dc2c21fb9e99a438507b892a8a370623a65281ca9eb5168807d5dfa` |
| `C:\IALD\Central de Patentes\Chatgpt\SmoothGeodesicFlow.20260906_020100.log` | `76afcf54f0f4809cc4c3058e286148902c0d19118febe202a34c00a10c59ebc9` |
| `C:\IALD\Central de Patentes\Chatgpt\SmoothGeodesicFlow.lean` | `cf900d670324ea20eeedd79acee28c0c0f9c2f059024ceb243e9bf3442f003de` |

## Tentativas preservadas

- `C:\IALD\Central de Patentes\Chatgpt\FlowRegularityInduction.20260906_014949.failed_compile.log`: exit code 1; cópia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\FlowRegularityInduction.20260906_015112.rejected_warning.log`: exit code 0; cópia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\FlowSmoothGerm.20260906_015211.failed_compile.log`: exit code 1; cópia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\FlowTimePropagation.20260906_015641.failed_compile.log`: exit code 1; cópia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\FlowTimePropagation.20260906_015811.failed_compile.log`: exit code 1; cópia exata do log rejeitado.

Os backups preservam os bytes das versões compiladas. As falhas intermediárias de coerção, vizinhanças e composição, além dos avisos de variáveis, foram corrigidas sem apagar os registros. Só as compilações finais limpas sustentam a entrega.

## Próxima obrigação geométrica

A regularidade C∞ do fluxo está paga. Ainda é preciso selecionar uma seção transversal de dados iniciais nulos, provar a invertibilidade do diferencial do mapa de posição e construir a inversa local suave. A velocidade transportada então poderá definir um campo SmoothVectorOn no espaço-tempo. O primeiro jato de equilíbrio continua uma obrigação própria.
O operador variacional J desta cadeia é flowVariation de 016; não foi identificado com a conjugação modular. A solda invertível e a assinatura permanecem INPUT. A família completa no espaço de fases não é inteiramente nula: a conclusão recebe explicitamente a nulidade do dado inicial.

Nenhum um.py executado, importado ou editado. Todas as escritas em Chatgpt; kernel canônico, Atlas, memórias, selos e gate não foram tocados pela bancada. A custódia 016 foi reconferida sem alterações. O objetivo amplo permanece ativo e OPEN; esta é uma prova local sob hipóteses nomeadas.

Parecer: C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO017_PARECER.md.

Ordens de entrada encontradas no inventário:
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_001_esperanca_condicional_e_escala.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_002_veredito_da_auditoria_e_incorporacao.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_003_localizacao_na_cadeia_e_ponte_volume.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_004_D1_fiacao_e_D7_segundo_objeto.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_005_reabertura_v98_e_teste_conjunto.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_006_esperanca_do_centralizador_e_inclusao_meio_lateral.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_007_habitante_global_nao_ciclicidade_e_assinatura.md
