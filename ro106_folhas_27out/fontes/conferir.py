# Conferencia por script das folhas substitutivas (medida, nao declarada).
# Uso: python conferir.py <pdf> <rotulo> [--ref-pdf <pdf_como_depositado>]
# Mede, por folha: tamanho (cm), margens (bbox da tinta, render a 600 dpi SEM antialias), cor (varredura vetorial +
# contagem de pixels nao pretos/brancos sem antialias + imagens raster), alturas de caracteres (metodo A5: componentes
# conexos agrupados em linhas, p90 por linha, 300 dpi), largura de traco, reducao a 2/3, figuras/legendas.
import sys, json, hashlib, importlib.util, pathlib, re
import numpy as np, fitz
from scipy import ndimage as ndi

W = pathlib.Path(r'C:\IALD\Central de Patentes\work\ro106_folhas_27out')
A5 = pathlib.Path(r'C:\IALD\Central de Patentes\work\patentes_atualizacao_12out\agentes\a5_desenhos_exigencias\scripts\a5_medir.py')
spec = importlib.util.spec_from_file_location('a5_medir', str(A5))
a5 = importlib.util.module_from_spec(spec)
spec.loader.exec_module(a5)

PXCM300 = 300 / 2.54


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def render_gray(pg, dpi, aa=True):
    fitz.TOOLS.set_aa_level(8 if aa else 0)
    pix = pg.get_pixmap(dpi=dpi, colorspace=fitz.csGRAY, alpha=False)
    fitz.TOOLS.set_aa_level(8)
    a = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.stride)[:, :pix.width]
    return a.copy()


def render_rgb(pg, dpi, aa=True):
    fitz.TOOLS.set_aa_level(8 if aa else 0)
    pix = pg.get_pixmap(dpi=dpi, colorspace=fitz.csRGB, alpha=False)
    fitz.TOOLS.set_aa_level(8)
    a = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.height, pix.stride)[:, :pix.width * 3]
    return a.reshape(pix.height, pix.width, 3).copy()


def vector_colors(pg):
    cols = {}
    for d in pg.get_drawings():
        for k in ('color', 'fill'):
            c = d.get(k)
            if c is not None:
                key = tuple(round(float(x), 3) for x in c)
                cols[key] = cols.get(key, 0) + 1
    tcols = {}
    for b in pg.get_text('dict')['blocks']:
        if b.get('type') != 0:
            continue
        for ln in b['lines']:
            for s in ln['spans']:
                tcols[s['color']] = tcols.get(s['color'], 0) + 1
    return cols, tcols


def stroke_widths(pg):
    ws = {}
    for d in pg.get_drawings():
        if d.get('color') is not None and d.get('width') is not None and d.get('type') in ('s', 'fs'):
            k = round(float(d['width']), 2)
            ws[k] = ws.get(k, 0) + 1
    return ws


def pattern_colors_ok(doc):
    """Varre os objetos de padrao (tiling) e imagens: cores dos operadores de cor nos streams dos padroes."""
    bad = []
    n_pat = 0
    for xref in range(1, doc.xref_length()):
        try:
            obj = doc.xref_object(xref, compressed=False)
        except Exception:
            continue
        if '/PatternType 1' in obj:
            n_pat += 1
            try:
                st = doc.xref_stream(xref).decode('latin-1')
            except Exception:
                st = ''
            for m in re.finditer(r'([\d.\- ]+)\s(rg|RG|g|G|k|K)\b', st):
                vals = [float(x) for x in m.group(1).split()]
                op = m.group(2)
                if op in ('g', 'G') and not (vals and vals[-1] in (0.0, 1.0)):
                    bad.append((xref, m.group(0)))
                if op in ('rg', 'RG') and len(vals) >= 3 and not (len(set(vals[-3:])) == 1 and vals[-1] in (0.0, 1.0)):
                    bad.append((xref, m.group(0)))
    return n_pat, bad


def n_components(g, thr=128):
    lab, n = ndi.label(g < thr, structure=np.ones((3, 3)))
    return int(n)


TALL = re.compile('[A-Z0-9bdfhkl\u03b2\u03b8\u03c6\u2113\u03b4\u03bb\u03b6\u03be\u03c8\u03c7\u0394\u0393\u0398\u039b\u039e\u03a0\u03a3\u03a6\u03a8\u03a9]')


def linhas_texto_altura(pg, dpi=600):
    """Altura MEDIDA no render: por linha de texto vivo, a maior componente conexa de glifo (linha posta na posicao de leitura).
    Linhas com maiuscula/algarismo/ascendente entram no criterio 0,32 cm; as so com letras sem haste (altura-x) ficam listadas a parte."""
    import math
    g = render_gray(pg, dpi, aa=True)
    pxcm = dpi / 2.54
    k = dpi / 72.0
    out = []
    for b in pg.get_text('dict')['blocks']:
        if b.get('type') != 0:
            continue
        for ln in b['lines']:
            txt = ''.join(s['text'] for s in ln['spans']).strip()
            if not txt:
                continue
            x0, y0, x1, y1 = ln['bbox']
            c = g[max(0, int(y0 * k) - 3):int(y1 * k) + 3, max(0, int(x0 * k) - 3):int(x1 * k) + 3] < 128
            dx, dy = ln['dir']
            ang = math.degrees(math.atan2(dy, dx))
            if abs(ang) > 0.5:
                best = None
                for sgn in (1, -1):
                    r = ndi.rotate(c.astype(np.uint8), sgn * ang, reshape=True, order=0) > 0
                    ys, xs = np.where(r)
                    if len(ys) == 0:
                        continue
                    asp = (xs.max() - xs.min() + 1) / float(ys.max() - ys.min() + 1)
                    if best is None or asp > best[0]:
                        best = (asp, r)
                if best is None:
                    continue
                c = best[1]
            lab, n = ndi.label(c, structure=np.ones((3, 3)))
            hs = []
            for sl in ndi.find_objects(lab):
                if sl is None:
                    continue
                h = sl[0].stop - sl[0].start
                w = sl[1].stop - sl[1].start
                if h < 0.12 * pxcm:
                    continue
                if w > 3.2 * h and w > 0.8 * pxcm:
                    continue
                if h > 1.0 * pxcm:
                    continue
                hs.append(h)
            if not hs:
                continue
            cls = 'cap_alg_asc' if TALL.search(txt) else 'so_altura_x'
            out.append({'texto': txt, 'h_max_cm': round(max(hs) / pxcm, 3), 'classe': cls,
                        'caixa_cm': [round(v * 2.54 / 72, 2) for v in ln['bbox']]})
    return out


def cruzamentos(pg):
    """Vetorial, com ordem de pintura e recortes (clip): palavra cruzada por traco desenhado (que nao esteja coberto por
    preenchimento branco pintado depois, e so onde o traco nao esta recortado) e palavra sobre palavra.
    Palavras inclinadas (nem horizontais nem verticais) vao para 'verificar_visualmente'."""
    import math
    dr = pg.get_drawings(extended=True)
    segs = []      # (p, q, seq, cliprect|None)
    whites = []    # (rect, seq)
    clips = {}
    for d in dr:
        if d['type'] == 'clip':
            lv = d.get('level', 0)
            clips[lv] = fitz.Rect(d['scissor'])
            for k in [k for k in clips if k > lv]:
                del clips[k]
            continue
        lv = d.get('level', 0)
        eff = None
        for k, rc in clips.items():
            if k < lv:
                eff = rc if eff is None else (eff & rc)
        seq = d.get('seqno', 0)
        fill = d.get('fill')
        if d['type'] in ('f', 'fs') and fill is not None and tuple(round(float(x), 2) for x in fill) == (1.0, 1.0, 1.0):
            whites.append((d['rect'], seq))
        if d.get('color') is None or d['type'] not in ('s', 'fs'):
            continue
        for it in d['items']:
            if it[0] == 'l':
                segs.append((it[1], it[2], seq, eff))
            elif it[0] == 're':
                r = it[1]
                P = [fitz.Point(r.x0, r.y0), fitz.Point(r.x1, r.y0), fitz.Point(r.x1, r.y1), fitz.Point(r.x0, r.y1)]
                segs += [(P[j], P[(j + 1) % 4], seq, eff) for j in range(4)]
            elif it[0] == 'qu':
                q = it[1]
                P = [q.ul, q.ur, q.lr, q.ll]
                segs += [(P[j], P[(j + 1) % 4], seq, eff) for j in range(4)]
            elif it[0] == 'c':
                p1, p2, p3, p4 = it[1:5]
                pts = []
                for t in np.linspace(0, 1, 13):
                    x = (1 - t) ** 3 * p1.x + 3 * (1 - t) ** 2 * t * p2.x + 3 * (1 - t) * t ** 2 * p3.x + t ** 3 * p4.x
                    y = (1 - t) ** 3 * p1.y + 3 * (1 - t) ** 2 * t * p2.y + 3 * (1 - t) * t ** 2 * p3.y + t ** 3 * p4.y
                    pts.append(fitz.Point(x, y))
                segs += [(pts[j], pts[j + 1], seq, eff) for j in range(12)]
    dirs = []
    for b_ in pg.get_text('dict')['blocks']:
        if b_.get('type') != 0:
            continue
        for ln in b_['lines']:
            dirs.append((fitz.Rect(ln['bbox']), ln['dir']))
    words = pg.get_text('words')
    cross, incl = [], []
    for w in words:
        if '\u221a' in w[4]:
            continue
        r = fitz.Rect(w[:4])
        d = (1.0, 0.0)
        for lr, ldir in dirs:
            if (lr & r).get_area() > 0.5 * r.get_area():
                d = ldir
                break
        ang = abs(math.degrees(math.atan2(d[1], d[0])))
        hh, ww = r.height, r.width
        if ang < 1 or abs(ang - 180) < 1:
            rs = fitz.Rect(r.x0 + 0.0 * ww, r.y0 + 0.22 * hh, r.x1 - 0.0 * ww, r.y1 - 0.22 * hh)
        elif abs(ang - 90) < 1:
            rs = fitz.Rect(r.x0 + 0.22 * ww, r.y0 + 0.0 * hh, r.x1 - 0.22 * ww, r.y1 - 0.0 * hh)
        else:
            incl.append({'palavra': w[4], 'caixa_cm': [round(v * 2.54 / 72, 2) for v in w[:4]]})
            continue
        hit = False
        for a_, b2, seq, eff in segs:
            L = math.hypot(b2.x - a_.x, b2.y - a_.y)
            n = max(2, int(L / 0.7))
            for t in np.linspace(0, 1, n):
                x = a_.x + t * (b2.x - a_.x)
                y = a_.y + t * (b2.y - a_.y)
                if eff is not None and not (eff.x0 - 0.01 <= x <= eff.x1 + 0.01 and eff.y0 - 0.01 <= y <= eff.y1 + 0.01):
                    continue
                if rs.x0 <= x <= rs.x1 and rs.y0 <= y <= rs.y1:
                    covered = any(wr.contains(rs) and wseq > seq for wr, wseq in whites)
                    if not covered:
                        hit = True
                    break
            if hit:
                break
        if hit:
            cross.append({'palavra': w[4], 'caixa_cm': [round(v * 2.54 / 72, 2) for v in w[:4]]})
    over = []
    for i in range(len(words)):
        for j in range(i + 1, len(words)):
            a_, b2 = fitz.Rect(words[i][:4]), fitz.Rect(words[j][:4])
            ii = a_ & b2
            if not ii.is_empty and ii.get_area() > 0.25 * min(a_.get_area(), b2.get_area()):
                over.append({'a': words[i][4], 'b': words[j][4], 'caixa_cm': [round(v * 2.54 / 72, 2) for v in tuple(ii)]})
    return cross, over, incl

def _poly_of(items):
    """Poligono (lista de pontos) de um caminho preenchido, a partir dos itens do PyMuPDF."""
    pts = []
    for it in items:
        if it[0] == 're':
            r = it[1]
            pts += [(r.x0, r.y0), (r.x1, r.y0), (r.x1, r.y1), (r.x0, r.y1)]
        elif it[0] == 'qu':
            q = it[1]
            pts += [(q.ul.x, q.ul.y), (q.ur.x, q.ur.y), (q.lr.x, q.lr.y), (q.ll.x, q.ll.y)]
        elif it[0] == 'l':
            pts += [(it[1].x, it[1].y), (it[2].x, it[2].y)]
        elif it[0] == 'c':
            p1, p2, p3, p4 = it[1:5]
            for t in np.linspace(0, 1, 14):
                pts.append(((1 - t) ** 3 * p1.x + 3 * (1 - t) ** 2 * t * p2.x + 3 * (1 - t) * t ** 2 * p3.x + t ** 3 * p4.x,
                            (1 - t) ** 3 * p1.y + 3 * (1 - t) ** 2 * t * p2.y + 3 * (1 - t) * t ** 2 * p3.y + t ** 3 * p4.y))
    return pts


def oclusao(pg, min_pontos=3):
    """TESTE DE OCLUSAO (vetorial, em ordem de pintura): qualquer elemento opaco/de fundo branco que cubra traco ou marca de
    dado pintado ANTES dele. Conta pontos (amostrados a cada ~0,8 pt) de tracos/marcas dentro do poligono branco (reduzido 0,5 pt).
    Ignora: o fundo da pagina/tela (area > 40% da pagina) e o traco do proprio objeto."""
    from matplotlib.path import Path
    dr = pg.get_drawings(extended=True)
    pa = pg.rect.width * pg.rect.height
    strokes = []     # (seq, pts(np.array Nx2), eff, tipo)
    whites = []      # (seq, rect, polygon pts, eff)
    clips = {}
    for d in dr:
        if d['type'] == 'clip':
            lv = d.get('level', 0)
            clips[lv] = fitz.Rect(d['scissor'])
            for k in [k for k in clips if k > lv]:
                del clips[k]
            continue
        lv = d.get('level', 0)
        eff = None
        for k, rc in clips.items():
            if k < lv:
                eff = rc if eff is None else (eff & rc)
        seq = d.get('seqno', 0)
        fill = d.get('fill')
        isw = fill is not None and tuple(round(float(x), 2) for x in fill) == (1.0, 1.0, 1.0)
        isb = fill is not None and tuple(round(float(x), 2) for x in fill) == (0.0, 0.0, 0.0)
        rect = d['rect']
        if d['type'] in ('f', 'fs') and isw:
            if rect.width * rect.height > 0.40 * pa:
                pass
            else:
                whites.append((seq, rect, _poly_of(d['items']), eff))
        # tracos e marcas
        if d.get('color') is not None and d['type'] in ('s', 'fs'):
            samp = []
            for it in d['items']:
                segs = []
                if it[0] == 'l':
                    segs = [(it[1], it[2])]
                elif it[0] == 're':
                    r = it[1]
                    P = [fitz.Point(r.x0, r.y0), fitz.Point(r.x1, r.y0), fitz.Point(r.x1, r.y1), fitz.Point(r.x0, r.y1)]
                    segs = [(P[j], P[(j + 1) % 4]) for j in range(4)]
                elif it[0] == 'qu':
                    q = it[1]
                    P = [q.ul, q.ur, q.lr, q.ll]
                    segs = [(P[j], P[(j + 1) % 4]) for j in range(4)]
                elif it[0] == 'c':
                    pp = _poly_of([it])
                    segs = [(fitz.Point(*pp[j]), fitz.Point(*pp[j + 1])) for j in range(len(pp) - 1)]
                for a, b in segs:
                    L = max(abs(b.x - a.x), abs(b.y - a.y))
                    n = max(2, int(L / 0.8) + 1)
                    for t in np.linspace(0, 1, n):
                        samp.append((a.x + t * (b.x - a.x), a.y + t * (b.y - a.y)))
            if samp:
                strokes.append((seq, np.array(samp), eff, 'traco'))
        if d['type'] == 'f' and isb and rect.width * rect.height < 4.0 * 72 * 72 / 2.54 / 2.54:
            pp = _poly_of(d['items'])
            if pp:
                strokes.append((seq, np.array(pp), eff, 'marca preenchida'))
    out = []
    for seq, rect, poly, eff in whites:
        if len(poly) < 3:
            continue
        inset = fitz.Rect(rect.x0 + 0.5, rect.y0 + 0.5, rect.x1 - 0.5, rect.y1 - 0.5)
        if inset.is_empty:
            continue
        path = Path(np.array(poly))
        n_in = 0
        kinds = set()
        for sq, pts, eff2, tipo in strokes:
            if sq >= seq:
                continue
            m = (pts[:, 0] > inset.x0) & (pts[:, 0] < inset.x1) & (pts[:, 1] > inset.y0) & (pts[:, 1] < inset.y1)
            if not m.any():
                continue
            sub = pts[m]
            if eff2 is not None:
                m2 = (sub[:, 0] >= eff2.x0 - 0.01) & (sub[:, 0] <= eff2.x1 + 0.01) & (sub[:, 1] >= eff2.y0 - 0.01) & (sub[:, 1] <= eff2.y1 + 0.01)
                sub = sub[m2]
            if eff is not None and len(sub):
                m3 = (sub[:, 0] >= eff.x0 - 0.01) & (sub[:, 0] <= eff.x1 + 0.01) & (sub[:, 1] >= eff.y0 - 0.01) & (sub[:, 1] <= eff.y1 + 0.01)
                sub = sub[m3]
            if len(sub) == 0:
                continue
            ins = path.contains_points(sub)
            k = int(ins.sum())
            if k:
                n_in += k
                kinds.add(tipo)
        if n_in >= min_pontos:
            out.append({'fundo_branco_caixa_cm': [round(v * 2.54 / 72, 2) for v in rect], 'pontos_de_traco_cobertos': n_in, 'tipos': sorted(kinds)})
    return out


def marcacao_RO(pg):
    """O RO carimba cada folha de substituicao no canto superior direito (numero do pedido, data de recebimento) e na margem
    inferior (SUBSTITUTE SHEET (RULE 26)): essas areas tem de ficar LIVRES de tinta (render a 600 dpi, sem antialias)."""
    g6 = render_gray(pg, 600, aa=False)
    px = 600 / 2.54
    H, Wd = g6.shape
    ink = g6 < 255

    def n(x0, y0, x1, y1):
        return int(ink[int(y0 * px):int(y1 * px), int(x0 * px):int(x1 * px)].sum())
    wcm, hcm = Wd / px, H / px
    r = {'canto_superior_direito (x>=12 cm, y<3,5 cm)': n(12.0, 0, wcm, 3.5),
         'margem_superior (y<2,5 cm)': n(0, 0, wcm, 2.5),
         'margem_inferior (y>=28,7 cm)': n(0, hcm - 1.0, wcm, hcm),
         'margem_direita (x>=19,5 cm)': n(wcm - 1.5, 0, wcm, hcm)}
    r['livres'] = all(v == 0 for v in r.values())
    ys, xs = np.where(ink)
    r['distancia_da_tinta_ao_canto_superior_direito_cm'] = round(float(np.min(np.hypot((wcm - xs / px), ys / px))), 2)
    return r


def _render_so(pdf_bytes, idx, manter, dpi=600):
    """Renderiza SO o texto ('texto') ou SO o grafico ('grafico') da pagina idx, por redacao em copia na memoria (sem antialias)."""
    doc = fitz.open(stream=pdf_bytes, filetype='pdf')
    pg = doc[idx]
    pg.add_redact_annot(pg.rect, fill=False)
    if manter == 'grafico':
        pg.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE, graphics=fitz.PDF_REDACT_LINE_ART_NONE, text=fitz.PDF_REDACT_TEXT_REMOVE)
    else:
        pg.apply_redactions(images=fitz.PDF_REDACT_IMAGE_NONE, graphics=fitz.PDF_REDACT_LINE_ART_REMOVE_IF_TOUCHED, text=fitz.PDF_REDACT_TEXT_NONE)
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


def conferir(pdf, label, ref_pdf=None, rotated=()):
    pdf = str(pdf)
    doc = fitz.open(pdf)
    out = {'rotulo': label, 'pdf': pdf, 'sha256': sha256(pdf), 'bytes': pathlib.Path(pdf).stat().st_size,
           'paginas': doc.page_count, 'ferramentas': 'PyMuPDF %s; numpy %s; scipy; metodo de altura = a5_medir.py (A5, 12/10)' % (fitz.VersionBind, np.__version__),
           'criterios': {'A4_cm': [21.0, 29.7], 'margens_cm_min': {'topo': 2.5, 'esquerda': 2.5, 'direita': 1.5, 'base': 1.0},
                         'altura_min_caractere_cm': 0.32, 'obs_altura': 'altura = p90 das alturas de glifo por linha de texto (maiuscula/algarismo/ascendente), como no A5; letras minusculas sem haste (altura-x) nao entram [LEGAL: leitura usual da Regra 11.13(h)]'},
           'folhas': []}
    n_pat, bad_pat = pattern_colors_ok(doc)
    out['padroes_tiling'] = {'n': n_pat, 'operadores_de_cor_fora_de_preto_branco': bad_pat}
    glob_min = 9.9
    glob_gray = 0
    glob_color = 0
    for i, pg in enumerate(doc):
        f = {'folha': i + 1}
        r = pg.rect
        f['tamanho_cm'] = [round(r.width * 2.54 / 72, 3), round(r.height * 2.54 / 72, 3)]
        f['rotacao_pagina'] = pg.rotation
        f['imagens_raster'] = len(pg.get_images())
        # margens: tinta a 600 dpi sem antialias
        g6 = render_gray(pg, 600, aa=False)
        ys, xs = np.where(g6 < 255)
        px = 600 / 2.54
        f['tinta_bbox_cm'] = [round(xs.min() / px, 3), round(ys.min() / px, 3), round((xs.max() + 1) / px, 3), round((ys.max() + 1) / px, 3)]
        f['margens_medidas_cm'] = {'topo': round(ys.min() / px, 3), 'esquerda': round(xs.min() / px, 3),
                                   'direita': round(f['tamanho_cm'][0] - (xs.max() + 1) / px, 3), 'base': round(f['tamanho_cm'][1] - (ys.max() + 1) / px, 3)}
        mm = f['margens_medidas_cm']
        f['margens_ok'] = bool(mm['topo'] >= 2.5 and mm['esquerda'] >= 2.5 and mm['direita'] >= 1.5 and mm['base'] >= 1.0)
        # cor: 600 dpi sem AA em RGB; pixels nao pretos nem brancos, e nao cinza (R!=G!=B)
        rgb = render_rgb(pg, 600, aa=False)
        isbw = ((rgb == 0).all(axis=2)) | ((rgb == 255).all(axis=2))
        f['pixels_nem_preto_nem_branco_600dpi_sem_AA'] = int((~isbw).sum())
        f['pixels_coloridos_R_G_B_diferentes'] = int((~((rgb[:, :, 0] == rgb[:, :, 1]) & (rgb[:, :, 1] == rgb[:, :, 2]))).sum())
        glob_gray += f['pixels_nem_preto_nem_branco_600dpi_sem_AA']
        glob_color += f['pixels_coloridos_R_G_B_diferentes']
        vc, tc = vector_colors(pg)
        f['cores_vetoriais'] = {str(k): v for k, v in vc.items()}
        f['cores_texto_rgb_int'] = {str(k): v for k, v in tc.items()}
        f['larguras_de_traco_pt'] = {str(k): v for k, v in sorted(stroke_widths(pg).items())}
        # texto: metodo A5 a 300 dpi (antialias ligado, igual ao A5), sobre a area util abaixo do numero da folha
        g3 = a5.gray_page(pg)
        pn = a5.page_number_span(pg)
        f['numero_da_folha'] = None
        if pn:
            f['numero_da_folha'] = {'texto': pn['texto'], 'fonte': pn['fonte'], 'tam_pt': round(pn['tam_pt'], 2),
                                    'centro_x_cm': round((pn['bbox'][0] + pn['bbox'][2]) / 2 * 2.54 / 72, 2),
                                    'topo_tinta_cm': f['margens_medidas_cm']['topo'],
                                    'altura_medida_cm': a5.measure_text_span(g3, pn['bbox'])}
        y_top = (pn['bbox'][3] + 4) if pn else 72.0
        rot = (i + 1) in rotated
        f['folha_em_paisagem_topo_a_esquerda'] = bool(rot)
        if rot:
            gg = g3.copy()
            gg[: int(round(y_top * 300 / 72.0)), :] = 255      # tira o numero da folha
            gg = np.ascontiguousarray(np.rot90(gg, k=-1))      # volta a figura para a posicao de leitura
            rect = fitz.Rect(0, 0, r.height, r.width)
            res, lines = a5.analyse_region(gg, rect)
            Hcm = f['tamanho_cm'][1]
            def back(b):   # caixa na imagem girada (cm) -> caixa na pagina (cm)
                x0, y0, x1, y1 = b
                return [y0, Hcm - x1, y1, Hcm - x0]
        else:
            rect = fitz.Rect(0, y_top, r.width, r.height)
            res, lines = a5.analyse_region(g3, rect)
            def back(b):
                return b
        f['texto_area_util'] = res.get('texto')
        f['tracos_area_util'] = res.get('tracos')
        f['preenchimento_cinza_cm2'] = res.get('tons', {}).get('preenchimento_cinza_cm2')
        def palavras(b):
            pb = back(b)
            c = fitz.Rect(pb[0] * 72 / 2.54 - 2, pb[1] * 72 / 2.54 - 2, pb[2] * 72 / 2.54 + 2, pb[3] * 72 / 2.54 + 2)
            return ' '.join(w[4] for w in pg.get_text('words', clip=c))
        f['linhas_menores'] = [{'h_cap_cm': L['h_cap_cm'], 'caixa_cm_pagina': [round(v, 2) for v in back(L['bbox_cm_folha'])], 'n_glifos': L['n_glifos'], 'texto_vivo': palavras(L['bbox_cm_folha'])} for L in res.get('linhas_menores', [])]
        f['linhas_com_tinta_alheia_sobre_o_texto'] = [{'h_cap_cm': L['h_cap_cm'], 'caixa_cm_pagina': [round(v, 2) for v in back(L['bbox_cm_folha'])], 'frac': L['tinta_alheia_frac'], 'texto_vivo': palavras(L['bbox_cm_folha'])} for L in res.get('linhas_sobrepostas', [])]
        lt = linhas_texto_altura(pg)
        capl = [x for x in lt if x['classe'] == 'cap_alg_asc']
        xl = [x for x in lt if x['classe'] == 'so_altura_x']
        f['altura_por_linha_texto_vivo'] = {
            'n_linhas_cap_alg_asc': len(capl),
            'h_min_cap_alg_asc_cm': min([x['h_max_cm'] for x in capl]) if capl else None,
            'linhas_abaixo_032_cap_alg_asc': [x for x in capl if x['h_max_cm'] < 0.32],
            'n_linhas_so_altura_x': len(xl),
            'so_altura_x_abaixo_032': [x for x in xl if x['h_max_cm'] < 0.32]}
        cr, ov, incl = cruzamentos(pg)
        f['oclusao_fundo_branco_sobre_traco_ou_marca'] = oclusao(pg)
        ct, ctinfo = contato_texto_grafico(pdf, i)
        f['TESTE_DE_CONTATO_texto_x_grafico (pixel a pixel, 600 dpi)'] = {'contatos': ct, 'passa': len(ct) == 0, **ctinfo}
        f['marcacao_do_RO_areas_livres'] = marcacao_RO(pg)
        f['texto_inclinado_verificar_visualmente'] = incl
        f['texto_cruzado_por_traco'] = cr
        f['texto_sobre_texto'] = ov
        # legendas (Figura N) por texto vivo
        caps = []
        for b in pg.get_text('dict')['blocks']:
            if b.get('type') != 0:
                continue
            for ln in b['lines']:
                t = ''.join(s['text'] for s in ln['spans']).strip()
                if re.match(r'^Fig(ura)?\s*\d+$', t):
                    caps.append({'texto': t, 'tam_pt': round(ln['spans'][0]['size'], 2), 'fonte': ln['spans'][0]['font'],
                                 'altura_medida_cm': a5.measure_text_span(g3, ln['bbox'])})
        f['legendas_figura'] = caps
        # reducao a 2/3: componentes conexos a 300 dpi vs a 200 dpi (= tamanho a 2/3 amostrado a 300 dpi)
        g2 = render_gray(pg, 200, aa=True)
        n3, n2 = n_components(g3), n_components(g2)
        f['reducao_2_3'] = {'componentes_100%': n3, 'componentes_a_2_3': n2, 'razao': round(n2 / max(n3, 1), 3),
                            'altura_min_linha_a_2_3_cm': round((f['texto_area_util'] or {}).get('h_cap_min_cm', 0) * 2 / 3, 3),
                            'traco_p10_a_2_3_mm': round((f['tracos_area_util'] or {}).get('largura_mm_p10', 0) * 2 / 3, 3)}
        # moldura: algum caminho vetorial cobre >= 90% da area util nas duas direcoes?
        mold = False
        for d in pg.get_drawings():
            rr = d['rect']
            if rr.width >= 0.9 * 17.0 * 72 / 2.54 and rr.height >= 0.9 * 26.2 * 72 / 2.54:
                mold = True
        f['moldura_detectada'] = mold
        t = f['texto_area_util'] or {}
        if t.get('n_linhas'):
            glob_min = min(glob_min, t['h_cap_min_cm'])
        out['folhas'].append(f)
    hm = [f['altura_por_linha_texto_vivo']['h_min_cap_alg_asc_cm'] for f in out['folhas'] if f['altura_por_linha_texto_vivo']['h_min_cap_alg_asc_cm'] is not None]
    out['resumo'] = {'altura_minima_cap_alg_asc_cm_todas_as_folhas_texto_vivo': min(hm) if hm else None,
                     'linhas_abaixo_032_cap_alg_asc_total': sum(len(f['altura_por_linha_texto_vivo']['linhas_abaixo_032_cap_alg_asc']) for f in out['folhas']),
                     'palavras_cruzadas_por_traco_total': sum(len(f['texto_cruzado_por_traco']) for f in out['folhas']),
                     'palavras_sobrepostas_total': sum(len(f['texto_sobre_texto']) for f in out['folhas']),
                     'contatos_texto_grafico_total': sum(len(f['TESTE_DE_CONTATO_texto_x_grafico (pixel a pixel, 600 dpi)']['contatos']) for f in out['folhas']),
                     'oclusoes_total': sum(len(f['oclusao_fundo_branco_sobre_traco_ou_marca']) for f in out['folhas']),
                     'folhas_com_marcacao_do_RO_livre': sum(1 for f in out['folhas'] if f['marcacao_do_RO_areas_livres']['livres']),
                     'altura_minima_de_linha_cm_metodo_A5': glob_min,
                     'pixels_nem_preto_nem_branco_total': glob_gray,
                     'pixels_coloridos_total': glob_color,
                     'folhas_com_margens_ok': sum(1 for f in out['folhas'] if f['margens_ok']),
                     'folhas_A4': sum(1 for f in out['folhas'] if abs(f['tamanho_cm'][0] - 21.0) < 0.05 and abs(f['tamanho_cm'][1] - 29.7) < 0.05)}
    if ref_pdf:
        rd = fitz.open(str(ref_pdf))
        refs = []
        for i, pg in enumerate(rd):
            g3 = a5.gray_page(pg)
            pn = a5.page_number_span(pg)
            y_top = (pn['bbox'][3] + 4) if pn else 72.0
            res, lines = a5.analyse_region(g3, fitz.Rect(0, y_top, pg.rect.width, pg.rect.height))
            refs.append({'folha': i + 1, 'texto': res.get('texto'), 'tracos': res.get('tracos'), 'tons': res.get('tons')})
        out['como_depositado_mesma_metrica'] = {'pdf': str(ref_pdf), 'sha256': sha256(ref_pdf), 'folhas': refs}
    return out


if __name__ == '__main__':
    pdf, label = sys.argv[1], sys.argv[2]
    ref = None
    if '--ref-pdf' in sys.argv:
        ref = sys.argv[sys.argv.index('--ref-pdf') + 1]
    rot = ()
    if '--rot' in sys.argv:
        rot = tuple(int(x) for x in sys.argv[sys.argv.index('--rot') + 1].split(','))
    o = conferir(pdf, label, ref, rot)
    outp = W / 'conferencia' / f'medidas_{label}.json'
    outp.write_text(json.dumps(o, indent=1, ensure_ascii=False), encoding='utf-8')
    print(json.dumps(o['resumo'], indent=1))
    for f in o['folhas']:
        t = f['texto_area_util'] or {}
        al = f['altura_por_linha_texto_vivo']
        print(f['folha'], 'h_min(vivo,cap/alg/asc)', al['h_min_cap_alg_asc_cm'], 'abaixo', len(al['linhas_abaixo_032_cap_alg_asc']), 'xheight<0.32', len(al['so_altura_x_abaixo_032']), 'cruz', len(f['texto_cruzado_por_traco']), 'sobre', len(f['texto_sobre_texto']), 'OCLUSAO', len(f['oclusao_fundo_branco_sobre_traco_ou_marca']), 'RO-livre', f['marcacao_do_RO_areas_livres']['livres'])
        print('  ', f['tamanho_cm'], 'margens', {k: float(v) for k, v in f['margens_medidas_cm'].items()}, 'ok' if f['margens_ok'] else 'FALHA',
              '| h_min', t.get('h_cap_min_cm'), 'p05', t.get('h_cap_p05_cm'), 'n<0.32', t.get('n_linhas_abaixo_032'), 'linhas', t.get('n_linhas'),
              '| traco_p10_mm', (f['tracos_area_util'] or {}).get('largura_mm_p10'), '| sobrep', len(f['linhas_com_tinta_alheia_sobre_o_texto']),
              '| nonBW', f['pixels_nem_preto_nem_branco_600dpi_sem_AA'], '| red2/3', f['reducao_2_3']['razao'])
