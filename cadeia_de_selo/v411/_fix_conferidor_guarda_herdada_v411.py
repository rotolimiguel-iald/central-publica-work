# -*- coding: utf-8 -*-
"""_fix_conferidor_guarda_herdada_v411.py -- (claude-construtor-v411, fork C, 12/11/2026, cadeia REAL) UMA rodada de conserto do achado do
teste_conferidor_positivo_v411.py (falso Nos do candidato real 21e87eb3df5098f8): NAO BATE em quatro itens HERDADOS da v410 -- a secao A Escala,
a secao do H0DN pre-registrado, o paragrafo do recibo HMS/13 e A MOLDURA. Medido (diagnostico por script sobre o .txt do falso Nos): os trechos
estao la' e na ordem; o que reprova e' a GUARDA: o conferidor julga o texto SELADO da v410 com a guarda da v411 (F60 «confirmacao expressa e' do
operador», F61 e F67 no titulo da secao pre-registrada, escrita antes da abertura), e a guarda da v410 o deixa limpo. A causa: na adaptacao, o
GF do conferidor virou guarda_frases_v411 para TUDO. A politica da cadeia, escrita no ensaio a seco (bloco 6j: «a guarda das frases da v410, por
CAMINHO, para os textos HERDADOS ...; as regras novas da v411, F60 a F67, julgam so' o texto novo»), e' outra. O conserto: o conferidor carrega a
guarda da v410 por caminho (com a ponte delta_v410 -> o delta da v410 SO' durante a carga, restaurada depois; a pasta da v410 sai do sys.path) e
a usa nos trechos HERDADOS selados (_secA, _secH, _sec410); o texto novo (os registros da v411, a secao, o quadro e o topo da v411) segue julgado
pela guarda da v411. Nenhum teste relaxado: a guarda da v410 e' a que selou esses trechos. Backup de BYTES antes; ancoras unicas; ast.parse.
uso: python -B -X utf8 _fix_conferidor_guarda_herdada_v411.py"""
import ast, datetime, os
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "conferir_rito_v411.py")
b = open(P, "rb").read(); t = b.decode("utf-8"); assert "\r" not in t
A0 = 'import guarda_frases_v411 as GF  # noqa: E402   # (a guarda das frases da v411: a mesma funcao do um.py; a P18 com a UNICA excecao da cabeca)\n'
N0 = (A0 +
      '# (fork C, 12/11) a guarda das frases da v410, por CAMINHO, para os trechos HERDADOS selados da v410 (a mesma politica do ensaio a seco, bloco 6j: as regras novas da v411, F60 a F67, julgam so\' o texto novo)\n'
      'import importlib.util as _ilu_gf10  # noqa: E402\n'
      '_d410_antes = sys.modules.get("delta_v410"); sys.modules["delta_v410"] = DL.D10; _path_antes = list(sys.path)\n'
      'try:\n'
      '    _sp_gf10 = _ilu_gf10.spec_from_file_location("guarda_frases_v410_herdada", os.path.join(DL.V410, "guarda_frases_v410.py")); GF10 = _ilu_gf10.module_from_spec(_sp_gf10); _sp_gf10.loader.exec_module(GF10)\n'
      'finally:\n'
      '    sys.modules["delta_v410"] = _d410_antes if _d410_antes is not None else DL; sys.path[:] = _path_antes   # (a ponte do quadro_v397 volta; a pasta da v410 sai do sys.path)\n')
PARES = [(A0, N0),
         ('not GF.violacoes(_secA["pt"]) and not GF.violacoes(_secA["en"])', 'not GF10.violacoes(_secA["pt"]) and not GF10.violacoes(_secA["en"])'),
         ('not GF.violacoes(_sec410["pt"]) and not GF.violacoes(_sec410["en"])', 'not GF10.violacoes(_sec410["pt"]) and not GF10.violacoes(_sec410["en"])')]
for a_, n_ in PARES:
    assert t.count(a_) == 1, (a_[:100], t.count(a_))
    t = t.replace(a_, n_)
a3 = 'not GF.violacoes(_secH["pt"]) and not GF.violacoes(_secH["en"])'
assert t.count(a3) == 2, t.count(a3)   # (a secao do H0DN da v410 e o paragrafo do recibo HMS/13 no fim dela)
t = t.replace(a3, 'not GF10.violacoes(_secH["pt"]) and not GF10.violacoes(_secH["en"])')
assert "GF.violacoes(_sec" not in t
ast.parse(t)
bak = P + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_guarda_herdada"; open(bak, "wb").write(b); assert open(bak, "rb").read() == b
nb = t.encode("utf-8"); open(P + ".tmp", "wb").write(nb); assert os.path.getsize(P + ".tmp") == len(nb); os.replace(P + ".tmp", P)
print("ok", len(b), "->", len(nb))
