from b_lib import *
import re
t = pt(); e = en(); m = md(); o = out()
def decs(s):
    s = s.replace("$-$", "-").replace("−", "-").replace("{,}", ".")
    return [x.replace(",", ".") for x in re.findall(r"(?<![\w.])-?\d+[.,]\d+", s)]
q_pt = t[t.index("A razão de Hubble, H0DN"):t.index("O Teste da Única Palavra [")]
q_en = e[e.index("The Hubble ratio, H0DN"):e.index("The Test of the Only Word [")]
i = m.index("> **A razão de Hubble, H0DN"); j = m.index("\n\n", i); q_md = m[i:j]
print("md quadro len", len(q_md))
d_pt, d_en, d_md = decs(q_pt), decs(q_en), decs(q_md)
print("PT", d_pt); print("EN", d_en); print("MD", d_md)
print("PT==EN", d_pt == d_en, " PT==MD", d_pt == d_md)
s_pt = t[t.index("== O teste decisivo"):t.index("== IALD ao quadrado")]
s_en = e[e.index("== The decisive test"):e.index("== IALD squared")]
print("secao PT==EN:", decs(s_pt) == decs(s_en))
# stdout numbers (full precision) vs quadro (rounded)
blk = o[o.index("H0DN x BG1 ABERTO"):][:1500]
nums = [float(x) for x in re.findall(r"-?\d+\.\d{6,}", blk)]
print("stdout:", nums, "-> rounded 2:", ["%.2f" % x for x in nums])
# the linha do md
k = m.index("**H0DN × BG1 ABERTO (v411"); print(m[k:k+1100].split("\n")[0][:900])
