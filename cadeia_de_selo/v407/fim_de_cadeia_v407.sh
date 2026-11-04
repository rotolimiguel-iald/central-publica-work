#!/bin/sh
# fim_de_cadeia_v407.sh -- (adaptado em 03/11/2026; nenhum nome do bundle entra aqui: o corpo e' independente do numero de modulos, e os arquivos que ele chama foram conferidos um a um) o que vem DEPOIS de refazer_candidato_v407.sh --regerar, numa ordem so', parando na primeira falha VISIVEL (os scripts do B(n) mascaram falha por pipe; aqui o resultado e' conferido por grep e pelos JSON):
# 1. guarda aside as saidas do B(n) pre-selo e do servico (os scripts recusam sobrescrever) em antes_de_<ts>/; 2. B(n) pre-selo; 3. servico estatico e controle negativo; 4. derivacao do pos-rito; 5. harness dos textos (com copias); 6. harness do fechar; 7. previa do X sobre o Nos emulado.
# Nao toca o Nos nem a producao, nao instala, nao roda o rito. A purga corre por fora (python -I -B -X utf8 purga_v407.py --listar > purga_out_v407.txt), porque leva 20 min. uso: sh ./fim_de_cadeia_v407.sh > fim_de_cadeia_out_v407.txt 2>&1
V="/c/IALD/Central de Patentes/work/cadeia_de_selo/v407"
cd "$V" || exit 9
TS=$(date +%Y%m%d_%H%M%S); D="antes_de_$TS"; mkdir -p "$D"
PY="python -I -B -X utf8"; PYN="python -B -X utf8"
echo "== 1. saidas antigas para $D $(date +%T)"
for a in bateria_pre_selo/ensaio_1 bateria_pre_selo/prova_producao bateria_pre_selo/conferencia_pelo_esboco_v407.json bateria_pre_selo/LIMPEZA_SANDBOX_vb21.json bateria_pre_selo/etapa1_stdout.txt PROVA_PRODUCAO_INTACTA_v407_pre_selo.json PINO_RECIBO_PRE_SELO_v407.json bancada_B3_servico/CONFERENCIA_EXIGENCIAS_SERVICO_v407.json bancada_B3_servico/controle_negativo/RESULTADO_CONTROLE_NEGATIVO_v407.json; do
  [ -e "$a" ] && mv "$a" "$D/" || true
done
python -B -X utf8 -c "
import os
p = 'C:' + os.sep + 't' + os.sep + 'vb21'
if os.path.exists(p):
    assert not os.listdir(p), ('C:/t/vb21 nao esta vazia', os.listdir(p))
    os.rmdir(p)
print('vb21 ausente')"
[ $? -eq 0 ] || { echo "FALHOU: vb21"; exit 1; }
echo "== 2. B(n) pre-selo $(date +%T)"
( cd bateria_pre_selo && sh ./rodar_bn_pre_selo_v407.sh > bn_pre_selo_out_v407.txt 2>&1; echo "RC_BN=$?" >> bn_pre_selo_out_v407.txt )
if grep -q "Traceback\|ja existe, nao\|NAO RODO" bateria_pre_selo/bn_pre_selo_out_v407.txt || ! grep -q "PRECONDICOES v407: TODAS PASSARAM" bateria_pre_selo/bn_pre_selo_out_v407.txt || ! grep -q "RC_BN=0" bateria_pre_selo/bn_pre_selo_out_v407.txt; then echo "FALHOU: B(n) pre-selo (ver bateria_pre_selo/bn_pre_selo_out_v407.txt)"; grep -n "Traceback\|ja existe, nao\|NAO RODO\|FALHOU" bateria_pre_selo/bn_pre_selo_out_v407.txt | head; exit 1; fi
[ -e /c/t/vb21 ] && { echo "FALHOU: vb21 ficou"; exit 1; }
echo "== 3. servico estatico $(date +%T)"
$PY bancada_B3_servico/conferir_exigencias_servico_v407.py | tail -2 || exit 1
$PY bancada_B3_servico/controle_negativo/mutar_conferidor_v407.py | tail -1 || exit 1
echo "== 4. derivacao do pos-rito $(date +%T)"
( cd pos_rito && $PY gerar_derivacao_pos_rito_v407.py | tail -1 )
echo "== 5. harness dos textos $(date +%T)"
( cd pos_rito && $PYN harness_textos_ensaio_v407.py --manter-copias > harness_textos_out_v407.txt 2>&1; echo "RC_HT=$?" >> harness_textos_out_v407.txt )
grep -q "RC_HT=0" pos_rito/harness_textos_out_v407.txt || { echo "FALHOU: harness dos textos"; grep -n "PROBLEMA" pos_rito/harness_textos_out_v407.txt | head -12 | cut -c1-300; exit 1; }
echo "== 6. previa do X sobre o Nos emulado $(date +%T)"
$PY pos_rito/gerar_x_custodia_v407.py --nos 'C:\t\h407\harness_saida_v407\nos_emulado' | tail -2 | cut -c1-200
echo "== 7. harness do fechar $(date +%T)"
( cd pos_rito && $PYN harness_fechar_sandbox_v407.py > harness_fechar_out_v407.txt 2>&1; echo "RC_HF=$?" >> harness_fechar_out_v407.txt )
grep -q "RC_HF=0" pos_rito/harness_fechar_out_v407.txt || { echo "FALHOU: harness do fechar"; grep -n "PROBLEMA" pos_rito/harness_fechar_out_v407.txt | head -12 | cut -c1-300; exit 1; }
echo "== FIM $(date +%T)"
