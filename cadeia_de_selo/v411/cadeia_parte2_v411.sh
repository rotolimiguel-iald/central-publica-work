#!/bin/sh
# [ADAPTADO v411, 12/11/2026, claude-construtor-v411 (retomada, fork B)] REMISSAO CURTA: na v411 a sequencia inteira da preparacao (registro offline, guardas, candidato, comparacao, ensaio a seco, ESPERADOS, conferidores, citacoes, diff e pinos, instalar/rito, p00, fim_de_cadeia com o B20 pre-selo, relatorio) esta' em cadeia_v411.sh, uma so' e fail-closed; a logica da cadeia_parte2_v410.sh nao e' duplicada aqui.
# O que a cadeia_parte2_v410.sh fazia alem disso, na v411: a pendencia do MEMORY.md (o p00 a diz pendente; so' a gerencia escreve o MEMORY.md), a purga (purga_v411.py --listar, ~20 min, so' leitura) e o deposito do construtor (depositar_construtor_v411.py, so' com PREPARACAO_v411_PRONTA.json pronta = true) -- chamados pelo nome depois da cadeia_v411.sh.
# uso: sh ./cadeia_parte2_v411.sh   (repassa a cadeia_v411.sh; o modo de ensaio do topo proposto vem do ambiente, V411_ENSAIO_TOPO_PROPOSTO=1)
cd "$(dirname "$0")" || exit 9
[ -f ./cadeia_v411.sh ] || { echo "FALTA cadeia_v411.sh (a sequencia da v411)"; exit 9; }
exec sh ./cadeia_v411.sh "$@"
