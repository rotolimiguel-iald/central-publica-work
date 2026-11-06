# Contrato de fidelidade da Bancada Um -- B16 / v407 (sincronizacao)

[REAL] Gerado por sincronizar_bancada.py R3.5 (19/10/2026) em 20261104_073356 UTC, no passo B(16) da cadeia de selo da v407, sob o evento c1 1459.

## Identidade pinada

- um.py v407: sha256 833121339e649f7171e2eccca1a19b3a1564aa306a787ed8cea76ded0fdf3475 (43065098 B), linha de alpha 5584 (unica, coluna 0, sem reatribuicao); beta = alpha*sqrt(e) em runtime = 0.012031300400803142.
- selo: sha256 d84834f41ec3d87c1d54ec05126fa0f52a1c9e61ae62f13521ed508449dbc54b.
- manifesto anterior: B15-v406-20261103-R1 (sha256 e91d3f4541b38c12cc75da9b004e3bd45fbde7517c44973f23f17e1d4ca5af16).
- recibo pre-selo (testes finais contra a versao anterior): sha256 49e993106e3437b034fc2c0a6b1db5b3f6df7892e1215f4ef5f2cb73bf9f2518.

## A regra

Uma versao nova do um.py invalida o contrato instalado: o canonical.py recusa toda operacao cientifica (PIN_CHANGED) ate que
o passo B(n) da cadeia regenere o manifesto, re-pine, rode a bateria sintetica e grave o recibo. Codigo e fontes NAO mudam numa
sincronizacao: mudar codigo ou fonte e implantacao B, com plano, testes e evento proprios. Nunca atualizar so o hash: a mesma versao
com outro hash do um.py e SELO_PROGRAMA_DIVERGE, recusado salvo reparo nomeado em evento. Nada se grava na Bancada sem evento c1
nomeado e verificado pela cadeia de hash do quadro. Custodia de fonte nao e admissao pelo operador. NOT_FALSIFIED nao e creditacao;
nenhum rito move o gate.
