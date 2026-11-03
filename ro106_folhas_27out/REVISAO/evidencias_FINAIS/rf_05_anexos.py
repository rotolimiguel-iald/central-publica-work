# -*- coding: utf-8 -*-
# C4/C5: anexos citados nas cartas finais (existencia, hash, n. de folhas, orientacao, numeracao n/N, figura por folha),
# e folhas depositadas (figura por folha). Somente leitura.
import fitz, json, pathlib, re, hashlib

K = pathlib.Path("C:/IALD/Central de Patentes/work/ro106_folhas_27out")
E = K / "REVISAO" / "evidencias_FINAIS"
ANEXOS = {
    "050576": {"anexo": "FOLHAS_SUBSTITUTIVAS_050576.pdf", "sha16": "884d978a39b20d1a", "dep": "entrada/aprendizado/04_DESENHOS_como_depositado.pdf",
               "n_folhas": 6, "paisagem": [1, 6],
               "fig_por_folha_esperado": {1: [1], 2: [2, 3], 3: [4, 5], 4: [6, 7], 5: [8], 6: [9]},
               "dep_esperado": {1: [1, 2], 2: [3, 4], 3: [5, 6], 4: [7, 8], 5: [9]}},
    "050579": {"anexo": "FOLHAS_SUBSTITUTIVAS_050579.pdf", "sha16": "4faa43ca81442fc5", "dep": "entrada/mqc/04_DESENHOS_CINZA_como_depositado.pdf",
               "n_folhas": 8, "paisagem": [1, 4, 8],
               "fig_por_folha_esperado": {i: [i] for i in range(1, 9)},
               "dep_esperado": {1: [1, 2, 3], 2: [4, 5, 6], 3: [7, 8]}},
}
res = {}
for pct, a in ANEXOS.items():
    p = K / a["anexo"]
    b = p.read_bytes()
    sha16 = hashlib.sha256(b).hexdigest()[:16]
    d = fitz.open(p)
    pags = []
    for i, pg in enumerate(d, 1):
        w, h = pg.rect.width, pg.rect.height
        txt = pg.get_text("text")
        nN = re.findall(r"\b(\d)\s*/\s*(\d)\b", txt)
        figs = sorted({int(x) for x in re.findall(r"(?:FIG\.?|Fig\.?|FIGURA|Figura)\s*(\d)", txt)})
        pags.append({"folha": i, "largura_mm": round(w * 25.4 / 72, 1), "altura_mm": round(h * 25.4 / 72, 1),
                     "paisagem_pela_pagina": w > h, "rotacao_pdf": pg.rotation, "n_sobre_N": nN[:3], "figuras_no_texto": figs,
                     "chars": len(txt), "imagens": len(pg.get_images())})
    dd = fitz.open(K / a["dep"])
    dep = []
    for i, pg in enumerate(dd, 1):
        txt = pg.get_text("text")
        figs = sorted({int(x) for x in re.findall(r"(?:FIG\.?|Fig\.?|FIGURA|Figura)\s*(\d)", txt)})
        dep.append({"folha": i, "w_mm": round(pg.rect.width * 25.4 / 72, 1), "h_mm": round(pg.rect.height * 25.4 / 72, 1), "chars": len(txt), "figuras_no_texto": figs, "imagens": len(pg.get_images())})
    res[pct] = {"anexo": a["anexo"], "sha16": sha16, "sha16_esperado": a["sha16"], "confere": sha16 == a["sha16"],
                "paginas": d.page_count, "paginas_esperadas": a["n_folhas"], "folhas": pags,
                "depositado": {"arquivo": a["dep"], "paginas": dd.page_count, "folhas": dep}}
    print("=" * 90)
    print(pct, a["anexo"], "sha16", sha16, "OK" if sha16 == a["sha16"] else "DIVERGE", "| paginas", d.page_count, "(esperado", a["n_folhas"], ")")
    for x in pags:
        print("  folha", x["folha"], f'{x["largura_mm"]}x{x["altura_mm"]} mm', "paisagem(pagina)" if x["paisagem_pela_pagina"] else "retrato", "rot", x["rotacao_pdf"],
              "n/N:", x["n_sobre_N"], "figs:", x["figuras_no_texto"], "chars", x["chars"], "imgs", x["imagens"])
    print("  depositado:", a["dep"], "paginas", dd.page_count)
    for x in dep:
        print("   dep folha", x["folha"], f'{x["w_mm"]}x{x["h_mm"]}', "figs", x["figuras_no_texto"], "chars", x["chars"], "imgs", x["imagens"])
(E / "rf_05_anexos.json").write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
