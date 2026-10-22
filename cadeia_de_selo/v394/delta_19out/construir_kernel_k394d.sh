#!/bin/sh
# DELTA 19/10 da v394 -- constroi o kernel do SANDBOX C:\t\k394d (nunca o k394, nunca o do Nos): UM `lake build` INCREMENTAL (compila a pedra nova, a raiz e o Audit; o resto e' reaproveitado);
# depois `lake env lean TGL/Audit.lean` (o Audit completo, com as linhas de axiomas, de proveniencia e a de cobertura). Logs crus (redirecionamento do shell, UTF-8) em kernel_k394d\.
# Molde: construir_kernel_v394.sh. Escreve SO' em C:\t\k394d e em delta_19out.
K="/c/t/k394d"
D="/c/IALD/Central de Patentes/work/cadeia_de_selo/v394/delta_19out/kernel_k394d"
mkdir -p "$D"
for f in lake_build.log audit.log construir_marcas.txt; do [ -f "$D/$f" ] && cp -p "$D/$f" "$D/$f.bak_$(date +%Y%m%d_%H%M%S)"; done
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
