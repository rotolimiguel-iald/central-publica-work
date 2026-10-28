#!/bin/sh
# v403, elo B(n), fase pre_selo, SO ENSAIO: os testes finais da Bancada contra o Nos v402 (canonico hoje) com a Bancada de producao JA pinando a v402 (sem salto de versoes).
# Esboco R3.5 (pino esboco_R3_5 de v402/PINOS_BN_v402.json) e bateria da v402 (pino de v402/bateria_pos_selo/PINOS_BATERIA_v402.json, gerada depois do selo da v402 e usada no B(n) da v402):
# os dois sha256 esperados sao LIDOS dos pinos e conferidos contra o disco antes de rodar (nunca digitados). SO LE a Bancada de producao e o Nos; grava recibos so em --saida.
# --versao v402 = a versao que o Nos tem agora (e que a Bancada pina). Sem --cadeia-de-selos (a Bancada nao esta atrasada: o esboco recusaria CADEIA_DE_SELOS_SEM_SALTO)
# e sem --recibo-pre-selo (so serve ao pos_selo). Veredito esperado: JA_SINCRONIZADA__ENSAIO__NADA_GRAVADO_NA_BANCADA (o que o pos_selo da v403 exige do recibo pre_selo).
V="/c/IALD/Central de Patentes/work/cadeia_de_selo/v403"
V12="/c/IALD/Central de Patentes/work/cadeia_de_selo/v402"
PY="python -I -B -X utf8"
SAIDA='C:\IALD\Central de Patentes\work\cadeia_de_selo\v403\bateria_pre_selo\ensaio_1'
OUT="$V/bateria_pre_selo/etapa1_stdout.txt"
cd "$V" || exit 9
pinow() { $PY -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8'))[sys.argv[2]][sys.argv[3]])" "$(cygpath -w "$1")" "$2" "$3" | tr -d '\r'; }
sha256w() { $PY -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" "$1" | tr -d '\r'; }
ESB=$(pinow "$V12/PINOS_BN_v402.json" esboco_R3_5 path)
ESB_PINO=$(pinow "$V12/PINOS_BN_v402.json" esboco_R3_5 sha256)
ESB_SHA=$(sha256w "$ESB")
[ -n "$ESB_SHA" ] && [ "$ESB_SHA" = "$ESB_PINO" ] || { echo "ESBOCO_SHA_DIVERGE $ESB_SHA != pino $ESB_PINO"; exit 9; }
BAT=$(pinow "$V12/bateria_pos_selo/PINOS_BATERIA_v402.json" bateria path)
BAT_PINO=$(pinow "$V12/bateria_pos_selo/PINOS_BATERIA_v402.json" bateria sha256)
BAT_SHA=$(sha256w "$BAT")
[ -n "$BAT_SHA" ] && [ "$BAT_SHA" = "$BAT_PINO" ] || { echo "BATERIA_SHA_DIVERGE $BAT_SHA != pino $BAT_PINO"; exit 9; }
$PY "$ESB" \
  --bancada "C:\IALD\Bancada_Um" --producao \
  --nos "C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós" \
  --versao v402 --fase pre_selo --modo ensaio \
  --bateria "$BAT" --bateria-sha256 "$BAT_SHA" \
  --saida "$SAIDA" \
  > "$OUT" 2>&1
echo "ETAPA1_RC=$?" >> "$OUT"
