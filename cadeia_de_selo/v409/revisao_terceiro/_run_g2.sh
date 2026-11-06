#!/bin/bash
cd "/c/IALD/Central de Patentes/work/cadeia_de_selo/v409/revisao_terceiro"
PY="C:/Python314/python.exe"
$PY -X utf8 d_kernel.py > d_kernel_out.txt 2>&1
$PY -X utf8 f_hashes.py > f_hashes_out.txt 2>&1
$PY -X utf8 e_citacoes.py > e_citacoes_out.txt 2>&1
$PY -X utf8 l_orquestrador.py > l_orquestrador_out.txt 2>&1
$PY -X utf8 m_flags_audit.py > m_flags_out.txt 2>&1
$PY -X utf8 c2_mecanica_direta.py > c2_mecanica_direta_out.txt 2>&1
$PY -X utf8 k_funcoes_vivas.py > k_funcoes_vivas_out.txt 2>&1
touch _g2.done
