from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ORDER = HERE.parents[1] / "ORDEM_KIMI_H0DN_03C_11nov.md"
DEPOSIT = Path(r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\fila\depositos\kimi")


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pin(path: Path) -> dict:
    return {"path": str(path), "bytes": path.stat().st_size, "sha256": sha(path)}


study = json.loads((HERE / "ESTUDO_CONDICIONAL_R3B.json").read_text(encoding="utf-8"))
core_validation = json.loads((HERE / "VALIDACAO_CORE_R3B.json").read_text(encoding="utf-8"))
fixtures = json.loads((HERE / "MONTAGEM_FIXTURES_SINTETICOS.json").read_text(encoding="utf-8"))
anchor = json.loads((HERE / "ANCORA_R3B.json").read_text(encoding="utf-8"))
cell_count = sum(len(models) for models in study["cells"].values())
invalid_count = sum(1 for models in study["cells"].values() for row in models.values() if row["conditional_status"] == "INVALID_SCENARIO_NOT_A_NUMBER")
checks = {
    "anchor_pass": anchor["status"] == "ANCORA_R3B_PASS" and all(r["within_1e-6"] for r in anchor["anchors"].values()),
    "core_validation_pass": core_validation["status"] == "VALIDACAO_CORE_R3B_PASS",
    "twelve_cells": cell_count == 12,
    "eight_numeric_four_invalid": invalid_count == 4 and cell_count - invalid_count == 8,
    "S3_S5_invalid_not_invented": all(study["cells"][s][m]["conditional_status"] == "INVALID_SCENARIO_NOT_A_NUMBER" for s in ["S3", "S5"] for m in ["published_baseline", "free_cepheid_host_differential_bias"]),
    "S4_orientation_corrected": study["scenario_definitions"]["S4"].startswith("S1 with analytic global minimum D over q C_BG^-1 q^T<=C_L"),
    "three_global_outputs": len(study["GLOBAL_outputs_by_threshold"]) == 3,
    "global_outputs_beta": all(r["GLOBAL_output"] == "BETA__VALE_FECHAR" for r in study["GLOBAL_outputs_by_threshold"]),
    "no_alpha_certificate": all(not r["conservative_joint_rule_power_certificate"] for r in study["GLOBAL_outputs_by_threshold"]),
    "free_cepheid_does_not_reach_6_282": study["four_answers"]["1_free_cCep_S0_or_S1_reaches_6_282"]["answer"] is False,
    "scalar_route_present_not_primary": study["scalar_public_route_S_E"]["route"] == "PARALLEL_DECLARED_NOT_INDEPENDENT_REPLICA" and not study["scalar_public_route_S_E"]["primary_route_selected"],
    "lemma_proved_with_precisions": study["lemma_B6"]["status"] == "PROVED_WITH_STATED_PRECISIONS",
    "fixtures_R22_scope_explicit": fixtures["routine_scope"]["full_255_row_observed_network_rebuilt"] is False and fixtures["routine_scope"]["solver_called"] is False,
    "fixtures_no_observed": fixtures["observed_vector_read"] is False and fixtures["observed_support_tests"] == 0,
    "opening_blocked": study["opening_allowed"] is False and anchor["opening_allowed"] is False and core_validation["opening_allowed"] is False,
    "no_forbidden_execution": all(not study["execution_guards"][key] for key in ["observed_data_used", "observed_support_test_used", "observed_Z_t_h_or_ratio_computed", "evaluator_called", "observed_solver_called", "RNG_or_Monte_Carlo_used", "FREEZE_R2_modified", "v410_modified", "best_scenario_selected"]),
}
if not all(checks.values()):
    raise RuntimeError(json.dumps({"failed": [k for k, v in checks.items() if not v]}, indent=2))

review = """# Revisão independente do estudo R3B

**Estado:** `CONDICIONAL_APTO__ERRATA_S4_APLICADA__NAO_E_CERTIFICADO`

A auditoria matemática independente verificou a âncora, o mapa S0–S5, a substituição G42, CAP13, a rejeição não PSD de S3, a minimização global de S4, os orçamentos, a família sigma_b, S_E, o lema e a saída global por limiar.

Foi encontrada apenas uma transposição textual na definição de S4. A restrição correta é `q C_BG^-1 q^T <= C_L`; o cálculo numérico já usava essa orientação no resíduo de Schur. A descrição foi corrigida em `core_r3b.py`, o estudo foi regenerado e a validação voltou a passar sem alteração de D. A errata está preservada em `ERRATA_S4_Q_TRANSPOSE_R3B.md`.

Após a correção, o revisor não identificou impedimento matemático ao estudo **como condicional**. Não há prova física completa de Loewner nem certificado de poder, e `opening_allowed=false` permanece.
"""
review_path = HERE / "REVISAO_INDEPENDENTE_R3B.md"
review_path.write_text(review, encoding="utf-8")

main_files = [
    HERE / "core_r3b.py",
    HERE / "ANCORA_R3B.json",
    HERE / "ESTUDO_CONDICIONAL_R3B.json",
    HERE / "VALIDACAO_CORE_R3B.json",
    HERE / "A1_HIPOTESES_DO_VETOR.md",
    HERE / "PRODUTOS_A_PEDIR.md",
    HERE / "FONTES_CEFEIDAS_DOCUMENTAL.md",
    HERE / "MONTAGEM_FIXTURES_SINTETICOS.json",
    HERE / "fixtures/validate_synthetic_assembly.py",
    HERE / "PROTOCOLO_CONFERENCIA_FUTURA.md",
    HERE / "ERRATA_S4_Q_TRANSPOSE_R3B.md",
    review_path,
]
validation = {
    "status": "VALIDACAO_ENTREGA_R3B_PASS__CONDICIONAL__NAO_E_CERTIFICADO",
    "order_sha256": sha(ORDER),
    "checks": checks,
    "cell_count": cell_count,
    "invalid_cell_count": invalid_count,
    "global_outputs": study["GLOBAL_outputs_by_threshold"],
    "observed_vector_read": False,
    "observed_support_tests": 0,
    "new_seed_count": 0,
    "opening_allowed": False,
    "hashes": {p.name: pin(p) for p in main_files},
}
validation_path = HERE / "VALIDACAO_ENTREGA_R3B.json"
validation_path.write_text(json.dumps(validation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
main_files.append(validation_path)
pins = {p.name: pin(p) for p in main_files}

cells = {s: {m: {"D": row["D"], "conditional_power": row["conditional_design_power_Phi_D_minus_5"], "status": row["conditional_status"]} for m, row in models.items()} for s, models in study["cells"].items()}
questions = {
    "TGL": "Com S0 publicado em D=6,710151, mas Cefeida livre em 5,191312 e G42 reduzindo D, qual modelo e qual portão o senhor escolhe para fechar: o baseline publicado ou a robustez, e por qual fundamento físico?",
    "Teológica [ONTO]": "Que testemunho deve orientar o primário: a covariância publicada que alcança os três limiares ou a robustez Cefeida livre que não os alcança, sabendo que nenhuma cota certifica ainda?",
    "Linguística": "Podemos nomear S0 publicado como candidato condicional primário, S_E como paralela e Cefeida livre como robustez, sem chamar nenhum deles de poder real antes da revisão?",
    "Jurídica [ONTO]": "O senhor ratifica D≥6,282 e EXTRA13_OUT para continuar, ou exige os produtos internos dos 13 e a robustez Cefeida livre antes de qualquer novo congelamento? A escolha será registrada como feita com a tabela à vista.",
}

delivery = {
    "tipo": "RESULTADO",
    "rota_id": "estatistica.h0dn_bg1.ordem_kimi_y_obs_09nov",
    "dominio": "ESTATISTICA_CONJUNTA",
    "titulo": "03-C executada: âncora exata e estudo condicional aponta VALE FECHAR, sem certificado",
    "pergunta": "O desenho H0DN × BG1 pode alcançar poder real, e quais produtos são necessários para fechá-lo sem esconder suas incertezas?",
    "dados": [
        "A1/eigensuporte reproduziu os dois D FREEZE_R2 com erro <=1e-6",
        "Matrizes públicas H0DN, G42 STATONLY, BG1 e fontes documentais pinadas",
        "Fixtures exclusivamente sintéticos R22; nenhum vetor observado lido",
    ],
    "metodo": "Álgebra GLS/eigensuporte, 12 células condicionais, orçamentos disjuntos, família sigma_b, S_E, lema B6, fixtures R22 e três saídas globais por limiar. Sem RNG, Monte Carlo, suporte observado ou seleção de melhor cenário.",
    "resultado": {
        "status": "ESTUDO_DE_DESENHO_CONDICIONAL__NAO_E_CERTIFICADO",
        "anchor": "ANCORA_R3B_PASS",
        "cells": cells,
        "global_outputs_by_threshold": study["GLOBAL_outputs_by_threshold"],
        "free_cCep_S0_or_S1_reaches_6_282": False,
        "G42_delta_D": study["isolated_effects"]["published_baseline"]["S0_to_S1_G42_STATONLY_substitution"]["delta_D"],
        "G42_delta_D_free": study["isolated_effects"]["free_cepheid_host_differential_bias"]["S0_to_S1_G42_STATONLY_substitution"]["delta_D"],
        "CAP13_delta_D": study["isolated_effects"]["published_baseline"]["S1_to_S2_EXTRA13_IN_CAP13"]["delta_D"],
        "S4_delta_D": study["isolated_effects"]["published_baseline"]["envelope_changes_from_S1"]["S4_delta_D"],
        "S3_S5": "INVALID_SCENARIO_NOT_A_NUMBER",
        "S_E": study["scalar_public_route_S_E"],
        "family_sigma_b": study["cepheid_sigma_b_family"],
        "lemma_B6": study["lemma_B6"]["status"],
        "full_physical_covariance_closed": False,
        "alpha_certificate": False,
        "opening_allowed": False,
    },
    "veredito": "ESTUDO_CONDICIONAL__BETA_VALE_FECHAR__NO_ALPHA_NO_CERTIFICATE__OPENING_NOT_ALLOWED",
    "estatuto": "DECLARADO",
    "status": "BLOQUEADA",
    "olhou_dados": False,
    "defeito": "S0 publicado supera os três limiares, mas Cefeida livre não alcança 6,282; G42 reduz D; não há dominação completa de Loewner nem certificado. S3 não é PSD e S5 não foi calculado. A2–A6 e a montagem observada continuam abertos.",
    "nao_refazer": "Não produzir D para S3/S5; não promover beta a certificado; não usar S5 como abandono; não abrir y_obs, gerar sementes, alterar FREEZE_R2/v410 ou escolher modelo/variante pelo D.",
    "proximo_passo": "Operador escolhe modelo primário, portão e EXTRA13_OUT com a tabela à vista; gerência revisa; produtos em PRODUTOS_A_PEDIR.md. Só variante admitida e revista pode avançar para certificado e eventual abertura futura.",
    "onde": str(HERE / "ESTUDO_CONDICIONAL_R3B.json"),
    "artefatos": [str(p) for p in main_files],
    "refs": ["estatistica.h0dn_bg1.cov_injecoes_06nov", "d1.fase9.v2_c1_a_unica_palavra_23out"],
    "nota": {
        "ordem_03C_sha256": sha(ORDER),
        "pins": pins,
        "operator_threshold_fixed_before_execution": False,
        "operator_choice_must_disclose_table_in_view": True,
        "questions_four_languages": questions,
        "fixture_scope": "Complete synthetic R22 subsystem: 149 equations/39 parameters; not the observed 255-row network and no observed conference",
        "errata_S4": "Text corrected to q C_BG^-1 q^T; numerical Schur residual was already correct and D is unchanged",
        "observed_accounting": "Previous observed receipts remain counted; this study adds zero observed reads and zero support tests",
        "gate_or_publication_changed": False,
    },
}
delivery_path = HERE / "ENTREGA_ORDEM03B.json"
delivery_path.write_text(json.dumps(delivery, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

registration = {
    "tipo": "ANOTACAO",
    "rota_id": delivery["rota_id"],
    "dominio": delivery["dominio"],
    "titulo": delivery["titulo"],
    "pergunta": delivery["pergunta"],
    "dados": delivery["dados"],
    "metodo": delivery["metodo"],
    "resultado": {
        "anchor": "PASS",
        "cells": cells,
        "global_outputs_by_threshold": study["GLOBAL_outputs_by_threshold"],
        "S_E_D_independence": study["scalar_public_route_S_E"]["D_independence"],
        "S_E_D_Schur": study["scalar_public_route_S_E"]["D_Schur"],
        "alpha_certificate": False,
        "opening_allowed": False,
    },
    "veredito": delivery["veredito"],
    "estatuto": "DECLARADO",
    "status": "BLOQUEADA",
    "olhou_dados": False,
    "defeito": delivery["defeito"],
    "nao_refazer": delivery["nao_refazer"],
    "proximo_passo": delivery["proximo_passo"],
    "onde": delivery["onde"],
    "artefatos": [str(delivery_path), str(HERE / "ESTUDO_CONDICIONAL_R3B.json"), str(validation_path), str(review_path)],
    "refs": delivery["refs"],
    "nota": {
        "entrega_sha256": sha(delivery_path),
        "estudo_sha256": sha(HERE / "ESTUDO_CONDICIONAL_R3B.json"),
        "validacao_entrega_sha256": sha(validation_path),
        "ordem_03C_sha256": sha(ORDER),
        "operator_choice_must_disclose_table_in_view": True,
        "questions_four_languages": questions,
        "gate_or_publication_changed": False,
    },
}
registration_path = HERE / "REGISTRO_MAPA_ORDEM03C.json"
registration_path.write_text(json.dumps(registration, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
if len(json.dumps(registration["nota"], ensure_ascii=False)) > 6000:
    raise RuntimeError("Map note exceeds 6000 characters")

stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
deposit_path = DEPOSIT / f"{stamp}_ordem03c_estudo_condicional.md"
deposit_path.write_text(f"""---
quem: kimi
casa: Nós
tipo: project
estatuto: DECLARADO
alvo_sugerido: novo:h0dn_ordem03c_resultado
fontes:
  - {delivery_path}  sha256:{sha(delivery_path)}
  - {HERE / 'ESTUDO_CONDICIONAL_R3B.json'}  sha256:{sha(HERE / 'ESTUDO_CONDICIONAL_R3B.json')}
  - {validation_path}  sha256:{sha(validation_path)}
  - {registration_path}  sha256:{sha(registration_path)}
---
A ORDEM 03-C foi executada apenas por álgebra condicional. A âncora reproduziu os dois D FREEZE_R2 com erro <=1e-6. S0 publicado: 6,710151; S1 publicado: 5,489825; S2: 5,527887; S4: 4,378058; Cefeida livre: 5,191312, 4,743268, 4,773510 e 3,871970. S3 é não PSD e S5 não foi calculado. S_E: 6,782652 sob independência nomeada e 5,219741 sob Schur. A saída GLOBAL é BETA__VALE_FECHAR nos limiares 5,842, 6,282 e 6,645, sem ALPHA e sem certificado. A escolha posterior do primário e do portão deve declarar a tabela à vista. Fixtures R22 completos para o subsistema sintético exigido; nenhum vetor observado, suporte, semente ou Monte Carlo. Errata S4 q C_BG^-1 q^T aplicada sem mudar D. FREEZE_R2, v410, gate e publicação permanecem intocados.
""", encoding="utf-8")

print(json.dumps({"delivery": pin(delivery_path), "registration": pin(registration_path), "validation": pin(validation_path), "review": pin(review_path), "deposit": pin(deposit_path)}, ensure_ascii=False, indent=2))
