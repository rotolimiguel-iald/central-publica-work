#!/bin/sh
# v394 (19/10): CADEIA POS-RITO -- no molde do chain_pos_rito_v393.sh (derivada por derivar_cadeia_v394.py; mesma ordem de passos 0..14 e mesmos portoes). O rito ja terminou (rito_v394.sh em segundo plano;
# RITO_RC=<rc> no fim do Nos\rodada_v394_stdout.txt). A v394 acrescenta o tempo e a frequencia (TimeGraviton*), a regra quadratica (RuleQuadraticResidual), a rede de Fock/Takesaki/Maxwell (F1Fecho394/*, 189 modulos novos)
# e os registros tempo_frequencia_v394, regra_quadratica_v394, rede_fock_v394, cunhagens_v394 e kh_n1_cobertura_v394.
# ORDEM: 0 guardas -> 1 o CONFERIDOR (copia byte a byte; so leitura do Nos) -> 2 a LEITURA (PROBLEMAS param) -> 3 ENSAIO das superficies em COPIAS (o plano e' conferido antes da primeira escrita; a arvore em dry;
# o sha16 da v394 na arvore (dry) e os marcadores do passo 9 nas COPIAS, conferidos ANTES de qualquer escrita real) -> 4 patch arvore/indice (OPCIONAL: so' se existir patch_arvore_indice_v394.py) -> 5 a arvore
# -> 6 atlas+indice -> 7 superficies reais (appends datados; SEM errata nova no CLAUDE.md da raiz) -> 8 porta_memoria.py (o ATLAS a mao nao se toca) -> 9 regra da linhagem completa COM O MARCADOR DO SELO (zero e'
# falha visivel) e a guarda de MEMORY.md (<24.000 B, <=195 linhas) -> 10 B(3) da Bancada, ENSAIO pos-selo -> 10a parada do servico (AGUARDA_OPERADOR) -> 10b B(3) APLICAR (so com B3_AUTORIZADO=sim e o evento c1)
# -> 10c religamento (AGUARDA_OPERADOR) -> 11 fechar -> 12 registrar_mapa (so MONTA o JSON e o comando) -> 13 inventario da bancada Lean -> 14 Nos vivo.
# Sai na primeira reprovacao e NAO restaura nada sozinha: a decisao de restaurar e' da gerencia. Retomada: CHAIN_DE=<passo> (e CHAIN_ATE=<passo>); os passos 3 a 9 sao idempotentes.
# Ambiente: B3_AUTORIZADO=sim, EVENTO=<seq> e EVENTO_HASH=<hash16> (so o 10b); V394_AVISO_REIVINDICACAO=<texto> (so' com ela o AVISO_GERENCIA.md e' escrito; sem ela e' PULADO e dito).
# Os pinos do B(n) vem de PINOS_BN_v394.json (lidos na hora; hash nunca de memoria). Sem o PINO recibo_pre_selo (a fase pre_selo da B(n) nao foi preparada) o 10 PARA em AGUARDA_OPERADOR.
# textos_v394.py, o handoff de fechar_v394.py e registrar_mapa_v394.py RECUSAM rodar enquanto tiverem trecho marcado para reescrever (as narrativas da v393 saem com a subida mecanica): os passos 0 a 2 nao os usam.
# Codigos de saida: 0 fim; 1 reprovacao (PARADA); 20 AGUARDA_OPERADOR (parada de proposito, nao e' falha).
# R3.5 (19/10/2026, depois da revisao independente EXAME_DELTA_E_R3_4.md): o PASSO 10 (10, 10a, 10b, 10c) e o helper b3_recibo_v394.py foram RE-DERIVADOS pela §7 do RESULTADO_R3_4.md com o esboco R3.5 (R3_5/_construcao/derivar_passo10_r35.py;
# NAO se rodou derivar_cadeia_v394.py): o B(n) e' o SALTO v392 -> v394 (a Bancada de producao pina a v392; o elo da v393 nunca rodou). Os pinos vem de PINOS_BN_v394.json FUNDIDO com o que e' da R3.4/R3.5 (esboco_R3_5, cadeia_de_selos,
# recibo_pre_selo 0d82d598 da R3.4, kernel_recibo R3_4 com modulos_de_auditoria, selo/manifesto do kernel da v393, gerador_bateria, driver_t12_t14, bateria_base_R2); a BATERIA da v394 e' GERADA por script no 10 (depois do selo; bateria por versao)
# e pinada ao lado (bateria_pos_selo/PINOS_BATERIA_v394.json); o 10 e o 10b passam --cadeia-de-selos; o 10b exige o evento c1 que nomeia a v394. Os passos 0 a 9, 10a, 10c e 11 a 14 estao como antes.
PK="/c/IALD/Central de Patentes/work/cadeia_de_selo/v394"; SEL="$PK/pos_rito"
TOOLS="/c/IALD/Central de Patentes/work/cadeia_de_selo"
NOS="/c/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós"
UMEM="/c/Users/rotol/.claude/projects/c--IALD-Central-de-Patentes/memory"
ATLD="/c/IALD/Central de Patentes/memory"
HAJA="/c/IALD/Artigo/Haja_Luz/CLAUDE.md"
RAIZ_CLAUDE="/c/IALD/CLAUDE.md"
AVISO="/c/IALD/Central de Patentes/Chatgpt/TUNEL/DO_CHATGPT/ORDEM_019/AVISO_GERENCIA.md"
PORTA="/c/LAR_MIGUEL/porta_memoria.py"
INV="/c/IALD/Central de Patentes/work/inventario_bancada"
CONFOUT="$SEL/conferidor"; ENS="$SEL/ensaio_superficies"; ENST="$SEL/ensaio_ferramentas"
PY="python -I -B -X utf8"; PY_B="python -B -X utf8"
unset TGL_RITE_CHECKPOINT TGL_CACHE_DIR
export PYTHONIOENCODING=utf-8
set -e
parar() { echo "PARADA: $*"; echo "(nada foi restaurado: a decisao de restaurar e da gerencia)"; exit 1; }
TOPICOS="missao-ultima-flag-um-py.md central-de-patentes-estado.md estatuto-da-prova-07out.md"
# o NOME do topico novo e' lido de textos_v394.TOPICO_NOVO (uma fonte so'); so' roda onde e' usado (passos 3 e 9): o textos_v394.py recusa importar com trecho marcado para reescrever
topico_novo() { $PY -c "import sys;sys.path.insert(0,sys.argv[1]);import textos_v394 as T;print(T.TOPICO_NOVO)" "$(cygpath -w "$SEL")"; }
aguarda() { echo "AGUARDA_OPERADOR: $*"; echo "(a cadeia parou de proposito, nao e' falha; retomar com CHAIN_DE=<passo>)"; exit 20; }
ORDEM="0 1 2 3 4 5 6 7 8 9 10 10a 10b 10c 11 12 13 14"
DE="${CHAIN_DE:-0}"; ATE="${CHAIN_ATE:-14}"
pos() { i=0; for x in $ORDEM; do if [ "$x" = "$1" ]; then echo "$i"; return 0; fi; i=$((i+1)); done; echo "-1"; }
quer() { p=$(pos "$1"); d=$(pos "$DE"); a=$(pos "$ATE"); if [ "$d" -lt 0 ] || [ "$a" -lt 0 ]; then echo "CHAIN_DE/CHAIN_ATE desconhecido (validos: $ORDEM)"; exit 1; fi; [ "$p" -ge "$d" ] && [ "$p" -le "$a" ]; }
exige() { f="$1"; shift; for m in "$@"; do n=$(grep -c -F -- "$m" "$f" || true); echo "  $n  $(basename "$f")  [$m]"; [ "$n" -gt 0 ] || parar "superficie sem o marcador da v394 ($m): $f"; done; }
sha256f() { $PY -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" "$1"; }
pino() { $PY -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8'))[sys.argv[2]]['sha256'])" "$(cygpath -w "$PK/PINOS_BN_v394.json")" "$1"; }
pinop() { $PY -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8'))[sys.argv[2]]['path'])" "$(cygpath -w "$PK/PINOS_BN_v394.json")" "$1"; }
b3_prepara() {
  # R3.5 (19/10/2026): o B(n) da v394 e' o SALTO v392 -> v394 (a Bancada de producao pina a v392; o elo da v393 nunca rodou) com o esboco R3.5, pela §7 do RESULTADO_R3_4.md. Os pinos vem de PINOS_BN_v394.json (lidos na hora;
  # hash nunca de memoria), FUNDIDO com o que e' da R3.4/R3.5 (R3_5/_construcao/fundir_pinos_bn_r35.py): o esboco R3.5, a cadeia de selos v392->v393, o recibo pre_selo (R3.4, gerado antes da instalacao), o recibo do kernel
  # R3_4 (modulos_de_auditoria), o selo e o manifesto do kernel da v393 (custodia), o driver, o gerador e a base R2 da bateria. A bateria da v394 e' GERADA aqui, por script, depois do selo (bateria por versao).
  for k in criterios esboco_R3_5 gerador_bateria driver_t12_t14 bateria_base_R2 cadeia_de_selos kernel_recibo candidato esperados pins_do_candidato recibo_pre_selo selo_anterior_v393 kernel_manifesto_anterior_v393; do
    tem_pino "$k" || aguarda "o PINO $k nao esta em PINOS_BN_v394.json: a fusao da R3.4/R3.5 no PINOS_BN nao foi feita (ato da gerencia: rodar R3_5/_construcao/fundir_pinos_bn_r35.py) e retomar com CHAIN_DE=$1"
    p=$(pinop "$k"); a=$(pino "$k"); b=$(sha256f "$p"); [ "$a" = "$b" ] || parar "o pino $k diverge do arquivo (pino $a != arquivo $b)"
  done
  [ "$(pino candidato)" = "$(sha256f "$(cygpath -w "$NOS/um.py")")" ] || parar "o um.py do Nos nao e o candidato pinado em PINOS_BN (candidato $(pino candidato))"
  CRI=$(pino criterios); RPS=$(pino recibo_pre_selo); CAD=$(pino cadeia_de_selos)
  W_NOS=$(cygpath -w "$NOS"); W_ESB=$(cygpath -w "$(pinop esboco_R3_5)"); W_CRI=$(cygpath -w "$(pinop criterios)"); W_RPS=$(cygpath -w "$(pinop recibo_pre_selo)"); W_CAD=$(cygpath -w "$(pinop cadeia_de_selos)")
  W_SELO=$(cygpath -w "$(pinop selo_anterior_v393)"); W_KMAN=$(cygpath -w "$(pinop kernel_manifesto_anterior_v393)")
  # o recibo do kernel do pos_selo e' o pino kernel_recibo (R3_4: contrato KERNEL_RECIBO_R3_4 + modulos_de_auditoria); o KERNEL_RECIBO_v394.json (R3_2) nao passa na N1k dos 3 modulos de auditoria
  W_KR=$(cygpath -w "$(pinop kernel_recibo)"); KRSHA=$(sha256f "$W_KR"); [ "$KRSHA" = "$(pino kernel_recibo)" ] || parar "o recibo do kernel diverge do pino"; echo "  recibo do kernel (R3_4, sha256 LIDO NA HORA, igual ao pino): $KRSHA"
  $PY -c "import json,os,sys;sys.exit(0 if os.path.isdir(json.load(open(sys.argv[1],encoding='utf-8'))['arvore']) else 1)" "$W_KR" || aguarda "a arvore so-fontes do recibo do kernel (campo arvore) nao existe mais: refazer a arvore (refazer_arvore_v394_pos_selo.py, sem build; ato da gerencia) e retomar com CHAIN_DE=$1"
  # a bateria da v394: GERADA UMA vez, depois do selo, a partir dos pinos da cadeia (PINOS_BN: candidato == o um.py do Nos); o que o ensaio (10) usa e' o que o aplicar (10b) usa (pino ao lado, gravado na geracao)
  BATD="$PK/bateria_pos_selo"
  if [ ! -e "$BATD/BATERIA_VINCULO_v394.json" ]; then
    mkdir -p "$BATD"
    $PY "$(cygpath -w "$(pinop gerador_bateria)")" --base "$(cygpath -w "$(pinop bateria_base_R2)")" --base-sha256 "$(pino bateria_base_R2)" --versao v394 --nos "$W_NOS" \
        --driver "$(cygpath -w "$(pinop driver_t12_t14)")" --pinos-bn "$(cygpath -w "$PK/PINOS_BN_v394.json")" \
        --pino-saida "$(cygpath -w "$BATD/PINO_UM_PY_v394.json")" --saida "$(cygpath -w "$BATD/BATERIA_VINCULO_v394.json")" > "$SEL/gerar_bateria_v394_out.txt" 2>&1 \
      || { cut -c1-300 "$SEL/gerar_bateria_v394_out.txt"; parar "gerar_bateria_r3_4.py recusou: o Nos nao e o candidato pinado em PINOS_BN, ou o selo nao pina o um.py (saida inteira em $SEL/gerar_bateria_v394_out.txt)"; }
    $PY -c "import hashlib,json,sys;h=lambda p:hashlib.sha256(open(p,'rb').read()).hexdigest();b,p,o=sys.argv[1:4];open(o,'x',encoding='utf-8').write(json.dumps({'bateria':{'path':b,'sha256':h(b)},'pino_um_py':{'path':p,'sha256':h(p)},'nota':'pino ao lado da bateria da v394, gravado quando o chain a gerou (R3.5)'},indent=1))" \
        "$(cygpath -w "$BATD/BATERIA_VINCULO_v394.json")" "$(cygpath -w "$BATD/PINO_UM_PY_v394.json")" "$(cygpath -w "$BATD/PINOS_BATERIA_v394.json")" || parar "nao gravei o pino ao lado da bateria da v394"
    echo "  bateria da v394 GERADA por script em $BATD (pino ao lado: PINOS_BATERIA_v394.json)"
  fi
  [ -f "$BATD/PINOS_BATERIA_v394.json" ] || parar "a bateria da v394 existe sem o pino ao lado ($BATD/PINOS_BATERIA_v394.json): nao se sabe quem a gerou"
  W_BAT=$(cygpath -w "$BATD/BATERIA_VINCULO_v394.json"); BAT=$(sha256f "$W_BAT")
  [ "$BAT" = "$($PY -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8'))['bateria']['sha256'])" "$(cygpath -w "$BATD/PINOS_BATERIA_v394.json")")" ] || parar "a bateria da v394 em disco diverge do pino gravado quando foi gerada"
  echo "  bateria da v394 (sha256 LIDO NA HORA, igual ao pino ao lado): $BAT"
}
tem_pino() { $PY -c "import json,sys;sys.exit(0 if sys.argv[2] in json.load(open(sys.argv[1],encoding='utf-8')) else 1)" "$(cygpath -w "$PK/PINOS_BN_v394.json")" "$1"; }
echo "== 0. guardas $(date +%T)"
command -v python > /dev/null || parar "python nao esta no PATH"
S16=$($PY -c "import glob,json,os,sys;ps=sorted(glob.glob(os.path.join(sys.argv[1],'APLICADO_AO_CANONICO_*.json')));print(json.load(open(ps[-1],encoding='utf-8'))['um_py_novo']['sha16'])" "$(cygpath -w "$PK")") || parar "APLICADO_AO_CANONICO_*.json ilegivel em $PK"
$PY -c "
import hashlib, json, glob, os, sys
um, pk = sys.argv[1], sys.argv[2]
ap = json.load(open(sorted(glob.glob(os.path.join(pk, 'APLICADO_AO_CANONICO_*.json')))[-1], encoding='utf-8'))
es = json.load(open(os.path.join(pk, 'ESPERADOS_v394.json'), encoding='utf-8'))
h = hashlib.sha256(open(um, 'rb').read()).hexdigest()[:16]
print('um.py no disco', h, '== instalado', ap['um_py_novo']['sha16'], '== candidato', es['candidato_sha16'])
sys.exit(0 if h == ap['um_py_novo']['sha16'] == es['candidato_sha16'] else 1)" "$(cygpath -w "$NOS/um.py")" "$(cygpath -w "$PK")" || parar "o um.py do disco nao e o instalado"
for f in "$TOOLS/arvore_da_prova.py" "$TOOLS/atlas_indice.py" "$PORTA" "$PK/conferir_rito_v394.py" "$PK/ESPERADOS_v394.json" "$PK/guarda_p18_v394.py" "$PK/PINOS_BN_v394.json" \
         "$PK/refazer_arvore_v394_pos_selo.py" "$PK/kernel/KERNEL_RECIBO_v394.json" "$HAJA" "$INV/inventario_bancada.py" "$INV/gerar_documento.py" "/c/IALD/NOS_VIVO/construir.py" \
         "$SEL/leitura_v394.py" "$SEL/textos_v394.py" "$SEL/superficies_v394.py" "$SEL/fechar_v394.py" "$SEL/registrar_mapa_v394.py" "$SEL/b3_recibo_v394.py"; do
  [ -f "$f" ] || parar "ferramenta/superficie ausente: $f"; done
$PY "$PK/guarda_p18_v394.py" "$SEL/textos_v394.py" > /dev/null || parar "a guarda de texto P18 achou violacao em textos_v394.py"
STD="$NOS/rodada_v394_stdout.txt"
grep -q '^RITO_RC=' "$STD" || parar "o rito nao acabou (sem RITO_RC= no stdout)"
tail -3 "$STD" | cut -c1-240
if quer 1; then
echo "== 1. conferidor (copia byte a byte; so leitura do Nos) $(date +%T)"
rm -rf "$CONFOUT"; mkdir -p "$CONFOUT"
cp -p "$PK/conferir_rito_v394.py" "$CONFOUT/"; cmp "$PK/conferir_rito_v394.py" "$CONFOUT/conferir_rito_v394.py" || parar "copia do conferidor difere"
for f in ESPERADOS_v394.json rito_servidor_v394.log rito_v394_sinal.txt; do
  if [ -f "$PK/$f" ]; then cp -p "$PK/$f" "$CONFOUT/$f"; cmp "$PK/$f" "$CONFOUT/$f" || parar "copia difere: $f"; echo "  copiado byte a byte: $f"; else echo "  (o pacote nao tem $f)"; fi
done
if [ -f "$PK/.servidor_parado_pelo_rito" ]; then parar "o marcador .servidor_parado_pelo_rito ficou no pacote: o servidor do modelo pode estar parado ($(cat "$PK/.servidor_parado_pelo_rito"))"; fi
set +e; (cd "$CONFOUT" && $PY conferir_rito_v394.py) > "$CONFOUT/conferir_rito_v394_stdout.txt" 2>&1; c=$?; set -e
cut -c1-240 "$CONFOUT/conferir_rito_v394_stdout.txt"
[ "$c" = "0" ] && tail -1 "$CONFOUT/conferir_rito_v394_stdout.txt" | grep -q "^TUDO BATE" || parar "CONFERIDOR REPROVOU (rc=$c) -- nada foi escrito nas superficies"
fi
if quer 2; then
echo "== 2. a leitura da rodada $(date +%T)"
set +e; $PY "$SEL/leitura_v394.py" > "$SEL/leitura_v394_out.txt" 2>&1; l=$?; set -e
tail -1 "$SEL/leitura_v394_out.txt" | cut -c1-600
[ "$l" = "0" ] || parar "a LEITURA tem PROBLEMAS (saida inteira em $SEL/leitura_v394_out.txt)"
fi
if quer 3; then
echo "== 3. ENSAIO em COPIAS: superficies (plano conferido antes da primeira escrita) e a arvore em DRY (nada real e' tocado)"
rm -rf "${ENS:?}" "${ENST:?}"; mkdir -p "$ENS" "$ENST"
cp -p "$NOS/MEMORIA_DA_LINHAGEM.md" "$NOS/DESENHO_DO_FECHAMENTO_QG.md" "$ATLD/TGL_ATLAS.md" "$ATLD/TGL_CORE_MEMORY.md" \
      "$UMEM/MEMORY.md" "$UMEM/MEMORY_2.md" "$HAJA" "$ENS/"
for t in $TOPICOS; do cp -p "$UMEM/$t" "$ENS/"; done
if [ -n "$V394_AVISO_REIVINDICACAO" ]; then cp -p "$AVISO" "$ENS/"; fi
set +e; $PY "$SEL/superficies_v394.py" --copias "$(cygpath -w "$ENS")" > "$SEL/ensaio_superficies_out.txt" 2>&1; es=$?; set -e
tail -24 "$SEL/ensaio_superficies_out.txt" | cut -c1-260
[ "$es" = "0" ] || parar "o ENSAIO das superficies falhou (rc=$es) -- nada real foi tocado"
n=$(wc -c < "$ENS/MEMORY.md"); l=$(wc -l < "$ENS/MEMORY.md"); echo "  MEMORY.md da copia: $n B, $l linhas"
[ "$n" -lt 24000 ] || parar "o MEMORY.md da copia chegou a 24 000 B ($n)"
[ "$l" -le 195 ] || parar "o MEMORY.md da copia passou de 195 linhas ($l)"
cp -p "$TOOLS/arvore_da_prova.py" "$TOOLS/atlas_indice.py" "$ENST/"
if [ -f "$SEL/patch_arvore_indice_v394.py" ]; then
  $PY "$SEL/patch_arvore_indice_v394.py" --tools "$(cygpath -w "$ENST")" || parar "o ENSAIO do patch da arvore/indice recusou ou falhou (so copias foram tocadas)"
else
  echo "  (sem patch_arvore_indice_v394.py: a arvore e o indice rodam SEM linha nova da v394 -- a v394 nao tem patch da arvore/indice; as ferramentas escrevem o sha16 sozinhas (na v393 o fizeram); o passo 3 confere isso ANTES de gravar)"
fi
(cd "$ENST" && $PY_B arvore_da_prova.py v394 dry) || parar "a arvore_da_prova.py (copia, dry) falhou"
[ -f "$ENST/arvore_dry.md" ] || parar "a arvore (dry) nao gerou arvore_dry.md em $ENST"
echo "  (fail-early do passo 9: a arvore (dry) e as COPIAS das superficies tem de trazer o sha16 e os marcadores da v394 ANTES de qualquer escrita real)"
exige "$ENST/arvore_dry.md" "$S16"
TOPICO_NOVO=$(topico_novo) || parar "nao li TOPICO_NOVO de textos_v394.py (o arquivo ainda tem trecho marcado para reescrever?)"
exige "$ENS/MEMORIA_DA_LINHAGEM.md" "$S16" "<!-- linhagem_v394_selada -->" "tempo_frequencia_v394" "kh_n1_cobertura_v394"
exige "$ENS/DESENHO_DO_FECHAMENTO_QG.md" "<!-- adendo_v394_selada -->" "$S16"
exige "$ENS/TGL_ATLAS.md" "<!-- atlas_v394_selada -->" "$S16" "tempo_frequencia_v394" "kh_n1_cobertura_v394"
exige "$ENS/TGL_CORE_MEMORY.md" "<!-- core_v394_selada -->" "$S16"
exige "$ENS/CLAUDE.md" "<!-- haja_luz_v394_selada -->" "$S16"
exige "$ENS/MEMORY.md" "$S16"
exige "$ENS/MEMORY_2.md" "v394"
exige "$ENS/estatuto-da-prova-07out.md" "<!-- v394_selada -->" "$S16"
exige "$ENS/$TOPICO_NOVO" "$S16" "tempo_frequencia_v394" "kh_n1_cobertura_v394"
fi
if quer 4; then
if [ -f "$SEL/patch_arvore_indice_v394.py" ]; then
echo "== 4. patches arvore/indice"; $PY "$SEL/patch_arvore_indice_v394.py" || parar "patch arvore/indice recusou/falhou (backups _p394 ao lado)"
else
echo "== 4. patches arvore/indice: PULADO (opcional; sem patch_arvore_indice_v394.py)"
fi
fi
if quer 5; then
echo "== 5. arvore"; (cd "$TOOLS" && $PY_B arvore_da_prova.py v394) || parar "arvore_da_prova.py v394 falhou"
fi
if quer 6; then
echo "== 6. atlas + indice (a ordem da v390: o indice antes das superficies)"; (cd "$TOOLS" && $PY_B atlas_indice.py v394) || parar "atlas_indice.py v394 falhou"
fi
if quer 7; then
echo "== 7. superficies (real: appends datados; a guarda P18 em todo texto; sem errata nova no CLAUDE.md da raiz)"
$PY "$SEL/superficies_v394.py" || parar "superficies_v394.py parou (backups .bak_<STAMP>_sup394 ao lado; rerodar e IDEMPOTENTE)"
fi
if quer 8; then
echo "== 8. espelho da memoria"
set +e; $PY_B "$PORTA" > "$SEL/porta_memoria_v394_out.txt" 2>&1; pm=$?; set -e
tail -1 "$SEL/porta_memoria_v394_out.txt"
[ "$pm" = "0" ] || parar "porta_memoria.py saiu com rc=$pm"
fi
if quer 9; then
echo "== 9. regra da linhagem completa: o MARCADOR DO SELO e o sha16 do um.py v394 ($S16) em cada superficie (zero e' falha visivel)"
exige "$NOS/MEMORIA_DA_LINHAGEM.md" "$S16" "<!-- linhagem_v394_selada -->" "tempo_frequencia_v394" "kh_n1_cobertura_v394"
exige "$NOS/DESENHO_DO_FECHAMENTO_QG.md" "<!-- adendo_v394_selada -->" "$S16"
exige "$ATLD/TGL_ATLAS.md" "<!-- atlas_v394_selada -->" "$S16" "tempo_frequencia_v394" "kh_n1_cobertura_v394"
exige "$ATLD/TGL_INDICE_VIVO.md" "$S16"
exige "$ATLD/TGL_CORE_MEMORY.md" "<!-- core_v394_selada -->" "$S16"
exige "$NOS/A_PROVA_DA_QG_TGL_arvore.md" "$S16"
exige "$HAJA" "<!-- haja_luz_v394_selada -->" "$S16"
exige "$UMEM/MEMORY.md" "$S16"
exige "$UMEM/MEMORY_2.md" "v394"
for t in missao-ultima-flag-um-py.md central-de-patentes-estado.md; do exige "$UMEM/$t" "$S16"; done
exige "$UMEM/estatuto-da-prova-07out.md" "<!-- v394_selada -->" "$S16"
TOPICO_NOVO=$(topico_novo) || parar "nao li TOPICO_NOVO de textos_v394.py"
exige "$UMEM/$TOPICO_NOVO" "$S16" "tempo_frequencia_v394" "kh_n1_cobertura_v394"
if [ -n "$V394_AVISO_REIVINDICACAO" ]; then exige "$AVISO" "<!-- aviso_v394_selada -->" "$S16"; else echo "  (AVISO_GERENCIA.md: PULADO -- sem V394_AVISO_REIVINDICACAO; escrever depois, sob reivindicacao)"; fi
n=$(wc -c < "$UMEM/MEMORY.md"); l=$(wc -l < "$UMEM/MEMORY.md"); echo "  MEMORY.md: $n B (limite 24000), $l linhas (limite 195)"
[ "$n" -lt 24000 ] || parar "MEMORY.md chegou a 24 000 B ($n)"
[ "$l" -le 195 ] || parar "MEMORY.md passou de 195 linhas ($l): o carregador do harness o corta acima de 200"
fi
if quer 10; then
echo "== 10. B(n) da Bancada, ENSAIO pos-selo, SALTO v392 -> v394, esboco R3.5 (nada e' gravado na Bancada; o servico pode estar no ar) $(date +%T)"
b3_prepara 10
SAIDA_E="$PK/bancada_B3_ensaio_$(date +%Y%m%d_%H%M%S)"
set +e
$PY "$W_ESB" --bancada 'C:\IALD\Bancada_Um' --producao --nos "$W_NOS" --versao v394 --fase pos_selo --modo ensaio --bateria "$W_BAT" --bateria-sha256 "$BAT" \
    --cadeia-de-selos "$W_CAD" --cadeia-de-selos-sha256 "$CAD" \
    --recibo-pre-selo "$W_RPS" --recibo-pre-selo-sha256 "$RPS" --selo-anterior "$W_SELO" --kernel-manifesto-anterior "$W_KMAN" \
    --kernel-recibo "$W_KR" --kernel-recibo-sha256 "$KRSHA" --criterios "$W_CRI" --criterios-sha256 "$CRI" \
    --saida "$(cygpath -w "$SAIDA_E")" > "$SEL/b3_ensaio_out.txt" 2>&1; b3=$?
set -e
tail -4 "$SEL/b3_ensaio_out.txt" | cut -c1-400
[ "$b3" = "0" ] || parar "o B(n) ENSAIO reprovou (rc=$b3): saida inteira em $SEL/b3_ensaio_out.txt"
$PY "$SEL/b3_recibo_v394.py" "$(cygpath -w "$SEL/b3_ensaio_out.txt")" ensaio "$CAD" || parar "o recibo do B(n) ENSAIO nao confere"
fi
if quer 10a; then
echo "== 10-bis-a. a parada do servico da Bancada Um (porta 18777), com recibo"
RP="$PK/bancada_B3_servico/RECIBO_PARADA_v394.json"
[ -f "$RP" ] || aguarda "sem o recibo da PARADA do um_bancada.py ($RP): quiesce e parada (PID, porta 18777 fechada e hora no recibo), no molde do restart_and_deploy.ps1 / RESTART_RECEIPT_R1.json da B2 -- ato do operador autorizado na B3. Sem esse recibo a cadeia para aqui."
$PY -c "import socket,sys
try:
    socket.create_connection(('127.0.0.1', 18777), timeout=1.5).close()
except OSError:
    sys.exit(0)
sys.exit(1)" || parar "o servico da Bancada esta no AR (a porta 18777 responde) apesar do recibo de parada"
echo "  recibo da parada: $RP (sha256 $(sha256f "$(cygpath -w "$RP")")); porta 18777 fechada"
fi
if quer 10b; then
echo "== 10-bis. B(n) APLICAR, SALTO v392 -> v394, esboco R3.5 (grava o manifesto B4 na Bancada de producao: backup de bytes, rollback se falhar) $(date +%T)"
[ "$B3_AUTORIZADO" = "sim" ] || aguarda "a B(n) nao esta autorizada: ato da gerencia sob evento c1 (SINCRONIZACAO_BANCADA, que nomeia a v394) + autorizacao do operador. Definir B3_AUTORIZADO=sim, EVENTO=<seq> e EVENTO_HASH=<hash16 do retorno de iald.py anotar>, com o servico parado (10-bis-a) e o recibo da parada, e retomar com CHAIN_DE=10b"
[ -n "$EVENTO" ] && [ -n "$EVENTO_HASH" ] || aguarda "faltam EVENTO e EVENTO_HASH (o elo do evento c1 nomeando a gravacao)"
[ -f "$PK/bancada_B3_servico/RECIBO_PARADA_v394.json" ] || aguarda "sem o recibo da parada do servico (10-bis-a)"
b3_prepara 10b
SAIDA_B3="$PK/bancada_B3"; k=1; while [ -e "$SAIDA_B3" ]; do k=$((k+1)); SAIDA_B3="$PK/bancada_B3_$k"; done
echo "  saida do B(n): $SAIDA_B3 (pasta nova)"
set +e
$PY "$W_ESB" --bancada 'C:\IALD\Bancada_Um' --producao --nos "$W_NOS" --versao v394 --fase pos_selo --modo aplicar --bateria "$W_BAT" --bateria-sha256 "$BAT" \
    --cadeia-de-selos "$W_CAD" --cadeia-de-selos-sha256 "$CAD" \
    --evento "$EVENTO" --evento-hash "$EVENTO_HASH" \
    --recibo-pre-selo "$W_RPS" --recibo-pre-selo-sha256 "$RPS" --selo-anterior "$W_SELO" --kernel-manifesto-anterior "$W_KMAN" \
    --kernel-recibo "$W_KR" --kernel-recibo-sha256 "$KRSHA" --criterios "$W_CRI" --criterios-sha256 "$CRI" \
    --saida "$(cygpath -w "$SAIDA_B3")" > "$SEL/b3_aplicar_out.txt" 2>&1; b3=$?
set -e
tail -4 "$SEL/b3_aplicar_out.txt" | cut -c1-400
[ "$b3" = "0" ] || parar "o B(n) APLICAR reprovou (rc=$b3): saida inteira em $SEL/b3_aplicar_out.txt; NADA foi restaurado por esta cadeia (o esboco faz o seu rollback)"
$PY "$SEL/b3_recibo_v394.py" "$(cygpath -w "$SEL/b3_aplicar_out.txt")" aplicar "$CAD" || parar "o recibo do B(n) APLICAR nao confere"
fi
if quer 10c; then
echo "== 10-ter. o religamento do servico e a reconexao dos adaptadores MCP (ato do operador)"
RR="$PK/bancada_B3_servico/RECIBO_RELIGAMENTO_v394.json"
[ -f "$RR" ] || aguarda "sem o recibo do RELIGAMENTO do um_bancada.py ($RR): religar o servico com recibo de identidade (a versao servida e v394 e o sha do manifesto e o do recibo do 10-bis) e reconectar os adaptadores MCP das sessoes (ato do operador)"
echo "  recibo do religamento: $RR (sha256 $(sha256f "$(cygpath -w "$RR")")); o fechar o confere contra o recibo do 10-bis"
fi
if quer 11; then
echo "== 11. fechar (manifesto, arquivo, os dois diffs, handoff) -- recusa sem os tres recibos do B(3)"
$PY "$SEL/fechar_v394.py" || parar "fechar_v394.py falhou"
fi
if quer 12; then
echo "== 12. registro no mapa de rotas: so MONTA o JSON e o comando (o registro e' ato da gerencia)"
$PY "$SEL/registrar_mapa_v394.py" || parar "registrar_mapa_v394.py falhou"
fi
if quer 13; then
echo "== 13. o inventario da bancada Lean (work\\inventario_bancada) regenerado; copia para memory\\ com backup de bytes"
(cd "$INV" && $PY_B inventario_bancada.py > "$SEL/inventario_bancada_out.txt" 2>&1 && $PY_B gerar_documento.py >> "$SEL/inventario_bancada_out.txt" 2>&1) || parar "o inventario da bancada falhou (ver $SEL/inventario_bancada_out.txt)"
tail -2 "$SEL/inventario_bancada_out.txt" | cut -c1-240
for f in INVENTARIO_BANCADA_CHATGPT.md INVENTARIO_BANCADA_CHATGPT.json; do
  [ -f "$INV/$f" ] || parar "o inventario nao gerou $f"
  if [ -f "$ATLD/$f" ]; then B="$ATLD/$f.bak_$(date +%Y%m%d_%H%M%S)_v394"; cp -p "$ATLD/$f" "$B"; cmp "$ATLD/$f" "$B" || parar "backup de bytes falhou: $B"; fi
  cp -p "$INV/$f" "$ATLD/$f.tmp_v394" && mv "$ATLD/$f.tmp_v394" "$ATLD/$f"; cmp "$INV/$f" "$ATLD/$f" || parar "a copia do inventario difere: $f"
done
fi
if quer 14; then
echo "== 14. o Nos vivo reconstruido (le o mapa de rotas: rodar depois do registro da gerencia no passo 12)"
$PY_B /c/IALD/NOS_VIVO/construir.py > "$SEL/nos_vivo_out.txt" 2>&1 || parar "NOS_VIVO/construir.py falhou (ver $SEL/nos_vivo_out.txt)"
tail -3 "$SEL/nos_vivo_out.txt" | cut -c1-240
fi
echo "== FIM $(date +%T)"
