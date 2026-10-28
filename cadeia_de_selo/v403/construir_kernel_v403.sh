#!/bin/sh
# Constroi o kernel do SANDBOX da v403 (C:\t\k403c\final; nunca o do Nos nem C:\t\k402c): um `lake build` INCREMENTAL (a v402 selada, com as tres pedras da v402, ja' esta compilada em .lake/build; as TRES pedras novas, Caminho, Vida e VerdadeAdendo, compilam agora; muda a raiz TGLExt; o Audit e' o da v402, inalterado) + `lake env lean TGL/Audit.lean`.
# Molde: construir_kernel_v402.sh. Logs crus (redirecionamento do bash, UTF-8) em kernel/; pos_build_kernel_v403.py monta o build_full.log no formato do molde e o recibo. A construcao de 27/10/2026 (08:43 a 08:53, rc 0) foi feita no sandbox pela gerencia c1 e os logs dela
# estao em ..\v403_kernel\ (copiados em bytes para kernel\ por copiar_logs_do_kernel_v403.py); este script e' o mesmo comando, para refazer.
K="/c/t/k403c/final"
D="/c/IALD/Central de Patentes/work/cadeia_de_selo/v403/kernel"
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
