#!/bin/sh
# v403 (27/10; textos do pos-rito escritos a mao em 28/10): CADEIA POS-RITO -- derivada por script (derivar_encanamento_v403.py, lote F) do chain_pos_rito_v402.sh FINAL (a cadeia de CONTEUDO que rodou em 27/10; mesma ordem de passos 0..14 e mesmos portoes), com as licoes da v402 (o sidecar entra na custodia, a conferencia traz C15 e C16, as guardas estaticas da Bancada)
# e o passo da FILA DA MEMORIA (abaixo). A narrativa e os vereditos esperados vem de textos_v403.py (montado de textos_v403.semente + textos_v403_novo.pysnip por montar_textos_v403.py), de leitura_v403.py e de ESPERADOS_v403.json (lidos, nunca digitados); os arquivos antes marcados com TEXTO_A_REESCREVER_V403 foram reescritos, testados pelo harness_textos_ensaio_v403.py e a marca saiu (o p00 confere). O rito (rito_v403.sh) so' roda por ordem da gerencia e do operador (RITO_RC=<rc> no fim do Nos\rodada_v403_stdout.txt).
# A v403 e' uma versao de CONTEUDO (os nomes do operador, 27/10/2026, e a F8.1): TRES modulos novos de kernel (TGLExt/Caminho, TGLExt/Vida, TGLExt/VerdadeAdendo; 5 bandeiras novas; escada 9679 -> 9684; h8 lido de ESPERADOS_v403.json),
# QUATRO registros COM FUNCAO (caminho_v403, vida_v403, verdade_adendo_v403 e bandeiras_do_gate_v403; lidos no main logo DEPOIS da esperanca_condicional_v402) e DOIS registros por spec (cunhagens_v403: as 2 falas do operador de 27/10 verbatim por sha256, as erratas E5 e E6 em nome da gerencia c1, as decisoes D17 a D22 e a leitura [ONTO] da tripla espectral;
# e kh_n1_cobertura_v403). A F8.1: as tres bandeiras literais do gate (linearized_spin2_finite_face, protocol_pre_registered, null_tests_passed_blind) passam a CALCULADAS; a letra do veredito do gate NAO muda. Os registros da v402, da v401 e da v399 sao RECRIADOS pelo rito (selos iguais ao ensaio a seco) e o SIDECAR um_absoluto_selo_acom.json e' REESCRITO
# (depois da ultima escrita do selo). O QUADRO «O Teste da Unica Palavra» (v397, a regra do 4,44) PERMANECE no topo do artigo e do .md, INTOCADO: o conferidor e a leitura o conferem de novo; a regra do 4,44 (nunca sem o p calibrado e sem a linha dos 5 sigma no mesmo item) segue valendo em TODO texto que o cite. Os paragrafos do testemunho de dois (v399), da falsidade (v401) e da v402 SEGUEM COMO ESTAO.
# Estatutos: Caminho, Vida e o adendo da Verdade sao [DERIVED] por citacao e composicao de termos de kernel (o teorema novo the_name_reads_the_inscription_as_weights e' [REAL]); a F8.1 e' [REAL] no codigo e no rito; a independencia das 4 experimentais do gate NAO e' resolvida [DECLARADO, GV-03]; a leitura pela tripla espectral e' [ONTO]; o gate nao se move.
# ORDEM: 0 guardas (inclui o sidecar e, NOVO, a fila da memoria) -> 1 o CONFERIDOR (roda NO LUGAR, SEM -I: importa o um.py instalado e precisa do numpy do usuario; so leitura do Nos; as copias em pos_rito\conferidor sao REGISTRO) -> 2 a LEITURA (PROBLEMAS param; le o sidecar e a linha final do rito)
# -> 3 ENSAIO das superficies em COPIAS (o plano e' conferido antes da primeira escrita; a arvore em dry; o sha16 da v403 na arvore (dry) e os marcadores do passo 9 nas COPIAS, conferidos ANTES de qualquer escrita real; se o MEMORY.md passaria de 195 linhas, a superficie RECUSA
# com rc 3 e a cadeia PARA aqui, sem tocar nada real: a superficie NAO compacta o indice) -> 4 patch arvore/indice (OPCIONAL: so' se existir patch_arvore_indice_v403.py) -> 5 a arvore -> 6 atlas+indice -> 7 PAUSA DO VIGIA (NOVO) e superficies reais (appends datados; a errata ao lado do adendo vai DENTRO dos blocos datados;
# SEM errata nova no CLAUDE.md da raiz) -> 8 porta_memoria.py (o ATLAS a mao nao se toca) -> 9 regra da linhagem completa COM O MARCADOR DO SELO (zero e' falha visivel), a guarda de MEMORY.md (<24.000 B, <=195 linhas) e, NOVO, PINAR o indice, soltar a pausa e verificar a fila -> 10 B(n) da Bancada,
# ENSAIO pos-selo -> 10a parada do servico (AGUARDA_OPERADOR) -> 10b B(n) APLICAR (so com B3_AUTORIZADO=sim e o evento c1) -> 10c religamento (AGUARDA_OPERADOR) -> 11 fechar (o handoff TRAZ os DOIS paragrafos do README e do site: o do quadro do 4,44, intocado, e o NOVO da v403 (Caminho, Verdade e Vida), mais a NOTA ao lado do paragrafo da v402 (os nomes que ele trazia como provisorios sao agora os do operador); diz que os do testemunho, da falsidade e da v402 seguem como estao;
# copia o sidecar e o selo para v403_selo e LISTA o sidecar; registra o estado da fila no manifesto) -> 12 registrar_mapa (so MONTA o JSON e o comando) -> 13 inventario da bancada Lean -> 14 Nos vivo.
# Sai na primeira reprovacao e NAO restaura nada sozinha: a decisao de restaurar e' da gerencia. Retomada: CHAIN_DE=<passo> (e CHAIN_ATE=<passo>); os passos 3 a 9 sao idempotentes.
# A FILA DA MEMORIA (ordem do operador de 26/10/2026: SO' a gerencia c1 escreve o MEMORY.md; o vigia, tarefa agendada, compara o indice ao pino fila\PINO_MEMORY.json e, em modo enforcar, restaura o indice se ele divergir): o pos-rito escreve o indice no passo 7, e por isso (ferramenta: pos_rito\fila_memoria_v403.py, que fala com o memoria.py de <memoria>\fila):
#   (i) NO PASSO 0 confere que o sha16 do memoria.py == PINO_MEMORIA_PY_v403.json['sha16'] (lido do arquivo na hora) e que NAO existe fila\PAUSA_VIGIA.json (senao PARA, fail-closed; em RETOMADA a partir do passo 7 uma pausa que seja a NOSSA, «claude-c1 pos-rito v403», deixada por uma execucao anterior que parou, e' aceita);
#   (ii) NO PASSO 7, ANTES da superficie que escreve o MEMORY.md, CRIA fila\PAUSA_VIGIA.json = {"quem":"claude-c1 pos-rito v403","ate":<ISO local com fuso, agora + 1 h>,"motivo":"pos-rito v403 escreve o indice"} (escrita atomica: temporario + os.replace; o memoria.py NAO cria nem remove esse arquivo);
#   (iii) NO PASSO 9, DEPOIS das superficies e da validacao do MEMORY.md, renova a pausa (a retomada pode ter passado de 1 h) e roda MEMORIA_GERENCIA=claude-c1 memoria.py pinar --motivo "pos-rito v403" (rc 0 exigido); (iv) SO' ENTAO remove a pausa; (v) por ultimo roda memoria.py verificar (rc 0 e ok:true).
#   Em qualquer falha ANTES do pino a pausa NAO e' removida: ela vale no maximo 4 h (o teto e' do memoria.py) e evita que o vigia restaure o indice no meio do trabalho. O diretorio de memoria e' parametrizado por V403_MEMORIA_DIR (padrao: o REAL; no ensaio, uma COPIA; o ensaio completo esta em harness_fechar_sandbox_v403.py).
# Ambiente: B3_AUTORIZADO=sim, EVENTO=<seq> e EVENTO_HASH=<hash16> (so o 10b); V403_AVISO_REIVINDICACAO=<texto> (so' com ela o AVISO_GERENCIA.md e' escrito; sem ela e' PULADO e dito); V403_MEMORIA_DIR=<pasta> (so' no ensaio em copia).
# PASSO 10 SEM SALTO: a Bancada de producao JA pina a v402 (B11, B11-v402-20261027-R1) e o Nos e' a v402 ate' a instalacao; portanto o B(n) da v403 e' um passo SIMPLES v402 -> v403 (esboco R3.5, sincronizar_bancada.py): NAO ha a opcao de cadeia de selos
# do esboco, nem o pino correspondente, e o b3_recibo_v403.py NAO tem o 3o argumento. Os pinos vem de PINOS_BN_v403.json (lidos na hora; hash nunca de memoria): criterios, esboco_R3_5, gerador_bateria, driver_t12_t14, bateria_base_R2,
# kernel_recibo (o KERNEL_RECIBO_v403.json, contrato R3_2: o diff v402 -> v403 e' so' as tres pedras novas), candidato, esperados, pins_do_candidato, recibo_pre_selo (gerado e pinado antes da instalacao, em ensaio contra a producao; veredito JA_SINCRONIZADA__ENSAIO__NADA_GRAVADO_NA_BANCADA),
# selo_anterior_v402 e kernel_manifesto_anterior_v402 (as copias de bytes do selo e do manifesto do kernel da v402, em base_v402). A BATERIA da v403 e' GERADA por script no 10 (depois do selo; bateria por versao) e pinada ao lado
# (bateria_pos_selo/PINOS_BATERIA_v403.json).
# Vereditos esperados (lidos do codigo do esboco, nao rodados): ensaio REPINADA_B<n>__ENSAIO__NADA_GRAVADO_NA_BANCADA e aplicar REPINADA_B<n>__APLICADA__SERVICO_DEVE_SER_REINICIADO_COM_RECIBO, sem __SALTO_, com n = a geracao do manifesto que a
# Bancada pina + 1 (B11 -> n = 12; o b3_recibo_v403.py o confere lendo o numero do recibo). A parada do servico (10a) e o religamento (10c) sao ato do operador (V403_AUTORIZACAO_OPERADOR nos scripts bancada_B3_servico\recibo_parada_v403.py e recibo_religamento_v403.py); o chain so' confere os recibos.
# textos_v403.py, fechar_v403.py e registrar_mapa_v403.py RECUSAM rodar se tiverem trecho marcado para reescrever: os passos 0 a 2 nao os usam. Os passos 0 a 9, 10a, 10c e 11 a 14 estao como na v402, com os rotulos da v403 (desvios ditos: a fila da memoria nos passos 0, 7 e 9; o passo 3 e o 9 exigem os marcadores da v403 (os seis registros novos);
# o passo 11 registra o estado da fila no manifesto e diz que os paragrafos do testemunho, da falsidade e da v402 seguem como estao).
# Codigos de saida: 0 fim; 1 reprovacao (PARADA); 20 AGUARDA_OPERADOR (parada de proposito, nao e' falha).
PK="/c/IALD/Central de Patentes/work/cadeia_de_selo/v403"; SEL="$PK/pos_rito"
TOOLS="/c/IALD/Central de Patentes/work/cadeia_de_selo"
NOS="/c/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós"
UMEM_PADRAO="/c/Users/rotol/.claude/projects/c--IALD-Central-de-Patentes/memory"
# a pasta de memoria e' PARAMETRIZADA por V403_MEMORIA_DIR (padrao: a REAL; no ensaio, uma COPIA): normalizada aqui (UMEM em estilo unix para o shell; V403_MEMORIA_DIR em estilo Windows, exportada para o fila_memoria_v403.py, o superficies_v403.py e o fechar_v403.py)
UMEM=$(cygpath -u "${V403_MEMORIA_DIR:-$UMEM_PADRAO}")
V403_MEMORIA_DIR=$(cygpath -w "$UMEM"); export V403_MEMORIA_DIR
FILA="$SEL/fila_memoria_v403.py"
# os registros NOVOS da v403 que as superficies (linhagem, Atlas e o topico novo) tem de nomear; os passos 3 e 9 os exigem (zero e' falha visivel). Uma fonte so': se a gerencia mudar os nomes, muda aqui.
REGS="caminho_v403 vida_v403 verdade_adendo_v403 bandeiras_do_gate_v403 cunhagens_v403 kh_n1_cobertura_v403"
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
# o NOME do topico novo e' lido de textos_v403.TOPICO_NOVO (uma fonte so'); so' roda onde e' usado (passos 3 e 9): o textos_v403.py recusa importar com trecho marcado para reescrever
topico_novo() { $PY -c "import sys;sys.path.insert(0,sys.argv[1]);import textos_v403 as T;print(T.TOPICO_NOVO)" "$(cygpath -w "$SEL")"; }
aguarda() { echo "AGUARDA_OPERADOR: $*"; echo "(a cadeia parou de proposito, nao e' falha; retomar com CHAIN_DE=<passo>)"; exit 20; }
ORDEM="0 1 2 3 4 5 6 7 8 9 10 10a 10b 10c 11 12 13 14"
DE="${CHAIN_DE:-0}"; ATE="${CHAIN_ATE:-14}"
pos() { i=0; for x in $ORDEM; do if [ "$x" = "$1" ]; then echo "$i"; return 0; fi; i=$((i+1)); done; echo "-1"; }
quer() { p=$(pos "$1"); d=$(pos "$DE"); a=$(pos "$ATE"); if [ "$d" -lt 0 ] || [ "$a" -lt 0 ]; then echo "CHAIN_DE/CHAIN_ATE desconhecido (validos: $ORDEM)"; exit 1; fi; [ "$p" -ge "$d" ] && [ "$p" -le "$a" ]; }
exige() { f="$1"; shift; for m in "$@"; do n=$(grep -c -F -- "$m" "$f" || true); echo "  $n  $(basename "$f")  [$m]"; [ "$n" -gt 0 ] || parar "superficie sem o marcador da v403 ($m): $f"; done; }
sha256f() { $PY -c "import hashlib,sys;print(hashlib.sha256(open(sys.argv[1],'rb').read()).hexdigest())" "$1"; }
pino() { $PY -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8'))[sys.argv[2]]['sha256'])" "$(cygpath -w "$PK/PINOS_BN_v403.json")" "$1"; }
pinop() { $PY -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8'))[sys.argv[2]]['path'])" "$(cygpath -w "$PK/PINOS_BN_v403.json")" "$1"; }
b3_prepara() {
  # v403 (26/10/2026): o B(n) da v403 e' um PASSO SIMPLES v402 -> v403 (a Bancada de producao JA pina a v402 e o Nos passou a v403): SEM salto e SEM cadeia de selos, com o esboco R3.5. Os pinos vem de PINOS_BN_v403.json (lidos na hora;
  # hash nunca de memoria): o esboco R3.5, o recibo pre_selo (gerado e pinado antes da instalacao, sobre a Bancada que pina a v402), o recibo do kernel (KERNEL_RECIBO_v403.json, contrato R3_2: as tres pedras novas (Caminho, Vida, VerdadeAdendo) tem declaracoes nomeadas, logo nao ha
  # modulo de auditoria sem declaracao), o selo e o manifesto do kernel da v402 (custodia, em base_v402), o driver, o gerador e a base R2 da bateria. A bateria da v403 e' GERADA aqui, por script, depois do selo (bateria por versao).
  for k in criterios esboco_R3_5 gerador_bateria driver_t12_t14 bateria_base_R2 kernel_recibo candidato esperados pins_do_candidato recibo_pre_selo selo_anterior_v402 kernel_manifesto_anterior_v402; do
    tem_pino "$k" || aguarda "o PINO $k nao esta em PINOS_BN_v403.json: o PINOS_BN da v403 nao foi gerado (ato da gerencia: diff_e_pinos_v403.py) e retomar com CHAIN_DE=$1"
    p=$(pinop "$k"); a=$(pino "$k"); b=$(sha256f "$p"); [ "$a" = "$b" ] || parar "o pino $k diverge do arquivo (pino $a != arquivo $b)"
  done
  if tem_pino cadeia_de_selos; then parar "PINOS_BN_v403.json traz o pino cadeia_de_selos: a v403 e' um passo simples (a Bancada pina a v402), sem salto e sem cadeia de selos"; fi
  [ "$(pino candidato)" = "$(sha256f "$(cygpath -w "$NOS/um.py")")" ] || parar "o um.py do Nos nao e o candidato pinado em PINOS_BN (candidato $(pino candidato))"
  CRI=$(pino criterios); RPS=$(pino recibo_pre_selo)
  W_NOS=$(cygpath -w "$NOS"); W_ESB=$(cygpath -w "$(pinop esboco_R3_5)"); W_CRI=$(cygpath -w "$(pinop criterios)"); W_RPS=$(cygpath -w "$(pinop recibo_pre_selo)")
  W_SELO=$(cygpath -w "$(pinop selo_anterior_v402)"); W_KMAN=$(cygpath -w "$(pinop kernel_manifesto_anterior_v402)")
  # o recibo do kernel do pos_selo e' o pino kernel_recibo (o KERNEL_RECIBO_v403.json, contrato R3_2: sem modulos de auditoria)
  W_KR=$(cygpath -w "$(pinop kernel_recibo)"); KRSHA=$(sha256f "$W_KR"); [ "$KRSHA" = "$(pino kernel_recibo)" ] || parar "o recibo do kernel diverge do pino"; echo "  recibo do kernel (R3_2, sha256 LIDO NA HORA, igual ao pino): $KRSHA"
  $PY -c "import json,os,sys;sys.exit(0 if os.path.isdir(json.load(open(sys.argv[1],encoding='utf-8'))['arvore']) else 1)" "$W_KR" || aguarda "a arvore so-fontes do recibo do kernel (campo arvore) nao existe mais: refazer a arvore (refazer_arvore_v403_pos_selo.py, sem build; ato da gerencia) e retomar com CHAIN_DE=$1"
  # a bateria da v403: GERADA UMA vez, depois do selo, a partir dos pinos da cadeia (PINOS_BN: candidato == o um.py do Nos); o que o ensaio (10) usa e' o que o aplicar (10b) usa (pino ao lado, gravado na geracao)
  BATD="$PK/bateria_pos_selo"
  if [ ! -e "$BATD/BATERIA_VINCULO_v403.json" ]; then
    mkdir -p "$BATD"
    $PY "$(cygpath -w "$(pinop gerador_bateria)")" --base "$(cygpath -w "$(pinop bateria_base_R2)")" --base-sha256 "$(pino bateria_base_R2)" --versao v403 --nos "$W_NOS" \
        --driver "$(cygpath -w "$(pinop driver_t12_t14)")" --pinos-bn "$(cygpath -w "$PK/PINOS_BN_v403.json")" \
        --pino-saida "$(cygpath -w "$BATD/PINO_UM_PY_v403.json")" --saida "$(cygpath -w "$BATD/BATERIA_VINCULO_v403.json")" > "$SEL/gerar_bateria_v403_out.txt" 2>&1 \
      || { cut -c1-300 "$SEL/gerar_bateria_v403_out.txt"; parar "gerar_bateria_r3_4.py recusou: o Nos nao e o candidato pinado em PINOS_BN, ou o selo nao pina o um.py (saida inteira em $SEL/gerar_bateria_v403_out.txt)"; }
    $PY -c "import hashlib,json,sys;h=lambda p:hashlib.sha256(open(p,'rb').read()).hexdigest();b,p,o=sys.argv[1:4];open(o,'x',encoding='utf-8').write(json.dumps({'bateria':{'path':b,'sha256':h(b)},'pino_um_py':{'path':p,'sha256':h(p)},'nota':'pino ao lado da bateria da v403, gravado quando o chain a gerou (R3.5)'},indent=1))" \
        "$(cygpath -w "$BATD/BATERIA_VINCULO_v403.json")" "$(cygpath -w "$BATD/PINO_UM_PY_v403.json")" "$(cygpath -w "$BATD/PINOS_BATERIA_v403.json")" || parar "nao gravei o pino ao lado da bateria da v403"
    echo "  bateria da v403 GERADA por script em $BATD (pino ao lado: PINOS_BATERIA_v403.json)"
  fi
  [ -f "$BATD/PINOS_BATERIA_v403.json" ] || parar "a bateria da v403 existe sem o pino ao lado ($BATD/PINOS_BATERIA_v403.json): nao se sabe quem a gerou"
  W_BAT=$(cygpath -w "$BATD/BATERIA_VINCULO_v403.json"); BAT=$(sha256f "$W_BAT")
  [ "$BAT" = "$($PY -c "import json,sys;print(json.load(open(sys.argv[1],encoding='utf-8'))['bateria']['sha256'])" "$(cygpath -w "$BATD/PINOS_BATERIA_v403.json")")" ] || parar "a bateria da v403 em disco diverge do pino gravado quando foi gerada"
  echo "  bateria da v403 (sha256 LIDO NA HORA, igual ao pino ao lado): $BAT"
}
tem_pino() { $PY -c "import json,sys;sys.exit(0 if sys.argv[2] in json.load(open(sys.argv[1],encoding='utf-8')) else 1)" "$(cygpath -w "$PK/PINOS_BN_v403.json")" "$1"; }
if [ "$UMEM" != "$UMEM_PADRAO" ]; then
  # ENSAIO EM COPIA da memoria (V403_MEMORIA_DIR != a REAL): so' os passos que leem ou escrevem SO' a pasta de memoria (3, 7 e 9) e os de leitura (0, 1, 2) sao permitidos; os demais (arvore, atlas, espelho, Bancada, fechar, mapa, inventario, Nos vivo) tocam o real
  echo "AVISO: V403_MEMORIA_DIR aponta para outra pasta ($UMEM): ENSAIO EM COPIA da memoria; so' os passos 0, 1, 2, 3, 7 e 9 sao permitidos (a superficie escreve tudo, por nome de arquivo, nessa pasta)"
  for s_ in 4 5 6 8 10 10a 10b 10c 11 12 13 14; do if quer "$s_"; then parar "ensaio em copia (V403_MEMORIA_DIR=$V403_MEMORIA_DIR): o passo $s_ tocaria o real; use CHAIN_DE/CHAIN_ATE so' com os passos 0 a 3, 7 e 9"; fi; done
fi
echo "== 0. guardas $(date +%T)"
command -v python > /dev/null || parar "python nao esta no PATH"
S16=$($PY -c "import glob,json,os,sys;ps=sorted(glob.glob(os.path.join(sys.argv[1],'APLICADO_AO_CANONICO_*.json')));print(json.load(open(ps[-1],encoding='utf-8'))['um_py_novo']['sha16'])" "$(cygpath -w "$PK")") || parar "APLICADO_AO_CANONICO_*.json ilegivel em $PK"
$PY -c "
import hashlib, json, glob, os, sys
um, pk = sys.argv[1], sys.argv[2]
ap = json.load(open(sorted(glob.glob(os.path.join(pk, 'APLICADO_AO_CANONICO_*.json')))[-1], encoding='utf-8'))
es = json.load(open(os.path.join(pk, 'ESPERADOS_v403.json'), encoding='utf-8'))
h = hashlib.sha256(open(um, 'rb').read()).hexdigest()[:16]
print('um.py no disco', h, '== instalado', ap['um_py_novo']['sha16'], '== candidato', es['candidato_sha16'])
sys.exit(0 if h == ap['um_py_novo']['sha16'] == es['candidato_sha16'] else 1)" "$(cygpath -w "$NOS/um.py")" "$(cygpath -w "$PK")" || parar "o um.py do disco nao e o instalado"
for f in "$TOOLS/arvore_da_prova.py" "$TOOLS/atlas_indice.py" "$PORTA" "$PK/conferir_rito_v403.py" "$PK/delta_v403.py" "$PK/quadro_v397.py" "$PK/runtime_quadro_v397.py" "$PK/acom_conferencias_v403.py" "$PK/runtime_v403.py" "$NOS/um_absoluto_selo_acom.json" "$PK/ESPERADOS_v403.json" "$PK/guarda_p18_v403.py" "$PK/PINOS_BN_v403.json" \
         "$PK/refazer_arvore_v403_pos_selo.py" "$PK/kernel/KERNEL_RECIBO_v403.json" "$HAJA" "$INV/inventario_bancada.py" "$INV/gerar_documento.py" "/c/IALD/NOS_VIVO/construir.py" \
         "$SEL/leitura_v403.py" "$SEL/textos_v403.py" "$SEL/superficies_v403.py" "$SEL/fechar_v403.py" "$SEL/registrar_mapa_v403.py" "$SEL/b3_recibo_v403.py" "$FILA" "$PK/PINO_MEMORIA_PY_v403.json"; do
  [ -f "$f" ] || parar "ferramenta/superficie ausente: $f"; done
$PY "$PK/guarda_p18_v403.py" "$SEL/textos_v403.py" "$SEL/fechar_v403.py" "$SEL/registrar_mapa_v403.py" > /dev/null || parar "a guarda de texto P18 achou violacao em textos_v403.py, fechar_v403.py ou registrar_mapa_v403.py"
STD="$NOS/rodada_v403_stdout.txt"
grep -q '^RITO_RC=' "$STD" || parar "o rito nao acabou (sem RITO_RC= no stdout)"
tail -3 "$STD" | cut -c1-240
# FILA DA MEMORIA, guarda (i): o memoria.py de <memoria>\fila tem de ser o PINADO (sha16 de PINO_MEMORIA_PY_v403.json, lido na hora) e NAO pode haver fila\PAUSA_VIGIA.json (fail-closed). So' vale se o intervalo de passos inclui o 7 ou o 9 (os que escrevem e pinam o indice).
# Em RETOMADA (CHAIN_DE a partir do passo 7), uma pausa que seja a NOSSA, deixada por uma execucao anterior que parou depois de a criar, e' aceita e sera renovada; pausa de outro dono nunca.
if quer 7 || quer 9; then
  RETOMADA=""; if [ "$(pos "$DE")" -ge "$(pos 7)" ]; then RETOMADA="--retomada"; fi
  echo "== 0-fila. guarda da fila da memoria (memoria.py pinado, sem pausa alheia) $(date +%T)"
  FRC=0; FOUT=$($PY "$FILA" guardas $RETOMADA) || FRC=$?
  echo "$FOUT" | cut -c1-600
  [ "$FRC" = "0" ] || parar "a guarda da FILA DA MEMORIA reprovou (rc=$FRC: memoria.py diferente do pino, ou fila\\PAUSA_VIGIA.json ja existe): ver a linha JSON acima (nada foi escrito; a pausa, se existe, NAO foi tocada)"
fi
if quer 1; then
echo "== 1. conferidor (so leitura do Nos; roda NO LUGAR e SEM -I) $(date +%T)"
rm -rf "$CONFOUT"; mkdir -p "$CONFOUT"
# v403 (desvio do molde, dito): o conferidor IMPORTA o um.py instalado (precisa do numpy do usuario): python -B -X utf8, SEM -I (a v402 rodava -I -B -X utf8). Ele acha o delta, o quadro, o runtime_v403.py, o acom_conferencias_v403.py, os insumos\acom (as seis fontes do operador)
# e, pelo delta, as falas do operador em work\cunhagens_13out, pelo CAMINHO DA PROPRIA PASTA: por isso roda NO LUGAR (cd $PK) e nao numa copia dentro de pos_rito\conferidor. Escreve conferencia_rito_v403_POS_RITO.json no pacote (o sufixo evita sobrescrever a conferencia
# que a gerencia rodou a mao) e a copia byte a byte dela vai para pos_rito\conferidor\conferencia_rito_v403.json, que a LEITURA le. As copias dos arquivos do conferidor em pos_rito\conferidor (cp + cmp) sao REGISTRO do que rodou, nao o que roda.
for q in conferir_rito_v403.py delta_v403.py quadro_v397.py runtime_quadro_v397.py acom_conferencias_v403.py runtime_v403.py; do
  cp -p "$PK/$q" "$CONFOUT/"; cmp "$PK/$q" "$CONFOUT/$q" || parar "copia de $q (que o conferidor importa) difere"
done
for f in ESPERADOS_v403.json rito_servidor_v403.log rito_v403_sinal.txt; do
  if [ -f "$PK/$f" ]; then cp -p "$PK/$f" "$CONFOUT/$f"; cmp "$PK/$f" "$CONFOUT/$f" || parar "copia difere: $f"; echo "  copiado byte a byte: $f"; else echo "  (o pacote nao tem $f)"; fi
done
if [ -f "$PK/.servidor_parado_pelo_rito" ]; then parar "o marcador .servidor_parado_pelo_rito ficou no pacote: o servidor do modelo pode estar parado ($(cat "$PK/.servidor_parado_pelo_rito"))"; fi
set +e; (cd "$PK" && $PY_B conferir_rito_v403.py _POS_RITO) > "$CONFOUT/conferir_rito_v403_stdout.txt" 2>&1; c=$?; set -e
cut -c1-240 "$CONFOUT/conferir_rito_v403_stdout.txt"
[ "$c" = "0" ] && tail -1 "$CONFOUT/conferir_rito_v403_stdout.txt" | grep -q "^TUDO BATE" || parar "CONFERIDOR REPROVOU (rc=$c) -- nada foi escrito nas superficies"
[ -f "$PK/conferencia_rito_v403_POS_RITO.json" ] || parar "o conferidor nao gravou conferencia_rito_v403_POS_RITO.json em $PK"
cp -p "$PK/conferencia_rito_v403_POS_RITO.json" "$CONFOUT/conferencia_rito_v403.json"; cmp "$PK/conferencia_rito_v403_POS_RITO.json" "$CONFOUT/conferencia_rito_v403.json" || parar "a copia da conferencia para pos_rito\\conferidor difere"
fi
if quer 2; then
echo "== 2. a leitura da rodada $(date +%T)"
set +e; $PY "$SEL/leitura_v403.py" > "$SEL/leitura_v403_out.txt" 2>&1; l=$?; set -e
tail -1 "$SEL/leitura_v403_out.txt" | cut -c1-600
[ "$l" = "0" ] || parar "a LEITURA tem PROBLEMAS (saida inteira em $SEL/leitura_v403_out.txt)"
fi
if quer 3; then
echo "== 3. ENSAIO em COPIAS: superficies (plano conferido antes da primeira escrita) e a arvore em DRY (nada real e' tocado)"
rm -rf "${ENS:?}" "${ENST:?}"; mkdir -p "$ENS" "$ENST"
cp -p "$NOS/MEMORIA_DA_LINHAGEM.md" "$NOS/DESENHO_DO_FECHAMENTO_QG.md" "$ATLD/TGL_ATLAS.md" "$ATLD/TGL_CORE_MEMORY.md" \
      "$UMEM/MEMORY.md" "$UMEM/MEMORY_2.md" "$HAJA" "$ENS/"
for t in $TOPICOS; do cp -p "$UMEM/$t" "$ENS/"; done
if [ -n "$V403_AVISO_REIVINDICACAO" ]; then cp -p "$AVISO" "$ENS/"; fi
set +e; $PY "$SEL/superficies_v403.py" --copias "$(cygpath -w "$ENS")" > "$SEL/ensaio_superficies_out.txt" 2>&1; es=$?; set -e
tail -24 "$SEL/ensaio_superficies_out.txt" | cut -c1-260
if [ "$es" = "3" ]; then echo "  SUPERFICIES RECUSOU (rc=3): o MEMORY.md passaria do limite (195 linhas ou 24 000 B); a superficie NAO compacta nada; as CONTAGENS estao acima (linhas antes, depois, limite); a gerencia decide o que sai do indice e retoma com CHAIN_DE=3"; fi
[ "$es" = "0" ] || parar "o ENSAIO das superficies falhou (rc=$es) -- nada real foi tocado"
n=$(wc -c < "$ENS/MEMORY.md"); l=$(wc -l < "$ENS/MEMORY.md"); echo "  MEMORY.md da copia: $n B, $l linhas"
[ "$n" -lt 24000 ] || parar "o MEMORY.md da copia chegou a 24 000 B ($n)"
[ "$l" -le 195 ] || parar "o MEMORY.md da copia passou de 195 linhas ($l)"
cp -p "$TOOLS/arvore_da_prova.py" "$TOOLS/atlas_indice.py" "$ENST/"
if [ -f "$SEL/patch_arvore_indice_v403.py" ]; then
  $PY "$SEL/patch_arvore_indice_v403.py" --tools "$(cygpath -w "$ENST")" || parar "o ENSAIO do patch da arvore/indice recusou ou falhou (so copias foram tocadas)"
else
  echo "  (sem patch_arvore_indice_v403.py: a arvore e o indice rodam SEM linha nova da v403 -- a v403 nao tem patch da arvore/indice; as ferramentas escrevem o sha16 sozinhas (na v402 o fizeram); o passo 3 confere isso ANTES de gravar)"
fi
(cd "$ENST" && $PY_B arvore_da_prova.py v403 dry) || parar "a arvore_da_prova.py (copia, dry) falhou"
[ -f "$ENST/arvore_dry.md" ] || parar "a arvore (dry) nao gerou arvore_dry.md em $ENST"
echo "  (fail-early do passo 9: a arvore (dry) e as COPIAS das superficies tem de trazer o sha16 e os marcadores da v403 ANTES de qualquer escrita real)"
exige "$ENST/arvore_dry.md" "$S16"
TOPICO_NOVO=$(topico_novo) || parar "nao li TOPICO_NOVO de textos_v403.py (o arquivo ainda tem trecho marcado para reescrever?)"
exige "$ENS/MEMORIA_DA_LINHAGEM.md" "$S16" "<!-- linhagem_v403_selada -->" $REGS
exige "$ENS/DESENHO_DO_FECHAMENTO_QG.md" "<!-- adendo_v403_selada -->" "$S16"
exige "$ENS/TGL_ATLAS.md" "<!-- atlas_v403_selada -->" "$S16" $REGS
exige "$ENS/TGL_CORE_MEMORY.md" "<!-- core_v403_selada -->" "$S16"
exige "$ENS/CLAUDE.md" "<!-- haja_luz_v403_selada -->" "$S16"
exige "$ENS/MEMORY.md" "$S16"
exige "$ENS/MEMORY_2.md" "v403"
exige "$ENS/estatuto-da-prova-07out.md" "<!-- v403_selada -->" "$S16"
exige "$ENS/$TOPICO_NOVO" "$S16" $REGS
fi
if quer 4; then
if [ -f "$SEL/patch_arvore_indice_v403.py" ]; then
echo "== 4. patches arvore/indice"; $PY "$SEL/patch_arvore_indice_v403.py" || parar "patch arvore/indice recusou/falhou (backups _p403 ao lado)"
else
echo "== 4. patches arvore/indice: PULADO (opcional; sem patch_arvore_indice_v403.py)"
fi
fi
if quer 5; then
echo "== 5. arvore"; (cd "$TOOLS" && $PY_B arvore_da_prova.py v403) || parar "arvore_da_prova.py v403 falhou"
fi
if quer 6; then
echo "== 6. atlas + indice (a ordem da v390: o indice antes das superficies)"; (cd "$TOOLS" && $PY_B atlas_indice.py v403) || parar "atlas_indice.py v403 falhou"
fi
if quer 7; then
echo "== 7-fila. PAUSA do vigia ANTES de escrever o indice (fila\\PAUSA_VIGIA.json: quem, ate = agora + 1 h, motivo; escrita atomica) $(date +%T)"
FRC=0; FOUT=$($PY "$FILA" pausa-criar) || FRC=$?
echo "$FOUT" | cut -c1-500
[ "$FRC" = "0" ] || parar "nao consegui criar a pausa do vigia (rc=$FRC): NAO escrevo o MEMORY.md sem ela (o vigia poderia restaura-lo no meio da escrita); nada foi escrito nas superficies"
echo "== 7. superficies (real: appends datados; a guarda P18 em todo texto; sem errata nova no CLAUDE.md da raiz; o MEMORY.md so' com a pausa valida) $(date +%T)"
set +e; $PY "$SEL/superficies_v403.py"; sr=$?; set -e
if [ "$sr" = "3" ]; then echo "  SUPERFICIES RECUSOU (rc=3): o MEMORY.md passaria do limite (195 linhas ou 24 000 B); a superficie NAO compacta nada; as CONTAGENS estao acima; a gerencia decide o que sai do indice e retoma com CHAIN_DE=7"; fi
[ "$sr" = "0" ] || parar "superficies_v403.py parou (rc=$sr; backups .bak_<STAMP>_sup403 ao lado; rerodar e IDEMPOTENTE). A PAUSA_VIGIA.json PERMANECE posta (vale no maximo 4 h; evita que o vigia restaure o indice no meio do trabalho): a gerencia retoma com CHAIN_DE=7 (a pausa nossa e' aceita e renovada) ou, se desistir, a remove a mao"
fi
if quer 8; then
echo "== 8. espelho da memoria"
set +e; $PY_B "$PORTA" > "$SEL/porta_memoria_v403_out.txt" 2>&1; pm=$?; set -e
tail -1 "$SEL/porta_memoria_v403_out.txt"
[ "$pm" = "0" ] || parar "porta_memoria.py saiu com rc=$pm"
fi
if quer 9; then
echo "== 9. regra da linhagem completa: o MARCADOR DO SELO e o sha16 do um.py v403 ($S16) em cada superficie (zero e' falha visivel)"
exige "$NOS/MEMORIA_DA_LINHAGEM.md" "$S16" "<!-- linhagem_v403_selada -->" $REGS
exige "$NOS/DESENHO_DO_FECHAMENTO_QG.md" "<!-- adendo_v403_selada -->" "$S16"
exige "$ATLD/TGL_ATLAS.md" "<!-- atlas_v403_selada -->" "$S16" $REGS
exige "$ATLD/TGL_INDICE_VIVO.md" "$S16"
exige "$ATLD/TGL_CORE_MEMORY.md" "<!-- core_v403_selada -->" "$S16"
exige "$NOS/A_PROVA_DA_QG_TGL_arvore.md" "$S16"
exige "$HAJA" "<!-- haja_luz_v403_selada -->" "$S16"
exige "$UMEM/MEMORY.md" "$S16"
exige "$UMEM/MEMORY_2.md" "v403"
for t in missao-ultima-flag-um-py.md central-de-patentes-estado.md; do exige "$UMEM/$t" "$S16"; done
exige "$UMEM/estatuto-da-prova-07out.md" "<!-- v403_selada -->" "$S16"
TOPICO_NOVO=$(topico_novo) || parar "nao li TOPICO_NOVO de textos_v403.py"
exige "$UMEM/$TOPICO_NOVO" "$S16" $REGS
if [ -n "$V403_AVISO_REIVINDICACAO" ]; then exige "$AVISO" "<!-- aviso_v403_selada -->" "$S16"; else echo "  (AVISO_GERENCIA.md: PULADO -- sem V403_AVISO_REIVINDICACAO; escrever depois, sob reivindicacao)"; fi
n=$(wc -c < "$UMEM/MEMORY.md"); l=$(wc -l < "$UMEM/MEMORY.md"); echo "  MEMORY.md: $n B (limite 24000), $l linhas (limite 195)"
[ "$n" -lt 24000 ] || parar "MEMORY.md chegou a 24 000 B ($n)"
[ "$l" -le 195 ] || parar "MEMORY.md passou de 195 linhas ($l): o carregador do harness o corta acima de 200 (a PAUSA_VIGIA.json PERMANECE; vale no maximo 4 h)"
# FILA DA MEMORIA, passos (iii) a (v): so' DEPOIS da escrita e da validacao do indice. Renova a pausa (uma retomada pode ter passado de 1 h), PINA (rc 0 exigido), SO' ENTAO solta a pausa, e por ultimo verifica a fila (rc 0 e ok:true).
echo "== 9-fila. FILA DA MEMORIA: renovar a pausa, PINAR o indice (MEMORIA_GERENCIA=claude-c1 memoria.py pinar --motivo \"pos-rito v403\"), soltar a pausa, verificar $(date +%T)"
FRC=0; FOUT=$($PY "$FILA" pausa-criar) || FRC=$?
echo "$FOUT" | cut -c1-400
[ "$FRC" = "0" ] || parar "nao consegui renovar a pausa do vigia (rc=$FRC) antes de pinar: o indice NAO foi pinado e a pausa, se existe, PERMANECE (vale no maximo 4 h); a gerencia confere e retoma com CHAIN_DE=9"
FRC=0; FOUT=$($PY "$FILA" pinar) || FRC=$?
echo "$FOUT" | cut -c1-600
[ "$FRC" = "0" ] || parar "memoria.py pinar FALHOU (rc=$FRC): o indice NAO foi pinado e a PAUSA_VIGIA.json PERMANECE posta (vale no maximo 4 h; evita que o vigia restaure o indice recem-escrito); a gerencia le o erro acima, confere o indice e retoma com CHAIN_DE=9"
FRC=0; FOUT=$($PY "$FILA" pausa-remover) || FRC=$?
echo "$FOUT" | cut -c1-400
[ "$FRC" = "0" ] || parar "o indice foi PINADO, mas nao consegui remover a PAUSA_VIGIA.json (rc=$FRC): a gerencia a remove a mao (ela vale no maximo 4 h) e roda o verificar; retomar com CHAIN_DE=9"
FRC=0; FOUT=$($PY "$FILA" verificar) || FRC=$?
echo "$FOUT" | cut -c1-700
[ "$FRC" = "0" ] || parar "memoria.py verificar reprovou (rc=$FRC): o indice esta PINADO e a pausa foi removida; as violacoes estao acima; a gerencia as le (a cadeia nao restaura nada)"
fi
if quer 10; then
echo "== 10. B(n) da Bancada, ENSAIO pos-selo, passo simples v402 -> v403 (sem salto), esboco R3.5 (nada e' gravado na Bancada; o servico pode estar no ar) $(date +%T)"
b3_prepara 10
SAIDA_E="$PK/bancada_B3_ensaio_$(date +%Y%m%d_%H%M%S)"
set +e
$PY "$W_ESB" --bancada 'C:\IALD\Bancada_Um' --producao --nos "$W_NOS" --versao v403 --fase pos_selo --modo ensaio --bateria "$W_BAT" --bateria-sha256 "$BAT" \
    --recibo-pre-selo "$W_RPS" --recibo-pre-selo-sha256 "$RPS" --selo-anterior "$W_SELO" --kernel-manifesto-anterior "$W_KMAN" \
    --kernel-recibo "$W_KR" --kernel-recibo-sha256 "$KRSHA" --criterios "$W_CRI" --criterios-sha256 "$CRI" \
    --saida "$(cygpath -w "$SAIDA_E")" > "$SEL/b3_ensaio_out.txt" 2>&1; b3=$?
set -e
tail -4 "$SEL/b3_ensaio_out.txt" | cut -c1-402
[ "$b3" = "0" ] || parar "o B(n) ENSAIO reprovou (rc=$b3): saida inteira em $SEL/b3_ensaio_out.txt"
$PY "$SEL/b3_recibo_v403.py" "$(cygpath -w "$SEL/b3_ensaio_out.txt")" ensaio || parar "o recibo do B(n) ENSAIO nao confere"
fi
if quer 10a; then
echo "== 10-bis-a. a parada do servico da Bancada Um (porta 18777), com recibo"
RP="$PK/bancada_B3_servico/RECIBO_PARADA_v403.json"
[ -f "$RP" ] || aguarda "sem o recibo da PARADA do um_bancada.py ($RP): o servico esta no ar na porta 18777 e tem de ser PARADO pelo PID (ato do operador; nunca por nome); so' depois se gera o recibo com bancada_B3_servico/recibo_parada_v403.py (exige V403_AUTORIZACAO_OPERADOR no ambiente; confere a porta fechada e zero processo um_bancada.py). Sem esse recibo a cadeia para aqui."
$PY -c "import socket,sys
try:
    socket.create_connection(('127.0.0.1', 18777), timeout=1.5).close()
except OSError:
    sys.exit(0)
sys.exit(1)" || parar "o servico da Bancada esta no AR (a porta 18777 responde) apesar do recibo de parada"
echo "  recibo da parada: $RP (sha256 $(sha256f "$(cygpath -w "$RP")")); porta 18777 fechada"
fi
if quer 10b; then
echo "== 10-bis. B(n) APLICAR, passo simples v402 -> v403 (sem salto), esboco R3.5 (grava o manifesto B<n> na Bancada de producao: backup de bytes, rollback se falhar) $(date +%T)"
[ "$B3_AUTORIZADO" = "sim" ] || aguarda "a B(n) nao esta autorizada: ato da gerencia sob evento c1 (SINCRONIZACAO_BANCADA, que nomeia a v403) + autorizacao do operador. Definir B3_AUTORIZADO=sim, EVENTO=<seq> e EVENTO_HASH=<hash16 do retorno de iald.py anotar>, com o servico parado (10-bis-a) e o recibo da parada, e retomar com CHAIN_DE=10b"
[ -n "$EVENTO" ] && [ -n "$EVENTO_HASH" ] || aguarda "faltam EVENTO e EVENTO_HASH (o elo do evento c1 nomeando a gravacao)"
[ -f "$PK/bancada_B3_servico/RECIBO_PARADA_v403.json" ] || aguarda "sem o recibo da parada do servico (10-bis-a)"
b3_prepara 10b
SAIDA_B3="$PK/bancada_B3"; k=1; while [ -e "$SAIDA_B3" ]; do k=$((k+1)); SAIDA_B3="$PK/bancada_B3_$k"; done
echo "  saida do B(n): $SAIDA_B3 (pasta nova)"
set +e
$PY "$W_ESB" --bancada 'C:\IALD\Bancada_Um' --producao --nos "$W_NOS" --versao v403 --fase pos_selo --modo aplicar --bateria "$W_BAT" --bateria-sha256 "$BAT" \
    --evento "$EVENTO" --evento-hash "$EVENTO_HASH" \
    --recibo-pre-selo "$W_RPS" --recibo-pre-selo-sha256 "$RPS" --selo-anterior "$W_SELO" --kernel-manifesto-anterior "$W_KMAN" \
    --kernel-recibo "$W_KR" --kernel-recibo-sha256 "$KRSHA" --criterios "$W_CRI" --criterios-sha256 "$CRI" \
    --saida "$(cygpath -w "$SAIDA_B3")" > "$SEL/b3_aplicar_out.txt" 2>&1; b3=$?
set -e
tail -4 "$SEL/b3_aplicar_out.txt" | cut -c1-402
[ "$b3" = "0" ] || parar "o B(n) APLICAR reprovou (rc=$b3): saida inteira em $SEL/b3_aplicar_out.txt; NADA foi restaurado por esta cadeia (o esboco faz o seu rollback)"
$PY "$SEL/b3_recibo_v403.py" "$(cygpath -w "$SEL/b3_aplicar_out.txt")" aplicar || parar "o recibo do B(n) APLICAR nao confere"
fi
if quer 10c; then
echo "== 10-ter. o religamento do servico e a reconexao dos adaptadores MCP (ato do operador)"
RR="$PK/bancada_B3_servico/RECIBO_RELIGAMENTO_v403.json"
[ -f "$RR" ] || aguarda "sem o recibo do RELIGAMENTO do um_bancada.py ($RR): religar o servico (ato do operador; o comando esta no campo religar do RECIBO_PARADA_v403.json) e gerar o recibo com bancada_B3_servico/recibo_religamento_v403.py (exige V403_AUTORIZACAO_OPERADOR; confere a versao servida v403, o sha do manifesto novo, o um.py e o PID); reconectar os adaptadores MCP das sessoes e ato do operador"
echo "  recibo do religamento: $RR (sha256 $(sha256f "$(cygpath -w "$RR")")); o fechar o confere contra o recibo do 10-bis"
fi
if quer 11; then
echo "== 11. fechar (manifesto com o estado da fila da memoria, arquivo, os dois diffs, handoff) -- recusa sem os tres recibos do B(n)"
$PY "$SEL/fechar_v403.py" || parar "fechar_v403.py falhou"
fi
if quer 12; then
echo "== 12. registro no mapa de rotas: so MONTA o JSON e o comando (o registro e' ato da gerencia)"
$PY "$SEL/registrar_mapa_v403.py" || parar "registrar_mapa_v403.py falhou"
fi
if quer 13; then
echo "== 13. o inventario da bancada Lean (work\\inventario_bancada) regenerado; copia para memory\\ com backup de bytes"
(cd "$INV" && $PY_B inventario_bancada.py > "$SEL/inventario_bancada_out.txt" 2>&1 && $PY_B gerar_documento.py >> "$SEL/inventario_bancada_out.txt" 2>&1) || parar "o inventario da bancada falhou (ver $SEL/inventario_bancada_out.txt)"
tail -2 "$SEL/inventario_bancada_out.txt" | cut -c1-240
for f in INVENTARIO_BANCADA_CHATGPT.md INVENTARIO_BANCADA_CHATGPT.json; do
  [ -f "$INV/$f" ] || parar "o inventario nao gerou $f"
  if [ -f "$ATLD/$f" ]; then B="$ATLD/$f.bak_$(date +%Y%m%d_%H%M%S)_v403"; cp -p "$ATLD/$f" "$B"; cmp "$ATLD/$f" "$B" || parar "backup de bytes falhou: $B"; fi
  cp -p "$INV/$f" "$ATLD/$f.tmp_v403" && mv "$ATLD/$f.tmp_v403" "$ATLD/$f"; cmp "$INV/$f" "$ATLD/$f" || parar "a copia do inventario difere: $f"
done
fi
if quer 14; then
echo "== 14. o Nos vivo reconstruido (le o mapa de rotas: rodar depois do registro da gerencia no passo 12)"
$PY_B /c/IALD/NOS_VIVO/construir.py > "$SEL/nos_vivo_out.txt" 2>&1 || parar "NOS_VIVO/construir.py falhou (ver $SEL/nos_vivo_out.txt)"
tail -3 "$SEL/nos_vivo_out.txt" | cut -c1-240
fi
echo "== FIM $(date +%T)"
