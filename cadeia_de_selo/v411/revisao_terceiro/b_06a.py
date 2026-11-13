from b_lib import *
import re
C = core()["core"]
hits = []
def walk(o, p):
    if isinstance(o, dict):
        for k, v in o.items():
            if k in ("ledger", "n_cobrancas", "livro_de_cobrancas", "charges") or "cobranca" in k.lower() or "ledger" in k.lower():
                hits.append((p + "." + k, type(v).__name__, (json.dumps(v, ensure_ascii=False)[:200])))
            walk(v, p + "." + k)
    elif isinstance(o, list):
        for i, v in enumerate(o[:3]): walk(v, p + "[%d]" % i)
walk(C, "")
for h in hits[:60]: print(h)
