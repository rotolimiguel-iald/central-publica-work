#!/bin/sh
# [ADAPTADO v408, 04/11/2026, claude-construtor-v408 (fork C)] molde v407/bateria_pre_selo/rodar_bn_pre_selo_v407.sh (rotulos subidos por _bump_copia_v408.py; diff em bump/); conferido em 04/11/2026: (1) os cinco scripts da v408 JA existem (nasceram da subida mecanica e foram adaptados a mao); o derivador da v407 nao se aplica
# (ver derivar_pre_selo_v408.py) e o que faltar PARA a corrida, em vez de ser rederivado; (2) os passos 4, 6, 8 e 9 NAO mascaram mais o codigo de saida pelo pipe `| tail` (o molde mascarava: RC_BN=0 mesmo com conferencia ou p00 reprovando);
# o codigo de saida de cada um e' impresso (RC_CONFERENCIA, RC_PINO, RC_DIFF_PINOS, RC_P00) e o desta corrida e' 0 so' se 4, 6 e 8 sairam 0 (o p00 e' o veredito da cadeia INTEIRA, inclusive de arquivos de outros: o veredito dele vem no texto e em RC_P00).
# v408, elo B(n), fase pre_selo, na ordem da v407 (NOTAS_PRE_SELO_v407.txt, TAREFA 1): fotografa a producao (antes); roda o ensaio da Bancada (so' leitura da producao e do Nos v407; grava so' em --saida); fotografa (depois); confere o recibo pelo proprio esboco R3.5
# (23 condicoes + 5 controles negativos); fotografa (final); gera PINO_RECIBO_PRE_SELO_v408.json e PROVA_PRODUCAO_INTACTA_v408_pre_selo.json em v408\; apaga o sandbox curto C:\t\vb21;
# e entao fecha a preparacao: diff_e_pinos_v408.py (regrava PINOS_BN_v408.json, DIFF_KERNEL_v408.txt e DIFF_v407_v408.diff) e p00_precondicoes_v408.py (regrava PRECONDICOES_v408.json). Nao toca o Nos, nao instala, nao roda o rito, nao grava na Bancada, nao para nem religa servico.
# uso: sh ./rodar_bn_pre_selo_v408.sh > bn_pre_selo_out_v408.txt 2>&1        (quem chama pode acrescentar `echo "RC_BN=$?"`, como o fim_de_cadeia_v408.sh)
set -e
V="/c/IALD/Central de Patentes/work/cadeia_de_selo/v408"
B="$V/bateria_pre_selo"
PY="/c/Python314/python.exe -I -B -X utf8"
SNAP='C:\t\vb21\snap'
cd "$B"
for f in rodar_ensaio_1_pre_selo_v408.sh snap_producao_v408.py conferir_recibo_pre_selo_v408.py gerar_pino_recibo_pre_selo_v408.py limpar_sandbox_vb21.py; do
  [ -f "$f" ] || { echo "FALTA $f -- NAO RODO (os cinco scripts da v408 nao sao rederivados; ver _bump_copia_v408.py e bump/)"; exit 9; }
done
if grep -l '^# \[A ADAPTAR v408\]' rodar_ensaio_1_pre_selo_v408.sh snap_producao_v408.py conferir_recibo_pre_selo_v408.py gerar_pino_recibo_pre_selo_v408.py limpar_sandbox_vb21.py rodar_bn_pre_selo_v408.sh; then echo "algum script ainda traz a marca [A ADAPTAR v408] -- NAO RODO"; exit 9; fi
ls -la
if [ -e /c/t/vb21 ]; then echo "C:\\t\\vb21 ja existe -- NAO RODO (limpe antes)"; exit 9; fi
mkdir -p /c/t/vb21/snap
echo "== 1. snap antes $(date +%T)"; $PY snap_producao_v408.py antes "$SNAP"
echo "== 2. ensaio 1 da Bancada (pre_selo, ensaio) $(date +%T)"; sh ./rodar_ensaio_1_pre_selo_v408.sh || true
tail -3 etapa1_stdout.txt
grep -q "ETAPA1_RC=0" etapa1_stdout.txt || { echo "ETAPA1 FALHOU"; exit 1; }
echo "== 3. snap depois $(date +%T)"; $PY snap_producao_v408.py depois "$SNAP"
echo "== 4. conferir o recibo pelo esboco R3.5 $(date +%T)"; RC_CONFERENCIA=0; $PY conferir_recibo_pre_selo_v408.py > conferencia_out_v408.txt 2>&1 || RC_CONFERENCIA=$?; tail -4 conferencia_out_v408.txt; echo "RC_CONFERENCIA=$RC_CONFERENCIA"
echo "== 5. snap final $(date +%T)"; $PY snap_producao_v408.py final "$SNAP"
echo "== 6. gerar o pino do recibo e a prova da producao intacta $(date +%T)"; RC_PINO=0; $PY gerar_pino_recibo_pre_selo_v408.py "$SNAP" > pino_out_v408.txt 2>&1 || RC_PINO=$?; tail -4 pino_out_v408.txt; echo "RC_PINO=$RC_PINO"
echo "== 7. limpar o sandbox curto $(date +%T)"; $PY limpar_sandbox_vb21.py | tail -2
cd "$V"
echo "== 8. diff_e_pinos_v408.py $(date +%T)"; RC_DIFF_PINOS=0; $PY diff_e_pinos_v408.py > "$B/diff_e_pinos_out_v408.txt" 2>&1 || RC_DIFF_PINOS=$?; tail -2 "$B/diff_e_pinos_out_v408.txt"; echo "RC_DIFF_PINOS=$RC_DIFF_PINOS"
echo "== 9. p00_precondicoes_v408.py $(date +%T)"; RC_P00=0; $PY p00_precondicoes_v408.py > "$B/p00_out_v408.txt" 2>&1 || RC_P00=$?; tail -16 "$B/p00_out_v408.txt"; echo "RC_P00=$RC_P00 (0 = TODAS PASSARAM; 3 = sem falha e com pendente; 1 = falhou)"
echo "== FIM $(date +%T)"
if [ "$RC_CONFERENCIA" != 0 ] || [ "$RC_PINO" != 0 ] || [ "$RC_DIFF_PINOS" != 0 ]; then echo "FALHOU: conferencia=$RC_CONFERENCIA pino=$RC_PINO diff_e_pinos=$RC_DIFF_PINOS"; exit 1; fi
