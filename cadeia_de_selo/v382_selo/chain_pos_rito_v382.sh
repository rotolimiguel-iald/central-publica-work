#!/bin/sh
# v382 (02/10): CADEIA POS-RITO -- no molde do chain_pos_rito_v370.sh. O rito ja foi lancado pela gerencia
# (echo 1 | python um.py > Nos\rodada_v382_stdout.txt 2>&1). Espera o fim SO POR LEITURA -> rc/teoremas/selftest/stdout limpo ->
# conferir_rito_v382.py (copia byte a byte do pacote) -> SO SE TUDO BATE: manifesto -> ENSAIO das superficies em COPIAS -> patches
# arvore/indice -> arvore v382 -> atlas/indice v382 -> superficies -> espelho da memoria -> grep -c v382 em cada superficie.
# Se algo reprovar: PARA e imprime o que reprovou. NAO restaura nada sozinho: a decisao de restaurar e da gerencia.
# rc do rito: passe V382_RC=<rc> (a gerencia o tem na saida da ferramenta dela). Opcional: V382_T0 / V382_T1.
SP="/c/Users/rotol/AppData/Local/Temp/claude/c--IALD-Central-de-Patentes/6da8f00d-d44f-4888-a88d-fc9f73eead3d/scratchpad"
SEL="$SP/v382_selo"; PK="$SP/v382"
TOOLS="/c/IALD/Central de Patentes/work/cadeia_de_selo"
NOS="/c/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós"
UMEM="/c/Users/rotol/.claude/projects/c--IALD-Central-de-Patentes/memory"
export PYTHONIOENCODING=utf-8
unset TGL_RITE_CHECKPOINT TGL_CACHE_DIR V382_NOS V382_REMAP_DIR V382_WRITE_ROOT
set -e
parar() { echo "PARADA: $*"; echo "(nada foi restaurado: a decisao de restaurar e da gerencia)"; exit 1; }
echo "== 0. guardas $(date +%T)"
python -c "
import hashlib,json,glob
ap=json.load(open(sorted(glob.glob(r'C:\Users\rotol\AppData\Local\Temp\claude\c--IALD-Central-de-Patentes\6da8f00d-d44f-4888-a88d-fc9f73eead3d\scratchpad\v382\APLICADO_AO_CANONICO_*.json'))[-1],encoding='utf-8'))
h=hashlib.sha256(open(r'C:\IALD\Artigo\Haja_Luz\A Ponte e o Um\Nós\um.py','rb').read()).hexdigest()[:16]
print('um.py no disco',h,'== instalado pela gerencia',ap['um_py_novo']['sha16']); assert h==ap['um_py_novo']['sha16']" || parar "o um.py do disco nao e o instalado"
echo "== 1. esperando o fim do rito (so leitura) $(date +%T)"
set +e; python "$SEL/espera_rito_v382.py"; e=$?; set -e
[ "$e" = "0" ] || parar "espera terminou com rc=$e (3 = sem a linha final; 4 = tempo esgotado)"
cd "$NOS"
tail -3 rodada_v382_stdout.txt
grep -o -E '[0-9]+ escritos, [0-9]+ inalterados' rodada_v382_stdout.txt | head -1
T=$(grep -o "teoremas limpos: [0-9]*/[0-9]*" rodada_v382_stdout.txt | head -1)
echo "$T"; A=$(echo "$T" | sed 's/.*: //; s#/.*##'); B=$(echo "$T" | sed 's#.*/##')
rc="${V382_RC:-$(grep -o '^RITO_RC=[0-9]*' rodada_v382_stdout.txt | tail -1 | sed 's/RITO_RC=//')}"
[ -n "$rc" ] || parar "rc do rito NAO DITO: rode com V382_RC=<rc da saida da ferramenta>"
[ "$rc" = "0" ] && [ -n "$A" ] && [ "$A" = "$B" ] && grep -q "FAIL_CLOSED_SELFTEST_PASSED" rodada_v382_stdout.txt || parar "RITO NAO LIMPO (rc=$rc; $T)"
if grep -n -E "Traceback|^\[selo\] AVISO" rodada_v382_stdout.txt; then parar "stdout com Traceback/AVISO (linhas acima)"; fi
grep -n "\[v382\]" rodada_v382_stdout.txt | cut -c1-260
echo "== 2. conferidor (copia byte a byte do pacote; so leitura do Nos) $(date +%T)"
mkdir -p "$SEL/conferidor"
for f in conferir_rito_v382.py ESPERADOS_v382.json; do cp -p "$PK/$f" "$SEL/conferidor/$f"; cmp "$PK/$f" "$SEL/conferidor/$f" || parar "copia do conferidor difere: $f"; done
cd "$SEL/conferidor"
set +e; python conferir_rito_v382.py > "$SEL/conferir_rito_v382_stdout.txt" 2>&1; c=$?; set -e
cat "$SEL/conferir_rito_v382_stdout.txt"
[ "$c" = "0" ] && tail -1 "$SEL/conferir_rito_v382_stdout.txt" | grep -q "^TUDO BATE" || {
  echo "---- o que REPROVOU:"; grep -E "^\s+\[NAO\]" "$SEL/conferir_rito_v382_stdout.txt" || true
  parar "CONFERIDOR REPROVOU (rc=$c) -- nada foi escrito nas superficies"; }
cd "$SEL"
echo "== 3. manifesto v382 -> pasta das ferramentas"; python manifesto_v382.py || parar "manifesto v382 recusou/falhou"
cp -p "$SEL/v382_incorporacao_manifesto.json" "$TOOLS/v382_incorporacao_manifesto.json" || parar "copia do manifesto para TOOLS falhou"
cmp "$SEL/v382_incorporacao_manifesto.json" "$TOOLS/v382_incorporacao_manifesto.json" || parar "manifesto em TOOLS difere"
echo "== 4. ENSAIO das superficies em COPIAS (nada real e tocado)"
ENS="$SEL/ensaio_superficies"; rm -rf "$ENS"; mkdir -p "$ENS"
for f in "$NOS/MEMORIA_DA_LINHAGEM.md" "$NOS/DESENHO_DO_FECHAMENTO_QG.md" "/c/IALD/Central de Patentes/memory/TGL_ATLAS.md" \
         "$UMEM/missao-ultima-flag-um-py.md" "$UMEM/central-de-patentes-estado.md" \
         "$UMEM/beta-e-a-regra-matriz-02out.md" "$UMEM/regra-dos-dois-regimes.md" "$UMEM/MEMORY.md" "$UMEM/MEMORY_2.md"; do cp -p "$f" "$ENS/"; done
set +e; V382_REMAP_DIR="$(cygpath -w "$ENS")" V382_WRITE_ROOT="$(cygpath -w "$ENS")" python superficies_v382.py > "$SEL/ensaio_superficies_out.txt" 2>&1; es=$?; set -e
tail -15 "$SEL/ensaio_superficies_out.txt"
[ "$es" = "0" ] || parar "o ENSAIO das superficies falhou (rc=$es) -- nada real foi tocado"
echo "== 5. patches arvore/indice"; python patch_arvore_indice_v382.py || parar "patch arvore/indice recusou/falhou (backups _p382 ao lado)"
echo "== 6. arvore"; cd "$TOOLS"; python arvore_da_prova.py v382 || parar "arvore_da_prova.py v382 falhou"
echo "== 7. atlas + indice"; python atlas_indice.py v382 || parar "atlas_indice.py v382 falhou"
echo "== 8. superficies"; cd "$SEL"
python superficies_v382.py || parar "superficies_v382.py parou (backups .bak_<STAMP>_sup382 ao lado; rerodar e IDEMPOTENTE)"
echo "== 9. espelho da memoria"
set +e; python "/c/LAR_MIGUEL/porta_memoria.py" > "$SEL/porta_memoria_v382_out.txt" 2>&1; pm=$?; set -e
tail -1 "$SEL/porta_memoria_v382_out.txt"
[ "$pm" = "0" ] || parar "porta_memoria.py saiu com rc=$pm"
echo "== 10. regra da linhagem completa: grep -c v382 em cada superficie"
for f in "$NOS/MEMORIA_DA_LINHAGEM.md" "$NOS/DESENHO_DO_FECHAMENTO_QG.md" "/c/IALD/Central de Patentes/memory/TGL_ATLAS.md" "/c/IALD/Central de Patentes/memory/TGL_INDICE_VIVO.md" \
         "$NOS/A_PROVA_DA_QG_TGL_arvore.md" "$UMEM/MEMORY.md"; do
  n=$(grep -c "v382" "$f" || true); echo "  $n  $(basename "$f")"; [ "$n" -gt 0 ] || parar "superficie sem a v382: $f"; done
echo "== FIM $(date +%T)"
