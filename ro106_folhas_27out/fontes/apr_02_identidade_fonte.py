# Prova de identidade da FONTE do Aprendizado: o .tex de origem, compilado sem alteracao,
# reproduz as figuras do PCT como depositado? (correlacao de forma + razao de aspecto, por figura)
import json, hashlib, pathlib
import numpy as np, fitz
from PIL import Image
W = pathlib.Path(r'C:\IALD\Central de Patentes\work\ro106_folhas_27out')
filed = fitz.open(str(W / 'entrada' / 'aprendizado' / '04_DESENHOS_como_depositado.pdf'))
orig = fitz.open(str(W / '_tmp' / 'orig' / 'orig_figs.pdf'))


def gray(pix):
    a = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.stride)[:, :pix.width]
    return a.copy()


def crop_ink(a, thr=245):
    ys, xs = np.where(a < thr)
    return a[ys.min():ys.max() + 1, xs.min():xs.max() + 1]


def norm_corr(a, b):
    a = a.astype(float) - a.mean(); b = b.astype(float) - b.mean()
    return float((a * b).sum() / (np.sqrt((a * a).sum() * (b * b).sum()) + 1e-9))


# figuras do PCT na ordem Fig.1..9
figs_filed = []
for pg in filed:
    infos = sorted(pg.get_image_info(xrefs=True), key=lambda i: i['bbox'][1])
    for i in infos:
        pix = fitz.Pixmap(filed, i['xref'])
        if pix.colorspace is None or pix.colorspace.n != 1:
            pix = fitz.Pixmap(fitz.csGRAY, pix)
        figs_filed.append(gray(pix))
assert len(figs_filed) == 9
res = []
for n in range(9):
    pg = orig[n]
    pix = pg.get_pixmap(dpi=300, colorspace=fitz.csGRAY, alpha=False)
    o = crop_ink(gray(pix))
    f = crop_ink(figs_filed[n])
    ar_o, ar_f = o.shape[1] / o.shape[0], f.shape[1] / f.shape[0]
    # blur-resize both to the same 400 x (400/ar) grid
    H = 300
    W_ = 600
    oi = np.asarray(Image.fromarray(o).resize((W_, H), Image.LANCZOS))
    fi = np.asarray(Image.fromarray(f).resize((W_, H), Image.LANCZOS))
    # 'tinta' = escuro; correlacao das mapas de tinta suavizados
    from scipy import ndimage as ndi
    so = ndi.gaussian_filter(255.0 - oi, 3)
    sf = ndi.gaussian_filter(255.0 - fi, 3)
    res.append({'figura': n + 1, 'aspecto_fonte_compilada': round(ar_o, 3), 'aspecto_PCT_depositado': round(ar_f, 3),
                'razao_aspecto': round(ar_o / ar_f, 3), 'correlacao_mapas_de_tinta': round(norm_corr(so, sf), 3),
                'tinta_fonte_px': list(o.shape[::-1]), 'tinta_PCT_px': list(f.shape[::-1])})
    # prancha lado a lado (fonte compilada | PCT depositado) para conferencia visual
    side = np.concatenate([oi, np.full((H, 10), 255, np.uint8), fi], axis=1)
    Image.fromarray(side).save(W / 'conferencia' / f'apr_identidade_fonte_fig{n + 1}.png')
(W / 'conferencia' / 'apr_identidade_fonte.json').write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding='utf-8')
for r in res:
    print(r)
