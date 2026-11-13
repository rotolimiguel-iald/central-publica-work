from b_lib import *
t = pt(); e = en()
def ln(tx, off): return tx.count("\n", 0, off) + 1
print("PT", {k: ln(t, k) for k in (25130, 25493, 61200, 62122, 59473, 13604, 19838, 203923, 4565, 24649, 22479, 241008, 14523)})
print("EN", {k: ln(e, k) for k in (26480, 26859, 66313, 67306, 64528, 14151, 20564, 261585, 4748, 25954, 23689, 15106)})
m = md(); print("MD", ln(m, 258), ln(m, 20324), ln(m, m.index("> **H0DN × BG1 pré-registrado (v410")), ln(m, m.index("esta versão roda sem o resultado")))
