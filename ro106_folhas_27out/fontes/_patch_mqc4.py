import pathlib
p = pathlib.Path(r'C:\IALD\Central de Patentes\work\ro106_folhas_27out\fontes\mqc_folhas.py')
s = p.read_text(encoding='utf-8')


def rep(a, b, n=1):
    global s
    assert s.count(a) == n, (a, s.count(a))
    s = s.replace(a, b)


i = s.index("    s = s.replace('∇',")
j = s.index("\n", i)
s = s[:i] + "    s = s.replace('∇', '$\\\\nabla$')" + s[j:]
rep("    row_h = [lh * max(len(c.split('\\n')) for c in r) + 0.5 for r in dados]", "    row_h = [lh * max(len(c.split('\\n')) for c in r) + 0.36 for r in dados]")
rep("    hh = 1.0\n", "    hh = 0.95\n")
p.write_text(s, encoding='utf-8')
print([l for l in s.splitlines() if 'nabla' in l])
