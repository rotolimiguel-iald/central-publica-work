# -*- coding: utf-8 -*-
"""Autor claude-autor-aescala, 10/11/2026 — SEXTA EMENDA à R6 na parte da §7 (só comentário) e a NOTA da gerência (fala 24: o operador
RATIFICOU o nome `o_nome_e_a_singularidade_da_informacao`). Lê parte7_constante_da_escala_emenda5.txt e grava ..._emenda6.txt.
As três frases antigas da sexta emenda (EP-02, EP-08, PAR-11) ficam nas seções 1 a 6 e no cabeçalho: quem as troca é o montador.
Nenhum enunciado nem prova muda (conferido no fim). uso: python emenda6_parte7.py"""
import re
from pathlib import Path

BLD = Path(r"C:\IALD\Central de Patentes\work\pedras_candidatas_09nov\R6_a_constante_da_escala\_build")
src = (BLD / "parte7_constante_da_escala_emenda5.txt").read_text(encoding="utf-8").replace("\r\n", "\n")
t = src
def um(velho, novo, rotulo):
    global t
    n = t.count(velho)
    assert n == 1, f"ancora {rotulo!r}: {n} ocorrencias (esperada 1)"
    t = t.replace(velho, novo)

um("[falas 13 e 15 a 23; D113 e as cinco emendas de 10/11]", "[falas 13 e 15 a 24; D113 e as seis emendas de 10/11]", "S1")
um("sai da frase do operador (falas 22 e 23) e está [DECLARADO; a ratificar pelo operador];",
   "sai da frase do operador (falas 22 e 23) e foi RATIFICADO por ele em 10/11/2026 (fala 24: @@FALA24@@);", "S2")
um("«o Nome é a singularidade da informação» [falas 22 e 23]\n", "«o Nome é a singularidade da informação» [falas 22, 23 e 24]\n", "S3")
um("β = α·√e a esta informação: fica [OPEN] (ver O FECHO, na abertura da seção). -/\n\nsection SingularidadeDaInformacao",
   "β = α·√e a esta informação: fica [OPEN] (ver O FECHO, na abertura da seção).\n"
   "O NOME do teorema foi RATIFICADO pelo operador (fala 24, 10/11/2026, por bytes): @@FALA24@@. -/\n\nsection SingularidadeDaInformacao", "S4")
um("a frase do operador é o NOME do teorema; nome DECLARADO; a ratificar pelo operador] —",
   "a frase do operador é o NOME do teorema; nome RATIFICADO pelo operador na fala 24: @@FALA24@@] —", "S5")

def semc2(s):
    out, i, n, prof = [], 0, len(s), 0
    while i < n:
        if s.startswith("/-", i):
            prof += 1; i += 2; continue
        if prof and s.startswith("-/", i):
            prof -= 1; i += 2; continue
        if prof:
            i += 1; continue
        if s.startswith("--", i):
            j = s.find("\n", i)
            i = n if j < 0 else j
            continue
        out.append(s[i]); i += 1
    assert prof == 0
    return re.sub(r"[ \t]+\n", "\n", "".join(out))
assert semc2(src) == semc2(t), "mudou algo fora de comentario"
assert "a ratificar" not in t and t.count("@@FALA24@@") == 3
assert t.count("nome RATIFICADO pelo operador na fala 18") == 6 and t.count("nome RATIFICADO pelo operador na fala 24") == 1
assert t.count("nome DECLARADO pela autoria") == 6
for ph in ("@@FALA17@@", "@@FALA19@@", "@@FALA20@@", "@@FALA21@@", "@@FALA22@@", "@@FALA23@@"):
    assert t.count(ph) == 1, ph
(BLD / "parte7_constante_da_escala_emenda6.txt").write_text(t, encoding="utf-8", newline="\n")
print("parte7 emenda6 gravada:", len(t.encode("utf-8")), "B | codigo fora de comentario identico ao da emenda5: True")
