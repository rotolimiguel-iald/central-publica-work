#!/bin/sh
# [ADAPTADO v411, 12/11/2026, claude-construtor-v411] conferido: refaz SO' o Audit do sandbox k411c (caminhos C:/t/k411c/final e v411/kernel); nao roda sem queda que corte o Audit
# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] refaz SO' o Audit do sandbox k410c (para uma queda de energia que corte o Audit; na v410 o build e o Audit de 06/11 terminaram com rc 0: NAO executado); conferido e adaptado em 06/11/2026 pelo fork B do claude-construtor-v410 (_adapt_forkB_*_v410.py)
# refaz SO' o Audit do sandbox da v411, se uma queda cortar o Audit depois de um build com rc 0 (molde: o da v410, escrito depois da queda de energia de 05/11 ~17:10). claude-construtor-v411, fork B, 06/11/2026.
K="/c/t/k411c/final"
D="/c/IALD/Central de Patentes/work/cadeia_de_selo/v411/kernel"
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
