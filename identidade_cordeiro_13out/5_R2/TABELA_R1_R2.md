TABELA r1 -> r2 — F1.IDENTIDADE — 13/10/2026 (construtor da r2, em nome próprio)

Lida do ambiente compilado pelo elaborador `#r2_tabela` (`pedra/AudR2.lean`): a r1 compilada numa cópia com o
namespace trocado (`TGLExt.TheIdentityHasAName_r1`, `pedra/IdR1_TheIdentityHasAName_r1.lean`) e a r2 no mesmo
ambiente. O tipo de cada constante da r1, com os nomes da r1 levados pelo mapa do ADENDO R2, comparado ao tipo da
r2 por `Expr.eqv` (alfa-equivalência), por `Expr.equal` (estrita) e por `Expr.equal` depois de apagar SÓ os nomes
de binder. Para definições, o mesmo com o valor. Fonte: `logs/aud_r2_SAIDA.txt` sha256 da49329f5706ce4d8a8356ca44496f695071e2709b06ed779bcffaed7e0e7cbc.

Contagem (todas): {"MANTIDA": 98, "TIPO_MUDOU": 9, "RENOMEADA": 12, "NOVA": 31}; sem as internas: {"MANTIDA": 83, "TIPO_MUDOU": 8, "RENOMEADA": 10, "NOVA": 18}.

| status | r1 | r2 | espécie | enunciado eqv | equal | equal sem nomes de binder | valor (eqv / equal sem nomes) |
|---|---|---|---|---|---|---|---|
| MANTIDA | `NamedIdentity` | `NamedIdentity` | inductive→inductive | true | true | true | na/na |
| MANTIDA | `NamedIdentity.alpha` | `NamedIdentity.alpha` | def→def | true | true | true | true/true |
| MANTIDA | `NamedIdentity.alpha_lt_one` | `NamedIdentity.alpha_lt_one` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `NamedIdentity.alpha_pos` | `NamedIdentity.alpha_pos` | theorem→theorem | true | true | true | na/na |
| TIPO_MUDOU | `NamedIdentity.casesOn` | `NamedIdentity.casesOn` | def→def | false | false | false | false/false |
| MANTIDA | `NamedIdentity.ctorIdx` | `NamedIdentity.ctorIdx` | def→def | true | false | true | true/true |
| MANTIDA | `NamedIdentity.i_am` | `NamedIdentity.i_am` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `NamedIdentity.in_the_tower` | `NamedIdentity.in_the_tower` | theorem→theorem | true | true | true | na/na |
| TIPO_MUDOU | `NamedIdentity.mk` | `NamedIdentity.mk` | ctor→ctor | false | false | false | na/na |
| TIPO_MUDOU | `NamedIdentity.mk.inj` | `NamedIdentity.mk.inj` | theorem→theorem | false | false | false | na/na |
| TIPO_MUDOU | `NamedIdentity.mk.injEq` | `NamedIdentity.mk.injEq` | theorem→theorem | false | false | false | na/na |
| TIPO_MUDOU | `NamedIdentity.mk.noConfusion` | `NamedIdentity.mk.noConfusion` | def→def | false | false | false | false/false |
| TIPO_MUDOU | `NamedIdentity.mk.sizeOf_spec` | `NamedIdentity.mk.sizeOf_spec` | theorem→theorem | false | false | false | na/na |
| MANTIDA | `NamedIdentity.name` | `NamedIdentity.name` | def→def | true | true | true | true/true |
| MANTIDA | `NamedIdentity.noConfusion` | `NamedIdentity.noConfusion` | def→def | true | true | true | false/false |
| MANTIDA | `NamedIdentity.noConfusionType` | `NamedIdentity.noConfusionType` | def→def | true | true | true | false/false |
| MANTIDA | `NamedIdentity.persists` | `NamedIdentity.persists` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `NamedIdentity.read_from_within` | `NamedIdentity.read_from_within` | theorem→theorem | true | true | true | na/na |
| TIPO_MUDOU | `NamedIdentity.rec` | `NamedIdentity.rec` | rec→rec | false | false | false | na/na |
| TIPO_MUDOU | `NamedIdentity.recOn` | `NamedIdentity.recOn` | def→def | false | false | false | false/false |
| MANTIDA | `NamedIdentity.rename` | `NamedIdentity.rename` | def→def | true | true | true | false/false |
| MANTIDA | `NamedIdentity.unit_projection` | `NamedIdentity.unit_projection` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `TowerIdentity` | `TowerIdentity` | def→def | true | true | true | true/true |
| MANTIDA | `alicerce_fundante` | `alicerce_fundante` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `alicerce_fundante_habitado` | `alicerce_fundante_habitado` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `alpha_above_one_breaks_the_form` | `alpha_above_one_breaks_the_form` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `alpha_below_minus_one_breaks_the_form` | `alpha_below_minus_one_breaks_the_form` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `alpha_is_measured_from_within` | `alpha_is_measured_from_within` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `alpha_is_recovered_by_the_inner_reading` | `alpha_is_recovered_by_the_inner_reading` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `alpha_one_degenerates` | `alpha_one_degenerates` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `alpha_zero_degenerates` | `alpha_zero_degenerates` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `changing_the_name_changes_nothing` | `changing_the_name_changes_nothing` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `dephase_apply'` | `dephase_apply'` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `dephased_det` | `dephased_det` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `eInner` | `eInner` | def→def | true | true | true | true/true |
| MANTIDA | `eInner.eq_1` | `eInner.eq_1` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `eOuter` | `eOuter` | def→def | true | true | true | true/true |
| MANTIDA | `eOuter.eq_1` | `eOuter.eq_1` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `every_name_bears_the_same_identity` | `every_name_bears_the_same_identity` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `halfProfile` | `halfProfile` | def→def | true | true | true | true/true |
| MANTIDA | `i_am_what_i_am` | `i_am_what_i_am` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `identityProj` | `identityProj` | def→def | true | true | true | true/true |
| MANTIDA | `identityProj.eq_1` | `identityProj.eq_1` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `identityProj_apply` | `identityProj_apply` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `identityProj_idem` | `identityProj_idem` | theorem→theorem | true | true | true | na/na |
| RENOMEADA | `identityProj_mulVec_inscription` | `identityProj_mulVec_quadInscription` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `identityProj_trace` | `identityProj_trace` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `identityProj_trace_one` | `identityProj_trace_one` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `identity_persists_in_the_limit` | `identity_persists_in_the_limit` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `identity_persists_under_dephasing` | `identity_persists_under_dephasing` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `inner_self_one_of_norm` | `inner_self_one_of_norm` | theorem→theorem | true | false | true | na/na |
| RENOMEADA | `inscription` | `quadInscription` | def→def | true | true | true | true/true |
| RENOMEADA | `inscription.eq_1` | `quadInscription.eq_1` | theorem→theorem | true | true | true | na/na |
| RENOMEADA | `inscription_dot` | `quadInscription_dot` | theorem→theorem | true | true | true | na/na |
| RENOMEADA | `inscription_is_unit` | `quadInscription_is_unit` | theorem→theorem | true | true | true | na/na |
| RENOMEADA | `inscription_ne_zero` | `quadInscription_ne_zero` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `ip00` | `ip00` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `ip01` | `ip01` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `ip10` | `ip10` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `ip11` | `ip11` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `negative_alpha_is_not_recovered` | `negative_alpha_is_not_recovered` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `no_named_identity_at_the_poles` | `no_named_identity_at_the_poles` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `observing_adds_nothing_reexport` | `observing_adds_nothing_reexport` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `ofName` | `ofName` | def→def | true | true | true | false/false |
| MANTIDA | `postedName` | `postedName` | def→def | true | true | true | true/true |
| MANTIDA | `probe_named_identity` | `probe_named_identity` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `probe_tower_identity` | `probe_tower_identity` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `qOf` | `qOf` | def→def | true | true | true | true/true |
| MANTIDA | `qOf.eq_1` | `qOf.eq_1` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `qOf_pos` | `qOf_pos` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `q_sq_add` | `q_sq_add` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `quadVec` | `quadVec` | def→def | true | false | true | true/true |
| MANTIDA | `quadVec.eq_1` | `quadVec.eq_1` | theorem→theorem | true | false | true | na/na |
| MANTIDA | `quadVec_inner_Omega` | `quadVec_inner_Omega` | theorem→theorem | true | false | true | na/na |
| MANTIDA | `quadVec_inner_self` | `quadVec_inner_self` | theorem→theorem | true | false | true | na/na |
| MANTIDA | `quadVec_inner_xi` | `quadVec_inner_xi` | theorem→theorem | true | false | true | na/na |
| MANTIDA | `quadVec_norm` | `quadVec_norm` | theorem→theorem | true | false | true | na/na |
| MANTIDA | `quadratic_reading` | `quadratic_reading` | theorem→theorem | true | false | true | na/na |
| MANTIDA | `rankOne_aux` | `rankOne_aux` | theorem→theorem | true | false | true | na/na |
| MANTIDA | `rank_one_does_not_persist` | `rank_one_does_not_persist` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `rank_one_does_not_persist_in_the_limit` | `rank_one_does_not_persist_in_the_limit` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `rank_two_of_det_ne_zero` | `rank_two_of_det_ne_zero` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `rank_zero_iff_aux` | `rank_zero_iff_aux` | theorem→theorem | true | false | true | na/na |
| MANTIDA | `reading_on_eInner` | `reading_on_eInner` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `reading_on_eOuter` | `reading_on_eOuter` | theorem→theorem | true | true | true | na/na |
| RENOMEADA | `rereading_adds_nothing` | `post_is_idempotent_on_the_vector` | theorem→theorem | true | false | true | na/na |
| MANTIDA | `theNamedIdentity` | `theNamedIdentity` | def→def | true | true | true | true/true |
| MANTIDA | `the_form_does_not_fix_alpha` | `the_form_does_not_fix_alpha` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `the_identity_in_the_tower` | `the_identity_in_the_tower` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `the_identity_is_the_quadratic_projection` | `the_identity_is_the_quadratic_projection` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `the_name_enters_no_proof` | `the_name_enters_no_proof` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `the_name_read_in_the_name` | `the_name_read_in_the_name` | theorem→theorem | true | false | true | na/na |
| MANTIDA | `the_named_identity_bears_the_posted_name` | `the_named_identity_bears_the_posted_name` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `the_named_identity_carries_the_identity` | `the_named_identity_carries_the_identity` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `the_self_reading_has_two_values` | `the_self_reading_has_two_values` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `the_structure_does_not_fix_the_name` | `the_structure_does_not_fix_the_name` | theorem→theorem | true | true | true | na/na |
| RENOMEADA | `towerInner` | `towerInnerAxis` | def→def | true | true | true | true/true |
| RENOMEADA | `towerInner_norm` | `towerInnerAxis_norm` | theorem→theorem | true | true | true | na/na |
| RENOMEADA | `towerInner_orth` | `towerInnerAxis_orth` | theorem→theorem | true | true | true | na/na |
| MANTIDA | `towerInscription` | `towerInscription` | def→def | true | true | true | true/true |
| MANTIDA | `trace_dephase` | `trace_dephase` | theorem→theorem | true | false | true | na/na |
| NOVA | `-` | `IALDTowerIdentity` | -→def | - | - | - | - |
| NOVA | `-` | `NamedIdentity.in_the_IALD_tower` | -→theorem | - | - | - | - |
| NOVA | `-` | `dephasing_fixes_the_poles` | -→theorem | - | - | - | - |
| NOVA | `-` | `probe_IALD_tower` | -→theorem | - | - | - | - |
| NOVA | `-` | `rereading_reads_the_same` | -→theorem | - | - | - | - |
| NOVA | `-` | `the_IALD_tower_erases_the_inner_axis` | -→theorem | - | - | - | - |
| NOVA | `-` | `the_identity_in_the_IALD_tower` | -→theorem | - | - | - | - |
| NOVA | `-` | `the_inner_axis_does_not_persist_in_the_tower` | -→theorem | - | - | - | - |
| NOVA | `-` | `the_inner_reading_at_five_is_not_an_identity` | -→theorem | - | - | - | - |
| NOVA | `-` | `the_inner_reading_is_by_construction` | -→theorem | - | - | - | - |
| NOVA | `-` | `thirdProfile` | -→def | - | - | - | - |
| NOVA | `-` | `towerInnerAxis.eq_1` | -→theorem | - | - | - | - |
| NOVA | `-` | `towerInscription.eq_1` | -→theorem | - | - | - | - |
| NOVA | `-` | `towerInscriptionElem` | -→def | - | - | - | - |
| NOVA | `-` | `towerInscriptionOp` | -→def | - | - | - | - |
| NOVA | `-` | `towerInscriptionOp.eq_1` | -→theorem | - | - | - | - |
| NOVA | `-` | `towerInscriptionOp_mem` | -→theorem | - | - | - | - |
| NOVA | `-` | `towerInscriptionOp_omega` | -→theorem | - | - | - | - |

Internas (nomes com componente `_`, geradas pelo elaborador): MANTIDA `NamedIdentity._sizeOf_1`, MANTIDA `NamedIdentity._sizeOf_inst`, TIPO_MUDOU `NamedIdentity.mk._flat_ctor`, MANTIDA `TowerIdentity._proof_1`, MANTIDA `TowerIdentity._proof_2`, MANTIDA `TowerIdentity._proof_3`, MANTIDA `TowerIdentity._proof_4`, MANTIDA `halfProfile._proof_1`, MANTIDA `halfProfile._proof_2`, MANTIDA `halfProfile._proof_3`, MANTIDA `ofName._proof_1`, MANTIDA `ofName._proof_2`, MANTIDA `ofName._proof_3`, MANTIDA `ofName._proof_4`, MANTIDA `ofName._proof_5`, MANTIDA `rankOne_aux._proof_1_1`, RENOMEADA `towerInnerAxis._proof_1`, RENOMEADA `towerInnerAxis._proof_2`, NOVA `IALDTowerIdentity._proof_1`, NOVA `IALDTowerIdentity._proof_2`, NOVA `IALDTowerIdentity._proof_3`, NOVA `IALDTowerIdentity._proof_4`, NOVA `IALDTowerIdentity._proof_5`, NOVA `IALDTowerIdentity._proof_6`, NOVA `IALDTowerIdentity._proof_7`, NOVA `IALDTowerIdentity._proof_8`, NOVA `IALDTowerIdentity._proof_9`, NOVA `ofName._proof_6`, NOVA `thirdProfile._proof_1`, NOVA `thirdProfile._proof_2`, NOVA `thirdProfile._proof_3`.

Conferências contra o ADENDO R2:
```
{
 "renomeacoes_de_1o_nivel_iguais_ao_mapa_do_ADENDO": true,
 "tipo_mudou_so_nos_geradores_de_NamedIdentity": true,
 "tipo_mudou_lista": [
  "NamedIdentity.casesOn",
  "NamedIdentity.mk",
  "NamedIdentity.mk._flat_ctor",
  "NamedIdentity.mk.inj",
  "NamedIdentity.mk.injEq",
  "NamedIdentity.mk.noConfusion",
  "NamedIdentity.mk.sizeOf_spec",
  "NamedIdentity.rec",
  "NamedIdentity.recOn"
 ],
 "removidas": [],
 "mantidas_ou_renomeadas_com_enunciado_diferente_eqv": [],
 "Expr_equal_falso_mas_eqv_verdadeiro": [
  "NamedIdentity.ctorIdx",
  "halfProfile._proof_2",
  "halfProfile._proof_3",
  "inner_self_one_of_norm",
  "quadVec",
  "quadVec.eq_1",
  "quadVec_inner_Omega",
  "quadVec_inner_self",
  "quadVec_inner_xi",
  "quadVec_norm",
  "quadratic_reading",
  "rankOne_aux",
  "rankOne_aux._proof_1_1",
  "rank_zero_iff_aux",
  "rereading_adds_nothing",
  "the_name_read_in_the_name",
  "trace_dephase"
 ],
 "Expr_equal_falso_mesmo_sem_nomes_de_binder": [],
 "definicoes_com_valor_diferente": [
  "NamedIdentity._sizeOf_1",
  "NamedIdentity.casesOn",
  "NamedIdentity.mk._flat_ctor",
  "NamedIdentity.mk.noConfusion",
  "NamedIdentity.noConfusion",
  "NamedIdentity.noConfusionType",
  "NamedIdentity.recOn",
  "NamedIdentity.rename",
  "ofName"
 ],
 "novas": [
  "IALDTowerIdentity",
  "IALDTowerIdentity._proof_1",
  "IALDTowerIdentity._proof_2",
  "IALDTowerIdentity._proof_3",
  "IALDTowerIdentity._proof_4",
  "IALDTowerIdentity._proof_5",
  "IALDTowerIdentity._proof_6",
  "IALDTowerIdentity._proof_7",
  "IALDTowerIdentity._proof_8",
  "IALDTowerIdentity._proof_9",
  "NamedIdentity.in_the_IALD_tower",
  "dephasing_fixes_the_poles",
  "ofName._proof_6",
  "probe_IALD_tower",
  "rereading_reads_the_same",
  "the_IALD_tower_erases_the_inner_axis",
  "the_identity_in_the_IALD_tower",
  "the_inner_axis_does_not_persist_in_the_tower",
  "the_inner_reading_at_five_is_not_an_identity",
  "the_inner_reading_is_by_construction",
  "thirdProfile",
  "thirdProfile._proof_1",
  "thirdProfile._proof_2",
  "thirdProfile._proof_3",
  "towerInnerAxis.eq_1",
  "towerInscription.eq_1",
  "towerInscriptionElem",
  "towerInscriptionOp",
  "towerInscriptionOp.eq_1",
  "towerInscriptionOp_mem",
  "towerInscriptionOp_omega"
 ]
}
```
