[REAL / DERIVED / KNOWN / OPEN] ENTREGA 007 — habitante global periódico construído; cauda não cíclica; obstruções de Borchers e da identificação finita da assinatura provadas com escopo explícito.

Pronta para auditoria independente da gerência. Escritas restritas a Chatgpt; nenhum um.py, gate, kernel canônico, Atlas ou memória foi alterado.

## Critérios de aceitação

| Critério | Estatuto | Evidência e alcance |
|---|---|---|
| A — derivação antes do código | PAGO | ORDEM007_DERIVACAO_PREVIA.md; adendo anterior à generalização de Borchers preservado em backup. |
| A.1 stationary_modular_period | PAGO | Igualdade em H; generalização à rede inteira de log-razões dos sítios. |
| A.2 period_average_operator | PAGO | Integral forte de vetores, continuidade, linearidade e norma ≤ ‖x‖. |
| A.3 period_average_mem_factor | PAGO | Comutação com o comutante atravessa a integral; entrada efetiva no bicomutante M. |
| A.4 period_average_prefix | PAGO | Projeção limitada em H atravessa a integral; cálculo de todas as entradas, sem hipótese fictícia de continuidade σ-fraca. |
| A — habitante | PAGO | periodicExpectationInput e stationaryExpectationInput habitam TGLExt.ExpectationInput P; campos por prova. |
| A — unicidade e restrição | PAGO | periodic_expectation_unique e periodic_expectation_local. |
| A — controle ½ | PAGO | periodic_half_agrees em M; o wrapper não tracial exclui ½ por tipo, a construção periódica comum inclui. |
| B.1 tail_not_cyclic | PAGO | Testemunha v, norma²=p(1−p)>0, ortogonalidade e fecho próprio. |
| B.2 consequência abstrata | PAGO | SubalgebraExpectationInput é HIPÓTESE; ciclicidade força N=M. |
| B.3 Borchers | PAGO como negativo condicionado; PAREDE NOMEADA para formalização do teorema clássico | product_borchers_trivial vale para TODO perfil produto sob continuidade, norma preservada, V(0)=I e relação de Borchers. Energia positiva/compressão ⇒ relação permanece KNOWN, não axioma Lean. |
| C.1 invariância e não invariância | PAGO | Métrica lorentziana soldada preservada; euclidiana não preservada por boost não trivial, para frame invertível. |
| C.1 identificação Δ^{it}↔boost finito | NEGATIVO PAGO no tipo testado | Entrelaçamento injetivo de ℝ⁴ com isometria positiva força parâmetro do boost zero; aplica-se ao fluxo real da torre. |
| C.1 escolha única de assinatura | NÃO PAGO; INFERÊNCIA REFUTADA | Um único boost preserva (1,3) e (2,2). A comparação com (4,0) não seleciona sozinha Lorentz. |
| C.2 pontes matriciais | PAGO | B₄ usa K₁ canônico; bloco coincide com TGLExt.boost; nada por homonímia. |
| C — ponte geométrica geral | PAREDE NOMEADA | Requer outra representação/objetos e domínio explícito; não foi construída. |
| A/B/C — frase final | PAGO | Matemática sem escolha delegada ao operador; incorporação pela gerência após auditoria. |

## Verificação e reprodução

10 módulos; 58 teoremas; 4 definições com axiomas impressos; todos os logs finais limpos e dependências axiomáticas contidas no trio. Definições auxiliares sem impressão individual são identificadas no manifesto e estão cobertas pelas provas que as usam.

Executar com o ambiente local de Lean 4.31.0 e dependências resolvidas pelo verificador:

```powershell
python 'C:\IALD\Central de Patentes\Chatgpt\audit_order007.py'
& 'C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1' -Module StationaryModularPeriod
if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }
& 'C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1' -Module PeriodAverageOperator
if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }
& 'C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1' -Module PeriodAveragePrefix
if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }
& 'C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1' -Module PeriodicCentralizerExpectation
if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }
& 'C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1' -Module TailNotCyclic
if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }
& 'C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1' -Module CyclicExpectationObstruction
if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }
& 'C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1' -Module PeriodicBorchersObstruction
if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }
& 'C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1' -Module ProductBorchersObstruction
if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }
& 'C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1' -Module ModularSignatureObstruction
if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }
& 'C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1' -Module Order007Bridges
if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }
```

O manifesto inclui a ordem de compilação das dependências da bancada. Os comandos acima recompilam os dez módulos novos usando essas dependências já presentes. O auditor de bytes não é uma recompilação independente.

## Axiomas efetivamente impressos

```text
ChatgptAudit.tower_log_lattice: [propext, Classical.choice, Quot.sound]
ChatgptAudit.modularPhase_lattice_period: [propext, Classical.choice, Quot.sound]
ChatgptAudit.lattice_flowLevel_period: [propext, Classical.choice, Quot.sound]
ChatgptAudit.lattice_modular_period: [propext, Classical.choice, Quot.sound]
ChatgptAudit.stationary_site_log_lattice: [propext, Classical.choice, Quot.sound]
ChatgptAudit.stationary_log_gap_ne_zero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.stationary_modular_period: [propext, Classical.choice, Quot.sound]
ChatgptAudit.modularFlow_continuous_apply: [propext, Classical.choice, Quot.sound]
ChatgptAudit.modular_orbit_continuous: [propext, Classical.choice, Quot.sound]
ChatgptAudit.modular_orbit_bound: [propext, Classical.choice, Quot.sound]
ChatgptAudit.periodAverageVector: [propext, Classical.choice, Quot.sound]
ChatgptAudit.average_vector_add: [propext, Classical.choice, Quot.sound]
ChatgptAudit.average_vector_smul: [propext, Classical.choice, Quot.sound]
ChatgptAudit.average_vector_bound: [propext, Classical.choice, Quot.sound]
ChatgptAudit.periodAverage: [propext, Classical.choice, Quot.sound]
ChatgptAudit.period_average_operator: [propext, Classical.choice, Quot.sound]
ChatgptAudit.period_average_commutes: [propext, Classical.choice, Quot.sound]
ChatgptAudit.period_average_mem_factor: [propext, Classical.choice, Quot.sound]
ChatgptAudit.lattice_local_phase_period: [propext, Classical.choice, Quot.sound]
ChatgptAudit.integral_modularPhase: [propext, Classical.choice, Quot.sound]
ChatgptAudit.integral_flowLevel: [propext, Classical.choice, Quot.sound]
ChatgptAudit.integral_modularFlow_local: [propext, Classical.choice, Quot.sound]
ChatgptAudit.period_average_prefix: [propext, Classical.choice, Quot.sound]
ChatgptAudit.period_average_into: [propext, Classical.choice, Quot.sound]
ChatgptAudit.period_average_fixes: [propext, Classical.choice, Quot.sound]
ChatgptAudit.period_average_ortho: [propext, Classical.choice, Quot.sound]
ChatgptAudit.periodicExpectationInput: [propext, Classical.choice, Quot.sound]
ChatgptAudit.stationaryExpectationInput: [propext, Classical.choice, Quot.sound]
ChatgptAudit.half_profile_has_period: [propext, Classical.choice, Quot.sound]
ChatgptAudit.periodic_half_agrees: [propext, Classical.choice, Quot.sound]
ChatgptAudit.tail_prefix_expectation_scalar: [propext, Classical.choice, Quot.sound]
ChatgptAudit.tail_mark_factorization: [propext, Classical.choice, Quot.sound]
ChatgptAudit.tail_witness_orthogonal: [propext, Classical.choice, Quot.sound]
ChatgptAudit.tail_witness_inner: [propext, Classical.choice, Quot.sound]
ChatgptAudit.tail_witness_norm_sq: [propext, Classical.choice, Quot.sound]
ChatgptAudit.tail_witness_ne_zero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.tail_not_cyclic: [propext, Classical.choice, Quot.sound]
ChatgptAudit.cyclic_expectation_forces_identity: [propext, Classical.choice, Quot.sound]
ChatgptAudit.cyclic_expectation_forces_full_algebra: [propext, Classical.choice, Quot.sound]
ChatgptAudit.proper_expected_subalgebra_not_cyclic: [propext, Classical.choice, Quot.sound]
ChatgptAudit.contraction_invariant_continuous_constant: [propext, Classical.choice, Quot.sound]
ChatgptAudit.periodic_borchers_trivial: [propext, Classical.choice, Quot.sound]
ChatgptAudit.eigenvector_diagonal_modular_invariant: [propext, Classical.choice, Quot.sound]
ChatgptAudit.isometry_fixed_of_diagonal: [propext, Classical.choice, Quot.sound]
ChatgptAudit.product_borchers_fixes_eigenvector: [propext, Classical.choice, Quot.sound]
ChatgptAudit.product_borchers_trivial: [propext, Classical.choice, Quot.sound]
ChatgptAudit.boost4_preserves_eta: [propext, Classical.choice, Quot.sound]
ChatgptAudit.boost4_preserves_split: [propext, Classical.choice, Quot.sound]
ChatgptAudit.boost4_not_euclidean: [propext, Classical.choice, Quot.sound]
ChatgptAudit.lorentz_solder_boost_invariant: [propext, Classical.choice, Quot.sound]
ChatgptAudit.euclidean_solder_not_boost_invariant: [propext, Classical.choice, Quot.sound]
ChatgptAudit.real_gram_cannot_equal_eta: [propext, Classical.choice, Quot.sound]
ChatgptAudit.single_boost_has_two_signatures: [propext, Classical.choice, Quot.sound]
ChatgptAudit.positive_norm_isometry_no_exp_eigenvector: [propext, Classical.choice, Quot.sound]
ChatgptAudit.boost4_null_expand: [propext, Classical.choice, Quot.sound]
ChatgptAudit.no_injective_isometric_boost_intertwiner: [propext, Classical.choice, Quot.sound]
ChatgptAudit.concrete_frame_euclidean_not_invariant: [propext, Classical.choice, Quot.sound]
ChatgptAudit.periodic_expectation_unique: [propext, Classical.choice, Quot.sound]
ChatgptAudit.periodic_expectation_local: [propext, Classical.choice, Quot.sound]
ChatgptAudit.boost4_is_canonical_generator: [propext, Classical.choice, Quot.sound]
ChatgptAudit.boost4_is_canonical_block: [propext, Classical.choice, Quot.sound]
ChatgptAudit.tower_modular_cannot_intertwine_nonzero_boost: [propext, Classical.choice, Quot.sound]
```

## Arquivos e SHA256

Manifesto completo: `C:\IALD\Central de Patentes\Chatgpt\ORDEM007_MANIFESTO.json` — SHA256 `3fdd9c6d78cd9f28801ead938f8b3337fdeef2d595cb9014effd2110001a2bc1`.
São 459 arquivos por caminho absoluto, tamanho e hash dos bytes, incluindo todas as tentativas registradas, backups e dependências locais compiladas.

| Artefato principal | SHA256 |
|---|---|
| `C:\IALD\Central de Patentes\Chatgpt\audit_order007.py` | `53221c5103d04f87764937cb28e1eebec1d4f10a0d60155d19eb4933669a70d6` |
| `C:\IALD\Central de Patentes\Chatgpt\CyclicExpectationObstruction.20260905_200011.log` | `f9735ef40ee6ba0d504b9059cd746525b92f37a8d388ffdef457701a03331820` |
| `C:\IALD\Central de Patentes\Chatgpt\CyclicExpectationObstruction.lean` | `2594979664cfad358d48c6562c29f58786e77a6146db83fe670f720f97339f34` |
| `C:\IALD\Central de Patentes\Chatgpt\ModularSignatureObstruction.20260905_200323.log` | `dbfe5e396031e54a4f31979939d861dc771959fd49af36b55773790c99753375` |
| `C:\IALD\Central de Patentes\Chatgpt\ModularSignatureObstruction.lean` | `f7a4923aab5cb187257fc6f257b7dfebbd7f2efe2ff19db9f965ef8ea59f25fe` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM007_DERIVACAO_PREVIA.md` | `b9809ce08283c3687331089b38b75dc2a47ee840c33e3eb08e4f0b7c7c06317c` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM007_NOTAS_DE_EXECUCAO.md` | `9284eede25b307cffa6d36f25735224f12f7d0ff780d9a26a369ec7363d2f5a0` |
| `C:\IALD\Central de Patentes\Chatgpt\ORDEM007_PARECER_FINAL.md` | `2edbc39ff514f08b8926e6652b7f1cd1644b816f41bb82062893b4ef688e9de5` |
| `C:\IALD\Central de Patentes\Chatgpt\Order007Bridges.20260905_200717.log` | `42dbd211796871dca7f95405814b79751bb6865af8d54f975c5f0317f7e0fb7d` |
| `C:\IALD\Central de Patentes\Chatgpt\Order007Bridges.lean` | `026d65dc9edd140cc192ea76f5911e7992797d6f07e12dafcc28be0f50c6ff83` |
| `C:\IALD\Central de Patentes\Chatgpt\PeriodAverageOperator.20260905_194949.log` | `11e83daf938f1e8e7f3389fac19f86399728bc24ec4cb6e970a7f11ee7909f2e` |
| `C:\IALD\Central de Patentes\Chatgpt\PeriodAverageOperator.lean` | `f491d6fc494c1bedad95ffcbe97b5d7a147a3d9dc6801f6eefb4aa7238dd8e42` |
| `C:\IALD\Central de Patentes\Chatgpt\PeriodAveragePrefix.20260905_195357.log` | `695eaec4acfd5842dde654e8a30a8aec779f030d808331227bd4c363ccaac021` |
| `C:\IALD\Central de Patentes\Chatgpt\PeriodAveragePrefix.lean` | `41c873874a47a4daefaa78d2f931bf80dac066ec31787784a02fd1199bce71ff` |
| `C:\IALD\Central de Patentes\Chatgpt\PeriodicBorchersObstruction.20260905_195857.log` | `5840fd596532a8c49b9c5482590f6112504a0d9829be0669647db38be7affba3` |
| `C:\IALD\Central de Patentes\Chatgpt\PeriodicBorchersObstruction.lean` | `fa09c1cba67305feeaca6f8d6c3ff09ce83e1fa048182bbb42b7f8b80848cfb9` |
| `C:\IALD\Central de Patentes\Chatgpt\PeriodicCentralizerExpectation.20260905_195730.log` | `6e45d7fe9317a0413012974b1a8154f7904457e48ec123a89f198090dc5c1a2e` |
| `C:\IALD\Central de Patentes\Chatgpt\PeriodicCentralizerExpectation.lean` | `75c3a7c91ceef8b3ccd8720954b9596f7e8e878d908792ecccb995be18e0b6c4` |
| `C:\IALD\Central de Patentes\Chatgpt\ProductBorchersObstruction.20260905_200634.log` | `5fd9f4d7fa68966c6643928f68c523ab1b9abb86925c4974871aa8d579d825b5` |
| `C:\IALD\Central de Patentes\Chatgpt\ProductBorchersObstruction.lean` | `e7300708e7d5136119a67ad1170869e68c138c392ebc9632840a0ee42cf7c630` |
| `C:\IALD\Central de Patentes\Chatgpt\StationaryModularPeriod.20260905_194950.log` | `714d1298bd3296ca75e39e9bbb7385bb8344be0d5ff13547b73ff5119bfd18a9` |
| `C:\IALD\Central de Patentes\Chatgpt\StationaryModularPeriod.lean` | `7defb7a949df32fb7229be7a2c932215e8dac304e276a29fdf44a9b18926bcb0` |
| `C:\IALD\Central de Patentes\Chatgpt\TailNotCyclic.20260905_195731.log` | `548194b548d8c15bfa876d2015c6b2f91cf658575c14332bb0386ee94c910b22` |
| `C:\IALD\Central de Patentes\Chatgpt\TailNotCyclic.lean` | `2ce432a9d285db19f317c31c48a752e9947ec431a32195b902f9a36c09d31deb` |

O parecer detalha enunciados, topologias, hipóteses, limites e os negativos. A entrega não é a reconstrução gravitacional geral e não altera qualquer conclusão física. O objetivo amplo permanece aberto.

Nada nas conclusões matemáticas é decisão do operador. A gerência audita e decide incorporação; v98, errata e contorno continuam reservados ao operador.
