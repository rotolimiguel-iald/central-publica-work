#!/bin/sh
# regerar_v404.sh -- refaz, NA ORDEM, tudo o que depende das TRES PEDRAS (work\cadeia_de_selo\v404_kernel\pedras\Caminho.lean, Vida.lean e VerdadeAdendo.lean): copia de bytes das pedras e dos insumos, sandbox do kernel (C:\t\k404c), build incremental + Audit,
# pos-build, insumos, e depois o refazer_candidato_v404.sh --regerar (candidato, comparacao AST, ensaio a seco, ESPERADOS, conferidor, citacoes, pinos, pre-condicoes). Nao toca o Nos, nao instala, nao roda o rito.
# ANTES: (1) atualizar pedras_sha16_da_ordem.json (o pino de cada pedra, lido do arquivo da pedra) e, se o CONTRATO ou o SUPORTE de alguma mudar, delta_v404.py; (2) apagar de pedra\ e insumos\ as COPIAS antigas (pedra\*.lean,
# insumos\*.lean, insumos\KH_N1_v404.json): os copiadores NAO sobrescrevem o que difere (abortam). O build leva ~10 a 25 min no sandbox. Depois: python -I -B -X utf8 purga_v404.py (tem de dar ZERO).
# uso: sh ./regerar_v404.sh   (cada passo para na primeira falha; nenhum passo e' mascarado por pipe)
set -e
V="/c/IALD/Central de Patentes/work/cadeia_de_selo/v404"
cd "$V"
PY="python -I -B -X utf8"
echo "== a. copiar_pedras_v404.py $(date +%T)"; $PY copiar_pedras_v404.py
echo "== b. preparar_kernel_v404.py gerar + conferir"; $PY preparar_kernel_v404.py gerar > /tmp/regerar_b1.txt; $PY preparar_kernel_v404.py conferir > /tmp/regerar_b2.txt; tail -1 /tmp/regerar_b2.txt
echo "== c. construir_kernel_v404.sh (lake build incremental + Audit) $(date +%T)"; sh ./construir_kernel_v404.sh
echo "== d. pos_build_kernel_v404.py (tem de dar VERDE)"; $PY pos_build_kernel_v404.py > /tmp/regerar_d.txt; tail -1 /tmp/regerar_d.txt
echo "== e. copiar_insumos_v404.py"; $PY copiar_insumos_v404.py > /tmp/regerar_e.txt; tail -1 /tmp/regerar_e.txt
echo "== f. refazer_candidato_v404.sh --regerar $(date +%T)"; sh ./refazer_candidato_v404.sh --regerar
echo "== FIM $(date +%T)"
