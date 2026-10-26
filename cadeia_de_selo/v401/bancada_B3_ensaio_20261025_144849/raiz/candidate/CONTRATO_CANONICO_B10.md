# Contrato de fidelidade da Bancada Um -- B10 / v401 (sincronizacao)

[REAL] Gerado por sincronizar_bancada.py R3.5 (19/10/2026) em 20261025_144849 UTC, no passo B(10) da cadeia de selo da v401, sob o evento c1 None.

## Identidade pinada

- um.py v401: sha256 1925cb691e933ae811933a6286b4acb9c25853ba2d89f926a6610d2d837eba01 (38688534 B), linha de alpha 5584 (unica, coluna 0, sem reatribuicao); beta = alpha*sqrt(e) em runtime = 0.012031300400803142.
- selo: sha256 60b369a56ac772935b73c12e2a0b246af1ae758138dd4126ac1e7a881150bf8a.
- manifesto anterior: B9-v400-20261024-R1 (sha256 9e0edf2dfbb868a2c5a0928c65c748b520965d83f2a32e9913964c1a0c5066d5).
- recibo pre-selo (testes finais contra a versao anterior): sha256 f1011f5c47a174181a533f1d5b2e25158a3a1dc650ec7de94109aea1a9a42f71.

## A regra

Uma versao nova do um.py invalida o contrato instalado: o canonical.py recusa toda operacao cientifica (PIN_CHANGED) ate que
o passo B(n) da cadeia regenere o manifesto, re-pine, rode a bateria sintetica e grave o recibo. Codigo e fontes NAO mudam numa
sincronizacao: mudar codigo ou fonte e implantacao B, com plano, testes e evento proprios. Nunca atualizar so o hash: a mesma versao
com outro hash do um.py e SELO_PROGRAMA_DIVERGE, recusado salvo reparo nomeado em evento. Nada se grava na Bancada sem evento c1
nomeado e verificado pela cadeia de hash do quadro. Custodia de fonte nao e admissao pelo operador. NOT_FALSIFIED nao e creditacao;
nenhum rito move o gate.
