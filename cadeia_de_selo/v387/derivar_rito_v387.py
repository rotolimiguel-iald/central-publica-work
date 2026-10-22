# -*- coding: utf-8 -*-
"""derivar_rito_v387.py -- deriva rito_v387.sh de rito_v386.sh POR SCRIPT (troca de nomes + o pacote duravel em work\\v387_pacote + a guarda do marcador da
rodada anterior (o pacote da v386) + o cabecalho), para que o diff contra o lancador da v386 (herdado inteiro, com as dez afericoes) seja legivel.
Grava rito_v387.sh (tempario -> tamanho -> substituir) e DIFF_rito_v386_v387.txt. uso: python derivar_rito_v387.py"""
import difflib, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), "scratch_6da8f00d", "v386_pacote", "rito_v386.sh")
src = open(SRC, "r", encoding="utf-8", newline="").read()
assert "\r" not in src
OLDSP = "/c/Users/rotol/AppData/Local/Temp/claude/c--IALD-Central-de-Patentes/6da8f00d-d44f-4888-a88d-fc9f73eead3d/scratchpad"
t = src
head_old = t.split("\n")[1:6]
assert head_old[0].startswith("# O RITO v386") and head_old[4].startswith("# inteiro, com as afericoes dele") is False and "rodada_v386_stdout.txt" in "\n".join(head_old), head_old
head_new = ["# O RITO v387 (ato da gerencia, 06/10/2026; handoff-sessao-nova-06out, passo C): os tres testes de estresse conjuntos (ordem do operador de 05/10 23:00:29",
            "# UTC, por sha256), a razao de Hubble (Fase 9) e a era da radiacao (Fase 8) pre-registradas por hash (nada aberto), retrodicao sem ajuste (a lei de 05/10);",
            "# o PILAR QUANTICO NAO roda de novo: reaproveitado da v385 pela chave do cache (_QP_REUSE_V386 segue no um.py; TGL_RITE_CHECKPOINT DESLIGADO); molde:",
            "# rito_v386.sh, herdado inteiro, com as afericoes dele, trocados so os nomes, o pacote (work\\v387_pacote, duravel) e a guarda do marcador: echo 1 | python",
            "# um.py no Nos, stdout canonico em rodada_v387_stdout.txt, trailer RITO_RC=<rc>, horarios no pacote. RODADA COMPLETA (os ritos cosmologicos rodam todos)."]
# 1. o pacote e os esperados (o pacote da v386 vivia no scratchpad efemero; o da v387 vive em work, duravel)
t = t.replace('PK="%s/v386/pacote"' % OLDSP, 'PK="/c/IALD/Central de Patentes/work/v387_pacote"')
t = t.replace("C:/Users/rotol/AppData/Local/Temp/claude/c--IALD-Central-de-Patentes/6da8f00d-d44f-4888-a88d-fc9f73eead3d/scratchpad/v386/pacote/ESPERADOS_v386.json",
              "C:/IALD/Central de Patentes/work/v387_pacote/ESPERADOS_v387.json")
# 2. a guarda do marcador da rodada ANTERIOR: a v386 (o pacote dela: scratchpad/v386/pacote) -- trocada ANTES da troca global
t = t.replace("# a guarda do marcador da rodada ANTERIOR (v386): se a v385 deixou o servidor parado", "# a guarda do marcador da rodada ANTERIOR (v387): se a v386 deixou o servidor parado")
t = t.replace('PK385="%s/v385"' % OLDSP, 'PK386="%s/v386/pacote"' % OLDSP + chr(10) + '[ -d "$PK386" ] || { echo "a pasta do pacote v386 ($PK386) sumiu: a guarda do marcador nao pode ser lida -- NAO RODO"; exit 18; }   # afericao A7')
t = t.replace('[ -f "$PK385/.servidor_parado_pelo_rito" ] && { echo "ha marcador de servidor parado pela rodada v385 ($(cat "$PK385/.servidor_parado_pelo_rito")) -- resolva-o antes -- NAO RODO"; exit 18; }',
              '[ -f "$PK386/.servidor_parado_pelo_rito" ] && { echo "ha marcador de servidor parado pela rodada v386 ($(cat "$PK386/.servidor_parado_pelo_rito")) -- resolva-o antes -- NAO RODO"; exit 18; }')
# 3. a troca global de nomes v386 -> v387 (log, pid, sinal, stdout, horarios, instalar, grep do cmdline, marcador), protegendo o pacote da v386 e o _QP_REUSE_V386
t = t.replace("%s/v386/pacote" % OLDSP, "@@OLDPAC@@").replace("_QP_REUSE_V386", "@@QPR@@").replace("PK386", "@@PKV@@").replace("rodada v386", "@@RODV@@").replace("se a v386", "@@SEV@@")
t = t.replace("v386", "v387")
t = t.replace("@@OLDPAC@@", "%s/v386/pacote" % OLDSP).replace("@@QPR@@", "_QP_REUSE_V386").replace("@@PKV@@", "PK386").replace("@@RODV@@", "rodada v386").replace("@@SEV@@", "se a v386")
t = t.replace("a pasta do pacote v387 ($PK386)", "a pasta do pacote v386 ($PK386)")
lines = t.split("\n")
lines[1:6] = head_new
t = "\n".join(lines)
assert "PK385" not in t and "v385/" not in t, [l for l in t.split("\n") if "v385" in l and "reaproveitado da v385" not in l]
assert t.count('PK="/c/IALD/Central de Patentes/work/v387_pacote"') == 1 and "ESPERADOS_v387.json" in t and "rodada_v387_stdout.txt" in t and ".rito_v387.pid" in t
assert "rito_servidor_v387.log" in t and "rito_v387_sinal.txt" in t and "rito_horarios_v387.txt" in t and t.count("PK386") == 5
assert "unset TGL_RITE_CHECKPOINT TGL_CACHE_DIR" in t and "echo 1 | python um.py > rodada_v387_stdout.txt" in t
_sobras = [l for l in t.split("\n") if "v386" in l and "PK386" not in l and "_QP_REUSE_V386" not in l and "rito_v386.sh" not in l and "/v386/pacote" not in l and "se a v386" not in l]
assert not _sobras, _sobras
out = os.path.join(HERE, "rito_v387.sh")
open(out + ".tmp", "w", encoding="utf-8", newline="\n").write(t)
assert os.path.getsize(out + ".tmp") > 20000
os.replace(out + ".tmp", out)
os.chmod(out, 0o755)
diff = list(difflib.unified_diff(src.split("\n"), t.split("\n"), "rito_v386.sh", "rito_v387.sh", lineterm="", n=0))
open(os.path.join(HERE, "DIFF_rito_v386_v387.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(diff) + "\n")
print("rito_v387.sh gravado; linhas no diff:", len([l for l in diff if l.startswith(("+", "-")) and not l.startswith(("+++", "---"))]))
