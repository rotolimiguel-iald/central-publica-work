#!/bin/bash
# v407, etapa 1 (offline): claims, fontes, prepare e finalize; para na primeira falha. Nada e instalado aqui e nenhuma API e chamada (a contagem nativa fica para a etapa 2,
# depois de a janela P2 ser conferida contra a folga medida).
cd "$(dirname "$0")" || exit 9
PY=C:/Python314/python.exe
BLD=claude-app-orquestrador
passo() { n=$1; shift; echo "== $n $(date +%H:%M:%S)"; "$@" > "${n}_stdout.txt" 2> "${n}_stderr.txt"; rc=$?; echo "   rc=$rc"; if [ $rc -ne 0 ]; then tail -5 "${n}_stderr.txt"; tail -5 "${n}_stdout.txt"; echo "PAROU EM $n"; exit $rc; fi; }
passo claim_sources $PY -B -X utf8 mission_step.py claim sources --actor $BLD
passo claim_app $PY -B -X utf8 mission_step.py claim app --actor $BLD
passo sources $PY -B -X utf8 verify_sources.py
passo prepare $PY -B -X utf8 app/prepare.py
passo finalize $PY -B -X utf8 app/finalize.py
echo "ETAPA 1 COMPLETA $(date +%H:%M:%S)"
