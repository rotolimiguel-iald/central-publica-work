# -*- coding: utf-8 -*-
"""Insere a Parte IX no memorial.tex com backup de BYTES antes de tocar (regra de 22/08 + emenda de 29/08).

Nunca abre o original com "w". Lê bytes, grava backup de bytes, monta o novo conteúdo em memória,
grava num temporário, confere o tamanho e só então substitui. Qualquer marcador ausente ou duplicado
aborta sem tocar o original.
"""
import hashlib
import os
import sys
import time
from pathlib import Path

MEMORIAL = Path(r"C:\IALD\Artigo\Haja_Luz\memorial_13ago2026\memorial.tex")
FRAGMENTO = Path(r"C:\IALD\Central de Patentes\work\experimento_espelho_30out\PARTE_IX_fragmento.tex")

# Marcador 1: o colofão final começa aqui (a Parte IX entra ANTES dele).
MARCA_COLOFAO = "\\clearpage\n\n{\\small\\itshape\nEste memorial foi composto por um assistente de IA"
# Marcador 2: a última frase do colofão antes de "Toda citação é literal."
MARCA_FIM_NONO = "incluindo três erratas que o compilador deve a si mesmo sobre o refrão do gate.\nToda citação é literal.\n"
FRASE_DECIMO = (
    "incluindo três erratas que o compilador deve a si mesmo sobre o refrão do gate.\n"
    "Um décimo levantamento, em 30 de outubro de 2026, foi feito por um leitor sem nenhuma memória da\n"
    "conversa --- a sessão que compilou as Partes I a VIII foi apagada, e nenhuma cópia da sua\n"
    "transcrição foi encontrada em sete lugares medidos ---, que releu o memorial, a síntese e as cinco\n"
    "memórias que aquela sessão deixou fora de si, mediu o selo corrente e as cópias do cofre, releu as\n"
    "memórias do arco de \\texttt{v365} a \\texttt{v404}, conferiu a página inicial do site no ar e o\n"
    "estado do orquestrador, e produziu a Parte IX, incluindo o dado que a Parte VIII deixara pendente\n"
    "sobre o operador.\n"
    "Toda citação é literal.\n"
)


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def main():
    raw = MEMORIAL.read_bytes()
    frag = FRAGMENTO.read_bytes()
    print("memorial antes:", len(raw), "bytes", sha256(raw)[:16])
    print("fragmento:", len(frag), "bytes", sha256(frag)[:16])

    # Recusa bytes de controle no fragmento (a lição de 17/09: \t \r \a por heredoc).
    bad = sorted({c for c in frag if c < 32 and c not in (10,)})
    if bad:
        print("RECUSADO: bytes de controle no fragmento:", bad)
        sys.exit(2)
    if b"\r" in raw:
        print("AVISO: o memorial tem CRLF; preservando como está (contagem:", raw.count(b"\r\n"), ")")

    texto = raw.decode("utf-8")
    if texto.count(MARCA_COLOFAO) != 1:
        print("RECUSADO: marcador do colofão ausente ou duplicado:", texto.count(MARCA_COLOFAO))
        sys.exit(2)
    if texto.count(MARCA_FIM_NONO) != 1:
        print("RECUSADO: marcador do nono levantamento ausente ou duplicado:", texto.count(MARCA_FIM_NONO))
        sys.exit(2)
    if "\\part{O espelho apagado}" in texto:
        print("RECUSADO: a Parte IX já está no memorial.")
        sys.exit(2)

    # Backup de BYTES, mesma pasta, do estado que está sendo tocado.
    ts = time.strftime("%Y%m%d_%H%M%S")
    bak = MEMORIAL.with_name(MEMORIAL.name + f".bak_{ts}")
    bak.write_bytes(raw)
    if bak.read_bytes() != raw:
        print("RECUSADO: backup não confere byte a byte.")
        sys.exit(2)
    print("backup:", bak.name, len(raw), "bytes")

    frag_txt = frag.decode("utf-8")
    novo = texto.replace(MARCA_COLOFAO, frag_txt + MARCA_COLOFAO, 1)
    novo = novo.replace(MARCA_FIM_NONO, FRASE_DECIMO, 1)
    novo_b = novo.encode("utf-8")
    esperado = len(raw) + len(frag) + (len(FRASE_DECIMO.encode("utf-8")) - len(MARCA_FIM_NONO.encode("utf-8")))
    if len(novo_b) != esperado:
        print("RECUSADO: tamanho inesperado", len(novo_b), "esperado", esperado)
        sys.exit(2)

    tmp = MEMORIAL.with_name(MEMORIAL.name + ".tmp_parte_ix")
    tmp.write_bytes(novo_b)
    if tmp.stat().st_size != len(novo_b) or tmp.read_bytes() != novo_b:
        print("RECUSADO: temporário não confere.")
        sys.exit(2)
    os.replace(tmp, MEMORIAL)
    depois = MEMORIAL.read_bytes()
    print("memorial depois:", len(depois), "bytes", sha256(depois)[:16], "cresceu", len(depois) - len(raw))
    if len(depois) <= len(raw):
        print("FALHA: o arquivo não cresceu; restaurando do backup.")
        MEMORIAL.write_bytes(raw)
        sys.exit(2)
    print("OK")


if __name__ == "__main__":
    main()
