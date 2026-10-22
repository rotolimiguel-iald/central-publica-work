#!/bin/sh
# O RITO v387 (ato da gerencia, 06/10/2026; handoff-sessao-nova-06out, passo C): os tres testes de estresse conjuntos (ordem do operador de 05/10 23:00:29
# UTC, por sha256), a razao de Hubble (Fase 9) e a era da radiacao (Fase 8) pre-registradas por hash (nada aberto), retrodicao sem ajuste (a lei de 05/10);
# o PILAR QUANTICO NAO roda de novo: reaproveitado da v385 pela chave do cache (_QP_REUSE_V386 segue no um.py; TGL_RITE_CHECKPOINT DESLIGADO); molde:
# rito_v386.sh, herdado inteiro, com as afericoes dele, trocados so os nomes, o pacote (work\v387_pacote, duravel) e a guarda do marcador: echo 1 | python
# um.py no Nos, stdout canonico em rodada_v387_stdout.txt, trailer RITO_RC=<rc>, horarios no pacote. RODADA COMPLETA (os ritos cosmologicos rodam todos).
# O SERVIDOR DO MODELO NATIVO: a tarefa agendada «IALD Llama Server» e o supervisor start_iald_llama.ps1 (que religa em 5 s) sao PARADOS antes, conferidos
# (nenhum llama-server vivo; VRAM usada <= 6000 MiB e LEGIVEL), VIGIADOS durante (se reaparecer, e' encerrado e o fato registrado) e, no fim -- mesmo se o
# rito falhar ou o lancador receber TERM/HUP/INT --, a tarefa e' RELIGADA SE o servidor estava ligado antes (o estado anterior e' lido pela TAREFA e pelo
# processo; sonda vazia conta como «ligado»). Servidor ligado SEM a tarefa, ou com a tarefa DESABILITADA: o lancador RECUSA (nao saberia religar). Enquanto
# o servidor estiver parado pelo rito, o marcador .servidor_parado_pelo_rito (com restaurar=0|1) fica no pacote: se o lancador morrer a forca (o trap nao
# roda), a proxima rodada o le e restaura o que ele gravou -- e a memoria da v387 manda a gerencia conferi-lo se nao houver proxima rodada. Um sinal antes do
# rito so restaura; durante, encerra a arvore do um.py e grava RITO_RC=SINAL_<x>. INT/HUP so sao capturados se o lancador NAO for iniciado em segundo plano
# com & por shell nao interativo nem com nohup (POSIX); TERM sempre. ABORTAR o rito = kill -TERM $(cat <pacote>/.rito_v387.pid) NO GIT BASH (sh), nao no
# PowerShell: o numero e' o PID do MSYS, nao o do Windows -- o TaskStop da ferramenta da gerencia NAO para o lancador; ANTES de abortar, conferir que
# /proc/$(cat .rito_v387.pid)/cmdline contem rito_v387. O mata_um so encerra a arvore DESTA rodada (descendentes do lancador), fail-closed. Com outro lancador
# vivo, RECUSA (codigo 16). O log da tentativa vai para .fase0 e so gira para o lugar do log real (.anterior) depois da ULTIMA recusa. Depois de um AVISO no
# religamento, o marcador so sai se a porta ainda escutar 30 s depois E nenhuma parada (Stop-ScheduledTask ou stop_iald_llama.ps1) estiver em curso (com a
# contagem ilegivel, o marcador fica). O .rito_v387.pid sai em qualquer saida antecipada e, armada a restauracao, so no FIM dela (a recusa 16 cobre a
# restauracao inteira). O .fase0 de tentativas anteriores e' ACRESCENTADO ao .fase0.anterior; os sinais giram antes do log real; se um desses giros falhar:
# FALHA VISIVEL e RECUSA (codigo 17). As recusas 6 a 9 e 16 (antes da fase 0) so vao a saida do lancador.
# (3a a 10a afericoes, 03-04/10/2026)
PK="/c/IALD/Central de Patentes/work/v387_pacote"
NOS="/c/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós"
STOPPS="C:\\IALD\\projetos_pyhton\\IALD\\stop_iald_llama.ps1"
MARCA="$PK/.servidor_parado_pelo_rito"
export PYTHONIOENCODING=utf-8
unset TGL_RITE_CHECKPOINT TGL_CACHE_DIR
cd "$NOS" || exit 9
# a guarda do marcador da rodada ANTERIOR (v387): se a v386 deixou o servidor parado (marcador no pacote dela), a gerencia o resolve antes -- NAO RODO
PK386="/c/Users/rotol/AppData/Local/Temp/claude/c--IALD-Central-de-Patentes/6da8f00d-d44f-4888-a88d-fc9f73eead3d/scratchpad/v386/pacote"
[ -d "$PK386" ] || { echo "a pasta do pacote v386 ($PK386) sumiu: a guarda do marcador nao pode ser lida -- NAO RODO"; exit 18; }   # afericao A7
[ -f "$PK386/.servidor_parado_pelo_rito" ] && { echo "ha marcador de servidor parado pela rodada v386 ($(cat "$PK386/.servidor_parado_pelo_rito")) -- resolva-o antes -- NAO RODO"; exit 18; }
LOGS="$PK/rito_servidor_v387.log"
log() { echo "$(date +%H:%M:%S) $*" | tee -a "$LOGS"; }
h=$(python -c "import hashlib;print(hashlib.sha256(open('um.py','rb').read()).hexdigest()[:16])")
e=$(python -c "import json;print(json.load(open('C:/IALD/Central de Patentes/work/v387_pacote/ESPERADOS_v387.json',encoding='utf-8'))['candidato_sha16'])")
[ "$h" = "$e" ] || { echo "um.py do disco ($h) != candidato esperado ($e) -- NAO RODO"; exit 8; }
v=$(powershell.exe -NoProfile -NonInteractive -Command "\$ErrorActionPreference='Stop'; Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='pythonw.exe' OR Name='py.exe'\" | Where-Object { \$_.CommandLine -ne \$null -and \$_.CommandLine -match '(^|[\\\\ \"])um\\.py\"?(\\s|\$)' } | ForEach-Object { \$_.ProcessId }; Write-Output 'VIGIA_OK'" 2>&1) || { echo "vigia de processos FALHOU: $v -- NAO RODO"; exit 7; }
echo "$v" | grep -q "VIGIA_OK" || { echo "vigia sem VIGIA_OK: $v -- NAO RODO"; exit 7; }
n=$(echo "$v" | grep -c -E '^[0-9]+\s*$'); [ "$n" = "0" ] || { echo "ha processo um.py vivo ($v) -- NAO RODO"; exit 6; }
# outro LANCADOR vivo (ainda sem um.py, por exemplo na parada do servidor): recusar ANTES de qualquer parada ou dos orfaos (7a afericao)
PID_VELHO=""
if [ -f "$PK/.rito_v387.pid" ]; then
  op_=$(cat "$PK/.rito_v387.pid" 2>/dev/null)
  if [ -n "$op_" ] && kill -0 "$op_" 2>/dev/null && grep -q "rito_v387" "/proc/$op_/cmdline" 2>/dev/null; then echo "OUTRO lancador do rito v387 esta VIVO (PID $op_) -- NAO RODO"; exit 16; fi
  PID_VELHO="$op_"
fi
# a VEZ: o PID deste lancador gravado JA (antes da fase 0) e removido em qualquer saida antecipada; armada a restauracao, so sai no FIM dela (8a e 9a)
echo $$ > "$PK/.rito_v387.pid"
trap 'rm -f "$PK/.rito_v387.pid"' EXIT
# a fase 0 escreve num log PROPRIO; o log real (e o registro dos sinais) so gira depois da ULTIMA recusa (8a afericao)
LOGF="$LOGS"; LOGS="$PK/rito_servidor_v387.log.fase0"
# o .fase0 de tentativas ANTERIORES (recusadas) e' ACRESCENTADO ao .fase0.anterior, com separador datado, antes de ser zerado -- nada se perde (9a e 10a)
if [ -f "$LOGS" ]; then { echo "== tentativa anterior (acrescentada em $(date '+%Y-%m-%d %H:%M:%S')) =="; cat "$LOGS"; } >> "$LOGS.anterior" || { echo "FALHA VISIVEL: o .fase0 da tentativa anterior nao foi guardado -- NAO RODO"; exit 17; }; fi
: > "$LOGS"
[ -n "$PID_VELHO" ] && log "AVISO_PID_VELHO: .rito_v387.pid velho ($PID_VELHO): de um lancador que nao vive mais -- sobrescrito"

orfaos() {
  # encerra qualquer trabalhador do pilar quantico vivo (de uma rodada morta, ou desta quando o rito ja acabou/morreu) -- a GPU nao pode ter dois
  o=$(powershell.exe -NoProfile -NonInteractive -Command "Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='pythonw.exe'\" | Where-Object { \$_.CommandLine -and \$_.CommandLine -match 'pilar_quantico_worker\.py' } | ForEach-Object { \$_.ProcessId }" 2>/dev/null | tr -d '\r')
  for p in $o; do log "trabalhador do pilar quantico vivo sem rito (PID $p) -- encerrando a arvore"; taskkill //T //F //PID "$p" >> "$LOGS" 2>&1; done
}

mata_um() {
  # encerra a ARVORE do rito DESTA rodada (o rito esta perdido) -- nunca a de outra casa (5a afericao) -- e e' FAIL-CLOSED (6a afericao):
  # (1) pelo PID nativo do subshell do rito, o pai Windows da cadeia (python um.py -> trabalhador -> referencia na CPU);
  # (2) so se ele for ilegivel, pelos python um.py DESCENDENTES do lancador (data de criacao do filho >= a do pai: PID reaproveitado nao entra), com a
  #     sentinela MATA_OK; (3) se nada der, ou se o subshell seguir vivo, FALHA VISIVEL no log e em rito_v387_sinal.txt.
  MATOU=0
  W=$(cat /proc/$UMPID/winpid 2>/dev/null)
  case "$W" in ''|*[!0-9]*) W="";; esac
  if [ -n "$W" ]; then
    log "encerrando a arvore do rito pelo PID nativo do subshell ($W)"
    taskkill //T //F //PID "$W" >> "$LOGS" 2>&1 && MATOU=1
  fi
  if [ "$MATOU" != "1" ]; then
    RW=$(cat /proc/$$/winpid 2>/dev/null)
    case "$RW" in ''|*[!0-9]*) log "FALHA VISIVEL: nem o PID do subshell nem o do lancador sao legiveis -- o um.py desta rodada pode seguir vivo (encerre-o a mao)"; echo "UM_PY_TALVEZ_VIVO $(date '+%Y-%m-%d %H:%M:%S')" >> "$PK/rito_v387_sinal.txt"; return 1;; esac
    u=$(powershell.exe -NoProfile -NonInteractive -Command "\$ErrorActionPreference='Stop'; \$all = Get-CimInstance Win32_Process; \$byid = @{}; foreach (\$x in \$all) { \$byid[[int]\$x.ProcessId] = \$x }; \$d = @($RW); \$i = 0; while (\$i -lt \$d.Count) { \$p = \$d[\$i]; \$pp = \$byid[[int]\$p]; foreach (\$c in \$all) { if (\$c.ParentProcessId -eq \$p -and -not (\$d -contains \$c.ProcessId) -and (\$pp -eq \$null -or \$c.CreationDate -ge \$pp.CreationDate)) { \$d += \$c.ProcessId } }; \$i++ }; \$all | Where-Object { (\$d -contains \$_.ProcessId) -and \$_.ProcessId -ne $RW -and \$_.Name -match '^(python|pythonw|py)\.exe\$' -and \$_.CommandLine -match '(^|[\\\\ \"])um\\.py\"?(\\s|\$)' } | ForEach-Object { \$_.ProcessId }; Write-Output 'MATA_OK'" 2>&1 | tr -d '\r')
    echo "$u" | grep -q "MATA_OK" || { log "FALHA VISIVEL: a consulta dos descendentes falhou ($u) -- o um.py desta rodada pode seguir vivo"; echo "UM_PY_TALVEZ_VIVO $(date '+%Y-%m-%d %H:%M:%S')" >> "$PK/rito_v387_sinal.txt"; return 1; }
    for p in $(echo "$u" | grep -E '^[0-9]+$'); do log "encerrando a arvore do um.py desta rodada (PID $p)"; taskkill //T //F //PID "$p" >> "$LOGS" 2>&1 && MATOU=1; done
  fi
  sleep 2
  if kill -0 "$UMPID" 2>/dev/null || [ "$MATOU" != "1" ]; then
    log "FALHA VISIVEL: o encerramento nao se confirmou (subshell vivo ou nada encerrado) -- o um.py desta rodada pode seguir vivo"
    echo "UM_PY_TALVEZ_VIVO $(date '+%Y-%m-%d %H:%M:%S')" >> "$PK/rito_v387_sinal.txt"; return 1
  fi
  return 0
}

VPID=""
RELIGADO=0
VIGIA_MORTO=0
ESPERA_EXPIROU=0
religar() {
  trap '' TERM HUP INT                                # a restauracao nao e' abortada por sinal (4a afericao)
  [ "$RELIGADO" = "1" ] && return 0
  RELIGADO=1
  # (o .rito_v387.pid NAO sai aqui: so no FIM da restauracao, pelo trap do EXIT -- 9a afericao)
  [ -f "$PK/.vigia_ativo" ] && rm -f "$PK/.vigia_ativo"
  if [ -n "$VPID" ]; then
    # o vigia NAO e' morto: ve a bandeira apagada, termina a parada que estiver fazendo e sai sozinho -- nenhuma parada orfa depois do religamento (5a afericao)
    w_=0; while kill -0 "$VPID" 2>/dev/null && [ $w_ -lt 120 ]; do sleep 1; w_=$((w_+1)); done
    if kill -0 "$VPID" 2>/dev/null; then log "AVISO: o vigia nao saiu em 120 s -- encerrado"; kill "$VPID" 2>/dev/null; VIGIA_MORTO=1; fi
  fi
  orfaos
  if [ "$ESTAVA_LIGADO" != "1" ]; then
    log "nao religo: o servidor nao estava ligado antes do rito (estado anterior restaurado)"; rm -f "$MARCA"; return 0
  fi
  # um stop_iald_llama.ps1 do vigia ainda em curso mataria o servidor recem-religado: esperar que nenhum esteja vivo (ate 60 s; 4a afericao)
  j=0
  while [ $j -lt 12 ]; do
    s_=$(powershell.exe -NoProfile -NonInteractive -Command "@(Get-CimInstance Win32_Process -Filter \"Name='powershell.exe' OR Name='pwsh.exe'\" | Where-Object { \$_.CommandLine -and ((\$_.CommandLine -match 'Stop-Scheduled[T]ask' -and \$_.CommandLine -match 'IALD Llama') -or \$_.CommandLine -match 'stop_iald_llam[a]\.ps1') }).Count" 2>/dev/null | tr -d '\r')   # a MESMA consulta da reconferencia (9a)
    [ "$s_" = "0" ] && break
    sleep 5; j=$((j+1))
  done
  [ "$s_" = "0" ] || { log "AVISO: depois de 60 s ainda havia parada em curso ou a contagem nao foi legivel ('$s_') -- religo assim mesmo"; ESPERA_EXPIROU=1; }
  log "RELIGANDO o servidor do modelo nativo pela tarefa agendada (como no boot)"
  powershell.exe -NoProfile -NonInteractive -Command "Start-ScheduledTask -TaskName 'IALD Llama Server'" >> "$LOGS" 2>&1
  i=0
  while [ $i -lt 36 ]; do
    if powershell.exe -NoProfile -NonInteractive -Command "if (Get-NetTCPConnection -State Listen -LocalPort 8081 -ErrorAction SilentlyContinue) { exit 0 } else { exit 1 }" > /dev/null 2>&1; then
      if [ "$VIGIA_MORTO" = "1" ] || [ "$ESPERA_EXPIROU" = "1" ]; then
        # depois de um AVISO, uma parada pendente pode derrubar o servidor recem-religado: reconferir a porta 30 s depois (6a afericao)
        sleep 30
        if powershell.exe -NoProfile -NonInteractive -Command "if (Get-NetTCPConnection -State Listen -LocalPort 8081 -ErrorAction SilentlyContinue) { exit 0 } else { exit 1 }" > /dev/null 2>&1; then
          # nenhuma parada ainda em curso (as classes [T] e [a] impedem a consulta de casar consigo mesma) -- senao, ou com a contagem ilegivel, o marcador fica (7a-9a)
          sp_=$(powershell.exe -NoProfile -NonInteractive -Command "@(Get-CimInstance Win32_Process -Filter \"Name='powershell.exe' OR Name='pwsh.exe'\" | Where-Object { \$_.CommandLine -and ((\$_.CommandLine -match 'Stop-Scheduled[T]ask' -and \$_.CommandLine -match 'IALD Llama') -or \$_.CommandLine -match 'stop_iald_llam[a]\.ps1') }).Count" 2>/dev/null | tr -d '\r')
          case "$sp_" in
            0) log "servidor de volta: a porta 8081 escuta (reconferida 30 s depois, por causa do AVISO acima)"; rm -f "$MARCA"; return 0;;
            ''|*[!0-9]*) log "AVISO: a porta 8081 escuta, mas a contagem das paradas em curso nao foi legivel ('$sp_') -- o marcador fica: $MARCA"; return 0;;
            *) log "AVISO: a porta 8081 escuta, mas ha parada (Stop-ScheduledTask ou stop_iald_llama.ps1) ainda em curso ($sp_) -- o marcador fica: $MARCA"; return 0;;
          esac
        fi
        log "AVISO: a porta 8081 escutou e PAROU em seguida (uma parada pendente?) -- conferir a tarefa; o marcador fica: $MARCA"; return 0
      fi
      log "servidor de volta: a porta 8081 escuta"; rm -f "$MARCA"; return 0
    fi
    sleep 5; i=$((i+1))
  done
  log "AVISO: a porta 8081 nao escutou em 180 s depois do religamento -- conferir a tarefa «IALD Llama Server» (o marcador fica: $MARCA)"
}

RITO_INICIADO=0
sinal() {
  # tres estados (5a afericao): 0 antes do rito, 1 durante, 2 depois (o RITO_RC ja foi gravado)
  if [ "$RITO_INICIADO" = "1" ]; then
    log "SINAL $1 recebido durante o rito: o rito esta perdido -- encerro a arvore do um.py desta rodada e restauro o servidor"
    mata_um
    echo "RITO_RC=SINAL_$1" >> rodada_v387_stdout.txt
    echo "RITO_RC=SINAL_$1 $(date '+%Y-%m-%d %H:%M:%S')" >> "$PK/rito_v387_sinal.txt"   # o um.py ainda vivo poderia sobrescrever o trailer do stdout (6a afericao)
  elif [ "$RITO_INICIADO" = "2" ]; then
    log "SINAL $1 recebido DEPOIS do rito (RITO_RC=$rc ja gravado): restauro o servidor"; exit $rc
  else
    log "SINAL $1 recebido ANTES do rito comecar: nada a encerrar; restauro o servidor"   # o stdout da tentativa anterior nao e' tocado (4a afericao)
  fi
  exit 143
}

# 0. o estado de antes (para restaurar exatamente ele), o marcador de uma rodada morta e os orfaos
TAREFA_EXISTE=$(powershell.exe -NoProfile -NonInteractive -Command "if (Get-ScheduledTask -TaskName 'IALD Llama Server' -ErrorAction SilentlyContinue) { '1' } else { '0' }" 2>/dev/null | tr -d '\r')
case "$TAREFA_EXISTE" in 0|1) ;; *) log "a sonda da tarefa falhou ('$TAREFA_EXISTE') -- NAO RODO"; exit 14;; esac
T_RODANDO=$(powershell.exe -NoProfile -NonInteractive -Command "\$t = Get-ScheduledTask -TaskName 'IALD Llama Server' -ErrorAction SilentlyContinue; if (\$t -and \$t.State -eq 'Running') { '1' } else { '0' }" 2>/dev/null | tr -d '\r')
P_VIVO=$(powershell.exe -NoProfile -NonInteractive -Command "if (@(Get-Process llama-server -ErrorAction SilentlyContinue).Count -gt 0) { '1' } else { '0' }" 2>/dev/null | tr -d '\r')
T_DESAB=$(powershell.exe -NoProfile -NonInteractive -Command "\$t = Get-ScheduledTask -TaskName 'IALD Llama Server' -ErrorAction SilentlyContinue; if (\$t -and \$t.State -eq 'Disabled') { '1' } else { '0' }" 2>/dev/null | tr -d '\r')
case "$T_DESAB" in 0|1) ;; *) log "a sonda da tarefa DESABILITADA falhou ('$T_DESAB') -- NAO RODO"; exit 14;; esac   # fail-closed, como a sonda da tarefa (5a afericao)
ORIGEM=""
[ "$T_RODANDO" = "1" ] && ORIGEM="$ORIGEM tarefa-rodando"
[ "$P_VIVO" = "1" ] && ORIGEM="$ORIGEM processo-vivo"
{ [ -z "$T_RODANDO" ] || [ -z "$P_VIVO" ]; } && ORIGEM="$ORIGEM sonda-vazia"
if [ -n "$ORIGEM" ]; then ESTAVA_LIGADO=1; else ESTAVA_LIGADO=0; fi   # sonda vazia = «ligado» (a favor do servico)
if [ -f "$MARCA" ]; then
  # o marcador de uma rodada que morreu com o servidor parado: vale o que ELE gravou (restaurar=0|1), nao mais (4a afericao)
  if grep -q "restaurar=1" "$MARCA"; then
    log "MARCADOR de uma rodada anterior que morreu com o servidor parado ($(cat "$MARCA")) -- o servidor sera religado no fim"; ESTAVA_LIGADO=1; ORIGEM="$ORIGEM marcador"
  else
    log "MARCADOR de uma rodada anterior com restaurar=0 ($(cat "$MARCA")) -- o servidor nao estava ligado; marcador removido"; rm -f "$MARCA"
  fi
fi
log "antes: tarefa existe=$TAREFA_EXISTE ; tarefa rodando=$T_RODANDO ; tarefa desabilitada=$T_DESAB ; llama-server vivo=$P_VIVO ; restaurar no fim=$ESTAVA_LIGADO (origem:${ORIGEM:- nenhuma})"
if [ "$TAREFA_EXISTE" != "1" ] && [ "$ESTAVA_LIGADO" = "1" ]; then
  log "restaurar=1 (origem:$ORIGEM) mas a tarefa agendada NAO existe: nao saberia religar o servidor -- NAO RODO (suba-o pela tarefa ou pare-o antes)"; exit 13
fi
if [ "$T_DESAB" = "1" ] && [ "$ESTAVA_LIGADO" = "1" ]; then
  log "restaurar=1 (origem:$ORIGEM) mas a tarefa agendada esta DESABILITADA: Start-ScheduledTask nao religaria -- NAO RODO"; exit 15
fi
orfaos
# 1. o trap ANTES de parar (TERM/HUP/INT durante a parada tambem restauram); depois parar: a TAREFA primeiro, depois o supervisor e os orfaos
trap 'religar; rm -f "$PK/.rito_v387.pid"' EXIT   # o PID so sai DEPOIS da restauracao inteira (9a afericao)
trap 'sinal TERM' TERM; trap 'sinal HUP' HUP; trap 'sinal INT' INT
# (o .rito_v387.pid ja foi gravado logo depois da guarda; abortar = kill -TERM $(cat .rito_v387.pid) NO GIT BASH, conferindo antes o /proc/<pid>/cmdline)
echo "$(date '+%Y-%m-%d %H:%M:%S') servidor parado pelo rito v387 (restaurar=$ESTAVA_LIGADO)" > "$MARCA"
log "PARANDO o servidor do modelo nativo: tarefa agendada, supervisor e llama-server (ordem do operador, 03/10)"
powershell.exe -NoProfile -NonInteractive -Command "Stop-ScheduledTask -TaskName 'IALD Llama Server'" >> "$LOGS" 2>&1
powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File "$STOPPS" -Tudo >> "$LOGS" 2>&1
sleep 5
vivos=$(powershell.exe -NoProfile -NonInteractive -Command "@(Get-Process llama-server -ErrorAction SilentlyContinue).Count" 2>/dev/null | tr -d '\r')
mem=$(nvidia-smi --query-gpu=memory.used --format=csv,noheader,nounits 2>/dev/null | head -1 | tr -d ' \r')
log "depois da parada: llama-server vivos = $vivos ; VRAM usada = $mem MiB"
if [ "$vivos" != "0" ]; then
  log "O SERVIDOR NAO PAROU -- NAO RODO (fail-closed); o trap restaura o estado anterior"; exit 10
fi
case "$mem" in ''|*[!0-9]*) log "a VRAM usada nao e' legivel ('$mem') -- NAO RODO (fail-closed)"; exit 12;; esac
if [ "$mem" -gt 6000 ]; then
  log "a VRAM usada ($mem MiB) passa de 6000 MiB com o servidor parado: ha outro processo na GPU -- NAO RODO (fail-closed)"; exit 11
fi

# a ROTACAO, so agora, depois da ULTIMA recusa: o log real da rodada anterior (e o registro dos sinais) so sai do lugar quando esta rodada vai mesmo rodar
# o giro CONFERIDO (9a afericao): se falhar, FALHA VISIVEL e recusa 17 -- o trap restaura o servidor; nada de anexar ao log de outra rodada.
# Os SINAIS giram PRIMEIRO (10a afericao): toda recusa 17 acontece com o log real ainda no lugar, e o registro dela fica no .fase0
# [ERRATA AO LADO, 11a: «toda» vale para a 17 dos sinais e a do log real; a da troca do .fase0 pelo log real vem DEPOIS de o log real girar -- sem perda:
#  o registro dela fica no .fase0, e a tentativa seguinte o acrescenta ao .fase0.anterior sem tocar o .anterior do log real]
if [ -f "$PK/rito_v387_sinal.txt" ]; then mv -f "$PK/rito_v387_sinal.txt" "$PK/rito_v387_sinal.txt.anterior" || { log "FALHA VISIVEL: o registro dos sinais nao girou -- NAO RODO"; exit 17; }; fi
if [ -f "$LOGF" ]; then mv -f "$LOGF" "$LOGF.anterior" || { log "FALHA VISIVEL: o log real da rodada anterior nao girou -- NAO RODO"; exit 17; }; fi
mv -f "$LOGS" "$LOGF" || { log "FALHA VISIVEL: o log da tentativa nao tomou o lugar do log real -- NAO RODO"; exit 17; }
LOGS="$LOGF"
# 2. o vigia: se o servidor reaparecer durante o rito, e' encerrado e o fato fica no log
touch "$PK/.vigia_ativo"
PAI=$$
(
  t_ini=$(date +%s)
  while [ -f "$PK/.vigia_ativo" ]; do
    # o vigia morre com o lancador (se o sh for morto a forca, o trap nao roda) e nunca passa de 8 h
    kill -0 "$PAI" 2>/dev/null || { echo "$(date +%H:%M:%S) VIGIA: o lancador morreu -- o vigia sai" >> "$LOGS"; break; }
    [ $(( $(date +%s) - t_ini )) -gt 28800 ] && { echo "$(date +%H:%M:%S) VIGIA: 8 h -- o vigia sai" >> "$LOGS"; break; }
    c=$(powershell.exe -NoProfile -NonInteractive -Command "@(Get-Process llama-server -ErrorAction SilentlyContinue).Count" 2>/dev/null | tr -d '\r')
    if [ -n "$c" ] && [ "$c" != "0" ]; then
      echo "$(date +%H:%M:%S) VIGIA: o llama-server REAPARECEU ($c) durante o rito -- encerrando" >> "$LOGS"
      powershell.exe -NoProfile -NonInteractive -Command "Stop-ScheduledTask -TaskName 'IALD Llama Server'" >> "$LOGS" 2>&1
      powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File "$STOPPS" -Tudo >> "$LOGS" 2>&1
    fi
    k_=0; while [ $k_ -lt 60 ] && [ -f "$PK/.vigia_ativo" ]; do sleep 1; k_=$((k_+1)); done   # dorme em passos de 1 s: sai logo depois da bandeira (5a afericao)
  done
) &
VPID=$!

# 3. o rito (em segundo plano + wait: um sinal ao lancador age na hora, sem esperar o rito acabar)
if [ -f rodada_v387_stdout.txt ]; then n=1; while [ -f "rodada_v387_stdout_tentativa$n.txt" ]; do n=$((n+1)); done; mv rodada_v387_stdout.txt "rodada_v387_stdout_tentativa$n.txt"; fi
t0=$(date +%H:%M:%S); echo "$t0" > "$PK/rito_horarios_v387.txt"
log "inicio do rito $t0 (um.py $h)"
RITO_INICIADO=1
( echo 1 | python um.py > rodada_v387_stdout.txt 2>&1 ) &
UMPID=$!
wait "$UMPID"
rc=$?
echo "RITO_RC=$rc" >> rodada_v387_stdout.txt
RITO_INICIADO=2
t1=$(date +%H:%M:%S); echo "$t1" >> "$PK/rito_horarios_v387.txt"
log "fim do rito $t1 rc=$rc"
tail -3 rodada_v387_stdout.txt
exit $rc
