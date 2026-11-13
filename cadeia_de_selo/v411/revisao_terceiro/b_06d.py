from b_lib import *
import re
t = pt()
for m in re.finditer(r"livro de cobran[çc]as", t):
    pass
idx = [m.start() for m in re.finditer(r"livro de cobran[çc]as", t)]
print(len(idx), idx[:40])
hs = [(m.start(), m.group(0).strip()) for m in re.finditer(r"^== .*==\s*$", t, re.M)]
# find heading containing 'estresse' or 'cobran'
for p, h in hs:
    if re.search(r"estresse|cobran|livro|testes", h, re.I): print(p, h[:140])
