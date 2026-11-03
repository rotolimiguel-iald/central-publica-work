# -*- coding: utf-8 -*-
# C1/C2/C6: extracao de texto dos PDFs (aceitos e finais) por PyMuPDF e por pdftotext (controle cruzado).
# Somente leitura sobre K; escreve apenas em REVISAO/evidencias_FINAIS.
import json, pathlib, subprocess, re, unicodedata
import fitz

K = pathlib.Path("C:/IALD/Central de Patentes/work/ro106_folhas_27out")
E = K / "REVISAO" / "evidencias_FINAIS"
PDFS = {
    "576_aceita": "CARTA_REGRA_26_4_050576.pdf",
    "576_final": "CARTA_REGRA_26_4_050576_FINAL.pdf",
    "579_aceita": "CARTA_REGRA_26_4_050579.pdf",
    "579_final": "CARTA_REGRA_26_4_050579_FINAL.pdf",
}
info = {}
for tag, nome in PDFS.items():
    p = K / nome
    d = fitz.open(p)
    pags = [pg.get_text("text") for pg in d]
    (E / f"txt_{tag}.fitz.txt").write_text("\n\f\n".join(pags), encoding="utf-8")
    # pdftotext (poppler) como segundo extrator, modo bruto de fluxo (-raw) e padrao
    r = subprocess.run(["pdftotext", "-enc", "UTF-8", "-raw", str(p), "-"], capture_output=True)
    raw = r.stdout.decode("utf-8", errors="replace")
    (E / f"txt_{tag}.pdftotext_raw.txt").write_text(raw, encoding="utf-8")
    r2 = subprocess.run(["pdftotext", "-enc", "UTF-8", "-layout", str(p), "-"], capture_output=True)
    (E / f"txt_{tag}.pdftotext_layout.txt").write_text(r2.stdout.decode("utf-8", errors="replace"), encoding="utf-8")
    meta = dict(d.metadata or {})
    # fontes, imagens, anotacoes, anexos, javascript
    fontes = sorted({f[3] for pg in d for f in pg.get_fonts()})
    n_img = sum(len(pg.get_images()) for pg in d)
    n_annot = sum(len(list(pg.annots() or [])) for pg in d)
    n_links = sum(len(pg.get_links()) for pg in d)
    info[tag] = {
        "arquivo": nome, "paginas": d.page_count,
        "tamanho_pagina_pt": [round(d[0].rect.width, 2), round(d[0].rect.height, 2)],
        "metadata": meta, "fontes": fontes, "imagens": n_img, "anotacoes": n_annot, "links": n_links,
        "embfile_count": d.embfile_count(), "chars_fitz": sum(len(x) for x in pags),
        "paginas_chars": [len(x) for x in pags],
        "xmp_len": len(d.get_xml_metadata() or ""),
    }
    print(tag, info[tag]["paginas"], "pag;", info[tag]["chars_fitz"], "chars; metadata:", meta)
(E / "rf_02_texto_pdf.json").write_text(json.dumps(info, indent=1, ensure_ascii=False), encoding="utf-8")
