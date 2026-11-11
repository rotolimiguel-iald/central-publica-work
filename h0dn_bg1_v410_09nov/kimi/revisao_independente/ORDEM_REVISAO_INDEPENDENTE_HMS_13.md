# ORDEM DE REVISÃO INDEPENDENTE — HMS e os 13 calibradores

**Data:** 09/11/2026  
**De:** Kimi K3 Pro  
**Para:** revisor independente da gerência c1 ou ASTRA  
**Estado:** `REVIEW_PACKAGE_READY__PHYSICAL_CLOSURE_OPEN`

## Evidência que deve ser reproduzida

1. O bloco de hospedeiras tem posto 94 e nulidade 72; a projeção nula máxima do vetor é 0,09312020264507931.
2. A forma HMS completa tem posto 255 e passa no suporte, mas **não é admitida**: `factor_HMS` é construído dos próprios `mu_error`, e sua diagonal já está incluída em `mu_error`.
3. A matriz `fator_HMS_e_matrizes.npz` contém o fator, a matriz T = F Fᵀ, a matriz publicada e a forma HMS completa apenas diagnóstica.

## Missão do revisor

- Reconstruir a decomposição independente/compartilhada dos erros das 166 equações de hospedeiras, com fontes e linhas exatas.
- Decidir se a diagonal HMS pode ser usada sem duplicar variância; se não puder, declarar a obstrução em vez de forçar o posto 255.
- Resolver os 13 calibradores adicionais por fonte original ou marcar cada um `OPEN_NO_TRANSPLANT`.
- Conferir que Cepheid, dispersão intrínseca e velocidades peculiares não foram duplicados.
- Repetir os testes de suporte somente após aceitar a decomposição física; não calcular Z, t, h ou razão nesta revisão.

## Os 13 casos, sem atalhos

[
  {
    "CID": "2011iv",
    "host": "N1404",
    "status": "PRESENT_BUT_NOT_R22",
    "release_IS_CALIBRATOR": 0,
    "next": "Reconcile H0DN value with independent original source; no direct transplant of Pantheon+ covariance"
  },
  {
    "CID": "2007on",
    "host": "N1404",
    "status": "PRESENT_BUT_NOT_R22",
    "release_IS_CALIBRATOR": 0,
    "next": "Same; do not use arithmetic combinations from unrelated SN rows"
  },
  {
    "CID": "2021rhu",
    "host": "N7814",
    "status": "ABSENT_FROM_PANTHEON_RELEASE",
    "release_IS_CALIBRATOR": null,
    "next": "Use Dhawan/TRGB and original light-curve/error budget; do not infer from another ID"
  },
  {
    "CID": "1980N",
    "host": "N1316",
    "status": "PRESENT_BUT_NOT_R22",
    "release_IS_CALIBRATOR": 0,
    "next": "Reconcile original photometry and uncertainty model; no direct transplant"
  },
  {
    "CID": "1981D",
    "host": "N1316",
    "status": "PRESENT_BUT_NOT_R22",
    "release_IS_CALIBRATOR": 0,
    "next": "Reconcile original photometry and uncertainty model; no direct transplant"
  },
  {
    "CID": "2006dd",
    "host": "N1316",
    "status": "PRESENT_BUT_NOT_R22",
    "release_IS_CALIBRATOR": 0,
    "next": "Reconcile original photometry and uncertainty model; no direct transplant"
  },
  {
    "CID": "1998bu",
    "host": "M96",
    "status": "CANONICAL_REDSHIFT_ONLY_TOO_REDDENED_FOR_R22",
    "release_IS_CALIBRATOR": null,
    "next": "Use Jha et al. 1999 and original photometry; do not treat as a missing alias"
  },
  {
    "CID": "1989B",
    "host": "M66",
    "status": "CANONICAL_REDSHIFT_ONLY_TOO_REDDENED_FOR_R22",
    "release_IS_CALIBRATOR": null,
    "next": "Use Wells et al. 1994 and original photometry; do not treat as a missing alias"
  },
  {
    "CID": "1994D",
    "host": "N4526",
    "status": "ALIAS_CLOSED_BUT_NOT_R22",
    "release_IS_CALIBRATOR": 0,
    "next": "Alias 1994DRichmond is validated; use Richmond et al. 1995 error budget, not R22 covariance"
  },
  {
    "CID": "1992A",
    "host": "N1380",
    "status": "PRESENT_BUT_NOT_R22",
    "release_IS_CALIBRATOR": 0,
    "next": "Reconcile original photometry and uncertainty model; no direct transplant"
  },
  {
    "CID": "ASASSN-14lp",
    "host": "N4666",
    "status": "ABSENT_FROM_PANTHEON_RELEASE",
    "release_IS_CALIBRATOR": null,
    "next": "Use arXiv:1507.04257 and original ASAS-SN/SNooPy error budget; no SALT2 substitution"
  },
  {
    "CID": "2021J",
    "host": "N4414",
    "status": "ABSENT_FROM_PANTHEON_RELEASE",
    "release_IS_CALIBRATOR": null,
    "next": "Use Gallego-Cano et al. 2022, OSN/Swift/SNooPy error budget; no SALT2 substitution"
  },
  {
    "CID": "2020nvb",
    "host": "N4457",
    "status": "ABSENT_FROM_PANTHEON_RELEASE",
    "release_IS_CALIBRATOR": null,
    "next": "Use AAVSO 709 and the independent TRGB route; no identity or covariance borrowed from Pantheon+"
  }
]

## Fontes exigidas

{
  "shared_HMS": "Original error budgets for every host equation, decomposed into independent and shared components with source lines",
  "original_sources": {
    "2021rhu": "Dhawan et al. 2022/TRGB and original ZTF/Swift photometry; Harvey et al. 2023 for transitional-SN treatment",
    "ASASSN-14lp": "https://arxiv.org/html/1507.04257v2",
    "2021J": "https://www.aanda.org/articles/aa/full_html/2022/10/aa43988-22/aa43988-22.html",
    "2020nvb": "AAVSO Alert Notice 709 plus https://arxiv.org/html/2508.20023 for independent TRGB route",
    "1998bu": "Jha et al. 1999, The Type Ia Supernova 1998bu in M96 and the Hubble Constant, doi:10.1086/313275",
    "1989B": "Wells et al. 1994 and original SN 1989B photometry",
    "1994D": "https://articles.adsabs.harvard.edu/pdf/1995AJ....109.2121R",
    "2008fv": "Tsvetkov & Elenin 2010 and Pantheon+ all_redshifts_PVs.csv for canonical identity",
    "2011iv/2007on/1980N/1981D/2006dd/1992A": "Original photometry/error budgets matching the H0DN values, not only Pantheon+ rows with IS_CALIBRATOR=0"
  },
  "prohibited": [
    "Adding the full HMS diagonal without removing the shared component already in mu_error",
    "Treating any missing ID as permission to assign a nearby alias",
    "Transplanting STAT+SYS wholesale and duplicating Cepheid-host covariance",
    "Choosing a covariance scenario because it raises power"
  ]
}

## Critério de aceite

A revisão só pode fechar G3/G4 quando a decomposição original estiver completa, sem duplicação, e o vetor passar no suporte com uma matriz cuja origem física tenha sido aceita independentemente. Se isso não for possível, o resultado correto é `OBSTRUCTION_EXACT`, não uma covariância artificialmente de posto completo.

**Não execute estimator.evaluate, não ajuste dados, não gere novas sementes e não mova o gate.**
