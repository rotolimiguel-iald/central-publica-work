#!/bin/sh
# v402 (26/10/2026): o sandbox do kernel da v402 = COPIA de C:\t\k401c\final (o kernel do Nos v401 SELADO, compilado: a v401 embutida + a pedra FalsidadeDaInercia); depois o preparar_kernel_v402.py `gerar` copia as TRES pedras novas e REGERA a raiz TGLExt.lean e o TGL/Audit.lean (v401 embutida + os tres imports).
# robocopy sem /PURGE (nunca apaga), sem juncoes (/XJ), sem rascunhos (probe) e sem .bak_. A origem so' e' LIDA. Reexecutavel (o robocopy so' copia o que difere). O comando exato que a preparacao rodou esta em preparar_kernel_v402.py (modo `copiar`).
# uso: sh ./copiar_k402c.sh   (escreve o log em C:\t\k402c\robocopy_*.log; sai com rc 0 se o robocopy devolveu < 8)
mkdir -p /c/t/k402c || exit 9
MSYS_NO_PATHCONV=1 robocopy "C:\t\k401c\final" "C:\t\k402c\final" /E /COPY:DAT /DCOPY:DAT /MT:32 /R:1 /W:1 /NFL /NDL /NP /XJ /XD probe /XF "*.bak_*" /LOG:"C:\t\k402c\robocopy_final.log" > /dev/null
rc1=$?
echo "robocopy final rc=$rc1"
[ $rc1 -lt 8 ] || exit 8
echo "OK"
