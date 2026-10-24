#!/bin/sh
# refaz o sandbox B do kernel da v399 (C:/t/k399c/final) a partir do kernel que o Nos TEM (a v398 instalada: sem a pasta probe\ de rascunhos e sem as pedras compiladas em .lake/build, entao o build COMPILA AS PEDRAS A FRIO, como o rito):
# copia (robocopy sobre a pasta, sem /PURGE), acrescenta as pedras Sonico e AfinacaoDasCordas e GERA a raiz e o Audit (preparar_kernel_v399.py gerar), UM `lake build` + Audit (construir_kernel_v399.sh) e o pos-build (pos_build_kernel_v399.py).
# USAR ANTES de instalar_v399.py: o `gerar` le o um.py do Nos (ou base_v398) como a base v398. Se o sandbox C:/t/k399c/final ja existe e esta certo, NAO ha o que refazer (ele e' o que o ensaio e os pinos usam).
V="/c/IALD/Central de Patentes/work/cadeia_de_selo/v399"
mkdir -p /c/t/k399c || exit 9
[ -f "$V/pos_build_kernel_v399.py" ] || { echo "falta pos_build_kernel_v399.py em $V -- NAO RODO"; exit 9; }
[ -f "$V/preparar_kernel_v399.py" ] && [ -f "$V/construir_kernel_v399.sh" ] || { echo "falta preparar_kernel_v399.py ou construir_kernel_v399.sh -- NAO RODO"; exit 9; }
MSYS_NO_PATHCONV=1 robocopy "C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\tgl_kernel" "C:\t\k399c\final" /E /COPY:DAT /DCOPY:DAT /MT:32 /R:1 /W:1 /NFL /NDL /NP /XJ /XF "TGLExt.lean.bak_*" /LOG:"C:\t\k399c\robocopy_final_refazer.log" > /dev/null
[ $? -lt 8 ] || exit 8
cd "$V" && python -I -B -X utf8 preparar_kernel_v399.py gerar && sh ./construir_kernel_v399.sh && python -I -B -X utf8 pos_build_kernel_v399.py
