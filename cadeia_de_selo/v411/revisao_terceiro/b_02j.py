import sys, os, json, re
sys.path.insert(0, r"C:\IALD\Central de Patentes\work\cadeia_de_selo\v411")
os.chdir(r"C:\t\k411c\revisao_B")
import guarda_frases_v411 as G
F = r"C:\t\k411c\falso_nos_v411"
tx = open(F + r"\um_absoluto_pt.txt", "rb").read().decode("utf-8").replace("\r\n", "\n")
i = tx.index("O método (forma $=$ conteúdo)")
p = re.match(r"[^\n]+(?:\n(?!\s*\n)[^\n]+)*", tx[i:]).group(0)
for v in G.violacoes(p): print(v)
old = open(r"C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um_absoluto_pt.txt", "rb").read().decode("utf-8").replace("\r\n", "\n")
j = old.index("O método (forma $=$ conteúdo)")
po = re.match(r"[^\n]+(?:\n(?!\s*\n)[^\n]+)*", old[j:]).group(0)
print("old method paragraph also flagged:", [x[0] for x in G.violacoes(po)])
