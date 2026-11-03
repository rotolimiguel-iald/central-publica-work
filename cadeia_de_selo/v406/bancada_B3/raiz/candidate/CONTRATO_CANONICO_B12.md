# Contrato de fidelidade da Bancada Um -- B12 / v403 (sincronizacao)

[REAL] Gerado por sincronizar_bancada.py R3.5 (19/10/2026) em 20261028_094742 UTC, no passo B(12) da cadeia de selo da v403, sob o evento c1 1305.

## Identidade pinada

- um.py v403: sha256 2ffe9edc7d7545bd0cfa0572dae97d371acea37991172b884a5b461a233cdcb7 (39135553 B), linha de alpha 5584 (unica, coluna 0, sem reatribuicao); beta = alpha*sqrt(e) em runtime = 0.012031300400803142.
- selo: sha256 eb79f2592fa22873646bd732b9b2108e1c937033f4861bd94474425076d6e88c.
- manifesto anterior: B11-v402-20261027-R1 (sha256 ed55cc885e68e046b42e1e23d7a459b88d8f5c82b919551ef4ed8ea08f9a8564).
- recibo pre-selo (testes finais contra a versao anterior): sha256 d573c0b81919b0580fada2d9b2726844392681eebc365ae6497081f634d9899a.

## A regra

Uma versao nova do um.py invalida o contrato instalado: o canonical.py recusa toda operacao cientifica (PIN_CHANGED) ate que
o passo B(n) da cadeia regenere o manifesto, re-pine, rode a bateria sintetica e grave o recibo. Codigo e fontes NAO mudam numa
sincronizacao: mudar codigo ou fonte e implantacao B, com plano, testes e evento proprios. Nunca atualizar so o hash: a mesma versao
com outro hash do um.py e SELO_PROGRAMA_DIVERGE, recusado salvo reparo nomeado em evento. Nada se grava na Bancada sem evento c1
nomeado e verificado pela cadeia de hash do quadro. Custodia de fonte nao e admissao pelo operador. NOT_FALSIFIED nao e creditacao;
nenhum rito move o gate.
