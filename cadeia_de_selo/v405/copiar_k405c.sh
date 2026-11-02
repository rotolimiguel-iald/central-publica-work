#!/bin/sh
# v405 (01/11/2026): o sandbox do kernel da v405 = COPIA do kernel do NOS v404 SELADO (C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel: as fontes da v404 e o .lake/build COMPILADO pelo rito de 28/10,
# com os .olean das 2 pedras da v404; a raiz TGLExt.lean do Nos = a embutida na v404) + as OITO pedras candidatas da v405 (compiladas e provadas por `lake env lean`/`lake build` em 30/10 a 01/11 no sandbox k404c:
# work\experimento_espelho_30out, cadeia_de_selo405, observador_terminal_31out, e0_cadeia_31out\RECIBO_*) e um `lake build` INCREMENTAL. C:\t\k404c NAO e' a origem (tem .olean soltos das pedras candidatas,
# sob os nomes provisorios e os novos); a origem e' o Nos, SO' LIDA. Molde: copiar_k404c.sh. robocopy sem /PURGE (nunca apaga), sem juncoes (/XJ: a juncao .lake/packages do Nos NAO e' copiada), sem rascunhos
# (probe) e sem .bak_. Depois do robocopy, cria a JUNCAO C:\t\k405c\final\.lake\packages -> C:\t\k404c\final\.lake\packages (a copia da mathlib compilada que os sandboxes anteriores usaram; conferida
# byte a byte igual a' do Nos em 01/11/2026: PosDef.olean, Trigonometric/Basic.olean, Mathlib.olean, Batteries.olean e o lake-manifest; so' leitura). Reexecutavel (o robocopy so' copia o que difere;
# a juncao so' e' criada se nao existir).
# uso: sh ./copiar_k405c.sh   (escreve o log em C:\t\k405c\robocopy_final.log; sai com rc 0 se o robocopy devolveu < 8 e a juncao existe)
mkdir -p /c/t/k405c || exit 9
MSYS_NO_PATHCONV=1 robocopy "C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel" "C:\t\k405c\final" /E /COPY:DAT /DCOPY:DAT /MT:32 /R:1 /W:1 /NFL /NDL /NP /XJ /XD probe /XF "*.bak_*" "*.k403_antes" "*.k404_antes" /LOG:"C:\t\k405c\robocopy_final.log" > /dev/null
rc1=$?
echo "robocopy final rc=$rc1"
[ $rc1 -lt 8 ] || exit 8
if [ ! -e /c/t/k405c/final/.lake/packages ]; then
  # (a juncao pelo PowerShell: `cmd //c mklink` nao funciona com MSYS_NO_PATHCONV=1, porque o `//c` deixa de virar `/c`)
  powershell.exe -NoProfile -NonInteractive -Command "New-Item -ItemType Junction -Path 'C:\t\k405c\final\.lake\packages' -Target 'C:\t\k404c\final\.lake\packages' | Out-Null; exit 0" || exit 7
fi
[ -e /c/t/k405c/final/.lake/packages/mathlib/.lake/build/lib/lean/Mathlib.olean ] || { echo "a juncao .lake/packages nao alcanca a mathlib compilada"; exit 7; }
echo "OK $(date '+%Y-%m-%d %H:%M:%S')" > /c/t/k405c/robocopy_done.txt
echo "OK"
