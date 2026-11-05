#!/bin/bash
cd /c/t/k408c/final
s=$(date +%s)
export PATH="$PATH:/c/Users/rotol/.elan/bin"
lake env lean axiomas_terceiro.lean > "/c/IALD/Central de Patentes/work/cadeia_de_selo/v408/revisao_terceiro/axiomas_terceiro_out.txt" 2>&1
echo "rc=$?" >> "/c/IALD/Central de Patentes/work/cadeia_de_selo/v408/revisao_terceiro/axiomas_terceiro_out.txt"
e=$(date +%s)
echo "$((e-s)) s" > "/c/IALD/Central de Patentes/work/cadeia_de_selo/v408/revisao_terceiro/axiomas_terceiro_time.txt"
