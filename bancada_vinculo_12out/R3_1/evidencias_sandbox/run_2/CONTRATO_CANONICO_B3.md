# Contrato de fidelidade da Bancada Um -- B3 / v392 (sincronizacao)

[REAL] Gerado por sincronizar_bancada.py R3.1 (13/10/2026) em 20261013_082250 UTC, no passo B(3) da cadeia de selo da v392, sob o evento c1 721.

## Identidade pinada

- um.py v392: sha256 0ea4e10728fde3c32e853305b6245af38188c6a7efc9b3790fd55298efe8a6e3 (33910631 B), linha de alpha 5557 (unica, coluna 0, sem reatribuicao); beta = alpha*sqrt(e) em runtime = 0.012031300400803142.
- selo: sha256 62ab33ebbe8c5839a5ddd3fa19948a6dff9b1611003e1733645cebf9e8242fb0.
- manifesto anterior: B2-NU3-20261009-R2 (sha256 ea14ba6af36cf5c5d76fb0e7d7ee6345f698808ad980328b3a7976e060a7893d).
- recibo pre-selo (testes finais contra a versao anterior): sha256 f26005e2b034e24674f06997c6da62325914163c67c03d08821caf5271bdf073.

## A regra

Uma versao nova do um.py invalida o contrato instalado: o canonical.py recusa toda operacao cientifica (PIN_CHANGED) ate que
o passo B(n) da cadeia regenere o manifesto, re-pine, rode a bateria sintetica e grave o recibo. Codigo e fontes NAO mudam numa
sincronizacao: mudar codigo ou fonte e implantacao B, com plano, testes e evento proprios. Nunca atualizar so o hash: a mesma versao
com outro hash do um.py e SELO_PROGRAMA_DIVERGE, recusado salvo reparo nomeado em evento. Nada se grava na Bancada sem evento c1
nomeado e verificado pela cadeia de hash do quadro. Custodia de fonte nao e admissao pelo operador. NOT_FALSIFIED nao e creditacao;
nenhum rito move o gate.
