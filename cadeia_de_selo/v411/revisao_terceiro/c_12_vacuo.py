import sys, os, re, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_lib import *
E = json.load(open(V + r"\ESPERADOS_v411.json", encoding="utf-8"))
src = rd(V + r"\conferir_rito_v411.py")
keys = sorted(set(re.findall(r'\bin\s+(?:sorted\()?ESP\["([A-Za-z0-9_]+)"\]', src)))
print("colecoes iteradas em all/any sobre ESP:", len(keys))
for k in keys:
    v = E.get(k, "AUSENTE")
    n = len(v) if hasattr(v, "__len__") else v
    flag = "  <<< VAZIA/AUSENTE" if (v == "AUSENTE" or n == 0) else ""
    print("  ", k, n, flag)
for nm in ("registros_v399", "registros_v401", "registros_v402", "registros_v403", "registros_v404", "registros_v405", "registros_v406", "registros_v407", "registros_v408", "registros_v409", "registros_v410", "registros_v411"):
    print(nm, len(E.get(nm, {})))
# 'all(' sobre iteraveis que nao sao ESP: listar quantos all( existem no arquivo
print("all( no arquivo:", len(re.findall(r"\ball\(", src)), "any(:", len(re.findall(r"\bany\(", src)))
# padroes de aceitar ausencia: 'if os.path.exists(...) else ...True'
for m in re.finditer(r"os\.path\.exists\([^)]*\)\s*(?:and|or)[^\n]{0,120}", src):
    ln = src[:m.start()].count("\n") + 1
    pass
print("exists() ocorrencias:", len(re.findall(r"os\.path\.exists", src)))
