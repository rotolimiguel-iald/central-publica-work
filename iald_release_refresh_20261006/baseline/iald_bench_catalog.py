"""Fixed local bench adapter. The caller owns operator authorization and journaling.

No scientific module is imported, no service is started, and no retry is made.
Freeze normalize() and provenance() in the plan; compare provenance before dispatch.
All POST operations require an external DISPATCHING receipt before request().
"""
from __future__ import annotations

import copy
import hashlib
import http.client
import json
import math
from pathlib import Path
import re
import unicodedata
from urllib.parse import urlencode, urlsplit
import uuid

BENCH_ROOT = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\TETELESTAI\BANCADA_OFICIAL")
CHATGPT_ROOT = Path(r"C:\IALD\Central de Patentes\Chatgpt")
EVENT_ROOT = CHATGPT_ROOT / "ORDEM_013_RINGDOWN"
COSMOS_PORT = 18766
BENCH_PORT = 18765
MAX_RESPONSE_BYTES = 16 * 1024 * 1024
HTTP_TIMEOUT_SECONDS = 120
CONTRACT_VERSION = "iald_bench_catalog_v1"
_SHA = re.compile(r"[0-9a-f]{64}\Z")
_DATA_ID = re.compile(r"[0-9a-f]{24}\Z")
_MISSING = object()


class BenchError(ValueError):
    """A safe public error; uncertain forbids automatic re-dispatch."""

    def __init__(self, code, message, *, uncertain=False):
        super().__init__(message)
        self.code = code
        self.uncertain = uncertain


def _fail(message, code="INVALID_PARAMETERS"):
    raise BenchError(code, message)


def _canonical(value):
    return json.dumps(value, ensure_ascii=False, sort_keys=True,
                      separators=(",", ":"), allow_nan=False)


def _object(properties=None, required=()):
    return {"type": "object", "properties": properties or {},
            "required": list(required), "additionalProperties": False}


def _number(low=None, high=None, default=_MISSING, **extra):
    out = {"type": "number", **extra}
    if low is not None:
        out["minimum"] = low
    if high is not None:
        out["maximum"] = high
    if default is not _MISSING:
        out["default"] = default
    return out


def _text(maximum, default=_MISSING, minimum=0, **extra):
    out = {"type": "string", "maxLength": maximum, "minLength": minimum, **extra}
    if default is not _MISSING:
        out["default"] = default
    return out


_PAGE = {"offset": {"type": "integer", "minimum": 0, "maximum": 1000000, "default": 0},
         "page_size": {"type": "integer", "minimum": 1, "maximum": 500, "default": 50}}
_ID = {"type": "string", "pattern": "^[0-9a-f]{24}$"}
_UUID = {"type": "string", "format": "uuid4"}
_READING = {"type": "string", "enum": ["R-A", "R-B", "R-RAIZ-0", "R-GLOBAL"]}
_COSMOS = _object({
    "model_id": {"type": "string", "default": "FLAT_MATTER_CPL_BACKGROUND", "enum": [
        "FLAT_MATTER_CPL_BACKGROUND", "TGL_V3_TOTAL_FIXED_BETA", "V3_TOTAL_BETA_ZERO"]},
    "H0": _number(40, 100, 67.4), "omega_m": _number(.1, .5, .315),
    "rd_mpc": _number(120, 170, 147.09), "w0": _number(-1.5, -.5, -1),
    "wa": _number(-1, 1, 0), "redshift": _number(.001, 3, .5),
})
_DETECTOR = _object({"amplitude": _number(0, 1e-15), "phase": _number()},
                    ("amplitude", "phase"))
_OPS = {}


def _add(name, path, description, *, schema=None, method="GET", cosmos=False,
         section="queries", list_key=None, upstream_limit=None, example=None):
    _OPS[name] = {"operation": name, "method": method, "port": COSMOS_PORT if cosmos else BENCH_PORT,
                  "path": path, "section": section, "description": description,
                  "parameters_schema": schema or _object(), "example": example or {},
                  "list_key": list_key, "upstream_limit": upstream_limit,
                  "writes": method == "POST"}


for _name, _path, _description in (
    ("bench_overview", "/api/overview", "Identidade e fontes da bancada; índice histórico v368, não compilação atual."),
    ("lab_memory", "/api/lab/memory", "Telemetria de RAM Windows; não aloca memória."),
    ("lab_gpu", "/api/lab/gpu", "Telemetria NVIDIA por comando fixo do servidor; sem computação GPU."),
    ("lab_coverage", "/api/lab/coverage", "Cobertura dos adaptadores de dados; não é validação física."),
    ("lab_canonical", "/api/lab/canonical", "Metadados e trecho da forma canônica; nunca executa um.py."),
    ("lab_bao_report", "/api/lab/bao-report", "Relatório BAO já existente; não recalcula."),
):
    _add(_name, _path, _description)
for _name, _path, _key, _cap in (
    ("routes", "/api/routes", "", None), ("data", "/api/data", "", None),
    ("protocols", "/api/protocols", "", None), ("runs", "/api/runs", "", 40),
    ("inquiries", "/api/inquiries", "", 20), ("lab_catalog", "/api/lab/catalog", "items", 3000),
):
    _add(_name, _path, "Lista paginada do acervo disponível; limites históricos do servidor preservados.",
         schema=_object(_PAGE), list_key=_key, upstream_limit=_cap)
_add("relations", "/api/relations", "Busca lexical no índice histórico, sem recompilar Lean.",
     schema=_object({**_PAGE, "q": _text(100, ""),
                     "limit": {"type": "integer", "minimum": 1, "maximum": 100, "default": 50}}),
     list_key="matches", upstream_limit=100, example={"q": "Identity"})
for _name in ("lab_treatment", "lab_describe"):
    _add(_name, "/api/lab/" + _name[4:], "Leitura de arquivo pelo ID do catálogo; HDF5 usa subprocesso fixo no servidor.",
         schema=_object({"id": _ID}, ("id",)))
_add("lab_preview", "/api/lab/preview", "Amostra limitada; exige duas colunas distintas obtidas em lab_describe.",
     schema=_object({"id": _ID, "x": _text(256, minimum=1), "y": _text(256, minimum=1),
                     "limit": {"type": "integer", "minimum": 1, "maximum": 1200, "default": 800}},
                    ("id", "x", "y")))
_add("identity_chain", "/api/run", "Conta algébrica registrada em runs; não testa a natureza.",
     method="POST", section="experiments")
_add("dephasing", "/api/run", "Gamma=beta*tau*omega²/2; 51 pontos, entradas explícitas, sem significância.",
     method="POST", section="experiments", schema=_object({
         "omega_rad_s": _number(0, 1e40), "tau_s": _number(0, 1e10),
         "duration_s": _number(0, 1e10)}, ("omega_rad_s", "tau_s", "duration_s")),
     example={"omega_rad_s": 100, "tau_s": .001, "duration_s": 1})
_add("inquiry", "/api/inquiry", "Registra pergunta e mapeia fontes; EXPLORATORY_NOT_PREREGISTERED.",
     method="POST", section="experiments", schema=_object({
         key: _text(500, "", minimum=8 if key == "question" else 0)
         for key in ("question", "hypothesis", "falsifier", "alternative", "instrumental", "discriminator")},
         ("question",)), example={"question": "Onde está a identidade modular?"})
_add("universe_domains", "/api/universe/domains", "Perfis RAM disponíveis; somente gw_strain implementado.", section="universe")
_add("universe_status", "/api/universe/status", "Estado RAM e hashes dos arrays; não inicia worker ausente.", section="universe")
_add("universe_load", "/api/universe/load", "Inicia carga gw_strain em background; LOADING não conclui. READY completo retorna ALREADY_RESIDENT sem POST. Nunca libera RAM.",
     method="POST", section="universe", schema=_object({
         "domain": {"type": "string", "enum": ["gw_strain"], "default": "gw_strain"}}))
_add("universe_view", "/api/universe/view", "Envelope min/max da janela residente; não é espectro nem ajuste.", section="universe",
     schema=_object({"id": _ID, "start_s": _number(0, default=0),
                     "duration_s": _number(default=1, exclusiveMinimum=0),
                     "bins": {"type": "integer", "minimum": 16, "maximum": 4096, "default": 1600}}, ("id",)))
_add("universe_model", "/api/universe/model", "Modelo 220 BCW condicional GR/TGL, 4096 pontos; leitura de relógio explícita.",
     method="POST", section="universe", schema=_object({
         "reading": _READING, "mass_source_solar": _number(1, 1e10, 65),
         "spin": _number(0, default=.7, exclusiveMaximum=1), "redshift": _number(0, default=.1),
         "amplitude": _number(default=1e-21), "phase": _number(default=0),
         "duration_s": _number(high=100, default=.08, exclusiveMinimum=0)}, ("reading",)),
     example={"reading": "R-GLOBAL"})
_add("universe_event", "/api/universe/event", "Metadados C6 do evento registrado; pode ler fontes via worker. Worker existente obrigatório.", section="universe")
_add("universe_event_view", "/api/universe/event_view", "Sobreposição manual H1/L1 nas janelas C6; sem ajuste, p-valor ou sigma.",
     method="POST", section="universe", schema=_object({
         "reading": _READING, "start_tm": _number(), "mass_source_solar": _number(1, 1e4),
         "spin": _number(0, default=.7, exclusiveMaximum=1), "redshift": _number(0),
         "detectors": _object({"H1": _DETECTOR, "L1": _DETECTOR}, ("H1", "L1"))}, ("reading", "detectors")),
     example={"reading": "R-GLOBAL", "detectors": {"H1": {"amplitude": 1e-21, "phase": 0},
                                                  "L1": {"amplitude": 1e-21, "phase": 0}}})
_add("cosmos_health", "/api/cosmology/health", "Identidade do servidor, sem inicializar dados ou executor.", cosmos=True, section="cosmos")
_add("cosmos_status", "/api/cosmology/status", "Contrato cosmológico e observações; inicializa pequeno cache DESI se vazio. Não usar como proveniência passiva.", cosmos=True, section="cosmos")
_add("cosmos_evaluate", "/api/cosmology/evaluate", "CPL ou V3 com beta fixo/zero; diagnóstico de fundo, não inferência CMB nem sigma.",
     method="POST", cosmos=True, section="cosmos", schema=_COSMOS,
     example={"model_id": "TGL_V3_TOTAL_FIXED_BETA"})
_add("cosmos_scenarios", "/api/cosmology/scenarios", "Cenários históricos verificados por hash; sem reavaliação.",
     cosmos=True, section="cosmos", schema=_object(_PAGE), list_key="scenarios")
_add("cosmos_scenario", "/api/cosmology/scenarios/{id}", "Snapshot histórico integral pelo UUID4.",
     cosmos=True, section="cosmos", schema=_object({"id": _UUID}, ("id",)))
_add("cosmos_save_scenario", "/api/cosmology/scenarios", "Avalia e grava cenário novo; não repetir após resultado incerto.",
     method="POST", cosmos=True, section="cosmos", schema=_object({
         "label": _text(120, minimum=1), "parameters": {**_COSMOS, "default": {}}}, ("label",)),
     example={"label": "Referência CPL", "parameters": {}})
_add("cosmos_export", "/api/cosmology/exports", "Exporta cenário existente sem recalcular, OU avalia dois parâmetros e exporta comparação.",
     method="POST", cosmos=True, section="cosmos", schema={"oneOf": [
         _object({"scenario_id": _UUID}, ("scenario_id",)),
         _object({"reference_parameters": _COSMOS, "current_parameters": _COSMOS},
                 ("reference_parameters", "current_parameters"))]},
     example={"reference_parameters": {}, "current_parameters": {"H0": 70}})
_add("cosmos_get_export", "/api/cosmology/exports/{id}", "JSON histórico por UUID4, com integridade verificada no servidor.",
     cosmos=True, section="cosmos", schema=_object({"id": _UUID}, ("id",)))


# Valid-shaped placeholders, not claims that these source IDs exist.
for _name in ("lab_treatment", "lab_describe", "universe_view"):
    _OPS[_name]["example"] = {"id": "0" * 24}
_OPS["lab_preview"]["example"] = {"id": "0" * 24, "x": "column_x", "y": "column_y"}
for _name in ("cosmos_scenario", "cosmos_get_export"):
    _OPS[_name]["example"] = {"id": "00000000-0000-4000-8000-000000000000"}


def catalog(section="overview"):
    """Pure metadata: no source reads, network, imports, or RAM operations."""
    valid = {"overview", "all", "queries", "experiments", "universe", "cosmos"}
    if section not in valid:
        _fail("Seção de catálogo inválida.")
    if section == "overview":
        return {"schema": CONTRACT_VERSION, "section": section,
                "sections": ["queries", "experiments", "universe", "cosmos"],
                "operations": [{"operation": op["operation"], "description": op["description"],
                                "writes": writes(op["operation"]), "section": op["section"]}
                               for op in _OPS.values()],
                "gpu_solver_available": False,
                "note": "Peça catalog(section) para schemas completos, defaults e exemplos. writes=True exige plano/run; somente luiz classe operador. Sem reiniciar serviços ou liberar RAM."}
    selected = [copy.deepcopy(op) for op in _OPS.values()
                if section in ("overview", "all") or op["section"] == section]
    for op in selected:
        op["writes"] = writes(op["operation"])
        op["requires_plan"] = op["writes"]
    return {"schema": CONTRACT_VERSION, "section": section, "operations": selected,
            "authorization": "Somente luiz com classe operador, validado pelo chamador autenticado; nunca por argumento do modelo.",
            "dispatch": "Normalizar, fixar proveniência, registrar plano, comparar proveniência e gravar DISPATCHING antes de qualquer POST; uma execução ativa; nunca repetir resultado incerto.",
            "limits": {"request_bytes": 8192, "response_bytes": MAX_RESPONSE_BYTES,
                       "http_timeout_seconds": HTTP_TIMEOUT_SECONDS, "page_size_max": 500,
                       "ram_load": "min(50% RAM Windows disponível,96 GiB), mais reserva WSL 2 GiB por array",
                       "cosmos": "13 observações; covariância 13x13; z 0.001..3; V3 exige w0=-1 e wa=0"},
            "limitations": ["Paginação local da resposta recebida; não recupera itens já truncados no servidor.",
                "Sem shell, URLs livres, instalação, inicialização/reinício de serviço ou liberação RAM.",
                "Protocolos A0-A8/T01-T19 são localizadores: replay não conectado à API.",
                "GPU oferece telemetria e visualização WebGL2; não existe executor GPU arbitrário.",
                "HDF5 e modelos V3 podem iniciar subprocessos fixos do próprio serviço durante a execução autorizada.",
                "GET cosmos_status pode inicializar cache; writes() é conservador também para consultas com efeitos internos.",
                "Evento C6 mantém INCONCLUSIVE_SYSTEMATICS; nada aqui promove gate ou calcula significância.",
                "Datas de execução pertencem ao journal, fora da identidade determinística da proveniência."],
            "event_defaults": "start_tm, massa e redshift são lidos do REGISTRO_C6.json local e materializados por normalize()."}


# This is correspondence, not permission to reuse results across generations.
HISTORICAL_MAPPING = {
    "runs": {"identity_chain": "identity_chain", "dephasing": "dephasing",
             "parameters": "Drop only the historical operation discriminator; normalize remaining fields.",
             "provenance": "source_sha256 hashes STRUCTURE, not the executor. Require result.engine_sha256 and result.atlas_sha256 too; otherwise inspection only."},
    "inquiries": {"operation": "inquiry", "parameters": "question,hypothesis,falsifier,alternative,instrumental,discriminator from result; no guessed missing evidence"},
    "scenarios": {"operation": "cosmos_save_scenario", "parameters": "label + evaluation.parameters + evaluation.model.id as parameters.model_id",
                  "provenance": "record.provenance.engine, data_hashes, and evaluation.memory.load_id are historical; require matching generation and source pins."},
    "exports": {"scenario": "cosmos_export with scenario_id", "comparison": "cosmos_export with both payload.*.request_parameters"},
    "resident_runs": {"operation": "universe_load", "parameters": {"domain": "gw_strain"},
                      "provenance": "load_id/generation and per-series hashes; metadata receipt alone is not a fresh dispatch authorization"},
    "policy": "Never infer identical provenance from matching parameters, labels or status. Missing historical pins mean read-only history, not execution dedupe.",
}


def _spec(operation):
    if not isinstance(operation, str) or operation not in _OPS:
        _fail("Operação da bancada não permitida.")
    return _OPS[operation]


def _validate(schema, value, name="parameters"):
    if "oneOf" in schema:
        matches = []
        for choice in schema["oneOf"]:
            try:
                matches.append(_validate(choice, value, name))
            except BenchError:
                pass
        if len(matches) != 1:
            _fail("Exportação exige scenario_id OU os dois conjuntos de parâmetros.")
        return matches[0]
    kind = schema["type"]
    if kind == "object":
        if type(value) is not dict or any(type(k) is not str for k in value):
            _fail(f"{name}: objeto JSON obrigatório.")
        props = schema["properties"]
        if set(value) - set(props) or set(schema["required"]) - set(value):
            _fail(f"{name}: campos desconhecidos ou obrigatórios ausentes.")
        result = {}
        for key, rule in props.items():
            item = value.get(key, copy.deepcopy(rule.get("default", _MISSING))) if key in value or "default" in rule else _MISSING
            if item is not _MISSING:
                result[key] = _validate(rule, item, name + "." + key)
        return result
    if kind in ("number", "integer"):
        if type(value) not in (int, float):
            _fail(f"{name}: número finito obrigatório.")
        try:
            number = float(value)
        except (OverflowError, ValueError):
            _fail(f"{name}: número inválido.")
        if not math.isfinite(number) or (kind == "integer" and not number.is_integer()):
            _fail(f"{name}: número inválido.")
        for bound, compare in (("minimum", lambda a,b:a < b), ("maximum", lambda a,b:a > b),
                               ("exclusiveMinimum", lambda a,b:a <= b), ("exclusiveMaximum", lambda a,b:a >= b)):
            if bound in schema and compare(number, schema[bound]):
                _fail(f"{name}: fora do intervalo permitido.")
        return int(number) if kind == "integer" else (0.0 if number == 0 else number)
    if type(value) is not str:
        _fail(f"{name}: texto obrigatório.")
    try:
        value.encode("utf-8")
    except UnicodeError:
        _fail(f"{name}: texto inválido.")
    if any(unicodedata.category(c).startswith("C") and c not in "\n\t\r" for c in value):
        _fail(f"{name}: caracteres de controle não permitidos.")
    if not schema.get("minLength", 0) <= len(value) <= schema.get("maxLength", 4096):
        _fail(f"{name}: tamanho inválido.")
    if "enum" in schema and value not in schema["enum"]:
        _fail(f"{name}: opção não permitida.")
    if "pattern" in schema and not re.fullmatch(schema["pattern"], value):
        _fail(f"{name}: identificador inválido.")
    if schema.get("format") == "uuid4":
        try:
            parsed = uuid.UUID(value)
        except ValueError:
            _fail(f"{name}: UUID4 inválido.")
        if parsed.version != 4 or str(parsed) != value:
            _fail(f"{name}: UUID4 canônico obrigatório.")
    return value


def _read_json(path, limit=4 * 1024 * 1024):
    _safe_path(path)
    try:
        with path.open("rb") as stream:
            raw = stream.read(limit + 1)
        if len(raw) > limit:
            _fail("Metadados excedem o limite local.", "PROVENANCE_UNAVAILABLE")
        return _decode(raw)
    except OSError as exc:
        raise BenchError("PROVENANCE_UNAVAILABLE", "Fonte local de proveniência indisponível.") from exc


def normalize(operation, parameters):
    """Return only effective parameters; no HTTP, execution, or mutable caching."""
    spec = _spec(operation)
    p = _validate(spec["parameters_schema"], parameters)
    if operation == "relations":
        p["q"] = p["q"].strip().lower()
    if operation == "inquiry":
        p = {k: v.strip() for k, v in p.items()}
        if len(p["question"]) < 8:
            _fail("A pergunta deve conter ao menos 8 caracteres.")
    if operation == "cosmos_save_scenario":
        if any(unicodedata.category(c).startswith("C") for c in p["label"]):
            _fail("O nome do cenário não permite caracteres de controle.")
        p["label"] = p["label"].strip()
        if not p["label"]:
            _fail("O nome do cenário não pode ser vazio.")
    if operation == "lab_preview" and p["x"] == p["y"]:
        _fail("Escolha duas colunas diferentes.")
    if operation == "universe_event_view":
        reg = _read_json(EVENT_ROOT / "REGISTRO_C6.json")
        defaults = {"start_tm": reg["primary_start_tM"], "redshift": reg["reference_redshift"],
                    "mass_source_solar": reg["reference_mass_for_start_solar"] / (1 + reg["reference_redshift"])}
        for key, value in defaults.items():
            p.setdefault(key, _validate(spec["parameters_schema"]["properties"][key], value, key))
        if p["start_tm"] not in reg["start_times_tM"]:
            _fail("Início fora das janelas C6 registradas.")
    if operation in ("universe_model", "universe_event_view"):
        if not math.isfinite(p["mass_source_solar"] * (1 + p["redshift"])):
            _fail("Massa no referencial do detector não finita.")
    if operation == "universe_view" and not math.isfinite(p["start_s"] + p["duration_s"]):
        _fail("Janela temporal não finita.")
    cosmos_sets = ([p] if operation == "cosmos_evaluate" else [p["parameters"]] if operation == "cosmos_save_scenario"
                  else [p["reference_parameters"], p["current_parameters"]]
                  if operation == "cosmos_export" and "scenario_id" not in p else [])
    for value in cosmos_sets:
        if value["model_id"] != "FLAT_MATTER_CPL_BACKGROUND" and (value["w0"] != -1 or value["wa"] != 0):
            _fail("O modelo V3 exige w0=-1 e wa=0.")
    if len(_canonical(p).encode("utf-8")) > 8000:
        _fail("Parâmetros excedem o limite de transporte.")
    return p


def writes(operation):
    """Conservative planning flag: includes queries that initialize worker caches."""
    return _spec(operation)["writes"] or operation in {"universe_event", "cosmos_status"}


def _decode(raw):
    def pairs(items):
        out = {}
        for key, value in items:
            if key in out:
                raise ValueError("duplicate key")
            out[key] = value
        return out
    def invalid(value):
        raise ValueError("nonfinite JSON")
    try:
        result = json.loads(raw.decode("utf-8"), object_pairs_hook=pairs, parse_constant=invalid)
        _canonical(result)
        return result
    except (ValueError, UnicodeError, RecursionError) as exc:
        raise BenchError("INVALID_RESPONSE", "A bancada devolveu JSON inválido.") from exc


def _http(port, method, path, payload=None):
    """Direct loopback TCP: no urllib, proxy environment, redirects, or cookies."""
    parsed = urlsplit(path)
    allowed = {op["path"] for op in _OPS.values() if op["port"] == port and op["method"] == method}
    base = parsed.path
    dynamic = re.fullmatch(r"/api/cosmology/(scenarios|exports)/([0-9a-f-]{36})", base)
    if (port not in (BENCH_PORT, COSMOS_PORT) or parsed.scheme or parsed.netloc or parsed.fragment
            or not path.startswith("/api/") or "\r" in path or "\n" in path
            or (base not in allowed and not (dynamic and method == "GET" and port == COSMOS_PORT))):
        _fail("Destino HTTP não permitido.")
    body = None if payload is None else _canonical(payload).encode("utf-8")
    if body is not None and len(body) > 8192:
        _fail("Corpo HTTP excede 8192 bytes.")
    headers = {"Accept": "application/json", "Origin": f"http://127.0.0.1:{port}"}
    if body is not None:
        headers["Content-Type"] = "application/json"
    connection = http.client.HTTPConnection("127.0.0.1", port, timeout=HTTP_TIMEOUT_SECONDS)
    attempted = False
    try:
        attempted = True
        connection.request(method, path, body=body, headers=headers)
        response = connection.getresponse()
        raw = response.read(MAX_RESPONSE_BYTES + 1)
        uncertain = method == "POST"
        if 300 <= response.status < 400:
            raise BenchError("REDIRECT_REFUSED", "Redirecionamento da bancada recusado.", uncertain=uncertain)
        if not 200 <= response.status < 300:
            raise BenchError("BENCH_HTTP_ERROR", f"A bancada recusou a operação (HTTP {response.status}).",
                             uncertain=uncertain and response.status >= 500)
        if len(raw) > MAX_RESPONSE_BYTES or response.getheader("Content-Type", "").split(";", 1)[0].strip().lower() != "application/json":
            raise BenchError("INVALID_RESPONSE", "Resposta da bancada fora do contrato.", uncertain=uncertain)
        try:
            result = _decode(raw)
        except BenchError as exc:
            exc.uncertain = uncertain
            raise
        if not isinstance(result, (dict, list)):
            raise BenchError("INVALID_RESPONSE", "Objeto ou lista JSON esperado.", uncertain=uncertain)
        # FAILED is a domain state with an important partial-load receipt here.
        # Preserve it only on these fixed GW endpoints, never as generic success.
        gw_load_receipt = (port == BENCH_PORT and (method, base) in {
            ("GET", "/api/universe/status"), ("POST", "/api/universe/load")})
        if isinstance(result, dict) and (result.get("status") == "error" or "error" in result
                or (result.get("status") == "FAILED" and not gw_load_receipt)):
            raise BenchError("BENCH_REJECTED", "A bancada informou falha; consulte o recibo local.", uncertain=uncertain)
        return result
    except (OSError, http.client.HTTPException) as exc:
        raise BenchError("UNAVAILABLE", "Bancada indisponível ou resposta perdida; nenhum serviço foi iniciado e não houve repetição.",
                         uncertain=attempted and method == "POST") from exc
    finally:
        connection.close()


def _gw_status():
    value = _http(BENCH_PORT, "GET", "/api/universe/status")
    if not isinstance(value, dict) or value.get("status") not in ("IDLE", "LOADING", "READY", "PARTIAL", "RELEASING", "FAILED"):
        _fail("Estado residente inválido.", "INVALID_RESPONSE")
    return value


def _require_worker(status):
    if type(status.get("generation")) is not int or type(status.get("worker_pid")) is not int:
        _fail("Worker RAM não está ativo; ativação deve ser feita pelo operador.", "UNAVAILABLE")


def _complete(status, domain):
    return (status.get("status") == "READY" and status.get("domain") == domain
            and type(status.get("total_files")) is int and status["total_files"] > 0
            and type(status.get("loaded_files")) is int
            and status["loaded_files"] == status["total_files"] and status.get("errors") == [])


def _checked_load_receipt(result, domain, *, dispatched):
    """Validate the actual returned load identity, without polling or retrying."""
    invalid = not isinstance(result, dict)
    if not invalid:
        try:
            load_uuid = uuid.UUID(result.get("load_id", ""))
            valid_id = load_uuid.version == 4 and str(load_uuid) == result["load_id"]
        except (ValueError, AttributeError, TypeError):
            valid_id = False
        total, loaded = result.get("total_files"), result.get("loaded_files")
        invalid = (result.get("domain") != domain or not valid_id
                   or type(result.get("generation")) is not int or result["generation"] < 1
                   or result.get("status") not in {"LOADING", "READY", "PARTIAL", "FAILED"}
                   or type(total) is not int or total < 1 or type(loaded) is not int
                   or not 0 <= loaded <= total or not isinstance(result.get("errors"), list))
        if result.get("status") == "READY" and not _complete(result, domain):
            invalid = True
    if invalid:
        raise BenchError("INVALID_LOAD_RECEIPT",
                         "Recibo de carga sem domínio, identidade ou contagem compatível; não repetir o POST.",
                         uncertain=dispatched)
    return {**result, "requested_domain": domain, "dispatched": dispatched,
            "load_complete": _complete(result, domain)}


def request(operation, parameters):
    """One bounded request, after external authorization/journaling. No retries."""
    spec = _spec(operation)
    p = normalize(operation, parameters)
    if operation in {"universe_load", "universe_view", "universe_model", "universe_event", "universe_event_view"}:
        status = _gw_status()
        if operation == "universe_load" and _complete(status, p["domain"]):
            receipt = _checked_load_receipt(status, p["domain"], dispatched=False)
            return {key: value for key, value in {**receipt, "status": "ALREADY_RESIDENT"}.items()
                    if key in {"status", "domain", "requested_domain", "load_id", "generation",
                               "loaded_files", "total_files", "resident_bytes", "errors", "dispatched", "load_complete"}}
        if operation != "universe_load":
            _require_worker(status)
        elif (status.get("status") != "IDLE" or status.get("loaded_files", 0)
              or status.get("domain") not in (None, p["domain"])):
            _fail("Há uma carga ativa ou parcial; preservada sem liberar RAM ou repetir POST.", "RESIDENT_BUSY")
        if operation in {"universe_view", "universe_event_view"} and status.get("status") not in ("READY", "PARTIAL"):
            _fail("Dados residentes indisponíveis; nenhuma carga automática foi iniciada.", "UNAVAILABLE")
    path = spec["path"]
    wire = {k: v for k, v in p.items() if k not in _PAGE}
    if "{id}" in path:
        path = path.replace("{id}", wire.pop("id"))
    if operation in ("identity_chain", "dephasing"):
        wire = {"operation": operation, **wire}
    if spec["method"] == "GET":
        if wire:
            path += "?" + urlencode(wire)
        result = _http(spec["port"], "GET", path)
    else:
        result = _http(spec["port"], "POST", path, wire)
    if operation == "universe_load":
        return _checked_load_receipt(result, p["domain"], dispatched=True)
    if spec["list_key"] is not None:
        key = spec["list_key"]
        items = result if key == "" else result.get(key) if isinstance(result, dict) else None
        if not isinstance(items, list):
            _fail("Lista da bancada fora do contrato.", "INVALID_RESPONSE")
        start, size = p["offset"], p["page_size"]
        page = items[start:start + size]
        more = start + len(page) < len(items)
        meta = {k: v for k, v in result.items() if k != key} if isinstance(result, dict) else {}
        return {"items": page, "offset": start, "page_size": size, "total_available": len(items),
                "next_offset": start + len(page) if more else None, "has_more": more,
                "upstream_limit": spec["upstream_limit"], "metadata": meta,
                "coverage": "RECEIVED_RESPONSE_ONLY_NOT_COMPLETE_HISTORICAL_ARCHIVE"}
    return result


def _safe_path(path):
    path = Path(path)
    for part in (path, *path.parents):
        try:
            if part.is_symlink() or (hasattr(part, "is_junction") and part.is_junction()):
                _fail("Fonte redirecionada por link não permitida.", "PROVENANCE_UNAVAILABLE")
        except OSError as exc:
            raise BenchError("PROVENANCE_UNAVAILABLE", "Não foi possível validar a fonte local.") from exc
    return path


def _pin(path, label):
    path = _safe_path(path)
    try:
        with path.open("rb") as stream:
            before = path.stat()
            digest = hashlib.file_digest(stream, "sha256").hexdigest()
            after = path.stat()
        if (before.st_size, before.st_mtime_ns) != (after.st_size, after.st_mtime_ns):
            _fail("Fonte mudou durante a leitura.", "PROVENANCE_CHANGED")
        return {"source": label, "bytes": after.st_size, "sha256": digest}
    except OSError as exc:
        raise BenchError("PROVENANCE_UNAVAILABLE", "Fonte local de proveniência indisponível.") from exc


_DATA_ROOTS = (
    Path(r"C:\IALD\Artigo\frente_alpha"),
    Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\cache"),
    Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\cache"),
    CHATGPT_ROOT / "TETELESTAI_V350_KERNEL_20260911/r/cache",
    EVENT_ROOT / "cache/gwosc", EVENT_ROOT / "cache/public",
    EVENT_ROOT / "bis/015/t07/strain", EVENT_ROOT / "C7_GWTC3_REPRODUCTION_v3_2/evidence",
)
_DATA_EXTENSIONS = {".fits", ".csv", ".dat", ".txt", ".npy", ".npz", ".h5", ".hdf5"}
_BAO_NAMES = ("desi_gaussian_bao_ALL_GCcomb_mean.txt", "desi_gaussian_bao_ALL_GCcomb_cov.txt")
_EVENT_FILES = ("REGISTRO_C6.json", "C6_DOWNLOADS.json", "C6_RESULTS.json", "C5_EMPIRICAL_NOISE.json",
                "C5_EMPIRICAL_IMR_STARTS.json", "C5_LIKELIHOOD_VALIDATION.json", "QNM_GRID.json",
                "c6_engine.py", "tgl_ringdown_prediction.py", "tgl_ringdown_likelihood.py",
                "cache/gwosc/metadata_1.json", "cache/empirical_noise/H1_noise.npz", "cache/empirical_noise/L1_noise.npz")


def _catalog_source(identifier, catalog_rows=None):
    rows = catalog_rows if catalog_rows is not None else _http(BENCH_PORT, "GET", "/api/lab/catalog")
    matches = [r for r in rows.get("items", []) if r.get("id") == identifier]
    if len(matches) != 1:
        _fail("Fonte ausente ou ambígua no catálogo.", "PROVENANCE_UNAVAILABLE")
    path = Path(matches[0].get("path", ""))
    if not path.is_absolute():
        _fail("Caminho do catálogo inválido.", "PROVENANCE_UNAVAILABLE")
    _safe_path(path)
    resolved = path.resolve()
    roots = [root.resolve() for root in _DATA_ROOTS if resolved.is_relative_to(root.resolve())]
    if (not roots or resolved.suffix.lower() not in _DATA_EXTENSIONS
            or any(part.lower() in {"e2_private", "vendor", "delivery_v2_fresh_20260922_032436_194092"}
                   or part.startswith(".") for part in resolved.parts)
            or (resolved.is_relative_to(_DATA_ROOTS[0].resolve()) and resolved.name not in _BAO_NAMES)
            or hashlib.sha256(str(resolved).encode("utf-8")).hexdigest()[:24] != identifier):
        _fail("Fonte fora do catálogo científico permitido.", "PROVENANCE_UNAVAILABLE")
    return resolved


def _resident_provenance(status, identifier=None):
    fields = ("status", "domain", "load_id", "generation", "loaded_files", "total_files")
    receipt = {k: status.get(k) for k in fields}
    records = status.get("series", [])
    if not isinstance(records, list):
        _fail("Recibo de arrays residentes inválido.", "PROVENANCE_UNAVAILABLE")
    if identifier is not None:
        records = [r for r in records if r.get("id") == identifier]
        if len(records) != 1:
            _fail("Série solicitada não está residente.", "PROVENANCE_UNAVAILABLE")
    stable = []
    for record in records:
        if not _SHA.fullmatch(str(record.get("strain_array_sha256", ""))):
            _fail("Hash do array residente ausente.", "PROVENANCE_UNAVAILABLE")
        stable.append({k: record.get(k) for k in (
            "id", "name", "rows", "dt_s", "gps_start", "detector", "numeric_datasets",
            "strain_array_sha256", "source_sha256", "source_bytes", "dataset_attributes", "metadata")})
    stable.sort(key=lambda r: str(r["id"]))
    receipt["series_count"] = len(stable)
    receipt["series_sha256"] = hashlib.sha256(_canonical(stable).encode("utf-8")).hexdigest()
    if identifier is not None:
        receipt["selected_series"] = [{k: row[k] for k in (
            "id", "name", "rows", "dt_s", "gps_start", "strain_array_sha256", "source_sha256", "source_bytes")}
            for row in stable]
    receipt["hash_scope"] = "RAM_STRAIN_HASH; source_sha256 may be null for unpinned non-event sources; masks have metadata but no independent RAM hash"
    return receipt


def provenance(operation, params):
    """Deterministic pins; only passive GETs, full file hashing, never RAM loading.

    Runtime hashes reported by a service remain identified as service evidence.
    Local disk hashes do not prove the in-process Python code generation.
    """
    spec = _spec(operation)
    p = normalize(operation, params)
    files = {"app.py"} if spec["port"] == BENCH_PORT else {"cosmology_server.py"}
    inputs, runtime = [], {}
    if operation.startswith("lab_") or operation in {"data", "universe_domains", "universe_load", "inquiry"}:
        files.update(("data_lab.py", "hdf5_bridge.py", "adapters/hdf5_reader.py", "treatment.py", "treatment_coverage.py"))
    if operation == "lab_gpu":
        files.add("gpu_status.py")
    if operation.startswith("universe_"):
        files.update(("resident_bridge.py", "adapters/resident_worker.py", "hdf5_bridge.py", "data_lab.py"))
        if operation != "universe_domains":
            status = _gw_status()
            runtime["gw"] = _resident_provenance(status, p.get("id") if operation == "universe_view" else None)
        if operation in {"universe_model", "universe_event_view", "universe_event", "universe_load"}:
            files.update(("models/model_sources.json", "models/tgl_ringdown_prediction.py", "models/tgl_ringdown_template.py"))
        if operation in {"universe_event_view", "universe_event", "universe_load"}:
            files.update(("event_sources.py", "adapters/event_runtime.py"))
            inputs.extend(_pin(EVENT_ROOT / name, "C6/" + name) for name in _EVENT_FILES)
        if operation == "universe_load" and not _complete(status, p["domain"]):
            catalog_data = _http(BENCH_PORT, "GET", "/api/lab/catalog")
            for row in catalog_data.get("items", []):
                if row.get("group") in {"GWOSC: strain", "GW: strain da bancada 013BIS"} and row.get("format") in {".h5", ".hdf5"}:
                    inputs.append(_pin(_catalog_source(row["id"], catalog_data), "data/" + row["id"]))
    if operation in {"lab_preview", "lab_describe", "lab_treatment"}:
        source = _catalog_source(p["id"])
        inputs.append(_pin(source, "data/" + p["id"]))
        if source.name == _BAO_NAMES[0]:
            inputs.append(_pin(source.with_name(_BAO_NAMES[1]), "BAO/covariance"))
    if operation in {"identity_chain", "dephasing", "bench_overview"}:
        inputs.append(_pin(Path(r"C:\IALD\Central de Patentes\memory\TGL_ATLAS.md"), "TGL_ATLAS.md"))
    if operation in {"relations", "routes", "inquiry", "bench_overview", "identity_chain", "dephasing"}:
        inputs.append(_pin(CHATGPT_ROOT / "APP_ESTRUTURA_V368_20260919/estrutura_v368.json", "historical_v368/estrutura_v368.json"))
    if operation == "bench_overview":
        inputs.append(_pin(CHATGPT_ROOT / "APP_ESTRUTURA_V368_20260919/proof_manifest.json", "historical_v368/proof_manifest.json"))
    if operation == "lab_canonical":
        scientific = Path(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós")
        for name in ("um.py", "um_absoluto_forma_canonica.md"):
            inputs.append(_pin(scientific / name, "canonical/" + name))
        inputs.append(_pin(Path(r"C:\IALD\Artigo\frente_alpha\tgl_multiprobe_v3.py"), "bao/tgl_multiprobe_v3.py"))
    if operation == "lab_bao_report":
        inputs.append(_pin(Path(r"C:\IALD\Artigo\frente_alpha\output_v3\multiprobe_v3_report_20260522_135856.json"), "bao/report.json"))
    if operation == "inquiry":
        data_index = _http(BENCH_PORT, "GET", "/api/data")
        inputs.append({"source": "bench/data_index", "sha256": hashlib.sha256(
            _canonical(data_index).encode("utf-8")).hexdigest(), "scope": "LEXICAL_CATALOG_INPUT_NOT_DATA_CONTENT"})
    if operation in {"protocols", "inquiry", "bench_overview"}:
        for name in ("ENTREGA_016_RELATORIO_FINAL.md", "ENTREGA_015_RELATORIO_FINAL.md"):
            inputs.append(_pin(CHATGPT_ROOT / "TUNEL/DO_CHATGPT" / name, name))
    if spec["port"] == COSMOS_PORT:
        files.update(("cosmology_runtime.py", "cosmology_v3_bridge.py", "workers/cosmology_v3_worker.py",
                      "scientific_models/tgl_camb_worker_v3.py", "cosmology_scenarios.py", "cosmology_exports.py"))
        health = _http(COSMOS_PORT, "GET", "/api/cosmology/health")
        if health.get("service") != "tgl-cosmology-resident-v1" or health.get("status") != "RUNNING":
            _fail("Identidade do serviço cosmológico não confirmada.", "PROVENANCE_UNAVAILABLE")
        runtime["cosmos"] = {"service": health["service"],
                             "load_id": health.get("memory", {}).get("load_id"),
                             "generation_scope": "HEALTH_ONLY_NO_CACHE_INITIALIZATION; missing load_id is unknown, not current generation verified"}
        if operation in {"cosmos_evaluate", "cosmos_status", "cosmos_save_scenario"} or (operation == "cosmos_export" and "scenario_id" not in p):
            inputs.extend(_pin(BENCH_ROOT / "data/cosmology" / name, "DESI_DR2/" + name) for name in _BAO_NAMES)
        historical_id = p.get("scenario_id") if operation == "cosmos_export" else p.get("id") if operation in {"cosmos_scenario", "cosmos_get_export"} else None
        if historical_id:
            route = "exports" if operation == "cosmos_get_export" else "scenarios"
            snapshot = _http(COSMOS_PORT, "GET", f"/api/cosmology/{route}/{historical_id}")
            if snapshot.get("id") != historical_id or not _SHA.fullmatch(str(snapshot.get("sha256", ""))):
                _fail("Recibo histórico sem identidade ou hash válido.", "PROVENANCE_UNAVAILABLE")
            inputs.append({"source": route + "/" + historical_id, "sha256": hashlib.sha256(_canonical(snapshot).encode("utf-8")).hexdigest(),
                           "service_record_sha256": snapshot["sha256"], "scope": "HTTP_SNAPSHOT_CANONICAL_JSON"})
    executors = [_pin(BENCH_ROOT / name, "bench/" + name) for name in sorted(files)]
    executors.append(_pin(Path(__file__), "iald_bench_catalog.py"))
    return {"schema": CONTRACT_VERSION, "operation": operation, "parameters": p,
            "executors": executors, "inputs": sorted(inputs, key=lambda x: x["source"]), "runtime": runtime,
            "scope": "SOURCE_AND_SELECTED_INPUT_PINS_NOT_PHYSICAL_VALIDATION; disk pins do not attest imported live code",
            "dates": "Record planned_at/dispatched_at in caller journal; excluded from dedupe."}
