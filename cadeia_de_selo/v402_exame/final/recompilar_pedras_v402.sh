#!/bin/sh
# Recompila as tres pedras do FONTE no sandbox k402c (lake env lean sem -o: nao grava .olean). So le o kernel.
E="/c/IALD/Central de Patentes/work/cadeia_de_selo/v402_exame/final"
cd /c/t/k402c/final || exit 9
for X in PonteDaEscalaDual QuedaSemGeometria EsperancaCondicional; do
  t0=$(date +%s)
  lake env lean "TGLExt/$X.lean" > "$E/recompilacao_$X.log" 2>&1; rc=$?
  t1=$(date +%s)
  echo "$X rc=$rc s=$((t1-t0))" >> "$E/recompilacao_marcas.txt"
done
echo FIM >> "$E/recompilacao_marcas.txt"
