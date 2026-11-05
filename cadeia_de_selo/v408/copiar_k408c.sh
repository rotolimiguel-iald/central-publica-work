#!/bin/sh
# v408 (04/11/2026): o sandbox do kernel da v408 = COPIA do kernel do NOS v407 SELADO (C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel: as fontes da v407 e o .lake/build COMPILADO pelo rito de 04/11,
# com os .olean dos 9 modulos da v407; a raiz TGLExt.lean do Nos = a embutida na v407). O bundle de 4 modulos da v408 NAO entra aqui: e' passo posterior (preparar_bundle_v408_04nov.py).
# C:\t\k407c NAO e' a origem nem o alvo da juncao (a receita manda partir de um sandbox novo); a origem e' o Nos, SO' LIDA. Molde: copiar_k407c.sh.
# robocopy sem /PURGE (nunca apaga), sem juncoes (/XJ: a juncao .lake/packages do Nos NAO e' copiada), sem rascunhos (probe) e sem .bak_. Depois do robocopy, cria a JUNCAO C:\t\k408c\final\.lake\packages -> C:\t\k404c\final\.lake\packages
# (a copia da mathlib compilada que os sandboxes anteriores usaram, so' leitura; e' a mesma para a qual a juncao do k407c aponta). Reexecutavel (o robocopy so' copia o que difere; a juncao so' e' criada se nao existir).
# uso: sh ./copiar_k408c.sh   (escreve o log em C:\t\k408c\robocopy_final.log; sai com rc 0 se o robocopy devolveu < 8 e a juncao existe)
mkdir -p /c/t/k408c || exit 9
MSYS_NO_PATHCONV=1 robocopy "C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel" "C:\t\k408c\final" /E /COPY:DAT /DCOPY:DAT /MT:32 /R:1 /W:1 /NFL /NDL /NP /XJ /XD probe /XF "*.bak_*" "*.k403_antes" "*.k404_antes" /LOG:"C:\t\k408c\robocopy_final.log" > /dev/null
rc1=$?
echo "robocopy final rc=$rc1"
[ $rc1 -lt 8 ] || exit 8
if [ ! -e /c/t/k408c/final/.lake/packages ]; then
  # (a juncao pelo PowerShell: `cmd //c mklink` nao funciona com MSYS_NO_PATHCONV=1, porque o `//c` deixa de virar `/c`)
  powershell.exe -NoProfile -NonInteractive -Command "New-Item -ItemType Junction -Path 'C:\t\k408c\final\.lake\packages' -Target 'C:\t\k404c\final\.lake\packages' | Out-Null; exit 0" || exit 7
fi
[ -e /c/t/k408c/final/.lake/packages/mathlib/.lake/build/lib/lean/Mathlib.olean ] || { echo "a juncao .lake/packages nao alcanca a mathlib compilada"; exit 7; }
echo "OK $(date '+%Y-%m-%d %H:%M:%S')" > /c/t/k408c/robocopy_done.txt
echo "OK"
