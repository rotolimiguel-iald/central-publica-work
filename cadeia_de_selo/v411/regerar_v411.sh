#!/bin/sh
# [ADAPTADO v411, 12/11/2026, claude-construtor-v411 (retomada, fork A)] do molde v410/regerar_v410.sh para uma versao SEM modulo novo: a guarda do sandbox deixa de conferir um bundle (nao ha) e passa a conferir que as FONTES do sandbox k411c sao as do kernel do Nos v410 (conferir_fontes_k410c_vs_nos_v411.py); build incremental, pos_build, insumos e refazer_candidato
# regerar_v411.sh -- refaz, NA ORDEM, o que depende do KERNEL e dos INSUMOS da v411 (a v411 NAO tem modulo novo: o kernel e' o da v410 byte a byte): (a) guarda do sandbox (as fontes de C:\t\k411c\final == as do kernel do Nos v410, por sha256),
# (b) construir_kernel_v411.sh (`lake build` incremental, nada a compilar, + Audit no sandbox), (c) pos_build_kernel_v411.py (FLAGS, KH_N1, KERNEL_RECIBO, POS_BUILD), (d) copiar_insumos_v411.py e (e) refazer_candidato_v411.sh --regerar
# (a cadeia inteira). Nao toca o Nos, nao instala, nao roda o rito. O QUE ESTE SCRIPT NAO FAZ (decisao da gerencia): montar o sandbox (ele nasce de `sh ./copiar_k411c.sh`, robocopy de C:\t\k410c\final SEM /PURGE). O kernel ja' esta' medido
# (PRONTO_PARA_CANDIDATO_v411.json): NAO refazer o build nem o Audit sem mudanca de fonte. O build incremental levou 85 s e o Audit 432 s (kernel/construir_marcas.txt, 12/11/2026). Depois: python -I -B -X utf8 purga_v411.py (tem de dar ZERO; ~20 min, por fora).
# uso: sh ./regerar_v411.sh   (cada passo para na primeira falha; nenhum passo e' mascarado por pipe)
set -e
V="/c/IALD/Central de Patentes/work/cadeia_de_selo/v411"
cd "$V"
PY="python -I -B -X utf8"
echo "== a. guarda do sandbox: as fontes de C:\\t\\k411c\\final == as do kernel do Nos v410 selado (sha256; nada so' num lado) $(date +%T)"
$PY conferir_fontes_k410c_vs_nos_v411.py "C:\\t\\k411c\\final" CONFERENCIA_FONTES_K411C_v411.json > /tmp/regerar_a_v411.txt; tail -1 /tmp/regerar_a_v411.txt
$PY -c "
import json
c = json.load(open('CONFERENCIA_FONTES_K411C_v411.json', encoding='utf-8'))
assert c['identico'] is True and c['n_diferentes'] == 0, c.get('n_diferentes')
print('sandbox k411c == kernel do Nos v410:', c['n_comuns'], 'arquivos comuns, 0 diferentes')"
echo "== b. construir_kernel_v411.sh (lake build incremental + Audit; marcas em kernel/construir_marcas.txt) $(date +%T)"; sh ./construir_kernel_v411.sh
echo "== c. pos_build_kernel_v411.py (tem de dar VERDE)"; $PY pos_build_kernel_v411.py > /tmp/regerar_c_v411.txt; tail -1 /tmp/regerar_c_v411.txt
echo "== d. copiar_insumos_v411.py"; $PY copiar_insumos_v411.py > /tmp/regerar_d_v411.txt; tail -1 /tmp/regerar_d_v411.txt
echo "== e. refazer_candidato_v411.sh --regerar $(date +%T)"; sh ./refazer_candidato_v411.sh --regerar
echo "== FIM $(date +%T)"
