#!/bin/sh
# v400 (24/10/2026): o sandbox do kernel da v400 = COPIA de C:\t\k399c (o kernel da v399, compilado) -- so' para o Audit e para as conferencias de bytes; NENHUM modulo novo, a raiz TGLExt.lean e o TGL/Audit.lean ficam os da v399.
# robocopy sem /PURGE (nunca apaga), sem juncoes (/XJ), sem rascunhos (probe) e sem .bak_. A origem so' e' LIDA. Reexecutavel (o robocopy so' copia o que difere).
# uso: sh ./copiar_k400c.sh   (escreve o log em C:\t\k400c\robocopy_*.log; sai com rc 0 se o robocopy devolveu < 8)
mkdir -p /c/t/k400c || exit 9
MSYS_NO_PATHCONV=1 robocopy "C:\t\k399c\final" "C:\t\k400c\final" /E /COPY:DAT /DCOPY:DAT /MT:32 /R:1 /W:1 /NFL /NDL /NP /XJ /XD probe /XF "*.bak_*" /LOG:"C:\t\k400c\robocopy_final.log" > /dev/null
rc1=$?
echo "robocopy final rc=$rc1"
[ $rc1 -lt 8 ] || exit 8
MSYS_NO_PATHCONV=1 robocopy "C:\t\k399c\arvore" "C:\t\k400c\arvore" /E /COPY:DAT /DCOPY:DAT /MT:32 /R:1 /W:1 /NFL /NDL /NP /XJ /XD probe /XF "*.bak_*" /LOG:"C:\t\k400c\robocopy_arvore.log" > /dev/null
rc2=$?
echo "robocopy arvore rc=$rc2"
[ $rc2 -lt 8 ] || exit 8
echo "OK"
