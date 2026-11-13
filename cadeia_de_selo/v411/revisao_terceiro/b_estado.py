import json, sys, datetime, os
P = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411\revisao_terceiro\ESTADO_REVISAO_v411.B.json"
def load():
    if os.path.exists(P): return json.load(open(P, encoding="utf-8"))
    return {"escopo": "B", "itens_feitos": {}, "achados": [], "nota": ""}
def save(s):
    s["atualizado"] = datetime.datetime.now().isoformat(timespec="seconds")
    open(P + ".tmp", "w", encoding="utf-8").write(json.dumps(s, ensure_ascii=False, indent=1)); os.replace(P + ".tmp", P)
def item(nome, resumo, achados=None):
    s = load(); s["itens_feitos"][nome] = resumo
    for a in (achados or []):
        s["achados"] = [x for x in s["achados"] if x["id"] != a["id"]] + [a]
    save(s)
if __name__ == "__main__":
    item("B1", "topo PT e EN do resumo: igual ao TOPO com marcadores do core (norm alnum); painel/estado nao estao nos rendidos do artigo (so README/handoff, escopo C)")
