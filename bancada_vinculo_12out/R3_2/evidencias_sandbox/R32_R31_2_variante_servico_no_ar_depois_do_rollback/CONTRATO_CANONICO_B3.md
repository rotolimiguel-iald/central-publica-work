# Contrato de fidelidade da Bancada Um -- B3 / v392 (sincronizacao)

[REAL] Gerado por sincronizar_bancada.py R3.2 (13/10/2026) em 20261013_092827 UTC, no passo B(3) da cadeia de selo da v392, sob o evento c1 741.

## Identidade pinada

- um.py v392: sha256 0ea4e10728fde3c32e853305b6245af38188c6a7efc9b3790fd55298efe8a6e3 (33910631 B), linha de alpha 5557 (unica, coluna 0, sem reatribuicao); beta = alpha*sqrt(e) em runtime = 0.012031300400803142.
- selo: sha256 fa361d8a2edf58bc04e13eec1104217a1622093e68e13f63226293f9ac49f643.
- manifesto anterior: B2-NU3-20261009-R2 (sha256 c7aa0d1c7df2cd6214335ffb2cec129a62edd07a42c939b00e1004372f0aca7e).
- recibo pre-selo (testes finais contra a versao anterior): sha256 40b71cac301bdbf2e91c0f431bbb75eb8b5840d8b29702bef58b74aa5262be52.

## A regra

Uma versao nova do um.py invalida o contrato instalado: o canonical.py recusa toda operacao cientifica (PIN_CHANGED) ate que
o passo B(n) da cadeia regenere o manifesto, re-pine, rode a bateria sintetica e grave o recibo. Codigo e fontes NAO mudam numa
sincronizacao: mudar codigo ou fonte e implantacao B, com plano, testes e evento proprios. Nunca atualizar so o hash: a mesma versao
com outro hash do um.py e SELO_PROGRAMA_DIVERGE, recusado salvo reparo nomeado em evento. Nada se grava na Bancada sem evento c1
nomeado e verificado pela cadeia de hash do quadro. Custodia de fonte nao e admissao pelo operador. NOT_FALSIFIED nao e creditacao;
nenhum rito move o gate.
