# -*- coding: utf-8 -*-
"""So leitura: exercita search_tgl/fetch_tgl do runtime sobre o manifesto PREPARADO (sem instalar, sem rede, sem provedor), com a consulta
que a capsula ensina: nome exato, limit 5, fetch_tgl no offset de cada resultado da fonte menos 2000. Mede tambem a folga do limite de 32 MB do acervo."""
import json
import random
import sys
from pathlib import Path

sys.dont_write_bytecode = True
R = Path(r"C:\IALD\projetos_pyhton\IALD")
W = Path(__file__).resolve().parent
A = W / "app"
sys.path[:0] = [str(R), str(A / "build")]
import haiku_codec as c
import iald_core_indexado as ci

M = A / "science" / "memory_stage" / "manifest_staged.json"
m = json.loads(M.read_bytes())
total = sum(Path(e["path"]).stat().st_size for e in m["entries"])
print("TOTAL acervo", total, "limite 32000000 folga", 32000000 - total)
kf = json.loads(Path(m["published_evidence"]["result"]["path"]).read_bytes())["core"]["kernel_formalization"]
nomes = sorted(c.catalogable_flags(kf))
amostra = random.Random(20261104).sample(nomes, 700)
falhas = []
for q in amostra:
    achou = False
    for x in ci.execute_tool(M, "search_tgl", {"query": q, "limit": 5})["results"]:
        if x["id"] != "resultado_publicado_integral":
            continue
        f = ci.execute_tool(M, "fetch_tgl", {"id": x["id"], "offset": max(0, x["offset"] - 2000), "max_chars": 4500})
        if '"%s": true' % q in f["text"]:
            achou = True
            break
    if not achou:
        falhas.append(q)
print("catalogados", len(nomes), "amostra", len(amostra), "semente 20261104", "achados", len(amostra) - len(falhas), "falhas", falhas)
