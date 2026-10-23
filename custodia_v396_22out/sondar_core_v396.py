# -*- coding: utf-8 -*-
"""SÓ LEITURA: o que a v396 traz no core selado contra o core da v395 (backup fora do repo), para escrever os geradores sem digitar número."""
import json, re, sys
from pathlib import Path
sys.stdout.reconfigure(encoding="utf-8")
NOS = Path(r"C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós")
BK = Path(r"C:/IALD/Artigo/the_boundary_BACKUPS/um_v395_8918b17803792cf2")
core = json.loads((NOS / "um_absoluto.json").read_text(encoding="utf-8")).get("core") or {}
c5 = json.loads((BK / "um_absoluto.json").read_text(encoding="utf-8")).get("core") or {}
novos = sorted(k for k in core if k not in c5)
print("novos registros:", novos)
kf, kf5 = core.get("kernel_formalization") or {}, c5.get("kernel_formalization") or {}
nb = [k for k in kf if k not in kf5]
print("bandeiras novas:", len(nb), nb[:3], nb[-2:])
T = core["testemunha_estatica_v396"]
def curto(x, n=400):
    return json.dumps(x, ensure_ascii=False)[:n]
for k, v in T.items():
    print("  T.%s = %s" % (k, curto(v, 600)))
C = core["cunhagens_v396"]
print("cunhagens keys:", list(C.keys()))
print("  verbatim:", list((C.get("verbatim") or {}).keys()))
print("  verdict:", C.get("verdict"))
K = core["kh_n1_cobertura_v396"]
print("kh keys:", list(K.keys()))
print("  verdict:", K.get("verdict"))
for e in K.get("erratas") or []:
    print("  errata:", curto(e, 700))
E = core["estatuto_da_prova_v391"]
print("P1:", curto(E["prova_1_kernel"], 300))
print("VE:", E["verdict"][:200])
for nome in ("kh_n1_cobertura_v395", "cunhagens_v395", "psibit_v395"):
    r = core.get(nome) or {}
    print(nome, "verdict:", str(r.get("verdict"))[:160], "| erratas:", len(r.get("erratas") or []))
    for e in r.get("erratas") or []:
        print("   e:", curto(e, 500))
