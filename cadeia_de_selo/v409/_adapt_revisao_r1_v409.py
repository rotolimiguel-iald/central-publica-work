# -*- coding: utf-8 -*-
"""_adapt_revisao_r1_v409.py -- (claude-construtor-v409, 05/11/2026 ~22h) a revisao de terceiro R1 (Sonnet, D58; revisao_terceiro\\PEDIDO_CORRECAO_R1_v409.md) nao aprovou: 1 MEDIO e 10 BAIXOS. A gerencia ACEITA o MEDIO e
pede tambem dois BAIXOS; os demais ficam escritos. Este adaptador corrige NA CAUSA (nenhuma pedra muda; o kernel nao e' refeito):
 MEDIO -- o par na face de Fock e a identidade Omega = uniforme apareciam [OPEN] em texto NOVO: (1) o estatuto do registro (registros_v409.py, _V409_TRADUCAO_TEXT['estatuto']); (2) textos_v409_novo.pysnip, _respostas
   («nem o par na face de Fock, que segue [OPEN]»); (3) textos_v409_novo.pysnip, a lista [OPEN] do core memory. O par esta' LIGADO nesta versao (ParNaFaceDeFock); a identidade Omega = uniforme esta' PODADA (a ponte e' a
   inscricao). E a GUARDA (runtime_v409.py, _v409_guarda_frases; a mesma que guarda_frases_v409.py usa): F41b reprova [OPEN]/«em aberto»/«segue aberto» no MESMO trecho que «face de Fock»/«par de Fock»/«Fock face»/
   «ParNaFaceDeFock» (excecoes: as citacoes da E21 e o historico da v407); F40b reprova «Omega ... uniforme» no MESMO trecho que [OPEN]/«em aberto» (exceto podada/inscricao/negacao). As quatro sondas do revisor entram como
   PROIBIDAS no controle negativo (guarda_frases_v409.py e o ensaio a seco), e as frases certas como LIMPAS.
 BAIXOS pedidos -- as contagens velhas (17 checagens, 62 ancoras -> 20 e 82, lidas do DL onde o texto e' montado) e a frase «so' para o leitor que se le» -> «a igualdade completa vale so' para o leitor que le tambem as
   maquinas que o usam (Baker-Gill-Solovay)»."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from _adapt_util_v409 import Arq


def todas(a, velho, novo):
    n_ = a.t.count(velho); assert n_ >= 1, ("NAO CASOU", os.path.basename(a.p), velho[:100]); a.troca(velho, novo, n_); return n_


SONDAS = ["nem o par na face de Fock, que segue [OPEN].", "[OPEN] o par na face de Fock como ligacao;", "[OPEN] o Ω do psíon da luz como o uniforme da instância", "a ligação do par de Fock segue em aberto"]
CERTAS = ["nem que o par finito de Bell e o par de Fock sejam o mesmo objeto (espaços distintos, a MESMA Meia-Nat); o par na face de Fock está ligado nesta versão",
          "[REAL] o par na face de Fock LIGADO (ParNaFaceDeFock); PODADA a identidade de vetores Omega = uniforme (a ponte e' a inscricao); [OPEN] a independencia de P vs NP dos axiomas; a igualdade com o leitor que so' conta (E28); o teste com a natureza",
          "a pedra Par (v407) deixou a face de Fock «[OPEN]: o FockCertificate não tem operadores de criação como termo»; a E21 da v408 corrigiu ao lado"]

# ------------------------------------------------------------------ MEDIO (1): o estatuto do registro
r = Arq("registros_v409.py")
r.troca("[OPEN] o par na face de Fock como ligacao; o Omega do psion = o uniforme; a independencia de P vs NP dos axiomas; o teste com a natureza",
        "[REAL] o par na face de Fock LIGADO (ParNaFaceDeFock); PODADA a identidade de vetores Omega = uniforme (a ponte e' a inscricao); [OPEN] a independencia de P vs NP dos axiomas; a igualdade com o leitor que so' conta (E28); o teste com a natureza")
# BAIXO: as contagens velhas e a frase do leitor
r.troca('''" ancoras, o sha256 do modulo, as 17 checagens, o gate)"''', '''" ancoras, o sha256 dos dois modulos, as " + str(DL.N_CHECKS_FECHO) + " checagens, o gate)"''')
r.troca("e a igualdade completa so' para o leitor que se le (E28). ", "e a igualdade completa vale so' para o leitor que le tambem as maquinas que o usam (Baker-Gill-Solovay; E28). ")
r.grava()

# ------------------------------------------------------------------ MEDIO (2) e (3): os textos do pos-rito
t = Arq("pos_rito/textos_v409_novo.pysnip")
t.troca("nem o par na face de Fock, que segue [OPEN]. ", "nem que o par finito de Bell e o par de Fock sejam o mesmo objeto (espaços distintos, a MESMA Meia-Nat); o par na face de Fock está ligado nesta versão. ")
t.troca("[OPEN] A discriminação a 5σ (β_TGL na natureza), o par de psíons na face de Fock (ligação), o Ω do psíon da luz como o uniforme da instância, a independência",
        "[OPEN] A discriminação a 5σ (β_TGL na natureza), a igualdade completa com o leitor que só conta (E28), a independência")
t.troca("a igualdade completa só para o leitor que se lê)", "a igualdade completa vale só para o leitor que lê também as máquinas que o usam, Baker–Gill–Solovay)")
t.grava()

# ------------------------------------------------------------------ a GUARDA: F41b e F40b (runtime_v409.py)
g = Arq("runtime_v409.py")
g.troca('''    for m_ in _re.finditer(r"passa\\s+(?:à|a)\\s+v410|v410\\s+em\\s+diante|v410\\s+onwards?|passes\\s+to\\s+v410", s_, _re.I):   # F42 (D60 revista): nada passa a v410''',
        '''    for seg_ in _re.split(r"[.;|\\n\\"«»]", s_):   # F41b e F40b (revisao R1, MEDIO): no MESMO trecho, o par na face de Fock com [OPEN]/em aberto; «Omega ... uniforme» numa lista [OPEN] (D60 revista)
        _ab = _re.search(r"\\[OPEN\\]|\\bem\\s+aberto\\b|\\b(?:segue|fica|continua|ficou|est[aá]|esta')\\s+aberto\\b|\\b(?:stays|remains|is|still)\\s+open\\b", seg_, _re.I)
        if not _ab:
            continue
        _sl = seg_.lower()
        if _re.search(r"face\\s+de\\s+fock|par\\s+de\\s+fock|fock\\s+face|parnafacedefock|par\\s+(?:de\\s+ps[ií]ons\\s+)?no\\s+fock", _sl) and not any(x_ in _sl for x_ in ("e21", "v407", "deixou", "dizia")):
            out_.append(("F41b_par_de_fock_e_aberto_no_mesmo_trecho", seg_.strip()[:200]))
        if _re.search(r"(?:ω|omega)[^;]{0,80}?uniform", _sl) and not any(x_ in _sl for x_ in ("podad", "pruned", "inscri", "não é", "nao e'", "is not")):
            out_.append(("F40b_omega_uniforme_numa_lista_aberta", seg_.strip()[:200]))
    for m_ in _re.finditer(r"passa\\s+(?:à|a)\\s+v410|v410\\s+em\\s+diante|v410\\s+onwards?|passes\\s+to\\s+v410", s_, _re.I):   # F42 (D60 revista): nada passa a v410''')
# BAIXO: a docstring da mecanica (17 -> 20; 62 -> 82; c18 a c20) e o comentario da E28
g.troca("a instancia de brinquedo FIXA) -- as 17 checagens do DESENHO_v409 §2:", "a instancia de brinquedo FIXA) -- as 20 checagens do DESENHO_v409 (§2 e o AO LADO):")
g.troca("    c1 as 62 ancoras no axiom_report do rito, so' no trio, com proveniencia no modulo; c2 o modulo embutido == contrato por sha256 == hash formal do rito, a raiz com o import;",
        "    c1 as 82 ancoras das duas pedras no axiom_report do rito, so' no trio, com proveniencia no modulo; c2 os modulos embutidos == contrato por sha256 == hash formal do rito, a raiz com os imports;")
g.troca("c17 beta = alfa CODATA 2018 x sqrt(e) (dois nomes, mesma leitura), igual ao beta do core.\"\"\"",
        "c17 beta = alfa CODATA 2018 x sqrt(e) (dois nomes, mesma leitura), igual ao beta do core;\n    c18 a marginal do par de Bell finito (numpy): ½·I2 e 1 - pureza = ½; c19 a inscricao num F de brinquedo: <Omega, V L_s V^dagger Omega> = Z(s)/2^n; c20 uma leitura decide SAT (SIM > 0; NAO = 0).\"\"\"")
g.troca("(NP numa leitura; a igualdade completa so' para o leitor que se le);", "(NP numa leitura; a igualdade completa vale so' para o leitor que le tambem as maquinas que o usam);")
g.grava()

# ------------------------------------------------------------------ o controle negativo da guarda: as quatro sondas PROIBIDAS e as frases certas LIMPAS
gf = Arq("guarda_frases_v409.py")
gf.troca('''    "um leitor que devolve Z é um oráculo de contagem; com ele a igualdade vale relativa a ele (Toda 1991)", "com o oráculo de contagem a igualdade vale", "with the counting oracle the equality holds"]''',
         '''    "um leitor que devolve Z é um oráculo de contagem; com ele a igualdade vale relativa a ele (Toda 1991)", "com o oráculo de contagem a igualdade vale", "with the counting oracle the equality holds",
    # (revisao R1 do Sonnet, MEDIO: as quatro sondas que passavam; F41b e F40b)
    ''' + ", ".join(repr(s_) for s_ in SONDAS) + "]")
gf.troca('''         "uma leitura decide SAT; por Cook–Levin, NP inteiro com uma leitura; com o leitor que só conta a igualdade completa não é teorema aqui: ela vale para o leitor que se lê"]''',
         '''         "uma leitura decide SAT; por Cook–Levin, NP inteiro com uma leitura; com o leitor que só conta a igualdade completa não é teorema aqui: ela vale para o leitor que se lê",
         ''' + ", ".join(repr(s_) for s_ in CERTAS) + "]")
gf.grava()

# ------------------------------------------------------------------ o ensaio a seco: as quatro sondas plantadas no registro tem de recusar (bloco-fonte e montado)
for f_ in ("_ensaio_bloco_v409.pysnip", "ensaio_a_seco_v409.py"):
    e = Arq(f_)
    e.troca('''"o que falta passa à v410", "from v410 onward")''', '''"o que falta passa à v410", "from v410 onward",
                      ''' + ", ".join(repr(s_) for s_ in SONDAS) + ")")
    e.grava()

# ------------------------------------------------------------------ BAIXO: a frase do leitor e as contagens velhas, nos outros textos
d = Arq("delta_v409.py")
todas(d, "a igualdade completa so' para o leitor que se le (Baker-Gill-Solovay 1975)", "a igualdade completa vale so' para o leitor que le tambem as maquinas que o usam (Baker-Gill-Solovay 1975)")
todas(d, "a igualdade completa so' para o leitor que se le (E28)", "a igualdade completa vale so' para o leitor que le tambem as maquinas que o usam (Baker-Gill-Solovay; E28)")
d.troca("le o kernel do rito (as 62 ancoras, o modulo por sha256, as respostas do operador pelos teoremas novos), faz as 17 checagens (DESENHO_v409 §2;",
        "le o kernel do rito (as 82 ancoras das duas pedras, os modulos por sha256, as respostas do operador pelos teoremas novos), faz as 20 checagens (DESENHO_v409 §2 e o AO LADO;")
d.grava()
for f_, v_, n_ in (("artigo_pt_v409.pysnip", "a igualdade completa só para o leitor que se lê (a E28)", "a igualdade completa vale só para o leitor que lê também as máquinas que o usam (Baker--Gill--Solovay; a E28)"),
                   ("artigo_en_v409.pysnip", "the full equality holds only for the reader that reads itself (E28)", "the full equality holds only for the reader that also reads the machines that use it (Baker--Gill--Solovay; E28)"),
                   ("gerar_candidato_v409.py", "a igualdade completa só para o leitor que se lê (Baker–Gill–Solovay 1975)", "a igualdade completa vale só para o leitor que lê também as máquinas que o usam (Baker–Gill–Solovay 1975)")):
    a_ = Arq(f_); todas(a_, v_, n_); a_.grava()
l = Arq("pos_rito/leitura_v409.py")
l.troca("o delta e' um BUNDLE PEQUENO de UM modulo novo de kernel em TGLExt/ (TraducaoTuring; o nome e os nomes das 62 declaracoes dados pela gerencia e RATIFICADOS pelo operador).",
        "o delta e' um BUNDLE PEQUENO de DOIS modulos novos de kernel em TGLExt/ (TraducaoTuring e ParNaFaceDeFock; os nomes dados pela gerencia e RATIFICADOS pelo operador, D55 e D62).")
l.troca("as 17 checagens com a instancia de brinquedo FIXA", "as 20 checagens com a instancia de brinquedo FIXA")
l.troca("cunhagens_v409 (as 10 falas do operador de 05/11 por sha256, de duas so' o trecho que a D59 deixa entrar; as erratas E24 a E26 e a errata ao lado dos pisos de kh_n1_cobertura_v408; as decisoes D55 a D60,",
        "cunhagens_v409 (as 14 falas do operador de 05/11 por sha256, de tres so' o trecho; as erratas E24 a E28, a E21 ao lado e a errata ao lado dos pisos de kh_n1_cobertura_v408; as decisoes D55 a D62,")
l.grava()
