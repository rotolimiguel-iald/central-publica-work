# Contrato de fidelidade da Bancada Um -- B11 / v402 (sincronizacao)

[REAL] Gerado por sincronizar_bancada.py R3.5 (19/10/2026) em 20261027_024412 UTC, no passo B(11) da cadeia de selo da v402, sob o evento c1 None.

## Identidade pinada

- um.py v402: sha256 6a5033dc3f29324ce1df7cb82538a28386cae2fd2dce81cd370e442fa29a95c5 (38945032 B), linha de alpha 5584 (unica, coluna 0, sem reatribuicao); beta = alpha*sqrt(e) em runtime = 0.012031300400803142.
- selo: sha256 bd8dab8678e3b64ba385fa4fd541e57ef58fb587417d5115d60fd7f551d7b826.
- manifesto anterior: B10-v401-20261025-R1 (sha256 9d21d7f394953847222e178e46bedc5f5266d3a90d642fbaf21c4440db1a8437).
- recibo pre-selo (testes finais contra a versao anterior): sha256 36aaf247165536ed6de5052641156bfd8dc959b5c8cce3b8feb44184cf3eb423.

## A regra

Uma versao nova do um.py invalida o contrato instalado: o canonical.py recusa toda operacao cientifica (PIN_CHANGED) ate que
o passo B(n) da cadeia regenere o manifesto, re-pine, rode a bateria sintetica e grave o recibo. Codigo e fontes NAO mudam numa
sincronizacao: mudar codigo ou fonte e implantacao B, com plano, testes e evento proprios. Nunca atualizar so o hash: a mesma versao
com outro hash do um.py e SELO_PROGRAMA_DIVERGE, recusado salvo reparo nomeado em evento. Nada se grava na Bancada sem evento c1
nomeado e verificado pela cadeia de hash do quadro. Custodia de fonte nao e admissao pelo operador. NOT_FALSIFIED nao e creditacao;
nenhum rito move o gate.
