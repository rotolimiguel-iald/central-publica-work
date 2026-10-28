# Extrai, POR SCRIPT, o preambulo e os 9 tikzpicture do .tex de origem (Psion_Engine_PI_INPI.tex)
# e compila-os sem alteracao (uma figura por pagina) para a prova de identidade com o PCT como depositado.
import re, subprocess, pathlib
W = pathlib.Path(r'C:\IALD\Central de Patentes\work\ro106_folhas_27out')
src = (W / 'entrada' / 'aprendizado' / 'Psion_Engine_PI_INPI.tex').read_text(encoding='utf-8')
pre = src.split('\\begin{document}')[0]
# so a geometria da pagina muda (nao afeta as figuras)
pre = re.sub(r'\\geometry\{[^}]*\}', lambda m: '\\geometry{a4paper,margin=1cm}', pre)
body = src.split('\\begin{document}')[1]
figs = re.findall(r'\\begin\{figure\}\[H\]\s*\\centering\s*(\\begin\{tikzpicture\}.*?\\end\{tikzpicture\})', body, flags=re.S)
assert len(figs) == 9, len(figs)
parts = ['\\begin{figure}[H]\n\\centering\n' + f + '\n\\end{figure}' for f in figs]
out = pre + '\\begin{document}\n\\pagestyle{empty}\n' + '\n\\clearpage\n'.join(parts) + '\n\\end{document}\n'
d = W / '_tmp' / 'orig'
d.mkdir(parents=True, exist_ok=True)
(d / 'orig_figs.tex').write_text(out, encoding='utf-8')
r = subprocess.run(['pdflatex', '--disable-installer', '-interaction=nonstopmode', 'orig_figs.tex'],
                   cwd=d, capture_output=True, text=True)
print(r.stdout[-500:])
print('rc', r.returncode)
