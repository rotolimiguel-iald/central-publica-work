#!/bin/sh
# Constroi o kernel do SANDBOX da v394 (C:\t\k394d\final; nunca o do Nos nem C:\t\k394): UM unico `lake build` compila os 190 modulos novos (189 do Codex + a pedra do delta de 19/10) + a raiz + o Audit; depois `lake env lean TGL/Audit.lean`.
# Molde: construir_kernel_v393.sh. Logs crus (redirecionamento do bash, UTF-8) em kernel/ (a geracao anterior fica como .bak_ de bytes); pos_build_kernel_v394.py monta o build_full.log no formato do molde e o recibo.
K="/c/t/k394d/final"
D="/c/IALD/Central de Patentes/work/cadeia_de_selo/v394/kernel"
mkdir -p "$D"
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
