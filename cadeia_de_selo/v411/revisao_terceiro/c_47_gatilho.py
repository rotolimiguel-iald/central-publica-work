import json
j = json.load(open(r"C:\t\k411c\ensaio_topo_proposto\pos_rito_gatilho\TESTE_GATILHO_CUSTODIA_v411.json", encoding="utf-8"))
print("tudo_passou:", j.get("tudo_passou"), "n_casos:", j.get("n_casos"), "n_negativos:", j.get("n_negativos"))
for k, v in j["casos"].items():
    if "ordem" in k.lower() or "D174" in k or "--ordem" in json.dumps(v):
        print(k[:90], "->", json.dumps(v, ensure_ascii=False)[:200])
print("falhas:", [k for k, v in j["casos"].items() if v.get("ok") is not True])
