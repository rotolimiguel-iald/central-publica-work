import fitz, numpy as np
from scipy import ndimage
W=r"C:\IALD\Central de Patentes\work\ro106_folhas_27out"
files={"apr":W+r"\FOLHAS_SUBSTITUTIVAS_050576.pdf","aprALT":W+r"\ALTERNATIVA_FOLHA_1_050576_PHOT.pdf","mqc":W+r"\FOLHAS_SUBSTITUTIVAS_050579.pdf","apr_R1":W+r"\FOLHAS_SUBSTITUTIVAS_050576.pdf.bak_20261027_094406","mqc_R1":W+r"\FOLHAS_SUBSTITUTIVAS_050579.pdf.bak_20261027_094406"}
dpi=600; sc=dpi/72
for k,p in files.items():
    O=fitz.open(p); T=fitz.open(p); G=fitz.open(p); tot=0; rep=[]
    for pg in T:
        pg.add_redact_annot(pg.rect); pg.apply_redactions(images=0,graphics=fitz.PDF_REDACT_LINE_ART_REMOVE_IF_TOUCHED,text=fitz.PDF_REDACT_TEXT_NONE)
    for pg in G:
        pg.add_redact_annot(pg.rect); pg.apply_redactions(images=0,graphics=fitz.PDF_REDACT_LINE_ART_NONE,text=fitz.PDF_REDACT_TEXT_REMOVE)
    for i in range(len(O)):
        t=T[i].get_pixmap(dpi=dpi,colorspace=fitz.csGRAY); g=G[i].get_pixmap(dpi=dpi,colorspace=fitz.csGRAY)
        Tm=np.frombuffer(t.samples,dtype=np.uint8).reshape(t.h,t.w)<128; Gm=np.frombuffer(g.samples,dtype=np.uint8).reshape(g.h,g.w)<128
        both=Tm&Gm
        lab,n=ndimage.label(ndimage.binary_dilation(both,iterations=6))
        words=O[i].get_text("words")
        for j,sl in enumerate(ndimage.find_objects(lab)):
            cnt=int(both[sl].sum()); cy=(sl[0].start+sl[0].stop)/2/sc; cx=(sl[1].start+sl[1].stop)/2/sc
            near=[w[4] for w in words if w[0]-3<=cx<=w[2]+3 and w[1]-3<=cy<=w[3]+3]
            if near and all(x.startswith("√") or x.endswith("√e") or x=="√e" or x.startswith("(√") for x in near): continue  # radical rule belongs to the glyph
            rep.append((i+1,cnt,near[:2]))
    print(k,"sheets with text/graphics ink coincidence (radical rules excluded):",rep)
