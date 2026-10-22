#!/bin/sh
# Constroi o kernel do SANDBOX (scratchpad\v376\kernel_src; nunca o do Nos) e roda a auditoria (TGL/Audit.lean): o log inteiro em build_full.log,
# com «inicio», a saida do lake build, a do #print axioms, rc=<rc> e «fim». O log anterior vai a build_full.log.bak_<ts> (bytes). Depois: extrair_axiomas_v386.py.
# (molde: v385/kernel/construir_kernel_v385.sh; so' a pasta de saida muda)
K="/c/Users/rotol/AppData/Local/Temp/claude/c--IALD-Central-de-Patentes/6da8f00d-d44f-4888-a88d-fc9f73eead3d/scratchpad/v376/kernel_src"
D="/c/Users/rotol/AppData/Local/Temp/claude/c--IALD-Central-de-Patentes/6da8f00d-d44f-4888-a88d-fc9f73eead3d/scratchpad/v386/kernel"
[ -f "$D/build_full.log" ] && cp -p "$D/build_full.log" "$D/build_full.log.bak_$(date +%Y%m%d_%H%M%S)"
cd "$K" || exit 9
{
  echo "inicio $(date '+%Y-%m-%d %H:%M:%S')"
  lake build 2>&1; rb=$?
  echo "rc_build=$rb"
  lake env lean TGL/Audit.lean 2>&1; ra=$?
  echo "rc_audit=$ra"
  if [ "$rb" = "0" ] && [ "$ra" = "0" ]; then echo "rc=0"; else echo "rc=1"; fi
  echo "fim $(date '+%Y-%m-%d %H:%M:%S')"
} > "$D/build_full.log.tmp"
mv -f "$D/build_full.log.tmp" "$D/build_full.log"
tail -3 "$D/build_full.log"
