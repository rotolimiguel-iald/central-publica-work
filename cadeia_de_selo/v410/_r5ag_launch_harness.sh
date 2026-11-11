#!/bin/sh
# _r5ag_launch_harness.sh -- R5, agente de adaptacao: roda os dois harnesses do pos-rito sobre o candidato corrente, em paralelo e em segundo plano, cada um com a SUA pasta de saida sob C:\t\h410 (--out; a pasta padrao e' compartilhada entre os dois);
# as saidas vao a harness_*_out_r5ag.txt com RC_HARNESS_*= no fim.
V="/c/IALD/Central de Patentes/work/cadeia_de_selo/v410"
cd "$V" || exit 9
( python -B -X utf8 pos_rito/harness_textos_ensaio_v410.py --out harness_saida_v410_r5ag_textos > harness_textos_out_r5ag.txt 2>&1; echo RC_HARNESS_TEXTOS=$? >> harness_textos_out_r5ag.txt ) &
( python -B -X utf8 pos_rito/harness_fechar_sandbox_v410.py --nao-exigir-refazer --out harness_saida_v410_r5ag_fechar > harness_fechar_out_r5ag.txt 2>&1; echo RC_HARNESS_FECHAR=$? >> harness_fechar_out_r5ag.txt ) &
wait
