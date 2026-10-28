# Compila um .tex de fontes\ com xelatex (sem rede) na pasta _tmp\<nome>[_ALTPHOT]\ e imprime as medidas; opcionalmente renderiza PNG.
# Uso: python compilar.py <nome> [dpi] [ALTPHOT]
import sys, subprocess, pathlib, shutil, re
import fitz
W = pathlib.Path(r'C:\IALD\Central de Patentes\work\ro106_folhas_27out')
name = sys.argv[1]                      # ex.: aprendizado_folhas
dpi = int(sys.argv[2]) if len(sys.argv) > 2 else 0
alt = len(sys.argv) > 3 and sys.argv[3] == 'ALTPHOT'
d = W / '_tmp' / (name + ('_ALTPHOT' if alt else ''))
d.mkdir(parents=True, exist_ok=True)
shutil.copy(W / 'fontes' / f'{name}.tex', d / f'{name}.tex')
main = name
if alt:
    main = name + '_ALTPHOT'
    (d / f'{main}.tex').write_text('\\def\\ALTPHOT{1}\\input{%s}\n' % name, encoding='utf-8')
r = subprocess.run(['xelatex', '--disable-installer', '-interaction=nonstopmode', f'{main}.tex'], cwd=d, capture_output=True, text=True)
log = (d / f'{main}.log').read_text(encoding='utf-8', errors='replace')
for m in re.finditer(r'^! .*$', log, flags=re.M):
    print('ERRO TeX:', m.group(0))
for m in re.finditer(r'\[MEDIDA\].*', log):
    t = m.group(0)

    def conv(x):
        return f'{float(x.group(1)) / 28.4528:.2f}cm'
    t = re.sub(r'([\d.]+)pt', conv, t)
    print(t)
pdf = d / f'{main}.pdf'
print('PDF', pdf.exists(), pdf.stat().st_size if pdf.exists() else 0)
if dpi and pdf.exists():
    doc = fitz.open(str(pdf))
    print('paginas', len(doc))
    for i, p in enumerate(doc):
        p.get_pixmap(dpi=dpi).save(str(d / f'p{i + 1}.png'))
