import pathlib, re
F = pathlib.Path(r'C:\IALD\Central de Patentes\work\ro106_folhas_27out\fontes')
p = F / 'mqc_folhas.py'
s = p.read_text(encoding='utf-8')
helpers = (F / '_mqc_helpers.txt').read_text(encoding='utf-8')
figs = (F / '_mqc_figs.txt').read_text(encoding='utf-8')
for n in range(2, 8):
    figs = figs.replace('def fig%d():\n' % n, 'def fig%d():\n    OPAQUE.clear()\n' % n)
assert 'CANVAS = {}' in s
s = s.replace('CANVAS = {}', helpers + '\nCANVAS = {}', 1)
a = s.index('# =============================================================== FIGURA 2')
b = s.index('# =============================================================== FIGURA 8')
s = s[:a] + figs + s[b:]
# fig 1: marcadores todos cheios e pretos (forma distingue a categoria), circulos sem fundo
old = "    marc = {'vertice': ('o', 'black', 'black', 110), 'aresta': ('s', 'white', 'black', 95),\n            'face': ('D', 'white', 'black', 105), 'centro': ('*', 'black', 'black', 330)}"
assert old in s
s = s.replace(old, "    marc = {'vertice': ('o', 'black', 'black', 110), 'aresta': ('s', 'black', 'black', 95),\n            'face': ('D', 'black', 'black', 105), 'centro': ('*', 'black', 'black', 330)}")
old2 = "mpatches.Circle((x, y), 1.3, fill=True, facecolor='white', edgecolor='black', linewidth=1.8, zorder=2)"
assert old2 in s
s = s.replace(old2, "mpatches.Circle((x, y), 1.3, fill=False, edgecolor='black', linewidth=1.8, zorder=2)")
p.write_text(s, encoding='utf-8')
print('ok', len(s))
