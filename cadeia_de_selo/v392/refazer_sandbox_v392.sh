#!/bin/sh
# refaz do ZERO o sandbox do kernel da v392 (apos a preparacao ter apagado C:\t\k392): copia a base v391, aplica as pedras de STONES (14 na rodada 2) e a raiz, e para o Audit final usa kernel/AUDIT_BLOCO_v392.txt
# (gerado por gerar_audit_v392.py a partir da enumeracao COB). Depois: construir_kernel_v392.sh, pos_build_kernel_v392.py, gerar_candidato_v392.py.
# Se a enumeracao precisar ser refeita (pedra mudou): preparar_kernel_v392.py explorar + kernel/explorar_v392.sh + gerar_audit_v392.py ANTES do `final`.
V="/c/IALD/Central de Patentes/work/cadeia_de_selo/v392"
mkdir -p /c/t/k392 || exit 9
MSYS_NO_PATHCONV=1 robocopy "C:\IALD\Central de Patentes\work\v388_kernel\kernel_src" "C:\t\k392\final" /E /COPY:DAT /DCOPY:DAT /MT:32 /R:1 /W:1 /NFL /NDL /NP /XF "TGLExt.lean.bak_*" /LOG:"C:\t\k392\robocopy_final.log" > /dev/null
[ $? -lt 8 ] || exit 8
cd "$V" && python -I -B -X utf8 preparar_kernel_v392.py final && sh ./construir_kernel_v392.sh && python -I -B -X utf8 pos_build_kernel_v392.py
