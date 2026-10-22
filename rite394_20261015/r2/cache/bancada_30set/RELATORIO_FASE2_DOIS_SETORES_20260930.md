# Fase 2 (30/09/2026) — dois setores de H₀ na verossimilhança: a lei D1a contra a escada, o fundo e as SNe

**Protocolo** `FASE2_DOIS_SETORES_20260930` · pré-registro sha256 `1f103573f28bc0f31dafa5a20dd7a463b2f8c616d8fd986c19568904932f0aa1` · resultado sha256 `80735aa770c8c7c5711eeca71beb3aa324bb0d75f5f2b8f74273f0bf4cf67109` · rodada 2026-09-30 09:38:45 → 2026-09-30 09:50:52 (728 s)

**β_TGL em runtime** = α_CODATA2018·√e = 0.012031300400803 (nunca literal). **Modelo:** conjunto `sh0es_local`: χ² = ((H₀·(1+z*)^β − 73,04)/1,04)², z* = 1089.95 [INPUT]; a lei D1a é [CONJECTURE]; em β = 0 devolve o ΛCDM com SH0ES direto. Motor: Bancada Um (GPU), modo `tgl` (corrigido + mapa de R efetivo); controle `nu`.

## VEREDITO

`TGL_FASE2_TWO_SECTORS__LADDER_TENSION_1_TO_3_SIGMA__BETA_PROFILE_Z_2P02__BAYES_STRONG_FOR_TGL__CONTROL_NU_PULL_1P81__NOT_A_CONFIRMATION`

**Estatuto:** `[REAL — medido nesta rodada]`; NOT_FALSIFIED ≠ CONFIRMED; nada aqui confirma; a RG é o limite clássico.

**Regra de leitura pré-registrada:** o veredito base vem da família F no modo tgl pelo PULL da escada no melhor ajuste TGL: |pull| < 1 reconciliada; 1–3 tensão; > 3 tensão forte (a lei D1a falsificada nesta combinação); sufixos: BETA_PROFILE_Z (z de α√e contra β livre em F), BAYES (ln B TGL/ΛCDM em F), CONTROL_NU_PULL (o mesmo pull no mapa nu, ao lado, nunca somado). Nada aqui confirma: NOT_FALSIFIED ≠ CONFIRMED; a RG é o limite clássico.

## Tabela 1 — χ², perfil de β, o pull da escada em cada melhor ajuste, evidência

| família | mapa | n | χ² ΛCDM / TGL / livre | Δχ² T−L | z perfil (α√e) | β̂ livre ± σ | pull escada ΛCDM / **TGL** / livre | H₀ → H₀_local (TGL) | ln B TGL/ΛCDM | ln B livre/ΛCDM | ln B TGL/livre | perto do limite |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| F_dr2_local | **tgl (eff)** | 17 | 31.627 / 18.126 / 14.038 | -13.501 | **2.02** | +0.00822 ± 0.0019 | -4.00 / **+1.95** / +0.03 | 69.01 → 75.07 | +6.76 (forte) | +5.79 | +0.97 (SD +1.29) | — |
| F_dr2_local | controle nu | 17 | 31.627 / 29.101 / 20.366 | -2.526 | **2.96** | +0.00650 ± 0.0019 | -4.00 / **+1.81** / -0.90 | 68.88 → 74.93 | +1.28 (fraco) | +2.57 | -1.29 (SD +0.49) | — |
| G_dr2_local_pantheon | **tgl (eff)** | 1597 | 1421.887 / 1407.606 / 1403.789 | -14.280 | **1.95** | +0.00834 ± 0.0019 | -4.11 / **+1.85** / -0.02 | 68.91 → 74.96 | +7.15 (forte) | +6.05 | +1.10 (SD +1.35) | — |
| G_dr2_local_pantheon | controle nu | 1597 | 1421.887 / 1417.888 / 1409.811 | -3.999 | **2.84** | +0.00672 ± 0.0019 | -4.11 / **+1.72** / -0.90 | 68.79 → 74.83 | +2.02 (fraco) | +2.98 | -0.96 (SD +0.61) | — |
| H_dr1_local | **tgl (eff)** | 16 | 34.172 / 18.969 / 15.998 | -15.203 | **1.72** | +0.00865 ± 0.0020 | -3.92 / **+1.60** / +0.03 | 68.68 → 74.71 | +7.61 (forte) | +6.11 | +1.50 (SD +1.56) | — |
| H_dr1_local | controle nu | 16 | 34.172 / 26.314 / 21.580 | -7.858 | **2.18** | +0.00754 ± 0.0021 | -3.92 / **+1.19** / -0.74 | 68.28 → 74.28 | +3.95 (moderado) | +3.37 | +0.58 (SD +1.08) | — |

Δχ² T−L = χ²(TGL) − χ²(ΛCDM), mesmo número de parâmetros; pull = (H₀_local(θ̂) − 73,04)/1,04 no melhor ajuste de cada modelo; z perfil = √max(χ²(TGL) − χ²(livre), 0). ln Z por quadratura em grade (n = 25; erro por n = 35), priors uniformes nos limites do pipeline; SD = Savage–Dickey.

## Tabela 2 — posteriores (modo tgl; ensemble na GPU, 256 × 3000, queima 600, semente 42)

| família | β mediana [16, 84] | H₀ mediana | fração ≥ α√e | fração ≥ 0 | z pela cauda | τ máx |
|---|---|---|---|---|---|---|
| F_dr2_local | +0.00817 [+0.00626, +0.01007] | 68.98 | 0.021 | 1.000 | 2.04 | 41 |
| G_dr2_local_pantheon | +0.00832 [+0.00641, +0.01021] | 68.88 | 0.025 | 1.000 | 1.96 | 40 |

## Leitura da gerência (condicionada às bandeiras calculadas pelo script)

1. **Veredito pré-registrado (família F, modo tgl):** `TGL_FASE2_TWO_SECTORS__LADDER_TENSION_1_TO_3_SIGMA__BETA_PROFILE_Z_2P02__BAYES_STRONG_FOR_TGL__CONTROL_NU_PULL_1P81__NOT_A_CONFIRMATION`. No melhor ajuste TGL (β = α√e, zero parâmetro livre) a escada fica a **+1.95σ** (H₀ de fundo 69.01 → H₀_local 75.07 contra 73.04 ± 1.04); no melhor ajuste ΛCDM (β = 0) a mesma escada fica a -4.00σ — é a tensão de Hubble desta combinação, que a TGL absorve pela lei D1a sem parâmetro novo.
2. **Parcimônia (a resposta ao item 1 de 30/09 — o «sigma» do exame conjunto é um fator de Bayes):** ln B(TGL/ΛCDM) = +6.76 (forte (|ln B| ≥ 5)); ln B(livre/ΛCDM) = +5.79; ln B(TGL/livre) = +0.97 (Savage–Dickey 1.29). Δχ²(TGL − ΛCDM) = -13.501 com o MESMO número de parâmetros.
3. **β livre agora é MEDIDO pela escada:** β̂ = +0.00822 ± 0.00191; α√e = 0.01203 fica a **2.02σ** (perfil). A escada constrange β com σ_β ≈ σ_H₀/(H₀·ln(1+z*)); o número que sai é o que a lei D1a prediz — e a circularidade da FORMA da lei está declarada no pré-registro (§ abaixo).
4. **Controle nu (o mapa do D1 V3):** pull da escada no TGL +1.81σ; β̂ = +0.00650 ± 0.00189; z de perfil 2.96; ln B(TGL/ΛCDM) = +1.28 (fraco (1 ≤ |ln B| < 2,5)). Ao lado, nunca somado.
5. **G (+ Pantheon+, cov completa, M profilado):** pull TGL +1.85σ; z de perfil 1.95; ln B(TGL/ΛCDM) = +7.15 (forte (|ln B| ≥ 5)); ln B(TGL/livre) = +1.10. As SNe medem a forma de D_L(z) sob o fundo TGL; não medem H₀ (M profilado).
6. **H (replicação com o BAO DR1 selado):** pull TGL +1.60σ; z de perfil 1.72; ln B(TGL/ΛCDM) = +7.61 (forte (|ln B| ≥ 5)).
7. **Posterior de F (modo tgl):** β mediana +0.00817 [+0.00626, +0.01007]; fração acima de α√e 0.021; z pela cauda 2.04; τ máx 41.

## Circularidade declarada (do pré-registro, verbatim)

a FORMA da lei D1a, H0_local/H0_CMB = (1+z*)^β, foi cunhada no pipeline de Coma já conhecendo a razão SH0ES/Planck (73,04/67,4 ≈ 1,084) e o valor (1+z*)^{α√e} ≈ 1,088; logo esta Fase NÃO testa a descoberta da lei — testa (i) a consistência conjunta sob o fundo TGL com o mapa efetivo e o BAO DR2 (o H0 de fundo é ajustado, não fixado em 67,4), (ii) a parcimônia: fator de Bayes de um modelo SEM parâmetro livre contra ΛCDM e contra β livre, (iii) a replicação com DR1. Um teste independente da lei precisa de uma predição em outro lugar (a dependência em z do H0 da escada; a calibração M das SNe; o D1 com o espectro completo) — fica dito, não feito aqui

**Visto antes de pré-registrar:** as linhas de χ²/evidência da tentativa 1 da Fase 1 (todas as famílias, os dois mapas, inclusive a família C com SH0ES direto: β livre no limite do prior, z 3,27σ, ln B TGL/ΛCDM +2,59); NÃO vistos: a linha D1a da Fase 1, os posteriores, o veredito da Fase 1 (o JSON não existia ao pré-registrar: True)

## Estatuto, multiplicidade e pendências

- **Cego/não-cego:** F_dr2_local: cego até esta rodada; G_dr2_local_pantheon: cego até esta rodada; H_dr1_local: cego até esta rodada.
- **Multiplicidade (livro da Bancada, Šidák), família F modo tgl:** `{"p_local": 0.04318060305029038, "z_local": 2.021958851368388, "n_familias": 21, "p_global": 0.6042422860565669, "z_global": 0.5183095855663662, "metodo": "Šidák sobre as famílias de teste do livro"}`.
- **O que este resultado NÃO diz:** não confirma β nem a lei D1a; a forma da lei foi cunhada conhecendo a razão SH0ES/Planck; não move o gate matemático. O que diz: com a lei D1a e β = α√e fixo, o fundo (DR2) e a escada são ou não compatíveis (o pull), e com que fator de Bayes contra ΛCDM.

## Próximo passo (a pré-registrar antes de abrir número)

- **Teste independente da lei D1a:** a dependência em z do H₀ da escada (Pantheon+SH0ES com calibradores, por bins de z); a calibração M das SNe sob os dois setores; o D1 com o espectro completo do CMB (quebra a degenerescência de β no fundo — Fase 3).
- **v377:** este resultado + a errata ao lado do D1 V3 (mapa nu) + a leitura de dois setores, no `um.py`, depois do aferidor.

---
*Gerado por `relatorio_fase2.py` em 2026-09-30 09:51:02 a partir de `RESULTADO_FASE2_DOIS_SETORES_20260930.json` (sha256 `80735aa770c8c7c5711eeca71beb3aa324bb0d75f5f2b8f74273f0bf4cf67109`). Números lidos do JSON; nenhum digitado.*
