import sys, os, json
sys.path.insert(0, r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411")
os.chdir(r"C:\t\k411c\revisao_B")
import guarda_frases_v411 as G
V = r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411"
for nome in ("secao_pt.tex", "secao_en.tex", "quadro_pt.tex", "quadro_en.tex"):
    tx = open(V + r"\amostras_quadro_v411" + "\\" + nome, encoding="utf-8").read()
    print("=====", nome, len(tx))
    for i, ln in enumerate(tx.splitlines()):
        v = G.violacoes(ln)
        if "contra o nulo" in ln or "against the null" in ln:
            print(i, "len", len(ln), "viol:", [x[0] for x in v], "|", ln[:90].replace("\n", " "))
# direct probes of the hole
probes = [
 r"\textbf{O esperado pelos agregados, ao lado do observado ($Z$ contra o nulo).} primario\_publicado: esperado $5{,}83$, observado $6{,}11$.",
 r"\textbf{Os estresses} Z contra o nulo $6{,}09$ e $4{,}37$.",
 "O Z contra o nulo do teste lê 6,11 contra o nulo.",
 "$Z$ contra o nulo $=6{,}11$ no H0DN",
 "Z contra o nulo = 6,11 no H0DN",
 "the primary Z against the null is 6.11 in H0DN",
 "$Z$ against the null $=6.11$ in H0DN",
]
for p in probes: print(repr(p[:70]), "->", [x[0] for x in G.violacoes(p)])
