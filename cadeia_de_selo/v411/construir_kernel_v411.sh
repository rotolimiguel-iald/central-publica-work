#!/bin/sh
# Constroi o kernel do SANDBOX da v411 (C:\t\k411c\final; nunca o do Nos): `lake build` INCREMENTAL (a v410 selada ja' esta compilada em .lake/build, copiada de C:\t\k410c\final; a v411 NAO tem
# modulo novo: nada a compilar) e depois o Audit, para MEDIR que a escada e as declaracoes sao as da v410 (DESENHO_v411 secao 1). Molde: construir_kernel_v410.sh (so' os rotulos sobem).
# Marcas de tempo em kernel/construir_marcas.txt. claude-construtor-v411, 12/11/2026.
K="/c/t/k411c/final"
D="/c/IALD/Central de Patentes/work/cadeia_de_selo/v411/kernel"
mkdir -p "$D"
for f in lake_build.log audit.log build_full.log; do [ -f "$D/$f" ] && cp -p "$D/$f" "$D/$f.bak_$(date +%Y%m%d_%H%M%S)"; done
cd "$K" || exit 9
echo "inicio $(date '+%Y-%m-%d %H:%M:%S')" > "$D/construir_marcas.txt"
echo "epoch_inicio=$(date +%s)" >> "$D/construir_marcas.txt"
/c/Users/rotol/.elan/bin/lake build > "$D/lake_build.log" 2>&1; rb=$?
echo "rc_build=$rb $(date '+%H:%M:%S')" >> "$D/construir_marcas.txt"
echo "epoch_build_fim=$(date +%s)" >> "$D/construir_marcas.txt"
/c/Users/rotol/.elan/bin/lake env lean TGL/Audit.lean > "$D/audit.log" 2>&1; ra=$?
echo "rc_audit=$ra $(date '+%H:%M:%S')" >> "$D/construir_marcas.txt"
echo "epoch_audit_fim=$(date +%s)" >> "$D/construir_marcas.txt"
if [ "$rb" = "0" ] && [ "$ra" = "0" ]; then echo "rc=0" >> "$D/construir_marcas.txt"; else echo "rc=1" >> "$D/construir_marcas.txt"; fi
echo "fim $(date '+%Y-%m-%d %H:%M:%S')" >> "$D/construir_marcas.txt"
cat "$D/construir_marcas.txt"
