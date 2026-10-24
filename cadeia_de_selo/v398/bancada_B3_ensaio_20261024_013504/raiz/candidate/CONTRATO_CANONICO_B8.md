# Contrato de fidelidade da Bancada Um -- B8 / v398 (sincronizacao)

[REAL] Gerado por sincronizar_bancada.py R3.5 (19/10/2026) em 20261024_013504 UTC, no passo B(8) da cadeia de selo da v398, sob o evento c1 None.

## Identidade pinada

- um.py v398: sha256 c632fa261ce3f53879374dde1199485283bd69bdfb7505edbeceefb7f9a49cf4 (38421415 B), linha de alpha 5584 (unica, coluna 0, sem reatribuicao); beta = alpha*sqrt(e) em runtime = 0.012031300400803142.
- selo: sha256 7b46af660e7cb895ef40a2cfc216cacf4ff65385c3d305ecf97ffbba493dc8a1.
- manifesto anterior: B7-v397-20261023-R1 (sha256 55a4462c1c5ecfefd334aaf1423aac545b688f7c07e2f95f1ac1ceb65f99f3a3).
- recibo pre-selo (testes finais contra a versao anterior): sha256 ca76584c1c6c9993db39140cc2b56c5d4a736c7ac867390b2e261df49e3af420.

## A regra

Uma versao nova do um.py invalida o contrato instalado: o canonical.py recusa toda operacao cientifica (PIN_CHANGED) ate que
o passo B(n) da cadeia regenere o manifesto, re-pine, rode a bateria sintetica e grave o recibo. Codigo e fontes NAO mudam numa
sincronizacao: mudar codigo ou fonte e implantacao B, com plano, testes e evento proprios. Nunca atualizar so o hash: a mesma versao
com outro hash do um.py e SELO_PROGRAMA_DIVERGE, recusado salvo reparo nomeado em evento. Nada se grava na Bancada sem evento c1
nomeado e verificado pela cadeia de hash do quadro. Custodia de fonte nao e admissao pelo operador. NOT_FALSIFIED nao e creditacao;
nenhum rito move o gate.
