#!/bin/sh
# Teste do mata_um do rito_v384.sh NA FORMA DO RITO (8a afericao): o subshell e' ( echo 1 | python um.py > f 2>&1 ) & -- com o cano, o subshell NAO vira o
# python (diferente do teste so de leitura da 7a, em que ( cd D && python um.py ) & fazia o subshell virar o proprio python). O um.py aqui e' FALSO (le a
# entrada e dorme 30 s) e mora em teste_mata_um_rito/; so processos DESTE teste sao encerrados.
# (A) o caminho principal: o PID nativo do subshell (/proc/<pid>/winpid) -> taskkill /T /F -> o python um.py falso tem de morrer com a arvore;
# (B) a reserva: a MESMA consulta do mata_um (descendentes deste sh com a data de criacao conferida; so python um.py; sentinela MATA_OK) -> taskkill de cada um.
D="$(cd "$(dirname "$0")" && pwd)/teste_mata_um_rito"
mkdir -p "$D"
printf 'import sys, time\nsys.stdin.readline()\ntime.sleep(30)\n' > "$D/um.py"
RW=$(cat /proc/$$/winpid 2>/dev/null)
echo "este sh: PID MSYS $$ ; winpid $RW"
arvore() {
  powershell.exe -NoProfile -NonInteractive -Command "\$all = Get-CimInstance Win32_Process; \$d = @($1); \$i = 0; while (\$i -lt \$d.Count) { \$p = \$d[\$i]; foreach (\$c in \$all) { if (\$c.ParentProcessId -eq \$p -and -not (\$d -contains \$c.ProcessId)) { \$d += \$c.ProcessId } }; \$i++ }; \$all | Where-Object { \$d -contains \$_.ProcessId } | ForEach-Object { \$_.ProcessId.ToString() + ' ' + \$_.Name + ' ' + \$_.CommandLine }" 2>&1 | tr -d '\r'
}
vivo_py() {   # quantos python um.py vivos ha na arvore deste sh
  powershell.exe -NoProfile -NonInteractive -Command "\$all = Get-CimInstance Win32_Process; \$d = @($RW); \$i = 0; while (\$i -lt \$d.Count) { \$p = \$d[\$i]; foreach (\$c in \$all) { if (\$c.ParentProcessId -eq \$p -and -not (\$d -contains \$c.ProcessId)) { \$d += \$c.ProcessId } }; \$i++ }; @(\$all | Where-Object { (\$d -contains \$_.ProcessId) -and \$_.Name -match '^(python|pythonw|py)\.exe\$' -and \$_.CommandLine -match 'um\.py' }).Count" 2>&1 | tr -d '\r'
}
cd "$D"
# ---------------- (A) o caminho principal
( echo 1 | python um.py > saida_A.txt 2>&1 ) &
UMPID=$!
sleep 3
W=$(cat /proc/$UMPID/winpid 2>/dev/null)
echo "(A) subshell do rito falso: PID MSYS $UMPID ; winpid '$W'"
echo "(A) a arvore Windows sob o subshell:"; arvore "$W"
echo "(A) python um.py vivos antes: $(vivo_py)"
taskkill //T //F //PID "$W" 2>&1 | tr -d '\r'
sleep 2
kill -0 "$UMPID" 2>/dev/null && echo "(A) o subshell SEGUE VIVO" || echo "(A) o subshell morreu"
NA=$(vivo_py); echo "(A) python um.py vivos depois: $NA"
[ "$NA" = "0" ] && ! kill -0 "$UMPID" 2>/dev/null && echo "(A) PASSOU" || echo "(A) FALHOU"
wait 2>/dev/null
# ---------------- (B) a reserva
( echo 1 | python um.py > saida_B.txt 2>&1 ) &
UMPID=$!
sleep 3
u=$(powershell.exe -NoProfile -NonInteractive -Command "\$ErrorActionPreference='Stop'; \$all = Get-CimInstance Win32_Process; \$byid = @{}; foreach (\$x in \$all) { \$byid[[int]\$x.ProcessId] = \$x }; \$d = @($RW); \$i = 0; while (\$i -lt \$d.Count) { \$p = \$d[\$i]; \$pp = \$byid[[int]\$p]; foreach (\$c in \$all) { if (\$c.ParentProcessId -eq \$p -and -not (\$d -contains \$c.ProcessId) -and (\$pp -eq \$null -or \$c.CreationDate -ge \$pp.CreationDate)) { \$d += \$c.ProcessId } }; \$i++ }; \$all | Where-Object { (\$d -contains \$_.ProcessId) -and \$_.ProcessId -ne $RW -and \$_.Name -match '^(python|pythonw|py)\.exe\$' -and \$_.CommandLine -match '(^|[\\\\ \"])um\\.py\"?(\\s|\$)' } | ForEach-Object { \$_.ProcessId }; Write-Output 'MATA_OK'" 2>&1 | tr -d '\r')
echo "(B) a consulta da reserva devolveu:"; echo "$u"
echo "$u" | grep -q "MATA_OK" && echo "(B) SENTINELA: presente" || echo "(B) SENTINELA: AUSENTE"
MB=0
for p in $(echo "$u" | grep -E '^[0-9]+$'); do taskkill //T //F //PID "$p" 2>&1 | tr -d '\r' && MB=1; done
sleep 2
kill -0 "$UMPID" 2>/dev/null && echo "(B) o subshell SEGUE VIVO" || echo "(B) o subshell saiu"
NB=$(vivo_py); echo "(B) python um.py vivos depois: $NB"
[ "$MB" = "1" ] && [ "$NB" = "0" ] && ! kill -0 "$UMPID" 2>/dev/null && echo "(B) PASSOU" || echo "(B) FALHOU"
wait 2>/dev/null
echo "fim"
