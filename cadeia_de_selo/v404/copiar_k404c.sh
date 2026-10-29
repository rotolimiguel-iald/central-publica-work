#!/bin/sh
# v404 (28/10/2026): o sandbox do kernel da v404 = COPIA de C:\t\k403c\final (o kernel do Nos v403 SELADO, compilado: as tres pedras Caminho/Vida/VerdadeAdendo com .olean;
# a raiz TGLExt.lean do sandbox k403c = a do Nos v403) + as DUAS pedras candidatas da v404 (ProjecaoTransversalDaMeiaNat e Jo8v32, compiladas e provadas por `lake env lean`
# em 28/10/2026 no proprio k403c: work\projecao_transversal_28out\RECIBO_PEDRA_*) e um `lake build` INCREMENTAL. Molde: copiar_k403c.sh. robocopy sem /PURGE (nunca apaga),
# sem juncoes (/XJ), sem rascunhos (probe) e sem .bak_. A origem so' e' LIDA. Reexecutavel (o robocopy so' copia o que difere).
# uso: sh ./copiar_k404c.sh   (escreve o log em C:\t\k404c\robocopy_final.log; sai com rc 0 se o robocopy devolveu < 8)
mkdir -p /c/t/k404c || exit 9
MSYS_NO_PATHCONV=1 robocopy "C:\t\k403c\final" "C:\t\k404c\final" /E /COPY:DAT /DCOPY:DAT /MT:32 /R:1 /W:1 /NFL /NDL /NP /XJ /XD probe /XF "*.bak_*" "*.k403_antes" /LOG:"C:\t\k404c\robocopy_final.log" > /dev/null
rc1=$?
echo "robocopy final rc=$rc1"
[ $rc1 -lt 8 ] || exit 8
echo "OK $(date '+%Y-%m-%d %H:%M:%S')" > /c/t/k404c/robocopy_done.txt
echo "OK"
