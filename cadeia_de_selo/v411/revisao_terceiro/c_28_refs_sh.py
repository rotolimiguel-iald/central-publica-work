import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_lib import *
P = V.replace("\\", "/")
env = {"PK": P, "SEL": P + "/pos_rito", "TOOLS": "C:/IALD/Central de Patentes/work/cadeia_de_selo", "INV": "C:/IALD/Central de Patentes/work/inventario_bancada",
       "NOS": "C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós", "ATLD": "C:/IALD/Central de Patentes/memory", "UMEM": "C:/Users/rotol/.claude/projects/c--IALD-Central-de-Patentes/memory"}
alvos = ["pos_rito/chain_pos_rito_v411.sh", "rito_v411.sh", "cadeia_v411.sh", "fim_de_cadeia_v411.sh"]
pat = re.compile(r"\$\{?(PK|SEL|TOOLS|INV|NOS|ATLD|UMEM)\}?/([A-Za-z0-9_./\-]+)")
visto = {}
for a in alvos:
    t = rd(P + "/" + a)
    for ln, l in enumerate(t.split("\n"), 1):
        if l.lstrip().startswith("#"):
            continue
        for m in pat.finditer(l):
            var, rel = m.group(1), m.group(2)
            full = env[var] + "/" + rel
            visto.setdefault(full, []).append("%s:%d" % (os.path.basename(a), ln))
ausentes = {k: v for k, v in visto.items() if not os.path.exists(k)}
print("referencias distintas:", len(visto), "| ausentes hoje:", len(ausentes))
for k, v in sorted(ausentes.items()):
    print("  ", k.replace(P, "$PK"), "<-", v[:3])
