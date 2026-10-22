# Einstein–sigma S³: redução escalar e vetorial, restrições e sinal físico

09/09/2026. **[DERIVED — demonstração própria escrita; não é nova prova Lean.]** A ação de Einstein–sigma ambiente continua sendo uma entrada explícita. Esta entrega resolve seus setores escalar e vetorial lineares no fundo escolhido. Não modifica a família categórica mínima nem demonstra um limite UV.

**Resultado:** para cada harmônico físico com ℓ≥2, a ação reduzida é

\[
S^{(2)}_A=\frac1{2\kappa}\int dr\,a^3 K_A
\left[\dot x_A^2-\frac{\omega_A^2}{a^2}x_A^2\right],
\]

\[
\boxed{K_S=\frac{4(\lambda-3)}{\lambda+3}>0,\quad\omega_S^2=\lambda+4,
\qquad K_V=\frac{4D}{D+8}>0,\quad\omega_V^2=D+8,}
\]

onde `λ=ℓ(ℓ+2)` e `D=ℓ(ℓ+2)−3`. Lapse e shift foram resolvidos, não apenas contados. Os coeficientes que zeram em ℓ=1 correspondem a calibre residual; não são propagadores a inverter. O setor homogêneo não tem campo sigma tangente escalar independente. As reconstruções abaixo dão soluções completas modulo calibre e preservam a forma simplética.

## 1. Modelo, sinal ADM e extensão global usada na decomposição

A entrada é a ação e o fundo da [nota anterior](../QUANTIZACAO_LOCAL_EINSTEIN_SIGMA_20260909_205633/OPERADOR_JACOBI_GAUGE_E_ESCOPO.md):

\[
S=-\frac1{2\kappa}\int\mu_g(R-2\Lambda)+\frac c2\int\mu_g |d\phi|_g^2,
\quad \phi:M\to S^3,
\]

\[
g=dr^2-a(r)^2\gamma,\quad a=2\cos(r/2),\quad\phi(r,z)=z,
\quad\Lambda=3/4,\quad\kappa c=4,\quad c>0,\quad\kappa>0.
\]

`γ` é a métrica unitária de S³; o ponto indica `d/dr`. Defina

\[
H=\dot a/a,\qquad H^2=a^{-2}-1/4,\qquad\dot H=-a^{-2}.
\tag{1.1}
\]

Escolha um intervalo aberto `I⊂(0,π)`; nele a>0 e H<0. O espaço-tempo geométrico estendido `M=I×S³` é globalmente hiperbólico, com seções r constante compactas e sem bordo. Os campos g e `φ=id` são suaves sobre essa esfera inteira. **Essa é uma extensão do fundo geométrico e do sigma, não uma extensão da carta de cinco probabilidades estritamente positivas.** As fórmulas `P_a=cos²(r/2)z_a²` perdem positividade em `z_a=0` e perdem os sinais dos z_a; portanto não definem o mesmo atlas positivo global. Em um diamante causalmente convexo contido na ortante positiva original, a restrição do fundo e das soluções coincide com o modelo local anterior e mantém todos os P_i positivos.

Use ADM com métrica espacial positiva q:

\[
ds^2=N^2dr^2-q_{ij}(dz^i+b^idr)(dz^j+b^jdr),\quad
K_{ij}=\frac1{2N}(\dot q_{ij}-\mathcal L_bq_{ij}).
\]

Com o sinal de R adotado na nota anterior, descartando a divergência de Einstein–Hilbert para variações de suporte compacto, a ação gravitacional é

\[
S_g=\frac1{2\kappa}\int dr\,d\mu_\gamma\,N\frac{\sqrt q}{\sqrt\gamma}
\big(K_{ij}K^{ij}-K^2+{}^{(3)}R[q]+2\Lambda\big).
\tag{1.2}
\]

O sinal `+2Λ` em (1.2) é necessário nesta convenção: para N homogêneo, q=a²γ, a equação de N dá `3(H²+a⁻²)+Λ=3κc/(2a²)`, exatamente (1.1) quando κc=4. Trocar o sinal da ação de matéria ou de Λ mudaria essa checagem.

## 2. Corte de calibre e ação quadrática antes das restrições

Nos setores S/V, imponha **métrica espacial sem perturbação**, `q=a²γ`, mantendo `N=1+α`, shift b e perturbação sigma `ξ∈Γ(TS³)`. Isso não chama a esfera de plana: sua curvatura espacial continua +1/a². A viabilidade e os resíduos desse corte são tratados na seção 6. A condição H≠0 é essencial para o calibre temporal usado aqui.

Parametrize o alvo por `φ_ε=Exp_id(εξ)`. A normalização sigma fica exata. Como o fundo é uma aplicação harmônica, a segunda variação integrada da energia espacial é

\[
\int_{S^3}|d\phi_\varepsilon|_\gamma^2
=\int_{S^3}\big[3+2\varepsilon\operatorname{div}\xi
+\varepsilon^2(|\nabla\xi|^2-2|\xi|^2)\big]+O(\varepsilon^3).
\tag{2.1}
\]

O termo linear é mantido antes de multiplicar por α: a integral de `α div ξ` em geral não é zero. A forma quadrática em (2.1) é a do Jacobi da identidade em S³, pois `Ric(γ)=2γ`. O termo temporal da matéria é `|dot ξ−b|²` na segunda ordem.

Defina `S(b)_ij=∇_(i b_j)` e `θ=div b`. Como

\[
K^i{}_j=N^{-1}(H\delta^i_j-S(b)^i{}_j),
\quad K_{ij}K^{ij}-K^2=N^{-2}(-6H^2+4H\theta+|S(b)|^2-\theta^2),
\]

expandir `1/N=1−α+α²` em (1.2) e somar a matéria dá, depois de usar κc=4,

\[
\boxed{S^{(2)}_{S,V}=\frac1{2\kappa}\int dr\,a^3\int_{S^3}d\mu_\gamma
\left[-6H^2\alpha^2-4H\alpha\operatorname{div}b
+|S(b)|^2-(\operatorname{div}b)^2
+4|\dot\xi-b|^2
-\frac4{a^2}(|\nabla\xi|^2-2|\xi|^2)
-\frac8{a^2}\alpha\operatorname{div}\xi\right].}
\tag{2.2}
\]

Todos os fatores vêm da ação. Os termos de segundo grau da parametrização do calibre que multiplicariam equações de primeira ordem desaparecem porque o fundo é on-shell. Não há derivadas temporais de α ou b; ambos são variáveis auxiliares.

## 3. Harmônicos e identidades de integração

Escolha harmônicos reais ortonormais; índices de degenerescência são implícitos. Para escalares,

\[
-\Delta_\gamma Y=\lambda Y,\quad\lambda=\ell(\ell+2),\quad\int Y^2=1,
\qquad U=\nabla Y/\sqrt\lambda\quad(\ell\ge1).
\]

Então

\[
\int|U|^2=1,\quad\operatorname{div}U=-\sqrt\lambda Y,\quad
\int|\nabla U|^2=\lambda-2,\quad
\int|S(U)|^2-(\operatorname{div}U)^2=-2.
\tag{3.1}
\]

As duas últimas identidades seguem de Bochner na esfera: `∫|Hess Y|²=λ²−2λ`. Para vetores transversais,

\[
\operatorname{div}V=0,\quad-\Delta_\gamma^{rough}V=\lambda_VV,
\quad\lambda_V=\ell(\ell+2)-1,\quad\int|V|^2=1,
\]

\[
\int|S(V)|^2=\tfrac12(\lambda_V-2),\qquad
\int(|\nabla V|^2-2|V|^2)=\lambda_V-2=:D.
\tag{3.2}
\]

Para (3.2), integrar a derivada cruzada dá `∫∇iVj∇jVi=−2∫|V|²`; a divergência nula elimina o outro termo. A igualdade D=0 caracteriza os Killing da esfera, em ℓ=1. As frequências e a completude escalar/vetorial/tensorial aqui usadas são as propriedades de [Lindblom–Taylor–Zhang, seções 2–4](https://arxiv.org/pdf/1709.08020), com raio unitário e nosso ℓ correspondendo ao índice principal k do artigo. As contas de restrição e de sinal seguintes são próprias.

## 4. Setor vetorial resolvido

Ponha `ξ=x(r)V`, `b=y(r)V`, `α=0`. A variação do lapse no setor vetorial também dá α=0, pois H≠0 e as divergências são zero. Retirando o fator comum `a³/(2κ)`, (2.2) torna-se

\[
L_V=\frac D2 y^2+4(\dot x-y)^2-\frac{4D}{a^2}x^2.
\tag{4.1}
\]

A equação do shift é `(D+8)y=8dot x`, logo

\[
\boxed{y_V=\frac8{D+8}\dot x,\qquad
L_V^{red}=\frac{4D}{D+8}\left[\dot x^2-\frac{D+8}{a^2}x^2\right].}
\tag{4.2}
\]

Para ℓ≥2, D=ℓ(ℓ+2)−3≥5, portanto a cinética é estritamente positiva. A energia canônica instantânea de um modo, após a escolha da ação sem termos de fronteira, é `a³ K_V/(2κ)[dot x²+(D+8)x²/a²]>0` para dados não nulos. Ela depende explicitamente do tempo e não é declarada uma energia conservada.

Em ℓ=1, D=0, y=dot x e toda a ação é zero. O campo `v=x(r)V`, com V Killing, gera `δq=L_v(a²γ)=0`, `δφ=xV` e `δb=dot x V`: é exatamente a solução obtida. Esse modo é calibre residual do sistema acoplado. Não se confunde com o Jacobi de matéria em métrica fixada, no qual proibir a transformação de g remove uma parte desse argumento.

## 5. Setor escalar resolvido, inclusive a derivada total

Para ℓ≥1, ponha `ξ=x(r)U`, `b=y(r)U`, `α=z(r)Y`. Por (3.1),

\[
L_S=-6H^2z^2+4H\sqrt\lambda zy-2y^2
+4(\dot x-y)^2-\frac{4(\lambda-4)}{a^2}x^2
+\frac{8\sqrt\lambda}{a^2}zx.
\tag{5.1}
\]

As duas restrições são

\[
-12H^2z+4H\sqrt\lambda y+8\sqrt\lambda x/a^2=0,
\quad 4y+4H\sqrt\lambda z-8\dot x=0.
\]

Seu determinante não zera para H≠0 e λ≥0. Resolver fornece

\[
\boxed{y_S=\frac6{\lambda+3}\dot x-\frac{2\lambda}{Ha^2(\lambda+3)}x,
\qquad z_S=\frac{2\sqrt\lambda}{H(\lambda+3)}\dot x
+\frac{2\sqrt\lambda}{H^2a^2(\lambda+3)}x.}
\tag{5.2}
\]

Após substituir,

\[
L_S=K_S\dot x^2+B_Sx\dot x+C_Sx^2,
\]

\[
K_S=\frac{4(\lambda-3)}{\lambda+3},\quad
B_S=\frac{16\lambda}{Ha^2(\lambda+3)},\quad
C_S=\frac{8\lambda}{H^2a^4(\lambda+3)}-\frac{4(\lambda-4)}{a^2}.
\tag{5.3}
\]

O fator a³ não pode ser ignorado ao integrar o termo cruzado. De (1.1),

\[
\frac1{2a^3}\frac d{dr}(a^3B_S)
=\frac{8\lambda}{a^2(\lambda+3)}
+\frac{8\lambda}{H^2a^4(\lambda+3)}.
\]

Assim, subtraindo a derivada total `d(a³B_Sx²/2)/dr`,

\[
\boxed{L_S^{red}=\frac{4(\lambda-3)}{\lambda+3}
\left[\dot x^2-\frac{\lambda+4}{a^2}x^2\right].}
\tag{5.4}
\]

Para ℓ≥2, λ≥8, K_S≥20/11>0 e o potencial instantâneo também é positivo. O modo ℓ=1 de Jacobi da matéria em g fixada teria a contribuição espacial λ−4=−1; após incluir e resolver as restrições gravitacionais, seu coeficiente completo é zero e ele é calibre, como se verifica abaixo. Esse controle impede interpretar a conta de matéria isolada como instabilidade física do sistema acoplado.

### Modos escalares excepcionais

Em ℓ=1, λ=3 e `Hess Y=−Yγ`. Dado x(r), escolha a difeomorfia infinitesimal

\[
v=T\partial_r+xU,\qquad T=\frac{x}{\sqrt3H}Y.
\]

Ela preserva `δq=0` porque `H T γ+sym∇(xU)=0`. Além disso,

\[
\delta b=\left(\dot x-\frac{x}{Ha^2}\right)U,
\qquad\delta N=\left(\frac{\dot x}{\sqrt3H}+\frac{x}{\sqrt3H^2a^2}\right)Y,
\]

que são precisamente (5.2) em λ=3. Logo o setor de ação zero é o calibre residual; nenhum estado com divisão por K_S=0 deve ser criado.

Em ℓ=0, `∇Y=0`, portanto ξ=xU não existe. A componente de traço homogênea da métrica pode ser removida por reparametrização temporal, pois H≠0. Resta em (2.2) `−6H²α₀²`, cuja restrição dá α₀=0. Variações de c ou Λ são mudanças de parâmetros da ação, não campos homogêneos admitidos nesta análise. Não se conclui que o calibre permaneça regular no extremo r=0, onde H=0; esse ponto está fora de I.

## 6. Completude do corte SVT e mapa de reconstrução

Sobre S³ compacta, uma perturbação espacial suave admite a decomposição

\[
\delta q_{ij}/a^2=2\psi\gamma_{ij}
+2(\nabla_i\nabla_j-\tfrac13\gamma_{ij}\Delta)E
+2\nabla_{(i}F_{j)}+t_{ij},
\]

com `div F=0`, `div t=0`, `tr t=0`. A decomposição usa a completude harmônica L², promovida a convergência suave para dados suaves por regularidade elíptica. E é tomado ortogonal a ℓ=0,1, onde seu tensor sem traço desaparece; F é tomado ortogonal aos Killing, que também produzem tensor zero. Não há setor de 1-formas harmônicas adicional, pois `H¹(S³)=0`.

Para ℓ≥2, uma difeomorfia espacial remove E e F. Uma transformação temporal remove o traço restante ψ porque H≠0. Sobra o tensor t, que é o setor TT tratado separadamente. Em ℓ=0,1, o mesmo calibre temporal remove ψ; a liberdade espacial não fixada em ℓ=1 é exatamente a descrita nas seções 4–5. A aplicação sigma tangente dispõe de uma decomposição completa em U e V; seus ℓ=1 podem ser removidos por essas liberdades residuais. Portanto os representantes físicos são os modos S/V com ℓ≥2 e o setor TT.

Aqui o grupo de calibre é o das difeomorfias infinitesimais suaves conectadas à identidade, com suporte espacial compacto; em Cauchy S³ isso permite os Killing globais dependentes do tempo. Uma escolha que trate transformações de bordo como simetrias físicas demandaria outro domínio e outra análise. Não há bordo espacial nesta construção.

**Reconstrução S/V explícita.** Para soluções reduzidas x_S,x_V, use (4.2),(5.2) e some harmônicos:

\[
\xi=\sum_{\ell\ge2}x_SU+\sum_{\ell\ge2}x_VV,
\quad b=\sum y_SU+\sum y_VV,
\quad\alpha=\sum z_SY.
\]

O par de perturbações covariantes é

\[
\boxed{\delta\phi=\xi,\qquad
h_{rr}=2\alpha,\quad h_{ri}=-a^2\gamma_{ij}b^j,\quad h_{ij}=0.}
\tag{6.1}
\]

Ao acrescentar uma solução TT `t_ij`, soma-se `h_ij=−a²t_ij`, com `α=b=ξ=0` nesse setor. A equação e a normalização da ação TT são uma obrigação separada; (6.1) não as supõe demonstradas pela presente redução S/V.

O mapa S/V é invertível **modulo calibre**: levar uma solução linearizada completa ao corte acima identifica seus x físicos de maneira única após excluir os núcleos ℓ=0,1; as restrições então forçam y,z às fórmulas dadas. Reciprocamente, uma solução de (4.2)/(5.4), reconstruída por (6.1), satisfaz todas as equações S/V. Para essa última afirmação, o corte é transversal aos calibres restantes em ℓ≥2; a primeira variação da ação completa se decompõe em variações do corte, de α,b e de calibre. As primeiras desaparecem pelas equações reduzidas, as segundas pelas restrições, as terceiras pela identidade de Noether no fundo on-shell. Assim não se perderam equações métricas ao fixar q.

As fórmulas são operadores espaciais espectrais de ordem finita, suaves em r onde a,H≠0. A reconstrução envolve inversos elípticos `(λ+3)⁻¹` e `(D+8)⁻¹`, projeções SVT e derivadas temporais. Ela é em geral não local no espaço. Portanto t, x_S, x_V e o lapse resolvido não são declarados observáveis locais apenas por serem variáveis reduzidas. A localização física continua sendo a dos funcionais invariantes de teste no quociente covariante.

### Mapa explícito dos testes covariantes para amplitudes canônicas

Escreva o funcional linear covariante, com f simétrico **contravariante**,

\[
F_{f,\chi}(h,\xi)=\int dr\,a^3\int d\mu_\gamma
\big(f^{\mu\nu}h_{\mu\nu}+\langle\chi,\xi\rangle\big).
\]

Se f foi inicialmente fornecido covariante, ele é elevado com o g de fundo. Exige-se a condição de calibre `−2∇_μ f^{μν}+〈u^ν,χ〉=0`; ela é o adjunto K* usado na nota anterior. Em cada harmônico escalar, defina

\[
A=\int f^{rr}Y,\qquad B=\int f^{ri}\gamma_{ij}U^j,
\qquad C=\int\langle\chi,U\rangle.
\]

Denote `y=y₁dot x+y₀x` e `z=z₁dot x+z₀x`, com coeficientes exatamente dados em (5.2). Então

\[
F_S=\int dr\,[R_S\dot x+Q_Sx],\quad
R_S=a^3(2z_1A-2a^2y_1B),\quad
Q_S=a^3(2z_0A-2a^2y_0B+C).
\]

Para testes compactamente suportados no tempo, integrar por partes dá `F_S=∫dr(Q_S−dot R_S)x`. Na variável canônica da seção 8, com `dr=a dη`, o teste correspondente é

\[
\boxed{j_S(\eta)=\sqrt{\kappa/K_S}\,[Q_S-\dot R_S]_{r=r(\eta)},
\qquad F_S=\int d\eta\,j_Su_S.}
\tag{6.2}
\]

Analogamente, com `B_V=∫f^{ri}γijV^j` e `C_V=∫〈χ,V〉`,

\[
\boxed{j_V(\eta)=\sqrt{\kappa/K_V}\left[
a^3C_V+\frac d{dr}\left(\frac{16a^5}{D+8}B_V\right)\right]_{r=r(\eta)}.}
\tag{6.3}
\]

O fator dois em ambos os termos de shift vem de `f^{ri}h_ri+f^{ir}h_ir`; omiti-lo muda a álgebra. Esses mapas usam somente ℓ≥2. Os modos removidos não são descartados por um filtro arbitrário no funcional: sua contribuição a um teste invariante é zero porque representam K(v). Coeficientes harmônicos de testes suaves em S³ decaem mais rapidamente que qualquer potência, enquanto (6.2)–(6.3) só introduzem ordens espectrais finitas e derivadas temporais; a soma de modos define os funcionais distribucionais usuais. A correspondência simplética a seguir garante que essa identificação de observáveis respeita o comutador covariante, independentemente da não localidade intermediária da decomposição.

## 7. Preservação simplética por cálculo de momento

No corte S/V, `δq=0`. A contribuição gravitacional ADM à potencial canônica, `∫π^{ij}δq_ij`, é zero nessas direções. A contribuição sigma na segunda ordem é

\[
\Theta_m=ca^3\int_{S^3}\langle\dot\xi-b,\delta\xi\rangle.
\tag{7.1}
\]

Para um modo vetorial físico, a substituição do shift dá

\[
p_V=ca^3(\dot x-y_V)=\frac{a^3}{\kappa}K_V\dot x.
\]

Para um modo escalar,

\[
p_S=ca^3(\dot x-y_S)=\frac{a^3}{\kappa}
\left[K_S\dot x+\frac{8\lambda}{Ha^2(\lambda+3)}x\right].
\]

O segundo termo é proporcional a x, com coeficiente de fundo, e sua contribuição a `δp∧δx` é zero. Consequentemente,

\[
\boxed{\Omega_A=\frac{a^3K_A}{\kappa}
(\delta_1\dot x_A\,\delta_2x_A-\delta_2\dot x_A\,\delta_1x_A),\quad A=S,V,}
\tag{7.2}
\]

somada sobre todos os modos. A ordem dos argumentos em Ω fixa a convenção; pode ser invertida em conjunto com a do comutador. É exatamente a forma canônica derivada da ação reduzida. A derivada total removida na seção 5 desloca a potencial canônica por uma diferencial exata no espaço de campos, sem modificar Ω. Não há termo espacial de bordo em S³. Direções de calibre são nulas na forma restrita às equações e restrições; a exclusão dos núcleos acima produz uma forma não degenerada nos modos S/V físicos.

Isso demonstra a correspondência simplética entre esses setores do quociente covariante e as variáveis reduzidas; não é apenas uma contagem de graus de liberdade.

## 8. Modos conformes exatos e o estatuto da positividade

Defina `dη=dr/a`, escolhendo

\[
\eta=\log(\sec(r/2)+\tan(r/2)),\quad a=2\operatorname{sech}\eta,\quad\eta>0.
\]

Para cada modo físico, `u_A=a√(K_A/κ)x_A`. Descartando uma derivada total temporal, a ação é

\[
S_A^{(2)}=\frac12\int d\eta\,
\big[(u_A')^2-(p_A^2+2\operatorname{sech}^2\eta)u_A^2\big],
\]

\[
\boxed{p_S^2=\lambda+3=(\ell+1)^2+2,\qquad
p_V^2=D+7=(\ell+1)^2+3.}
\tag{8.1}
\]

A frequência quadrática é estritamente positiva. Uma solução complexa normalizada é

\[
\boxed{f_p(\eta)=\frac{(p-i\tanh\eta)e^{-ip\eta}}
{\sqrt{2p(p^2+1)}},\qquad
f_pf_p^{*\prime}-f_p'f_p^*=i.}
\tag{8.2}
\]

Substituir em `f''+(p²+2sech²η)f=0` e no Wronskiano verifica ambas as igualdades exatamente. O modo tende a uma onda de frequência positiva, até fase constante, quando η→+∞; essa é uma escolha de estado de referência, não uma imposição de unicidade física. Seu uso em qualquer subintervalo interior de η>0 é regular.

Para um conjunto finito de modos, ou a álgebra de dados suaves com a soma distribucional correspondente, `u=f_pa+f_p*a†`, `[a,a†]=ℏ`, produz uma representação quase livre positiva. A positividade segue de `Σ_n|∫f_{p_n}^*F_n|²≥0`; o comutador correto segue do Wronskiano e de (7.2). Assim há uma construção efetiva de estado positivo para os setores reduzidos, além da verificação do sinal cinético.

O enunciado de Hadamard requer o controle microlocal da soma e de sua reconstrução covariante. Uma verificação desse passo deve usar (8.2), os operadores espectrais em (6.1), a equivalência simplética e os núcleos já excluídos. A referência [Gérard–Wrochna](https://arxiv.org/abs/1209.2604) é pertinente para caracterização por operadores pseudodiferenciais; sua existência geral não é tomada aqui como substituta da demonstração dos mapas deste modelo. Esta entrega fornece os mapas e a forma reduzida; não declara a parte microlocal completa apenas pelo símbolo principal.

Ausência de ghost e frequência instantânea positiva não significam um limite uniforme para toda perturbação geométrica até r→π. O fator `x=u/(a√(K/κ))` pode crescer no ramo em contração quando a→0. Os coeficientes de reconstrução também têm fatores 1/a e 1/H. Em compactos interiores são suaves e finitos; os extremos singulares e a retroação não linear exigem análise própria. Não se alegou estabilidade não linear global.

## 9. Alcance físico e obrigações de integração

1. A redução resolve S/V da **extensão ambiente** Einstein–sigma, em que g e φ podem variar independentemente antes da redução de calibre. Não remove a proposição anterior de que a família mínima de cinco probabilidades só induz variações de calibre locais.
2. A extensão geométrica a S³ inteira permite usar harmônicos completos e Cauchy compacta. A preservação global da carta estritamente positiva de probabilidades não foi pressuposta. Para a casa categórica original, restringe-se a região causal interior apropriada.
3. O quociente e o estado aqui construídos são da teoria **linearizada**. Em variedades com Cauchy compacta e simetrias, a integrabilidade de dados lineares a famílias não lineares pode exigir condições adicionais de segunda ordem; a presente redução não demonstra essa integrabilidade nem uma teoria interagente completa.
4. A junção com TT deve manter o mapa `h_ij=−a²t_ij`, a ação TT correta e sua forma simplética. A álgebra de observáveis locais é transportada pelos funcionais covariantes invariantes, não pela suposição de que as projeções SVT sejam locais.
5. Nenhum resultado sobre anomalias interagentes, contra-termos ou UV é inferido desta redução.

## 10. Verificação e custódia

O script novo `check_reduction.py` verificou **17 identidades exatas**, com todos os resíduos zero, usando SymPy 1.14.0: as duas restrições escalares, sua substituição, a derivada total decisiva, os momentos simpléticos, as fórmulas residuais de ℓ=1, a eliminação vetorial, a transformação conforme, o modo exato e o Wronskiano. O recibo `VERIFICACAO_REDUCAO.json` registra `PASS_EXACT_CAS_NOT_LEAN`; ele não formaliza a derivação ADM/SVT em Lean. A primeira tentativa sob sandbox não encontrou a dependência de usuário; a repetição com acesso de leitura autorizado à instalação existente passou. Nenhum pacote foi instalado e nenhum ambiente original foi alterado. O manifesto lê os hashes dos arquivos. As fontes e os arquivos canônicos permanecem intactos; nenhum `um.py` foi executado/importado.
