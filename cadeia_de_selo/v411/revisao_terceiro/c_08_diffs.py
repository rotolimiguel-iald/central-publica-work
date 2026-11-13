import sys, os, difflib
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_lib import *
pairs = [
 ("pos_rito/leitura_v411.py", "pos_rito/leitura_v411.py.bak_20261112_151918_integ"),
 ("pos_rito/harness_fechar_sandbox_v411.py", "pos_rito/harness_fechar_sandbox_v411.py.bak_20261112_151918_integ"),
 ("pos_rito/harness_textos_ensaio_v411.py", "pos_rito/harness_textos_ensaio_v411.py.bak_20261112_151918_integ"),
 ("pos_rito/blocos_custodia_v411.py", "pos_rito/blocos_custodia_v411.py.bak_20261112_151935_integ"),
 ("cadeia_v411.sh", "cadeia_v411.sh.bak_20261112_152244_integ"),
 ("p00_precondicoes_v411.py", "p00_precondicoes_v411.py.bak_20261112_152057_integ"),
 ("pos_rito/textos_v411.py", "pos_rito/textos_v411.py.bak_20261112_153726"),
 ("pos_rito/textos_v411_novo.pysnip", "pos_rito/textos_v411_novo.pysnip.bak_20261112_153723_integ"),
]
os.makedirs(W + r"\diffs", exist_ok=True)
for cur, bak in pairs:
    a = rd(V + "\\" + bak.replace("/", "\\")).split("\n"); b = rd(V + "\\" + cur.replace("/", "\\")).split("\n")
    d = list(difflib.unified_diff(a, b, "bak", "cur", n=0, lineterm=""))
    out = W + r"\diffs\\" + os.path.basename(cur) + ".diff"
    open(out, "w", encoding="utf-8").write("\n".join(d))
    add = sum(1 for l in d if l.startswith("+") and not l.startswith("+++")); rem = sum(1 for l in d if l.startswith("-") and not l.startswith("---"))
    print(os.path.basename(cur), "+%d -%d" % (add, rem), "bak sha16", sha16(V + "\\" + bak.replace("/", "\\")), "cur", sha16(V + "\\" + cur.replace("/", "\\")))
