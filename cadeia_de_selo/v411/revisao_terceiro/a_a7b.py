import json, os
N = r"C:\t\k411c\falso_nos_v411"
core = json.load(open(os.path.join(N, "um_absoluto.json"), encoding="utf-8"))["core"]
c = core["cunhagens_v411"]
for e in c["erratas"]:
    print("errata:", e.get("ao_lado_de")[:90], "|", e.get("assinatura"))
    print("      agora:", e.get("agora")[:160])
ex = c["extras"]; print("extras chaves:", list(ex.keys()))
print("decisoes:", list(ex["decisoes"].keys()), len(ex["decisoes"]))
print("erratas_ids:", ex["erratas_ids"], "| ressalvas:", len(ex["ressalvas_rotulos"]), "| gerencia citados:", len(ex["textos_da_gerencia_citados"]), "| fora:", ex["falas_fora_do_desenho"])
print("verbatim:", type(c["verbatim"]).__name__, json.dumps(c["verbatim"], ensure_ascii=False)[:500])
print("lido:", json.dumps(c["lido"], ensure_ascii=False)[:600])
print("checks descricoes:"); [print("   ", x.get("descricao", "")[:130], "|", x.get("ok")) for x in c["checks"]]
print("leituras_do_operador:", json.dumps(c.get("leituras_do_operador"), ensure_ascii=False)[:400])
print("diz:", [d[:120] for d in c["diz"]][:6]); print("nao_diz:", [d[:120] for d in c["nao_diz"]][:6])
