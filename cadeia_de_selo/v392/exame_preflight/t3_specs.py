import json, re
C = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v392\um_v392_candidato.py"
lines = open(C, encoding="utf-8").read().split("\n")
def grab(start_pat):
    i = next(k for k,l in enumerate(lines) if l.startswith(start_pat))
    j = i+1
    while j < len(lines) and (lines[j].startswith((" ", "\t")) or lines[j]=="" or lines[j].startswith(("]","}"))): 
        j += 1
    return "\n".join(lines[i:j]), i+1
g = {}
for p in ["_V392_SPECS =", "_V392_FONTES =", "_V392_VERBATINS2 ="]:
    src, ln = grab(p); exec(src, g); print(p, "line", ln)
T = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v392\tentativa1_rito_falhou_20261013_160045" + "\\"
d = json.load(open(T+"um_absoluto.json", encoding="utf-8")); core = d.get("core", d)
for s in g["_V392_SPECS"]:
    if s["nome"] in ("kh_n1_cobertura_v392","erratas_o_que_resta_v392"):
        print("=====", s["nome"], "fontes", s.get("fontes"))
        for ck in s.get("checks", []):
            print(" ", ck.get("id"), ck["onde"], ck["caminho"], ck["op"], repr(ck.get("valor"))[:120])
        r = core[s["nome"]]
        for c in r["checks"]:
            if not c["ok"]: print("   FAIL:", c["descricao"][:200])
print(len(g["_V392_SPECS"]), "specs")
json.dump({"specs":[s["nome"] for s in g["_V392_SPECS"]]}, open("specs_nomes.json","w"))
