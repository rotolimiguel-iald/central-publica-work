# Contrato de fidelidade da Bancada Um -- B14 / v405 (sincronizacao)

[REAL] Gerado por sincronizar_bancada.py R3.5 (19/10/2026) em 20261102_002232 UTC, no passo B(14) da cadeia de selo da v405, sob o evento c1 1416.

## Identidade pinada

- um.py v405: sha256 0030242565cc13f6dbac57a6f1f98fdef69c1b3efe5eb052c359cdb3bf21f053 (40175869 B), linha de alpha 5584 (unica, coluna 0, sem reatribuicao); beta = alpha*sqrt(e) em runtime = 0.012031300400803142.
- selo: sha256 ef4f4621d60413cb5e97c8c2711d407f4c51b29bb62bed4fa5839a798a8c31cc.
- manifesto anterior: B13-v404-20261028-R1 (sha256 cc515b53d666cefd4bf636caa57b163231da5789809ccde38eb16af6f8dcdfac).
- recibo pre-selo (testes finais contra a versao anterior): sha256 c53b38ed940d90ef11b2b7326a0899a01c1b51f2f7e7f26112b33eac22d23746.

## A regra

Uma versao nova do um.py invalida o contrato instalado: o canonical.py recusa toda operacao cientifica (PIN_CHANGED) ate que
o passo B(n) da cadeia regenere o manifesto, re-pine, rode a bateria sintetica e grave o recibo. Codigo e fontes NAO mudam numa
sincronizacao: mudar codigo ou fonte e implantacao B, com plano, testes e evento proprios. Nunca atualizar so o hash: a mesma versao
com outro hash do um.py e SELO_PROGRAMA_DIVERGE, recusado salvo reparo nomeado em evento. Nada se grava na Bancada sem evento c1
nomeado e verificado pela cadeia de hash do quadro. Custodia de fonte nao e admissao pelo operador. NOT_FALSIFIED nao e creditacao;
nenhum rito move o gate.
