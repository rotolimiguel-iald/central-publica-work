# -*- coding: utf-8 -*-
"""7a afericao no RUNTIME: o marcador devolve o sha256 dos BYTES que escreveu (sem reler o arquivo do Nos depois da troca: um PermissionError transitorio na
releitura nao remove mais um marcador valido); e result_file_absent e' MEDIDO no proprio marcador, no disco (run_dir, ou cache_dir na rodada reaproveitada:
result.json ou result_partial.json) -- None («nao verificado») quando nao ha pasta. Backup ja feito (.bak_antes_afer7)."""
import ast, hashlib, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "v384_runtime.py")
raw = open(P, "rb").read(); s = raw.decode("utf-8")
assert open(P + ".bak_antes_afer7", "rb").read() == raw
PAIRS = [
    ('''    p = os.path.join(OUT, "um_absoluto_pilar_quantico.json"); tmp = p + ".tmp_qp"
    b = json.dumps({"verdict": verdict, "marker": True, "reason": reason, "result_file_absent": not result_present,''',
     '''    p = os.path.join(OUT, "um_absoluto_pilar_quantico.json"); tmp = p + ".tmp_qp"
    _rd = st.get("cache_dir") if st.get("mode") == "REUSE" else st.get("run_dir")   # MEDIDO no disco, aqui (7a afericao); None = nao verificado
    _absent = (not (os.path.exists(os.path.join(_rd, "result.json")) or os.path.exists(os.path.join(_rd, "result_partial.json")))) if _rd else None
    b = json.dumps({"verdict": verdict, "marker": True, "reason": reason, "result_file_absent": _absent,'''),
    ('''    return hashlib.sha256(open(p, "rb").read()).hexdigest()''', '''    return hashlib.sha256(b).hexdigest()   # os bytes escritos, sem reler o Nos depois da troca (7a afericao)'''),
]
for old, new in PAIRS:
    c = s.count(old); assert c == 1, (c, old[:120])
    s = s.replace(old, new)
ast.parse(s.replace("__QP_WORKER_SRC__", "x").replace("__QP_SPEC_JSON__", "x"))
b = s.encode("utf-8")
open(P + ".tmp", "wb").write(b); assert os.path.getsize(P + ".tmp") == len(b); os.replace(P + ".tmp", P)
print("ok", len(PAIRS), hashlib.sha256(b).hexdigest()[:16])
