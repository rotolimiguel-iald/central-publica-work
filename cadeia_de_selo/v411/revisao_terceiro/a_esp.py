import json, os
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411"
e = json.load(open(os.path.join(V, "ESPERADOS_v411.json"), encoding="utf-8"))
c = json.load(open(r"C:\t\k411c\falso_nos_v411\um_absoluto.json", encoding="utf-8"))["core"]
h = e["h0dn_v411"]; print("ESPERADOS.h0dn_v411 chaves:", list(h.keys()))
for k, v in h.items(): print("  ", k, "|", json.dumps(v, ensure_ascii=False)[:170])
print("h0dn:", list(e["h0dn"].keys())[:19])
hc = c["h0dn_bg1_v411"]
print("verdict esperado == core:", h.get("verdict") == hc["verdict"] if "verdict" in h else "n/a")
print("candidato_sha16 == 21e87eb3df5098f8:", e["candidato_sha16"], "| ensaio_sha16:", e["ensaio_sha16"])
print("escada:", e["escada"], "| gate:", e["qg_closure_verdict"][:40], "| beta:", e["beta"])
