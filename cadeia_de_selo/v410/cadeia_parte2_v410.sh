#!/bin/sh
# cadeia_parte2_v410.sh -- [claude-construtor-v410, 09/11/2026, parte 2: D86/D87 + a RETOMADA] a cadeia INTEIRA da v410, UMA vez, lancada DESACOPLADA do VS Code (PowerShell Start-Process -> bash --login; a saida vai a cadeia_parte2_out_v410.txt e o PID a cadeia_parte2_pid_v410.txt),
# parando na primeira falha VISIVEL e gravando ESTADO_PARTE2_v410.json a cada etapa concluida (a retomada e' possivel so' do disco):
#   perna1: refazer_candidato_v410.sh (gerar [identico], comparar, ensaio a seco, esperados, conferidores, citacoes, diff e pinos, instalar/rito, p00) + a conferencia pelos arquivos;
#   (entre as pernas) a pendencia do MEMORY.md no p00: se o indice real nao comporta o handoff novo, PARA com rc 3 (so' a gerencia escreve o MEMORY.md); retomar com: sh ./cadeia_parte2_v410.sh perna2
#   perna2: fim_de_cadeia_v410.sh (B(n) pre-selo, servico estatico, derivacao do pos-rito, harnesses, previa do X) -> purga_v410.py --listar -> gerar_relatorio_v410.py (PREPARACAO_v410_PRONTA.json) -> depositar_construtor_v410.py (fila + Mapa), este so' com pronta = true.
# Nao toca o Nos nem a producao, nao instala, nao roda o rito, nao toca o MEMORY.md nem o treino do Qwen.   uso: sh ./cadeia_parte2_v410.sh [tudo|perna1|perna2]
V="/c/IALD/Central de Patentes/work/cadeia_de_selo/v410"
cd "$V" || exit 9
MODO="${1:-tudo}"
PY="python -I -B -X utf8"; PYN="python -B -X utf8"
passo() { echo "=== [$(date +%T)] $1"; }
estado() { e_="$1"; p_="$2"; shift 2; $PY _estado_parte2_v410.py "$e_" "$p_" "$@" > /dev/null 2>&1 || echo "AVISO: o ESTADO_PARTE2 nao foi gravado: $e_"; }
falha() { passo "FALHOU: $1"; estado "CADEIA DA PARTE 2 PAROU ($MODO): $1" "diagnosticar pelo cadeia_parte2_out_v410.txt e pelo arquivo citado; a cadeia nao se repete sem a causa conhecida e corrigida" cadeia_parte2_out_v410.txt; echo "CADEIA_PARTE2_RC=1"; exit 1; }
echo "$$" > cadeia_parte2_shpid_v410.txt
T0=$(date +%s)
passo "cadeia da parte 2, modo $MODO | candidato $(sha256sum um_v410_candidato.py | cut -c1-16) | CANDIDATO_v410.json $(sha256sum CANDIDATO_v410.json | cut -c1-16)"
if [ "$MODO" = "tudo" ] || [ "$MODO" = "perna1" ]; then
  C0=$(sha256sum um_v410_candidato.py | cut -c1-64)
  passo "perna1: refazer_candidato_v410.sh (sem --regerar: o gerador tem de reproduzir o candidato identico)"
  sh ./refazer_candidato_v410.sh > refazer_out_v410.txt 2>&1; RC=$?
  echo "RC_REFAZER=$RC" >> refazer_out_v410.txt   # (o codigo de saida REAL desta passada, escrito por quem a chamou, como a cadeia sempre fez; o gerar_relatorio le o FIM e este RC)
  tail -14 refazer_out_v410.txt | cut -c1-500
  [ "$RC" -eq 0 ] || falha "refazer_candidato rc=$RC (ver refazer_out_v410.txt; se foi o ensaio, ensaio_out.txt)"
  grep -q "^== FIM" refazer_out_v410.txt || falha "refazer_candidato nao chegou ao FIM"
  grep -q "Traceback" refazer_out_v410.txt && falha "ha' Traceback no refazer_out_v410.txt (um passo mascarado por pipe caiu)"
  [ "$(sha256sum um_v410_candidato.py | cut -c1-64)" = "$C0" ] || falha "o candidato mudou de bytes no refazer (o gerador nao reproduziu o identico)"
  $PY _conferir_pernas_parte2_v410.py perna1 "$T0" || falha "a conferencia da perna1 pelos arquivos"
  estado "perna1 da cadeia concluida: refazer_candidato (gerar identico, comparar, ensaio a seco TUDO PASSOU, ESPERADOS, conferidor positivo TUDO BATE e controle negativo, citacoes, pinos, instalar/rito, p00 sem falha)" "a pendencia do MEMORY.md no p00 e a perna2 (fim_de_cadeia, purga, gerar_relatorio, deposito)" um_v410_candidato.py CANDIDATO_v410.json ensaio_a_seco_v410.json ESPERADOS_v410.json conferencia_rito_v410_POSITIVO_FALSO_NOS.json conferir_citacoes_v410.json PINOS_BN_v410.json DERIVACAO_v410.json PRECONDICOES_v410.json refazer_out_v410.txt
  passo "perna1 concluida"
fi
if [ "$MODO" = "perna1" ]; then echo "CADEIA_PARTE2_RC=0 (so' a perna1)"; exit 0; fi
# ---- entre as pernas: o MEMORY.md real comporta o handoff novo? (o p00 simula a superficie sobre o indice real; so' a gerencia escreve o MEMORY.md)
passo "p00 de novo (so' para medir a pendencia do MEMORY.md antes do B(n) pre-selo)"
$PY p00_precondicoes_v410.py > p00_entre_pernas_out_v410.txt 2>&1; RCP=$?
grep -a "^FALHA\|PRECONDICOES v410:" p00_entre_pernas_out_v410.txt | cut -c1-700
[ "$RCP" -eq 1 ] && falha "o p00 tem FALHA (ver p00_entre_pernas_out_v410.txt)"
$PY _conferir_pernas_parte2_v410.py memory; RCM=$?
if [ "$RCM" -eq 3 ]; then
  passo "PARADA (nao e' falha da cadeia): o MEMORY.md real NAO comporta o handoff novo; so' a gerencia escreve o MEMORY.md. Retomar depois com: sh ./cadeia_parte2_v410.sh perna2"
  estado "cadeia PARADA entre as pernas: o MEMORY.md real nao comporta o handoff novo (o p00 da' PENDENTE e o B(n) pre-selo exige TODAS PASSARAM); a perna1 esta' concluida" "a gerencia tira do indice o que falta (so' ela escreve o MEMORY.md); depois: sh ./cadeia_parte2_v410.sh perna2 (desacoplado)" PRECONDICOES_v410.json p00_entre_pernas_out_v410.txt
  echo "CADEIA_PARTE2_RC=3"; exit 3
fi
[ "$RCM" -eq 0 ] || falha "a leitura da pendencia do MEMORY.md no PRECONDICOES_v410.json"
T1=$(date +%s)
passo "perna2: fim_de_cadeia_v410.sh"
sh ./fim_de_cadeia_v410.sh > fim_de_cadeia_out_v410.txt 2>&1; RC=$?
cut -c1-400 fim_de_cadeia_out_v410.txt | tail -30
[ "$RC" -eq 0 ] || falha "fim_de_cadeia rc=$RC (ver fim_de_cadeia_out_v410.txt)"
grep -q "^== FIM" fim_de_cadeia_out_v410.txt || falha "fim_de_cadeia nao chegou ao FIM"
grep -q "^FALHOU\|Traceback" fim_de_cadeia_out_v410.txt && falha "fim_de_cadeia traz FALHOU ou Traceback"
estado "fim_de_cadeia concluido (B(n) pre-selo, servico estatico, derivacao do pos-rito, harness dos textos, previa do X, harness do fechar)" "purga_v410.py --listar (~20 min), gerar_relatorio, deposito" fim_de_cadeia_out_v410.txt PINO_RECIBO_PRE_SELO_v410.json PROVA_PRODUCAO_INTACTA_v410_pre_selo.json pos_rito/HARNESS_TEXTOS_ENSAIO_v410.json pos_rito/HARNESS_FECHAR_SANDBOX_v410.json
passo "purga_v410.py --listar (so' leitura; ~20 min)"
$PY purga_v410.py --listar > purga_out_v410.txt 2>&1; RC=$?
tail -3 purga_out_v410.txt | cut -c1-400
[ "$RC" -eq 0 ] || falha "a purga achou ocorrencia ou caiu (rc=$RC; ver purga_out_v410.txt e purga_v410.json)"
passo "p00 final (depois do B(n) pre-selo, dos harnesses e da purga)"
$PY p00_precondicoes_v410.py > p00_final_out_v410.txt 2>&1; RCP=$?
grep -a "^FALHA\|^PEND\|PRECONDICOES v410:" p00_final_out_v410.txt | cut -c1-500
$PY _conferir_pernas_parte2_v410.py perna2 "$T1" || falha "a conferencia da perna2 pelos arquivos (p00 rc=$RCP)"
estado "purga com zero ocorrencias e p00 final TODAS PASSARAM" "gerar_relatorio_v410.py (PREPARACAO_v410_PRONTA.json) e o deposito do construtor" purga_v410.json PRECONDICOES_v410.json
passo "gerar_relatorio_v410.py"
$PYN gerar_relatorio_v410.py > gerar_relatorio_out_v410.txt 2>&1; RC=$?
tail -4 gerar_relatorio_out_v410.txt | cut -c1-600
[ "$RC" -eq 0 ] || falha "gerar_relatorio rc=$RC (ver gerar_relatorio_out_v410.txt)"
PRONTA=$($PY -c "import json; j = json.load(open('PREPARACAO_v410_PRONTA.json', encoding='utf-8')); print('SIM' if j.get('pronta') is True else 'NAO: ' + json.dumps(j.get('falta'), ensure_ascii=False)[:900])")
passo "PREPARACAO_v410_PRONTA.json: pronta = $PRONTA | sha16 $(sha256sum PREPARACAO_v410_PRONTA.json | cut -c1-16)"
if [ "$PRONTA" != "SIM" ]; then
  estado "gerar_relatorio rodou e a PREPARACAO NAO esta' pronta: $PRONTA" "ler PREPARACAO_v410_PRONTA.json (falta, portoes) e decidir; o deposito do construtor NAO foi feito" PREPARACAO_v410_PRONTA.json RELATORIO_PREPARACAO_v410.md PLANO_v410.md
  echo "CADEIA_PARTE2_RC=4"; exit 4
fi
estado "PREPARACAO_v410_PRONTA.json gravada com pronta = true" "depositar_construtor_v410.py (a fila da memoria, quem = a pasta do construtor, e a rota no Mapa)" PREPARACAO_v410_PRONTA.json RELATORIO_PREPARACAO_v410.md PLANO_v410.md um_v410_candidato.py CANDIDATO_v410.json kernel/KERNEL_RECIBO_v410.json ESPERADOS_v410.json PRECONDICOES_v410.json
passo "depositar_construtor_v410.py (a fila da memoria e a rota no Mapa)"
$PY depositar_construtor_v410.py > depositar_construtor_out_v410.txt 2>&1; RC=$?
tail -6 depositar_construtor_out_v410.txt | cut -c1-500
[ "$RC" -eq 0 ] || falha "depositar_construtor rc=$RC (ver depositar_construtor_out_v410.txt)"
estado "CADEIA DA PARTE 2 CONCLUIDA: PREPARACAO pronta, deposito na fila e rota no Mapa" "relatorio final a gerencia (ate' 15 linhas, com os sha16)" PREPARACAO_v410_PRONTA.json depositar_construtor_out_v410.txt
passo "FIM DA CADEIA DA PARTE 2 ($(( $(date +%s) - T0 )) s)"
echo "CADEIA_PARTE2_RC=0"
