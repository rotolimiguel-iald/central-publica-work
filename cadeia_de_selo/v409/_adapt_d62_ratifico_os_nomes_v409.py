# -*- coding: utf-8 -*-
"""_adapt_d62_ratifico_os_nomes_v409.py -- (claude-construtor-v409, 05/11/2026 ~20h) AO LADO D62 do fim do DESENHO_v409.md: o operador RATIFICOU os nomes («Ratifico os nomes»,
work\\cunhagens_13out\\OPERADOR_05nov_ratifico_os_nomes_verbatim.txt; o sha16 e' LIDO do arquivo e conferido contra o que o AO LADO deu). A fala entra INTEIRA na lista congelada (a 14a) e no spec cunhagens_v409
(como D62); onde os textos/registros diziam que o nome ParNaFaceDeFock ou os nomes acrescentados na R9 estavam [DECLARADO], passam a dizer que foram ratificados pelo operador em 05/11 (D62). As pedras e o kernel NAO
mudam (as docstrings dizem «[DECLARADO] ate a ratificacao», verdade como registro da epoca da pedra; o preparo do bundle segue conferindo esse cabecalho). As conferencias que contavam 13 falas e D55 a D61 passam a 14 e
D55 a D62 (os numeros sobem com o conteudo; nada relaxado)."""
import datetime, hashlib, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq, HERE

FALA = os.path.join(os.path.dirname(os.path.dirname(HERE)), "cunhagens_13out", "OPERADOR_05nov_ratifico_os_nomes_verbatim.txt")
B_FALA = open(FALA, "rb").read(); H_FALA = hashlib.sha256(B_FALA).hexdigest()
assert H_FALA[:16] == "4b5a1d867954b6ed" and B_FALA.decode("utf-8").strip() == "Ratifico os nomes", (H_FALA[:16], B_FALA)

# ------------------------------------------------------------------ (1) a lista CONGELADA: +1 (a 14a, inteira)
CONG = os.path.join(HERE, "VERBATIM_CONGELADO_v409.json")
raw = open(CONG, "rb").read(); c = json.loads(raw.decode("utf-8"))
assert c["n"] == 13 == len(c["arquivos"]) == len(c["registro"]) and FALA not in c["arquivos"], c["n"]
c["arquivos"].append(FALA); c["registro"].append({"arquivo": FALA, "sha256": H_FALA, "bytes": len(B_FALA), "autor": "operador"}); c["n"] = len(c["arquivos"])
c.setdefault("acrescimos", []).append({"quando": datetime.datetime.now().isoformat(timespec="seconds"), "por": "claude-construtor-v409", "o_que": "a 14a fala (AO LADO D62 do DESENHO_v409.md): a ratificacao dos nomes, inteira", "sha16": H_FALA[:16]})
c["nota"] = ("as catorze falas de 05/11/2026 que esta versao embute (as dez do DESENHO_v409 §3 e as quatro dos AO LADO do fim dele); de tres, so' o trecho e' embutido e citado (duas pela D59; uma porque o resto e' aviso operacional); "
             "lista de trabalho da cadeia (NAO pinada como fonte: traz os caminhos de origem)")
ts = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
open(CONG + ".bak_" + ts + "_d62", "wb").write(raw); assert open(CONG + ".bak_" + ts + "_d62", "rb").read() == raw
nb = json.dumps(c, ensure_ascii=False, indent=1).encode("utf-8")
open(CONG + ".tmp", "wb").write(nb); assert os.path.getsize(CONG + ".tmp") == len(nb); os.replace(CONG + ".tmp", CONG)
print("VERBATIM_CONGELADO_v409.json: %d falas" % c["n"])


def todas(a, velho, novo):
    n_ = a.t.count(velho); assert n_ >= 1, ("NAO CASOU", os.path.basename(a.p), velho[:100]); a.troca(velho, novo, n_); return n_


ST_A_OLD = ("o nome TraducaoTuring e os nomes das declaracoes das rodadas R1 a R8 dados pela gerencia c1 e RATIFICADOS pelo operador em 05/11/2026; os nomes acrescentados na R9 (a inscricao no psion e a formula SAT) "
            "e os da ParNaFaceDeFock sao da gerencia e ficam [DECLARADO] ate a ratificacao (a fala de 05/11 e' anterior a eles)")
ST_A_NEW = ("o nome TraducaoTuring e os nomes das declaracoes das rodadas R1 a R8, dados pela gerencia c1, foram RATIFICADOS pelo operador em 05/11/2026 («concordo com todos os nomes que foram dados»); os nomes acrescentados na R9 "
            "(a inscricao no psion e a formula SAT) e os da ParNaFaceDeFock, tambem da gerencia, foram RATIFICADOS por ele em 05/11/2026 («Ratifico os nomes», D62)")
ST_PT_OLD = "o nome `TraducaoTuring` e os nomes das declarações das rodadas R1–R8 dados pela gerência e ratificados pelo operador; os nomes acrescentados na R9 e os da `ParNaFaceDeFock` são da gerência e ficam [DECLARADO] até a ratificação"
ST_PT_NEW = ("o nome `TraducaoTuring` e os nomes das declarações das rodadas R1–R8, dados pela gerência, foram ratificados pelo operador em 05/11 («concordo com todos os nomes que foram dados»); "
             "os acrescentados na R9 e os da `ParNaFaceDeFock`, também da gerência, foram ratificados por ele em 05/11 («Ratifico os nomes», D62)")

# ------------------------------------------------------------------ (2) delta
d = Arq("delta_v409.py")
d.troca('''N_TUDO_NA_V409 = "OPERADOR_05nov_tudo_na_v409_nada_para_a_v410_verbatim.txt"   # (DESENHO, AO LADO de ~18h: a ORDEM do operador que traz tudo para a v409; a 13a fala, inteira)''',
        '''N_TUDO_NA_V409 = "OPERADOR_05nov_tudo_na_v409_nada_para_a_v410_verbatim.txt"   # (DESENHO, AO LADO de ~18h: a ORDEM do operador que traz tudo para a v409; a 13a fala, inteira)
N_RATIFICO_OS_NOMES = "OPERADOR_05nov_ratifico_os_nomes_verbatim.txt"   # (DESENHO, AO LADO D62 de ~20h: a ratificacao dos nomes; a 14a fala, inteira)''')
d.troca("N_SORRY, N_RATIFICA_D61, N_TUDO_NA_V409)   # as TREZE falas: as dez do DESENHO_v409 §3 e as tres dos AO LADO do fim", "N_SORRY, N_RATIFICA_D61, N_TUDO_NA_V409, N_RATIFICO_OS_NOMES)   # as CATORZE falas: as dez do DESENHO_v409 §3 e as quatro dos AO LADO do fim")
d.troca("N_FALAS_V409 = 13", "N_FALAS_V409 = 14")
d.troca("RESTRITA aos treze nomes do DESENHO (as dez do §3 e as tres dos AO LADO;", "RESTRITA aos catorze nomes do DESENHO (as dez do §3 e as quatro dos AO LADO;")
d.troca('''N_RATIFICA_D61: "9ee7d5a1b161437f", N_TUDO_NA_V409: "fb3dc69e3c9b5516"}   # (as tres ultimas:''', '''N_RATIFICA_D61: "9ee7d5a1b161437f", N_TUDO_NA_V409: "fb3dc69e3c9b5516", N_RATIFICO_OS_NOMES: "4b5a1d867954b6ed"}   # (as quatro ultimas:''')
d.troca('''FRASE_TUDO_NA_V409 = "eu quero que entre tudo na versão 409 não deixar nada para a v410"   # (a 13a fala, verbatim: a ordem que traz tudo para a v409; D60 revista)''',
        '''FRASE_TUDO_NA_V409 = "eu quero que entre tudo na versão 409 não deixar nada para a v410"   # (a 13a fala, verbatim: a ordem que traz tudo para a v409; D60 revista)
FRASE_RATIFICO_OS_NOMES = "Ratifico os nomes"   # (a 14a fala, verbatim e inteira: a ratificacao dos nomes acrescentados depois da fala «concordo com todos os nomes que foram dados»; D62)''')
d.troca("(N_TUDO_NA_V409, FRASE_TUDO_NA_V409)]", "(N_TUDO_NA_V409, FRASE_TUDO_NA_V409), (N_RATIFICO_OS_NOMES, FRASE_RATIFICO_OS_NOMES)]")
d.troca('''    "o_par_na_face_de_fock": ''', '''    "os_nomes_ratificados": "«Ratifico os nomes» [INPUT; a fala inteira; D62]: o operador ratifica o nome ParNaFaceDeFock e os nomes das declaracoes acrescentados depois da fala «concordo com todos os nomes que foram dados» (a inscricao no psion e a formula SAT, na TraducaoTuring); as docstrings das pedras dizem [DECLARADO] ate a ratificacao, registro da epoca da pedra (o kernel nao e' refeito por isso)",
    "o_par_na_face_de_fock": ''')
d.troca('''DECISOES_V409 = ("D55", "D56", "D57", "D58", "D59", "D60", "D61")''',
        '''DECISOES["D62"] = ("o operador RATIFICOU os nomes (sha16 %s: «%s»): o nome ParNaFaceDeFock e os nomes das declaracoes das duas pedras acrescentados depois da fala de 05/11 «concordo com todos os nomes que foram dados» "
                   "(a inscricao no psion e a formula SAT, na TraducaoTuring); a fala entra inteira na lista congelada e no registro cunhagens_v409; as docstrings das pedras NAO mudam (dizem [DECLARADO] ate a ratificacao, "
                   "verdade como registro da epoca da pedra; o kernel nao e' refeito por isso); os textos da v409 dizem que a ratificacao aconteceu [decisao da gerencia c1, 05/11/2026, ~20h, pela fala do operador]" % (_sha16_arq(N_RATIFICO_OS_NOMES), FRASE_RATIFICO_OS_NOMES))
DECISOES_V409 = ("D55", "D56", "D57", "D58", "D59", "D60", "D61", "D62")''')
d.troca('''os nomes acrescentados na R9 (a inscricao no psion e a formula SAT) sao da gerencia e ficam [DECLARADO] ate a ratificacao (a fala e' anterior a eles)" % _H_NOMES),''',
        '''os nomes acrescentados na R9 (a inscricao no psion e a formula SAT), tambem da gerencia, foram RATIFICADOS pelo operador em 05/11/2026 («Ratifico os nomes», D62)" % _H_NOMES),''')
d.troca('''"ParNaFaceDeFock": ("dado pela gerencia c1 (05/11/2026, tarde), com os nomes das declaracoes; fica [DECLARADO] ate a ratificacao (a fala de 05/11, sha16 %s, e' anterior a esta pedra e nao a cobre); "''',
        '''"ParNaFaceDeFock": ("dado pela gerencia c1 (05/11/2026, tarde), com os nomes das declaracoes, e RATIFICADO pelo operador em 05/11/2026 («Ratifico os nomes», D62; a fala de 05/11 «concordo com todos os nomes que foram dados», sha16 %s, e' anterior a esta pedra e nao a cobria); "''')
d.troca("os acrescentados na R9 e os da ParNaFaceDeFock [DECLARADO] ate a ratificacao; ditos assim em todo texto, D55)", "os acrescentados na R9 e os da ParNaFaceDeFock RATIFICADOS por ele em 05/11 (D62); ditos assim em todo texto, D55)")
d.troca('''"e o nome ParNaFaceDeFock com os das declaracoes dela sao da gerencia e ficam [DECLARADO] ate a ratificacao (a fala e' anterior a eles); ditos assim em todo texto''',
        '''"e o nome ParNaFaceDeFock com os das declaracoes dela, tambem da gerencia, foram RATIFICADOS pelo operador em 05/11/2026 («Ratifico os nomes», D62); ditos assim em todo texto''')
d.troca("# as falas do operador de 05/11 por sha256 + D55-D61 + E24-E28", "# as falas do operador de 05/11 por sha256 + D55-D62 + E24-E28")
d.grava()

# ------------------------------------------------------------------ (3) registros
r = Arq("registros_v409.py")
r.troca("os acrescentados na R9, [DECLARADO] ate a ratificacao): o dicionario de Turing;", "os acrescentados na R9, RATIFICADOS por ele em 05/11, D62): o dicionario de Turing;")
r.troca("(os da TraducaoTuring R1 a R8; os acrescentados na R9 e os da ParNaFaceDeFock ficam [DECLARADO] ate a ratificacao)", "(os da TraducaoTuring R1 a R8; os acrescentados na R9 e os da ParNaFaceDeFock ele ratificou na fala «Ratifico os nomes», D62)")
r.troca("os acrescentados na R9, [DECLARADO] ate a ratificacao) e ParNaFaceDeFock", "os acrescentados na R9, ratificados por ele em 05/11, D62) e ParNaFaceDeFock")
r.troca("o nome e os das declaracoes dela, da gerencia, [DECLARADO] ate a ratificacao).", "o nome e os das declaracoes dela, da gerencia, ratificados pelo operador em 05/11, D62).")
todas(r, ST_A_OLD, ST_A_NEW)
r.troca('''" + " («concordo com todos os nomes que foram dados»; D55)",''', '''" + " (D55; D62)",''')
r.grava()

# ------------------------------------------------------------------ (4) artigos, gerador, textos e scripts da gerencia
a = Arq("artigo_pt_v409.pysnip")
a.troca(ST_PT_OLD.replace("R1–R8", "R1–R8"), ST_PT_NEW)
a.troca("os acrescentados na R9 ficam [DECLARADO] até a ratificação) e \\texttt{ParNaFaceDeFock} (o nome e os das declarações, da gerência, ficam [DECLARADO] até a ratificação; entra pela ordem do operador:",
        "os acrescentados na R9, também, em 05/11, pela fala «Ratifico os nomes») e \\texttt{ParNaFaceDeFock} (o nome e os das declarações, da gerência, ratificados pelo operador em 05/11; entra pela ordem do operador:")
a.grava()
e = Arq("artigo_en_v409.pysnip")
e.troca("the names added in R9 and those of ParNaFaceDeFock are the management's and stay [DECLARADO] until ratification);", "the names added in R9 and those of ParNaFaceDeFock, also the management's, were ratified by the operator on 05/11, D62);")
e.troca("those added in R9 stay [DECLARADO] until ratification) and \\texttt{ParNaFaceDeFock} (its name and those of its declarations, the management's, stay [DECLARADO] until ratification;",
        "those added in R9 too, on 05/11, by the saying «Ratifico os nomes») and \\texttt{ParNaFaceDeFock} (its name and those of its declarations, the management's, ratified by the operator on 05/11;")
e.grava()
g = Arq("gerar_candidato_v409.py")
g.troca("e os acrescentados na R9 [DECLARADO] até a ratificação, e `ParNaFaceDeFock`, nomes da gerência [DECLARADO] até a ratificação, pela ordem dele:",
        "e os acrescentados na R9 ratificados por ele em 05/11 (D62), e `ParNaFaceDeFock`, nomes da gerência ratificados pelo operador em 05/11 (D62), pela ordem dele:")
g.grava()

t = Arq("pos_rito/textos_v409_novo.pysnip")
todas(t, ST_PT_OLD, ST_PT_NEW)
t.troca("os acrescentados na R9 e os da ParNaFaceDeFock [DECLARADO] ate a ratificacao).", "os acrescentados na R9 e os da ParNaFaceDeFock ratificados por ele em 05/11, D62).")
t.troca("; a fala da ratificação: %s), com %s bandeiras", "; a primeira ratificação, verbatim: %s), com %s bandeiras")
todas(t, "D55 a D61", "D55 a D62")
t.troca("cunhagens_v409: as 13 falas, as erratas", "cunhagens_v409: as 14 falas, as erratas")
t.troca("cunhagens_v409 (as 13 falas de 05/11 por sha256", "cunhagens_v409 (as 14 falas de 05/11 por sha256")
t.troca("O registro por spec cunhagens_v409 do core SELADO: as 13 falas de 05/11 por sha256", "O registro por spec cunhagens_v409 do core SELADO: as 14 falas de 05/11 por sha256")
t.troca('''"sorry": _sha_por("o_dispositivo_e_o_no_sorry"), "ratifica": _sha_por("d61_ratificada")}''', '''"sorry": _sha_por("o_dispositivo_e_o_no_sorry"), "ratifica": _sha_por("d61_ratificada"), "ratnomes": _sha_por("ratifico_os_nomes")}''')
t.troca('''("sorry", DL_.N_SORRY), ("ratifica", DL_.N_RATIFICA_D61))), "os sha16 das falas != os que a ordem da gerencia deu"''', '''("sorry", DL_.N_SORRY), ("ratifica", DL_.N_RATIFICA_D61), ("ratnomes", DL_.N_RATIFICO_OS_NOMES))), "os sha16 das falas != os que a ordem da gerencia deu"''')
t.troca('''("rat", DL_.FRASE_RATIFICA_D6''', '''("ratn", DL_.FRASE_RATIFICO_OS_NOMES), ("rat", DL_.FRASE_RATIFICA_D6''')
t.troca("e a ratificação dela (`{s11}`): {rat} (D61). ", "e a ratificação dela (`{s11}`): {rat} (D61); e, à noite, a ratificação dos nomes (`{s12}`): {ratn} (D62). ")
t.troca('''s10=ss["sorry"], s11=ss["ratifica"], **q)''', '''s10=ss["sorry"], s11=ss["ratifica"], s12=ss["ratnomes"], **q)''')
t.troca("a candidata R8 e o recibo de compilação, a saída do lean,", "as candidatas R9 e R2 e as saídas do lean delas, as saídas do lean das fontes,")
t.troca("ao lado das falas dele (a D61 ele já ratificou).", "ao lado das falas dele (a D61 e os nomes, D62, ele já ratificou).")
t.grava()

m = Arq("pos_rito/registrar_mapa_v409.py")
todas(m, ST_A_OLD, ST_A_NEW)
m.troca("e os acrescentados na R9 [DECLARADO] ate a ratificacao, D55)", "e os acrescentados na R9 ratificados por ele em 05/11, D55 e D62)")
m.troca("os acrescentados na R9 [DECLARADO] ate a ratificacao, D55;", "os acrescentados na R9 ratificados em 05/11, D55 e D62;")
m.troca("e os acrescentados na R9 [DECLARADO] ate a ratificacao; ", "e os acrescentados na R9 ratificados por ele em 05/11 ({_aspas_(DL_.FRASE_RATIFICO_OS_NOMES)}, D62); ")
m.troca("DECLARADO (o recibo de compilacao da candidata; o nome e os das declaracoes, da gerencia, ate a ratificacao)", "DECLARADO (o recibo de compilacao da candidata); INPUT (o nome e os das declaracoes, da gerencia, ratificados pelo operador em 05/11, D62)")
m.troca('''all(("D%d" % i) in dec for i in range(55, 62)), "faltam decisoes D55 a D61 no registro"''', '''all(("D%d" % i) in dec for i in range(55, 63)), "faltam decisoes D55 a D62 no registro"''')
m.troca("(a D61, ratificada pelo operador), ao lado", "(a D61, ratificada pelo operador; a D62, a ratificacao dos nomes), ao lado")
m.grava()

l = Arq("pos_rito/leitura_v409.py")
todas(l, "D55 a D61", "D55 a D62")
l.troca("as 13 falas por sha256 e a linha do bloco", "as 14 falas por sha256 e a linha do bloco")
l.grava()
h = Arq("pos_rito/harness_textos_ensaio_v409.py")
todas(h, 'espera="cunhagens_v409: as decisoes D55 a D61"', 'espera="cunhagens_v409: as decisoes D55 a D62"')
h.grava()
cu = Arq("pos_rito/textos_custodia_handoff_v409.py")
cu.troca("those added in R9 and those of `ParNaFaceDeFock` stay [DECLARADO] until ratification), ", "those added in R9 and those of `ParNaFaceDeFock` ratified by him on 05/11 as well, «Ratifico os nomes», D62), ")
cu.grava()
x = Arq("pos_rito/gerar_x_custodia_v409.py")
x.troca("os acrescentados na R9 e os da ParNaFaceDeFock ficam [DECLARADO] até a ratificação),", "os acrescentados na R9 e os da ParNaFaceDeFock ratificados por ele também em 05/11, «{DL.FRASE_RATIFICO_OS_NOMES}» (D62)),")
x.grava()

rl = Arq("gerar_relatorio_v409.py")
rl.troca("os acrescentados na R9 (a inscricao no psion e a formula SAT) e os da ParNaFaceDeFock (o modulo e as 10 declaracoes), da gerencia, ficam [DECLARADO] ate a ratificacao: a fala e' anterior a eles (recibo revisto de 05/11 ~19h30;",
         "os acrescentados na R9 (a inscricao no psion e a formula SAT) e os da ParNaFaceDeFock (o modulo e as 10 declaracoes), da gerencia, foram RATIFICADOS por ele em 05/11 («Ratifico os nomes», D62; as docstrings das pedras dizem [DECLARADO] ate a ratificacao, registro da epoca da pedra; recibo revisto de 05/11 ~19h30;")
todas(rl, "D55 a D61", "D55 a D62")
todas(rl, "D55-D61", "D55-D62")
rl.troca("as tres ultimas vieram dos AO LADO do fim do DESENHO: a 11a, a 12a e a 13a, a ordem de tudo entrar na v409", "as quatro ultimas vieram dos AO LADO do fim do DESENHO: a 11a, a 12a, a 13a (a ordem de tudo entrar na v409) e a 14a (a ratificacao dos nomes, D62)")
rl.grava()
for f_ in ("fechar_preparacao_v409.py", "acom_inscrever_prep_v409.py"):
    a_ = Arq(f_); todas(a_, ST_A_OLD, ST_A_NEW); a_.grava()
dp = Arq("depositar_construtor_v409.py")
dp.troca('''"13 falas do operador de 05/11 (de tres, so' o trecho)"''', '''"14 falas do operador de 05/11 (de tres, so' o trecho)"''')
dp.grava()

# ------------------------------------------------------------------ (5) as conferencias que contavam 13 falas e D55 a D61
for f_ in ("_ensaio_bloco_v409.pysnip", "ensaio_a_seco_v409.py"):
    a_ = Arq(f_)
    a_.troca("as 13 falas do contrato,", "as 14 falas do contrato,")
    a_.troca('''len(r9["inscriptions"]) == len(_CP9["verbatins"]) == DL.N_FALAS_V409 == 13 and''', '''len(r9["inscriptions"]) == len(_CP9["verbatins"]) == DL.N_FALAS_V409 == 14 and''')
    a_.troca('''bool(ok_ and len(_CP9["verbatins"]) == DL.N_FALAS_V409 == 13 and''', '''bool(ok_ and len(_CP9["verbatins"]) == DL.N_FALAS_V409 == 14 and''')
    a_.troca('''== len(DL.VERBATIM_PREFIXOS_DA_ORDEM_V409) == DL.N_FALAS_V409 == 13)''', '''== len(DL.VERBATIM_PREFIXOS_DA_ORDEM_V409) == DL.N_FALAS_V409 == 14)''')
    a_.troca("as decisoes D55-D61, as erratas E24-E28", "as decisoes D55-D62, as erratas E24-E28")
    a_.troca('''== len(_sp9s["verbatins"]) == DL.N_FALAS_V409 == 13 and all(v_["embedded_ok"]''', '''== len(_sp9s["verbatins"]) == DL.N_FALAS_V409 == 14 and all(v_["embedded_ok"]''')
    a_.troca('''{"D55", "D56", "D57", "D58", "D59", "D60", "D61"}''', '''{"D55", "D56", "D57", "D58", "D59", "D60", "D61", "D62"}''')
    a_.troca('''and _xn9.get("n_falas") == 13''', '''and _xn9.get("n_falas") == 14''')
    a_.troca('''sorted((_xn9.get("autores") or {}).values()) == ["operador"] * 13''', '''sorted((_xn9.get("autores") or {}).values()) == ["operador"] * 14''')
    a_.grava()
p = Arq("p00_precondicoes_v409.py")
p.troca("82 ancoras (13 principais), 13 falas (de tres, so' o trecho;", "82 ancoras (13 principais), 14 falas (de tres, so' o trecho;")
p.troca("82 ancoras, 13 falas de 05/11, de tres so' o trecho;", "82 ancoras, 14 falas de 05/11, de tres so' o trecho;")
p.troca('''and len(vb_) == len(DL.VERBATIM_ORIGEM_V409) == DL.N_FALAS_V409 == 13 and''', '''and len(vb_) == len(DL.VERBATIM_ORIGEM_V409) == DL.N_FALAS_V409 == 14 and''')
p.troca('''== len(CM["cunhagens"]) == DL.N_FALAS_V409 == 13, {"embutidas"''', '''== len(CM["cunhagens"]) == DL.N_FALAS_V409 == 14, {"embutidas"''')
p.troca('''chk("as 13 falas de 05/11 (todas do operador;''', '''chk("as 14 falas de 05/11 (todas do operador;''')
p.troca("o manifesto traz exatamente as 13 entradas cunhagens/", "o manifesto traz exatamente as 14 entradas cunhagens/")
p.troca('''len([k for k in MI if k.startswith("cunhagens/")]) == DL.N_FALAS_V409 == 13 and''', '''len([k for k in MI if k.startswith("cunhagens/")]) == DL.N_FALAS_V409 == 14 and''')
p.grava()
ci = Arq("conferir_instalar_rito_v409.py")
ci.troca('''assert _DEC_NOVAS and _DEC_NOVAS[0] == "D55" and _DEC_NOVAS[-1] == "D61", _DEC_NOVAS''', '''assert _DEC_NOVAS and _DEC_NOVAS[0] == "D55" and _DEC_NOVAS[-1] == "D62", _DEC_NOVAS''')
ci.troca("# as decisoes que a v409 acrescenta (D55..D61)", "# as decisoes que a v409 acrescenta (D55..D62)")
ci.troca("D55-D61/E24-E28 e a E21 lidas do delta", "D55-D62/E24-E28 e a E21 lidas do delta")
ci.grava()
rt = Arq("rito_v409.sh")
rt.troca("as 13 falas de 05/11 por sha256", "as 14 falas de 05/11 por sha256")
rt.troca("as decisoes D55 a D61 e as erratas E24 a E28 e a E21 ao lado", "as decisoes D55 a D62 e as erratas E24 a E28 e a E21 ao lado")
rt.troca("nenhuma decisao da v409 [D55 a D61] as muda", "nenhuma decisao da v409 [D55 a D62] as muda")
rt.grava()
for f_, v_, n_ in (("conferir_rito_v409.py", "e as decisoes D55 a D61 (a D61 ratificada pelo operador)", "e as decisoes D55 a D62 (a D61 ratificada pelo operador; a D62, a ratificacao dos nomes)"),
                   ("gerar_esperados_v409.py", "e as decisoes D55 a D61 (a D61 ratificada pelo operador)", "e as decisoes D55 a D62 (a D61 ratificada pelo operador; a D62, a ratificacao dos nomes)")):
    a_ = Arq(f_); a_.troca(v_, n_); a_.grava()
