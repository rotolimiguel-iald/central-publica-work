#!/bin/sh
# regerar_v401.sh -- refaz, NA ORDEM, tudo o que depende da PEDRA (work\falsidade_da_inercia_v401\FalsidadeDaInercia.lean): copia de bytes da pedra e dos insumos, sandbox do kernel (C:\t\k401c), build incremental + Audit,
# pos-build, insumos, e depois o refazer_candidato_v401.sh --regerar (candidato, comparacao AST, ensaio a seco, ESPERADOS, conferidor, citacoes, pinos, pre-condicoes). Nao toca o Nos, nao instala, nao roda o rito.
# ANTES: (1) atualizar pedra_sha16_da_ordem.txt (o pino da ordem, lido do arquivo da pedra) e, se o CONTRATO ou o SUPORTE mudarem, delta_v401.py; (2) apagar de pedra\ e insumos\ as COPIAS antigas (pedra\FalsidadeDaInercia.lean,
# insumos\FalsidadeDaInercia.lean, insumos\KH_N1_v401.json): os copiadores NAO sobrescrevem o que difere (abortam). O build leva ~10 a 25 min no sandbox. Depois: python -I -B -X utf8 purga_v401.py (tem de dar ZERO).
# uso: sh ./regerar_v401.sh   (cada passo para na primeira falha; nenhum passo e' mascarado por pipe)
set -e
V="/c/IALD/Central de Patentes/work/cadeia_de_selo/v401"
cd "$V"
PY="python -I -B -X utf8"
echo "== a. copiar_pedras_v401.py $(date +%T)"; $PY copiar_pedras_v401.py
echo "== b. preparar_kernel_v401.py gerar + conferir"; $PY preparar_kernel_v401.py gerar > /tmp/regerar_b1.txt; $PY preparar_kernel_v401.py conferir > /tmp/regerar_b2.txt; tail -1 /tmp/regerar_b2.txt
echo "== c. construir_kernel_v401.sh (lake build incremental + Audit) $(date +%T)"; sh ./construir_kernel_v401.sh
echo "== d. pos_build_kernel_v401.py (tem de dar VERDE)"; $PY pos_build_kernel_v401.py > /tmp/regerar_d.txt; tail -1 /tmp/regerar_d.txt
echo "== e. copiar_insumos_v401.py"; $PY copiar_insumos_v401.py > /tmp/regerar_e.txt; tail -1 /tmp/regerar_e.txt
echo "== f. refazer_candidato_v401.sh --regerar $(date +%T)"; sh ./refazer_candidato_v401.sh --regerar
echo "== FIM $(date +%T)"
