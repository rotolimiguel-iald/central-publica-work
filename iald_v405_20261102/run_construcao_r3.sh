#!/bin/bash
# Reconstrucao r3 da release do app (v405): so a frase de recuperacao da capsula muda frente a r2; para na primeira falha. Nada e instalado aqui.
cd "$(dirname "$0")" || exit 9
PY=C:/Python314/python.exe
passo() { n=$1; shift; echo "== $n $(date +%H:%M:%S)"; "$@" > "${n}_stdout.txt" 2> "${n}_stderr.txt"; rc=$?; echo "   rc=$rc"; if [ $rc -ne 0 ]; then tail -5 "${n}_stderr.txt"; tail -5 "${n}_stdout.txt"; echo "PAROU EM $n"; exit $rc; fi; }
passo selftest bash -c "cd app/build && $PY -B -X utf8 haiku_codec.py --self-test"
passo prepare $PY -B -X utf8 app/prepare.py
passo finalize $PY -B -X utf8 app/finalize.py
passo count $PY -B -X utf8 app/count_final_public.py
passo validate $PY -B -X utf8 app/validate_plan.py
passo medidas $PY -B -X utf8 builder_measurements.py
passo busca $PY -B -X utf8 exercita_busca.py
cp busca_stdout.txt BUSCA_EXERCITADA_v405.txt
echo "CONSTRUCAO R3 COMPLETA $(date +%H:%M:%S)"
