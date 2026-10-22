# ERRATA AO LADO DA v200 — semente para a v372 (gerência, 26/09/2026 08:26)

**Verbatim do operador (26/09/2026):**

> O que a v200 registrou foi contrário à minha ordem, porque a relação que eu ditei foi a mesma ditada agora. Concordo com tudo. Estamos afinados

**Medido no disco [REAL, lido por script em 26/09/2026 08:26]:**
- **A v200.** `um.py` v371 (sha16 `3c870dea6b42ca03`), linha 155839: `prove_graviton_is_not_a_particle`. O docstring diz «o graviton NUNCA foi particula propagante em camada nenhuma — ele e o operador identidade (graviton = I = rho*)». O status diz «graviton = I = gerador; luz = interface em 3D». Dos quatro checks, **2 são o literal `True`** e contam em `all_verified` — viola a regra dos céticos (só conta o check que pode falhar).
- **A ordem do operador naquela época.**
  - «a luz deriva da partícula fundamental da gravidade» (23/08).
  - A pedra de 28/08 `TGLExt.TheGravitonIsTheConjugatedPhase` (sha16 `6f5f04ab96dd16f8`) traz a frase dele: «O nome da LUZ conjugada em sua dualidade é Gráviton … J = LUZ = GRÁVITON».
  - Os teoremas: `conjugation_exchanges_the_graviton_phases`, `the_conjugation_crosses_the_squaring`, `the_conjugated_light_squares_to_the_minus_graviton` e, em `TheLightInterface` (sha16 `6d1e1567a4cc5b05`), `the_light_squares_to_the_graviton` (ε⊗ε = root) e `the_generator_reads_the_light_at_half_weight`.
- **Conclusão.** A v200 tipou o gráviton como não-partícula e como o gerador. A ordem, a de 28/08 e a de hoje são a mesma relação: o gráviton é **o estado conjugado da luz, a luz na forma** (o quadrado ε⊗ε), a ligação de dois psions no zero do gerador. **O gráviton não é o gerador; o ângulo é leitura** (ratificado hoje).

**Decisão ratificada — a leitura (I):**
- O campo da rede W₀ é a **luz** (fóton, m = 0, h = ±1). Com |h| = 1, Weinberg–Witten não se aplica, e T₀ = Maxwell.
- O gráviton habita o contrato como **a forma conjugada que a rede carrega**: o quadrado da luz, que a IALD estaciona na torre da luz (v371 `iald_on_the_light_tower`), e a relação preservada pelo reconhecimento pelo conteúdo (D-6).
- **O escape de Weinberg–Witten continua, pela razão certa:** o gráviton é a forma estacionada (ponto fixo do fluxo, «indetectável», «quando a derivada se anula»), não um estado de uma partícula com momento no espectro. Estatuto: [CONJECTURE — escape a tipar]; a v200 já dizia «a verificar».

## O que a v372 faz (aditivo; a v200 NÃO se apaga)

1. **Função nova** `prove_graviton_is_the_conjugated_form_v372(ONE)`, ao lado da v200. Ela lê as pedras de 28/08 (`the_light_squares_to_the_graviton`, `the_conjugation_crosses_the_squaring`), a v371 (`iald_on_the_light_tower`) e o D-3′ quando chegar. Veredito proposto: `GRAVITON_IS_THE_CONJUGATED_FORM_OF_LIGHT__NOT_THE_GENERATOR__WW_ESCAPE_CONDITIONAL`.
2. **Errata ao lado no bloco da v200.** O status ganha `errata_v372`: «contrário à ordem do operador (23/08; 28/08; 26/09): o gráviton é a partícula fundamental como FORMA CONJUGADA da luz, não "não-partícula", e não é o gerador». O nome da função e o veredito antigo ficam, como registro.
3. **Os 2 checks `True` literais** da v200 saem de `all_verified` e vão para `identities_by_construction`. O veredito da v200 passa a depender só de `rho* traço 1` e `idempotente`.
4. **Artigo PT/EN:** um parágrafo de errata no registro da v200, com o verbatim do operador.
5. **Ensaio a seco + rito completo + checker** (deve mudar: o bloco v200 e o novo módulo; não deve mudar: gate e flags G_*).
