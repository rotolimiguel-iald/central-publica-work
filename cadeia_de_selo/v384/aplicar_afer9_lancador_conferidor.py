# -*- coding: utf-8 -*-
"""9a afericao no LANCADOR e no CONFERIDOR (script salvo; count == 1; backup de BYTES .bak_antes_afer9 feito e conferido AQUI):
- 9N4/9N8: o .rito_v384.pid sai no FIM da restauracao (o trap do EXIT passa a ser «religar; rm -f pid»), nao no comeco do religar: a recusa 16 cobre a
  restauracao inteira;
- 9N5/9N9: o .fase0 de uma tentativa anterior GIRA para .fase0.anterior antes de ser zerado (se nao girar, recusa 17); as recusas 14 vao pelo log();
- 9N14: o giro do log real e do registro dos sinais e' CONFERIDO: falhou -> FALHA VISIVEL e recusa 17 (o trap restaura);
- 9N15: a espera de 60 s antes de religar usa a MESMA consulta da reconferencia (Stop-ScheduledTask da tarefa ou stop_iald_llama.ps1);
- 9N6/9N10: a linha do log diz «parada (Stop-ScheduledTask ou stop_iald_llama.ps1)» e separa a contagem ILEGIVEL; o conferidor casa as formas novas (e a antiga);
- o cabecalho diz o codigo 17, o .fase0.anterior e o PID ate o fim da restauracao."""
import ast, os
HERE = os.path.dirname(os.path.abspath(__file__))


def bak(p):
    raw = open(p, "rb").read()
    if os.path.exists(p + ".bak_antes_afer9"):
        assert open(p + ".bak_antes_afer9", "rb").read() == raw, "o .bak_antes_afer9 existe e nao e' o estado corrente: " + p
    else:
        open(p + ".bak_antes_afer9", "wb").write(raw); assert open(p + ".bak_antes_afer9", "rb").read() == raw
    return raw


P = os.path.join(HERE, "rito_v384.sh"); s = bak(P).decode("utf-8")
Q = r"""@(Get-CimInstance Win32_Process -Filter \"Name='powershell.exe' OR Name='pwsh.exe'\" | Where-Object { \$_.CommandLine -and ((\$_.CommandLine -match 'Stop-Scheduled[T]ask' -and \$_.CommandLine -match 'IALD Llama') -or \$_.CommandLine -match 'stop_iald_llam[a]\.ps1') }).Count"""
PAIRS = [
    (r'''# religamento, o marcador so sai se a porta ainda escutar 30 s depois E nenhuma parada (Stop-ScheduledTask ou stop_iald_llama.ps1) estiver em curso.
# (3a a 8a afericoes, 03-04/10/2026)''',
     r'''# religamento, o marcador so sai se a porta ainda escutar 30 s depois E nenhuma parada (Stop-ScheduledTask ou stop_iald_llama.ps1) estiver em curso (com a
# contagem ilegivel, o marcador fica). O .rito_v384.pid so sai no FIM da restauracao (a recusa 16 cobre a restauracao inteira). O .fase0 de uma tentativa
# anterior vai para .fase0.anterior; se esse giro, ou o do log real, falhar: FALHA VISIVEL e RECUSA (codigo 17).
# (3a a 9a afericoes, 03-04/10/2026)'''),
    (r'''# a VEZ: o PID deste lancador gravado JA (antes da fase 0) e removido em qualquer saida antecipada; o religar o remove no fim (8a afericao)''',
     r'''# a VEZ: o PID deste lancador gravado JA (antes da fase 0) e removido em qualquer saida antecipada; armada a restauracao, so sai no FIM dela (8a e 9a)'''),
    (r'''LOGF="$LOGS"; LOGS="$PK/rito_servidor_v384.log.fase0"; : > "$LOGS"''',
     r'''LOGF="$LOGS"; LOGS="$PK/rito_servidor_v384.log.fase0"
# o .fase0 de uma tentativa ANTERIOR (recusada) gira antes de ser zerado -- e' o unico registro dela (9a afericao)
if [ -f "$LOGS" ]; then mv -f "$LOGS" "$LOGS.anterior" || { echo "FALHA VISIVEL: o .fase0 da tentativa anterior nao girou -- NAO RODO"; exit 17; }; fi
: > "$LOGS"'''),
    ('''  RELIGADO=1
  rm -f "$PK/.rito_v384.pid"
''', '''  RELIGADO=1
  # (o .rito_v384.pid NAO sai aqui: so no FIM da restauracao, pelo trap do EXIT -- 9a afericao)
'''),
    ('''    s_=$(powershell.exe -NoProfile -NonInteractive -Command "@(Get-CimInstance Win32_Process -Filter \\"Name='powershell.exe' OR Name='pwsh.exe'\\" | Where-Object { \\$_.CommandLine -and \\$_.CommandLine -match 'stop_iald_llama\\.ps1' }).Count" 2>/dev/null | tr -d '\\r')''',
     '''    s_=$(powershell.exe -NoProfile -NonInteractive -Command "''' + Q + '''" 2>/dev/null | tr -d '\\r')   # a MESMA consulta da reconferencia (9a)'''),
    ('''          # nenhuma parada da tarefa ainda em curso (a classe [T] impede a consulta de casar consigo mesma) -- senao o marcador fica (7a afericao)''',
     '''          # nenhuma parada ainda em curso (as classes [T] e [a] impedem a consulta de casar consigo mesma) -- senao, ou com a contagem ilegivel, o marcador fica (7a-9a)'''),
    ('''          if [ "$sp_" = "0" ]; then log "servidor de volta: a porta 8081 escuta (reconferida 30 s depois, por causa do AVISO acima)"; rm -f "$MARCA"; return 0; fi
          log "AVISO: a porta 8081 escuta, mas ha parada da tarefa ainda em curso ('$sp_') -- o marcador fica: $MARCA"; return 0''',
     '''          case "$sp_" in
            0) log "servidor de volta: a porta 8081 escuta (reconferida 30 s depois, por causa do AVISO acima)"; rm -f "$MARCA"; return 0;;
            ''|*[!0-9]*) log "AVISO: a porta 8081 escuta, mas a contagem das paradas em curso nao foi legivel ('$sp_') -- o marcador fica: $MARCA"; return 0;;
            *) log "AVISO: a porta 8081 escuta, mas ha parada (Stop-ScheduledTask ou stop_iald_llama.ps1) ainda em curso ($sp_) -- o marcador fica: $MARCA"; return 0;;
          esac'''),
    ('''case "$TAREFA_EXISTE" in 0|1) ;; *) echo "a sonda da tarefa falhou ('$TAREFA_EXISTE') -- NAO RODO"; exit 14;; esac''',
     '''case "$TAREFA_EXISTE" in 0|1) ;; *) log "a sonda da tarefa falhou ('$TAREFA_EXISTE') -- NAO RODO"; exit 14;; esac'''),
    ('''case "$T_DESAB" in 0|1) ;; *) echo "a sonda da tarefa DESABILITADA falhou ('$T_DESAB') -- NAO RODO"; exit 14;; esac''',
     '''case "$T_DESAB" in 0|1) ;; *) log "a sonda da tarefa DESABILITADA falhou ('$T_DESAB') -- NAO RODO"; exit 14;; esac'''),
    ('''trap religar EXIT
''', '''trap 'religar; rm -f "$PK/.rito_v384.pid"' EXIT   # o PID so sai DEPOIS da restauracao inteira (9a afericao)
'''),
    ('''[ -f "$LOGF" ] && mv -f "$LOGF" "$LOGF.anterior"
mv -f "$LOGS" "$LOGF"; LOGS="$LOGF"
[ -f "$PK/rito_v384_sinal.txt" ] && mv -f "$PK/rito_v384_sinal.txt" "$PK/rito_v384_sinal.txt.anterior"''',
     '''# o giro CONFERIDO (9a afericao): se falhar, FALHA VISIVEL e recusa 17 -- o trap restaura o servidor; nada de anexar ao log de outra rodada
if [ -f "$LOGF" ]; then mv -f "$LOGF" "$LOGF.anterior" || { log "FALHA VISIVEL: o log real da rodada anterior nao girou -- NAO RODO"; exit 17; }; fi
mv -f "$LOGS" "$LOGF" || { log "FALHA VISIVEL: o log da tentativa nao tomou o lugar do log real -- NAO RODO"; exit 17; }
LOGS="$LOGF"
if [ -f "$PK/rito_v384_sinal.txt" ]; then mv -f "$PK/rito_v384_sinal.txt" "$PK/rito_v384_sinal.txt.anterior" || { log "FALHA VISIVEL: o registro dos sinais nao girou -- NAO RODO"; exit 17; }; fi'''),
]
for old, new in PAIRS:
    c = s.count(old); assert c == 1, (c, old[:150])
    s = s.replace(old, new)
assert 'rm -f "$PK/.rito_v384.pid"\n' not in s.split("religar() {", 1)[1].split("\n}\n", 1)[0], "o religar ainda remove o PID"
b = s.encode("utf-8"); assert b"\r" not in b
open(P + ".tmp", "wb").write(b); assert os.path.getsize(P + ".tmp") == len(b); os.replace(P + ".tmp", P); assert open(P, "rb").read() == b
print("ok lancador", len(PAIRS))
C = os.path.join(HERE, "conferir_rito_v384.py"); c = bak(C).decode("utf-8")
CP = [
    ('''                                  "ESCUTA, MAS HAVIA PARADA DA TAREFA EM CURSO (o marcador ficou) -- conferir a tarefa" if "ha parada da tarefa ainda em curso" in _lt else''',
     '''                                  "ESCUTA, MAS A CONTAGEM DAS PARADAS NAO FOI LEGIVEL (o marcador ficou) -- conferir a tarefa" if "a contagem das paradas em curso nao foi legivel" in _lt else
                                  "ESCUTA, MAS HAVIA PARADA EM CURSO (o marcador ficou) -- conferir a tarefa" if ("ainda em curso" in _lt and ("ha parada (Stop-ScheduledTask" in _lt or "ha parada da tarefa" in _lt)) else'''),
]
for old, new in CP:
    k = c.count(old); assert k == 1, (k, old[:100])
    c = c.replace(old, new)
ast.parse(c)
cb = c.encode("utf-8"); open(C + ".tmp", "wb").write(cb); assert os.path.getsize(C + ".tmp") == len(cb); os.replace(C + ".tmp", C); assert open(C, "rb").read() == cb
print("ok conferidor", len(CP))
