"""Prepared F9 conditional physical-prior integrals, never executed in this unit.

Trusted caller injects the frozen consumer/context and precision services.
No new Gaussian solver, CAMB call, file access, optimizer or data release.
"""
import math

REQUEST_ID = "df482198-56c4-4169-ae5e-3908f5d12f2c"
SOURCE_PINS = {'f9_likelihood_consumer_preparation/likelihood_consumer.py': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\f9_likelihood_consumer_preparation\\likelihood_consumer.py', 'bytes': 24982, 'sha256': '6776bb660f6b8565c7282f937ecdc5239d5b941cce3e257aa6155379c9ccd6a5'}, 'f9_five_model_assembly_preparation/five_model_assembly.py': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\f9_five_model_assembly_preparation\\five_model_assembly.py', 'bytes': 17325, 'sha256': 'd65bc8be6123a0bca8ef6e47db10c85b89ff487d9c2edfd5cc6c465e84c4b87f'}, 'covariance_support/linear_gaussian.py': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\covariance_support\\linear_gaussian.py', 'bytes': 3772, 'sha256': '7dc486b5568876385f4b2e6647e0f449accfea0862c3b0d46ce90d657fba2736'}, 'covariance_support/singular_gaussian_v2.py': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\covariance_support\\singular_gaussian_v2.py', 'bytes': 4953, 'sha256': '98264bdd57aaad0904bd342631fd3c147fa19f90e8922f0ad6b15ac1b3b93374'}, 'f9_consolidated_draft/RESOLUTOR_F9.json': {'path': 'C:\\IALD\\Central de Patentes\\Chatgpt\\TUNEL\\DO_CHATGPT\\ORDEM_018\\f9_consolidated_draft\\RESOLUTOR_F9.json', 'bytes': 69740, 'sha256': 'c45de68d187fc49d5f79316b1561c9d9807dbb525019160837e8deea5e13ba53'}}
MODELS = ("H1_TGL", "H2_LCDM", "H3_beta_free", "H4_Cepheid", "H5_rd_free")
BETA_LIMITS = (-0.05, 0.05)
S_LIMITS = (-0.15, 0.15)
RD_LIMITS = (130.0, 160.0)


class PriorError(ValueError):
    """Engineering/admission failure, never a substitute likelihood zero."""
    def __init__(self, code, detail):
        self.code, self.detail = code, detail
        super().__init__(f"{code}: {detail}")


def _require(ok, code, detail):
    if not ok:
        raise PriorError(code, detail)


def _finite(x, label):
    _require(type(x) in (int, float), "NUMERIC_ERROR", label)
    try:
        value = float(x)
    except (ValueError, OverflowError) as exc:
        raise PriorError("NUMERIC_ERROR", label) from exc
    _require(math.isfinite(value), "NUMERIC_ERROR", label)
    return value


def _service_result(result, service_id, value_key):
    _require(type(result) is dict, "SERVICE_ERROR", "mapping required")
    _require(set(result) == {"service_id", "status", value_key, "error_estimate",
                            "error_kind", "converged", "evaluations", "method"},
             "SERVICE_ERROR", "unexpected precision receipt fields")
    _require(result["service_id"] == service_id and result["status"] == "ENGINEERING_ESTIMATE",
             "SERVICE_ERROR", "service identity/status")
    _require(type(result["converged"]) is bool and type(result["evaluations"]) is int and
             result["evaluations"] >= 0 and type(result["method"]) is str and result["method"],
             "SERVICE_ERROR", "service diagnostics")
    if result["error_kind"] == "UNASSESSED":
        _require(result["error_estimate"] is None, "SERVICE_ERROR", "unassessed error")
    else:
        _require(result["error_kind"] == "ESTIMATED_NOT_CERTIFIED",
                 "SERVICE_ERROR", "no certification promoted from service flags")
        _require(_finite(result["error_estimate"], "estimated error") >= 0,
                 "SERVICE_ERROR", "negative error")
    value = _finite(result[value_key], value_key)
    return value


def _precision(consumer, raw, digest):
    doc = consumer._json(raw, digest, "physical-prior precision admission")
    consumer._keys(doc, ("schema", "source_pins", "consumer_admission_sha256",
                         "assembly_sha256", "services", "max_quadrature_evaluations",
                         "max_window_evaluations", "absolute_log_error_target",
                         "absolute_scaled_error_target", "relative_scaled_error_target",
                         "caller_verification_reference"), "precision admission")
    _require(doc["schema"] == "F9_PHYSICAL_PRIOR_PRECISION_V1" and
             doc["source_pins"] == SOURCE_PINS, "PIN_ERROR", "frozen dependencies")
    for key in ("consumer_admission_sha256", "assembly_sha256"):
        consumer._digest(doc[key], key)
    consumer._reference(doc["caller_verification_reference"], "loaded precision services")
    consumer._keys(doc["services"], ("log_exp_quad_interval", "positive_quad_1d"), "services")
    for key, reference in doc["services"].items():
        consumer._reference(reference, key)
    for name in ("max_quadrature_evaluations", "max_window_evaluations"):
        _require(type(doc[name]) is int and 1 <= doc[name] <= 1000000,
                 "BUDGET_ERROR", name)
    for name in ("absolute_log_error_target", "absolute_scaled_error_target",
                 "relative_scaled_error_target"):
        _require(_finite(doc[name], name) > 0, "PRECISION_ERROR", name)
    return doc


class _Curve:
    """One affine mean, projected only by the existing Gaussian backend."""
    def __init__(self, joint, mu, direction, reference, lower, upper, base_point):
        self.joint, self.mu, self.direction = joint, mu, direction
        self.reference, self.lower, self.upper = reference, lower, upper
        self.base_point = base_point
        np, engine = joint._np, joint._engine
        _require(lower < upper and lower <= reference <= upper,
                 "DOMAIN_ERROR", "reference inside exact prior interval")
        _require(mu.shape == (283,) and direction.shape == (283,) and
                 bool(np.isfinite(mu).all()) and bool(np.isfinite(direction).all()),
                 "CURVE_ERROR", "finite full 283-dimensional vectors")
        # No block reduction: all cross-covariances remain in the shared engine.
        projected = engine.residualize(direction[:, None])[:, 0]
        self.projected_direction = projected
        _require(bool(np.isfinite(projected).all()), "CURVE_ERROR", "projected direction")
        self.a = float(projected @ projected)
        _require(math.isfinite(self.a) and self.a >= 0, "CURVATURE_ERROR", "invalid a")
        exact_float_zero = bool((projected == 0).all())
        _require(self.a != 0 or exact_float_zero, "CURVATURE_UNDERFLOW",
                 "nonzero projected vector must not be mistaken for a flat extra")
        self.flat_in_float_geometry = exact_float_zero
        self.endpoint_support = []
        for x in (lower, upper):
            check = engine.support.evaluate(self.mean(x) - joint._origin)
            _require(math.isfinite(check["null_residual_norm"]) and check["support_ok"],
                     "AFFINE_SUPPORT_CHANGED", "prior endpoint outside common affine support")
            self.endpoint_support.append({k: check[k] for k in
                 ("rank", "nullity", "null_residual_norm", "support_tolerance", "support_ok")})
        self.zero_density = base_point["status"] == "ZERO_DENSITY_OUTSIDE_FIXED_AFFINE_SUPPORT"
        self.b = None
        if not self.zero_density:
            residual = joint._y - mu
            r = engine.residualize(residual[:, None])[:, 0]
            _require(bool(np.isfinite(r).all()), "CURVE_ERROR", "projected residual")
            self.b = float(r @ projected)
            _require(math.isfinite(self.b), "CURVE_ERROR", "nonfinite linear coefficient")
            _require(not exact_float_zero or self.b == 0, "CURVE_ERROR", "a=0 requires b=0")

    def mean(self, x):
        return self.mu + self.direction * (x - self.reference)

    def log_likelihood(self, x):
        value = _finite(x, "curve coordinate")
        _require(self.lower <= value <= self.upper, "DOMAIN_ERROR", "curve query")
        engine = self.joint._engine
        residual = self.joint._y - self.mean(value)
        check = engine.support.evaluate(residual)
        _require(check["support_ok"] and math.isfinite(check["null_residual_norm"]),
                 "SUPPORT_INCONSISTENCY", "in-support curve evaluation left fixed support")
        result = engine.log_integral(residual)
        _require(math.isfinite(result), "BACKEND_VALUE_ERROR", "finite curve integral")
        return result

    def peak(self, prior_linear=0.0):
        # Find the restricted vertex without overflowing b/a when it is outside.
        k = math.fsum((self.b, prior_linear))
        lo, hi = self.lower - self.reference, self.upper - self.reference
        left, right = self.a * lo, self.a * hi
        _require(math.isfinite(k) and math.isfinite(left) and math.isfinite(right),
                 "NUMERIC_ERROR", "restricted quadratic vertex")
        if k <= left:
            return self.lower
        if k >= right:
            return self.upper
        x = self.reference + k / self.a
        _require(math.isfinite(x) and self.lower <= x <= self.upper,
                 "NUMERIC_ERROR", "interior quadratic vertex")
        return x


def _constant_case(curve):
    if curve.zero_density:
        return {"log_conditional_integral": float("-inf"),
                "status": "ZERO_DENSITY_ON_COMMON_AFFINE_SUPPORT_COMPLEMENT",
                "method": "common support; not underflow", "precision": None}
    if curve.flat_in_float_geometry:
        return {"log_conditional_integral": curve.base_point["log_integral_deta"],
                "status": "FLAT_EXTRA_IN_PROJECTED_FLOAT_GEOMETRY",
                "method": "proper normalized extra prior integrates to one",
                "precision": {"scope": "computed geometry only, not exact scientific rank certificate"}}
    return None


def _analytic(curve, prior_linear, log_density_constant, precision, services):
    constant = _constant_case(curve)
    if constant is not None:
        return constant
    peak = curve.peak(prior_linear)
    log_at_peak = curve.log_likelihood(peak)
    shift = peak - curve.reference
    h = math.fsum((curve.b, prior_linear, -curve.a * shift))
    lo, hi = curve.lower - peak, curve.upper - peak
    # The special-function service evaluates the whole combined log integral,
    # not a subtraction of ordinary CDF floats or exp(b*b/(2*a)).
    result = services["log_exp_quad_interval"](
        curve.a, h, lo, hi,
        absolute_log_error_target=precision["absolute_log_error_target"],
        max_evaluations=precision["max_window_evaluations"])
    log_window = _service_result(result, precision["services"]["log_exp_quad_interval"]["id"], "log_value")
    _require(result["evaluations"] <= precision["max_window_evaluations"],
             "BUDGET_ERROR", "window service evaluation budget")
    value = math.fsum((log_at_peak, log_density_constant, prior_linear * peak, log_window))
    _require(math.isfinite(value), "NUMERIC_ERROR", "positive finite-window integral log")
    return {"log_conditional_integral": value, "status": "ENGINEERING_ESTIMATE",
            "method": "restricted-vertex shifted analytic exponential-quadratic window",
            "anchor_coordinate": peak, "precision": result}


def _rd_quadrature(curve, precision, services):
    constant = _constant_case(curve)
    if constant is not None:
        return constant
    peak = curve.peak()
    log_peak = curve.log_likelihood(peak)
    qlo, qhi = curve.lower, curve.upper
    width_q = qhi - qlo
    width_rd = RD_LIMITS[1] - RD_LIMITS[0]
    # Positive integration on u in [0,1], q=qlo+width_q*u.
    # Anchor also absorbs the maximum q^-2 prior weight at qlo.
    log_anchor = math.fsum((log_peak, math.log(width_q), -math.log(width_rd), -2 * math.log(qlo)))
    counters = {"integrand_calls": 0, "underflowed_nodes": 0}

    failure = {"exception": None}

    def raw_integrand(u):
        u = _finite(u, "quadrature unit coordinate")
        _require(0 <= u <= 1, "DOMAIN_ERROR", "quadrature outside [0,1]")
        _require(counters["integrand_calls"] < precision["max_quadrature_evaluations"],
                 "BUDGET_ERROR", "quadrature evaluation cap")
        counters["integrand_calls"] += 1
        # Use exact endpoints when requested, avoiding endpoint-addition drift.
        q = qlo if u == 0 else qhi if u == 1 else qlo + width_q * u
        log_scaled = math.fsum((curve.log_likelihood(q), -log_peak, 2 * math.log(qlo / q)))
        _require(math.isfinite(log_scaled), "NUMERIC_ERROR", "scaled log integrand")
        value = math.exp(log_scaled)
        _require(math.isfinite(value) and value >= 0, "NUMERIC_ERROR", "scaled integrand")
        if value == 0:
            counters["underflowed_nodes"] += 1
        return value

    def integrand(u):
        # A service must not turn a swallowed callback failure into success.
        try:
            return raw_integrand(u)
        except Exception as exc:
            failure["exception"] = exc
            raise

    result = services["positive_quad_1d"](
        integrand, 0.0, 1.0,
        absolute_error_target=precision["absolute_scaled_error_target"],
        relative_error_target=precision["relative_scaled_error_target"],
        max_evaluations=precision["max_quadrature_evaluations"])
    if failure["exception"] is not None:
        raise PriorError("QUADRATURE_CALLBACK_FAILED", "latched callback failure") from failure["exception"]
    area = _service_result(result, precision["services"]["positive_quad_1d"]["id"], "value")
    _require(result["evaluations"] == counters["integrand_calls"],
             "SERVICE_ERROR", "reported quadrature count differs from callback count")
    _require(area > 0, "QUADRATURE_ZERO_OR_UNDERFLOW",
             "positive mathematical prior integral cannot be inferred zero from sampled nodes")
    value = math.fsum((log_anchor, math.log(area)))
    _require(math.isfinite(value), "NUMERIC_ERROR", "H5 log integral")
    return {"log_conditional_integral": value, "status": "ENGINEERING_ESTIMATE",
            "method": "q=1/rd, exact analytic q^-2 prior Jacobian; scaled positive 1D quadrature",
            "anchor_coordinate": peak, "precision": result, "counters": counters,
            "underflow_interpretation": "nodes rounded to zero are not exact zero mass; error unbounded without validated remainder"}


def integrate_at_fixed_theta(joint, assembly_json, *, assembly_sha256,
                             background_json, consumer_module, precision_json,
                             precision_sha256, services):
    """Return five conditional prior averages at one fixed background theta.

    H1/H2 remain pointwise; H3/H4 integrate their extra analytically via the
    injected stable window primitive; H5 integrates q=1/rd with a 1D service.
    The common three-dimensional theta prior is NOT applied or integrated.
    """
    c = consumer_module
    _require(getattr(c, "REQUEST_ID", None) == "a9874f79-9d71-48f5-824c-d51d6d819534" and
             isinstance(joint, c.PreparedJoint), "CONSUMER_IDENTITY_ERROR", "frozen trusted consumer context")
    _require(type(services) is dict and set(services) ==
             {"log_exp_quad_interval", "positive_quad_1d"} and all(callable(f) for f in services.values()),
             "SERVICE_ERROR", "two explicitly injected services required")
    precision = _precision(c, precision_json, precision_sha256)
    _require(precision["consumer_admission_sha256"] == joint._admission_sha256 and
             precision["assembly_sha256"] == assembly_sha256,
             "PIN_ERROR", "fixed admitted context/assembly")
    packet = c._json(assembly_json, assembly_sha256, "fixed-theta five-model packet")
    # Reuse all existing packet/structure/affine-support checks and normalization.
    pointwise = joint.evaluate_five(assembly_json, assembly_sha256=assembly_sha256)
    background_sha = packet["identity"]["background_packet_sha256"]
    bg = c._json(background_json, background_sha, "same background; never recomputed")
    _require(bg.get("schema") == "F9_BACKGROUND_PACKET_V1" and
             bg.get("status") == "ENGINEERING_RESULT" and bg.get("error") is None,
             "BACKGROUND_ERROR", "background packet status")
    _require(bg["identity"] == packet["identity"]["background_identity"],
             "PIN_ERROR", "exact shared background identity")
    theta = tuple(_finite(packet["models"]["H2_LCDM"]["parameters"][name], name)
                  for name in ("H0", "ombh2", "omch2"))
    _require(tuple(bg["result"]["theta"]) == theta and tuple(bg["identity"]["theta"]) == theta,
             "BACKGROUND_ERROR", "fixed theta mismatch")
    expected_parameters = {
        "H1_TGL": ("H0", "ombh2", "omch2"), "H2_LCDM": ("H0", "ombh2", "omch2"),
        "H3_beta_free": ("H0", "ombh2", "omch2", "beta"),
        "H4_Cepheid": ("H0", "ombh2", "omch2", "s"),
        "H5_rd_free": ("H0", "ombh2", "omch2", "rd_Mpc")}
    density = {"H1_TGL": "1", "H2_LCDM": "1", "H3_beta_free": "10",
               "H4_Cepheid": "10/3", "H5_rd_free": "1/30"}
    for model in MODELS:
        record = packet["models"][model]
        c._keys(record["parameters"], expected_parameters[model], model + " parameters")
        _require(tuple(_finite(record["parameters"][n], n) for n in ("H0","ombh2","omch2")) == theta,
                 "BACKGROUND_ERROR", "model-specific theta changed")
        _require(record["prior"] == {"coordinates": list(expected_parameters[model]),
                 "common_theta_density_exact": "50/3", "extra_density_exact": density[model],
                 "measure": "uniform_in_listed_coordinates"}, "PRIOR_ERROR", "frozen original prior")
    np = joint._np
    response = joint._structure["response_columns"]
    ah = np.array([float(c._fraction(v, "a_h")) for v in response["a_h"]], dtype="<f8")
    cc = np.array([float(c._fraction(v, "c_C")) for v in response["c_C"]], dtype="<f8")
    I = _finite(bg["result"]["I_law"], "I_law")
    E = _finite(bg["result"]["E_law"], "E_law")
    _require(E > 0 and math.isclose(I, (2 / 3) * math.log(E), rel_tol=1e-12, abs_tol=1e-14),
             "BACKGROUND_ERROR", "same I_law/E_law engineering check as producer")
    vectors = {model: np.array(packet["models"][model]["mean_without_nuisance"], dtype="<f8")
               for model in MODELS}
    p3 = packet["models"]["H3_beta_free"]["parameters"]["beta"]
    p4 = packet["models"]["H4_Cepheid"]["parameters"]["s"]
    p5 = packet["models"]["H5_rd_free"]["parameters"]["rd_Mpc"]
    p3, p4, p5 = (_finite(x, "reference extra") for x in (p3, p4, p5))
    _require(BETA_LIMITS[0] <= p3 <= BETA_LIMITS[1] and S_LIMITS[0] <= p4 <= S_LIMITS[1] and
             RD_LIMITS[0] <= p5 <= RD_LIMITS[1], "PRIOR_ERROR", "reference outside fixed prior")
    lam = math.log(10) / 5
    dlo = -5 * math.log1p(S_LIMITS[1]) / math.log(10)
    dhi = -5 * math.log1p(S_LIMITS[0]) / math.log(10)
    dref = -5 * math.log1p(p4) / math.log(10)
    direction5 = np.zeros(283, dtype="<f8")
    direction5[3:16] = vectors["H5_rd_free"][3:16] * p5
    curves = {
        "H3_beta_free": _Curve(joint, vectors["H3_beta_free"], (I / math.log(10)) * ah,
                              p3, *BETA_LIMITS, pointwise["models"]["H3_beta_free"]),
        "H4_Cepheid": _Curve(joint, vectors["H4_Cepheid"], cc,
                            dref, dlo, dhi, pointwise["models"]["H4_Cepheid"]),
        "H5_rd_free": _Curve(joint, vectors["H5_rd_free"], direction5,
                            1 / p5, 1 / RD_LIMITS[1], 1 / RD_LIMITS[0],
                            pointwise["models"]["H5_rd_free"])}
    outputs = {m: {"log_conditional_integral": pointwise["models"][m]["log_integral_deta"],
                   "status": pointwise["models"][m]["status"],
                   "method": "no physical extra; unchanged qualified pointwise value"}
               for m in ("H1_TGL", "H2_LCDM")}
    outputs["H3_beta_free"] = _analytic(curves["H3_beta_free"], 0.0,
                                      -math.log(BETA_LIMITS[1] - BETA_LIMITS[0]), precision, services)
    outputs["H4_Cepheid"] = _analytic(curves["H4_Cepheid"], -lam,
                                    math.log(lam / (S_LIMITS[1] - S_LIMITS[0])), precision, services)
    outputs["H5_rd_free"] = _rd_quadrature(curves["H5_rd_free"], precision, services)
    for model, curve in curves.items():
        outputs[model]["geometry"] = {"a": curve.a, "b": curve.b,
            "extra_reference": curve.reference, "endpoint_support": curve.endpoint_support,
            "flat_status_is_not_exact_scientific_certificate": True}
    return {"schema": "F9_CONDITIONAL_PHYSICAL_PRIOR_RESULT_V1",
            "status": "ENGINEERING_ONLY", "request_id": REQUEST_ID,
            "models": outputs, "theta": list(theta),
            "base_theta_prior": {"density_exact": "50/3", "applied": False, "integrated": False},
            "measure": pointwise["measure"], "output_measure": pointwise["output_measure"],
            "normalization": pointwise["normalization"], "MM_status": "CONDITIONAL_UNRATIFIED",
            "certification": pointwise["certification"],
            "precision_scope": "service-local estimates only; backend, coefficient, reconstruction and theory errors unbounded",
            "provenance": {"source_pins": SOURCE_PINS, "assembly_sha256": assembly_sha256,
                           "background_sha256": background_sha,
                           "consumer_admission_sha256": joint._admission_sha256,
                           "precision_sha256": precision_sha256},
            "absolute_evidence": None, "theta_integrated_evidence": None,
            "lnB": None, "p": None, "sigma": None, "verdict": None}
