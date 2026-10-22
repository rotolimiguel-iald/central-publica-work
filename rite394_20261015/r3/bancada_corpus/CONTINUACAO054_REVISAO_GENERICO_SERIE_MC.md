# Continuação054 — revisão independente do custo genérico e da série

[REAL — leitura dos fontes e medição dos bytes; não é aprovação do build final]

Revisor: agente review_cocycle_covariance. Não construí `PolarizerModularCost.lean` (Newton) nem `PolarizerCostSeries.lean` (Beauvoir). Minha autoria de `TowerModularCost.lean` é distinta e não recebe autoaprovação neste documento.

A leitura matemática foi integral nos dois fontes abaixo. Não executei Lean nem auditor final para esta revisão, não modifiquei esses fontes e não emiti manifesto. A validação conjunta final ainda está pendente; os resultados de sondas coordenadas pela raiz não substituem essa etapa.

| Fonte lido | Bytes | SHA256 medido | Teoremas / definições / instâncias / prints |
|---|---:|---|---|
| PolarizerModularCost.lean | 9200 | ee1b871c6e8f0535dba24085687c8948dd3f5069e6366038a028aa0e2a7035c3 | 19 / 4 / 0 / 23 |
| PolarizerCostSeries.lean | 6011 | 52b147834a44d8d6e8b6a8af62d9d924e51d2c3243ba50214b4f602129f25342 | 12 / 0 / 0 / 12 |

## Resultado matemático

Não encontrei falha material nos enunciados e nas provas examinadas, dentro das hipóteses explícitas.

1. **Custo estendido e divergência.** O genérico define a soma em `ENNReal` de `ofReal(2/(2n+1) · ‖D^(n+1)x‖²)`. Cada parcela é finita e não negativa; a soma pode valer infinito. Não há conversão de uma série real divergente para zero. O operador D é qualquer operador real linear contínuo no espaço com produto interno; a norma estritamente menor que um não é hipótese global.
2. **Núcleo e domínio.** A primeira parcela, `2‖Dx‖²`, fornece custo zero se e somente se `Dx=0`. No sentido inverso, todas as potências positivas anulam x. O domínio é exatamente `{x : custo(x)<∞}`. A homogeneidade por `ofReal(a²)` e a cota `custo(x+y)≤2custo(x)+2custo(y)` fecham esse conjunto sob as operações de submódulo. O caso a=0 também é compatível com a multiplicação estendida, mesmo quando o custo original é infinito.
3. **Covariância.** A hipótese é uma isometria linear real bijetiva W que satisfaz `D(Wx)=W(Dx)` para todos os vetores. A indução transporta cada potência, preserva a norma, e fornece igualdade do custo e equivalência da pertinência ao domínio. Não é postulada uma covariância de um objeto físico adicional.
4. **Semicontinuidade inferior.** Cada parcela é contínua; a soma estendida de parcelas não negativas é semicontínua inferior, inclusive nos pontos onde vale infinito. O fonte não conclui daí, por si só, um operador autoadjunto associado nem uma forma bilinear fechada empacotada.
5. **Série escalar.** O contrato exige `|d|<1` e prova

       Σ(n≥0) 2 d^(2n+2)/(2n+1) = d[log(1+d)−log(1−d)].

   Os expoentes são pares e o resultado cobre d negativo e d=0. A prova não divide por d. A passagem para a razão de pesos usa wi,wj estritamente positivos e aceita wi=wj. Os extremos d=±1 não são abrangidos pela identidade logarítmica; sua exclusão evita aplicar o logaritmo real totalizado ao limite divergente.
6. **Passagem para o custo.** As igualdades entre a série real e a soma em `ENNReal` usam `HasSum` e a não negatividade das parcelas. As avaliações espectrais de um vetor exigem uma lei explícita para as normas das potências; não afirmam essa lei para vetores arbitrários. A prova dessa hipótese na torre é uma obrigação separada do módulo que eu construí.

## Limites da revisão e do resultado

[OPEN] Estes dois módulos não identificam o custo com entropia relativa global de Araki, não constroem `log Δ` global com domínio, e não identificam o custo com `inducedArea` ou `constructedHeat`. Não selecionam escala dimensional, região física ou dinâmica gravitacional.

A densidade de vetores locais no espaço de Hilbert, se demonstrada por outro módulo, não será tratada como prova de que esses vetores constituem núcleo da forma. O estatuto de uma forma quadrática fechada por polarização depende de enunciados adicionais; a semicontinuidade inferior e o domínio submódulo, isoladamente, não recebem esse rótulo como resultado Lean desta revisão.

Esta nota confirma a coerência matemática dos bytes medidos e a separação das hipóteses. Não certifica custódia geral, não altera o gate canônico e não substitui a revisão do build definitivo. H3 e a reconstrução gravitacional geral permanecem OPEN.

Emissão UTC: 2026-09-07T06:38:53.154831+00:00
