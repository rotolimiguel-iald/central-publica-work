from b_lib import *
import re, math
C = core()["core"]; h = C["h0dn_bg1_v411"]; v = h["values"]
print("atos:", json.dumps(v.get("atos"), ensure_ascii=False))
W = r"C:\IALD\Central de Patentes\work\pre_registro_h0dn_publicacao_12nov"
for fn in ("RECIBO_PUBLICACAO_20261112_074508.json", "RECIBO_PUBLICACAO_RESULTADO_20261112_075315.json"):
    r = json.loads(rd(W + "\\" + fn))
    def walk(o, p=""):
        if isinstance(o, dict):
            for k, x in o.items():
                if re.search(r"commit|push|hora|time|utc|quando|inicio|data", k, re.I) and not isinstance(x, (dict, list)): print("  ", fn[:30], p + "." + k, "=", str(x)[:90])
                walk(x, p + "." + k)
        elif isinstance(o, list):
            for i, x in enumerate(o[:6]): walk(x, p + "[%d]" % i)
    walk(r)
