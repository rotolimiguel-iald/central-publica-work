#!/bin/sh
# exploracao no sandbox A (C:\t\k392\kernel): lake build (compila as pedras de STONES, 14 na rodada 2) + enumeracao COB. Logs em kernel/.
V="/c/IALD/Central de Patentes/work/cadeia_de_selo/v392/kernel"
cd /c/t/k392/kernel || exit 9
echo "inicio $(date '+%Y-%m-%d %H:%M:%S')" > "$V/explorar_A.log"
lake build > "$V/explorar_A_lake_build.log" 2>&1; echo "rc_build=$?" >> "$V/explorar_A.log"
lake env lean "$V/Cob_v392.lean" > "$V/cob_v392.txt" 2> "$V/cob_v392.err"; echo "rc_cob=$?" >> "$V/explorar_A.log"
echo "fim $(date '+%Y-%m-%d %H:%M:%S')" >> "$V/explorar_A.log"
