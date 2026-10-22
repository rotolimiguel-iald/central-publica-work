[REAL / INPUT / OPEN] ENTREGA 023 ESPONTÂNEA — família unitária direcional, tensor candidato e conservação calculada.

06/09/2026. Continuação da entrega 022 e do objetivo amplo associado à ordem 007. A ordem 006 já foi aprovada pela gerência, segundo a ordem 007. Esta entrega não é uma nova ordem gerencial.

## Resultado e alcance

Com eixo M=[[a,b],[b,−a]] e referência u,v fixos, usar um único campo de covetores w: ell_x(d)=w_x(d), H_x(d)=ell_x(d)M. A composição U_x(d+e,t)=U_x(d,t)U_x(e,t) é provada no mesmo ponto. Direções no núcleo de w produzem fluxo trivial; isso não constrói translações do espaço-tempo.

A resposta da marginal efetiva de 022 é L_x(d)=L0 ell_x(d)². A matriz L0 w⊗w transforma-se por congruência quando o covetor muda de base. Escolhe-se κ=−L0/π e constrói-se T=κ[w⊗w−g q/2], q=gInv(w,w). Em direções nulas L=−πT(d,d), e o erro calor–modular/t² tende a zero para o calor temporal efetivo de 020. Essa escolha de normalização realiza a correspondência; não deriva as unidades ou a origem física de T.

Definindo W_ij=∇_i w_j, a prova calcula ∇^iT_ij=κ[(∇^i w_i)w_j+gInv^{ik}w_k(W_ij−W_ji)]. Sob covetor fechado e conexão sem torção, a segunda parcela desaparece. Com κ≠0 e w(x)≠0, conservação no ponto equivale a ∇^i w_i=0. Para w=dφ suave, o fechamento é demonstrado; a equação de onda continua uma hipótese dinâmica.

O tensor escalar e a dependência da conservação nas equações de movimento são [KNOWN] na literatura; o resultado desta bancada é sua verificação formal nas definições geométricas existentes e sua ligação à resposta escolhida. Referência primária: [Carroll, capítulo 1, equações (1.112)–(1.113)](https://ned.ipac.caltech.edu/level5/March01/Carroll3/Carroll1.html).

Qualquer tensor simétrico conservado com as mesmas contrações nulas difere do candidato por uma constante vezes a métrica, em domínio aberto preconexo, sob os antecedentes declarados. A conclusão depende da conservação de ambos.

O coeficiente do erro entropia–área é L_x(d)+η Ric_x(d,d)/2. Sua anulação equivale ao balanço nulo η Ric=2πT. Sob esse erro pequeno e a condição de onda, obtém-se G+Λg=(2π/η)T. A equivalência registra exatamente a dívida restante: a origem da relação de área não foi demonstrada pela renomeação do balanço de Einstein.

## Controles

No plano, com w=e0 constante e o eixo de resposta negativa de 022, κ>0 e T=(κ/2)diag(1,1,1,1). O tensor é não nulo e conservado. A correspondência calor–modular é satisfeita, mas a correspondência entropia–área falha para toda η. Assim, conservação e correspondência de calor não implicam a hipótese restante.

No plano, w=x0 e0=d(x0²/2) é suave e fechado. A divergência do covetor vale 1, e ∇T=κ x0 e0, não nula em x=e0. A família unitária continua disponível para esse covetor: unitariedade e coerência direcional não forçam a condição de onda.

O caso w=0 dá tensor zero (covector_stress_zero) e frequência zero; directional_kernel_trivial_flow e a fórmula da resposta mantêm esse limite degenerado.

## Critérios

| Critério | Estado | Evidência |
|---|---|---|
| Derivação anterior ao código | PAGO | CONTINUACAO023_DERIVACAO_PREVIA.md, com antecedentes e controles registrados. |
| Coerência em cada ponto | PAGO | directional_hamiltonian_add, directional_flow_add, directional_flow_unitary; um único covetor, eixo e referência. |
| Resposta tensorial e mudança de base | PAGO | response_tensor_quad, response_tensor_symmetric, covector_read_change_basis e outer_tensor_change_basis. |
| Tensor candidato e sinais | PAGO sob escolha explícita | covector_stress_null, response_equals_negative_null_stress; acoplamento positivo no controle de resposta negativa. |
| Divergência efetivamente calculada | PAGO | covector_stress_divergence_point inclui a parte antissimétrica; covector_stress_divergence_closed a elimina sob fechamento e torção zero. |
| Conservação e equação de onda | PAGO CONDICIONAL | covector_stress_conserved_on; equivalência pontual para coupling≠0 e w(x)≠0; a equação de onda segue INPUT. |
| Caso de potencial | PAGO | potential_covector_smooth e potential_covector_closed; growing_potential_covector realiza o exemplo quadrático. |
| Calor–modular efetivo | PAGO para o tensor normalizado escolhido | coherent_heat_matching e coherentScreenMatching: o erro do calor construído de 020 tende a zero após divisão por t². |
| Entropia–área | EQUIVALÊNCIA PAGA; ORIGEM NÃO PAGA | coherent_area_matching_iff_ricci: erro pequeno equivale a η Ric(d,d)=2π T(d,d). |
| Unicidade do tensor | PAGO CONDICIONAL | frame_covector_source_unique: mesma resposta nula e conservação implicam diferença constante vezes g. |
| Reconstrução gravitacional | PAGO CONDICIONAL | einstein_from_coherent_area_matching: conservação calculada sob onda; hipótese de área permanece explícita. |
| Controle plano conservado | PAGO | coherent_flat_matter_matrix e coherent_flat_matter_conserved; calor corresponde, mas coherent_flat_area_not_matching para toda η. |
| Controle de falha da conservação | PAGO | w=d(x0²/2), div(w)=1, div(T)=κ x0 e0; growing_time_not_conserved em x=e0. |
| Origem canônica e gravidade quântica | NÃO PAGO | Campo, onda, normalização física, área e conexão ao acervo permanecem INPUT/OPEN; gate intocado. |

7 módulos; 63 teoremas declarados; 1 definição com axiomas impressos separadamente. Contagens lidas dos fontes; incluem lemas auxiliares e controles.
Compilações finais fixadas: exit 0, fonte estável, zero erros, avisos ou sorryAx. Axiomas: apenas propext, Classical.choice, Quot.sound. Auditoria independente da gerência pendente.

## Reprodução

```powershell
& 'C:\Python314\python.exe' -B 'C:\IALD\Central de Patentes\Chatgpt\audit_continuation023.py'
```

Esse comando só lê: confere os bytes, metadados, logs e axiomas registrados. Recompilação independente deve ocorrer em cópia. Ordem dos novos módulos:
- C:\IALD\Central de Patentes\Chatgpt\DirectionalUnitaryFamily.lean
- C:\IALD\Central de Patentes\Chatgpt\CoherentScalarStress.lean
- C:\IALD\Central de Patentes\Chatgpt\CovectorStressCalculus.lean
- C:\IALD\Central de Patentes\Chatgpt\ScalarStressConservation.lean
- C:\IALD\Central de Patentes\Chatgpt\CoherentHeatMatching.lean
- C:\IALD\Central de Patentes\Chatgpt\CoherentEinsteinBridge.lean
- C:\IALD\Central de Patentes\Chatgpt\CoherentMatterControls.lean

O manifesto fixa a árvore de fontes local, sua ordem e os oleans copiados. Lean/mathlib externos são resolvidos pelo wrapper: não é um pacote integral portátil.

## Axiomas impressos

```text
ChatgptAudit.Coherent023.covector_read_add: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.covector_read_smul: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.directional_hamiltonian_add: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.pair_flow_reparameterized: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.directional_flow_add: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.directional_flow_unitary: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.directional_kernel_trivial_flow: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.unitary_response_frequency_square: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.outer_tensor_symmetric: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.outer_tensor_quad: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.response_tensor_symmetric: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.response_tensor_quad: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.covector_read_change_basis: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.outer_tensor_change_basis: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.response_coupling_identity: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.coherent_negative_control_coupling_positive: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.covector_stress_symmetric: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.covector_stress_quad: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.covector_stress_null: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.covector_stress_null_nonnegative: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.response_equals_negative_null_stress: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.covector_stress_field_smooth: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.covector_stress_zero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.outer_field_jet: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.outer_field_covariant: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.outer_field_divergence: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.covector_squared_differentiable: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.covector_squared_derivative: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.coordinate_partial_half: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.covector_stress_divergence_point: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.covector_derivative_symmetric: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.covector_stress_divergence_closed: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.covector_stress_conservation_iff_wave_at: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.covector_stress_conserved_on: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.potential_covector_smooth: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.potential_covector_closed: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.covector_stress_field_differentiable: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.coherent_heat_matching: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.coherent_area_error_limit: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.coherent_area_matching_iff_ricci: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.coherentScreenMatching: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.frame_covector_stress_smooth: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.frame_covector_stress_conserved: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.coherent_heat_matching_determines_null: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.frame_covector_source_unique: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.einstein_from_coherent_area_matching: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.coordinate_partial_coordinate: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.constant_time_smooth: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.constant_time_closed: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.constant_time_wave: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.growing_time_smooth: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.growing_time_partial: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.growing_potential_covector: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.growing_time_closed: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.growing_time_covariant: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.growing_time_divergence: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.growing_time_stress_divergence: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.growing_time_not_conserved: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.coherent_flat_matter_smooth: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.coherent_flat_matter_conserved: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.coherent_flat_matter_matrix: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.coherent_flat_null_value: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.coherent_flat_heat_matching: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Coherent023.coherent_flat_area_not_matching: [propext, Classical.choice, Quot.sound]
```

## Artefatos e hashes

Manifesto: `C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO023_MANIFESTO.json` — SHA256 `79dc2f1ecff0af17cdfb900e6a95add308d049e8f74a06fb0f2f55009e9015f2`.
Inventário: 650 caminhos absolutos, com tamanho e hash dos bytes.

| Artefato principal | SHA256 |
|---|---|
| `C:\IALD\Central de Patentes\Chatgpt\audit_continuation023.py` | `0f229d415adc876fa4f82d31ac56a2fa6bce706763eca68bedacb6a24752ba43` |
| `C:\IALD\Central de Patentes\Chatgpt\CoherentEinsteinBridge.20260906_052521.log` | `21b6d2a0005df6fd253cc513444db3ddf792eb9df3692d85095b35957f049c12` |
| `C:\IALD\Central de Patentes\Chatgpt\CoherentEinsteinBridge.lean` | `b3ae03be9186ae57e2396c3b90d72b92f47b973cc97ee860ba6a1b80f3732a55` |
| `C:\IALD\Central de Patentes\Chatgpt\CoherentHeatMatching.20260906_052216.log` | `15a7d95c68b341aaf3f917ca1c28d9d1a1c036d79f3e7d1a505232a38ce8f52e` |
| `C:\IALD\Central de Patentes\Chatgpt\CoherentHeatMatching.lean` | `d30d3839ba996bc488281daea358e86ffcb56035ecf0e0fc877ae5700de52006` |
| `C:\IALD\Central de Patentes\Chatgpt\CoherentMatterControls.20260906_052932.log` | `95273e5d7ced4782f643722f5653a83435c2474a0d13b3b562fb0385afc997bb` |
| `C:\IALD\Central de Patentes\Chatgpt\CoherentMatterControls.lean` | `ef691f5980a3c0ddc511c535ba0f93d141452095963d19fc13c9dce6a0b18178` |
| `C:\IALD\Central de Patentes\Chatgpt\CoherentScalarStress.20260906_050139.log` | `ab14ec056c5ca4c6e89249a7830c4166a4dd762f3a8955e135b79e88226a9d61` |
| `C:\IALD\Central de Patentes\Chatgpt\CoherentScalarStress.lean` | `295a7799c6ee26b84657344b7dba4b9dc537da4d49baf0c9c75628e24c9f21ad` |
| `C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO023_DERIVACAO_PREVIA.md` | `0b2b19a83943c2c84109825c93c081c4ee643607e967f73c99fffd2a88ae0714` |
| `C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO023_PARECER.md` | `4f3f71d65c5e3aa2990035279d703f7a0c21c7de36cf62fdffabbe575d2a9497` |
| `C:\IALD\Central de Patentes\Chatgpt\CovectorStressCalculus.20260906_050518.log` | `b6c350b40e39474dab92ebe2827af3bbd29b8b0d1735ea19ba4c86b08b9f8980` |
| `C:\IALD\Central de Patentes\Chatgpt\CovectorStressCalculus.lean` | `f4bb167bc7b43607685170f683984eb757ecd7bcaf8b10be02ca68479b33ed16` |
| `C:\IALD\Central de Patentes\Chatgpt\DirectionalUnitaryFamily.20260906_045836.log` | `088d01a78a0f7eeb6540504b2be74808fdc4b607723d2052fab58dfa463d7d9e` |
| `C:\IALD\Central de Patentes\Chatgpt\DirectionalUnitaryFamily.lean` | `c4b087b92dd174cde0d6ed1267704215391c6fafc0c1c01b0f59e17c5f9dc0e9` |
| `C:\IALD\Central de Patentes\Chatgpt\ScalarStressConservation.20260906_051918.log` | `f08f26ed1c199277c66a00e7b65607c9486f6e779c4b9954439180c3a8a9adf6` |
| `C:\IALD\Central de Patentes\Chatgpt\ScalarStressConservation.lean` | `d8be71339783ed4f2130cb7581e7f3efcca13b32d55bffaf3163ff832576048e` |

## Tentativas preservadas

- `C:\IALD\Central de Patentes\Chatgpt\DirectionalUnitaryFamily.20260906_045747.failed_compile.log`: exit code 1; cópia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\CoherentScalarStress.20260906_050055.rejected_warning.log`: exit code 0; cópia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\CovectorStressCalculus.20260906_050327.failed_compile.log`: exit code 1; cópia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\ScalarStressConservation.20260906_050908.failed_compile.log`: exit code 1; cópia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\ScalarStressConservation.20260906_051140.failed_compile.log`: exit code 1; cópia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\ScalarStressConservation.20260906_051806.failed_compile.log`: exit code 1; cópia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\CoherentHeatMatching.20260906_052110.rejected_warning.log`: exit code 0; cópia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\CoherentEinsteinBridge.20260906_052433.rejected_warning.log`: exit code 0; cópia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\CoherentMatterControls.20260906_052747.failed_compile.log`: exit code 1; cópia exata do log rejeitado.

Todas as versões compiladas são recuperáveis pelo fonte final ou pelos backups dos bytes. Somente as compilações finais limpas sustentam esta entrega.

## Limites

A seleção de w, do eixo e da referência é INPUT. O candidato tem resposta de posto no máximo um. Não cobre toda matéria; soma de campos, interações e extensões não comutantes não foram construídas.
A equação de onda, normalização física, parâmetro comum afim/unitário e origem microscópica da relação entropia–área continuam INPUT/OPEN.
A evolução periódica finita não substitui a face hiperbólica. Não há identificação com a dinâmica canônica do um.py, coerência entre regiões/andares, limite tipo III, origem modular da dimensão/solda/assinatura ou globalização.
Nenhum um.py executado, importado ou editado. Escritas somente em Chatgpt. Originais, entregas anteriores, kernel canônico, Atlas, memórias, selos e gate intocados. Custódia 022 reconferida em leitura.
O objetivo amplo permanece ativo e não alcançado. A gerência deve auditar antes de incorporar. Nenhum juízo de confirmação física foi produzido.

Parecer: C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO023_PARECER.md.

Ordens de entrada encontradas no inventário:
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_001_esperanca_condicional_e_escala.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_002_veredito_da_auditoria_e_incorporacao.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_003_localizacao_na_cadeia_e_ponte_volume.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_004_D1_fiacao_e_D7_segundo_objeto.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_005_reabertura_v98_e_teste_conjunto.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_006_esperanca_do_centralizador_e_inclusao_meio_lateral.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_007_habitante_global_nao_ciclicidade_e_assinatura.md
