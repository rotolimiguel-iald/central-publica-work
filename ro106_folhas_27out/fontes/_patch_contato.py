import pathlib
p = pathlib.Path(r'C:\IALD\Central de Patentes\work\ro106_folhas_27out\fontes\conferir.py')
s = p.read_text(encoding='utf-8')
add = r'''

def _render_so(pdf_bytes, idx, manter, dpi=600):
    """Renderiza SO o texto ('texto') ou SO o grafico ('grafico') da pagina idx, por redacao em copia na memoria (sem antialias)."""
    doc = fitz.open(stream=pdf_bytes, filetype='pdf')
    pg = doc[idx]
    pg.add_redact_annot(pg.rect, fill=False)
    if manter == 'grafico':
        pg.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE, graphics=fitz.PDF_REDACT_LINE_ART_NONE, text=fitz.PDF_REDACT_TEXT_REMOVE)
    else:
        pg.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE, graphics=fitz.PDF_REDACT_LINE_ART_REMOVE_IF_COVERED, text=fitz.PDF_REDACT_TEXT_NONE)
    return render_gray(pg, dpi, aa=False) < 255


def contato_texto_grafico(pdf_path, idx, dpi=600, min_px=3):
    """TESTE DE CONTATO PIXEL A PIXEL: texto e grafico renderizados em separado (600 dpi, sem antialias); contato = pixel de tinta
    comum aos dois. Componentes conexos de contato com >= min_px pixels. Exclui as reguas de radical (parte do glifo de «sqrt»):
    contato dentro da caixa de uma palavra que contem o sinal de raiz. Pega o caso da grade que toca uma letra."""
    data = pathlib.Path(pdf_path).read_bytes()
    doc = fitz.open(stream=data, filetype='pdf')
    pg = doc[idx]
    words = pg.get_text('words')
    t = _render_so(data, idx, 'texto', dpi)
    g = _render_so(data, idx, 'grafico', dpi)
    both = t & g
    lab, n = ndi.label(both, structure=np.ones((3, 3)))
    k = dpi / 72.0
    out = []
    for i, sl in enumerate(ndi.find_objects(lab), start=1):
        if sl is None:
            continue
        area = int((lab[sl] == i).sum())
        if area < min_px:
            continue
        y0, y1, x0, x1 = sl[0].start / k, sl[0].stop / k, sl[1].start / k, sl[1].stop / k
        cx, cy = (x0 + x1) / 2, (y0 + y1) / 2
        w_in = [w for w in words if w[0] - 2 <= cx <= w[2] + 2 and w[1] - 2 <= cy <= w[3] + 2]
        if any('\u221a' in w[4] for w in w_in):
            continue
        out.append({'px': area, 'caixa_cm': [round(v * 2.54 / 72, 2) for v in (x0, y0, x1, y1)], 'palavra': ' '.join(w[4] for w in w_in) or None})
    return out, {'pixels_de_texto': int(t.sum()), 'pixels_de_grafico': int(g.sum())}
'''
marker = "\n\ndef conferir(pdf, label, ref_pdf=None, rotated=()):"
assert s.count(marker) == 1
s = s.replace(marker, add + marker)
m2 = "        f['oclusao_fundo_branco_sobre_traco_ou_marca'] = oclusao(pg)\n"
assert s.count(m2) == 1
s = s.replace(m2, m2 + "        ct, ctinfo = contato_texto_grafico(pdf, i)\n        f['TESTE_DE_CONTATO_texto_x_grafico (pixel a pixel, 600 dpi)'] = {'contatos': ct, 'passa': len(ct) == 0, **ctinfo}\n")
m3 = "                     'oclusoes_total': sum("
assert s.count(m3) == 1
s = s.replace(m3, "                     'contatos_texto_grafico_total': sum(len(f['TESTE_DE_CONTATO_texto_x_grafico (pixel a pixel, 600 dpi)']['contatos']) for f in out['folhas']),\n" + m3)
p.write_text(s, encoding='utf-8')
print('ok')
