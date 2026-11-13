#!/bin/sh
# [ADAPTADO v411, 12/11/2026, claude-construtor-v411 (retomada, fork B)] ESCRITO DE NOVO a partir do molde fim_de_cadeia_v410.sh: a mesma ordem (B(n) pre-selo, servico estatico e o controle negativo dele, derivacao do pos-rito, harness dos textos, previa do X, harness do fechar); o B(n) da v411 e' o passo simples B20; os dois modos (o real e o ENSAIO DO TOPO PROPOSTO, V411_ENSAIO_TOPO_PROPOSTO=1) pela pasta de saida LIDA do delta_v411; as saidas antigas vao para <RODADA_PAI>\antes_de_<ts> (fora de work, D135); nenhum codigo de saida mascarado por pipe
# fim_de_cadeia_v411.sh -- o que vem DEPOIS do p00 na cadeia da v411 (cadeia_v411.sh, passo 15), numa ordem so', parando na primeira falha VISIVEL (cada passo grava a sua saida em arquivo e o codigo de saida e' conferido; o molde mascarava alguns por pipe):
# 1. as saidas antigas do B(n) pre-selo e do servico (os scripts recusam sobrescrever) para <RODADA_PAI>\antes_de_<ts>\ (fora de work) e o sandbox curto C:\t\vb22 ausente (vazio: apagado; com conteudo: PARA);
# 2. o B(n) pre-selo (bateria_pre_selo\rodar_bn_pre_selo_v411.sh: so' ensaio contra o Nos da v410, a producao so' lida; o p00 dentro dele sem FALHA, so' com os pendentes que sao atos da gerencia);
# 3. o servico estatico (conferir_exigencias_servico_v411.py) e o controle negativo dele (mutar_conferidor_v411.py); 4. a derivacao do pos-rito; 5. o harness dos textos (com copias); 6. a previa do X sobre o Nos emulado; 7. o harness do fechar.
# Os passos 4 a 7 sao da OUTRA frente (pos_rito\): chamados PELO NOME, sem editar os arquivos dela. Nao toca o Nos nem a producao, nao instala, nao roda o rito. A purga corre por fora (~20 min: purga_v411.py --listar), como na v410.
# uso: sh ./fim_de_cadeia_v411.sh > <SAIDA>/fim_de_cadeia_out_v411.txt 2>&1     (no ensaio do topo proposto: V411_ENSAIO_TOPO_PROPOSTO=1 sh ./fim_de_cadeia_v411.sh ...)
cd "$(dirname "$0")" || exit 9
V="$(pwd)"
PY="/c/Python314/python.exe -I -B -X utf8"; PYN="/c/Python314/python.exe -B -X utf8"
LIDO=$($PY -c "import importlib.util as u,sys; s=u.spec_from_file_location('d',sys.argv[1]); m=u.module_from_spec(s); s.loader.exec_module(m); print(m.SAIDA); print(m.RODADA_PAI); print(int(m.ENSAIO_TOPO_PROPOSTO)); print(m.MANIFESTO_ARQ)" "$(cygpath -w "$V/delta_v411.py")" | tr -d '\r')
SAIDA_W=$(echo "$LIDO" | sed -n 1p); PAI_W=$(echo "$LIDO" | sed -n 2p); ENSAIO=$(echo "$LIDO" | sed -n 3p); MANI_W=$(echo "$LIDO" | sed -n 4p)
[ -n "$SAIDA_W" ] && [ -n "$PAI_W" ] && [ -n "$MANI_W" ] || { echo "FALHOU: a pasta de saida nao foi lida do delta_v411"; exit 9; }
OS=$(cygpath -u "$SAIDA_W"); OPAI=$(cygpath -u "$PAI_W"); OB="$OS/bateria_pre_selo"
[ -f "$(cygpath -u "$MANI_W")" ] || { echo "FALHOU: o manifesto do artefato desta rodada nao existe ($MANI_W): o fim da cadeia vem depois do candidato (ou do artefato de ensaio)"; exit 9; }
echo "== modo: $([ "$ENSAIO" = 1 ] && echo 'ENSAIO DO TOPO PROPOSTO (nada aqui e candidato)' || echo 'real') | saida: $SAIDA_W | rodada: $PAI_W $(date +%T)"
TS=$(date +%Y%m%d_%H%M%S); D="$OPAI/antes_de_${TS}_fim_de_cadeia"
echo "== 1. saidas antigas para $D $(date +%T)"
mkdir -p "$D" || exit 9
for a in "$OB/ensaio_1" "$OB/prova_producao" "$OB/conferencia_pelo_esboco_v411.json" "$OB/LIMPEZA_SANDBOX_vb22.json" "$OB/etapa1_stdout.txt" "$OB/bn_pre_selo_out_v411.txt" "$OB/conferencia_out_v411.txt" "$OB/pino_out_v411.txt" \
         "$OB/diff_e_pinos_out_v411.txt" "$OB/p00_out_v411.txt" "$OS/PROVA_PRODUCAO_INTACTA_v411_pre_selo.json" "$OS/PINO_RECIBO_PRE_SELO_v411.json" \
         "$OS/bancada_B3_servico/CONFERENCIA_EXIGENCIAS_SERVICO_v411.json" "$OS/bancada_B3_servico/controle_negativo/RESULTADO_CONTROLE_NEGATIVO_v411.json"; do
  if [ -e "$a" ]; then r=$(echo "$a" | sed "s#^$OS/##" | tr '/' '_'); mv "$a" "$D/$r" || { echo "FALHOU: nao movi $a"; exit 1; }; fi
done
$PY -c "
import os
p = 'C:' + os.sep + 't' + os.sep + 'vb22'
if os.path.exists(p):
    assert not os.listdir(p), ('C:/t/vb22 nao esta vazia', os.listdir(p))
    os.rmdir(p)
print('vb22 ausente')" || { echo "FALHOU: vb22"; exit 1; }
mkdir -p "$OB" "$OS/bancada_B3_servico/controle_negativo" "$OS/pos_rito"
echo "== 2. B(n) pre-selo $(date +%T)"
( cd bateria_pre_selo && sh ./rodar_bn_pre_selo_v411.sh > "$OB/bn_pre_selo_out_v411.txt" 2>&1; echo "RC_BN=$?" >> "$OB/bn_pre_selo_out_v411.txt" )
if grep -q "Traceback\|ja existe, nao\|NAO RODO" "$OB/bn_pre_selo_out_v411.txt" || ! grep -q "RC_BN=0" "$OB/bn_pre_selo_out_v411.txt"; then echo "FALHOU: B(n) pre-selo (ver $OB/bn_pre_selo_out_v411.txt)"; grep -n "Traceback\|ja existe, nao\|NAO RODO\|FALHOU\|RC_" "$OB/bn_pre_selo_out_v411.txt" | head; exit 1; fi
# o p00 dentro do B(n): nenhuma FALHA; pendente so' o que e' ato da gerencia (o pino do memoria.py e a folga do MEMORY.md; no ensaio, tambem o topo ratificado e o candidato, que o ensaio nao tem)
$PY -c "
import json, sys, importlib.util as u
s = u.spec_from_file_location('d', sys.argv[1]); m = u.module_from_spec(s); s.loader.exec_module(m)
p = json.load(open(m.saida('PRECONDICOES_v411.json'), encoding='utf-8'))
ok_pend = ('PINO_MEMORIA_PY_v411.json', 'a folga do MEMORY.md', 'as citacoes em ') + (('TOPO_RATIFICADO_v411.json', 'o candidato um_v411_candidato.py') if m.ENSAIO_TOPO_PROPOSTO else ())
ruins = [x['checagem'] for x in p.get('pendentes') or [] if not str(x.get('checagem', '')).startswith(ok_pend)]
print('p00 no B(n):', p.get('veredito'), '| falhas', p.get('n_falhas'), '| pendentes que nao sao atos da gerencia:', ruins)
sys.exit(0 if p.get('n_falhas') == 0 and not ruins else 1)" "$(cygpath -w "$V/delta_v411.py")" || { echo "FALHOU: o p00 do B(n) pre-selo tem FALHA ou pendente que nao e' ato da gerencia"; exit 1; }
[ -e /c/t/vb22 ] && { echo "FALHOU: vb22 ficou"; exit 1; }
echo "== 3. servico estatico e o controle negativo dele $(date +%T)"
$PY bancada_B3_servico/conferir_exigencias_servico_v411.py > "$OS/bancada_B3_servico/conferir_out_v411.txt" 2>&1; RC=$?; tail -3 "$OS/bancada_B3_servico/conferir_out_v411.txt" | cut -c1-400
[ "$RC" -eq 0 ] || { echo "FALHOU: servico estatico rc=$RC"; exit 1; }
$PY bancada_B3_servico/controle_negativo/mutar_conferidor_v411.py > "$OS/bancada_B3_servico/controle_negativo/mutar_out_v411.txt" 2>&1; RC=$?; tail -2 "$OS/bancada_B3_servico/controle_negativo/mutar_out_v411.txt" | cut -c1-300
[ "$RC" -eq 0 ] || { echo "FALHOU: controle negativo do servico rc=$RC"; exit 1; }
[ -e /c/t/vb22 ] && { echo "FALHOU: vb22 ficou depois do controle negativo"; exit 1; }
echo "== 4. derivacao do pos-rito (outra frente: pos_rito/gerar_derivacao_pos_rito_v411.py) $(date +%T)"
( cd pos_rito && $PY gerar_derivacao_pos_rito_v411.py > "$OS/pos_rito/derivacao_out_v411.txt" 2>&1; echo "RC_DER=$?" >> "$OS/pos_rito/derivacao_out_v411.txt" ); tail -2 "$OS/pos_rito/derivacao_out_v411.txt" | cut -c1-300
grep -q "RC_DER=0" "$OS/pos_rito/derivacao_out_v411.txt" || { echo "FALHOU: derivacao do pos-rito"; exit 1; }
echo "== 5. harness dos textos (outra frente: pos_rito/harness_textos_ensaio_v411.py) $(date +%T)"
( cd pos_rito && $PYN harness_textos_ensaio_v411.py --manter-copias > "$OS/pos_rito/harness_textos_out_v411.txt" 2>&1; echo "RC_HT=$?" >> "$OS/pos_rito/harness_textos_out_v411.txt" )
grep -q "RC_HT=0" "$OS/pos_rito/harness_textos_out_v411.txt" || { echo "FALHOU: harness dos textos"; grep -n "PROBLEMA" "$OS/pos_rito/harness_textos_out_v411.txt" | head -12 | cut -c1-300; exit 1; }
echo "== 6. previa do X sobre o Nos emulado (outra frente: pos_rito/gerar_x_custodia_v411.py) $(date +%T)"
$PY pos_rito/gerar_x_custodia_v411.py --nos 'C:\t\h411\harness_saida_v411\nos_emulado' > "$OS/pos_rito/previa_x_out_v411.txt" 2>&1; RC=$?; tail -2 "$OS/pos_rito/previa_x_out_v411.txt" | cut -c1-200
[ "$RC" -eq 0 ] || { echo "FALHOU: previa do X rc=$RC"; exit 1; }
echo "== 7. harness do fechar (outra frente: pos_rito/harness_fechar_sandbox_v411.py) $(date +%T)"
( cd pos_rito && $PYN harness_fechar_sandbox_v411.py > "$OS/pos_rito/harness_fechar_out_v411.txt" 2>&1; echo "RC_HF=$?" >> "$OS/pos_rito/harness_fechar_out_v411.txt" )
grep -q "RC_HF=0" "$OS/pos_rito/harness_fechar_out_v411.txt" || { echo "FALHOU: harness do fechar"; grep -n "PROBLEMA" "$OS/pos_rito/harness_fechar_out_v411.txt" | head -12 | cut -c1-300; exit 1; }
echo "== FIM $(date +%T)"
