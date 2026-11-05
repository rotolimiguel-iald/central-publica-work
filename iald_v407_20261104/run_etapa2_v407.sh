#!/bin/bash
# v407, etapa 2: contagem nativa (SO contagem, 0 geracao; 3 pacotes x 2 pedidos, max_retries=0), validacao do plano, medidas do construtor e exercicio da busca.
# Para na primeira falha. Nada e instalado aqui.
cd "$(dirname "$0")" || exit 9
PY=C:/Python314/python.exe
passo() { n=$1; shift; echo "== $n $(date +%H:%M:%S)"; "$@" > "${n}_stdout.txt" 2> "${n}_stderr.txt"; rc=$?; echo "   rc=$rc"; if [ $rc -ne 0 ]; then tail -5 "${n}_stderr.txt"; tail -5 "${n}_stdout.txt"; echo "PAROU EM $n"; exit $rc; fi; }
passo count $PY -B -X utf8 app/count_final_public.py
passo validate $PY -B -X utf8 app/validate_plan.py
passo medidas $PY -B -X utf8 builder_measurements.py
passo busca $PY -B -X utf8 exercita_busca.py
cp busca_stdout.txt BUSCA_EXERCITADA_v407.txt
echo "ETAPA 2 COMPLETA $(date +%H:%M:%S)"
