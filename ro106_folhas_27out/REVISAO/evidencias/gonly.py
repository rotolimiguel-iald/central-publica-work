import fitz
W=r"C:\IALD\Central de Patentes\work\ro106_folhas_27out"
for n in ("050576","050579"):
    d=fitz.open(W+"\FOLHAS_SUBSTITUTIVAS_"+n+".pdf")
    for pg in d:
        pg.add_redact_annot(pg.rect)
        pg.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE, graphics=fitz.PDF_REDACT_LINE_ART_NONE, text=fitz.PDF_REDACT_TEXT_REMOVE)
    d.save(f"gonly_{n}.pdf")
    t=fitz.open(f"gonly_{n}.pdf")
    print(n,[ (len(p.get_drawings()),len(p.get_text("words"))) for p in t])
