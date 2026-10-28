#!/bin/sh
# Elo B(n) da Bancada Um para a v403 (passos 10a, 10b, 10c e 11 a 13 da cadeia do pós-rito), numa só ordem da gerência c1 (28/10/2026).
# Para na primeira falha. O serviço (porta 18777) é parado SÓ PELO PID (nunca por nome), depois de conferir que o PID é o um_bancada.py;
# religado pelo comando do campo «religar» do recibo de parada (Start-Process, destacado); cada ato com recibo (recibo_parada_v403.py / recibo_religamento_v403.py).
# uso: sh ./rodar_elo_bancada_v403.sh > elo_bancada_out_v403.txt 2>&1   (ambiente: V403_AUTORIZACAO_OPERADOR, B3_AUTORIZADO=sim, EVENTO, EVENTO_HASH)
set -e
PK="/c/IALD/Central de Patentes/work/cadeia_de_selo/v403"
SEL="$PK/pos_rito"; SRV="$PK/bancada_B3_servico"
PY="/c/Python314/python.exe -I -B -X utf8"
[ -n "$V403_AUTORIZACAO_OPERADOR" ] || { echo "sem V403_AUTORIZACAO_OPERADOR"; exit 2; }
[ "$B3_AUTORIZADO" = "sim" ] && [ -n "$EVENTO" ] && [ -n "$EVENTO_HASH" ] || { echo "sem B3_AUTORIZADO/EVENTO/EVENTO_HASH"; exit 2; }
porta_aberta() { $PY -c "import socket,sys
s=socket.socket(); s.settimeout(1.5)
sys.exit(0 if s.connect_ex(('127.0.0.1',18777))==0 else 1)"; }
echo "== A. parada do servico da Bancada pelo PID $(date +%T)"
if porta_aberta; then
  PID=$(powershell.exe -NoProfile -Command "(Get-NetTCPConnection -LocalPort 18777 -State Listen | Select-Object -First 1).OwningProcess" | tr -d '\r ')
  CMD=$(powershell.exe -NoProfile -Command "(Get-CimInstance Win32_Process -Filter 'ProcessId = $PID').CommandLine" | tr -d '\r')
  echo "  PID na porta 18777: $PID ; cmd: $CMD"
  case "$CMD" in *um_bancada.py*) ;; *) echo "o PID $PID NAO e' o um_bancada.py -- NAO PARO"; exit 3;; esac
  taskkill //PID "$PID" > /dev/null 2>&1 || true
  i=0; while porta_aberta && [ $i -lt 10 ]; do sleep 1; i=$((i+1)); done
  if porta_aberta; then echo "  ainda escuta apos TERM: taskkill /F pelo PID $PID"; taskkill //F //PID "$PID"; i=0; while porta_aberta && [ $i -lt 15 ]; do sleep 1; i=$((i+1)); done; fi
  porta_aberta && { echo "porta 18777 continua aberta -- PARO"; exit 3; }
  echo "  servico parado (PID $PID); porta 18777 fechada $(date +%T)"
else
  echo "  porta 18777 ja estava fechada"
fi
echo "== B. recibo da parada $(date +%T)"
(cd "$SRV" && $PY recibo_parada_v403.py | tail -3 | cut -c1-300)
[ -f "$SRV/RECIBO_PARADA_v403.json" ] || { echo "sem RECIBO_PARADA_v403.json"; exit 4; }
echo "== C. chain 10a $(date +%T)"
(cd "$SEL" && CHAIN_DE=10a CHAIN_ATE=10a sh ./chain_pos_rito_v403.sh | tail -4 | cut -c1-300)
echo "== D. chain 10b: B(n) APLICAR (evento $EVENTO / $EVENTO_HASH) $(date +%T)"
(cd "$SEL" && CHAIN_DE=10b CHAIN_ATE=10b sh ./chain_pos_rito_v403.sh | tail -6 | cut -c1-400)
echo "== E. religar o servico (comando do recibo de parada) $(date +%T)"
REL=$($PY -c "import json;print(json.load(open(r'$SRV/RECIBO_PARADA_v403.json',encoding='utf-8'))['religar'])" | tr -d '\r')
echo "  religar: $REL"
case "$REL" in *um_bancada.py*) ;; *) echo "comando de religar inesperado -- PARO"; exit 5;; esac
powershell.exe -NoProfile -Command "Start-Process -FilePath 'C:\Python314\pythonw.exe' -ArgumentList '-X','utf8','C:\IALD\Bancada_Um\um_bancada.py' -WorkingDirectory 'C:\IALD\Bancada_Um' -WindowStyle Hidden"
i=0; until porta_aberta || [ $i -ge 120 ]; do sleep 2; i=$((i+1)); done
porta_aberta || { echo "o servico nao voltou a escutar em 240 s"; exit 6; }
echo "  porta 18777 escuta de novo $(date +%T)"; sleep 5
echo "== F. recibo do religamento $(date +%T)"
(cd "$SRV" && $PY recibo_religamento_v403.py | tail -3 | cut -c1-300)
[ -f "$SRV/RECIBO_RELIGAMENTO_v403.json" ] || { echo "sem RECIBO_RELIGAMENTO_v403.json"; exit 7; }
echo "== G. chain 10c a 13 (religamento conferido, fechar, registrar_mapa monta, inventario da bancada) $(date +%T)"
(cd "$SEL" && CHAIN_DE=10c CHAIN_ATE=13 sh ./chain_pos_rito_v403.sh > "$SEL/chain_10c_13_out_v403.txt" 2>&1; rc=$?; grep -n -E "^== |PARADA:|AGUARDA_OPERADOR|Traceback|FALH|RECUS" "$SEL/chain_10c_13_out_v403.txt" | cut -c1-240 | head -30; tail -4 "$SEL/chain_10c_13_out_v403.txt" | cut -c1-300; exit $rc)
echo "== FIM $(date +%T)"
