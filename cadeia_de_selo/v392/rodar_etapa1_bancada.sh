#!/bin/sh
# ETAPA 1 (v392): os testes finais da Bancada contra a v391 AINDA canonica (ensaio, pre_selo). SO LE a Bancada de producao e o Nos; grava recibos so em --saida.
# comando do PLANO (R3.2-0), com a saida na pasta da cadeia (raiz admitida pelo esboco: work/cadeia_de_selo/v392).
V="/c/IALD/Central de Patentes/work/cadeia_de_selo/v392"
cd "$V" || exit 9
python -I -B -X utf8 vinculo/sincronizar_bancada.py \
  --bancada "C:\IALD\Bancada_Um" --producao \
  --nos "C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós" \
  --versao v391 --fase pre_selo --modo ensaio \
  --bateria "C:\IALD\Central de Patentes\work\cadeia_de_selo\v392\vinculo\BATERIA_VINCULO.json" \
  --bateria-sha256 "$(python -I -B -X utf8 -c "import hashlib;print(hashlib.sha256(open(r'C:\IALD\Central de Patentes\work\cadeia_de_selo\v392\vinculo\BATERIA_VINCULO.json','rb').read()).hexdigest())")" \
  --saida "C:\IALD\Central de Patentes\work\cadeia_de_selo\v392\bateria_pre_selo\ensaio_1" \
  > "$V/bateria_pre_selo/etapa1_stdout.txt" 2>&1
echo "ETAPA1_RC=$?" >> "$V/bateria_pre_selo/etapa1_stdout.txt"
