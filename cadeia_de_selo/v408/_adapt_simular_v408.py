# -*- coding: utf-8 -*-
"""_adapt_simular_v408.py -- adapta simular_arvore_do_nos_v408.py (subida mecanica) a v408: o registro NOVO tetelestai_terminal_v408 e os specs da v408 rodam NA ORDEM DO MAIN depois dos da v407; os tres registros da v408 entram na lista conferida; a chave do lema (v407) segue conferida (herdada).
Trocas de contagem EXATA; backup de bytes; retira a marca. Escrito pela ferramenta Write."""
import ast, datetime, os, re
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "simular_arvore_do_nos_v408.py")
raw = open(P, "rb").read(); open(P + ".bak_" + datetime.datetime.now().strftime("%Y%m%d_%H%M%S") + "_adapt", "wb").write(raw)
t = raw.decode("utf-8"); assert "\r\n" not in t


def sub(old, new, n=1):
    global t
    assert t.count(old) == n, (old[:100], t.count(old), n); t = t.replace(old, new)


t = re.sub(r"(?m)^# \[A ADAPTAR v408\][^\n]*\n", "", t, count=1)
t = re.sub(r"(?m)^# ADAPTADO a v408 \(03/11/2026, claude-prep-v408\):[^\n]*\n", "# ADAPTADO a v408 (04/11/2026, claude-construtor-v408): molde v407/simular_arvore_do_nos_v407.py; bundle de 4 modulos em TGLExt/ (TetelestaiTerminal, TempoIgualMoeda, PontoDeContradicao, PIgualNP), registro tetelestai_terminal_v408 + specs cunhagens_v408/kh_n1_cobertura_v408 chamados NA ORDEM DO MAIN depois dos da v407 (herdados); a chave do lema (v407) segue conferida como herdada; nenhuma chave antiga muda.\n", t, count=1)
sub("um.psion_canto_v407(core); um._v407_rodar_specs(core)", "um.psion_canto_v407(core); um._v407_rodar_specs(core); um.tetelestai_terminal_v408(core); um._v408_rodar_specs(core)")
sub('for k in ("psion_canto_v407", "cunhagens_v407", "kh_n1_cobertura_v407", "fechamento_v406",', 'for k in ("tetelestai_terminal_v408", "cunhagens_v408", "kh_n1_cobertura_v408", "psion_canto_v407", "cunhagens_v407", "kh_n1_cobertura_v407", "fechamento_v406",')
sub("# (v408) A CHAVE DO LEMA sobre a arvore simulada:", "# (v407, HERDADO na v408: nenhuma chave antiga muda) A CHAVE DO LEMA sobre a arvore simulada:")
assert "[A ADAPTAR" not in t
ast.parse(t); open(P, "wb").write(t.encode("utf-8")); print("ok simular", len(t))
