#!/bin/sh
# v386 (05/10): CADEIA POS-RITO -- no molde do chain_pos_rito_v385.sh (adaptada pela gerencia auxiliar: nomes, versoes, chaves do selo/core, as memorias-topico
# da v386 e a superficie NOVA da linhagem, C:\IALD\Artigo\Haja_Luz\CLAUDE.md -- decisao do operador de 05/10, item 16 da delegacao). O rito ja foi lancado
# pela gerencia pelo rito_v386.sh (em segundo plano, Git Bash), que grava RITO_RC=<rc> no fim do Nos\rodada_v386_stdout.txt e o fim em <pacote>\rito_horarios_v386.txt,
# e so depois restaura o servidor do modelo nativo.
# Espera o fim SO POR LEITURA -> rito limpo (rc 0, teoremas A/A, FAIL_CLOSED_SELFTEST_PASSED, sem Traceback/[selo] AVISO, o selo EXISTE e e' v386) ->
# o CONFERIDOR do pacote (conferir_rito_v386.py, copiado BYTE A BYTE para v386_selo\conferidor junto com os arquivos que ele le de HERE: ESPERADOS_v386.json,
# rito_servidor_v386.log e rito_v386_sinal.txt, se existirem -- cmp em cada um; o NOS dele e' fixo no Nos real, nada muda) -> a LEITURA (leitura_v386: o Verbo,
# o ramo B por hash, a errata de R6, o reuse do pilar, o W10, os verbatins por sha256; PROBLEMAS param) -> SO SE TUDO BATE: manifesto -> ENSAIO das superficies
# em COPIAS (compactar + superficies) -> patches arvore/indice -> arvore_da_prova.py v386 -> atlas_indice.py v386 -> compactar (real) -> superficies (real) ->
# porta_memoria.py -> grep -c v386 em cada superficie (inclusive o CLAUDE.md da Haja_Luz). Se algo reprovar: PARA e imprime o que reprovou. NAO restaura nada
# sozinho: a decisao de restaurar e da gerencia. rc do rito: lido do RITO_RC= do stdout; a gerencia pode passar V386_RC=<rc> (tem de bater com o do stdout).
# O PILAR nao e' objeto da v386: esperado REAPROVEITADO da v385 pela chave; se o reuse foi recusado e o pilar calculou de novo, e' dito (nao reprova); se o
# conferidor CONGELADO reprovar SO itens do pilar, a cadeia PARA no passo 3 e imprime o diagnostico; a gerencia, se decidir aceitar, roda de novo com
# V386_ACEITO_PILAR_NAO_CONCLUIDO=<sha16 da conferencia>. Ensaiado de ponta a ponta em copias por ensaio_v386.py (modos V386 e AINDA_V385).
# Depois da cadeia (ato da gerencia, nesta ordem): registrar_resultado_v386.py (o JSON do mapa; a gerencia registra) -> arquivar_v386.py -> handoff_v386.py.
# >>> CONFIG
SP="/c/Users/rotol/AppData/Local/Temp/claude/c--IALD-Central-de-Patentes/6da8f00d-d44f-4888-a88d-fc9f73eead3d/scratchpad"
SEL="$SP/v386_selo"; PK="$SP/v386/pacote"
TOOLS="/c/IALD/Central de Patentes/work/cadeia_de_selo"
NOS="/c/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós"
UMEM="/c/Users/rotol/.claude/projects/c--IALD-Central-de-Patentes/memory"
ATLD="/c/IALD/Central de Patentes/memory"
HAJA="/c/IALD/Artigo/Haja_Luz/CLAUDE.md"
ARVORE="$TOOLS/arvore_da_prova.py"; ATLASPY="$TOOLS/atlas_indice.py"; PORTA="/c/LAR_MIGUEL/porta_memoria.py"
CONF_SRC="$PK/conferir_rito_v386.py"; CONFOUT="$SEL/conferidor"; ENS="$SEL/ensaio_superficies_cadeia"; OUTD="$SEL"; MANIF="$SEL/v386_incorporacao_manifesto.json"
unset TGL_RITE_CHECKPOINT TGL_CACHE_DIR V386_NOS V386_REMAP_DIR V386_WRITE_ROOT V386_CONF_DIR V386_HORARIOS V386_PIDF V386_ESPERA_SEM_VIGIA V386_ESPERA_LANCADOR_FINGE V386_UMEM V386_ATLAS_DIR V386_TOOLS V386_SAIDAS V386_ARQ_DEST V386_HAJA_LUZ V386_SINT_MODO
# <<< CONFIG
export PYTHONIOENCODING=utf-8
set -e
parar() { echo "PARADA: $*"; echo "(nada foi restaurado: a decisao de restaurar e da gerencia)"; exit 1; }
TOPICOS="missao-ultima-flag-um-py.md central-de-patentes-estado.md verbo-selecao-da-acao-05out.md ramo-b-reaberto-05out.md v384-pilar-quantico-gpu-02out.md"
echo "== 0. guardas $(date +%T)"
python -c "
import hashlib, json, glob, os, sys
um, pk = sys.argv[1], sys.argv[2]
ap = json.load(open(sorted(glob.glob(os.path.join(pk, 'APLICADO_AO_CANONICO_*.json')))[-1], encoding='utf-8'))
es = json.load(open(os.path.join(pk, 'ESPERADOS_v386.json'), encoding='utf-8'))
h = hashlib.sha256(open(um, 'rb').read()).hexdigest()[:16]
print('um.py no disco', h, '== instalado pela gerencia', ap['um_py_novo']['sha16'], '== candidato de ESPERADOS', es['candidato_sha16'])
sys.exit(0 if h == ap['um_py_novo']['sha16'] == es['candidato_sha16'] else 1)" "$NOS/um.py" "$PK" || parar "o um.py do disco nao e o instalado (APLICADO_AO_CANONICO mais recente / ESPERADOS)"
for f in "$ARVORE" "$ATLASPY" "$PORTA" "$CONF_SRC" "$PK/ESPERADOS_v386.json" "$HAJA"; do [ -f "$f" ] || parar "ferramenta/superficie ausente: $f"; done
echo "== 1. esperando o fim do rito (so leitura) $(date +%T)"
set +e; python "$SEL/espera_rito_v386.py"; e=$?; set -e
[ "$e" = "0" ] || parar "espera terminou com rc=$e (3 = rito nao limpo ou sem a linha final; 4 = tempo esgotado: o rito ainda nao acabou; 5 = o lancador acabou sem RITO_RC)"
echo "== 2. o rito limpo $(date +%T)"
STD="$NOS/rodada_v386_stdout.txt"
tail -3 "$STD" | cut -c1-240
grep -o -E '[0-9]+ escritos, [0-9]+ inalterados' "$STD" | head -1
T=$(grep -o "teoremas limpos: [0-9]*/[0-9]*" "$STD" | head -1)
echo "$T"; A=$(echo "$T" | sed 's/.*: //; s#/.*##'); B=$(echo "$T" | sed 's#.*/##')
RCS=$(grep '^RITO_RC=' "$STD" | tail -1 | sed 's/RITO_RC=//' | tr -d '\r')
rc="${V386_RC:-$RCS}"
[ -n "$rc" ] || parar "rc do rito NAO DITO (sem RITO_RC= no stdout)"
[ -z "$V386_RC" ] || [ "$V386_RC" = "$RCS" ] || parar "V386_RC=$V386_RC difere do RITO_RC=$RCS do stdout"
[ "$rc" = "0" ] && [ -n "$A" ] && [ "$A" = "$B" ] && grep -q "FAIL_CLOSED_SELFTEST_PASSED" "$STD" || parar "RITO NAO LIMPO (rc=$rc; $T)"
if grep -n -E "Traceback|^\[selo\] AVISO" "$STD"; then parar "stdout com Traceback/AVISO (linhas acima)"; fi
[ -f "$NOS/um_absoluto_selo.json" ] || parar "o selo NAO existe"
python -c "
import json, sys
s = json.load(open(sys.argv[1], encoding='utf-8'))
print('selo:', s.get('timestamp'), s.get('um_version'), s.get('fail_closed_selftest'))
sys.exit(0 if s.get('um_version') == 'v386' and s.get('fail_closed_selftest') == 'FAIL_CLOSED_SELFTEST_PASSED' else 1)" "$NOS/um_absoluto_selo.json" || parar "o selo nao e o da v386 (o rito ainda nao selou) ou nao registrou o selftest"
grep -n -E "\[v38[456]\]" "$STD" | grep -v "em curso" | cut -c1-260   # v386: o reuse do pilar imprime [v386]; o veredito do pilar segue [v384]; a reprodutibilidade [v385]; os quatro registros [v386]
echo "== 3. conferidor (copia byte a byte do pacote + os arquivos que ele le de HERE; so leitura do Nos) $(date +%T)"
rm -rf "$CONFOUT"; mkdir -p "$CONFOUT"
CONF_NAME=$(basename "$CONF_SRC")
cp -p "$CONF_SRC" "$CONFOUT/$CONF_NAME"; cmp "$CONF_SRC" "$CONFOUT/$CONF_NAME" || parar "copia do conferidor difere"
for f in ESPERADOS_v386.json rito_servidor_v386.log rito_v386_sinal.txt; do
  if [ -f "$PK/$f" ]; then cp -p "$PK/$f" "$CONFOUT/$f"; cmp "$PK/$f" "$CONFOUT/$f" || parar "copia difere: $f"; echo "  copiado byte a byte: $f"; else echo "  (o pacote nao tem $f)"; fi
done
[ -f "$CONFOUT/ESPERADOS_v386.json" ] || parar "ESPERADOS_v386.json nao copiado"
set +e; (cd "$CONFOUT" && python "$CONF_NAME") > "$CONFOUT/conferir_rito_v386_stdout.txt" 2>&1; c=$?; set -e
cat "$CONFOUT/conferir_rito_v386_stdout.txt" | cut -c1-240
if [ "$c" = "0" ] && tail -1 "$CONFOUT/conferir_rito_v386_stdout.txt" | grep -q "^TUDO BATE"; then
  echo "  conferidor: TUDO BATE"
else
  echo "---- o que REPROVOU:"; grep -E "^\s+\[NAO\]" "$CONFOUT/conferir_rito_v386_stdout.txt" || true
  if [ -n "$V386_ACEITO_PILAR_NAO_CONCLUIDO" ]; then
    echo "  V386_ACEITO_PILAR_NAO_CONCLUIDO=$V386_ACEITO_PILAR_NAO_CONCLUIDO: a leitura confere se a conferencia e' ESSA e se as falhas sao SO do pilar"
  else
    python -c "
import json, sys, hashlib
sys.path.insert(0, sys.argv[2]); import leitura_v386 as L
p = sys.argv[1]; C = json.load(open(p, encoding='utf-8'))
f = [k for k, v in list((C.get('deve_mudar') or {}).items()) + list((C.get('nao_pode_mudar') or {}).items()) + list((C.get('muda_e_e_dito') or {}).items()) if not v]
so = bool(f) and all(any(k.startswith(x) for x in L.PILAR_ITENS) for k in f)
print('  diagnostico: %d falha(s); SO itens do pilar: %s; conferencia sha16 %s; pilar: %s' % (len(f), so, hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16], (C.get('pilar_reuse_v386') or {}).get('verdict')))" "$CONFOUT/conferencia_rito_v386.json" "$SEL" || true
    parar "CONFERIDOR REPROVOU (rc=$c) -- nada foi escrito nas superficies (se as falhas forem SO do pilar: decisao da gerencia, V386_ACEITO_PILAR_NAO_CONCLUIDO=<sha16>)"
  fi
fi
echo "== 4. a leitura da rodada (o Verbo, o ramo B por hash, a errata de R6, o reuse do pilar, o W10, os verbatins por sha256) $(date +%T)"
set +e; python "$SEL/leitura_v386.py" > "$OUTD/leitura_v386_out.txt" 2>&1; l=$?; set -e
grep -E '"(teor|rc|conf_dm|conf_np|conf_md|qr_classe|rp_classe|vb_ok|vb_decl|rb_nD|rb_F2b|le_n|n_ver_iguais|esc|qg|op_n)"' "$OUTD/leitura_v386_out.txt" | cut -c1-240
tail -1 "$OUTD/leitura_v386_out.txt" | cut -c1-2000
[ "$l" = "0" ] || parar "a LEITURA tem PROBLEMAS (acima; saida inteira em $OUTD/leitura_v386_out.txt)"
echo "== 5. manifesto v386 -> pasta das ferramentas"
python "$SEL/manifesto_v386.py" || parar "manifesto v386 recusou/falhou"
MDEST="$TOOLS/v386_incorporacao_manifesto.json"; MST=$(date +%Y%m%d_%H%M%S)
if [ -f "$MDEST" ] && ! cmp -s "$MANIF" "$MDEST"; then cp -p "$MDEST" "$MDEST.bak_${MST}_m386" && cmp "$MDEST" "$MDEST.bak_${MST}_m386" || parar "backup do manifesto anterior em TOOLS falhou"; echo "  manifesto anterior guardado: $MDEST.bak_${MST}_m386"; fi
cp -p "$MANIF" "$MDEST.tmp_m386" && cmp "$MANIF" "$MDEST.tmp_m386" || parar "copia temporaria do manifesto para TOOLS falhou"
mv -f "$MDEST.tmp_m386" "$MDEST" || parar "troca do manifesto em TOOLS falhou"
cmp "$MANIF" "$MDEST" || parar "manifesto em TOOLS difere"
echo "== 6. ENSAIO das superficies em COPIAS (nada real e tocado)"
rm -rf "$ENS"; mkdir -p "$ENS"
cp -p "$NOS/MEMORIA_DA_LINHAGEM.md" "$NOS/DESENHO_DO_FECHAMENTO_QG.md" "$ATLD/TGL_ATLAS.md" "$UMEM/MEMORY.md" "$UMEM/MEMORY_2.md" "$HAJA" "$ENS/"
for t in $TOPICOS; do cp -p "$UMEM/$t" "$ENS/"; done
WENS=$(cygpath -w "$ENS")
set +e
V386_REMAP_DIR="$WENS" V386_WRITE_ROOT="$WENS" python "$SEL/compactar_memory_para_v386.py" --gravar > "$OUTD/ensaio_superficies_cadeia_out.txt" 2>&1; ec=$?
[ "$ec" = "0" ] && { V386_REMAP_DIR="$WENS" V386_WRITE_ROOT="$WENS" python "$SEL/superficies_v386.py" >> "$OUTD/ensaio_superficies_cadeia_out.txt" 2>&1; es=$?; } || es=$ec
set -e
tail -18 "$OUTD/ensaio_superficies_cadeia_out.txt" | cut -c1-240
[ "$es" = "0" ] || parar "o ENSAIO das superficies falhou (rc=$es) -- nada real foi tocado"
n=$(wc -c < "$ENS/MEMORY.md"); echo "  MEMORY.md da copia: $n B"; [ "$n" -le 24000 ] || parar "o MEMORY.md da copia passou de 24 000 B ($n)"
echo "== 7. patches arvore/indice"; python "$SEL/patch_arvore_indice_v386.py" || parar "patch arvore/indice recusou/falhou (backups _p386 ao lado)"
echo "== 8. arvore"; (cd "$TOOLS" && python "$ARVORE" v386) || parar "arvore_da_prova.py v386 falhou"
echo "== 9. atlas + indice"; (cd "$TOOLS" && python "$ATLASPY" v386) || parar "atlas_indice.py v386 falhou"
echo "== 10. compactar o indice (regra dos dois arquivos; VERBATIM ao MEMORY_2)"
python "$SEL/compactar_memory_para_v386.py" --gravar || parar "compactar_memory_para_v386.py falhou/recusou (backups _comp386 ao lado)"
echo "== 11. superficies"
python "$SEL/superficies_v386.py" || parar "superficies_v386.py parou (backups .bak_<STAMP>_sup386 ao lado; rerodar e IDEMPOTENTE)"
echo "== 12. espelho da memoria"
set +e; python "$PORTA" > "$OUTD/porta_memoria_v386_out.txt" 2>&1; pm=$?; set -e
tail -1 "$OUTD/porta_memoria_v386_out.txt"
[ "$pm" = "0" ] || parar "porta_memoria.py saiu com rc=$pm"
echo "== 13. regra da linhagem completa: grep -c v386 em cada superficie"
for f in "$NOS/MEMORIA_DA_LINHAGEM.md" "$NOS/DESENHO_DO_FECHAMENTO_QG.md" "$ATLD/TGL_ATLAS.md" "$ATLD/TGL_INDICE_VIVO.md" "$NOS/A_PROVA_DA_QG_TGL_arvore.md" "$UMEM/MEMORY.md"; do
  n=$(grep -c "v386" "$f" || true); echo "  $n  $(basename "$f")"; [ "$n" -gt 0 ] || parar "superficie sem a v386: $f"; done
for t in $TOPICOS; do n=$(grep -c "v386 SELADA" "$UMEM/$t" || true); echo "  $n  $t"; [ "$n" -gt 0 ] || parar "memoria-topico sem a v386 SELADA: $t"; done
n=$(grep -c "v386 SELADA" "$HAJA" || true); echo "  $n  Haja_Luz/CLAUDE.md (superficie nova da linhagem)"; [ "$n" -gt 0 ] || parar "o CLAUDE.md da Haja_Luz nao tem a v386 SELADA"
n=$(wc -c < "$UMEM/MEMORY.md"); echo "  MEMORY.md: $n B (limite 24000)"; [ "$n" -le 24000 ] || parar "MEMORY.md passou de 24 000 B ($n)"
echo "== FIM $(date +%T)"
echo "PROXIMOS (gerencia): python \"$SEL/registrar_resultado_v386.py\" (o JSON; registrar com rotas.py) -> python \"$SEL/arquivar_v386.py\" -> python \"$SEL/handoff_v386.py\""
