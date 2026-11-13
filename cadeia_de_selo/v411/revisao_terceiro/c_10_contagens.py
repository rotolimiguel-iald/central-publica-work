import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_lib import *
pairs = [("pos_rito\leitura_v411.py", "pos_rito\leitura_v411.py.bak_20261112_151918_integ"), ("pos_rito\harness_textos_ensaio_v411.py", "pos_rito\harness_textos_ensaio_v411.py.bak_20261112_151918_integ"),
         ("pos_rito\harness_fechar_sandbox_v411.py", "pos_rito\harness_fechar_sandbox_v411.py.bak_20261112_151918_integ"), ("pos_rito\textos_v411.py", "pos_rito\textos_v411.py.bak_20261112_153726"),
         ("p00_precondicoes_v411.py", "p00_precondicoes_v411.py.bak_20261112_152057_integ"), ("pos_rito\blocos_custodia_v411.py", "pos_rito\blocos_custodia_v411.py.bak_20261112_151935_integ")]
pats = {"P.append": r"P\.append\(", "variante(": r"\bvariante\(", "falha(": r"\bfalha\(", "assert": r"\bassert\b", "chk(": r"\bchk\(", "pend(": r"\bpend\(", "raise": r"\braise\b", "sys.exit": r"sys\.exit", "etapa(": r"\betapa\("}
for cur, bak in pairs:
    a = rd(V + "\\" + bak); b = rd(V + "\\" + cur)
    print(cur.split("\\")[-1], {k: (len(re.findall(p, a)), len(re.findall(p, b))) for k, p in pats.items() if len(re.findall(p, a)) or len(re.findall(p, b))})
