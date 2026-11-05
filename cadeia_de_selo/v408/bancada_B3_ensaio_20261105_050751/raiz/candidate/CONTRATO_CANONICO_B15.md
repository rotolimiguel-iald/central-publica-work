# Contrato de fidelidade da Bancada Um -- B15 / v406 (sincronizacao)

[REAL] Gerado por sincronizar_bancada.py R3.5 (19/10/2026) em 20261103_015114 UTC, no passo B(15) da cadeia de selo da v406, sob o evento c1 1443.

## Identidade pinada

- um.py v406: sha256 ddcb91930982d6143f47127d43020ab97cb9f5275331f470f2d0e4caaffd1fc0 (42740484 B), linha de alpha 5584 (unica, coluna 0, sem reatribuicao); beta = alpha*sqrt(e) em runtime = 0.012031300400803142.
- selo: sha256 682715ba3f1b11134510b6d244264ffc64e2b54ead60d14057c2efdfd17c8abb.
- manifesto anterior: B14-v405-20261102-R1 (sha256 19738ed92dbc1a3a2948e3de1d11953ebc4630515b8101090d5eabf0d596ced4).
- recibo pre-selo (testes finais contra a versao anterior): sha256 53838534b220f92d2c90485a2da657b36f2628d00c926ec76531f0ea4bdf26e7.

## A regra

Uma versao nova do um.py invalida o contrato instalado: o canonical.py recusa toda operacao cientifica (PIN_CHANGED) ate que
o passo B(n) da cadeia regenere o manifesto, re-pine, rode a bateria sintetica e grave o recibo. Codigo e fontes NAO mudam numa
sincronizacao: mudar codigo ou fonte e implantacao B, com plano, testes e evento proprios. Nunca atualizar so o hash: a mesma versao
com outro hash do um.py e SELO_PROGRAMA_DIVERGE, recusado salvo reparo nomeado em evento. Nada se grava na Bancada sem evento c1
nomeado e verificado pela cadeia de hash do quadro. Custodia de fonte nao e admissao pelo operador. NOT_FALSIFIED nao e creditacao;
nenhum rito move o gate.
