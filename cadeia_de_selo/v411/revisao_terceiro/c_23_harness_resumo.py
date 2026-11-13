import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_lib import *
for nome in ("HARNESS_TEXTOS_ENSAIO_v411.json", "HARNESS_FECHAR_SANDBOX_v411.json"):
    j = json.load(open(V + "\pos_rito\\" + nome, encoding="utf-8"))
    print("==", nome, "tudo_passou:", j.get("tudo_passou"), "problemas:", len(j.get("problemas") or []), "inicio", j.get("inicio"), "veredito:", str(j.get("veredito"))[:60])
    for k, v in (j.get("etapas") or {}).items():
        ok = v.get("ok") if isinstance(v, dict) else v
        print("   ", k, ok, (str(v)[:100] if not ok else ""))
