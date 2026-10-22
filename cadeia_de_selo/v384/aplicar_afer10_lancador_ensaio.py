# -*- coding: utf-8 -*-
"""10a afericao no LANCADOR e no ENSAIO A SECO (script salvo; count == 1; backups de BYTES .bak_antes_afer10 feitos e conferidos AQUI):
- 10N4 (a regressao do 9N14): o giro do registro dos sinais (com a sua recusa 17) vem ANTES do giro do log real -- toda recusa 17 dos giros acontece com o log
  real ainda no lugar, e o registro dela fica no .fase0;
- 10N5: o .fase0 de tentativas anteriores e' ACRESCENTADO ao .fase0.anterior (com um separador datado), nunca sobrescrito: nada se perde;
- 10N2/10N6: o ensaio a seco RECUSA rodar com -O/PYTHONOPTIMIZE (as guardas dele tambem sao assert)."""
import ast, os
HERE = os.path.dirname(os.path.abspath(__file__))


def bak(p):
    raw = open(p, "rb").read()
    if os.path.exists(p + ".bak_antes_afer10"):
        assert open(p + ".bak_antes_afer10", "rb").read() == raw, p
    else:
        open(p + ".bak_antes_afer10", "wb").write(raw); assert open(p + ".bak_antes_afer10", "rb").read() == raw
    return raw


P = os.path.join(HERE, "rito_v384.sh"); s = bak(P).decode("utf-8")
PAIRS = [
    (r'''# o .fase0 de uma tentativa ANTERIOR (recusada) gira antes de ser zerado -- e' o unico registro dela (9a afericao)
if [ -f "$LOGS" ]; then mv -f "$LOGS" "$LOGS.anterior" || { echo "FALHA VISIVEL: o .fase0 da tentativa anterior nao girou -- NAO RODO"; exit 17; }; fi
: > "$LOGS"''',
     r'''# o .fase0 de tentativas ANTERIORES (recusadas) e' ACRESCENTADO ao .fase0.anterior, com separador datado, antes de ser zerado -- nada se perde (9a e 10a)
if [ -f "$LOGS" ]; then { echo "== tentativa anterior (acrescentada em $(date '+%Y-%m-%d %H:%M:%S')) =="; cat "$LOGS"; } >> "$LOGS.anterior" || { echo "FALHA VISIVEL: o .fase0 da tentativa anterior nao foi guardado -- NAO RODO"; exit 17; }; fi
: > "$LOGS"'''),
    (r'''# o giro CONFERIDO (9a afericao): se falhar, FALHA VISIVEL e recusa 17 -- o trap restaura o servidor; nada de anexar ao log de outra rodada
if [ -f "$LOGF" ]; then mv -f "$LOGF" "$LOGF.anterior" || { log "FALHA VISIVEL: o log real da rodada anterior nao girou -- NAO RODO"; exit 17; }; fi
mv -f "$LOGS" "$LOGF" || { log "FALHA VISIVEL: o log da tentativa nao tomou o lugar do log real -- NAO RODO"; exit 17; }
LOGS="$LOGF"
if [ -f "$PK/rito_v384_sinal.txt" ]; then mv -f "$PK/rito_v384_sinal.txt" "$PK/rito_v384_sinal.txt.anterior" || { log "FALHA VISIVEL: o registro dos sinais nao girou -- NAO RODO"; exit 17; }; fi''',
     r'''# o giro CONFERIDO (9a afericao): se falhar, FALHA VISIVEL e recusa 17 -- o trap restaura o servidor; nada de anexar ao log de outra rodada.
# Os SINAIS giram PRIMEIRO (10a afericao): toda recusa 17 acontece com o log real ainda no lugar, e o registro dela fica no .fase0
if [ -f "$PK/rito_v384_sinal.txt" ]; then mv -f "$PK/rito_v384_sinal.txt" "$PK/rito_v384_sinal.txt.anterior" || { log "FALHA VISIVEL: o registro dos sinais nao girou -- NAO RODO"; exit 17; }; fi
if [ -f "$LOGF" ]; then mv -f "$LOGF" "$LOGF.anterior" || { log "FALHA VISIVEL: o log real da rodada anterior nao girou -- NAO RODO"; exit 17; }; fi
mv -f "$LOGS" "$LOGF" || { log "FALHA VISIVEL: o log da tentativa nao tomou o lugar do log real -- NAO RODO"; exit 17; }
LOGS="$LOGF"'''),
    (r'''# contagem ilegivel, o marcador fica). O .rito_v384.pid so sai no FIM da restauracao (a recusa 16 cobre a restauracao inteira). O .fase0 de uma tentativa
# anterior vai para .fase0.anterior; se esse giro, ou o do log real, falhar: FALHA VISIVEL e RECUSA (codigo 17).
# (3a a 9a afericoes, 03-04/10/2026)''',
     r'''# contagem ilegivel, o marcador fica). O .rito_v384.pid sai em qualquer saida antecipada e, armada a restauracao, so no FIM dela (a recusa 16 cobre a
# restauracao inteira). O .fase0 de tentativas anteriores e' ACRESCENTADO ao .fase0.anterior; os sinais giram antes do log real; se um desses giros falhar:
# FALHA VISIVEL e RECUSA (codigo 17). As recusas 6 a 9 e 16 (antes da fase 0) so vao a saida do lancador.
# (3a a 10a afericoes, 03-04/10/2026)'''),
]
for old, new in PAIRS:
    c = s.count(old); assert c == 1, (c, old[:150])
    s = s.replace(old, new)
b = s.encode("utf-8"); assert b"\r" not in b
open(P + ".tmp", "wb").write(b); assert os.path.getsize(P + ".tmp") == len(b); os.replace(P + ".tmp", P); assert open(P, "rb").read() == b
print("ok lancador", len(PAIRS))
E = os.path.join(HERE, "ensaio_a_seco_v384.py"); e = bak(E).decode("utf-8")
old = "import copy, hashlib, io, json, os, re, shutil, subprocess, sys, time, ast, builtins, textwrap\n"
assert e.count(old) == 1 and "sys.flags.optimize" not in e
e = e.replace(old, old + 'if sys.flags.optimize:   # as guardas sao assert: com -O elas sumiriam sem aviso (10a afericao)\n    raise SystemExit("RECUSO: rodar sem -O / PYTHONOPTIMIZE (as guardas sao assert)")\n')
ast.parse(e)
eb = e.encode("utf-8"); open(E + ".tmp", "wb").write(eb); assert os.path.getsize(E + ".tmp") == len(eb); os.replace(E + ".tmp", E); assert open(E, "rb").read() == eb
print("ok ensaio")
