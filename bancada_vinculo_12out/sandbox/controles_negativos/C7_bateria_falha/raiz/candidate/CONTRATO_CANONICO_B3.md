# Contrato de fidelidade da Bancada Um -- B3 / v392 (sincronizacao)

[REAL] Gerado por sincronizar_bancada.py em 20261012_200308 UTC, no passo B(3) da cadeia de selo da v392, sob o evento c1 SANDBOX:controle C7.

## Identidade pinada

- um.py v392: sha256 0ea4e10728fde3c32e853305b6245af38188c6a7efc9b3790fd55298efe8a6e3 (33910631 B), linha de alpha 5557 (unica, coluna 0); beta = alpha*sqrt(e) em runtime = 0.012031300400803142.
- selo: sha256 a3e6aee34fbacd71a771701328c3c8dc13d3416ed70f531cb74bce6446389398.
- manifesto anterior: B2-NU3-20261009-R2 (sha256 54fc9e27e4599c49990adb9587a45a8858393f2d8f5d66ec3e022b8140757c1b).

## A regra

Uma versao nova do um.py invalida o contrato instalado: o canonical.py recusa toda operacao cientifica (PIN_CHANGED) ate que
o passo B(n) da cadeia regenere o manifesto, re-pine, rode a bateria sintetica e grave o recibo. Codigo e fontes NAO mudam numa
sincronizacao: mudar codigo ou fonte e implantacao B, com plano, testes e evento proprios. Nunca atualizar so o hash. Nada se grava
na Bancada sem evento c1 nomeado. Custodia de fonte nao e admissao pelo operador. NOT_FALSIFIED nao e creditacao; nenhum rito move o gate.
