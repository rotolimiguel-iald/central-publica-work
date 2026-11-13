"""grava (merge) um item no ESTADO_REVISAO_v411.CU.json: python cu_est.py <ITEM> <arquivo-json-com-o-conteudo>"""
import json, os, sys, time
P = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411\revisao_terceiro\ESTADO_REVISAO_v411.CU.json"
d = json.load(open(P, encoding="utf-8"))
item = sys.argv[1]
conteudo = json.load(open(sys.argv[2], encoding="utf-8"))
conteudo["gravado_em"] = time.strftime("%Y-%m-%dT%H:%M:%S")
d["itens"][item] = conteudo
open(P + ".tmp", "w", encoding="utf-8").write(json.dumps(d, ensure_ascii=False, indent=1))
os.replace(P + ".tmp", P)
print("estado gravado:", item, "| itens:", sorted(d["itens"]))
