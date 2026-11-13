#!/bin/sh
# v411 (12/11/2026, claude-construtor-v411): o sandbox do kernel da v411 = COPIA do sandbox C:\t\k410c\final (DESENHO_v411 secao 1: «Sandbox C:\t\k411c\final copiado de C:\t\k410c\final
# (robocopy SEM /PURGE); nenhum bundle»). As fontes .lean de k410c\final foram conferidas por sha256 contra o kernel do NOS v410 SELADO antes da copia (conferir_fontes_k410c_vs_nos_v411.py ->
# CONFERENCIA_FONTES_K410C_v411.json: 1764 fontes comuns, todas iguais, nada so' num dos lados). A v411 NAO tem modulo novo: nada se acrescenta ao sandbox. A origem k410c\final e' SO' LIDA.
# Molde: copiar_k410c.sh (so' os rotulos e a origem sobem). robocopy sem /PURGE (nunca apaga), sem juncoes (/XJ), sem rascunhos (probe) e sem .bak_. Depois do robocopy, cria a JUNCAO
# C:\t\k411c\final\.lake\packages -> C:\t\k404c\final\.lake\packages (a copia da mathlib compilada que os sandboxes anteriores usaram, so' leitura; a mesma da juncao do k410c).
# Reexecutavel (o robocopy so' copia o que difere; a juncao so' e' criada se nao existir).
# uso: sh ./copiar_k411c.sh   (log em C:\t\k411c\robocopy_final.log; rc 0 se o robocopy devolveu < 8 e a juncao alcanca a mathlib)
mkdir -p /c/t/k411c || exit 9
MSYS_NO_PATHCONV=1 robocopy "C:\t\k410c\final" "C:\t\k411c\final" /E /COPY:DAT /DCOPY:DAT /MT:32 /R:1 /W:1 /NFL /NDL /NP /XJ /XD probe /XF "*.bak_*" "*.k403_antes" "*.k404_antes" /LOG:"C:\t\k411c\robocopy_final.log" > /dev/null
rc1=$?
echo "robocopy final rc=$rc1"
[ $rc1 -lt 8 ] || exit 8
if [ ! -e /c/t/k411c/final/.lake/packages ]; then
  powershell.exe -NoProfile -NonInteractive -Command "New-Item -ItemType Junction -Path 'C:\t\k411c\final\.lake\packages' -Target 'C:\t\k404c\final\.lake\packages' | Out-Null; exit 0" || exit 7
fi
[ -e /c/t/k411c/final/.lake/packages/mathlib/.lake/build/lib/lean/Mathlib.olean ] || { echo "a juncao .lake/packages nao alcanca a mathlib compilada"; exit 7; }
echo "OK $(date '+%Y-%m-%d %H:%M:%S')" > /c/t/k411c/robocopy_done.txt
echo "OK"
