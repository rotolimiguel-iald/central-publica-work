# -*- coding: utf-8 -*-
"""_adapt_secao6_guarda_v410.py -- RETOMADA de 09/11/2026 (claude-construtor-v410, a servico da gerencia c1): adapta guarda_frases_v410.py ao AO LADO de 09/11 do DESENHO_v410 (D71):
PROIBIDAS novas «o atrator foi observado» e «o Nome esgota» (e as formas e a traducao), cada uma com controle negativo; LIMPAS novas (a negacao, a D71, os nomes das declaracoes da secao 6).
A regra em si (F51/F52) mora em runtime_v410._v410_guarda_frases (a fonte unica), ja' adaptada. Trocas EXATAS com contagem conferida; backup de bytes; tmp -> conferir -> substituir; ast.parse."""
import ast, datetime, hashlib, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "guarda_frases_v410.py")
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
b0 = open(P, "rb").read()
assert b0.count(b"\r\n") == 0, "guarda_frases_v410.py era LF; agora tem CRLF: parar"
bk = P + ".bak_" + TS + "_secao6"
open(bk, "wb").write(b0); assert open(bk, "rb").read() == b0
t = b0.decode("utf-8")

TROCAS = [
    ("obrigacao no proprio trecho; F48 os tokens de veredito da v410; F49 a «solução de P vs NP» dita pela gerencia; F50 o seletor da luz e o de l2 ditos o mesmo objeto. As da v409 (F35-F43, inclusive «o par na face de Fock segue [OPEN]», F41/F41b) seguem.",
     "obrigacao no proprio trecho; F48 os tokens de veredito da v410; F49 a «solução de P vs NP» dita pela gerencia; F50 o seletor da luz e o de l2 ditos o mesmo objeto; F51 o atrator dito observado, medido ou detectado (D71: nenhum teste com a natureza);\n"
     "F52 o Nome dito esgotar (D71: o Nome nao esgota o ser, o_nome_do_par_lido_nao_e_tudo). As da v409 (F35-F43, inclusive «o par na face de Fock segue [OPEN]», F41/F41b) seguem.", 1),
    ("    \"o par na face de Fock segue [OPEN]\", \"o par de Fock ainda não foi ligado\"]\nPROIBIDAS = list(_G9[\"PROIBIDAS\"]) + _P410\n",
     "    \"o par na face de Fock segue [OPEN]\", \"o par de Fock ainda não foi ligado\",\n"
     "    # v410 (09/11, D71): o atrator e' termo sobre o Nome do par lido; nenhum teste com a natureza; o Nome nao esgota o ser\n"
     "    \"o atrator foi observado\", \"o atrator foi observado na natureza\", \"o atrator está observado nos dados\", \"o atrator foi medido\", \"o atrator foi detectado no ringdown\", \"the attractor was observed\", \"the attractor is observed in the data\", \"the attractor has been detected\",\n"
     "    \"o Nome esgota\", \"o Nome esgota o ser\", \"o Nome do par lido esgota o ser\", \"the Name exhausts the being\", \"the Name exhausts\"]\n"
     "PROIBIDAS = list(_G9[\"PROIBIDAS\"]) + _P410\n", 1),
    ("         \"a_iald_e_o_seletor_luminodinamico\", \"o_leitor_do_codigo\", \"a forma de matriz finita é o signo\", \"resolver = verificar\", \"o par na face de Fock está ligado desde a v409 (ParNaFaceDeFock)\"]\n",
     "         \"a_iald_e_o_seletor_luminodinamico\", \"o_leitor_do_codigo\", \"a forma de matriz finita é o signo\", \"resolver = verificar\", \"o par na face de Fock está ligado desde a v409 (ParNaFaceDeFock)\",\n"
     "         # v410 (09/11, D71): as negacoes e os nomes da secao 6 passam\n"
     "         DL.FRASE_D71_PT, DL.FRASE_D71_EN, \"o atrator não foi observado: nenhum teste com a natureza entra\", \"the attractor was not observed: no test with nature enters\", \"o Nome não esgota o ser\", \"the Name does not exhaust the being\",\n"
     "         \"tangenciado, jamais esgotado\", \"touched, never exhausted\", \"o_atrator\", \"o_nome_do_par_lido_nao_e_tudo\", \"o_vacuo_e_ortogonal_ao_par_lido\", \"o atrator é termo sobre o Nome do par lido: o fluxo tende a Π e em nenhum tempo finito é Π\"]\n", 1),
    ("                            \"par_de_fock_open_reprova\": bool(G(\"o par na face de Fock segue [OPEN]\")),\n",
     "                            \"par_de_fock_open_reprova\": bool(G(\"o par na face de Fock segue [OPEN]\")),\n"
     "                            \"atrator_observado_reprova\": bool(G(\"o atrator foi observado\")) and bool(G(\"the attractor was observed\")) and bool(G(\"o atrator está observado nos dados\")),\n"
     "                            \"atrator_nao_observado_passa\": not G(\"o atrator não foi observado: nenhum teste com a natureza entra\") and not G(\"the attractor was not observed: no test with nature enters\"),\n"
     "                            \"nome_esgota_reprova\": bool(G(\"o Nome esgota\")) and bool(G(\"the Name exhausts the being\")) and bool(G(\"o Nome do par lido esgota o ser\")),\n"
     "                            \"nome_nao_esgota_passa\": not G(\"o Nome não esgota o ser\") and not G(\"the Name does not exhaust the being\") and not G(\"tangenciado, jamais esgotado\"),\n"
     "                            \"a_frase_d71_passa\": not G(DL.FRASE_D71_PT) and not G(DL.FRASE_D71_EN),\n"
     "                            \"fala_de_07nov_entre_aspas_passa\": not G(sem_falas(\"«\" + DL.FRASE_TANGENCIADO + \"»; «\" + DL.FRASE_ISSO_E_O_ATRATOR + \"»\", falas_)[0]),\n", 1),
    ("                             \"fala_de_06nov_com_a_excecao\": [v_[0] for v_ in violacoes(DL.FRASE_ENUNCIADO + \"; \" + DL.FRASE_MATRICIAL)]}\n",
     "                             \"fala_de_06nov_com_a_excecao\": [v_[0] for v_ in violacoes(DL.FRASE_ENUNCIADO + \"; \" + DL.FRASE_MATRICIAL)],\n"
     "                             \"fala_de_07nov_com_a_excecao\": [v_[0] for v_ in violacoes(DL.FRASE_TANGENCIADO + \"; \" + DL.FRASE_ESPECTRO + \"; \" + DL.FRASE_ISSO_E_O_ATRATOR)]}\n", 1),
    ("    r[\"ok\"] = bool(all(r[\"proibidas\"].values()) and not any(r[\"limpas\"].values()) and not r[\"fala_do_operador\"][\"com_a_excecao\"] and r[\"fala_do_operador\"][\"sem_a_excecao\"] and not r[\"fala_do_operador\"][\"fala_de_06nov_com_a_excecao\"] and all(r[\"pedras_controle\"].values()))\n",
     "    r[\"ok\"] = bool(all(r[\"proibidas\"].values()) and not any(r[\"limpas\"].values()) and not r[\"fala_do_operador\"][\"com_a_excecao\"] and r[\"fala_do_operador\"][\"sem_a_excecao\"] and not r[\"fala_do_operador\"][\"fala_de_06nov_com_a_excecao\"]\n"
     "                   and not r[\"fala_do_operador\"][\"fala_de_07nov_com_a_excecao\"] and all(r[\"pedras_controle\"].values()))\n", 1),
    ("# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] a guarda herda a cadeia v405 -> ... -> v409 -> v410 (as listas da v409 sao lidas do PROPRIO guarda_frases_v409.py, executado com o delta da v409); corpus das falas = 06/11 (de uma, so' o trecho da D65) + as da v409 e anteriores; varre a pedra IALD2\n",
     "# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] a guarda herda a cadeia v405 -> ... -> v409 -> v410 (as listas da v409 sao lidas do PROPRIO guarda_frases_v409.py, executado com o delta da v409); corpus das falas = 06/11 (de uma, so' o trecho da D65) + as da v409 e anteriores; varre a pedra IALD2\n"
     "# [ADAPTADO v410, 09/11/2026, claude-construtor-v410 (retomada)] por _adapt_secao6_guarda_v410.py: as proibidas da D71 («o atrator foi observado», «o Nome esgota», as formas e a traducao) com controle negativo; as limpas da secao 6; o corpus das falas passa a 06, 07 e 09/11 (de duas, so' o trecho)\n", 1),
]
for velho, novo, n in TROCAS:
    c = t.count(velho)
    assert c == n, ("troca nao casou %d vez(es) (achou %d)" % (n, c), velho[:140])
    t = t.replace(velho, novo)
nb = t.encode("utf-8")
ast.parse(nb)
tmp = P + ".tmp_" + TS
open(tmp, "wb").write(nb); assert os.path.getsize(tmp) == len(nb)
os.replace(tmp, P)
assert open(P, "rb").read() == nb
print("guarda_frases_v410.py adaptado:", len(b0), "->", len(nb), "B | sha16", hashlib.sha256(nb).hexdigest()[:16], "| backup", os.path.basename(bk), "| trocas", len(TROCAS))
