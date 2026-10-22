"""Consulta SOMENTE-LEITURA ao inventario da bancada (memory/INVENTARIO_BANCADA_CHATGPT.json) para os temas novos do
pre-registro F1.TEMPO. Grava inventario_consultas_prereg.json na pasta de saida. Uso: python -X utf8 <script> <saida.json>"""
import hashlib
import json
import re
import sys

INV = r"C:\IALD\Central de Patentes\memory\INVENTARIO_BANCADA_CHATGPT.json"
TEMAS = [
    ("pureza", r"purity|pureza"),
    ("inverso_nao_positivo", r"inverse.*(pos|cp)|not_?positive|nonpositive|inv.*dephas|dephas.*inv"),
    ("determinante_volume", r"\bdet_|_det\b|det_diagonal|volume|measurePreserving"),
    ("isometria_orbita", r"isometr"),
    ("espectro_conjugacao", r"charpoly|spectrum.*conj|conj.*spectrum|eigenvalue.*unitar"),
    ("weyl_ccr", r"weyl|ccr|canonical_?commut|commutator_ne|wielandt|wintner"),
    ("schur_multiplier", r"schur|hadamard"),
    ("tempo_sem_posto", r"time.?has.?no.?rank|flow.*not.*idempot|idempot.*flow|not_?idempotent"),
    ("relogio_fase", r"clock|relogio|circle\.exp|angularquotient"),
    ("davies", r"davies"),
]


def main():
    raw = open(INV, "rb").read()
    d = json.loads(raw)
    out = dict(inventario=INV, sha256=hashlib.sha256(raw).hexdigest(), gerado_em=d.get("gerado_em"), temas=[])
    for nome, padrao in TEMAS:
        rx = re.compile(padrao, re.I)
        hits = []
        for u in d["unicos"]:
            ds = [x for x in u.get("decls", []) if rx.search(x)]
            if ds or rx.search(u["arquivo"]):
                hits.append(dict(arquivo=u["arquivo"], sha16=u["sha16"], copias=u.get("copias"), decls=ds[:12]))
        out["temas"].append(dict(tema=nome, padrao=padrao, n_arquivos=len(hits), arquivos=hits[:40]))
    with open(sys.argv[1], "w", encoding="utf-8") as fo:
        json.dump(out, fo, ensure_ascii=False, indent=1)
    for t in out["temas"]:
        print(t["tema"], "n_arquivos=", t["n_arquivos"])
        for h in t["arquivos"][:8]:
            print("    ", h["arquivo"], h["sha16"], h["decls"][:4])


if __name__ == "__main__":
    main()
