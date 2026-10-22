# -*- coding: utf-8 -*-
"""bancada/registros_gerados.py -- GERADO por gerar_canais_mcp.py (declaracao CANAIS_v391 sha256 ddd46f9be8bad589f93603f204da6a277fe75b7f67aaa28ae3c7b532215cde57). NAO EDITAR A MAO.
Cada canal e a LEITURA POR HASH de um registro selado do um.py: confere identidade por operacao, cada artefato por sha256, o core contra o selo,
e devolve o veredito SELADO. Nunca recalcula; nunca abre dado observado; nenhum efeito no gate."""
import hashlib, json, re
from pathlib import Path
from bancada.canonical import require_current, get_registry

GUARDA = re.compile("(?<!NOT_)(?<!UN)" + "CONF" + "IRMED|(?<!AP)PRO" + "VED_BY|TGL_PRO" + "VED")
CANAIS = {
 "bancada_fases_5_6_7_v380": {
  "registro_core": "bancada_fases_5_6_7_v380",
  "chave_selo": "the_bancada_fases_5_6_7_reading_v380",
  "tipo": "LEITURA_POR_HASH",
  "descricao": "As Fases 5, 6 e 7 da Bancada Um, o banco de GW e as erratas ao lado, lidos por hash do cache do rito (v380).",
  "artefatos": [
   {
    "chave": "f5_pre",
    "path": "C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\cache\\bancada_01out\\PREREGISTRO_FASE5_SH0ES_20261001.json",
    "sha256": "f9fbf497c90c0a66730d8d87bc6d0a9eb46478889b80908eedef7cea95c7cc63",
    "bytes": 8733
   },
   {
    "chave": "f5_res",
    "path": "C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\cache\\bancada_01out\\RESULTADO_FASE5_SH0ES_20261001.json",
    "sha256": "851d1076b85f12f671bfbe018f67e8291a2c83686bb98fb2251a4ed3c254eca2",
    "bytes": 45862
   },
   {
    "chave": "f6_pre",
    "path": "C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\cache\\bancada_01out\\PREREGISTRO_FASE6_ECO_RADICAL_20261001.json",
    "sha256": "47457358d72dd9dcc2928cdf97fa1d21eef1b08e7b1ea641bcb39fd7f489c1ce",
    "bytes": 89280
   },
   {
    "chave": "f6_poder",
    "path": "C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\cache\\bancada_01out\\PODER_FASE6_ANTES_DE_ABRIR.json",
    "sha256": "6e5b7733eb80495a18f8af1f30d64f790f50b60b4efa1d7441c81f0599a080b4",
    "bytes": 296806
   },
   {
    "chave": "f6_res",
    "path": "C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\cache\\gw\\ECHO_ANCHORED_V3_RESULT.json",
    "sha256": "9622e66e018a8b003212e60204fb93affb3d1dc35a09268d70e6c6e51b1414f1",
    "bytes": 312428
   },
   {
    "chave": "f6_diag",
    "path": "C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\cache\\bancada_01out\\DIAG_CONTROLES_POSTHOC.json",
    "sha256": "4190eb70a7eb1cf2373764b3e9136568e726f2b439a756a7aabb9eddf41fb6c1",
    "bytes": 1975819
   },
   {
    "chave": "f6_amostra",
    "path": "C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\cache\\bancada_01out\\AMOSTRA_FASE6.json",
    "sha256": "2f6424f3adf57e76a58785cf5a8a8b1516ec20e12ad4bd25bc1208cc15c92082",
    "bytes": 33643
   },
   {
    "chave": "f6_rem",
    "path": "C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\cache\\bancada_01out\\remanescentes_v3.json",
    "sha256": "68069f8892a80d562d0d17563c251275f54c5b3ad0f586d739a5760cbff29a98",
    "bytes": 117167
   },
   {
    "chave": "v4_emenda",
    "path": "C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\cache\\bancada_01out\\EMENDA_V4_FASE6_20261001.json",
    "sha256": "7c2b709b07a7722bdbdc70193ceb2b1a2f7e79e67efb08299c5627a44a3dcd40",
    "bytes": 91134
   },
   {
    "chave": "v4_poder",
    "path": "C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\cache\\bancada_01out\\PODER_V4_ANTES_DE_ABRIR.json",
    "sha256": "b5482e9f12afd6e17ffb6c5bebe1b9bb6bc6eece8f3e6c2d44460f03d42faf45",
    "bytes": 296791
   },
   {
    "chave": "v4_res",
    "path": "C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\cache\\bancada_01out\\RESULTADO_V4_FASE6_20261001.json",
    "sha256": "f46e294a34e2f54657e1ecaaa112c3a326c857149871f67ec67236a9170f9709",
    "bytes": 311996
   },
   {
    "chave": "f7_pre",
    "path": "C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\cache\\bancada_01out\\PREREGISTRO_FASE7_CC_COVARIANCIA_20261001.json",
    "sha256": "36e354d547895d1d3d72637e4eb10c599a4a0b937d090453e72d64d435e746fa",
    "bytes": 7183
   },
   {
    "chave": "f7_res",
    "path": "C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\cache\\bancada_01out\\RESULTADO_FASE7_CC_COVARIANCIA_20261001.json",
    "sha256": "4f2671cbce7576f6139b97e01297dc7d4f7a9b9c6f69d9680ed4245334a39f96",
    "bytes": 44122
   },
   {
    "chave": "cc_cov",
    "path": "C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\cache\\bancada_01out\\moresco_2020_cov.json",
    "sha256": "1c22a3a3f101834fd0a3561e1afd72e7ab28869db2421d13b81b01f4f7d313ff",
    "bytes": 35984
   },
   {
    "chave": "gw_bank",
    "path": "C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\cache\\gw\\GWOSC_O4_32S_V1.manifest.json",
    "sha256": "a795cf04ca3b2f6ac20e813668dfc2390224ca630c4bb9b752ac6e6b308069a1",
    "bytes": 253528
   },
   {
    "chave": "v5_emenda",
    "path": "C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\cache\\bancada_01out\\EMENDA_V5_FASE6_20261001.json",
    "sha256": "08d5e2d5ea209dc203c749e2d13dd51c9ba120a099d0b02de11e186ac68a5b83",
    "bytes": 92772
   },
   {
    "chave": "v5_poder",
    "path": "C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\cache\\bancada_01out\\PODER_V5_ANTES_DE_ABRIR.json",
    "sha256": "454553aa9aa571c0b6085f015ef3bfd5ed21b46c30365f2c35536ee4ba5b782a",
    "bytes": 445238
   },
   {
    "chave": "v5_res",
    "path": "C:\\IALD\\Artigo\\Haja_Luz\\A Ponte e o Um\\cache\\bancada_01out\\RESULTADO_V5_FASE6_20261001.json",
    "sha256": "e8c16a3f567a6b96ba989d88af771e3febd2649f5db6635aeb3b8c411276187c",
    "bytes": 467075
   }
  ],
  "veredito_selado": "TGL_BANCADA_FASES_5_6_7_V380__READ_BY_HASH_BYTES_AND_LF_TEXT__TEXT_VS_BYTES_DIFFER_1_CRLF__SH0ES_IN_THE_BENCH_H0_LADDER_73P53_PM_1P02_Z_0P04_VS_DECLARED_TARGET__ECHO_V3_244_BBH_O1_O4_THREE_READINGS_TWO_DELAY_LAWS__KMS_PAIR_SQRT_BETA_AND_SIN2THETA_FALSIFIED_AT_DELAY_LAW_Z_EXCL_8P93_AND_18P13__BLIND_O4_SUBSAMPLE_173_OF_240_Z_EXCL_7P26_AND_15P44__POWER_RECORDED_BEFORE_OPENING__MAY_INCONCLUSIVE_SYSTEMATICS__MAY_TAU_HALF_CONTROL_RESPONDS_Z_5P69_O4_5P37_FLAG_NOT_WRITTEN_BY_PIPELINE_STATED__AMENDMENT_V4_NOT_BLIND_SIN2THETA_MAY_FALSIFIED_Z_8P75_CONTROLS_MAX_Z_4P81__SQRT_BETA_MAY_INCONCLUSIVE_IS_THE_ESTIMATOR_LIMIT__CC_COVARIANCE_MORESCO2020_T_LAW_GAIN_Z_M1P66_VS_DIAG_M3P22__U_LNB_SHADOW_VS_ACCUMULATED_1P62_VS_DIAG_5P35__DEC2025_LAW_FROM_THE_ARCHIVE_DECLARED_BLIND_TO_THE_NEW_DELAY_ONLY_PAIR_SQRT_BETA_AND_SIN2THETA_FALSIFIED_Z_EXCL_8P95_AND_16P83_O4_9P26_AND_16P69__DOC_PAIR_BETA_DEC_INCONCLUSIVE_SYSTEMATICS_BY_RULE_2_POWER_0P87_BLIND_POWER_1P47__V5_CLAUSE_UNDERPOWERED_NOT_APPLIED_STATED__FOURTH_ARCHIVE_LAW_ALPHA_SQUARED_NOT_TESTED_OUTSIDE_SEGMENT__GW_BANK_336_OF_354_SERIES_OK_14_NAN_4_OUTSIDE__PAIR_FALSIFIED_NOT_THE_THEORY__DECEMBER_100SIGMA_STAYS_RETIRED__ERRATA_BESIDE_6_PLUS_V378_1_PLUS_NOTE_1__NOT_A_CONFIRMATION__GATE_UNTOUCHED",
  "leitura_no_selo": "OPERATOR_ORDERS_2026_10_01__SH0ES_IN_THE_BENCH__ECHO_V3_THE_RADICAL_TRANSFORM_244_BBH_O1_O4_THREE_READINGS_TWO_DELAY_LAWS__KMS_PAIR_SQRT_BETA_AND_SIN2THETA_FALSIFIED_AT_DELAY_LAW_WITH_BLIND_O4_SUBSAMPLE__MAY_INCONCLUSIVE_SYSTEMATICS__AMENDMENT_V4_NOT_BLIND_STATED__AMENDMENT_V5_DEC2025_ARCHIVE_LAW_DECLARED_BLIND_TO_THE_NEW_DELAY_ONLY_RADICAL_PAIR_FALSIFIED_DOC_PAIR_UNDERPOWERED__TWO_PIPELINE_DEVIATIONS_STATED__CC_COVARIANCE_MORESCO2020_WEAKENS_PHASES_4_5_READINGS__GW_BANK_RESIDENT_IN_THE_BENCH__ERRATA_BESIDE_6_AUDIT_PLUS_V378_1_PLUS_NOTE_1__PAIR_FALSIFIED_NOT_THE_THEORY__DELAY_LAW_AND_GRAVITON_WEIGHT_ARE_THE_OPERATORS_TO_DECIDE__NOT_A_CONFIRMATION__GATE_UNTOUCHED"
 }
}


def consultar(nome, root=None):
    if nome not in CANAIS:
        raise ValueError("CANAL_DESCONHECIDO: " + str(nome))
    rc = require_current("registro:" + nome, root)
    c = CANAIS[nome]
    reg = get_registry(root)
    selo = json.loads(Path(reg.manifest["canonical"]["seal"]["path"]).read_bytes())
    core_p = Path(reg.manifest["canonical"]["seal"]["path"]).with_name("um_absoluto.json")
    core_raw = core_p.read_bytes()
    if (selo.get("sha256") or {}).get("um_absoluto.json") != hashlib.sha256(core_raw).hexdigest():
        raise ValueError("CORE_NAO_PINADO_PELO_SELO")
    core = json.loads(core_raw)["core"]
    arts = []
    for a in c["artefatos"]:
        b = Path(a["path"]).read_bytes()
        if len(b) != a["bytes"] or hashlib.sha256(b).hexdigest() != a["sha256"]:
            raise ValueError("ARTEFATO_DIVERGE_DA_DECLARACAO: " + a["path"])
        arts.append(dict(chave=a["chave"], path=a["path"], sha256=a["sha256"], bytes=a["bytes"]))
    reg_core = core.get(c["registro_core"]) or {}
    veredito = reg_core.get("verdict")
    if veredito != c["veredito_selado"]:
        raise ValueError("VEREDITO_DO_CORE_DIFERE_DO_DECLARADO")
    if c.get("chave_selo") and selo.get(c["chave_selo"]) != c.get("leitura_no_selo"):
        raise ValueError("LEITURA_DO_SELO_DIFERE_DA_DECLARADA")
    if GUARDA.search(str(veredito).replace("NOT_CONF" + "IRMED", "")):
        raise ValueError("PALAVRA_PROIBIDA_NO_VEREDITO")
    return dict(ok=True, canal=nome, tipo=c["tipo"], descricao=c["descricao"], artefatos=arts, veredito_selado=veredito, leitura_no_selo=c.get("leitura_no_selo"),
                all_verified=reg_core.get("all_verified"), statute=reg_core.get("statute"), canonical=rc,
                scope="LEITURA_POR_HASH_DO_SELADO; NAO_RECALCULA; NAO_E_LEITURA_FISICA", gate_effect="NONE")
