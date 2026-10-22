# Critério espectral para o centralizador na realização Fock

16/09/2026. [DERIVED — demonstração escrita condicional, não Lean]. Esta nota não afirma que a hipótese espectral abaixo foi verificada para o diamante Einstein–sigma.

Na [construção regional](ESTADO_EINSTEIN_SIGMA_E_MODULAR_LOCAL.md), seja L(D) standard, δD seu operador modular de uma partícula e hD=log δD. Na representação Fock bosônica, ΔD=Γ(δD), log ΔD=dΓ(hD). O vácuo Ω é cíclico e separante para a álgebra regional M.

**Proposição.** Se hD não possui espectro pontual, então M^ω=ℂI.

**Prova.** A ausência de autovalores significa que todas as medidas espectrais escalares μv(B)=⟨v,E_h(B)v⟩ são não atômicas. No produto tensorial de n≥1 partículas, a projeção espectral de soma h1+⋯+hn no valor zero tem, sobre um vetor produto v1⊗⋯⊗vn, norma ao quadrado

\[
\int 1_{\lambda_1+\cdots+\lambda_n=0}\,d\mu_{v_1}\cdots d\mu_{v_n}=0.
\]

Por Fubini, fixadas as outras coordenadas, a condição exige um singleton na primeira medida, de massa zero. Logo a projeção se anula nos vetores produto, cuja combinação linear é densa, e se anula em todo o produto. A restrição simétrica também não possui vetor fixo modular. Na soma direta Fock resta somente o setor zero: ker log ΔD=ℂΩ.

Se A∈M^ω, então ΔD^{it}AΩ=AΩ. Portanto AΩ=cΩ; como Ω é separante, A=cI. ∎

Nesse caso a esperança normal que preserva ω sobre o centralizador é Eω(A)=ω(A)I. Toda derivação definida sobre I o anula. Assim, a trivialidade da ação do resto sobre essa imagem seria automática e não testemunharia geometricidade em observáveis fora dela.

## O que não foi demonstrado

O espectro de hD para o estado 067 permanece [OPEN]. Standardness, isoladamente, não implica espectro contínuo. Tampouco basta excluir somente o autovalor zero de hD: se há vetores de autovalores λ e −λ, sua combinação simétrica no setor de duas partículas é um vetor de autovalor zero de dΓ(hD). A conjugação modular relaciona justamente os sinais opostos. Esse controle impede substituir a hipótese da proposição por uma hipótese mais fraca sem prova.

Um vetor Fock fixo não foi aqui identificado com AΩ para algum A limitado do centralizador: não afirmamos a recíproca a partir desse exemplo. Não inferimos tipo III₁, centralizador não trivial ou um valor para R1 a partir da existência abstrata do operador modular.

## Consequência para o handoff

O motor deve manter separados: (a) existência modular regional, já construída; (b) espectro regional, ainda não calculado; (c) ação geométrica, sujeita ao [teste Weyl](TESTE_GEOMETRICO_WEYL_ESTADO_067.md). Nenhuma função adicional de pinching resolve (b) por renomeação.

Referência de contexto para a segunda quantização modular: [Conti–Morsella, §2](https://arxiv.org/pdf/2305.07606). A prova espectral por Fubini acima está explicitada nesta nota; não é atribuída como teorema numerado dessa fonte.
