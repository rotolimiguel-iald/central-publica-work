# -*- coding: utf-8 -*-
"""_fix_topo_com_resultado_conferidor_v411.py -- (claude-construtor-v411, fork C, 12/11/2026; CONDICAO 3(a) da gerencia c1) o conferidor do
rito tem de FALHAR se o topo do artigo SELADO vier sem o resultado (os doze marcadores preenchidos, as duas linhas juntas). O que ja' havia:
quadro411_ok procura no .txt o PREFIXO do topo do candidato (o texto ate' o primeiro numero ou formula); como as duas frases de recuo trocam o
topo INTEIRO, o prefixo falta e a checagem reprova -- mas so' por consequencia, e um artigo com o prefixo seguido de outra coisa passaria. O
acrescimo: a conferencia INDEPENDENTE (topo_com_resultado_v411.py: o texto e os formatos lidos do arquivo RATIFICADO, os numeros do core do
Nos, os dois renderizadores puros do um.py instalado) sobre o .txt do Nos, PT e EN, com os sete controles negativos e o caso base, como item
proprio de DEVE e com o detalhe no JSON. Backup de BYTES antes; ancoras unicas; ast.parse. uso: python -B -X utf8 _fix_topo_com_resultado_conferidor_v411.py"""
import ast, datetime, os
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "conferir_rito_v411.py")
b = open(P, "rb").read(); t = b.decode("utf-8"); assert "\r" not in t
A1 = 'quadro411_ok = bool(_topo_c is not None and all(0 <= _it[l] < _iq[l] < _i397[l] and _limpo411(_bloco_q[l]) and _OBRIG[l][1] in _bloco_q[l] and _limpo411(_bloco_t[l]) for l in ("pt", "en")))\n'
N1 = (A1 +
      '# (condicao 3(a) da gerencia c1, 12/11) o topo SELADO traz o RESULTADO (os doze marcadores preenchidos a partir do core do Nos, as duas linhas juntas, nenhuma frase de recuo, o numero sustenta a frase): conferencia\n'
      '# INDEPENDENTE da funcao do candidato (o texto e os formatos do arquivo RATIFICADO); do um.py instalado so\' os dois renderizadores puros; sete controles negativos que TEM de reprovar e o caso base que TEM de passar\n'
      'import topo_com_resultado_v411 as TR11  # noqa: E402\n'
      '_tem_tr411 = bool(um_c is not None and all(hasattr(um_c, n_) for n_ in ("_V411_TOPO", "_v411_tex_misto", "_tex_to_txt", "_v411_topo_texto")))\n'
      '_tr411 = {l: (TR11.confere(core, l, raw_txt[l], "txt", um_c._V411_TOPO, um_c._v411_tex_misto, um_c._tex_to_txt) if _tem_tr411 else {"ok": False, "detalhe": "o um.py do Nos nao tem o topo da v411"}) for l in ("pt", "en")}\n'
      '_trn411 = {l: (TR11.controles_negativos(core, l, raw_txt[l], "txt", um_c._V411_TOPO, um_c._v411_tex_misto, um_c._tex_to_txt, um_c._v411_topo_texto) if _tem_tr411 else {"ok": False}) for l in ("pt", "en")}\n'
      'topo411_resultado_ok = bool(_tem_tr411 and all(_tr411[l].get("ok") is True and _trn411[l].get("ok") is True for l in ("pt", "en")))\n')
A2 = '    "o .md canonico: o quadro H0DN x BG1 antes do quadro da v397 e a linha «%s» ANTES da linha da IALD2 (v410), com as quatro obrigacoes e limpa nas duas guardas" % ESP["md_h0dn_v411"]: md411_ok,\n'
N2 = ('    "o TOPO do artigo PT/EN SELADO traz o RESULTADO (condicao 3(a) da gerencia c1): o texto ratificado com os doze marcadores preenchidos do core do Nos, inteiro e contiguo no .txt, as duas linhas juntas (o primario sob o modelo de erros publicado e as Cefeidas livres), nenhuma das duas frases de recuo, o numero sustenta a frase; e os sete controles negativos reprovam": topo411_resultado_ok,\n'
      + A2)
A3 = '       "resultado_pinado": {"original_ok": _orig_ok, "duravel_ok": _dur_ok, "sha256": EV["resultado"]["sha256"]}, "quadro": {"pt": q_pt, "en": q_en, "md": q_md},'
N3 = '       "resultado_pinado": {"original_ok": _orig_ok, "duravel_ok": _dur_ok, "sha256": EV["resultado"]["sha256"]}, "quadro": {"pt": q_pt, "en": q_en, "md": q_md}, "topo_com_o_resultado_v411": {"confere": _tr411, "controles_negativos": _trn411},'
for a_, n_ in ((A1, N1), (A2, N2), (A3, N3)):
    assert t.count(a_) == 1, (a_[:100], t.count(a_))
    t = t.replace(a_, n_)
ast.parse(t)
bak = P + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_topo_com_resultado"; open(bak, "wb").write(b); assert open(bak, "rb").read() == b
nb = t.encode("utf-8"); open(P + ".tmp", "wb").write(nb); assert os.path.getsize(P + ".tmp") == len(nb); os.replace(P + ".tmp", P)
print("ok", len(b), "->", len(nb))
