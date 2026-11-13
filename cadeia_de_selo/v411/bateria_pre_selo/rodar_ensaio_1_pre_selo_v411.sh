#!/bin/sh
# [ADAPTADO v411, 12/11/2026, claude-construtor-v411 (retomada, fork B)] o ensaio pre_selo contra o Nos v410 (canonico hoje), esboco e bateria pinados na v410 (lidos dos pinos); --versao v410; a saida (--saida) e o stdout em OUTB, lido do delta (no ensaio do topo proposto, a pasta de ensaio)
# [ADAPTADO v410, 06/11/2026, claude-construtor-v410] o ensaio pre_selo contra o Nos v409 (canonico hoje), com o esboco e a bateria pinados na v409 (lidos dos pinos); --versao v409; conferido e adaptado em 06/11/2026 pelo fork B do claude-construtor-v410 (_adapt_forkB_*_v410.py)
# (nota herdada da adaptacao da v408 [fork C, 04/11/2026], reconferida em 05/11/2026 pelo fork B do claude-construtor-v410 e em 06/11/2026 pelo fork B do claude-construtor-v410, com os rotulos subidos; na v411, adaptado em 12/11/2026 pelo fork B do claude-construtor-v411, retomada) molde v410/bateria_pre_selo/rodar_ensaio_1_pre_selo_v410.sh (rotulos subidos por _bump_copia_v411.py; diff em bump/); conferido linha a linha em 04/11/2026: o passo e' simples v410 -> v411, o esboco e a bateria sao os pinados na v410 (path e sha256 lidos dos pinos), nada de bundle nem de contagem de modulos aqui
# v411, elo B(n), fase pre_selo, SO ENSAIO: os testes finais da Bancada contra o Nos v410 (canonico hoje) com a Bancada de producao JA pinando a v410 (sem salto de versoes).
# Esboco R3.5 (pino esboco_R3_5 de v410/PINOS_BN_v410.json) e bateria da v410 (pino de v410/bateria_pos_selo/PINOS_BATERIA_v410.json, gerada depois do selo da v410 e usada no B(n) da v410):
# os dois sha256 esperados sao LIDOS dos pinos e conferidos contra o disco antes de rodar (nunca digitados). SO LE a Bancada de producao e o Nos; grava recibos so em --saida.
# --versao v410 = a versao que o Nos tem agora (e que a Bancada pina). Sem --cadeia-de-selos (a Bancada nao esta atrasada: o esboco recusaria CADEIA_DE_SELOS_SEM_SALTO)
# e sem --recibo-pre-selo (so serve ao pos_selo). Veredito esperado: JA_SINCRONIZADA__ENSAIO__NADA_GRAVADO_NA_BANCADA (o que o pos_selo da v411 exige do recibo pre_selo).
V="/c/IALD/Central de Patentes/work/cadeia_de_selo/v411"
V14="/c/IALD/Central de Patentes/work/cadeia_de_selo/v410"
PY="python -I -B -X utf8"
cd "$V" || exit 9
# (v411) onde a bateria grava: no ensaio do topo proposto (V411_ENSAIO_TOPO_PROPOSTO=1, lido pelo delta_v411) a pasta de ensaio, fora de work; no real, esta pasta (como na v410)
OUTB_W=$($PY -c "import importlib.util as u,os,sys; s=u.spec_from_file_location('d',sys.argv[1]); m=u.module_from_spec(s); s.loader.exec_module(m); print(os.path.join(m.SAIDA,'bateria_pre_selo') if m.ENSAIO_TOPO_PROPOSTO else sys.argv[2])" "$(cygpath -w "$V/delta_v411.py")" "$(cygpath -w "$V/bateria_pre_selo")" | tr -d '\r')
[ -n "$OUTB_W" ] || { echo "a pasta de saida da bateria nao foi lida do delta_v411"; exit 9; }
OUTB=$(cygpath -u "$OUTB_W"); mkdir -p "$OUTB"
SAIDA="$OUTB_W\\ensaio_1"
OUT="$OUTB/etapa1_stdout.txt"
pinow() { $PY -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8'))[sys.argv[2]][sys.argv[3]])" "$(cygpath -w "$1")" "$2" "$3" | tr -d '\r'; }
sha256w() { $PY -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" "$1" | tr -d '\r'; }
ESB=$(pinow "$V14/PINOS_BN_v410.json" esboco_R3_5 path)
ESB_PINO=$(pinow "$V14/PINOS_BN_v410.json" esboco_R3_5 sha256)
ESB_SHA=$(sha256w "$ESB")
[ -n "$ESB_SHA" ] && [ "$ESB_SHA" = "$ESB_PINO" ] || { echo "ESBOCO_SHA_DIVERGE $ESB_SHA != pino $ESB_PINO"; exit 9; }
BAT=$(pinow "$V14/bateria_pos_selo/PINOS_BATERIA_v410.json" bateria path)
BAT_PINO=$(pinow "$V14/bateria_pos_selo/PINOS_BATERIA_v410.json" bateria sha256)
BAT_SHA=$(sha256w "$BAT")
[ -n "$BAT_SHA" ] && [ "$BAT_SHA" = "$BAT_PINO" ] || { echo "BATERIA_SHA_DIVERGE $BAT_SHA != pino $BAT_PINO"; exit 9; }
$PY "$ESB" \
  --bancada "C:\IALD\Bancada_Um" --producao \
  --nos "C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós" \
  --versao v410 --fase pre_selo --modo ensaio \
  --bateria "$BAT" --bateria-sha256 "$BAT_SHA" \
  --saida "$SAIDA" \
  > "$OUT" 2>&1
echo "ETAPA1_RC=$?" >> "$OUT"
