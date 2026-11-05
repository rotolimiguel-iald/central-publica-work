# -*- coding: utf-8 -*-
"""_adapt_guarda_ordem_v408.py -- adapta guarda_ordem_de_chamada_v408.py (subida mecanica) a v408: a funcao NOVA e' tetelestai_terminal_v408 (le kernel_formalization, external_ladder, qg_closure e beta; miolo _v408_formal e _v398_beta; mecanica v408_terminal_mechanics);
as herdadas ganham o psion_canto_v407; os insumos exigidos do terminal sao os registros que o main roda antes (psion_canto_v407, _v407_rodar_specs, fechamento_v406, ...). Controles negativos novos: o terminal chamado ANTES do psion reprova; o terminal sem chamada no main reprova.
Trocas de contagem EXATA; backup de bytes; retira a marca. Escrito pela ferramenta Write."""
import ast, datetime, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "guarda_ordem_de_chamada_v408.py")
raw = open(P, "rb").read(); open(P + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_adapt", "wb").write(raw)
t = raw.decode("utf-8"); assert "\r\n" not in t


def sub(old, new, n=1):
    global t
    assert t.count(old) == n, (old[:100], t.count(old), n); t = t.replace(old, new)


t = re.sub(r"(?m)^# \[A ADAPTAR v408\][^\n]*\n", "", t, count=1)
sub('FUNCOES_HERDADAS_V408 = FUNCOES_HERDADAS_V407 + ("fechamento_v406",)   # (v408: o registro da v407 e\' herdado; so\' a checagem c8 da mecanica muda)',
    'FUNCOES_HERDADAS_V408 = FUNCOES_HERDADAS_V407 + ("fechamento_v406", "psion_canto_v407")   # (v408: os registros da v406 e da v407 sao herdados, intactos: nenhuma chave antiga muda)')
sub('FUNCOES_NOVAS_V408 = ("psion_canto_v407",)                         # a v408 e\' um BUNDLE de nove modulos de kernel: o UNICO registro com funcao novo e\' o do psion e do canto',
    'FUNCOES_NOVAS_V408 = ("tetelestai_terminal_v408",)                 # a v408 e\' um BUNDLE de quatro modulos de kernel: o UNICO registro com funcao novo e\' o do terminal')
sub('MECANICA_DE["psion_canto_v407"] = "v407_psion_mechanics"\n', 'MECANICA_DE["psion_canto_v407"] = "v407_psion_mechanics"\nMECANICA_DE["tetelestai_terminal_v408"] = "v408_terminal_mechanics"\n')
sub('             "psion_canto_v407": ("_v407_formal", "_v407_chaves", "_v398_beta")}   # o miolo comum do psion (a leitura das chaves, a da v408 e as quatro da v407, esta em _v407_chaves)',
    '             "psion_canto_v407": ("_v407_formal", "_v407_chaves", "_v398_beta"),   # o miolo comum do psion (a leitura das chaves, a da v407 e as quatro da v406, esta em _v407_chaves)\n'
    '             "tetelestai_terminal_v408": ("_v408_formal", "_v398_beta")}   # o miolo comum do terminal (nao le chave de testemunha: nenhuma chave antiga muda)')
sub('INSUMOS_EXIGIDOS = {"psion_canto_v407": ("fechamento_v406", "rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "witness_layers", "_v405_rodar_specs"),',
    'INSUMOS_EXIGIDOS = {"tetelestai_terminal_v408": ("psion_canto_v407", "_v407_rodar_specs", "fechamento_v406", "rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "witness_layers"),\n'
    '                    "psion_canto_v407": ("fechamento_v406", "rede_fock_v394", "psibit_v395", "testemunha_estatica_v396", "witness_layers", "_v405_rodar_specs"),')
sub('    (5) [v406] o fechamento_v406 sem a chamada no main reprova (nunca «ok» por omissao); (6) [v407] o psion_canto_v407 chamado ANTES do fechamento_v406 (as duas instrucoes trocam de lugar) reprova, e o motivo e\' o insumo exigido ausente; (7) [v407] o psion_canto_v407 sem a chamada no main reprova. Rodado sobre o texto: nada executa."""',
    '    (5) [v406] o fechamento_v406 sem a chamada no main reprova (nunca «ok» por omissao); (6) [v407] o psion_canto_v407 chamado ANTES do fechamento_v406 (as duas instrucoes trocam de lugar) reprova, e o motivo e\' o insumo exigido ausente; (7) [v407] o psion_canto_v407 sem a chamada no main reprova;\n'
    '    (8) [v408] o tetelestai_terminal_v408 chamado ANTES do psion_canto_v407 reprova, e o motivo e\' o insumo exigido ausente; (9) [v408] o tetelestai_terminal_v408 sem a chamada no main reprova. Rodado sobre o texto: nada executa."""')
sub('    r6 = ordem_de_chamada(_sem_chamada(src, "psion_canto_v407", "_r407"), ("psion_canto_v407",))\n',
    '    r6 = ordem_de_chamada(_sem_chamada(src, "psion_canto_v407", "_r407"), ("psion_canto_v407",))\n'
    '    # (8) o tetelestai_terminal_v408 e o psion_canto_v407 trocam de lugar: o terminal passa a ser chamado ANTES do psion\n'
    '    r7 = ordem_de_chamada(_troca_blocos(src, "psion_canto_v407", "tetelestai_terminal_v408"), ("tetelestai_terminal_v408",))\n'
    '    f7_ = r7["funcoes"].get("tetelestai_terminal_v408") or {}\n'
    '    # (9) a chamada do tetelestai_terminal_v408 sai do main\n'
    '    r8 = ordem_de_chamada(_sem_chamada(src, "tetelestai_terminal_v408", "_r408"), ("tetelestai_terminal_v408",))\n')
sub('         "psion_antes_do_fechamento_reprova": bool(not r5["ok"] and "fechamento_v406" in (f5_.get("insumos_exigidos_ausentes") or [])), "psion_sem_chamada_no_main_reprova": bool(not r6["ok"] and "erro" in (r6["funcoes"].get("psion_canto_v407") or {}))}',
    '         "psion_antes_do_fechamento_reprova": bool(not r5["ok"] and "fechamento_v406" in (f5_.get("insumos_exigidos_ausentes") or [])), "psion_sem_chamada_no_main_reprova": bool(not r6["ok"] and "erro" in (r6["funcoes"].get("psion_canto_v407") or {})),\n'
    '         "tetelestai_antes_do_psion_reprova": bool(not r7["ok"] and "psion_canto_v407" in (f7_.get("insumos_exigidos_ausentes") or [])), "tetelestai_sem_chamada_no_main_reprova": bool(not r8["ok"] and "erro" in (r8["funcoes"].get("tetelestai_terminal_v408") or {}))}')
assert "[A ADAPTAR" not in t
ast.parse(t); open(P, "wb").write(t.encode("utf-8")); print("ok guarda_ordem", len(t))
