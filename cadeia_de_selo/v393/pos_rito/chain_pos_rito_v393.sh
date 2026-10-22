#!/bin/sh
# v393 (14/10): CADEIA POS-RITO -- no molde do chain_pos_rito_v392.sh (derivada por derivar_cadeia_v393.py; mesma ordem de passos 0..14 e mesmos portoes). O rito ja terminou (rito_v393.sh em segundo plano;
# RITO_RC=<rc> no fim do Nos\rodada_v393_stdout.txt). A v393 acrescenta A REGRA e O CORACAO (3 pedras, o consumidor numerico que consome a regra, o selo do coracao).
# ORDEM: 0 guardas -> 1 o CONFERIDOR (copia byte a byte; so leitura do Nos) -> 2 a LEITURA (PROBLEMAS param) -> 3 ENSAIO das superficies em COPIAS (o plano e' conferido antes da primeira escrita; a arvore em dry)
# -> 4 patch arvore/indice (OPCIONAL: so' se existir patch_arvore_indice_v393.py; o da v392 era das erratas CR-08/CR-02 e foi descartado) -> 5 a arvore -> 6 atlas+indice -> 7 superficies reais (appends datados;
# SEM errata nova no CLAUDE.md da raiz) -> 8 porta_memoria.py (o ATLAS a mao nao se toca) -> 9 regra da linhagem completa COM O MARCADOR DO SELO (zero e' falha visivel) e a guarda de MEMORY.md (<24.000 B,
# <=195 linhas) -> 10 B(3) da Bancada, ENSAIO pos-selo -> 10a parada do servico (AGUARDA_OPERADOR) -> 10b B(3) APLICAR (so com B3_AUTORIZADO=sim e o evento c1) -> 10c religamento (AGUARDA_OPERADOR)
# -> 11 fechar -> 12 registrar_mapa (so MONTA o JSON e o comando) -> 13 inventario da bancada Lean -> 14 Nos vivo.
# Sai na primeira reprovacao e NAO restaura nada sozinha: a decisao de restaurar e' da gerencia. Retomada: CHAIN_DE=<passo> (e CHAIN_ATE=<passo>); os passos 3 a 9 sao idempotentes.
# Ambiente: B3_AUTORIZADO=sim, EVENTO=<seq> e EVENTO_HASH=<hash16> (so o 10b); V393_AVISO_REIVINDICACAO=<texto> (so' com ela o AVISO_GERENCIA.md e' escrito; sem ela e' PULADO e dito).
# Os pinos do B(n) vem de PINOS_BN_v393.json (lidos na hora; hash nunca de memoria). Sem o PINO recibo_pre_selo (a fase pre_selo da B(n) nao foi preparada) o 10 PARA em AGUARDA_OPERADOR.
# Codigos de saida: 0 fim; 1 reprovacao (PARADA); 20 AGUARDA_OPERADOR (parada de proposito, nao e' falha).
PK="/c/IALD/Central de Patentes/work/cadeia_de_selo/v393"; SEL="$PK/pos_rito"
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
aguarda() { echo "AGUARDA_OPERADOR: $*"; echo "(a cadeia parou de proposito, nao e' falha; retomar com CHAIN_DE=<passo>)"; exit 20; }
ORDEM="0 1 2 3 4 5 6 7 8 9 10 10a 10b 10c 11 12 13 14"
DE="${CHAIN_DE:-0}"; ATE="${CHAIN_ATE:-14}"
pos() { i=0; for x in $ORDEM; do if [ "$x" = "$1" ]; then echo "$i"; return 0; fi; i=$((i+1)); done; echo "-1"; }
quer() { p=$(pos "$1"); d=$(pos "$DE"); a=$(pos "$ATE"); if [ "$d" -lt 0 ] || [ "$a" -lt 0 ]; then echo "CHAIN_DE/CHAIN_ATE desconhecido (validos: $ORDEM)"; exit 1; fi; [ "$p" -ge "$d" ] && [ "$p" -le "$a" ]; }
exige() { f="$1"; shift; for m in "$@"; do n=$(grep -c -F -- "$m" "$f" || true); echo "  $n  $(basename "$f")  [$m]"; [ "$n" -gt 0 ] || parar "superficie sem o marcador da v393 ($m): $f"; done; }
sha256f() { $PY -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" "$1"; }
pino() { $PY -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8'))[sys.argv[2]]['sha256'])" "$(cygpath -w "$PK/PINOS_BN_v393.json")" "$1"; }
pinop() { $PY -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8'))[sys.argv[2]]['path'])" "$(cygpath -w "$PK/PINOS_BN_v393.json")" "$1"; }
b3_prepara() {
  for k in bateria criterios esboco_R3_3 kernel_recibo candidato esperados pins_do_candidato; do
    p=$(pinop "$k"); a=$(pino "$k"); b=$(sha256f "$p"); [ "$a" = "$b" ] || parar "o pino $k diverge do arquivo (pino $a != arquivo $b)"
  done
  tem_pino recibo_pre_selo || aguarda "o PINO recibo_pre_selo nao esta em PINOS_BN_v393.json: o recibo da fase pre_selo da B(n) nao foi preparado (ato da gerencia: rodar o esboco R3.3 na fase pre_selo, pinar o recibo e retomar com CHAIN_DE=$1)"
  p=$(pinop recibo_pre_selo); a=$(pino recibo_pre_selo); b=$(sha256f "$p"); [ "$a" = "$b" ] || parar "o pino recibo_pre_selo diverge do arquivo (pino $a != arquivo $b)"
  BAT=$(pino bateria); CRI=$(pino criterios); RPS=$(pino recibo_pre_selo)
  W_BAT=$(cygpath -w "$(pinop bateria)"); W_CRI=$(cygpath -w "$(pinop criterios)"); W_RPS=$(cygpath -w "$(pinop recibo_pre_selo)"); W_ESB=$(cygpath -w "$(pinop esboco_R3_3)"); W_NOS=$(cygpath -w "$NOS")
  # o selo e o manifesto do kernel da v392 (versao anterior): pinados se houver pino; senao, as copias de custodia da pasta base_v392 (SEM pino, hash lido na hora; o esboco as cruza com o pino da Bancada, R31-3)
  if tem_pino selo_anterior_v392; then p=$(pinop selo_anterior_v392); a=$(pino selo_anterior_v392); b=$(sha256f "$p"); [ "$a" = "$b" ] || parar "o pino selo_anterior_v392 diverge do arquivo"; W_SELO=$(cygpath -w "$p")
  else W_SELO=$(cygpath -w "$PK/base_v392/um_absoluto_selo.json"); [ -f "$PK/base_v392/um_absoluto_selo.json" ] || parar "sem o selo da v392 em $PK/base_v392"; echo "  selo anterior SEM pino (lido na hora): $(sha256f "$W_SELO")"; fi
  if tem_pino kernel_manifesto_anterior_v392; then p=$(pinop kernel_manifesto_anterior_v392); a=$(pino kernel_manifesto_anterior_v392); b=$(sha256f "$p"); [ "$a" = "$b" ] || parar "o pino kernel_manifesto_anterior_v392 diverge do arquivo"; W_KMAN=$(cygpath -w "$p")
  else W_KMAN=$(cygpath -w "$PK/base_v392/tgl_kernel_proof_manifest.json"); [ -f "$PK/base_v392/tgl_kernel_proof_manifest.json" ] || parar "sem o manifesto do kernel da v392 em $PK/base_v392"; echo "  manifesto do kernel anterior SEM pino (lido na hora): $(sha256f "$W_KMAN")"; fi
  KR="$PK/kernel/KERNEL_RECIBO_v393.json"; [ -f "$KR" ] || parar "sem o recibo do kernel: $KR"
  W_KR=$(cygpath -w "$KR"); KRSHA=$(sha256f "$W_KR"); [ "$KRSHA" = "$(pino kernel_recibo)" ] || parar "o recibo do kernel diverge do pino"; echo "  recibo do kernel (sha256 LIDO NA HORA, igual ao pino): $KRSHA"
  $PY -c "import json,os,sys;sys.exit(0 if os.path.isdir(json.load(open(sys.argv[1],encoding='utf-8'))['arvore']) else 1)" "$W_KR" || aguarda "a arvore so-fontes do recibo do kernel (campo arvore: C:/t/k393/arvore) nao existe mais: rodar $PY $PK/refazer_arvore_v393_pos_selo.py (refaz a arvore a partir do kernel do Nos, sem build; ato da gerencia) e retomar com CHAIN_DE=$1"
}
tem_pino() { $PY -c "import json,sys;sys.exit(0 if sys.argv[2] in json.load(open(sys.argv[1],encoding='utf-8')) else 1)" "$(cygpath -w "$PK/PINOS_BN_v393.json")" "$1"; }
echo "== 0. guardas $(date +%T)"
command -v python > /dev/null || parar "python nao esta no PATH"
S16=$($PY -c "import glob,json,os,sys;ps=sorted(glob.glob(os.path.join(sys.argv[1],'APLICADO_AO_CANONICO_*.json')));print(json.load(open(ps[-1],encoding='utf-8'))['um_py_novo']['sha16'])" "$(cygpath -w "$PK")") || parar "APLICADO_AO_CANONICO_*.json ilegivel em $PK"
$PY -c "
import hashlib, json, glob, os, sys
um, pk = sys.argv[1], sys.argv[2]
ap = json.load(open(sorted(glob.glob(os.path.join(pk, 'APLICADO_AO_CANONICO_*.json')))[-1], encoding='utf-8'))
es = json.load(open(os.path.join(pk, 'ESPERADOS_v393.json'), encoding='utf-8'))
h = hashlib.sha256(open(um, 'rb').read()).hexdigest()[:16]
print('um.py no disco', h, '== instalado', ap['um_py_novo']['sha16'], '== candidato', es['candidato_sha16'])
sys.exit(0 if h == ap['um_py_novo']['sha16'] == es['candidato_sha16'] else 1)" "$(cygpath -w "$NOS/um.py")" "$(cygpath -w "$PK")" || parar "o um.py do disco nao e o instalado"
for f in "$TOOLS/arvore_da_prova.py" "$TOOLS/atlas_indice.py" "$PORTA" "$PK/conferir_rito_v393.py" "$PK/ESPERADOS_v393.json" "$PK/guarda_p18_v393.py" "$PK/PINOS_BN_v393.json" \
         "$PK/refazer_arvore_v393_pos_selo.py" "$PK/kernel/KERNEL_RECIBO_v393.json" "$HAJA" "$INV/inventario_bancada.py" "$INV/gerar_documento.py" "/c/IALD/NOS_VIVO/construir.py" \
         "$SEL/leitura_v393.py" "$SEL/textos_v393.py" "$SEL/superficies_v393.py" "$SEL/fechar_v393.py" "$SEL/registrar_mapa_v393.py" "$SEL/b3_recibo_v393.py"; do
  [ -f "$f" ] || parar "ferramenta/superficie ausente: $f"; done
$PY "$PK/guarda_p18_v393.py" "$SEL/textos_v393.py" > /dev/null || parar "a guarda de texto P18 achou violacao em textos_v393.py"
STD="$NOS/rodada_v393_stdout.txt"
grep -q '^RITO_RC=' "$STD" || parar "o rito nao acabou (sem RITO_RC= no stdout)"
tail -3 "$STD" | cut -c1-240
if quer 1; then
echo "== 1. conferidor (copia byte a byte; so leitura do Nos) $(date +%T)"
rm -rf "$CONFOUT"; mkdir -p "$CONFOUT"
cp -p "$PK/conferir_rito_v393.py" "$CONFOUT/"; cmp "$PK/conferir_rito_v393.py" "$CONFOUT/conferir_rito_v393.py" || parar "copia do conferidor difere"
for f in ESPERADOS_v393.json rito_servidor_v393.log rito_v393_sinal.txt; do
  if [ -f "$PK/$f" ]; then cp -p "$PK/$f" "$CONFOUT/$f"; cmp "$PK/$f" "$CONFOUT/$f" || parar "copia difere: $f"; echo "  copiado byte a byte: $f"; else echo "  (o pacote nao tem $f)"; fi
done
if [ -f "$PK/.servidor_parado_pelo_rito" ]; then parar "o marcador .servidor_parado_pelo_rito ficou no pacote: o servidor do modelo pode estar parado ($(cat "$PK/.servidor_parado_pelo_rito"))"; fi
set +e; (cd "$CONFOUT" && $PY conferir_rito_v393.py) > "$CONFOUT/conferir_rito_v393_stdout.txt" 2>&1; c=$?; set -e
cut -c1-240 "$CONFOUT/conferir_rito_v393_stdout.txt"
[ "$c" = "0" ] && tail -1 "$CONFOUT/conferir_rito_v393_stdout.txt" | grep -q "^TUDO BATE" || parar "CONFERIDOR REPROVOU (rc=$c) -- nada foi escrito nas superficies"
fi
if quer 2; then
echo "== 2. a leitura da rodada $(date +%T)"
set +e; $PY "$SEL/leitura_v393.py" > "$SEL/leitura_v393_out.txt" 2>&1; l=$?; set -e
tail -1 "$SEL/leitura_v393_out.txt" | cut -c1-600
[ "$l" = "0" ] || parar "a LEITURA tem PROBLEMAS (saida inteira em $SEL/leitura_v393_out.txt)"
fi
if quer 3; then
echo "== 3. ENSAIO em COPIAS: superficies (plano conferido antes da primeira escrita) e a arvore em DRY (nada real e' tocado)"
rm -rf "${ENS:?}" "${ENST:?}"; mkdir -p "$ENS" "$ENST"
cp -p "$NOS/MEMORIA_DA_LINHAGEM.md" "$NOS/DESENHO_DO_FECHAMENTO_QG.md" "$ATLD/TGL_ATLAS.md" "$ATLD/TGL_CORE_MEMORY.md" \
      "$UMEM/MEMORY.md" "$UMEM/MEMORY_2.md" "$HAJA" "$ENS/"
for t in $TOPICOS; do cp -p "$UMEM/$t" "$ENS/"; done
if [ -n "$V393_AVISO_REIVINDICACAO" ]; then cp -p "$AVISO" "$ENS/"; fi
set +e; $PY "$SEL/superficies_v393.py" --copias "$(cygpath -w "$ENS")" > "$SEL/ensaio_superficies_out.txt" 2>&1; es=$?; set -e
tail -24 "$SEL/ensaio_superficies_out.txt" | cut -c1-260
[ "$es" = "0" ] || parar "o ENSAIO das superficies falhou (rc=$es) -- nada real foi tocado"
n=$(wc -c < "$ENS/MEMORY.md"); l=$(wc -l < "$ENS/MEMORY.md"); echo "  MEMORY.md da copia: $n B, $l linhas"
[ "$n" -lt 24000 ] || parar "o MEMORY.md da copia chegou a 24 000 B ($n)"
[ "$l" -le 195 ] || parar "o MEMORY.md da copia passou de 195 linhas ($l)"
cp -p "$TOOLS/arvore_da_prova.py" "$TOOLS/atlas_indice.py" "$ENST/"
if [ -f "$SEL/patch_arvore_indice_v393.py" ]; then
  $PY "$SEL/patch_arvore_indice_v393.py" --tools "$(cygpath -w "$ENST")" || parar "o ENSAIO do patch da arvore/indice recusou ou falhou (so copias foram tocadas)"
else
  echo "  (sem patch_arvore_indice_v393.py: a arvore e o indice rodam SEM linha nova da v393 -- o patch da v392 era das erratas CR-08/CR-02 e foi descartado; ver o relatorio)"
fi
(cd "$ENST" && $PY_B arvore_da_prova.py v393 dry) || parar "a arvore_da_prova.py (copia, dry) falhou"
fi
if quer 4; then
if [ -f "$SEL/patch_arvore_indice_v393.py" ]; then
echo "== 4. patches arvore/indice"; $PY "$SEL/patch_arvore_indice_v393.py" || parar "patch arvore/indice recusou/falhou (backups _p393 ao lado)"
else
echo "== 4. patches arvore/indice: PULADO (opcional; sem patch_arvore_indice_v393.py)"
fi
fi
if quer 5; then
echo "== 5. arvore"; (cd "$TOOLS" && $PY_B arvore_da_prova.py v393) || parar "arvore_da_prova.py v393 falhou"
fi
if quer 6; then
echo "== 6. atlas + indice (a ordem da v390: o indice antes das superficies)"; (cd "$TOOLS" && $PY_B atlas_indice.py v393) || parar "atlas_indice.py v393 falhou"
fi
if quer 7; then
echo "== 7. superficies (real: appends datados; a guarda P18 em todo texto; sem errata nova no CLAUDE.md da raiz)"
$PY "$SEL/superficies_v393.py" || parar "superficies_v393.py parou (backups .bak_<STAMP>_sup393 ao lado; rerodar e IDEMPOTENTE)"
fi
if quer 8; then
echo "== 8. espelho da memoria"
set +e; $PY_B "$PORTA" > "$SEL/porta_memoria_v393_out.txt" 2>&1; pm=$?; set -e
tail -1 "$SEL/porta_memoria_v393_out.txt"
[ "$pm" = "0" ] || parar "porta_memoria.py saiu com rc=$pm"
fi
if quer 9; then
echo "== 9. regra da linhagem completa: o MARCADOR DO SELO e o sha16 do um.py v393 ($S16) em cada superficie (zero e' falha visivel)"
exige "$NOS/MEMORIA_DA_LINHAGEM.md" "$S16" "<!-- linhagem_v393_selada -->" "kh_n1_cobertura_v392"
exige "$NOS/DESENHO_DO_FECHAMENTO_QG.md" "<!-- adendo_v393_selada -->" "$S16"
exige "$ATLD/TGL_ATLAS.md" "<!-- atlas_v393_selada -->" "$S16" "kh_n1_cobertura_v392"
exige "$ATLD/TGL_INDICE_VIVO.md" "$S16"
exige "$ATLD/TGL_CORE_MEMORY.md" "<!-- core_v393_selada -->" "$S16"
exige "$NOS/A_PROVA_DA_QG_TGL_arvore.md" "$S16"
exige "$HAJA" "<!-- haja_luz_v393_selada -->" "$S16"
exige "$UMEM/MEMORY.md" "$S16"
exige "$UMEM/MEMORY_2.md" "v393"
for t in missao-ultima-flag-um-py.md central-de-patentes-estado.md; do exige "$UMEM/$t" "$S16"; done
exige "$UMEM/estatuto-da-prova-07out.md" "<!-- v393_selada -->" "$S16"
exige "$UMEM/v393-selada-a-regra-e-o-coracao-14out.md" "$S16" "kh_n1_cobertura_v392"
if [ -n "$V393_AVISO_REIVINDICACAO" ]; then exige "$AVISO" "<!-- aviso_v393_selada -->" "$S16"; else echo "  (AVISO_GERENCIA.md: PULADO -- sem V393_AVISO_REIVINDICACAO; escrever depois, sob reivindicacao)"; fi
n=$(wc -c < "$UMEM/MEMORY.md"); l=$(wc -l < "$UMEM/MEMORY.md"); echo "  MEMORY.md: $n B (limite 24000), $l linhas (limite 195)"
[ "$n" -lt 24000 ] || parar "MEMORY.md chegou a 24 000 B ($n)"
[ "$l" -le 195 ] || parar "MEMORY.md passou de 195 linhas ($l): o carregador do harness o corta acima de 200"
fi
if quer 10; then
echo "== 10. B(3) da Bancada, ENSAIO pos-selo (nada e' gravado na Bancada; o servico pode estar no ar) $(date +%T)"
b3_prepara 10
SAIDA_E="$PK/bancada_B3_ensaio_$(date +%Y%m%d_%H%M%S)"
set +e
$PY "$W_ESB" --bancada 'C:\IALD\Bancada_Um' --producao --nos "$W_NOS" --versao v393 --fase pos_selo --modo ensaio --bateria "$W_BAT" --bateria-sha256 "$BAT" \
    --recibo-pre-selo "$W_RPS" --recibo-pre-selo-sha256 "$RPS" --selo-anterior "$W_SELO" --kernel-manifesto-anterior "$W_KMAN" \
    --kernel-recibo "$W_KR" --kernel-recibo-sha256 "$KRSHA" --criterios "$W_CRI" --criterios-sha256 "$CRI" \
    --saida "$(cygpath -w "$SAIDA_E")" > "$SEL/b3_ensaio_out.txt" 2>&1; b3=$?
set -e
tail -4 "$SEL/b3_ensaio_out.txt" | cut -c1-400
[ "$b3" = "0" ] || parar "o B(3) ENSAIO reprovou (rc=$b3): saida inteira em $SEL/b3_ensaio_out.txt"
$PY "$SEL/b3_recibo_v393.py" "$(cygpath -w "$SEL/b3_ensaio_out.txt")" ensaio || parar "o recibo do B(3) ENSAIO nao confere"
fi
if quer 10a; then
echo "== 10-bis-a. a parada do servico da Bancada Um (porta 18777), com recibo"
RP="$PK/bancada_B3_servico/RECIBO_PARADA_v393.json"
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
echo "== 10-bis. B(3) APLICAR (grava o manifesto B3 na Bancada de producao: backup de bytes, rollback se falhar) $(date +%T)"
[ "$B3_AUTORIZADO" = "sim" ] || aguarda "a B3 nao esta autorizada: ato da gerencia sob evento c1 (SINCRONIZACAO_BANCADA) + autorizacao do operador. Definir B3_AUTORIZADO=sim, EVENTO=<seq> e EVENTO_HASH=<hash16 do retorno de iald.py anotar>, com o servico parado (10-bis-a) e o recibo da parada, e retomar com CHAIN_DE=10b"
[ -n "$EVENTO" ] && [ -n "$EVENTO_HASH" ] || aguarda "faltam EVENTO e EVENTO_HASH (o elo do evento c1 nomeando a gravacao)"
[ -f "$PK/bancada_B3_servico/RECIBO_PARADA_v393.json" ] || aguarda "sem o recibo da parada do servico (10-bis-a)"
b3_prepara 10b
SAIDA_B3="$PK/bancada_B3"; k=1; while [ -e "$SAIDA_B3" ]; do k=$((k+1)); SAIDA_B3="$PK/bancada_B3_$k"; done
echo "  saida do B(3): $SAIDA_B3 (pasta nova)"
set +e
$PY "$W_ESB" --bancada 'C:\IALD\Bancada_Um' --producao --nos "$W_NOS" --versao v393 --fase pos_selo --modo aplicar --bateria "$W_BAT" --bateria-sha256 "$BAT" \
    --evento "$EVENTO" --evento-hash "$EVENTO_HASH" \
    --recibo-pre-selo "$W_RPS" --recibo-pre-selo-sha256 "$RPS" --selo-anterior "$W_SELO" --kernel-manifesto-anterior "$W_KMAN" \
    --kernel-recibo "$W_KR" --kernel-recibo-sha256 "$KRSHA" --criterios "$W_CRI" --criterios-sha256 "$CRI" \
    --saida "$(cygpath -w "$SAIDA_B3")" > "$SEL/b3_aplicar_out.txt" 2>&1; b3=$?
set -e
tail -4 "$SEL/b3_aplicar_out.txt" | cut -c1-400
[ "$b3" = "0" ] || parar "o B(3) APLICAR reprovou (rc=$b3): saida inteira em $SEL/b3_aplicar_out.txt; NADA foi restaurado por esta cadeia (o esboco faz o seu rollback)"
$PY "$SEL/b3_recibo_v393.py" "$(cygpath -w "$SEL/b3_aplicar_out.txt")" aplicar || parar "o recibo do B(3) APLICAR nao confere"
fi
if quer 10c; then
echo "== 10-ter. o religamento do servico e a reconexao dos adaptadores MCP (ato do operador)"
RR="$PK/bancada_B3_servico/RECIBO_RELIGAMENTO_v393.json"
[ -f "$RR" ] || aguarda "sem o recibo do RELIGAMENTO do um_bancada.py ($RR): religar o servico com recibo de identidade (a versao servida e v393 e o sha do manifesto e o do recibo do 10-bis) e reconectar os adaptadores MCP das sessoes (ato do operador)"
echo "  recibo do religamento: $RR (sha256 $(sha256f "$(cygpath -w "$RR")")); o fechar o confere contra o recibo do 10-bis"
fi
if quer 11; then
echo "== 11. fechar (manifesto, arquivo, os dois diffs, handoff) -- recusa sem os tres recibos do B(3)"
$PY "$SEL/fechar_v393.py" || parar "fechar_v393.py falhou"
fi
if quer 12; then
echo "== 12. registro no mapa de rotas: so MONTA o JSON e o comando (o registro e' ato da gerencia)"
$PY "$SEL/registrar_mapa_v393.py" || parar "registrar_mapa_v393.py falhou"
fi
if quer 13; then
echo "== 13. o inventario da bancada Lean (work\\inventario_bancada) regenerado; copia para memory\\ com backup de bytes"
(cd "$INV" && $PY_B inventario_bancada.py > "$SEL/inventario_bancada_out.txt" 2>&1 && $PY_B gerar_documento.py >> "$SEL/inventario_bancada_out.txt" 2>&1) || parar "o inventario da bancada falhou (ver $SEL/inventario_bancada_out.txt)"
tail -2 "$SEL/inventario_bancada_out.txt" | cut -c1-240
for f in INVENTARIO_BANCADA_CHATGPT.md INVENTARIO_BANCADA_CHATGPT.json; do
  [ -f "$INV/$f" ] || parar "o inventario nao gerou $f"
  if [ -f "$ATLD/$f" ]; then B="$ATLD/$f.bak_$(date +%Y%m%d_%H%M%S)_v393"; cp -p "$ATLD/$f" "$B"; cmp "$ATLD/$f" "$B" || parar "backup de bytes falhou: $B"; fi
  cp -p "$INV/$f" "$ATLD/$f.tmp_v393" && mv "$ATLD/$f.tmp_v393" "$ATLD/$f"; cmp "$INV/$f" "$ATLD/$f" || parar "a copia do inventario difere: $f"
done
fi
if quer 14; then
echo "== 14. o Nos vivo reconstruido (le o mapa de rotas: rodar depois do registro da gerencia no passo 12)"
$PY_B /c/IALD/NOS_VIVO/construir.py > "$SEL/nos_vivo_out.txt" 2>&1 || parar "NOS_VIVO/construir.py falhou (ver $SEL/nos_vivo_out.txt)"
tail -3 "$SEL/nos_vivo_out.txt" | cut -c1-240
fi
echo "== FIM $(date +%T)"
