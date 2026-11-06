#!/bin/bash
cd "/c/IALD/Central de Patentes/work/cadeia_de_selo/v409/revisao_terceiro"
PY="C:/Python314/python.exe"
$PY -X utf8 a_intocados.py > a_intocados_out.txt 2>&1
$PY -X utf8 a_intocados_b.py > a_intocados_b_out.txt 2>&1
$PY -X utf8 a_intocados_c.py > a_intocados_c_out.txt 2>&1
$PY -X utf8 a2_mudados.py > a2_mudados_out.txt 2>&1
touch _g1.done
