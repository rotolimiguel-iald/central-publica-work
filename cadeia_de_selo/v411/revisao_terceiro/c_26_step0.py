import sys, os, re
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from c_lib import *
sh = rd(V + r"\pos_rito\chain_pos_rito_v411.sh").split("\n")
i = next(k for k, l in enumerate(sh) if l.startswith('for f in "$TOOLS/arvore_da_prova.py"'))
blk = []
k = i
while True:
    blk.append(sh[k]); 
    if "; do" in sh[k]: break
    k += 1
txt = " ".join(blk)
toks = re.findall(r'"([^"]+)"', txt)
env = {"TOOLS": "/c/IALD/Central de Patentes/work/cadeia_de_selo", "PK": "/c/IALD/Central de Patentes/work/cadeia_de_selo/v411", "NOS": "/c/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós",
       "PORTA": "/c/LAR_MIGUEL/porta_memoria.py", "HAJA": "/c/IALD/Artigo/Haja_Luz/CLAUDE.md", "INV": "/c/IALD/Central de Patentes/work/inventario_bancada"}
env["SEL"] = env["PK"] + "/pos_rito"; env["FILA"] = env["SEL"] + "/fila_memoria_v411.py"
def winp(p):
    return re.sub(r"^/c/", "C:\\\\", p).replace("/", "\\") if p.startswith("/c/") else p
print("linha do chain:", i + 1, "| itens:", len(toks))
faltam = []
for t in toks:
    p = t
    for kk, vv in env.items(): p = p.replace("$" + kk, vv)
    wp = winp(p)
    # o NOS ainda e' a v410 ate' o rito: o selo_acom existe da v410
    if not os.path.isfile(wp): faltam.append(wp)
print("FALTAM (existencia hoje):", faltam)
# o passo 1 copia runtime_v411.py
j = next(k for k, l in enumerate(sh) if l.startswith("for q in conferir_rito_v411.py"))
print("passo 1 (linha %d):" % (j + 1), sh[j][:200])
print("existe runtime_v411.py no pacote:", os.path.exists(V + r"\runtime_v411.py"), "| existe em v410:", os.path.exists(V + r"\..\v410\runtime_v410.py"))
# quem mais cita runtime_v411.py como arquivo a existir
import glob
for f in ("conferir_rito_v411.py", "delta_v411.py", "pos_rito/leitura_v411.py", "pos_rito/fechar_v411.py", "orquestrador/pos_treino_v411.py", "p00_precondicoes_v411.py", "gerar_relatorio_v411.py", "instalar_v411.py"):
    t = rd(V + "\\" + f.replace("/", "\\"))
    n = len(re.findall(r"runtime_v411\.py", t))
    if n: print("cita runtime_v411.py:", f, n)
