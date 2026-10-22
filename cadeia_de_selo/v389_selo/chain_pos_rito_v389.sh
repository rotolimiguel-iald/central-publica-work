#!/bin/sh
# v389 (06/10): CADEIA POS-RITO -- no molde do chain_pos_rito_v388.sh, enxuta. O rito ja terminou (rito_v389.sh em segundo plano; RITO_RC=<rc> no fim do
# Nos\rodada_v389_stdout.txt). Ordem: guardas -> o CONFERIDOR (copia byte a byte do pacote para v389_selo\conferidor, com ESPERADOS e os logs do lancador; so leitura
# do Nos) -> a LEITURA (PROBLEMAS param) -> ENSAIO das superficies em COPIAS -> patches arvore/indice -> arvore_da_prova.py v389 -> atlas_indice.py v389 ->
# superficies (real) -> porta_memoria.py -> grep -c v389 em cada superficie -> fechar (manifesto, arquivo, handoff). Se algo reprovar: PARA e imprime o que reprovou.
# NAO restaura nada sozinho: a decisao de restaurar e da gerencia. Depois: o registro no mapa de rotas (gerencia).
SEL="/c/IALD/Central de Patentes/work/v389_selo"; PK="/c/IALD/Central de Patentes/work/v389_pacote"
TOOLS="/c/IALD/Central de Patentes/work/cadeia_de_selo"
NOS="/c/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós"
UMEM="/c/Users/rotol/.claude/projects/c--IALD-Central-de-Patentes/memory"
ATLD="/c/IALD/Central de Patentes/memory"
HAJA="/c/IALD/Artigo/Haja_Luz/CLAUDE.md"
PORTA="/c/LAR_MIGUEL/porta_memoria.py"
CONFOUT="$SEL/conferidor"; ENS="$SEL/ensaio_superficies"
unset TGL_RITE_CHECKPOINT TGL_CACHE_DIR
export PYTHONIOENCODING=utf-8
set -e
parar() { echo "PARADA: $*"; echo "(nada foi restaurado: a decisao de restaurar e da gerencia)"; exit 1; }
TOPICOS="missao-ultima-flag-um-py.md central-de-patentes-estado.md"
echo "== 0. guardas $(date +%T)"
python -c "
import hashlib, json, glob, os, sys
um, pk = sys.argv[1], sys.argv[2]
ap = json.load(open(sorted(glob.glob(os.path.join(pk, 'APLICADO_AO_CANONICO_*.json')))[-1], encoding='utf-8'))
es = json.load(open(os.path.join(pk, 'ESPERADOS_v389.json'), encoding='utf-8'))
h = hashlib.sha256(open(um, 'rb').read()).hexdigest()[:16]
print('um.py no disco', h, '== instalado', ap['um_py_novo']['sha16'], '== candidato', es['candidato_sha16'])
sys.exit(0 if h == ap['um_py_novo']['sha16'] == es['candidato_sha16'] else 1)" "$NOS/um.py" "$PK" || parar "o um.py do disco nao e o instalado"
for f in "$TOOLS/arvore_da_prova.py" "$TOOLS/atlas_indice.py" "$PORTA" "$PK/conferir_rito_v389.py" "$PK/ESPERADOS_v389.json" "$HAJA"; do [ -f "$f" ] || parar "ferramenta/superficie ausente: $f"; done
STD="$NOS/rodada_v389_stdout.txt"
grep -q '^RITO_RC=' "$STD" || parar "o rito nao acabou (sem RITO_RC= no stdout)"
tail -3 "$STD" | cut -c1-240
echo "== 1. conferidor (copia byte a byte; so leitura do Nos) $(date +%T)"
rm -rf "$CONFOUT"; mkdir -p "$CONFOUT"
cp -p "$PK/conferir_rito_v389.py" "$CONFOUT/"; cmp "$PK/conferir_rito_v389.py" "$CONFOUT/conferir_rito_v389.py" || parar "copia do conferidor difere"
for f in ESPERADOS_v389.json rito_servidor_v389.log rito_v389_sinal.txt; do
  if [ -f "$PK/$f" ]; then cp -p "$PK/$f" "$CONFOUT/$f"; cmp "$PK/$f" "$CONFOUT/$f" || parar "copia difere: $f"; echo "  copiado byte a byte: $f"; else echo "  (o pacote nao tem $f)"; fi
done
set +e; (cd "$CONFOUT" && python conferir_rito_v389.py) > "$CONFOUT/conferir_rito_v389_stdout.txt" 2>&1; c=$?; set -e
cut -c1-240 "$CONFOUT/conferir_rito_v389_stdout.txt"
[ "$c" = "0" ] && tail -1 "$CONFOUT/conferir_rito_v389_stdout.txt" | grep -q "^TUDO BATE" || parar "CONFERIDOR REPROVOU (rc=$c) -- nada foi escrito nas superficies"
echo "== 2. a leitura da rodada $(date +%T)"
set +e; python "$SEL/leitura_v389.py" > "$SEL/leitura_v389_out.txt" 2>&1; l=$?; set -e
tail -1 "$SEL/leitura_v389_out.txt" | cut -c1-600
[ "$l" = "0" ] || parar "a LEITURA tem PROBLEMAS (saida inteira em $SEL/leitura_v389_out.txt)"
echo "== 3. ENSAIO das superficies em COPIAS (nada real e tocado)"
rm -rf "$ENS"; mkdir -p "$ENS"
cp -p "$NOS/MEMORIA_DA_LINHAGEM.md" "$NOS/DESENHO_DO_FECHAMENTO_QG.md" "$ATLD/TGL_ATLAS.md" "$UMEM/MEMORY.md" "$UMEM/MEMORY_2.md" "$HAJA" "$ENS/"
for t in $TOPICOS; do cp -p "$UMEM/$t" "$ENS/"; done
set +e; python "$SEL/superficies_v389.py" --copias "$(cygpath -w "$ENS")" > "$SEL/ensaio_superficies_out.txt" 2>&1; es=$?; set -e
tail -16 "$SEL/ensaio_superficies_out.txt" | cut -c1-240
[ "$es" = "0" ] || parar "o ENSAIO das superficies falhou (rc=$es) -- nada real foi tocado"
n=$(wc -c < "$ENS/MEMORY.md"); echo "  MEMORY.md da copia: $n B"; [ "$n" -le 24000 ] || parar "o MEMORY.md da copia passou de 24 000 B ($n)"
echo "== 4. patches arvore/indice"; python "$SEL/patch_arvore_indice_v389.py" || parar "patch arvore/indice recusou/falhou (backups _p387 ao lado)"
echo "== 5. arvore"; (cd "$TOOLS" && python arvore_da_prova.py v389) || parar "arvore_da_prova.py v389 falhou"
echo "== 6. atlas + indice (a ordem da v388: o indice antes das superficies)"; (cd "$TOOLS" && python atlas_indice.py v389) || parar "atlas_indice.py v389 falhou"
echo "== 7. superficies (real)"
python "$SEL/superficies_v389.py" || parar "superficies_v389.py parou (backups .bak_<STAMP>_sup387 ao lado; rerodar e IDEMPOTENTE)"
echo "== 8. espelho da memoria"
set +e; python "$PORTA" > "$SEL/porta_memoria_v389_out.txt" 2>&1; pm=$?; set -e
tail -1 "$SEL/porta_memoria_v389_out.txt"
[ "$pm" = "0" ] || parar "porta_memoria.py saiu com rc=$pm"
echo "== 9. regra da linhagem completa: grep -c v389 em cada superficie"
for f in "$NOS/MEMORIA_DA_LINHAGEM.md" "$NOS/DESENHO_DO_FECHAMENTO_QG.md" "$ATLD/TGL_ATLAS.md" "$ATLD/TGL_INDICE_VIVO.md" "$NOS/A_PROVA_DA_QG_TGL_arvore.md" "$UMEM/MEMORY.md" "$HAJA"; do
  n=$(grep -c "v389" "$f" || true); echo "  $n  $(basename "$f")"; [ "$n" -gt 0 ] || parar "superficie sem a v389: $f"; done
for t in $TOPICOS; do n=$(grep -c "v389" "$UMEM/$t" || true); echo "  $n  $t"; [ "$n" -gt 0 ] || parar "memoria-topico sem a v389: $t"; done
n=$(wc -c < "$UMEM/MEMORY.md"); echo "  MEMORY.md: $n B (limite 24000)"; [ "$n" -le 24000 ] || parar "MEMORY.md passou de 24 000 B ($n)"
echo "== 10. fechar (manifesto, arquivo, handoff)"; python "$SEL/fechar_v389.py" || parar "fechar_v389.py falhou"
echo "== FIM $(date +%T)"
