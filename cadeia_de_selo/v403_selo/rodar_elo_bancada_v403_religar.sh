#!/bin/sh
# Retomada do elo B(n) da v403 a partir do RELIGAMENTO (passos E, F e G do rodar_elo_bancada_v403.sh): A-D ja' feitos (recibo da parada, 10a, 10b APLICADA = REPINADA_B12).
# Correcao: o caminho do recibo passado ao python vai em forma Windows (cygpath -w), nao em forma MSYS.
# uso: sh ./rodar_elo_bancada_v403_religar.sh > elo_bancada_religar_out_v403.txt 2>&1   (ambiente: V403_AUTORIZACAO_OPERADOR)
set -e
PK="/c/IALD/Central de Patentes/work/cadeia_de_selo/v403"
SEL="$PK/pos_rito"; SRV="$PK/bancada_B3_servico"
PY="/c/Python314/python.exe -I -B -X utf8"
[ -n "$V403_AUTORIZACAO_OPERADOR" ] || { echo "sem V403_AUTORIZACAO_OPERADOR"; exit 2; }
[ -f "$SRV/RECIBO_PARADA_v403.json" ] || { echo "sem o recibo da parada"; exit 4; }
[ -d "$PK/bancada_B3" ] || { echo "sem a pasta do B(n) aplicado"; exit 4; }
porta_aberta() { $PY -c "import socket,sys
s=socket.socket(); s.settimeout(1.5)
sys.exit(0 if s.connect_ex(('127.0.0.1',18777))==0 else 1)"; }
echo "== E. religar o servico (comando do recibo de parada) $(date +%T)"
RPW=$(cygpath -w "$SRV/RECIBO_PARADA_v403.json")
REL=$($PY -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8'))['religar'])" "$RPW" | tr -d '\r')
echo "  religar: $REL"
case "$REL" in *Bancada_Um*) ;; *) echo "comando de religar inesperado -- PARO"; exit 5;; esac
if porta_aberta; then echo "  a porta 18777 ja escuta -- nao religo de novo"; else
  powershell.exe -NoProfile -Command "Start-Process -FilePath 'C:\Python314\pythonw.exe' -ArgumentList '-X','utf8','C:\IALD\Bancada_Um\um_bancada.py' -WorkingDirectory 'C:\IALD\Bancada_Um' -WindowStyle Hidden"
  i=0; until porta_aberta || [ $i -ge 120 ]; do sleep 2; i=$((i+1)); done
  porta_aberta || { echo "o servico nao voltou a escutar em 240 s"; exit 6; }
  echo "  porta 18777 escuta de novo $(date +%T)"; sleep 5
fi
echo "== F. recibo do religamento $(date +%T)"
(cd "$SRV" && $PY recibo_religamento_v403.py | tail -3 | cut -c1-300)
[ -f "$SRV/RECIBO_RELIGAMENTO_v403.json" ] || { echo "sem RECIBO_RELIGAMENTO_v403.json"; exit 7; }
echo "== G. chain 10c a 13 (religamento conferido, fechar, registrar_mapa monta, inventario da bancada) $(date +%T)"
(cd "$SEL" && CHAIN_DE=10c CHAIN_ATE=13 sh ./chain_pos_rito_v403.sh > "$SEL/chain_10c_13_out_v403.txt" 2>&1; rc=$?; grep -n -E "^== |PARADA:|AGUARDA_OPERADOR|Traceback|FALH|RECUS" "$SEL/chain_10c_13_out_v403.txt" | cut -c1-240 | head -30; tail -4 "$SEL/chain_10c_13_out_v403.txt" | cut -c1-300; exit $rc)
echo "== FIM $(date +%T)"
