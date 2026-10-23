# -*- coding: utf-8 -*-
"""f9v2_verdict.py -- carrega a FUNCAO DE VEREDITO PINADA (o texto, nunca uma copia reescrita) num espaco restrito (so math e decimal)."""
import decimal
import hashlib
import math

FUNCTION_NAME = "veredito_fase9_v2_c1"
TOKEN_BASE = "TGL_FASE9_V2_A_UNICA_PALAVRA_BETA_TGL"


class VerdictLoadError(RuntimeError):
    pass


def load_pinned_verdict(source, expected_sha256, name=FUNCTION_NAME):
    if not isinstance(source, str):
        raise VerdictLoadError("fonte da funcao nao e' texto")
    digest = hashlib.sha256(source.encode("utf-8")).hexdigest()
    if digest != expected_sha256:
        raise VerdictLoadError("sha256 da funcao difere do pino: %s != %s" % (digest, expected_sha256))

    def import_allowed(module, *args, **kwargs):
        if module == "math":
            return math
        if module == "decimal":
            return decimal
        raise VerdictLoadError("a funcao tentou importar %r" % module)

    ns = {"__builtins__": {"__import__": import_allowed, "abs": abs, "any": any, "all": all, "bool": bool, "dict": dict, "enumerate": enumerate,
                           "float": float, "format": format, "int": int, "isinstance": isinstance, "len": len, "list": list, "range": range,
                           "set": set, "str": str, "tuple": tuple, "type": type, "ValueError": ValueError}}
    exec(compile(source, "<pinned-veredito_fase9_v2_c1>", "exec"), ns)
    fn = ns.get(name)
    if not callable(fn):
        raise VerdictLoadError("funcao %s ausente" % name)
    return fn, digest
