# -*- coding: utf-8 -*-
# C3: independente da medida p90-por-linha do preparador. Lista os spans de texto vivo por tamanho de fonte (pt) e fonte, nos dois anexos,
# para achar sub/sobrescritos ou texto menor que o corpo (14-15 pt) que contenha algarismo, maiuscula ou letra com haste.
import fitz, json, pathlib, collections, re, unicodedata

K = pathlib.Path("C:/IALD/Central de Patentes/work/ro106_folhas_27out")
E = K / "REVISAO" / "evidencias_FINAIS"
PT_CM = 2.54 / 72
res = {}
for pct, nome in (("050579", "FOLHAS_SUBSTITUTIVAS_050579.pdf"), ("050576", "FOLHAS_SUBSTITUTIVAS_050576.pdf")):
    d = fitz.open(K / nome)
    tamanhos = collections.Counter()
    pequenos = []
    for i, pg in enumerate(d, 1):
        for b in pg.get_text("dict")["blocks"]:
            for ln in b.get("lines", []):
                for sp in ln["spans"]:
                    t = sp["text"]
                    if not t.strip():
                        continue
                    tamanhos[(round(sp["size"], 2), sp["font"].split("+")[-1])] += len(t.strip())
                    if sp["size"] < 13.5:
                        pequenos.append({"folha": i, "tam_pt": round(sp["size"], 2), "fonte": sp["font"], "texto": t, "dir": [round(v) for v in ln["dir"]],
                                         "bbox_cm": [round(v * PT_CM, 2) for v in sp["bbox"]]})
    res[pct] = {"tamanhos_pt_fonte_caracteres": {f"{k[0]} | {k[1]}": v for k, v in sorted(tamanhos.items())}, "spans_menores_que_13_5_pt": pequenos}
    print("=" * 100)
    print(pct, nome)
    for (s, f), n in sorted(tamanhos.items()):
        print(f"   {s:6.2f} pt  {f:32s} {n:5d} caracteres")
    print("   spans < 13,5 pt:", len(pequenos))
    for x in pequenos:
        print("    folha", x["folha"], x["tam_pt"], "pt", x["fonte"].split("+")[-1], repr(x["texto"]), "dir", x["dir"])
(E / "rf_07_spans_pequenos.json").write_text(json.dumps(res, indent=1, ensure_ascii=False), encoding="utf-8")
