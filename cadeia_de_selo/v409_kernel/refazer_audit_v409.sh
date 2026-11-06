#!/bin/sh
# refaz SO' o Audit do sandbox da v409 (o build terminou com rc 0 as 17:05:33; a queda de energia de ~17:10 cortou o Audit). claude-construtor-v409, 05/11/2026.
K="/c/t/k409c/final"
D="/c/IALD/Central de Patentes/work/cadeia_de_selo/v409/kernel"
[ -f "$D/audit.log" ] && cp -p "$D/audit.log" "$D/audit.log.bak_cortado_$(date +%Y%m%d_%H%M%S)"
cp -p "$D/construir_marcas.txt" "$D/construir_marcas.txt.bak_$(date +%Y%m%d_%H%M%S)"
cd "$K" || exit 9
echo "audit_refeito_inicio $(date '+%H:%M:%S') (o Audit anterior foi cortado pela queda de energia)" >> "$D/construir_marcas.txt"
echo "epoch_audit_inicio=$(date +%s)" >> "$D/construir_marcas.txt"
/c/Users/rotol/.elan/bin/lake env lean TGL/Audit.lean > "$D/audit.log" 2>&1; ra=$?
echo "rc_audit=$ra $(date '+%H:%M:%S')" >> "$D/construir_marcas.txt"
echo "epoch_audit_fim=$(date +%s)" >> "$D/construir_marcas.txt"
if [ "$ra" = "0" ]; then echo "rc=0" >> "$D/construir_marcas.txt"; else echo "rc=1" >> "$D/construir_marcas.txt"; fi
echo "fim $(date '+%Y-%m-%d %H:%M:%S')" >> "$D/construir_marcas.txt"
cat "$D/construir_marcas.txt"
