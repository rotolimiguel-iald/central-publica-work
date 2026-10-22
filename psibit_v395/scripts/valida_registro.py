"""Valida registro_mapa_psibit.json com a MESMA função que o mapa usa (rotas._valida), SEM registrar.

Só leitura: importa rotas.py (que só define constantes/funções), lê rotas.jsonl para obter os ids/seqs existentes,
chama _valida e imprime o registro normalizado (artefatos com sha256 calculado). Não escreve no livro.
"""
import importlib.util
import json
import sys

MAPA = r"C:\IALD\MAPA_DE_ROTAS"
REG = r"C:\IALD\Central de Patentes\work\psibit_v395\registro_mapa_psibit.json"

spec = importlib.util.spec_from_file_location("rotas_ro", MAPA + r"\rotas.py")
rotas = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rotas)

ids, seqs = set(), set()
with open(MAPA + r"\rotas.jsonl", encoding="utf-8") as f:
    for ln in f:
        ln = ln.strip()
        if not ln:
            continue
        r = json.loads(ln)
        if "rota_id" in r:
            ids.add(r["rota_id"])
        if isinstance(r.get("seq"), int):
            seqs.add(r["seq"])

reg = json.load(open(REG, encoding="utf-8"))
campos_modelo = set(rotas.MODELO)
extras = sorted(set(reg) - campos_modelo)
faltando_no_registro = sorted(campos_modelo - set(reg))
print("campos fora do modelo:", extras)
print("campos do modelo ausentes (aceitável: corrige só em ERRATA):", faltando_no_registro)
r = rotas._valida(reg, ids, seqs)
print("VALIDO. rota_id livre no livro:", r["rota_id"] not in ids, "| registros no livro:", len(seqs))
print(json.dumps({k: (v if k != "artefatos" else v) for k, v in r.items() if k in ("tipo", "rota_id", "dominio", "status", "estatuto", "olhou_dados", "artefatos")},
                 ensure_ascii=False, indent=1))
