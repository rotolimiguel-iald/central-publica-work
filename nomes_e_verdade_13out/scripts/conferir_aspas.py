# -*- coding: utf-8 -*-
"""Confere as citacoes «...» NOVAS (as que estao na pedra nova e nao na fonte original) contra os bytes dos verbatins do operador
(13/10 nomes/identidade; 13/10 identidade r1; 12/10 rank e tempo). Espaco em branco normalizado. Falha visivel se alguma estiver fora."""
import re, json, hashlib, sys, os
W = "C:/IALD/Central de Patentes/work"
AQUI = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
V = {"13out_nomes": W + "/cunhagens_13out/OPERADOR_13out_nomes_identidade_cordeiro_torre_verbatim.txt",
     "13out_identidade_r1": W + "/cunhagens_13out/OPERADOR_13out_identidade_cordeiro_verbatim.txt",
     "12out_rank_tempo": W + "/cunhagens_12out/OPERADOR_12out_rank_e_tempo_santo_verbatim.txt"}
norm = lambda s: re.sub(r"\s+", " ", s)
vt = {k: norm(open(p, "rb").read().decode("utf-8")) for k, p in V.items()}
vh = {k: hashlib.sha256(open(p, "rb").read()).hexdigest()[:16] for k, p in V.items()}
PARES = {"Posto": (W + "/frequencia_defasa_12out/5_R3/sandbox/TGLExt/TheUnitIsTheRank.lean", AQUI + "/1_POSTO/Posto.lean"),
         "Santo": (W + "/tempo_santo_12out/5_R2/1_PEDRA/sandbox/TheTimeIsNotAPost.lean", AQUI + "/2_SANTO/Santo.lean"),
         "IALD": (W + "/organismo_iald_12out/7_R3_DOCSTRINGS/fonte/TGLExt/IALD.lean", AQUI + "/3_IALD/IALD.lean"),
         "Verdade": (W + "/identidade_cordeiro_13out/5_R2/pedra/TheIdentityHasAName.lean", AQUI + "/4_VERDADE/Verdade.lean")}
res = {}
ruins = 0
for nome, (orig, novo) in PARES.items():
    qo = set(norm(q) for q in re.findall(r"«([^»]+)»", open(orig, encoding="utf-8").read()))
    qn = [norm(q) for q in re.findall(r"«([^»]+)»", open(novo, encoding="utf-8").read())]
    novos = sorted(set(q for q in qn if q not in qo))
    linhas = []
    for q in novos:
        frags = [f.strip() for f in q.split("…") if f.strip()]
        onde = [k for k, v in vt.items() if all(f in v for f in frags)]
        linhas.append({"citacao": q, "nos_bytes_de": onde})
        if not onde:
            ruins += 1
    res[nome] = {"citacoes_novas": len(novos), "fora_dos_bytes": [l["citacao"] for l in linhas if not l["nos_bytes_de"]], "detalhe": linhas}
json.dump({"verbatins_sha16": vh, "resultado": res}, open(AQUI + "/medidas/CONFERENCIA_ASPAS.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print({k: (v["citacoes_novas"], v["fora_dos_bytes"]) for k, v in res.items()})
sys.exit(1 if ruins else 0)
