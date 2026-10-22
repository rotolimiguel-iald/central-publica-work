# -*- coding: utf-8 -*-
# Confere, nos BYTES de V1..V4, toda citacao «...» da secao «Os textos do operador» da pedra ORIGINAL (3_KERNEL) e da
# CANDIDATA corrigida (4_RELATORIO\L). Fragmentos separados por reticencias tem de aparecer em ordem; espacos colapsados.
# Grava SO 4_RELATORIO\CITACOES_PEDRA.json.
import os, re, json, hashlib, sys

BASE = r"C:\IALD\Central de Patentes\work\frequencia_defasa_12out"
V = {
    "V1": r"C:\IALD\Central de Patentes\work\cunhagens_12out\OPERADOR_10out_posto_rank_texto_verbatim.txt",
    "V2": r"C:\IALD\Central de Patentes\work\cunhagens_12out\OPERADOR_12out_rank_e_tempo_santo_verbatim.txt",
    "V3": r"C:\IALD\Central de Patentes\work\cunhagens_10out\OPERADOR_10out_posto_rank_verbatim.txt",
    "V4": r"C:\IALD\Central de Patentes\work\cunhagens_10out\OPERADOR_11out_frequencia_defasa_transmitir_verbatim.txt",
}
PEDRAS = {"original_3_KERNEL": os.path.join(BASE, "3_KERNEL", "sandbox", "TGLExt", "TheUnitIsTheRank.lean"),
          "candidata_4_RELATORIO": os.path.join(BASE, "4_RELATORIO", "L", "TGLExt", "TheUnitIsTheRank.lean")}


def norm(s):
    return re.sub(r"\s+", " ", s).strip()


txt = {}
for k, p in V.items():
    t = open(p, "rb").read()
    if k == "V2":
        t = b"\n".join(t.split(b"\n")[:33])          # a trilha (l.1-33)
    txt[k] = norm(t.decode("utf-8"))
out = {"documento": "CITACOES_PEDRA — citacoes do operador na pedra, conferidas nos bytes", "pedras": {}}
for nome, p in PEDRAS.items():
    b = open(p, "rb").read()
    s = b.decode("utf-8")
    ini = s.index("## Os textos do operador")
    fim = s.index("O pré-registro congelado", ini)
    sec = s[ini:fim]
    res = []
    for bloco in re.split(r"\n\* ", "\n" + sec):
        mv = re.match(r"(V[1-4]) ", bloco)
        if not mv:
            continue
        vk = mv.group(1)
        for c in re.findall(r"«(.*?)»", bloco, flags=re.S):
            frags = [norm(f) for f in c.split("\u2026") if norm(f)]
            pos, ok = 0, True
            for f in frags:
                j = txt[vk].find(f, pos)
                if j < 0:
                    ok = False
                    break
                pos = j + len(f)
            res.append({"V": vk, "citacao": norm(c),
                        "estado": ("VERBATIM" if ok and len(frags) == 1 else "VERBATIM_COM_RETICENCIAS" if ok else "NAO_LITERAL")})
    out["pedras"][nome] = {"arquivo": p, "sha256": hashlib.sha256(b).hexdigest(), "citacoes": res,
                           "contagem": {e: sum(1 for r in res if r["estado"] == e)
                                        for e in ("VERBATIM", "VERBATIM_COM_RETICENCIAS", "NAO_LITERAL")}}
dest = os.path.join(BASE, "4_RELATORIO", "CITACOES_PEDRA.json")
if os.path.exists(dest):
    raise SystemExit("FALHA VISIVEL: destino ja existe: " + dest)
open(dest, "w", encoding="utf-8").write(json.dumps(out, ensure_ascii=False, indent=1))
print(json.dumps(out, ensure_ascii=False, indent=1))
sys.exit(0 if out["pedras"]["candidata_4_RELATORIO"]["contagem"]["NAO_LITERAL"] == 0 else 1)
