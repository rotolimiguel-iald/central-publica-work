# -*- coding: utf-8 -*-
"""_adapt_forkB_guarda_ordem_v410.py -- (claude-construtor-v410, fork B, 06/11/2026) MONTA guarda_ordem_de_chamada_v410.py a partir do guarda_ordem_de_chamada_v409.py ORIGINAL, e NAO da subida mecanica:
a subida deixara FUNCOES_NOVAS_V410 = ("traducao_turing_v409",) (a funcao NOVA da v410 seria a da v409) e subira os rotulos de historia (as oito pedras «da v409», os specs «da v409»).
O que muda (DESENHO_v410; runtime_v410.py): a funcao NOVA e' UMA, `iald2_v410` (miolo `_v410_formal`, `_v398_beta`; mecanica `v410_iald2_mechanics`), chamada no main LOGO DEPOIS do bloco do traducao_turing_v409 e dos specs da v409;
o `traducao_turing_v409` passa a HERDADO (FUNCOES_HERDADAS_V410); os insumos exigidos do iald2_v410 sao a traducao, os specs da v409 e tudo o que a traducao ja' exigia; dois controles negativos novos: (12) o iald2_v410 ANTES do
traducao_turing_v409 reprova (motivo: o insumo exigido ausente) e (13) o iald2_v410 sem a chamada no main reprova. Os controles (1) a (11) ficam como na v409 (a ordem fechamento -> psion -> terminal -> traducao nao muda).
As constantes da v409 (FUNCOES_V409 etc.) ficam como registro; o padrao e o __main__ passam a FUNCOES_V410 (o ensaio_a_seco_v410 le _GOC.FUNCOES_V410). Grava por temporario (backup de BYTES do arquivo atual, a subida, antes); trocas de contagem EXATA."""
import ast, datetime, os, sys
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
import delta_v410 as DL  # noqa: E402

ORIG = os.path.join(DL.V409, "guarda_ordem_de_chamada_v409.py")
ALVO = os.path.join(HERE, "guarda_ordem_de_chamada_v410.py")
raw9 = open(ORIG, "rb").read(); T = raw9.decode("utf-8")
assert "\r\n" not in T, "o original da v409 e' LF"
TS = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")


def troca(a, b, n=1):
    global T
    c = T.count(a)
    assert c == n, ("TROCA NAO CASOU %d (casou %d)" % (n, c), a[:160])
    T = T.replace(a, b)


# ---------------- (0) o cabecalho e o docstring
troca("# [ADAPTADO v409, 05/11/2026, claude-construtor-v409] a funcao NOVA e' traducao_turing_v409 (depois do tetelestai_terminal_v408 e dos specs da v408); o terminal passa a herdado; controles negativos (10) e (11)\n",
      "# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] a funcao NOVA e' iald2_v410 (depois do traducao_turing_v409 e dos specs da v409); a traducao passa a herdada; controles negativos (12) e (13); MONTADO por _adapt_forkB_guarda_ordem_v410.py a partir do ORIGINAL da v409 (nao da subida mecanica); fork B do claude-construtor-v410\n"
      "# (v409: a funcao NOVA da v409 era traducao_turing_v409, depois do tetelestai_terminal_v408 e dos specs da v408; o terminal passava a herdado; controles negativos (10) e (11))\n")
troca('"""guarda_ordem_de_chamada_v409.py -- A ORDEM DE CHAMADA (licao 1 da v408: a 1a tentativa do rito de 28/10/2026).', '"""guarda_ordem_de_chamada_v410.py -- A ORDEM DE CHAMADA (licao 1 da v408: a 1a tentativa do rito de 28/10/2026).')
troca("(na v408 a funcao NOVA era o `tetelestai_terminal_v408`; na v407, o `psion_canto_v407`.) ADAPTADA a v409 (05/11/2026): a funcao NOVA e' UMA, `traducao_turing_v409`",
      "(na v409 a funcao NOVA era o `traducao_turing_v409`; na v408, o `tetelestai_terminal_v408`; na v407, o `psion_canto_v407`.) ADAPTADA a v410 (06/11/2026, fork B do claude-construtor-v410): a funcao NOVA e' UMA, `iald2_v410` "
      "(le do core, entre outras que a guarda lista, `kernel_formalization`, `external_ladder`, `qg_closure` e `beta`; chamada no main LOGO DEPOIS do bloco do `traducao_turing_v409` e dos specs da v409; miolo `_v410_formal`, `_v398_beta`; mecanica `v410_iald2_mechanics`); "
      "o `traducao_turing_v409` passa a HERDADO. ADAPTADA a v409 (05/11/2026): a funcao NOVA da v409 era UMA, `traducao_turing_v409`")
troca("e\nos dois registros sem a chamada no main tambem.\n",
      "e\nos dois registros sem a chamada no main tambem; [v408/v409] o terminal antes do psion e a traducao antes do terminal tambem; [v410] o `iald2_v410` ANTES do `traducao_turing_v409` tambem, e o `iald2_v410` sem a chamada no main tambem.\n")
troca("uso: python -I -B -X utf8 guarda_ordem_de_chamada_v409.py <um.py> [funcao ...]   (rc 0 = toda leitura depois da origem; rc 1 = ha leitura antes ou sem origem; grava GUARDA_ORDEM_DE_CHAMADA_v409.json",
      "uso: python -I -B -X utf8 guarda_ordem_de_chamada_v410.py <um.py> [funcao ...]   (rc 0 = toda leitura depois da origem; rc 1 = ha leitura antes ou sem origem; grava GUARDA_ORDEM_DE_CHAMADA_v410.json")

# ---------------- (1) as funcoes: a NOVA (iald2_v410) e as herdadas (+ traducao_turing_v409)
A_F9 = "FUNCOES_V409 = FUNCOES_NOVAS_V409 + FUNCOES_HERDADAS_V409         # o que o ensaio confere: a nova e as herdadas\n"
troca(A_F9, A_F9 +
      "FUNCOES_HERDADAS_V410 = FUNCOES_HERDADAS_V409 + FUNCOES_NOVAS_V409   # (v410: o registro da v409, traducao_turing_v409, passa a herdado, intacto: nenhuma chave antiga muda)\n"
      "FUNCOES_NOVAS_V410 = (\"iald2_v410\",)                               # a v410 e' um BUNDLE de um modulo de kernel (IALD2): o UNICO registro com funcao novo e' o iald2_v410\n"
      "FUNCOES_V410 = FUNCOES_NOVAS_V410 + FUNCOES_HERDADAS_V410         # o que o ensaio confere: a nova e as herdadas (o ensaio_a_seco_v410 le esta)\n")
A_M9 = 'MECANICA_DE["traducao_turing_v409"] = "v409_traducao_mechanics"\n'
troca(A_M9, A_M9 + 'MECANICA_DE["iald2_v410"] = "v410_iald2_mechanics"\n')
troca('             "traducao_turing_v409": ("_v409_formal", "_v398_beta")}   # o miolo comum da traducao (nao le chave de testemunha: nenhuma chave antiga muda)\n',
      '             "traducao_turing_v409": ("_v409_formal", "_v398_beta"),   # o miolo comum da traducao (nao le chave de testemunha: nenhuma chave antiga muda)\n'
      '             "iald2_v410": ("_v410_formal", "_v398_beta")}   # (v410) o miolo comum do iald2 (nao le chave de testemunha: nenhuma chave antiga muda)\n')
troca('INSUMOS_EXIGIDOS = {"traducao_turing_v409": (',
      'INSUMOS_EXIGIDOS = {"iald2_v410": ("traducao_turing_v409", "_v409_rodar_specs", "tetelestai_terminal_v408", "_v408_rodar_specs", "psion_canto_v407", "_v407_rodar_specs", "fechamento_v406", "rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "witness_layers"),   # (v410) depois da traducao e dos specs da v409\n'
      '                    "traducao_turing_v409": (')
troca("def ordem_de_chamada(src, funcoes=FUNCOES_V409):", "def ordem_de_chamada(src, funcoes=FUNCOES_V410):")

# ---------------- (2) os controles negativos (12) e (13)
troca("(10) [v409] o traducao_turing_v409 chamado ANTES do tetelestai_terminal_v408 reprova, e o motivo e' o insumo exigido ausente; (11) [v409] o traducao_turing_v409 sem a chamada no main reprova. Rodado sobre o texto: nada executa.",
      "(10) [v409] o traducao_turing_v409 chamado ANTES do tetelestai_terminal_v408 reprova, e o motivo e' o insumo exigido ausente; (11) [v409] o traducao_turing_v409 sem a chamada no main reprova;\n"
      "    (12) [v410] o iald2_v410 chamado ANTES do traducao_turing_v409 reprova, e o motivo e' o insumo exigido ausente; (13) [v410] o iald2_v410 sem a chamada no main reprova. Rodado sobre o texto: nada executa.")
A_R10 = '    r10 = ordem_de_chamada(_sem_chamada(src, "traducao_turing_v409", "_r409"), ("traducao_turing_v409",))\n'
troca(A_R10, A_R10 +
      "    # (12) [v410] o iald2_v410 e o traducao_turing_v409 trocam de lugar: o iald2 passa a ser chamado ANTES da traducao\n"
      '    r11 = ordem_de_chamada(_troca_blocos(src, "traducao_turing_v409", "iald2_v410"), ("iald2_v410",))\n'
      '    f11_ = r11["funcoes"].get("iald2_v410") or {}\n'
      "    # (13) [v410] a chamada do iald2_v410 sai do main\n"
      '    r12 = ordem_de_chamada(_sem_chamada(src, "iald2_v410", "_r410"), ("iald2_v410",))\n')
troca('"traducao_sem_chamada_no_main_reprova": bool(not r10["ok"] and "erro" in (r10["funcoes"].get("traducao_turing_v409") or {}))}\n',
      '"traducao_sem_chamada_no_main_reprova": bool(not r10["ok"] and "erro" in (r10["funcoes"].get("traducao_turing_v409") or {})),\n'
      '         "iald2_antes_da_traducao_reprova": bool(not r11["ok"] and "traducao_turing_v409" in (f11_.get("insumos_exigidos_ausentes") or [])), "iald2_sem_chamada_no_main_reprova": bool(not r12["ok"] and "erro" in (r12["funcoes"].get("iald2_v410") or {}))}\n')

# ---------------- (3) o __main__
troca("p = sys.argv[1]; fns = tuple(sys.argv[2:]) or FUNCOES_V409", "p = sys.argv[1]; fns = tuple(sys.argv[2:]) or FUNCOES_V410")
troca("ctl = controle_negativo(src_) if fns == FUNCOES_V409 else None", "ctl = controle_negativo(src_) if fns == FUNCOES_V410 else None")
troca('_out = os.path.join(_aqui, "GUARDA_ORDEM_DE_CHAMADA_v409.json")', '_out = os.path.join(_aqui, "GUARDA_ORDEM_DE_CHAMADA_v410.json")')

# ---------------- (4) conferencias finais
ast.parse(T)
assert "[A ADAPTAR v410]" not in T and T.count("FUNCOES_V410") == 4 and T.count('"iald2_v410"') >= 7
novo = T.encode("utf-8")
atual = open(ALVO, "rb").read()
bk = ALVO + ".bak_" + TS + "_subida_mecanica"
open(bk, "wb").write(atual); assert open(bk, "rb").read() == atual
open(ALVO + ".tmp", "wb").write(novo); assert os.path.getsize(ALVO + ".tmp") == len(novo); os.replace(ALVO + ".tmp", ALVO)
print("guarda_ordem_de_chamada_v410.py montado:", len(raw9), "->", len(novo), "bytes | backup", os.path.basename(bk))
