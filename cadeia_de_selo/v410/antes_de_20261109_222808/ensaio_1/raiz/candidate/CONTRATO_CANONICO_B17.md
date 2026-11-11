# Contrato de fidelidade da Bancada Um -- B17 / v408 (sincronizacao)

[REAL] Gerado por sincronizar_bancada.py R3.5 (19/10/2026) em 20261105_050935 UTC, no passo B(17) da cadeia de selo da v408, sob o evento c1 1473.

## Identidade pinada

- um.py v408: sha256 e7bc6b10e8ff76beb40e05e45fb47adf9bcc2f9222440552af017deb4435e365 (43466447 B), linha de alpha 5584 (unica, coluna 0, sem reatribuicao); beta = alpha*sqrt(e) em runtime = 0.012031300400803142.
- selo: sha256 3ad4be10599155c1a476eff1622b02c29b254ffcd5030d251643337aea325709.
- manifesto anterior: B16-v407-20261104-R1 (sha256 8d2165cf566e28e70759594e55fb02d40261fe36d8ac9dbea32d85e317202da6).
- recibo pre-selo (testes finais contra a versao anterior): sha256 193aaebdcf76f54a0203eb60f3c6131320c754b22bb9c9ca8bb4b08ad529520c.

## A regra

Uma versao nova do um.py invalida o contrato instalado: o canonical.py recusa toda operacao cientifica (PIN_CHANGED) ate que
o passo B(n) da cadeia regenere o manifesto, re-pine, rode a bateria sintetica e grave o recibo. Codigo e fontes NAO mudam numa
sincronizacao: mudar codigo ou fonte e implantacao B, com plano, testes e evento proprios. Nunca atualizar so o hash: a mesma versao
com outro hash do um.py e SELO_PROGRAMA_DIVERGE, recusado salvo reparo nomeado em evento. Nada se grava na Bancada sem evento c1
nomeado e verificado pela cadeia de hash do quadro. Custodia de fonte nao e admissao pelo operador. NOT_FALSIFIED nao e creditacao;
nenhum rito move o gate.
