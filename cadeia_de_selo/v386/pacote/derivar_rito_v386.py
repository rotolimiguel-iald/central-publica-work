# -*- coding: utf-8 -*-
"""derivar_rito_v386.py -- deriva rito_v386.sh de rito_v385.sh POR SCRIPT (so troca de nomes + a guarda do marcador da rodada anterior + o cabecalho), para
que o diff contra o lancador da v385 (herdado inteiro, com as dez afericoes) seja legivel e conferivel. Grava rito_v386.sh (tempario -> tamanho -> substituir)
e DIFF_rito_v385_v386.txt. uso: python derivar_rito_v386.py"""
import difflib, os, re, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
V6 = os.path.dirname(HERE); SP = os.path.dirname(V6)
src = open(os.path.join(SP, "v385", "rito_v385.sh"), "r", encoding="utf-8", newline="").read()
assert "\r" not in src
t = src
# 1. o cabecalho (as 6 primeiras linhas de comentario descrevem a rodada): reescrito para a v386; o resto do cabecalho (as afericoes) fica
head_old = t.split("\n")[1:6]
assert head_old[0].startswith("# O RITO v385") and head_old[4].startswith("# Pre-condicao: instalar_v385.py"), head_old
head_new = ["# O RITO v386 (ato da gerencia; decisoes do operador de 05/10/2026 lidas por hash -- o Verbo tipado («Verbo=seleção da ação»; o Nome e' o posto), o ramo B",
            "# reaberto por pre-registro (V1 por hash; nada aberto), a errata ao lado de R6, e «o resto vc consegue responder tudo agroa»; o PILAR QUANTICO NAO roda de",
            "# novo: e' reaproveitado da v385 pela chave do cache (_QP_REUSE_V386 no um.py; TGL_RITE_CHECKPOINT segue DESLIGADO); molde: rito_v385.sh, herdado",
            "# inteiro, com as afericoes dele, trocados so os nomes, o pacote e a guarda do marcador): echo 1 | python um.py no Nos, stdout canonico em",
            "# rodada_v386_stdout.txt, trailer RITO_RC=<rc>, horarios no pacote. RODADA COMPLETA: TGL_RITE_CHECKPOINT desligado (os ritos cosmologicos rodam todos)."]
# 2. a troca global de nomes v385 -> v386 (log, pid, sinal, stdout, horarios, ESPERADOS, instalar, grep do cmdline, marcador) -- ANTES do cabecalho novo,
#    que cita a v385 de proposito («reaproveitado da v385»; «molde: rito_v385.sh»)
t = t.replace("v385", "v386")
lines = t.split("\n")
lines[1:6] = head_new
t = "\n".join(lines)
# 3. o pacote da v386 e' .../scratchpad/v386/pacote (nao a raiz v386)
t = t.replace('PK="/c/Users/rotol/AppData/Local/Temp/claude/c--IALD-Central-de-Patentes/6da8f00d-d44f-4888-a88d-fc9f73eead3d/scratchpad/v386"',
              'PK="/c/Users/rotol/AppData/Local/Temp/claude/c--IALD-Central-de-Patentes/6da8f00d-d44f-4888-a88d-fc9f73eead3d/scratchpad/v386/pacote"')
t = t.replace("scratchpad/v386/ESPERADOS_v386.json", "scratchpad/v386/pacote/ESPERADOS_v386.json")
# 4. a guarda do marcador da rodada ANTERIOR: a v385 (o pacote dela e' a raiz scratchpad/v385), nao mais a v384
t = t.replace("# a guarda do marcador da rodada ANTERIOR (v386): se a v384 deixou o servidor parado", "# a guarda do marcador da rodada ANTERIOR (v386): se a v385 deixou o servidor parado")
t = t.replace('PK384="/c/Users/rotol/AppData/Local/Temp/claude/c--IALD-Central-de-Patentes/6da8f00d-d44f-4888-a88d-fc9f73eead3d/scratchpad/v384"',
              'PK385="/c/Users/rotol/AppData/Local/Temp/claude/c--IALD-Central-de-Patentes/6da8f00d-d44f-4888-a88d-fc9f73eead3d/scratchpad/v385"')
t = t.replace('[ -f "$PK384/.servidor_parado_pelo_rito" ] && { echo "ha marcador de servidor parado pela rodada v384 ($(cat "$PK384/.servidor_parado_pelo_rito")) -- resolva-o antes -- NAO RODO"; exit 18; }',
              '[ -f "$PK385/.servidor_parado_pelo_rito" ] && { echo "ha marcador de servidor parado pela rodada v385 ($(cat "$PK385/.servidor_parado_pelo_rito")) -- resolva-o antes -- NAO RODO"; exit 18; }')
assert "PK384" not in t and "v384" not in t, [l for l in t.split("\n") if "v384" in l]
_sobras = [l for l in t.split("\n") if "v385" in l.replace("scratchpad/v385", "").replace("rodada v385", "").replace("se a v385", "").replace("PK385", "").replace("da v385", "").replace("rito_v385.sh", "")]
assert not _sobras, _sobras
assert t.count('/scratchpad/v386/pacote"') == 1 and "ESPERADOS_v386.json" in t and "rodada_v386_stdout.txt" in t and ".rito_v386.pid" in t and "rito_servidor_v386.log" in t and "rito_v386_sinal.txt" in t and "rito_horarios_v386.txt" in t
assert "unset TGL_RITE_CHECKPOINT TGL_CACHE_DIR" in t and 'echo 1 | python um.py > rodada_v386_stdout.txt' in t
out = os.path.join(HERE, "rito_v386.sh")
open(out + ".tmp", "w", encoding="utf-8", newline="\n").write(t)
assert os.path.getsize(out + ".tmp") > 20000
os.replace(out + ".tmp", out)
os.chmod(out, 0o755)
diff = list(difflib.unified_diff(src.split("\n"), t.split("\n"), "rito_v385.sh", "rito_v386.sh", lineterm="", n=0))
open(os.path.join(HERE, "DIFF_rito_v385_v386.txt"), "w", encoding="utf-8", newline="\n").write("\n".join(diff) + "\n")
print("rito_v386.sh gravado; linhas no diff:", len([l for l in diff if l.startswith(("+", "-")) and not l.startswith(("+++", "---"))]))
