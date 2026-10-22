"""sha256/bytes/mtime dos arquivos citados pela ESTRATEGIA B. Uso: python hashes.py <saida.json> <rotulo=caminho> ..."""
import hashlib, json, os, sys, datetime
out = {}
dest = sys.argv[1]
for arg in sys.argv[2:]:
    k, p = arg.split("=", 1)
    try:
        raw = open(p, "rb").read()
        out[k] = {"path": p, "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw),
                  "mtime": datetime.datetime.fromtimestamp(os.stat(p).st_mtime).isoformat(timespec="seconds")}
    except Exception as e:
        out[k] = {"path": p, "erro": repr(e)}
json.dump(out, open(dest, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
for k, v in out.items():
    print(k, "|", v.get("sha256", "ERRO")[:16], "|", v.get("bytes", v.get("erro")), "|", v["path"])
