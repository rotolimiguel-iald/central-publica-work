# Normalidade da amplificação: APIs de supremos positivos

[REAL — consulta local em 11/09/2026] **O teorema central já existe no kernel da bancada.**
Importação exata: `TGLExt.MonotoneOperatorLimit`. Namespace exato:
`ChatgptAudit.Expectation047` — não `TGLExt` nem `TGLV350.Regular`.
Fonte: [MonotoneOperatorLimit.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLExt/MonotoneOperatorLimit.lean>). O módulo foi lido integralmente, incluindo todas as provas.
Também foi lido integralmente [ExpectationNormality.lean](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLExt/ExpectationNormality.lean>), que contém
um precedente de normalidade por preservação de supremos positivos dirigidos.

A busca em Mathlib não localizou teorema central equivalente pronto nem equivalência geral
normalidade ↔ preservação de limites SOT limitados. Isso é resultado da busca realizada,
não afirmação de inexistência universal. **Reutilizar o módulo local resolve a lacuna principal.**

[REAL — inspeção dos artefatos] Duas execuções de `Lean --stdin`, sem `-o`, sem criar fonte Lean,
sem build novo e sem log em disco, carregaram os `.olean` existentes e terminaram com **exit 0**.
Foram inspecionadas as assinaturas dos dois teoremas centrais, do lema de positividade e do
nosso transporte de limites. Os axiomas dos dois teoremas centrais e dos lemas
`positive_of_strong_limit`, `positive_increment_norm_sq_le`, `monotone_operator_vector_cauchy`
são exclusivamente `propext`, `Classical.choice`, `Quot.sound`.
A expressão `OrderHomClass.monotone (TGLV350.Regular.fibreRepresentation (H := H))`
também foi verificada no ambiente Lean e resolve para a monotonicidade da representação.
Isso verifica as APIs nos binários carregados; **não é uma recompilação das fontes nesta consulta**.

## 1. Assinaturas centrais existentes, não propostas

Contexto comum dos dois teoremas abaixo:

```lean
variable {H : Type*} [NormedAddCommGroup H] [InnerProductSpace ℂ H] [CompleteSpace H]
variable {ι : Type*} [Preorder ι] [IsDirectedOrder ι] [Nonempty ι]
```

[Construção do limite e do supremo](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLExt/MonotoneOperatorLimit.lean:223>):

```lean
theorem monotone_operator_limit (A : ι → H →L[ℂ] H)
    (hpos : ∀ i, 0 ≤ A i) (hmono : Monotone A)
    (C : ℝ) (hC : 0 ≤ C) (hbound : ∀ i, ‖A i‖ ≤ C) :
    ∃ B : H →L[ℂ] H, 0 ≤ B ∧ ‖B‖ ≤ C ∧
      (∀ v, Tendsto (fun i => A i v) atTop (𝓝 (B v))) ∧
      IsLUB (Set.range A) B
```

[Supremo a partir de limite forte](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLExt/MonotoneOperatorLimit.lean:204>):

```lean
theorem monotone_strong_limit_isLUB (A : ι → H →L[ℂ] H)
    (hmono : Monotone A) (B : H →L[ℂ] H)
    (hlim : ∀ v, Tendsto (fun i => A i v) atTop (𝓝 (B v))) :
    IsLUB (Set.range A) B
```

Não há restrição a sequências, dimensão finita, separabilidade, primeira enumerabilidade ou
`SemilatticeSup ι`. São redes sobre qualquer pré-ordem dirigida não vazia; o filtro é `atTop`.
Não se assume a existência do limite na primeira assinatura: ela é conclusão construída.
Na segunda, a convergência é hipótese porque o objetivo é identificar o supremo a partir dela.

## 2. Caminho mínimo para a amplificação

[DERIVED — composição proposta, ainda não implementada nesta subtarefa]
Alvo: dados `A : ι → (H →L[ℂ] H)`, `hpos : ∀ i, 0 ≤ A i`, `hmono : Monotone A`,
`B : H →L[ℂ] H` e **`hB : IsLUB (Set.range A) B`**, concluir
**`IsLUB (Set.range (fun i => TGLV350.Regular.fibre (A i))) (TGLV350.Regular.fibre B)`**.
Manter `[Preorder ι] [IsDirectedOrder ι] [Nonempty ι]`.
Para usar a amplificação já escrita, H está em `Type`, conforme a assinatura atual da base.

1. **Cota derivada do supremo.** `hB.1 (Set.mem_range_self i)` dá `A i ≤ B`.
   `CStarAlgebra.norm_le_norm_of_nonneg_of_le (hpos i) ...` dá `‖A i‖ ≤ ‖B‖`.
   Assim a entrada do teorema pode ser apenas o supremo positivo dirigido; não é necessário
   acrescentar uma hipótese artificial de convergência SOT ou uma cota que o supremo já fornece.
2. **Limite forte construído.** Aplicar `ChatgptAudit.Expectation047.monotone_operator_limit`
   com `C = ‖B‖` e `hC = norm_nonneg B`. Ele devolve um operador L, sua convergência forte e
   `hL : IsLUB (Set.range A) L`. Usar `hL.unique hB` para obter `L = B` e substituir.
3. **Transporte da convergência.** Aplicar
   `TGLV350.Regular.fibre_tendsto_of_uniformly_bounded` com `l = atTop`, `T = A`, `S = B`,
   `C = ‖B‖`, a cota do passo 1 e o limite do passo 2. Resulta convergência em cada vetor de
   `RegularHilbert H` para `fibre B`.
4. **Monotonicidade na imagem.** Usar
   `OrderHomClass.monotone (TGLV350.Regular.fibreRepresentation (H := H))` e compor com `hmono`.
   A classe de ordem é derivada de o mapa preservar adição, multiplicação e star entre
   `StarOrderedRing`; não precisa refazer a positividade pela integral L².
   A aplicação de `fibreRepresentation` é a própria `fibre` pela definição.
5. **Supremo na imagem.** Aplicar `ChatgptAudit.Expectation047.monotone_strong_limit_isLUB`
   no Hilbert `RegularHilbert H`, à família `fun i => fibre (A i)`, à monotonicidade do passo 4
   e ao limite do passo 3. O resultado é exatamente o alvo em `IsLUB`.
   Este último lema não exige uma cota adicional para a família amplificada.

Importações suficientes a conferir pelo implementador: `TGLExt.MonotoneOperatorLimit` e
`TGLV350.L2BoundedStrongContinuity`. Ambas foram carregadas juntas nas inspeções desta consulta.
A cadeia não depende de `ExpectationInput`, `SiteProfile` ou da torre: o teorema monotônico é
inteiramente genérico em H.

[DERIVED] Para também concluir **existência** do supremo de uma família positiva dirigida com
cota de ordem D, primeiro obter `‖A i‖ ≤ ‖D‖`, construir B pelo mesmo teorema e repetir os passos
3–5. O precedente local já faz exatamente essa conversão para a esperança:
[expectation_preserves_order_bounded_nets](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLExt/ExpectationNormality.lean:124>).
A identificação com um supremo previamente dado aparece em
[general_expectation_normal_order](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLExt/ExpectationNormality.lean:140>).
Esses dois enunciados da esperança têm domínio próprio na torre; servem como modelo da
composição, não como teoremas diretamente aplicáveis a `fibre`.

## 3. APIs locais que sustentam o teorema central

Todas as linhas abaixo pertencem ao namespace `ChatgptAudit.Expectation047`.

| Declaração e localização | Conteúdo efetivo |
|---|---|
| [`operatorQuadratic`](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLExt/MonotoneOperatorLimit.lean:55>) | Re ⟨v, A v⟩. |
| [`positive_square_le_norm_smul`](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLExt/MonotoneOperatorLimit.lean:59>) | 0 ≤ D implica D*D ≤ ‖D‖ • D. |
| [`positive_apply_norm_sq_le`](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLExt/MonotoneOperatorLimit.lean:73>) | ‖D v‖² ≤ ‖D‖ * operatorQuadratic D v. |
| [`positive_increment_norm_sq_le`](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLExt/MonotoneOperatorLimit.lean:89>) | 0 ≤ A ≤ B e ‖B‖ ≤ C dão ‖(B-A)v‖² ≤ C*(q_B(v)-q_A(v)). |
| [`positive_of_strong_limit`](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLExt/MonotoneOperatorLimit.lean:105>) | Positividade eventualmente válida passa a limite forte ao longo de qualquer filtro não trivial; dispensa completude de H. |
| [`monotone_quadratic_limit`](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLExt/MonotoneOperatorLimit.lean:131>) | As leituras escalares convergem a seu ciSup real; recebe monotonicidade e cota uniforme. |
| [`monotone_operator_vector_cauchy`](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLExt/MonotoneOperatorLimit.lean:152>) | A rede positiva monótona limitada é Cauchy em cada vetor; índices dirigidos gerais. |
| [`monotone_strong_limit_isLUB`](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLExt/MonotoneOperatorLimit.lean:204>) | Uma rede monótona com limite forte tem esse limite como IsLUB; não exige cota nem positividade como hipóteses adicionais. |
| [`monotone_operator_limit`](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLExt/MonotoneOperatorLimit.lean:223>) | Constrói simultaneamente operador positivo limitado, limite forte e IsLUB. |

Prova central lida: `CFC.sqrt D` e a desigualdade de conjugação fornecem `D² ≤ ‖D‖ D`;
a leitura quadrática converte isso em estimativa da norma de Dv. Para incrementos positivos,
`0 ≤ B-A ≤ B` permite manter a constante C. As leituras escalares convergem ao `ciSup` real.
No teste de Cauchy, a prova usa `delta = eps² / (4*(C+1))` e `exists_ge_ge` para comparar
índices arbitrários. A completude de H fornece o limite de cada vetor, e
`ContinuousLinearMap.ofTendstoOfBoundedRange` empacota esses limites em um operador limitado.
A positividade passa ao limite, e duas aplicações desse fato provam as duas cláusulas de `IsLUB`.

Transporte novo já compilado:
[fibre_tendsto_of_uniformly_bounded](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/L2BoundedStrongContinuity.lean:70>).
Representação star já construída:
[fibreRepresentation](<C:/IALD/Central de Patentes/Chatgpt/TETELESTAI_V350_KERNEL_20260911/kernel/TGLV350/L2OperatorLift.lean:53>).

## 4. Mathlib: nomes e localizações conferidos

Raiz Mathlib consultada: `C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/.lake/packages/mathlib/Mathlib`. Os links abaixo são absolutos.

| API exata | Fonte | Uso e hipótese relevante |
|---|---|---|
| `CStarAlgebra.norm_le_norm_of_nonneg_of_le` | [Order.lean](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/.lake/packages/mathlib/Mathlib/Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Order.lean:449>) | `0 ≤ a` e `a ≤ b` implicam `‖a‖ ≤ ‖b‖`; `NonUnitalCStarAlgebra`, `PartialOrder`, `StarOrderedRing`. Lema lido integralmente. |
| `CStarAlgebra.star_left_conjugate_le_norm_smul` | [Order.lean](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/.lake/packages/mathlib/Mathlib/Analysis/CStarAlgebra/ContinuousFunctionalCalculus/Order.lean:464>) | `IsSelfAdjoint b` implica `star a * b * a ≤ ‖b‖ • (star a * a)`. Lema lido integralmente. |
| `CFC.sqrt_nonneg`, `CFC.sqrt_mul_sqrt_self` | [Rpow/Basic.lean](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/.lake/packages/mathlib/Mathlib/Analysis/SpecialFunctions/ContinuousFunctionalCalculus/Rpow/Basic.lean:234>) | Positividade da raiz; `sqrt a * sqrt a = a` para `0 ≤ a`. Seção correspondente lida. |
| `ContinuousLinearMap.le_def`, `ContinuousLinearMap.nonneg_iff_isPositive` | [Positive.lean](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Positive.lean:468>) | Ordem de Loewner: `f ≤ g ↔ (g-f).IsPositive`; `0 ≤ f ↔ f.IsPositive`. |
| `ContinuousLinearMap.isPositive_def`, `ContinuousLinearMap.IsPositive.inner_left_eq_inner_right` | [Positive.lean](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/Positive.lean:269>) | Simetria e positividade da forma quadrática; indispensável manter a simetria no limite. |
| `ContinuousLinearMap.instStarOrderedRing` | [StarOrder.lean](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/StarOrder.lean>) | Ordem star dos operadores no Hilbert complexo completo; módulo lido inteiro. |
| `StarRingHomClass.instOrderHomClass` | [Star/Basic.lean](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/.lake/packages/mathlib/Mathlib/Algebra/Order/Star/Basic.lean:442>) | Fornece monotonicidade de homomorfismos star; prova via `NonUnitalStarRingHom.map_le_map_of_map_star` em 433, lida inteira. |
| `OrderHomClass.monotone` | [Order/Hom/Basic.lean](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/.lake/packages/mathlib/Mathlib/Order/Hom/Basic.lean:165>) | A aplicação a `fibreRepresentation` foi checada no Lean. |
| `tendsto_atTop_ciSup` | [MonotoneConvergence.lean](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/.lake/packages/mathlib/Mathlib/Topology/Order/MonotoneConvergence.lean:116>) | Convergência escalar monótona e limitada; aplicar em ℝ. Assinatura e prova lidas. |
| `cauchy_map_iff_exists_tendsto` | [Cauchy.lean](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/.lake/packages/mathlib/Mathlib/Topology/UniformSpace/Cauchy.lean:424>) | Completude e filtro não trivial: `Cauchy (l.map f) ↔ ∃ x, Tendsto f l (𝓝 x)`. |
| `ContinuousLinearMap.ofTendstoOfBoundedRange` | [Completeness.lean](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/.lake/packages/mathlib/Mathlib/Analysis/Normed/Operator/Completeness.lean:62>) | Constrói CLM de limite pontual e família limitada, para qualquer filtro não trivial. Definição e auxiliar lidos por inteiro; coerção para função é definicionalmente o limite. |
| `IsLUB.unique` | [Bounds/Basic.lean](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/.lake/packages/mathlib/Mathlib/Order/Bounds/Basic.lean:816>) | Identifica o limite construído ao supremo dado, sem assumir convergência de antemão. |
| `le_of_tendsto` | [OrderClosed.lean](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/.lake/packages/mathlib/Mathlib/Topology/Order/OrderClosed.lean:131>) | Passagem de desigualdades escalares ao limite; filtro não trivial. |

## 5. Rotas que não encurtam esta implementação

[REAL — APIs lidas] [WeakOperatorTopology de Hilbert](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/.lake/packages/mathlib/Mathlib/Analysis/InnerProductSpace/WeakOperatorTopology.lean>)
foi lido inteiro. `ContinuousLinearMapWOT.tendsto_iff_forall_inner_apply_tendsto`, na linha 48,
caracteriza WOT por todos os coeficientes `⟨y, A x⟩`. Não contém o teorema monotônico central.

`WeakDual.isCompact_closedBall`, em
[WeakDual.lean](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/.lake/packages/mathlib/Mathlib/Analysis/Normed/Module/WeakDual.lean:268>), foi lido integralmente:
para `[ProperSpace 𝕜]`, a pré-imagem de uma bola fechada do dual forte é compacta no dual fraco-*.
É um resultado sobre funcionais escalares; não identifica por si só B(H) com um dual ou
fornece a ordem de operadores nessa topologia.

`ContinuousLinearMap.isCompact_image_coe_closedBall`, em
[Completeness.lean](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/.lake/packages/mathlib/Mathlib/Analysis/Normed/Operator/Completeness.lean:156>), exige
**`[ProperSpace F]` no contradomínio**. Não serve diretamente como compacidade SOT da bola de
operadores com contradomínio H geral. A rota WOT exigiria transporte/reconstrução adicional;
o módulo local de limites monótonos já evita esse trabalho.

`tendsto_atTop_isLUB`, em
[MonotoneConvergence.lean](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/.lake/packages/mathlib/Mathlib/Topology/Order/MonotoneConvergence.lean:89>), exige
`SupConvergenceClass` no espaço topológico alvo. Não assumir essa classe para B(H) com a
norma de operador nem usá-la para pressupor a convergência forte que se quer provar.
Da mesma forma, usar **`IsLUB`** diretamente: não postular uma estrutura de reticulado completo
ou `sSup` arbitrário nos operadores para tratar supremos positivos dirigidos.

[VonNeumannAlgebra/Basic.lean](<C:/IALD/Artigo/Haja_Luz/A Ponte e o Um/Nós/tgl_kernel/.lake/packages/mathlib/Mathlib/Analysis/VonNeumannAlgebra/Basic.lean>)
foi lido integralmente. O arquivo distingue `WStarAlgebra` abstrata por predual e a álgebra
concreta por bicomutante, e deixa equivalências estruturais como projeto futuro no cabeçalho.
Essas declarações não oferecem uma equivalência pronta entre normalidade e SOT limitada.

## 6. Contrato honesto da conclusão a implementar

[OPEN — implementação pelo pai] Provar o enunciado de preservação de **todo supremo positivo
monótono dirigido** da seção 2. Esse enunciado tem conteúdo de ordem independente:
o limite forte não é dado na hipótese, mas produzido pelo teorema local e identificado por unicidade.
Ele pode fundamentar a declaração de normalidade no sentido da ordem para a amplificação.
**Não definir normalidade como alias de `fibre_tendsto_of_uniformly_bounded`**, nem substituir
`IsLUB` por uma condição que já pressuponha sua preservação.

A equivalência com continuidade ultra-fraca/predual não foi provada nesta consulta e não é
necessária à rota curta acima. Os resultados próprios do domínio da esperança não autorizam
transferir a normalidade dessa esperança à amplificação sem fazer a composição indicada.
Nenhuma implementação Lean, memória, raiz, monólito ou fonte existente foi escrita nesta subtarefa.
Nenhuma mudança de gate ou conclusão física é reivindicada.

## 7. Identidade dos artefatos consultados

[REAL — SHA-256 calculados por script nesta consulta]

| Artefato | SHA-256 |
|---|---|
| `kernel/TGLExt/MonotoneOperatorLimit.lean` | `c08824988f1bf53b9aeb11c582703b099f9382b1259c2e41029a9a8fc40edda5` |
| `build/TGLExt/MonotoneOperatorLimit.olean` | `a0fe4a41dd846b286e0290896347510e1238a6dd316390aa707836dba14bdec8` |
| `kernel/TGLExt/ExpectationNormality.lean` | `e941f703e74773f215d617235caf2e9523a44554f094beebd51a68aa6a45578e` |
| `kernel/TGLV350/L2BoundedStrongContinuity.lean` | `afc18b6b9c10d8427ef5f5750ae612b22cae485950e7577b6122273b9bf0f5dc` |

A inspeção via `Lean --stdin` carregou os módulos existentes, confirmou as assinaturas e os
axiomas mencionados e terminou com exit 0. O arquivo `.trace` preexistente do módulo central
contém a auditoria histórica; não foi tratado como recompilação atual.
O único arquivo persistente criado por esta consulta é esta nota.
