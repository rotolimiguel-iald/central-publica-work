#!/bin/bash
cd /c/t/k409c/final
s=$(date +%s)
export PATH="$PATH:/c/Users/rotol/.elan/bin"
cp "/c/IALD/Central de Patentes/work/cadeia_de_selo/v409/revisao_terceiro/axiomas_terceiro.lean" axiomas_terceiro.lean
lake env lean axiomas_terceiro.lean > "/c/IALD/Central de Patentes/work/cadeia_de_selo/v409/revisao_terceiro/axiomas_terceiro_out.txt" 2>&1
echo "rc=$?" >> "/c/IALD/Central de Patentes/work/cadeia_de_selo/v409/revisao_terceiro/axiomas_terceiro_out.txt"
rm -f axiomas_terceiro.lean
e=$(date +%s)
echo "$((e-s)) s" > "/c/IALD/Central de Patentes/work/cadeia_de_selo/v409/revisao_terceiro/axiomas_terceiro_time.txt"
touch "/c/IALD/Central de Patentes/work/cadeia_de_selo/v409/revisao_terceiro/_lean.done"
