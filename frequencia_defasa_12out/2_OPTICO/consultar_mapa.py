# -*- coding: utf-8 -*-
"""Consultas SO-LEITURA ao mapa de rotas (rodada 2 do construtor optico, F1.FREQUENCIA trilha POSTO).

Cetico aferidor: antes de escrever «falta», «nao existe» ou «ja examinado», consultar e citar.
Usa `rotas.py consultar` (que so le o livro; nao toma a trava nem grava). Confere o sha256 do livro
rotas.jsonl antes e depois. Grava SO em 2_OPTICO/consultas_mapa/. NUNCA roda `registrar`.
"""
import hashlib
import json
import os
import subprocess
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
SAIDA = os.path.join(AQUI, "consultas_mapa")
ROTAS_PY = r"C:\IALD\MAPA_DE_ROTAS\rotas.py"
LIVRO = r"C:\IALD\MAPA_DE_ROTAS\rotas.jsonl"

CONSULTAS = [
    ("o01", "otic|optic|modelo otico|ensaio otico|run_optico"),
    ("o02", "posto_e_defasagem|frequencia_defasa|F1.FREQUENCIA|TheUnitIsTheRank|unidade e o rank"),
    ("o03", "Smat_pow|potencia da matriz|S\\(th\\)\\^n|sin.2.\\(n|passagens"),
    ("o04", "dephase|defasagem|semigrupo"),
    ("o05", "anticomut|anticommut|anticomm"),
    ("o06", "vazamento|leak"),
    ("o07", "pureza|purity|posto 1|rank"),
    ("o08", "fractal|D_beta|Tudo = D"),
    ("o09", "singularidade_le_atrator|F1.ATRATOR|atrator"),
]


def sha256(p):
    with open(p, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def main():
    os.makedirs(SAIDA, exist_ok=True)
    antes = dict(sha256=sha256(LIVRO), bytes=os.path.getsize(LIVRO), quando_local=time.strftime("%Y-%m-%d %H:%M:%S"))
    resumo = []
    for cid, padrao in CONSULTAS:
        destino = os.path.join(SAIDA, cid + ".json")
        if os.path.exists(destino):
            print("FALHA VISIVEL: consulta ja existe (nao sobrescrevo): " + destino, file=sys.stderr)
            return 2
        r = subprocess.run([sys.executable, "-X", "utf8", ROTAS_PY, "consultar", padrao, "--limite", "200"],
                           capture_output=True, text=True, encoding="utf-8")
        with open(destino, "w", encoding="utf-8") as fh:
            fh.write(r.stdout)
        with open(os.path.join(SAIDA, cid + ".err"), "w", encoding="utf-8") as fh:
            fh.write(r.stderr)
        with open(os.path.join(SAIDA, cid + ".q.txt"), "w", encoding="utf-8") as fh:
            fh.write(padrao)
        try:
            d = json.loads(r.stdout)
            resumo.append(dict(id=cid, padrao=padrao, n=d.get("n"), cabeca=d.get("cabeca"), n_registros=d.get("n_registros"),
                               rotas=[x["rota_id"] for x in d.get("rotas", [])], codigo=r.returncode))
        except Exception as e:  # falha visivel, nunca 'ok' falso
            resumo.append(dict(id=cid, padrao=padrao, erro=repr(e), codigo=r.returncode))
    depois = dict(sha256=sha256(LIVRO), bytes=os.path.getsize(LIVRO), quando_local=time.strftime("%Y-%m-%d %H:%M:%S"))
    out = dict(documento="consultas so-leitura ao mapa de rotas (rodada 2, construtor optico)", livro=LIVRO,
               livro_antes=antes, livro_depois=depois, livro_inalterado=(antes["sha256"] == depois["sha256"]),
               consultas=resumo)
    with open(os.path.join(SAIDA, "RESUMO_CONSULTAS.json"), "w", encoding="utf-8") as fh:
        json.dump(out, fh, ensure_ascii=False, indent=1)
    print(json.dumps(out, ensure_ascii=False, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
