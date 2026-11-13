# -*- coding: utf-8 -*-
"""_adapt_guarda_ordem_v411.py -- (claude-construtor-v411, fork C, 12/11/2026) monta guarda_ordem_de_chamada_v411.py a partir do ORIGINAL ..\\v410\\guarda_ordem_de_chamada_v410.py: a funcao NOVA da v411 e' UMA,
h0dn_bg1_v411 (mecanica v411_h0dn_mechanics; miolo _v398_beta; le qg_closure, external_ladder e h0dn_bg1_v410, todas do main/run_um), chamada no main LOGO DEPOIS do bloco da v410 (h0dn_fontes_hms13_v410 e os specs
da v410); os quatro registros da v410 passam a HERDADOS, intactos; controles negativos novos (18) o h0dn_bg1_v411 ANTES do h0dn_fontes_hms13_v410 reprova (insumo exigido ausente) e (19) sem a chamada no main reprova.
A saida GUARDA_ORDEM_DE_CHAMADA_v411.json vai para DL.saida quando o delta da v411 carrega (no rito o script nao e' usado). Backup de BYTES do destino antes. uso: python -B -X utf8 _adapt_guarda_ordem_v411.py"""
import ast, datetime, os
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), "v410", "guarda_ordem_de_chamada_v410.py")
DST = os.path.join(HERE, "guarda_ordem_de_chamada_v411.py")
t = open(SRC, "rb").read().decode("utf-8"); assert "\r" not in t
l1 = t.split("\n", 1)[0]
cab = ("# [ADAPTADO v411, 12/11/2026, claude-construtor-v411 (retomada, fork C)] montado por _adapt_guarda_ordem_v411.py do ORIGINAL v410/guarda_ordem_de_chamada_v410.py: a funcao NOVA e' h0dn_bg1_v411 (depois do h0dn_fontes_hms13_v410 e dos specs da v410);"
       " os quatro registros da v410 passam a herdados; controles negativos (18) e (19)\n")
assert l1.startswith("# -*- coding")
PARES = [
    (l1 + "\n", l1 + "\n" + cab),
    ('"""guarda_ordem_de_chamada_v410.py -- A ORDEM DE CHAMADA', '"""guarda_ordem_de_chamada_v411.py -- (v411: a funcao NOVA e\' h0dn_bg1_v411, LOGO DEPOIS do bloco da v410; as da v410 passam a herdadas) A ORDEM DE CHAMADA'),
    ("uso: python -I -B -X utf8 guarda_ordem_de_chamada_v410.py <um.py> [funcao ...]", "uso: python -I -B -X utf8 guarda_ordem_de_chamada_v411.py <um.py> [funcao ...]"),
    ("grava GUARDA_ORDEM_DE_CHAMADA_v410.json ao lado do script", "grava GUARDA_ORDEM_DE_CHAMADA_v411.json em DL.saida (a pasta da cadeia, ou a de ensaio)"),
    ("FUNCOES_V410 = FUNCOES_NOVAS_V410 + FUNCOES_HERDADAS_V410         # o que o ensaio confere: a nova e as herdadas (o ensaio_a_seco_v410 le esta)\n",
     "FUNCOES_V410 = FUNCOES_NOVAS_V410 + FUNCOES_HERDADAS_V410         # (registro da v410)\n"
     "FUNCOES_HERDADAS_V411 = FUNCOES_HERDADAS_V410 + FUNCOES_NOVAS_V410   # (v411: os quatro registros com funcao da v410 passam a herdados, intactos: nenhuma chave antiga muda)\n"
     "FUNCOES_NOVAS_V411 = (\"h0dn_bg1_v411\",)                          # a v411 NAO tem modulo novo de kernel; o UNICO registro com funcao novo e' o do teste H0DN x BG1 ABERTO (recalculado dos bytes embutidos)\n"
     "FUNCOES_V411 = FUNCOES_NOVAS_V411 + FUNCOES_HERDADAS_V411         # o que o ensaio confere: a nova e as herdadas (o ensaio_a_seco_v411 le esta)\n"),
    ('MECANICA_DE["h0dn_fontes_hms13_v410"] = "_v410_hms13_mechanics"   # (v410, D80: o recibo documental HMS/13, na instrucao SEGUINTE do main)\n',
     'MECANICA_DE["h0dn_fontes_hms13_v410"] = "_v410_hms13_mechanics"   # (v410, D80: o recibo documental HMS/13, na instrucao SEGUINTE do main)\n'
     'MECANICA_DE["h0dn_bg1_v411"] = "v411_h0dn_mechanics"   # (v411: o teste aberto, recalculado no rito)\n'),
    ('             "h0dn_fontes_hms13_v410": ("_v398_beta",),\n', '             "h0dn_fontes_hms13_v410": ("_v398_beta",),\n             "h0dn_bg1_v411": ("_v398_beta",),   # (v411) le qg_closure, external_ladder e core["h0dn_bg1_v410"] (gravado no bloco da v410)\n'),
    ('INSUMOS_EXIGIDOS = {"h0dn_bg1_v410": ',
     'INSUMOS_EXIGIDOS = {"h0dn_bg1_v411": ("h0dn_fontes_hms13_v410", "_v410_rodar_specs", "iald2_v410", "a_escala_v410", "h0dn_bg1_v410", "traducao_turing_v409", "_v409_rodar_specs", "tetelestai_terminal_v408", "_v408_rodar_specs", "psion_canto_v407", "_v407_rodar_specs", "fechamento_v406", "rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "witness_layers"),   # (v411) depois do bloco INTEIRO da v410 (o hms13 e os specs da v410)\n'
     '                    "h0dn_bg1_v410": '),
    ("def ordem_de_chamada(src, funcoes=FUNCOES_V410):", "def ordem_de_chamada(src, funcoes=FUNCOES_V411):"),
    ("(14) [v410, D72] o h0dn_bg1_v410 sem a chamada no main reprova (a linha traz comentario: a troca e' por prefixo). Rodado sobre o texto: nada executa.\"\"\"",
     "(14) [v410, D72] o h0dn_bg1_v410 sem a chamada no main reprova (a linha traz comentario: a troca e' por prefixo); (15) a (17) [v410] o hms13 e o a_escala;\n"
     "    (18) [v411] o h0dn_bg1_v411 chamado ANTES do h0dn_fontes_hms13_v410 reprova, e o motivo e' o insumo exigido ausente; (19) [v411] o h0dn_bg1_v411 sem a chamada no main reprova. Rodado sobre o texto: nada executa.\"\"\""),
    ('    r16 = ordem_de_chamada("\\n".join(m17_), ("a_escala_v410",))\n',
     '    r16 = ordem_de_chamada("\\n".join(m17_), ("a_escala_v410",))\n'
     '    # (18) [v411] a instrucao do h0dn_bg1_v411 trocada de lugar com a do hms13: o h0dn v411 passa a vir ANTES do bloco da v410\n'
     '    r17 = ordem_de_chamada(_troca_blocos(src, "h0dn_fontes_hms13_v410", "h0dn_bg1_v411"), ("h0dn_bg1_v411",))\n'
     '    f17_ = r17["funcoes"].get("h0dn_bg1_v411") or {}\n'
     '    # (19) [v411] a chamada do h0dn_bg1_v411 sai do main (a linha e\' `_h411 = h0dn_bg1_v411(core)`: troca por prefixo)\n'
     '    _l11 = [i for i, l in enumerate(linhas) if re.match(r"\\s+_h411 = h0dn_bg1_v411\\(core\\)", l)]; assert len(_l11) == 1, ("a linha da chamada do h0dn_bg1_v411 nao foi achada uma vez", _l11)\n'
     '    m19_ = list(linhas); m19_[_l11[0]] = m19_[_l11[0]].replace("h0dn_bg1_v411(core)", "{}", 1)\n'
     '    r18 = ordem_de_chamada("\\n".join(m19_), ("h0dn_bg1_v411",))\n'),
    ('         "aescala_sem_chamada_no_main_reprova": bool(not r16["ok"] and "erro" in (r16["funcoes"].get("a_escala_v410") or {}))}',
     '         "aescala_sem_chamada_no_main_reprova": bool(not r16["ok"] and "erro" in (r16["funcoes"].get("a_escala_v410") or {})),\n'
     '         "h0dn_v411_antes_do_hms13_reprova": bool(not r17["ok"] and "h0dn_fontes_hms13_v410" in (f17_.get("insumos_exigidos_ausentes") or [])), "h0dn_v411_sem_chamada_no_main_reprova": bool(not r18["ok"] and "erro" in (r18["funcoes"].get("h0dn_bg1_v411") or {}))}'),
    ("    p = sys.argv[1]; fns = tuple(sys.argv[2:]) or FUNCOES_V410\n", "    p = sys.argv[1]; fns = tuple(sys.argv[2:]) or FUNCOES_V411\n"),
    ("    ctl = controle_negativo(src_) if fns == FUNCOES_V410 else None\n", "    ctl = controle_negativo(src_) if fns == FUNCOES_V411 else None\n"),
    ('    _out = os.path.join(_aqui, "GUARDA_ORDEM_DE_CHAMADA_v410.json")\n',
     '    try:   # (v411) a saida vai para DL.saida (a pasta da cadeia, ou a de ensaio com V411_ENSAIO_TOPO_PROPOSTO=1)\n'
     '        sys.path.insert(0, _aqui); import delta_v411 as _DL11\n'
     '        _out = _DL11.saida("GUARDA_ORDEM_DE_CHAMADA_v411.json")\n'
     '    except Exception:   # noqa: BLE001 (sem o delta, ao lado do script, como na v410)\n'
     '        _out = os.path.join(_aqui, "GUARDA_ORDEM_DE_CHAMADA_v411.json")\n'),
]
for a_, n_ in PARES:
    assert t.count(a_) == 1, (a_[:100], t.count(a_))
    t = t.replace(a_, n_, 1)
ast.parse(t)
b0 = open(DST, "rb").read()
bak = DST + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_forkc"; open(bak, "wb").write(b0); assert open(bak, "rb").read() == b0
nb = t.encode("utf-8"); open(DST + ".tmp", "wb").write(nb); assert os.path.getsize(DST + ".tmp") == len(nb); os.replace(DST + ".tmp", DST)
print("ok", DST, len(b0), "->", len(nb))
