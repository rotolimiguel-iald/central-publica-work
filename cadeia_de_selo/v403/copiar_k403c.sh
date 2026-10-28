#!/bin/sh
# v403 (27/10/2026): o sandbox do kernel da v403 = COPIA de C:\t\k402c\final (o kernel do Nos v402 SELADO, compilado: TGLExt.lean
# 065a0206da7a89f3 = Nos; as tres pedras PonteDaEscalaDual/QuedaSemGeometria/EsperancaCondicional com .olean). Depois entram as
# pedras candidatas da v403 (Caminho, Vida, VerdadeAdendo — os nomes do operador, 27/10, verbatins ef3ca5eb1edbdddf/b34bd70fa8cfb0b2)
# e um `lake build` INCREMENTAL. Molde: copiar_k402c.sh. robocopy sem /PURGE (nunca apaga), sem juncoes (/XJ), sem rascunhos
# (probe) e sem .bak_. A origem so' e' LIDA. Reexecutavel (o robocopy so' copia o que difere).
# uso: sh ./copiar_k403c.sh   (escreve o log em C:\t\k403c\robocopy_final.log; sai com rc 0 se o robocopy devolveu < 8)
mkdir -p /c/t/k403c || exit 9
MSYS_NO_PATHCONV=1 robocopy "C:\t\k402c\final" "C:\t\k403c\final" /E /COPY:DAT /DCOPY:DAT /MT:32 /R:1 /W:1 /NFL /NDL /NP /XJ /XD probe /XF "*.bak_*" /LOG:"C:\t\k403c\robocopy_final.log" > /dev/null
rc1=$?
echo "robocopy final rc=$rc1"
[ $rc1 -lt 8 ] || exit 8
echo "OK $(date '+%Y-%m-%d %H:%M:%S')" > /c/t/k403c/robocopy_done.txt
echo "OK"
