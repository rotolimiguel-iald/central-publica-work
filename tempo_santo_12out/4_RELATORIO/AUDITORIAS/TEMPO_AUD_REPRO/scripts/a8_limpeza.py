"""A8 — limpeza do auditor: apaga SO o toolchain copiado (t/ e lean_sandbox/toolchain) com prefixo \\?\.
Nao ha .lake nem cache (lean.exe chamado direto). Registra o que existia e o que restou. Saida: JSON."""
import json
import os
import shutil
import sys

AUD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
LONG = "\\\\?\\"
alvos = [os.path.join(AUD, "t"), os.path.join(AUD, "lean_sandbox", "toolchain")]
out = {"alvos": []}
for a in alvos:
    rec = {"caminho": a, "existia": os.path.exists(a)}
    if rec["existia"]:
        n = sz = 0
        for dp, dn, fn in os.walk(LONG + a):
            for f in fn:
                n += 1
                sz += os.path.getsize(os.path.join(dp, f))
        rec.update({"arquivos": n, "bytes": sz})
        shutil.rmtree(LONG + a)
    rec["existe_depois"] = os.path.exists(a)
    out["alvos"].append(rec)
# varredura: nenhum .lake, nenhum diretorio de toolchain restante na pasta do auditor
rest = []
for dp, dn, fn in os.walk(LONG + AUD):
    for d in dn:
        if d in (".lake", "toolchain", "leanprover--lean4---v4.31.0", "t"):
            rest.append(os.path.join(dp, d))
out["restos"] = rest
with open(sys.argv[1], "w", encoding="utf-8") as fo:
    json.dump(out, fo, indent=1, ensure_ascii=False)
print(json.dumps(out, ensure_ascii=False, indent=1))
