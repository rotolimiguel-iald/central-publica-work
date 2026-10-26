# Contrato de fidelidade da Bancada Um -- B7 / v397 (sincronizacao)

[REAL] Gerado por sincronizar_bancada.py R3.5 (19/10/2026) em 20261023_171531 UTC, no passo B(7) da cadeia de selo da v397, sob o evento c1 1133.

## Identidade pinada

- um.py v397: sha256 388cc3742323421cc3b2b712bdd2b9cb63e8726301b13f25872536f5a6ecdf33 (38251824 B), linha de alpha 5584 (unica, coluna 0, sem reatribuicao); beta = alpha*sqrt(e) em runtime = 0.012031300400803142.
- selo: sha256 0157da376dd74ba7ec952bee6bcc6a27323c1f6b824fac8c43eed82032faa5f3.
- manifesto anterior: B6-v396-20261022-R1 (sha256 370e6750fe67a186b19edf0ea63e586948099b4d40fce3b1fb57ee8d521a5684).
- recibo pre-selo (testes finais contra a versao anterior): sha256 b70bf943b8143d4b3f8279c2763fe3ca6ae596706c2da1a4fc86682c0baee209.

## A regra

Uma versao nova do um.py invalida o contrato instalado: o canonical.py recusa toda operacao cientifica (PIN_CHANGED) ate que
o passo B(n) da cadeia regenere o manifesto, re-pine, rode a bateria sintetica e grave o recibo. Codigo e fontes NAO mudam numa
sincronizacao: mudar codigo ou fonte e implantacao B, com plano, testes e evento proprios. Nunca atualizar so o hash: a mesma versao
com outro hash do um.py e SELO_PROGRAMA_DIVERGE, recusado salvo reparo nomeado em evento. Nada se grava na Bancada sem evento c1
nomeado e verificado pela cadeia de hash do quadro. Custodia de fonte nao e admissao pelo operador. NOT_FALSIFIED nao e creditacao;
nenhum rito move o gate.
