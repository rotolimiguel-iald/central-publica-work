import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_lib import *
for nome in ("conferencia_rito_v411_POSITIVO_FALSO_NOS.json", "conferencia_rito_v411_CONTROLE_NEGATIVO_PRE_RITO.json"):
    j = json.load(open(V + "\\" + nome, encoding="utf-8"))
    print("==", nome, "tudo_bate:", j.get("tudo_bate"), "chaves:", list(j)[:14])
    for sec in ("deve_mudar", "nao_pode_mudar"):
        d = j[sec]; n = len(d); t = sum(1 for v in d.values() if v is True); f = [k for k, v in d.items() if v is not True]
        print(" ", sec, n, "True:", t, "nao-True:", len(f))
        if "NEGATIVO" in nome:
            for k in f[:100]:
                print("     F:", k[:110])
j = json.load(open(V + r"\conferencia_rito_v411_POSITIVO_FALSO_NOS.json", encoding="utf-8"))
print("--- itens NAO (nao_pode_mudar) no positivo:")
for k, v in j["nao_pode_mudar"].items():
    print("  ", v, k[:170])
