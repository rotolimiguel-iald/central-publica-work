#!/bin/sh
# Constroi o kernel do SANDBOX (work\v388_kernel\kernel_src; nunca o do Nos) e roda a auditoria (TGL/Audit.lean): o log inteiro em work\v390_kernel\build_full.log,
# com «inicio», a saida do lake build, a do #print axioms, rc=<rc> e «fim». (molde: o da v388; so' a pasta de saida muda)
K="/c/IALD/Central de Patentes/work/v388_kernel/kernel_src"
D="/c/IALD/Central de Patentes/work/v390_kernel"
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
