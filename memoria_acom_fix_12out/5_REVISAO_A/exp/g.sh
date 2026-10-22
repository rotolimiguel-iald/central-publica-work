#!/bin/sh
# run python under the auditor guard, root = 5_REVISAO_A
R='C:\IALD\Central de Patentes\work\memoria_acom_fix_12out\5_REVISAO_A'
mkdir -p "/c/IALD/Central de Patentes/work/memoria_acom_fix_12out/5_REVISAO_A/guard_log"
export PYTHONPATH="$R\int\guard"
export ACOM_AUDIT_ROOT="$R"
export TEMP="$R\exp\tmp" TMP="$R\exp\tmp" PYTHONDONTWRITEBYTECODE=1 PYTHONUTF8=1 PYTHONIOENCODING=utf-8
export IALD_MEMORY_SNAPSHOT_ARCHIVE_DIR="$R\exp\runs\arquivo_D_default"
cd "/c/IALD/Central de Patentes/work/memoria_acom_fix_12out/5_REVISAO_A/exp"
exec C:/Python314/python.exe -B -X utf8 "$@"
