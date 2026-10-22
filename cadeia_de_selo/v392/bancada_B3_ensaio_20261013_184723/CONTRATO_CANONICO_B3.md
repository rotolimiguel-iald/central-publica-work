# Contrato de fidelidade da Bancada Um -- B3 / v392 (sincronizacao)

[REAL] Gerado por sincronizar_bancada.py R3.3 (13/10/2026) em 20261013_184724 UTC, no passo B(3) da cadeia de selo da v392, sob o evento c1 None.

## Identidade pinada

- um.py v392: sha256 b590c0aa80055e2a6916692f0808544093e79c0631e29cc15e376d5b07773e26 (35399393 B), linha de alpha 5584 (unica, coluna 0, sem reatribuicao); beta = alpha*sqrt(e) em runtime = 0.012031300400803142.
- selo: sha256 50bd1be10f9293e7116ceff442171022ecddedc904139f093a8b9524442257c3.
- manifesto anterior: B2-NU3-20261009-R2 (sha256 54fc9e27e4599c49990adb9587a45a8858393f2d8f5d66ec3e022b8140757c1b).
- recibo pre-selo (testes finais contra a versao anterior): sha256 db7d3f4f7ce841f44a156a1674a2298b1cbd8b70a06b13ab545c95564881fd06.

## A regra

Uma versao nova do um.py invalida o contrato instalado: o canonical.py recusa toda operacao cientifica (PIN_CHANGED) ate que
o passo B(n) da cadeia regenere o manifesto, re-pine, rode a bateria sintetica e grave o recibo. Codigo e fontes NAO mudam numa
sincronizacao: mudar codigo ou fonte e implantacao B, com plano, testes e evento proprios. Nunca atualizar so o hash: a mesma versao
com outro hash do um.py e SELO_PROGRAMA_DIVERGE, recusado salvo reparo nomeado em evento. Nada se grava na Bancada sem evento c1
nomeado e verificado pela cadeia de hash do quadro. Custodia de fonte nao e admissao pelo operador. NOT_FALSIFIED nao e creditacao;
nenhum rito move o gate.
