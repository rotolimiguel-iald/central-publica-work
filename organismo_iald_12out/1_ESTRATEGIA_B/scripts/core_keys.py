"""Le registros selecionados do core v391 (um_absoluto.json) e imprime compacto. So leitura."""
import json, sys, hashlib
P = r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto.json"
raw = open(P, "rb").read(); print("core sha16", hashlib.sha256(raw).hexdigest()[:16], len(raw))
core = json.loads(raw.decode("utf-8"))
def show(k, maxlen=6000):
    v = core.get(k)
    print("\n" + "=" * 90 + "\n## " + k + (" (AUSENTE)" if v is None else ""))
    if v is not None:
        s = json.dumps(v, ensure_ascii=False, indent=1); print(s[:maxlen] + (" ...[cortado %d]" % len(s) if len(s) > maxlen else ""))
for k in sys.argv[1:]: show(k)
