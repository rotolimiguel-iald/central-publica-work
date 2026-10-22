#!/bin/sh
# Constroi o kernel do SANDBOX B (C:\t\k393\final; nunca o do Nos): UM unico `lake build` compila as 3 pedras da REGRA + a raiz + o Audit; depois `lake env lean TGL/Audit.lean`.
# Molde: construir_kernel_v392.sh. Logs crus (redirecionamento do bash, UTF-8) em kernel/; pos_build_kernel_v393.py monta o build_full.log no formato do molde e o recibo.
K="/c/t/k393/final"
D="/c/IALD/Central de Patentes/work/cadeia_de_selo/v393/kernel"
for f in lake_build.log audit.log build_full.log; do [ -f "$D/$f" ] && cp -p "$D/$f" "$D/$f.bak_$(date +%Y%m%d_%H%M%S)"; done
cd "$K" || exit 9
echo "inicio $(date '+%Y-%m-%d %H:%M:%S')" > "$D/construir_marcas.txt"
echo "epoch_inicio=$(date +%s)" >> "$D/construir_marcas.txt"
lake build > "$D/lake_build.log" 2>&1; rb=$?
echo "rc_build=$rb $(date '+%H:%M:%S')" >> "$D/construir_marcas.txt"
echo "epoch_build_fim=$(date +%s)" >> "$D/construir_marcas.txt"
lake env lean TGL/Audit.lean > "$D/audit.log" 2>&1; ra=$?
echo "rc_audit=$ra $(date '+%H:%M:%S')" >> "$D/construir_marcas.txt"
echo "epoch_audit_fim=$(date +%s)" >> "$D/construir_marcas.txt"
if [ "$rb" = "0" ] && [ "$ra" = "0" ]; then echo "rc=0" >> "$D/construir_marcas.txt"; else echo "rc=1" >> "$D/construir_marcas.txt"; fi
echo "fim $(date '+%Y-%m-%d %H:%M:%S')" >> "$D/construir_marcas.txt"
cat "$D/construir_marcas.txt"
