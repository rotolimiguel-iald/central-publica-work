# -*- coding: utf-8 -*-
"""consultar_mapa.py -- roda `rotas.py consultar <tema>` (SO LEITURA do livro) para cada tema e guarda as saidas em mapa_consulta_<tema>.json
na pasta de trabalho; imprime o resumo (n de rotas, ids, registros do livro, cabeca). Nada e registrado.
Uso: python -I -B -X utf8 consultar_mapa.py
"""
import json
import os
import re
import subprocess

W = r"C:\IALD\Central de Patentes\work\afinacao_das_cordas_v398"
MAPA = r"C:\IALD\MAPA_DE_ROTAS"
PY = r"C:\Python314\python.exe"
TEMAS = [
    "cordas", "dimensao critica", "zeta", "string", "supercorda", "10 dimensoes", "afinacao", "Matsubara", "Hagedorn",
    "periodo minimo", "PolarPeriod", "face hiperbolica", "superposicao", "Palavra", "Station", "Fundacao", "abismo",
    "Unruh", "Bisognano", "Casimir", "Tetelestai", "Ultima Corda", "d_crit", "Bernoulli", "Hurwitz", "regularizacao",
]

resumo = {}
for tema in TEMAS:
    r = subprocess.run([PY, "-X", "utf8", os.path.join(MAPA, "rotas.py"), "consultar", tema], capture_output=True, text=True,
                       encoding="utf-8", cwd=MAPA, timeout=300)
    assert r.returncode == 0, (tema, r.stderr[:300])
    d = json.loads(r.stdout)
    nome = "mapa_consulta_" + re.sub(r"[^A-Za-z0-9_]+", "_", tema) + ".json"
    with open(os.path.join(W, nome), "w", encoding="utf-8", newline="\n") as f:
        json.dump(d, f, ensure_ascii=False, indent=1)
    resumo[tema] = {"n": d["n"], "rotas": [x["rota_id"] for x in d["rotas"]][:12], "registros_do_livro": d["n_registros"], "cabeca": d["cabeca"], "arquivo": nome}
with open(os.path.join(W, "mapa_consultas_resumo.json"), "w", encoding="utf-8", newline="\n") as f:
    json.dump(resumo, f, ensure_ascii=False, indent=1)
for t, v in resumo.items():
    print(f"{t!r}: n={v['n']} | livro={v['registros_do_livro']} cabeca={v['cabeca']} | {v['rotas'][:6]}")
