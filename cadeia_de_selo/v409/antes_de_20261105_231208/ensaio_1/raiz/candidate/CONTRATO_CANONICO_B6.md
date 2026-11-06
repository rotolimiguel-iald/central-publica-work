# Contrato de fidelidade da Bancada Um -- B6 / v396 (sincronizacao)

[REAL] Gerado por sincronizar_bancada.py R3.5 (19/10/2026) em 20261022_131712 UTC, no passo B(6) da cadeia de selo da v396, sob o evento c1 1115.

## Identidade pinada

- um.py v396: sha256 0a4395a89eeebbb74c06ab5d8d29ea7708cb76ac704205a7e7aabc3f4d35b6c8 (38162265 B), linha de alpha 5584 (unica, coluna 0, sem reatribuicao); beta = alpha*sqrt(e) em runtime = 0.012031300400803142.
- selo: sha256 d59ef82736758a1c8b3b9fcf56eb445ca6b738883ebd9b13555a978e1caa49b5.
- manifesto anterior: B5-v395-20261021-R1 (sha256 5ad4c67b56de5d34929a02b8721b42275f302b1de0ff3660c37bb49a862bffd3).
- recibo pre-selo (testes finais contra a versao anterior): sha256 19871055b4331efaad939a296eae3cea02d879ee1374322ac82004d49233bf16.

## A regra

Uma versao nova do um.py invalida o contrato instalado: o canonical.py recusa toda operacao cientifica (PIN_CHANGED) ate que
o passo B(n) da cadeia regenere o manifesto, re-pine, rode a bateria sintetica e grave o recibo. Codigo e fontes NAO mudam numa
sincronizacao: mudar codigo ou fonte e implantacao B, com plano, testes e evento proprios. Nunca atualizar so o hash: a mesma versao
com outro hash do um.py e SELO_PROGRAMA_DIVERGE, recusado salvo reparo nomeado em evento. Nada se grava na Bancada sem evento c1
nomeado e verificado pela cadeia de hash do quadro. Custodia de fonte nao e admissao pelo operador. NOT_FALSIFIED nao e creditacao;
nenhum rito move o gate.
