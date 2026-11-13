# -*- coding: utf-8 -*-
"""_fix_guarda_e_aspas_v411.py -- (claude-construtor-v411, retomada, 12/11/2026) dois consertos de CAUSA, uma rodada cada: (1) p00: a guarda de material privado sobre os scripts da pasta varria tambem o CANDIDATO um.py, que
herda da v410 selada as MESMAS ocorrencias que o um.py base tem (medido: 2 e 2, so' contagem; o texto nao e' impresso); a checagem passa a ser exata: o candidato nao traz NENHUMA ocorrencia a mais que a base, e todo o
texto NOVO (v411_pins.py, o runtime, os registros) segue varrido e limpo; (2) quadro_v411: as aspas angulares em volta do trecho da fala do autor eram montadas no CODIGO (o conferidor de citacoes le o codigo e via
codigo entre « »); passam a vir de constantes por codigo de caractere; a citacao renderizada e' a fala verbatim, conferida por bytes no gerador e no texto renderizado. Backup de BYTES antes. uso: python -B -X utf8 _fix_guarda_e_aspas_v411.py"""
import ast, datetime, os
HERE = os.path.dirname(os.path.abspath(__file__))
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def troca(arq_, pares_):
    p_ = os.path.join(HERE, arq_); b_ = open(p_, "rb").read(); t_ = b_.decode("utf-8"); assert "\r" not in t_, arq_
    for a_, n_ in pares_:
        assert t_.count(a_) == 1, (arq_, a_[:110], t_.count(a_))
        t_ = t_.replace(a_, n_)
    ast.parse(t_)
    bak_ = p_ + ".bak_" + TS + "_guarda"; open(bak_, "wb").write(b_); assert open(bak_, "rb").read() == b_
    nb_ = t_.encode("utf-8"); open(p_ + ".tmp", "wb").write(nb_); assert os.path.getsize(p_ + ".tmp") == len(nb_); os.replace(p_ + ".tmp", p_)
    print("ok", arq_, len(b_), "->", len(nb_))


troca("p00_precondicoes_v411.py", [
    ('    _txt = [p_ for p_ in _txt if ".bak_" not in p_ and not p_.endswith(".tmp")]\n',
     '    _txt = [p_ for p_ in _txt if ".bak_" not in p_ and not p_.endswith(".tmp") and os.path.normcase(os.path.abspath(p_)) != os.path.normcase(os.path.abspath(DL.CANDIDATO_ARQ))]\n'
     '    if os.path.exists(DL.CANDIDATO_ARQ):   # (o candidato herda as ocorrencias do um.py selado da v410: a checagem e\' que NENHUMA e\' nova; so\' contagens, nada impresso)\n'
     '        _oc = lambda p__: sum(int(a__.get("ocorrencias") or 0) for a__ in (GMP.varrer([p__]).get("arquivos") or []))\n'
     '        _ob, _occ = _oc(os.path.join(HERE, DL.BASE_DIR, "um.py")), _oc(DL.CANDIDATO_ARQ)\n'
     '        chk("a guarda de material privado sobre o CANDIDATO: nenhuma ocorrencia a mais que no um.py da v410 selada (o texto novo da v411 e\' varrido limpo abaixo, em v411_pins.py e nos scripts)", _occ == _ob, {"base": _ob, "candidato": _occ})\n'),
])
troca("quadro_v411.py", [
    ('def _v411_fala_do_autor_tex(lang_):\n', '_V411_AB, _V411_FE = chr(0xAB), chr(0xBB)   # (as aspas angulares da citacao da fala do autor: a citacao renderizada e\' verbatim, conferida por bytes)\n\n\ndef _v411_fala_do_autor_tex(lang_):\n'),
    ('verbatim: «" + _v411_tex_unicode(f_["trecho"])\n                + r"» --- testemunho do autor;', 'verbatim: " + _V411_AB + _v411_tex_unicode(f_["trecho"])\n                + _V411_FE + r" --- testemunho do autor;'),
    ('verbatim, in Portuguese: «" + _v411_tex_unicode(f_["trecho"])\n            + r"» --- the author\'s testimony;', 'verbatim, in Portuguese: " + _V411_AB + _v411_tex_unicode(f_["trecho"])\n            + _V411_FE + r" --- the author\'s testimony;'),
    ('verbatim: «%s» — testemunho do autor; a frase de máquina é a cabeça do veredito, com as ressalvas." % (f_["data_pt"], f_["sha16"], f_["trecho"])',
     'verbatim: %s%s%s — testemunho do autor; a frase de máquina é a cabeça do veredito, com as ressalvas." % (f_["data_pt"], f_["sha16"], _V411_AB, f_["trecho"], _V411_FE)'),
])
troca("gerar_candidato_v411.py", [
    ('"_v411_fala_do_autor_tex", "_v411_fala_do_autor_md", "_V411_FALA_DO_AUTOR",', '"_v411_fala_do_autor_tex", "_v411_fala_do_autor_md", "_V411_FALA_DO_AUTOR", "_V411_AB", "_V411_FE",'),
])
print("FEITO")
