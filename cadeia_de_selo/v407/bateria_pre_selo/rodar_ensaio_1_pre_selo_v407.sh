#!/bin/sh
# [ADAPTADO v407, 03/11/2026] molde v406/bateria_pre_selo/rodar_ensaio_1_pre_selo_v406.sh (rotulos subidos por _bump_copia_v407.py; diff em bump/); conferido linha a linha: o passo e' simples v406 -> v407, o esboco e a bateria sao os pinados na v406 (path e sha256 lidos dos pinos), nada de bundle nem de contagem de modulos aqui
# v407, elo B(n), fase pre_selo, SO ENSAIO: os testes finais da Bancada contra o Nos v406 (canonico hoje) com a Bancada de producao JA pinando a v406 (sem salto de versoes).
# Esboco R3.5 (pino esboco_R3_5 de v406/PINOS_BN_v406.json) e bateria da v406 (pino de v406/bateria_pos_selo/PINOS_BATERIA_v406.json, gerada depois do selo da v406 e usada no B(n) da v406):
# os dois sha256 esperados sao LIDOS dos pinos e conferidos contra o disco antes de rodar (nunca digitados). SO LE a Bancada de producao e o Nos; grava recibos so em --saida.
# --versao v406 = a versao que o Nos tem agora (e que a Bancada pina). Sem --cadeia-de-selos (a Bancada nao esta atrasada: o esboco recusaria CADEIA_DE_SELOS_SEM_SALTO)
# e sem --recibo-pre-selo (so serve ao pos_selo). Veredito esperado: JA_SINCRONIZADA__ENSAIO__NADA_GRAVADO_NA_BANCADA (o que o pos_selo da v407 exige do recibo pre_selo).
V="/c/IALD/Central de Patentes/work/cadeia_de_selo/v407"
V14="/c/IALD/Central de Patentes/work/cadeia_de_selo/v406"
PY="python -I -B -X utf8"
SAIDA='C:\IALD\Central de Patentes\work\cadeia_de_selo\v407\bateria_pre_selo\ensaio_1'
OUT="$V/bateria_pre_selo/etapa1_stdout.txt"
cd "$V" || exit 9
pinow() { $PY -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8'))[sys.argv[2]][sys.argv[3]])" "$(cygpath -w "$1")" "$2" "$3" | tr -d '\r'; }
sha256w() { $PY -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" "$1" | tr -d '\r'; }
ESB=$(pinow "$V14/PINOS_BN_v406.json" esboco_R3_5 path)
ESB_PINO=$(pinow "$V14/PINOS_BN_v406.json" esboco_R3_5 sha256)
ESB_SHA=$(sha256w "$ESB")
[ -n "$ESB_SHA" ] && [ "$ESB_SHA" = "$ESB_PINO" ] || { echo "ESBOCO_SHA_DIVERGE $ESB_SHA != pino $ESB_PINO"; exit 9; }
BAT=$(pinow "$V14/bateria_pos_selo/PINOS_BATERIA_v406.json" bateria path)
BAT_PINO=$(pinow "$V14/bateria_pos_selo/PINOS_BATERIA_v406.json" bateria sha256)
BAT_SHA=$(sha256w "$BAT")
[ -n "$BAT_SHA" ] && [ "$BAT_SHA" = "$BAT_PINO" ] || { echo "BATERIA_SHA_DIVERGE $BAT_SHA != pino $BAT_PINO"; exit 9; }
$PY "$ESB" \
  --bancada "C:\IALD\Bancada_Um" --producao \
  --nos "C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós" \
  --versao v406 --fase pre_selo --modo ensaio \
  --bateria "$BAT" --bateria-sha256 "$BAT_SHA" \
  --saida "$SAIDA" \
  > "$OUT" 2>&1
echo "ETAPA1_RC=$?" >> "$OUT"
