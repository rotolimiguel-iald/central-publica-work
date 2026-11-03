#!/bin/bash
# Construcao da release do app (v405), do preflight ao plano de instalacao; para na primeira falha. Nada e instalado aqui.
cd "$(dirname "$0")" || exit 9
PY=C:/Python314/python.exe
BLD=opus-app-v405-construtor
passo() { n=$1; shift; echo "== $n $(date +%H:%M:%S)"; "$@" > "${n}_stdout.txt" 2> "${n}_stderr.txt"; rc=$?; echo "   rc=$rc"; if [ $rc -ne 0 ]; then tail -5 "${n}_stderr.txt"; tail -5 "${n}_stdout.txt"; echo "PAROU EM $n"; exit $rc; fi; }
passo preflight $PY -B -X utf8 app/preflight_offline.py
passo task $PY -B -X utf8 task.py
passo claim_sources $PY -B -X utf8 mission_step.py claim sources --actor $BLD
passo claim_app $PY -B -X utf8 mission_step.py claim app --actor $BLD
passo sources $PY -B -X utf8 verify_sources.py
passo prepare $PY -B -X utf8 app/prepare.py
passo finalize $PY -B -X utf8 app/finalize.py
passo count $PY -B -X utf8 app/count_final_public.py
passo validate $PY -B -X utf8 app/validate_plan.py
echo "CONSTRUCAO COMPLETA $(date +%H:%M:%S)"
