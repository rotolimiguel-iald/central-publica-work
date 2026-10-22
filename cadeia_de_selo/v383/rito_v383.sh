#!/bin/sh
# O RITO v383 (ato da gerencia; ordem do operador «prefiro a primeira opção» (os nove pares do eco fora do livro), 02/10/2026, noite): echo 1 | python um.py no Nos, stdout canonico em rodada_v383_stdout.txt,
# trailer RITO_RC=<rc>, horarios no pacote. Pre-condicao: instalar_v383.py aplicado (um.py do disco = candidato). Nao roda se ja houver processo um.py vivo
# (vigia fail-closed, o MESMO do instalador -- aferidor v382 C1/C2).
PK="/c/Users/rotol/AppData/Local/Temp/claude/c--IALD-Central-de-Patentes/6da8f00d-d44f-4888-a88d-fc9f73eead3d/scratchpad/v383"
NOS="/c/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós"
export PYTHONIOENCODING=utf-8
unset TGL_RITE_CHECKPOINT TGL_CACHE_DIR
cd "$NOS" || exit 9
h=$(python -c "import hashlib;print(hashlib.sha256(open('um.py','rb').read()).hexdigest()[:16])")
e=$(python -c "import json;print(json.load(open('C:/Users/rotol/AppData/Local/Temp/claude/c--IALD-Central-de-Patentes/6da8f00d-d44f-4888-a88d-fc9f73eead3d/scratchpad/v383/ESPERADOS_v383.json',encoding='utf-8'))['candidato_sha16'])")
[ "$h" = "$e" ] || { echo "um.py do disco ($h) != candidato esperado ($e) -- NAO RODO"; exit 8; }
v=$(powershell.exe -NoProfile -NonInteractive -Command "\$ErrorActionPreference='Stop'; Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='pythonw.exe' OR Name='py.exe'\" | Where-Object { \$_.CommandLine -ne \$null -and \$_.CommandLine -match '(^|[\\\\ \"])um\\.py\"?(\\s|\$)' } | ForEach-Object { \$_.ProcessId }; Write-Output 'VIGIA_OK'" 2>&1) || { echo "vigia de processos FALHOU: $v -- NAO RODO"; exit 7; }
echo "$v" | grep -q "VIGIA_OK" || { echo "vigia sem VIGIA_OK: $v -- NAO RODO"; exit 7; }
n=$(echo "$v" | grep -c -E '^[0-9]+\s*$'); [ "$n" = "0" ] || { echo "ha processo um.py vivo ($v) -- NAO RODO"; exit 6; }
if [ -f rodada_v383_stdout.txt ]; then n=1; while [ -f "rodada_v383_stdout_tentativa$n.txt" ]; do n=$((n+1)); done; mv rodada_v383_stdout.txt "rodada_v383_stdout_tentativa$n.txt"; fi
t0=$(date +%H:%M:%S); echo "$t0" > "$PK/rito_horarios_v383.txt"
echo "inicio $t0 (um.py $h)"
echo 1 | python um.py > rodada_v383_stdout.txt 2>&1
rc=$?
echo "RITO_RC=$rc" >> rodada_v383_stdout.txt
t1=$(date +%H:%M:%S); echo "$t1" >> "$PK/rito_horarios_v383.txt"
echo "fim $t1 rc=$rc"
tail -3 rodada_v383_stdout.txt
exit $rc
