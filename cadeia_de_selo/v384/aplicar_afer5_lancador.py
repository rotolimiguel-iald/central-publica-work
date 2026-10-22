# -*- coding: utf-8 -*-
"""5a afericao no LANCADOR (por script, count == 1, como a afericao pediu): o vigia NAO e' mais morto -- ele termina a parada em curso e sai sozinho (dorme em
passos de 1 s conferindo a bandeira), e o religar espera por ele (ate 120 s, com AVISO); a espera pelos stop_iald_llama.ps1 registra quando expira; a sonda da
tarefa DESABILITADA e' fail-closed (codigo 14); tres estados do rito para o sinal (antes, durante, depois); o mata_um so encerra a arvore DESTA rodada
(descendentes do lancador); o PID do lancador em .rito_v384.pid (abortar = kill -TERM); o cabecalho. Backup ja feito (.bak_antes_afer5)."""
import os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "rito_v384.sh")
raw = open(P, "rb").read(); s = raw.decode("utf-8")
assert open(P + ".bak_antes_afer5", "rb").read() == raw
PAIRS = [
    ('''# por shell nao interativo nem com nohup (POSIX); rodar em PRIMEIRO PLANO. (3a e 4a afericoes, 03/10/2026)''',
     '''# com & por shell nao interativo nem com nohup (POSIX); TERM sempre. ABORTAR o rito = kill -TERM $(cat <pacote>/.rito_v384.pid) -- o TaskStop da ferramenta
# da gerencia NAO para o lancador. O mata_um so encerra a arvore DESTA rodada (descendentes do lancador). (3a a 5a afericoes, 03-04/10/2026)'''),
    ('''mata_um() {
  # encerra a ARVORE do um.py desta rodada (o rito esta perdido): usado so no manejador de sinal
  u=$(powershell.exe -NoProfile -NonInteractive -Command "Get-CimInstance Win32_Process -Filter \\"Name='python.exe' OR Name='pythonw.exe' OR Name='py.exe'\\" | Where-Object { \\$_.CommandLine -ne \\$null -and \\$_.CommandLine -match '(^|[\\\\\\\\ \\"])um\\\\.py\\"?(\\\\s|\\$)' } | ForEach-Object { \\$_.ProcessId }" 2>/dev/null | tr -d '\\r')
  for p in $u; do log "encerrando a arvore do um.py (PID $p)"; taskkill //T //F //PID "$p" >> "$LOGS" 2>&1; done
}''', '''mata_um() {
  # encerra a ARVORE do um.py DESTA rodada (o rito esta perdido): so os um.py DESCENDENTES do lancador, nunca os de outra casa (5a afericao)
  RW=$(cat /proc/$$/winpid 2>/dev/null)
  case "$RW" in ''|*[!0-9]*) log "o PID nativo do lancador nao e' legivel -- NAO encerro nada as cegas (encerre o um.py desta rodada a mao)"; return 0;; esac
  u=$(powershell.exe -NoProfile -NonInteractive -Command "\\$all = Get-CimInstance Win32_Process; \\$d = @($RW); \\$i = 0; while (\\$i -lt \\$d.Count) { \\$p = \\$d[\\$i]; foreach (\\$c in \\$all) { if (\\$c.ParentProcessId -eq \\$p -and -not (\\$d -contains \\$c.ProcessId)) { \\$d += \\$c.ProcessId } }; \\$i++ }; \\$all | Where-Object { (\\$d -contains \\$_.ProcessId) -and \\$_.CommandLine -and \\$_.CommandLine -match 'um\\.py' } | ForEach-Object { \\$_.ProcessId }" 2>/dev/null | tr -d '\\r')
  for p in $u; do log "encerrando a arvore do um.py desta rodada (PID $p)"; taskkill //T //F //PID "$p" >> "$LOGS" 2>&1; done
}'''),
    ('''  [ -f "$PK/.vigia_ativo" ] && rm -f "$PK/.vigia_ativo"
  if [ -n "$VPID" ]; then kill "$VPID" 2>/dev/null; wait "$VPID" 2>/dev/null; fi   # o vigia sai ANTES do religamento (nao mata o servidor recem-religado)''',
     '''  rm -f "$PK/.rito_v384.pid"
  [ -f "$PK/.vigia_ativo" ] && rm -f "$PK/.vigia_ativo"
  if [ -n "$VPID" ]; then
    # o vigia NAO e' morto: ve a bandeira apagada, termina a parada que estiver fazendo e sai sozinho -- nenhuma parada orfa depois do religamento (5a afericao)
    w_=0; while kill -0 "$VPID" 2>/dev/null && [ $w_ -lt 120 ]; do sleep 1; w_=$((w_+1)); done
    if kill -0 "$VPID" 2>/dev/null; then log "AVISO: o vigia nao saiu em 120 s -- encerrado"; kill "$VPID" 2>/dev/null; fi
  fi'''),
    ('''    [ "$s_" = "0" ] && break
    sleep 5; j=$((j+1))
  done''', '''    [ "$s_" = "0" ] && break
    sleep 5; j=$((j+1))
  done
  [ "$s_" = "0" ] || log "AVISO: depois de 60 s ainda havia parada em curso ou a contagem nao foi legivel ('$s_') -- religo assim mesmo"'''),
    ('''RITO_INICIADO=0
sinal() {
  if [ "$RITO_INICIADO" = "1" ]; then
    log "SINAL $1 recebido durante o rito: o rito esta perdido -- encerro a arvore do um.py e restauro o servidor"
    mata_um
    echo "RITO_RC=SINAL_$1" >> rodada_v384_stdout.txt
  else
    log "SINAL $1 recebido ANTES do rito comecar: nada a encerrar; restauro o servidor"   # o stdout da tentativa anterior nao e' tocado (4a afericao)
  fi
  exit 143
}''', '''RITO_INICIADO=0
sinal() {
  # tres estados (5a afericao): 0 antes do rito, 1 durante, 2 depois (o RITO_RC ja foi gravado)
  if [ "$RITO_INICIADO" = "1" ]; then
    log "SINAL $1 recebido durante o rito: o rito esta perdido -- encerro a arvore do um.py desta rodada e restauro o servidor"
    mata_um
    echo "RITO_RC=SINAL_$1" >> rodada_v384_stdout.txt
  elif [ "$RITO_INICIADO" = "2" ]; then
    log "SINAL $1 recebido DEPOIS do rito (RITO_RC=$rc ja gravado): restauro o servidor"; exit $rc
  else
    log "SINAL $1 recebido ANTES do rito comecar: nada a encerrar; restauro o servidor"   # o stdout da tentativa anterior nao e' tocado (4a afericao)
  fi
  exit 143
}'''),
    ('''T_DESAB=$(powershell.exe -NoProfile -NonInteractive -Command "\\$t = Get-ScheduledTask -TaskName 'IALD Llama Server' -ErrorAction SilentlyContinue; if (\\$t -and \\$t.State -eq 'Disabled') { '1' } else { '0' }" 2>/dev/null | tr -d '\\r')''',
     '''T_DESAB=$(powershell.exe -NoProfile -NonInteractive -Command "\\$t = Get-ScheduledTask -TaskName 'IALD Llama Server' -ErrorAction SilentlyContinue; if (\\$t -and \\$t.State -eq 'Disabled') { '1' } else { '0' }" 2>/dev/null | tr -d '\\r')
case "$T_DESAB" in 0|1) ;; *) echo "a sonda da tarefa DESABILITADA falhou ('$T_DESAB') -- NAO RODO"; exit 14;; esac   # fail-closed, como a sonda da tarefa (5a afericao)'''),
    ('''trap 'sinal TERM' TERM; trap 'sinal HUP' HUP; trap 'sinal INT' INT''', '''trap 'sinal TERM' TERM; trap 'sinal HUP' HUP; trap 'sinal INT' INT
echo $$ > "$PK/.rito_v384.pid"   # abortar = kill -TERM $(cat .rito_v384.pid) (5a afericao)'''),
    ('''    sleep 60
  done
) &
VPID=$!''', '''    k_=0; while [ $k_ -lt 60 ] && [ -f "$PK/.vigia_ativo" ]; do sleep 1; k_=$((k_+1)); done   # dorme em passos de 1 s: sai logo depois da bandeira (5a afericao)
  done
) &
VPID=$!'''),
    ('''echo "RITO_RC=$rc" >> rodada_v384_stdout.txt
RITO_INICIADO=0''', '''echo "RITO_RC=$rc" >> rodada_v384_stdout.txt
RITO_INICIADO=2'''),
]
for old, new in PAIRS:
    c = s.count(old); assert c == 1, (c, old[:120])
    s = s.replace(old, new)
b = s.encode("utf-8"); assert b"\r" not in b
open(P + ".tmp", "wb").write(b); assert os.path.getsize(P + ".tmp") == len(b); os.replace(P + ".tmp", P)
print("ok", len(PAIRS))
