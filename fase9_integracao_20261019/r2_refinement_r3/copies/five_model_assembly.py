"""Pure F9 prediction assembly. Prepared statically; not executed in this unit.

Only in-memory, pinned JSON bytes enter. No solver, filesystem, likelihood,
observations, optimizer or evidence calculation. All numerical outputs are
engineering estimates; an independent certificate layer is deliberately absent.
"""
import hashlib
import json
import math
from fractions import Fraction

# Filled from verified source bytes by prepare_delivery.py, never from memory.
SOURCE_PINS = {'resolver': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\f9_consolidated_draft\\RESOLUTOR_F9.json', 'bytes': 69740, 'sha256': 'c45de68d187fc49d5f79316b1561c9d9807dbb525019160837e8deea5e13ba53'}, 'background_layout': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\f9_structural_layout_preparation\\LAYOUT_ESTRUTURAL_3CMB_13BAO.json', 'bytes': 16475, 'sha256': '7581c71fb1a548fc1e20110137a3e3d940e363725096485de837bac56d3a2317'}, 'linear_design': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\h0dn_documentary_review\\linear_design\\ESPECIFICACAO_LINEAR.json', 'bytes': 109887, 'sha256': '9aca9fffe3c7788d3c8ef1411b1dfa5c908c7366ef32ad969b14e59492199a95'}, 'background_engine': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\f9_background_prediction\\background_controls.py', 'bytes': 15896, 'sha256': 'c41aee4bcd1d8a137df8d7541e53738e68e9a77605ec8e51d4051459544265a2'}, 'background_protocol': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\f9_background_prediction\\PROTOCOL.json', 'bytes': 7442, 'sha256': '13a2595f0d15fc194475ca7e977cacbcd45524a1d8637f92c0d7ebbae6a720eb'}, 'MM_contract': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\f9_mm_model_preparation\\CONTRATO_MM_CANDIDATO.json', 'bytes': 15582, 'sha256': 'c7731bcc21e29cf94c7d835e86e94f6e16d666a0085de90f5137b270f669936b'}}
MODELS = ("H1_TGL", "H2_LCDM", "H3_beta_free", "H4_Cepheid", "H5_rd_free")
THETA_NAMES = ("H0", "ombh2", "omch2")
BOUNDS = {"H0": (50, 90), "ombh2": (.015, .030), "omch2": (.08, .18),
          "beta": (-.05, .05), "s": (-.15, .15), "rd_Mpc": (130, 160)}
EXTRAS = {"H1_TGL": (), "H2_LCDM": (), "H3_beta_free": ("beta",),
          "H4_Cepheid": ("s",), "H5_rd_free": ("rd_Mpc",)}
BACKGROUND_UNITS = {"theta": ["km/s/Mpc", "dimensionless", "dimensionless"],
                    "R": "dimensionless", "lA": "dimensionless",
                    "E_law": "dimensionless", "I_law": "dimensionless",
                    "z_law": "dimensionless", "rstar_Mpc": "Mpc",
                    "rdrag_Mpc": "Mpc", "low_z": {"z": "dimensionless",
                    "DM_Mpc": "Mpc", "DH_Mpc": "Mpc", "DV_Mpc": "Mpc"}}


class AssemblyError(ValueError):
    """The caller must preserve this failure; it is not zero likelihood."""

    def __init__(self, code, detail):
        self.code, self.detail = code, detail
        super().__init__(f"{code}: {detail}")


def _require(condition, code, detail):
    if not condition:
        raise AssemblyError(code, detail)


def _keys(value, required, label, exact=False):
    _require(type(value) is dict, "SCHEMA_ERROR", label)
    ok = set(value) == set(required) if exact else set(required) <= set(value)
    _require(ok, "SCHEMA_ERROR", label + ": keys")


def _number(value, label, positive=False):
    _require(type(value) in (int, float), "NUMERIC_ERROR", label)
    try:
        result = float(value)
    except (OverflowError, ValueError) as exc:
        raise AssemblyError("NUMERIC_ERROR", label) from exc
    _require(math.isfinite(result) and (not positive or result > 0),
             "NUMERIC_ERROR", label)
    return result


def _sha(raw):
    _require(type(raw) is bytes, "SCHEMA_ERROR", "expected bytes")
    return hashlib.sha256(raw).hexdigest()


def _digest(value, label):
    _require(type(value) is str and len(value) == 64
             and all(c in "0123456789abcdef" for c in value), "PIN_ERROR", label)
    return value


def _pairs(pairs):
    result = {}
    for key, value in pairs:
        _require(key not in result, "SCHEMA_ERROR", "duplicate JSON key")
        result[key] = value
    return result


def _constant(text):
    raise AssemblyError("NUMERIC_ERROR", "nonfinite JSON token")


def _json(raw, expected_sha, label):
    _digest(expected_sha, label)
    _require(_sha(raw) == expected_sha, "PIN_ERROR", label)
    try:
        value = json.loads(raw, object_pairs_hook=_pairs, parse_constant=_constant)
    except (ValueError, UnicodeError, RecursionError) as exc:
        raise AssemblyError("SCHEMA_ERROR", label + ": invalid JSON") from exc
    _require(type(value) is dict, "SCHEMA_ERROR", label)
    return value


def _source_pin(pin, label):
    _keys(pin, ("sha256", "bytes", "path"), label, exact=True)
    _digest(pin["sha256"], label)
    _require(type(pin["bytes"]) is int and pin["bytes"] > 0
             and type(pin["path"]) is str and bool(pin["path"]), "PIN_ERROR", label)


def _layout(raw, digest):
    # Consume the coordinator's existing structural artifact directly.
    _require(digest == SOURCE_PINS["background_layout"]["sha256"], "PIN_ERROR", "frozen background layout")
    doc = _json(raw, digest, "background layout with alpha provenance")
    _require(doc.get("schema") == "F9_BACKGROUND_STRUCTURAL_LAYOUT_V1" and
             doc.get("status") == "STRUCTURAL_PROJECTION_NO_OBSERVED_CENTRES",
             "SCHEMA_ERROR", "layout schema")
    components = doc["components"]
    _require(type(components) is list and len(components) == 16, "ROW_ERROR", "16 background rows required")
    names = {"R": "R", "l_A": "lA", "omega_b_h2": "ombh2",
             "DM_over_rdrag": "DM_over_rd", "DH_over_rdrag": "DH_over_rd", "DV_over_rdrag": "DV_over_rd"}
    rows, seen, cmb = [], set(), set()
    for i, c in enumerate(components):
        _require(c["index_1based"] == i + 1 and c["units"] == "1", "ROW_ERROR", "component order/units")
        obs = names.get(c["observable"])
        _require(obs is not None, "ROW_ERROR", "unknown source observable")
        rid = c["source_path"] + ":L" + str(c["source_line"]) + "#" + c["observable"]
        _require(rid not in seen, "ROW_ERROR", "duplicate background row")
        seen.add(rid)
        if i < 3:
            _require(c["block"] == "planck_comp" and c["block_index_1based"] == i + 1
                     and obs in ("R", "lA", "ombh2") and obs not in cmb
                     and c["redshift_decimal"] is None, "ROW_ERROR", rid)
            cmb.add(obs)
            z, block = None, "CMB"
        else:
            _require(c["block"] == "desi_dr2" and c["block_index_1based"] == i - 2
                     and obs in ("DM_over_rd", "DH_over_rd", "DV_over_rd"), "ROW_ERROR", rid)
            z = _number(float(c["redshift_decimal"]), rid + ": z", positive=True)
            _require(z <= 3, "DOMAIN_ERROR", "BAO redshift outside documented low-z domain")
            block = "BAO"
        rows.append({"row_id": rid, "block": block, "observable": obs, "unit": "dimensionless", "z": z})
    return rows, doc["alpha"]


def _local_design(raw):
    d = _json(raw, SOURCE_PINS["linear_design"]["sha256"], "frozen local design")
    columns, rows = d["eta_columns"], d["rows"]
    _require(len(columns) == 63 and len(rows) == 267, "ROW_ERROR", "local design dimensions")
    names = [x["key"] for x in columns]
    _require(len(set(names)) == 63 and all(x["unit"] == "mag" for x in columns),
             "UNIT_ERROR", "nuisance columns")
    identities, X, ah, cc, scale = [], [], [], [], []
    for row in rows:
        identities.append(row["row_id"])
        # The frozen resolver chooses all-magnitude local coordinates.
        factor = 5 if row["family"] in ("SN_HF", "SBF_HF", "megamaser") else 1
        scale.append(factor)
        _require(set(row["X"]) <= set(names), "ROW_ERROR", "unknown nuisance column")
        X.append({key: str(factor * Fraction(value)) for key, value in row["X"].items()})
        ah.append(str(factor * Fraction(row["a_h"])))
        cc.append(str(factor * Fraction(row["c_C"])))
    _require(len(set(identities)) == 267, "ROW_ERROR", "duplicate local row")
    return columns, identities, X, ah, cc, scale


def _parameters(model_parameters):
    _keys(model_parameters, MODELS, "five model parameters", exact=True)
    result, common = {}, None
    for model in MODELS:
        p = model_parameters[model]
        _keys(p, THETA_NAMES + EXTRAS[model], model, exact=True)
        values = {key: _number(value, model + ": " + key) for key, value in p.items()}
        for key, value in values.items():
            lo, hi = BOUNDS[key]
            _require(lo <= value <= hi, "DOMAIN_ERROR", model + ": " + key)
        theta = tuple(values[key] for key in THETA_NAMES)
        _require(common is None or theta == common, "IDENTITY_ERROR", "shared background theta required")
        common = theta
        result[model] = values
    return result, common


def assemble_five(model_parameters, *, design_json, layout_json,
                  background_json, admission_json, admission_sha256):
    """Return 5 deterministic engineering means and one shared sparse X.

    Admission must be independently frozen by the caller, not self-declared by
    the prediction packet. No caller-controlled flag enables certification.
    Inputs are described exhaustively in API_CONTRATO.md.
    """
    admission = _json(admission_json, admission_sha256, "structural admission")
    fields = ("schema", "status", "layout_sha256", "sources",
              "engine_configuration_sha256", "runtime_sha256")
    _keys(admission, fields, "admission", exact=True)
    _require(admission["schema"] == "F9_ASSEMBLY_ADMISSION_V1" and
             admission["status"] == "ENGINEERING_STRUCTURAL_ADMISSION", "ADMISSION_ERROR", "explicit engineering admission required")
    _require(admission["sources"] == SOURCE_PINS, "PIN_ERROR", "frozen source set")
    for key in ("layout_sha256", "engine_configuration_sha256", "runtime_sha256"):
        _digest(admission[key], key)
    layout, alpha = _layout(layout_json, admission["layout_sha256"])
    _keys(alpha, ("symbol", "decimal_token", "units", "origin", "source_line"), "alpha")
    _require(alpha["symbol"] == "ALPHA_FINE_CODATA_2018" and alpha["units"] == "1"
             and type(alpha["source_line"]) is int and alpha["source_line"] > 0,
             "IDENTITY_ERROR", "alpha origin")
    _source_pin(alpha["origin"], "alpha source pin")
    alpha_value = _number(float(alpha["decimal_token"]), "ALPHA_FINE_CODATA_2018", positive=True)
    _require(alpha_value < 1, "DOMAIN_ERROR", "alpha")
    beta_tgl = alpha_value * math.sqrt(math.e)
    _require(BOUNDS["beta"][0] <= beta_tgl <= BOUNDS["beta"][1], "DOMAIN_ERROR", "fixed beta outside nested diagnostic domain")
    pars, theta = _parameters(model_parameters)
    # Hash of raw packet is provenance, not proof of its solver's correctness.
    packet_sha = _sha(background_json)
    packet = _json(background_json, packet_sha, "background packet")
    _keys(packet, ("schema", "status", "identity", "result", "error"), "background packet", exact=True)
    _require(packet["schema"] == "F9_BACKGROUND_PACKET_V1", "SCHEMA_ERROR", "background packet schema")
    _require(packet["status"] == "ENGINEERING_RESULT" and packet["error"] is None,
             "UPSTREAM_FAILURE", "background did not return a usable engineering result")
    ident = packet["identity"]
    _keys(ident, ("engine_sha256", "protocol_sha256", "engine_configuration_sha256", "runtime_sha256",
                  "theta", "z_law", "units", "execution_receipt_sha256"), "background identity", exact=True)
    for k, source in (("engine_sha256", "background_engine"), ("protocol_sha256", "background_protocol")):
        _require(ident[k] == SOURCE_PINS[source]["sha256"], "PIN_ERROR", k)
    for k in ("engine_configuration_sha256", "runtime_sha256"):
        _require(ident[k] == admission[k], "IDENTITY_ERROR", k)
    _digest(ident["execution_receipt_sha256"], "execution receipt")
    _require(type(ident["theta"]) is list and len(ident["theta"]) == 3, "IDENTITY_ERROR", "theta identity")
    _require(tuple(_number(v, "packet theta") for v in ident["theta"]) == theta,
             "IDENTITY_ERROR", "packet theta differs")
    _require(_number(ident["z_law"], "law redshift") == 1089.95, "IDENTITY_ERROR", "law redshift is not derived zstar")
    _require(ident["units"] == BACKGROUND_UNITS, "UNIT_ERROR", "background units")
    bg = packet["result"]
    _keys(bg, ("theta", "R", "lA", "rstar_Mpc", "rdrag_Mpc", "E_law", "I_law", "low_z", "physics_status"), "background result")
    _require(type(bg["theta"]) is list and len(bg["theta"]) == 3 and
             tuple(_number(v, "result theta") for v in bg["theta"]) == theta,
             "IDENTITY_ERROR", "result theta differs")
    _require(bg["physics_status"] == "STANDARD_BACKGROUND_THEORY_CONTROL_NOT_OBSERVATION",
             "IDENTITY_ERROR", "background result kind")
    for k in ("R", "lA", "rstar_Mpc", "rdrag_Mpc", "E_law"):
        _number(bg[k], k, positive=True)
    I = _number(bg["I_law"], "I_law")
    expected_I = (2 / 3) * math.log(bg["E_law"])
    _require(math.isclose(I, expected_I, rel_tol=1e-12, abs_tol=1e-14),
             "IDENTITY_ERROR", "I_law/E_law mismatch (engineering consistency only)")
    low_z = {}
    _require(type(bg["low_z"]) is list, "SCHEMA_ERROR", "low_z")
    for row in bg["low_z"]:
        _keys(row, ("z", "DM_Mpc", "DH_Mpc", "DV_Mpc"), "distance row")
        z = _number(row["z"], "distance redshift")
        _require(0 <= z <= 3 and z not in low_z, "ROW_ERROR", "duplicate/out-of-domain distance redshift")
        distances = {key: _number(row[key], key) for key in ("DM_Mpc", "DH_Mpc", "DV_Mpc")}
        _require(distances["DH_Mpc"] > 0 and distances["DM_Mpc"] >= 0 and distances["DV_Mpc"] >= 0,
                 "NUMERIC_ERROR", "distance sign")
        low_z[z] = distances
    for row in layout[3:]:
        _require(row["z"] in low_z, "BACKGROUND_GRID_MISSING", row["row_id"])
    columns, local_ids, local_X, local_ah, local_cc, scale = _local_design(design_json)
    row_ids = [row["row_id"] for row in layout] + local_ids
    _require(len(set(row_ids)) == 283, "ROW_ERROR", "joint row identity collision")
    X = [{} for _ in range(16)] + local_X
    ah, cc = ["0"] * 16 + local_ah, ["0"] * 16 + local_cc
    outputs = {}
    for model in MODELS:
        p = pars[model]
        beta = beta_tgl if model == "H1_TGL" else p["beta"] if model == "H3_beta_free" else 0.0
        h = math.log10(theta[0]) + I * beta / math.log(10)
        delta_C = -5 * math.log1p(p["s"]) / math.log(10) if model == "H4_Cepheid" else 0.0
        rd = p["rd_Mpc"] if model == "H5_rd_free" else bg["rdrag_Mpc"]
        values = []
        for row in layout:
            obs = row["observable"]
            if row["block"] == "CMB":
                values.append(theta[1] if obs == "ombh2" else bg[obs])
            else:
                key = obs.replace("_over_rd", "_Mpc")
                values.append(low_z[row["z"]][key] / rd)
        values.extend(float(Fraction(a)) * h + float(Fraction(c)) * delta_C
                      for a, c in zip(local_ah, local_cc))
        _require(len(values) == 283 and all(math.isfinite(x) for x in values), "NUMERIC_ERROR", "assembled mean")
        extra_density = {"H1_TGL": "1", "H2_LCDM": "1", "H3_beta_free": "10",
                         "H4_Cepheid": "10/3", "H5_rd_free": "1/30"}[model]
        outputs[model] = {"mean_without_nuisance": values, "parameters": p,
                          "h_local_dex": h, "delta_C_mag": delta_C, "beta": beta,
                          "bao_rd_Mpc": rd, "cmb_rstar_Mpc": bg["rstar_Mpc"],
                          "prior": {"coordinates": list(THETA_NAMES + EXTRAS[model]),
                                    "common_theta_density_exact": "50/3", "extra_density_exact": extra_density,
                                    "measure": "uniform_in_listed_coordinates"}}
    return {"schema": "F9_FIVE_MODEL_PREDICTIONS_V1", "status": "ENGINEERING_ONLY",
            "row_ids": row_ids, "row_units": ["dimensionless"] * 16 + ["mag"] * 267,
            "native_to_output_row_scale": [1] * 16 + scale,
            "observation_contract": "Apply the same T to y and T C T^T to covariance before using these means and X.",
            "nuisance": {"columns": columns, "X_sparse_rows": X, "dimension": 63,
                         "measure": "common kappa d_eta; no absolute evidence"},
            "response_columns": {"a_h": ah, "c_C": cc}, "models": outputs,
            "beta_TGL_runtime": beta_tgl,
            "identity": {"admission_sha256": admission_sha256, "layout_sha256": _sha(layout_json),
                         "alpha_source": alpha["origin"], "alpha_source_line": alpha["source_line"],
                         "background_packet_sha256": packet_sha,
                         "background_identity": ident, "sources": json.loads(json.dumps(SOURCE_PINS))},
            "certification": {"status": "UNBOUNDED_THEORY_ERROR", "uniform_error_bound": None,
                              "certified": False, "numerical_certificate": None},
            "observed_outputs": {"chi2": None, "p": None, "sigma": None, "lnB": None}}
