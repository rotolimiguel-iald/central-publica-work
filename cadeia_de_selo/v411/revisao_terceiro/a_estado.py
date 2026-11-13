import json, os, sys, datetime
P = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411\revisao_terceiro\ESTADO_REVISAO_v411.A.json"
def carregar():
    if os.path.exists(P):
        return json.load(open(P, encoding="utf-8"))
    return {"escopo": "A", "revisor": "Sonnet 5.5 (claude-sonnet-5-5), revisor de terceiro do escopo A; NAO construiu a v411", "itens": {}, "achados": [], "candidato_sha16_no_inicio": "21e87eb3df5098f8", "notas": []}
def gravar(d):
    d["atualizado"] = datetime.datetime.now().isoformat(timespec="seconds")
    open(P + ".tmp", "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=1)); os.replace(P + ".tmp", P)
if __name__ == "__main__":
    d = carregar()
    item, feito, resumo = sys.argv[1], sys.argv[2], sys.argv[3]
    d["itens"][item] = {"feito": feito == "sim", "resumo": resumo}
    for a in sys.argv[4:]:
        d["achados"].append(json.loads(a))
    gravar(d); print("estado gravado:", item)
