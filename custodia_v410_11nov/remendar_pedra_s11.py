# -*- coding: utf-8 -*-
r"""Errata AO LADO na pedra generica (custodia_generica.py, S11), 11/11/2026, claude-site-custodia: a mesma regra dos contratos de REGISTRO
da errata do fatos.py, implementada de novo aqui (a pedra audita os fatos; nao importa fatos.py). A pedra confere tambem que a lista de
registro que ela acha e IGUAL a declarada nos fatos. Edita em bytes, preserva CRLF. Backup de bytes antes."""
import os
import shutil
import sys
import time

P = r"C:\IALD\Central de Patentes\tools\custodia_g1\generico\custodia_generica.py"
b = open(P, "rb").read()
assert b.count(b"\r\n") == b.count(b"\n"), "nao e CRLF puro"
shutil.copy2(P, P + ".bak_" + time.strftime("%Y%m%d_%H%M%S") + "_contratos_de_registro")
t = b.decode("utf-8").replace("\r\n", "\n")

A1 = r'''import copy
import hashlib'''
N1 = r'''import ast
import copy
import hashlib'''
A2 = r'''# =================================================================== a semântica pura (roda também sobre as cópias injetadas)'''
N2 = r'''_CHAVES_KERNEL_PEDRA = ("theorems", "declarations", "declaration_sources", "stone")


def _contratos_registro(um_text, contratos):
    r"""[AO LADO, 11/11/2026, claude-site-custodia; o C4 da v410 parou no S11] Contrato de REGISTRO (pré-registro de teste, recibo
    documental): sem expected_ladder, literal Python e sem nenhuma chave de conteúdo de kernel. Implementação própria da pedra (não importa
    fatos.py). Contrato de kernel sem a escada, ou não literal, NÃO é de registro: o S11 segue reprovando nele."""
    out = []
    for nome, x in sorted(contratos.items()):
        if x is not None:
            continue
        m = re.search(r"^%s\s*=\s*" % re.escape(nome), um_text, re.M)
        prox = re.compile(r"\n(?=[A-Za-z_@#])").search(um_text, m.end())
        try:
            d = ast.literal_eval(um_text[m.end(): prox.start() if prox else len(um_text)].strip())
        except (ValueError, SyntaxError):
            continue
        if isinstance(d, dict) and "expected_ladder" not in d and not any(k in d for k in _CHAVES_KERNEL_PEDRA):
            out.append(nome)
    return out


# =================================================================== a semântica pura (roda também sobre as cópias injetadas)'''
A3 = r'''    contratos = _contratos(um_text)
    chk("S11_contratos", contratos == F["contratos_expected_ladder"] and all(x == F["escada"]["esperadas"] for x in contratos.values()),
        F["escada"]["esperadas"], contratos)'''
N3 = r'''    contratos = _contratos(um_text)
    reg_pedra = _contratos_registro(um_text, contratos)    # AO LADO (11/11/2026, v410): os de registro saem da escada e conferem com os fatos
    contratos = {k: x for k, x in contratos.items() if k not in reg_pedra}
    chk("S11_contratos", contratos == F["contratos_expected_ladder"] and all(x == F["escada"]["esperadas"] for x in contratos.values())
        and reg_pedra == list(F.get("contratos_de_registro") or []),
        {"escada": F["escada"]["esperadas"], "registro": list(F.get("contratos_de_registro") or [])}, {"escada": contratos, "registro": reg_pedra})'''
for a, n in ((A1, N1), (A2, N2), (A3, N3)):
    k = t.count(a)
    if k != 1:
        sys.exit("trecho encontrado %d vezes: %r" % (k, a[:80]))
    t = t.replace(a, n, 1)
nb = t.replace("\n", "\r\n").encode("utf-8")
tmp = P + ".tmp"
open(tmp, "wb").write(nb)
assert os.path.getsize(tmp) == len(nb)
os.replace(tmp, P)
print(len(b), "->", len(nb), "B | CRLF", nb.count(b"\r\n"), "| LF solto", nb.count(b"\n") - nb.count(b"\r\n"))
