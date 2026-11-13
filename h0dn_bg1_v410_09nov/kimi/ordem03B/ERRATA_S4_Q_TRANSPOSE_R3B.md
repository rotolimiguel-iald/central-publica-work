# ERRATA PONTUAL R3B — orientação de S4

**Arquivo anterior:** `core_r3b.py`, SHA-256 `a04eb3fc806bfe50d3deb1e65a2663e2c3f158a7881f255dd1a0ebde1eeed54c`.

A descrição de S4 trazia `q^T C_BG^-1 q <= C_L`, dimensionalmente incorreto para o `q` utilizado, de forma `n×3`. A forma correta é:

\[
q C_{BG}^{-1} q^T \preceq C_L.
\]

O código numérico já calculava o resíduo de Schur como `C_local - q @ cb_inv @ q.T`, com a orientação correta. A errata altera somente a descrição textual; nenhum D, poder, raiz, orçamento ou saída global muda.

A revisão independente confirmou que, após esta correção formal, o estudo permanece matematicamente apto como `ESTUDO_DE_DESENHO_CONDICIONAL__NAO_E_CERTIFICADO`. Nenhum observado, semente ou alteração de `FREEZE_R2`/v410 foi usado.
