#!/bin/sh
# _r5ag_launch_ensaio.sh -- R5, agente de adaptacao: lanca o ensaio a seco e o pre-teste da parte 2 sobre o candidato corrente, em paralelo, com os mesmos comandos do refazer_candidato_v410.sh (passo 3) e do _preteste_ensaio_parte2_v410.py; marca RC_ENSAIO= e RC_PRETESTE= no fim das saidas.
cd "/c/IALD/Central de Patentes/work/cadeia_de_selo/v410" || exit 9
( python -B -X utf8 ensaio_a_seco_v410.py um_v410_candidato.py v410 > ensaio_out.txt 2>&1; echo RC_ENSAIO=$? >> ensaio_out.txt ) &
( python -B -X utf8 _preteste_ensaio_parte2_v410.py > preteste_out_v410.txt 2>&1; echo RC_PRETESTE=$? >> preteste_out_v410.txt ) &
wait
