#!/bin/sh
# O RITO v377 (ato da gerencia; ordem do operador «pode rodar», 30/09/2026): echo 1 | python um.py no Nos, stdout canonico em rodada_v377_stdout.txt,
# trailer RITO_RC=<rc>, horarios no pacote. Pre-condicao: instalar_v377.py aplicado (um.py do disco = candidato). Nao roda se ja houver processo um.py vivo.
PK="/c/Users/rotol/AppData/Local/Temp/claude/c--IALD-Central-de-Patentes/6da8f00d-d44f-4888-a88d-fc9f73eead3d/scratchpad/v377"
NOS="/c/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós"
export PYTHONIOENCODING=utf-8
unset TGL_RITE_CHECKPOINT TGL_CACHE_DIR
cd "$NOS" || exit 9
h=$(python -c "import hashlib;print(hashlib.sha256(open('um.py','rb').read()).hexdigest()[:16])")
e=$(python -c "import json;print(json.load(open('C:/Users/rotol/AppData/Local/Temp/claude/c--IALD-Central-de-Patentes/6da8f00d-d44f-4888-a88d-fc9f73eead3d/scratchpad/v377/ESPERADOS_v377.json',encoding='utf-8'))['candidato_sha16'])")
[ "$h" = "$e" ] || { echo "um.py do disco ($h) != candidato esperado ($e) -- NAO RODO"; exit 8; }
if [ -f rodada_v377_stdout.txt ]; then n=1; while [ -f "rodada_v377_stdout_tentativa$n.txt" ]; do n=$((n+1)); done; mv rodada_v377_stdout.txt "rodada_v377_stdout_tentativa$n.txt"; fi
t0=$(date +%H:%M:%S); echo "$t0" > "$PK/rito_horarios_v377.txt"
echo "inicio $t0 (um.py $h)"
echo 1 | python um.py > rodada_v377_stdout.txt 2>&1
rc=$?
echo "RITO_RC=$rc" >> rodada_v377_stdout.txt
t1=$(date +%H:%M:%S); echo "$t1" >> "$PK/rito_horarios_v377.txt"
echo "fim $t1 rc=$rc"
tail -3 rodada_v377_stdout.txt
exit $rc
