#!/bin/sh
# v404, elo B(n), fase pre_selo, COMPLETO e na ordem da v403 (NOTAS_PRE_SELO_v403.txt, TAREFA 1): deriva os cinco scripts da v404 (se ainda nao existem) do molde v403 por subida de versao;
# fotografa a producao (antes); roda o ensaio da Bancada (so' leitura da producao e do Nos v403; grava so' em --saida); fotografa (depois); confere o recibo pelo proprio esboco R3.5
# (23 condicoes + 5 controles negativos); fotografa (final); gera PINO_RECIBO_PRE_SELO_v404.json e PROVA_PRODUCAO_INTACTA_v404_pre_selo.json em v404\; apaga o sandbox curto C:\t\vb21;
# e entao fecha a preparacao: diff_e_pinos_v404.py (PINOS_BN_v404.json) e p00_precondicoes_v404.py. Para na primeira falha (set -e). Nao toca o Nos, nao instala, nao roda o rito.
# uso: sh ./rodar_bn_pre_selo_v404.sh > bn_pre_selo_out_v404.txt 2>&1
set -e
V="/c/IALD/Central de Patentes/work/cadeia_de_selo/v404"
B="$V/bateria_pre_selo"
PY="/c/Python314/python.exe -I -B -X utf8"
SNAP='C:\t\vb21\snap'
cd "$B"
[ -f rodar_ensaio_1_pre_selo_v404.sh ] || { echo "== 0b. derivar_pre_selo_v404.py $(date +%T)"; $PY derivar_pre_selo_v404.py; }
ls -la
if [ -e /c/t/vb21 ]; then echo "C:\\t\\vb21 ja existe -- NAO RODO (limpe antes)"; exit 9; fi
mkdir -p /c/t/vb21/snap
echo "== 1. snap antes $(date +%T)"; $PY snap_producao_v404.py antes "$SNAP"
echo "== 2. ensaio 1 da Bancada (pre_selo, ensaio) $(date +%T)"; sh ./rodar_ensaio_1_pre_selo_v404.sh || true
tail -3 etapa1_stdout.txt
grep -q "ETAPA1_RC=0" etapa1_stdout.txt || { echo "ETAPA1 FALHOU"; exit 1; }
echo "== 3. snap depois $(date +%T)"; $PY snap_producao_v404.py depois "$SNAP"
echo "== 4. conferir o recibo pelo esboco R3.5 $(date +%T)"; $PY conferir_recibo_pre_selo_v404.py | tail -4
echo "== 5. snap final $(date +%T)"; $PY snap_producao_v404.py final "$SNAP"
echo "== 6. gerar o pino do recibo e a prova da producao intacta $(date +%T)"; $PY gerar_pino_recibo_pre_selo_v404.py "$SNAP" | tail -4
echo "== 7. limpar o sandbox curto $(date +%T)"; $PY limpar_sandbox_vb21.py | tail -2
cd "$V"
echo "== 8. diff_e_pinos_v404.py $(date +%T)"; $PY diff_e_pinos_v404.py | tail -2
echo "== 9. p00_precondicoes_v404.py $(date +%T)"; $PY p00_precondicoes_v404.py | tail -16
echo "== FIM $(date +%T)"
