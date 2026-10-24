"""Executable counterexamples for the INSTALLED rank_nodes (layered_retrieval.py, 21/10 10:35; not Kimi's code).
Runs inside the copy (pure function, no IO)."""
import sys

sys.path.insert(0, r"C:\t\orq_copia_kimi")
from iald_orchestrator.layered_retrieval import rank_nodes, terms  # noqa: E402

query = "Revisao Claude do benchmark turbina e descida grep-c3 de Kimi: o criterio de fechado para a unidade"
rows = [
    {"id": "alvo_curto", "tipo": "rota", "titulo": "benchmark turbina", "texto": "descida grep-c3", "quando": "2026-10-21T10:00:00-03:00"},
    {"id": "ruido_generico", "tipo": "memoria", "titulo": "Anotacoes",
     "texto": "o criterio de fechado para a unidade e do que com por uma regra geral sobre outro assunto", "quando": "2026-10-01T10:00:00-03:00"},
]
q = terms(query)
for r in rows:
    print(r["id"], "overlap =", len(q & terms(r["titulo"] + " " + r["texto"])))
print("order (stopword inflation):", [r["id"] for r in rank_nodes(rows, query)])
rows3 = [{"id": "x_REAL", "tipo": "rota", "titulo": "t", "texto": "descida camadas", "estatuto": "REAL", "quando": "2026-10-01"},
         {"id": "x_OPEN", "tipo": "rota", "titulo": "t", "texto": "descida camadas", "estatuto": "OPEN", "quando": "2026-10-02"}]
print("order when only estatuto differs (recency decides, estatuto ignored):", [r["id"] for r in rank_nodes(rows3, "descida camadas")])
