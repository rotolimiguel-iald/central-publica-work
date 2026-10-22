[REAL / INPUT / OPEN] ENTREGA 022 ESPONTÂNEA — resposta quadrática de uma evolução unitária explícita.

06/09/2026. Continuação de 021. Auditoria independente da gerência pendente. Nenhuma alteração de gate.

## Critérios

| Critério | Estado | Evidência |
|---|---|---|
| Derivação antes do código | PAGO | CONTINUACAO022_DERIVACAO_PREVIA.md. |
| Hamiltoniano e grupo unitário | PAGO | axis_hermitian, axis_square, pair_flow_group, pair_flow_adjoint_mul, pair_flow_mul_adjoint. |
| Equação diferencial e energia total | PAGO | pair_flow_schrodinger e pair_energy_conserved. |
| Estado bipartido produzido pelo fluxo | PAGO | correlated_flow_unitary, correlated_state_is_evolved e evolved_state_valid. |
| Marginal e admissibilidade | PAGO | pair_amplitude_weights, pair_weights_nonnegative, pair_weights_normalized; positividade estrita perto da referência. |
| Resposta inicialmente quadrática | PAGO | pair_weights_derivative, pair_tangent_at_zero e unitary_first_weight_response. |
| Entropia relativa da trajetória efetiva | PAGO | unitary_relative_entropy_quadratic_zero: D/t²→0. |
| Coeficientes de entropia e energia modular | PAGO | unitary_entropy_quadratic_limit, unitary_modular_quadratic_limit e unitary_marginal_modular_trace. |
| Clausius e reconstrução de Einstein | PAGO CONDICIONAL | unitary_matching_gives_clausius e einstein_from_unitary_microscopic_matching. |
| Restrição de sinal da matéria | PAGO CONDICIONAL / NEGATIVO | unitary_heat_matching_requires_matter e positive_response_blocks_nonnegative_heat_matching. |
| Controles exatos | PAGO | Hamiltonianos admissíveis com respostas (7/25)log(16/9)>0 e (−176/625)log(16/9)<0; controles estacionário e tracial. |
| Habitante do novo contrato | PAGO em controle plano | flatUnitaryVacuumMatching: eixo diagonal, marginal estacionária, calor e área de 020. |
| Recusa do controle incompatível | PAGO | flat_incompatible_matter_has_no_unitary_matching. |
| Identificações físicas gerais | NÃO PAGO | Os dois erros pequenos e a relação entre parâmetros permanecem INPUT/OPEN. |
| Dinâmica canônica e gravidade quântica | NÃO PAGO | Modelo finito candidato; nenhum novo veredito de gate. |

7 módulos; 73 teoremas declarados; 2 definições com axiomas impressos separadamente. Contagens lidas dos fontes.
Todas as compilações finais fixadas: exit 0, fonte estável, sem erros, avisos ou sorryAx. Axiomas permitidos: propext, Classical.choice, Quot.sound. A contagem inclui lemas auxiliares e controles.

## Resultado e alcance

O eixo M=[[a,b],[b,−a]], com a²+b²=1, define H=ωM e U(t)=cos(ωt)I−i sin(ωt)M. O código verifica o grupo unitário, U′=−iHU e U†HU=H. A energia total conservada não é identificada com o gerador modular da marginal.
A partir de Ψ(0)=u|00>+v|11>, u,v>0, u²+v²=1, a evolução dá amplitudes complexas explícitas. A extensão do fluxo ao espaço bipartido é unitária; sua ação coincide com o estado construído. A densidade é positiva, tem traço um e é idempotente.
O traço parcial efetivo é diagonal: r0(t)=u²+C sin²(ωt), r1(t)=v²−C sin²(ωt), C=(au+bv)²−u². A não negatividade global vem dos módulos quadrados; a referência estritamente positiva garante fidelidade local.
A tangente inicial da marginal zera. Portanto D(r(t)||r(0))/t²→0. As variações ΔS/t² e ΔK/t² convergem a L=ω²C log(v²/u²). A fórmula é da marginal diagonal; não se aplica a mesma entropia relativa ao estado bipartido puro.
UnitaryScreenMatching contém os parâmetros unitários, a referência normalizada e os dois erros de identificação E_heat/t²→0 e E_area/t²→0. Sob essas hipóteses, a identidade B=E_heat+cD+cE_area de 021 fornece Clausius e a reconstrução condicional G+Λg=(2π/η)T. O contrato não recebe Einstein como campo, mas ainda exige as identificações físicas.
A tangente nula foi demonstrada para esta família e suas amplitudes iniciais reais selecionadas. Não foi demonstrada para toda evolução unitária ou para estados iniciais arbitrários.
O uso do mesmo t nos estados e na curva geométrica é INPUT. Não há uma mudança livre de parâmetro afim nem uma demonstração de que esse Hamiltoniano é a dinâmica canônica do um.py.

## Controles e restrição de sinal

Para u=3/5, v=4/5 e ω=1: a=0,b=1 dá C=7/25; a=−3/5,b=4/5 dá C=−176/625. Os dois eixos satisfazem a²+b²=1. Como log(16/9)>0, o sinal da resposta muda com o Hamiltoniano. Os limites da entropia foram instanciados nos dois casos.
A correspondência calor–modular, combinada com o calor integrado de 020 e rate≠0, exige T_x(direction,direction)=−L/π. Assim, L>0 é incompatível com contração nula não negativa da matéria. L<0 retira essa obstrução de sinal; não demonstra a correspondência completa.
O eixo diagonal a=1,b=0 mantém os pesos fixos. Uma referência tracial tem resposta modular quadrática zero. Esses controles preservam os casos degenerados.
flatUnitaryVacuumMatching realiza os dois erros pequenos no controle plano de vácuo com eixo diagonal e marginal estacionária. É uma realização explícita do contrato; não fornece resposta gravitacional não nula. O controle plano conservado incompatível não admite UnitaryScreenMatching.

## Reprodução

```powershell
& 'C:\Python314\python.exe' -B 'C:\IALD\Central de Patentes\Chatgpt\audit_continuation022.py'
```

O comando só lê e confere bytes, logs e axiomas registrados. Recompilação independente é feita pela gerência em cópia. Ordem dos novos módulos:
- HermitianTwoLevelFlow.lean
- TwoLevelSchrodinger.lean
- CorrelatedUnitaryState.lean
- UnitaryMarginalDynamics.lean
- UnitaryEntropyResponse.lean
- UnitaryClausiusBridge.lean
- UnitaryResponseControls.lean

O manifesto fixa a árvore local e registra sua ordem. Lean/mathlib externos são resolvidos pelo wrapper; não é um pacote portátil integral.

## Axiomas impressos

```text
ChatgptAudit.Unitary022.axis_hermitian: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.axis_square: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.pair_hamiltonian_hermitian: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.axis_polynomial_product: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.pair_flow_zero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.pair_flow_group: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.pair_flow_adjoint: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.pair_flow_adjoint_mul: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.pair_flow_mul_adjoint: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.pair_hamiltonian_commutes: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.pair_energy_conserved: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.frequency_cos_derivative: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.frequency_sin_derivative: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.pair_flow_derivative: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.velocity_is_schrodinger: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.pair_flow_schrodinger: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.evolved_pair_zero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.evolved_pair_first: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.evolved_pair_second: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.cartesian_amplitude_square: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.first_weight_square: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.second_weight_square: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.pair_amplitude_weights: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.pair_weights_nonnegative: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.pair_weights_normalized: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.correlated_extension_one: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.correlated_extension_product: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.correlated_extension_adjoint: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.correlated_flow_unitary: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.correlated_extension_action: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.correlated_state_is_evolved: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.correlated_density_positive: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.correlated_amplitude_normalized: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.correlated_density_trace: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.correlated_density_idempotent: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.correlated_right_reduction: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.evolved_state_valid: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.pair_weights_derivative: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.pair_weights_at_zero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.pair_tangent_at_zero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.unitaryStateCurve: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.base_weights_positive: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.unitary_weights_positive_near: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.unitary_relative_entropy_quadratic_zero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.frequency_sin_slope: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.frequency_sin_square_limit: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.unitary_first_weight_response: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.unitary_modular_increment: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.unitary_modular_quadratic_limit: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.unitary_entropy_quadratic_limit: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.unitary_marginal_modular_trace: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.unitary_heat_error_limit: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.unitary_matching_gives_clausius: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.unitary_heat_matching_requires_matter: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.positive_response_blocks_nonnegative_heat_matching: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.unitary_screen_matching_produces_clausius: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.einstein_from_unitary_microscopic_matching: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.flatUnitaryVacuumMatching: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.flat_incompatible_matter_has_no_unitary_matching: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.transfer_coefficient_expanded: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.control_initial_normalized: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.positive_axis_normalized: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.negative_axis_normalized: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.positive_control_transfer: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.negative_control_transfer: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.control_log_positive: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.positive_control_response: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.negative_control_response: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.positive_control_response_strict: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.negative_control_response_strict: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.positive_control_entropy_limit: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.negative_control_entropy_limit: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.negative_control_required_matter_positive: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.diagonal_axis_stationary: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Unitary022.tracial_reference_response_zero: [propext, Classical.choice, Quot.sound]
```

## Artefatos e hashes

Manifesto: `C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO022_MANIFESTO.json` — SHA256 `dc4f5cff2ff8ef71f095a0788087ce420cd09e0ce7b83fb64a85835b3f8b575b`.
Inventário: 649 caminhos absolutos, com tamanho e hash dos bytes.

| Artefato principal | SHA256 |
|---|---|
| `C:\IALD\Central de Patentes\Chatgpt\audit_continuation022.py` | `d6ec3f797749c57a52810f42e66df78d2c02b3f748de1c6fdaf8cdde073d5a4e` |
| `C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO022_DERIVACAO_PREVIA.md` | `83520472b4d5a82e21f2bf5bd3eaf2caa208e5f54b4659cf7380e10f7c2e1249` |
| `C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO022_PARECER.md` | `2542586eaea5baf7e4e1b08611cdbf6eb72010277cc3cbe7cf86e5cecf405c4c` |
| `C:\IALD\Central de Patentes\Chatgpt\CorrelatedUnitaryState.20260906_043723.log` | `ec6247c0099aa6e89a213a243f8c630088e91b10c566092a13a07e458c9f1703` |
| `C:\IALD\Central de Patentes\Chatgpt\CorrelatedUnitaryState.lean` | `2d1e7d34247ff4ab794950ff03762e0e65a7efcdde6a663330a37559f37a0aea` |
| `C:\IALD\Central de Patentes\Chatgpt\HermitianTwoLevelFlow.20260906_042552.log` | `271db62921dfad10d1fd39eb7e7a00ef41184aef6554ed434c910efe0d5f3ef6` |
| `C:\IALD\Central de Patentes\Chatgpt\HermitianTwoLevelFlow.lean` | `c81b587b9e08e8f7308b358f0821cfacd56ad6b0348bfa201b8202f34b48b06e` |
| `C:\IALD\Central de Patentes\Chatgpt\TwoLevelSchrodinger.20260906_043255.log` | `e97d4e5a2f4dc9189b9c37e0bc67df0f8a3e7b68082e099b1ca3ac19c964b0c2` |
| `C:\IALD\Central de Patentes\Chatgpt\TwoLevelSchrodinger.lean` | `b12109e61c896f710989a3cecb4e37ea44f1f44cc95d3b33bd400b901e1a99c9` |
| `C:\IALD\Central de Patentes\Chatgpt\UnitaryClausiusBridge.20260906_044412.log` | `0326d1daca22e3a42daa5a5a8be62ea97212bf25d8baede1f955653a3711159f` |
| `C:\IALD\Central de Patentes\Chatgpt\UnitaryClausiusBridge.lean` | `29b2b9e4325c9fad325c70ffd998f6c976ed2db3c23ca9add23516b1f24d5995` |
| `C:\IALD\Central de Patentes\Chatgpt\UnitaryEntropyResponse.20260906_044034.log` | `1ea4ac4052d292a225b909538b0cb408d52463da8ad738a8adc259b98ac94834` |
| `C:\IALD\Central de Patentes\Chatgpt\UnitaryEntropyResponse.lean` | `fe4ce251ab3fe6ed0869a789d16fdd41d743b49a445e7f6f4e365701558ce540` |
| `C:\IALD\Central de Patentes\Chatgpt\UnitaryMarginalDynamics.20260906_043849.log` | `d361ad07ec7d786b27bfd2c8bcea7ccd5721d4e934cd192dab92d1257cc64806` |
| `C:\IALD\Central de Patentes\Chatgpt\UnitaryMarginalDynamics.lean` | `1b6844219157a386a7c6731497f83f48c45ea4d61e01029524fbfc440613f623` |
| `C:\IALD\Central de Patentes\Chatgpt\UnitaryResponseControls.20260906_044624.log` | `ca7cb05a01f38871faed5a878da76075207a28933bcf80a74612f04f332525b5` |
| `C:\IALD\Central de Patentes\Chatgpt\UnitaryResponseControls.lean` | `5495a1f413229189fd180dac745f6dc6e46e69244ace33a0cdf036c7a5a6c00d` |

## Tentativas preservadas

- `C:\IALD\Central de Patentes\Chatgpt\HermitianTwoLevelFlow.20260906_041654.failed_compile.log`: exit code 1; cópia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\HermitianTwoLevelFlow.20260906_041757.failed_compile.log`: exit code 1; cópia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\HermitianTwoLevelFlow.20260906_042507.failed_compile.log`: exit code 1; cópia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\TwoLevelSchrodinger.20260906_042713.failed_compile.log`: exit code 1; cópia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\TwoLevelSchrodinger.20260906_042816.failed_compile.log`: exit code 1; cópia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\TwoLevelSchrodinger.20260906_043036.failed_compile.log`: exit code 1; cópia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\TwoLevelSchrodinger.20260906_043139.rejected_warning.log`: exit code 0; cópia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\CorrelatedUnitaryState.20260906_043334.failed_compile.log`: exit code 1; cópia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\CorrelatedUnitaryState.20260906_043508.failed_compile.log`: exit code 1; cópia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\UnitaryEntropyResponse.20260906_043935.failed_compile.log`: exit code 1; cópia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\UnitaryClausiusBridge.20260906_044324.failed_compile.log`: exit code 1; cópia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\UnitaryResponseControls.20260906_044540.failed_compile.log`: exit code 1; cópia exata do log rejeitado.

Todas as versões compiladas são recuperáveis pelo fonte final ou pelos backups de bytes. Apenas as compilações finais limpas sustentam a entrega.

## Limites

O modelo é finito, com marginais comutantes. A evolução unitária finita aqui construída não substitui o regime hiperbólico da face e não contorna a obstrução de Borchers da torre-produto.
Não foram demonstradas seleção canônica do Hamiltoniano, coerência entre andares ou regiões, limite tipo III, origem modular da solda, dimensão/assinatura sem entrada, identificação do tensor T, unidades físicas ou globalização.
Os dados de cada tela no contrato podem ser escolhidos separadamente. Coerência entre essas escolhas não foi postulada como conclusão nem provada.
Calor–modular e entropia–área de ordem o(t²), parâmetro físico, horizonte imerso e área espacial integrada continuam OPEN.

Nenhum um.py executado, importado ou editado. Escritas somente em Chatgpt. Originais, entregas anteriores, kernel canônico, Atlas, memórias, selos e gate intocados. A custódia 021 foi reconferida em leitura.
O objetivo amplo permanece ativo e não alcançado. Incorporação depende da auditoria independente da gerência; confirmação física é ato do observador.

Parecer: C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO022_PARECER.md.

Ordens de entrada encontradas no inventário:
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_001_esperanca_condicional_e_escala.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_002_veredito_da_auditoria_e_incorporacao.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_003_localizacao_na_cadeia_e_ponte_volume.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_004_D1_fiacao_e_D7_segundo_objeto.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_005_reabertura_v98_e_teste_conjunto.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_006_esperanca_do_centralizador_e_inclusao_meio_lateral.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_007_habitante_global_nao_ciclicidade_e_assinatura.md
