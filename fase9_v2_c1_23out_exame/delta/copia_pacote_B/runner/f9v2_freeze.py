# -*- coding: utf-8 -*-
"""f9v2_freeze.py -- a TRAVA: o runner recusa abrir sem um RECIBO DE CONGELAMENTO emitido pela gerencia e sem um RECIBO DE ABERTURA (ato proprio).

RECIBO DE CONGELAMENTO (freeze/RECIBO_DE_CONGELAMENTO.json) pina por sha256: a spec (arquivo e forma canonica), a funcao de veredito, o registro D-H, os modulos do runner
(e nenhum .py a mais na pasta runner/), as fontes dos leitores, o recibo da calibracao e, no pacote REAL, os arquivos da Bancada que formam o fornecedor do fundo.
Todo arquivo pinado e' lido UMA vez; a funcao devolve os bytes verificados e o runner nunca reabre o caminho (sem TOCTOU).
Esta trava nao e' autenticacao: o recibo e' ato da gerencia; o runner confere que o recibo existe, e' integro (autohash) e bate com os bytes.

ABERTURA UNICA (B4): check_freeze_core confere tudo MENOS as fontes; o runner consome o marcador freeze/ABERTURA_CONSUMIDA.json (criacao exclusiva, com o sha do recibo
de abertura) ANTES de read_sources ler a primeira fonte. Marcador existente => REFUSE__ALREADY_OPENED, com registro de recusa em freeze/REGISTRO_DE_RECUSA_*.json.
PYCACHE (B6): os pinos cobrem os .py, nao o bytecode; um runner/__pycache__ nao vazio recusa (REFUSE__PYCACHE_IN_RUNNER). Rodar SEMPRE com python -B."""
import hashlib
import json
import os
import time

SCHEMA_FREEZE = "F9V2C1_RECIBO_DE_CONGELAMENTO_V1"
SCHEMA_OPEN = "F9V2C1_RECIBO_DE_ABERTURA_V1"
SCHEMA_MARKER = "F9V2C1_ABERTURA_CONSUMIDA_V1"
KINDS = ("REAL", "SYNTHETIC_TEST_PACKAGE")
FREEZE_REL = "freeze/RECIBO_DE_CONGELAMENTO.json"
OPEN_REL = "freeze/RECIBO_DE_ABERTURA.json"
MARKER_REL = "freeze/ABERTURA_CONSUMIDA.json"
REFUSAL_PREFIX = "freeze/REGISTRO_DE_RECUSA_"


class Refusal(RuntimeError):
    """Recusa de abrir. code e' estavel (os testes de controle negativo leem o code)."""

    def __init__(self, code, detail=""):
        super().__init__("%s%s" % (code, (": " + detail) if detail else ""))
        self.code, self.detail = code, detail


def sha256_bytes(b):
    return hashlib.sha256(b).hexdigest()


def canonical(obj):
    return json.dumps(obj, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def autohash(obj):
    o = {k: v for k, v in obj.items() if k != "autohash"}
    return sha256_bytes(canonical(o))


def _read(root, rel):
    p = os.path.join(root, *rel.split("/"))
    if not os.path.isfile(p):
        raise Refusal("REFUSE__PINNED_FILE_MISSING", rel)
    return open(p, "rb").read()


def list_runner_py(root):
    d = os.path.join(root, "runner")
    return sorted("runner/" + f for f in os.listdir(d) if f.endswith(".py"))


def build_pins(root, kind, register_rel="spec/REGISTRO_DH_V2_C1.json", spec_rel=None, func_rel="spec/veredito_fase9_v2_c1.py",
               calib_rel="calibracao/CALIBRACAO_CAUDA_RECIBO.json", bancada_pins=None):
    """Calcula os pinos a partir do pacote (usado na EMISSAO do recibo e nos testes)."""
    spec_rel = spec_rel or "spec/PREREGISTRO_FASE9_V2_C1_A_UNICA_PALAVRA.json"
    pins = {}
    for key, rel in (("spec_arquivo", spec_rel), ("funcao_arquivo", func_rel), ("registro_dh", register_rel), ("calibracao_recibo", calib_rel)):
        b = _read(root, rel)
        pins[key] = {"path": rel, "sha256": sha256_bytes(b), "bytes": len(b)}
    spec_obj = json.loads(_read(root, spec_rel).decode("utf-8"))
    pins["spec_canonico_sha256"] = sha256_bytes(canonical(spec_obj["spec"]))
    pins["runner_modulos"] = {}
    for rel in list_runner_py(root):
        b = _read(root, rel)
        pins["runner_modulos"][rel] = {"sha256": sha256_bytes(b), "bytes": len(b)}
    reg = json.loads(_read(root, register_rel).decode("utf-8"))
    pins["fontes"] = {}
    for rid, r in reg["leitores"].items():
        b = _read(root, r["file"])
        pins["fontes"][rid] = {"path": r["file"], "sha256": sha256_bytes(b), "bytes": len(b)}
    if bancada_pins is not None:
        pins["bancada"] = bancada_pins
    return pins


def make_freeze_receipt(root, kind, emitido_por, auditoria_ref, token_base, bancada_pins=None, extra_atos=None, **kw):
    pins = build_pins(root, kind, bancada_pins=bancada_pins, **kw)
    rec = {"schema": SCHEMA_FREEZE, "package_kind": kind, "emitido_por": emitido_por, "token_base": token_base, "pins": pins,
           "atos": {"x13_decisao_do_operador_pinada": True, "dh_admissao_pinada": True, "auditoria_c1_runner_aprovada": True,
                    "auditoria_ref": auditoria_ref, **(extra_atos or {})}}
    rec["autohash"] = autohash(rec)
    return rec


def make_open_receipt(freeze_receipt_bytes, ato):
    rec = {"schema": SCHEMA_OPEN, "freeze_receipt_sha256": sha256_bytes(freeze_receipt_bytes), "ato_do_operador": ato}
    rec["autohash"] = autohash(rec)
    return rec


def check_freeze_core(root, *, require_bancada=None):
    """Confere o recibo de congelamento contra os bytes de TUDO que nao e' fonte (spec, funcao, registro, calibracao, modulos do runner, Bancada).
    NAO le nenhuma fonte. Devolve (recibo, bytes_verificados). Levanta Refusal."""
    p = os.path.join(root, *FREEZE_REL.split("/"))
    if not os.path.isfile(p):
        raise Refusal("REFUSE__FREEZE_RECEIPT_MISSING", FREEZE_REL)
    raw = open(p, "rb").read()
    try:
        rec = json.loads(raw.decode("utf-8"))
    except (UnicodeError, ValueError) as e:
        raise Refusal("REFUSE__FREEZE_RECEIPT_INVALID", "json") from e
    if not isinstance(rec, dict) or rec.get("schema") != SCHEMA_FREEZE:
        raise Refusal("REFUSE__FREEZE_RECEIPT_INVALID", "schema")
    if rec.get("autohash") != autohash(rec):
        raise Refusal("REFUSE__FREEZE_RECEIPT_INVALID", "autohash")
    if rec.get("package_kind") not in KINDS:
        raise Refusal("REFUSE__FREEZE_RECEIPT_INVALID", "package_kind")
    atos = rec.get("atos") or {}
    for k in ("x13_decisao_do_operador_pinada", "dh_admissao_pinada", "auditoria_c1_runner_aprovada"):
        if atos.get(k) is not True:
            raise Refusal("REFUSE__FREEZE_ACT_MISSING", k)
    if not rec.get("emitido_por"):
        raise Refusal("REFUSE__FREEZE_RECEIPT_INVALID", "emitido_por")
    pins = rec.get("pins") or {}
    verified = {"__freeze_raw__": raw}
    for key in ("spec_arquivo", "funcao_arquivo", "registro_dh", "calibracao_recibo"):
        pin = pins.get(key)
        if not isinstance(pin, dict):
            raise Refusal("REFUSE__FREEZE_RECEIPT_INVALID", "pin " + key)
        b = _read(root, pin["path"])
        if sha256_bytes(b) != pin["sha256"] or len(b) != pin["bytes"]:
            raise Refusal("REFUSE__PIN_MISMATCH", key)
        verified[key] = b
    spec_obj = json.loads(verified["spec_arquivo"].decode("utf-8"))
    if sha256_bytes(canonical(spec_obj["spec"])) != pins.get("spec_canonico_sha256"):
        raise Refusal("REFUSE__PIN_MISMATCH", "spec_canonico")
    if spec_obj.get("spec_sha256") != pins.get("spec_canonico_sha256"):
        raise Refusal("REFUSE__PIN_MISMATCH", "spec_sha256_interno")
    mods = pins.get("runner_modulos") or {}
    on_disk = list_runner_py(root)
    if sorted(mods) != on_disk:
        extra = sorted(set(on_disk) ^ set(mods))
        raise Refusal("REFUSE__RUNNER_FILESET_DIFFERS", ",".join(extra))
    for rel, pin in mods.items():
        b = _read(root, rel)
        if sha256_bytes(b) != pin["sha256"] or len(b) != pin["bytes"]:
            raise Refusal("REFUSE__PIN_MISMATCH", rel)
    pyc = os.path.join(root, "runner", "__pycache__")
    if os.path.isdir(pyc) and os.listdir(pyc):
        raise Refusal("REFUSE__PYCACHE_IN_RUNNER", "apague runner/__pycache__ e rode com python -B")
    reg = json.loads(verified["registro_dh"].decode("utf-8"))
    fontes = pins.get("fontes") or {}
    if sorted(fontes) != sorted(reg["leitores"]):
        raise Refusal("REFUSE__PIN_MISMATCH", "inventario de fontes difere do registro D-H")
    for rid, pin in fontes.items():
        rr = reg["leitores"][rid]
        if pin["path"] != rr["file"] or pin["sha256"] != rr["sha256"]:
            raise Refusal("REFUSE__PIN_MISMATCH", "fonte %s: recibo difere do registro D-H" % rid)
    if rec["package_kind"] == "REAL":
        bp = pins.get("bancada")
        if not isinstance(bp, dict) or not bp:
            raise Refusal("REFUSE__FREEZE_RECEIPT_INVALID", "pinos da Bancada ausentes no pacote REAL")
        if require_bancada is not None:
            for rel, pin in bp.items():
                cur = require_bancada.get(rel)
                if cur is None or cur["sha256"] != pin["sha256"]:
                    raise Refusal("REFUSE__PIN_MISMATCH", "bancada " + rel)
    return rec, verified


def read_sources(root, rec, verified):
    """Le cada fonte pinada UMA vez e confere o sha256. SO depois do marcador de abertura. Preenche verified['sources']."""
    reg = json.loads(verified["registro_dh"].decode("utf-8"))
    sources = {}
    for rid, pin in (rec["pins"].get("fontes") or {}).items():
        b = _read(root, pin["path"])
        if sha256_bytes(b) != pin["sha256"] or len(b) != pin["bytes"]:
            raise Refusal("REFUSE__SOURCE_ADULTERATED", rid)
        sources[rid] = b
    if sorted(sources) != sorted(reg["leitores"]):
        raise Refusal("REFUSE__PIN_MISMATCH", "fontes lidas difere do registro D-H")
    verified["sources"] = sources
    return verified


def check_freeze(root, *, require_bancada=None):
    """Conferencia completa (preflight e testes): core + fontes. O runner NAO usa esta funcao: usa core, marcador, read_sources."""
    rec, verified = check_freeze_core(root, require_bancada=require_bancada)
    read_sources(root, rec, verified)
    return rec, verified


def check_opening_act(root, freeze_raw):
    p = os.path.join(root, *OPEN_REL.split("/"))
    if not os.path.isfile(p):
        raise Refusal("REFUSE__OPENING_ACT_MISSING", OPEN_REL)
    raw_open = open(p, "rb").read()
    try:
        rec = json.loads(raw_open.decode("utf-8"))
    except (UnicodeError, ValueError) as e:
        raise Refusal("REFUSE__OPENING_ACT_INVALID", "json") from e
    if rec.get("schema") != SCHEMA_OPEN or rec.get("autohash") != autohash(rec):
        raise Refusal("REFUSE__OPENING_ACT_INVALID", "schema/autohash")
    if rec.get("freeze_receipt_sha256") != sha256_bytes(freeze_raw):
        raise Refusal("REFUSE__OPENING_ACT_INVALID", "o ato de abertura nao se refere a este recibo de congelamento")
    ato = rec.get("ato_do_operador")
    if not isinstance(ato, dict) or not ato.get("quem") or not ato.get("texto"):
        raise Refusal("REFUSE__OPENING_ACT_INVALID", "ato do operador vazio")
    out = dict(rec)
    out["__file_sha256__"] = sha256_bytes(raw_open)
    return out


def consume_opening_marker(root, freeze_raw, opening):
    """B4: a abertura vira UMA SO, mecanicamente. Cria freeze/ABERTURA_CONSUMIDA.json por criacao EXCLUSIVA (O_EXCL), com o sha256 do recibo de abertura,
    ANTES de qualquer fonte ser lida. Se o marcador ja' existe (mesmo meio escrito, apos queda), levanta Refusal(REFUSE__ALREADY_OPENED)."""
    path = os.path.join(root, *MARKER_REL.split("/"))
    os.makedirs(os.path.dirname(path), exist_ok=True)
    body = json.dumps({"schema": SCHEMA_MARKER, "recibo_de_abertura_sha256": opening["__file_sha256__"], "recibo_de_abertura_autohash": opening["autohash"],
                       "recibo_de_congelamento_sha256": sha256_bytes(freeze_raw), "quando_unix": time.time(), "pid": os.getpid(),
                       "nota": "este marcador impede uma segunda abertura; remove-lo e' ato registrado da gerencia, com novo recibo de abertura"},
                      ensure_ascii=False, indent=1, sort_keys=True).encode("utf-8")
    try:
        fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, "O_BINARY", 0))
    except FileExistsError as e:
        raise Refusal("REFUSE__ALREADY_OPENED", MARKER_REL) from e
    try:
        os.write(fd, body)
        os.fsync(fd)
    finally:
        os.close(fd)
    if os.path.getsize(path) != len(body):
        raise Refusal("REFUSE__WRITE_SIZE_MISMATCH", MARKER_REL)
    return sha256_bytes(body)


def write_refusal_record(root, code, detail, fase, opening_sha=None):
    """Recusa DEPOIS de aberto (ou tentativa de reabrir) tambem grava registro: freeze/REGISTRO_DE_RECUSA_<carimbo>_<n>.json (criacao exclusiva)."""
    stamp = time.strftime("%Y%m%d_%H%M%S")
    body = json.dumps({"schema": "F9V2C1_REGISTRO_DE_RECUSA_V1", "codigo": code, "detalhe": str(detail)[:2000], "fase": fase, "recibo_de_abertura_sha256": opening_sha,
                       "quando_unix": time.time(), "pid": os.getpid()}, ensure_ascii=False, indent=1, sort_keys=True).encode("utf-8")
    os.makedirs(os.path.join(root, "freeze"), exist_ok=True)
    for n in range(1000):
        path = os.path.join(root, *(REFUSAL_PREFIX + "%s_%03d.json" % (stamp, n)).split("/"))
        try:
            fd = os.open(path, os.O_CREAT | os.O_EXCL | os.O_WRONLY | getattr(os, "O_BINARY", 0))
        except FileExistsError:
            continue
        try:
            os.write(fd, body)
            os.fsync(fd)
        finally:
            os.close(fd)
        return path
    raise Refusal("REFUSE__REFUSAL_RECORD_FAILED", code)
