# Protocolo da única conferência futura do vetor observado

**Estado:** `ESCRITO_AGORA__NAO_EXECUTADO__REQUER_AUTORIZACAO_EXPLICITA`  
**Estatuto:** `ESTUDO_DE_DESENHO_CONDICIONAL__NAO_E_CERTIFICADO` · `[DECLARADO pelo Kimi]`  
**Ordem vigente:** `ORDEM_KIMI_H0DN_03C_11nov.md`  
**Rota:** `estatistica.h0dn_bg1.ordem_kimi_y_obs_09nov`  
**Conferências observadas executadas nesta entrega:** `0`.

## 1. Objeto e limite

Este protocolo admite **uma única conferência de montagem por variante admitida**, compreendendo as 72 identidades em uma só abertura do vetor. Não é teste estatístico de H0, não é ajuste, não é seleção de variante e não autoriza qualquer inferência de poder ou detecção.

Não haverá conferência enquanto não existirem simultaneamente:

1. autorização explícita do operador para a variante nomeada;
2. variante fisicamente admitida e revista, com estimando, modelo e convenção afim congelados;
3. mapa público das linhas e proveniência individual dos 37 tripletes R22;
4. fits 9/10/11, centros e offsets MAS reconstruídos documentalmente;
5. precisão por célula, regra de quantização e tolerâncias congeladas conforme §3;
6. hashes do vetor, do mapa, do código e desta autorização registrados **antes** da abertura.

A ausência de qualquer item produz `NOT_AUTHORIZED` **sem ler o vetor**. `NOT_AUTHORIZED` não é resultado de conferência e não consome uma rota; tampouco permite procurar outra variante pelo resultado.

## 2. Pré-registro obrigatório por variante

Antes da abertura, gravar um único manifesto imutável contendo:

```text
variant_id
operator_authorization_and_sha256
vector_path_and_sha256
row_map_path_and_sha256
source_fits_and_versions
center_convention = raw_MAS | documented_MAS_corrected
reference_host = N7250
anchor_order = N4258, LMC, MW
host_order = a ordem pública de A1
cell_precision_and_quantization_rule
identity_tolerances[72]
numeric_tolerance = 1e-12 mag
code_sha256
protocol_sha256
route_name
route_sequence_number
```

`raw_MAS` e `documented_MAS_corrected` não podem ser misturados. Se a convenção de centros mudar, trata-se de outra variante que precisa de admissão e autorização próprias; não se pode renomear uma tentativa falha para obter repetição.

## 3. Tolerância pré-fixada pela precisão da fonte

Para cada célula `y_{k,a}`, registrar um limite documental de erro de representação `b_{k,a} ≥ 0`, derivado apenas da fonte:

- arredondamento ao mais próximo com passo decimal `q_{k,a}`: `b_{k,a}=q_{k,a}/2`;
- truncamento ou regra não simétrica: usar o limite superior documentado, sem substituí-lo por `q/2`;
- transformação entre fits/âncoras: propagar o limite documental da transformação; não usar incerteza astrofísica como se fosse erro de arredondamento;
- valor de precisão completa em ponto flutuante: `b_{k,a}=0` na camada documental, restando a tolerância numérica.

A tolerância numérica é fixada agora em **`τ_num = 1e-12 mag`**, para cobrir apenas aritmética de ponto flutuante na montagem. Ela não pode ser ampliada após leitura.

Para `NL = N4258−LMC` e `NM = N4258−MW`:

\[
\tau^{NL}_k=b_{k,N}+b_{k,L}+b_{0,N}+b_{0,L}+\tau_{num},
\]
\[
\tau^{NM}_k=b_{k,N}+b_{k,M}+b_{0,N}+b_{0,M}+\tau_{num}.
\]

Essas tolerâncias são **limites de representação**, não desvios-padrão, intervalos de confiança ou folgas escolhidas para obter aprovação. Se `b_{k,a}` ou a regra de quantização não for conhecida, a variante não está pronta: não abrir.

## 4. As 72 comparações, sem projeção

Com `0=N7250`, `N=N4258`, `L=LMC`, `M=MW`, calcular somente:

\[
r^{NL}_k=(y_{k,N}-y_{k,L})-(y_{0,N}-y_{0,L}),\qquad k=1,\ldots,36,
\]
\[
r^{NM}_k=(y_{k,N}-y_{k,M})-(y_{0,N}-y_{0,M}),\qquad k=1,\ldots,36.
\]

Os nomes dos 36 hospedeiros e as 72 expressões estão congelados em `A1_HIPOTESES_DO_VETOR.md`. O cálculo de `r` é apenas avaliação das combinações lineares declaradas. **Não** calcular nem aplicar `Py`, `y−Py`, pseudoinversa para “corrigir” o vetor, jitter, reponderação ou projeção no suporte.

Não exigir igualdade dentro dos tripletes. Offsets MAS comuns por âncora podem tornar as três linhas diferentes e ainda satisfazer as 72 identidades.

## 5. Regra binária e parada

Depois de verificar hashes, mapa, dimensões, finitude e autorização, a conferência tem somente dois resultados:

- **`PASS`**: todas as 72 identidades satisfazem `|r_i| ≤ τ_i`, inclusive os limites de precisão documental;
- **`ASSEMBLY_CONSTRAINT_VIOLATION`**: qualquer `|r_i| > τ_i`, valor não finito, linha ausente/duplicada, mapa/hash incompatível ou erro depois que o vetor foi aberto.

**Uma falha encerra a variante.** Não há reparo, ajuste de centros, escolha de subconjunto, alteração de tolerância, segunda leitura, repetição com outra regra ou tentativa de contornar por outra rota. A abertura do vetor consome a rota mesmo se uma falha técnica impedir o cálculo completo.

`PASS` significa somente que a montagem passou nas restrições declaradas; não admite covariância física, não valida independência e não autoriza solver ou avaliação estatística.

## 6. Contabilidade da rota

A rota `estatistica.h0dn_bg1.ordem_kimi_y_obs_09nov` deve registrar, em um recibo append-only da futura execução:

1. `variant_id` e número sequencial;
2. data, autorização e hashes pré-registrados;
3. instante da única abertura, que marca o consumo da rota;
4. tolerâncias por identidade e seus limites de precisão;
5. `PASS` ou `ASSEMBLY_CONSTRAINT_VIOLATION`;
6. flags de proibição e assinatura do executor.

**Contagem atual:** `0` conferências futuras executadas e `0` rotas observadas consumidas nesta entrega. O planejamento é exatamente `1` conferência por variante admitida e autorizada, nunca mais de uma.

## 7. Proibições durante e depois da conferência

- Nenhum Z, t, ĥ, D, razão ou poder com dado observado.
- Nenhum `estimator.evaluate`, solver observado ou teste de suporte adicional.
- Nenhuma semente, Monte Carlo, HMS completa, jitter ou projeção de `y`.
- Nenhuma alteração de `FREEZE_R2`, v410, variante, contraste ou tolerância.
- Nenhuma escolha de modelo/variante pelo resultado da conferência.
- Nenhuma publicação ou palavra de detecção/confirmação.

## 8. Hashes congelados nesta entrega

| Arquivo | SHA-256 |
|---|---|
| `ORDEM_KIMI_H0DN_03C_11nov.md` | `d0df9b4430ca9ff9d4fccb74ffcddc789819a5f29f7b030aa461a09c5a7c6836` |
| `A1_HIPOTESES_DO_VETOR.md` | `e45a0f0dbe67dc502eaaf0674a9477466c2dd6b78c3627a6bd7cfe587878aeae` |
| `PRODUTOS_A_PEDIR.md` | `3dc258d5dacbde3b9c8dc86e4a4c110beee132f4f8b068ab0953ab98243aa472` |
| `FONTES_CEFEIDAS_DOCUMENTAL.md` | `45c99c2a79a12fb1291a38c60ec3febaf3512e20f36637aba6492116a2004bb6` |
| `MONTAGEM_FIXTURES_SINTETICOS.json` | `6ab9218275602f9a98c8de486c420eb1503a7bd3a7c5e95c4b240199e8488c13` |
| `fixtures/validate_synthetic_assembly.py` | `5e49189c4d83d15a48e857f2e1c5378b859c765cdae2cf8788bc31ac223a8162` |

O SHA-256 deste protocolo deve ser acrescentado pelo manifesto de entrega externo; ele não é embutido no próprio conteúdo para evitar autorreferência.

## 9. Flags atuais

```json
{
  "protocol_status": "WRITTEN_NOT_EXECUTED",
  "observed_vector_read": false,
  "observed_support_tests": 0,
  "observed_conferences_executed": 0,
  "observed_routes_consumed": 0,
  "planned_conferences_per_admitted_variant": 1,
  "repeat_after_failure_allowed": false,
  "projection_or_repair_allowed": false,
  "operator_authorization_obtained_for_observed_check": false,
  "estimator_evaluate_called": false,
  "solver_on_observed_called": false,
  "new_seed_or_monte_carlo": false,
  "freeze_R2_or_v410_modified": false
}
```
