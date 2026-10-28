import glob, hashlib, os, collections, json
import numpy as np, fitz
from PIL import Image
base = r'C:\IALD\Central de Patentes\patents\BR102026003460-6_MQC'
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
    im = Image.open(path).convert('RGBA')
    bg = Image.new('RGBA', im.size, (255, 255, 255, 255))
    bg.alpha_composite(im)
    return np.asarray(bg.convert('L'))


def ncc(a, b):
    a = a.astype(float) - a.mean(); b = b.astype(float) - b.mean()
    return float((a * b).sum() / (np.sqrt((a * a).sum() * (b * b).sum()) + 1e-9))


def alinhar(png_gray, filed_gray, sc=8):
    H, Wd = filed_gray.shape
    Hp, Wp = png_gray.shape
    f_small = np.asarray(Image.fromarray(filed_gray).resize((Wd // sc, H // sc), Image.BILINEAR)).astype(float)
    p_small = np.asarray(Image.fromarray(png_gray).resize((Wp // sc, Hp // sc), Image.BILINEAR)).astype(float)
    fh, fw = f_small.shape
    best = (-2, None)
    for dy in range(0, max(1, p_small.shape[0] - fh + 1)):
        for dx in range(0, max(1, p_small.shape[1] - fw + 1)):
            crop = p_small[dy:dy + fh, dx:dx + fw]
            if crop.shape != f_small.shape:
                continue
            c = ncc(255 - crop, 255 - f_small)
            if c > best[0]:
                best = (c, (dx * sc, dy * sc))
    return round(best[0], 4), best[1]


names = ['MQC_fig1_topologia', 'MQC_fig2_estabilizacao', 'MQC_fig3_termodinamica', 'MQC_fig4_translacao',
         'MQC_fig5_correcao_erros', 'MQC_fig6_convergencia', 'MQC_fig7_comunicacao', 'MQC_fig8_correspondencia']
out = {}
for k in (4, 6):   # figs 5 e 7
    nm = names[k]
    groups = collections.defaultdict(list)
    for f in sorted(glob.glob(base + r'\results\*\figures\%s.png' % nm)):
        h = hashlib.sha256(open(f, 'rb').read()).hexdigest()[:12]
        groups[h].append(f.split('\\')[-3])
    print(nm, len(groups), 'versoes distintas')
    for h, runs in groups.items():
        f = base + r'\results\%s\figures\%s.png' % (runs[0], nm)
        c = alinhar(gray_of(f), figs[k])
        print('  ', h, runs[0], '...', runs[-1], len(runs), 'corr_alinhada_vs_PCT', c)
        out.setdefault(nm, []).append({'sha12': h, 'primeira_corrida': runs[0], 'n': len(runs), 'corr': c})
json.dump(out, open(W + r'\conferencia\mqc_fig5_fig7_candidatos.json', 'w'), indent=1)
