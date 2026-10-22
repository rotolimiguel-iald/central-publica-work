[REAL / INPUT / OPEN] ENTREGA 018 ESPONTÂNEA — congruência nula local construída por seção transversal e inversão suave.

06/09/2026. Continuação de 017. Auditoria independente da gerência pendente. Nenhuma alteração de gate.

## Critérios e alcance

| Critério | Estado | Evidência |
|---|---|---|
| Derivação anterior ao código | PAGO | CONTINUACAO018_DERIVACAO_PREVIA.md; seis passos anteriores às provas Lean. |
| Dados transversais | PAGO | exists_normalized_covector, initial_position_in_section, initial_position_shift e transported_seed_null. |
| Domínio aberto e suavidade | PAGO | shooting_domain_zero e shooting_phase_smooth; argumentos mantidos no domínio fixo do fluxo de 017. |
| Diferencial invertível | PAGO | shooting_position_derivative_zero: DX(0)=I, usando o diferencial efetivo do fluxo de 016. |
| Inversa suave no aberto | PAGO | smoothLocalChart produz OpenPartialHomeomorph com fonte contida no domínio e inversa ContDiffOn ℝ ∞ em todo o alvo. |
| Campo espacial construído | PAGO | shootingCongruence=Y∘X⁻¹; congruence_smooth, congruence_nonzero, congruence_null e congruence_base_value. |
| Equação geodésica | PAGO | congruence_geodesic: vectorAcceleration Γ V=0; a prova usa derivadas reais das curvas X(z+sv) e Y(z+sv). |
| Existência a partir da solda | PAGO sob INPUT | local_levi_civita_null_congruence recebe apenas aberto, solda/inversa suaves e tangente nula não nula; constrói N e V. |
| Tela e variação de área | PAGO sob INPUT | constructed_congruence_transported_screen aplica 014 ao campo construído e prova A′=θA localmente, no lado t<0. |
| Controles | PAGO | Congruência construída com solda identidade; construção em fundo de curvatura não zero; campo explícito geodésico nulo com θ(0)=2. |
| Primeiro jato de equilíbrio | NÃO PAGO | Nulidade e geodesicidade não impõem θ=0 nem cisalhamento nulo. O controle separa essas obrigações. |
| Reconstrução gravitacional geral | NÃO PAGO | Horizonte nulo imerso, área integrada, H3, ponte microscópica, coeficiente físico, calor, ponte modular e globalização seguem OPEN. |

7 módulos; 37 teoremas declarados; 1 definição com axiomas impressos separadamente. Contagens lidas dos fontes.
Todas as compilações finais fixadas têm exit 0, fonte estável e nenhum erro, aviso ou sorryAx. Os axiomas impressos pertencem ao trio propext, Classical.choice, Quot.sound.
As contagens incluem lemas auxiliares, aplicações e controles que reutilizam resultados anteriores. Não são contagens de descobertas científicas.

## Enunciado principal

Se U é aberto, A e B são campos matriciais suaves com AB=BA=I em U, p∈U, v≠0 e (A(p)ᵀηA(p))(v,v)=0, existem N aberto com p∈N⊆U e V suave em N tais que V(p)=v, V não se anula, g(V,V)=0 e ∇_V V=0 em N.
A solda, a dimensão e a assinatura são INPUT. A existência de V deixou de ser INPUT nesta etapa. A conclusão é local; não constrói por si uma hipersuperfície nula ou um horizonte.

## Reprodução

```powershell
& 'C:\Python314\python.exe' -B 'C:\IALD\Central de Patentes\Chatgpt\audit_continuation018.py'
```

O comando é somente leitura e confere os bytes, logs, enunciados contados e dependências de axiomas registrados. A gerência deve recompilar numa cópia para a auditoria independente, preservando os artefatos entregues. Ordem dos módulos novos:
- TransverseInitialData.lean
- GeodesicShooting.lean
- ShootingLocalInverse.lean
- NullCongruenceField.lean
- ConstructedNullCongruence.lean
- CongruenceScreenIntegration.lean
- NullCongruenceControls.lean

NullCongruenceControls importa toda a árvore 018 e as entregas anteriores usadas. A ordem local completa consta do manifesto. verify_stage.ps1 documenta a compilação Lean 4.31.0; as dependências externas não constituem um pacote portátil integral.

## Axiomas impressos

```text
ChatgptAudit.Flow018.exists_normalized_covector: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow018.transverse_projection_decomposition: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow018.transverse_projection_velocity: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow018.initial_position_in_section: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow018.initial_position_shift: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow018.initial_time_shift: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow018.initial_position_smooth: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow018.transported_seed_initial: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow018.transported_seed_null: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow018.transported_seed_nonzero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow018.transported_seed_smooth: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow018.shooting_position_derivative_zero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow018.shooting_position_along_time: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow018.shooting_velocity_along_time: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow018.shooting_input_zero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow018.shooting_phase_zero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow018.shooting_domain_open: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow018.shooting_domain_zero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow018.shooting_input_smooth: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow018.shooting_phase_smooth: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow018.shooting_regular: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow018.shooting_null: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow018.smoothLocalChart: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow018.chart_position_inverse: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow018.congruence_smooth: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow018.congruence_target_subset: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow018.congruence_nonzero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow018.congruence_base_mem: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow018.congruence_base_value: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow018.congruence_null: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow018.congruence_geodesic: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow018.local_null_congruence_from_seed: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow018.local_levi_civita_null_congruence: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow018.constructed_congruence_transported_screen: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow018.control_direction_nonzero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow018.flat_constructed_congruence_control: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow018.curved_constructed_congruence_control: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow018.geodesic_nullity_does_not_force_zero_expansion: [propext, Classical.choice, Quot.sound]
```

## Artefatos e hashes

Manifesto: `C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO018_MANIFESTO.json` — SHA256 `36cb5978d8c1ef85c6168d241abd6281429d2d80dae25d7cebacd24a75981d73`.
Inventário: 553 caminhos absolutos, cada um com tamanho e hash dos bytes.

| Artefato principal | SHA256 |
|---|---|
| `C:\IALD\Central de Patentes\Chatgpt\audit_continuation018.py` | `7bc56df472c4d949976b93329cc59a2c697a19b0a2268f0aeb5181ef3aefbfce` |
| `C:\IALD\Central de Patentes\Chatgpt\CongruenceScreenIntegration.20260906_023435.log` | `e6c2187913f72fd71f113c77fbf68eb18f7df25c452c88e559cf87f5649b9aef` |
| `C:\IALD\Central de Patentes\Chatgpt\CongruenceScreenIntegration.lean` | `30296b142d74ffc9fdd11f4b837470bec4a0339e05dc9d3e9ff05ae2a98dd1bf` |
| `C:\IALD\Central de Patentes\Chatgpt\ConstructedNullCongruence.20260906_023308.log` | `3354289fa2c29a28fd70ad26909cf36778ffc92ca46910f95531e9f0136c90c4` |
| `C:\IALD\Central de Patentes\Chatgpt\ConstructedNullCongruence.lean` | `679c8937c82f37a2a1894d860eed40ee171f031f9130b16c0d7fd3ac82283a91` |
| `C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO018_DERIVACAO_PREVIA.md` | `5d1452bfda4d71eaccb3b42da74d144f242ce496f481fae5e575799efa3ac989` |
| `C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO018_PARECER.md` | `9fe0464b7f6552fd9b83309614201c19e9df7b9fb3c593071480a35ba9a8fb6e` |
| `C:\IALD\Central de Patentes\Chatgpt\GeodesicShooting.20260906_022911.log` | `03c3324073cfeb8b018bbffaee542515849a2a66e86f2d8667d35d5f9c23793d` |
| `C:\IALD\Central de Patentes\Chatgpt\GeodesicShooting.lean` | `075597b01a7d8056910cb98bccf823364fd7635a5c6c13b061023208914a5e32` |
| `C:\IALD\Central de Patentes\Chatgpt\NullCongruenceControls.20260906_023702.log` | `d7ac91b612d3efa80747ae404a780910daaab1757f8fe6783c3bfbc145c5f2de` |
| `C:\IALD\Central de Patentes\Chatgpt\NullCongruenceControls.lean` | `349968bc736b7c47d7c2a4f1771279723928459f48627dc496b863b74fab8f7b` |
| `C:\IALD\Central de Patentes\Chatgpt\NullCongruenceField.20260906_023134.log` | `6c367fa200f573b4cdb4d541812015fc4b258c8e126f804fb0e70602f994482e` |
| `C:\IALD\Central de Patentes\Chatgpt\NullCongruenceField.lean` | `51b2356d38291598d26a4b801e8648c44260ebb41b260c1ea212cff9bf9a0a46` |
| `C:\IALD\Central de Patentes\Chatgpt\ShootingLocalInverse.20260906_021641.log` | `a834fa00e94b7469c5550a96d179d153a40b6b5ba7a1018adceb2e6de46cf5ae` |
| `C:\IALD\Central de Patentes\Chatgpt\ShootingLocalInverse.lean` | `eb755ace607e766389b68257bd1b07b527bec28f3ebdbe79c6425786d0d6278a` |
| `C:\IALD\Central de Patentes\Chatgpt\TransverseInitialData.20260906_021721.log` | `ca711f94cf6c85958353003648974be61b6b23547ca59c36be935fe35b2bf055` |
| `C:\IALD\Central de Patentes\Chatgpt\TransverseInitialData.lean` | `da70165d09adc8c5e3728fd4af07dcf7192f94ce9aa45a8c83a3be44fb21300f` |

## Tentativas preservadas

- `C:\IALD\Central de Patentes\Chatgpt\TransverseInitialData.20260906_021451.failed_compile.log`: exit code 1; cópia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\GeodesicShooting.20260906_022147.failed_compile.log`: exit code 1; cópia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\GeodesicShooting.20260906_022710.failed_compile.log`: exit code 1; cópia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\NullCongruenceField.20260906_022956.failed_compile.log`: exit code 1; cópia exata do log rejeitado.

Todas as versões compiladas são recuperáveis pelo fonte final ou pelos backups de bytes. Falhas intermediárias não são evidência de prova: somente as compilações finais limpas sustentam a entrega. O helper de revisão teve uma quebra de linha ausente na criação; falhou antes de escrever documentos e sua versão defeituosa também foi preservada.

## Limites e próximo elo

A seção transversal inicial usa ℓ(v)=1 e Π=I−v⊗ℓ. Isso garante uma carta do fluxo; não garante que o campo resultante seja normal a uma hipersuperfície nula. Primeiro jato de equilíbrio e integrabilidade do horizonte são obrigações próprias.
O controle com θ(0)=2 reutiliza o campo explícito expandingNullVelocity de 014; não afirma que toda escolha de campo construída tenha essa expansão. Seu papel é refutar a implicação geodesicidade + nulidade ⇒ expansão zero.
A identidade de área é a da tela transportada de 014, válida eventualmente para t<0 perto de zero. Não é ainda uma integração sobre um horizonte.
Não se identifica flowVariation com a conjugação modular. Nenhuma ponte região–álgebra, entropia–área, H3 ou coeficiente físico foi assumida paga pelo novo teorema.

Nenhum um.py executado, importado ou editado. Todas as escritas em Chatgpt; kernel canônico, Atlas, memórias, selos e gate intocados pela bancada. As custódias 016 e 017 foram reconferidas por seus auditores de leitura.
O objetivo amplo permanece ativo e OPEN. A incorporação é da gerência após auditoria; a confirmação física é ato do observador. Esta entrega transporta o enunciado condicional exato.

Parecer: C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO018_PARECER.md.

Ordens de entrada encontradas no inventário:
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_001_esperanca_condicional_e_escala.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_002_veredito_da_auditoria_e_incorporacao.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_003_localizacao_na_cadeia_e_ponte_volume.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_004_D1_fiacao_e_D7_segundo_objeto.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_005_reabertura_v98_e_teste_conjunto.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_006_esperanca_do_centralizador_e_inclusao_meio_lateral.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_007_habitante_global_nao_ciclicidade_e_assinatura.md
