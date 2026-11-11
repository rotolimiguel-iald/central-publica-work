from __future__ import annotations

import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ARCH = HERE / "fontes_primarias"
UP = Path(r"C:\IALD\Central de Patentes\work\astra_bell_fock_tt_05nov\h0dn_bg1_06nov\network\upstream\data")
IDS = ["2011iv", "2007on", "2021rhu", "1980N", "1981D", "2006dd", "1998bu", "1989B", "1994D", "1992A", "ASASSN-14lp", "2021J", "2020nvb"]


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pin(path: Path) -> dict:
    return {"path": str(path), "sha256": sha(path), "bytes": path.stat().st_size}


# CID, SN line, SN sigma, host, host line, host sigma, method, source, MAS, MAS line, MAS sigma, group line, sources, recoverable, missing
ROWS = [
    ("2011iv", 44, 0.10, "N1404", 466, 0.034, "trgb_jwst", "A25", "trgb_jwst&N4258&A25", 463, 0.05, 19, ["gall2018", "newman2025"], "Gall tabelas F.1–F.5; erro instrumental+zero-point noturno; sistemáticos SNooPy; TRGB posterior.", "Matriz completa entre os dois eventos e entre fotometria/modelo/distância; covariância UVOT recíproca não tabulada."),
    ("2007on", 45, 0.19, "N1404", 466, 0.034, "trgb_jwst", "A25", "trgb_jwst&N4258&A25", 463, 0.05, 19, ["gall2018", "newman2025"], "Mesma fonte Gall; host e sequência locais compartilhados com 2011iv; TRGB posterior.", "Matriz completa; imagens UVOT usadas reciprocamente na subtração de host impedem presumir independência."),
    ("2021rhu", 46, 0.15, "N7814", 295, 0.07, "trgb_hst", "Ex", "trgb_hst&N4258&Ex", 294, 0.04, None, ["dhawan2022", "harvey2023"], "Dhawan tabela 1 com orçamento TRGB; Harvey tabela A1 com fotometria ZTF/Swift.", "SALT2 fornece erro marginal via covariância, mas a matriz entre mB,x1,c não é tabelada; sem covariância com as demais SNe."),
    ("1980N", 47, 0.15, "N1316", 276, 0.04, "trgb_hst", "CCHP", "trgb_hst&N4258&CCHP", 273, 0.04, None, ["hamuy1991", "elias1981", "stritzinger2010"], "Fotometria óptica/IR e erros parciais; análise posterior em Stritzinger.", "Sem matriz entre épocas/filtros, máximo, extinção e modelo; erros IR percentuais não são mag."),
    ("1981D", 48, 0.23, "N1316", 276, 0.04, "trgb_hst", "CCHP", "trgb_hst&N4258&CCHP", 273, 0.04, None, ["hamuy1991", "elias1981", "stritzinger2010"], "Erros por ponto incluem fundo; Stritzinger refaz fundo com dados modernos.", "Sistemas fotométricos/fundo/extinção sem covariância conjunta; não combinar reduções como independentes."),
    ("2006dd", 49, 0.11, "N1316", 276, 0.04, "trgb_hst", "CCHP", "trgb_hst&N4258&CCHP", 273, 0.04, None, ["stritzinger2010"], "Tabelas 3–5; erros fotométricos e orçamento por método; covariância do ajuste é usada no artigo.", "A matriz numérica completa do ajuste e as cadeias/produtos internos não estão publicados; algumas independências são hipóteses."),
    ("1998bu", 50, 0.15, "M96", 281, 0.04, "trgb_hst", "CCHP", "trgb_hst&N4258&CCHP", 273, 0.04, None, ["jha1999", "suntzeff1999"], "Fotometria e erros por ponto; alertas explícitos de correlação e orçamento de distância.", "Sem matriz entre campanhas, estrelas de comparação, MLCS e distância; não combinar Jha/Suntzeff como independentes."),
    ("1989B", 51, 0.15, "M66", 283, 0.04, "trgb_hst", "CCHP", "trgb_hst&N4258&CCHP", 273, 0.04, None, ["wells1994", "saha1999"], "Fotometria com erros de fundo e orçamento Cepheid posterior.", "Sem covariância conjunta; inconsistência publicada no erro de Delta-mu exige preservação, não escolha oportunista."),
    ("1994D", 52, 0.14, "N4526", 286, 0.07, "trgb_hst", "CCHP", "trgb_hst&N4258&CCHP", 273, 0.04, None, ["richmond1995", "patat1996"], "Richmond tabelas 5–8 e Patat tabela 1; várias campanhas primárias.", "Sem orçamento unificado; erros internos não incluem todos os sistemáticos; K e K′ não são o mesmo filtro."),
    ("1992A", 53, 0.135, "N1380", 464, 0.034, "trgb_jwst", "A25", "trgb_jwst&N4258&A25", 463, 0.05, 17, ["hamuy1996", "suntzeff1999", "newman2025"], "Template Hamuy e resumo posterior; nova rota TRGB/JWST em Newman.", "NOT_FOUND_ORIGINAL_FULL_BUDGET: Hamuy diz que a fotometria CTIO seria publicada elsewhere; o orçamento óptico original completo não foi recuperado."),
    ("ASASSN-14lp", 54, 0.13, "N4666", 303, 0.05, "trgb_hst", "Ex", "trgb_hst&N4258&Ex", 294, 0.04, None, ["shappee2016", "li2025"], "Shappee fotometria ancillary e sistemáticos SNooPy; Li oferece rota TRGB independente posterior.", "A distância de Shappee deriva da própria SN e não é calibração independente; sem matriz SN–SN completa."),
    ("2021J", 55, 0.14, "N4414", 301, 0.09, "trgb_hst", "Ex", "trgb_hst&N4258&Ex", 294, 0.04, None, ["gallego2022", "li2025"], "Gallego fotometria OSN/Swift e orçamento sistemático (tabela 4 arXiv; A.1 A&A); Li rota TRGB posterior.", "Covariância explícita é com SN1974G, fora dos 13; sem matriz com as demais; não usar mu_SN como distância independente."),
    ("2020nvb", 56, 0.14, "N4457", 302, 0.10, "trgb_hst", "Ex", "trgb_hst&N4258&Ex", 294, 0.04, None, ["newman2025", "aavso709", "li2025"], "Newman tabelas 4,5,8 com TRGB, SALT2/BayeSN e fotometria; Alert 709 apenas descoberta/classificação.", "Alert não tem orçamento; matriz SALT2 completa ausente; reduções Li/Newman das mesmas imagens HST não são independentes."),
]

objects = []
for cid, sn_line, sn_sigma, host, host_line, host_sigma, method, source, mas, mas_line, mas_sigma, group_line, sources, recoverable, missing in ROWS:
    objects.append({
        "CID": cid,
        "local": {
            "sn_line": sn_line,
            "sn_sigma_mag": sn_sigma,
            "host": host,
            "host_line": host_line,
            "host_mu_error_mag": host_sigma,
            "method": method,
            "source": source,
            "anchor": "N4258",
            "anchor_line": 2,
            "anchor_geometric_sigma_mag": 0.032,
            "hms": f"{host}&{method}&{source}",
            "MAS": mas,
            "mas_reference_line": mas_line,
            "mas_sigma_mag": mas_sigma,
            "group": None if group_line is None else {"name": "Fornax", "line": group_line, "sigma_mag": 0.057},
        },
        "primary_sources": sources,
        "recoverable_without_transplant": recoverable,
        "missing_for_full_covariance": missing,
        "covariance_status": "NOT_FOUND_ORIGINAL_FULL_BUDGET__OPEN_NO_TRANSPLANT" if cid == "1992A" else "OPEN_NO_TRANSPLANT",
        "local_semantics": "SN diagonal scalar plus separately coded host/MAS/anchor/group factors; not a complete within-SN error decomposition",
    })

map_payload = {
    "status": "PRIMARY_SOURCES_MAPPED__PARTIAL_COMPONENTS_ONLY__PHYSICAL_COVARIANCE_OPEN",
    "route_id": "estatistica.h0dn_bg1.ordem_kimi_y_obs_09nov",
    "opening_allowed": False,
    "full_HMS_admitted": False,
    "observed_vector_read": False,
    "observed_statistics_computed": False,
    "local_files": {
        "sn1a_calib": str(UP / "sn1a_calib.dat"),
        "host_data": str(UP / "host_data.dat"),
        "anchors": str(UP / "anchors.dat"),
        "groups": str(UP / "groups.dat"),
    },
    "local_file_pins": {name: pin(UP / f"{name}.dat") for name in ["sn1a_calib", "host_data", "anchors", "groups"]},
    "objects": objects,
    "shared_structures": {
        "anchor": {"name": "N4258", "sigma_mag": 0.032, "line": 2, "members": IDS},
        "MAS": [
            {"name": "trgb_jwst&N4258&A25", "line": 463, "sigma_mag": 0.05, "members": ["2011iv", "2007on", "1992A"]},
            {"name": "trgb_hst&N4258&CCHP", "line": 273, "sigma_mag": 0.04, "members": ["1980N", "1981D", "2006dd", "1998bu", "1989B", "1994D"]},
            {"name": "trgb_hst&N4258&Ex", "line": 294, "sigma_mag": 0.04, "members": ["2021rhu", "ASASSN-14lp", "2021J", "2020nvb"]},
        ],
        "same_host": [
            {"host": "N1404", "members": ["2011iv", "2007on"], "status": "HOST_DISTANCE_SHARED__PHOTOMETRIC_COVARIANCE_OPEN"},
            {"host": "N1316", "members": ["1980N", "1981D", "2006dd"], "status": "HOST_DISTANCE_SHARED__PHOTOMETRIC_COVARIANCE_OPEN"},
        ],
        "Fornax_group": {"line_N1380": 17, "line_N1404": 19, "sigma_mag": 0.057, "meaning": "Intrinsic host-within-group dispersion equation; not a generic SN covariance"},
        "HMS_note": "Each involved HMS has one active host row. Multiple SNe in one host do not themselves create an off-diagonal HMS term.",
        "sn1a_covar_pp": "NOT_THESE_CALIBRATORS: that file belongs to the Hubble-flow block and must not be transplanted to rows 44–56 of sn1a_calib.dat",
    },
    "admission": {
        "primary_source_archive_complete": True,
        "partial_factor_map_available": True,
        "within_SN_full_decomposition_available": False,
        "full_13x13_covariance_available": False,
        "independent_physical_review_complete": False,
        "physical_covariance_closed": False,
        "opening_allowed": False,
    },
    "prohibitions": [
        "No Pantheon+/R22 covariance transplant",
        "No full-HMS diagonal addition",
        "No inference of zero covariance from missing publications",
        "No treatment of same-image TRGB reductions as independent",
        "No SN-derived distance used as independent host calibration",
        "No observed opening, solver, estimator.evaluate, Z, t, h_hat or ratio",
    ],
}
map_path = HERE / "MAPA_FONTES_E_COVARIANCIA_13.json"
map_path.write_text(json.dumps(map_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

initial = json.loads((ARCH / "MANIFEST_DOWNLOAD.json").read_text(encoding="utf-8"))
recovery1 = json.loads((ARCH / "MANIFEST_RECOVERY.json").read_text(encoding="utf-8"))
recovery2 = json.loads((ARCH / "MANIFEST_RECOVERY_02.json").read_text(encoding="utf-8"))
rec1 = {r["key"]: r for r in recovery1["sources"]}
final_sources = []
for old in initial["sources"]:
    key = old["key"]
    if key in rec1:
        r = rec1[key]
        final = {"key": key, "objects": old["objects"], "title": old["title"], "original_url": old["url"], "archive_url": r["url"], "local_path": r["local_path"], "bytes": r["bytes"], "sha256": r["sha256"], "text_path": r["text_path"], "text_sha256": r["text_sha256"], "text_characters": r["text_characters"], "archive_status": "RECOVERED_ALTERNATE_ROUTE", "initial_error_preserved": True}
    elif key == "newman2025":
        r = recovery2
        final = {"key": key, "objects": ["2020nvb", "2011iv", "2007on", "1992A", "2006dd"], "title": old["title"], "original_url": old["url"], "archive_url": r["url"], "local_path": r["local_path"], "bytes": r["bytes"], "sha256": r["sha256"], "text_path": r["text_path"], "text_sha256": r["text_sha256"], "text_characters": r["text_characters"], "archive_status": "FULL_PDF_BESIDE_PARTIAL_HTML", "partial_html_preserved": True}
    else:
        final = {"key": key, "objects": old["objects"], "title": old["title"], "original_url": old["url"], "archive_url": old.get("final_url", old["url"]), "local_path": old["local_path"], "bytes": old["bytes"], "sha256": old["sha256"], "text_path": old["text_path"], "text_sha256": old["text_sha256"], "text_characters": old["text_characters"], "archive_status": "OK"}
    final_sources.append(final)
manifest = {
    "status": "SOURCE_ARCHIVE_COMPLETE__VALIDATION_PENDING",
    "source_count": len(final_sources),
    "coverage": {cid: [s["key"] for s in final_sources if cid in s["objects"]] for cid in IDS},
    "sources": final_sources,
    "side_receipts": [pin(ARCH / "MANIFEST_DOWNLOAD.json"), pin(ARCH / "MANIFEST_RECOVERY.json"), pin(ARCH / "MANIFEST_RECOVERY_02.json")],
    "opening_allowed": False,
    "physical_covariance_closed": False,
}
manifest_path = ARCH / "MANIFEST_FONTES_PRIMARIAS.json"
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

lines = [
    "# Levantamento das fontes primárias — 13 calibradores H0DN",
    "",
    "**Estado:** `PRIMARY_SOURCES_MAPPED__PARTIAL_COMPONENTS_ONLY__PHYSICAL_COVARIANCE_OPEN`  ",
    "**Escopo:** fontes e incertezas; nenhum centro fotométrico é reproduzido aqui; nenhuma abertura ou estatística observada.",
    "",
    "## Resultado por objeto",
    "",
    "| Objeto | SN linha / sigma (mag) | Host linha / mu_error (mag) | Fontes primárias | O que é recuperável | Estado da covariância |",
    "|---|---:|---:|---|---|---|",
]
for o in objects:
    l = o["local"]
    lines.append(f"| {o['CID']} | {l['sn_line']} / {l['sn_sigma_mag']} | {l['host_line']} / {l['host_mu_error_mag']} | {', '.join(o['primary_sources'])} | {o['recoverable_without_transplant']} | {o['covariance_status']} |")
lines += [
    "",
    "## Estruturas compartilhadas efetivamente presentes no H0DN",
    "",
    "- **N4258:** todos os 13 usam a geometria da âncora com 0,032 mag (`anchors.dat:2`).",
    "- **MAS A25:** 2011iv, 2007on e 1992A, com 0,05 mag (`host_data.dat:463`).",
    "- **MAS CCHP:** 1980N, 1981D, 2006dd, 1998bu, 1989B e 1994D, com 0,04 mag (`host_data.dat:273`).",
    "- **MAS Ex:** 2021rhu, ASASSN-14lp, 2021J e 2020nvb, com 0,04 mag (`host_data.dat:294`).",
    "- **Mesmo host:** N1404 compartilha 2011iv/2007on; N1316 compartilha 1980N/1981D/2006dd. A distância é comum, mas a covariância fotométrica completa não está publicada.",
    "- **Fornax:** N1380 e N1404 têm equações de grupo com 0,057 mag (`groups.dat:17,19`); isso não é uma covariância genérica entre SNe.",
    "- **HMS:** cada HMS envolvido tem uma linha ativa de host; várias SNe no mesmo host não criam, por si sós, um termo HMS fora da diagonal.",
    "- **`sn1a_covar_pp.dat`:** pertence ao fluxo de Hubble e não é a covariância das linhas 44–56 dos calibradores.",
    "",
    "## Fontes arquivadas",
    "",
    "Os hashes completos, URLs finais, textos extraídos e recibos de recuperação estão em `fontes_primarias/MANIFEST_FONTES_PRIMARIAS.json`.",
    "",
    "| Chave | Fonte | URL de arquivamento | SHA-256 |",
    "|---|---|---|---|",
]
for s in final_sources:
    lines.append(f"| {s['key']} | {s['title']} | {s['archive_url']} | `{s['sha256']}` |")
lines += [
    "",
    "## Veredito",
    "",
    "A cobertura documental está completa para esta etapa: todos os 13 têm fonte primária arquivada. A covariância física completa continua **OPEN_NO_TRANSPLANT**. O pacote admite somente fatores e dependências explicitamente documentados; não transforma ausência de matriz em independência, nem fotometria pública em covariância pronta.",
    "",
    "Para fechar a matriz ainda são necessários produtos internos dos ajustes ou novas decomposições pré-especificadas, revisão independente e um novo teste de suporte somente depois da aceitação física.",
]
report_path = HERE / "LEVANTAMENTO_FONTES_PRIMARIAS_13.md"
report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

validator = r'''from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
EXPECTED_HASHES = {
    "MAPA_FONTES_E_COVARIANCIA_13.json": "__MAP_SHA__",
    "LEVANTAMENTO_FONTES_PRIMARIAS_13.md": "__REPORT_SHA__",
    "fontes_primarias/MANIFEST_FONTES_PRIMARIAS.json": "__MANIFEST_SHA__",
}
IDS = ["2011iv", "2007on", "2021rhu", "1980N", "1981D", "2006dd", "1998bu", "1989B", "1994D", "1992A", "ASASSN-14lp", "2021J", "2020nvb"]
REQUIRED_TEXT = {
    "gall2018": ["nightly zero-point error", "uncertainties and their covariances"],
    "hamuy1991": ["acceptable fits"],
    "hamuy1996": ["photometry obtained at CTIO which will be published else"],
    "shappee2016": ["requires an independent distance to the host galaxy", "have correlated errors"],
    "dhawan2022": ["statistical and systematic error budget for computing the TRGB", "SALT2 covariance matrix"],
    "newman2025": ["SN 2020nvb", "Table 8", "SALT2", "BayeSN"],
    "stritzinger2010": ["a complete covariance matrix for the light curve parameters"],
    "jha1999": ["correlations in the MLCS analysis"],
}

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

actual_hashes = {name: sha(HERE / name) for name in EXPECTED_HASHES}
mapa = json.loads((HERE / "MAPA_FONTES_E_COVARIANCIA_13.json").read_text(encoding="utf-8"))
manifest = json.loads((HERE / "fontes_primarias/MANIFEST_FONTES_PRIMARIAS.json").read_text(encoding="utf-8"))
object_checks = {}
for o in mapa["objects"]:
    cid = o["CID"]
    loc = o["local"]
    sn_parts = Path(mapa["local_files"]["sn1a_calib"]).read_text(encoding="utf-8").splitlines()[loc["sn_line"] - 1].split()
    host_parts = Path(mapa["local_files"]["host_data"]).read_text(encoding="utf-8").splitlines()[loc["host_line"] - 1].split()
    sn_ok = sn_parts[1] == loc["host"] and sn_parts[2] == cid and float(sn_parts[4]) == loc["sn_sigma_mag"]
    host_ok = host_parts[0] == loc["host"] and float(host_parts[2]) == loc["host_mu_error_mag"] and host_parts[3] == loc["method"] and host_parts[4] == loc["anchor"] and host_parts[5] == loc["source"]
    mas_parts = Path(mapa["local_files"]["host_data"]).read_text(encoding="utf-8").splitlines()[loc["mas_reference_line"] - 1].split()
    mas_ok = mas_parts[0] == "N4258" and float(mas_parts[2]) == loc["mas_sigma_mag"] and mas_parts[3] == loc["method"] and mas_parts[5] == loc["source"]
    group_ok = True
    if loc["group"] is not None:
        group_parts = Path(mapa["local_files"]["groups"]).read_text(encoding="utf-8").splitlines()[loc["group"]["line"] - 1].split()
        group_ok = group_parts == ["Fornax", loc["host"], str(loc["group"]["sigma_mag"])]
    object_checks[cid] = bool(sn_ok and host_ok and mas_ok and group_ok and o["covariance_status"].endswith("OPEN_NO_TRANSPLANT"))
anchor_parts = Path(mapa["local_files"]["anchors"]).read_text(encoding="utf-8").splitlines()[1].split()
archive_checks = {}
for s in manifest["sources"]:
    source = Path(s["local_path"])
    text = Path(s["text_path"])
    ok = source.is_file() and text.is_file() and sha(source) == s["sha256"] and sha(text) == s["text_sha256"] and len(text.read_text(encoding="utf-8")) == s["text_characters"] and s["text_characters"] > 1000
    if s["key"] in REQUIRED_TEXT:
        content = text.read_text(encoding="utf-8")
        ok = ok and all(snippet in content for snippet in REQUIRED_TEXT[s["key"]])
    archive_checks[s["key"]] = bool(ok)
coverage_checks = {cid: bool(manifest["coverage"].get(cid)) and all(archive_checks.get(k, False) for k in manifest["coverage"][cid]) for cid in IDS}
map_source_checks = {o["CID"]: all(k in manifest["coverage"][o["CID"]] and archive_checks.get(k, False) for k in o["primary_sources"]) for o in mapa["objects"]}
checks = {
    "package_hashes_match": actual_hashes == EXPECTED_HASHES,
    "exact_13_ids": [o["CID"] for o in mapa["objects"]] == IDS and len(set(o["CID"] for o in mapa["objects"])) == 13,
    "all_local_rows_match": all(object_checks.values()),
    "anchor_N4258_matches": anchor_parts[0] == "N4258" and float(anchor_parts[2]) == 0.032,
    "source_count_18": manifest["source_count"] == 18 and len(archive_checks) == 18,
    "all_archives_and_required_texts_match": all(archive_checks.values()),
    "all_13_covered_by_primary_archive": all(coverage_checks.values()),
    "all_object_source_lists_match_manifest": all(map_source_checks.values()),
    "all_full_covariances_remain_open": all(o["covariance_status"].endswith("OPEN_NO_TRANSPLANT") for o in mapa["objects"]),
    "physical_closure_flags_false": mapa["admission"]["full_13x13_covariance_available"] is False and mapa["admission"]["physical_covariance_closed"] is False and mapa["opening_allowed"] is False and mapa["full_HMS_admitted"] is False,
    "no_observed_work_flags": mapa["observed_vector_read"] is False and mapa["observed_statistics_computed"] is False,
}
validated = all(checks.values())
result = {
    "status": "SOURCES_VALIDATED__COVARIANCE_PHYSICS_OPEN" if validated else "SOURCE_PACKAGE_VALIDATION_FAILED",
    "source_archive_complete": True,
    "all_13_have_primary_sources": all(coverage_checks.values()),
    "full_13x13_covariance_available": False,
    "physical_covariance_closed": False,
    "full_HMS_admitted": False,
    "opening_allowed": False,
    "observed_vector_read_by_validator": False,
    "observed_statistics_computed": False,
    "checks": checks,
    "object_checks": object_checks,
    "archive_checks": archive_checks,
    "coverage_checks": coverage_checks,
    "hashes": actual_hashes,
}
path = HERE / "VALIDACAO_FONTES_13.json"
path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False, indent=2))
if not validated:
    raise RuntimeError("Source package validation failed")
'''
for token, path in {"__MAP_SHA__": map_path, "__REPORT_SHA__": report_path, "__MANIFEST_SHA__": manifest_path}.items():
    validator = validator.replace(token, sha(path))
validator_path = HERE / "validar_fontes_13.py"
validator_path.write_text(validator, encoding="utf-8")
print(json.dumps({"map": pin(map_path), "report": pin(report_path), "manifest": pin(manifest_path), "validator": pin(validator_path)}, ensure_ascii=False, indent=2))
