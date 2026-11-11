#!/bin/bash
cd "/c/t/k410c/final"
S=$(date +%s)
export PATH="/c/Users/rotol/.elan/bin:$PATH"
lake env lean "C:/IALD/Central de Patentes/work/cadeia_de_selo/v410/revisao_terceiro/axiomas_terceiro_v410.lean" > "C:/IALD/Central de Patentes/work/cadeia_de_selo/v410/revisao_terceiro/axiomas_terceiro_v410_out.txt" 2>&1
echo "rc=$?" >> "C:/IALD/Central de Patentes/work/cadeia_de_selo/v410/revisao_terceiro/axiomas_terceiro_v410_out.txt"
E=$(date +%s)
echo "$((E-S)) s" > "C:/IALD/Central de Patentes/work/cadeia_de_selo/v410/revisao_terceiro/axiomas_terceiro_v410_time.txt"
touch "C:/IALD/Central de Patentes/work/cadeia_de_selo/v410/revisao_terceiro/_lean.done"
