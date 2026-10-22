[REAL / INPUT / OPEN] ENTREGA 026 ESPONTANEA — criterio de afinidade, estado global e fidelidade no Hilbert original.

06/09/2026. A entrega 025 foi reconferida e classificada como PROGRESSO. Continuacao do objetivo amplo associado a ordem 007; nao e nova ordem gerencial.

Dados dois perfis produto positivos P,Q, F_N=diag sqrt(q_N/p_N) e Psi_N=pi_P(F_N)Omega vivem no mesmo H(P). Seus estados reproduzem exatamente as marginais Q de todo andar L menor ou igual a N.

Defina c_n=sum sqrt(p_n)sqrt(q_n), C_N=prod_{n<=N}c_n e C=lim C_N. Foram provados 0<c_n<=1, C_N positivo antitono, <Psi_L,Psi_N>=C_N/C_L e ||Psi_L-Psi_N||^2=2(1-C_N/C_L). A sequencia Psi_N e Cauchy, equivalentemente possui limite em norma, SE E SOMENTE SE C>0.

Se C>0, o vetor limite Phi tem norma um, e o estado <Phi,A Phi> e complexo-linear, positivo, normalizado, SeqWOTContinuous e reproduz todas as marginais Q no fator ORIGINAL de P. Para provar fidelidade, os filtros inversos locais aplicados a Phi convergem a Omega e coincidem com as acoes direitas correspondentes. O comutante e a separancia de Omega dao A Phi=0 => A=0. A mesma recuperacao de Omega e a densidade da torre provam que Phi tambem e ciclico.

A somabilidade de (1-c_n) e suficiente para C>0. Um limite quadratico de Hellinger da um exemplo inteiramente demonstrado: P_n=1/3 e Q_n=1/3+1/(12(n+1)). Todos os sitios mudam; as diferencas nao sao somaveis, mas seus quadrados sao. O estado global construido e fiel e diferente da referencia.

O controle estacionario P_n=1/3, Q_n=1/2 tem C=0 e nao admite limite em norma desta preparacao. Q=P tem C=1. A igualdade com a preparacao de Gibbs de 024 e tipada quando Q=thermalProfile(P,s).

[KNOWN] Afinidades e estados produtos infinitos fazem parte da teoria classica de [Promislow, The Kakutani theorem for tensor products of W*-algebras](https://msp.org/pjm/1971/36-2/pjm-v36-n2-p20-s.pdf). Esta entrega formaliza uma preparacao concreta na torre da casa. Nao importa o teorema geral como axioma nem reivindica sua descoberta.

O criterio exato concerne a sequencia especificada. Nao se provou aqui classificacao de todos os estados normais, disjuncao ou quase-equivalencia de representacoes; a continuidade formalizada e sequencial WOT. A existencia e fidelidade obtidas nao implicam H3, lei de area ou reconstrucao gravitacional geral.

## Criterios

| Criterio | Estado | Evidencia |
|---|---|---|
| Derivacao antes do codigo | PAGO | CONTINUACAO026_DERIVACAO_PREVIA.md, com auditoria 025 novamente PASS. |
| Preparacao relativa finita e marginais | PAGO | relative_filter_positive, profile_vector_norm e profile_state_marginal. |
| Produto e sobreposicao entre quaisquer andares | PAGO | profile_affinity_product, profile_vectors_overlap e profile_vectors_distance. |
| Criterio exato de limite no H original | PAGO NO ENUNCIADO | profile_vectors_cauchy_iff e profile_vectors_limit_iff; sequencia canonica especificada. |
| Somabilidade suficiente | PAGO | affinity_loss_summable_positive_limit; sem importar o teorema geral de Kakutani. |
| Estado global no H original | PAGO | globalProfileVector, global_profile_state_local, _one, _positive e _seqWOT. |
| Fidelidade e ciclicidade no fator original | PAGO | global_profile_inverse_tendsto, global_profile_right_left, global_profile_vector_separating, global_profile_state_faithful e global_profile_vector_cyclic. |
| Controle quadratico | PAGO | binary_affinity_quadratic_bound e profile_square_summable_positive. |
| Mudanca em infinitos sitios | PAGO | gradualProfile, gradual_profile_changes_every_site, _square_summable, _diff_not_summable e _affinity_positive. |
| Estado distinto e fiel | PAGO | gradual_state_not_reference, gradual_state_local e gradual_state_faithful. |
| Controles e ligacao com Gibbs | PAGO | profile_affinity_limit_self, stationary_changed_no_preparation_limit e thermal_preparation_limit_iff. |
| Classificacao de todos os estados normais e QG | NAO PAGO | O criterio nao e promovido a teorema geral de disjuncao; H3 e demais folhas continuam abertas. |

8 modulos; 83 teoremas; 2 definicoes com axiomas impressos separadamente. Contagens incluem auxiliares e controles.
Fontes finais: exit 0, fonte estavel, zero erros/avisos/sorryAx. Dependencias axiomaticas apenas propext, Classical.choice e Quot.sound. Auditoria independente da gerencia pendente.

## Reproducao

```powershell
& 'C:\Python314\python.exe' -B 'C:\IALD\Central de Patentes\Chatgpt\audit_continuation026.py'
```

O comando so le os artefatos e verifica a custodia. Recompilacao independente deve ocorrer em copia. Ordem dos novos modulos:
- C:\IALD\Central de Patentes\Chatgpt\RelativeProfilePreparation.lean
- C:\IALD\Central de Patentes\Chatgpt\ProfileOverlapFactorization.lean
- C:\IALD\Central de Patentes\Chatgpt\AffinityProducts.lean
- C:\IALD\Central de Patentes\Chatgpt\AffinityVectorCriterion.lean
- C:\IALD\Central de Patentes\Chatgpt\GlobalProfileState.lean
- C:\IALD\Central de Patentes\Chatgpt\GlobalProfileFaithfulness.lean
- C:\IALD\Central de Patentes\Chatgpt\ProfileAffinityBound.lean
- C:\IALD\Central de Patentes\Chatgpt\GlobalProfileControls.lean

Dependencias locais e sua ordem estao fixadas no manifesto; Lean/mathlib externos sao resolvidos pelo wrapper. Nao e um pacote integral portatil.

## Axiomas

```text
ChatgptAudit.Profile026.relative_filter_self_adjoint: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.relative_weighted_square: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.relative_amplitude_product: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.relative_filter_product: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.relative_filter_local_state: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.profile_state_local: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.profile_state_one: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.profile_vector_norm: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.profile_state_marginal: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.profile_omega_overlap: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.relative_filter_reverse: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.relative_filter_positive: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.site_affinity_positive: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.site_affinity_le_one: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.profile_affinity_positive: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.profile_affinity_le_one: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.profile_affinity_succ: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.profile_affinity_product: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.relative_trace: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.profile_filter_step: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.profile_trace_step: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.profile_trace_push: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.profile_filter_square_state: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.profile_vectors_overlap: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.profile_vectors_distance: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.profile_inverse_overlap: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.profile_affinity_antitone: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.profile_affinity_bddBelow: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.profile_affinity_limit_nonnegative: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.profile_affinity_limit_le: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.profile_affinity_tendsto: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.profile_affinity_ratio_tendsto: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.affinity_loss_sum_succ: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.affinity_tail_loss_bound: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.affinity_loss_summable_positive_limit: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.profile_vectors_cauchy_of_positive: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.profile_positive_of_vectors_cauchy: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.profile_vectors_cauchy_iff: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.profile_vectors_limit_iff: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.profile_zero_affinity_no_limit: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.profile_summable_has_limit: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.globalProfileVector: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.global_profile_vector_tendsto: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.global_profile_vector_norm: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.global_profile_state_limit: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.global_profile_state_local: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.global_profile_state_one: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.global_profile_state_add: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.global_profile_state_smul: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.global_profile_square_value: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.global_profile_state_positive: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.global_profile_state_seqWOT: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.global_profile_inverse_norm: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.push_diagonal_exists: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.pushed_relative_commute: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.profile_relative_right_left: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.global_profile_right_left: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.global_profile_inverse_overlap: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.global_profile_inverse_distance: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.global_profile_inverse_tendsto: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.global_profile_vector_separating: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.global_profile_state_faithful: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.sqrt_difference_square_bound: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.binary_affinity_quadratic_bound: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.binary_third_affinity_bound: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.profile_weighted_square_summable_positive: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.profile_square_summable_positive: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.global_profile_vector_cyclic: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.gradualProfile: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.gradual_profile_diff: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.gradual_profile_changes_every_site: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.gradual_profile_square_summable: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.gradual_profile_diff_not_summable: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.gradual_profile_affinity_positive: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.gradual_state_local: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.gradual_state_faithful: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.gradual_state_not_reference: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.profile_thermal_preparation: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.thermal_preparation_limit_iff: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.profile_affinity_self: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.profile_affinity_limit_self: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.profile_affinity_stationary: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.third_half_site_affinity_lt_one: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.stationary_changed_affinity_zero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.Profile026.stationary_changed_no_preparation_limit: [propext, Classical.choice, Quot.sound]
```

## Artefatos e hashes

Manifesto: `C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO026_MANIFESTO.json` - SHA256 `fca1a8a73a19aec95fb0b51fc4bf7720e4ae1a5dbf2315a08d6b2e895a0e2b74`.
Inventario: 705 caminhos absolutos, com tamanho e SHA256 dos bytes.

| Artefato principal | SHA256 |
|---|---|
| `C:\IALD\Central de Patentes\Chatgpt\AffinityProducts.20260906_071454.log` | `e542c0a31b95f8373b7be8b918ddce7ee71a2dbedb877889bba5d9d36ff589d2` |
| `C:\IALD\Central de Patentes\Chatgpt\AffinityProducts.lean` | `7c5c047bde93c760db3671c06cb6e02d4d8a5e0760dad67a91066423faf77947` |
| `C:\IALD\Central de Patentes\Chatgpt\AffinityVectorCriterion.20260906_071916.log` | `7d4ae8eebfb5ea669dc8bbe3e17a5c66a0d5ddc8573da000be2f61320b053472` |
| `C:\IALD\Central de Patentes\Chatgpt\AffinityVectorCriterion.lean` | `8d5e7a611adff81f29c40c53230afd22f6ab13813239962876fb1670ded03e90` |
| `C:\IALD\Central de Patentes\Chatgpt\audit_continuation026.py` | `8c86932a71a34e9f1855bf21e0201becce4da8bd42d4f09fffa3338f123d32c5` |
| `C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO026_DERIVACAO_PREVIA.md` | `7f66793d8dfab778b40dd2d637ba05c9761398835423b02a66450cf43715eaf7` |
| `C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO026_PARECER.md` | `367fc5df1287acd085ecb96895fd91c59f3139672f518bc40a0a06da58f1c846` |
| `C:\IALD\Central de Patentes\Chatgpt\GlobalProfileControls.20260906_072742.log` | `3655b17d951e77250216cc1e6f705fcc8ca14405e0f59fc9d9b2fbf9872f8a27` |
| `C:\IALD\Central de Patentes\Chatgpt\GlobalProfileControls.lean` | `d01d057e9d8752733b62f04f74d27a9e65d2116b8bbe49d261a96f6d68442457` |
| `C:\IALD\Central de Patentes\Chatgpt\GlobalProfileFaithfulness.20260906_072158.log` | `c6e2214ed67b35f689142667c382aae8a783233f3547097b332e24f5845ab27e` |
| `C:\IALD\Central de Patentes\Chatgpt\GlobalProfileFaithfulness.lean` | `1271727d6b0c6977c8716d392fedb7f759927c0198d3cf76912a367a63d7b343` |
| `C:\IALD\Central de Patentes\Chatgpt\GlobalProfileState.20260906_072019.log` | `02bc5f50cc558cfa27f831babb6371e3d8657e6ebaeb27829f9cfb594e643703` |
| `C:\IALD\Central de Patentes\Chatgpt\GlobalProfileState.lean` | `987f346696e7682f06b5dbea879722145f9cf95b2291c5ea53eebe1121716da9` |
| `C:\IALD\Central de Patentes\Chatgpt\ProfileAffinityBound.20260906_072435.log` | `b70b51d1c941b1fc5512ccac18129c3ea81cf9c096d56a509bd876874c48e979` |
| `C:\IALD\Central de Patentes\Chatgpt\ProfileAffinityBound.lean` | `df173fd2b3ecaec2f8c9dc4f139864399077ec200669b31f876de86fc2339e57` |
| `C:\IALD\Central de Patentes\Chatgpt\ProfileOverlapFactorization.20260906_070553.log` | `0c4a2d7197cb3e31ae1b043c2ebd8e059311a824086370b7f4d3279112442152` |
| `C:\IALD\Central de Patentes\Chatgpt\ProfileOverlapFactorization.lean` | `9d932be7a279867433f513a9285a17c6f6eb74597214fb828f4fa4e3e3e4b74e` |
| `C:\IALD\Central de Patentes\Chatgpt\RelativeProfilePreparation.20260906_070359.log` | `fc29b393bdc97f067e5a82ced1bfd9cb96b90b499e1da244291c793bb9002251` |
| `C:\IALD\Central de Patentes\Chatgpt\RelativeProfilePreparation.lean` | `aaac255a923a30b7d324c2b0ecfa45e37225175885b5c879b473bf3b21c4c18e` |

## Tentativas preservadas

- `C:\IALD\Central de Patentes\Chatgpt\RelativeProfilePreparation.20260906_070247.failed_compile.log`: exit 1; copia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\AffinityProducts.20260906_070734.failed_compile.log`: exit 1; copia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\AffinityProducts.20260906_070908.failed_compile.log`: exit 1; copia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\AffinityProducts.20260906_071050.failed_compile.log`: exit 1; copia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\AffinityProducts.20260906_071222.rejected_warning.log`: exit 0; copia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\AffinityVectorCriterion.20260906_071624.rejected_warning.log`: exit 0; copia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\ProfileAffinityBound.20260906_072320.failed_compile.log`: exit 1; copia exata do log rejeitado.
- `C:\IALD\Central de Patentes\Chatgpt\GlobalProfileControls.20260906_072614.failed_compile.log`: exit 1; copia exata do log rejeitado.

8 tentativas rejeitadas preservadas. Fontes compilados recuperaveis pelos arquivos finais e backups dos bytes. Somente as compilacoes finais limpas sustentam esta entrega.

## Dividas

- P e Q sao perfis produto estritamente positivos, fornecidos como INPUT. Nao se construiu estado correlacionado nem foi selecionado um perfil por dinamica fisica.
- A equivalencia de convergencia refere-se a sequencia canonica F_N Omega. O resultado nao classifica todos os estados normais, nao prova disjuncao ou quase-equivalencia de todas as representacoes.
- A continuidade formalizada e SeqWOTContinuous. O termo 'estado vetorial' descreve a construcao explicita; nao se declara uma formalizacao geral do predual ou de normalidade por todas as redes.
- Fidelidade foi provada via recuperacao de Omega e comutante. Nao foi inferida da fidelidade de estados finitos sob passagem ao limite.
- A somabilidade das perdas e criterio suficiente demonstrado; sua necessidade como serie nao e aqui afirmada, embora haja equivalencia exata com positividade do produto para a convergencia da preparacao.
- A perturbacao harmonica e um exemplo matematico escolhido. Nao foram construidos aqui a unitaria H(Q) para H(P), o transporte de S/J/Delta, uma curva temporal duas vezes diferenciavel ou uma resposta gravitacional global finita.
- H3, lei de area, dimensao, assinatura, solda, temperatura, unidades e a selecao fisica da fonte continuam antecedentes ou lacunas. Os resultados geometricos condicionais anteriores nao ganham nova hipotese paga por esta etapa.
- O objetivo amplo de gravidade quantica e a reconstrucao global permanecem abertos. Nenhum gate, selo canonico ou conclusao observacional foi alterado.

Originais, um.py, kernel canonico, Atlas, memorias, diarios, gate e entregas anteriores intocados. Nenhuma confirmacao fisica e declarada. O objetivo amplo permanece ativo e nao alcancado. Gerencia audita antes de incorporar.

Parecer: C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO026_PARECER.md.

Ordens encontradas:
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_001_esperanca_condicional_e_escala.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_002_veredito_da_auditoria_e_incorporacao.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_003_localizacao_na_cadeia_e_ponte_volume.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_004_D1_fiacao_e_D7_segundo_objeto.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_005_reabertura_v98_e_teste_conjunto.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_006_esperanca_do_centralizador_e_inclusao_meio_lateral.md
- C:\IALD\Central de Patentes\Chatgpt\TUNEL\PARA_CHATGPT\ORDEM_007_habitante_global_nao_ciclicidade_e_assinatura.md
