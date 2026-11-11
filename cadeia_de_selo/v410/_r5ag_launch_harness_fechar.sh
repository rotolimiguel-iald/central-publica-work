#!/bin/sh
# _r5ag_launch_harness_fechar.sh -- R5, agente de adaptacao: o harness do fechar em sandbox quebrava no import do delta da copia (o runner do ACOM Mirror, sob Central\patents, nao era espelhado; _r5ag_21 corrige o espelho); roda de novo, com a pasta de saida propria.
V="/c/IALD/Central de Patentes/work/cadeia_de_selo/v410"
cd "$V" || exit 9
mv harness_fechar_out_r5ag.txt harness_fechar_out_r5ag_1a_tentativa_rc1.txt
python -B -X utf8 pos_rito/harness_fechar_sandbox_v410.py --nao-exigir-refazer --out harness_saida_v410_r5ag_fechar > harness_fechar_out_r5ag.txt 2>&1; echo RC_HARNESS_FECHAR=$? >> harness_fechar_out_r5ag.txt
