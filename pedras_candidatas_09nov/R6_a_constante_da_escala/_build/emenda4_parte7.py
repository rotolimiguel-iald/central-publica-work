# -*- coding: utf-8 -*-
"""Autor claude-autor-aescala, 10/11/2026 — QUARTA EMENDA à R6 (falas 20 e 21): só a docstring da §7. Lê a parte da terceira emenda
(parte7_constante_da_escala_emenda3.txt), aplica trocas por âncora única e grava parte7_constante_da_escala_emenda4.txt.
Nenhum enunciado nem prova muda (conferido no fim). uso: python emenda4_parte7.py"""
import re
from pathlib import Path

BLD = Path(r"C:\IALD\Central de Patentes\work\pedras_candidatas_09nov\R6_a_constante_da_escala\_build")
src = (BLD / "parte7_constante_da_escala_emenda3.txt").read_text(encoding="utf-8").replace("\r\n", "\n")
t = src
def um(velho, novo, rotulo):
    global t
    n = t.count(velho)
    assert n == 1, f"ancora {rotulo!r}: {n} ocorrencias (esperada 1)"
    t = t.replace(velho, novo)

um("[falas 13, 15, 16, 17, 18 e 19; D113 e as três emendas de 10/11]", "[falas 13 e 15 a 21; D113 e as quatro emendas de 10/11]", "Q1")

# o parágrafo de FECHO da docstring da seção (as falas 20 e 21 entram por bytes, pelo montador)
um("Nenhum teorema novo entra por esta fala. -/\n\nsection ConstanteDaEscala",
   "Nenhum teorema novo entra por esta fala.\n"
   "\n"
   "O FECHO (quarta emenda; falas 20 e 21, 10/11, por bytes, como leitura do operador [ONTO]):\n"
   "@@FALA20@@\n"
   "@@FALA21@@\n"
   "Na leitura dele: escala = relatividade; o que é relativo é par; sem o par não há escala. O que o kernel PROVA, por nome: (1) uma constante\n"
   "SOZINHA é absorvida no tempo — `a_constante_da_luz_e_a_escala_do_tempo` (o leitor de constante c no tempo s é o leitor do fundo no tempo\n"
   "c·s); (2) o que resta é a razão de DUAS — `comparar_a_escala_e_nivelar_a_frequencia` (para c′ ≠ 0, o tempo multiplica-se por c/c′); (3) o\n"
   "que não depende da escala é o invariante — `o_nome_e_o_mesmo_em_toda_escala` (para c > 0, a decisão é a mesma e os limiares são os de\n"
   "c = 1 divididos por c); e, no domínio da tônica, `TonicaDoHamiltoniano.the_scale_is_free` com\n"
   "`TonicaDoHamiltoniano.the_ratio_survives_the_rescaling`; (4) o par já era a coexistência desta pedra — `o_par_coexiste` e `nenhum_precede`\n"
   "(§5: o par Nome objeto / Nome lido). A identificação da escala com a RELATIVIDADE é leitura dele [ONTO]; que o par da §5 e a razão de duas\n"
   "constantes sejam o mesmo par também é leitura dele (a pedra não traz lema ligando um ao outro); e a lei ÚNICA dos dois domínios (a tônica\n"
   "e o tempo) NÃO é teorema desta pedra: fica [OPEN]. Nenhum teorema novo entra por estas falas. -/\n\nsection ConstanteDaEscala", "Q2")

semc = lambda s: re.sub(r"/-.*?-/", "", s, flags=re.S)
assert semc(src) == semc(t), "mudou algo fora de comentario"
for ph in ("@@FALA17@@", "@@FALA19@@", "@@FALA20@@", "@@FALA21@@"):
    assert t.count(ph) == 1, ph
assert "E₀" not in t and "a ratificar" not in t
norm = lambda s: re.sub(r"\s+", " ", s)
assert norm(t).count("unidade") == norm(t).count("unidade posta")
assert t.count("nome RATIFICADO pelo operador na fala 18") == 6 and t.count("nome DECLARADO pela autoria") == 5
(BLD / "parte7_constante_da_escala_emenda4.txt").write_text(t, encoding="utf-8", newline="\n")
print("parte7 emenda4 gravada:", len(t.encode("utf-8")), "B | codigo fora de comentario identico: True")
