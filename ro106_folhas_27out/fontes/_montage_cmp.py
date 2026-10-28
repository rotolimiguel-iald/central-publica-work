import numpy as np, fitz
from PIL import Image
W = r'C:\IALD\Central de Patentes\work\ro106_folhas_27out'
filed = fitz.open(W + r'\entrada\mqc\04_DESENHOS_CINZA_como_depositado.pdf')
figs = []
for pg in filed:
    for i in sorted(pg.get_image_info(xrefs=True), key=lambda i: i['bbox'][1]):
        pix = fitz.Pixmap(filed, i['xref'])
        if pix.colorspace is None or pix.colorspace.n != 1:
            pix = fitz.Pixmap(fitz.csGRAY, pix)
        a = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.stride)[:, :pix.width]
        figs.append(a.copy())
def gray_of(path):
    im = Image.open(path).convert('RGBA'); bg = Image.new('RGBA', im.size, (255, 255, 255, 255)); bg.alpha_composite(im)
    return bg.convert('L')
for k, nm in ((5, 'MQC_fig5_correcao_erros'), (7, 'MQC_fig7_comunicacao')):
    f = Image.fromarray(figs[k - 1]); r = gray_of(W + r'\_tmp\mqc_orig\%s.png' % nm)
    w = 1500
    f2 = f.resize((w, int(f.height * w / f.width))); r2 = r.resize((w, int(r.height * w / r.width)))
    canvas = Image.new('L', (w, f2.height + r2.height + 10), 255)
    canvas.paste(f2, (0, 0)); canvas.paste(r2, (0, f2.height + 10))
    canvas.save(W + r'\_tmp\cmp_fig%d.png' % k)
    print(k, f.size, r.size)
