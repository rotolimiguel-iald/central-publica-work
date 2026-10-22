"""Pure F9 five-model likelihood adapter; prepared, NOT executed in this unit.

The trusted caller injects numpy and the already qualified FlatNuisanceGaussian.
No filesystem, catalog, solver, optimizer, physical-prior integration or
scientific certificate is implemented here. Caller receipts are provenance
inputs, NOT authority or proof that the admitted statistical model is true.
"""
import hashlib
import json
import math
import re
from fractions import Fraction

REQUEST_ID = "a9874f79-9d71-48f5-824c-d51d6d819534"
SOURCE_PINS = {'resolver': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\f9_consolidated_draft\\RESOLUTOR_F9.json', 'bytes': 69740, 'sha256': 'c45de68d187fc49d5f79316b1561c9d9807dbb525019160837e8deea5e13ba53'}, 'linear_gaussian': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\covariance_support\\linear_gaussian.py', 'bytes': 3772, 'sha256': '7dc486b5568876385f4b2e6647e0f449accfea0862c3b0d46ce90d657fba2736'}, 'support': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\covariance_support\\singular_gaussian_v2.py', 'bytes': 4953, 'sha256': '98264bdd57aaad0904bd342631fd3c147fa19f90e8922f0ad6b15ac1b3b93374'}, 'assembler': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\f9_five_model_assembly_preparation\\five_model_assembly.py', 'bytes': 17325, 'sha256': 'd65bc8be6123a0bca8ef6e47db10c85b89ff487d9c2edfd5cc6c465e84c4b87f'}, 'layout': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\f9_structural_layout_preparation\\LAYOUT_ESTRUTURAL_3CMB_13BAO.json', 'bytes': 16475, 'sha256': '7581c71fb1a548fc1e20110137a3e3d940e363725096485de837bac56d3a2317'}, 'design': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\h0dn_documentary_review\\linear_design\\ESPECIFICACAO_LINEAR.json', 'bytes': 109887, 'sha256': '9aca9fffe3c7788d3c8ef1411b1dfa5c908c7366ef32ad969b14e59492199a95'}, 'measure': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\h0dn_documentary_review\\linear_design\\MEDIDA_NUISANCE_CANDIDATA.json', 'bytes': 6429, 'sha256': 'ef4e425026ee1047e1ca358e06aaf978c8ff9fdca9dbdcac8d0b09e8e6946895'}, 'MM_contract': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\f9_mm_model_preparation\\CONTRATO_MM_CANDIDATO.json', 'bytes': 15582, 'sha256': 'c7731bcc21e29cf94c7d835e86e94f6e16d666a0085de90f5137b270f669936b'}}
ASSEMBLY_SOURCE_PINS = {'resolver': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\f9_consolidated_draft\\RESOLUTOR_F9.json', 'bytes': 69740, 'sha256': 'c45de68d187fc49d5f79316b1561c9d9807dbb525019160837e8deea5e13ba53'}, 'background_layout': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\f9_structural_layout_preparation\\LAYOUT_ESTRUTURAL_3CMB_13BAO.json', 'bytes': 16475, 'sha256': '7581c71fb1a548fc1e20110137a3e3d940e363725096485de837bac56d3a2317'}, 'linear_design': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\h0dn_documentary_review\\linear_design\\ESPECIFICACAO_LINEAR.json', 'bytes': 109887, 'sha256': '9aca9fffe3c7788d3c8ef1411b1dfa5c908c7366ef32ad969b14e59492199a95'}, 'background_engine': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\f9_background_prediction\\background_controls.py', 'bytes': 15896, 'sha256': 'c41aee4bcd1d8a137df8d7541e53738e68e9a77605ec8e51d4051459544265a2'}, 'background_protocol': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\f9_background_prediction\\PROTOCOL.json', 'bytes': 7442, 'sha256': '13a2595f0d15fc194475ca7e977cacbcd45524a1d8637f92c0d7ebbae6a720eb'}, 'MM_contract': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\f9_mm_model_preparation\\CONTRATO_MM_CANDIDATO.json', 'bytes': 15582, 'sha256': 'c7731bcc21e29cf94c7d835e86e94f6e16d666a0085de90f5137b270f669936b'}}
MODELS = ("H1_TGL", "H2_LCDM", "H3_beta_free", "H4_Cepheid", "H5_rd_free")
STRUCTURAL_IDENTITY_PINS = {'row_ids': '4cda798ca1033de349098c7e9e36e95910b3e5e06f92e5d8f72f89fe5f7388c7', 'eta_columns': '19fdce4048603d9bd64c7d10d65b2dfe293851b6a8a718bd4234640e24beaa40', 'native_to_output_row_scale': '2270182f2b9ad44d7623b480c5f8bff83db501bccc095155fbd1014f2d58adef'}
N_ROWS, N_ETA = 283, 63
MAX_JSON_BYTES = 4 * 1024 * 1024
STRUCTURE_FIELDS = ("row_ids", "row_units", "native_to_output_row_scale",
                    "nuisance", "response_columns")
MEASURE = "common kappa d_eta; no absolute evidence"
COORDINATES = "NATIVE_EQUATION_Y_OFFSETS_ALREADY_INCLUDED"
OUTPUT_MEASURE = "EUCLIDEAN_ON_FIXED_TRANSFORMED_SUPPORT"
MM_STATUS = "CONDITIONAL_UNRATIFIED"


class ConsumerError(ValueError):
    """Engineering/admission failure; NEVER a zero-likelihood surrogate."""
    def __init__(self, code, detail):
        self.code, self.detail = code, detail
        super().__init__(f"{code}: {detail}")


def _require(ok, code, detail):
    if not ok:
        raise ConsumerError(code, detail)


def _keys(doc, required, label, exact=True):
    _require(type(doc) is dict, "SCHEMA_ERROR", label)
    ok = set(doc) == set(required) if exact else set(required) <= set(doc)
    _require(ok, "SCHEMA_ERROR", label + ": keys")


def _digest(value, label):
    _require(type(value) is str and re.fullmatch("[0-9a-f]{64}", value) is not None,
             "PIN_ERROR", label)
    return value


def _sha(raw):
    return hashlib.sha256(raw).hexdigest()


def _canonical(doc):
    return json.dumps(doc, sort_keys=True, ensure_ascii=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def _pairs(pairs):
    out = {}
    for key, value in pairs:
        _require(key not in out, "SCHEMA_ERROR", "duplicate JSON key")
        out[key] = value
    return out


def _constant(token):
    raise ConsumerError("SCHEMA_ERROR", "nonfinite JSON token")


def _json(raw, digest, label):
    _digest(digest, label)
    _require(type(raw) is bytes and 0 < len(raw) <= MAX_JSON_BYTES,
             "SCHEMA_ERROR", label + ": bounded JSON bytes required")
    _require(_sha(raw) == digest, "PIN_ERROR", label)
    try:
        doc = json.loads(raw, object_pairs_hook=_pairs, parse_constant=_constant)
    except (ValueError, UnicodeError, RecursionError) as exc:
        raise ConsumerError("SCHEMA_ERROR", label + ": invalid JSON") from exc
    _require(type(doc) is dict, "SCHEMA_ERROR", label)
    return doc


def _text(value, label):
    _require(type(value) is str and 0 < len(value) <= 4096,
             "SCHEMA_ERROR", label)
    return value


def _number(value, label):
    _require(type(value) in (int, float), "NUMERIC_ERROR", label)
    try:
        number = float(value)
    except (ValueError, OverflowError) as exc:
        raise ConsumerError("NUMERIC_ERROR", label) from exc
    _require(math.isfinite(number), "NUMERIC_ERROR", label)
    return number


def _reference(ref, label):
    _keys(ref, ("id", "sha256"), label)
    _text(ref["id"], label)
    _digest(ref["sha256"], label)


def _fraction(value, label):
    _require(type(value) is str and len(value) <= 64 and
             re.fullmatch(r"-?(?:0|[1-9][0-9]*)(?:/[1-9][0-9]*)?", value),
             "SCHEMA_ERROR", label + ": bounded rational string required")
    result = Fraction(value)
    _require(str(result) == value, "SCHEMA_ERROR", label + ": noncanonical rational")
    return result


def _row_ids(value):
    if type(value) is bytes:
        _require(len(value) <= MAX_JSON_BYTES, "ROW_ERROR", "row_ids bytes cap")
        try:
            value = json.loads(value, object_pairs_hook=_pairs, parse_constant=_constant)
        except (ValueError, UnicodeError, RecursionError) as exc:
            raise ConsumerError("ROW_ERROR", "invalid row_ids JSON") from exc
    _require(type(value) in (list, tuple) and len(value) == N_ROWS,
             "ROW_ERROR", "exactly 283 ordered row identifiers")
    ids = tuple(_text(v, "row identifier") for v in value)
    _require(len(set(ids)) == N_ROWS, "ROW_ERROR", "duplicate row identifier")
    return ids


def _structure(doc):
    _keys(doc, STRUCTURE_FIELDS, "structure")
    ids = _row_ids(doc["row_ids"])
    _require(_sha(_canonical(list(ids))) == STRUCTURAL_IDENTITY_PINS["row_ids"],
             "ROW_ERROR", "ordered rows differ from frozen layout/design metadata")
    _require(doc["row_units"] == ["dimensionless"] * 16 + ["mag"] * 267,
             "UNIT_ERROR", "fixed 16+267 target units")
    scales = doc["native_to_output_row_scale"]
    _require(type(scales) is list and len(scales) == N_ROWS and
             all(type(v) is int and v in (1, 5) for v in scales) and
             scales[:16] == [1] * 16 and scales.count(5) == 7,
             "UNIT_ERROR", "exactly seven native dex rows mapped by five")
    nuisance = doc["nuisance"]
    _keys(nuisance, ("columns", "X_sparse_rows", "dimension", "measure"), "nuisance")
    _require(type(nuisance["dimension"]) is int and nuisance["dimension"] == N_ETA and
             nuisance["measure"] == MEASURE, "MEASURE_ERROR", "same 63 eta and kappa")
    columns = nuisance["columns"]
    _require(_sha(_canonical(columns)) == STRUCTURAL_IDENTITY_PINS["eta_columns"] and
             _sha(_canonical(scales)) == STRUCTURAL_IDENTITY_PINS["native_to_output_row_scale"],
             "STRUCTURE_CHANGED", "eta order/T differ from frozen source metadata")
    _require(type(columns) is list and len(columns) == N_ETA, "ROW_ERROR", "63 columns")
    keys = []
    for col in columns:
        _keys(col, ("key", "unit"), "eta column")
        keys.append(_text(col["key"], "eta key"))
        _require(col["unit"] == "mag", "UNIT_ERROR", "eta coordinate")
    _require(len(set(keys)) == N_ETA, "ROW_ERROR", "duplicate eta column")
    rows = nuisance["X_sparse_rows"]
    _require(type(rows) is list and len(rows) == N_ROWS and rows[:16] == [{}] * 16,
             "ROW_ERROR", "283 X rows, zero background nuisance block")
    for row in rows:
        _require(type(row) is dict and set(row) <= set(keys), "ROW_ERROR", "X keys")
        for coefficient in row.values():
            _fraction(coefficient, "X coefficient already transformed")
    _keys(doc["response_columns"], ("a_h", "c_C"), "responses")
    for name, vec in doc["response_columns"].items():
        _require(type(vec) is list and len(vec) == N_ROWS and vec[:16] == ["0"] * 16,
                 "ROW_ERROR", name)
        for coefficient in vec:
            _fraction(coefficient, name + " already transformed")
    return ids, tuple(keys)


def extract_structure(assembly_json, *, assembly_sha256):
    """Return canonical structural bytes; caller must independently admit the hash.

    A projection produced here is not a scientific admission or authority.
    No means, priors, solver or observations are evaluated by this helper.
    """
    packet = _json(assembly_json, assembly_sha256, "assembly")
    _require(packet.get("schema") == "F9_FIVE_MODEL_PREDICTIONS_V1" and
             packet.get("status") == "ENGINEERING_ONLY", "SCHEMA_ERROR", "assembly schema")
    _keys(packet, STRUCTURE_FIELDS, "assembly structure", exact=False)
    structure = {key: packet[key] for key in STRUCTURE_FIELDS}
    _structure(structure)
    return _canonical(structure)


def _array(np, value, shape, label):
    # No object/string arrays, array-like coercion, pickle, NPZ or file paths.
    size = math.prod(shape)
    if type(value) is bytes:
        _require(len(value) == size * 8, "ARRAY_ERROR", label + ": raw <f8 length")
        out = np.frombuffer(value, dtype="<f8").reshape(shape).copy(order="C")
    else:
        _require(type(value) is np.ndarray and value.shape == shape and
                 value.dtype.kind == "f" and value.dtype.itemsize == 8,
                 "ARRAY_ERROR", label + ": float64 ndarray required")
        out = np.array(value, dtype="<f8", order="C", copy=True)
    _require(out.shape == shape and bool(np.isfinite(out).all()),
             "ARRAY_ERROR", label + ": shape/nonfinite")
    out.setflags(write=False)
    return out


def _diagnostic(check):
    names = ("rank", "nullity", "threshold", "null_residual_norm",
             "support_tolerance", "support_ok")
    return {name: check[name] for name in names}


def prepare_joint(y, C, row_ids, *, affine_origin_native, structure_json,
                  admission_json, admission_sha256, backend_receipt_json,
                  numpy_module, flat_gaussian_class):
    """Build one fixed full-covariance context from explicit admitted inputs.

    Loading/verifying the injected class and issuing the admission are external
    trusted-caller responsibilities. This function does not grant data access.
    """
    admission = _json(admission_json, admission_sha256, "caller admission")
    required = ("schema", "scope", "scenario_id", "data_kind", "input_sha256",
                "structure_sha256", "source_pins", "backend_receipt_sha256",
                "prediction_admission_sha256", "coordinates", "output_measure",
                "common_measure_id", "MM_status", "expected_support_rank",
                "tolerances", "references")
    _keys(admission, required, "caller admission")
    _require(admission["schema"] == "F9_CONSUMER_ADMISSION_V1" and
             admission["scope"] == "ENGINEERING_POINTWISE_ONLY", "ADMISSION_ERROR", "scope")
    _text(admission["scenario_id"], "scenario id")
    _text(admission["common_measure_id"], "common kappa and eta coordinate id")
    _require(admission["coordinates"] == COORDINATES and
             admission["output_measure"] == OUTPUT_MEASURE and
             admission["MM_status"] == MM_STATUS, "ADMISSION_ERROR", "units/measure/MM")
    _require(admission["source_pins"] == SOURCE_PINS, "PIN_ERROR", "qualified lineage")
    _digest(admission["prediction_admission_sha256"], "upstream admission")
    refs = admission["references"]
    required_refs = {"statistical_model", "covariance_and_cross_blocks",
                     "fixed_affine_support", "compression_and_offsets",
                     "common_nuisance_measure", "MM_conditional_model", "structure_review"}
    if admission["data_kind"] == "OPERATOR_RELEASED_OBSERVATIONS":
        required_refs |= {"operator_release", "V1"}
    else:
        _require(admission["data_kind"] == "SYNTHETIC", "ADMISSION_ERROR", "data kind")
        required_refs |= {"synthetic_fixture"}
    _keys(refs, required_refs, "external references")
    for name, ref in refs.items():
        _reference(ref, name)

    structure = _json(structure_json, admission["structure_sha256"], "admitted structure")
    ids, columns = _structure(structure)
    _require(_row_ids(row_ids) == ids, "ROW_ERROR", "y/C order must equal admitted order")
    backend = _json(backend_receipt_json, admission["backend_receipt_sha256"], "backend receipt")
    _keys(backend, ("schema", "source_pins", "runtime_reference", "class_module",
                    "class_name", "caller_verification_reference"), "backend receipt")
    _require(backend["schema"] == "F9_QUALIFIED_BACKEND_CALLER_RECEIPT_V1" and
             backend["source_pins"] == {k: SOURCE_PINS[k] for k in ("linear_gaussian", "support")},
             "PIN_ERROR", "backend source pins")
    _reference(backend["runtime_reference"], "numpy/runtime verification")
    _reference(backend["caller_verification_reference"], "loaded-object verification")
    _require(backend["class_name"] == "FlatNuisanceGaussian" and
             getattr(flat_gaussian_class, "__name__", None) == backend["class_name"] and
             getattr(flat_gaussian_class, "__module__", None) == backend["class_module"],
             "BACKEND_IDENTITY_ERROR", "caller-injected class metadata")
    _text(backend["class_module"], "backend class module")
    _require(getattr(numpy_module, "__name__", None) == "numpy",
             "BACKEND_IDENTITY_ERROR", "caller-injected numpy")
    # Metadata checks above do NOT authenticate arbitrary Python objects.

    tol = admission["tolerances"]
    _keys(tol, ("relative_cutoff", "absolute_cutoff", "support_tolerance",
                "design_relative_cutoff"), "mandatory units-aware tolerances")
    tol = {k: _number(v, k) for k, v in tol.items()}
    _require(all(v >= 0 for v in tol.values()) and
             tol["relative_cutoff"] < 1 and tol["design_relative_cutoff"] < 1,
             "TOLERANCE_ERROR", "explicit finite nonnegative tolerances")
    rank = admission["expected_support_rank"]
    _require(type(rank) is int and N_ETA <= rank <= N_ROWS,
             "RANK_ERROR", "independently admitted fixed support rank")
    pins = admission["input_sha256"]
    _keys(pins, ("y_native_f64le", "C_native_f64le", "affine_origin_native_f64le",
                 "row_ids_canonical_json"), "input pins")
    np = numpy_module
    yy = _array(np, y, (N_ROWS,), "y native")
    cc = _array(np, C, (N_ROWS, N_ROWS), "C native")
    oo = _array(np, affine_origin_native, (N_ROWS,), "fixed affine origin native")
    actual = {"y_native_f64le": _sha(yy.tobytes(order="C")),
              "C_native_f64le": _sha(cc.tobytes(order="C")),
              "affine_origin_native_f64le": _sha(oo.tobytes(order="C")),
              "row_ids_canonical_json": _sha(_canonical(list(ids)))}
    for name, expected in pins.items():
        _require(actual[name] == _digest(expected, name), "PIN_ERROR", name)

    scales = np.array(structure["native_to_output_row_scale"], dtype="<f8")
    # X and physical means supplied by assemble_five are ALREADY target-unit values.
    x = np.zeros((N_ROWS, N_ETA), dtype="<f8")
    column_index = {name: index for index, name in enumerate(columns)}
    for index, row in enumerate(structure["nuisance"]["X_sparse_rows"]):
        for name, value in row.items():
            x[index, column_index[name]] = float(_fraction(value, "X"))
    y_out = scales * yy
    covariance_out = (scales[:, None] * cc) * scales[None, :]
    origin_out = scales * oo
    _require(bool(np.isfinite(y_out).all()) and bool(np.isfinite(covariance_out).all()) and
             bool(np.isfinite(origin_out).all()) and bool(np.isfinite(x).all()),
             "TRANSFORM_ERROR", "nonfinite Ty/TCTt/Torigin/X")
    for array in (y_out, covariance_out, origin_out, x):
        array.setflags(write=False)
    try:
        engine = flat_gaussian_class(covariance_out, x, **tol)
    except Exception as exc:
        raise ConsumerError("BACKEND_PREPARATION_FAILED", type(exc).__name__ + ": " + str(exc)) from exc
    _require(engine.n == N_ROWS and engine.p == N_ETA and engine.support.rank == rank,
             "RANK_ERROR", "backend dimensions/rank differ from admission")
    return PreparedJoint(np, engine, y_out, origin_out, structure, admission,
                         admission_sha256, _sha(covariance_out.tobytes(order="C")))


class PreparedJoint:
    """Trusted in-process context; private internals must not be modified by caller."""
    def __init__(self, np, engine, y_out, origin_out, structure, admission,
                 admission_sha256, transformed_covariance_sha256):
        self._np, self._engine = np, engine
        self._y, self._origin = y_out, origin_out
        self._structure, self._admission = structure, admission
        self._admission_sha256 = admission_sha256
        self._transformed_covariance_sha256 = transformed_covariance_sha256

    def evaluate_five(self, assembly_json, *, assembly_sha256):
        """Pointwise log integral over d_eta, with common log(kappa) omitted.

        No physical prior is multiplied/integrated. No optimization, Bayes factor,
        calibration or verdict. Outside common affine support can be genuine zero.
        Engineering exceptions abort the whole call; no model is dropped.
        """
        packet = _json(assembly_json, assembly_sha256, "five-model packet")
        _require(packet.get("schema") == "F9_FIVE_MODEL_PREDICTIONS_V1" and
                 packet.get("status") == "ENGINEERING_ONLY", "SCHEMA_ERROR", "assembly schema")
        _keys(packet, (*STRUCTURE_FIELDS, "models", "identity", "certification",
                       "observed_outputs"), "packet", exact=False)
        structure = {key: packet[key] for key in STRUCTURE_FIELDS}
        _require(_canonical(structure) == _canonical(self._structure),
                 "STRUCTURE_CHANGED", "rows/units/T/eta/X/responses must remain fixed")
        identity = packet["identity"]
        _keys(identity, ("admission_sha256", "layout_sha256", "sources",
                         "background_packet_sha256"), "assembly identity", exact=False)
        _require(identity["sources"] == ASSEMBLY_SOURCE_PINS and
                 identity["layout_sha256"] == SOURCE_PINS["layout"]["sha256"] and
                 identity["admission_sha256"] == self._admission["prediction_admission_sha256"],
                 "PIN_ERROR", "assembly lineage/admission")
        _digest(identity["background_packet_sha256"], "background packet")
        _require(packet["observed_outputs"] == {"chi2": None, "p": None, "sigma": None, "lnB": None},
                 "SCHEMA_ERROR", "upstream must not transport an observed verdict")
        _require(packet["certification"] == {"status": "UNBOUNDED_THEORY_ERROR",
                 "uniform_error_bound": None, "certified": False, "numerical_certificate": None},
                 "SCHEMA_ERROR", "engineering packet is not a numerical certificate")
        _keys(packet["models"], MODELS, "complete five-model family")
        prepared = {}
        for model in MODELS:
            record = packet["models"][model]
            _keys(record, ("mean_without_nuisance", "parameters", "prior"),
                  model, exact=False)
            means = record["mean_without_nuisance"]
            _require(type(means) is list and len(means) == N_ROWS,
                     "ROW_ERROR", model + ": mean vector")
            means = [_number(v, model + ": mean") for v in means]
            mu = self._np.array(means, dtype="<f8")
            try:
                support = self._engine.support.evaluate(mu - self._origin)
            except Exception as exc:
                raise ConsumerError("BACKEND_SUPPORT_FAILED",
                                    model + ": " + type(exc).__name__ + ": " + str(exc)) from exc
            _require(math.isfinite(support["null_residual_norm"]) and support["support_ok"],
                     "AFFINE_SUPPORT_CHANGED", model + ": mean not on admitted affine support")
            prepared[model] = (mu, record, _diagnostic(support))

        outputs = {}
        for model in MODELS:
            mu, record, mean_support = prepared[model]
            residual = self._y - mu
            try:
                check = self._engine.support.evaluate(residual)
                value = self._engine.log_integral(residual)
            except Exception as exc:
                raise ConsumerError("BACKEND_EVALUATION_FAILED",
                                    model + ": " + type(exc).__name__ + ": " + str(exc)) from exc
            _require(math.isfinite(check["null_residual_norm"]), "BACKEND_DIAGNOSTIC_ERROR", model)
            if check["support_ok"]:
                _require(math.isfinite(value), "BACKEND_VALUE_ERROR", model + ": inside support")
                status = "FINITE_LOG_FLAT_INTEGRAL"
            else:
                _require(value == float("-inf"), "BACKEND_VALUE_ERROR", model + ": outside support")
                status = "ZERO_DENSITY_OUTSIDE_FIXED_AFFINE_SUPPORT"
            outputs[model] = {"status": status, "log_integral_deta": value,
                              "residual_support": _diagnostic(check),
                              "mean_support": mean_support,
                              "parameters": record["parameters"],
                              "prior_metadata_not_applied": record["prior"]}
        return {"schema": "F9_POINTWISE_FLAT_CONSUMER_RESULT_V1",
                "status": "ENGINEERING_ONLY", "models": outputs,
                "scope": "POINTWISE_IN_PHYSICAL_PARAMETERS_NO_EVIDENCE",
                "MM_status": MM_STATUS, "measure": MEASURE,
                "output_measure": OUTPUT_MEASURE,
                "common_measure_id": self._admission["common_measure_id"],
                "normalization": {"rank": self._engine.support.rank, "eta_dimension": N_ETA,
                                  "log_prefactor": self._engine.log_prefactor,
                                  "common_log_kappa_omitted": True},
                "provenance": {"admission_sha256": self._admission_sha256,
                               "assembly_sha256": assembly_sha256,
                               "source_pins": SOURCE_PINS,
                               "transformed_covariance_sha256": self._transformed_covariance_sha256},
                "certification": packet["certification"],
                "absolute_evidence": None, "lnB": None, "p": None, "sigma": None,
                "fit": None, "verdict": None}
