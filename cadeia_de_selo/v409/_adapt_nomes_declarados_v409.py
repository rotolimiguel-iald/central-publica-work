# -*- coding: utf-8 -*-
"""_adapt_nomes_declarados_v409.py -- (claude-construtor-v409, 05/11/2026 ~19h40) a gerencia c1 corrigiu os INSUMOS (recibo revisto: TraducaoTuring sha16 86ddaa69fabd67f5; ParNaFaceDeFock e998d73d3ce60835) e o ESTATUTO
DOS NOMES: o nome `TraducaoTuring` e os nomes das declaracoes das rodadas R1 a R8 seguem RATIFICADOS pelo operador (a fala de 05/11, «concordo com todos os nomes que foram dados»); os nomes acrescentados na R9 (a inscricao no
psion e a formula SAT) e o nome `ParNaFaceDeFock` com os das declaracoes dela ficam [DECLARADO] ate a ratificacao (a fala e' anterior a eles). Este adaptador leva o estatuto a todo texto/registro da cadeia que dizia
«ratificados» para tudo, e o preparo do bundle passa a conferir o CABECALHO NOVO de cada pedra (o texto com os espacos normalizados; a frase propria de cada uma). Nada relaxado: o cabecalho de cada pedra tem de dizer
exatamente o estatuto do recibo revisto."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq

ST_PT = "o nome `TraducaoTuring` e os nomes das declarações das rodadas R1–R8 dados pela gerência e ratificados pelo operador; os nomes acrescentados na R9 e os da `ParNaFaceDeFock` são da gerência e ficam [DECLARADO] até a ratificação"
ST_A = ("o nome TraducaoTuring e os nomes das declaracoes das rodadas R1 a R8 dados pela gerencia c1 e RATIFICADOS pelo operador em 05/11/2026; os nomes acrescentados na R9 (a inscricao no psion e a formula SAT) "
        "e os da ParNaFaceDeFock sao da gerencia e ficam [DECLARADO] ate a ratificacao (a fala de 05/11 e' anterior a eles)")

# ------------------------------------------------------------------ o preparo do bundle: o tipo do nome e o cabecalho novo de cada pedra
p = Arq("preparar_bundle_v409_05nov.py")
p.troca('''PEDRAS = [{"name": "TraducaoTuring", "src": INS / "TraducaoTuring.lean", "old": "TraducaoTuring", "tipo": "05nov_nome_da_gerencia_ratificado_pelo_operador",''',
        '''PEDRAS = [{"name": "TraducaoTuring", "src": INS / "TraducaoTuring.lean", "old": "TraducaoTuring", "tipo": "05nov_nome_da_gerencia_ratificado_R1_a_R8__acrescimos_da_R9_DECLARADO",''')
p.troca('''          {"name": "ParNaFaceDeFock", "src": INS / "ParNaFaceDeFock.lean", "old": "ParNaFaceDeFock", "tipo": "05nov_nome_da_gerencia_ratificado_pelo_operador",''',
        '''          {"name": "ParNaFaceDeFock", "src": INS / "ParNaFaceDeFock.lean", "old": "ParNaFaceDeFock", "tipo": "05nov_nome_da_gerencia_DECLARADO_ate_a_ratificacao",''')
p.troca('''    assert ("o nome `%s` e os nomes das declarações foram dados pela gerência e RATIFICADOS" % n) in t and "entra na v409" in t, ("cabecalho do nome nao casou", n)''',
        '''    _tn = re.sub(r"\\s+", " ", t)   # (o cabecalho quebra linha no meio da frase: confere-se com os espacos normalizados)
    _CAB = {"TraducaoTuring": ["o nome `TraducaoTuring` e os nomes das declarações das rodadas R1–R8 foram dados pela gerência e RATIFICADOS pelo operador em 05/11/2026",
                               "os nomes acrescentados depois dessa fala (a inscrição no psíon e a fórmula SAT) são da gerência e ficam [DECLARADO] até a ratificação", "entra na v409"],
            "ParNaFaceDeFock": ["o nome `ParNaFaceDeFock` e os nomes das declarações são da gerência e ficam [DECLARADO] até a ratificação", "entra na v409, por ordem do operador"]}   # (o estatuto do recibo revisto de 05/11 ~19h30)
    assert all(f_ in _tn for f_ in _CAB[n]), ("cabecalho do nome nao casou (o estatuto do recibo revisto)", n, [f_ for f_ in _CAB[n] if f_ not in _tn])''')
p.grava()

# ------------------------------------------------------------------ delta: o estatuto dos nomes (o dict segue com o nome antigo, NOMES_RATIFICADOS, porque os scripts o leem; o CONTEUDO diz o estatuto)
d = Arq("delta_v409.py")
d.troca('''NOMES_RATIFICADOS = {"TraducaoTuring": "dado pela gerencia c1 (05/11/2026) e RATIFICADO pelo operador em 05/11/2026 (sha16 %s: «concordo com todos os nomes que foram dados»), como os nomes das declaracoes (D55)" % _H_NOMES,''',
        '''NOMES_RATIFICADOS = {"TraducaoTuring": ("dado pela gerencia c1 (05/11/2026) e RATIFICADO pelo operador em 05/11/2026 (sha16 %s: «concordo com todos os nomes que foram dados»), como os nomes das declaracoes das rodadas R1 a R8 (D55); "
                                        "os nomes acrescentados na R9 (a inscricao no psion e a formula SAT) sao da gerencia e ficam [DECLARADO] ate a ratificacao (a fala e' anterior a eles)" % _H_NOMES),''')
d.troca('''                     "ParNaFaceDeFock": ("dado pela gerencia c1 (05/11/2026, tarde), com os nomes das declaracoes; o cabecalho da pedra diz que foram ratificados pelo operador («concordo com todos os nomes que foram dados», sha16 %s) "
                                         "[DECLARADO pela gerencia: a fala da ratificacao e' anterior a esta pedra]; entra na v409 pela ordem do operador (sha16 %s: «eu quero que entre tudo na versão 409 não deixar nada para a v410»)" % (_H_NOMES, _H_TUDO))}''',
        '''                     "ParNaFaceDeFock": ("dado pela gerencia c1 (05/11/2026, tarde), com os nomes das declaracoes; fica [DECLARADO] ate a ratificacao (a fala de 05/11, sha16 %s, e' anterior a esta pedra e nao a cobre); "
                                         "entra na v409 pela ordem do operador (sha16 %s: «eu quero que entre tudo na versão 409 não deixar nada para a v410»)" % (_H_NOMES, _H_TUDO))}''')
d.troca("# (o nome dos scripts bumpados; na v409 os nomes sao da gerencia e RATIFICADOS pelo operador: ditos assim em todo texto, D55)",
        "# (o nome dos scripts bumpados; na v409 os nomes sao da gerencia: os da TraducaoTuring R1 a R8 RATIFICADOS pelo operador, os acrescentados na R9 e os da ParNaFaceDeFock [DECLARADO] ate a ratificacao; ditos assim em todo texto, D55)")
d.troca('''    "D55": "nomes: TraducaoTuring e os nomes das 62 declaracoes, dados pela gerencia c1 e RATIFICADOS pelo operador em 05/11/2026 (sha16 %s: «concordo com todos os nomes que foram dados»); ditos assim em todo texto [decisao da gerencia c1, 05/11/2026]" % _H_NOMES,''',
        '''    "D55": ("nomes: TraducaoTuring e os nomes das declaracoes das rodadas R1 a R8, dados pela gerencia c1 e RATIFICADOS pelo operador em 05/11/2026 (sha16 %s: «concordo com todos os nomes que foram dados»); os nomes acrescentados na R9 "
            "e o nome ParNaFaceDeFock com os das declaracoes dela sao da gerencia e ficam [DECLARADO] ate a ratificacao (a fala e' anterior a eles); ditos assim em todo texto [decisao da gerencia c1, 05/11/2026, revista ~19h30]" % _H_NOMES),''')
d.grava()

# ------------------------------------------------------------------ registros
r = Arq("registros_v409.py")
r.troca("refeita a tarde da R9; o nome e os nomes das declaracoes dados pela gerencia e RATIFICADOS pelo operador em 05/11): o dicionario de Turing;",
        "refeita a tarde da R9; o nome e os nomes das declaracoes das rodadas R1 a R8 dados pela gerencia e RATIFICADOS pelo operador em 05/11; os acrescentados na R9, [DECLARADO] ate a ratificacao): o dicionario de Turing;")
r.troca("que ratifica os nomes dados pela gerencia, e as falas dele do dia", "que ratifica os nomes dados pela gerencia ate entao (os da TraducaoTuring R1 a R8; os acrescentados na R9 e os da ParNaFaceDeFock ficam [DECLARADO] ate a ratificacao), e as falas dele do dia")
r.troca("TraducaoTuring (o nome e os nomes das declaracoes dados pela gerencia c1 e ratificados pelo operador em 05/11/2026) e ParNaFaceDeFock (pela ordem do operador de trazer tudo para a v409).",
        "TraducaoTuring (o nome e os nomes das declaracoes das rodadas R1 a R8 dados pela gerencia c1 e ratificados pelo operador em 05/11/2026; os acrescentados na R9, [DECLARADO] ate a ratificacao) e ParNaFaceDeFock (pela ordem do operador de trazer tudo para a v409; o nome e os das declaracoes dela, da gerencia, [DECLARADO] ate a ratificacao).")
r.troca('''"as respostas do operador de 05/11 conferem no kernel, pelos teoremas da pedra; os nomes foram dados pela gerencia e ratificados pelo operador",''',
        '''"as respostas do operador de 05/11 conferem no kernel, pelos teoremas da pedra; " + ST_A,'''.replace("ST_A", repr(ST_A)))
r.troca('''"[INPUT] os nomes da pedra e das 62 declaracoes foram dados pela gerencia c1 e ratificados pelo operador («concordo com todos os nomes que foram dados»; D55)",''',
        '''"[INPUT] " + %r + " («concordo com todos os nomes que foram dados»; D55)",''' % ST_A)
r.grava()

# ------------------------------------------------------------------ os artigos (o comentario da primeira linha e a frase do que entra)
for f_, old1, new1, old2, new2 in (
        ("artigo_pt_v409.pysnip",
         "# v409 (05/11/2026) -- A TRADUÇÃO ÀS CLASSES DE TURING: 1 módulo novo no kernel (TraducaoTuring; o nome e os nomes das 62 declarações dados pela gerência e ratificados pelo operador);",
         "# v409 (05/11/2026) -- A TRADUÇÃO ÀS CLASSES DE TURING E O PAR NA FACE DE FOCK: 2 módulos novos no kernel (TraducaoTuring e ParNaFaceDeFock; " + ST_PT + ");",
         r"\texttt{TraducaoTuring} (o nome e os nomes das declarações foram dados pela gerência e ratificados pelo operador) e \texttt{ParNaFaceDeFock} (entra pela ordem do operador:",
         r"\texttt{TraducaoTuring} (o nome e os nomes das declarações das rodadas R1--R8 foram dados pela gerência e ratificados pelo operador; os acrescentados na R9 ficam [DECLARADO] até a ratificação) e \texttt{ParNaFaceDeFock} (o nome e os das declarações, da gerência, ficam [DECLARADO] até a ratificação; entra pela ordem do operador:"),
        ("artigo_en_v409.pysnip",
         "# v409 (05/11/2026) -- THE TRANSLATION TO TURING'S CLASSES: 1 new kernel module (TraducaoTuring; the name and the names of the 62 declarations given by the management and ratified by the operator);",
         "# v409 (05/11/2026) -- THE TRANSLATION TO TURING'S CLASSES AND THE PAIR ON THE FOCK FACE: 2 new kernel modules (TraducaoTuring and ParNaFaceDeFock; the name TraducaoTuring and the names of the declarations of rounds R1-R8 given by the management and ratified by the operator; the names added in R9 and those of ParNaFaceDeFock are the management's and stay [DECLARADO] until ratification);",
         r"\texttt{TraducaoTuring} (the name and the names of the declarations were given by the management and ratified by the operator) and \texttt{ParNaFaceDeFock} (it enters by the operator's order,",
         r"\texttt{TraducaoTuring} (the name and the names of the declarations of rounds R1--R8 were given by the management and ratified by the operator; those added in R9 stay [DECLARADO] until ratification) and \texttt{ParNaFaceDeFock} (its name and those of its declarations, the management's, stay [DECLARADO] until ratification; it enters by the operator's order,")):
    a_ = Arq(f_); a_.troca(old1, new1); a_.troca(old2, new2); a_.grava()

g = Arq("gerar_candidato_v409.py")
g.troca("(`TraducaoTuring`, com os nomes dados pela gerência e ratificados pelo operador, e `ParNaFaceDeFock`, pela ordem dele:",
        "(`TraducaoTuring`, com os nomes das rodadas R1–R8 dados pela gerência e ratificados pelo operador e os acrescentados na R9 [DECLARADO] até a ratificação, e `ParNaFaceDeFock`, nomes da gerência [DECLARADO] até a ratificação, pela ordem dele:")
g.grava()

# ------------------------------------------------------------------ o pos-rito e os textos da gerencia
t = Arq("pos_rito/textos_v409_novo.pysnip")
t.troca('''    """Onde mora o modulo novo (TGLExt/), com o nome dado pela gerencia e ratificado pelo operador em 05/11 (lido de delta_v409)."""''',
        '''    """Onde moram os modulos novos (TGLExt/), com o estatuto dos nomes (os da TraducaoTuring R1 a R8 ratificados pelo operador em 05/11; os acrescentados na R9 e os da ParNaFaceDeFock [DECLARADO] ate a ratificacao)."""''')
t.troca('''    return "em `TGLExt`: %s, com o nome dado pela gerência e ratificado pelo operador em 05/11" % ", ".join("`%s`" % n_ for n_ in ns)''',
        '''    return "em `TGLExt`: %s; %s" % (", ".join("`%s`" % n_ for n_ in ns), ''' + repr(ST_PT) + ''')''')
t.troca('''    """O que entrou no kernel: o modulo (nome da gerencia, ratificado pelo operador) e, como REGISTRO, as pedras e os modulos das versoes anteriores."""''',
        '''    """O que entrou no kernel: os modulos (nomes da gerencia; o estatuto de cada nome lido de delta_v409) e, como REGISTRO, as pedras e os modulos das versoes anteriores."""''')
t.troca("Os nomes dos módulos são da gerência (o da `TraducaoTuring` ratificado pelo operador; o da `ParNaFaceDeFock` dado como ratificado pelo cabeçalho da pedra [DECLARADO]);",
        "Os nomes dos módulos são da gerência: " + ST_PT + ";")
t.troca("%s módulos novos no kernel (`TGLExt`: %s, nomes dados pela gerência; a ratificação: %s)", "%s módulos novos no kernel (`TGLExt`: %s; " + ST_PT + "; a fala da ratificação: %s)")
t.grava()

m = Arq("pos_rito/registrar_mapa_v409.py")
m.troca("o modulo TraducaoTuring de TGLExt/, nome da gerencia ratificado pelo operador;", "os modulos TraducaoTuring e ParNaFaceDeFock de TGLExt/ (" + ST_A + ");")
m.troca("com o nome e os nomes das 72 declaracoes dados pela gerencia e ratificados pelo operador, D55)", "com o nome e os nomes das declaracoes das rodadas R1 a R8 ratificados pelo operador e os acrescentados na R9 [DECLARADO] ate a ratificacao, D55)")
m.troca("(a fonte pinada e' a da R9, com os nomes da gerencia ratificados pelo operador, D55;", "(a fonte pinada e' a da R9; os nomes R1 a R8 ratificados pelo operador, os acrescentados na R9 [DECLARADO] ate a ratificacao, D55;")
m.troca("que entrou no kernel do rito como TGLExt/%s (nome da gerencia ratificado pelo operador, D55); a identidade performada", "que entrou no kernel do rito como TGLExt/%s (o nome ratificado pelo operador, D55); a identidade performada")
m.troca("com os nomes da gerencia ratificados pelo operador ({_aspas_(DL_.FRASE_NOMES_RATIFICADOS_V409)}); ", "com os nomes das rodadas R1 a R8 ratificados pelo operador ({_aspas_(DL_.FRASE_NOMES_RATIFICADOS_V409)}) e os acrescentados na R9 [DECLARADO] ate a ratificacao; ")
m.troca("DECLARADO (o recibo de compilacao da candidata; a ratificacao do nome dita pelo cabecalho da pedra)", "DECLARADO (o recibo de compilacao da candidata; o nome e os das declaracoes, da gerencia, ate a ratificacao)")
m.troca("%d modulo de kernel (%s, nome da gerencia ratificado pelo operador),", "%d modulos de kernel (%s; " + ST_A + "),")
m.grava()

c = Arq("pos_rito/textos_custodia_handoff_v409.py")
c.troca('''"; the names given by the management, those of `TraducaoTuring` ratified by the operator on 05/11: «" + Q_NOMES + "»), "''',
        '''"; the names given by the management: those of `TraducaoTuring` from rounds R1-R8 ratified by the operator on 05/11, «" + Q_NOMES + "»; those added in R9 and those of `ParNaFaceDeFock` stay [DECLARADO] until ratification), "''')
c.grava()
x = Arq("pos_rito/gerar_x_custodia_v409.py")
x.troca("({nomes}; os nomes dados pela gerência, os da TraducaoTuring ratificados pelo operador: «{DL.FRASE_NOMES_RATIFICADOS_V409}»),",
        "({nomes}; os nomes são da gerência: os da TraducaoTuring das rodadas R1–R8 ratificados pelo operador, «{DL.FRASE_NOMES_RATIFICADOS_V409}»; os acrescentados na R9 e os da ParNaFaceDeFock ficam [DECLARADO] até a ratificação),")
x.grava()

rl = Arq("gerar_relatorio_v409.py")
rl.troca('''"os nomes (o modulo TraducaoTuring e as 72 declaracoes dele) foram dados pela gerencia c1 e RATIFICADOS pelo operador em 05/11/2026; os da ParNaFaceDeFock (o modulo e as 10 declaracoes), dados pela gerencia e ditos ratificados pelo cabecalho da pedra [DECLARADO: a fala da ratificacao e' anterior a esta pedra] (D55;''',
         '''"os nomes: o modulo TraducaoTuring e as declaracoes das rodadas R1 a R8, dados pela gerencia c1 e RATIFICADOS pelo operador em 05/11/2026; os acrescentados na R9 (a inscricao no psion e a formula SAT) e os da ParNaFaceDeFock (o modulo e as 10 declaracoes), da gerencia, ficam [DECLARADO] ate a ratificacao: a fala e' anterior a eles (recibo revisto de 05/11 ~19h30; D55;''')
rl.grava()
f = Arq("fechar_preparacao_v409.py")
f.troca("Os nomes (o modulo TraducaoTuring e as 72 declaracoes dele) foram dados pela gerencia c1 e ratificados pelo operador em 05/11/2026 (D55); os da ParNaFaceDeFock (o modulo e as 10 declaracoes), dados pela gerencia e ditos ratificados pelo cabecalho da pedra [DECLARADO];",
        "Os nomes: " + ST_A + " (D55);")
f.grava()
ac = Arq("acom_inscrever_prep_v409.py")
ac.troca("2 modulos (TraducaoTuring, com os nomes dados pela gerencia c1 e ratificados pelo operador em 05/11, D55; ParNaFaceDeFock, nomes da gerencia, ratificacao dita pelo cabecalho da pedra [DECLARADO]) no sandbox k409c;",
         "2 modulos (TraducaoTuring e ParNaFaceDeFock; " + ST_A + "; D55) no sandbox k409c;")
ac.grava()
