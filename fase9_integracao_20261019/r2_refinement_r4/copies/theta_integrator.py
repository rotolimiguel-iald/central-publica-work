"""Preparation only: full-box theta integration of five conditional priors.

No candidate/backend imports, I/O, background solver, executor or authorization.
The trusted future controller owns durable per-node idempotence and loaded code.
"""
import hashlib
import itertools
import json
import math

REQUEST_ID = "ad02511d-1536-4a1b-a6c4-fb3e5eb26550"
PRIOR_REQUEST_ID = "df482198-56c4-4169-ae5e-3908f5d12f2c"
SOURCE_PINS = {'f9_physical_prior_preparation/physical_prior.py': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\f9_physical_prior_preparation\\physical_prior.py', 'bytes': 21629, 'sha256': '4fbae1160282875c4ed61c242361c14db9434416a1886d41905c79f0a4f7a3f6'}, 'f9_physical_prior_preparation/CONTRATO_API.json': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\f9_physical_prior_preparation\\CONTRATO_API.json', 'bytes': 6777, 'sha256': '96dbd03f15ac8614eba760b8775145014d9684d1e51a5f63a1cad9303a0c1a03'}, 'f9_five_model_assembly_preparation/five_model_assembly.py': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\f9_five_model_assembly_preparation\\five_model_assembly.py', 'bytes': 17325, 'sha256': 'd65bc8be6123a0bca8ef6e47db10c85b89ff487d9c2edfd5cc6c465e84c4b87f'}, 'f9_consolidated_draft/RESOLUTOR_F9.json': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\f9_consolidated_draft\\RESOLUTOR_F9.json', 'bytes': 69740, 'sha256': 'c45de68d187fc49d5f79316b1561c9d9807dbb525019160837e8deea5e13ba53'}, 'f9_likelihood_consumer_preparation/likelihood_consumer.py': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\f9_likelihood_consumer_preparation\\likelihood_consumer.py', 'bytes': 24982, 'sha256': '6776bb660f6b8565c7282f937ecdc5239d5b941cce3e257aa6155379c9ccd6a5'}}
PRIOR_SOURCE_PINS = {'f9_likelihood_consumer_preparation/likelihood_consumer.py': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\f9_likelihood_consumer_preparation\\likelihood_consumer.py', 'bytes': 24982, 'sha256': '6776bb660f6b8565c7282f937ecdc5239d5b941cce3e257aa6155379c9ccd6a5'}, 'f9_five_model_assembly_preparation/five_model_assembly.py': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\f9_five_model_assembly_preparation\\five_model_assembly.py', 'bytes': 17325, 'sha256': 'd65bc8be6123a0bca8ef6e47db10c85b89ff487d9c2edfd5cc6c465e84c4b87f'}, 'covariance_support/linear_gaussian.py': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\covariance_support\\linear_gaussian.py', 'bytes': 3772, 'sha256': '7dc486b5568876385f4b2e6647e0f449accfea0862c3b0d46ce90d657fba2736'}, 'covariance_support/singular_gaussian_v2.py': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\covariance_support\\singular_gaussian_v2.py', 'bytes': 4953, 'sha256': '98264bdd57aaad0904bd342631fd3c147fa19f90e8922f0ad6b15ac1b3b93374'}, 'f9_consolidated_draft/RESOLUTOR_F9.json': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\f9_consolidated_draft\\RESOLUTOR_F9.json', 'bytes': 69740, 'sha256': 'c45de68d187fc49d5f79316b1561c9d9807dbb525019160837e8deea5e13ba53'}}
MODELS = ("H1_TGL", "H2_LCDM", "H3_beta_free", "H4_Cepheid", "H5_rd_free")
THETA_NAMES = ("H0", "ombh2", "omch2")
BOUNDS = ((50.0, 90.0), (0.015, 0.030), (0.08, 0.18))
MAX_LEVEL = 6  # Schema ceiling, not an execution budget or recommendation.
MAX_CALLBACKS = 300000
CERTIFICATION = {"status": "UNBOUNDED_THEORY_ERROR", "uniform_error_bound": None,
                 "certified": False, "numerical_certificate": None}
MEASURE = "common kappa d_eta; no absolute evidence"
OUTPUT_MEASURE = "EUCLIDEAN_ON_FIXED_TRANSFORMED_SUPPORT"


class ThetaError(ValueError):
    """Terminal engineering/admission failure; never a likelihood-zero fallback."""
    def __init__(self, code, detail):
        self.code, self.detail = code, detail
        super().__init__(f"{code}: {detail}")


def _require(ok, code, detail):
    if not ok:
        raise ThetaError(code, detail)


def _keys(obj, expected, label, exact=True):
    _require(type(obj) is dict, "SCHEMA_ERROR", label)
    _require(set(obj) == set(expected) if exact else set(expected) <= set(obj),
             "SCHEMA_ERROR", label + ": fields")


def _finite(x, label):
    _require(type(x) in (int, float), "NUMERIC_ERROR", label)
    try:
        value = float(x)
    except (OverflowError, ValueError) as exc:
        raise ThetaError("NUMERIC_ERROR", label) from exc
    _require(math.isfinite(value), "NUMERIC_ERROR", label)
    return value


def _text(x, label):
    _require(type(x) is str and 0 < len(x) <= 512, "SCHEMA_ERROR", label)
    return x


def _digest(x, label):
    _require(type(x) is str and len(x) == 64 and all(c in "0123456789abcdef" for c in x),
             "PIN_ERROR", label)
    return x


def _reference(x, label):
    _keys(x, ("id", "sha256"), label)
    _text(x["id"], label)
    _digest(x["sha256"], label)


def _canonical(x):
    return json.dumps(x, sort_keys=True, ensure_ascii=True,
                      separators=(",", ":"), allow_nan=False).encode("utf-8")


def _sha(x):
    return hashlib.sha256(x).hexdigest()


def _pairs(pairs):
    out = {}
    for key, value in pairs:
        _require(key not in out, "SCHEMA_ERROR", "duplicate JSON key")
        out[key] = value
    return out


def _bad_constant(token):
    raise ThetaError("SCHEMA_ERROR", "nonfinite JSON token")


def _json(raw, digest):
    _digest(digest, "plan digest")
    _require(type(raw) is bytes and 0 < len(raw) <= 65536, "SCHEMA_ERROR", "plan bytes")
    _require(_sha(raw) == digest, "PIN_ERROR", "plan")
    try:
        return json.loads(raw, object_pairs_hook=_pairs, parse_constant=_bad_constant)
    except (ValueError, UnicodeError, RecursionError) as exc:
        raise ThetaError("SCHEMA_ERROR", "plan JSON") from exc


def _json_ready(value, path=()):
    """Defined transport encoding of the one legitimate nonfinite output field."""
    _require(len(path) <= 64, "SCHEMA_ERROR", "conditional metadata depth")
    if value is None or type(value) in (str, bool, int):
        return value
    if type(value) is float:
        if value == float("-inf"):
            _require(len(path) == 3 and path[0] == "models" and path[1] in MODELS
                     and path[2] == "log_conditional_integral",
                     "NUMERIC_ERROR", "nonfinite field outside conditional integral")
            return {"$float": "-inf"}
        _require(math.isfinite(value), "NUMERIC_ERROR", "nonfinite conditional field")
        return value
    if type(value) is list:
        return [_json_ready(v, path + (i,)) for i, v in enumerate(value)]
    if type(value) is dict:
        _require(all(type(k) is str for k in value), "SCHEMA_ERROR", "JSON field names")
        return {k: _json_ready(v, path + (k,)) for k, v in value.items()}
    raise ThetaError("SCHEMA_ERROR", "conditional output must contain native JSON types")


def canonical_conditional_sha256(result):
    """Digest of native df482 result, with log-integral -inf explicitly tagged."""
    raw = _canonical(_json_ready(result))
    _require(len(raw) <= 4194304, "SCHEMA_ERROR", "conditional result metadata cap")
    return _sha(raw)


def _node_key(indices, denominator):
    a, b, c = indices
    while denominator > 1 and a % 2 == b % 2 == c % 2 == 0:
        a, b, c, denominator = a // 2, b // 2, c // 2, denominator // 2
    return (a, b, c, denominator)


def _theta(key):
    denominator = key[3]
    return tuple(lo if num == 0 else hi if num == denominator
                 else lo + (hi - lo) * (num / denominator)
                 for num, (lo, hi) in zip(key[:3], BOUNDS))


def _integer_weight(i, n):
    return 1 if i in (0, n) else 4 if i % 2 else 2


class ThetaIntegrator:
    """Single use in-process; cannot substitute for the controller's durable ledger."""
    def __init__(self, plan_json, *, plan_sha256, evaluate_node):
        p = _json(plan_json, plan_sha256)
        _keys(p, ("schema", "preparation_request_id", "execution_unit_id", "source_pins",
                  "consumer_admission_sha256", "assembly_admission_sha256", "engine_configuration_sha256",
                  "callback_reference", "controller_reference",
                  "first_level", "last_level", "max_callback_calls",
                  "absolute_log_refinement_target", "common_measure_id"), "plan")
        _require(p["schema"] == "F9_THETA_INTEGRATION_PLAN_V1"
                 and p["preparation_request_id"] == REQUEST_ID
                 and p["source_pins"] == SOURCE_PINS, "PIN_ERROR", "preparation/lineage")
        _text(p["execution_unit_id"], "execution unit")
        _require(p["execution_unit_id"] != REQUEST_ID, "IDENTITY_ERROR",
                 "preparation ID is not a future execution ID")
        for field in ("consumer_admission_sha256", "assembly_admission_sha256", "engine_configuration_sha256"):
            _digest(p[field], field)
        for key in ("callback_reference", "controller_reference"):
            _reference(p[key], key)
        _text(p["common_measure_id"], "common measure ID")
        lo, hi = p["first_level"], p["last_level"]
        _require(type(lo) is int and type(hi) is int and 1 <= lo < hi <= MAX_LEVEL,
                 "GRID_ERROR", "at least two consecutive dyadic levels")
        cap = p["max_callback_calls"]
        _require(type(cap) is int and 1 <= cap <= MAX_CALLBACKS,
                 "BUDGET_ERROR", "explicit callback cap")
        required = ((1 << hi) + 1) ** 3
        _require(required <= cap, "BUDGET_ERROR",
                 "cap must cover complete finest grid before any callback")
        target = _finite(p["absolute_log_refinement_target"], "refinement target")
        _require(target > 0, "PRECISION_ERROR", "explicit positive target")
        _require(callable(evaluate_node), "CALLBACK_ERROR", "callable required")
        self._plan, self._plan_sha, self._callback = p, plan_sha256, evaluate_node
        self._state = "PREPARED"
        self._cache, self._attempted, self._background_seen = {}, set(), set()
        self._attempts, self._completed = 0, 0
        self._active, self._failure = None, None
        self._common = None
        self._chain = _sha(plan_json)
        self._required = required
        self._quality = {"service_unassessed": 0, "service_not_converged": 0,
                         "conditional_underflowed_nodes": 0}
        self._levels = []
        self._background_counts = {"new_calls_declared": 0, "durable_cache_hits_declared": 0}

    def diagnostics(self):
        return {"state": self._state, "callback_attempts": self._attempts,
                "callback_completed": self._completed, "active_node": self._active,
                "failure": self._failure, "completed_node_chain_sha256": self._chain,
                "completed_levels": len(self._levels),
                "no_interprocess_idempotence_claim": True}

    def _descriptor(self, key):
        core = {"execution_unit_id": self._plan["execution_unit_id"],
                "consumer_admission_sha256": self._plan["consumer_admission_sha256"],
                "callback_reference": self._plan["callback_reference"],
                "assembly_admission_sha256": self._plan["assembly_admission_sha256"],
                "engine_configuration_sha256": self._plan["engine_configuration_sha256"],
                "dyadic_numerators": list(key[:3]), "dyadic_denominator": key[3]}
        return {**core, "node_id": _sha(_canonical(core)), "theta": list(_theta(key)),
                "theta_names": list(THETA_NAMES), "five_models": list(MODELS)}

    def _accept(self, envelope, descriptor):
        _keys(envelope, ("conditional_result", "receipt"), "callback envelope")
        result, receipt = envelope["conditional_result"], envelope["receipt"]
        _keys(receipt, ("node_id", "execution_unit_id", "callback_reference",
                        "conditional_result_reference", "background_execution_reference",
                        "background_attempts", "background_successes", "background_origin",
                        "background_calls_this_callback", "assembly_admission_sha256",
                        "engine_configuration_sha256"), "node receipt")
        _require(receipt["node_id"] == descriptor["node_id"]
                 and receipt["execution_unit_id"] == self._plan["execution_unit_id"]
                 and receipt["callback_reference"] == self._plan["callback_reference"],
                 "PIN_ERROR", "callback/node identity")
        for field in ("assembly_admission_sha256", "engine_configuration_sha256"):
            _require(receipt[field] == self._plan[field], "PIN_ERROR", "fixed global grid configuration/admission")
        for key in ("conditional_result_reference", "background_execution_reference"):
            _reference(receipt[key], key)
        _require(type(receipt["background_attempts"]) is int
                 and type(receipt["background_successes"]) is int
                 and receipt["background_attempts"] == receipt["background_successes"] == 1,
                 "BACKGROUND_ERROR", "original successful shared background receipt required")
        origin = receipt["background_origin"]
        _require(origin in ("NEW_EXECUTION", "VERIFIED_DURABLE_CACHE"), "BACKGROUND_ERROR", "background origin")
        new_calls = receipt["background_calls_this_callback"]
        _require(type(new_calls) is int and new_calls == (1 if origin == "NEW_EXECUTION" else 0),
                 "BACKGROUND_ERROR", "new call count versus durable cache")
        digest = canonical_conditional_sha256(result)
        _require(receipt["conditional_result_reference"]["sha256"] == digest,
                 "PIN_ERROR", "conditional result fingerprint")
        _keys(result, ("schema", "status", "request_id", "models", "theta", "base_theta_prior",
                       "measure", "output_measure", "normalization", "MM_status", "certification",
                       "precision_scope", "provenance", "absolute_evidence",
                       "theta_integrated_evidence", "lnB", "p", "sigma", "verdict"), "df482 result")
        _require(result["schema"] == "F9_CONDITIONAL_PHYSICAL_PRIOR_RESULT_V1"
                 and result["status"] == "ENGINEERING_ONLY"
                 and result["request_id"] == PRIOR_REQUEST_ID, "SCHEMA_ERROR", "df482 identity")
        _require(type(result["theta"]) is list and len(result["theta"]) == 3
                 and tuple(_finite(x, "theta") for x in result["theta"]) == tuple(descriptor["theta"]),
                 "IDENTITY_ERROR", "callback theta")
        _require(result["base_theta_prior"] == {"density_exact": "50/3", "applied": False,
                                               "integrated": False},
                 "PRIOR_ERROR", "base prior not previously applied/integrated")
        _require(result["measure"] == MEASURE and result["output_measure"] == OUTPUT_MEASURE
                 and result["MM_status"] == "CONDITIONAL_UNRATIFIED"
                 and result["certification"] == CERTIFICATION,
                 "MEASURE_ERROR", "same experiment, MM and engineering status")
        _require(all(result[k] is None for k in ("absolute_evidence", "theta_integrated_evidence",
                                               "lnB", "p", "sigma", "verdict")),
                 "SCHEMA_ERROR", "conditional callback cannot transport an observed verdict")
        _keys(result["normalization"], ("rank", "eta_dimension", "log_prefactor",
                                        "common_log_kappa_omitted"), "normalization")
        normal = result["normalization"]
        _require(type(normal["rank"]) is int and 63 <= normal["rank"] <= 283
                 and type(normal["eta_dimension"]) is int and normal["eta_dimension"] == 63
                 and normal["common_log_kappa_omitted"] is True,
                 "MEASURE_ERROR", "fixed nuisance normalization")
        _finite(normal["log_prefactor"], "log prefactor")
        common = _canonical({k: result[k] for k in ("measure", "output_measure", "normalization",
                                                   "MM_status", "certification")})
        _require(self._common is None or self._common == common,
                 "MEASURE_CHANGED", "context/normalization changed across theta")
        self._common = common
        provenance = result["provenance"]
        _keys(provenance, ("source_pins", "assembly_sha256", "background_sha256",
                           "consumer_admission_sha256", "precision_sha256"), "provenance")
        _require(provenance["source_pins"] == PRIOR_SOURCE_PINS
                 and provenance["consumer_admission_sha256"] == self._plan["consumer_admission_sha256"],
                 "PIN_ERROR", "fixed context and conditional implementation")
        for key in ("assembly_sha256", "background_sha256", "precision_sha256"):
            _digest(provenance[key], key)
        _require(provenance["background_sha256"] not in self._background_seen,
                 "BACKGROUND_ERROR", "same background packet reused at a different theta")
        _keys(result["models"], MODELS, "complete family")
        values = []
        for index, model in enumerate(MODELS):
            rec = result["models"][model]
            _keys(rec, ("log_conditional_integral", "status", "method"), model, exact=False)
            _text(rec["method"], model + " method")
            value = rec["log_conditional_integral"]
            zero_status = ("ZERO_DENSITY_OUTSIDE_FIXED_AFFINE_SUPPORT" if index < 2
                           else "ZERO_DENSITY_ON_COMMON_AFFINE_SUPPORT_COMPLEMENT")
            finite_status = (("FINITE_LOG_FLAT_INTEGRAL",) if index < 2 else
                             ("ENGINEERING_ESTIMATE", "FLAT_EXTRA_IN_PROJECTED_FLOAT_GEOMETRY"))
            if type(value) is float and value == float("-inf"):
                _require(rec["status"] == zero_status, "DENSITY_ERROR", "unexplained zero")
            else:
                value = _finite(value, model + " log conditional integral")
                _require(rec["status"] in finite_status, "DENSITY_ERROR", "finite status")
            values.append(value)
            service = rec.get("precision")
            if type(service) is dict and "error_kind" in service:
                self._quality["service_unassessed"] += int(service["error_kind"] == "UNASSESSED")
                self._quality["service_not_converged"] += int(service.get("converged") is not True)
            counters = rec.get("counters")
            if type(counters) is dict and "underflowed_nodes" in counters:
                count = counters["underflowed_nodes"]
                _require(type(count) is int and count >= 0, "SCHEMA_ERROR", "underflow counter")
                self._quality["conditional_underflowed_nodes"] += count
        self._background_counts["new_calls_declared"] += new_calls
        self._background_counts["durable_cache_hits_declared"] += int(origin == "VERIFIED_DURABLE_CACHE")
        self._background_seen.add(provenance["background_sha256"])
        return tuple(values), digest, receipt

    def _evaluate(self, key):
        if key in self._cache:
            return
        _require(key not in self._attempted, "REPLAY_ERROR", "uncertain node cannot repeat")
        _require(self._attempts < self._plan["max_callback_calls"], "BUDGET_ERROR", "callback cap")
        descriptor = self._descriptor(key)
        self._attempted.add(key)  # Before the call: exceptions leave it consumed in this instance.
        self._active = descriptor["node_id"]
        self._attempts += 1
        envelope = self._callback(descriptor)
        values, digest, receipt = self._accept(envelope, descriptor)
        self._cache[key] = values  # Only complete validated five-model results are reusable.
        self._chain = _sha(_canonical({"previous": self._chain, "node": descriptor,
                                       "conditional_sha256": digest, "receipt": receipt}))
        self._completed += 1
        self._active = None

    def _terms(self, n, model_index):
        denominator_log = 3 * math.log(3 * n)
        for indices in itertools.product(range(n + 1), repeat=3):
            key = _node_key(indices, n)
            value = self._cache[key][model_index]
            if value != float("-inf"):
                numerator = math.prod(_integer_weight(i, n) for i in indices)
                term = math.fsum((value, math.log(numerator), -denominator_log))
                _require(math.isfinite(term), "NUMERIC_ERROR", "weighted log contribution")
                yield term, key, any(i in (0, n) for i in indices), value

    def _level_result(self, level):
        n, models = 1 << level, {}
        for index, model in enumerate(MODELS):
            maximum, peak, positive = float("-inf"), None, 0
            sample_max, sample_peak = float("-inf"), None
            for term, key, boundary, unweighted in self._terms(n, index):
                positive += 1
                if term > maximum:
                    maximum, peak = term, key
                if unweighted > sample_max:
                    sample_max, sample_peak = unweighted, key
            if positive == 0:
                # Keep refining the entire box; sampled zeros alone are not zero integrated mass.
                models[model] = {"log_relative_integral_without_log_kappa": None,
                                 "status": "NO_POSITIVE_SAMPLED_MASS",
                                 "positive_nodes": 0, "support_zero_nodes": (n + 1) ** 3}
                continue
            scaled, boundary_scaled, underflow = [], [], 0
            for term, key, boundary, unweighted in self._terms(n, index):
                value = math.exp(term - maximum)
                underflow += int(value == 0)
                scaled.append(value)
                if boundary:
                    boundary_scaled.append(value)
            total = math.fsum(scaled)
            value = math.fsum((maximum, math.log(total)))
            _require(math.isfinite(value), "NUMERIC_ERROR", "positive sampled integral log")
            models[model] = {
                "log_relative_integral_without_log_kappa": value,
                "status": "POSITIVE_PRODUCT_RULE_ENGINEERING_ESTIMATE",
                "positive_nodes": positive, "support_zero_nodes": (n + 1) ** 3 - positive,
                "summation_underflowed_terms": underflow,
                "largest_weighted_node_fraction": 1 / total,
                "boundary_weight_fraction": math.fsum(boundary_scaled) / total,
                "largest_weighted_node": self._descriptor(peak)["node_id"],
                "largest_unweighted_node": self._descriptor(sample_peak)["node_id"],
                "largest_unweighted_log_value": sample_max}
        return {"level": level, "intervals_per_axis": n, "nodes_in_rule": (n + 1) ** 3,
                "models": models}

    def run(self):
        _require(self._state == "PREPARED", "REPLAY_ERROR", "instance is single-use")
        self._state = "RUNNING"
        try:
            for level in range(self._plan["first_level"], self._plan["last_level"] + 1):
                n = 1 << level
                for indices in itertools.product(range(n + 1), repeat=3):
                    self._evaluate(_node_key(indices, n))
                self._levels.append(self._level_result(level))
            _require(self._completed == self._required == self._attempts,
                     "COUNT_ERROR", "complete nested finest grid")
            final, previous = self._levels[-1]["models"], self._levels[-2]["models"]
            _require(all(final[m]["log_relative_integral_without_log_kappa"] is not None
                         for m in MODELS), "NO_POSITIVE_SAMPLED_MASS",
                     "finest sampled zero is not certified zero integral; no partial family")
            estimates = {m: final[m]["log_relative_integral_without_log_kappa"] for m in MODELS}
            gaps = {}
            for model in MODELS:
                old = previous[model]["log_relative_integral_without_log_kappa"]
                gaps[model] = None if old is None else abs(math.fsum((estimates[model], -old)))
                if gaps[model] is not None:
                    _require(math.isfinite(gaps[model]), "NUMERIC_ERROR", "log refinement gap")
            ratios = {m: math.fsum((estimates[m], -estimates["H2_LCDM"])) for m in MODELS}
            _require(all(math.isfinite(x) for x in ratios.values()), "NUMERIC_ERROR", "log ratios")
            result = {
                "schema": "F9_THETA_RELATIVE_INTEGRATION_RESULT_V1", "status": "ENGINEERING_ONLY",
                "preparation_request_id": REQUEST_ID, "execution_unit_id": self._plan["execution_unit_id"],
                "plan_sha256": self._plan_sha, "algorithm": "POSITIVE_NESTED_COMPOSITE_SIMPSON",
                "models": {m: {"log_relative_evidence_without_common_log_kappa": estimates[m]}
                           for m in MODELS},
                "lnB_against_H2_same_context": ratios,
                "prior": {"coordinates": list(THETA_NAMES), "bounds": [list(x) for x in BOUNDS],
                          "density_exact": "50/3", "box_jacobian_exact": "3/50",
                          "unit_cube_density_exact": "1", "box_complete_rule": True},
                "refinement": {"last_absolute_log_difference": gaps,
                               "requested_target": self._plan["absolute_log_refinement_target"],
                               "indicator_satisfied": all(v is not None and v <= self._plan["absolute_log_refinement_target"]
                                                          for v in gaps.values()),
                               "error_kind": "HEURISTIC_LEVEL_DIFFERENCE_NOT_CERTIFIED",
                               "global_convergence": None, "unresolved_peak_mass_bound": None,
                               "all_declared_levels_completed": True, "early_stopping": False},
                "levels": self._levels, "callback_counts": {"attempted": self._attempts,
                    "completed": self._completed, "required_unique_nodes": self._required,
                    "background_calls": dict(self._background_counts),
                    "background_count_scope": "declared receipts, including verified durable cache; not independently instrumented here"},
                "conditional_precision_summary": self._quality,
                "normalization": json.loads(self._common)["normalization"],
                "common_measure_id": self._plan["common_measure_id"], "measure": MEASURE,
                "output_measure": OUTPUT_MEASURE, "MM_status": "CONDITIONAL_UNRATIFIED",
                "certification": CERTIFICATION.copy(), "absolute_evidence": None,
                "p": None, "sigma": None, "verdict": None,
                "precision_scope": "Outer level differences do not bound missed peaks or inherited inner/background errors.",
                "provenance": {"source_pins": SOURCE_PINS,
                    "consumer_admission_sha256": self._plan["consumer_admission_sha256"],
                    "callback_reference": self._plan["callback_reference"],
                    "controller_reference": self._plan["controller_reference"],
                    "assembly_admission_sha256": self._plan["assembly_admission_sha256"],
                    "engine_configuration_sha256": self._plan["engine_configuration_sha256"],
                    "completed_node_chain_sha256": self._chain}}
            self._state = "COMPLETED"
            return result
        except BaseException as exc:
            self._state = "FAILED_TERMINAL"
            self._failure = {"type": type(exc).__name__, "code": getattr(exc, "code", None),
                             "node_id": self._active, "partial_family_returned": False}
            raise
