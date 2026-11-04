# -*- coding: utf-8 -*-
"""03/11/2026 06:3x, gerencia c1 (a unica que escreve no indice e nos topicos): (1) entrada datada no fim do topico construir-tudo-o-fechamento-02nov.md (append, backup de bytes);
(2) o ponteiro `· [v406](licoes-custodia-v406-03nov.md)` na linha da G1 do MEMORY.md (ao lado do da v405; limites <= 195 linhas, <= 24.000 B; backup de bytes); (3) memoria.py pinar
e verificar. Escrito pelo Write."""
import os, subprocess, time
from pathlib import Path
MEMD = Path(r"C:\Users\rotol\.claude\projects\c--IALD-Central-de-Patentes\memory"); FILA = MEMD / "fila"; MEM = MEMD / "MEMORY.md"; TOP = MEMD / "construir-tudo-o-fechamento-02nov.md"
PY = r"C:\Python314\python.exe"; ENV = dict(os.environ, MEMORIA_GERENCIA="claude-c1"); TS = time.strftime("%Y%m%d_%H%M%S")
assert (MEMD / "licoes-custodia-v406-03nov.md").is_file()


def troca_bytes(p, f, rot):
    b = p.read_bytes(); novo = f(b); assert novo != b
    bak = p.with_name(p.name + ".bak_" + TS + "_c1_" + rot); open(bak, "xb").write(b); assert bak.read_bytes() == b
    tmp = p.with_name(p.name + ".tmp_" + TS); open(tmp, "xb").write(novo); os.replace(tmp, p); assert p.read_bytes() == novo
    print("%s: %d -> %d B; backup %s" % (p.name, len(b), len(novo), bak.name))


ENTRADA = ("**03/11, 06:2x — v406 PUBLICADA; t3 aberto.** Orquestrador `pos_treino_v406` S0–S8 ok (S5, S6c e S7 com decisão da gerência dita na `ESTADO.json`); tarefa desabilitada. "
           "G1: 37 aplicados — espelho `a381c4d1`, Central `42f3b0c9`, site v406 no ar (subidas verificadas `20261103_025919` e `20261103_055922`), Central pública 22/22 no quadro das 06:10, "
           "leitor de IA R1, conferência final 13/13, ACOM t1/t2, rota `custodia.v406`, Nós vivo, `TORRE_v406.json`, `auditar` rc 0. Parou em C19: 7 DEFASADOS fora desta custódia "
           "(fila científica: só o Codex, sem cota até 04/11 06:37; JEV v406 nasce com a release do app, C21, decisão do operador; Torre: `CLAUDE.md` de Haja_Luz e da Nativa acima do "
           "teto de 262.144 B; missão ACOM de 12/10 recusada pelo guarda). O hospedeiro não honrou `Range` na subida das 05:35 (86 arquivos íntegros revertidos, ar incoerente por horas: "
           "parede medida, não falsificação; errata ao lado em `subir_site.py`; às 05:59 voltou a 206). Quatro paradas antes (prosa do handoff, rev1 da semântica, estação do runner, camadas "
           "v395/v396 do módulo dos 16) e duas depois (Range; ordem das pernas na retomada): lições 43–50 em `work\\custodia_G1\\LICOES_v400_25out.md`; tópico [[licoes-custodia-v406-03nov]]. "
           "Memória: índice em PUBLICADA (pino 06:01), 15 depósitos promovidos (9 da custódia, 4 das patentes de 02/11, app v405, preparação v406). Decisões dele em aberto: nomes das pedras, "
           "D2, README pinado (D39), D34–D40, app, motor contínuo v407, Locaweb/Range.")


def f_top(b):
    nl = b"\r\n" if b"\r\n" in b else b"\n"
    return b.rstrip(b"\r\n") + nl + nl + ENTRADA.encode("utf-8") + nl


troca_bytes(TOP, f_top, "fechamento_03nov")
ANT = b"[v405](licoes-custodia-v405-02nov.md)"; NOV = b"[v405](licoes-custodia-v405-02nov.md) \xc2\xb7 [v406](licoes-custodia-v406-03nov.md)"


def f_mem(b):
    assert b.count(ANT) == 1 and NOV not in b, "a linha da G1 nao esta' UMA vez ou o ponteiro ja existe"
    novo = b.replace(ANT, NOV); n_lin = novo.count(b"\n") + (0 if novo.endswith(b"\n") else 1)
    assert len(novo) <= 24000 and n_lin <= 195, "o indice estouraria: %d B, %d linhas" % (len(novo), n_lin)
    return novo


troca_bytes(MEM, f_mem, "ponteiro_licoes_v406")
for args in (["pinar"], ["verificar"]):
    q = subprocess.run([PY, "-X", "utf8", str(FILA / "memoria.py"), *args], cwd=str(FILA), env=ENV, capture_output=True, timeout=300)
    print("memoria.py %s -> rc %d %s" % (args[0], q.returncode, (q.stdout or q.stderr).decode("utf-8", "replace")[:160].replace("\n", " ")))
    assert q.returncode == 0
print("OK: topico do fechamento, ponteiro no indice, pino e verificacao")
