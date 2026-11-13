from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path

import numpy as np

HERE = Path(__file__).resolve().parent
ORDER = HERE.parents[1] / "ORDEM_KIMI_H0DN_05_11nov.md"
PRE_REG = HERE.parents[2] / "h0dn_bg1_v411_emenda_11nov" / "EMENDA_E_PRE_REGISTRO_V411_rascunho.md"
Y_OBS = HERE.parent / "y_obs.npz"
STUDY = HERE.parent / "ordem03B" / "ESTUDO_CONDICIONAL_R3B.json"
DEPOSIT = Path(r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\fila\depositos\kimi")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pin(path: Path) -> dict:
    return {"path": str(path), "bytes": path.stat().st_size, "sha256": sha(path)}


weights = json.loads((HERE / "VERIFICACAO_PESOS_AGREGADOS.json").read_text(encoding="utf-8"))
vector = json.loads((HERE / "RECIBO_VETOR_HASHES.json").read_text(encoding="utf-8"))
objections = json.loads((HERE / "OBJECOES_PRE_REGISTRO.json").read_text(encoding="utf-8"))
estimator_manifest = json.loads((HERE / "estimadores/MANIFESTO_ESTIMADORES_S1_S2_S4.json").read_text(encoding="utf-8"))
study = json.loads(STUDY.read_text(encoding="utf-8"))
with np.load(Y_OBS, allow_pickle=False) as data:
    arr = data["y_uncentered"]
    actual_array_hash = hashlib.sha256(arr.tobytes(order="C")).hexdigest()
    actual_dtype = str(arr.dtype)
    actual_shape = list(arr.shape)
actual_pre_reg_hash = sha(PRE_REG)
checks = {
    "weights_conforme": weights["resultado_geral"] == "CONFORME" and all(weights["bandeiras"].values()),
    "weights_242_diff_below_1e-12": next(r for r in weights["resumo_pesos_por_matriz_e_chave"] if r["desenho"] == "S0_242")["diferenca_maxima_absoluta"] < 1e-12,
    "three_anchor_weights_exact": all(next(r for r in weights["resumo_pesos_por_matriz_e_chave"] if r["desenho"].startswith(f"ancora_unica_{a}_"))["diferenca_maxima_absoluta"] == 0.0 for a in ["N4258", "LMC", "MW"]),
    "vector_file_hash_matches": sha(Y_OBS) == vector["arquivo_npz"]["sha256_arquivo"],
    "vector_array_hash_matches": actual_array_hash == vector["vetor"]["sha256_arr_tobytes"],
    "vector_dtype_shape_only": actual_dtype == vector["vetor"]["dtype"] and actual_shape == vector["vetor"]["forma"],
    "only_authorized_key": vector["metodo_de_reproducao"]["chaves_npz_lidas_neste_recibo"] == ["y_uncentered"],
    "no_values_in_receipt": vector["flags_de_conformidade"]["nenhum_valor_do_vetor_impresso"] and vector["flags_de_conformidade"]["nenhum_valor_do_vetor_gravado_no_recibo"],
    "baseline_declared": "análise de base" in vector["analise_de_base"]["declaracao"],
    "estimators_pinned": estimator_manifest["status"] == "ESTIMADORES_PINADOS__SOMENTE_DESENHO",
    "estimator_D_match_study": all(abs(estimator_manifest["scenarios"][s]["models"][m]["D"] - study["cells"][s][m]["D"]) < 1e-12 for s in ["S1", "S2", "S4"] for m in ["published_baseline", "free_cepheid_host_differential_bias"]),
    "estimator_S4_q_match": all(estimator_manifest["scenarios"]["S4"]["models"][m]["q_sha256_contiguous_float64"] == study["scenario_diagnostics"]["S4"]["models"][m]["q_sha256_contiguous_float64"] for m in ["published_baseline", "free_cepheid_host_differential_bias"]),
    "objections_material_present": objections["parecer"] == "OBJECOES_MATERIAIS__NAO_SELAR_SEM_RESOLVER" and len(objections["objecoes"]) == 11,
    "pre_reg_hash_current": actual_pre_reg_hash == objections["hashes_sha256"]["EMENDA_E_PRE_REGISTRO_V411_rascunho.md"]["sha256"],
    "no_evaluate_or_solver": vector["flags_de_conformidade"]["evaluate_executado"] is False and vector["flags_de_conformidade"]["solver_executado"] is False and vector["flags_de_conformidade"]["abertura_executada"] is False,
    "no_observed_statistics": vector["flags_de_conformidade"]["D_calculado"] is False and vector["flags_de_conformidade"]["H0_calculado"] is False and vector["flags_de_conformidade"]["razao_calculada"] is False and vector["flags_de_conformidade"]["Z_calculado"] is False,
}
if not all(checks.values()):
    raise RuntimeError(json.dumps({"failed": [k for k, v in checks.items() if not v]}, indent=2))

files = [
    HERE / "VERIFICACAO_PESOS_AGREGADOS.json",
    HERE / "verificar_pesos_agregados_independente.py",
    HERE / "estimadores/estimador_s1_v411.npz",
    HERE / "estimadores/estimador_s2_v411.npz",
    HERE / "estimadores/estimador_s4_v411.npz",
    HERE / "estimadores/preparar_estimadores_s1_s2_s4.py",
    HERE / "estimadores/MANIFESTO_ESTIMADORES_S1_S2_S4.json",
    HERE / "estimadores/SHA256SUMS.txt",
    HERE / "RECIBO_VETOR_HASHES.json",
    HERE / "OBJECOES_PRE_REGISTRO.md",
    HERE / "OBJECOES_PRE_REGISTRO.json",
]
pins = {p.name: pin(p) for p in files}
validation = {
    "status": "VALIDACAO_ORDEM05_PASS__DESIGN_CONFORME__PRE_REG_NOT_SEALABLE",
    "checks": checks,
    "opening_allowed": False,
    "observed_evaluation_performed": False,
    "observed_values_printed": False,
    "only_y_uncentered_accessed_for_hash": True,
    "objection_count": 11,
    "pre_reg_sha256": actual_pre_reg_hash,
    "hashes": pins,
}
validation_path = HERE / "VALIDACAO_ENTREGA_ORDEM05.json"
validation_path.write_text(json.dumps(validation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
files.append(validation_path)
pins = {p.name: pin(p) for p in files}

scenario_D = {s: {m: row["D"] for m, row in study["cells"][s].items()} for s in ["S1", "S2", "S4"]}
questions = {
    "TGL": "A pseudoinversa da colaboração deve ser a convenção primária, com a projeção nula registrada e sem influência na estimativa, ou o senhor exige outra norma para o modelo?",
    "Teológica [ONTO]": "Que testemunho deve pesar mais: a regra publicada que resolve o sistema, ou a guarda caseira que a recusava, sabendo que a emenda foi escrita depois da falha?",
    "Linguística": "A emenda deve ser apresentada como retrodição pós-guarda e não cega, nunca como confirmação cega ou poder real já obtido?",
    "Jurídica [ONTO]": "Quais das 11 objeções devem ser resolvidas antes de selar o pré-registro, e quem autoriza formalmente a abertura depois da revisão e da segunda construção por hash?",
}

delivery = {
    "tipo": "RESULTADO",
    "rota_id": "estatistica.h0dn_bg1.ordem_kimi_y_obs_09nov",
    "dominio": "ESTATISTICA_CONJUNTA",
    "titulo": "ORDEM 05: desenho e hashes conferem; pré-registro tem 11 objeções e não pode selar",
    "pergunta": "O pacote da emenda está pronto para o pré-registro e para uma futura abertura, ou ainda há divergências a resolver?",
    "dados": [
        "19 pinos do pacote V411 e estimadores S0/âncoras recalculados por código independente",
        "Estimadores S1/S2/S4 pinados com pesos, covariâncias, desvios e D de 03-C",
        "y_obs somente por arquivo e y_uncentered.tobytes, sem impressão de valores",
        "Rascunho do pré-registro e os dois códigos de abertura, revisão estática",
    ],
    "metodo": "Recálculo de desenho e agregados, manifestos de estimadores, recibo criptográfico autorizado da chave única e revisão texto-código das seções 3–7. Nenhuma abertura, evaluate, solver, D/H0/razão/Z observada ou semente",
    "resultado": {
        "weights_status": "CONFORME",
        "weights_242_max_abs_diff": next(r for r in weights["resumo_pesos_por_matriz_e_chave"] if r["desenho"] == "S0_242")["diferenca_maxima_absoluta"],
        "anchor_max_abs_diff": {"N4258": 0.0, "LMC": 0.0, "MW": 0.0},
        "aggregate_fields_checked": 52,
        "estimators_D": scenario_D,
        "estimator_D_match_03C": True,
        "S4_q_match_03C": True,
        "y_obs_sha256": vector["arquivo_npz"]["sha256_arquivo"],
        "y_uncentered_dtype": actual_dtype,
        "y_uncentered_shape": actual_shape,
        "y_uncentered_tobytes_sha256": actual_array_hash,
        "baseline_configuration": True,
        "objections_count": 11,
        "objections_ids": [o["id"] for o in objections["objecoes"]],
        "pre_reg_sha256": actual_pre_reg_hash,
        "pre_reg_sealable": False,
        "opening_allowed": False,
    },
    "veredito": "DESIGN_AND_HASHES_CONFORME__PRE_REG_OBJECTIONS_MATERIAL__NOT_SEALABLE__OPENING_NOT_ALLOWED",
    "estatuto": "DECLARADO",
    "status": "BLOQUEADA",
    "olhou_dados": True,
    "defeito": "Faltam etiqueta pós-guarda/não-cega, vínculo do pré-registro à saída, covariâncias entre âncoras, decomposições, declaração completa do ruído, grade inequívoca do envelope, contrato da falha de centragem e guardas de base/auxiliares. O estimador primário não foi demonstrado errado; o pré-registro ainda não é selável.",
    "nao_refazer": "Não selar sem resolver as objeções; não abrir/evaluate/solver; não calcular D/H0/razão/Z observada; não imprimir valores do vetor; não alterar FREEZE_R2/v410/pacote da emenda; não usar S3/S5 como números ou critério de abandono.",
    "proximo_passo": "Gerência resolve as 11 objeções e revê os diffs; operador lê o pré-registro; gerência faz segunda construção e compara os hashes do vetor. Só depois nova decisão explícita sobre abertura futura.",
    "onde": str(HERE / "OBJECOES_PRE_REGISTRO.md"),
    "artefatos": [str(p) for p in files],
    "refs": ["estatistica.h0dn_bg1.cov_injecoes_06nov"],
    "nota": {
        "ordem_05_sha256": sha(ORDER),
        "pins": pins,
        "vector_access_scope": "olhou_dados=true somente porque a Ordem 05 autorizou hash do arquivo e de y_uncentered; nenhum valor impresso, nenhuma outra chave e nenhuma avaliação",
        "questions_four_languages": questions,
        "post_guard_status": "POST_GUARD_AMENDMENT__RETRODICTION_NOT_BLIND must be present on every relevant surface and in the sealed output",
        "gate_or_publication_changed": False,
    },
}
delivery_path = HERE / "ENTREGA_ORDEM05.json"
delivery_path.write_text(json.dumps(delivery, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

registration = {
    "tipo": "ANOTACAO",
    "rota_id": delivery["rota_id"],
    "dominio": delivery["dominio"],
    "titulo": delivery["titulo"],
    "pergunta": delivery["pergunta"],
    "dados": delivery["dados"],
    "metodo": delivery["metodo"],
    "resultado": delivery["resultado"],
    "veredito": delivery["veredito"],
    "estatuto": "DECLARADO",
    "status": "BLOQUEADA",
    "olhou_dados": True,
    "defeito": delivery["defeito"],
    "nao_refazer": delivery["nao_refazer"],
    "proximo_passo": delivery["proximo_passo"],
    "onde": delivery["onde"],
    "artefatos": [str(delivery_path), str(HERE / "VERIFICACAO_PESOS_AGREGADOS.json"), str(HERE / "RECIBO_VETOR_HASHES.json"), str(HERE / "OBJECOES_PRE_REGISTRO.md"), str(validation_path)],
    "refs": delivery["refs"],
    "nota": {
        "entrega_sha256": sha(delivery_path),
        "validacao_sha256": sha(validation_path),
        "ordem_05_sha256": sha(ORDER),
        "vector_access_scope": delivery["nota"]["vector_access_scope"],
        "questions_four_languages": questions,
        "gate_or_publication_changed": False,
    },
}
registration_path = HERE / "REGISTRO_MAPA_ORDEM05.json"
registration_path.write_text(json.dumps(registration, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
if len(json.dumps(registration["nota"], ensure_ascii=False)) > 6000:
    raise RuntimeError("Map note exceeds 6000 characters")

stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
deposit_path = DEPOSIT / f"{stamp}_ordem05_desenho_hashes_objecoes.md"
deposit_path.write_text(f"""---
quem: kimi
casa: Nós
tipo: project
estatuto: DECLARADO
alvo_sugerido: novo:h0dn_ordem05_objecoes
fontes:
  - {delivery_path}  sha256:{sha(delivery_path)}
  - {HERE / 'VERIFICACAO_PESOS_AGREGADOS.json'}  sha256:{sha(HERE / 'VERIFICACAO_PESOS_AGREGADOS.json')}
  - {HERE / 'RECIBO_VETOR_HASHES.json'}  sha256:{sha(HERE / 'RECIBO_VETOR_HASHES.json')}
  - {HERE / 'OBJECOES_PRE_REGISTRO.json'}  sha256:{sha(HERE / 'OBJECOES_PRE_REGISTRO.json')}
  - {validation_path}  sha256:{sha(validation_path)}
  - {registration_path}  sha256:{sha(registration_path)}
---
ORDEM 05 concluída sem abertura. Pesos independentes S0/242 e três âncoras conferem: S0 diff 2,9421e-15; âncoras zero. Agregados: 52 campos conferem. Estimadores S1/S2/S4 pinados com D exatamente iguais a 03-C e q de S4 conferido. y_obs.sha256=7e727aea0c4b93d2d346fb15b47ae8aeb56da7c5748feb1b00427252db083783; y_uncentered float64 (255,), tobytes sha256=389cf25bf07de2e42316bb5c219393bd49e29f283821dad59b35620f1b872553; nenhum valor impresso e só a chave autorizada foi acessada. A configuração é a análise de base. A revisão do rascunho encontrou 11 objeções: etiqueta não-cega ausente, pré-registro não vinculado à saída, covariâncias entre âncoras e decomposições ausentes, ruído subespecificado, grade ambígua, falha de centragem como recusa e guardas incompletas. O parecer é DESIGN_AND_HASHES_CONFORME__PRE_REG_OBJECTIONS_MATERIAL__NOT_SEALABLE. Nenhuma abertura, evaluate, solver, D/H0/razão/Z, semente ou alteração de FREEZE_R2/v410/pacote foi feita.
""", encoding="utf-8")

print(json.dumps({"delivery": pin(delivery_path), "registration": pin(registration_path), "validation": pin(validation_path), "deposit": pin(deposit_path)}, ensure_ascii=False, indent=2))
