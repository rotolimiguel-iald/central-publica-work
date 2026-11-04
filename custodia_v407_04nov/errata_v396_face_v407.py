# -*- coding: utf-8 -*-
"""Errata ao lado na checagem `face_de_fock_dita_condicional` da camada v396 do modulo comum dos 16 dispositivos (custodia v407, 04/11/2026, claude-site-custodia).
Molde: a errata da v406 (03/11, gerencia c1). As duas formas antigas ficam; entra uma terceira, a da v407. Backup de BYTES; temporario, conferencia, os.replace."""
import os
import py_compile
import time
from pathlib import Path

P = Path(r"C:\IALD\Central de Patentes\patents\_formula_completa\tgl_formula_completa.py")
b = P.read_bytes()
t = b.decode("utf-8")
CR, LF = chr(13), chr(10)
eol = CR + LF if (CR + LF) in t else LF
I = " " * 41
J = " " * 45
A = J + 'and (core.get("fechamento_v406") or {}).get("certificate_inhabited") is True),' + eol
L = [
    J + 'and (core.get("fechamento_v406") or {}).get("certificate_inhabited") is True)',
    I + "# ERRATA AO LADO (04/11/2026, custodia v407, claude-site-custodia, em nome proprio): desde a v407 a chave linked_to_the_corner_by_a_lemma",
    I + "# e LIDA do kernel do rito (TGLExt.PsionCanto.the_psion_is_the_corner_on_both_faces; errata E18; registro psion_canto_v407). Aceita-se TAMBEM",
    I + "# o mesmo status V406 com a chave True, desde que o elo seja esse lema, de ESTRUTURA e nao de vetores (Omega e o vetor de Bell nao identificados),",
    I + "# com o registro psion_canto_v407 verificado. As duas formas acima ficam como registro; o nome da checagem nao muda.",
    I + 'or (fo.get("status") == "INHABITED_BY_physicalFockCertificate_V406" and fo.get("inhabitant_exhibited") is True',
    J + 'and bool(fo.get("reading_v396")) and fo.get("linked_to_the_corner_by_a_lemma") is True',
    J + 'and (fo.get("elo_v407") or {}).get("lemma") == "TGLExt.PsionCanto.the_psion_is_the_corner_on_both_faces"',
    J + 'and (fo.get("elo_v407") or {}).get("kind") == "STRUCTURE_NOT_VECTORS"',
    J + 'and (fo.get("elo_v407") or {}).get("identifies_omega_with_bell_vector") is False',
    J + 'and (core.get("psion_canto_v407") or {}).get("all_verified") is True',
    J + 'and (core.get("fechamento_v406") or {}).get("certificate_inhabited") is True),',
]
N = eol.join(L) + eol
assert t.count(A) == 1, t.count(A)
novo = t.replace(A, N).encode("utf-8")
P.with_name(P.name + ".bak_v407_errata_face_" + time.strftime("%Y%m%d_%H%M%S")).write_bytes(b)
tmp = P.with_name(P.name + ".tmp")
tmp.write_bytes(novo)
assert tmp.stat().st_size == len(novo)
os.replace(tmp, P)
py_compile.compile(str(P), doraise=True)
print("ok", len(b), "->", len(novo))
