"""A7: specs cunhagens_v411 e kh_n1_cobertura_v411; erratas; p2_ao_lado_da_v387; selo; os 6 textos da gerencia (sha256 completo)."""
import json, os, hashlib
import a_lib
V = a_lib.V
N = r"C:\t\k411c\falso_nos_v411"
core = json.load(open(os.path.join(N, "um_absoluto.json"), encoding="utf-8"))["core"]
selo = json.load(open(os.path.join(N, "um_absoluto_selo.json"), encoding="utf-8"))
base = json.load(open(os.path.join(V, "base_v410", "um_absoluto.json"), encoding="utf-8"))["core"]
bselo = json.load(open(os.path.join(V, "base_v410", "um_absoluto_selo.json"), encoding="utf-8"))
print("selo um_version:", selo.get("um_version"), "| base:", bselo.get("um_version"), "| chaves novas no selo:", [k for k in selo if k not in bselo], "| sumidas:", [k for k in bselo if k not in selo])
sh = selo.get("h0dn_bg1_v411"); print("selo.h0dn_bg1_v411 chaves:", len(sh) if sh else None, list(sh.keys()) if sh else None)
print("selo.registros_v411:", json.dumps(selo.get("registros_v411"), ensure_ascii=False)[:500])
h = core["h0dn_bg1_v411"]
print("selo.h0dn == core (campo a campo):", all(sh.get(k) == h.get(k) for k in sh), "| p2 no selo == core:", sh.get("p2_ao_lado_da_v387") == h.get("p2_ao_lado_da_v387"))
p2 = h["p2_ao_lado_da_v387"]; print("p2_ao_lado:", json.dumps(p2, ensure_ascii=False)[:900])
topo = json.load(open(os.path.join(V, "TOPO_RATIFICADO_v411.json"), encoding="utf-8"))
print("TOPO chaves:", list(topo.keys()))
print("rotulo_p2 do TOPO:", repr(topo.get("rotulo_p2"))[:400])
print("rotulo do core == TOPO.rotulo_p2 (com <n> trocado por 6):", p2["rotulo"] == str(topo["rotulo_p2"] if isinstance(topo["rotulo_p2"], str) else topo["rotulo_p2"].get("texto", "")).replace("<n>", "6"))
c = core["cunhagens_v411"]
print("cunhagens_v411: chaves:", list(c.keys())); print("  verdict:", c.get("verdict")); print("  all_verified:", c.get("all_verified"))
for k in ("falas", "decisoes", "erratas", "ressalvas"):
    if k in c: print("  ", k, type(c[k]).__name__, len(c[k]))
print("  decisoes ids:", list((c.get("decisoes") or {}).keys()) if isinstance(c.get("decisoes"), dict) else c.get("decisoes"))
er = c.get("erratas")
print("  erratas:", json.dumps(er, ensure_ascii=False)[:1500])
print("  checks:", [(x.get("id"), x.get("ok")) for x in c.get("checks", [])])
k = core["kh_n1_cobertura_v411"]
print("kh_n1_cobertura_v411:", k.get("verdict"), "| all_verified:", k.get("all_verified"))
for x in k.get("checks", []):
    print("   ", x.get("id"), x.get("ok"), x.get("op"), "|", str(x.get("descricao"))[:110], "| esperado:", str(x.get("esperado"))[:50], "| obtido:", str(x.get("obtido"))[:50])
print("  erratas:", json.dumps(k.get("erratas"), ensure_ascii=False)[:1200])
k10 = core["kh_n1_cobertura_v410"]; print("kh_n1_cobertura_v410 (candidato):", k10.get("verdict"), k10.get("all_verified"), "| base:", base["kh_n1_cobertura_v410"].get("verdict"), base["kh_n1_cobertura_v410"].get("all_verified"))
for x, y in zip(k10["checks"], base["kh_n1_cobertura_v410"]["checks"]):
    if json.dumps(x, sort_keys=True) != json.dumps(y, sort_keys=True):
        print("   v410 check mudou:", x["id"], "| op", y.get("op"), "->", x.get("op"), "| ok", y.get("ok"), "->", x.get("ok"))
print("erratas da v410 (candidato):", [ (e.get("ao_lado_de") or "")[:80] for e in k10.get("erratas", [])])
# os 6 textos da gerencia
f = a_lib.Fonte(a_lib.CAND, "cand")
ns = f.carregar(["_V411_SPECS"])
for s in ns["_V411_SPECS"]:
    if s["nome"] == "cunhagens_v411":
        for t in s["textos_da_gerencia_citados"] if "textos_da_gerencia_citados" in s else []:
            pass
def acha(x):
    if isinstance(x, dict):
        for k_, v_ in x.items():
            if k_ == "textos_da_gerencia_citados": yield v_
            else: yield from acha(v_)
    elif isinstance(x, list):
        for v_ in x: yield from acha(v_)
for lst in acha(ns["_V411_SPECS"]):
    for t in lst:
        p = os.path.join(r"C:\IALD\Central de Patentes\work\cunhagens_13out", t["nome"])
        print("  gerencia:", t["nome"][:70], "| sha ok:", hashlib.sha256(open(p, "rb").read()).hexdigest() == t["sha256"])
