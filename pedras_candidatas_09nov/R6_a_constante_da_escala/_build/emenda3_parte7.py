# -*- coding: utf-8 -*-
"""Autor claude-autor-aescala, 10/11/2026 — TERCEIRA EMENDA à R6 (fala 19): só docstrings da §7. Lê a parte da segunda emenda
(parte7_constante_da_escala_emenda2.txt), aplica trocas por âncora única e grava parte7_constante_da_escala_emenda3.txt.
Nenhum enunciado nem prova muda (conferido no fim). uso: python emenda3_parte7.py"""
import re
from pathlib import Path

BLD = Path(r"C:\IALD\Central de Patentes\work\pedras_candidatas_09nov\R6_a_constante_da_escala\_build")
src = (BLD / "parte7_constante_da_escala_emenda2.txt").read_text(encoding="utf-8").replace("\r\n", "\n")
t = src
def um(velho, novo, rotulo):
    global t
    n = t.count(velho)
    assert n == 1, f"ancora {rotulo!r}: {n} ocorrencias (esperada 1)"
    t = t.replace(velho, novo)

um("[falas 13, 15, 16, 17 e 18; D113 e as duas emendas de 10/11]", "[falas 13, 15, 16, 17, 18 e 19; D113 e as três emendas de 10/11]", "T1")

# o parágrafo DOIS DOMÍNIOS, antes de «O QUE O KERNEL JÁ TEM» (a fala 19 entra por bytes, pelo montador)
um("\n\nO QUE O KERNEL JÁ TEM: `TraducaoTuring.a_fita_sem_escala`",
   "\n\nDOIS DOMÍNIOS (terceira emenda; fala 19, 10/11, por bytes, como leitura dele [ONTO]):\n"
   "@@FALA19@@\n"
   "O operador não vê contradição entre a pedra da v405 e esta seção: são dois domínios, cada um com a sua escala. O que o kernel tem em cada\n"
   "um, por nome: (1) no domínio da TÔNICA (a energia) a escala é a unidade posta — `TonicaDoHamiltoniano.the_scale_is_free` e\n"
   "`TonicaDoHamiltoniano.the_tonic_lands_on_the_posted_unit`, e `LeiDoDiminuto.tonica`; (2) no domínio do TEMPO — da computação, do\n"
   "processamento, da relatividade — a escala do observador é a constante desta seção: `leitorComConstante` e\n"
   "`a_constante_da_luz_e_a_escala_do_tempo`. São objetos DISTINTOS, e esta pedra NÃO deriva um do outro. Na cadeia\n"
   "(`tudo_depende_da_escala`), o item (i), `tonica κ 0 = 0`, fala da escala da tônica; o item (iv), `leitorComConstante 0 k s = 1`, fala da\n"
   "escala do tempo. E a frase da fala 17, «posto não é escala, posto é domínio», foi dita do LEITOR (o domínio do tempo); na tônica, pela\n"
   "fala 19, a escala é a unidade posta."
   "\n\nO QUE O KERNEL JÁ TEM: `TraducaoTuring.a_fita_sem_escala`", "T2")

# a docstring da cadeia e a do leitor: os dois domínios ditos onde a leitura poderia confundir
um("(vi) a nota principal modulada é zero ⟺ a nota principal é zero. [TEOREMA.] O que NÃO é termo:",
   "(vi) a nota principal modulada é zero ⟺ a nota principal é zero. [TEOREMA.] DOIS DOMÍNIOS\n"
   "    (fala 19): o item (i) fala da escala da TÔNICA, que é a unidade posta (`TonicaDoHamiltoniano.the_tonic_lands_on_the_posted_unit`); o item\n"
   "    (iv), da escala do TEMPO, a constante desta seção; a pedra não deriva uma da outra. O que NÃO é termo:", "T3")
um("o que a pedra tem de domínio é o tipo X dos pixels e a normalização `brilho k 0 = 1`. -/\ntheorem o_leitor_so_admite_uma_escala",
   "o que a pedra tem de domínio é o tipo X dos pixels e a normalização `brilho k 0 = 1`.\n"
   "    A frase foi dita do LEITOR (o domínio do tempo); na tônica, a escala é a unidade posta (fala 19; ver DOIS DOMÍNIOS na abertura da seção). -/\n"
   "theorem o_leitor_so_admite_uma_escala", "T4")
um("que o posto seja domínio (fala 17); e a cadeia como dependência FÍSICA",
   "que o posto seja domínio (fala 17); que a tônica e o tempo sejam dois domínios, cada um com a sua escala (fala 19); e a cadeia como\n"
   "dependência FÍSICA", "T5")

semc = lambda s: re.sub(r"/-.*?-/", "", s, flags=re.S)
assert semc(src) == semc(t), "mudou algo fora de comentario"
assert "@@FALA19@@" in t and "@@FALA17@@" in t
assert "E₀" not in t and "a ratificar" not in t
assert t.count("unidade") == t.count("unidade posta"), "a palavra so' entra como 'unidade posta'"
assert t.count("nome RATIFICADO pelo operador na fala 18") == 6 and t.count("nome DECLARADO pela autoria") == 5
# nenhuma frase da autoria diz que posto NUNCA é escala (a fala 17 fica por bytes, entre aspas angulares)
sem_aspas = re.sub("\u00ab[^\u00bb]*\u00bb", "", t)
for proib in ("posto nunca é escala", "posto não é escala", "nunca é escala"):
    assert proib not in sem_aspas.lower(), "frase da autoria a corrigir: " + proib
(BLD / "parte7_constante_da_escala_emenda3.txt").write_text(t, encoding="utf-8", newline="\n")
print("parte7 emenda3 gravada:", len(t.encode("utf-8")), "B | codigo fora de comentario identico: True | 'unidade posta':", t.count("unidade posta"))
