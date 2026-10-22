# -*- coding: utf-8 -*-
"""8a afericao no RUNTIME: sai o parametro morto result_present (e o st["_qp_result_present"]): o fato e' medido so no marcador; e o run_dir entra no st LOGO
depois do makedirs (antes do Popen), para o marcador medir a pasta tambem no LAUNCH_FAILED. Backup ja feito (.bak_antes_afer8)."""
import ast, hashlib, os
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "v384_runtime.py")
raw = open(P, "rb").read(); s = raw.decode("utf-8")
assert open(P + ".bak_antes_afer8", "rb").read() == raw
PAIRS = [
    ('''def _qp_out_marker(verdict, st, reason, result_present=False):''', '''def _qp_out_marker(verdict, st, reason):'''),
    ('''def _qp_out_marker_safe(out, verdict, st, reason, result_present=False):''', '''def _qp_out_marker_safe(out, verdict, st, reason):'''),
    ('''        out["out_file_sha256"] = _qp_out_marker(verdict, st, reason, result_present)''', '''        out["out_file_sha256"] = _qp_out_marker(verdict, st, reason)'''),
    ('''        st["_qp_result_present"] = bool(os.path.exists(rp))
''', ''''''),
    ('''        _qp_out_marker_safe(out, out.get("verdict"), st, "copy_failed" if out.get("copy_to_out_error") else "finish_failed", bool(st.get("_qp_result_present")))''',
     '''        _qp_out_marker_safe(out, out.get("verdict"), st, "copy_failed" if out.get("copy_to_out_error") else "finish_failed")   # o fato (result_file_absent) e' medido no marcador'''),
    ('''        os.makedirs(run_dir, exist_ok=False)
''', '''        os.makedirs(run_dir, exist_ok=False)
        st["run_dir"] = run_dir   # ja aqui: o marcador mede esta pasta mesmo se o lancamento falhar (8a afericao)
'''),
]
for old, new in PAIRS:
    c = s.count(old); assert c == 1, (c, old[:100])
    s = s.replace(old, new)
assert "result_present" not in s and "_qp_result_present" not in s
ast.parse(s.replace("__QP_WORKER_SRC__", "x").replace("__QP_SPEC_JSON__", "x"))
b = s.encode("utf-8"); open(P + ".tmp", "wb").write(b); assert os.path.getsize(P + ".tmp") == len(b); os.replace(P + ".tmp", P)
print("ok", len(PAIRS), hashlib.sha256(b).hexdigest()[:16])
