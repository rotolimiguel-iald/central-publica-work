#!/bin/bash
cd /c/t/k409c/final
export PATH="$PATH:/c/Users/rotol/.elan/bin"
RV="/c/IALD/Central de Patentes/work/cadeia_de_selo/v409/revisao_terceiro"
for N in ParNaFaceDeFock TraducaoTuring; do
  cp "$RV/_fontes_compilar/zz_rev_$N.lean" "zz_rev_$N.lean"
  s=$(date +%s)
  lake env lean "zz_rev_$N.lean" > "$RV/_fontes_compilar/out_$N.txt" 2>&1
  echo "rc=$?" >> "$RV/_fontes_compilar/out_$N.txt"
  e=$(date +%s)
  echo "$((e-s)) s" > "$RV/_fontes_compilar/tempo_$N.txt"
  rm -f "zz_rev_$N.lean"
done
touch "$RV/_lean2.done"
