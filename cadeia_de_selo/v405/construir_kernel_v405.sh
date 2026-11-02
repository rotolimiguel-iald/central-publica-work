#!/bin/sh
# Constroi o kernel do SANDBOX da v405 (C:\t\k405c\final; nunca o do Nos nem C:\t\k404c): um `lake build` INCREMENTAL (a v404 selada ja' esta compilada em .lake/build, copiada do Nos; as OITO pedras novas -- PonteDaMassa, MassaTensaoPura, Identidade, ObservadorTerminal, LeiDoDiminuto, TonicaDoHamiltoniano, DiscoDeEuler, PontoZeroDoPsion -- compilam agora; muda a raiz TGLExt; o Audit e' o da v404, inalterado) + `lake env lean TGL/Audit.lean`.
# Molde: construir_kernel_v404.sh. Logs crus (redirecionamento do bash, UTF-8) em kernel/; pos_build_kernel_v405.py monta o build_full.log no formato do molde e o recibo. Na preparacao de 01/11/2026 a construcao foi feita por este mesmo script (agente claude-prep-v405), com o treino v4 da IALD nativa rodando na mesma maquina
# (CPU a ~97%; o Lake 5.0.0-src+68218e8 desta maquina NAO aceita a opcao de numero de jobs, logo o build roda com o paralelismo padrao e disputa a CPU com o treino; o tempo medido vai em construir_marcas.txt); as oito pedras ja' tinham sido provadas por `lake env lean`/`lake build` no k404c (os recibos de 30/10 a 01/11); copiar_logs_do_kernel_v405.py confere os logs ja' em kernel\ e grava LOGS_COPIADOS_v405.json; este script e' o mesmo comando, para refazer.
K="/c/t/k405c/final"
D="/c/IALD/Central de Patentes/work/cadeia_de_selo/v405/kernel"
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
