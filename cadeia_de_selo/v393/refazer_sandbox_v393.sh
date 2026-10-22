#!/bin/sh
# refaz do ZERO o sandbox B do kernel da v393: copia o kernel que o Nos TEM (v392 instalada), aplica as 3 pedras, a raiz e o Audit (kernel/AUDIT_BLOCO_v393.txt, gerado por gerar_audit_v393.py a partir da COB),
# um unico lake build + Audit, e o pos-build. Se a enumeracao precisar ser refeita (pedra mudou): preparar_kernel_v393.py explorar + kernel/explorar_v393.sh + gerar_audit_v393.py ANTES do `final`.
V="/c/IALD/Central de Patentes/work/cadeia_de_selo/v393"
mkdir -p /c/t/k393 || exit 9
MSYS_NO_PATHCONV=1 robocopy "C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel" "C:\t\k393\final" /E /COPY:DAT /DCOPY:DAT /MT:32 /R:1 /W:1 /NFL /NDL /NP /XF "TGLExt.lean.bak_*" /LOG:"C:\t\k393\robocopy_final.log" > /dev/null
[ $? -lt 8 ] || exit 8
cd "$V" && python -I -B -X utf8 preparar_kernel_v393.py final && sh ./construir_kernel_v393.sh && python -I -B -X utf8 pos_build_kernel_v393.py
