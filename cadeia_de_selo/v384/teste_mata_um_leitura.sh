#!/bin/sh
# Teste SO DE LEITURA do mata_um do rito_v384.sh (7a afericao, achado [6]: a evidencia do teste tem de ficar guardada). NADA e' encerrado: nenhum taskkill.
# (1) o caminho principal: o PID nativo de um subshell que roda um python um.py FALSO (/proc/<pid>/winpid);
# (2) a reserva: a MESMA consulta do mata_um (descendentes do lancador com a data de criacao conferida; so python um.py; sentinela MATA_OK).
D="$(cd "$(dirname "$0")" && pwd)/teste_mata_um"
mkdir -p "$D"
printf 'import time\ntime.sleep(10)\n' > "$D/um.py"
RW=$(cat /proc/$$/winpid 2>/dev/null)
echo "lancador (este sh): PID MSYS $$ ; winpid $RW"
( cd "$D" && python um.py ) &
UMPID=$!
sleep 2
W=$(cat /proc/$UMPID/winpid 2>/dev/null)
echo "(1) subshell do rito falso: PID MSYS $UMPID ; winpid '$W' (o caminho principal faria taskkill //T //F //PID $W -- NAO feito)"
u=$(powershell.exe -NoProfile -NonInteractive -Command "\$ErrorActionPreference='Stop'; \$all = Get-CimInstance Win32_Process; \$byid = @{}; foreach (\$x in \$all) { \$byid[[int]\$x.ProcessId] = \$x }; \$d = @($RW); \$i = 0; while (\$i -lt \$d.Count) { \$p = \$d[\$i]; \$pp = \$byid[[int]\$p]; foreach (\$c in \$all) { if (\$c.ParentProcessId -eq \$p -and -not (\$d -contains \$c.ProcessId) -and (\$pp -eq \$null -or \$c.CreationDate -ge \$pp.CreationDate)) { \$d += \$c.ProcessId } }; \$i++ }; \$all | Where-Object { (\$d -contains \$_.ProcessId) -and \$_.ProcessId -ne $RW -and \$_.Name -match '^(python|pythonw|py)\.exe\$' -and \$_.CommandLine -match '(^|[\\\\ \"])um\\.py\"?(\\s|\$)' } | ForEach-Object { \$_.ProcessId.ToString() + ' ' + \$_.CommandLine }; Write-Output 'MATA_OK'" 2>&1 | tr -d '\r')
echo "(2) reserva (descendentes python um.py; sentinela):"
echo "$u"
echo "$u" | grep -q "MATA_OK" && echo "SENTINELA: presente" || echo "SENTINELA: AUSENTE"
wait
echo "fim (nada encerrado)"
