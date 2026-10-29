#!/bin/sh
# Constroi o kernel do SANDBOX da v404 (C:\t\k404c\final; nunca o do Nos nem C:\t\k403c): um `lake build` INCREMENTAL (a v403 selada, com as tres pedras da v403, ja' esta compilada em .lake/build; as DUAS pedras novas, ProjecaoTransversalDaMeiaNat e Jo8v32, compilam agora; muda a raiz TGLExt; o Audit e' o da v403, inalterado) + `lake env lean TGL/Audit.lean`.
# Molde: construir_kernel_v403.sh. Logs crus (redirecionamento do bash, UTF-8) em kernel/; pos_build_kernel_v404.py monta o build_full.log no formato do molde e o recibo. Na preparacao de 28/10/2026 a construcao foi feita por este mesmo script (agente claude-prep-v404); as duas pedras ja' tinham sido provadas
# uma a uma por `lake env lean` no k403c (work\projecao_transversal_28out\RECIBO_PEDRA_*); copiar_logs_do_kernel_v404.py confere os logs ja' em kernel\ e grava LOGS_COPIADOS_v404.json; este script e' o mesmo comando, para refazer.
K="/c/t/k404c/final"
D="/c/IALD/Central de Patentes/work/cadeia_de_selo/v404/kernel"
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
