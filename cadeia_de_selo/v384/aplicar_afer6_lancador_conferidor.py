# -*- coding: utf-8 -*-
"""6a afericao no LANCADOR e no CONFERIDOR (por script, count == 1):
- o mata_um e' fail-closed: encerra a arvore pelo PID NATIVO do subshell do rito (o pai Windows da cadeia); so se ele for ilegivel, procura os python um.py
  DESCENDENTES do lancador (com a data de criacao conferida contra o pai, contra PID reaproveitado) e exige a sentinela MATA_OK; se nada disso der, ou se o
  subshell seguir vivo, e' FALHA VISIVEL no log e em rito_v384_sinal.txt (o trailer do stdout pode ser sobrescrito pelo um.py ainda vivo);
- se o vigia foi morto por prazo ou a espera pelos stop expirou, a porta 8081 e' reconferida 30 s depois e o marcador so sai se ela ainda escutar;
- um .rito_v384.pid velho e' dito no log; o cabecalho diz que o PID e' do MSYS (abortar no Git Bash, nao no PowerShell);
- o conferidor devolve TODA linha AVISO do log do lancador e diz «COM AVISO».
Backups ja feitos (.bak_antes_afer6)."""
import ast, os, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
P = os.path.join(HERE, "rito_v384.sh")
raw = open(P, "rb").read(); s = raw.decode("utf-8")
assert open(P + ".bak_antes_afer6", "rb").read() == raw
MATA_OLD_START = '''mata_um() {
  # encerra a ARVORE do um.py DESTA rodada (o rito esta perdido): so os um.py DESCENDENTES do lancador, nunca os de outra casa (5a afericao)'''
i0 = s.index(MATA_OLD_START); i1 = s.index("\n}\n", i0) + 3
MATA_NEW = r'''mata_um() {
  # encerra a ARVORE do rito DESTA rodada (o rito esta perdido) -- nunca a de outra casa (5a afericao) -- e e' FAIL-CLOSED (6a afericao):
  # (1) pelo PID nativo do subshell do rito, o pai Windows da cadeia (python um.py -> trabalhador -> referencia na CPU);
  # (2) so se ele for ilegivel, pelos python um.py DESCENDENTES do lancador (data de criacao do filho >= a do pai: PID reaproveitado nao entra), com a
  #     sentinela MATA_OK; (3) se nada der, ou se o subshell seguir vivo, FALHA VISIVEL no log e em rito_v384_sinal.txt.
  MATOU=0
  W=$(cat /proc/$UMPID/winpid 2>/dev/null)
  case "$W" in ''|*[!0-9]*) W="";; esac
  if [ -n "$W" ]; then
    log "encerrando a arvore do rito pelo PID nativo do subshell ($W)"
    taskkill //T //F //PID "$W" >> "$LOGS" 2>&1 && MATOU=1
  fi
  if [ "$MATOU" != "1" ]; then
    RW=$(cat /proc/$$/winpid 2>/dev/null)
    case "$RW" in ''|*[!0-9]*) log "FALHA VISIVEL: nem o PID do subshell nem o do lancador sao legiveis -- o um.py desta rodada pode seguir vivo (encerre-o a mao)"; echo "UM_PY_TALVEZ_VIVO $(date '+%Y-%m-%d %H:%M:%S')" >> "$PK/rito_v384_sinal.txt"; return 1;; esac
    u=$(powershell.exe -NoProfile -NonInteractive -Command "\$ErrorActionPreference='Stop'; \$all = Get-CimInstance Win32_Process; \$byid = @{}; foreach (\$x in \$all) { \$byid[[int]\$x.ProcessId] = \$x }; \$d = @($RW); \$i = 0; while (\$i -lt \$d.Count) { \$p = \$d[\$i]; \$pp = \$byid[[int]\$p]; foreach (\$c in \$all) { if (\$c.ParentProcessId -eq \$p -and -not (\$d -contains \$c.ProcessId) -and (\$pp -eq \$null -or \$c.CreationDate -ge \$pp.CreationDate)) { \$d += \$c.ProcessId } }; \$i++ }; \$all | Where-Object { (\$d -contains \$_.ProcessId) -and \$_.ProcessId -ne $RW -and \$_.Name -match '^(python|pythonw|py)\.exe\$' -and \$_.CommandLine -match '(^|[\\\\ \"])um\\.py\"?(\\s|\$)' } | ForEach-Object { \$_.ProcessId }; Write-Output 'MATA_OK'" 2>&1 | tr -d '\r')
    echo "$u" | grep -q "MATA_OK" || { log "FALHA VISIVEL: a consulta dos descendentes falhou ($u) -- o um.py desta rodada pode seguir vivo"; echo "UM_PY_TALVEZ_VIVO $(date '+%Y-%m-%d %H:%M:%S')" >> "$PK/rito_v384_sinal.txt"; return 1; }
    for p in $(echo "$u" | grep -E '^[0-9]+$'); do log "encerrando a arvore do um.py desta rodada (PID $p)"; taskkill //T //F //PID "$p" >> "$LOGS" 2>&1 && MATOU=1; done
  fi
  sleep 2
  if kill -0 "$UMPID" 2>/dev/null || [ "$MATOU" != "1" ]; then
    log "FALHA VISIVEL: o encerramento nao se confirmou (subshell vivo ou nada encerrado) -- o um.py desta rodada pode seguir vivo"
    echo "UM_PY_TALVEZ_VIVO $(date '+%Y-%m-%d %H:%M:%S')" >> "$PK/rito_v384_sinal.txt"; return 1
  fi
  return 0
}
'''
s = s[:i0] + MATA_NEW + s[i1:]
PAIRS = [
    ('''    mata_um
    echo "RITO_RC=SINAL_$1" >> rodada_v384_stdout.txt''', '''    mata_um
    echo "RITO_RC=SINAL_$1" >> rodada_v384_stdout.txt
    echo "RITO_RC=SINAL_$1 $(date '+%Y-%m-%d %H:%M:%S')" >> "$PK/rito_v384_sinal.txt"   # o um.py ainda vivo poderia sobrescrever o trailer do stdout (6a afericao)'''),
    ('''    if kill -0 "$VPID" 2>/dev/null; then log "AVISO: o vigia nao saiu em 120 s -- encerrado"; kill "$VPID" 2>/dev/null; fi''',
     '''    if kill -0 "$VPID" 2>/dev/null; then log "AVISO: o vigia nao saiu em 120 s -- encerrado"; kill "$VPID" 2>/dev/null; VIGIA_MORTO=1; fi'''),
    ('''  [ "$s_" = "0" ] || log "AVISO: depois de 60 s ainda havia parada em curso ou a contagem nao foi legivel ('$s_') -- religo assim mesmo"''',
     '''  [ "$s_" = "0" ] || { log "AVISO: depois de 60 s ainda havia parada em curso ou a contagem nao foi legivel ('$s_') -- religo assim mesmo"; ESPERA_EXPIROU=1; }'''),
    ('''      log "servidor de volta: a porta 8081 escuta"; rm -f "$MARCA"; return 0''',
     '''      if [ "$VIGIA_MORTO" = "1" ] || [ "$ESPERA_EXPIROU" = "1" ]; then
        # depois de um AVISO, uma parada pendente pode derrubar o servidor recem-religado: reconferir a porta 30 s depois (6a afericao)
        sleep 30
        if powershell.exe -NoProfile -NonInteractive -Command "if (Get-NetTCPConnection -State Listen -LocalPort 8081 -ErrorAction SilentlyContinue) { exit 0 } else { exit 1 }" > /dev/null 2>&1; then
          log "servidor de volta: a porta 8081 escuta (reconferida 30 s depois, por causa do AVISO acima)"; rm -f "$MARCA"; return 0
        fi
        log "AVISO: a porta 8081 escutou e PAROU em seguida (uma parada pendente?) -- conferir a tarefa; o marcador fica: $MARCA"; return 0
      fi
      log "servidor de volta: a porta 8081 escuta"; rm -f "$MARCA"; return 0'''),
    ('''VPID=""
RELIGADO=0''', '''VPID=""
RELIGADO=0
VIGIA_MORTO=0
ESPERA_EXPIROU=0'''),
    ('''echo $$ > "$PK/.rito_v384.pid"   # abortar = kill -TERM $(cat .rito_v384.pid) (5a afericao)''',
     '''[ -f "$PK/.rito_v384.pid" ] && log "um .rito_v384.pid VELHO estava no pacote ($(cat "$PK/.rito_v384.pid")): de um lancador que morreu sem restaurar -- sobrescrito"
echo $$ > "$PK/.rito_v384.pid"   # abortar = kill -TERM $(cat .rito_v384.pid) NO GIT BASH (e' PID do MSYS, nao do Windows) (5a e 6a afericoes)'''),
    ('''# com & por shell nao interativo nem com nohup (POSIX); TERM sempre. ABORTAR o rito = kill -TERM $(cat <pacote>/.rito_v384.pid) -- o TaskStop da ferramenta
# da gerencia NAO para o lancador.''', '''# com & por shell nao interativo nem com nohup (POSIX); TERM sempre. ABORTAR o rito = kill -TERM $(cat <pacote>/.rito_v384.pid) NO GIT BASH (sh), nao no
# PowerShell: o numero e' o PID do MSYS, nao o do Windows -- o TaskStop da ferramenta da gerencia NAO para o lancador.'''),
]
for old, new in PAIRS:
    c = s.count(old); assert c == 1, (c, old[:120])
    s = s.replace(old, new)
b = s.encode("utf-8"); assert b"\r" not in b
open(P + ".tmp", "wb").write(b); assert os.path.getsize(P + ".tmp") == len(b); os.replace(P + ".tmp", P)
print("ok lancador", len(PAIRS) + 1)
# o conferidor: todos os AVISOs
C = os.path.join(HERE, "conferir_rito_v384.py"); c = open(C, "rb").read().decode("utf-8")
assert open(C + ".bak_antes_afer6", "rb").read().decode("utf-8") == c
old = '''print("servidor do modelo nativo depois do rito (informacao):", res["servidor_depois_do_rito"])'''
new = '''res["avisos_do_lancador"] = [l_ for l_ in _lt.splitlines() if "AVISO" in l_ or "FALHA VISIVEL" in l_]   # TODA linha de AVISO/FALHA (6a afericao)
if res["avisos_do_lancador"] and res["servidor_depois_do_rito"].startswith("RELIGADO"):
    res["servidor_depois_do_rito"] = "RELIGADO COM AVISO: " + " | ".join(res["avisos_do_lancador"])
print("servidor do modelo nativo depois do rito (informacao):", res["servidor_depois_do_rito"])
for l_ in res["avisos_do_lancador"]:
    print("  AVISO DO LANCADOR:", l_)'''
assert c.count(old) == 1
c = c.replace(old, new); ast.parse(c)
open(C + ".tmp", "wb").write(c.encode("utf-8")); os.replace(C + ".tmp", C); print("ok conferidor")
