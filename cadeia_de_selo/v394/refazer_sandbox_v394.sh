#!/bin/sh
# refaz do ZERO o sandbox B do kernel da v394 (C:/t/k394d/final): copia o kernel que o Nos TEM (a v393 instalada), acrescenta os 189 modulos do Codex (TimeGraviton*, RuleQuadraticResidual, F1Fecho394/*) e a pedra do criterio binario de parada e GERA a raiz e o Audit
# (preparar_kernel_v394.py gerar: conferido byte a byte contra a arvore candidate_r8 do Codex), UM unico lake build + Audit (construir_kernel_v394.sh) e o pos-build (pos_build_kernel_v394.py). USAR ANTES de instalar_v394.py: o `gerar` le o um.py do Nos como a base v393.
V="/c/IALD/Central de Patentes/work/cadeia_de_selo/v394"
mkdir -p /c/t/k394d || exit 9
MSYS_NO_PATHCONV=1 robocopy "C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel" "C:\t\k394d\final" /E /COPY:DAT /DCOPY:DAT /MT:32 /R:1 /W:1 /NFL /NDL /NP /XF "TGLExt.lean.bak_*" /LOG:"C:\t\k394d\robocopy_final.log" > /dev/null
[ $? -lt 8 ] || exit 8
[ -f "$V/pos_build_kernel_v394.py" ] || { echo "falta pos_build_kernel_v394.py em $V (gerado a parte) -- NAO RODO"; exit 9; }
[ -f "$V/preparar_kernel_v394.py" ] && [ -f "$V/construir_kernel_v394.sh" ] || { echo "falta preparar_kernel_v394.py ou construir_kernel_v394.sh -- NAO RODO"; exit 9; }
cd "$V" && python -I -B -X utf8 preparar_kernel_v394.py gerar && sh ./construir_kernel_v394.sh && python -I -B -X utf8 pos_build_kernel_v394.py
