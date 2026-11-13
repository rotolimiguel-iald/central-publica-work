from __future__ import annotations

import hashlib
import json
from datetime import datetime
from pathlib import Path

HERE = Path(__file__).resolve().parent
ORDER = HERE.parents[1] / "ORDEM_KIMI_H0DN_04_11nov.md"
BASE = HERE.parents[2] / "astra_bell_fock_tt_05nov" / "h0dn_bg1_06nov"
DEPOSIT = Path(r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory\fila\depositos\kimi")
HOSTS = [
    "N7250", "N4536", "N3972", "N4424", "N4639", "N4038", "M101",
    "N2442", "N1365", "N5643", "N5584", "N1559", "N5468", "N1448",
    "N2525", "N3370", "N5861", "N3147", "N3021", "N1309", "N3982",
    "N1015", "N3447", "N5917", "U9391", "N3583", "N2608", "N7541",
    "N0691", "N3254", "N5728", "N7678", "M1337", "N4680", "N7329",
    "N0976", "N0105",
]
ANCHORS = ["N4258", "LMC", "MW"]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pin(path: Path) -> dict:
    return {"path": str(path), "bytes": path.stat().st_size, "sha256": sha(path)}


manifest = {
    "schema": "H0DN_VARIANT_MANIFEST_INCOMPLETE_V1",
    "manifest_status": "INCOMPLETE_NOT_AUTHORIZED",
    "manifest_immutable": False,
    "stage1_complete": False,
    "variant_id": "H0DN_PUBLICADO_REDUZIDO_183__EXTRA13_OUT__raw_MAS",
    "operator_authorization_and_sha256": None,
    "vector_path_and_sha256": None,
    "observed_vector_read": False,
    "row_map_path_and_sha256": str(BASE / "network/rows.json") + "#" + sha(BASE / "network/rows.json"),
    "source_fits_and_versions": [
        {"source": "H0DN_paper_v1.html", "citation": "R22a fits 9,10,11", "status": "UNRESOLVED_AGAINST_R22"},
        {"source": "R22 Table 5 p.28", "mapping": {"fit 9": "none", "fit 10": "N4258", "fit 11": "Milky Way", "fit 12": "LMC"}, "status": "PUBLIC_BUT_CELL_MAP_NOT_CLOSED"},
    ],
    "center_convention": "raw_MAS",
    "raw_MAS_proof": {
        "equations.py": "334-345: yval is copied from mu_host; 348-376: covariance only",
        "org_v3p9.pro": "1410-1417: anchor and host-anchor difference are already combined in mu_host2_value",
        "mas_ref_value_added_or_subtracted": False,
    },
    "reference_host": "N7250",
    "anchor_order": ANCHORS,
    "host_order": HOSTS,
    "cell_precision": {
        f"{host}|{anchor}": {
            "least_significant_unit": 0.001,
            "decimal_places": 3,
            "quantization_rule": "OPEN",
        }
        for anchor in ANCHORS for host in HOSTS
    },
    "quantization_rule": "OPEN",
    "identity_tolerances": "NOT_AUTHORIZED",
    "conditional_tolerance_formula_not_adopted": {
        "requires_primary_proof_of_symmetric_rounding": True,
        "b_per_cell_if_proven": 0.0005,
        "tau_each_of_72_if_proven": 0.002000000000001,
        "currently_adopted": False,
    },
    "numeric_tolerance": 1e-12,
    "covariance_public": {
        "geometric_anchor_errors": {"N4258": 0.032, "LMC": 0.024, "MW": 0.020},
        "source": str(BASE / "network/upstream/data/anchors.dat"),
        "sha256": sha(BASE / "network/upstream/data/anchors.dat"),
    },
    "code_sha256": sha(HERE / "montar_variante.py"),
    "fixture_validation_sha256": sha(HERE / "VALIDACAO_FIXTURES.json"),
    "protocol_sha256": "db74c3f866128276361abd932af721394126615903a899a8dae1880099e566f8",
    "route_name": "estatistica.h0dn_bg1.ordem_kimi_y_obs_09nov",
    "route_sequence_number": "PENDING_STAGE2",
    "stage2_authorized": False,
    "opening_allowed": False,
    "production_execution": "REFUSED_BY_GUARD",
    "open_documentary_requirements": [
        "Full 111-cell map to the R22 fit centers, with version and parameter index",
        "Resolution of H0DN fits 9,10,11 versus R22 fits 10,11,12",
        "Equation or full-precision product proving the shared HMS center plus anchor offset",
        "Documented quantization rule or full-precision centers",
        "Seventy-two production tolerances derived only after those sources",
        "Management review and explicit operator authorization for Stage 2",
    ],
}
manifest_path = HERE / "MANIFESTO_VARIANTE.json"
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

fixtures = json.loads((HERE / "VALIDACAO_FIXTURES.json").read_text(encoding="utf-8"))
checks = {
    "manifest_incomplete_not_authorized": manifest["manifest_status"] == "INCOMPLETE_NOT_AUTHORIZED" and not manifest["manifest_immutable"],
    "raw_MAS": manifest["center_convention"] == "raw_MAS" and not manifest["raw_MAS_proof"]["mas_ref_value_added_or_subtracted"],
    "111_cell_precisions": len(manifest["cell_precision"]) == 111 and all(p["least_significant_unit"] == 0.001 and p["decimal_places"] == 3 for p in manifest["cell_precision"].values()),
    "quantization_open": manifest["quantization_rule"] == "OPEN",
    "tolerances_not_authorized": manifest["identity_tolerances"] == "NOT_AUTHORIZED",
    "stage1_not_complete": manifest["stage1_complete"] is False,
    "stage2_blocked": manifest["stage2_authorized"] is False and manifest["opening_allowed"] is False,
    "no_vector": manifest["observed_vector_read"] is False and manifest["vector_path_and_sha256"] is None,
    "fixtures_pass_not_admission": fixtures["status"] == "FIXTURES_PASS__VARIANT_NOT_ADMITTED" and fixtures["variant_admitted"] is False,
    "fixtures_72_pass": fixtures["execution"]["raw_72_residual_max_abs_mag"] < 1e-12 and fixtures["execution"]["A_theta_72_residual_max_abs_mag"] == 0.0,
    "fixtures_rank": fixtures["execution"]["R22_covariance_rank"] == 39 and fixtures["execution"]["R22_covariance_nullity"] == 72 and fixtures["execution"]["constraint_rank"] == 72,
    "fixtures_exclusions": fixtures["execution"]["exclusions"]["excluded_N4151_rows"] == 3 and fixtures["execution"]["exclusions"]["excluded_MAS_self_reference_rows"] == 3,
    "no_projection": fixtures["execution"]["checks"]["no_projection_or_jitter"],
    "guards_refuse_production": all(fixtures["execution"]["production_guard_unit_tests"].values()),
    "no_observed": fixtures["observed_vector_read"] is False and fixtures["observed_support_tests"] == 0,
}
if not all(checks.values()):
    raise RuntimeError(json.dumps({"failed": [k for k, v in checks.items() if not v]}, indent=2))
validation = {
    "status": "VALIDACAO_ORDEM04_PASS__STAGE1_INCOMPLETE__STAGE2_NOT_AUTHORIZED",
    "checks": checks,
    "raw_MAS": True,
    "stage1_complete": False,
    "stage2_authorized": False,
    "opening_allowed": False,
    "observed_vector_read": False,
    "observed_support_tests": 0,
}
validation_path = HERE / "VALIDACAO_ENTREGA_ORDEM04.json"
validation_path.write_text(json.dumps(validation, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

files = [HERE / "RECONSTRUCAO_DOCUMENTAL_A1.md", manifest_path, HERE / "montar_variante.py", HERE / "VALIDACAO_FIXTURES.json", HERE / "LINHAS_DE_ESTRESSE.md", validation_path]
pins = {p.name: pin(p) for p in files}
questions = {
    "TGL": "Qual produto full-precision e qual mapa de centros demonstram a decomposição ε_k+o_a e permitem fixar as tolerâncias sem criar variância?",
    "Teológica [ONTO]": "Que testemunha documental pode certificar que os três centros pertencem à mesma medida compartilhada, sem corrigi-los até coincidir?",
    "Linguística": "A convenção raw_MAS, que copia o centro sem nova soma ou subtração MAS, é a que o senhor confirma para esta variante?",
    "Jurídica [ONTO]": "Que prova de proveniência e quantização o senhor aceita para completar o manifesto e autorizar a única conferência da Etapa 2?",
}

delivery = {
    "tipo": "RESULTADO",
    "rota_id": "estatistica.h0dn_bg1.ordem_kimi_y_obs_09nov",
    "dominio": "ESTATISTICA_CONJUNTA",
    "titulo": "ORDEM 04 Etapa 1: raw_MAS decidido; manifesto incompleto e Etapa 2 bloqueada",
    "pergunta": "A cadeia pública basta para montar a variante raw_MAS e autorizar a conferência das 72 identidades?",
    "dados": [
        "H0DN/R22 public code and host_data line map",
        "R22 Data Release compact products and fit-numbering discrepancy",
        "Synthetic R22 fixtures only; no observed vector or observed output",
    ],
    "metodo": "Documentary reconstruction, raw_MAS proof, explicit 37x3 selection, synthetic fixtures and production guards. No solver, evaluate, D/H0/ratio, seeds or observed support test",
    "resultado": {
        "center_convention": "raw_MAS",
        "raw_MAS_source_proof": True,
        "fixtures_status": "FIXTURES_PASS__VARIANT_NOT_ADMITTED",
        "raw_72_residual_max_abs_mag": fixtures["execution"]["raw_72_residual_max_abs_mag"],
        "A_theta_72_residual_max_abs_mag": 0.0,
        "R22_covariance_rank": 39,
        "R22_covariance_nullity": 72,
        "cell_precision_least_significant_unit": 0.001,
        "quantization_rule": "OPEN",
        "fit_center_bridge": "OPEN",
        "identity_tolerances": "NOT_AUTHORIZED",
        "manifest_status": "INCOMPLETE_NOT_AUTHORIZED",
        "stage1_complete": False,
        "stage2_authorized": False,
        "opening_allowed": False,
    },
    "veredito": "RAW_MAS_DECIDED__STAGE1_INCOMPLETE__STAGE2_NOT_AUTHORIZED",
    "estatuto": "DECLARADO",
    "status": "BLOQUEADA",
    "olhou_dados": False,
    "defeito": "Faltam a ponte completa dos 111 centros aos fits, a prova do centro HMS compartilhado e a regra de quantização/full precision. Três casas decimais estão verificadas, mas q/2 não será presumido; as 72 tolerâncias e o manifesto final não podem ser congelados.",
    "nao_refazer": "Não usar q/2 sem fonte; não escolher convenção pelo resultado histórico; não abrir vetor, reproduzir H0, calcular D/razão, gerar sementes, alterar FREEZE_R2/v410/gate ou executar Etapa 2.",
    "proximo_passo": "Operador decide se envia os pedidos às fontes. Obter mapa full-precision dos centros, prova do HMS e regra de quantização; gerência revisa o manifesto completo e só depois o operador autoriza a Etapa 2.",
    "onde": str(manifest_path),
    "artefatos": [str(p) for p in files],
    "refs": ["estatistica.h0dn_bg1.cov_injecoes_06nov"],
    "nota": {
        "ordem_04_sha256": sha(ORDER),
        "pins": pins,
        "conditional_tolerance_not_adopted": 0.002000000000001,
        "reason_not_adopted": "Only conditional on primary proof of symmetric rounding; quantization remains OPEN",
        "questions_four_languages": questions,
        "observed_accounting": "Zero observed reads and zero observed conferences in this order",
        "gate_or_publication_changed": False,
    },
}
delivery_path = HERE / "ENTREGA_ORDEM04.json"
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
    "olhou_dados": False,
    "defeito": delivery["defeito"],
    "nao_refazer": delivery["nao_refazer"],
    "proximo_passo": delivery["proximo_passo"],
    "onde": delivery["onde"],
    "artefatos": [str(delivery_path), str(manifest_path), str(validation_path)],
    "refs": delivery["refs"],
    "nota": {
        "entrega_sha256": sha(delivery_path),
        "manifesto_sha256": sha(manifest_path),
        "validacao_sha256": sha(validation_path),
        "ordem_04_sha256": sha(ORDER),
        "questions_four_languages": questions,
        "gate_or_publication_changed": False,
    },
}
registration_path = HERE / "REGISTRO_MAPA_ORDEM04.json"
registration_path.write_text(json.dumps(registration, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
if len(json.dumps(registration["nota"], ensure_ascii=False)) > 6000:
    raise RuntimeError("Map note exceeds 6000 characters")

stamp = datetime.now().strftime("%Y%m%d_%H%M%S")
deposit_path = DEPOSIT / f"{stamp}_ordem04_raw_mas_stage1_incomplete.md"
deposit_path.write_text(f"""---
quem: kimi
casa: Nós
tipo: project
estatuto: DECLARADO
alvo_sugerido: novo:h0dn_ordem04_raw_mas
fontes:
  - {delivery_path}  sha256:{sha(delivery_path)}
  - {manifest_path}  sha256:{sha(manifest_path)}
  - {validation_path}  sha256:{sha(validation_path)}
  - {registration_path}  sha256:{sha(registration_path)}
---
Etapa 1 da ORDEM 04: a fonte decidiu raw_MAS: mu_host é copiado sem somar/subtrair mas_ref_value, pois âncora e diferença já estão reunidas no centro publicado. Os fixtures passaram: 72/72 identidades brutas e 72/72 em y=Aθ, posto R22 39/nulidade 72, N4151 e autorreferências MAS excluídos, sem projeção/jitter. A Etapa 1 NÃO está completa: faltam a ponte dos 111 centros aos fits R22, a prova do centro HMS compartilhado e a regra de quantização/full precision. As células têm três casas decimais, mas q/2 não será presumido; as tolerâncias estão NOT_AUTHORIZED e o manifesto é INCOMPLETE_NOT_AUTHORIZED. Etapa 2 e abertura continuam bloqueadas. Nenhum vetor observado, saída observada, solver, evaluate, D/H0/razão, semente, alteração de FREEZE_R2/v410/gate foi usado.
""", encoding="utf-8")

print(json.dumps({"delivery": pin(delivery_path), "manifest": pin(manifest_path), "validation": pin(validation_path), "registration": pin(registration_path), "deposit": pin(deposit_path)}, ensure_ascii=False, indent=2))
