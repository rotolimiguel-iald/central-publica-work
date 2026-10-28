import pathlib
p = pathlib.Path(r'C:\IALD\Central de Patentes\work\ro106_folhas_27out\fontes\mqc_folhas.py')
s = p.read_text(encoding='utf-8')


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a, s.count(a))
    s = s.replace(a, b)


rep("        top = 3.75 * PT", "        top = 3.6 * PT")
rep("    Wc, Hc = 25.0, 15.9\n", "    Wc, Hc = 25.0, 16.4\n")
rep("    lh = 0.64            # cm por linha de texto", "    lh = 0.72            # cm por linha de texto")
rep("+ 0.36 for r in dados]", "+ 0.32 for r in dados]")
rep("ha='center', va='center', fontsize=FS, linespacing=1.2)", "ha='center', va='center', fontsize=FS, linespacing=1.38)")
p.write_text(s, encoding='utf-8')
print('ok')
