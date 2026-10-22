[REAL / INPUT / OPEN] ENTREGA 016 ESPONTÂNEA — diferencial efetivo do fluxo e regularidade conjunta C1.

06/09/2026. Continuação de 015. Auditoria independente pendente. Nenhuma alteração de gate.

## Critérios e alcance

| Critério | Estado | Evidência |
|---|---|---|
| Derivação anterior ao código | PAGO | CONTINUACAO016_DERIVACAO_PREVIA.md; adendo posterior identificado, versão anterior preservada em backup de bytes. |
| Existência com Lipschitz nos dados iniciais | PAGO | lipschitzLocalFlow; bola e intervalo comuns no aberto prescrito. |
| Operador variacional | PAGO | variationalLocalFlow; J(0)=I e J′=Df(Φ)∘J por HasDerivAt. |
| Equação do erro de linearização | PAGO | flow_remainder_derivative, com resto de Taylor explícito. |
| Taylor uniforme deduzido | PAGO | flow_taylor_uniform usa suavidade e compacidade do intervalo temporal; não acrescenta uma hipótese de Taylor ao resultado final. |
| Derivada efetiva nos dados | PAGO | flow_initial_hasFDerivAt em ambos os sinais do tempo; prova por Grönwall e little-o. |
| Derivada conjunta e C1 | PAGO | flow_joint_hasStrictFDerivAt e flow_joint_c1; DΦ[h,τ]=Jh+τf(Φ). |
| Fluxo geodésico C1 e nulidade | PAGO sob INPUT | local_c1_metric_null_geodesics e local_c1_levi_civita_null_geodesics; solda/conexão suave recebida, nulidade inicial explícita. |
| Controles | PAGO | Campo linear com resto zero, campo nulo com J=I, bloco plano J(hx,hv)=(hx+t hv,hv), fluxo curvo C1 inicialmente nulo. |
| C∞ nos dados e congruência espacial | NÃO PAGO | Regularidade superior, seção transversal, inversão local da posição e primeiro jato de equilíbrio ainda faltam. |
| Reconstrução gravitacional geral | NÃO PAGO | H3, entropia-área microscópica, coeficiente físico, calor, ponte modular e globalização permanecem OPEN. |

6 módulos; 41 teoremas declarados; 4 definições com axiomas impressos separadamente. Contagens lidas dos fontes.
As declarações reutilizam resultados de Picard/mathlib e conservação de 015; a contagem não representa descobertas matemáticas novas. A contribuição formal está na identificação do diferencial do fluxo e sua continuidade conjunta.
Os logs finais da fonte fixada não têm erros, avisos ou sorryAx. Axiomas impressos: apenas propext, Classical.choice e Quot.sound.

## Reprodução

```powershell
& 'C:\Python314\python.exe' -B 'C:\IALD\Central de Patentes\Chatgpt\audit_continuation016.py'
```

Esse comando é somente leitura. Confere os bytes e as evidências do compilador; não substitui a recompilação independente da gerência. A ordem de compilação dos módulos novos é:
- DifferentialFlowExistence.lean
- VariationalFlow.lean
- FlowLinearizationError.lean
- FlowDifferentiability.lean
- GeodesicInitialRegularity.lean
- FlowDifferentiabilityControls.lean

FlowDifferentiabilityControls importa toda a árvore 016 e os controles 015. O manifesto registra também a ordem completa dos fontes locais. Recompilar em cópia independente, mantendo imutáveis fontes, oleans e logs entregues. O wrapper verify_stage.ps1 e os metadados documentam a configuração Lean 4.31.0/mathlib usada.

## Axiomas impressos

```text
ChatgptAudit.Flow016.eventually_flow_rectangle: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow016.lipschitzLocalFlow: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow016.flow_initial_distance_bound: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow016.flow_joint_continuous_at: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow016.variational_domain_open: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow016.variational_field_smooth: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow016.variationalLocalFlow: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow016.diagonal_initial_mem: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow016.flow_solution_initial: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow016.flow_variation_initial: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow016.flow_solution_derivative: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow016.flow_variation_derivative: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow016.flow_variation_apply_derivative: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow016.flow_solution_stays: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow016.flow_solution_distance_bound: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow016.solution_and_variation_continuous: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow016.flow_remainder_initial: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow016.flow_remainder_derivative: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow016.flow_remainder_gronwall: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow016.gronwall_zero_scaling: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow016.flow_remainder_normalized_bound: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow016.flow_remainder_normalized_bound_nonpositive: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow016.flow_initial_hasFDerivAt_nonpositive: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow016.flow_initial_hasFDerivAt: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow016.taylor_remainder_eventually: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow016.flow_taylor_uniform: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow016.flow_derivative_norm_bounded: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow016.flow_initial_hasFDerivAt_nonnegative: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow016.phaseFlowOfVariational: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow016.phase_flow_of_variational_c1: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow016.c1GeodesicFlow: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow016.c1_geodesic_flow_joint_c1: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow016.local_c1_metric_null_geodesics: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow016.local_c1_levi_civita_null_geodesics: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow016.flow_time_derivative_continuous: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow016.flow_joint_hasStrictFDerivAt: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow016.flow_joint_derivative_continuous: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow016.flow_joint_c1: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow016.linear_taylor_remainder_zero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow016.zero_field_flow_constant: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow016.zero_field_variation_identity: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow016.flat_geodesic_initial_derivative: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow016.flat_variation_block: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow016.flat_variation_on_perturbation: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow016.curved_c1_null_flow_control: [propext, Classical.choice, Quot.sound]
```

## Artefatos e hashes

Manifesto: `C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO016_MANIFESTO.json` — SHA256 `5296e7fa2d8874240b24f211408166239a52d58b204f9256182969bb75c2e2a1`.
Inventário: 538 caminhos absolutos com tamanho e hash dos bytes.

| Artefato principal | SHA256 |
|---|---|
| `C:\IALD\Central de Patentes\Chatgpt\audit_continuation016.py` | `5d5fca891e2b0c22edf515399ab07f3e1b48f07c6f3c680eaaf515471fb276ce` |
| `C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO016_DERIVACAO_PREVIA.md` | `ae0ed29844c62e83d012c74fb88d361d65cffc8398d23718c3803166569a492c` |
| `C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO016_PARECER.md` | `af14cab89ba0d449c683f1c1adf615ce575fc41cd9dc7cec159b904144c9e431` |
| `C:\IALD\Central de Patentes\Chatgpt\DifferentialFlowExistence.20260906_010850.log` | `63268d15272f0f8d5abfe646f8f64c005d28d0118f3ae6261e4ec2a510f67b98` |
| `C:\IALD\Central de Patentes\Chatgpt\DifferentialFlowExistence.lean` | `f851ce4709144f7f2ffe5da5de7ed82784399373f434592539d92116ae5df09e` |
| `C:\IALD\Central de Patentes\Chatgpt\FlowDifferentiability.20260906_013114.log` | `2a9e9fbbd5a4eeebae89cdb9176c36fea8e37eb01a66c7b3030b5d60f7a6ba83` |
| `C:\IALD\Central de Patentes\Chatgpt\FlowDifferentiability.lean` | `6a87f5fff36009f4502c8a013d70f5e038581a440bc5be39b23ca5d4b6e60fb2` |
| `C:\IALD\Central de Patentes\Chatgpt\FlowDifferentiabilityControls.20260906_013554.log` | `6568f4667dd566caaa16a0dce23d3ed3c63e0fd07bff27f604923db6d088eab0` |
| `C:\IALD\Central de Patentes\Chatgpt\FlowDifferentiabilityControls.lean` | `a9e1752b26a07641593b2847dc442bf93c25323bba51aab134e3161907b33d68` |
| `C:\IALD\Central de Patentes\Chatgpt\FlowLinearizationError.20260906_011726.log` | `648a0f0960192209b561e098216b2710e85a5fe91ce2655b6a49e80423e5db3c` |
| `C:\IALD\Central de Patentes\Chatgpt\FlowLinearizationError.lean` | `32945b3f3a49181b0f508a44cbbb854934e8d87a951ada050574f57388f4d7b0` |
| `C:\IALD\Central de Patentes\Chatgpt\GeodesicInitialRegularity.20260906_013331.log` | `d44ecf28be1bfdb6208a8f8bdfcf992e43d48efe622ae7e9daba6eacbff54e70` |
| `C:\IALD\Central de Patentes\Chatgpt\GeodesicInitialRegularity.lean` | `c49d2b3c5e207d241261f60beb2534f1149d6991e55c1f5ec1726113c307c009` |
| `C:\IALD\Central de Patentes\Chatgpt\VariationalFlow.20260906_011406.log` | `f9b6ea0075e7093791f0f16aab243d00a275848c0205478d8c4f77ae9bb775af` |
| `C:\IALD\Central de Patentes\Chatgpt\VariationalFlow.lean` | `74fb3acaca323323b83e77627657eedf4dabbd8b4bf529ad129c18badb65c0b6` |

## Tentativas preservadas

- `C:\IALD\Central de Patentes\Chatgpt\DifferentialFlowExistence.20260906_010622.failed_compile.log`: exit code 1; erro de elaboração ou aviso; cópia exata do log.
- `C:\IALD\Central de Patentes\Chatgpt\VariationalFlow.20260906_011038.failed_compile.log`: exit code 1; erro de elaboração ou aviso; cópia exata do log.
- `C:\IALD\Central de Patentes\Chatgpt\VariationalFlow.20260906_011248.failed_compile.log`: exit code 1; erro de elaboração ou aviso; cópia exata do log.
- `C:\IALD\Central de Patentes\Chatgpt\FlowDifferentiability.20260906_011827.failed_compile.log`: exit code 1; erro de elaboração ou aviso; cópia exata do log.
- `C:\IALD\Central de Patentes\Chatgpt\FlowDifferentiability.20260906_012310.failed_compile.log`: exit code 1; erro de elaboração ou aviso; cópia exata do log.
- `C:\IALD\Central de Patentes\Chatgpt\FlowDifferentiability.20260906_012902.failed_compile.log`: exit code 1; erro de elaboração ou aviso; cópia exata do log.
- `C:\IALD\Central de Patentes\Chatgpt\FlowDifferentiability.20260906_012958.rejected_warning.log`: exit code 0; erro de elaboração ou aviso; cópia exata do log.
- `C:\IALD\Central de Patentes\Chatgpt\GeodesicInitialRegularity.20260906_013147.failed_compile.log`: exit code 1; erro de elaboração ou aviso; cópia exata do log.

Os backups preservam todas as versões efetivamente compiladas. Falhas intermediárias de tipos, composição e continuidade foram corrigidas; avisos de argumentos redundantes foram removidos. Só as compilações finais limpas sustentam a entrega.

## Parede exata

O fluxo é C1 conjunto. SmoothVectorOn de 014 requer C∞: a indução de regularidade superior ainda não foi formalizada. Também faltam a seleção transversal de dados e a inversa local da projeção para a posição. A família completa no espaço de fases não é uma congruência espacial e não é inteiramente nula; a preservação da nulidade recebe o dado inicial nulo.
A construção usa uma nova escolha de Picard no sistema variacional. Não foi provada igualdade literal com a escolha existencial da entrega 015; seus teoremas gerais de conservação se aplicam ao novo LocalPhaseFlow.

A relação microscópica entropia-área e Clausius/H3 permanecem abertas. [Jacobson, 1995](https://arxiv.org/html/gr-qc/9504004) assume a proporcionalidade entropia-área e a relação de Clausius para sua dedução termodinâmica; citar essa dedução não paga as hipóteses.

Escritas exclusivamente em Chatgpt. Nenhum um.py executado, importado ou editado; kernel canônico, Atlas, memórias, selos e gate intocados. As custódias 014 e 015 foram reconferidas sem alteração. O objetivo amplo de gravidade quântica permanece ativo e OPEN.

Parecer: C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO016_PARECER.md.

Ordens de entrada encontradas no momento do inventário:
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_001_esperanca_condicional_e_escala.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_002_veredito_da_auditoria_e_incorporacao.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_003_localizacao_na_cadeia_e_ponte_volume.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_004_D1_fiacao_e_D7_segundo_objeto.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_005_reabertura_v98_e_teste_conjunto.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_006_esperanca_do_centralizador_e_inclusao_meio_lateral.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_007_habitante_global_nao_ciclicidade_e_assinatura.md
