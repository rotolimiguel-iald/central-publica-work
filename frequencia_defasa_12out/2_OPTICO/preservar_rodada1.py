# -*- coding: utf-8 -*-
"""PRESERVACAO DA RODADA 1 do construtor optico (F1.FREQUENCIA, trilha POSTO).

A pasta 2_OPTICO ja continha uma execucao anterior completa deste mesmo passo (12/10, 13:31-13:56 local),
referenciada por hash pela 3_KERNEL e pela 4_RELATORIO. Esta rodada 2 (o workflow foi retomado com
«prossiga») reconstroi o ensaio do zero. Regra da casa: correcao ao lado, nunca por cima; backup de BYTES.

O que este script faz (so dentro de 2_OPTICO):
  1. lista TODO arquivo ja existente na pasta (caminho relativo, tamanho, mtime_ns, sha256 dos bytes);
  2. MOVE (rename, preserva bytes e mtime) cada entrada de topo para rodada1_20261012_1356/;
  3. recalcula o sha256 de cada arquivo movido e confere byte a byte com a listagem;
  4. grava PRESERVACAO_RODADA1.json (topo) e rodada1_20261012_1356/MANIFESTO_RODADA1.json.
Falha de conferencia = falha visivel (codigo 2); nada e apagado.
"""
import hashlib
import json
import os
import sys
import time

AQUI = os.path.dirname(os.path.abspath(__file__))
DEST_NOME = "rodada1_20261012_1356"
DEST = os.path.join(AQUI, DEST_NOME)
EU = os.path.basename(os.path.abspath(__file__))


def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for bloco in iter(lambda: fh.read(1 << 20), b""):
            h.update(bloco)
    return h.hexdigest()


def listar(base, ignorar_topo):
    out = []
    for dp, dns, fns in os.walk(base):
        dns.sort()
        rel_dp = os.path.relpath(dp, base)
        if rel_dp == ".":
            dns[:] = [d for d in dns if d not in ignorar_topo]
        for fn in sorted(fns):
            if rel_dp == "." and fn in ignorar_topo:
                continue
            p = os.path.join(dp, fn)
            st = os.stat(p)
            out.append(dict(rel=os.path.relpath(p, base).replace("\\", "/"), bytes=st.st_size,
                            mtime_ns=st.st_mtime_ns, sha256=sha256(p)))
    return out


def main():
    if os.path.exists(DEST):
        print("FALHA VISIVEL: destino ja existe, nao sobrescrevo: " + DEST, file=sys.stderr)
        return 2
    ignorar = {EU}
    antes = listar(AQUI, ignorar)
    topo = sorted(e for e in os.listdir(AQUI) if e not in ignorar)
    if not antes:
        print("nada a preservar")
        return 0
    os.makedirs(DEST)
    for e in topo:
        os.rename(os.path.join(AQUI, e), os.path.join(DEST, e))
    depois = {d["rel"]: d for d in listar(DEST, set())}
    divergencias = []
    for a in antes:
        d = depois.get(a["rel"])
        if d is None or d["sha256"] != a["sha256"] or d["bytes"] != a["bytes"] or d["mtime_ns"] != a["mtime_ns"]:
            divergencias.append(dict(rel=a["rel"], antes=a, depois=d))
    manifesto = dict(
        documento="PRESERVACAO DA RODADA 1 do construtor optico (F1.FREQUENCIA, trilha POSTO)",
        quando_local=time.strftime("%Y-%m-%d %H:%M:%S"),
        motivo=("workflow retomado ('prossiga'); a rodada 2 reconstroi o ensaio do zero; a rodada 1 fica AO LADO, "
                "byte a byte, porque a 3_KERNEL e a 4_RELATORIO a citam por hash"),
        origem=AQUI,
        destino=DEST,
        entradas_de_topo_movidas=topo,
        n_arquivos=len(antes),
        arquivos=antes,
        conferencia_byte_a_byte=("OK" if not divergencias else "DIVERGENCIA"),
        divergencias=divergencias,
    )
    txt = json.dumps(manifesto, ensure_ascii=False, indent=1)
    for p in (os.path.join(DEST, "MANIFESTO_RODADA1.json"), os.path.join(AQUI, "PRESERVACAO_RODADA1.json")):
        tmp = p + ".tmp"
        with open(tmp, "w", encoding="utf-8") as fh:
            fh.write(txt)
        if os.path.getsize(tmp) <= 0:
            print("FALHA VISIVEL: manifesto vazio", file=sys.stderr)
            return 2
        os.replace(tmp, p)
    print(json.dumps(dict(n_arquivos=len(antes), topo=topo, conferencia=manifesto["conferencia_byte_a_byte"]),
                     ensure_ascii=False, indent=1))
    return 0 if not divergencias else 2


if __name__ == "__main__":
    sys.exit(main())
