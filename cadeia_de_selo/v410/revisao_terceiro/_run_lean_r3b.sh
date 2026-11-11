#!/bin/bash
cd "/c/t/k410c/final"
S=$(date +%s)
export PATH="/c/Users/rotol/.elan/bin:$PATH"
lake env lean "C:/IALD/Central de Patentes/work/cadeia_de_selo/v410/revisao_terceiro/axiomas_terceiro_r3b.lean" > "C:/IALD/Central de Patentes/work/cadeia_de_selo/v410/revisao_terceiro/axiomas_terceiro_r3b_out.txt" 2>&1
echo "rc=$?" >> "C:/IALD/Central de Patentes/work/cadeia_de_selo/v410/revisao_terceiro/axiomas_terceiro_r3b_out.txt"
E=$(date +%s)
echo "$((E-S)) s" > "C:/IALD/Central de Patentes/work/cadeia_de_selo/v410/revisao_terceiro/axiomas_terceiro_r3b_time.txt"
touch "C:/IALD/Central de Patentes/work/cadeia_de_selo/v410/revisao_terceiro/_lean_r3b.done"
