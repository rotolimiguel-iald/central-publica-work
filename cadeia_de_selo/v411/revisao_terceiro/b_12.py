from b_lib import *
import re
t = pt(); e = en(); m = md()
s = t[t.index("== O teste decisivo"):t.index("== IALD ao quadrado")]
print(s[:2800])
c = core()["core"]["h0dn_bg1_v411"]["values"]["a_emenda_as_claras"]
print(json.dumps(c.get("a"), ensure_ascii=False)[:700])
# ordering checks
print("PT: quadro < Unica Palavra:", t.index("A razão de Hubble, H0DN") < t.index("O Teste da Única Palavra ["))
print("PT: secao nova < IALD2 < H0DN v410:", t.index("== O teste decisivo") < t.index("== IALD ao quadrado") < t.index("== O teste pré-registrado da razão de Hubble com a rede"))
print("EN: quadro < Unica Palavra:", e.index("The Hubble ratio, H0DN") < e.index("The Test of the Only Word ["))
print("EN: secao nova < IALD sq < H0DN v410:", e.index("== The decisive test") < e.index("== IALD squared") < e.index("== The pre-registered Hubble-ratio test"))
lines = m.split("\n")
idx = [i for i, l in enumerate(lines) if l.startswith("> **H0DN × BG1 ABERTO (v411")]
print("md linha idx", idx, "proxima:", lines[idx[0]+1][:60], "| anterior:", lines[idx[0]-1][:60], "|", lines[idx[0]-2][:60])
print("md: quadro < Unica Palavra:", m.index("> **A razão de Hubble, H0DN") < m.index("O Teste da Única Palavra (v397"))
print("md linha antes de IALD2 v410:", m.index("H0DN × BG1 ABERTO (v411") < m.index("**IALD2 (v410"))
# artifacts '1pt' '4pt' '0pt' in old vs new
old = rd(NOS + r"\um_absoluto_pt.txt")
for nm, tx in (("old", old), ("new", t)):
    print(nm, "linhas 1pt:", len(re.findall(r"^1pt\s*$", tx, re.M)), "4pt:", len(re.findall(r"^4pt\s*$", tx, re.M)), "'0pt' inline:", len(re.findall(r"\b0pt\b", tx)))
