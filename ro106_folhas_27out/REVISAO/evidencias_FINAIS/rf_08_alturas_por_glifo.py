# -*- coding: utf-8 -*-
# C3 (independente): altura de tinta ACIMA DA LINHA DE BASE de cada glifo de texto vivo nos anexos, por classe
# (algarismo, maiuscula, letra com haste, minuscula sem haste), a partir do contorno da fonte (FreeType via PIL) x tamanho do span (pt).
# Nao usa a medida p90-por-linha do preparador. Fontes: Arial Narrow do Windows, STIXGeneral do matplotlib, CM embutida no PDF.
import fitz, io, json, os, pathlib, collections, unicodedata
from PIL import ImageFont

K = pathlib.Path("C:/IALD/Central de Patentes/work/ro106_folhas_27out")
E = K / "REVISAO" / "evidencias_FINAIS"
PT_CM = 2.54 / 72
PX = 2048

import matplotlib
MPL = pathlib.Path(matplotlib.get_data_path()) / "fonts" / "ttf"
SYS = {
    "ArialNarrow": "C:/Windows/Fonts/ARIALN.TTF",
    "ArialNarrow-Bold": "C:/Windows/Fonts/ARIALNB.TTF",
    "ArialNarrow-Italic": "C:/Windows/Fonts/ARIALNI.TTF",
    "STIXGeneral-Regular": str(MPL / "STIXGeneral.ttf"),
}
ASC = set("bdfhkl")
XH = set("acemnorsuvwxz")
_cache = {}


def load(doc, fontname_full, xref):
    base = fontname_full.split("+")[-1]
    key = (base, xref)
    if key in _cache:
        return _cache[key]
    ft = None
    src = None
    if base in SYS and os.path.exists(SYS[base]):
        ft = ImageFont.truetype(SYS[base], PX)
        src = SYS[base]
    else:
        try:
            data = doc.extract_font(xref)   # (basename, ext, type, content)
            buf = data[3]
            if buf:
                ft = ImageFont.truetype(io.BytesIO(buf), PX)
                src = f"embutida no PDF ({data[1]})"
        except Exception as e:  # noqa
            ft = None
            src = f"FALHA {type(e).__name__}: {e}"
    _cache[key] = (ft, src)
    return _cache[key]


def acima_da_base_em(ft, ch):
    # anchor 'ls' = esquerda/linha de base; top negativo = acima da linha
    try:
        l, t, r, b = ft.getbbox(ch, anchor="ls")
    except Exception:
        return None
    if r - l <= 0:
        return None
    return -t / PX, -b / PX  # topo acima da base (em em), fundo (negativo = abaixo da base)


def classe(ch):
    if ch.isdigit():
        return "algarismo"
    if ch.isalpha() and ch.isupper():
        return "maiuscula (latina/grega)"
    if ch in ASC:
        return "minuscula com haste (b d f h k l)"
    if ch in XH:
        return "minuscula sem haste (a c e m n o r s u v w x z)"
    if ch.isalpha() and ch.islower():
        n = unicodedata.name(ch, "")
        return "outra letra minuscula (" + n.title() + ")"
    return None


res = {}
for pct, nome in (("050579", "FOLHAS_SUBSTITUTIVAS_050579.pdf"), ("050576", "FOLHAS_SUBSTITUTIVAS_050576.pdf")):
    d = fitz.open(K / nome)
    xref_por_fonte = {}
    for pg in d:
        for f in pg.get_fonts():
            xref_por_fonte[f[3].split('+')[-1]] = f[0]
    por_classe = collections.defaultdict(list)
    fontes_usadas = {}
    falhas = collections.Counter()
    for i, pg in enumerate(d, 1):
        for b in pg.get_text("rawdict")["blocks"]:
            for ln in b.get("lines", []):
                for sp in ln["spans"]:
                    fn = sp["font"]
                    xref = xref_por_fonte.get(fn.split('+')[-1])
                    ft, src = load(d, fn, xref)
                    fontes_usadas[fn.split("+")[-1]] = src
                    for c in sp["chars"]:
                        ch = c["c"]
                        cl = classe(ch)
                        if cl is None:
                            continue
                        if ft is None:
                            falhas[fn.split("+")[-1]] += 1
                            continue
                        m = acima_da_base_em(ft, ch)
                        if m is None:
                            falhas[fn.split("+")[-1] + " sem glifo " + repr(ch)] += 1
                            continue
                        top_em, _ = m
                        h_cm = top_em * sp["size"] * PT_CM
                        por_classe[cl].append((round(h_cm, 4), i, ch, fn.split("+")[-1], round(sp["size"], 2)))
    out = {"fontes": fontes_usadas, "falhas": dict(falhas), "classes": {}}
    print("=" * 100)
    print(pct, nome)
    print("  fontes:", fontes_usadas, "| falhas:", dict(falhas))
    for cl, v in sorted(por_classe.items()):
        v.sort()
        out["classes"][cl] = {"n": len(v), "minimo_cm": v[0][0], "mais_baixos": v[:5], "maximo_cm": v[-1][0]}
        print(f"  {cl:60s} n={len(v):5d}  min={v[0][0]:.4f} cm  (folha {v[0][1]}, {v[0][2]!r}, {v[0][3]} {v[0][4]} pt)  max={v[-1][0]:.4f}")
        if cl.startswith(("algarismo", "maiuscula", "minuscula com")):
            abaixo = [x for x in v if x[0] < 0.32]
            print(f"      abaixo de 0,32 cm: {len(abaixo)}", abaixo[:8])
            out["classes"][cl]["abaixo_0_32"] = abaixo[:50]
    res[pct] = out
(E / "rf_08_alturas_por_glifo.json").write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
