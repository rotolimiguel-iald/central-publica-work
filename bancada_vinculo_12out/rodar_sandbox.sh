#!/bin/sh
# rodar_sandbox.sh -- a sequencia do ensaio do vinculo (12/10/2026), toda dentro de work\bancada_vinculo_12out\sandbox:
#   run 1: fase pre_selo, modo ensaio, Nos REAL v391, a COPIA como Bancada (ja sincronizada -> bateria inteira, T12-T14 incluidos)
#   controles negativos (a copia segue B2; cada recusa esperada tem de acontecer e nada se grava)
#   run 2: fase pos_selo, modo aplicar, Nos SINTETICO v392, a COPIA como Bancada, com o recibo pre-selo do run 1 (re-pino B3 na copia)
# A producao (C:\IALD\Bancada_Um, o Nos) e so lida. Nenhum provedor. Nenhum dado observado.
set -e
cd "/c/IALD/Central de Patentes/work/bancada_vinculo_12out"
PY=python
echo "== run 1 $(date +%T)"
$PY -B -X utf8 sincronizar_bancada.py --bancada sandbox/bancada_copia --versao v391 --saida sandbox/saida_1_pre_selo_v391 --bateria BATERIA_VINCULO.json \
  --modo ensaio --fase pre_selo --evento "SANDBOX:ensaio pre-selo v391 (ja sincronizada)" > sandbox/run1_stdout.txt 2>&1 || echo "run1 rc=$?" >> sandbox/run1_stdout.txt
tail -1 sandbox/run1_stdout.txt | cut -c1-200
R1=$(ls sandbox/saida_1_pre_selo_v391/RECIBO_SINCRONIZACAO_*.json 2>/dev/null | tail -1)
[ -n "$R1" ] || { echo "run 1 sem recibo: parada"; exit 1; }
echo "== controles negativos $(date +%T)"
$PY -B -X utf8 controles_negativos.py > sandbox/controles_stdout.txt 2>&1 || echo "controles rc=$?" >> sandbox/controles_stdout.txt
tail -8 sandbox/controles_stdout.txt
echo "== run 2 $(date +%T)"
$PY -B -X utf8 sincronizar_bancada.py --bancada sandbox/bancada_copia --versao v392 --nos sandbox/nos_sintetico --sandbox \
  --saida sandbox/saida_2_pos_selo_v392_sintetico --bateria BATERIA_VINCULO.json --modo aplicar --fase pos_selo --recibo-pre-selo "$R1" \
  --evento "SANDBOX:ensaio do elo B3 sobre a COPIA com Nos sintetico v392 (12/10)" > sandbox/run2_stdout.txt 2>&1 || echo "run2 rc=$?" >> sandbox/run2_stdout.txt
tail -1 sandbox/run2_stdout.txt | cut -c1-200
echo "== fim $(date +%T)"
