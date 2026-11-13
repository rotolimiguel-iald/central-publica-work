from b_lib import *
import re
t = pt()
print(t[203100:204300])
print("======= seção 'estatuto' fora de v411 com 5σ pendente:")
for mm in re.finditer(r"(?:segue|seguem|fica|ficam|resta|restam|permanece|aguarda|espera)[^.]{0,80}5\$?σ|5\$?σ[^.]{0,60}(?:segue|aguarda|espera|pendente)|pendente[^.]{0,40}5\$?σ|elo pendente", t):
    s = mm.start(); print(s, "|", t[max(0, s-120): s+160].replace("\r\n", " "))
