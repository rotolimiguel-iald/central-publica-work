# Contrato de fidelidade da Bancada Um -- B4 / v393 (sincronizacao)

[REAL] Gerado por sincronizar_bancada.py R3.4 (19/10/2026) em 20261019_134158 UTC, no passo B(4) da cadeia de selo da v393, sob o evento c1 None.

## Identidade pinada

- um.py v393: sha256 18be2ddb06c60f9037b1efecb72034e6a0c9409b0d3900452fd9d186cf4905c0 (35606254 B), linha de alpha 5584 (unica, coluna 0, sem reatribuicao); beta = alpha*sqrt(e) em runtime = 0.012031300400803142.
- selo: sha256 bfddccfd153374dd3f337ac3e4c2efd2a77d2bfc2ba7ac2bfa7e96d0864416ce.
- manifesto anterior: B3-v392-20261013-R1 (sha256 6733b9a28c725244deba60eb41a80965af4bc1605c9526838852a0fc6422527e).
- recibo pre-selo (testes finais contra a versao anterior): sha256 (ausente: so em --sandbox).

## A regra

Uma versao nova do um.py invalida o contrato instalado: o canonical.py recusa toda operacao cientifica (PIN_CHANGED) ate que
o passo B(n) da cadeia regenere o manifesto, re-pine, rode a bateria sintetica e grave o recibo. Codigo e fontes NAO mudam numa
sincronizacao: mudar codigo ou fonte e implantacao B, com plano, testes e evento proprios. Nunca atualizar so o hash: a mesma versao
com outro hash do um.py e SELO_PROGRAMA_DIVERGE, recusado salvo reparo nomeado em evento. Nada se grava na Bancada sem evento c1
nomeado e verificado pela cadeia de hash do quadro. Custodia de fonte nao e admissao pelo operador. NOT_FALSIFIED nao e creditacao;
nenhum rito move o gate.

## Salto (R3.4)

A Bancada pinava v392 e foi levada a v393 sem passar pelas versoes puladas v393 (nenhuma delas teve elo B(n)). A cadeia de selos (sha256 0f96cebd7c2135c17204153b733be4578b1c2a40fd94cb38f0984693e4194a4e, 2 elos) liga,
por hash, o que a Bancada pinava ao Nos que o recibo pre-selo testou (v393): copias de bytes de cada versao, o selo de cada uma pinando o seu um.py e o
seu manifesto do kernel, e o registro do instalador de cada troca com os backups de bytes. Sem cadeia verificavel o salto e recusado.
