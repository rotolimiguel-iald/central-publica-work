from b_lib import *
import re, runpy
exec(open("b_01_topo.py", encoding="utf-8").read().split("t = pt(); e = en()")[0])
t = pt(); e = en()
rp = t[t.index("Dois resultados abrem"):t.index("Apresentação do programa terminal")]
i = e.index("Two results open"); re_ = e[i:e.index("Presentation of the TGL terminal program")]
num = lambda s: re.findall(r"(?:\$-\$|−|-)?\d+(?:[.,]\d+)?", s)
n_rp = [x.replace("$-$","-").replace("−","-") for x in num(rp)]
n_ep = [x.replace("$-$","-").replace("−","-") for x in num(exp_pt)]
print("PT nums render :", n_rp)
print("PT nums esperado:", n_ep)
print("iguais", n_rp == n_ep)
n_re = [x.replace("$-$","-").replace("−","-") for x in num(re_)]
n_ee = [x.replace("$-$","-").replace("−","-") for x in num(exp_en)]
print("EN nums render :", n_re)
print("EN nums esperado:", n_ee)
print("iguais", n_re == n_ee)
# word-level diff (tokens) to detect extra/missing words
def toks(s):
    s = s.replace("$-$","-")
    return re.findall(r"[\wβασΛδ√]+|[−\-]?\d+", s, flags=re.U)
import difflib
tp = toks(rp); te = toks(exp_pt)
sm = difflib.SequenceMatcher(a=tp, b=te, autojunk=False)
print("PT token diff ops:", [(o, tp[a1:a2], te[b1:b2]) for o,a1,a2,b1,b2 in sm.get_opcodes() if o != "equal"][:30])
tp = toks(re_); te = toks(exp_en)
sm = difflib.SequenceMatcher(a=tp, b=te, autojunk=False)
print("EN token diff ops:", [(o, tp[a1:a2], te[b1:b2]) for o,a1,a2,b1,b2 in sm.get_opcodes() if o != "equal"][:30])
