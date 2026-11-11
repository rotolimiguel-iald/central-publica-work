#!/bin/sh
# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] molde: copiar_k409c.sh (subida de rotulo em bump/copiar_k410c.sh.diff); so' os comentarios e o /XF do rascunho da gerencia mudaram.
# v410 (06/11/2026, claude-construtor-v410): o sandbox do kernel da v410 = COPIA do sandbox C:\t\k409c\final (ordem da gerencia c1: «a partir do C:\t\k409c\final, ja construido com a v409»). As fontes .lean de k409c\final foram
# conferidas por sha256 contra o kernel do NOS v409 SELADO antes da copia (conferir_fontes_k409c_vs_nos_v410.py -> CONFERENCIA_FONTES_K409C_v410.json: 1762 fontes comuns, todas iguais; so' no sandbox o rascunho IALD2_ins.lean da gerencia,
# que NAO e' copiado); o .lake/build de k409c\final tem os .olean dos 2 modulos da v409. A raiz TGLExt.lean = a embutida na v409.
# O bundle da v410 (IALD2) NAO entra aqui: e' passo posterior (preparar_bundle_v410_06nov.py, que so' roda quando a gerencia mandar o insumo final). A origem k409c\final e' SO' LIDA. Molde: copiar_k409c.sh.
# robocopy sem /PURGE (nunca apaga), sem juncoes (/XJ: a juncao .lake/packages de k409c NAO e' copiada), sem rascunhos (probe, IALD2_ins.lean) e sem .bak_. Depois do robocopy, cria a JUNCAO C:\t\k410c\final\.lake\packages -> C:\t\k404c\final\.lake\packages
# (a copia da mathlib compilada que os sandboxes anteriores usaram, so' leitura; e' a mesma para a qual a juncao do k409c aponta). Reexecutavel (o robocopy so' copia o que difere; a juncao so' e' criada se nao existir).
# uso: sh ./copiar_k410c.sh   (escreve o log em C:\t\k410c\robocopy_final.log; sai com rc 0 se o robocopy devolveu < 8 e a juncao existe)
mkdir -p /c/t/k410c || exit 9
MSYS_NO_PATHCONV=1 robocopy "C:\t\k409c\final" "C:\t\k410c\final" /E /COPY:DAT /DCOPY:DAT /MT:32 /R:1 /W:1 /NFL /NDL /NP /XJ /XD probe /XF "*.bak_*" "*.k403_antes" "*.k404_antes" "IALD2_ins.lean" /LOG:"C:\t\k410c\robocopy_final.log" > /dev/null
rc1=$?
echo "robocopy final rc=$rc1"
[ $rc1 -lt 8 ] || exit 8
if [ ! -e /c/t/k410c/final/.lake/packages ]; then
  # (a juncao pelo PowerShell: `cmd //c mklink` nao funciona com MSYS_NO_PATHCONV=1, porque o `//c` deixa de virar `/c`)
  powershell.exe -NoProfile -NonInteractive -Command "New-Item -ItemType Junction -Path 'C:\t\k410c\final\.lake\packages' -Target 'C:\t\k404c\final\.lake\packages' | Out-Null; exit 0" || exit 7
fi
[ -e /c/t/k410c/final/.lake/packages/mathlib/.lake/build/lib/lean/Mathlib.olean ] || { echo "a juncao .lake/packages nao alcanca a mathlib compilada"; exit 7; }
echo "OK $(date '+%Y-%m-%d %H:%M:%S')" > /c/t/k410c/robocopy_done.txt
echo "OK"
