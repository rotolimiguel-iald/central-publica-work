#!/bin/sh
# exploracao no sandbox A (C:\t\k393\kernel): lake build das 3 pedras da REGRA (so' elas e suas dependencias) + enumeracao COB. Logs em kernel/.
V="/c/IALD/Central de Patentes/work/cadeia_de_selo/v393/kernel"
cd /c/t/k393/kernel || exit 9
echo "inicio $(date '+%Y-%m-%d %H:%M:%S')" > "$V/explorar_A.log"
lake build TGLExt.RuleTruthContract TGLExt.TheRuleAndTheFigureOfTruth TGLExt.TheRuleInTheContinuousMotor > "$V/explorar_A_lake_build.log" 2>&1; echo "rc_build=$?" >> "$V/explorar_A.log"
lake env lean "$V/Cob_v393.lean" > "$V/cob_v393.txt" 2> "$V/cob_v393.err"; echo "rc_cob=$?" >> "$V/explorar_A.log"
echo "fim $(date '+%Y-%m-%d %H:%M:%S')" >> "$V/explorar_A.log"
