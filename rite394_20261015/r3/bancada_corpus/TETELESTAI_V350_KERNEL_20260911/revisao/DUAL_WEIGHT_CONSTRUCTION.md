# Peso dual e traço na mesma regularCoreAlgebra

11/09/2026. Pesquisa; nenhuma implementação Lean. A construção abaixo permanece em
`N = regularCoreAlgebra P`. **Os cortes SOT são suficientes para construir a integral
ampliada; precisam de pontos fixos, semifinitude e identificação modular para entregar
o peso dual e o traço.**

## Hipóteses de aplicação

[INPUT] Escreva `M = theFactorObject P`, `K = L²(ℝ,H,dx)`,
`ι(a)=fibre(a)`, `V_t=Δ_φ^{it}`, `Λ_t=ι(V_t)S_t`,
`S_tξ(x)=ξ(x−t)`, `D_sξ(x)=e^{−isx}ξ(x)` e `θ_s=Ad(D_s)|N`.
Aqui `ι(V_t)` denota a amplificação ambiente; não exige `V_t∈M`.
Exigir φ fiel, normal e semifinito, com **grupo modular efetivamente igual**
a `a↦V_t a V_t*` em M. Preservar φ e normalizar M, isoladamente, não identificam
esse grupo como modular. Um estado normal fiel serve; não se exige tipo III.

[DERIVED] A identificação com o produto cruzado padrão é explícita:

\[
(W\xi)(x)=V_x\xi(x),\qquad
(\pi(a)\xi)(x)=\sigma^\phi_{-x}(a)\xi(x),
\]
\[
W\pi(a)W^*=\iota(a),\quad WS_tW^*=\Lambda_t,\quad WD_s=D_sW.
\]

W é unitário por integração da isometria de cada V_x, com inverso V_{−x}.
As três identidades seguem por substituição pontual. Assim, transportar os
resultados do modelo padrão chega exatamente a N e à θ dadas.

## Resultados publicados usados

[KNOWN] Fonte consultada integralmente nas partes pertinentes:
[Hiai, arXiv:2004.02383v1](https://arxiv.org/pdf/2004.02383).
Paginação impressa coincide com `#page=`.

| Referência exata | Conteúdo necessário |
|---|---|
| [Lema 10.8, p. 92; Teorema 10.11(1), p. 94](https://arxiv.org/pdf/2004.02383#page=92) | Modelo conjugado acima; pontos fixos `N^θ=ι(M)`. |
| [Definição 8.1, Teorema 8.3, Proposições 8.4/8.6, pp. 68–71](https://arxiv.org/pdf/2004.02383#page=68) | Cone ampliado, resolução espectral com parte infinita, extensão de pesos e composição. |
| [Teorema 10.13(a–c), pp. 96–98, (10.3)/(10.5)](https://arxiv.org/pdf/2004.02383#page=96) | Integral da ação dual é peso operadorial fiel, normal, semifinito; sua composição com φ é o peso dual. |
| [Teorema 10.15(1–2), pp. 99–100](https://arxiv.org/pdf/2004.02383#page=99) | Grupo modular do peso dual implementado por Λ; construção do traço e escala. |
| [§9, (9.3), Proposição 9.3 e Teorema 9.4, pp. 83–85](https://arxiv.org/pdf/2004.02383#page=83) | Perturbação por operador afiliado ao centralizador; normalidade, semifinitude, fidelidade e grupo modular. |

Hiai demonstra 10.13 e 10.15; não é necessário importar a dualidade dupla 10.7
para esta rota. O antecedente de 10.13 é Haagerup, *Dual weights II*, Math.
Scand. 43 (1978/79), 119–140, referência [22]; não foi necessária outra consulta.

## Derivação dos cortes e sua normalização

[DERIVED — cálculos para a representação fornecida, não formalizados]
Com Lebesgue `dt` no grupo original e caracteres `e^{ist}`, Fourier sem prefator
na transformada exige medida dual `ds/(2π)`. Fixe, portanto,

\[
T_R(X)v=\int_{-R}^{R}\theta_s(X)v\,ds,\qquad
\mathcal T(X)=\sup_{R>0}\frac{T_R(X)}{2\pi}\quad(X\in N_+).
\]

A primeira integral é Bochner **em K, para cada vetor v**: o integrando é
contínuo e limitado por `‖X‖‖v‖`. Ela define operador com
`0≤T_R(X)≤2R‖X‖1`. Somas de Riemann pertencem a N e convergem fortemente;
o fechamento WOT de N mantém o integral em N. Não se pressupõe mensurabilidade
Bochner de `s↦θ_s(X)` na norma de B(K).

Para `ω∈N_*⁺`, a definição do supremo é

\[
\mathcal T(X)(\omega)
 =\sup_R\frac{\omega(T_R(X))}{2\pi}
 =\frac1{2\pi}\int_{\mathbb R}\omega(\theta_s(X))\,ds.
\]

É aditiva, homogênea e semicontínua inferiormente em ω, por ser supremo
crescente de avaliações contínuas: produz elemento de `N̂₊` sem exigir teto
uniforme em R. Equivalentemente, sua forma é

\[
q_X(v)=\frac1{2\pi}\int_{\mathbb R}
 \|X^{1/2}D_{-s}v\|^2\,ds,
\qquad D(q_X)=\{v:q_X(v)<\infty\}.
\]

Esse domínio pode não ser denso. Deve-se permitir a projeção de valor infinito
na resolução espectral; `T_R(1)=2R1` já impede um supremo limitado em N.
R inteiros positivos são cofinalmente suficientes para essa integral.

Translação da variável s dá `θ_r(𝒯(X))=𝒯(X)` e `𝒯(θ_r(X))=𝒯(X)`.
Por unicidade espectral, todas as projeções, inclusive a parte infinita, são
fixas. **É aqui que `N^θ=ι(M)` é necessário** para obter
\(\mathcal T:N_+\to\widehat{\iota(M)}_+\). Os próprios cortes finitos geralmente não estão em `ι(M)`.
Para `b∈ι(M)`, mover b pela integral dá `𝒯(b*Xb)=b*𝒯(X)b`.
Fidelidade: integral zero de cada função positiva contínua
`s↦ω(θ_s(X))` força seu valor em zero, `ω(X)`, a ser zero.

Normalidade para redes: obtida a normalidade de cada T_R, trocar os dois
supremos positivos prova `𝒯(sup_i X_i)=sup_i𝒯(X_i)`. Para provar aquela etapa
diretamente, as funções contínuas `ω(θ_s(X_i))` crescem à função contínua
`ω(θ_s(X))`; Dini para redes em `[-R,R]` segue de cobertura finita e direção.
Não substituir esse argumento por convergência dominada sequencial aplicada
a uma rede arbitrária.

## Domínio finito e peso dual

[DERIVED — especialização e teste de aplicação] Use coeficientes **à direita**:

\[
\mu(a)=\int_{\mathbb R}\Lambda_t\iota(a(t))\,dt,
\qquad
\mathcal T(\mu(a)^*\mu(a))=
 \iota\!\left(\int_{\mathbb R}a(t)^*a(t)\,dt\right).
\]

Para a contínua σ-fortemente*, de suporte compacto, essa é a identidade
de avaliação em zero (10.3); nesta convenção
`(a♯⋆a)(0)=∫a(t)*a(t)dt`. A integral à direita é limitada.
Assim `μ(a)∈𝒩_𝒯={Y:𝒯(Y*Y)∈ι(M)₊}`. A densidade dos integrados fornece
a semifinitude que **não decorre apenas da existência dos cortes**.

Defina em todos os positivos, admitindo infinito,

\[
\widetilde\phi(X)=
 \widehat\phi\bigl(\widehat\iota^{-1}(\mathcal T(X))\bigr),\qquad
\mathcal N_{\widetilde\phi}
 =\{Y\in N:\widetilde\phi(Y^*Y)<\infty\}.
\]

Os chapéus são extensões ao cone ampliado, não inversos aplicados aos T_R.
Um núcleo finito concreto é `a(t)=f(t)b`, `f∈C_c(ℝ)`, `b∈𝒩_φ`:

\[
\widetilde\phi(\mu(fb)^*\mu(fb))
 =\|f\|_{L^2(dt)}^2\phi(b^*b).
\]

Com funções aproximando deltas e o domínio denso de φ, obtém-se a densidade
necessária; para φ geral, a composição semifinita é justificada por 8.6.
Em contraste, `𝒯(ι(a))=∞·s(ι(a))` para `a≥0`, e
`φ̃(ι(a))=∞` quando `a≠0`, pela fidelidade. O peso dual não é extensão de φ
por simples restrição a `ι(M)`.

Controle independente da constante: para `M=ℂ`, no Fourier unitário de
Lebesgue, `S_t=M_{e^{-itp}}`, `θ_s(F)(p)=F(p+s)`. Logo

\[
\widetilde\phi(M_F)=\frac1{2\pi}\int F(p)\,dp,
\qquad A=M_{e^{-p}},\qquad
\tau(M_F)=\frac1{2\pi}\int e^pF(p)\,dp.
\]

Usar os cortes crus com ds, sem dividir por 2π, multiplica ambos os pesos
por 2π; a lei de escala sozinha não detecta isso. Um funcional de vetor
`Ω⊗g` normalizado tem valor 1 na identidade, enquanto `φ̃(1)=∞`;
ele não fornece o peso dual canônico.

## Operador afiliado e passagem ao traço

[KNOWN — aplicação de (10.7)/(10.9), pp. 97–98] No produto cruzado modular,
`σ_t^{φ̃}(ι(a))=ι(σ_t^φ(a))` e `σ_t^{φ̃}(Λ_r)=Λ_r`, pois
`φ∘σ_r^φ=φ`. Covariância e comutação dos Λ mostram que esses valores são
os de `Ad(Λ_t)` nos geradores; normalidade estende a igualdade a N.

[DERIVED, usando os resultados modulares publicados acima] Stone fornece
`Λ_t=e^{itL}`. Tome `A=e^L`, positivo autoadjunto com núcleo zero;
suas projeções espectrais estão em `{Λ_t}''⊂N`. Assim `A` e `A^{-1}` são
afiliados a N, não necessariamente limitados. Seus domínios são
`∫e^{±2λ}d‖E_L(λ)v‖²<∞`; não substituir A por `fibre(Δ_φ)`.

Uma vez provado `σ_t^{φ̃}=Ad(Λ_t)`, todos os Λ_r são fixos por esse grupo.
Logo A e `B=A^{-1}` são afiliados ao **centralizador** de φ̃, hipótese da
perturbação de Pedersen–Takesaki. Com `B_ε=B(1+εB)^{-1}=(A+ε1)^{-1}`,

\[
\tau(X)=(\widetilde\phi)_{A^{-1}}(X)
 =\sup_{\varepsilon>0}
 \widetilde\phi(B_\varepsilon^{1/2}XB_\varepsilon^{1/2}),
 \qquad X\in N_+.
\]

A monotonicidade aqui é dos **pesos escalares**, assegurada pelo
centralizador; não se afirma monotonicidade dos operadores sanduíche para X
arbitrário. 9.3 fornece peso fiel, normal, semifinito; 9.4 dá
`σ_t^τ=Ad(A^{-it})∘σ_t^{φ̃}=id`, portanto τ é traço.

Finalmente, a relação fornecida `θ_s(Λ_t)=e^{-ist}Λ_t` implica, por Stone,
`θ_s(L)=L−s1`, `θ_s(A)=e^{-s}A`, `θ_s(B)=e^sB`. Usando invariância de φ̃ e
`θ_{−s}(B_ε)=e^{-s}B_{e^{-s}ε}` na fórmula anterior, resulta
`τ(θ_s(X))=e^{-s}τ(X)`, com o sinal solicitado.

[OPEN — formalização desta entrega] Identificação explícita W/pontos fixos;
cone ampliado e extensões; identidade dos integrados/densidade;
identificação modular de φ e φ̃; Stone/afiliação e perturbação.
Os cortes finitos que o pai implementa são a primeira etapa dessa cadeia.
Esta nota não declara esses passos compilados nem altera o gate.
