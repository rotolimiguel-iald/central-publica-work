# Contrato de fidelidade da Bancada Um -- B5 / v395 (sincronizacao)

[REAL] Gerado por sincronizar_bancada.py R3.5 (19/10/2026) em 20261021_173038 UTC, no passo B(5) da cadeia de selo da v395, sob o evento c1 1099.

## Identidade pinada

- um.py v395: sha256 8918b17803792cf2725e69221718a974a15ebb7e6dc77aac008d609782bdd8fb (38038591 B), linha de alpha 5584 (unica, coluna 0, sem reatribuicao); beta = alpha*sqrt(e) em runtime = 0.012031300400803142.
- selo: sha256 55175f478e93032ce28a6d4265983dcd4fed03f4eab1781bcfa5fbe711e76c30.
- manifesto anterior: B4-v394-20261019-R1 (sha256 eda4b550c1d48be44863028b4b1596f49f575876197a152eb1baf22942bb67d8).
- recibo pre-selo (testes finais contra a versao anterior): sha256 9a467db6d7c50c087b4839301a7f77b4340f49fd3f5b8a652c0ada174d182624.

## A regra

Uma versao nova do um.py invalida o contrato instalado: o canonical.py recusa toda operacao cientifica (PIN_CHANGED) ate que
o passo B(n) da cadeia regenere o manifesto, re-pine, rode a bateria sintetica e grave o recibo. Codigo e fontes NAO mudam numa
sincronizacao: mudar codigo ou fonte e implantacao B, com plano, testes e evento proprios. Nunca atualizar so o hash: a mesma versao
com outro hash do um.py e SELO_PROGRAMA_DIVERGE, recusado salvo reparo nomeado em evento. Nada se grava na Bancada sem evento c1
nomeado e verificado pela cadeia de hash do quadro. Custodia de fonte nao e admissao pelo operador. NOT_FALSIFIED nao e creditacao;
nenhum rito move o gate.
