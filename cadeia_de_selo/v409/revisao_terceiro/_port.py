# -*- coding: utf-8 -*-
"""Revisor v409: porta os scripts da revisao da v408 (molde) para a v409 por tabela de trocas; depois cada um e' ajustado a mao. So escreve nesta pasta."""
import os, sys
sys.stdout.reconfigure(encoding="utf-8")
M = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v408/revisao_terceiro/"
D = "C:/IALD/Central de Patentes/work/cadeia_de_selo/v409/revisao_terceiro/"
TROCAS = [("cadeia_de_selo/v408/", "cadeia_de_selo/v409/"), ("k408c", "k409c"), ("h408", "h409"),
          ("v408", "v409"), ("V408", "V409"), ("v407", "v408"), ("V407", "V408"), ("v406", "v407"), ("V406", "V407")]
LISTA = ["a_intocados.py", "a_intocados_b.py", "a_intocados_c.py", "a2_mudados.py", "d_kernel.py", "f_hashes.py", "c_fail_closed.py", "c2_mecanica_direta.py", "e_citacoes.py", "e2_citacoes_rendidos.py",
         "h_guardas.py", "k_funcoes_vivas.py", "l_orquestrador.py", "m_flags_audit.py", "n_hashes_digitados.py", "n2_hashes_docs.py", "n2_falas_mistas.py"]
for f in LISTA:
    t = open(M + f, "rb").read().decode("utf-8")
    for a, b in TROCAS: t = t.replace(a, b)
    open(D + f, "w", encoding="utf-8", newline="\n").write(t)
    print("portado", f, len(t))
