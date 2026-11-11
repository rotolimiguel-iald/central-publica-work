"""Self-contained F7.2 source inventory. No events, likelihood, fit or TGL limit.

This candidate consumes immutable relative R8 custody plus a provenance-pinned
historical v369 projection. Published model limits are not transferred to TGL.
"""
from __future__ import annotations
import ast
import hashlib
import json
import math
from pathlib import Path
import re
from .canonical import require_current
ROOT = Path(__file__).resolve().parents[1]
MANIFEST = Path(__file__).with_name("neutrino_fontes_f72_b2.json")
MANIFEST_SHA256 = "48dd88dc38e1de80e8f4aaaf78a83a63c7208205c2a8d9c5e292b400204dd9b8"
JUNO_NAME = "Beccaria_Ternes_2026_arxiv_2606.13362v1.pdf"
REJECTED_HTML = frozenset({"Kovachy_2015_Nature_abstract.html","Fein_2019_NaturePhysics_abstract.html"})
class FonteRecusada(ValueError):
    """A source identity or structural check failed."""
def _source(entry, *, python_source=False, pdf=False):
    if not isinstance(entry,dict):
        raise FonteRecusada("source entry is not an object")
    relative,pin,size = (entry.get(k) for k in ("relative_path","sha256","bytes"))
    if (not isinstance(relative,str) or not isinstance(pin,str) or not re.fullmatch(r"[0-9a-f]{64}",pin,re.ASCII)
            or type(size) is not int or size <= 0):
        raise FonteRecusada("source path/pin/size invalid")
    path = (ROOT/relative).resolve()
    if not path.is_relative_to((ROOT/"fontes_externas/F7.2").resolve()):
        raise FonteRecusada("source path escapes custody")
    try:
        raw = path.read_bytes()
    except OSError as exc:
        raise FonteRecusada(f"source unavailable: {path.name}") from exc
    if hashlib.sha256(raw).hexdigest() != pin or len(raw) != size:
        raise FonteRecusada(f"source hash/size differs: {path.name}")
    if pdf and (len(raw)<1000 or not raw.startswith(b"%PDF-")):
        raise FonteRecusada("invalid substantive PDF bytes")
    if python_source:
        try:
            ast.parse(raw.decode("utf-8-sig"))
        except (UnicodeError,SyntaxError) as exc:
            raise FonteRecusada("script is not parseable source") from exc
    return raw,{"path":str(path),"sha256":pin,"bytes":size,"origin":entry.get("origin"),
                "ast_parsed":python_source,"pdf_header_valid":pdf}
def _load_sources(manifest_path=MANIFEST):
    try:
        raw = Path(manifest_path).read_bytes()
        if hashlib.sha256(raw).hexdigest()!=MANIFEST_SHA256:
            raise FonteRecusada("manifest hash differs")
        manifest=json.loads(raw)
        if (manifest["schema"]!="iald.f7_2.channel_sources.v4" or manifest["unit"]!="F7.2"
                or manifest["primary_article_pdfs_custodied"] is not True or manifest["raw_experimental_data_custodied"] is not False):
            raise FonteRecusada("manifest identity/custody differs")
        scripts,docs,pdfs,doc_raw={},{},{},{}
        for entry in manifest["scripts"]:
            name=entry["name"]
            if name in scripts:
                raise FonteRecusada("duplicate script")
            _,scripts[name]=_source(entry,python_source=True)
        for name,entry in manifest["documents"].items():
            doc_raw[name],docs[name]=_source(entry)
        for entry in manifest["primary_pdfs"]:
            name=entry["name"]
            if name in pdfs:
                raise FonteRecusada("duplicate PDF")
            _,source=_source(entry,pdf=True)
            pdfs[name]={**source,"name":name,"channel":entry["channel"],"url":entry["url"],"matter_validation":entry["validated_matter"]}
        for entry in manifest["context_sources"]:
            _source(entry,pdf=entry["relative_path"].lower().endswith(".pdf"))
        snapshot=json.loads(doc_raw["clock_v369_result"])
        if (snapshot["schema"]!="iald.historical_projection.v369.v1"
                or snapshot["source_json_sha256"]!=manifest["historical_source_sha256"]
                or snapshot["extraction_path"]!="core.clock_test_result_v369.five_sigma_requirement"):
            raise FonteRecusada("historical clock provenance differs")
        projection=manifest["clock_v369_projection"]
        required=snapshot["requirement"]
        for key in ("ghz_N_needed","hbar_omega_needed_eV_at_todays_sigma"):
            value=required[key]
            if type(value) not in (int,float) or not math.isfinite(value) or value<=0 or value!=projection[key]:
                raise FonteRecusada("clock projection values differ")
        if (required["platform"]!="sr87_kim2025" or projection["platform"]!=required["platform"]
                or projection["kind"]!="CONDITIONAL_5SIGMA_PROJECTION"):
            raise FonteRecusada("clock projection kind/platform differs")
        return scripts,docs,pdfs,projection,MANIFEST_SHA256
    except FonteRecusada:
        raise
    except (OSError,UnicodeError,json.JSONDecodeError,KeyError,TypeError,ValueError) as exc:
        raise FonteRecusada("manifest/source structure unreadable") from exc

def canal(manifest_path: str | Path = MANIFEST) -> dict:
    """Return a read-only, source-pinned table; never infer a TGL limit."""
    current = require_current("neutrino_canal_f72_v2", root=ROOT)
    scripts, docs, pdfs, clock_projection, manifest_hash = _load_sources(Path(manifest_path))
    table = docs["channel_power_table"]
    def model_row(identifier: str, exponent: int, value: float, unit: str,
                  relation: str, pivot_gev: float, cl_percent: int,
                  gamma_channel: str, ordering: str | None, pdf_name: str,
                  anchor: str, scenario: str) -> dict:
        source = pdfs[pdf_name]
        return {
            "channel": identifier,
            "energy_exponent_n": exponent,
            "published_model_limit": {
                "value": value, "unit": unit, "relation": relation,
                "pivot_energy_GeV": pivot_gev, "confidence_level_percent": cl_percent,
                "gamma_channel": gamma_channel, "mass_ordering": ordering,
            },
            "published_observation": None,
            "model_scenario": scenario,
            "external_reference": source["url"],
            "source_basis": source,
            "citation_anchor": anchor,
            "local_table_basis": table,
            "statute": "[KNOWN]",
            "primary_bytes_custodied": True,
            "raw_data_reanalysed": False,
            "conditional": True,
            "exponent_measured": False,
            "operator_mapping_to_TGL": "OPEN",
            "tau_star_limit_s": None,
            "verdict": "SEM_LIMITE_TGL",
        }
    def matter_row(identifier: str, pdf_name: str, anchor: str, observation: dict,
                   scenario: str, prior_version: str | None = None) -> dict:
        source = pdfs[pdf_name]
        return {
            "channel": identifier,
            "energy_exponent_n": None,
            "published_model_limit": None,
            "published_observation": observation,
            "model_scenario": scenario,
            "external_reference": source["url"],
            "source_basis": source,
            "citation_anchor": anchor,
            "local_table_basis": table,
            "supporting_previous_version": pdfs[prior_version] if prior_version else None,
            "statute": "[KNOWN]",
            "primary_bytes_custodied": True,
            "raw_data_reanalysed": False,
            "conditional": True,
            "exponent_measured": False,
            "operator_mapping_to_TGL": "OPEN",
            "tau_star_limit_s": None,
            "verdict": "SEM_LIMITE_TGL",
        }
    rows = [
        {
            "channel": "JUNE_TGL_SIGNATURE",
            "energy_exponent_n": -2,
            "published_model_limit": None,
            "published_observation": None,
            "model_scenario": "Vacuum scaling conditional on constant mass gap, tau_star and Kfac.",
            "external_reference": None,
            "source_basis": scripts["tgl_neutrino_decoherence.py"],
            "citation_anchor": "local June script, model formula",
            "local_table_basis": table,
            "statute": "[DERIVED]",
            "primary_bytes_custodied": False,
            "raw_data_reanalysed": False,
            "conditional": True,
            "exponent_measured": False,
            "operator_mapping_to_TGL": "OPEN",
            "tau_star_limit_s": None,
            "verdict": "SEM_LIMITE_TGL",
        },
        model_row("FOGLI_2007", -2, 8.1e-29, "GeV", "<", 1.0, 95,
                  "gamma_0", None, "Fogli_2007_arxiv_0704.2568.pdf", "Eq. 3; Table I",
                  "Solar+KamLAND with Fogli's solar matter dissipator; not pure dephasing."),
        model_row("JUNO_2026_EQUAL_21_31", -2, 4.1e-27, "GeV", "<", 1.0, 90,
                  "Gamma_21=Gamma_31; Gamma_32=0", None, JUNO_NAME,
                  "Sec. III.B; Eq. (6); Eq. (13), Table I",
                  "Beccaria-Ternes analysis of initial JUNO data; TGL operator/likelihood map remains open."),
        model_row("DE_ROMERI_2023_A", -2, 7.8e-27, "GeV", "<", 1.0, 90,
                  "Gamma_21=Gamma_31=Gamma_32", None, "DeRomeri_2023_arxiv_2306.14699.pdf",
                  "Table 3; sections III-IV", "Historical KamLAND bound in model A."),
        model_row("DE_ROMERI_2023_E", -2, 7.9e-27, "GeV", "<", 1.0, 90,
                  "Gamma_21 only", None, "DeRomeri_2023_arxiv_2306.14699.pdf",
                  "Table 3; sections III-IV", "Historical KamLAND bound in model E."),
        model_row("ORCA6_GAMMA21_NO", -2, 2.8e-21, "GeV", "<", 1.0, 90,
                  "Gamma_21 profiled", "NO", "ORCA6_2025_arxiv_2410.01388.pdf",
                  "Table 3; Eqs. (2.10), (2.15)", "ORCA6 normal ordering."),
        model_row("ORCA6_GAMMA21_IO", -2, 4.6e-21, "GeV", "<", 1.0, 90,
                  "Gamma_21 profiled", "IO", "ORCA6_2025_arxiv_2410.01388.pdf",
                  "Table 3; Eqs. (2.10), (2.15)", "ORCA6 inverted ordering."),
        model_row("ORCA6_GAMMA31_NO", -2, 8.4e-21, "GeV", "<", 1.0, 90,
                  "Gamma_31 profiled", "NO", "ORCA6_2025_arxiv_2410.01388.pdf",
                  "Table 3; Eqs. (2.10), (2.15)", "ORCA6 normal ordering."),
        model_row("ORCA6_GAMMA31_IO", -2, 2.2e-21, "GeV", "<", 1.0, 90,
                  "Gamma_31 profiled", "IO", "ORCA6_2025_arxiv_2410.01388.pdf",
                  "Table 3; Eqs. (2.10), (2.15)", "ORCA6 inverted ordering."),
        model_row("ICECUBE_2024_STATE_SELECTION", 0, 1.17e-15, "eV", "<=", 1000.0, 90,
                  "Gamma_0 state selection", None, "IceCube_2024_arxiv_2308.00105.pdf",
                  "Table 1", "IceCube n=0, not a direct n=-2 test."),
        matter_row("ATOM_INTERFEROMETRY_CHAPMAN_1995", "Chapman_1995_author.pdf",
                   "p. 3, Figs. 2-3",
                   {"contrast_near_half_scattered_photon_wavelength": "approximately_zero",
                    "recovered_lost_contrast_fraction_greater_than": 0.60},
                   "Photon scattering and angular selection, not a gravitational dephasing bound."),
        matter_row("MOLECULE_INTERFEROMETRY_C70_2004",
                   "Hackermueller_2004_arxiv_quant-ph_0402146.pdf", "p. 2, Fig. 2",
                   {"material": "C70", "speed_m_per_s": 190,
                    "visibility_by_heating": [
                        {"power_W": 0.0, "visibility_percent": 47},
                        {"power_W": 3.0, "visibility_percent": 29},
                        {"power_W": 6.0, "visibility_percent": 7},
                        {"power_W": 10.5, "visibility_percent": 0},
                    ]},
                   "Thermal-emission decoherence in the article's apparatus."),
        matter_row("NANOPARTICLE_INTERFEROMETRY_PEDALINO_2026",
                   "Pedalino_2026_published_author.pdf", "pp. 1-3, Fig. 2",
                   {"atom_count_greater_than": 7000, "mass_kDa_range": [143, 197],
                    "visibility_runs": [
                        {"mean_mass_kDa": 172, "visibility": 0.10, "uncertainty": 0.01},
                        {"mean_mass_kDa": 172, "visibility": 0.08, "uncertainty": 0.01},
                    ]},
                   "Published nanoparticle interferometry; visibility limited in part by photodepletion.",
                   prior_version="Pedalino_2025_preprint_arxiv_2507.21211v1.pdf"),
    ]
    return {
        "ok": True, "unit": "F7.2", "mode": "READ_ONLY_SOURCE_PROVENANCE_B2",
        "manifest_sha256": manifest_hash, "current_contract": current,
        "served_contract": "F7_2_B2_SELF_CONTAINED", "requested_endpoint": "neutrino_canal_f72_v2",
        "likelihood_available": False, "detector_response_available": False, "tgl_operator_mapping": "OPEN", "local_sources": scripts,
        "local_documents": docs, "primary_pdfs": pdfs,
        "primary_article_pdfs_custodied": True,
        "raw_experimental_data_custodied": False,
        "rejected_publisher_html": sorted(REJECTED_HTML),
        "clock_v369_context": {
            "statute": "[DERIVED]",
            "qualification": "projeção condicional da v369",
            "kind": "CONDITIONAL_5SIGMA_PROJECTION",
            "source_json_path": clock_projection["json_path"],
            "platform": clock_projection["platform"],
            "ghz_N_needed_exact": clock_projection["ghz_N_needed"],
            "hbar_omega_needed_eV_exact": clock_projection["hbar_omega_needed_eV_at_todays_sigma"],
            "comparison_symbol": "≳",
            "GHZ_N_approx": 1690000,
            "hbar_omega_MeV_approx": 3.0,
            "rounded_thresholds_not_exact_bounds": True,
            "matter_interferometry_measurement": False,
            "observed_measurement": False,
            "source_basis": docs["clock_v369_result"],
            "interpretation_basis": table,
        },
        "preregistration_required_before_nature_verdict": True,
        "rows": rows, "overall_verdict": "SEM_LIMITE_TGL",
        "gate_effect": "NONE", "not_falsified_is_not_confirmed": True,
    }
