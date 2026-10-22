# -*- coding: utf-8 -*-
"""E -- o auditor nao tocou nada fora da propria pasta: livro do mapa, pastas da unidade e artefatos por hash."""
import datetime as dt, hashlib, json, os

U = r"C:\IALD\Central de Patentes\work\frequencia_defasa_12out"
R2 = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
a1 = json.load(open(os.path.join(R2, "saidas", "A1_FREEZE.json"), encoding="utf-8"))
mapa = json.load(open(os.path.join(R2, "saidas", "consultas_mapa", "RESUMO.json"), encoding="utf-8"))


def sha(p):
    return hashlib.sha256(open(p, "rb").read()).hexdigest()


res = {}
L = r"C:\IALD\MAPA_DE_ROTAS\rotas.jsonl"
res["livro_mapa"] = dict(sha256=sha(L), igual_ao_da_consulta=(sha(L) == mapa["livro_depois"]["sha256"]))
pastas = {}
for sub in ("0_LEVANTAMENTO", "1_PREREGISTRO", "2_OPTICO", "3_KERNEL"):
    n, mx = 0, 0
    for dp, dns, fns in os.walk(os.path.join(U, sub)):
        for f in fns:
            n += 1
            mx = max(mx, os.stat(os.path.join(dp, f)).st_mtime_ns)
    pastas[sub] = dict(n_arquivos=n, mtime_mais_recente_utc=dt.datetime.fromtimestamp(mx / 1e9, dt.timezone.utc).isoformat())
res["pastas_da_unidade"] = pastas
art = {}
for rel, v in a1["artefatos_declarados"].items():
    h = sha(os.path.join(U, rel))
    art[rel] = dict(igual_ao_A1=(h == v["medido"][1]))
res["artefatos"] = art
res["todos_iguais"] = res["livro_mapa"]["igual_ao_da_consulta"] and all(x["igual_ao_A1"] for x in art.values())
with open(os.path.join(R2, "saidas", "E_INTOCADOS.json"), "x", encoding="utf-8") as fh:
    json.dump(res, fh, ensure_ascii=False, indent=1)
print(json.dumps(res, ensure_ascii=False, indent=1))
