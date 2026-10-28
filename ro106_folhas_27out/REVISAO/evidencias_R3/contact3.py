import fitz, numpy as np
from scipy import ndimage

W = r"C:\IALD\Central de Patentes\work\ro106_folhas_27out"
files = {
    "main_R3": W + r"\FOLHAS_SUBSTITUTIVAS_050576.pdf",
    "variante_PHOT_R3": W + r"\FOLHAS_SUBSTITUTIVAS_050576_VARIANTE_PHOT.pdf",
    "alt_f1_R3": W + r"\ALTERNATIVA_FOLHA_1_050576_PHOT.pdf",
    "main_R2_backup": W + r"\FOLHAS_SUBSTITUTIVAS_050576.pdf.bak_20261027_103927",
    "mqc_frozen": W + r"\FOLHAS_SUBSTITUTIVAS_050579.pdf",
}
dpi = 600
sc = dpi / 72
for k, p in files.items():
    O = fitz.open(p)
    T = fitz.open(p)
    G = fitz.open(p)
    for pg in T:
        pg.add_redact_annot(pg.rect)
        pg.apply_redactions(images=0, graphics=fitz.PDF_REDACT_LINE_ART_REMOVE_IF_TOUCHED, text=fitz.PDF_REDACT_TEXT_NONE)
    for pg in G:
        pg.add_redact_annot(pg.rect)
        pg.apply_redactions(images=0, graphics=fitz.PDF_REDACT_LINE_ART_NONE, text=fitz.PDF_REDACT_TEXT_REMOVE)
    rep = []
    near_rep = []
    for i in range(len(O)):
        t = T[i].get_pixmap(dpi=dpi, colorspace=fitz.csGRAY)
        g = G[i].get_pixmap(dpi=dpi, colorspace=fitz.csGRAY)
        Tm = np.frombuffer(t.samples, dtype=np.uint8).reshape(t.h, t.w) < 128
        Gm = np.frombuffer(g.samples, dtype=np.uint8).reshape(g.h, g.w) < 128
        both = Tm & Gm
        lab, n = ndimage.label(ndimage.binary_dilation(both, iterations=6))
        words = O[i].get_text("words")
        for j, sl in enumerate(ndimage.find_objects(lab)):
            cnt = int(both[sl].sum())
            cy = (sl[0].start + sl[0].stop) / 2 / sc
            cx = (sl[1].start + sl[1].stop) / 2 / sc
            near = [w[4] for w in words if w[0] - 3 <= cx <= w[2] + 3 and w[1] - 3 <= cy <= w[3] + 3]
            if near and all(x.startswith("√") or x.endswith("√e") or x == "√e" or x.startswith("(√") for x in near):
                continue  # radical rule belongs to the glyph
            rep.append((i + 1, cnt, near[:2]))
        # nearest distance word-ink to graphics-ink (mm) for sheet 2 words
        if i == 1 and k.startswith(("main", "variante")):
            dist = ndimage.distance_transform_edt(~Gm)
            for w in words:
                x0, y0, x1, y1, txt = w[:5]
                xs0, xs1, ys0, ys1 = int(x0 * sc) - 1, int(x1 * sc) + 1, int(y0 * sc) - 1, int(y1 * sc) + 1
                sub = Tm[ys0:ys1, xs0:xs1]
                if not sub.any():
                    continue
                dd = dist[ys0:ys1, xs0:xs1][sub]
                near_rep.append((txt, round(float(dd.min()) / dpi * 25.4, 3)))
    print(k, "sheets", len(O), "| text/graphics ink coincidences (radical rules excluded):", rep)
    if near_rep:
        near_rep.sort(key=lambda t: t[1])
        print("    sheet 2 closest word-ink to any stroke (mm):", near_rep[:6])
