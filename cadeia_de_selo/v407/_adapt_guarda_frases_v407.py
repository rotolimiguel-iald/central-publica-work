# -*- coding: utf-8 -*-
"""_adapt_guarda_frases_v407.py -- adapta guarda_frases_v407.py (subida mecanica do molde v406) a v407: a cadeia de guardas (v405 -> v406 -> v407), o corpus das falas (03/11, 02/11 e 30/10-01/11), as 9 pedras, as frases proibidas novas e as limpas novas. Substituicoes de contagem EXATA; backup de bytes."""
import ast
import datetime
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "guarda_frases_v407.py")
raw = open(P, "rb").read()
open(P + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S"), "wb").write(raw)
t = raw.decode("utf-8")


def sub(old, new, n=1):
    global t
    assert t.count(old) == n, (old[:100], t.count(old), n)
    t = t.replace(old, new)


t = re.sub(r"(?m)^# \[A ADAPTAR v407\][^\n]*\n", "# [ADAPTADO v407] a guarda herda a cadeia v405 -> v406 -> v407; corpus das falas = 03/11 + 02/11 + 30/10-01/11; varre as 9 pedras\n", t, count=1)
sub('''_sp5 = _ilu.spec_from_file_location("runtime_v405", os.path.join(DL.V406, "runtime_v406.py")); _rt5 = _ilu.module_from_spec(_sp5); _sp5.loader.exec_module(_rt5)
RT._v405_guarda_frases = _rt5._v405_guarda_frases   # a guarda da v407 HERDA a da v406: dentro do um.py as duas vivem no mesmo modulo; aqui, fora dele, a da v406 e' injetada''',
    '''_sp5 = _ilu.spec_from_file_location("runtime_v405", os.path.join(DL.V405, "runtime_v405.py")); _rt5 = _ilu.module_from_spec(_sp5); _sp5.loader.exec_module(_rt5)
_sp6 = _ilu.spec_from_file_location("runtime_v406", os.path.join(DL.V406, "runtime_v406.py")); _rt6 = _ilu.module_from_spec(_sp6); _sp6.loader.exec_module(_rt6)
_rt6._v405_guarda_frases = _rt5._v405_guarda_frases   # a guarda da v406 chama a da v405 (dentro do um.py vivem no mesmo modulo; aqui, fora dele, a da v405 e' injetada na da v406)
RT._v406_guarda_frases = _rt6._v406_guarda_frases   # a guarda da v407 HERDA a da v406: idem (a da v406, ja' com a da v405 dentro, e' injetada na da v407)''')
sub("RT._v406_guarda_frases(", "RT._v407_guarda_frases(", t.count("RT._v406_guarda_frases("))
sub("(list(DL.VERBATIM_ORIGEM_V406) + list(DL.D5.VERBATIM_ORIGEM_V406))", "(list(DL.VERBATIM_ORIGEM_V407) + list(DL.VERBATIM_ORIGEM_V406) + list(DL.D5.VERBATIM_ORIGEM_V405))")
sub("o corpus das excecoes das pedras: as falas embutidas (os arquivos de VERBATIM_ORIGEM_V406)", "o corpus das excecoes das pedras: as falas embutidas (os arquivos de VERBATIM_ORIGEM_V407, V406 e V405)")
sub("# v407: as falas de 02/11 e as de 30/10 a 01/11 (a candidata e os textos podem citar as duas)", "# v407: as falas de 03/11, as de 02/11 e as de 30/10 a 01/11 (as pedras e os textos podem citar todas)")
sub('''    """a varredura das pedras da gerencia (v407: a candidata CanonicalFullTGLWitnessR1): {modulo: {violacoes, falas_retiradas}}."""
    falas = _falas_do_operador(); out = {}
    for s_ in ([DL.TESTEMUNHA] + list(DL.STONES)):   # v407: so' a candidata da gerencia (os 300 modulos da bancada nao sao texto da gerencia; DL.STONES e' vazio)''',
    '''    """a varredura das pedras da gerencia (v407: as 9 pedras de TGLExt/, na copia duravel normalizada v407\\\\pedra): {modulo: {violacoes, falas_retiradas}}."""
    falas = _falas_do_operador(); out = {}
    for s_ in list(DL.PEDRAS_V407):   # v407: as nove pedras da gerencia (os 301 modulos do fecho da v406 ja' foram varridos na v406)''')
# frases proibidas novas (as que afirmam demais sobre o psion, o canto e o par) e limpas novas
sub('''"CERTIFICATE_CONFIRMED", "CLOSURE_CONFIRMED", "QG_CONFIRMED", "FULLY_DERIVED", "ALL_DERIVED", "NOTHING_REMAINS_OPEN"]''',
    '''"CERTIFICATE_CONFIRMED", "CLOSURE_CONFIRMED", "QG_CONFIRMED", "FULLY_DERIVED", "ALL_DERIVED", "NOTHING_REMAINS_OPEN",
             # v407: as frases que afirmam demais sobre o psion, o canto e o par
             "o par na face de Fock está provado", "o par de psions na face de Fock foi construído", "o par de psíons na face de Fock está habitado", "the pair on the Fock face is proved", "the pair of psions on the Fock face is constructed",
             "Ω = Φ⁺", "Omega = Phi+", "o vácuo de Fock é o vetor de Bell", "the Fock vacuum is the Bell vector", "PAIR_CONFIRMED", "PSION_CONFIRMED", "CORNER_CONFIRMED", "PAIR_ON_THE_FOCK_FACE_PROVED"]''')
sub('''LIMPAS = [DL.FRASE_DA_MOLDURA_PT, DL.FRASE_DA_MOLDURA_EN, DL.FRASE_DA_MOLDURA_V407_PT, DL.FRASE_DA_MOLDURA_V407_EN,''',
    '''LIMPAS = [DL.FRASE_DA_MOLDURA_PT, DL.FRASE_DA_MOLDURA_EN, DL.FRASE_DA_MOLDURA_V406_PT, DL.FRASE_DA_MOLDURA_V406_EN, DL.FRASE_DA_MOLDURA_V407_PT, DL.FRASE_DA_MOLDURA_V407_EN, "o elo das duas faces e' de estrutura, nao de vetores", "the link of the two faces is one of structure, not of vectors", "o par na face de Fock segue [OPEN]", "the pair on the Fock face stays open",''')
open(P, "wb").write(t.encode("utf-8"))
ast.parse(t)
print("ok", len(t))
