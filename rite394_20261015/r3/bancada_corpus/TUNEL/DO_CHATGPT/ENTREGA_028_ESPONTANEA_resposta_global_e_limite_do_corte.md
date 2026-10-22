[REAL / INPUT / OPEN] ENTREGA 028 ESPONTANEA — resposta global finita, limite conjunto e obstrucao termodinamica.

06/09/2026. Continuacao do objetivo associado a ordem 007. A entrega 027 foi reconferida e classificada como PROGRESSO. O objetivo amplo permanece aberto.

O perfil harmonico da 026 fornece um contraexemplo exato: afinidade infinita positiva, estado fiel e equivalencia unitaria no Hilbert original coexistem com incrementos modular e de entropia que divergem a +infinito quando o corte cresce. Sua entropia relativa de prefixo, em contraste, converge a um real finito. Existencia e equivalencia da representacao nao bastam para uma resposta termodinamica finita.

A construcao positiva usa P_n=1/3, amplitudes 0<=b_n<=1/12 com soma B finita e Q_t(n)=1/3-b_n*h(t), h(t)=t^2/(1+t^2). Para todo t ha um estado fiel no H(P) original, com essas marginais, e a unitaria da 027. Pesos, entropias de prefixo e expectativas do gerador local sao explicitamente lidos dos estados.

Foram provados os limites de corte K(t)=-log(2)*B*h(t), D(t)=lim D_N(t) e S(t)=lim[S(Q_t,N)-S(P,N)]=K(t)-D(t), com 0<=D(t)<=9/2*h(t)^2*sum b_n^2. S e limite das diferencas, sem subtrair infinitos.

Ao reparametrizar por frequency*t, K/t^2 e S/t^2 tendem a -frequency^2*log(2)*B; D/t^2 tende a zero. A mesma resposta vale no LIMITE CONJUNTO, para qualquer corte que tenda a infinito e tempo que tenda a zero fora de zero, sem relacao imposta entre as velocidades. A cota do resto e uniforme em todo corte.

O coeficiente kappa=log(2)*B/pi liga essa resposta finita ao tensor covetor anterior. O casamento do calor e provado. O defeito de area tem coeficiente -frequency^2*log(2)*B+eta*Ric(d,d)/2. Sua anulacao continua equivalente ao balanco nulo de Ricci; sob essa hipotese e as demais condicoes geometricas explicitadas, segue a equacao de Einstein com Lambda constante no dominio preconexo.

Controle em infinitos sitios: b_n=(1/24)*(1/2)^n, B=1/12, sum b_n^2=1/432 e kappa=log(2)/(12*pi)>0. Todos os sitios mudam para parametro nao nulo. Amplitudes zero devolvem o estado original. No plano, a fonte nao nula e conservada e satisfaz calor, mas o casamento de area falha para todo eta.

[KNOWN] [Casini, Relative entropy and the Bekenstein bound](https://arxiv.org/abs/0804.2182) trata entropia relativa de estados reduzidos e uma formulacao do limite em espaco plano. [Jacobson, Entanglement Equilibrium and the Einstein Equation](https://arxiv.org/abs/1505.04753) relaciona Einstein a uma hipotese de equilibrio, com alcance e condicoes proprios. Nenhum desses resultados e importado como axioma desta formalizacao.

[OPEN] O limite diagonal especificado nao foi identificado ao funcional de Araki completo. A curva e o acoplamento sao escolhas explicitas, e a origem microscopica da correspondencia de area permanece aberta. Finitude da resposta global nao prova H3.

## Criterios

| Criterio | Estado | Evidencia |
|---|---|---|
| Derivacao anterior ao codigo | PAGO | CONTINUACAO028_DERIVACAO_PREVIA.md; auditoria 027 reconferida. |
| Cotas e produtos de entropia relativa | PAGO | diagonal_relative_nonnegative, diagonal_relative_upper, relative_entropy_product e third_binary_relative_bound. |
| Valores efetivos de prefixo | PAGO | prefix_relative_sum, prefix_modular_sum e prefix_entropy_identity. |
| Contraexemplo harmonico | PAGO | harmonic_relative_limit, harmonic_modular_diverges, harmonic_entropy_diverges e finite_relative_not_finite_entropy. |
| Familia global fiel | PAGO | amplitudeProfile, amplitude_profile_affinity_positive, amplitudeState, amplitude_state_faithful e amplitude_unitary_omega. |
| Leitura dos estados | PAGO | amplitude_read_weights, amplitude_read_modular_increment e amplitude_read_entropy_tendsto. |
| Resposta finita sem corte | PAGO | amplitude_modular_tendsto, amplitude_relative_tendsto e amplitude_entropy_tendsto. |
| Cota uniforme e limite conjunto | PAGO | amplitude_prefix_relative_scaled_bound, amplitude_prefix_modular_joint e amplitude_prefix_entropy_joint. |
| Calor e coeficiente de area | PAGO NO ENUNCIADO | amplitude_heat_matching e amplitude_area_matching_iff_ricci. |
| Implicacao Einstein | PAGO CONDICIONAL | einstein_from_summable_area_matching conserva harea, solda suave invertivel, covetor fechado e equacao de onda. |
| Controles exatos | PAGO | geometric_amplitude_mass, geometric_amplitude_square_mass, geometric_state_not_reference, zero_amplitude_state e geometric_flat_area_not_matching. |
| Lei de area microscopica e QG geral | NAO PAGO | A lei de area nao foi derivada da torre; o controle plano impede inferi-la apenas dos resultados obtidos. |

8 modulos; 112 teoremas; 6 definicoes com axiomas impressos separadamente. Contagens incluem auxiliares e controles.
Fontes finais: exit 0, fonte estavel, zero erros/avisos/sorryAx. Dependencias axiomaticas apenas propext, Classical.choice e Quot.sound. Auditoria independente da gerencia pendente.

## Reproducao

```powershell
& 'C:\Python314\python.exe' -B 'C:\IALD\Central de Patentes\Chatgpt\audit_continuation028.py'
```

O comando so le os artefatos e verifica a custodia. Recompilacao independente deve ocorrer em copia. Ordem dos novos modulos:
- C:\IALD\Central de Patentes\Chatgpt\RelativeEntropyProductBounds.lean
- C:\IALD\Central de Patentes\Chatgpt\ProfileEntropyLimits.lean
- C:\IALD\Central de Patentes\Chatgpt\HarmonicEnergyObstruction.lean
- C:\IALD\Central de Patentes\Chatgpt\SummableProfileCurve.lean
- C:\IALD\Central de Patentes\Chatgpt\SummableStateThermodynamics.lean
- C:\IALD\Central de Patentes\Chatgpt\UniformQuadraticResponse.lean
- C:\IALD\Central de Patentes\Chatgpt\SummableGravityBridge.lean
- C:\IALD\Central de Patentes\Chatgpt\SummableGravityControls.lean

Dependencias locais e sua ordem estao fixadas no manifesto; Lean/mathlib externos sao resolvidos pelo wrapper. Nao e um pacote integral portatil.

## Axiomas

```text
ChatgptAudit.Response028.relative_atom_lower: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.relative_atom_upper: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.diagonal_relative_nonnegative: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.diagonal_relative_upper: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.modular_increment_energy: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.reference_energy_product: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.modular_increment_product: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.relative_entropy_product: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.third_binary_modular_increment: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.third_binary_relative_bound: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.site_relative_nonnegative: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.prefix_relative_nonnegative: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.prefix_relative_succ: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.prefix_relative_sum: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.prefix_modular_succ: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.prefix_modular_sum: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.prefix_entropy_identity: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.prefix_relative_tendsto: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.prefix_relative_le_total: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.profile_relative_total_nonnegative: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.third_relative_sites_summable: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.third_relative_total_bound: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.third_prefix_modular_formula: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.third_prefix_modular_tendsto: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.prefix_entropy_tendsto: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.harmonic_shift_square_summable: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.harmonic_relative_summable: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.harmonic_relative_limit: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.harmonic_shift_diverges: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.harmonic_modular_diverges: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.harmonic_entropy_diverges: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.harmonic_modular_no_finite_limit: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.harmonic_entropy_no_finite_limit: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.positive_affinity_not_finite_modular: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.finite_relative_not_finite_entropy: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_square_summable: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_mass_nonnegative: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_square_mass_nonnegative: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_prefix_le_mass: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_square_prefix_le_mass: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_prefix_tendsto: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.regular_parameter_nonnegative: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.regular_parameter_lt_one: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.regular_parameter_le_square: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.regular_parameter_zero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.regular_parameter_positive: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitudeProfile: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_profile_deviation: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_profile_square_summable: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_profile_affinity_positive: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitudeVector: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitudeState: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitudeUnitary: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_vector_norm: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_state_local: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_state_faithful: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_unitary_omega: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_read_weights: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_read_entropy: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_state_generator: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.reference_state_generator: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_read_modular_increment: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_deviation_summable: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_relative_summable: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_prefix_modular_formula: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_modular_tendsto: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_relative_tendsto: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_entropy_tendsto: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_relative_nonnegative: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_relative_bound: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_prefix_relative_bound: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_modular_zero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_relative_zero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_entropy_zero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_read_entropy_tendsto: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.regular_parameter_ratio: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_relative_scaled_bound: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_prefix_relative_scaled_bound: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.regular_parameter_ratio_along: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.quadratic_error_bound_tendsto: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_relative_quadratic_along: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_prefix_relative_quadratic_along: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_modular_quadratic_along: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_entropy_quadratic_along: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_prefix_modular_joint: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_prefix_entropy_joint: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.past_time_nonzero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_modular_quadratic_limit: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_relative_quadratic_limit: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_entropy_quadratic_limit: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_coupling_nonnegative: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_response_null_stress: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_heat_defect_limit: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_heat_matching: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_area_defect_limit: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_area_matching_iff_ricci: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_balance_from_matching: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.einstein_from_summable_area_matching: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.geometricAmplitude: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.zeroAmplitude: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.geometric_amplitude_positive: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.geometric_amplitude_mass: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.geometric_amplitude_square_mass: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.geometric_coupling: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.geometric_coupling_positive: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.geometric_profile_changes_every_site: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.geometric_state_not_reference: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.geometric_joint_entropy: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.site_profiles_eq_of_weights: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.zero_amplitude_profile: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.zero_amplitude_state: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.zero_amplitude_response: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.zero_amplitude_entropy: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_flat_matter_smooth: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_flat_matter_conserved: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_flat_null_value: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.amplitude_flat_heat_matching: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Response028.geometric_flat_area_not_matching: [propext, Classical.choice, Quot.sound]
```

## Artefatos e hashes

Manifesto: `C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO028_MANIFESTO.json` - SHA256 `d1075e45c2788d3bbc2313c8c17fef699118725c7c2ca28153f2ff7147d82fcc`.
Inventario: 730 caminhos absolutos, com tamanho e SHA256 dos bytes.

| Artefato principal | SHA256 |
|---|---|
| `C:\IALD\Central de Patentes\Chatgpt\audit_continuation028.py` | `43223a54a127801a7b8041e4a73cf0337e41ba2a5a965d5bffeb895e9bba1ed7` |
| `C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO028_DERIVACAO_PREVIA.md` | `dc3315e6df748154a01af56e621b3da519add2f2323178dc629b0e0bcae29bc1` |
| `C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO028_PARECER.md` | `57dfda184a679818f22b20a1baacadd2439f9f4eb381ce4089a3c24c72ea291e` |
| `C:\IALD\Central de Patentes\Chatgpt\HarmonicEnergyObstruction.20260906_083234.log` | `b337f4b16cd4ee18f6ab342df8da9f1156c05e306c2b3c42443146779d6f1118` |
| `C:\IALD\Central de Patentes\Chatgpt\HarmonicEnergyObstruction.lean` | `4e12abce41311401e28a4ba2f3447356fb8a3dcfaaf809c1ce58eb78e459c9db` |
| `C:\IALD\Central de Patentes\Chatgpt\ProfileEntropyLimits.20260906_083013.log` | `0fa5c45b524c4faeacab072473e3079cd48d21967ece4a52d01d3dfadd4bb884` |
| `C:\IALD\Central de Patentes\Chatgpt\ProfileEntropyLimits.lean` | `6a032eb7dba9896579f2439c7accf4bb3f9d5909af639c3f87412a8c8f4e30b8` |
| `C:\IALD\Central de Patentes\Chatgpt\RelativeEntropyProductBounds.20260906_082517.log` | `b2462f714d458c181b3ce3a83edf9e8448b2aee52f6509550a4493aa52786f84` |
| `C:\IALD\Central de Patentes\Chatgpt\RelativeEntropyProductBounds.lean` | `8c1b1f506536c20f34547d3ce08c687c333f52688ccab79d22adadfcfc843c52` |
| `C:\IALD\Central de Patentes\Chatgpt\SummableGravityBridge.20260906_084610.log` | `7a29585f0b900eb7a0c00eeb5ec37d946bb88a87357709b99a3c3ebba764ebbc` |
| `C:\IALD\Central de Patentes\Chatgpt\SummableGravityBridge.lean` | `7df241c5485960ddecf1633b366a432ddc2f264d5421336e315ab4998f9ec07e` |
| `C:\IALD\Central de Patentes\Chatgpt\SummableGravityControls.20260906_084932.log` | `fa7e3cbc8b8ec5699d76ed118fa0211cc372c860cf8dcea494e188ce41cbc9dd` |
| `C:\IALD\Central de Patentes\Chatgpt\SummableGravityControls.lean` | `787151dbb68fd3011043e342ad1337ae8a721c0a830c5d72122ec7a3d9032468` |
| `C:\IALD\Central de Patentes\Chatgpt\SummableProfileCurve.20260906_083412.log` | `87b9f6186789e0de1dee794d141c0e41c994750acb24ad550654e4d4798f8b8b` |
| `C:\IALD\Central de Patentes\Chatgpt\SummableProfileCurve.lean` | `2385597f86a806b733f54d33721f339f3805253d111dbcd5968434cb256e1e35` |
| `C:\IALD\Central de Patentes\Chatgpt\SummableStateThermodynamics.20260906_083655.log` | `c8af9b4bedb1bbca03acdc8a090b098e9837c3507c0c9a640c87fb42b23a5ec3` |
| `C:\IALD\Central de Patentes\Chatgpt\SummableStateThermodynamics.lean` | `f5ae98640c3567a3a1c4fe6f217fcefd4804c9cbb7de1951e154207cb3709a7d` |
| `C:\IALD\Central de Patentes\Chatgpt\UniformQuadraticResponse.20260906_084100.log` | `080855bbc016d6460eb7cb45531960f5a6bc89841d4b4dbab036b4b56cf6ee2e` |
| `C:\IALD\Central de Patentes\Chatgpt\UniformQuadraticResponse.lean` | `e1b918e45b7aad4f0d29f9432ebdef89e9ab83cbc7b42e361ff043cbd8cd6e03` |

## Tentativas preservadas

- `C:\IALD\Central de Patentes\Chatgpt\RelativeEntropyProductBounds.20260906_082406.failed_compile.log`: exit 1; copia exata do registro rejeitado (saida do compilador).
- `C:\IALD\Central de Patentes\Chatgpt\ProfileEntropyLimits.20260906_082648.failed_compile.log`: exit 1; copia exata do registro rejeitado (saida do compilador).
- `C:\IALD\Central de Patentes\Chatgpt\ProfileEntropyLimits.20260906_082848.failed_compile.log`: exit 1; copia exata do registro rejeitado (saida do compilador).
- `C:\IALD\Central de Patentes\Chatgpt\UniformQuadraticResponse.20260906_083911.failed_compile.log`: exit 1; copia exata do registro rejeitado (saida do compilador).
- `C:\IALD\Central de Patentes\Chatgpt\SummableGravityBridge.20260906_084322.failed_compile.log`: exit 1; copia exata do registro rejeitado (saida do compilador).
- `C:\IALD\Central de Patentes\Chatgpt\SummableGravityControls.20260906_084654.failed_compile.log`: exit 1; copia exata do registro rejeitado (saida do compilador).

6 tentativas rejeitadas preservadas, incluindo eventual interrupcao explicitamente rotulada como nota da bancada. Fontes compilados recuperaveis pelos arquivos finais e backups dos bytes. Somente as compilacoes finais limpas sustentam esta entrega.

## Dividas

- A referencia escolhida e o perfil produto binario constante (1/3,2/3). As amplitudes b_n sao INPUT: nao negativas, no maximo 1/12 e somaveis. A escolha fisica desse perfil ou dessas amplitudes nao foi derivada.
- Q_t.w(n)=1/3-b_n*t^2/(1+t^2) e uma curva escolhida matematicamente. Os estados fieis e suas marginais foram construidos; nao se postulou a lei de area na definicao da curva.
- A entropia relativa global desta entrega e o limite das entropias relativas diagonais nos prefixos especificados. Sua identificacao com a entropia relativa de Araki completa nao foi formalizada.
- S(t) e o limite das DIFERENCAS de entropias finitas, nao a subtracao de duas entropias infinitas tratadas como reais. K_N=-log(rho_N) e um observavel local; nao foi identificado a -log(Delta) global.
- A regularidade demonstrada para a resposta e o limite quadratico, inclusive conjunto em corte e tempo. Nao se afirma derivada segunda em norma do vetor global ou continuidade em norma de toda a familia U(t).
- A fidelidade e o transporte modular de cada estado reutilizam 026-027. A continuidade de estado formalizada anteriormente e sequencial WOT; nao se declara aqui um predual geral.
- A fonte e do tipo covetor escalar, com acoplamento escolhido para o casamento do calor. Nao classifica toda materia quantica nem deriva a equacao de onda ou o perfil de uma dinamica fisica.
- A area geometrica e calculada independentemente; sua correspondencia com S(t) continua HIPOTESE, equivalentemente o balanco nulo de Ricci. O controle plano mostra que a finitude global e o casamento do calor nao a implicam.
- Regiao-algebra, correlacoes fisicas, dimensao, assinatura, solda, temperatura, unidades e origem microscopica da lei de area permanecem antecedentes ou lacunas. H3 e a reconstrucao gravitacional geral continuam abertas.
- O objetivo amplo de gravidade quantica nao foi alcancado. Nenhum original, gate, selo canonico, memoria ou conclusao observacional foi alterado.

Originais, um.py, kernel canonico, Atlas, memorias, diarios, gate e entregas anteriores intocados. Nenhuma confirmacao fisica e declarada. O objetivo amplo permanece ativo e nao alcancado. Gerencia audita antes de incorporar.

Parecer: C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO028_PARECER.md.

Ordens encontradas:
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_001_esperanca_condicional_e_escala.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_002_veredito_da_auditoria_e_incorporacao.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_003_localizacao_na_cadeia_e_ponte_volume.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_004_D1_fiacao_e_D7_segundo_objeto.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_005_reabertura_v98_e_teste_conjunto.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_006_esperanca_do_centralizador_e_inclusao_meio_lateral.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_007_habitante_global_nao_ciclicidade_e_assinatura.md
