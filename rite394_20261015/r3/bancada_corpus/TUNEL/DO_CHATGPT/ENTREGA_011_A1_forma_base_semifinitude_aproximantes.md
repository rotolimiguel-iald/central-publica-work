[REAL — A1 parcial: forma dual na base, densidade do domínio e aproximantes crescentes verificados; OPEN — traço canônico ainda não construído]

# Entrega 011 · A1 — forma, semifinitude e recuperação na base

Responde à ORDEM_011. A1(a) e A1(c) permanecem pagos; A1(b) NÃO PAGO. O resultado novo é uma construção efetiva de aproximantes positivos NA MESMA BASE, recuperando a forma dual inteira, somada à afiliação da forma na base e à densidade WOT do domínio escalar. Não se entrega habitante de RegularCoreTraceData nem se move gate.

As fichas de aproveitamento antecederam cada módulo e estão anexadas ao final. Nenhuma rederivação do integral, GNS, resolvente ou equivalência F=M foi introduzida.

## Critérios

| Critério | Estado | Evidência |
|---|---|---|
| A1(a), contrato forte e recusa do zero legado | PAGO, preservado | manifesto anterior inteiro reconferido |
| A1(b), habitante para todo SiteProfile ou impossibilidade tipada | NÃO PAGO | peso e aproximação construídos; rota modular/perturbação ainda aberta |
| A1(c), auditoria no trio | PAGO no delta | três módulos: 17 teoremas + 2 definições, todos rc0 sem avisos |

## Resultados e próxima obrigação

, para não ser refeito

1. `fixedFormOnBase` transporta uma forma afiliada ao fixo F para uma forma afiliada à própria base M. A afiliação é demonstrada pelos unitários de M′, amplificados por `fibre`, e pela identificação F=fibre(M). O transporte não pressupõe output limitado.
2. `baseDualWeight` é essa forma para o integral dual existente. Zero, soma, escala, ordem, fidelidade, bimódulo e normalidade por supremos internos estão provados. Avaliar no mesmo Ω dá exatamente `scalarDualWeight`, inclusive no infinito. Unidade tem valor infinito em todo vetor não zero; a média quadrática de comprimento 1 tem valor escalar 1.
3. `scalarWeight_square_finite_wot_closure` prova que nν={a∈N:ν(a*a)<∞} é WOT-denso no mesmo core N, reutilizando a aproximação forte anterior. `scalarWeight_unit_not_square_finite` recusa a unidade nesse domínio. O enunciado Lean não identifica topologias preduais arbitrárias.
4. `exists_base_moreau_approximant` produz, para c>0, D_c∈M, 0≤D_c≤cI, tal que a forma limitada de fibre(D_c) é o mínimo de q_A(w)+c‖w−v‖². Usa o resolvente já construído de A/c e c(I−R_c), sem refazer a representação do operador.
5. `exists_monotone_base_dual_approximation` produz D_n∈M positivo, crescente na ordem de operadores, e para TODO vetor da representação regular:

    q_A(v) = sup_n ofReal Re⟨v,fibre(D_n)v⟩.

A recuperação inclui q_A(v)=∞. Quando o supremo é finito, o bound de energia dá w_n→v, e o subnível fechado da mesma forma conclui a igualdade. Não foi presumida densidade do domínio finito da forma individual.

O novo delta tem três módulos, 17 teoremas e duas definições, totalizando 19 declarações auditadas no trio. São fornecedores formais de A1; não são funções novas no Python e não foram embutidos no monólito.

## A obrigação imediata, sem reiniciar o que já foi pago

Ponham-se M=theFactorObject P, N=regularCoreAlgebra P, ι=fibre e ψ∈M_*^+.
Os aproximantes agora EXISTEM em kernel. A próxima construção é

    m_A(ψ) := sup_n ofReal Re ψ(D_n(A)).

Ela deve usar funcionais normais positivos da MESMA M. Faltam tipar essa interface e provar aditividade/homogeneidade/semicontinuidade em ψ, a avaliação m_A(ω_v)=baseDualWeight(A)(v), e a extensionalidade necessária para transportar as leis em A.

Um fornecedor suficiente, precisamente delimitado, é: para cada funcional normal positivo ψ sobre esta M existe uma família v_k na Hilbert da base, com soma_k ‖v_k‖²<∞, tal que ψ(D)=soma_k ⟨v_k,Dv_k⟩ para todo D∈M. Convergência monótona dá então m_A(ψ)=soma_k baseDualWeight(A)(v_k). Alternativamente, uma extensão normal positiva ambiente com a mesma propriedade serve. Não presumir que todo ψ seja um único estado vetorial nem tratar um funcional positivo arbitrário como normal.

As buscas dirigidas no kernel e na Analysis da mathlib estão preservadas. A mathlib declara WStarAlgebra com existência abstrata de predual; isso não fornece por si só a interface concreta, sua identificação com esta representação ou o lema de decomposição. `GNSBridge` é um fornecedor de funcional finito em matrizes, não essa ponte infinita. O nome correto `exists_dualFormRepresentation` foi conferido e registrado no adendo da ficha; uma busca pelo nome com sublinhados foi negativa apenas por grafia.

## O que permanece depois dessa obrigação

As pontes 2–4 de `LACUNAS_A1.md` continuam: implementação modular do mesmo peso, gerador positivo afiliado h com h^{it}=Λ_t e perturbação por h^{-1} produzindo o traço fiel normal semifinito, tracial e com τ∘θ_s=e^{-s}τ. A invariância ν∘θ_s=ν não é essa escala; o peso ν não fornece τ diretamente. Não há parede contra a existência de τ neste marco.

Correção de exigência, ao lado do texto anterior: para o peso não tracial ν, usar o domínio nν fracamente denso como critério de semifinitude; não cobrar o campo de todos os minorantes positivos finitos de cada A, que pertence aqui ao contrato final do TRAÇO. Esse campo final não foi enfraquecido. A consulta independente registra um contraexemplo analítico de peso não tracial, explicitamente não Lean. Referência primária: Hiai, definições 7.1 e 8.1/8.5, https://arxiv.org/pdf/2004.02383.

Os três marcos não alteram o gate, não produzem dados físicos e não autorizam iniciar A2 antes de resolver A1. Canonicalidade/normalização não é inferida da mera lei de escala.


## Artefatos e reprodução

- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V351ExtendedBaseDualWeight.lean` — SHA256 `1ea9226e3fe1ee75bc66178f575f47c0207e80dca34a0113efd0c0f099b7cd87`; objeto `75d88c1f7a929319f789cc7f7da9d2fd49995f9b2ef3128aaca65c5ff7827c81`; 14 declarações. Revisão: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\revisao\REVIEW_A1_BASE_ESTENDIDA_FINAL.md`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V351ScalarWeightSemifiniteness.lean` — SHA256 `f5e7e85b034949be6517286f60c692d3d97d29c341aeba42a1f7172b7e610c2a`; objeto `36361c7abcb29c182d36457c5b69371217e5208936e2c2bec6a82974dbb3689b`; 2 declarações. Revisão: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\revisao\REVIEW_A1_SEMIFINITUDE_FINAL.md`.
- `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V351BaseMoreauApproximants.lean` — SHA256 `45d47db69249a1873c8059b0a9e85f74c0af6920e31ce48b787a4c33e4fde49d`; objeto `8d9403a721b132f34c97780a46288b1beb9287c9a1b00e8beb9c632490382176`; 3 declarações. Revisão: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\revisao\REVIEW_A1_APROXIMANTES_BASE_FINAL.md`.

Manifesto: `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\MANIFESTO_A1_BASE_SEMIFINITUDE_APROXIMANTES.json` — SHA256 `c0ece778e275083bc58dbf515d0c4b02625f4b79489557232ef7c5aef5adf348`. Contém fontes, objetos, fichas, revisões, auditorias e tentativas por hash. O manifesto anterior tem 39 arquivos, todos reconferidos sem alteração. Monólito local e canônico continuam idênticos: `95e8cf8eb0b33c5d65e244195021b71977cca1a91836ef0d314964a8e2f97c43`.

Compilação com Lean 4.31.0 pinado (PowerShell):

```powershell
& C:\Python314\python.exe -X utf8 -B 'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\compile_a1.py' kernel/TGLExt/V351ExtendedBaseDualWeight.lean
& C:\Python314\python.exe -X utf8 -B 'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\compile_a1.py' kernel/TGLExt/V351ScalarWeightSemifiniteness.lean
& C:\Python314\python.exe -X utf8 -B 'C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\compile_a1.py' kernel/TGLExt/V351BaseMoreauApproximants.lean
```

Cada comando cria uma tentativa nova e compila apenas o módulo no build isolado. As dependências antigas são binários herdados e verificados por hash, não uma recompilação integral. `DEPENDENCIAS_A1_MARCO_BASE.json` registra 384 entradas: 380 herdadas e quatro V351, contando o contrato anterior. A revisão independente reproduz os módulos em árvore própria. Não executar os scripts autorais de registro/auditoria novamente: eles preservam saídas imutáveis e recusam sobrescrita. As sondas adulteradas podem ser recompiladas pelo mesmo compilador, esperando rc1.

## Axiomas e controles

- `TGLV351.fixedFormOnBase`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.baseDualWeight`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.baseDualWeight_value`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.scalarDualWeight_eq_base_evaluation`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.baseDualWeight_zero`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.baseDualWeight_add`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.baseDualWeight_scale`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.baseDualWeight_bimodule`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.baseDualWeight_mono`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.baseDualWeight_faithful`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.baseDualWeight_preserves_internal_isLUB`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.baseDualWeight_bounded_value`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.baseDualWeight_unit_infinite`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.baseDualWeight_averageSquare`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.scalarWeight_square_finite_wot_closure`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.scalarWeight_unit_not_square_finite`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.dualResolvent_minimum_energy_value`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.exists_base_moreau_approximant`: `propext`, `Classical.choice`, `Quot.sound`.
- `TGLV351.exists_monotone_base_dual_approximation`: `propext`, `Classical.choice`, `Quot.sound`.

O teste da média 1→2 e o teste da energia mínima acrescida de +1 foram recusados por erros reais de elaboração, não por dependências ausentes. Tentativas com `sorryAx` automático foram recusadas integralmente. A tentativa de semifinitude inicialmente sem objeto de dependência é classificada separadamente como falha de ambiente. Todas as tentativas e snapshots permanecem; o manifesto lista seus códigos. Uma tentativa intermediária Moreau rc0 com aviso de tática redundante foi substituída por uma final sem avisos, preservando o histórico.

## Escopo de integração

A gerência pode auditar estes três módulos como fornecedores de A1. Eles não devem acender `qgf_continuous_modular_realization_constructed`: não existe ainda o traço exigido. Não houve rodada integral do Python porque nenhum byte do programa foi alterado. A2–A7, natureza, física, memórias, selos e espelho ficaram fora deste marco. A entrega é parcial e o objetivo A1 permanece ativo.

## Fichas anexas


---

[REAPROVEITAMENTO — ANTES DO CÓDIGO FORMAL]

# A1: forma dual na base

2026-09-14T08:39:58.871426

Consumidor: `RegularCoreTraceData P`, via a ponte 1 de `LACUNAS_A1.md` e a perturbação do peso. O alvo local é transportar `AffiliatedPositiveForm (dualFixedCore P)` para `AffiliatedPositiveForm (theFactorObject P)`, usando `testVectorIsometry` e provando afiliação. A avaliação no mesmo Ω deve ser igual ao peso escalar em ENNReal, sem hipótese de finitude.

- **CONSUMIDOR** `structure RegularCoreTraceData`, `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V351RegularCoreTraceContract.lean:43`; SHA256 `3694175f8ef5bcf5848d88bd8061abf8546480873964ebfdc19dd41ad05928f0`. A1(b): o traço neste cone e nesta ação. A ponte de base integra a identificação do peso usado para a perturbação; não fornece ainda o traço.

```lean
structure RegularCoreTraceData (P : SiteProfile) where
```

- **REUSAR** `structure AffiliatedPositiveForm`, `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350DualClosedForm.lean:84`; SHA256 `69a47c01fc1a366a61b871b86e1d7114e43e865b025a04cd57918f09ed7c5be7`. Forma positiva fechada estendida com invariância sob o comutante unitário; mesma tipagem, agora na base.

```lean
structure AffiliatedPositiveForm (N : VonNeumannAlgebra H) extends ClosedPositiveForm H where
```

- **ADAPTAR** `def dualFixedWeight`, `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350DualFixedWeightLaws.lean:50`; SHA256 `93fda2f3b9a2c519d13e1356de7fcebd2f273d3d0078eeac6d505af795ae9c75`. Fornecedor retorna AffiliatedPositiveForm(dualFixedCore P); exigimos saída em AffiliatedPositiveForm(theFactorObject P).

```lean
def dualFixedWeight (P : TGLExt.SiteProfile) (A : PositiveCoreInput P) :
    AffiliatedPositiveForm (dualFixedCore P) :=
```

- **REUSAR** `theorem dualFixedWeight_bimodule`, `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350DualFixedWeightLaws.lean:93`; SHA256 `93fda2f3b9a2c519d13e1356de7fcebd2f273d3d0078eeac6d505af795ae9c75`. Transportar pela equivalência e pela isometria já construídas.

```lean
theorem dualFixedWeight_bimodule (P : TGLExt.SiteProfile)
    (A : PositiveCoreInput P) (B : (dualFixedCore P).toStarSubalgebra) :
    dualFixedWeight P (A.conjugate B) =
      (dualFixedWeight P A).conjugate B.val B.property := by
```

- **REUSAR** `theorem dualFixedWeight_preserves_internal_isLUB`, `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350DualFixedWeightLaws.lean:126`; SHA256 `93fda2f3b9a2c519d13e1356de7fcebd2f273d3d0078eeac6d505af795ae9c75`. Normalidade do mesmo integral, aplicada aos vetores da base.

```lean
theorem dualFixedWeight_preserves_internal_isLUB (P : TGLExt.SiteProfile)
    (A : ι → (regularCoreAlgebra P).toStarSubalgebra)
    (S : (regularCoreAlgebra P).toStarSubalgebra)
    (hpos : ∀ i, 0 ≤ A i) (hmono : Monotone A) (hS : IsLUB (Set.range A) S) :
    IsLUB (Set.range (fun i => dualFixedWeight P ⟨(A i).val, (A i).property, hpos i⟩))
      (dualFixedWeight P ⟨S.val, S.property, positive_internal_isLUB_nonneg P A S hpos hS⟩) := by
```

- **REUSAR** `def fixedBaseEquiv`, `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350FixedBaseEquivalence.lean:29`; SHA256 `6b4cda490d27efc86fdac21e57b91c30778477221d08ff9c90f31a1bf8b8f278`. Equivalência concreta entre M e F, não hipótese abstrata.

```lean
def fixedBaseEquiv (P : SiteProfile) :
    (theFactorObject P).toStarSubalgebra ≃⋆ₐ[ℂ] (dualFixedCore P).toStarSubalgebra :=
```

- **REUSAR** `theorem dualFixedCore_eq_amplified_base`, `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350FixedCoreBaseIdentification.lean:21`; SHA256 `0454ce14669be84c8384143a8ace33b7e795bc5b262355afc97284d1a963f4a1`. Identificação de cada operador fixo com fibre de um elemento da base.

```lean
theorem dualFixedCore_eq_amplified_base (P : SiteProfile)
    (B : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P)) :
    B ∈ dualFixedCore P ↔ ∃ C ∈ theFactorObject P, B = fibre C := by
```

- **REUSAR** `def testVectorIsometry`, `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350L2Order.lean:14`; SHA256 `763b6ebd38541bb028c6a007c492b5155fd5859d2bc9572a0016ab8bef93f46d`. H →ₗᵢ[ℂ] L²(R,H); fornece continuidade e linearidade para restrição da forma.

```lean
def testVectorIsometry : H →ₗᵢ[ℂ] RegularHilbert H where
```

- **REUSAR** `def fibreRepresentation`, `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350L2OperatorLift.lean:53`; SHA256 `bbdf07f64bc1abdfb50fed8420911c868a11cc6c8036b6f06167f021a1db7465`. Amplifica o unitário de M′ para provar afiliação da forma restrita.

```lean
def fibreRepresentation : (H →L[ℂ] H) →⋆ₐ[ℂ] (RegularHilbert H →L[ℂ] RegularHilbert H) where
```

- **ADAPTAR** `theorem scalarDualWeight_bounded_base_value`, `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350ScalarDualWeight.lean:77`; SHA256 `e20dc5262ec98b62c8a6797fd07492e584a03fefefd0dd87b1666484dd72bc53`. A hipótese exige output limitado; o novo caso cobrirá ENNReal inclusive infinito.

```lean
theorem scalarDualWeight_bounded_base_value (P : SiteProfile) (A : PositiveCoreInput P)
    (D : (theFactorObject P).toStarSubalgebra)
    (hrep : ∀ v, dualQuadraticIntegral A.val v =
      ENNReal.ofReal (inner ℂ v (fibre D.val v)).re) :
    scalarDualWeight P A = ENNReal.ofReal (inner ℂ (hOmega P) (D.val (hOmega P))).re := by
```

- **REUSAR** `theorem scalarDualWeight_square_finite_strong_density`, `C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350ScalarDualWeight.lean:66`; SHA256 `e20dc5262ec98b62c8a6797fd07492e584a03fefefd0dd87b1666484dd72bc53`. Não substituir a semifinitude de peso por exigência mais forte de minorantes finitos de cada positivo.

```lean
theorem scalarDualWeight_square_finite_strong_density (P : SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra) :
    (∀ h : ℝ, 0 < h → dualQuadraticIntegral
      (star (A.val * regularAverage P h) * (A.val * regularAverage P h)) (regularVacuum P) < ⊤) ∧
    (∀ h : ℝ, A.val * regularAverage P h ∈ regularCoreAlgebra P) ∧
    (∀ v, Tendsto (fun h : ℝ => (A.val * regularAverage P h) v) (𝓝[>] 0) (𝓝 (A.val v))) := by
```

As seis modalidades de busca de A1 constam da ficha original e de seus adendos, cujos hashes são referidos no JSON. As duas buscas adicionais estão registradas integralmente. Não se afirma ausência universal de fornecedor.

Este marco não paga A1(b): a identificação abstrata do cone/predual e as pontes modulares/gerador/traço continuam explícitas. Não se cria nova camada Python nem se altera o gate.

---

[REAPROVEITAMENTO — ANTES DO CÓDIGO FORMAL]

# A1: semifinitude pelo domínio do peso

A1(b), LACUNAS_A1.md item 1: semi-finitude usual de scalarDualWeight; não usar o campo de minorantes do contrato tracial para um peso não tracial.

Alvo exato:
```lean
closure {A : RegularHilbert (TowerHilbert P) →WOT[ℂ] RegularHilbert (TowerHilbert P) | A.toCLM ∈ regularCoreAlgebra P ∧ HasFiniteScalarSquare P A.toCLM} = {A | A.toCLM ∈ regularCoreAlgebra P}
```

ADAPTAR: aplicar strong_tendsto_wot à aproximação forte já paga, e a clausura WOT ao outro sentido. Não reconstruir médias.

## def HasFiniteScalarSquare

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350ScalarWeightDomain.lean:14 · SHA256 e83ada9b5abbf2c179c28b03d3c020be83861681ba3ae450999c1c64ea8e2f0f

```lean
def HasFiniteScalarSquare (P : SiteProfile)
    (A : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P)) : Prop :=
```

## def scalarWeightLeftIdeal

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350ScalarWeightDomain.lean:43 · SHA256 e83ada9b5abbf2c179c28b03d3c020be83861681ba3ae450999c1c64ea8e2f0f

```lean
def scalarWeightLeftIdeal (P : SiteProfile) :
    Submodule ℂ (regularCoreAlgebra P).toStarSubalgebra where
```

## theorem scalarDualWeight_square_finite_strong_density

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350ScalarDualWeight.lean:66 · SHA256 e20dc5262ec98b62c8a6797fd07492e584a03fefefd0dd87b1666484dd72bc53

```lean
theorem scalarDualWeight_square_finite_strong_density (P : SiteProfile)
    (A : (regularCoreAlgebra P).toStarSubalgebra) :
    (∀ h : ℝ, 0 < h → dualQuadraticIntegral
      (star (A.val * regularAverage P h) * (A.val * regularAverage P h)) (regularVacuum P) < ⊤) ∧
    (∀ h : ℝ, A.val * regularAverage P h ∈ regularCoreAlgebra P) ∧
    (∀ v, Tendsto (fun h : ℝ => (A.val * regularAverage P h) v) (𝓝[>] 0) (𝓝 (A.val v))) := by
```

## theorem strong_tendsto_wot

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350RegularNormality.lean:19 · SHA256 bcd49e92800bf99d7770bb9969879be02a9768f129ce842ae2f39cefaca3cc0a

```lean
theorem strong_tendsto_wot {ι : Type*} {l : Filter ι}
    (T : ι → (H →L[ℂ] H)) (B : H →L[ℂ] H)
    (hstrong : ∀ v, Tendsto (fun i => T i v) l (𝓝 (B v))) :
    Tendsto (fun i => ContinuousLinearMapWOT.ofCLM (T i)) l
      (𝓝 (ContinuousLinearMapWOT.ofCLM B)) := by
```

## theorem regularCore_wot_closed

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350RegularTopology.lean:39 · SHA256 13c92b1d8948bc4d2c3891d4cbfa9bf43ac353a95e9126e2c128b1379db0ebd5

```lean
theorem regularCore_wot_closed (P : TGLExt.SiteProfile) :
    IsClosed {A : RegularHilbert (TGLExt.TowerHilbert P) →WOT[ℂ]
      RegularHilbert (TGLExt.TowerHilbert P) | A.toCLM ∈ regularCoreAlgebra P} :=
```

## theorem baseDualWeight_unit_infinite

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V351ExtendedBaseDualWeight.lean:126 · SHA256 1ea9226e3fe1ee75bc66178f575f47c0207e80dca34a0113efd0c0f099b7cd87

```lean
theorem baseDualWeight_unit_infinite (P : SiteProfile) (v : TowerHilbert P) (hv : v ≠ 0) :
    (baseDualWeight P (positiveUnit P)).value v = ⊤ := by
```

A ficha inicial de A1 guarda as seis modalidades de busca. Consulta independente: revisao/CONSULTA_A1_RESTRICAO_FORMAS_BASE.md. A distinção peso/traço é verificada na definição 7.1 de Hiai, https://arxiv.org/pdf/2004.02383. Não se declara aqui densidade na topologia de norma nem construção do traço.

---

[REAPROVEITAMENTO — ANTES DO CÓDIGO]

# A1: aproximantes positivos na base

2026-09-14T08:54:01.909739-03:00

A1(b), ponte 1: valores preduais do peso dual; depois ponte 4 para RegularCoreTraceData

Para P, A∈N positivo e c>0: produzir D_c∈M, 0≤D_c≤c I, cujo valor amplificado é inf_w(q_A(w)+c||w-v||²); depois crescimento e sup_c q_Dc=q_A. Nenhum traço é prometido por este lema.

ADAPTAR resolvente do input A/c, formar c(1-R_c) no fixo F e usar a equivalência concreta F=M. NOVO apenas as identidades variacionais e aproximação necessárias para o predual; não reconstruir resolvente ou integral.

## structure RegularCoreTraceData

CONSUMIDOR

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V351RegularCoreTraceContract.lean:43

SHA256 `3694175f8ef5bcf5848d88bd8061abf8546480873964ebfdc19dd41ad05928f0`

```lean
structure RegularCoreTraceData (P : SiteProfile) where
```

## def baseDualWeight

ADAPTAR: aproximação por operadores positivos da mesma base

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V351ExtendedBaseDualWeight.lean:39

SHA256 `1ea9226e3fe1ee75bc66178f575f47c0207e80dca34a0113efd0c0f099b7cd87`

```lean
def baseDualWeight (P : SiteProfile) (A : PositiveCoreInput P) :
    AffiliatedPositiveForm (theFactorObject P) :=
```

## theorem exists_dualResolvent_fixed

REUSAR

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350DualResolventFixed.lean:78

SHA256 `1d1805ed2f6544c3a11cdfecf503258448681ef49376af4409d80de7d8570056`

```lean
theorem exists_dualResolvent_fixed (P : TGLExt.SiteProfile)
    (A : RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ]
      RegularHilbert (TGLExt.TowerHilbert P))
    (hA : A ∈ regularCoreAlgebra P) (hpos : 0 ≤ A) :
    ∃ R : RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ]
      RegularHilbert (TGLExt.TowerHilbert P),
      R ∈ regularCoreAlgebra P ∧ 0 ≤ R ∧ R ≤ 1 ∧
      (∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v))) ∧
      (∀ s : ℝ, dualAmbient s R = R) := by
```

## theorem dualResolvent_limit_minimizes_energy

REUSAR

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350DualVariational.lean:76

SHA256 `c375e63d7cc8415d90c8663e9230b9696171ba3138f8b1fe250bb5898938cee0`

```lean
theorem dualResolvent_limit_minimizes_energy
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v)))
    (v w : RegularHilbert H) : dualEnergy A v (R v) ≤ dualEnergy A v w := by
```

## theorem dualResolvent_limit_energy_identity

REUSAR

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350DualEnergyOnResolvent.lean:56

SHA256 `020b86bf18e19388c8716b046fc0276fde43216a2782d52de6c27dfabc941c5d`

```lean
theorem dualResolvent_limit_energy_identity
    (A R : RegularHilbert H →L[ℂ] RegularHilbert H) (hA : 0 ≤ A)
    (hlim : ∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v)))
    (v : RegularHilbert H) :
    (dualQuadraticIntegral A (R v)).toReal = (inner ℂ (R v) (v-R v)).re := by
```

## theorem dualQuadraticIntegral_smul_operator

REUSAR

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350DualQuadraticLaws.lean:61

SHA256 `7085d5ad460720e87ea5e1e3cc8bcbf5b55193be77b2ba283988fbf03120c1f3`

```lean
theorem dualQuadraticIntegral_smul_operator (r : ℝ) (hr : 0 ≤ r)
    (A : RegularHilbert H →L[ℂ] RegularHilbert H) (v : RegularHilbert H) :
    dualQuadraticIntegral (r • A) v = ENNReal.ofReal r * dualQuadraticIntegral A v := by
```

## theorem dualFixedCore_eq_amplified_base

REUSAR

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350FixedCoreBaseIdentification.lean:21

SHA256 `0454ce14669be84c8384143a8ace33b7e795bc5b262355afc97284d1a963f4a1`

```lean
theorem dualFixedCore_eq_amplified_base (P : SiteProfile)
    (B : RegularHilbert (TowerHilbert P) →L[ℂ] RegularHilbert (TowerHilbert P)) :
    B ∈ dualFixedCore P ↔ ∃ C ∈ theFactorObject P, B = fibre C := by
```

## def fixedBaseOrderIso

REUSAR

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350FixedBaseEquivalence.lean:44

SHA256 `6b4cda490d27efc86fdac21e57b91c30778477221d08ff9c90f31a1bf8b8f278`

```lean
def fixedBaseOrderIso (P : SiteProfile) :
    (theFactorObject P).toStarSubalgebra ≃o (dualFixedCore P).toStarSubalgebra where
```

## theorem exists_dual_form_representation

não usar por homônimo

C:\IALD\Central de Patentes\Chatgpt\TETELESTAI_V351_FECHO_MATEMATICO\kernel\TGLExt\V350DualFormRepresentation.lean:?

SHA256 `842848ee7e13c1ab8d7c0d189e33db5a5e459f76dde0ab54c0265719043a487c`

```lean
NAO_LOCALIZADO_POR_ESSE_NOME
```

Busca adicional e seis modalidades prévias: comandos, resultados e hashes no JSON. Não se afirma ausência universal de fornecedor. A dependência imediata é a representação no predual; a aceitação A1(b) continua aberta até existir o traço.


Adendo da ficha dos aproximantes (grafia do fornecedor):

```json
{
  "timestamp": "2026-09-14T08:58:10.474846-03:00",
  "correction": "O nome correto do fornecedor é exists_dualFormRepresentation. A busca por exists_dual_form_representation foi negativa por grafia, não por ausência de matemática. Fonte agora lida integralmente na região.",
  "file": "C:\\IALD\\Central de Patentes\\Chatgpt\\TETELESTAI_V351_FECHO_MATEMATICO\\kernel\\TGLExt\\V350DualFormRepresentation.lean",
  "line": 137,
  "sha256": "842848ee7e13c1ab8d7c0d189e33db5a5e459f76dde0ab54c0265719043a487c",
  "statement": "theorem exists_dualFormRepresentation (P : TGLExt.SiteProfile)\n    (A : RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ]\n      RegularHilbert (TGLExt.TowerHilbert P))\n    (hmem : A ∈ regularCoreAlgebra P) (hA : 0 ≤ A) :\n    ∃ R : RegularHilbert (TGLExt.TowerHilbert P) →L[ℂ]\n      RegularHilbert (TGLExt.TowerHilbert P),\n    ∃ T S : dualFormSupport A hA →ₗ.[ℂ] dualFormSupport A hA,\n      R ∈ regularCoreAlgebra P ∧ 0 ≤ R ∧ R ≤ 1 ∧\n      (∀ v, Tendsto (fun n => dualCutResolvent n A v) atTop (𝓝 (R v))) ∧\n      T.IsClosed ∧ Dense (T.domain : Set (dualFormSupport A hA)) ∧ IsSelfAdjoint T ∧\n      S.IsClosed ∧ Dense (S.domain : Set (dualFormSupport A hA)) ∧ IsSelfAdjoint S ∧\n      (∀ x : S.domain, 0 ≤ (inner ℂ (x : dualFormSupport A hA) (S x)).re) ∧\n      partialOperatorSquare S = T ∧\n      (∀ w : RegularHilbert (TGLExt.TowerHilbert P), dualQuadraticIntegral A w < ⊤ ↔\n        ∃ x : S.domain, ((x : dualFormSupport A hA) : RegularHilbert (TGLExt.TowerHilbert P)) = w) ∧\n      (∀ x : S.domain, dualQuadraticIntegral A (x : dualFormSupport A hA) =\n        ENNReal.ofReal (‖S x‖^2)) ∧\n      (∀ u : dualFormSupport A hA, ∃ x : T.domain,\n        ((x : dualFormSupport A hA) : RegularHilbert (TGLExt.TowerHilbert P)) = R u ∧\n        (x : dualFormSupport A hA) + T x = u) := by",
  "decision": "A representação completa produz operador e raiz no suporte da forma. Não fornece diretamente a sequência limitada crescente na base exigida pela avaliação predual. Reusar os resolventes e a identidade de energia já pagos para obter essa sequência, sem reconstruir a representação."
}
```
