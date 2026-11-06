#!/bin/sh
# fim_de_cadeia_passos3a7_v409.sh -- (claude-construtor-v409, 05/11/2026) os passos 3 a 7 do fim_de_cadeia_v409.sh, com os MESMOS comandos, para quando o passo 2 (B(n) pre-selo) termina com RC_BN=0, BATERIA_PASSA e producao
# intacta, mas o p00 dele da' NENHUMA FALHA com PENDENTE (o pino do memoria.py, PINO_MEMORIA_PY_v409.json, ato da gerencia) e o grep do fim_de_cadeia (que exige TODAS PASSARAM) para a corrida. O fim_de_cadeia nao e' mudado.
# O passo 7 roda o harness do fechar INTEIRO (a fila da memoria exige o pino REAL); sem o pino, ele recusa, e a parte do fechar e' validada a parte com --sem-fila --pino-emulado (o gerar_relatorio NAO conta essa rodada no portao).
# Nao toca o Nos nem a producao. uso: sh ./fim_de_cadeia_passos3a7_v409.sh > fim_de_cadeia_passos3a7_out_v409.txt 2>&1
V="/c/IALD/Central de Patentes/work/cadeia_de_selo/v409"
cd "$V" || exit 9
PY="python -I -B -X utf8"; PYN="python -B -X utf8"
grep -q "RC_BN=0" bateria_pre_selo/bn_pre_selo_out_v409.txt && grep -q "BATERIA_PASSA" bateria_pre_selo/bn_pre_selo_out_v409.txt || { echo "FALHOU: o B(n) pre-selo nao terminou limpo (RC_BN=0 e BATERIA_PASSA)"; exit 1; }
grep -q "PRECONDICOES v409: NENHUMA FALHA" bateria_pre_selo/bn_pre_selo_out_v409.txt || grep -q "PRECONDICOES v409: TODAS PASSARAM" bateria_pre_selo/bn_pre_selo_out_v409.txt || { echo "FALHOU: o p00 do B(n) tem falha"; exit 1; }
echo "== 3. servico estatico $(date +%T)"
$PY bancada_B3_servico/conferir_exigencias_servico_v409.py | tail -2 || exit 1
$PY bancada_B3_servico/controle_negativo/mutar_conferidor_v409.py | tail -1 || exit 1
echo "== 4. derivacao do pos-rito $(date +%T)"
( cd pos_rito && $PY gerar_derivacao_pos_rito_v409.py | tail -1 )
echo "== 5. harness dos textos $(date +%T)"
( cd pos_rito && $PYN harness_textos_ensaio_v409.py --manter-copias > harness_textos_out_v409.txt 2>&1; echo "RC_HT=$?" >> harness_textos_out_v409.txt )
grep "RC_HT=" pos_rito/harness_textos_out_v409.txt; grep -n "PROBLEMA" pos_rito/harness_textos_out_v409.txt | head -12 | cut -c1-300
echo "== 6. previa do X sobre o Nos emulado $(date +%T)"
$PY pos_rito/gerar_x_custodia_v409.py --nos 'C:\t\h409\harness_saida_v409\nos_emulado' | tail -2 | cut -c1-200
echo "== 7. harness do fechar $(date +%T)"
( cd pos_rito && $PYN harness_fechar_sandbox_v409.py > harness_fechar_out_v409.txt 2>&1; echo "RC_HF=$?" >> harness_fechar_out_v409.txt )
grep "RC_HF=" pos_rito/harness_fechar_out_v409.txt
if [ ! -f PINO_MEMORIA_PY_v409.json ]; then
  echo "== 7b. sem o pino REAL do memoria.py (ato da gerencia): a parte do FECHAR validada com --sem-fila --pino-emulado (nao conta no portao) $(date +%T)"
  ( cd pos_rito && $PYN harness_fechar_sandbox_v409.py --sem-fila --pino-emulado > harness_fechar_sem_fila_out_v409.txt 2>&1; echo "RC_HF_SEM_FILA=$?" >> harness_fechar_sem_fila_out_v409.txt )
  grep "RC_HF_SEM_FILA=" pos_rito/harness_fechar_sem_fila_out_v409.txt; grep -n "PROBLEMA" pos_rito/harness_fechar_sem_fila_out_v409.txt | head -12 | cut -c1-300
fi
echo "== FIM $(date +%T)"
