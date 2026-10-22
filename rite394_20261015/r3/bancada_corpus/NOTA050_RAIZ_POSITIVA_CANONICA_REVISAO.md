# Revisão independente050 — raiz positiva e identificação canônica

[DERIVED — análise; nenhuma nova prova Lean ou compilação nesta revisão]

O alvo planejado `S†S=Δ=T_(2c)`, acompanhado da autoadjunticidade e positividade de T_c e da igualdade de operadores parciais `T_c²=Δ`, prova que T_c é uma raiz positiva autoadjunta de Δ. Para afirmar unicidade formal entre todas as raízes, a conclusão deve quantificar um operador parcial Q arbitrário, não apenas membros da família T_d, e demonstrar `Q=T_c` a partir de Q positivo, autoadjunto e `Q²=Δ` com igualdade de domínios. Batizar uma definição de sqrt não substitui esse teorema.

## API local medida

[REAL — somente leitura dos fontes instalados] Em `Mathlib/Analysis/SpecialFunctions/ContinuousFunctionalCalculus/Rpow/Basic.lean:283` existe:

```lean
lemma CFC.sqrt_unique {a b : A} (h : b * b = a)
    (hb : 0 ≤ b := by cfc_tac) : CFC.sqrt a = b
```

O contexto inclui uma álgebra ordenada com cálculo funcional contínuo não unital, `StarOrderedRing`, `NonnegSpectrumClass`, separação e estrutura topológica. A API aplica-se aos operadores contínuos limitados no Hilbert. Não é uma API pronta para `LinearPMap` não limitado. `CFC.mul_self_eq_mul_self_iff` (linha294) também pertence a esse contexto.

O arquivo `Mathlib/Analysis/InnerProductSpace/LinearPMap.lean` fornece `adjoint_apply_eq`, `IsFormalAdjoint.le_adjoint`, `IsSelfAdjoint.dense_domain` e `IsSelfAdjoint.isClosed`. A busca global pelos nomes de cálculo funcional de Borel/medida espectral e pelas associações sqrt–LinearPMap não encontrou uma API correspondente. Isto delimita a investigação realizada; não afirma impossibilidade de desenvolver tal teoria.

A rota escalar usa `Real.sqrt_sq (h : 0 ≤ x)` em `Mathlib/Analysis/Real/Sqrt.lean:181`, positividade da exponencial e `Real.exp_add`. Em049, `continuous_modular_graph_iff` e `continuous_modular_domain_iff` já descrevem exatamente o operador e seu domínio ponderado. Não foi compilado qualquer fragmento novo nesta análise.

## O que a representação multiplicativa paga

[DERIVED] Escrevendo m(ξ)=exp(-2cξ), a raiz escalar não negativa é sqrt(m(ξ))=exp(-cξ). Assim, o operador de multiplicação M_sqrt(m), no domínio `{f∈L² : sqrt(m)f∈L²}`, coincide com T_c. Esse domínio é o domínio da raiz, não necessariamente o domínio de Δ=M_m.

Provar essa igualdade de gráficos é útil e legítimo: não depende de autovetores generalizados nem troca igualdade quase em toda parte por igualdade de representantes. Porém, a unicidade da raiz escalar identifica a raiz entre multiplicadores não negativos. Sozinha não prova que qualquer operador positivo autoadjunto Q com Q²=M_m é esse multiplicador. Esse último passo é justamente uma versão do teorema de unicidade de raiz não limitada.

Um cálculo funcional específico de multiplicadores pode ser construído e ter as propriedades pertinentes demonstradas. Definir apenas a notação `sqrtΔ := T_c` ou `sqrtΔ := M_sqrt(m)` não deve ser apresentado como prova da caracterização abstrata que falta.

## Rota intrínseca disponível a partir da parametrização049

[DERIVED — proposta de alvo, ainda não formalizada] Sejam A=A_c e B=B_c os multiplicadores limitados já construídos. Defina C=A². Com as relações do grafo e o quadrado de T, é possível demonstrar as duas identidades de resolvente:

- Para f∈H: C f∈D(Δ) e (I+Δ)(C f)=f.
- Para x∈D(Δ): C(x+Δx)=x.

Em termos da parametrização, Δ(A²f)=B²f e A²+B²=I; a identidade inversa também segue de Bx=Ay, By=Az e comutação de A e B. O resolvente C fica determinado por Δ, não escolhido independentemente.

Provando A e B positivos como operadores limitados, a unicidade CFC limitada fornece `A=CFC.sqrt C` e `B=CFC.sqrt(I-C)`. O grafo concreto de T torna-se então

`{(CFC.sqrt C h, CFC.sqrt(I-C) h) : h∈H}`, com domínio `range(CFC.sqrt C)`.

Este é um vínculo intrínseco por cálculo funcional genuíno de operadores limitados. Avança além da simples nomeação de uma raiz. Para terminar a unicidade não limitada no kernel, ainda é preciso demonstrar que uma raiz positiva autoadjunta arbitrária de Δ admite a mesma parametrização. Não se deve esconder essa hipótese em um novo registro.

## Literatura e dívida formal

[KNOWN] Bernau, *The square root of a positive self-adjoint operator*, Theorem11, prova unicidade para operadores positivos autoadjuntos não necessariamente limitados. Sua definição de igualdade de operadores inclui domínio e ação. Aplicar esse resultado aos contratos planejados é uma especialização matemática válida, a declarar KNOWN/DERIVED se o teorema geral não estiver formalizado. Fonte primária: https://doi.org/10.1017/S1446788700004560 .

[KNOWN] Sebestyén–Tarcsay, *On the square root of a positive selfadjoint operator* (2017), Theorem2.3, utiliza a fatoração por raízes limitadas dos resolventes. A unicidade passa pela igualdade de domínios de operadores fechados com mesmo Q†Q, pelo resolvente positivo de Q, por comutação com as raízes limitadas e pela positividade de QA; então a unicidade limitada determina QA=B. O manuscrito integral foi disponibilizado pelo autor. Referências: https://doi.org/10.1007/s10998-017-0192-1 e https://www.researchgate.net/publication/318660686_On_the_square_root_of_a_positive_selfadjoint_operator .

[OPEN — no levantamento local] Não encontrei prontas, para LinearPMap, as peças gerais de igualdade dos domínios a partir de Q†Q, resolvente positivo e transporte de domínio pela raiz CFC limitada. Essa fatoração é um caminho rigoroso para desenvolver a unicidade sem primeiro formalizar todo o teorema espectral. Deve conservar explicitamente as inclusões de domínio; comutação algébrica de símbolos não as substitui.

Recomendação: distinguir no resultado050 (1) adjunto antilinear maximal e Δ=S†S efetivo; (2) igualdade T_c²=Δ e raiz multiplicativa explícita; (3) reconstrução intrínseca pelo resolvente, se construída; (4) unicidade abstrata, formal ou apenas KNOWN/DERIVED conforme a prova realmente disponível. Não atribuir a (1)–(3) a generalidade de (4).

A revisão não construiu teoremas, não compilou Lean, não alterou049, Atlas ou memórias, e não emitiu selo. Δ^it, Fourier, Bisognano–Wichmann, inclusão semilateral, localização física e H3 não se seguem automaticamente da identidade de raiz.
