# Levantamento das fontes primárias — 13 calibradores H0DN

**Estado:** `PRIMARY_SOURCES_MAPPED__PARTIAL_COMPONENTS_ONLY__PHYSICAL_COVARIANCE_OPEN`  
**Escopo:** fontes e incertezas; nenhum centro fotométrico é reproduzido aqui; nenhuma abertura ou estatística observada.

## Resultado por objeto

| Objeto | SN linha / sigma (mag) | Host linha / mu_error (mag) | Fontes primárias | O que é recuperável | Estado da covariância |
|---|---:|---:|---|---|---|
| 2011iv | 44 / 0.1 | 466 / 0.034 | gall2018, newman2025 | Gall tabelas F.1–F.5; erro instrumental+zero-point noturno; sistemáticos SNooPy; TRGB posterior. | OPEN_NO_TRANSPLANT |
| 2007on | 45 / 0.19 | 466 / 0.034 | gall2018, newman2025 | Mesma fonte Gall; host e sequência locais compartilhados com 2011iv; TRGB posterior. | OPEN_NO_TRANSPLANT |
| 2021rhu | 46 / 0.15 | 295 / 0.07 | dhawan2022, harvey2023 | Dhawan tabela 1 com orçamento TRGB; Harvey tabela A1 com fotometria ZTF/Swift. | OPEN_NO_TRANSPLANT |
| 1980N | 47 / 0.15 | 276 / 0.04 | hamuy1991, elias1981, stritzinger2010 | Fotometria óptica/IR e erros parciais; análise posterior em Stritzinger. | OPEN_NO_TRANSPLANT |
| 1981D | 48 / 0.23 | 276 / 0.04 | hamuy1991, elias1981, stritzinger2010 | Erros por ponto incluem fundo; Stritzinger refaz fundo com dados modernos. | OPEN_NO_TRANSPLANT |
| 2006dd | 49 / 0.11 | 276 / 0.04 | stritzinger2010 | Tabelas 3–5; erros fotométricos e orçamento por método; covariância do ajuste é usada no artigo. | OPEN_NO_TRANSPLANT |
| 1998bu | 50 / 0.15 | 281 / 0.04 | jha1999, suntzeff1999 | Fotometria e erros por ponto; alertas explícitos de correlação e orçamento de distância. | OPEN_NO_TRANSPLANT |
| 1989B | 51 / 0.15 | 283 / 0.04 | wells1994, saha1999 | Fotometria com erros de fundo e orçamento Cepheid posterior. | OPEN_NO_TRANSPLANT |
| 1994D | 52 / 0.14 | 286 / 0.07 | richmond1995, patat1996 | Richmond tabelas 5–8 e Patat tabela 1; várias campanhas primárias. | OPEN_NO_TRANSPLANT |
| 1992A | 53 / 0.135 | 464 / 0.034 | hamuy1996, suntzeff1999, newman2025 | Template Hamuy e resumo posterior; nova rota TRGB/JWST em Newman. | NOT_FOUND_ORIGINAL_FULL_BUDGET__OPEN_NO_TRANSPLANT |
| ASASSN-14lp | 54 / 0.13 | 303 / 0.05 | shappee2016, li2025 | Shappee fotometria ancillary e sistemáticos SNooPy; Li oferece rota TRGB independente posterior. | OPEN_NO_TRANSPLANT |
| 2021J | 55 / 0.14 | 301 / 0.09 | gallego2022, li2025 | Gallego fotometria OSN/Swift e orçamento sistemático (tabela 4 arXiv; A.1 A&A); Li rota TRGB posterior. | OPEN_NO_TRANSPLANT |
| 2020nvb | 56 / 0.14 | 302 / 0.1 | newman2025, aavso709, li2025 | Newman tabelas 4,5,8 com TRGB, SALT2/BayeSN e fotometria; Alert 709 apenas descoberta/classificação. | OPEN_NO_TRANSPLANT |

## Estruturas compartilhadas efetivamente presentes no H0DN

- **N4258:** todos os 13 usam a geometria da âncora com 0,032 mag (`anchors.dat:2`).
- **MAS A25:** 2011iv, 2007on e 1992A, com 0,05 mag (`host_data.dat:463`).
- **MAS CCHP:** 1980N, 1981D, 2006dd, 1998bu, 1989B e 1994D, com 0,04 mag (`host_data.dat:273`).
- **MAS Ex:** 2021rhu, ASASSN-14lp, 2021J e 2020nvb, com 0,04 mag (`host_data.dat:294`).
- **Mesmo host:** N1404 compartilha 2011iv/2007on; N1316 compartilha 1980N/1981D/2006dd. A distância é comum, mas a covariância fotométrica completa não está publicada.
- **Fornax:** N1380 e N1404 têm equações de grupo com 0,057 mag (`groups.dat:17,19`); isso não é uma covariância genérica entre SNe.
- **HMS:** cada HMS envolvido tem uma linha ativa de host; várias SNe no mesmo host não criam, por si sós, um termo HMS fora da diagonal.
- **`sn1a_covar_pp.dat`:** pertence ao fluxo de Hubble e não é a covariância das linhas 44–56 dos calibradores.

## Fontes arquivadas

Os hashes completos, URLs finais, textos extraídos e recibos de recuperação estão em `fontes_primarias/MANIFEST_FONTES_PRIMARIAS.json`.

| Chave | Fonte | URL de arquivamento | SHA-256 |
|---|---|---|---|
| hamuy1991 | The Optical Light Curves of SN 1980N and SN 1981D in NGC 1316 | https://adsabs.harvard.edu/pdf/1991AJ....102..208H | `87065aaf56c642382b2508416d8d9c17ffd54140bf88aed76aa9cae1fc762fc5` |
| elias1981 | Infrared Light Curves of Type I Supernovae | https://articles.adsabs.harvard.edu/pdf/1981ApJ...251L..13E | `fbc2aaa53f78dc8e78f44802b5e59d47679343ee5d3c759981d7769b12e5f6d2` |
| wells1994 | The Type Ia Supernova 1989B in NGC 3627 (M66) | https://adsabs.harvard.edu/pdf/1994AJ....108.2233W | `be3ac25917a3d6bd4c7371c2a0da8be925b529cebf786c98a3eb5565c26e2fa7` |
| saha1999 | Cepheid Calibration of the Peak Brightness of SNe Ia IX SN 1989B | https://arxiv.org/pdf/astro-ph/9904389 | `d63f97e38de023ba652dfd6d1531dd52e2611e0281378508c5e25c4ba907361c` |
| hamuy1996 | The Morphology of Type Ia Supernova Light Curves | https://articles.adsabs.harvard.edu/pdf/1996AJ....112.2438H | `b8c251f1d8526465dbb4e98cc7adfcfa2c0888959f972a0ef468ce07031a5e81` |
| richmond1995 | UBVRI Photometry of the Type Ia SN 1994D in NGC 4526 | https://articles.adsabs.harvard.edu/pdf/1995AJ....109.2121R | `24d1b5fd3cdbf8785387e04efda6eceb3c6a7cec096a935f5e30f9faeb21c03b` |
| patat1996 | The Type Ia Supernova 1994D in NGC 4526 the Early Phases | https://articles.adsabs.harvard.edu/pdf/1996MNRAS.278..111P | `73d73fde16fa3aba957b681ef124da0015d0a4f9702d17d04eb2ea0660f4463e` |
| jha1999 | The Type Ia Supernova 1998bu in M96 and the Hubble Constant | https://arxiv.org/pdf/astro-ph/9906220 | `4f158f05489fe1569cf3ae384f2273f418f0c23d12b667481f0734b2be512e2a` |
| suntzeff1999 | Optical Light Curve of SN 1998bu in M96 and the Supernova Calibration of H0 | https://arxiv.org/pdf/astro-ph/9811205 | `e283e69e6b5b7b8d0a4c8c96bba8f0e31fad3dfb3c60e1891da855d37f6df31d` |
| stritzinger2010 | The Distance to NGC 1316 from Observations of Four Type Ia Supernovae | https://arxiv.org/pdf/1009.4390 | `d23251eb35171e347ff9f2fcbed7134669e65d18651cb23e25f0b3a3fc8a718c` |
| gall2018 | Two transitional Type Ia supernovae in NGC 1404 | https://arxiv.org/pdf/1707.03823 | `948695f52f81b6cbdca55eed2f1085891eda22c9e72a9f50099fddda45f65210` |
| dhawan2022 | TRGB distances to SN 2021rhu and calibrators | https://arxiv.org/html/2203.04241 | `7e1f3db3906d5614bf2dd2dbdc62fdc0e120386e2861ae909f14b7f9e5c43318` |
| harvey2023 | SN 2021rhu photometry and analysis | https://arxiv.org/html/2304.10129v2 | `95aed026a3ad0c0f3d80f2191cac26b3d005e9b88229ecd829bd072c9fbeb648` |
| shappee2016 | ASASSN-14lp photometry and light-curve analysis | https://arxiv.org/html/1507.04257v2 | `0f5834fb6caade5efb4938f64b1712647ed71921209a05b7aeb1f39ede0aad53` |
| li2025 | Independent TRGB routes for SN calibrator hosts | https://arxiv.org/html/2504.08921v1 | `dc72c4c276d951e9048929cbe569ff407c93a4967f825b04a20b4298225cd3ef` |
| gallego2022 | SN 2021J in NGC 4414 | https://arxiv.org/html/2204.10668v3 | `24bce7877c584ca5344ff5ed17d412ead396cf24aa36ad9484a3e217e09101cd` |
| newman2025 | TRGB and SN analysis including SN 2020nvb | https://arxiv.org/pdf/2508.20023v2 | `010510f5d52da19d1ea2bc34e944d9eb7f1c61ac2127687edb454ec893b08343` |
| aavso709 | AAVSO Alert Notice 709 | https://archive.aavso.org/aavso-alert-notice-709 | `566ce301431555df3a200dfb5ea126d22509779820352fae42623a4bf15369d0` |

## Veredito

A cobertura documental está completa para esta etapa: todos os 13 têm fonte primária arquivada. A covariância física completa continua **OPEN_NO_TRANSPLANT**. O pacote admite somente fatores e dependências explicitamente documentados; não transforma ausência de matriz em independência, nem fotometria pública em covariância pronta.

Para fechar a matriz ainda são necessários produtos internos dos ajustes ou novas decomposições pré-especificadas, revisão independente e um novo teste de suporte somente depois da aceitação física.
