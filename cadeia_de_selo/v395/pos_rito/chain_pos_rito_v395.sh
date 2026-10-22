#!/bin/sh
# v395 (21/10): CADEIA POS-RITO -- no molde do chain_pos_rito_v394.sh FINAL (o que rodou em 19/10; derivada por derivar_cadeia_v395.py; mesma ordem de passos 0..14 e mesmos portoes). O rito ja terminou (rito_v395.sh em segundo plano;
# RITO_RC=<rc> no fim do Nos\rodada_v395_stdout.txt). A v395 e' um DELTA PEQUENO: 1 modulo novo de kernel (TGLExt/Psibit, a leitura psibit da orbita do Um pela matriz-S), o registro psibit_v395 (a funcao do runtime chamada NA FRACTALIZACAO DO UM)
# e os registros por spec cunhagens_v395 (as quatro falas de 21/10) e kh_n1_cobertura_v395; os tres contratos da v394 ganham expected_ladder novo e kh_n1_cobertura_v394 passa a piso (erratas ao lado).
# ORDEM: 0 guardas -> 1 o CONFERIDOR (copia byte a byte, com o delta_v395.py que ele importa; so leitura do Nos) -> 2 a LEITURA (PROBLEMAS param) -> 3 ENSAIO das superficies em COPIAS (o plano e' conferido antes da primeira escrita; a arvore em dry;
# o sha16 da v395 na arvore (dry) e os marcadores do passo 9 nas COPIAS, conferidos ANTES de qualquer escrita real) -> 4 patch arvore/indice (OPCIONAL: so' se existir patch_arvore_indice_v395.py) -> 5 a arvore
# -> 6 atlas+indice -> 7 superficies reais (appends datados; SEM errata nova no CLAUDE.md da raiz) -> 8 porta_memoria.py (o ATLAS a mao nao se toca) -> 9 regra da linhagem completa COM O MARCADOR DO SELO (zero e'
# falha visivel) e a guarda de MEMORY.md (<24.000 B, <=195 linhas) -> 10 B(n) da Bancada, ENSAIO pos-selo -> 10a parada do servico (AGUARDA_OPERADOR) -> 10b B(n) APLICAR (so com B3_AUTORIZADO=sim e o evento c1)
# -> 10c religamento (AGUARDA_OPERADOR) -> 11 fechar -> 12 registrar_mapa (so MONTA o JSON e o comando) -> 13 inventario da bancada Lean -> 14 Nos vivo.
# Sai na primeira reprovacao e NAO restaura nada sozinha: a decisao de restaurar e' da gerencia. Retomada: CHAIN_DE=<passo> (e CHAIN_ATE=<passo>); os passos 3 a 9 sao idempotentes.
# Ambiente: B3_AUTORIZADO=sim, EVENTO=<seq> e EVENTO_HASH=<hash16> (so o 10b); V395_AVISO_REIVINDICACAO=<texto> (so' com ela o AVISO_GERENCIA.md e' escrito; sem ela e' PULADO e dito).
# PASSO 10 SEM SALTO: a Bancada de producao pina a v394 e o Nos e' a v394 ate' a instalacao; portanto o B(n) da v395 e' um passo SIMPLES v394 -> v395 (esboco R3.5, sincronizar_bancada.py): NAO ha a opcao de cadeia de selos do esboco, nem o pino correspondente,
# e o b3_recibo_v395.py NAO tem o 3o argumento. Os pinos vem de PINOS_BN_v395.json (lidos na hora; hash nunca de memoria): criterios, esboco_R3_5, gerador_bateria, driver_t12_t14, bateria_base_R2, kernel_recibo (o KERNEL_RECIBO_v395.json,
# contrato R3_2: a v395 nao acrescenta modulo de auditoria), candidato, esperados, pins_do_candidato, recibo_pre_selo (gerado antes da instalacao; veredito JA_SINCRONIZADA__ENSAIO__NADA_GRAVADO_NA_BANCADA), selo_anterior_v394 e
# kernel_manifesto_anterior_v394 (as copias de bytes do selo e do manifesto do kernel da v394, em base_v394). A BATERIA da v395 e' GERADA por script no 10 (depois do selo; bateria por versao) e pinada ao lado (bateria_pos_selo/PINOS_BATERIA_v395.json).
# Vereditos esperados (lidos do codigo do esboco, nao rodados): ensaio REPINADA_B<n>__ENSAIO__NADA_GRAVADO_NA_BANCADA e aplicar REPINADA_B<n>__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO, sem __SALTO_, com n = a geracao do manifesto que a
# Bancada pina + 1 (o b3_recibo_v395.py o confere). A parada do servico (10a) e o religamento (10c) sao ato do operador (V395_AUTORIZACAO_OPERADOR nos scripts bancada_B3_servico\recibo_parada_v395.py e recibo_religamento_v395.py); o chain so' confere os recibos.
# textos_v395.py, fechar_v395.py e registrar_mapa_v395.py RECUSAM rodar se tiverem trecho marcado para reescrever: os passos 0 a 2 nao os usam. Os passos 0 a 9, 10a, 10c e 11 a 14 estao como na v394, com os rotulos da v395.
# Codigos de saida: 0 fim; 1 reprovacao (PARADA); 20 AGUARDA_OPERADOR (parada de proposito, nao e' falha).
PK="/c/IALD/Central de Patentes/work/cadeia_de_selo/v395"; SEL="$PK/pos_rito"
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
# o NOME do topico novo e' lido de textos_v395.TOPICO_NOVO (uma fonte so'); so' roda onde e' usado (passos 3 e 9): o textos_v395.py recusa importar com trecho marcado para reescrever
topico_novo() { $PY -c "import sys;sys.path.insert(0,sys.argv[1]);import textos_v395 as T;print(T.TOPICO_NOVO)" "$(cygpath -w "$SEL")"; }
aguarda() { echo "AGUARDA_OPERADOR: $*"; echo "(a cadeia parou de proposito, nao e' falha; retomar com CHAIN_DE=<passo>)"; exit 20; }
ORDEM="0 1 2 3 4 5 6 7 8 9 10 10a 10b 10c 11 12 13 14"
DE="${CHAIN_DE:-0}"; ATE="${CHAIN_ATE:-14}"
pos() { i=0; for x in $ORDEM; do if [ "$x" = "$1" ]; then echo "$i"; return 0; fi; i=$((i+1)); done; echo "-1"; }
quer() { p=$(pos "$1"); d=$(pos "$DE"); a=$(pos "$ATE"); if [ "$d" -lt 0 ] || [ "$a" -lt 0 ]; then echo "CHAIN_DE/CHAIN_ATE desconhecido (validos: $ORDEM)"; exit 1; fi; [ "$p" -ge "$d" ] && [ "$p" -le "$a" ]; }
exige() { f="$1"; shift; for m in "$@"; do n=$(grep -c -F -- "$m" "$f" || true); echo "  $n  $(basename "$f")  [$m]"; [ "$n" -gt 0 ] || parar "superficie sem o marcador da v395 ($m): $f"; done; }
sha256f() { $PY -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" "$1"; }
pino() { $PY -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8'))[sys.argv[2]]['sha256'])" "$(cygpath -w "$PK/PINOS_BN_v395.json")" "$1"; }
pinop() { $PY -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8'))[sys.argv[2]]['path'])" "$(cygpath -w "$PK/PINOS_BN_v395.json")" "$1"; }
b3_prepara() {
  # v395 (21/10/2026): o B(n) da v395 e' um PASSO SIMPLES v394 -> v395 (a Bancada de producao pina a v394 e o Nos passou a v395): SEM salto e SEM cadeia de selos, com o esboco R3.5. Os pinos vem de PINOS_BN_v395.json (lidos na hora;
  # hash nunca de memoria): o esboco R3.5, o recibo pre_selo (gerado antes da instalacao, sobre a Bancada que pina a v394), o recibo do kernel (KERNEL_RECIBO_v395.json, contrato R3_2, sem modulos de auditoria: a v395 nao acrescenta
  # modulo de auditoria), o selo e o manifesto do kernel da v394 (custodia, em base_v394), o driver, o gerador e a base R2 da bateria. A bateria da v395 e' GERADA aqui, por script, depois do selo (bateria por versao).
  for k in criterios esboco_R3_5 gerador_bateria driver_t12_t14 bateria_base_R2 kernel_recibo candidato esperados pins_do_candidato recibo_pre_selo selo_anterior_v394 kernel_manifesto_anterior_v394; do
    tem_pino "$k" || aguarda "o PINO $k nao esta em PINOS_BN_v395.json: o PINOS_BN da v395 nao foi gerado (ato da gerencia: diff_e_pinos_v395.py) e retomar com CHAIN_DE=$1"
    p=$(pinop "$k"); a=$(pino "$k"); b=$(sha256f "$p"); [ "$a" = "$b" ] || parar "o pino $k diverge do arquivo (pino $a != arquivo $b)"
  done
  if tem_pino cadeia_de_selos; then parar "PINOS_BN_v395.json traz o pino cadeia_de_selos: a v395 e' um passo simples (a Bancada pina a v394), sem salto e sem cadeia de selos"; fi
  [ "$(pino candidato)" = "$(sha256f "$(cygpath -w "$NOS/um.py")")" ] || parar "o um.py do Nos nao e o candidato pinado em PINOS_BN (candidato $(pino candidato))"
  CRI=$(pino criterios); RPS=$(pino recibo_pre_selo)
  W_NOS=$(cygpath -w "$NOS"); W_ESB=$(cygpath -w "$(pinop esboco_R3_5)"); W_CRI=$(cygpath -w "$(pinop criterios)"); W_RPS=$(cygpath -w "$(pinop recibo_pre_selo)")
  W_SELO=$(cygpath -w "$(pinop selo_anterior_v394)"); W_KMAN=$(cygpath -w "$(pinop kernel_manifesto_anterior_v394)")
  # o recibo do kernel do pos_selo e' o pino kernel_recibo (o KERNEL_RECIBO_v395.json, contrato R3_2: sem modulos de auditoria)
  W_KR=$(cygpath -w "$(pinop kernel_recibo)"); KRSHA=$(sha256f "$W_KR"); [ "$KRSHA" = "$(pino kernel_recibo)" ] || parar "o recibo do kernel diverge do pino"; echo "  recibo do kernel (R3_2, sha256 LIDO NA HORA, igual ao pino): $KRSHA"
  $PY -c "import json,os,sys;sys.exit(0 if os.path.isdir(json.load(open(sys.argv[1],encoding='utf-8'))['arvore']) else 1)" "$W_KR" || aguarda "a arvore so-fontes do recibo do kernel (campo arvore) nao existe mais: refazer a arvore (refazer_arvore_v395_pos_selo.py, sem build; ato da gerencia) e retomar com CHAIN_DE=$1"
  # a bateria da v395: GERADA UMA vez, depois do selo, a partir dos pinos da cadeia (PINOS_BN: candidato == o um.py do Nos); o que o ensaio (10) usa e' o que o aplicar (10b) usa (pino ao lado, gravado na geracao)
  BATD="$PK/bateria_pos_selo"
  if [ ! -e "$BATD/BATERIA_VINCULO_v395.json" ]; then
    mkdir -p "$BATD"
    $PY "$(cygpath -w "$(pinop gerador_bateria)")" --base "$(cygpath -w "$(pinop bateria_base_R2)")" --base-sha256 "$(pino bateria_base_R2)" --versao v395 --nos "$W_NOS" \
        --driver "$(cygpath -w "$(pinop driver_t12_t14)")" --pinos-bn "$(cygpath -w "$PK/PINOS_BN_v395.json")" \
        --pino-saida "$(cygpath -w "$BATD/PINO_UM_PY_v395.json")" --saida "$(cygpath -w "$BATD/BATERIA_VINCULO_v395.json")" > "$SEL/gerar_bateria_v395_out.txt" 2>&1 \
      || { cut -c1-300 "$SEL/gerar_bateria_v395_out.txt"; parar "gerar_bateria_r3_4.py recusou: o Nos nao e o candidato pinado em PINOS_BN, ou o selo nao pina o um.py (saida inteira em $SEL/gerar_bateria_v395_out.txt)"; }
    $PY -c "import hashlib,json,sys;h=lambda p:hashlib.sha256(open(p,'rb').read()).hexdigest();b,p,o=sys.argv[1:4];open(o,'x',encoding='utf-8').write(json.dumps({'bateria':{'path':b,'sha256':h(b)},'pino_um_py':{'path':p,'sha256':h(p)},'nota':'pino ao lado da bateria da v395, gravado quando o chain a gerou (R3.5)'},indent=1))" \
        "$(cygpath -w "$BATD/BATERIA_VINCULO_v395.json")" "$(cygpath -w "$BATD/PINO_UM_PY_v395.json")" "$(cygpath -w "$BATD/PINOS_BATERIA_v395.json")" || parar "nao gravei o pino ao lado da bateria da v395"
    echo "  bateria da v395 GERADA por script em $BATD (pino ao lado: PINOS_BATERIA_v395.json)"
  fi
  [ -f "$BATD/PINOS_BATERIA_v395.json" ] || parar "a bateria da v395 existe sem o pino ao lado ($BATD/PINOS_BATERIA_v395.json): nao se sabe quem a gerou"
  W_BAT=$(cygpath -w "$BATD/BATERIA_VINCULO_v395.json"); BAT=$(sha256f "$W_BAT")
  [ "$BAT" = "$($PY -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8'))['bateria']['sha256'])" "$(cygpath -w "$BATD/PINOS_BATERIA_v395.json")")" ] || parar "a bateria da v395 em disco diverge do pino gravado quando foi gerada"
  echo "  bateria da v395 (sha256 LIDO NA HORA, igual ao pino ao lado): $BAT"
}
tem_pino() { $PY -c "import json,sys;sys.exit(0 if sys.argv[2] in json.load(open(sys.argv[1],encoding='utf-8')) else 1)" "$(cygpath -w "$PK/PINOS_BN_v395.json")" "$1"; }
echo "== 0. guardas $(date +%T)"
command -v python > /dev/null || parar "python nao esta no PATH"
S16=$($PY -c "import glob,json,os,sys;ps=sorted(glob.glob(os.path.join(sys.argv[1],'APLICADO_AO_CANONICO_*.json')));print(json.load(open(ps[-1],encoding='utf-8'))['um_py_novo']['sha16'])" "$(cygpath -w "$PK")") || parar "APLICADO_AO_CANONICO_*.json ilegivel em $PK"
$PY -c "
import hashlib, json, glob, os, sys
um, pk = sys.argv[1], sys.argv[2]
ap = json.load(open(sorted(glob.glob(os.path.join(pk, 'APLICADO_AO_CANONICO_*.json')))[-1], encoding='utf-8'))
es = json.load(open(os.path.join(pk, 'ESPERADOS_v395.json'), encoding='utf-8'))
h = hashlib.sha256(open(um, 'rb').read()).hexdigest()[:16]
print('um.py no disco', h, '== instalado', ap['um_py_novo']['sha16'], '== candidato', es['candidato_sha16'])
sys.exit(0 if h == ap['um_py_novo']['sha16'] == es['candidato_sha16'] else 1)" "$(cygpath -w "$NOS/um.py")" "$(cygpath -w "$PK")" || parar "o um.py do disco nao e o instalado"
for f in "$TOOLS/arvore_da_prova.py" "$TOOLS/atlas_indice.py" "$PORTA" "$PK/conferir_rito_v395.py" "$PK/delta_v395.py" "$PK/ESPERADOS_v395.json" "$PK/guarda_p18_v395.py" "$PK/PINOS_BN_v395.json" \
         "$PK/refazer_arvore_v395_pos_selo.py" "$PK/kernel/KERNEL_RECIBO_v395.json" "$HAJA" "$INV/inventario_bancada.py" "$INV/gerar_documento.py" "/c/IALD/NOS_VIVO/construir.py" \
         "$SEL/leitura_v395.py" "$SEL/textos_v395.py" "$SEL/superficies_v395.py" "$SEL/fechar_v395.py" "$SEL/registrar_mapa_v395.py" "$SEL/b3_recibo_v395.py"; do
  [ -f "$f" ] || parar "ferramenta/superficie ausente: $f"; done
$PY "$PK/guarda_p18_v395.py" "$SEL/textos_v395.py" "$SEL/fechar_v395.py" "$SEL/registrar_mapa_v395.py" > /dev/null || parar "a guarda de texto P18 achou violacao em textos_v395.py, fechar_v395.py ou registrar_mapa_v395.py"
STD="$NOS/rodada_v395_stdout.txt"
grep -q '^RITO_RC=' "$STD" || parar "o rito nao acabou (sem RITO_RC= no stdout)"
tail -3 "$STD" | cut -c1-240
if quer 1; then
echo "== 1. conferidor (copia byte a byte; so leitura do Nos) $(date +%T)"
rm -rf "$CONFOUT"; mkdir -p "$CONFOUT"
cp -p "$PK/conferir_rito_v395.py" "$CONFOUT/"; cmp "$PK/conferir_rito_v395.py" "$CONFOUT/conferir_rito_v395.py" || parar "copia do conferidor difere"
cp -p "$PK/delta_v395.py" "$CONFOUT/"; cmp "$PK/delta_v395.py" "$CONFOUT/delta_v395.py" || parar "copia do delta_v395.py (que o conferidor importa) difere"
for f in ESPERADOS_v395.json rito_servidor_v395.log rito_v395_sinal.txt; do
  if [ -f "$PK/$f" ]; then cp -p "$PK/$f" "$CONFOUT/$f"; cmp "$PK/$f" "$CONFOUT/$f" || parar "copia difere: $f"; echo "  copiado byte a byte: $f"; else echo "  (o pacote nao tem $f)"; fi
done
if [ -f "$PK/.servidor_parado_pelo_rito" ]; then parar "o marcador .servidor_parado_pelo_rito ficou no pacote: o servidor do modelo pode estar parado ($(cat "$PK/.servidor_parado_pelo_rito"))"; fi
set +e; (cd "$CONFOUT" && $PY conferir_rito_v395.py) > "$CONFOUT/conferir_rito_v395_stdout.txt" 2>&1; c=$?; set -e
cut -c1-240 "$CONFOUT/conferir_rito_v395_stdout.txt"
[ "$c" = "0" ] && tail -1 "$CONFOUT/conferir_rito_v395_stdout.txt" | grep -q "^TUDO BATE" || parar "CONFERIDOR REPROVOU (rc=$c) -- nada foi escrito nas superficies"
fi
if quer 2; then
echo "== 2. a leitura da rodada $(date +%T)"
set +e; $PY "$SEL/leitura_v395.py" > "$SEL/leitura_v395_out.txt" 2>&1; l=$?; set -e
tail -1 "$SEL/leitura_v395_out.txt" | cut -c1-600
[ "$l" = "0" ] || parar "a LEITURA tem PROBLEMAS (saida inteira em $SEL/leitura_v395_out.txt)"
fi
if quer 3; then
echo "== 3. ENSAIO em COPIAS: superficies (plano conferido antes da primeira escrita) e a arvore em DRY (nada real e' tocado)"
rm -rf "${ENS:?}" "${ENST:?}"; mkdir -p "$ENS" "$ENST"
cp -p "$NOS/MEMORIA_DA_LINHAGEM.md" "$NOS/DESENHO_DO_FECHAMENTO_QG.md" "$ATLD/TGL_ATLAS.md" "$ATLD/TGL_CORE_MEMORY.md" \
      "$UMEM/MEMORY.md" "$UMEM/MEMORY_2.md" "$HAJA" "$ENS/"
for t in $TOPICOS; do cp -p "$UMEM/$t" "$ENS/"; done
if [ -n "$V395_AVISO_REIVINDICACAO" ]; then cp -p "$AVISO" "$ENS/"; fi
set +e; $PY "$SEL/superficies_v395.py" --copias "$(cygpath -w "$ENS")" > "$SEL/ensaio_superficies_out.txt" 2>&1; es=$?; set -e
tail -24 "$SEL/ensaio_superficies_out.txt" | cut -c1-260
[ "$es" = "0" ] || parar "o ENSAIO das superficies falhou (rc=$es) -- nada real foi tocado"
n=$(wc -c < "$ENS/MEMORY.md"); l=$(wc -l < "$ENS/MEMORY.md"); echo "  MEMORY.md da copia: $n B, $l linhas"
[ "$n" -lt 24000 ] || parar "o MEMORY.md da copia chegou a 24 000 B ($n)"
[ "$l" -le 195 ] || parar "o MEMORY.md da copia passou de 195 linhas ($l)"
cp -p "$TOOLS/arvore_da_prova.py" "$TOOLS/atlas_indice.py" "$ENST/"
if [ -f "$SEL/patch_arvore_indice_v395.py" ]; then
  $PY "$SEL/patch_arvore_indice_v395.py" --tools "$(cygpath -w "$ENST")" || parar "o ENSAIO do patch da arvore/indice recusou ou falhou (so copias foram tocadas)"
else
  echo "  (sem patch_arvore_indice_v395.py: a arvore e o indice rodam SEM linha nova da v395 -- a v395 nao tem patch da arvore/indice; as ferramentas escrevem o sha16 sozinhas (na v394 o fizeram); o passo 3 confere isso ANTES de gravar)"
fi
(cd "$ENST" && $PY_B arvore_da_prova.py v395 dry) || parar "a arvore_da_prova.py (copia, dry) falhou"
[ -f "$ENST/arvore_dry.md" ] || parar "a arvore (dry) nao gerou arvore_dry.md em $ENST"
echo "  (fail-early do passo 9: a arvore (dry) e as COPIAS das superficies tem de trazer o sha16 e os marcadores da v395 ANTES de qualquer escrita real)"
exige "$ENST/arvore_dry.md" "$S16"
TOPICO_NOVO=$(topico_novo) || parar "nao li TOPICO_NOVO de textos_v395.py (o arquivo ainda tem trecho marcado para reescrever?)"
exige "$ENS/MEMORIA_DA_LINHAGEM.md" "$S16" "<!-- linhagem_v395_selada -->" "psibit_v395" "kh_n1_cobertura_v395"
exige "$ENS/DESENHO_DO_FECHAMENTO_QG.md" "<!-- adendo_v395_selada -->" "$S16"
exige "$ENS/TGL_ATLAS.md" "<!-- atlas_v395_selada -->" "$S16" "psibit_v395" "kh_n1_cobertura_v395"
exige "$ENS/TGL_CORE_MEMORY.md" "<!-- core_v395_selada -->" "$S16"
exige "$ENS/CLAUDE.md" "<!-- haja_luz_v395_selada -->" "$S16"
exige "$ENS/MEMORY.md" "$S16"
exige "$ENS/MEMORY_2.md" "v395"
exige "$ENS/estatuto-da-prova-07out.md" "<!-- v395_selada -->" "$S16"
exige "$ENS/$TOPICO_NOVO" "$S16" "psibit_v395" "kh_n1_cobertura_v395"
fi
if quer 4; then
if [ -f "$SEL/patch_arvore_indice_v395.py" ]; then
echo "== 4. patches arvore/indice"; $PY "$SEL/patch_arvore_indice_v395.py" || parar "patch arvore/indice recusou/falhou (backups _p395 ao lado)"
else
echo "== 4. patches arvore/indice: PULADO (opcional; sem patch_arvore_indice_v395.py)"
fi
fi
if quer 5; then
echo "== 5. arvore"; (cd "$TOOLS" && $PY_B arvore_da_prova.py v395) || parar "arvore_da_prova.py v395 falhou"
fi
if quer 6; then
echo "== 6. atlas + indice (a ordem da v390: o indice antes das superficies)"; (cd "$TOOLS" && $PY_B atlas_indice.py v395) || parar "atlas_indice.py v395 falhou"
fi
if quer 7; then
echo "== 7. superficies (real: appends datados; a guarda P18 em todo texto; sem errata nova no CLAUDE.md da raiz)"
$PY "$SEL/superficies_v395.py" || parar "superficies_v395.py parou (backups .bak_<STAMP>_sup395 ao lado; rerodar e IDEMPOTENTE)"
fi
if quer 8; then
echo "== 8. espelho da memoria"
set +e; $PY_B "$PORTA" > "$SEL/porta_memoria_v395_out.txt" 2>&1; pm=$?; set -e
tail -1 "$SEL/porta_memoria_v395_out.txt"
[ "$pm" = "0" ] || parar "porta_memoria.py saiu com rc=$pm"
fi
if quer 9; then
echo "== 9. regra da linhagem completa: o MARCADOR DO SELO e o sha16 do um.py v395 ($S16) em cada superficie (zero e' falha visivel)"
exige "$NOS/MEMORIA_DA_LINHAGEM.md" "$S16" "<!-- linhagem_v395_selada -->" "psibit_v395" "kh_n1_cobertura_v395"
exige "$NOS/DESENHO_DO_FECHAMENTO_QG.md" "<!-- adendo_v395_selada -->" "$S16"
exige "$ATLD/TGL_ATLAS.md" "<!-- atlas_v395_selada -->" "$S16" "psibit_v395" "kh_n1_cobertura_v395"
exige "$ATLD/TGL_INDICE_VIVO.md" "$S16"
exige "$ATLD/TGL_CORE_MEMORY.md" "<!-- core_v395_selada -->" "$S16"
exige "$NOS/A_PROVA_DA_QG_TGL_arvore.md" "$S16"
exige "$HAJA" "<!-- haja_luz_v395_selada -->" "$S16"
exige "$UMEM/MEMORY.md" "$S16"
exige "$UMEM/MEMORY_2.md" "v395"
for t in missao-ultima-flag-um-py.md central-de-patentes-estado.md; do exige "$UMEM/$t" "$S16"; done
exige "$UMEM/estatuto-da-prova-07out.md" "<!-- v395_selada -->" "$S16"
TOPICO_NOVO=$(topico_novo) || parar "nao li TOPICO_NOVO de textos_v395.py"
exige "$UMEM/$TOPICO_NOVO" "$S16" "psibit_v395" "kh_n1_cobertura_v395"
if [ -n "$V395_AVISO_REIVINDICACAO" ]; then exige "$AVISO" "<!-- aviso_v395_selada -->" "$S16"; else echo "  (AVISO_GERENCIA.md: PULADO -- sem V395_AVISO_REIVINDICACAO; escrever depois, sob reivindicacao)"; fi
n=$(wc -c < "$UMEM/MEMORY.md"); l=$(wc -l < "$UMEM/MEMORY.md"); echo "  MEMORY.md: $n B (limite 24000), $l linhas (limite 195)"
[ "$n" -lt 24000 ] || parar "MEMORY.md chegou a 24 000 B ($n)"
[ "$l" -le 195 ] || parar "MEMORY.md passou de 195 linhas ($l): o carregador do harness o corta acima de 200"
fi
if quer 10; then
echo "== 10. B(n) da Bancada, ENSAIO pos-selo, passo simples v394 -> v395 (sem salto), esboco R3.5 (nada e' gravado na Bancada; o servico pode estar no ar) $(date +%T)"
b3_prepara 10
SAIDA_E="$PK/bancada_B3_ensaio_$(date +%Y%m%d_%H%M%S)"
set +e
$PY "$W_ESB" --bancada 'C:\IALD\Bancada_Um' --producao --nos "$W_NOS" --versao v395 --fase pos_selo --modo ensaio --bateria "$W_BAT" --bateria-sha256 "$BAT" \
    --recibo-pre-selo "$W_RPS" --recibo-pre-selo-sha256 "$RPS" --selo-anterior "$W_SELO" --kernel-manifesto-anterior "$W_KMAN" \
    --kernel-recibo "$W_KR" --kernel-recibo-sha256 "$KRSHA" --criterios "$W_CRI" --criterios-sha256 "$CRI" \
    --saida "$(cygpath -w "$SAIDA_E")" > "$SEL/b3_ensaio_out.txt" 2>&1; b3=$?
set -e
tail -4 "$SEL/b3_ensaio_out.txt" | cut -c1-400
[ "$b3" = "0" ] || parar "o B(n) ENSAIO reprovou (rc=$b3): saida inteira em $SEL/b3_ensaio_out.txt"
$PY "$SEL/b3_recibo_v395.py" "$(cygpath -w "$SEL/b3_ensaio_out.txt")" ensaio || parar "o recibo do B(n) ENSAIO nao confere"
fi
if quer 10a; then
echo "== 10-bis-a. a parada do servico da Bancada Um (porta 18777), com recibo"
RP="$PK/bancada_B3_servico/RECIBO_PARADA_v395.json"
[ -f "$RP" ] || aguarda "sem o recibo da PARADA do um_bancada.py ($RP): o servico esta no ar na porta 18777 e tem de ser PARADO pelo PID (ato do operador; nunca por nome); so' depois se gera o recibo com bancada_B3_servico/recibo_parada_v395.py (exige V395_AUTORIZACAO_OPERADOR no ambiente; confere a porta fechada e zero processo um_bancada.py). Sem esse recibo a cadeia para aqui."
$PY -c "import socket,sys
try:
    socket.create_connection(('127.0.0.1', 18777), timeout=1.5).close()
except OSError:
    sys.exit(0)
sys.exit(1)" || parar "o servico da Bancada esta no AR (a porta 18777 responde) apesar do recibo de parada"
echo "  recibo da parada: $RP (sha256 $(sha256f "$(cygpath -w "$RP")")); porta 18777 fechada"
fi
if quer 10b; then
echo "== 10-bis. B(n) APLICAR, passo simples v394 -> v395 (sem salto), esboco R3.5 (grava o manifesto B<n> na Bancada de producao: backup de bytes, rollback se falhar) $(date +%T)"
[ "$B3_AUTORIZADO" = "sim" ] || aguarda "a B(n) nao esta autorizada: ato da gerencia sob evento c1 (SINCRONIZACAO_BANCADA, que nomeia a v395) + autorizacao do operador. Definir B3_AUTORIZADO=sim, EVENTO=<seq> e EVENTO_HASH=<hash16 do retorno de iald.py anotar>, com o servico parado (10-bis-a) e o recibo da parada, e retomar com CHAIN_DE=10b"
[ -n "$EVENTO" ] && [ -n "$EVENTO_HASH" ] || aguarda "faltam EVENTO e EVENTO_HASH (o elo do evento c1 nomeando a gravacao)"
[ -f "$PK/bancada_B3_servico/RECIBO_PARADA_v395.json" ] || aguarda "sem o recibo da parada do servico (10-bis-a)"
b3_prepara 10b
SAIDA_B3="$PK/bancada_B3"; k=1; while [ -e "$SAIDA_B3" ]; do k=$((k+1)); SAIDA_B3="$PK/bancada_B3_$k"; done
echo "  saida do B(n): $SAIDA_B3 (pasta nova)"
set +e
$PY "$W_ESB" --bancada 'C:\IALD\Bancada_Um' --producao --nos "$W_NOS" --versao v395 --fase pos_selo --modo aplicar --bateria "$W_BAT" --bateria-sha256 "$BAT" \
    --evento "$EVENTO" --evento-hash "$EVENTO_HASH" \
    --recibo-pre-selo "$W_RPS" --recibo-pre-selo-sha256 "$RPS" --selo-anterior "$W_SELO" --kernel-manifesto-anterior "$W_KMAN" \
    --kernel-recibo "$W_KR" --kernel-recibo-sha256 "$KRSHA" --criterios "$W_CRI" --criterios-sha256 "$CRI" \
    --saida "$(cygpath -w "$SAIDA_B3")" > "$SEL/b3_aplicar_out.txt" 2>&1; b3=$?
set -e
tail -4 "$SEL/b3_aplicar_out.txt" | cut -c1-400
[ "$b3" = "0" ] || parar "o B(n) APLICAR reprovou (rc=$b3): saida inteira em $SEL/b3_aplicar_out.txt; NADA foi restaurado por esta cadeia (o esboco faz o seu rollback)"
$PY "$SEL/b3_recibo_v395.py" "$(cygpath -w "$SEL/b3_aplicar_out.txt")" aplicar || parar "o recibo do B(n) APLICAR nao confere"
fi
if quer 10c; then
echo "== 10-ter. o religamento do servico e a reconexao dos adaptadores MCP (ato do operador)"
RR="$PK/bancada_B3_servico/RECIBO_RELIGAMENTO_v395.json"
[ -f "$RR" ] || aguarda "sem o recibo do RELIGAMENTO do um_bancada.py ($RR): religar o servico (ato do operador; o comando esta no campo religar do RECIBO_PARADA_v395.json) e gerar o recibo com bancada_B3_servico/recibo_religamento_v395.py (exige V395_AUTORIZACAO_OPERADOR; confere a versao servida v395, o sha do manifesto novo, o um.py e o PID); reconectar os adaptadores MCP das sessoes e ato do operador"
echo "  recibo do religamento: $RR (sha256 $(sha256f "$(cygpath -w "$RR")")); o fechar o confere contra o recibo do 10-bis"
fi
if quer 11; then
echo "== 11. fechar (manifesto, arquivo, os dois diffs, handoff) -- recusa sem os tres recibos do B(3)"
$PY "$SEL/fechar_v395.py" || parar "fechar_v395.py falhou"
fi
if quer 12; then
echo "== 12. registro no mapa de rotas: so MONTA o JSON e o comando (o registro e' ato da gerencia)"
$PY "$SEL/registrar_mapa_v395.py" || parar "registrar_mapa_v395.py falhou"
fi
if quer 13; then
echo "== 13. o inventario da bancada Lean (work\\inventario_bancada) regenerado; copia para memory\\ com backup de bytes"
(cd "$INV" && $PY_B inventario_bancada.py > "$SEL/inventario_bancada_out.txt" 2>&1 && $PY_B gerar_documento.py >> "$SEL/inventario_bancada_out.txt" 2>&1) || parar "o inventario da bancada falhou (ver $SEL/inventario_bancada_out.txt)"
tail -2 "$SEL/inventario_bancada_out.txt" | cut -c1-240
for f in INVENTARIO_BANCADA_CHATGPT.md INVENTARIO_BANCADA_CHATGPT.json; do
  [ -f "$INV/$f" ] || parar "o inventario nao gerou $f"
  if [ -f "$ATLD/$f" ]; then B="$ATLD/$f.bak_$(date +%Y%m%d_%H%M%S)_v395"; cp -p "$ATLD/$f" "$B"; cmp "$ATLD/$f" "$B" || parar "backup de bytes falhou: $B"; fi
  cp -p "$INV/$f" "$ATLD/$f.tmp_v395" && mv "$ATLD/$f.tmp_v395" "$ATLD/$f"; cmp "$INV/$f" "$ATLD/$f" || parar "a copia do inventario difere: $f"
done
fi
if quer 14; then
echo "== 14. o Nos vivo reconstruido (le o mapa de rotas: rodar depois do registro da gerencia no passo 12)"
$PY_B /c/IALD/NOS_VIVO/construir.py > "$SEL/nos_vivo_out.txt" 2>&1 || parar "NOS_VIVO/construir.py falhou (ver $SEL/nos_vivo_out.txt)"
tail -3 "$SEL/nos_vivo_out.txt" | cut -c1-240
fi
echo "== FIM $(date +%T)"
