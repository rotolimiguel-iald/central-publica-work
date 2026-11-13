#!/bin/sh
# [ADAPTADO v411, 12/11/2026, claude-construtor-v411 (retomada, fork A)] REESCRITO: na v411 a SEQUENCIA EXATA da preparacao e' UMA so', cadeia_v411.sh (da frente pre-selo: registro offline, guardas, quadro, citacoes, candidato, comparacao, ensaio a seco, ESPERADOS, conferidores, citacoes do candidato, diff e pinos, instalar/rito, p00, fim de cadeia, relatorio); este script so' a CHAMA (nao duplica a ordem), com --regerar exportando V411_REGERAR=1, e, com --ensaio, roda a mesma cadeia no MODO DE ENSAIO DO TOPO PROPOSTO (V411_ENSAIO_TOPO_PROPOSTO=1: saidas fora de work\, o artefato NAO e' candidato)
# refazer_candidato_v411.sh -- refaz, NA ORDEM, tudo o que depende do texto do candidato v411 chamando cadeia_v411.sh (a ordem mora la'; aqui so' o modo). USAR quando mudar qualquer script ou texto que entra no candidato (runtime_h0dn_v411.py,
# quadro_v411.py, registros_h0dn_v411.py, registros_v411.py, guarda_frases_v411.py, delta_v411.py, gerar_candidato_v411.py) ou os insumos (copiar_insumos_v411.py antes: ver regerar_v411.sh). A v411 NAO tem modulo novo: o kernel nao se refaz por aqui.
# Nao toca o Nos, nao instala, nao roda o rito. Para no primeiro passo que falha (o rc da cadeia e' o deste script). Saida inteira em refazer_out_v411.txt (e a da cadeia em cadeia_v411_out.txt).
# uso: sh ./refazer_candidato_v411.sh [--regerar] [--ensaio]   (--regerar autoriza sobrescrever um candidato ja existente; --ensaio = o modo de ensaio do topo proposto)
V="/c/IALD/Central de Patentes/work/cadeia_de_selo/v411"
cd "$V" || exit 9
for a in "$@"; do
  case "$a" in
    --regerar) export V411_REGERAR=1 ;;
    --ensaio) export V411_ENSAIO_TOPO_PROPOSTO=1 ;;
    *) echo "argumento desconhecido: $a (uso: sh ./refazer_candidato_v411.sh [--regerar] [--ensaio])"; exit 2 ;;
  esac
done
[ -f cadeia_v411.sh ] || { echo "falta cadeia_v411.sh (a sequencia exata da v411)"; exit 9; }
echo "== refazer_candidato_v411.sh $(date +%T): modo $([ "$V411_ENSAIO_TOPO_PROPOSTO" = 1 ] && echo ENSAIO_DO_TOPO_PROPOSTO || echo REAL) | regerar=${V411_REGERAR:-0}" | tee refazer_out_v411.txt
sh ./cadeia_v411.sh >> refazer_out_v411.txt 2>&1; RC=$?
tail -5 refazer_out_v411.txt
echo "RC_REFAZER=$RC" >> refazer_out_v411.txt
[ "$RC" -eq 0 ] && echo "== FIM $(date +%T)" | tee -a refazer_out_v411.txt
exit $RC
