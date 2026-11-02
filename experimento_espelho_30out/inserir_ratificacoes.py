# -*- coding: utf-8 -*-
"""Insere o capítulo «Ao lado: as oito leituras, respondidas» e o apêndice «A identidade» no fim da Parte IX, com backup de BYTES.

Mesma disciplina dos dois scripts anteriores: nunca abre o original com "w"; marcadores únicos; temporário conferido; os.replace.
Confere os hashes verbatim citados no fragmento contra os arquivos da pasta (régua nº 2: hash nunca de memória).
"""
import hashlib
import os
import re
import sys
import time
from pathlib import Path

MEMORIAL = Path(r"C:\IALD\Artigo\Haja_Luz\memorial_13ago2026\memorial.tex")
PASTA = Path(r"C:\IALD\Central de Patentes\work\experimento_espelho_30out")
FRAGMENTO = PASTA / "RATIFICACOES_fragmento.tex"

MARCA_COLOFAO = "\\clearpage\n\n{\\small\\itshape\nEste memorial foi composto por um assistente de IA"
MARCA_FIM = "ao lado da Parte IX, com as suas palavras por hash.\nToda citação é literal.\n"
FRASE_NOVA = (
    "ao lado da Parte IX, com as suas palavras por hash.\n"
    "Ainda em 30 de outubro, o operador respondeu às oito leituras da Parte IX, uma por vez: seis ratificadas, uma\n"
    "conjectura corrigida, uma recusada; as respostas, e o texto ``A identidade'' que ele enviou, estão ao lado, por hash.\n"
    "Toda citação é literal.\n"
)


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def main():
    raw = MEMORIAL.read_bytes()
    frag_b = FRAGMENTO.read_bytes()
    frag = frag_b.decode("utf-8")
    bad = sorted({c for c in frag_b if c < 32 and c != 10})
    if bad:
        print("RECUSADO: bytes de controle no fragmento:", bad)
        sys.exit(2)

    # Régua nº 2: cada sha16 citado no fragmento tem de bater com um arquivo verbatim da pasta.
    hashes = {sha256(p.read_bytes())[:16] for p in PASTA.glob("OPERADOR_30out_*_verbatim.txt")}
    citados = set(re.findall(r"\\texttt\{([0-9a-f]{16})\}", frag))
    faltam = citados - hashes
    if faltam:
        print("RECUSADO: hashes citados sem arquivo verbatim correspondente:", sorted(faltam))
        sys.exit(2)
    print("hashes citados:", len(citados), "todos conferidos contra os arquivos")

    texto = raw.decode("utf-8")
    if texto.count(MARCA_COLOFAO) != 1 or texto.count(MARCA_FIM) != 1:
        print("RECUSADO: marcadores:", texto.count(MARCA_COLOFAO), texto.count(MARCA_FIM))
        sys.exit(2)
    if "\\chapter{Ao lado: as oito leituras, respondidas}" in texto:
        print("RECUSADO: o capítulo já está no memorial.")
        sys.exit(2)

    ts = time.strftime("%Y%m%d_%H%M%S")
    bak = MEMORIAL.with_name(MEMORIAL.name + f".bak_{ts}")
    bak.write_bytes(raw)
    if bak.read_bytes() != raw:
        print("RECUSADO: backup não confere.")
        sys.exit(2)
    print("memorial antes:", len(raw), "bytes", sha256(raw)[:16], "| backup:", bak.name, "| fragmento:", len(frag_b), "bytes")

    novo = texto.replace(MARCA_COLOFAO, frag + MARCA_COLOFAO, 1).replace(MARCA_FIM, FRASE_NOVA, 1)
    novo_b = novo.encode("utf-8")
    esperado = len(raw) + len(frag_b) + (len(FRASE_NOVA.encode("utf-8")) - len(MARCA_FIM.encode("utf-8")))
    if len(novo_b) != esperado:
        print("RECUSADO: tamanho inesperado", len(novo_b), "esperado", esperado)
        sys.exit(2)
    tmp = MEMORIAL.with_name(MEMORIAL.name + ".tmp_ratif")
    tmp.write_bytes(novo_b)
    if tmp.read_bytes() != novo_b:
        print("RECUSADO: temporário não confere.")
        sys.exit(2)
    os.replace(tmp, MEMORIAL)
    depois = MEMORIAL.read_bytes()
    print("memorial depois:", len(depois), "bytes", sha256(depois)[:16], "cresceu", len(depois) - len(raw))
    print("OK" if len(depois) > len(raw) else "FALHA")


if __name__ == "__main__":
    main()
