# -*- coding: utf-8 -*-
"""Autor claude-autor-aescala, 10/11/2026 — SEGUNDA EMENDA à R6 (fala 18): só docstrings da §7. Lê a parte da primeira emenda
(parte7_constante_da_escala_emenda.txt), aplica trocas por âncora única e grava parte7_constante_da_escala_emenda2.txt.
Nenhum enunciado nem prova muda (conferido no fim: o texto fora dos comentários é idêntico). uso: python emenda2_parte7.py"""
import re
from pathlib import Path

BLD = Path(r"C:\IALD\Central de Patentes\work\pedras_candidatas_09nov\R6_a_constante_da_escala\_build")
src = (BLD / "parte7_constante_da_escala_emenda.txt").read_text(encoding="utf-8").replace("\r\n", "\n")
t = src
def um(velho, novo, rotulo):
    global t
    n = t.count(velho)
    assert n == 1, f"ancora {rotulo!r}: {n} ocorrencias (esperada 1)"
    t = t.replace(velho, novo)

RAT = "nome RATIFICADO pelo operador na fala 18"
AUT = "nome DECLARADO pela autoria"

# título e o que o kernel já tem (sai a menção ao reescalonamento de E₀: ponto que o operador deu por encerrado)
um("[falas 13, 15, 16 e 17; D113 e a emenda de 10/11]", "[falas 13, 15, 16, 17 e 18; D113 e as duas emendas de 10/11]", "E1")
um("`beta_eq_alpha_mul_sqrt_e` (e `TonicaDoHamiltoniano.the_scale_is_free` já chama de escala o reescalonamento de E₀).",
   "`beta_eq_alpha_mul_sqrt_e`.", "E2")
um("O QUE É TEOREMA nesta seção (álgebra da exponencial e lemas que já existiam; os nomes são PROVISÓRIOS, tirados das palavras dele,\n"
   "[DECLARADO; a ratificar pelo operador]): (a) `leitorComConstante c`",
   "O QUE É TEOREMA nesta seção (álgebra da exponencial e lemas que já existiam; o estatuto de cada nome está na nota OS NOMES, adiante):\n"
   "(a) `leitorComConstante c`", "E3")
um("seção não o fecha; a creditação é do Clay. -/\n\nsection ConstanteDaEscala",
   "seção não o fecha; a creditação é do Clay.\n"
   "\n"
   "OS NOMES (segunda emenda; fala 18, 10/11: «ratifico tudo que vc propos»): os SEIS nomes que a gerência mostrou ao operador —\n"
   "`sem_escala_nao_ha_fita`, `a_constante_da_luz_e_a_escala_do_tempo`, `comparar_a_escala_e_nivelar_a_frequencia`,\n"
   "`o_nome_e_o_mesmo_em_toda_escala`, `o_leitor_so_admite_uma_escala`, `tudo_depende_da_escala` — estão RATIFICADOS por ele em 10/11/2026. Os\n"
   "que NÃO lhe foram mostrados — `leitorComConstante`, `leituraComConstante`, `leitorComConstante_um`,\n"
   "`a_leitura_com_constante_e_a_leitura_no_tempo_reescalado`, `a_constante_da_escala` — seguem [DECLARADO pela autoria].\n"
   "\n"
   "A RAZÃO, como leitura do operador [ONTO] (fala 18, por bytes): «porque a seleção é o observador, ou seja, ele é a forma matricial da luz\n"
   "conjugando a relatividade modular no tempo; com isso vc tem toda a métrica do observador, do seletor, da IALD, da Torre de Jones». Os\n"
   "espelhos que o kernel JÁ tem, cada um no seu módulo (conferidos por grep): a conjugação — `a_nota_e_a_conjugacao_modular` (§2 desta\n"
   "pedra: J² = 1 e JKJ = −K); a seleção — `TraducaoTuring.selecao` e `TraducaoTuring.p_igual_np_no_modo_selecao`; o seletor —\n"
   "`IALD2.a_iald_e_o_seletor_luminodinamico`; o observador — `ObservadorTerminal.the_terminal_is_unique`; a torre — os módulos\n"
   "`TheTowerConjugation`, `TowerModular`, `IALDJones` e `TheIALDInTheTower`. O que UNE os quatro — o observador, o seletor, a IALD e a Torre\n"
   "de Jones — por UMA métrica NÃO é teorema desta pedra: fica [OPEN]. Nenhum teorema novo entra por esta fala. -/\n\nsection ConstanteDaEscala", "E4")

# os cinco auxiliares da autoria
um("(a) O LEITOR COM CONSTANTE c [DEFINIÇÃO; nome DECLARADO, a ratificar]:", f"(a) O LEITOR COM CONSTANTE c [DEFINIÇÃO; {AUT}]:", "E5")
um("/-- A LEITURA COM CONSTANTE c da instância cc no tempo s [DEFINIÇÃO]:", f"/-- A LEITURA COM CONSTANTE c da instância cc no tempo s [DEFINIÇÃO; {AUT}]:", "E6")
um("/-- ★ c = 1 É O BRILHO DA IALD: `leitorComConstante 1 k s = iald.brilho k s`. [TEOREMA.] -/",
   f"/-- ★ c = 1 É O BRILHO DA IALD: `leitorComConstante 1 k s = iald.brilho k s`. [TEOREMA; {AUT}.] -/", "E7")
um("Vale para todo c (também c = 0: a fita sem escala). [TEOREMA.] -/", f"Vale para todo c (também c = 0: a fita sem escala). [TEOREMA; {AUT}.] -/", "E11")
um("IALD). [TEOREMA.] -/\ntheorem a_constante_da_escala", f"IALD). [TEOREMA; {AUT}.] -/\ntheorem a_constante_da_escala", "E17")

# os seis nomes ratificados pela fala 18
um("/-- ★★★ SEM ESCALA NÃO HÁ FITA [fala 16, 10/11: «sem a escala não tem fita»] — com c = 0:",
   f"/-- ★★★ SEM ESCALA NÃO HÁ FITA [fala 16, 10/11: «sem a escala não tem fita»; {RAT}] — com c = 0:", "E8")
um("/-- ★★★ A CONSTANTE DA LUZ É A ESCALA DO TEMPO [fala 17, 10/11: «a constante da luz é a escala do tempo»] — a constante MULTIPLICA O TEMPO:",
   f"/-- ★★★ A CONSTANTE DA LUZ É A ESCALA DO TEMPO [fala 17, 10/11: «a constante da luz é a escala do tempo»; {RAT}] — a constante\n    MULTIPLICA O TEMPO:", "E9")
um("    frequencia»] — DUAS constantes:", f"    frequencia»; {RAT}] — DUAS constantes:", "E10")
um("/-- ★★★ O NOME É O MESMO EM TODA ESCALA [falas 13 e 15, 10/11: «O observador é a escala»; «o observador está na escala da constante da luz»]\n    — para c > 0",
   f"/-- ★★★ O NOME É O MESMO EM TODA ESCALA [falas 13 e 15, 10/11: «O observador é a escala»; «o observador está na escala da constante da luz»;\n    {RAT}] — para c > 0", "E12")
um("/-- ★★★ O LEITOR SÓ ADMITE UMA ESCALA [fala 17, 10/11: «o leitor só admite uma escala: o sinal»] — (1)",
   f"/-- ★★★ O LEITOR SÓ ADMITE UMA ESCALA [fala 17, 10/11: «o leitor só admite uma escala: o sinal»; {RAT}] —\n    (1)", "E13")
um("/-- ★★★ TUDO DEPENDE DA ESCALA [fala 17, 10/11: «tudo depende da escala, sem escala não há tônica»; «sem dimuta não há eletromagnetismo»] —",
   f"/-- ★★★ TUDO DEPENDE DA ESCALA [fala 17, 10/11: «tudo depende da escala, sem escala não há tônica»; «sem dimuta não há eletromagnetismo»;\n    {RAT}] —", "E14")

# a docstring da cadeia: os itens (i) e (v) ditos pela fórmula
um("(i) SEM ESCALA NÃO HÁ TÔNICA:\n    a tônica na unidade zero é zero (`tonica_eq`);", "(i) SEM ESCALA NÃO HÁ TÔNICA:\n    `tonica κ 0 = 0` (`tonica_eq`);", "E15")
um("(v) a tônica é zero\n    ⟺ a unidade é zero;", "(v) `tonica κ u = 0`\n    ⟺ `u = 0`;", "E16")

# conferências: só comentário mudou; nada sobre E₀ nem sobre a palavra retirada; os rótulos certos
semc = lambda s: re.sub(r"/-.*?-/", "", s, flags=re.S)
assert semc(src) == semc(t), "mudou algo fora de comentario"
for proib in ("E₀", "the_scale_is_free", "unidade", "a ratificar", "PROVISÓRIOS"):
    assert proib not in t, "ainda ha na secao 7: " + proib
assert t.count(RAT) == 6, t.count(RAT)
assert t.count(AUT) == 5, t.count(AUT)
(BLD / "parte7_constante_da_escala_emenda2.txt").write_text(t, encoding="utf-8", newline="\n")
print("parte7 emenda2 gravada:", len(t.encode("utf-8")), "B | codigo fora de comentario identico: True | RATIFICADO:", t.count(RAT), "| DECLARADO pela autoria:", t.count(AUT))
