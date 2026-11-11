# -*- coding: utf-8 -*-
"""_adapt_forkB_util_v410.py -- (claude-construtor-v410, fork B, 06/11/2026) apoio dos adaptadores do fork B: sobre _adapt_util_v410.aplicar (backup de bytes, contagem exata, CRLF, ast/sh -n),
acrescenta (1) `linha(p, prefixo)`: a linha INTEIRA do arquivo que comeca com `prefixo` (tem de ser unica), para trocar linha por linha sem redigitar o texto antigo; (2) as trocas GENERICAS das notas herdadas
que o bump subiu de rotulo (a nota da adaptacao da v408 pelo fork C de 04/11 e a reconferencia do fork B da v409 em 05/11 passavam a dizer v409/v410: o rotulo verdadeiro volta)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v410 import aplicar  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
NOTA_FORKB = "conferido e adaptado em 06/11/2026 pelo fork B do claude-construtor-v410 (_adapt_forkB_*_v410.py)"


def caminho(rel):
    return os.path.join(HERE, *rel.replace("\\", "/").split("/"))


def texto(rel):
    return open(caminho(rel), "rb").read().decode("utf-8")


def linha(rel, prefixo):
    ls = [l.rstrip("\r") for l in texto(rel).split("\n") if l.startswith(prefixo)]
    assert len(ls) == 1, ("a linha nao e' unica", rel, prefixo[:80], len(ls))
    return ls[0]


def herdadas(rel, depois_de=()):
    """as trocas genericas das notas herdadas (contagem lida no texto JA com as trocas explicitas `depois_de`; zero ocorrencias = nenhuma troca)."""
    t = texto(rel)
    crlf = "\r\n" in t and t.count("\r\n") == t.count("\n")
    for a, b, _n in depois_de:
        if crlf:
            a, b = a.replace("\r\n", "\n").replace("\n", "\r\n"), b.replace("\r\n", "\n").replace("\n", "\r\n")
        t = t.replace(a, b)
    out = []
    for a, b in (("(nota herdada da adaptacao da v409 [fork C, 04/11/2026], com os rotulos subidos; reconferida em 05/11/2026 pelo fork B do claude-construtor-v410)",
                  "(nota herdada da adaptacao da v408 [fork C, 04/11/2026], reconferida em 05/11/2026 pelo fork B do claude-construtor-v409 e em 06/11/2026 pelo fork B do claude-construtor-v410, com os rotulos subidos)"),
                 ("(nota herdada da adaptacao da v409 [fork C da cadeia v409], com os rotulos subidos; reconferida em 05/11/2026 pelo fork B do claude-construtor-v410)",
                  "(nota herdada da adaptacao da v408 [fork C da cadeia v408], reconferida em 05/11/2026 pelo fork B do claude-construtor-v409 e em 06/11/2026 pelo fork B do claude-construtor-v410, com os rotulos subidos)")):
        n = t.count(a)
        if n:
            out.append((a, b, n))
    return out


def adaptar(rel, trocas, nota):
    return aplicar(caminho(rel), list(trocas) + herdadas(rel, trocas), nota=nota)
