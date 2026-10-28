# Regenera, com o script de origem SEM alteracao, as 8 figuras do MQC e compara com
# (i) os PNG originais de 11/02/2026 e (ii) as imagens embutidas no PCT como depositado (04_DESENHOS_CINZA.pdf).
import os, sys, json, pathlib, importlib.util, hashlib
import numpy as np, fitz
from PIL import Image
from scipy import ndimage as ndi
W = pathlib.Path(r'C:\IALD\Central de Patentes\work\ro106_folhas_27out')
tmp = W / '_tmp' / 'mqc_orig'
tmp.mkdir(parents=True, exist_ok=True)
os.chdir(tmp)
spec = importlib.util.spec_from_file_location('mqcsim', str(W / 'entrada' / 'mqc' / 'mqc_simulacao_celula_elementar.py'))
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)
import matplotlib
print('matplotlib', matplotlib.__version__)
m.gerar_figura_1_topologia()
m.gerar_figura_2_estabilizacao()
m.gerar_figura_3_termodinamica()
m.gerar_figura_4_translacao()
m.gerar_figura_5_correcao_erros()
m.gerar_figura_6_convergencia()
m.gerar_figura_7_comunicacao()
m.gerar_figura_8_correspondencia()
names = ['MQC_fig1_topologia', 'MQC_fig2_estabilizacao', 'MQC_fig3_termodinamica', 'MQC_fig4_translacao',
         'MQC_fig5_correcao_erros', 'MQC_fig6_convergencia', 'MQC_fig7_comunicacao', 'MQC_fig8_correspondencia']
filed = fitz.open(str(W / 'entrada' / 'mqc' / '04_DESENHOS_CINZA_como_depositado.pdf'))
figs_filed = []
for pg in filed:
    for i in sorted(pg.get_image_info(xrefs=True), key=lambda i: i['bbox'][1]):
        pix = fitz.Pixmap(filed, i['xref'])
        if pix.colorspace is None or pix.colorspace.n != 1:
            pix = fitz.Pixmap(fitz.csGRAY, pix)
        a = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.stride)[:, :pix.width]
        figs_filed.append((a.copy(), i['bbox']))
assert len(figs_filed) == 8


def gray_of(path):
    im = Image.open(path).convert('RGBA')
    bg = Image.new('RGBA', im.size, (255, 255, 255, 255))
    bg.alpha_composite(im)
    return np.asarray(bg.convert('L'))


def crop_ink(a, thr=245):
    ys, xs = np.where(a < thr)
    return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def ncc(a, b):
    a = a.astype(float) - a.mean(); b = b.astype(float) - b.mean()
    return float((a * b).sum() / (np.sqrt((a * a).sum() * (b * b).sum()) + 1e-9))


def alinhar(png_gray, filed_gray, sc=8):
    """O PCT traz o PNG sem a faixa do suptitulo (topo) e sem margem: procura o deslocamento (dx,dy) que maximiza a correlacao."""
    H, Wd = filed_gray.shape
    Hp, Wp = png_gray.shape
    f_small = np.asarray(Image.fromarray(filed_gray).resize((Wd // sc, H // sc), Image.BILINEAR)).astype(float)
    best = (-2, None)
    # reescala do PNG para a mesma escala px/px do embutido (mesma largura -> escala ~1)
    p_small = np.asarray(Image.fromarray(png_gray).resize((Wp // sc, Hp // sc), Image.BILINEAR)).astype(float)
    fh, fw = f_small.shape
    for dy in range(0, max(1, p_small.shape[0] - fh + 1)):
        for dx in range(0, max(1, p_small.shape[1] - fw + 1)):
            crop = p_small[dy:dy + fh, dx:dx + fw]
            if crop.shape != f_small.shape:
                continue
            c = ncc(255 - crop, 255 - f_small)
            if c > best[0]:
                best = (c, (dx * sc, dy * sc))
    return round(best[0], 4), best[1]


res = []
for k, nm in enumerate(names):
    regen = gray_of(tmp / f'{nm}.png')
    orig = gray_of(W / 'entrada' / 'mqc' / 'png_originais_11fev' / f'{nm}.png')
    fl = figs_filed[k][0]
    rc, oc, fc = crop_ink(regen), crop_ink(orig), crop_ink(fl)
    def cmp(a, b):
        H, Wd = 320, 640
        ai = np.asarray(Image.fromarray(a).resize((Wd, H), Image.LANCZOS))
        bi = np.asarray(Image.fromarray(b).resize((Wd, H), Image.LANCZOS))
        return round(ncc(ndi.gaussian_filter(255.0 - ai, 2), ndi.gaussian_filter(255.0 - bi, 2)), 4)
    r = {'figura': k + 1, 'regenerado_px': list(regen.shape[::-1]), 'png_11fev_px': list(orig.shape[::-1]), 'embutido_no_PCT_px': list(fl.shape[::-1]),
         'corr_regenerado_vs_png11fev': cmp(rc, oc), 'corr_png11fev_vs_PCT': cmp(oc, fc), 'corr_regenerado_vs_PCT': cmp(rc, fc),
         'corr_alinhada_regenerado_vs_PCT(deslocamento_px)': alinhar(regen, fl), 'corr_alinhada_png11fev_vs_PCT(deslocamento_px)': alinhar(orig, fl), 'png_identico_byte_a_byte': hashlib.sha256((tmp / f'{nm}.png').read_bytes()).hexdigest() == hashlib.sha256((W / 'entrada' / 'mqc' / 'png_originais_11fev' / f'{nm}.png').read_bytes()).hexdigest()}
    res.append(r)
    print(r)
(W / 'conferencia' / 'mqc_identidade_fonte.json').write_text(json.dumps({'matplotlib': matplotlib.__version__, 'itens': res}, indent=1, ensure_ascii=False), encoding='utf-8')
