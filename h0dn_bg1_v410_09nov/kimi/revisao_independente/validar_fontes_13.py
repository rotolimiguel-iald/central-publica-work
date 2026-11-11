from pathlib import Path
import hashlib
import json

HERE = Path(__file__).resolve().parent
EXPECTED_HASHES = {
    "MAPA_FONTES_E_COVARIANCIA_13.json": "ec20246fe4d4d11976e08b43efb7965a89c4e10f175411c2b4b77a813b072b03",
    "LEVANTAMENTO_FONTES_PRIMARIAS_13.md": "8c4dd827334785bfcd15611afa62acd5fdce58ecc9bdc3abc91d27d3e614a590",
    "fontes_primarias/MANIFEST_FONTES_PRIMARIAS.json": "52a60df567f6cca9fbde121899ce111ceadfcb0cc82b8e83db53bdc9e9081e83",
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
