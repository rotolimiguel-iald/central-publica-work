# -*- coding: utf-8 -*-
"""_adapt_harness_fechar_out_v407.py -- acrescenta ao harness_fechar_sandbox_v407.py a opcao `--out <nome>` (a pasta de saida em C:\\t\\h407; padrao harness_saida_v407), como o harness_textos_ensaio_v407.py ja' tem, para duas rodadas simultaneas nao se pisarem
(achado de 03/11: duas rodadas do harness dos textos na mesma pasta apagaram o nos_emulado uma da outra)."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import adaptar_pos_rito_v407 as M

NOME = "harness_fechar_sandbox_v407.py"
t, crlf, raw = M.le(NOME)
velho = 'OUT = os.path.join("C:" + os.sep, "t", "h407", "harness_saida_v407"); SB = os.path.join(OUT, "fechar_sandbox")'
novo = 'OUT = os.path.join("C:" + os.sep, "t", "h407", (sys.argv[sys.argv.index("--out") + 1] if "--out" in sys.argv else "harness_saida_v407")); SB = os.path.join(OUT, "fechar_sandbox")   # --out <nome>: pasta propria da rodada (duas rodadas simultaneas na mesma pasta se pisam)'
if velho not in t:
    print("JA' FEITO ou texto diferente"); sys.exit(0)
t = M.sub(t, velho, novo)
M.grava(NOME, t, crlf, raw)
