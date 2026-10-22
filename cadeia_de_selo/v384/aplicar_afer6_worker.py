# -*- coding: utf-8 -*-
"""6a afericao no TRABALHADOR: a falha da gravacao do parcial do D128 deixa marca (partial_write_error); a referencia na CPU ausente ganha um CODIGO
(error_code CPUREF_JSON_ABSENT), para cada lingua do artigo compor a sua frase. Backup ja feito (pilar_quantico_worker_auditado_6a_passada.py)."""
import ast, hashlib, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "pilar_quantico_worker.py")
raw = open(P, "rb").read(); s = raw.decode("utf-8")
assert open(os.path.join(HERE, "pilar_quantico_worker_auditado_6a_passada.py"), "rb").read() == raw
PAIRS = [
    ('''            try:
                on_spectrum(dict(out))
            except Exception:
                pass''', '''            try:
                on_spectrum(dict(out))
            except Exception as e_:
                out["partial_write_error"] = _err(e_)   # a falha da gravacao do parcial deixa marca (6a afericao)'''),
    ('''            R["cpuref_compare"] = {"ok": False, "error": "cpuref.json ausente", "child_rc": child_rc}''',
     '''            R["cpuref_compare"] = {"ok": False, "error": "cpuref.json ausente", "error_code": "CPUREF_JSON_ABSENT", "child_rc": child_rc}   # o codigo: cada lingua compoe a frase (6a)'''),
]
for old, new in PAIRS:
    c = s.count(old); assert c == 1, (c, old[:120])
    s = s.replace(old, new)
ast.parse(s)
b = s.encode("utf-8"); assert b"\r" not in b
open(P + ".tmp", "wb").write(b); assert os.path.getsize(P + ".tmp") == len(b); os.replace(P + ".tmp", P)
print("ok", len(PAIRS), "sha16", hashlib.sha256(b).hexdigest()[:16])
