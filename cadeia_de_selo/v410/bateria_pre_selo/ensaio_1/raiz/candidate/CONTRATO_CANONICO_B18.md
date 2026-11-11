# Contrato de fidelidade da Bancada Um -- B18 / v409 (sincronizacao)

[REAL] Gerado por sincronizar_bancada.py R3.5 (19/10/2026) em 20261106_014125 UTC, no passo B(18) da cadeia de selo da v409, sob o evento c1 1491.

## Identidade pinada

- um.py v409: sha256 53284ba461ecd94060cc2d12fed992bba70ab857f70198b24e6535b9f24f8da6 (43970027 B), linha de alpha 5584 (unica, coluna 0, sem reatribuicao); beta = alpha*sqrt(e) em runtime = 0.012031300400803142.
- selo: sha256 d0dbcd8a23718707c9d707c1f1b7b4a3e86f80718fe24fafbcb6c188b4b5e97c.
- manifesto anterior: B17-v408-20261105-R1 (sha256 0cd0446407c4258a9312ff454daf9d5469688f53e577e14cad8568245ef2d608).
- recibo pre-selo (testes finais contra a versao anterior): sha256 e2b65da9aa9d8a10c9e52229e7129604b0b1b6ae2100ad2bf529b6a22dc351a0.

## A regra

Uma versao nova do um.py invalida o contrato instalado: o canonical.py recusa toda operacao cientifica (PIN_CHANGED) ate que
o passo B(n) da cadeia regenere o manifesto, re-pine, rode a bateria sintetica e grave o recibo. Codigo e fontes NAO mudam numa
sincronizacao: mudar codigo ou fonte e implantacao B, com plano, testes e evento proprios. Nunca atualizar so o hash: a mesma versao
com outro hash do um.py e SELO_PROGRAMA_DIVERGE, recusado salvo reparo nomeado em evento. Nada se grava na Bancada sem evento c1
nomeado e verificado pela cadeia de hash do quadro. Custodia de fonte nao e admissao pelo operador. NOT_FALSIFIED nao e creditacao;
nenhum rito move o gate.
