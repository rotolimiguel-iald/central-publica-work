#!/bin/sh
# v384 (04/10): CADEIA POS-RITO -- no molde do chain_pos_rito_v383.sh. O rito ja foi lancado pela gerencia pelo rito_v384.sh (em segundo plano, Git Bash),
# que grava RITO_RC=<rc> no fim do Nos\rodada_v384_stdout.txt e o fim em <pacote>\rito_horarios_v384.txt, e so depois restaura o servidor do modelo nativo.
# Espera o fim SO POR LEITURA -> rito limpo (rc 0, teoremas A/A, FAIL_CLOSED_SELFTEST_PASSED, sem Traceback/[selo] AVISO, o selo EXISTE e e' v384) ->
# o CONFERIDOR do pacote (conferir_rito_v384.py, copiado BYTE A BYTE para v384_selo\conferidor junto com os arquivos que ele le de HERE: ESPERADOS_v384.json,
# rito_servidor_v384.log e rito_v384_sinal.txt, se existirem -- cmp em cada um; o NOS dele e' fixo no Nos real, nada muda) -> a LEITURA (leitura_v384: os
# hashes do pilar, do selo, do result.json, do pre-registro; PROBLEMAS param) -> SO SE TUDO BATE: manifesto -> ENSAIO das superficies em COPIAS (compactar +
# superficies) -> patches arvore/indice -> arvore_da_prova.py v384 -> atlas_indice.py v384 -> compactar (real) -> superficies (real) -> porta_memoria.py ->
# grep -c v384 em cada superficie. Se algo reprovar: PARA e imprime o que reprovou. NAO restaura nada sozinho: a decisao de restaurar e da gerencia.
# rc do rito: lido do RITO_RC= do stdout; a gerencia pode passar V384_RC=<rc> (tem de bater com o do stdout).
# O PILAR: um resultado negativo ou parcial do pilar e' RESULTADO (a leitura o classifica, com a causa, e os textos o dizem sem frase de sucesso); mas o
# conferidor CONGELADO exige o ramo 9 -- se ele reprovar SO itens do pilar, a cadeia PARA no passo 3 e imprime o diagnostico (SO itens do pilar: True e o
# sha16 da conferencia); a gerencia, se decidir registrar o negativo como resultado, roda de novo com V384_ACEITO_PILAR_NAO_CONCLUIDO=<esse sha16>: a
# leitura confere que a conferencia e' ESSA e que as falhas sao SO do pilar, e os textos dizem o aceite. Ensaiado de ponta a ponta, ate o FIM, em cada
# classe (PARCIAL, ANULADO, NOT_RUN com e sem arquivo, recusa do um.py, motor que falhou, fase que falhou) por ensaio_guardas_v384.py (04/10, corretor).
# Depois da cadeia (ato da gerencia, nesta ordem): registrar_resultado_v384.py (o JSON do mapa; a gerencia registra) -> arquivar_v384.py -> handoff_v384.py.
# >>> CONFIG (o ensaio das guardas troca SO este bloco; conferido por diff)
SP="/c/Users/rotol/AppData/Local/Temp/claude/c--IALD-Central-de-Patentes/6da8f00d-d44f-4888-a88d-fc9f73eead3d/scratchpad"
SEL="$SP/v384_selo"; PK="$SP/v384"
TOOLS="/c/IALD/Central de Patentes/work/cadeia_de_selo"
NOS="/c/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós"
UMEM="/c/Users/rotol/.claude/projects/c--IALD-Central-de-Patentes/memory"
ATLD="/c/IALD/Central de Patentes/memory"
ARVORE="$TOOLS/arvore_da_prova.py"; ATLASPY="$TOOLS/atlas_indice.py"; PORTA="/c/LAR_MIGUEL/porta_memoria.py"
CONF_SRC="$PK/conferir_rito_v384.py"; CONFOUT="$SEL/conferidor"; ENS="$SEL/ensaio_superficies_cadeia"; OUTD="$SEL"; MANIF="$SEL/v384_incorporacao_manifesto.json"
unset TGL_RITE_CHECKPOINT TGL_CACHE_DIR V384_NOS V384_REMAP_DIR V384_WRITE_ROOT V384_CONF_DIR V384_HORARIOS V384_PIDF V384_ESPERA_SEM_VIGIA V384_UMEM V384_ATLAS_DIR V384_TOOLS V384_SAIDAS V384_ARQ_DEST
# <<< CONFIG
export PYTHONIOENCODING=utf-8
set -e
parar() { echo "PARADA: $*"; echo "(nada foi restaurado: a decisao de restaurar e da gerencia)"; exit 1; }
TOPICOS="missao-ultima-flag-um-py.md central-de-patentes-estado.md beta-e-a-regra-matriz-02out.md regra-dos-dois-regimes.md v382-custodia-suspensa.md v384-pilar-quantico-gpu-02out.md"
echo "== 0. guardas $(date +%T)"
python -c "
import hashlib, json, glob, os, sys
um, pk = sys.argv[1], sys.argv[2]
ap = json.load(open(sorted(glob.glob(os.path.join(pk, 'APLICADO_AO_CANONICO_*.json')))[-1], encoding='utf-8'))
es = json.load(open(os.path.join(pk, 'ESPERADOS_v384.json'), encoding='utf-8'))
h = hashlib.sha256(open(um, 'rb').read()).hexdigest()[:16]
print('um.py no disco', h, '== instalado pela gerencia', ap['um_py_novo']['sha16'], '== candidato de ESPERADOS', es['candidato_sha16'])
sys.exit(0 if h == ap['um_py_novo']['sha16'] == es['candidato_sha16'] else 1)" "$NOS/um.py" "$PK" || parar "o um.py do disco nao e o instalado (APLICADO_AO_CANONICO mais recente / ESPERADOS)"
for f in "$ARVORE" "$ATLASPY" "$PORTA" "$CONF_SRC" "$PK/ESPERADOS_v384.json"; do [ -f "$f" ] || parar "ferramenta ausente: $f"; done
echo "== 1. esperando o fim do rito (so leitura) $(date +%T)"
set +e; python "$SEL/espera_rito_v384.py"; e=$?; set -e
[ "$e" = "0" ] || parar "espera terminou com rc=$e (3 = rito nao limpo ou sem a linha final; 4 = tempo esgotado; 5 = o lancador acabou sem RITO_RC)"
echo "== 2. o rito limpo $(date +%T)"
STD="$NOS/rodada_v384_stdout.txt"
tail -3 "$STD" | cut -c1-240
grep -o -E '[0-9]+ escritos, [0-9]+ inalterados' "$STD" | head -1
T=$(grep -o "teoremas limpos: [0-9]*/[0-9]*" "$STD" | head -1)
echo "$T"; A=$(echo "$T" | sed 's/.*: //; s#/.*##'); B=$(echo "$T" | sed 's#.*/##')
RCS=$(grep '^RITO_RC=' "$STD" | tail -1 | sed 's/RITO_RC=//' | tr -d '\r')
rc="${V384_RC:-$RCS}"
[ -n "$rc" ] || parar "rc do rito NAO DITO (sem RITO_RC= no stdout)"
[ -z "$V384_RC" ] || [ "$V384_RC" = "$RCS" ] || parar "V384_RC=$V384_RC difere do RITO_RC=$RCS do stdout"
[ "$rc" = "0" ] && [ -n "$A" ] && [ "$A" = "$B" ] && grep -q "FAIL_CLOSED_SELFTEST_PASSED" "$STD" || parar "RITO NAO LIMPO (rc=$rc; $T)"
if grep -n -E "Traceback|^\[selo\] AVISO" "$STD"; then parar "stdout com Traceback/AVISO (linhas acima)"; fi
[ -f "$NOS/um_absoluto_selo.json" ] || parar "o selo NAO existe"
python -c "
import json, sys
s = json.load(open(sys.argv[1], encoding='utf-8'))
print('selo:', s.get('timestamp'), s.get('um_version'), s.get('fail_closed_selftest'))
sys.exit(0 if s.get('um_version') == 'v384' and s.get('fail_closed_selftest') == 'FAIL_CLOSED_SELFTEST_PASSED' else 1)" "$NOS/um_absoluto_selo.json" || parar "o selo nao e o da v384 ou nao registrou o selftest"
grep -n "\[v384\]" "$STD" | grep -v "em curso" | cut -c1-260
echo "== 3. conferidor (copia byte a byte do pacote + os arquivos que ele le de HERE; so leitura do Nos) $(date +%T)"
rm -rf "$CONFOUT"; mkdir -p "$CONFOUT"
CONF_NAME=$(basename "$CONF_SRC")
cp -p "$CONF_SRC" "$CONFOUT/$CONF_NAME"; cmp "$CONF_SRC" "$CONFOUT/$CONF_NAME" || parar "copia do conferidor difere"
for f in ESPERADOS_v384.json rito_servidor_v384.log rito_v384_sinal.txt; do
  if [ -f "$PK/$f" ]; then cp -p "$PK/$f" "$CONFOUT/$f"; cmp "$PK/$f" "$CONFOUT/$f" || parar "copia difere: $f"; echo "  copiado byte a byte: $f"; else echo "  (o pacote nao tem $f)"; fi
done
[ -f "$CONFOUT/ESPERADOS_v384.json" ] || parar "ESPERADOS_v384.json nao copiado"
set +e; (cd "$CONFOUT" && python "$CONF_NAME") > "$CONFOUT/conferir_rito_v384_stdout.txt" 2>&1; c=$?; set -e
cat "$CONFOUT/conferir_rito_v384_stdout.txt" | cut -c1-240
if [ "$c" = "0" ] && tail -1 "$CONFOUT/conferir_rito_v384_stdout.txt" | grep -q "^TUDO BATE"; then
  echo "  conferidor: TUDO BATE"
else
  echo "---- o que REPROVOU:"; grep -E "^\s+\[NAO\]" "$CONFOUT/conferir_rito_v384_stdout.txt" || true
  if [ -n "$V384_ACEITO_PILAR_NAO_CONCLUIDO" ]; then
    echo "  V384_ACEITO_PILAR_NAO_CONCLUIDO=$V384_ACEITO_PILAR_NAO_CONCLUIDO: a leitura confere se a conferencia e' ESSA e se as falhas sao SO do pilar"
  else
    python -c "
import json, sys, hashlib
sys.path.insert(0, sys.argv[2]); import leitura_v384 as L
p = sys.argv[1]; C = json.load(open(p, encoding='utf-8'))
f = [k for k, v in list((C.get('deve_mudar') or {}).items()) + list((C.get('nao_pode_mudar') or {}).items()) if not v]
so = bool(f) and all(any(k.startswith(x) for x in L.PILAR_ITENS) for k in f)
print('  diagnostico: %d falha(s); SO itens do pilar: %s; conferencia sha16 %s; veredito do pilar: %s' % (len(f), so, hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16], (C.get('pilar') or {}).get('verdict')))" "$CONFOUT/conferencia_rito_v384.json" "$SEL" || true
    parar "CONFERIDOR REPROVOU (rc=$c) -- nada foi escrito nas superficies (se as falhas forem SO do pilar: decisao da gerencia, V384_ACEITO_PILAR_NAO_CONCLUIDO=<sha16>)"
  fi
fi
echo "== 4. a leitura da rodada (os hashes do pilar, do selo, do result.json, do pre-registro) $(date +%T)"
set +e; python "$SEL/leitura_v384.py" > "$OUTD/leitura_v384_out.txt" 2>&1; l=$?; set -e
grep -E '"(teor|rc|conf_dm|conf_np|qp_classe|qp_negativos|pr_ev|pr_conf|n_ver_iguais|esc|qg)"' "$OUTD/leitura_v384_out.txt" | cut -c1-240
tail -1 "$OUTD/leitura_v384_out.txt" | cut -c1-2000
[ "$l" = "0" ] || parar "a LEITURA tem PROBLEMAS (acima; saida inteira em $OUTD/leitura_v384_out.txt)"
echo "== 5. manifesto v384 -> pasta das ferramentas"
python "$SEL/manifesto_v384.py" || parar "manifesto v384 recusou/falhou"
# o manifesto em TOOLS (8o achado da revisao de 04/10): se o destino existe e DIFERE, o anterior vai a backup de BYTES (.bak_<STAMP>_m384) antes;
# temporario -> cmp -> mv; nunca cp direto por cima
MDEST="$TOOLS/v384_incorporacao_manifesto.json"; MST=$(date +%Y%m%d_%H%M%S)
if [ -f "$MDEST" ] && ! cmp -s "$MANIF" "$MDEST"; then cp -p "$MDEST" "$MDEST.bak_${MST}_m384" && cmp "$MDEST" "$MDEST.bak_${MST}_m384" || parar "backup do manifesto anterior em TOOLS falhou"; echo "  manifesto anterior guardado: $MDEST.bak_${MST}_m384"; fi
cp -p "$MANIF" "$MDEST.tmp_m384" && cmp "$MANIF" "$MDEST.tmp_m384" || parar "copia temporaria do manifesto para TOOLS falhou"
mv -f "$MDEST.tmp_m384" "$MDEST" || parar "troca do manifesto em TOOLS falhou"
cmp "$MANIF" "$MDEST" || parar "manifesto em TOOLS difere"
echo "== 6. ENSAIO das superficies em COPIAS (nada real e tocado)"
rm -rf "$ENS"; mkdir -p "$ENS"
cp -p "$NOS/MEMORIA_DA_LINHAGEM.md" "$NOS/DESENHO_DO_FECHAMENTO_QG.md" "$ATLD/TGL_ATLAS.md" "$UMEM/MEMORY.md" "$UMEM/MEMORY_2.md" "$ENS/"
for t in $TOPICOS; do cp -p "$UMEM/$t" "$ENS/"; done
WENS=$(cygpath -w "$ENS")
set +e
V384_REMAP_DIR="$WENS" V384_WRITE_ROOT="$WENS" python "$SEL/compactar_memory_para_v384.py" --gravar > "$OUTD/ensaio_superficies_cadeia_out.txt" 2>&1; ec=$?
[ "$ec" = "0" ] && { V384_REMAP_DIR="$WENS" V384_WRITE_ROOT="$WENS" python "$SEL/superficies_v384.py" >> "$OUTD/ensaio_superficies_cadeia_out.txt" 2>&1; es=$?; } || es=$ec
set -e
tail -16 "$OUTD/ensaio_superficies_cadeia_out.txt" | cut -c1-240
[ "$es" = "0" ] || parar "o ENSAIO das superficies falhou (rc=$es) -- nada real foi tocado"
n=$(wc -c < "$ENS/MEMORY.md"); echo "  MEMORY.md da copia: $n B"; [ "$n" -le 24000 ] || parar "o MEMORY.md da copia passou de 24 000 B ($n)"
echo "== 7. patches arvore/indice"; python "$SEL/patch_arvore_indice_v384.py" || parar "patch arvore/indice recusou/falhou (backups _p384 ao lado)"
echo "== 8. arvore"; (cd "$TOOLS" && python "$ARVORE" v384) || parar "arvore_da_prova.py v384 falhou"
echo "== 9. atlas + indice"; (cd "$TOOLS" && python "$ATLASPY" v384) || parar "atlas_indice.py v384 falhou"
echo "== 10. compactar o indice (regra dos dois arquivos; VERBATIM ao MEMORY_2)"
python "$SEL/compactar_memory_para_v384.py" --gravar || parar "compactar_memory_para_v384.py falhou/recusou (backups _comp384 ao lado)"
echo "== 11. superficies"
python "$SEL/superficies_v384.py" || parar "superficies_v384.py parou (backups .bak_<STAMP>_sup384 ao lado; rerodar e IDEMPOTENTE)"
echo "== 12. espelho da memoria"
set +e; python "$PORTA" > "$OUTD/porta_memoria_v384_out.txt" 2>&1; pm=$?; set -e
tail -1 "$OUTD/porta_memoria_v384_out.txt"
[ "$pm" = "0" ] || parar "porta_memoria.py saiu com rc=$pm"
echo "== 13. regra da linhagem completa: grep -c v384 em cada superficie"
for f in "$NOS/MEMORIA_DA_LINHAGEM.md" "$NOS/DESENHO_DO_FECHAMENTO_QG.md" "$ATLD/TGL_ATLAS.md" "$ATLD/TGL_INDICE_VIVO.md" "$NOS/A_PROVA_DA_QG_TGL_arvore.md" "$UMEM/MEMORY.md"; do
  n=$(grep -c "v384" "$f" || true); echo "  $n  $(basename "$f")"; [ "$n" -gt 0 ] || parar "superficie sem a v384: $f"; done
for t in $TOPICOS; do n=$(grep -c "v384 SELADA" "$UMEM/$t" || true); echo "  $n  $t"; [ "$n" -gt 0 ] || parar "memoria-topico sem a v384 SELADA: $t"; done
n=$(wc -c < "$UMEM/MEMORY.md"); echo "  MEMORY.md: $n B (limite 24000)"; [ "$n" -le 24000 ] || parar "MEMORY.md passou de 24 000 B ($n)"
echo "== FIM $(date +%T)"
echo "PROXIMOS (gerencia): python \"$SEL/registrar_resultado_v384.py\" (o JSON; registrar com rotas.py) -> python \"$SEL/arquivar_v384.py\" -> python \"$SEL/handoff_v384.py\""
