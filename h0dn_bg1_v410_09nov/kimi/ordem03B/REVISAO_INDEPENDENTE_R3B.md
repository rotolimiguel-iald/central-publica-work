# Revisão independente do estudo R3B

**Estado:** `CONDICIONAL_APTO__ERRATA_S4_APLICADA__NAO_E_CERTIFICADO`

A auditoria matemática independente verificou a âncora, o mapa S0–S5, a substituição G42, CAP13, a rejeição não PSD de S3, a minimização global de S4, os orçamentos, a família sigma_b, S_E, o lema e a saída global por limiar.

Foi encontrada apenas uma transposição textual na definição de S4. A restrição correta é `q C_BG^-1 q^T <= C_L`; o cálculo numérico já usava essa orientação no resíduo de Schur. A descrição foi corrigida em `core_r3b.py`, o estudo foi regenerado e a validação voltou a passar sem alteração de D. A errata está preservada em `ERRATA_S4_Q_TRANSPOSE_R3B.md`.

Após a correção, o revisor não identificou impedimento matemático ao estudo **como condicional**. Não há prova física completa de Loewner nem certificado de poder, e `opening_allowed=false` permanece.
