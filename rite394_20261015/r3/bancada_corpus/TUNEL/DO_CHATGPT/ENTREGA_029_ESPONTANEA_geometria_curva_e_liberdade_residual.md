[REAL / INPUT / OPEN] ENTREGA 029 ESPONTANEA - geometria curva, casamento entropico e liberdade residual.

06/09/2026. Continuacao da ordem 007 e da entrega 028. O objetivo amplo permanece aberto; auditoria independente da gerencia pendente.

Foi construida uma familia classica de metricas de onda plana, em todo R4, ligada aos estados globais reais da 028. Com eta4=diag(1,-1,-1,-1), k=(1,0,0,1), l=(1,0,0,-1), H=a*x^2+c*y^2, o coframe E=I+(H/2)(l tensor k) tem inversa D=I-(H/2)(l tensor k). O kernel calcula g=eta4+H(k tensor k), a inversa, sua Levi-Civita, Ric=(a+c)(k tensor k), R=0 e G=Ric.

O covetor constante k foi provado paralelo, nulo na metrica inversa e igual ao gradiente da funcao t+z. Sua equacao de onda e a conservacao do tensor escalar T=kappa(k tensor k) sao demonstradas. Para os estados da 028, kappa=log(2)*sum(b)/pi.

Para eta nao zero, define-se r=2*pi*kappa/eta, a=r/2+s e c=r/2-s. A condicao harea foi demonstrada nessa FAMILIA ESCOLHIDA, para toda tela de equilibrio local em todo ponto e direcao nula nao zero. O calor corresponde e a equacao G=(2*pi/eta)T vale com Lambda=0. A cadeia geral anterior de area para Einstein tambem foi instanciada, sem harea como hipotese no teorema final da familia.

A resposta entropica e ligada as probabilidades efetivamente lidas dos estados: o defeito entre a entropia lida e a area tende a zero, dividido pelo tempo ao quadrado, no limite conjunto arbitrario de corte e tempo (matched_read_area_joint). Nao se define entropia a partir da area.

Controle adversarial: na origem, a correspondencia exige exatamente eta*(a+c)=2*pi*kappa. Coeficiente errado falha. O parametro s permanece livre: Ric e materia ficam iguais, as metricas coincidem na origem, mas as componentes de curvatura diferem e R^1_(0 1 0)-R^2_(0 2 0)=2*s. Isso prova subdeterminacao da coordenada de curvatura no ansatz; nao e uma classificacao de metricas modulo isometria.

Com b=0 e s nao zero, Ric=0 e a curvatura e nao nula. Com o perfil geometrico da 028 e eta nao zero, ha materia nao nula e geometria curva correspondente.

[INPUT / OPEN] Selecionar o ansatz e ajustar a soma dos coeficientes a resposta fornece existencia. Nao demonstra uma dinamica microscopica que force esse ajuste. H3 geral, regiao-algebra, origem da assinatura/dimensao, correlacoes e materia quantica geral permanecem abertos.

[KNOWN] A classe geometrica tem antecedentes classicos: [David Tong, General Relativity, secao 5.2.3](https://davidtong.org/teaching/general-relativity/grhtml/S5) apresenta ondas de Brinkmann e a liberdade de perfil sem traco no vacuo; [Harte e Drivas, Physical Review D 85, 124039](https://link.aps.org/accepted/10.1103/PhysRevD.85.124039) apresenta a curvatura e Ricci de pp-waves. As formulas e os sinais desta bancada foram verificados por Lean; nenhum resultado externo entrou como axioma.

## Criterios

| Criterio | Estado | Evidencia |
|---|---|---|
| Derivacao anterior ao codigo | PAGO | CONTINUACAO029_DERIVACAO_PREVIA.md; auditor 028 reconferido. |
| Metrica e inversa reais | PAGO | wave_solder_inverse, wave_inverse_solder, wave_metric_formula, wave_inverse_metric_formula. |
| Conexao calculada | PAGO | wave_metric_jet e wave_levi_civita, com derivadas de fderiv. |
| Curvatura calculada | PAGO | wave_ricci, wave_scalar_curvature, wave_einstein, wave_first_curvature e wave_second_curvature. |
| Materia escalar conservada | PAGO | wave_covector_parallel, wave_covector_wave, wave_covector_potential e wave_matter_conserved. |
| Habitante curvo de harea | PAGO NA FAMILIA ESCOLHIDA | matched_wave_area e matched_constructed_area, em todos os pontos e telas locais. |
| Calor e Einstein | PAGO NA FAMILIA ESCOLHIDA | wave_heat_matching, matched_wave_einstein e matched_wave_einstein_from_area. |
| Resposta lida dos estados | PAGO | wave_read_entropy_joint e matched_read_area_joint; marginais e fidelidade de 026-028. |
| Controle da escolha e liberdade | PAGO | wave_origin_area_iff, wave_wrong_trace_refused, zero_eta_nonzero_source_refused, matched_curvature_distinguishes e state_alone_not_curvature_coordinate. |
| Controles nao triviais | PAGO | zero_wave_vacuum, zero_wave_nonflat, geometric_wave_matter_nonzero e geometric_wave_curved. |
| Dinamica microscopica geral e prova ampla | NAO PAGO | A geometria foi selecionada dentro de um ansatz. A lei de area geral e a selecao da liberdade radiativa permanecem abertas. |

6 modulos; 64 teoremas; 12 definicoes impressas. Contagens incluem auxiliares.
Fontes finais: exit 0, bytes estaveis, zero erros/avisos/sorryAx; somente propext, Classical.choice, Quot.sound.

## Reproducao

```powershell
& 'C:\Python314\python.exe' -B 'C:\IALD\Central de Patentes\Chatgpt\audit_continuation029.py'
```

Comando somente leitura; recompilacao independente em copias, na ordem do manifesto:
- C:\IALD\Central de Patentes\Chatgpt\PlaneWaveSolder.lean
- C:\IALD\Central de Patentes\Chatgpt\PlaneWaveConnection.lean
- C:\IALD\Central de Patentes\Chatgpt\PlaneWaveCurvature.lean
- C:\IALD\Central de Patentes\Chatgpt\PlaneWaveMatter.lean
- C:\IALD\Central de Patentes\Chatgpt\PlaneWaveEntropyMatching.lean
- C:\IALD\Central de Patentes\Chatgpt\PlaneWaveReconstructionControls.lean

## Axiomas

```text
ChatgptAudit.Wave029.waveCovector: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.waveRaised: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.waveSolder: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.waveInverseSolder: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.wave_covector_nonzero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.wave_nilpotent_square: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.wave_solder_inverse: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.wave_inverse_solder: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.wave_metric_formula: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.wave_inverse_metric_formula: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.wave_profile_smooth: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.wave_solder_smooth: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.wave_inverse_solder_smooth: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.wave_profile_partial: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.wave_metric_at_origin: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.wave_inverse_metric_null: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.waveConnection: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.wave_metric_jet: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.wave_levi_civita: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.wave_connection_smooth: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.wave_connection_torsion_free: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.wave_transverse_partial: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.wave_connection_linear: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.wave_connection_jet: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.wave_connection_commute: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.wave_curvature_formula: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.wave_ricci: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.wave_scalar_curvature: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.wave_einstein: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.wave_first_curvature: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.wave_second_curvature: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.wave_curvature_nonzero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.waveCovectorField: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.waveMatter: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.wave_covector_smooth: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.wave_covector_closed: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.wave_covector_parallel: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.wave_covector_wave: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.wave_matter_formula: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.wave_matter_smooth: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.wave_matter_conserved: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.wave_matter_independent: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.wave_matter_nonzero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.wave_covector_potential: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.matched_read_area_joint: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.waveRicciScale: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.matchedSolder: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.matchedInverseSolder: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.matchedScreen: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.matched_parameter_sum: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.wave_ricci_quad: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.wave_matter_quad: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.wave_area_matching_of_sum: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.matched_wave_area: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.matched_constructed_area: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.wave_heat_matching: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.matched_wave_einstein: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.matched_wave_einstein_from_area: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.wave_read_entropy_joint: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.zero_eta_nonzero_source_refused: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.waveOriginScreen: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.wave_test_nonzero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.wave_test_null: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.wave_test_frequency: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.wave_origin_area_iff: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.wave_wrong_trace_refused: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.matched_ricci_independent: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.matched_curvature_difference: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.matched_curvature_distinguishes: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.matched_metrics_agree_at_origin: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.zero_wave_ricci_scale: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.zero_wave_vacuum: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.zero_wave_nonflat: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.geometric_wave_matter_nonzero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.geometric_wave_curved: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Wave029.state_alone_not_curvature_coordinate: [propext, Classical.choice, Quot.sound]
```

## Artefatos

Manifesto: C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO029_MANIFESTO.json; SHA256 dos bytes: 77a2aded4cf1c990fed4da5cfb3e4eec36f3b39b726f8c7542f78b0de5dfb69d.
Inventario: 763 caminhos, com tamanho e SHA256.

| Artefato principal | SHA256 |
|---|---|
| C:\IALD\Central de Patentes\Chatgpt\audit_continuation029.py | 90537fe6964dcd2c1069d3ff137b4a598ddc0a5d8111696d9d8bb470bc5d4c21 |
| C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO029_DERIVACAO_PREVIA.md | 2d20c0cc417cb7ba96a91b8ba355500abc561e63e8fb0d606b9a2d9823557a11 |
| C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO029_PARECER.md | 8c5f05df1a5ff1fad8b9c18a9ae3e11608b6344367941d41ede3e7d67fb4717e |
| C:\IALD\Central de Patentes\Chatgpt\PlaneWaveConnection.20260906_091523.log | 056dfd0efb4727a68e445229f291893f4b60fe0b37ee21a107576c1a364aa9a8 |
| C:\IALD\Central de Patentes\Chatgpt\PlaneWaveConnection.lean | dfaec97ec688c973e51c5381e34e04ff47e3537c4d91ab196d76392a8f13692c |
| C:\IALD\Central de Patentes\Chatgpt\PlaneWaveCurvature.20260906_092036.log | 279545c90d0dcd64b1b67b2d84c6ef8cf6a7cc1655d05fca5e97419b52230090 |
| C:\IALD\Central de Patentes\Chatgpt\PlaneWaveCurvature.lean | be472ae7657b8c6b5b788f2f0f6a03911aa931cb67dae50081130c5e2b6fb99c |
| C:\IALD\Central de Patentes\Chatgpt\PlaneWaveEntropyMatching.20260906_092447.log | 2d5503ebb516a1f7a8016bb36eb38ab24bbfd5c03964dcb82da49c584e393141 |
| C:\IALD\Central de Patentes\Chatgpt\PlaneWaveEntropyMatching.lean | e26f2baeac3286f068ab644ce445749f86f599e4194b06b0ccd05676aa6a3000 |
| C:\IALD\Central de Patentes\Chatgpt\PlaneWaveMatter.20260906_092253.log | b7f97ec36f3971f43ffc0a1a21551c7ef989c8765b13b5031d0b50efaec6607a |
| C:\IALD\Central de Patentes\Chatgpt\PlaneWaveMatter.lean | b5bf094650858478f3ee84ca862d5952ab51b51e4e1bb97c3c2276458383b41d |
| C:\IALD\Central de Patentes\Chatgpt\PlaneWaveReconstructionControls.20260906_092721.log | 302a89ddb9c21dcc505956a40e4ff63072f0ab3b6fce100ccf170ca6e147a06b |
| C:\IALD\Central de Patentes\Chatgpt\PlaneWaveReconstructionControls.lean | cdd5013252ade12d9ace0eca7e74ff032bae3b473a2f5eb5aef8f2cf28884cdd |
| C:\IALD\Central de Patentes\Chatgpt\PlaneWaveSolder.20260906_091055.log | 6249a47b6a1ca02094f025d0024d2260e9ffcba6b2820e18878dca395cdff118 |
| C:\IALD\Central de Patentes\Chatgpt\PlaneWaveSolder.lean | 56aae7d8f8ebb30f724117182298173ba1a48951933a2370e09902a53518b981 |

## Tentativas rejeitadas preservadas

- C:\IALD\Central de Patentes\Chatgpt\PlaneWaveSolder.20260906_090327.failed_compile.log: exit 1; copia dos bytes do log.
- C:\IALD\Central de Patentes\Chatgpt\PlaneWaveSolder.20260906_090645.failed_compile.log: exit 1; copia dos bytes do log.
- C:\IALD\Central de Patentes\Chatgpt\PlaneWaveSolder.20260906_090747.failed_compile.log: exit 1; copia dos bytes do log.
- C:\IALD\Central de Patentes\Chatgpt\PlaneWaveSolder.20260906_090924.rejected_warning.log: exit 0; copia dos bytes do log.
- C:\IALD\Central de Patentes\Chatgpt\PlaneWaveConnection.20260906_091147.failed_compile.log: exit 1; copia dos bytes do log.
- C:\IALD\Central de Patentes\Chatgpt\PlaneWaveConnection.20260906_091413.rejected_warning.log: exit 0; copia dos bytes do log.
- C:\IALD\Central de Patentes\Chatgpt\PlaneWaveCurvature.20260906_091720.rejected_warning.log: exit 0; copia dos bytes do log.
- C:\IALD\Central de Patentes\Chatgpt\PlaneWaveMatter.20260906_092133.rejected_warning.log: exit 0; copia dos bytes do log.
- C:\IALD\Central de Patentes\Chatgpt\PlaneWaveEntropyMatching.20260906_092343.failed_compile.log: exit 1; copia dos bytes do log.
- C:\IALD\Central de Patentes\Chatgpt\PlaneWaveReconstructionControls.20260906_092627.rejected_warning.log: exit 0; copia dos bytes do log.

10 tentativas rejeitadas preservadas com logs e fontes em backups dos bytes.

## Limites e dividas

- The metric ansatz, four-dimensional Lorentzian reference, scalar covector and entropy family are specified inputs. This is an existence construction inside that class, not derivation of general geometry from omega(I)=1.
- The sum of transverse coefficients is chosen to satisfy the area matching. Its successful construction is not an independent microscopic dynamics forcing that choice. H3 remains OPEN for the general objective.
- The difference of those coefficients remains a free real parameter. Equal entropy, Ricci and matter do not select the tested curvature coordinate. No global non-isometry classification is inferred merely from components.
- The eta coefficient must be nonzero in the area theorem. The direct algebraic Einstein formula also holds at eta=0 under Lean's total division convention; that degenerate formula is not a physical area-matching assertion.
- The matter source is a massless scalar with a parallel null gradient. No classification of general quantum matter, physical selection of eta or Newton units, region-algebra correspondence, correlations or positive-energy spacetime translations is supplied.
- The state-read limits are those of specified diagonal prefix functionals. Araki identification, full path differentiability, and a general quantum gravitational theory are not established.
- Only exact final clean compilations support the delivery. Counts include helper lemmas and controls; no count measures completion of the broad proof.
- Canonical originals, um.py, Atlas, memories, gates, seals and earlier deliveries remain untouched. Managerial independent audit/incorporation remain pending.

Parecer: C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO029_PARECER.md

Ordens encontradas:
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_001_esperanca_condicional_e_escala.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_002_veredito_da_auditoria_e_incorporacao.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_003_localizacao_na_cadeia_e_ponte_volume.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_004_D1_fiacao_e_D7_segundo_objeto.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_005_reabertura_v98_e_teste_conjunto.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_006_esperanca_do_centralizador_e_inclusao_meio_lateral.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_007_habitante_global_nao_ciclicidade_e_assinatura.md
