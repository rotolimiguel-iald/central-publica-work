# Pranchas de conferencia visual: linha de cima = folhas COMO DEPOSITADAS; linha de baixo = FOLHAS SUBSTITUTIVAS (mesma escala).
import pathlib
import fitz
from PIL import Image, ImageDraw
W = pathlib.Path(r'C:\IALD\Central de Patentes\work\ro106_folhas_27out')
DPI = 45
import sys
for k, filed in [x for x in (('050576', W / 'entrada/aprendizado/04_DESENHOS_como_depositado.pdf'), ('050579', W / 'entrada/mqc/04_DESENHOS_CINZA_como_depositado.pdf')) if x[0] in sys.argv[1:]]:
    rows = []
    for pdf in (filed, W / f'FOLHAS_SUBSTITUTIVAS_{k}.pdf'):
        d = fitz.open(str(pdf))
        ims = []
        for p in d:
            pix = p.get_pixmap(dpi=DPI, colorspace=fitz.csRGB, alpha=False)
            ims.append(Image.frombytes('RGB', (pix.width, pix.height), pix.samples))
        rows.append(ims)
    n = max(len(r) for r in rows)
    w, h = rows[0][0].size
    pad = 6
    canvas = Image.new('RGB', (n * (w + pad) + pad, 2 * (h + 24) + pad), (255, 255, 255))
    dr = ImageDraw.Draw(canvas)
    for r, ims in enumerate(rows):
        for i, im in enumerate(ims):
            x = pad + i * (w + pad)
            y = pad + r * (h + 24) + 18
            canvas.paste(im, (x, y))
            dr.rectangle([x - 1, y - 1, x + w, y + h], outline=(90, 90, 90))
        dr.text((pad, pad + r * (h + 24)), 'COMO DEPOSITADO (%d folhas)' % len(ims) if r == 0 else 'FOLHAS SUBSTITUTIVAS (%d folhas)' % len(ims), fill=(0, 0, 0))
    out = W / 'conferencia' / f'prancha_antes_depois_{k}.png'
    canvas.save(out)
    print(out, canvas.size)
