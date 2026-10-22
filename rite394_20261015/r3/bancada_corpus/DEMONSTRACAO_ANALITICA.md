# Fechabilidade do operador de Tomita na torre — 05/09/2026

[DERIVED] Esta é uma composição explícita das estruturas da casa. O resultado matemático é clássico; a contribuição desta bancada é sua formalização sobre `TowerHilbert P`, sem exigir `TakesakiInput` ou `CommutationInput`. O estatuto de compilação está no relatório e no log Lean.

Sejam H = TowerHilbert P, Ω = hOmega P e M = theFactorObject P. Para cada matriz local b, denote por R_b a ação limitada à direita rTowerPi P b. A casa já fornece:

- Ω separante para M (`factor_omega_separating`);
- MΩ denso em H (`factor_omega_cyclic`);
- A R_b = R_b A para A ∈ M (`factor_comm_rTowerPi`);
- R_b Ω = [b] (`rTowerPi_omega`), e a união dessas imagens é densa (`exists_tof`, `towerPre_denseRange`).

Defina S₀(AΩ) = A*Ω sobre MΩ. A separância torna a definição unívoca: se AΩ = BΩ, então (A−B)Ω = 0, logo A=B. A regra é antilinear, pois o adjunto é antilinear.

Com a convenção de produto interno linear no segundo argumento, para todo A ∈ M e toda matriz local b:

\[
\langle S_0(A\Omega),R_b\Omega\rangle
=\langle A^*\Omega,R_b\Omega\rangle
=\langle\Omega,A R_b\Omega\rangle
=\langle\Omega,R_b A\Omega\rangle
=\langle R_b^*\Omega,A\Omega\rangle.
\]

Suponha AₙΩ → 0 e S₀(AₙΩ) → y. Pela continuidade do produto interno:

\[
\langle y,R_b\Omega\rangle
=\lim_n\langle R_b^*\Omega,A_n\Omega\rangle=0.
\]

Como {R_bΩ} é denso, y=0. Portanto S₀ é fechável. **Não foi preciso que S₀ fosse limitado ou isométrico.** A continuidade usada é a dos funcionais de teste definidos por vetores fixos.

A formulação pelo gráfico elimina qualquer dependência de uma escolha de sequências. Seja

\[
G_0=\{(A\Omega,A^*\Omega):A\in M\}.
\]

Para cada b, a identidade acima define um conjunto fechado de H×H contendo G₀, logo contém seu fecho G. Se (x,y) e (x,z) pertencem a G, então ⟨y,R_bΩ⟩=⟨z,R_bΩ⟩ para todo b. Pela densidade, y=z. Assim G é o gráfico de um operador fechado com domínio denso, que estende S₀.

O gráfico inicial é um subespaço real e satisfaz (x,y)∈G₀ ⇒ (c x,conj(c)y)∈G₀; essas propriedades sobrevivem ao fecho. Portanto a extensão é antilinear. A operação (x,y)↦(y,x) também preserva G₀, porque A**=A, e preserva G. A extensão é involutiva no seu domínio. Esses argumentos adicionais são demonstrações em prosa; consultar o arquivo Lean para o alcance exato formalizado.

## O que permanece

O resultado retira a fechabilidade da lista de obstáculos desta construção. Não entrega sozinho o cálculo espectral do operador não limitado Δ=S* S, a identificação de sua decomposição polar com o `towerJ` existente, a invariância modular de M, a esperança de Takesaki formalizada, nem uma geometria gravitacional geral.

Um operador não isométrico não é necessariamente ilimitado. No perfil tracial, por exemplo, a adjunção preserva a norma GNS. A prova acima funciona para todo `SiteProfile` admissível e não depende de declarar S₀ ilimitado.

Referência de contexto [KNOWN]: Jonathan Sorce, [A short proof of Tomita’s theorem](https://arxiv.org/html/2309.16762v2), introdução, distingue a fechabilidade inicial do teorema posterior de invariância modular. A prova Lean desta bancada usa diretamente as peças locais da casa.
