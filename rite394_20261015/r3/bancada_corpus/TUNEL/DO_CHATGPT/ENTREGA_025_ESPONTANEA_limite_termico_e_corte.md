[REAL / INPUT / OPEN] ENTREGA 025 ESPONTANEA - perfil termico global, obstrucao ao limite em norma da preparacao e escala da resposta.

06/09/2026. A etapa 024 foi reconferida e classificada como PROGRESSO. Continuacao do objetivo amplo associado a ordem 007; nao e uma nova ordem gerencial.

Gibbs respeita o produto: r_(p tensor q)(s)=r_p(s) tensor r_q(s). A variancia do gerador local soma. O perfil P_s com pesos de sitio inclinados e construido como SiteProfile e satisfaz towerW(P_s,N)=r_(towerW(P,N))(s) para todo N.

O estado canonico do perfil P_s realiza todas as marginais na sua propria representacao H(P_s). Os estados vetoriais de 024, todos em H(P), tambem sao exatamente compativeis nos observaveis de cada andar fixo quando o corte da preparacao cresce. Estas duas afirmacoes nao identificam as representacoes completas.

A afinidade c(p,r)=sum sqrt(p_i)sqrt(r_i) pertence a (0,1] para pesos positivos normalizados, e vale um exatamente quando p=r. Para Gibbs nao tracial e s diferente de zero, c<1. Em perfil constante, <Omega,Psi_N>=c^(N+1) e ||Psi_N-Psi_(N+1)||^2=2(1-c). Logo a sequencia de vetores da preparacao NAO e Cauchy e nao tem limite em norma em H(P).

Este negativo e sobre a sequencia especifica. Nao equivale, sozinho, a um teorema de disjuncao, inexistencia de outro vetor, ou nao normalidade de toda realizacao com essas marginais. Referencia primaria de contexto: [Promislow, The Kakutani theorem for tensor products of W*-algebras](https://msp.org/pjm/1971/36-2/pjm-v36-n2-p20-s.pdf), que trata produtos infinitos e estados normais com hipoteses e metricas proprias. O teorema geral desse artigo nao foi importado como axioma nem formalizado aqui.

Para perfil constante nao tracial, V_N=(N+1)V_site e kappa_N=V_N/pi cresce sem limite. Escolhendo frequencia_N=frequencia/sqrt(N+1), o coeficiente de DeltaS/t^2 e DeltaK/t^2 passa a -frequencia^2 V_site para todo N; D/t^2 tende a zero. Esta normalizacao e INPUT.

Para t fixo, s_N=(frequencia*t)^2/(N+1) tende a zero. Em TODO andar observado fixo, o estado reescalado retorna ao estado original. A resposta extensiva nao e apresentada como uma variacao local nao trivial sobrevivente. Os limites temporais sao provados para cada N; nao foi provada permutacao dos limites.

O tensor usa kappa_site=V_site/pi. A correspondencia do calor temporal efetivo e provada com a familia reescalada, mas area continua equivalente a eta Ric(d,d)=2 pi T(d,d). No espaco plano, o tensor e conservado, o calor corresponde e a area falha para todo N e toda eta quando V_site>0. A nova escala nao produz H3.

## Criterios

| Criterio | Estado | Evidencia |
|---|---|---|
| Derivacao anterior ao codigo | PAGO | CONTINUACAO025_DERIVACAO_PREVIA.md registra as distincoes e os limites pretendidos. |
| Fatoracao de Gibbs | PAGO | gibbs_partition_product, gibbs_weights_product e gibbs_mean_product. |
| Variancia e corte | PAGO | modular_variance_product, tower_variance_sum, tower_variance_uniform, tower_coupling_unbounded. |
| Perfil global construido | PAGO NO TIPO DECLARADO | thermalProfile e thermal_profile_tower_weights; representacao H(P_s), nao identificacao com H(P). |
| Compatibilidade dos andares | PAGO | thermal_global_local_state, thermal_tower_marginal e thermal_tower_marginal_weights. |
| Afinidade exata | PAGO | hellinger_sum_identity, diagonal_affinity_eq_one_iff, gibbs_fixed_iff_tracial e gibbs_affinity_product. |
| Limite em H original | NEGATIVO PAGO | thermal_vectors_no_norm_limit e thermal_vectors_not_cauchy, para perfil constante nao tracial e s diferente de zero. |
| Resposta com escala escolhida | PAGO CONDICIONAL | cutoff_response_equals_site e cutoff_modular_limit/cutoff_entropy_limit/cutoff_relative_entropy_limit. |
| Estado local no limite do corte | PAGO | cutoff_local_state_returns_reference, para todo observavel local fixo; nao se afirma troca dos limites. |
| Calor e area | CALOR PAGO; AREA CONDICIONAL | cutoff_heat_matching e cutoff_area_matching_iff_ricci para o acoplamento por sitio. |
| Controles | PAGO | half_thermal_vectors_fixed, half_thermal_variance_zero; third_thermal_vectors_not_cauchy; cutoff_flat_area_not_matching. |
| Normalidade/disjuncao e objetivo amplo | NAO PAGO | O alcance novo e medido sem promover nao-Cauchy a teorema geral de disjuncao; H3 e demais antecedentes continuam abertos. |

7 modulos; 72 teoremas; 1 definicoes com axiomas impressos separadamente. Contagens incluem auxiliares e controles.
Fontes finais: exit 0, fonte estavel, zero erros/avisos/sorryAx. Dependencias axiomaticas apenas propext, Classical.choice e Quot.sound. Auditoria independente da gerencia pendente.

## Reproducao

```powershell
& 'C:\Python314\python.exe' -B 'C:\IALD\Central de Patentes\Chatgpt\audit_continuation025.py'
```

O comando so le os artefatos e verifica a custodia. Recompilacao independente deve ocorrer em copia. Ordem dos novos modulos:
- C:\IALD\Central de Patentes\Chatgpt\GibbsProductLaw.lean
- C:\IALD\Central de Patentes\Chatgpt\GibbsProductVariance.lean
- C:\IALD\Central de Patentes\Chatgpt\TowerThermalProfile.lean
- C:\IALD\Central de Patentes\Chatgpt\GibbsAffinity.lean
- C:\IALD\Central de Patentes\Chatgpt\TowerThermalOverlap.lean
- C:\IALD\Central de Patentes\Chatgpt\ThermalCutoffResponse.lean
- C:\IALD\Central de Patentes\Chatgpt\ThermalLimitControls.lean

Dependencias locais e sua ordem estao fixadas no manifesto; Lean/mathlib externos sao resolvidos pelo wrapper. Nao e um pacote integral portatil.

## Axiomas

```text
ChatgptAudit.Thermal025.modular_score_product: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.gibbs_atom_product: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.gibbs_partition_product: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.gibbs_weights_product: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.product_expectation_add: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.gibbs_product_entropy: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.gibbs_mean_product: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.modular_mean_product: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.product_second_moment: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.modular_variance_product: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.tower_variance_zero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.tower_variance_succ: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.tower_variance_sum: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.tower_variance_uniform: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.thermalProfile: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.thermal_profile_site: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.thermal_profile_zero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.thermal_profile_tower_weights: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.thermal_global_local_state: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.thermal_tower_marginal: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.thermal_tower_marginal_weights: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.thermal_global_state_faithful: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.thermal_profile_uniform: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.thermal_tower_entropy_uniform: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.diagonal_affinity_self: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.hellinger_sum_identity: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.diagonal_affinity_le_one: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.diagonal_affinity_eq_one_iff: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.diagonal_affinity_product: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.weighted_sqrt_ratio: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.diagonal_affinity_positive: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.gibbs_fixed_iff_tracial: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.gibbs_affinity_positive: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.gibbs_affinity_lt_one: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.gibbs_filter_affinity: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.gibbs_affinity_product: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.gibbs_amplitude_product: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.tower_gibbs_omega_overlap: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.tower_gibbs_affinity_uniform: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.tower_gibbs_uniform_overlap: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.tower_step_diagonal: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.tower_local_vectors_inner: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.tower_gibbs_successive_overlap: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.tower_gibbs_successive_distance: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.nontracial_site_affinity_lt_one: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.thermal_uniform_overlap_tends_zero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.thermal_vectors_no_norm_limit: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.thermal_vectors_not_cauchy: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.cutoff_size_positive: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.cutoff_frequency_square: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.cutoff_parameter_matches: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.cutoff_size_tends_infinity: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.cutoff_parameter_tends_zero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.tower_coupling_uniform: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.stationary_site_variance_positive: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.tower_coupling_unbounded: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.cutoff_response_equals_site: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.cutoff_modular_limit: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.cutoff_entropy_limit: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.cutoff_relative_entropy_limit: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.cutoff_state_entropy_limit: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.thermal_local_state_continuous: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.cutoff_local_state_returns_reference: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.half_site_equal: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.half_gibbs_affinity: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.half_thermal_vectors_fixed: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.half_thermal_variance_zero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.third_thermal_vectors_not_cauchy: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.third_thermal_coupling_unbounded: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.cutoff_heat_matching: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.cutoff_area_matching_iff_ricci: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.cutoff_flat_heat_matching: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Thermal025.cutoff_flat_area_not_matching: [propext, Classical.choice, Quot.sound]
```

## Artefatos e hashes

Manifesto: `C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO025_MANIFESTO.json` - SHA256 `d4a1cde5b10465a83cf6582213db5d054c17cb651da0be4af63ad7ce52379012`.
Inventario: 675 caminhos absolutos, com tamanho e SHA256 dos bytes.

| Artefato principal | SHA256 |
|---|---|
| `C:\IALD\Central de Patentes\Chatgpt\audit_continuation025.py` | `89a3032df502ce98896a9dac4bc4accdba3afcbb84114ab3ac6cae763a208a4b` |
| `C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO025_DERIVACAO_PREVIA.md` | `4cd5631ea07c9d663355a5752035cd7604cd38018fcd8c54c6fada14bd36bce9` |
| `C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO025_PARECER.md` | `31b27a3f9426d73324766695b001e2da11932a466e62e29ea351709e8ea0fc7f` |
| `C:\IALD\Central de Patentes\Chatgpt\GibbsAffinity.20260906_063550.log` | `90519d1df0c8863ee611ae3d9e84d2636ab0621ce54cd85106239842a1e9eacf` |
| `C:\IALD\Central de Patentes\Chatgpt\GibbsAffinity.lean` | `4e31278c63aaf9234c5c6fd354c1589be2a9c9923a07b1a5046e1b0c244fb2e9` |
| `C:\IALD\Central de Patentes\Chatgpt\GibbsProductLaw.20260906_062230.log` | `68a2c99e0dffb2d76456c9217d4a9c1d81958d7411443e033190231c5939e279` |
| `C:\IALD\Central de Patentes\Chatgpt\GibbsProductLaw.lean` | `e87bb861c6d10a01ab9304434bc2908b52aae9d64ceaac98aabac2c89e898f30` |
| `C:\IALD\Central de Patentes\Chatgpt\GibbsProductVariance.20260906_062758.log` | `f70c6e1a0c48f95040ffe8b52618b4d27899c9a90bac52f41720ae6c6a017af5` |
| `C:\IALD\Central de Patentes\Chatgpt\GibbsProductVariance.lean` | `b94299b376face46ab394780e9e3c9111bdc82cd2eddc82f1adb5087053c78ee` |
| `C:\IALD\Central de Patentes\Chatgpt\ThermalCutoffResponse.20260906_064537.log` | `ae14f47b06a4a4d4cac8568bd6af19630f65bf2bd7b41a776e5ae68a88cb59eb` |
| `C:\IALD\Central de Patentes\Chatgpt\ThermalCutoffResponse.lean` | `26da3b76d4714c0787967de95026350d84e095bff9b2412a07abe3ea500f9fe9` |
| `C:\IALD\Central de Patentes\Chatgpt\ThermalLimitControls.20260906_064633.log` | `2da2a865c97e7ea83aa4b0e8410e7d91f20ba5c49577075ec799865ff716890e` |
| `C:\IALD\Central de Patentes\Chatgpt\ThermalLimitControls.lean` | `efb0a4ad954ced66afaea0bc68d96ec0c67b29e6df81dd829bf6b8f1460a76bd` |
| `C:\IALD\Central de Patentes\Chatgpt\TowerThermalOverlap.20260906_064259.log` | `5237ef80c8d356a874c7921d32434e62e96ec55e525ddf86d85f4d0d74449903` |
| `C:\IALD\Central de Patentes\Chatgpt\TowerThermalOverlap.lean` | `4f5f9f06cea199b7770d2a3c0f225c9bb127544714c18a7d6e9a8e8ea6c48ec3` |
| `C:\IALD\Central de Patentes\Chatgpt\TowerThermalProfile.20260906_063156.log` | `3cdf7f14ee6360fdc9ea1558162168d336f4a166710c51f0e2c4c7d9dd0d285f` |
| `C:\IALD\Central de Patentes\Chatgpt\TowerThermalProfile.lean` | `1cad20d554253860b115ed871c9eaa5e14136df400c8ce0fecdab3b16f1c2739` |

## Tentativas preservadas

- `C:\IALD\Central de Patentes\Chatgpt\GibbsProductLaw.20260906_062030.failed_compile.log`: exit 1; copia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\GibbsProductVariance.20260906_062354.failed_compile.log`: exit 1; copia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\TowerThermalProfile.20260906_062959.failed_compile.log`: exit 1; copia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\GibbsAffinity.20260906_063359.failed_compile.log`: exit 1; copia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\TowerThermalOverlap.20260906_063831.failed_compile.log`: exit 1; copia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\TowerThermalOverlap.20260906_064144.failed_compile.log`: exit 1; copia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\ThermalCutoffResponse.20260906_064401.failed_compile.log`: exit 1; copia exata do log rejeitado.

7 tentativas rejeitadas preservadas. Fontes compilados recuperaveis pelos arquivos finais e backups dos bytes. Somente as compilacoes finais limpas sustentam esta entrega.

## Dividas

- O estado de referencia e produto. A formula linear de variancia e o negativo uniforme usam perfil constante nao tracial; nao se estendem automaticamente a perfis gerais ou estados correlacionados.
- A representacao global construida e H(P_s). Nao foi provada identificacao com H(P), nem o teorema geral de normalidade, quase-equivalencia ou disjuncao de produtos infinitos.
- O negativo em H(P) refere-se a sequencia especifica de vetores preparados em 024. Afinidade com Omega tendendo a zero nao prova, isoladamente, convergencia fraca a zero ou inexistencia de outro vetor com dadas marginais.
- A escala por sqrt(N+1) e escolha explicita. O limite temporal de segunda ordem e tomado para cada N; nao se prova troca de limites ou uniformidade em N.
- A resposta reescalada e extensiva. Todo observavel em andar fixo retorna a referencia para parametro temporal fixo; nao se declara nova dinamica local sobrevivente.
- A correspondencia entropia-area, covetor/onda, quatro dimensoes, assinatura, solda, unidades, temperatura e coeficiente de Newton continuam antecedentes ou lacunas.
- O objetivo amplo de gravidade quantica e a reconstrucao global permanecem abertos. Nenhum gate ou conclusao fisica foi alterado.

Originais, um.py, kernel canonico, Atlas, memorias, diarios, gate e entregas anteriores intocados. Nenhuma confirmacao fisica e declarada. O objetivo amplo permanece ativo e nao alcancado. Gerencia audita antes de incorporar.

Parecer: C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO025_PARECER.md.

Ordens encontradas:
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_001_esperanca_condicional_e_escala.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_002_veredito_da_auditoria_e_incorporacao.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_003_localizacao_na_cadeia_e_ponte_volume.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_004_D1_fiacao_e_D7_segundo_objeto.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_005_reabertura_v98_e_teste_conjunto.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_006_esperanca_do_centralizador_e_inclusao_meio_lateral.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_007_habitante_global_nao_ciclicidade_e_assinatura.md
