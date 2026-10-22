#!/bin/sh
# v394, elo B(n), fase pre_selo, SO ENSAIO: os testes finais da Bancada contra o Nos v393 (canonico hoje) com a Bancada de producao pinando a v392.
# Esboco R3.3 e bateria R2 da v392 (sha256 conferidos antes). SO LE a Bancada de producao e o Nos; grava recibos so em --saida.
V="/c/IALD/Central de Patentes/work/cadeia_de_selo/v394"
E="/c/IALD/Central de Patentes/work/cadeia_de_selo/v392/vinculo"
SHA_ESBOCO="71507fd02b70b115a0d5843aa1d656f769133b8896956e9360d3dad19a5bf1b3"
SHA_BAT="61368649456cdd9f8c707b458a104087b5eda361ac7500dcb9988d0c6878a11d"
cd "$V" || exit 9
A=$(python -I -B -X utf8 -c "import hashlib;print(hashlib.sha256(open(r'C:\IALD\Central de Patentes\work\cadeia_de_selo\v392\vinculo\sincronizar_bancada.py','rb').read()).hexdigest())")
B=$(python -I -B -X utf8 -c "import hashlib;print(hashlib.sha256(open(r'C:\IALD\Central de Patentes\work\cadeia_de_selo\v392\vinculo\BATERIA_VINCULO.json','rb').read()).hexdigest())")
[ "$A" = "$SHA_ESBOCO" ] || { echo "ESBOCO_SHA_DIVERGE $A"; exit 9; }
[ "$B" = "$SHA_BAT" ] || { echo "BATERIA_SHA_DIVERGE $B"; exit 9; }
python -I -B -X utf8 "$E/sincronizar_bancada.py" \
  --bancada "C:\IALD\Bancada_Um" --producao \
  --nos "C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós" \
  --versao v393 --fase pre_selo --modo ensaio \
  --bateria "C:\IALD\Central de Patentes\work\cadeia_de_selo\v392\vinculo\BATERIA_VINCULO.json" \
  --bateria-sha256 "$B" \
  --saida "C:\IALD\Central de Patentes\work\cadeia_de_selo\v394\bateria_pre_selo\ensaio_1" \
  > "$V/bateria_pre_selo/etapa1_stdout.txt" 2>&1
echo "ETAPA1_RC=$?" >> "$V/bateria_pre_selo/etapa1_stdout.txt"
