#!/bin/sh
# v409 (05/11/2026, claude-construtor-v409): o sandbox do kernel da v409 = COPIA do sandbox C:\t\k408c\final (ordem da gerencia c1: «a partir do C:\t\k408c\final, ja construido com a v408»). As fontes .lean de k408c\final foram
# conferidas por sha256 contra o kernel do NOS v408 SELADO (1760 arquivos fonte, todos iguais, 05/11/2026 ~12h50); o .lake/build de k408c\final tem os .olean dos 4 modulos da v408. A raiz TGLExt.lean = a embutida na v408.
# O bundle de 1 modulo da v409 (TraducaoTuring) NAO entra aqui: e' passo posterior (preparar_bundle_v409_05nov.py). A origem k408c\final e' SO' LIDA. Molde: copiar_k408c.sh (que copiava do Nos).
# robocopy sem /PURGE (nunca apaga), sem juncoes (/XJ: a juncao .lake/packages de k408c NAO e' copiada), sem rascunhos (probe) e sem .bak_. Depois do robocopy, cria a JUNCAO C:\t\k409c\final\.lake\packages -> C:\t\k404c\final\.lake\packages
# (a copia da mathlib compilada que os sandboxes anteriores usaram, so' leitura; e' a mesma para a qual a juncao do k408c aponta). Reexecutavel (o robocopy so' copia o que difere; a juncao so' e' criada se nao existir).
# uso: sh ./copiar_k409c.sh   (escreve o log em C:\t\k409c\robocopy_final.log; sai com rc 0 se o robocopy devolveu < 8 e a juncao existe)
mkdir -p /c/t/k409c || exit 9
MSYS_NO_PATHCONV=1 robocopy "C:\t\k408c\final" "C:\t\k409c\final" /E /COPY:DAT /DCOPY:DAT /MT:32 /R:1 /W:1 /NFL /NDL /NP /XJ /XD probe /XF "*.bak_*" "*.k403_antes" "*.k404_antes" /LOG:"C:\t\k409c\robocopy_final.log" > /dev/null
rc1=$?
echo "robocopy final rc=$rc1"
[ $rc1 -lt 8 ] || exit 8
if [ ! -e /c/t/k409c/final/.lake/packages ]; then
  # (a juncao pelo PowerShell: `cmd //c mklink` nao funciona com MSYS_NO_PATHCONV=1, porque o `//c` deixa de virar `/c`)
  powershell.exe -NoProfile -NonInteractive -Command "New-Item -ItemType Junction -Path 'C:\t\k409c\final\.lake\packages' -Target 'C:\t\k404c\final\.lake\packages' | Out-Null; exit 0" || exit 7
fi
[ -e /c/t/k409c/final/.lake/packages/mathlib/.lake/build/lib/lean/Mathlib.olean ] || { echo "a juncao .lake/packages nao alcanca a mathlib compilada"; exit 7; }
echo "OK $(date '+%Y-%m-%d %H:%M:%S')" > /c/t/k409c/robocopy_done.txt
echo "OK"
