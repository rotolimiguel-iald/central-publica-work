#!/bin/sh
# Constroi o kernel do SANDBOX da v400 (C:\t\k400c\final, COPIA de C:\t\k399c\final; nunca o do Nos): a v400 NAO acrescenta modulo ao kernel (a raiz TGLExt e o Audit sao os da v399, byte a byte); a copia ja' traz tudo compilado em .lake/build.
# Para o recibo do kernel ter as linhas `Built` da raiz (TGLExt) e do Audit (TGL.Audit) -- o que o T17 do B(n) exige -- este script apaga SO' os artefatos compilados desses dois modulos (ir/ e lib/lean/), o que obriga o lake a
# recompila-los (~200 s cada); a pedra Testemunho e o resto ficam como estao (Replayed). Depois: `lake build` + `lake env lean TGL/Audit.lean`.
# Molde: construir_kernel_v399.sh. Logs crus (redirecionamento do bash, UTF-8) em kernel/; pos_build_kernel_v400.py monta o build_full.log no formato do molde e o recibo.
K="/c/t/k400c/final"
D="/c/IALD/Central de Patentes/work/cadeia_de_selo/v400/kernel"
mkdir -p "$D"
for f in lake_build.log audit.log build_full.log; do [ -f "$D/$f" ] && cp -p "$D/$f" "$D/$f.bak_$(date +%Y%m%d_%H%M%S)"; done
cd "$K" || exit 9
for f in ir/TGL/Audit.c ir/TGL/Audit.c.hash ir/TGL/Audit.setup.json ir/TGLExt.c ir/TGLExt.c.hash ir/TGLExt.setup.json lib/lean/TGL/Audit.ilean lib/lean/TGL/Audit.ilean.hash lib/lean/TGL/Audit.olean lib/lean/TGL/Audit.olean.hash lib/lean/TGL/Audit.trace lib/lean/TGLExt.ilean lib/lean/TGLExt.ilean.hash lib/lean/TGLExt.olean lib/lean/TGLExt.olean.hash lib/lean/TGLExt.trace; do rm -f ".lake/build/$f"; done
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
