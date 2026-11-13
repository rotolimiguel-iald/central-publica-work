# Pedidos às fontes — RASCUNHO para o operador enviar (11/11/2026)

**Estado:** `RASCUNHO__NADA_ENVIADO`. O envio é ato do operador. Os pedidos correm em paralelo e NÃO travam a abertura do teste (ver `DESENHO_RATIFICADO_H0DN_11nov.md`). A lista de produtos vem de `kimi\ordem03B\PRODUTOS_A_PEDIR.md` (sha256 `3dc258d5dacbde3b9c8dc86e4a4c110beee132f4f8b068ab0953ab98243aa472`). Os destinatários ficam por preencher com os autores correspondentes indicados em cada artigo; nenhum nome foi posto aqui de memória.

## 1. Para a equipe do H0DN (autores correspondentes do artigo)

```
Subject: Request for assembly conventions and covariance products (H0DN release)

Dear [corresponding author],

I am carrying out an independent, pre-registered analysis that uses the public H0DN
distance-network release exactly as published (data vector and covariance), without
modifying your error model. To make sure I assemble the public products correctly, could
you point me to, or share:

1. the row-by-row equation map of the network (which rows share a host measurement), and
   the centring convention used for the host rows (raw MAS reference values versus
   anchor-corrected centres);
2. the full-precision values behind the published host tables (the fits and MAS reference
   values), so that rounding can be bounded;
3. how the errors of the 42 calibrator supernovae were aggregated, and whether those error
   variables are the same as in the Pantheon+ release;
4. if available, the internal covariance (and cross-terms) for the 13 additional calibrators.

I will cite the release and acknowledge any clarification. Thank you for making the data
public.

Luiz Antonio Rotoli Miguel
IALD Ltda. - ORCID 0009-0005-1114-6106
```

## 2. Para a equipe SH0ES / R22 (autores correspondentes)

```
Subject: Request for full-precision R22 products (fits 9/10/11, MAS values, equation map)

Dear [corresponding author],

For an independent, pre-registered analysis built on public distance-ladder products, I
need to reproduce the host-centre chain of R22 at full precision. Could you point me to, or
share, the full-precision outputs of fits 9, 10 and 11 (host centres, MAS reference values
and anchor conversions) together with the equation map? The public tables are rounded, and
I would like to bound the rounding rather than assume it.

Thank you.

Luiz Antonio Rotoli Miguel
IALD Ltda. - ORCID 0009-0005-1114-6106
```

## 3. Para a equipe Pantheon+ (autores correspondentes)

```
Subject: Request for the decomposition of the Hubble-flow covariance (peculiar velocities)

Dear [corresponding author],

For an independent, pre-registered analysis that uses the public Pantheon+ covariance as
released, I would like to report a stress test by component. Is the decomposition of the
Hubble-flow covariance by component (statistical, peculiar-velocity model, calibration)
available, with the supports and weights used?

Thank you.

Luiz Antonio Rotoli Miguel
IALD Ltda. - ORCID 0009-0005-1114-6106
```

## 4. O que NÃO se pede

A covariância conjunta entre a medida local e o fundo (Planck, DESI): a independência entra como hipótese nomeada no pré-registro, e o cenário adverso entra como linha de estresse.
