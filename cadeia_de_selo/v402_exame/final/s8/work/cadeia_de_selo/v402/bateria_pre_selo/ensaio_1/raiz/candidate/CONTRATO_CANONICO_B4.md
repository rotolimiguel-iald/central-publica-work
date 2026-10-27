# Contrato de fidelidade da Bancada Um -- B4 / v394 (sincronizacao)

[REAL] Gerado por sincronizar_bancada.py R3.5 (19/10/2026) em 20261019_174116 UTC, no passo B(4) da cadeia de selo da v394, sob o evento c1 1037.

## Identidade pinada

- um.py v394: sha256 972e81f22dd8cc68bd5671fa610d2664e26f4681ab52932e001e5ef97e8f5991 (37885889 B), linha de alpha 5584 (unica, coluna 0, sem reatribuicao); beta = alpha*sqrt(e) em runtime = 0.012031300400803142.
- selo: sha256 993e26f19f12de1c5ad4999d4f789cc7c5a08c5f3640edbeb9502e85f1a94ef3.
- manifesto anterior: B3-v392-20261013-R1 (sha256 6733b9a28c725244deba60eb41a80965af4bc1605c9526838852a0fc6422527e).
- recibo pre-selo (testes finais contra a versao anterior): sha256 0d82d598229fd39881193f69843dfda17968c9170696647ab827e8643f26e878.

## A regra

Uma versao nova do um.py invalida o contrato instalado: o canonical.py recusa toda operacao cientifica (PIN_CHANGED) ate que
o passo B(n) da cadeia regenere o manifesto, re-pine, rode a bateria sintetica e grave o recibo. Codigo e fontes NAO mudam numa
sincronizacao: mudar codigo ou fonte e implantacao B, com plano, testes e evento proprios. Nunca atualizar so o hash: a mesma versao
com outro hash do um.py e SELO_PROGRAMA_DIVERGE, recusado salvo reparo nomeado em evento. Nada se grava na Bancada sem evento c1
nomeado e verificado pela cadeia de hash do quadro. Custodia de fonte nao e admissao pelo operador. NOT_FALSIFIED nao e creditacao;
nenhum rito move o gate.

## Salto (R3.4)

A Bancada pinava v392 e foi levada a v394 sem passar pelas versoes puladas v393 (nenhuma delas teve elo B(n)). A cadeia de selos (sha256 0f96cebd7c2135c17204153b733be4578b1c2a40fd94cb38f0984693e4194a4e, 2 elos) liga,
por hash, o que a Bancada pinava ao Nos que o recibo pre-selo testou (v393): copias de bytes de cada versao, o selo de cada uma pinando o seu um.py e o
seu manifesto do kernel, e o registro do instalador de cada troca com os backups de bytes. Sem cadeia verificavel o salto e recusado.
