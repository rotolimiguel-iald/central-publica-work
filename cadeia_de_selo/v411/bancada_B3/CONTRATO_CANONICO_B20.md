# Contrato de fidelidade da Bancada Um -- B20 / v411 (sincronizacao)

[REAL] Gerado por sincronizar_bancada.py R3.6 (13/11/2026) em 20261113_035359 UTC, no passo B(20) da cadeia de selo da v411, sob o evento c1 1617.

## Identidade pinada

- um.py v411: sha256 1203b1f9202020d602a7fa8a6bea56d4b48e27ed8baffe98bcbd16e94f97a8e0 (46828680 B), linha de alpha 5584 (unica, coluna 0, sem reatribuicao); beta = alpha*sqrt(e) em runtime = 0.012031300400803142.
- selo: sha256 d52de881621067681843d6a68cf9dc6a5d26e1d0b741666b31df696a4ffafdd3.
- manifesto anterior: B19-v410-20261111-R1 (sha256 1cce1f648ec70229a492a46bfd8ba505c1071671ed2202d7c80a531f91eeafcd).
- recibo pre-selo (testes finais contra a versao anterior): sha256 667d137f341b9e69941b1fc0b007b711ba34f42d154ae235bc6f4c52931abcbc.

## A regra

Uma versao nova do um.py invalida o contrato instalado: o canonical.py recusa toda operacao cientifica (PIN_CHANGED) ate que
o passo B(n) da cadeia regenere o manifesto, re-pine, rode a bateria sintetica e grave o recibo. Codigo e fontes NAO mudam numa
sincronizacao: mudar codigo ou fonte e implantacao B, com plano, testes e evento proprios. Nunca atualizar so o hash: a mesma versao
com outro hash do um.py e SELO_PROGRAMA_DIVERGE, recusado salvo reparo nomeado em evento. Nada se grava na Bancada sem evento c1
nomeado e verificado pela cadeia de hash do quadro. Custodia de fonte nao e admissao pelo operador. NOT_FALSIFIED nao e creditacao;
nenhum rito move o gate.
