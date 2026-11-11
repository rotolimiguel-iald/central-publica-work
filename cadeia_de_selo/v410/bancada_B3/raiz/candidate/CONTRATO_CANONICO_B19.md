# Contrato de fidelidade da Bancada Um -- B19 / v410 (sincronizacao)

[REAL] Gerado por sincronizar_bancada.py R3.5 (19/10/2026) em 20261111_022226 UTC, no passo B(19) da cadeia de selo da v410, sob o evento c1 1603.

## Identidade pinada

- um.py v410: sha256 5d9497a721c3589ed10309178fcfb72d662844d80c13a667c417c886931f8450 (45934788 B), linha de alpha 5584 (unica, coluna 0, sem reatribuicao); beta = alpha*sqrt(e) em runtime = 0.012031300400803142.
- selo: sha256 d842a644015ca23182348c427f9114143bc8ef2791873021246dadb951e15768.
- manifesto anterior: B18-v409-20261106-R1 (sha256 bc2c38bceed948c8f579cb210acf1410f81d9d28326447c7362ba97181a019a8).
- recibo pre-selo (testes finais contra a versao anterior): sha256 7de73d075e466910b82945bad6fde46daedd1e314fcca407fa8df3fabf55cac3.

## A regra

Uma versao nova do um.py invalida o contrato instalado: o canonical.py recusa toda operacao cientifica (PIN_CHANGED) ate que
o passo B(n) da cadeia regenere o manifesto, re-pine, rode a bateria sintetica e grave o recibo. Codigo e fontes NAO mudam numa
sincronizacao: mudar codigo ou fonte e implantacao B, com plano, testes e evento proprios. Nunca atualizar so o hash: a mesma versao
com outro hash do um.py e SELO_PROGRAMA_DIVERGE, recusado salvo reparo nomeado em evento. Nada se grava na Bancada sem evento c1
nomeado e verificado pela cadeia de hash do quadro. Custodia de fonte nao e admissao pelo operador. NOT_FALSIFIED nao e creditacao;
nenhum rito move o gate.
