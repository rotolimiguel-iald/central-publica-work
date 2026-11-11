#!/bin/sh
# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] o ensaio pre_selo contra o Nos v409 (canonico hoje), com o esboco e a bateria pinados na v409 (lidos dos pinos); --versao v409; conferido e adaptado em 06/11/2026 pelo fork B do claude-construtor-v410 (_adapt_forkB_*_v410.py)
# (nota herdada da adaptacao da v408 [fork C, 04/11/2026], reconferida em 05/11/2026 pelo fork B do claude-construtor-v409 e em 06/11/2026 pelo fork B do claude-construtor-v410, com os rotulos subidos) molde v409/bateria_pre_selo/rodar_ensaio_1_pre_selo_v409.sh (rotulos subidos por _bump_copia_v410.py; diff em bump/); conferido linha a linha em 04/11/2026: o passo e' simples v409 -> v410, o esboco e a bateria sao os pinados na v409 (path e sha256 lidos dos pinos), nada de bundle nem de contagem de modulos aqui
# v410, elo B(n), fase pre_selo, SO ENSAIO: os testes finais da Bancada contra o Nos v409 (canonico hoje) com a Bancada de producao JA pinando a v409 (sem salto de versoes).
# Esboco R3.5 (pino esboco_R3_5 de v409/PINOS_BN_v409.json) e bateria da v409 (pino de v409/bateria_pos_selo/PINOS_BATERIA_v409.json, gerada depois do selo da v409 e usada no B(n) da v409):
# os dois sha256 esperados sao LIDOS dos pinos e conferidos contra o disco antes de rodar (nunca digitados). SO LE a Bancada de producao e o Nos; grava recibos so em --saida.
# --versao v409 = a versao que o Nos tem agora (e que a Bancada pina). Sem --cadeia-de-selos (a Bancada nao esta atrasada: o esboco recusaria CADEIA_DE_SELOS_SEM_SALTO)
# e sem --recibo-pre-selo (so serve ao pos_selo). Veredito esperado: JA_SINCRONIZADA__ENSAIO__NADA_GRAVADO_NA_BANCADA (o que o pos_selo da v410 exige do recibo pre_selo).
V="/c/IALD/Central de Patentes/work/cadeia_de_selo/v410"
V14="/c/IALD/Central de Patentes/work/cadeia_de_selo/v409"
PY="python -I -B -X utf8"
SAIDA='C:\IALD\Central de Patentes\work\cadeia_de_selo\v410\bateria_pre_selo\ensaio_1'
OUT="$V/bateria_pre_selo/etapa1_stdout.txt"
cd "$V" || exit 9
pinow() { $PY -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8'))[sys.argv[2]][sys.argv[3]])" "$(cygpath -w "$1")" "$2" "$3" | tr -d '\r'; }
sha256w() { $PY -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" "$1" | tr -d '\r'; }
ESB=$(pinow "$V14/PINOS_BN_v409.json" esboco_R3_5 path)
ESB_PINO=$(pinow "$V14/PINOS_BN_v409.json" esboco_R3_5 sha256)
ESB_SHA=$(sha256w "$ESB")
[ -n "$ESB_SHA" ] && [ "$ESB_SHA" = "$ESB_PINO" ] || { echo "ESBOCO_SHA_DIVERGE $ESB_SHA != pino $ESB_PINO"; exit 9; }
BAT=$(pinow "$V14/bateria_pos_selo/PINOS_BATERIA_v409.json" bateria path)
BAT_PINO=$(pinow "$V14/bateria_pos_selo/PINOS_BATERIA_v409.json" bateria sha256)
BAT_SHA=$(sha256w "$BAT")
[ -n "$BAT_SHA" ] && [ "$BAT_SHA" = "$BAT_PINO" ] || { echo "BATERIA_SHA_DIVERGE $BAT_SHA != pino $BAT_PINO"; exit 9; }
$PY "$ESB" \
  --bancada "C:\IALD\Bancada_Um" --producao \
  --nos "C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós" \
  --versao v409 --fase pre_selo --modo ensaio \
  --bateria "$BAT" --bateria-sha256 "$BAT_SHA" \
  --saida "$SAIDA" \
  > "$OUT" 2>&1
echo "ETAPA1_RC=$?" >> "$OUT"
