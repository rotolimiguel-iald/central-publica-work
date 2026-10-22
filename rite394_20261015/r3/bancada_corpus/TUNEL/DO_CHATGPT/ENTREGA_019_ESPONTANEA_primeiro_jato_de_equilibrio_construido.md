[REAL / INPUT / OPEN] ENTREGA 019 ESPONTÂNEA — primeiro jato de equilíbrio construído na congruência nula local.

06/09/2026. Continuação de 018. Auditoria independente da gerência pendente. Nenhuma alteração de gate.

## Critérios

| Critério | Estado | Evidência |
|---|---|---|
| Derivação anterior ao código | PAGO | CONTINUACAO019_DERIVACAO_PREVIA.md. |
| Campo afim com jato prescrito | PAGO | affine_seed_derivative e affine_seed_gradient_zero. |
| Erro de nulidade com derivada zero | PAGO | affine_seed_energy_derivative_zero, por compatibilidade métrica. |
| Correção nula sem alterar o jato | PAGO | null_correction_null e null_correction_preserves_derivative. |
| Dados iniciais inteiramente construídos | PAGO sob INPUT | local_null_seed_with_zero_covariant_jet constrói companheiro, aberto e campo nulo. |
| Transferência para a congruência | PAGO | shooting_velocity_derivative_zero, shooting_inverse_derivative_base e congruence_prescribed_gradient_zero. |
| Existência com equilíbrio | PAGO sob INPUT | local_levi_civita_equilibrium_congruence acrescenta ∇V(p)=0 à construção de 018, sem receber esse equilíbrio como hipótese. |
| Tela e focalização | PAGO sob INPUT | localEquilibriumScreen e local_equilibrium_screen_with_focusing: θ(p)=0, A(0)=1 e θ′(0)=−Ric(v,v). |
| Forma óptica inicial | PAGO | equilibrium_screen_optical_form_zero: Sᵀg(∇V)S=0 no ponto. |
| Controles | PAGO | Campo de equilíbrio construído em fundo plano e em fundo com curvatura não zero; o segundo difere do campo expansivo de 014. |
| Horizonte nulo imerso e área integrada | NÃO PAGO | A carta do fluxo e o jato no ponto não fornecem por si uma hipersuperfície nula integrada. |
| Reconstrução gravitacional geral | NÃO PAGO | Ponte microscópica, coeficiente físico, calor, Clausius/H3, ponte modular e globalização permanecem OPEN. |

7 módulos; 38 teoremas declarados; 1 definição com axiomas impressos separadamente. Contagens lidas dos fontes.
As compilações finais fixadas têm exit 0, fonte estável e nenhum erro, aviso ou sorryAx. Os axiomas impressos pertencem ao trio propext, Classical.choice, Quot.sound. As contagens incluem aplicações, lemas auxiliares e controles que reutilizam resultados anteriores.

## Enunciado principal

Dados U aberto, A e B suaves com AB=BA=I em U, p∈U e uma tangente v≠0 nula para g(p)=A(p)ᵀηA(p), existem p∈N⊆U aberto e V suave em N com V(p)=v, V≠0, g(V,V)=0, ∇_V V=0 em N e ∇V(p)=0.
A nova condição é pontual. Não se afirma que V seja paralelo num aberto. A construção não exige curvatura zero; o controle curvo verifica isso.

## Reprodução

```powershell
& 'C:\Python314\python.exe' -B 'C:\IALD\Central de Patentes\Chatgpt\audit_continuation019.py'
```

O comando só lê e confere bytes, logs e axiomas registrados. A gerência deve recompilar em uma cópia para a auditoria independente. Ordem dos novos módulos:
- NullJetAlgebra.lean
- PrescribedCovariantJet.lean
- NullSeedWithJet.lean
- ShootingJetTransfer.lean
- EquilibriumNullCongruence.lean
- EquilibriumScreenIntegration.lean
- EquilibriumCongruenceControls.lean

EquilibriumCongruenceControls importa toda a árvore 019 e as dependências locais anteriores. O manifesto contém a ordem local completa. O wrapper documenta Lean 4.31.0/mathlib; não se declara um pacote portátil integral.

## Axiomas impressos

```text
ChatgptAudit.Flow019.quadratic_sub_null_direction: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow019.null_correction_null: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow019.null_correction_fixes_null: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow019.tensor_pair_smooth: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow019.null_correction_smooth: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow019.scalar_derivative_zero_from_partials: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow019.zero_jet_quotient: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow019.null_correction_preserves_derivative: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow019.connection_initial_jet_apply: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow019.vector_partial_of_derivative: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow019.gradient_action_derivative: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow019.derivative_of_zero_covariant_gradient: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow019.affine_seed_initial: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow019.affine_seed_smooth: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow019.affine_seed_derivative: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow019.affine_seed_covariant_derivative_zero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow019.affine_seed_gradient_zero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow019.affine_seed_energy_derivative_zero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow019.null_companion_of_frame: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow019.null_seed_with_companion: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow019.local_null_seed_with_zero_covariant_jet: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow019.shooting_velocity_derivative_zero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow019.shooting_inverse_base_zero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow019.shooting_inverse_derivative_base: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow019.congruence_derivative_base: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow019.congruence_prescribed_gradient_zero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow019.local_equilibrium_congruence_from_seed: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow019.local_levi_civita_equilibrium_congruence: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow019.localEquilibriumScreen: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow019.equilibrium_screen_expansion_zero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow019.equilibrium_screen_optical_form_zero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow019.equilibrium_screen_area_initial: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow019.equilibrium_screen_focusing: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow019.local_equilibrium_screen_with_focusing: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow019.control_companion_null: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow019.control_companion_pair: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow019.zero_gradient_differs_from_expanding_field: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow019.flat_equilibrium_congruence_control: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Flow019.curved_equilibrium_congruence_control: [propext, Classical.choice, Quot.sound]
```

## Artefatos e hashes

Manifesto: `C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO019_MANIFESTO.json` — SHA256 `79c189dd36a1c2aacfee80c182b65b14e5068b76a3f95df8e4e5809a0b89765c`.
Inventário: 588 caminhos absolutos, com tamanho e hash dos bytes.

| Artefato principal | SHA256 |
|---|---|
| `C:\IALD\Central de Patentes\Chatgpt\audit_continuation019.py` | `740335c4fafabb507cd15e06e447416b403355da0ec268a28bd69dc3e924352e` |
| `C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO019_DERIVACAO_PREVIA.md` | `7ecb01b4885f0b2ec49a8df584fe621d0cc8990c9537b26ae3d2687850e26a74` |
| `C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO019_PARECER.md` | `3bf0e6a42461f572f04ba76f150eea2bad20e3377fd4571fe5b1855f9b0a9385` |
| `C:\IALD\Central de Patentes\Chatgpt\EquilibriumCongruenceControls.20260906_030814.log` | `985cf6e77c738c60111096108f59d8faacaf020fd8814ff0f27867b0f15b6cb5` |
| `C:\IALD\Central de Patentes\Chatgpt\EquilibriumCongruenceControls.lean` | `9e839270ad00c11f9bba28dbe03ead72334e44995467b191301fd4ca5df3ea20` |
| `C:\IALD\Central de Patentes\Chatgpt\EquilibriumNullCongruence.20260906_030444.log` | `3fac439d2da5aa6aaa96ea4dbb743e0aebb2129b33dac75bfa612d4db496853f` |
| `C:\IALD\Central de Patentes\Chatgpt\EquilibriumNullCongruence.lean` | `5e7b7a185bf0cf54352eba4a157076b1d8bc9298d86a5b43e9c6efdad7444425` |
| `C:\IALD\Central de Patentes\Chatgpt\EquilibriumScreenIntegration.20260906_030720.log` | `755741f6d7cc3af6357a6334980158f950d24c7f139c35c2111a6db1e9053c5f` |
| `C:\IALD\Central de Patentes\Chatgpt\EquilibriumScreenIntegration.lean` | `3f101e3e72741fe93c06099f4c254c4c09bcbd86983d13dfc92d22963b903cf2` |
| `C:\IALD\Central de Patentes\Chatgpt\NullJetAlgebra.20260906_025200.log` | `01348f0bebed4eedef19ffa6240c06aac8e81180391542d3c75436e9e24c9c80` |
| `C:\IALD\Central de Patentes\Chatgpt\NullJetAlgebra.lean` | `6751e63dda74886d33ea1959531d177cd9d756da3aa375e8b85a2e9b76b1985e` |
| `C:\IALD\Central de Patentes\Chatgpt\NullSeedWithJet.20260906_030054.log` | `84e2511330e36ade496dcc79ca5228ba3971df8113cf795b621f194c14bbc660` |
| `C:\IALD\Central de Patentes\Chatgpt\NullSeedWithJet.lean` | `67e27e009b70497d70e5aa932356865729b75ca0b095e1d9ded97fe21cb06cce` |
| `C:\IALD\Central de Patentes\Chatgpt\PrescribedCovariantJet.20260906_025814.log` | `8a752b7de101261786a4a15aaeae10a755833eef95d06d0eb9a62c22bcaebf16` |
| `C:\IALD\Central de Patentes\Chatgpt\PrescribedCovariantJet.lean` | `cedd249385dd2779baa178dac8587ebd1bb8daf9cba59e76a4c79f6f74d1781a` |
| `C:\IALD\Central de Patentes\Chatgpt\ShootingJetTransfer.20260906_030357.log` | `ae388698319b29901b12bdf21f2859072f4437dcf40201a1ef544afae04d0c3a` |
| `C:\IALD\Central de Patentes\Chatgpt\ShootingJetTransfer.lean` | `ac8f4c525a2c251ebc415fe5e85d37836adf2c631ee28668da8e4fd59aef850f` |

## Tentativas preservadas

- `C:\IALD\Central de Patentes\Chatgpt\NullJetAlgebra.20260906_024440.failed_compile.log`: exit code 1; cópia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\NullJetAlgebra.20260906_024705.failed_compile.log`: exit code 1; cópia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\NullJetAlgebra.20260906_024858.failed_compile.log`: exit code 1; cópia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\NullJetAlgebra.20260906_025052.rejected_warning.log`: exit code 0; cópia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\PrescribedCovariantJet.20260906_025335.failed_compile.log`: exit code 1; cópia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\PrescribedCovariantJet.20260906_025601.rejected_warning.log`: exit code 0; cópia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\NullSeedWithJet.20260906_025938.failed_compile.log`: exit code 1; cópia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\ShootingJetTransfer.20260906_030141.rejected_warning.log`: exit code 0; cópia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\EquilibriumScreenIntegration.20260906_030530.failed_compile.log`: exit code 1; cópia exata do log rejeitado.

Todas as versões compiladas são recuperáveis pelo fonte final ou pelos backups de bytes. Somente as compilações finais limpas sustentam a entrega; as falhas intermediárias e os avisos não foram apagados.

## Limites

O equilíbrio inicial é pago como gradiente covariante zero. A forma óptica projetada também zera; não foi introduzida uma definição independente de cisalhamento para rebatizar uma hipótese.
EquilibriumScreenData contém somente os dados geométricos construídos. Não se disfarçam calor ou Clausius como geometria: GeometricHorizonPencil ainda os exige e não foi declarado habitado por esta entrega.
A área inicial um é a normalização da base da tela. Não fixa unidade física nem coeficiente microscópico de entropia por área.
A hipersuperfície nula, a integrabilidade além do ponto, a área integrada, as identificações microscópicas, o calor/H3 e a ponte modular seguem OPEN. Dimensão, assinatura e solda continuam INPUT.

Nenhum um.py executado, importado ou editado. Todas as escritas em Chatgpt; kernel canônico, Atlas, memórias, selos e gate intocados pela bancada. A custódia 018 foi reconferida em modo de leitura.
O objetivo amplo permanece ativo e não alcançado. Incorporação pela gerência após auditoria; confirmação física reservada ao observador.

Parecer: C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO019_PARECER.md.

Ordens de entrada encontradas no inventário:
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_001_esperanca_condicional_e_escala.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_002_veredito_da_auditoria_e_incorporacao.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_003_localizacao_na_cadeia_e_ponte_volume.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_004_D1_fiacao_e_D7_segundo_objeto.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_005_reabertura_v98_e_teste_conjunto.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_006_esperanca_do_centralizador_e_inclusao_meio_lateral.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_007_habitante_global_nao_ciclicidade_e_assinatura.md
