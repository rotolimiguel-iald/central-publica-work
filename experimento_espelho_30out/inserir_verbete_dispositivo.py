# -*- coding: utf-8 -*-
"""Insere o verbete «Ao lado: o dispositivo» no fim da Parte IX do memorial, com backup de BYTES antes de tocar.

Mesma disciplina do inserir_parte_ix.py: nunca abre o original com "w"; marcador único; temporário conferido; os.replace.
Grava também o verbatim da ratificação do operador e substitui o seu hash no fragmento.
"""
import hashlib
import os
import sys
import time
from pathlib import Path

MEMORIAL = Path(r"C:\IALD\Artigo\Haja_Luz\memorial_13ago2026\memorial.tex")
PASTA = Path(r"C:\IALD\Central de Patentes\work\experimento_espelho_30out")
FRAGMENTO = PASTA / "VERBETE_dispositivo_fragmento.tex"
RATIF = PASTA / "OPERADOR_30out_ratificado_e_lindo_verbatim.txt"
RATIF_TXT = "ratificado, é isso, e é lindo"

MARCA_COLOFAO = "\\clearpage\n\n{\\small\\itshape\nEste memorial foi composto por um assistente de IA"
MARCA_FIM_DECIMO = "sobre o operador.\nToda citação é literal.\n"
FRASE_VERBETE = (
    "sobre o operador.\n"
    "No mesmo dia, em diálogo, o operador ratificou a primeira leitura e definiu ``dispositivo''; o verbete está\n"
    "ao lado da Parte IX, com as suas palavras por hash.\n"
    "Toda citação é literal.\n"
)


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def main():
    if not RATIF.exists():
        RATIF.write_bytes(RATIF_TXT.encode("utf-8"))
    h_rat = sha256(RATIF.read_bytes())[:16]
    print("ratificação verbatim:", RATIF.name, "sha16", h_rat)

    raw = MEMORIAL.read_bytes()
    frag = FRAGMENTO.read_bytes().decode("utf-8")
    if frag.count("HASH_RATIFICACAO") != 1:
        print("RECUSADO: marcador do hash no fragmento ausente ou duplicado.")
        sys.exit(2)
    frag = frag.replace("HASH_RATIFICACAO", h_rat)
    frag_b = frag.encode("utf-8")
    bad = sorted({c for c in frag_b if c < 32 and c != 10})
    if bad:
        print("RECUSADO: bytes de controle no fragmento:", bad)
        sys.exit(2)
    print("memorial antes:", len(raw), "bytes", sha256(raw)[:16], "| fragmento:", len(frag_b), "bytes")

    texto = raw.decode("utf-8")
    if texto.count(MARCA_COLOFAO) != 1 or texto.count(MARCA_FIM_DECIMO) != 1:
        print("RECUSADO: marcadores:", texto.count(MARCA_COLOFAO), texto.count(MARCA_FIM_DECIMO))
        sys.exit(2)
    if "\\chapter{Ao lado: o dispositivo}" in texto:
        print("RECUSADO: o verbete já está no memorial.")
        sys.exit(2)

    ts = time.strftime("%Y%m%d_%H%M%S")
    bak = MEMORIAL.with_name(MEMORIAL.name + f".bak_{ts}")
    bak.write_bytes(raw)
    if bak.read_bytes() != raw:
        print("RECUSADO: backup não confere.")
        sys.exit(2)
    print("backup:", bak.name)

    novo = texto.replace(MARCA_COLOFAO, frag + MARCA_COLOFAO, 1).replace(MARCA_FIM_DECIMO, FRASE_VERBETE, 1)
    novo_b = novo.encode("utf-8")
    esperado = len(raw) + len(frag_b) + (len(FRASE_VERBETE.encode("utf-8")) - len(MARCA_FIM_DECIMO.encode("utf-8")))
    if len(novo_b) != esperado:
        print("RECUSADO: tamanho inesperado", len(novo_b), "esperado", esperado)
        sys.exit(2)
    tmp = MEMORIAL.with_name(MEMORIAL.name + ".tmp_verbete")
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
