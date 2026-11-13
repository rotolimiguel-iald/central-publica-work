# A1 — Hipóteses do vetor e as 72 identidades de montagem

**Estatuto:** `ESTUDO_DE_DESENHO_CONDICIONAL__NAO_E_CERTIFICADO` · `[DECLARADO pelo Kimi]`  
**Ordem vigente:** `ORDEM_KIMI_H0DN_03C_11nov.md`  
**SHA-256 da ordem:** `d0df9b4430ca9ff9d4fccb74ffcddc789819a5f29f7b030aa461a09c5a7c6836`  
**Escopo:** hipóteses documentais e álgebra pública de A1. Nenhuma conferência do vetor observado foi feita.

## 1. Convenção e por que não são tripletes iguais

Sejam `N = N4258`, `L = LMC`, `M = MW` e `0 = N7250` como hospedeiro de referência. Para cada um dos outros 36 hospedeiros R22, `k = 1,…,36`, e para cada âncora `a ∈ {N,L,M}`, `y_{k,a}` denota o centro da equação daquele hospedeiro, método, fonte e âncora na variante documentada.

Uma linha pode conter um offset comum de MAS/âncora:

\[
y_{k,a}=\mu_k+o_a+\varepsilon_k,
\]

em que `o_a` não depende do hospedeiro e `ε_k` é a medida compartilhada de HMS. Logo, **não se exige** `y_{k,N}=y_{k,L}=y_{k,M}`. Os offsets `o_a` e as calibrações de âncora desaparecem apenas ao formar as **segundas diferenças entre hospedeiros**:

\[
r^{NL}_k=(y_{k,N}-y_{k,L})-(y_{0,N}-y_{0,L})=0,
\]
\[
r^{NM}_k=(y_{k,N}-y_{k,M})-(y_{0,N}-y_{0,M})=0.
\]

Uma diferença isolada `y_{k,N}-y_{k,L}` contém, em geral, `o_N-o_L` e **não** é uma direção nula. Também não se pode criar uma suposta medida independente para eliminar a singularidade: a proveniência pública HMS declara compartilhamento da mesma medida dentro do tripleto.

## 2. As 72 identidades, explicitamente

Cada linha da tabela contém duas identidades, totalizando `36 × 2 = 72`. Todos os índices de hospedeiro seguem a ordem pública usada em A1; os nomes são identificadores, não valores observados.

| k | hospedeiro `k` | identidade `NL` | identidade `NM` |
|---:|---|---|---|
| 1 | N4536 | `(y_N4536,N-y_N4536,L)-(y_N7250,N-y_N7250,L)=0` | `(y_N4536,N-y_N4536,M)-(y_N7250,N-y_N7250,M)=0` |
| 2 | N3972 | `(y_N3972,N-y_N3972,L)-(y_N7250,N-y_N7250,L)=0` | `(y_N3972,N-y_N3972,M)-(y_N7250,N-y_N7250,M)=0` |
| 3 | N4424 | `(y_N4424,N-y_N4424,L)-(y_N7250,N-y_N7250,L)=0` | `(y_N4424,N-y_N4424,M)-(y_N7250,N-y_N7250,M)=0` |
| 4 | N4639 | `(y_N4639,N-y_N4639,L)-(y_N7250,N-y_N7250,L)=0` | `(y_N4639,N-y_N4639,M)-(y_N7250,N-y_N7250,M)=0` |
| 5 | N4038 | `(y_N4038,N-y_N4038,L)-(y_N7250,N-y_N7250,L)=0` | `(y_N4038,N-y_N4038,M)-(y_N7250,N-y_N7250,M)=0` |
| 6 | M101 | `(y_M101,N-y_M101,L)-(y_N7250,N-y_N7250,L)=0` | `(y_M101,N-y_M101,M)-(y_N7250,N-y_N7250,M)=0` |
| 7 | N2442 | `(y_N2442,N-y_N2442,L)-(y_N7250,N-y_N7250,L)=0` | `(y_N2442,N-y_N2442,M)-(y_N7250,N-y_N7250,M)=0` |
| 8 | N1365 | `(y_N1365,N-y_N1365,L)-(y_N7250,N-y_N7250,L)=0` | `(y_N1365,N-y_N1365,M)-(y_N7250,N-y_N7250,M)=0` |
| 9 | N5643 | `(y_N5643,N-y_N5643,L)-(y_N7250,N-y_N7250,L)=0` | `(y_N5643,N-y_N5643,M)-(y_N7250,N-y_N7250,M)=0` |
| 10 | N5584 | `(y_N5584,N-y_N5584,L)-(y_N7250,N-y_N7250,L)=0` | `(y_N5584,N-y_N5584,M)-(y_N7250,N-y_N7250,M)=0` |
| 11 | N1559 | `(y_N1559,N-y_N1559,L)-(y_N7250,N-y_N7250,L)=0` | `(y_N1559,N-y_N1559,M)-(y_N7250,N-y_N7250,M)=0` |
| 12 | N5468 | `(y_N5468,N-y_N5468,L)-(y_N7250,N-y_N7250,L)=0` | `(y_N5468,N-y_N5468,M)-(y_N7250,N-y_N7250,M)=0` |
| 13 | N1448 | `(y_N1448,N-y_N1448,L)-(y_N7250,N-y_N7250,L)=0` | `(y_N1448,N-y_N1448,M)-(y_N7250,N-y_N7250,M)=0` |
| 14 | N2525 | `(y_N2525,N-y_N2525,L)-(y_N7250,N-y_N7250,L)=0` | `(y_N2525,N-y_N2525,M)-(y_N7250,N-y_N7250,M)=0` |
| 15 | N3370 | `(y_N3370,N-y_N3370,L)-(y_N7250,N-y_N7250,L)=0` | `(y_N3370,N-y_N3370,M)-(y_N7250,N-y_N7250,M)=0` |
| 16 | N5861 | `(y_N5861,N-y_N5861,L)-(y_N7250,N-y_N7250,L)=0` | `(y_N5861,N-y_N5861,M)-(y_N7250,N-y_N7250,M)=0` |
| 17 | N3147 | `(y_N3147,N-y_N3147,L)-(y_N7250,N-y_N7250,L)=0` | `(y_N3147,N-y_N3147,M)-(y_N7250,N-y_N7250,M)=0` |
| 18 | N3021 | `(y_N3021,N-y_N3021,L)-(y_N7250,N-y_N7250,L)=0` | `(y_N3021,N-y_N3021,M)-(y_N7250,N-y_N7250,M)=0` |
| 19 | N1309 | `(y_N1309,N-y_N1309,L)-(y_N7250,N-y_N7250,L)=0` | `(y_N1309,N-y_N1309,M)-(y_N7250,N-y_N7250,M)=0` |
| 20 | N3982 | `(y_N3982,N-y_N3982,L)-(y_N7250,N-y_N7250,L)=0` | `(y_N3982,N-y_N3982,M)-(y_N7250,N-y_N7250,M)=0` |
| 21 | N1015 | `(y_N1015,N-y_N1015,L)-(y_N7250,N-y_N7250,L)=0` | `(y_N1015,N-y_N1015,M)-(y_N7250,N-y_N7250,M)=0` |
| 22 | N3447 | `(y_N3447,N-y_N3447,L)-(y_N7250,N-y_N7250,L)=0` | `(y_N3447,N-y_N3447,M)-(y_N7250,N-y_N7250,M)=0` |
| 23 | N5917 | `(y_N5917,N-y_N5917,L)-(y_N7250,N-y_N7250,L)=0` | `(y_N5917,N-y_N5917,M)-(y_N7250,N-y_N7250,M)=0` |
| 24 | U9391 | `(y_U9391,N-y_U9391,L)-(y_N7250,N-y_N7250,L)=0` | `(y_U9391,N-y_U9391,M)-(y_N7250,N-y_N7250,M)=0` |
| 25 | N3583 | `(y_N3583,N-y_N3583,L)-(y_N7250,N-y_N7250,L)=0` | `(y_N3583,N-y_N3583,M)-(y_N7250,N-y_N7250,M)=0` |
| 26 | N2608 | `(y_N2608,N-y_N2608,L)-(y_N7250,N-y_N7250,L)=0` | `(y_N2608,N-y_N2608,M)-(y_N7250,N-y_N7250,M)=0` |
| 27 | N7541 | `(y_N7541,N-y_N7541,L)-(y_N7250,N-y_N7250,L)=0` | `(y_N7541,N-y_N7541,M)-(y_N7250,N-y_N7250,M)=0` |
| 28 | N0691 | `(y_N0691,N-y_N0691,L)-(y_N7250,N-y_N7250,L)=0` | `(y_N0691,N-y_N0691,M)-(y_N7250,N-y_N7250,M)=0` |
| 29 | N3254 | `(y_N3254,N-y_N3254,L)-(y_N7250,N-y_N7250,L)=0` | `(y_N3254,N-y_N3254,M)-(y_N7250,N-y_N7250,M)=0` |
| 30 | N5728 | `(y_N5728,N-y_N5728,L)-(y_N7250,N-y_N7250,L)=0` | `(y_N5728,N-y_N5728,M)-(y_N7250,N-y_N7250,M)=0` |
| 31 | N7678 | `(y_N7678,N-y_N7678,L)-(y_N7250,N-y_N7250,L)=0` | `(y_N7678,N-y_N7678,M)-(y_N7250,N-y_N7250,M)=0` |
| 32 | M1337 | `(y_M1337,N-y_M1337,L)-(y_N7250,N-y_N7250,L)=0` | `(y_M1337,N-y_M1337,M)-(y_N7250,N-y_N7250,M)=0` |
| 33 | N4680 | `(y_N4680,N-y_N4680,L)-(y_N7250,N-y_N7250,L)=0` | `(y_N4680,N-y_N4680,M)-(y_N7250,N-y_N7250,M)=0` |
| 34 | N7329 | `(y_N7329,N-y_N7329,L)-(y_N7250,N-y_N7250,L)=0` | `(y_N7329,N-y_N7329,M)-(y_N7250,N-y_N7250,M)=0` |
| 35 | N0976 | `(y_N0976,N-y_N0976,L)-(y_N7250,N-y_N7250,L)=0` | `(y_N0976,N-y_N0976,M)-(y_N7250,N-y_N7250,M)=0` |
| 36 | N0105 | `(y_N0105,N-y_N0105,L)-(y_N7250,N-y_N7250,L)=0` | `(y_N0105,N-y_N0105,M)-(y_N7250,N-y_N7250,M)=0` |

Na notação matricial, essas 72 linhas formam `B`. A álgebra pública de A1 exige `BA = 0` e `BC = 0` no bloco correspondente; a nulidade do bloco R22 é 72. Isso não autoriza projetar `y` no espaço admitido, acrescentar jitter ou transformar uma violação em ajuste.

## 3. Hipóteses, em ordem inicial de plausibilidade pela fonte

A ordem abaixo é uma prioridade de investigação **documental**, não uma probabilidade medida e não uma escolha por resultado.

### H1 — Centros por âncora/MAS

**Hipótese.** As três linhas representam a mesma medida de hospedeiro, mas os centros publicados estão em referências MAS/âncora diferentes. A assinatura esperada é um offset comum por MAS, cancelado pelas segundas diferenças.

**Produto público decisivo.** Produtos R22 de precisão completa, fits 9/10/11, valores MAS e mapa de equações; a transformação própria do H0DN, quando houver. Deve-se reconstruir a cadeia “tabela → fit → MAS → centro compartilhado” antes de qualquer conferência observada.

### H2 — Convenção de montagem

**Hipótese.** `A` e `C` estão corretos, mas `y` foi copiado linha a linha sem validar as restrições nem documentar a propagação dos centros MAS. Em particular, a extração de `yval` e a extração separada de `mas_ref_value` precisam ter uma convenção única.

**Produto público decisivo.** Código upstream e do H0DN, `construir_y_obs.py:127–128`, `equations.py:334–376`, `data_loader.py:328–400`, propagação de `mas_ref_value` e mapa das 255 equações. O fixture sintético desta entrega testa essa cadeia sem ler o vetor observado.

### H3 — Precisão completa/arredondamento

**Hipótese.** Células decimais publicadas podem produzir resíduos de quantização. Arredondamento **não** será presumido como explicação antes de sua magnitude ser delimitada pela fonte.

**Produto público decisivo.** Valores R22 de precisão completa, não apenas tabelas arredondadas; precisão declarada por célula e regra de quantização congelada antes da consulta. A tolerância futura é a soma dos limites de arredondamento das quatro células de cada identidade, mais apenas a tolerância numérica pré-fixada.

### H4 — As linhas não são a mesma medida

**Hipótese.** Alguma linha tem proveniência individual diferente daquela presumida pelo modelo. É a menos favorecida pela fonte, porque o H0DN declara compartilhamento para host/método/fonte; se comprovada, exige nova variante, não reparo do vetor.

**Produto público decisivo.** H0DN B.3.2, proveniência individual das linhas, identificadores de objetos e tabelas/fontes primárias. Não se pode inventar variância independente para eliminar a singularidade.

## 4. Regra de decisão documental

1. Primeiro recuperar e congelar a convenção de centros, os fits, os offsets MAS e o mapa de linhas.
2. Depois fixar a precisão e a tolerância; só então pedir autorização para a única conferência por variante admitida.
3. A conferência futura é binária e segue `PROTOCOLO_CONFERENCIA_FUTURA.md`; nenhuma hipótese acima foi testada agora.
4. Falha documental ou de montagem não autoriza projeção, reparo, repetição com outra tolerância ou escolha de variante pelo resultado.

## 5. Flags e rastreabilidade

```json
{
  "observed_vector_read": false,
  "observed_support_tests": 0,
  "estimator_evaluate_called": false,
  "solver_on_observed_called": false,
  "Z_t_h_or_ratio_computed": false,
  "new_seed_or_monte_carlo": false,
  "freeze_R2_or_v410_modified": false,
  "observed_conference_executed": false
}
```
