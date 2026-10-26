#!/bin/sh
# v401 (25/10/2026): o sandbox do kernel da v401 = COPIA de C:\t\k401\final (o kernel da v400 compilado + a pedra FalsidadeDaInercia compilada ISOLADA + os imports de teste); depois o preparar_kernel_v401.py `gerar` REGERA a raiz TGLExt.lean e o TGL/Audit.lean (v400 embutida + o import da pedra).
# robocopy sem /PURGE (nunca apaga), sem juncoes (/XJ), sem rascunhos (probe) e sem .bak_. A origem so' e' LIDA. Reexecutavel (o robocopy so' copia o que difere). O comando exato que a preparacao rodou esta em preparar_kernel_v401.py (modo `copiar`).
# uso: sh ./copiar_k401c.sh   (escreve o log em C:\t\k401c\robocopy_*.log; sai com rc 0 se o robocopy devolveu < 8)
mkdir -p /c/t/k401c || exit 9
MSYS_NO_PATHCONV=1 robocopy "C:\t\k401\final" "C:\t\k401c\final" /E /COPY:DAT /DCOPY:DAT /MT:32 /R:1 /W:1 /NFL /NDL /NP /XJ /XD probe /XF "*.bak_*" /LOG:"C:\t\k401c\robocopy_final.log" > /dev/null
rc1=$?
echo "robocopy final rc=$rc1"
[ $rc1 -lt 8 ] || exit 8
echo "OK"
