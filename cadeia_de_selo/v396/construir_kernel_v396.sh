#!/bin/sh
# Constroi o kernel do SANDBOX da v396 (C:\t\k396c\final; nunca o do Nos nem C:\t\k396): um `lake build` INCREMENTAL (a pedra TestemunhaEstatica pode ja' estar compilada em .lake/build numa versao anterior do texto, e o Lake a recompila se a fonte mudou; muda a raiz TGLExt e o Audit) + `lake env lean TGL/Audit.lean`.
# Molde: construir_kernel_v395.sh. Logs crus (redirecionamento do bash, UTF-8) em kernel/; pos_build_kernel_v396.py monta o build_full.log no formato do molde e o recibo.
K="/c/t/k396c/final"
D="/c/IALD/Central de Patentes/work/cadeia_de_selo/v396/kernel"
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
