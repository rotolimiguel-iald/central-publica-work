#!/bin/sh
# _r5ag_launch_harness_textos.sh -- R5, agente de adaptacao: o harness de textos recusou (rc 4) a primeira vez porque exige o refazer_out_v410.txt (a regeneracao completa, que o agente NAO roda); o proprio harness traz o modo de ENSAIO --nao-exigir-refazer
# (a saida DIZ que a regeneracao nao foi comprovada); roda de novo com ele, com a pasta de saida propria.
V="/c/IALD/Central de Patentes/work/cadeia_de_selo/v410"
cd "$V" || exit 9
mv harness_textos_out_r5ag.txt harness_textos_out_r5ag_1a_tentativa_rc4.txt
python -B -X utf8 pos_rito/harness_textos_ensaio_v410.py --nao-exigir-refazer --out harness_saida_v410_r5ag_textos > harness_textos_out_r5ag.txt 2>&1; echo RC_HARNESS_TEXTOS=$? >> harness_textos_out_r5ag.txt
