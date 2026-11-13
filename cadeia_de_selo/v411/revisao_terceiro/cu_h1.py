"""CU-H1: os MEUS arquivos nao carregam fala: o scan da D181 (cu_b1) sobre cu_*.py, o estado, o registro e as saidas em C:\\t\\k411c\\revisao_CU (exceto os textos extraidos dos PDF, que sao do artigo)."""
import glob, os, sys
src = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "cu_b1.py"), encoding="utf-8").read()
cut = src.index("alvos = {}")
g = {"__name__": "cu_b1_defs"}
so = sys.stdout
sys.stdout = open(os.devnull, "w")
exec(compile(src[:cut], "cu_b1_defs", "exec"), g)
sys.stdout = so
varrer, TOPO_WIN, V = g["varrer"], g["TOPO_WIN"], g["V"]
RT = os.path.join(V, "revisao_terceiro")
fs = sorted(glob.glob(os.path.join(RT, "cu_*.py"))) + [os.path.join(RT, n) for n in ("ESTADO_REVISAO_v411.CU.json", "REVISAO_TERCEIRO_v411.CU.json", "REVISAO_TERCEIRO_v411.CU.md", "REVISAO_TERCEIRO_v411.json", "REVISAO_TERCEIRO_v411.md")]
fs += [p for p in glob.glob(r"C:\t\k411c\revisao_CU\*") if os.path.isfile(p) and not os.path.basename(p).startswith("pdf_")]
tot = 0
for p in fs:
    t = open(p, "rb").read().decode("utf-8", errors="replace")
    r = varrer(os.path.basename(p), t, "", None, TOPO_WIN)
    n = len(r["ocorrencias"]) + len(r["nomes"]) + r["n_janelas_excedentes"]
    tot += n
    if n:
        print("ACHADO em", os.path.basename(p), "| ocorrencias", len(r["ocorrencias"]), "| nomes", len(r["nomes"]), "| janelas", r["n_janelas_excedentes"], [{k: o[k] for k in ("fala", "tipo", "len")} for o in r["ocorrencias"][:3]])
print("arquivos varridos:", len(fs), "| total de achados:", tot)
