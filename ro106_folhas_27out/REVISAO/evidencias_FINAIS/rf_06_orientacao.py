# -*- coding: utf-8 -*-
# C4/C5: a orientacao das folhas dos anexos bate com o que as cartas declaram (paisagem = topo da figura a esquerda)?
# Mede a direcao dominante do texto de cada folha (exclui o n/N). dir=(1,0): texto em pe; dir=(0,-1): lido de baixo para cima
# (topo da figura voltado para a esquerda).
import fitz, json, pathlib, collections, re

K = pathlib.Path("C:/IALD/Central de Patentes/work/ro106_folhas_27out")
E = K / "REVISAO" / "evidencias_FINAIS"
CARTA_PAISAGEM = {"050576": [1, 6], "050579": [1, 4, 8]}
res = {}
for pct, nome in (("050576", "FOLHAS_SUBSTITUTIVAS_050576.pdf"), ("050579", "FOLHAS_SUBSTITUTIVAS_050579.pdf")):
    d = fitz.open(K / nome)
    out = []
    for i, pg in enumerate(d, 1):
        c = collections.Counter()
        nN = None
        for b in pg.get_text("dict")["blocks"]:
            for ln in b.get("lines", []):
                t = "".join(s["text"] for s in ln["spans"]).strip()
                if re.fullmatch(r"\d\s*/\s*\d", t):
                    nN = (t, tuple(round(v, 2) for v in ln["dir"]), [round(v, 1) for v in ln["bbox"]])
                    continue
                n = sum(len(s["text"].strip()) for s in ln["spans"])
                if n:
                    c[(round(ln["dir"][0]), round(ln["dir"][1]))] += n
        dom = c.most_common(1)[0][0] if c else None
        pais = dom == (0, -1)
        out.append({"folha": i, "direcao_dominante": dom, "caracteres_por_direcao": {str(k): v for k, v in c.items()}, "nN": nN,
                    "paisagem_medida": pais, "paisagem_declarada_na_carta": i in CARTA_PAISAGEM[pct]})
        print(pct, "folha", i, "dir dominante", dom, dict(c), "n/N:", nN, "| paisagem medida:", pais, "| declarada:", i in CARTA_PAISAGEM[pct],
              "OK" if pais == (i in CARTA_PAISAGEM[pct]) else "DIVERGE")
    res[pct] = out
(E / "rf_06_orientacao.json").write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
