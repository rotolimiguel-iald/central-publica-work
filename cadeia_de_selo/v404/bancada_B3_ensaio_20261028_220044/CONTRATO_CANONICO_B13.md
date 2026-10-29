# Contrato de fidelidade da Bancada Um -- B13 / v404 (sincronizacao)

[REAL] Gerado por sincronizar_bancada.py R3.5 (19/10/2026) em 20261028_220044 UTC, no passo B(13) da cadeia de selo da v404, sob o evento c1 None.

## Identidade pinada

- um.py v404: sha256 3820476c83267f614fee8f8df13bedcc814998015ddf3b95c8252f5cf6043395 (39313509 B), linha de alpha 5584 (unica, coluna 0, sem reatribuicao); beta = alpha*sqrt(e) em runtime = 0.012031300400803142.
- selo: sha256 cb22ab23063eb22b1d26ef266b40d220828fd1b59e9663608fb3e02c10fefef9.
- manifesto anterior: B12-v403-20261028-R1 (sha256 7140a26bf678d3d52a145d8ac081347ad080c257b0c8f6861a42ce3c508290d3).
- recibo pre-selo (testes finais contra a versao anterior): sha256 20573c330654c130e27f78cfa1f426386ccfbe5f8b0f889575d7a4327b326a8e.

## A regra

Uma versao nova do um.py invalida o contrato instalado: o canonical.py recusa toda operacao cientifica (PIN_CHANGED) ate que
o passo B(n) da cadeia regenere o manifesto, re-pine, rode a bateria sintetica e grave o recibo. Codigo e fontes NAO mudam numa
sincronizacao: mudar codigo ou fonte e implantacao B, com plano, testes e evento proprios. Nunca atualizar so o hash: a mesma versao
com outro hash do um.py e SELO_PROGRAMA_DIVERGE, recusado salvo reparo nomeado em evento. Nada se grava na Bancada sem evento c1
nomeado e verificado pela cadeia de hash do quadro. Custodia de fonte nao e admissao pelo operador. NOT_FALSIFIED nao e creditacao;
nenhum rito move o gate.
