[REAL / INPUT / OPEN] ENTREGA 013 ESPONTÂNEA — preservação da nulidade e construção pontual da tela.

Continuação de 012, 05/09/2026. Nenhuma ordem 013 da gerência estava no túnel ao publicar. Auditoria independente pendente; nenhuma alteração de gate.

## Critérios e alcance

| Critério | Estado | Evidência |
|---|---|---|
| Derivação anterior ao código | PAGO nos alvos iniciais | CONTINUACAO013_DERIVACAO_PREVIA.md; o controle suplementar de famílias normalizadas é documentado posteriormente no parecer. |
| Preservação de g(V,V)=0 | PAGO | Derivadas efetivas: d[g(V,V)](w)=2g(V,∇wV); nulidade numa vizinhança implica g(V,∇wV)=0. |
| Condição da tela anteriormente recebida | PAGO | null_field_preserves_frame_pairing produz preserves_null_pairing da primeira coluna V; nenhuma hipótese geodésica necessária aqui. |
| Base transversal para todo eixo unitário | PAGO | reflectedSpatialScreen usa uma reflexão ortogonal em R³. |
| Referencial nulo para toda direção não nula | PAGO | flatNullFrame: Gram G0=nullScreenGram(-I), inversa construída e primeira coluna v. |
| Transporte para métrica soldada | PAGO | solderedNullFrame: g=EᵀηE, F=D F0; produtos inversos e Gram provados. Assinatura e dimensão permanecem INPUT. |
| Habitante do contrato da entrega 012 | PAGO no ponto | leviCivitaScreenAtPoint e levi_civita_null_screen_exists; não recebem tela nem preserves_null_pairing. |
| Densidade inicial | PAGO como normalização | Gram transversal -I implica A=1 na base escolhida. Não fixa área física. |
| Controles contra vacuidade e promoção indevida | PAGO | Vetor (5,3,4,0), direção zero impossível, família normalizada com lei A′=θA exige θ=0. |
| Família transportada e horizontes gerais | NÃO PAGO | Não construída uma tela suave que satisfaça transporte de Lie, nem congruência/superfície geral. |
| Gravitação quântica geral | NÃO PAGO | Entropia-área microscópica, calor, H3, ponte modular, escala e globalização permanecem abertos. |

5 módulos; 26 teoremas; 7 definições com axiomas separadamente impressos. Contagens lidas dos fontes. Apenas propext, Classical.choice e Quot.sound nas dependências finais; sem erros, avisos ou sorryAx.

## Reprodução

```powershell
& 'C:\Python314\python.exe' -B 'C:\IALD\Central de Patentes\Chatgpt\audit_continuation013.py'
```

O comando acima só lê e confere a custódia. Comandos de recompilação dos módulos novos, na ordem abaixo (a gerência deve usar sua cópia independente):

```powershell
& 'C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1' -Module CovariantNullPreservation
if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }
& 'C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1' -Module SpatialScreenConstruction
if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }
& 'C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1' -Module NullFrameConstruction
if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }
& 'C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1' -Module ConstructedScreenAtPoint
if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }
& 'C:\IALD\Central de Patentes\Chatgpt\verify_stage.ps1' -Module NullScreenConstructionControls
if ($LASTEXITCODE -ne 0) { throw "Falha Lean" }
```

O manifesto fixa a árvore local de fontes, cópias binárias e logs. Lean 4.31.0/mathlib são dependências externas locais; isto não é um pacote portátil nem uma recompilação independente.

## Axiomas impressos

```text
ChatgptAudit.tensor_pair_symmetric: [propext, Classical.choice, Quot.sound]
ChatgptAudit.frame_pair_entry: [propext, Classical.choice, Quot.sound]
ChatgptAudit.mixed_frame_pair_entry: [propext, Classical.choice, Quot.sound]
ChatgptAudit.quad_coordinate_derivative: [propext, Classical.choice, Quot.sound]
ChatgptAudit.metric_compatible_quad_derivative: [propext, Classical.choice, Quot.sound]
ChatgptAudit.null_field_covariant_pairing: [propext, Classical.choice, Quot.sound]
ChatgptAudit.null_field_direction_pairing: [propext, Classical.choice, Quot.sound]
ChatgptAudit.null_field_preserves_frame_pairing: [propext, Classical.choice, Quot.sound]
ChatgptAudit.reflectedSpatialScreen: [propext, Classical.choice, Quot.sound]
ChatgptAudit.spatial_inner_components: [propext, Classical.choice, Quot.sound]
ChatgptAudit.minkowski_quad_coordinates: [propext, Classical.choice, Quot.sound]
ChatgptAudit.nonzero_null_time: [propext, Classical.choice, Quot.sound]
ChatgptAudit.unit_null_spatial_norm: [propext, Classical.choice, Quot.sound]
ChatgptAudit.minkowski_pair_lift: [propext, Classical.choice, Quot.sound]
ChatgptAudit.null_frame_matrix_gram: [propext, Classical.choice, Quot.sound]
ChatgptAudit.normalized_null_gram_squared: [propext, Classical.choice, Quot.sound]
ChatgptAudit.flatNullFrame: [propext, Classical.choice, Quot.sound]
ChatgptAudit.invertible_solder_nonzero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.solderedNullFrame: [propext, Classical.choice, Quot.sound]
ChatgptAudit.normalized_frame_screen_gram: [propext, Classical.choice, Quot.sound]
ChatgptAudit.negative_identity_screen_area: [propext, Classical.choice, Quot.sound]
ChatgptAudit.assembleNormalizedScreen: [propext, Classical.choice, Quot.sound]
ChatgptAudit.solderedScreenAtPoint: [propext, Classical.choice, Quot.sound]
ChatgptAudit.leviCivitaScreenAtPoint: [propext, Classical.choice, Quot.sound]
ChatgptAudit.normalized_screen_at_point_area: [propext, Classical.choice, Quot.sound]
ChatgptAudit.levi_civita_null_screen_exists: [propext, Classical.choice, Quot.sound]
ChatgptAudit.zero_direction_has_no_null_screen: [propext, Classical.choice, Quot.sound]
ChatgptAudit.off_axis_vector_nonzero: [propext, Classical.choice, Quot.sound]
ChatgptAudit.off_axis_vector_null: [propext, Classical.choice, Quot.sound]
ChatgptAudit.offAxisNullFrame: [propext, Classical.choice, Quot.sound]
ChatgptAudit.off_axis_frame_verified: [propext, Classical.choice, Quot.sound]
ChatgptAudit.normalized_family_area_constant: [propext, Classical.choice, Quot.sound]
ChatgptAudit.normalized_family_expansion_obstruction: [propext, Classical.choice, Quot.sound]
```

## Artefatos e hashes

Manifesto: `C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO013_MANIFESTO.json` — SHA256 `03f4f30f326e2bfd4efc06e5e395b2103c96013c3dadb6c3c88654ef98971019`.
Inventário: 408 caminhos absolutos com tamanho e hash dos bytes.

| Artefato principal | SHA256 |
|---|---|
| `C:\IALD\Central de Patentes\Chatgpt\audit_continuation013.py` | `a96881e90d994b30eb608ded9346f4826f76fe7917dd637256e9ec4a287701b5` |
| `C:\IALD\Central de Patentes\Chatgpt\ConstructedScreenAtPoint.20260905_234641.log` | `539cd560250019da4f5e29d2d2f6082f9288e22e8a03021edef3167ec8b9d649` |
| `C:\IALD\Central de Patentes\Chatgpt\ConstructedScreenAtPoint.lean` | `1c9f184f1a22b2739d234a39ce1c92a81ccbe74bd1853f0dc95209898a456143` |
| `C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO013_DERIVACAO_PREVIA.md` | `c0513e5957e4cda53deaffaa0ced012871dd51e85ba4dfcfbba4d7cbb9afaa53` |
| `C:\IALD\Central de Patentes\Chatgpt\CONTINUACAO013_PARECER.md` | `d6672d3b624086bbfcdaa65766b1806a9b9ca286513ad0d52cf21c6110887db2` |
| `C:\IALD\Central de Patentes\Chatgpt\CovariantNullPreservation.20260905_233403.log` | `c2d2dabce195b8fb04a8e884a2ff04e010c6521b9e1cc2dff43dddcdcf45824d` |
| `C:\IALD\Central de Patentes\Chatgpt\CovariantNullPreservation.lean` | `348c04fc4c754920557525b92a5910c9173d16e08bd5eaf15e99ff5f05c5304a` |
| `C:\IALD\Central de Patentes\Chatgpt\NullFrameConstruction.20260905_234419.log` | `ab00795bfde1eb5234dba59e7aded05295d149bc67a5fe261ae4950b79943389` |
| `C:\IALD\Central de Patentes\Chatgpt\NullFrameConstruction.lean` | `07cfa22cc187b3bb236797fd4542e4ca09f45c8cbbe29ea20e5b6788aa4c7fc9` |
| `C:\IALD\Central de Patentes\Chatgpt\NullScreenConstructionControls.20260905_234752.log` | `ed7d17df63e919d8e4e63adb0c8046065585ba7e9e0aae1bc699c5572bce9d17` |
| `C:\IALD\Central de Patentes\Chatgpt\NullScreenConstructionControls.lean` | `e2ff51d93084bcdc739b467ddba8a97428de2ab3ce6b773ca9d80cd841f66391` |
| `C:\IALD\Central de Patentes\Chatgpt\SpatialScreenConstruction.20260905_233857.log` | `2896c16e118a0fe74c070381188ad2ed073dd464206a6aec97004edf818e47c3` |
| `C:\IALD\Central de Patentes\Chatgpt\SpatialScreenConstruction.lean` | `0d7b34ff075ed7f35112ec8e43608edc4de63fb74c54a2eb23cacbd1607dd4f7` |

## Tentativas preservadas

- `C:\IALD\Central de Patentes\Chatgpt\CovariantNullPreservation.20260905_233303.failed_compile.log`: exit code 1; erro de elaboração ou aviso; cópia exata do log.
- `C:\IALD\Central de Patentes\Chatgpt\SpatialScreenConstruction.20260905_233513.failed_compile.log`: exit code 1; erro de elaboração ou aviso; cópia exata do log.
- `C:\IALD\Central de Patentes\Chatgpt\SpatialScreenConstruction.20260905_233613.failed_compile.log`: exit code 1; erro de elaboração ou aviso; cópia exata do log.
- `C:\IALD\Central de Patentes\Chatgpt\SpatialScreenConstruction.20260905_233800.rejected_warning.log`: exit code 0; erro de elaboração ou aviso; cópia exata do log.
- `C:\IALD\Central de Patentes\Chatgpt\NullFrameConstruction.20260905_234027.failed_compile.log`: exit code 1; erro de elaboração ou aviso; cópia exata do log.
- `C:\IALD\Central de Patentes\Chatgpt\NullFrameConstruction.20260905_234127.failed_compile.log`: exit code 1; erro de elaboração ou aviso; cópia exata do log.
- `C:\IALD\Central de Patentes\Chatgpt\NullFrameConstruction.20260905_234316.failed_compile.log`: exit code 1; erro de elaboração ou aviso; cópia exata do log.

As revisões têm backups dos bytes. Erros de sintaxe, diferenciação de somas e redução das entradas matriciais foram corrigidos; seus logs continuam no inventário. O histórico da correção de assinatura da entrega 012 permanece fixado por seu manifesto, sem alterar os arquivos anteriores.

## Limites e integração

O enunciado principal assume um campo V suave e nulo numa vizinhança, V(x)≠0 e uma solda suave invertível em quatro dimensões. A construção é pontual. A existência desse campo para todos os dados de horizonte, sua geodesicidade e o transporte dos vetores de tela ainda têm de ser construídos.

Normalizar independentemente cada tela produz Gram -I e área 1 em cada parâmetro; isso não é o transporte que mede uma área em expansão. O controle normalized_family_expansion_obstruction formaliza precisamente essa restrição.

Fonte primária de contexto: [Dey e Majhi, 2020](https://arxiv.org/abs/2009.08221), sobre superfície nula, projeção transversal e vetor nulo auxiliar. As provas aqui usam as definições e operações formais locais; a referência não fornece uma hipótese física ao kernel.

Escritas exclusivamente em Chatgpt. Nenhum um.py executado, importado ou editado; kernel canônico, Atlas, memórias, selos e gate intocados. Sem dados observacionais. A gerência recompila e audita antes de incorporar. Objetivo amplo ativo e OPEN.
