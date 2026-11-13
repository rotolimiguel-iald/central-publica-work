import json
for f in ("rotas_prep.json", "rotas_h0dn.json"):
    j = json.load(open(r"C:\t\k411c\revisao_C\\" + f, encoding="utf-8"))
    for r in j["rotas"]:
        print(r["rota_id"], "|", r["status"], "|", str(r.get("veredito"))[:70])
