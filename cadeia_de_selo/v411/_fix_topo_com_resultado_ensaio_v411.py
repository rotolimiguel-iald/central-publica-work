# -*- coding: utf-8 -*-
"""_fix_topo_com_resultado_ensaio_v411.py -- (claude-construtor-v411, fork C, 12/11/2026; CONDICAO 3(a) da gerencia c1) o ensaio a seco
tem de FALHAR se o topo do artigo selado vier sem o resultado (os doze marcadores preenchidos, as duas linhas juntas). Antes, a checagem
«topo_abre_o_paragrafo_de_apresentacao» comparava o artigo com a PROPRIA funcao do candidato sobre o MESMO core: com a fonte ausente, a funcao
devolve o recuo visivel e a checagem passaria. Agora _checagens_v411_do_artigo chama a conferencia INDEPENDENTE (topo_com_resultado_v411.py:
o texto e os formatos lidos do arquivo RATIFICADO, os numeros do core) sobre o .tex e o .txt, exige que a funcao do candidato devolva o mesmo
topo, e roda os sete controles negativos (que TEM de reprovar) e o caso base (que TEM de passar). O ensaio e' editado direto (o adaptador
_adapt_ensaio_v411.py ficou para tras: o pai editou o ensaio no passo 10). Backup de BYTES antes; ancoras unicas; ast.parse.
uso: python -B -X utf8 _fix_topo_com_resultado_ensaio_v411.py"""
import ast, datetime, os
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "ensaio_a_seco_v411.py")
b = open(P, "rb").read(); t = b.decode("utf-8"); assert "\r" not in t
PARES = [
    ('import guarda_frases_v411 as _GF11  # noqa: E402   (a guarda das frases da v411, com a UNICA excecao da P18: _GF11.p18_sem_cabeca)\n',
     'import guarda_frases_v411 as _GF11  # noqa: E402   (a guarda das frases da v411, com a UNICA excecao da P18: _GF11.p18_sem_cabeca)\n'
     'import topo_com_resultado_v411 as _TR11  # noqa: E402   (condicao 3(a) da gerencia c1, 12/11: o topo SELADO traz o resultado; a variante de recuo nunca passa como selo)\n'),
    ('            "a2_no_conversor": "^(" in inspect.getsource(um._tex_to_txt) and txt_.count("^(") >= 100, "violacoes": viol_[:4]}\n'
     '    out_["ok"] = bool(all(v_ is True for k_, v_ in out_.items() if k_ != "violacoes") and not viol_)\n',
     '            "a2_no_conversor": "^(" in inspect.getsource(um._tex_to_txt) and txt_.count("^(") >= 100, "violacoes": viol_[:4]}\n'
     '    # (condicao 3(a) da gerencia c1, 12/11) o topo do artigo traz o RESULTADO: a conferencia INDEPENDENTE (texto e formatos do arquivo ratificado, numeros do core) no .tex e no .txt; a funcao do\n'
     '    # candidato devolve o MESMO topo; e os sete controles negativos reprovam (sem a v397 no core; registro sem selar; marcador nao finito; texto != ratificado; o topo de recuo; sem a linha das Cefeidas livres; so\' o prefixo)\n'
     '    trx_ = _TR11.confere(c, lang_, tex_, "tex", um._V411_TOPO, um._v411_tex_misto, um._tex_to_txt); trt_ = _TR11.confere(c, lang_, txt_, "txt", um._V411_TOPO, um._v411_tex_misto, um._tex_to_txt)\n'
     '    cheio_, _ = _TR11.preencher(c, lang_, um._V411_TOPO.get("marcadores"))\n'
     '    trn_ = _TR11.controles_negativos(c, lang_, tex_, "tex", um._V411_TOPO, um._v411_tex_misto, um._tex_to_txt, um._v411_topo_texto)\n'
     '    trnt_ = _TR11.controles_negativos(c, lang_, txt_, "txt", um._V411_TOPO, um._v411_tex_misto, um._tex_to_txt, um._v411_topo_texto)\n'
     '    out_.update({"topo_com_o_resultado_tex": trx_["ok"] is True, "topo_com_o_resultado_txt": trt_["ok"] is True, "topo_do_candidato_e_o_preenchimento_independente": bool(cheio_ is not None and top_ == um._v411_tex_misto(cheio_) + " "),\n'
     '                 "topo_com_o_resultado_controles_negativos": trn_["ok"] is True and trnt_["ok"] is True})\n'
     '    out_["topo_com_o_resultado_detalhe"] = {"tex": {k_: v_ for k_, v_ in trx_.items() if k_ != "detalhe"}, "txt": {k_: v_ for k_, v_ in trt_.items() if k_ != "detalhe"}, "controles_negativos_tex": trn_, "controles_negativos_txt": trnt_,\n'
     '                                            "valores": trx_["detalhe"].get("valores"), "faltam_no_core": trx_["detalhe"].get("faltam_no_core")}\n'
     '    out_["ok"] = bool(all(v_ is True for k_, v_ in out_.items() if k_ not in ("violacoes", "topo_com_o_resultado_detalhe")) and not viol_)\n'),
]
for a_, n_ in PARES:
    assert t.count(a_) == 1, (a_[:100], t.count(a_))
    t = t.replace(a_, n_)
ast.parse(t)
bak = P + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_topo_com_resultado"; open(bak, "wb").write(b); assert open(bak, "rb").read() == b
nb = t.encode("utf-8"); open(P + ".tmp", "wb").write(nb); assert os.path.getsize(P + ".tmp") == len(nb); os.replace(P + ".tmp", P)
print("ok", len(b), "->", len(nb))
