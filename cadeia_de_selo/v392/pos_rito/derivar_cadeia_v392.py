# -*- coding: utf-8 -*-
"""derivar_cadeia_v392.py -- DERIVA a cadeia pos-rito da v392 a partir do molde REAL da v391 (work\\v391_selo) (molde do derivar: derivar_cadeia_v391.py).
O QUE GERA: chain_pos_rito_v392.sh = os TRECHOS HERDADOS do chain_pos_rito_v391.sh (a prelude set -e/parar, o guarda do um.py instalado, o vaivem do conferidor, a chamada da leitura, o espelho
da memoria), extraidos por ancora e com a subida de versao, COMPOSTOS com os blocos novos da R2 e da R3 (passos 3 em copias com errata e patches, 9 com o marcador do selo, 10 a 10c do B(3),
11 a 14). Cada trecho herdado e' conferido por assert (ancora achada exatamente uma vez).
O QUE CONFERE (nao gera): os scripts Python da v392 foram ESCRITOS sobre os da v391 (a R2 reescreve a maior parte de cada um); este deriva confere que cada invariante do molde
sobrevive no v392 (a guarda da palavra recusada, o 'prefixo exato' do backup, temporario->substituir, a recusa quando a leitura tem problema...) e grava DERIVACAO_v392.json (sha16 de cada
molde e de cada derivado, os invariantes conferidos). Roda `ast.parse` em cada .py e `sh -n` no .sh. NAO EXECUTA nenhum script derivado.
Uso: python -I -B -X utf8 derivar_cadeia_v392.py"""
import ast, hashlib, json, os, shutil, subprocess, sys
sys.stdout.reconfigure(encoding="utf-8")
HERE = os.path.dirname(os.path.abspath(__file__))
MOLDE = os.path.join("C:" + os.sep, "IALD", "Central de Patentes", "work", "v391_selo")
sh16 = lambda b: hashlib.sha256(b).hexdigest()[:16]
rd = lambda d, n: open(os.path.join(d, n), encoding="utf-8").read()
bump = lambda s: s.replace("v391", "v392").replace("v390", "v391")


def trecho(s, ini, fim=None, incluir_fim=False):
    """linhas de s desde a unica linha que COMECA por `ini` ate (exclusive) a unica que comeca por `fim`."""
    L = s.split("\n"); i = [k for k, l in enumerate(L) if l.startswith(ini)]; assert len(i) == 1, ("ancora inicial", ini, len(i))
    if fim is None:
        return L[i[0]]
    j = [k for k, l in enumerate(L) if k > i[0] and l.startswith(fim)]; assert j, ("ancora final", fim)
    return "\n".join(L[i[0]:j[0] + (1 if incluir_fim else 0)])


def rep(s, pairs):
    for a, b in pairs:
        assert s.count(a) >= 1, (a[:100], s.count(a)); s = s.replace(a, b)
    return s


mold = rd(MOLDE, "chain_pos_rito_v391.sh")
# ------------------------------------------------------------------ os trechos HERDADOS do molde (com a subida de versao e as trocas ditas)
H_PRELUDE = "\n".join([trecho(mold, "unset TGL_RITE_CHECKPOINT"), trecho(mold, "export PYTHONIOENCODING"), trecho(mold, "set -e"), trecho(mold, "parar() {")])
assert H_PRELUDE.count("\n") == 3
H_GUARD = rep(trecho(mold, 'python -c "', 'for f in "$TOOLS/arvore_da_prova.py"'),
              [('python -c "', '$PY -c "'), ("ESPERADOS_v391.json", "ESPERADOS_v392.json"), ('"$NOS/um.py" "$PK" || parar', '"$(cygpath -w "$NOS/um.py")" "$(cygpath -w "$PK")" || parar')])
H_STD = trecho(mold, 'grep -q \'^RITO_RC=\' "$STD"', 'echo "== 1.')
H_CONF_COPY = rep(trecho(mold, "rm -rf \"$CONFOUT\"", "set +e; (cd \"$CONFOUT\""),
                  [("ESPERADOS_v391.json rito_servidor_v391.log rito_v391_sinal.txt", "ESPERADOS_v392.json rito_servidor_v392.log rito_v392_sinal.txt"),
                   ("conferir_rito_v391.py", "conferir_rito_v392.py")])
H_PORTA = rep(trecho(mold, 'set +e; python "$PORTA"', 'echo "== 9.'), [("v391", "v392"), ('python "$PORTA"', '$PY_B "$PORTA"')])
for nome, h in (("H_PRELUDE", H_PRELUDE), ("H_GUARD", H_GUARD), ("H_STD", H_STD), ("H_CONF_COPY", H_CONF_COPY), ("H_PORTA", H_PORTA)):
    assert "v391" not in h and "v390" not in h, (nome, [l for l in h.split("\n") if "v391" in l or "v390" in l])
# ------------------------------------------------------------------ o script
HEADER = r'''#!/bin/sh
# v392 (13/10): CADEIA POS-RITO -- no molde do chain_pos_rito_v391.sh (trechos herdados, com a subida de versao), com os acrescimos da R2 e da R3 do plano (PLANO_V392 §11 passos 0-11,
# §12-bis e §12-ter). O rito ja terminou (rito_v392.sh em segundo plano; RITO_RC=<rc> no fim do Nos\rodada_v392_stdout.txt).
# ORDEM: 0 guardas -> 1 o CONFERIDOR (copia byte a byte; so leitura do Nos) -> 2 a LEITURA (PROBLEMAS param) -> 3 ENSAIO das superficies, da errata do CLAUDE.md e dos patches em COPIAS
# (o plano e' conferido antes da primeira escrita) -> 4 patches arvore/indice (CR-08, CR-02) -> 5 a arvore -> 6 atlas+indice -> 7 superficies reais (erratas ao lado + appends) e a errata
# do CLAUDE.md -> 8 porta_memoria.py (o ATLAS a mao nao se toca) -> 9 regra da linhagem completa COM O MARCADOR DO SELO (zero e' falha visivel) e a guarda de MEMORY.md (<24.000 B, <=195
# linhas) -> 10 B(3) da Bancada, ENSAIO pos-selo -> 10a parada do servico (AGUARDA_OPERADOR) -> 10b B(3) APLICAR (so com B3_AUTORIZADO=sim e o evento c1) -> 10c religamento (AGUARDA_OPERADOR)
# -> 11 fechar -> 12 registrar_mapa (so MONTA o JSON e o comando) -> 13 inventario da bancada Lean -> 14 Nos vivo.
# Sai na primeira reprovacao e NAO restaura nada sozinha: a decisao de restaurar e' da gerencia. Retomada: CHAIN_DE=<passo> (e CHAIN_ATE=<passo>); os passos 3 a 9 sao idempotentes.
# Ambiente: B3_AUTORIZADO=sim, EVENTO=<seq> e EVENTO_HASH=<hash16> (so o 10b); V392_AVISO_REIVINDICACAO=<texto> (so' com ela o AVISO_GERENCIA.md e' escrito; sem ela e' PULADO e dito).
# Codigos de saida: 0 fim; 1 reprovacao (PARADA); 20 AGUARDA_OPERADOR (parada de proposito, nao e' falha).
'''
VARS = r'''PK="/c/IALD/Central de Patentes/work/cadeia_de_selo/v392"; SEL="$PK/pos_rito"
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
'''
GATE = r'''TOPICOS="missao-ultima-flag-um-py.md central-de-patentes-estado.md estatuto-da-prova-07out.md"
aguarda() { echo "AGUARDA_OPERADOR: $*"; echo "(a cadeia parou de proposito, nao e' falha; retomar com CHAIN_DE=<passo>)"; exit 20; }
ORDEM="0 1 2 3 4 5 6 7 8 9 10 10a 10b 10c 11 12 13 14"
DE="${CHAIN_DE:-0}"; ATE="${CHAIN_ATE:-14}"
pos() { i=0; for x in $ORDEM; do if [ "$x" = "$1" ]; then echo "$i"; return 0; fi; i=$((i+1)); done; echo "-1"; }
quer() { p=$(pos "$1"); d=$(pos "$DE"); a=$(pos "$ATE"); if [ "$d" -lt 0 ] || [ "$a" -lt 0 ]; then echo "CHAIN_DE/CHAIN_ATE desconhecido (validos: $ORDEM)"; exit 1; fi; [ "$p" -ge "$d" ] && [ "$p" -le "$a" ]; }
exige() { f="$1"; shift; for m in "$@"; do n=$(grep -c -F -- "$m" "$f" || true); echo "  $n  $(basename "$f")  [$m]"; [ "$n" -gt 0 ] || parar "superficie sem o marcador da v392 ($m): $f"; done; }
sha256f() { $PY -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" "$1"; }
pino() { $PY -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8'))[sys.argv[2]]['sha256'])" "$(cygpath -w "$PK/PINOS_BN_v392.json")" "$1"; }
pinop() { $PY -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8'))[sys.argv[2]]['path'])" "$(cygpath -w "$PK/PINOS_BN_v392.json")" "$1"; }
b3_prepara() {
  for k in bateria criterios recibo_pre_selo selo_anterior_v391 kernel_manifesto_anterior_v391 esboco_R3_3; do
    p=$(pinop "$k"); a=$(pino "$k"); b=$(sha256f "$p"); [ "$a" = "$b" ] || parar "o pino $k diverge do arquivo (pino $a != arquivo $b)"
  done
  BAT=$(pino bateria); CRI=$(pino criterios); RPS=$(pino recibo_pre_selo)
  W_BAT=$(cygpath -w "$(pinop bateria)"); W_CRI=$(cygpath -w "$(pinop criterios)"); W_RPS=$(cygpath -w "$(pinop recibo_pre_selo)")
  W_SELO=$(cygpath -w "$(pinop selo_anterior_v391)"); W_KMAN=$(cygpath -w "$(pinop kernel_manifesto_anterior_v391)"); W_ESB=$(cygpath -w "$(pinop esboco_R3_3)"); W_NOS=$(cygpath -w "$NOS")
  KR="$PK/kernel/KERNEL_RECIBO_v392.json"; [ -f "$KR" ] || parar "sem o recibo do kernel: $KR"
  W_KR=$(cygpath -w "$KR"); KRSHA=$(sha256f "$W_KR"); echo "  recibo do kernel (sha256 LIDO NA HORA): $KRSHA"
  $PY -c "import json,os,sys;sys.exit(0 if os.path.isdir(json.load(open(sys.argv[1],encoding='utf-8'))['arvore']) else 1)" "$W_KR" || aguarda "a arvore do sandbox do kernel (campo arvore do recibo) nao existe mais: rodar sh $PK/refazer_sandbox_v392.sh (~8 min, ~30 GB; ato da gerencia), reler o sha do recibo (esta funcao o le na hora) e retomar com CHAIN_DE=$1"
}
'''
S0_A = r'''echo "== 0. guardas $(date +%T)"
command -v python > /dev/null || parar "python nao esta no PATH"
S16=$($PY -c "import glob,json,os,sys;ps=sorted(glob.glob(os.path.join(sys.argv[1],'APLICADO_AO_CANONICO_*.json')));print(json.load(open(ps[-1],encoding='utf-8'))['um_py_novo']['sha16'])" "$(cygpath -w "$PK")") || parar "APLICADO_AO_CANONICO_*.json ilegivel em $PK"
'''
S0_B = r'''for f in "$TOOLS/arvore_da_prova.py" "$TOOLS/atlas_indice.py" "$PORTA" "$PK/conferir_rito_v392.py" "$PK/ESPERADOS_v392.json" "$PK/guarda_p18_v392.py" "$PK/PINOS_BN_v392.json" \
         "$PK/vinculo/sincronizar_bancada.py" "$PK/kernel/KERNEL_RECIBO_v392.json" "$HAJA" "$RAIZ_CLAUDE" "$INV/inventario_bancada.py" "$INV/gerar_documento.py" "/c/IALD/NOS_VIVO/construir.py" \
         "$SEL/leitura_v392.py" "$SEL/textos_v392.py" "$SEL/superficies_v392.py" "$SEL/patch_arvore_indice_v392.py" "$SEL/errata_claude_md_v392.py" "$SEL/fechar_v392.py" "$SEL/registrar_mapa_v392.py" "$SEL/b3_recibo_v392.py"; do
  [ -f "$f" ] || parar "ferramenta/superficie ausente: $f"; done
$PY "$PK/guarda_p18_v392.py" "$SEL/textos_v392.py" > /dev/null || parar "a guarda de texto P18 achou violacao em textos_v392.py"
STD="$NOS/rodada_v392_stdout.txt"
'''
STEP1 = r'''if quer 1; then
echo "== 1. conferidor (copia byte a byte; so leitura do Nos) $(date +%T)"
__H_CONF_COPY__
if [ -f "$PK/.servidor_parado_pelo_rito" ]; then parar "o marcador .servidor_parado_pelo_rito ficou no pacote: o servidor do modelo pode estar parado ($(cat "$PK/.servidor_parado_pelo_rito"))"; fi
set +e; (cd "$CONFOUT" && $PY conferir_rito_v392.py) > "$CONFOUT/conferir_rito_v392_stdout.txt" 2>&1; c=$?; set -e
cut -c1-240 "$CONFOUT/conferir_rito_v392_stdout.txt"
[ "$c" = "0" ] && tail -1 "$CONFOUT/conferir_rito_v392_stdout.txt" | grep -q "^TUDO BATE" || parar "CONFERIDOR REPROVOU (rc=$c) -- nada foi escrito nas superficies"
fi
'''
STEP2 = r'''if quer 2; then
echo "== 2. a leitura da rodada $(date +%T)"
set +e; $PY "$SEL/leitura_v392.py" > "$SEL/leitura_v392_out.txt" 2>&1; l=$?; set -e
tail -1 "$SEL/leitura_v392_out.txt" | cut -c1-600
[ "$l" = "0" ] || parar "a LEITURA tem PROBLEMAS (saida inteira em $SEL/leitura_v392_out.txt)"
fi
'''
STEP3 = r'''if quer 3; then
echo "== 3. ENSAIO em COPIAS: superficies (plano conferido antes da primeira escrita), errata do CLAUDE.md, patches da arvore e do indice, a arvore em DRY (nada real e' tocado)"
rm -rf "${ENS:?}" "${ENST:?}"; mkdir -p "$ENS" "$ENST"
cp -p "$NOS/MEMORIA_DA_LINHAGEM.md" "$NOS/DESENHO_DO_FECHAMENTO_QG.md" "$NOS/HANDOFF_v390_CUSTODIA.md" "$ATLD/TGL_ATLAS.md" "$ATLD/TGL_CORE_MEMORY.md" \
      "$UMEM/MEMORY.md" "$UMEM/MEMORY_2.md" "$UMEM/handoff-v390-custodia.md" "$HAJA" "$ENS/"
for t in $TOPICOS; do cp -p "$UMEM/$t" "$ENS/"; done
if [ -n "$V392_AVISO_REIVINDICACAO" ]; then cp -p "$AVISO" "$ENS/"; fi
cp -p "$RAIZ_CLAUDE" "$ENS/CLAUDE_raiz.md"
set +e; $PY "$SEL/superficies_v392.py" --copias "$(cygpath -w "$ENS")" > "$SEL/ensaio_superficies_out.txt" 2>&1; es=$?; set -e
tail -24 "$SEL/ensaio_superficies_out.txt" | cut -c1-260
[ "$es" = "0" ] || parar "o ENSAIO das superficies falhou (rc=$es) -- nada real foi tocado"
n=$(wc -c < "$ENS/MEMORY.md"); l=$(wc -l < "$ENS/MEMORY.md"); echo "  MEMORY.md da copia: $n B, $l linhas"
[ "$n" -lt 24000 ] || parar "o MEMORY.md da copia chegou a 24 000 B ($n)"
[ "$l" -le 195 ] || parar "o MEMORY.md da copia passou de 195 linhas ($l)"
set +e; $PY "$SEL/errata_claude_md_v392.py" --alvo "$(cygpath -w "$ENS/CLAUDE_raiz.md")" > "$SEL/ensaio_errata_claude_out.txt" 2>&1; ec=$?; set -e
tail -3 "$SEL/ensaio_errata_claude_out.txt" | cut -c1-260
[ "$ec" = "0" ] || parar "o ENSAIO da errata do CLAUDE.md falhou (rc=$ec) -- nada real foi tocado"
cp -p "$TOOLS/arvore_da_prova.py" "$TOOLS/atlas_indice.py" "$ENST/"
$PY "$SEL/patch_arvore_indice_v392.py" --tools "$(cygpath -w "$ENST")" || parar "o ENSAIO do patch da arvore/indice recusou ou falhou (so copias foram tocadas)"
(cd "$ENST" && $PY_B arvore_da_prova.py v392 dry) || parar "a arvore_da_prova.py patchada (copia, dry) falhou"
for m in "AS PEDRAS DA v392" "ERRATA AO LADO (CR-08, v392" "ERRATA AO LADO (CR-02, v392"; do
  n=$(grep -c -F -- "$m" "$ENST/arvore_dry.md" || true); echo "  $n  arvore_dry.md  [$m]"; [ "$n" -gt 0 ] || parar "a arvore (dry) nao traz: $m"; done
fi
'''
STEP4_8 = r'''if quer 4; then
echo "== 4. patches arvore/indice"; $PY "$SEL/patch_arvore_indice_v392.py" || parar "patch arvore/indice recusou/falhou (backups _p392 ao lado)"
fi
if quer 5; then
echo "== 5. arvore"; (cd "$TOOLS" && $PY_B arvore_da_prova.py v392) || parar "arvore_da_prova.py v392 falhou"
fi
if quer 6; then
echo "== 6. atlas + indice (a ordem da v390: o indice antes das superficies)"; (cd "$TOOLS" && $PY_B atlas_indice.py v392) || parar "atlas_indice.py v392 falhou"
fi
if quer 7; then
echo "== 7. superficies (real: erratas ao lado + appends; a guarda P18 em todo texto) e a errata do CLAUDE.md"
$PY "$SEL/superficies_v392.py" || parar "superficies_v392.py parou (backups .bak_<STAMP>_sup392 ao lado; rerodar e IDEMPOTENTE)"
$PY "$SEL/errata_claude_md_v392.py" || parar "errata_claude_md_v392.py parou (backup .bak_<STAMP>_errata_v392 ao lado)"
fi
if quer 8; then
echo "== 8. espelho da memoria"
__H_PORTA__
fi
'''
STEP9 = r'''if quer 9; then
echo "== 9. regra da linhagem completa: o MARCADOR DO SELO e o sha16 do um.py v392 ($S16) em cada superficie (zero e' falha visivel)"
exige "$NOS/MEMORIA_DA_LINHAGEM.md" "$S16" "errata_cr08_v392" "errata_3_v392"
exige "$NOS/DESENHO_DO_FECHAMENTO_QG.md" "<!-- adendo_v392_selada -->" "$S16" "errata_cr08_v392"
exige "$ATLD/TGL_ATLAS.md" "<!-- atlas_v392_selada -->" "$S16" "errata_cr08_v392"
exige "$ATLD/TGL_INDICE_VIVO.md" "$S16"
exige "$ATLD/TGL_CORE_MEMORY.md" "<!-- core_v392_selada -->" "$S16"
exige "$NOS/A_PROVA_DA_QG_TGL_arvore.md" "$S16" "AS PEDRAS DA v392" "ERRATA AO LADO (CR-08, v392" "ERRATA AO LADO (CR-02, v392"
exige "$HAJA" "<!-- haja_luz_v392_selada -->" "$S16" "errata_coulomb_v392"
exige "$RAIZ_CLAUDE" "<!-- errata_v392_selada -->" "$S16"
exige "$NOS/HANDOFF_v390_CUSTODIA.md" "errata_cr08_v392"
exige "$UMEM/handoff-v390-custodia.md" "errata_cr08_v392"
exige "$UMEM/MEMORY.md" "$S16"
exige "$UMEM/MEMORY_2.md" "v392"
for t in missao-ultima-flag-um-py.md central-de-patentes-estado.md; do exige "$UMEM/$t" "$S16"; done
exige "$UMEM/estatuto-da-prova-07out.md" "<!-- v392_selada -->" "$S16"
exige "$UMEM/v392-selada-pedras-e-barreiras-13out.md" "$S16"
if [ -n "$V392_AVISO_REIVINDICACAO" ]; then exige "$AVISO" "<!-- aviso_v392_selada -->" "$S16"; else echo "  (AVISO_GERENCIA.md: PULADO -- sem V392_AVISO_REIVINDICACAO; escrever depois, sob reivindicacao)"; fi
n=$(wc -c < "$UMEM/MEMORY.md"); l=$(wc -l < "$UMEM/MEMORY.md"); echo "  MEMORY.md: $n B (limite 24000), $l linhas (limite 195)"
[ "$n" -lt 24000 ] || parar "MEMORY.md chegou a 24 000 B ($n)"
[ "$l" -le 195 ] || parar "MEMORY.md passou de 195 linhas ($l): o carregador do harness o corta acima de 200"
fi
'''
STEP10 = r'''if quer 10; then
echo "== 10. B(3) da Bancada, ENSAIO pos-selo (nada e' gravado na Bancada; o servico pode estar no ar) $(date +%T)"
b3_prepara 10
SAIDA_E="$PK/bancada_B3_ensaio_$(date +%Y%m%d_%H%M%S)"
set +e
$PY "$W_ESB" --bancada 'C:\IALD\Bancada_Um' --producao --nos "$W_NOS" --versao v392 --fase pos_selo --modo ensaio --bateria "$W_BAT" --bateria-sha256 "$BAT" \
    --recibo-pre-selo "$W_RPS" --recibo-pre-selo-sha256 "$RPS" --selo-anterior "$W_SELO" --kernel-manifesto-anterior "$W_KMAN" \
    --kernel-recibo "$W_KR" --kernel-recibo-sha256 "$KRSHA" --criterios "$W_CRI" --criterios-sha256 "$CRI" \
    --saida "$(cygpath -w "$SAIDA_E")" > "$SEL/b3_ensaio_out.txt" 2>&1; b3=$?
set -e
tail -4 "$SEL/b3_ensaio_out.txt" | cut -c1-400
[ "$b3" = "0" ] || parar "o B(3) ENSAIO reprovou (rc=$b3): saida inteira em $SEL/b3_ensaio_out.txt"
$PY "$SEL/b3_recibo_v392.py" "$(cygpath -w "$SEL/b3_ensaio_out.txt")" ensaio || parar "o recibo do B(3) ENSAIO nao confere"
fi
'''
STEP10A = r'''if quer 10a; then
echo "== 10-bis-a. a parada do servico da Bancada Um (porta 18777), com recibo"
RP="$PK/bancada_B3_servico/RECIBO_PARADA_v392.json"
[ -f "$RP" ] || aguarda "sem o recibo da PARADA do um_bancada.py ($RP): quiesce e parada (PID, porta 18777 fechada e hora no recibo), no molde do restart_and_deploy.ps1 / RESTART_RECEIPT_R1.json da B2 -- ato do operador autorizado na B3. Sem esse recibo a cadeia para aqui."
$PY -c "import socket,sys
try:
    socket.create_connection(('127.0.0.1', 18777), timeout=1.5).close()
except OSError:
    sys.exit(0)
sys.exit(1)" || parar "o servico da Bancada esta no AR (a porta 18777 responde) apesar do recibo de parada"
echo "  recibo da parada: $RP (sha256 $(sha256f "$(cygpath -w "$RP")")); porta 18777 fechada"
fi
'''
STEP10B = r'''if quer 10b; then
echo "== 10-bis. B(3) APLICAR (grava o manifesto B3 na Bancada de producao: backup de bytes, rollback se falhar) $(date +%T)"
[ "$B3_AUTORIZADO" = "sim" ] || aguarda "a B3 nao esta autorizada: ato da gerencia sob evento c1 (SINCRONIZACAO_BANCADA) + autorizacao do operador. Definir B3_AUTORIZADO=sim, EVENTO=<seq> e EVENTO_HASH=<hash16 do retorno de iald.py anotar>, com o servico parado (10-bis-a) e o recibo da parada, e retomar com CHAIN_DE=10b"
[ -n "$EVENTO" ] && [ -n "$EVENTO_HASH" ] || aguarda "faltam EVENTO e EVENTO_HASH (o elo do evento c1 nomeando a gravacao)"
[ -f "$PK/bancada_B3_servico/RECIBO_PARADA_v392.json" ] || aguarda "sem o recibo da parada do servico (10-bis-a)"
b3_prepara 10b
SAIDA_B3="$PK/bancada_B3"; k=1; while [ -e "$SAIDA_B3" ]; do k=$((k+1)); SAIDA_B3="$PK/bancada_B3_$k"; done
echo "  saida do B(3): $SAIDA_B3 (pasta nova)"
set +e
$PY "$W_ESB" --bancada 'C:\IALD\Bancada_Um' --producao --nos "$W_NOS" --versao v392 --fase pos_selo --modo aplicar --bateria "$W_BAT" --bateria-sha256 "$BAT" \
    --evento "$EVENTO" --evento-hash "$EVENTO_HASH" \
    --recibo-pre-selo "$W_RPS" --recibo-pre-selo-sha256 "$RPS" --selo-anterior "$W_SELO" --kernel-manifesto-anterior "$W_KMAN" \
    --kernel-recibo "$W_KR" --kernel-recibo-sha256 "$KRSHA" --criterios "$W_CRI" --criterios-sha256 "$CRI" \
    --saida "$(cygpath -w "$SAIDA_B3")" > "$SEL/b3_aplicar_out.txt" 2>&1; b3=$?
set -e
tail -4 "$SEL/b3_aplicar_out.txt" | cut -c1-400
[ "$b3" = "0" ] || parar "o B(3) APLICAR reprovou (rc=$b3): saida inteira em $SEL/b3_aplicar_out.txt; NADA foi restaurado por esta cadeia (o esboco faz o seu rollback)"
$PY "$SEL/b3_recibo_v392.py" "$(cygpath -w "$SEL/b3_aplicar_out.txt")" aplicar || parar "o recibo do B(3) APLICAR nao confere"
fi
'''
STEP10C = r'''if quer 10c; then
echo "== 10-ter. o religamento do servico e a reconexao dos adaptadores MCP (ato do operador)"
RR="$PK/bancada_B3_servico/RECIBO_RELIGAMENTO_v392.json"
[ -f "$RR" ] || aguarda "sem o recibo do RELIGAMENTO do um_bancada.py ($RR): religar o servico com recibo de identidade (a versao servida e v392 e o sha do manifesto e o do recibo do 10-bis) e reconectar os adaptadores MCP das sessoes (ato do operador)"
echo "  recibo do religamento: $RR (sha256 $(sha256f "$(cygpath -w "$RR")")); o fechar o confere contra o recibo do 10-bis"
fi
'''
STEP11_14 = r'''if quer 11; then
echo "== 11. fechar (manifesto, arquivo, os dois diffs, handoff) -- recusa sem os tres recibos do B(3)"
$PY "$SEL/fechar_v392.py" || parar "fechar_v392.py falhou"
fi
if quer 12; then
echo "== 12. registro no mapa de rotas: so MONTA o JSON e o comando (o registro e' ato da gerencia)"
$PY "$SEL/registrar_mapa_v392.py" || parar "registrar_mapa_v392.py falhou"
fi
if quer 13; then
echo "== 13. o inventario da bancada Lean (work\\inventario_bancada) regenerado; copia para memory\\ com backup de bytes"
(cd "$INV" && $PY_B inventario_bancada.py > "$SEL/inventario_bancada_out.txt" 2>&1 && $PY_B gerar_documento.py >> "$SEL/inventario_bancada_out.txt" 2>&1) || parar "o inventario da bancada falhou (ver $SEL/inventario_bancada_out.txt)"
tail -2 "$SEL/inventario_bancada_out.txt" | cut -c1-240
for f in INVENTARIO_BANCADA_CHATGPT.md INVENTARIO_BANCADA_CHATGPT.json; do
  [ -f "$INV/$f" ] || parar "o inventario nao gerou $f"
  if [ -f "$ATLD/$f" ]; then B="$ATLD/$f.bak_$(date +%Y%m%d_%H%M%S)_v392"; cp -p "$ATLD/$f" "$B"; cmp "$ATLD/$f" "$B" || parar "backup de bytes falhou: $B"; fi
  cp -p "$INV/$f" "$ATLD/$f.tmp_v392" && mv "$ATLD/$f.tmp_v392" "$ATLD/$f"; cmp "$INV/$f" "$ATLD/$f" || parar "a copia do inventario difere: $f"
done
fi
if quer 14; then
echo "== 14. o Nos vivo reconstruido (le o mapa de rotas: rodar depois do registro da gerencia no passo 12)"
$PY_B /c/IALD/NOS_VIVO/construir.py > "$SEL/nos_vivo_out.txt" 2>&1 || parar "NOS_VIVO/construir.py falhou (ver $SEL/nos_vivo_out.txt)"
tail -3 "$SEL/nos_vivo_out.txt" | cut -c1-240
fi
echo "== FIM $(date +%T)"
'''
# ---- composicao
S = HEADER + VARS + H_PRELUDE + "\n" + GATE
S += S0_A + H_GUARD + "\n" + S0_B + H_STD + "\n"
S += STEP1.replace("__H_CONF_COPY__", H_CONF_COPY) + STEP2 + STEP3 + STEP4_8.replace("__H_PORTA__", H_PORTA) + STEP9 + STEP10 + STEP10A + STEP10B + STEP10C
S += STEP11_14
assert "__H_" not in S and "\r" not in S
out = os.path.join(HERE, "chain_pos_rito_v392.sh")
open(out, "w", encoding="utf-8", newline="\n").write(S)
print("gerado", out, len(S.splitlines()), "linhas,", len(S.encode("utf-8")), "B")
# ------------------------------------------------------------------ as conferencias
res = {"molde": {}, "derivados": {}, "invariantes": {}, "sintaxe": {}}
sh = shutil.which("sh")
if sh:
    r = subprocess.run([sh, "-n", out], capture_output=True, text=True)
    res["sintaxe"]["chain_pos_rito_v392.sh"] = "sh -n rc=%d %s" % (r.returncode, r.stderr[:300])
    assert r.returncode == 0, ("sh -n reprovou", r.stderr)
else:
    res["sintaxe"]["chain_pos_rito_v392.sh"] = "sh nao achado: nao conferido"
INV = {  # v392 -> (molde, invariantes: trechos que o molde tem (com a subida de versao) e o derivado TEM DE manter)
    "leitura_v392.py": ("leitura_v391.py", ["TRAILER_RE = re.compile(r'^(exit=\\d+|rc=\\d+|RITO_RC=\\S+|inicio |fim )')", "FAIL_CLOSED_SELFTEST_PASSED", "'SEAL_WITHHELD' in out", "re.findall(r'^RITO_RC=(\\S+)'",
                                                          "GUARDA = re.compile('(?<!NOT_)(?<!UN)' + 'CONF' + 'IRMED|(?<!AP)PRO' + 'VED_BY|TGL_PRO' + 'VED')", "P.append('o gate MUDOU')", "'rodada nao COMPLETA'"]),
    "superficies_v392.py": ("superficies_v391.py", ["def nl_de(raw):", "assert open(bak, 'rb').read() == d['raw'], 'backup de bytes falhou: %s' % bak", "os.replace(tmp, p); tmp_atual = None",
                                                  "assert open(p, 'rb').read() == d['novo']", "'ESCRITA FORA DAS COPIAS: %s' % p", "print('SUPERFICIES RECUSADAS -- nada foi escrito; a leitura da rodada tem problema(s):')",
                                                  "assert b'\\r\\n' not in raw, 'MEMORY.md com CRLF: o molde espera LF'", "def livre(base):"]),
    "patch_arvore_indice_v392.py": ("patch_arvore_indice_v391.py", ["def grava(P, s):", "ast.parse(s)", "raise AssertionError('o arquivo novo nao cresceu -- nao substituo')", "def backup(P):",
                                                                "print('PATCH RECUSADO -- a leitura da rodada tem problema(s):')", "assert '\\r' not in s"]),
    "errata_claude_md_v392.py": ("errata_claude_md_v391.py", ["open(bak, \"wb\").write(raw); assert open(bak, \"rb\").read() == raw", "assert len(novo) > len(raw) and novo.replace(nl + LINHA.encode(\"utf-8\") + nl, b\"\", 1) == raw",
                                                           "os.replace(tmp, P)", "JA ESTA (idempotente)"]),
    "fechar_v392.py": ("fechar_v391.py", ["def grava(p, b):", "FECHAR RECUSADO:", "assert os.path.getsize(tmp) == len(b); os.replace(tmp, p); assert open(p, \"rb\").read() == b", "def copia(src, dst):",
                                          "grava(os.path.join(UMEM, \"handoff-v392-custodia.md\")", "grava(os.path.join(NOS, \"HANDOFF_v392_CUSTODIA.md\")"]),
    "registrar_mapa_v392.py": ("registrar_mapa_v391.py", ["rotas.py", "registrar", "--quem", "MAPA_DE_ROTAS"]),
    "textos_v392.py": ("textos_v391.py", ["def _g(d, *ks):", "def linhagem(V):", "def desenho(V):", "def atlas(V):", "def topico_missao(V):", "def linha_handoff(V):", "def arvore_linha(V):", "def verbete(V):", "def remissivo(V):"]),
}
for novo, (molde_n, invs) in INV.items():
    ms = rd(MOLDE, molde_n); ns = rd(HERE, novo)
    res["molde"][molde_n] = sh16(ms.encode("utf-8")); res["derivados"][novo] = sh16(ns.encode("utf-8")); ast.parse(ns)
    ok = []
    for t in invs:
        t_m = t.replace("v392", "v391")
        em_molde = (t in ms) or (t_m in ms) or (bump(t_m) in ms)
        assert em_molde, ("invariante que o MOLDE nao tem (corrigir a lista)", molde_n, t[:100])
        assert t in ns, ("invariante do molde PERDIDO no derivado", novo, t[:100])
        ok.append(t[:80])
    res["invariantes"][novo] = ok
    res["sintaxe"][novo] = "ast.parse ok"
for extra in ("b3_recibo_v392.py", "derivar_cadeia_v392.py"):
    ast.parse(rd(HERE, extra)); res["sintaxe"][extra] = "ast.parse ok"; res["derivados"][extra] = sh16(rd(HERE, extra).encode("utf-8"))
res["derivados"]["chain_pos_rito_v392.sh"] = sh16(S.encode("utf-8")); res["molde"]["chain_pos_rito_v391.sh"] = sh16(mold.encode("utf-8"))
open(os.path.join(HERE, "DERIVACAO_v392.json"), "w", encoding="utf-8").write(json.dumps(res, ensure_ascii=False, indent=1))
print("DERIVADO; invariantes conferidos:", {k: len(v) for k, v in res["invariantes"].items()})
