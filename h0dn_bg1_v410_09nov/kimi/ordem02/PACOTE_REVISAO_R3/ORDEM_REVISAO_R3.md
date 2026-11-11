# PACOTE DE REVISÃO INDEPENDENTE R3 — A1 e certificado bloqueado

**Estado:** `A1_ALGEBRA_CLOSED__FULL_PHYSICAL_COVARIANCE_OPEN__POWER_NOT_EVALUABLE`

## O revisor deve confirmar

1. As 111 linhas R22 formam 37 tripletes de uma mesma medida; não existem 111 erros independentes a recuperar.
2. A decomposição `diag(sigma_independent^2)+F_HMS_effective F_HMS_effective^T+F_MAS F_MAS^T+F_anchor F_anchor^T` reproduz o bloco publicado sem duplicação.
3. As 72 restrições explícitas têm posto 72, anulam C e A e correspondem às 72 equações redundantes do H0DN público.
4. A matriz permanece PSD, com posto 183 no suporte; somente vetores sintéticos determinísticos foram ajustados e uma direção nula sintética foi rejeitada.
5. A2–A6 continuam sem admissão física completa. Nenhuma variante tem D, poder ou semente R3; o certificado é de recusa de admissão, não `UNDERPOWERED`.
6. Nenhuma projeção de y, jitter, diagonal HMS completa, abertura observada ou teste de suporte observado foi feito nesta ordem.

## Futura única rota observada por variante admitida

Validar estrutura e hashes; montar y bruto; conferir as 72 identidades com tolerância pré-fixada; falhar sem reparo se houver violação; só então reduzir por QR ou usar pseudoinversa. Nunca projetar y para passar. A causa numérica da violação histórica não foi reexaminada.

## O que falta para poder real

Produtos internos/agregados G42, decomposição PV, covariâncias/cruzamentos dos 13 ou poda cega após admissão, covariância local–BG1 e revisão independente. Só então registrar sementes novas e executar D, orçamento de variância e Monte Carlo cruzado.
