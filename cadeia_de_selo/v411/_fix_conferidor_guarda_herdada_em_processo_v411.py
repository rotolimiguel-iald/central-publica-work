# -*- coding: utf-8 -*-
"""_fix_conferidor_guarda_herdada_em_processo_v411.py -- (claude-construtor-v411, fork C, 12/11/2026, cadeia REAL) UMA rodada de conserto do achado do
harness do fechar em modo de depuracao (o conferidor roda dentro de um SANDBOX que copia uma lista explicita de arquivos): o conserto anterior do
conferidor (_fix_conferidor_guarda_herdada_v411.py) carregava a guarda das frases da v410 POR CAMINHO (..\\v410\\guarda_frases_v410.py, que puxa
runtime_v410.py e guarda_p18_v410.py), tres arquivos que o sandbox nao leva. A causa: eu fui buscar no disco o que ja' esta' em processo. A guarda da
v411 (guarda_frases_v411.py, na lista do sandbox) ja' carrega a funcao SELADA _v410_guarda_frases do um.py da v410 selada (base_um_v410, conferido por
sha256 contra o selo): e' ela, depois de retiradas as falas verbatim do operador (GF.sem_falas), que julga os trechos HERDADOS selados da v410.
Medido antes de trocar (script de diagnostico, fora de work): nas seis secoes herdadas do falso Nos (IALD2, A Escala e H0DN pre-registrado, PT e EN) a
funcao selada em processo da' 0 violacoes, igual a guarda da cadeia da v410 por caminho; e reprova as 300 frases PROIBIDAS da guarda da v410 (300 de
300). O conserto: o bloco do caminho sai; GF10.violacoes passa a ser a funcao selada em processo; e entra um controle negativo dos dois lados (tres
frases que ela TEM de reprovar -- F51, F52, F53 -- e a frase negada que TEM de passar), exigido em moldura_ok. Nenhum teste relaxado.
Backup de BYTES antes; ancoras unicas; ast.parse. uso: python -B -X utf8 _fix_conferidor_guarda_herdada_em_processo_v411.py"""
import ast, datetime, os
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "conferir_rito_v411.py")
b = open(P, "rb").read(); t = b.decode("utf-8"); assert "\r" not in t
A0 = ('# (fork C, 12/11) a guarda das frases da v410, por CAMINHO, para os trechos HERDADOS selados da v410 (a mesma politica do ensaio a seco, bloco 6j: as regras novas da v411, F60 a F67, julgam so\' o texto novo)\n'
      'import importlib.util as _ilu_gf10  # noqa: E402\n'
      '_d410_antes = sys.modules.get("delta_v410"); sys.modules["delta_v410"] = DL.D10; _path_antes = list(sys.path)\n'
      'try:\n'
      '    _sp_gf10 = _ilu_gf10.spec_from_file_location("guarda_frases_v410_herdada", os.path.join(DL.V410, "guarda_frases_v410.py")); GF10 = _ilu_gf10.module_from_spec(_sp_gf10); _sp_gf10.loader.exec_module(GF10)\n'
      'finally:\n'
      '    sys.modules["delta_v410"] = _d410_antes if _d410_antes is not None else DL; sys.path[:] = _path_antes   # (a ponte do quadro_v397 volta; a pasta da v410 sai do sys.path)\n')
N0 = ('# (fork C, 12/11) a guarda das frases da v410 para os trechos HERDADOS selados da v410 (a mesma politica do ensaio a seco, bloco 6j: as regras novas da v411, F60 a F67, julgam so\' o texto novo): a funcao SELADA\n'
      '# _v410_guarda_frases, que a guarda da v411 ja\' carrega do um.py da v410 selada (base_um_v410, conferido por sha256 contra o selo), depois de retiradas as falas verbatim do operador (GF.sem_falas).\n'
      '# Nenhum arquivo a mais e\' lido (o sandbox do harness do fechar copia uma lista explicita de arquivos); o controle negativo dos dois lados entra em moldura_ok.\n'
      'class GF10:   # (so\' o nome que os itens herdados usam: GF10.violacoes)\n'
      '    violacoes = staticmethod(lambda t_: GF.NS["_v410_guarda_frases"](GF.sem_falas(t_)))\n'
      '\n'
      '\n'
      '_GF10_REPROVA = ("o atrator foi observado na natureza", "o Nome esgota o ser", "o teste deu 5 sigma atingido")   # (F51, F52 e F53 da guarda selada da v410)\n'
      '_GF10_PASSA = "o Nome nao esgota o ser; o atrator nao foi observado: nenhum teste com a natureza"\n'
      'gf10_controle_ok = bool(all(GF10.violacoes(f_) for f_ in _GF10_REPROVA) and not GF10.violacoes(_GF10_PASSA))\n')
A1 = 'and _frase_no_artigo and secao411_ok and (GF.controle_negativo() or {}).get("ok") is True)'
N1 = 'and _frase_no_artigo and secao411_ok and (GF.controle_negativo() or {}).get("ok") is True and gf10_controle_ok)'
for a_, n_ in ((A0, N0), (A1, N1)):
    assert t.count(a_) == 1, (a_[:100], t.count(a_))
    t = t.replace(a_, n_)
assert "guarda_frases_v410.py" not in t and "_ilu_gf10" not in t
ast.parse(t)
bak = P + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_guarda_em_processo"; open(bak, "wb").write(b); assert open(bak, "rb").read() == b
nb = t.encode("utf-8"); open(P + ".tmp", "wb").write(nb); assert os.path.getsize(P + ".tmp") == len(nb); os.replace(P + ".tmp", P)
print("ok", len(b), "->", len(nb))
