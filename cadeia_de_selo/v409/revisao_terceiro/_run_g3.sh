#!/bin/bash
cd "/c/IALD/Central de Patentes/work/cadeia_de_selo/v409/revisao_terceiro"
PY="C:/Python314/python.exe"
$PY -X utf8 c_fail_closed.py > c_fail_closed_out.txt 2>&1
$PY -X utf8 h_guardas.py > h_guardas_out.txt 2>&1
$PY -X utf8 t1_fock_open.py > t1_fock_open_out.txt 2>&1
$PY -X utf8 t2_uniforme_open.py > t2_uniforme_open_out.txt 2>&1
touch _g3.done
