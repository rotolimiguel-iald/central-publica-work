# Fisher refletida: símbolo, liberdade de variação e contraexemplo ao recíproco

[DERIVED — demonstração escrita nesta revisão, sem compilação Lean] O mapa de probabilidades para a métrica possui degenerescências. A existência local de probabilidades que representem uma métrica, demonstrada anteriormente com Nash, não estabelece equivalência entre a variação da ação nas probabilidades e a variação independente de todos os campos.

O contraexemplo abaixo se refere exclusivamente ao recíproco variacional da ação Einstein–Hilbert mais sigma normalizada explicitada na seção 5. Não é uma refutação da TGL, de seus dados ou da lei de área. O mesmo perfil tem um ajuste conhecido de constantes no qual a equação gravitacional é satisfeita; esse ajuste é exibido na seção 5.6.

## 1. Derivada e símbolo principal

Sejam `P_i>0`, `i=0,…,m−1`, funções suaves em uma variedade de dimensão `n`, com `Σ_iP_i=1`. Escreva

\[
r_i=dP_i,\quad F=\sum_i\frac{r_i\otimes r_i}{P_i}>0,
\quad c=dP_0\ne0,\quad w=F^{-1}c,\quad b=c(w)>0,
\quad g=\frac{2c\otimes c}{b}-F.
\]

Usamos `α⊙β=α⊗β+β⊗α`. Uma variação admissível `π_i=δP_i`, com `Σ_iπ_i=0`, dá

\[
\delta F=\sum_i\left(\frac{r_i\odot d\pi_i}{P_i}
-\frac{\pi_i}{P_i^2}r_i\otimes r_i\right),\qquad
\delta c=d\pi_0,
\]

\[
\delta b=2\delta c(w)-\delta F(w,w),\qquad
\delta g=-\delta F+\frac{2}{b}c\odot\delta c
-\frac{2}{b^2}\delta b\,c\otimes c.
\]

Para um covetor não nulo `ξ` e amplitude `u=(u_i)` com `Σ_iu_i=0`, defina `A_u=Σ_i(u_i/P_i)r_i`. O símbolo principal real, omitindo apenas o fator convencional `i` da transformada de Fourier, é

\[
\boxed{\sigma_{Dg}(\xi)u
=-A_u\odot\xi+\frac{2u_0}{b}c\odot\xi
-\frac{4}{b^2}\xi(w)\bigl(u_0-A_u(w)\bigr)c\otimes c.}
\]

Ele depende de `u` apenas por `A_u∈T*` e `u₀∈ℝ`: o posto é no máximo `n+1`, portanto no máximo cinco em dimensão quatro, independentemente do número de probabilidades. Isso não prova, isoladamente, impossibilidade de um inverso do operador completo: componentes normais podem contribuir em ordem zero, como mostra a seção 3.

### Margem do relógio e postos exatos

No espaço tangente da simplex, use o produto interno `I_P(u,v)=Σ_i u_iv_i/P_i`. O representante de `u↦u₀` é

\[
R_i=P_i(\delta_{i0}-q),\qquad q=P_0,
\quad \|R\|_{I_P}^2=q(1-q).
\]

A projeção de `R` no subespaço `dP(T)` é `dP(w)`. Logo, para `N=R−dP(w)`,

\[
\kappa_0:=\|N\|_{I_P}^2=q(1-q)-b\ge0,
\qquad u_0-A_u(w)=I_P(N,u).
\]

Portanto a margem `b<q(1−q)` é precisamente a condição para que `u↦(A_u,u₀)` seja sobrejetivo em `T*⊕ℝ`. Se a margem é estrita, o símbolo tem posto `n+1` quando `ξ(w)≠0` e `ξ` não é proporcional a `c`; tem posto `n` quando `ξ(w)=0` ou `ξ∥c`. Isso segue porque sua imagem é a soma de `{α⊙ξ}` com a direção `c⊗c`, e esta última fornece uma direção nova exatamente no caso genérico indicado.

Se `κ₀=0`, então `u₀=A_u(w)` para toda amplitude, e o símbolo tem posto `n`. Em todos os casos, amplitudes com `A_u=0` e `u₀=0` estão no núcleo do símbolo para todo `ξ`. Com margem estrita, esse espaço tem dimensão `m−n−2`.

Para uma amplitude tangencial `u=dP(X)`, temos `A_u=F(X,·)` e `u₀=c(X)`, de modo que

\[
\sigma_{Dg}(\xi)dP(X)=g(X,\cdot)\odot\xi.
\]

É o símbolo esperado da derivada de Lie da métrica, coerente com a naturalidade `g[P∘ψ]=ψ*g[P]`.

## 2. Degenerescência exata por rotações das amplitudes

Defina `z_i=2√P_i`. Então `|z|²=4` e `F=Σ_i dz_i⊗dz_i`. Uma transformação ortogonal **constante** de `(z₁,…,z_{m−1})`, mantendo `z₀` fixo, preserva `F`, `P₀`, `dP₀` e `g` exatamente. Em uma vizinhança relativamente compacta dentro da ortante positiva, rotações suficientemente próximas da identidade também preservam a positividade das componentes.

Infinitesimalmente, para uma matriz antissimétrica constante `B` que anule a coordenada zero, `δz=Bz` e `π_i=z_i(Bz)_i/2` satisfazem `Dg[P]π=0`. A família é, em geral, não trivial. Trata-se de uma degenerescência matemática desta representação; a identificação de ramos com observáveis adicionais pode restringir quais dessas rotações possuem interpretação física.

## 3. Condição suficiente concreta para liberdade métrica, com estimativa

Esta condição diz respeito a **Dg**, não à derivada conjunta de todos os campos selecionados.

Considere o subespaço normal com relógio fixo

\[
\mathcal N_0(x)=\{W\in\mathbb R^m:
\langle W,z\rangle=0,\ \langle W,\partial_\mu z\rangle=0\ (\forall\mu),\ W_0=0\}.
\]

Se `W(x)` é uma seção suave desse subespaço, a variação `δz=W` satisfaz `δP₀=0` como função e, portanto, `δc=0`. Diferenciando `⟨W,∂_νz⟩=0`, obtemos

\[
\delta F_{\mu\nu}=-2\langle W,\partial_\mu\partial_\nu z\rangle.
\]

Defina o operador em formas simétricas

\[
L(h)=-h+\frac{2h(w,w)}{b^2}c\otimes c.
\]

Então `δg=L(δF)`, `L²=Id`, e `L` preserva a norma tensorial induzida por `F`. De fato, `c⊗c/b` é um vetor unitário no espaço de tensores simétricos, e `L` é uma reflexão nesse espaço.

Projete as segundas derivadas `∂_μ∂_νz` em `𝒩₀`, formando a segunda forma `B` com valores em `𝒩₀`. Essa projeção elimina os termos tangenciais introduzidos por mudanças de coordenadas, portanto o objeto é tensorial. Em um referencial ortonormal do espaço `Sym²(T*)`, sejam `B_a`, `a=1,…,d`, suas `d=n(n+1)/2` componentes. A condição verificável é

\[
M_{ab}=\langle B_a,B_b\rangle>0.
\]

Para um tensor métrico desejado `h` de suporte compacto, escreva `k_a=−(Lh)_a/2` e escolha

\[
W=\sum_b(M^{-1}k)_bB_b.
\]

Temos `⟨W,B_a⟩=k_a`, logo `δF=Lh` e **`δg=h`**. A escolha é algébrica em `h`, preserva suporte e é suave onde o Gram é positivo. Se `M≥λId`, `λ>0`, em um compacto, então

\[
\boxed{\|\pi\|_{I_P}=|W|\le\frac{\|h\|_F}{2\sqrt\lambda}.}
\]

Não há derivadas de `h` nessa estimativa. A derivação das identidades elimina precisamente as derivadas dos coeficientes de `W` que seriam tangenciais.

Essa variação é realizável por curvas exatas de probabilidades positivas. Mantenha `z₀` fixo, ponha `r=√(4−z₀²)` e

\[
z_J(s)=r\,\frac{z_J+sW_J}{|z_J+sW_J|},\qquad P_i(s)=z_i(s)^2/4.
\]

Como `⟨z_J,W_J⟩=0`, sua derivada inicial é `W`; a soma das probabilidades é exatamente um. Para suporte compacto e `s` pequeno, a positividade é preservada.

Com margem estrita do relógio, `dim𝒩₀=m−n−2`. Assim, em dimensão quatro, a condição de Gram positivo requer **pelo menos 16 probabilidades**, ou `|J|≥15` na notação `Option J`. Isso é apenas uma condição dimensional necessária para este certificado suficiente, não uma prova de que 16 probabilidades bastam em todo caso. O teorema de Nash empregado na representação local não fornece automaticamente esse Gram positivo para o mapa final escolhido.

Se a ação depender somente de `g`, essa condição permite testar toda variação métrica e concluir `E_P=0⇒E_g=0`. Se houver outros campos independentes cujas equações já estejam satisfeitas, a mesma conclusão métrica é válida. Ela não estabelece liberdade conjunta quando esses campos são funções das próprias probabilidades.

## 4. Obstrução à liberdade conjunta no sigma selecionado atual

Na definição comunicada pela tarefa de `SelectedProbabilitySigma`,

\[
q=P_0,\qquad \phi_j=\sqrt{P_j/(1-q)},\qquad
P_j=(1-q)\phi_j^2,\qquad \sum_j\phi_j^2=1.
\]

As `φ_j` recuperam todos os graus relativos das probabilidades. Manter **`δφ≡0` como campo** força

\[
\pi_0=\delta q,\qquad \pi_j=-\phi_j^2\delta q.
\]

Logo, com `φ` fixa, `δg` depende apenas do primeiro jato de uma função escalar `δq`: `n+1` números em cada ponto. Em dimensão quatro são cinco números para dez componentes de `δg`. Portanto não é possível produzir todas as variações métricas mantendo os campos sigma fixos, qualquer que seja o tamanho de `J`. Esta é uma obstrução ao teste conjunto `(δg,δφ)=(h,0)`; a condição de Gram da seção 3 não a remove.

O enunciado geral da primeira variação é

\[
E_P=Dg[P]^*E_g+D\phi[P]^*E_\phi
\quad\text{(mais termos dos demais campos dependentes).}
\]

Anular essa combinação não separa os seus termos. Também, se `λ` for um multiplicador independente de `Σφ²−1`, esse termo desaparece identicamente da ação composta nas probabilidades. `E_P` não determina `λ`; mudar `λ` altera a componente radial de `E_φ`. Uma regra separada para `λ`, ou a própria equação sigma completa, é necessária para resolver essa questão. Não se atribui ao modelo uma escolha de `λ` diferente daquela efetivamente definida em suas fontes.

## 5. Contraexemplo completo ao recíproco variacional

### 5.1 Ação e regime controlado

Em dimensão quatro, com assinatura `(+---)`, considere

\[
S[g,\phi,\lambda]=\int_U\sqrt{|g|}\left[
\frac{R-2\Lambda}{2\kappa}
-\frac C2\left(g^{\mu\nu}\sum_j\partial_\mu\phi_j\partial_\nu\phi_j
+\lambda\left(\sum_j\phi_j^2-1\right)\right)\right].
\]

Aqui `κ≠0` e `C>0` são constantes. As equações independentes são `G+Λg=κT`, `Box_gφ_j=λφ_j` e `Σφ²=1`; na superfície de normalização,

\[
T_{\mu\nu}=C\left(H_{\mu\nu}-\tfrac12g_{\mu\nu}\operatorname{tr}_gH\right),
\qquad H=\sum_jd\phi_j\otimes d\phi_j.
\]

Para o contraexemplo de falha gravitacional, tome **`Λ=0` e `C=1`**, com qualquer `κ` constante. Variações têm suporte compacto em `U`, eliminando os termos de fronteira da primeira variação. Outros termos físicos adicionais na ação precisariam de exame separado.

### 5.2 Probabilidades positivas para qualquer alfabeto suficientemente grande

Seja `U=I×V`, com `I⊂(0,π)` um intervalo aberto e `V` uma carta na ortante estritamente positiva da esfera unitária `S³`. Denote por `r₁,…,r₄` suas coordenadas cartesianas, com `Σ_ar_a²=1`, e por `γ=Σ_adr_a²` a métrica da esfera unitária.

Escolha `q=sin²(t/2)`. Reparta os índices não temporais em quatro grupos não vazios e escolha constantes `α_{aℓ}>0`, com `Σ_ℓα_{aℓ}=1` em cada grupo. Defina

\[
P_0=q,\qquad P_{a\ell}=(1-q)\alpha_{a\ell}r_a^2,
\qquad \phi_{a\ell}=\sqrt{\alpha_{a\ell}}\,r_a.
\]

Todas as probabilidades e componentes sigma são positivas. Sua soma e a normalização sigma são exatas. Subdividir grupos permite qualquer número `m≥5` de probabilidades, em particular o regime `|J|≥5`, que possui `m≥6`.

Em amplitudes `z=2√P`, a imagem é uma região de uma grande esfera `S⁴` de raio dois, contida em um subespaço linear **constante** `L⊂ℝ^m` de dimensão cinco. O vetor `e₀` pertence a `L`. O diferencial de `z` tem posto quatro e preenche o espaço tangente dessa grande esfera.

### 5.3 Métrica e equações sigma

Um cálculo direto fornece

\[
F=\frac{dq^2}{q(1-q)}+4(1-q)\gamma
=dt^2+a(t)^2\gamma,\qquad a(t)=2\cos(t/2),
\]

\[
b=q(1-q)>0,\qquad
g=dt^2-a(t)^2\gamma,\qquad H=\gamma.
\]

O relógio não se anula e `F` é positiva. O exemplo satura a desigualdade `b≤q(1−q)`; portanto não pertence à subclasse com margem estrita usada na construção local anterior por Nash. Essa margem estrita não faz parte das hipóteses básicas `F>0` e `dP₀≠0` consideradas aqui.

Nas coordenadas da esfera unitária, `Δ_γr_a=−3r_a`. Como `φ` é independente de `t`,

\[
\Box_g\phi_j=-a^{-2}\Delta_\gamma\phi_j
=\frac3{a^2}\phi_j.
\]

Assim, **`λ=3/a²` satisfaz todas as equações sigma e a equação do multiplicador**. A identidade `Δ_γr_a=−3r_a` pode ser obtida diretamente da fórmula do laplaciano euclidiano em coordenadas polares aplicada à função linear `x_a=ρr_a`.

### 5.4 Estacionariedade sob todas as variações admissíveis de P

Uma variação arbitrária `π`, com soma zero, corresponde a `δz_i=2π_i/z_i`; então `⟨z,δz⟩=0`. A decomposição ortogonal no subespaço constante `L` dá, de modo único e suave,

\[
\delta z=dz(X)+W,\qquad W\in L^\perp.
\]

Se a variação tem suporte compacto, `X` e `W` também têm. O primeiro termo é realizado pelo fluxo de um campo vetorial com suporte compacto, `P_s=P∘ψ_s`, e induz `(δg,δφ)=(\mathcal L_Xg,\mathcal L_Xφ)`.

Para o termo normal, `W₀=0` porque `e₀∈L`, e `dz∈L`, `dW∈L⊥` porque `L` é constante. Portanto

\[
\delta P_0=0,\quad\delta c=0,\quad
\delta F=2\langle dz,dW\rangle_{\rm sym}=0,\quad
\delta g=0.
\]

Além disso,

\[
\delta\phi_J=\frac{W_J}{2\sqrt{1-q}}\in L_J^\perp.
\]

Os campos `φ,dφ` pertencem ao subespaço constante `L_J`, enquanto `δφ,dδφ` pertencem a `L_J⊥`. Consequentemente, **`δH=0` ponto a ponto**. A curva exata com `P₀` fixo da seção 3 realiza esse `W`, preservando normalização e positividade para parâmetro suficientemente pequeno.

No setor normal a primeira variação da ação é zero, pois `δg=δH=0` e a normalização é preservada. No setor tangencial a invariância por difeomorfismos da ação completa faz a primeira variação ser uma divergência de suporte compacto. O multiplicador deve ser transportado junto no argumento de invariância; se ele for mantido fixo na variação em `P`, a diferença é multiplicada por `E_λ=0`, pois a normalização é identicamente satisfeita. Logo também não há contribuição desse termo.

Por linearidade da primeira variação, **`E_P=0` sob todas as variações admissíveis compactamente suportadas**, não apenas sob variações que mantenham a divisão em grupos. As variações normais precisamente incluem as direções que saem desse agrupamento.

### 5.5 A equação gravitacional não segue

Com a convenção `R^ρ{}_{σμν}=∂_μΓ^ρ_{νσ}−∂_νΓ^ρ_{μσ}+…`, as conexões de `g=dt²−a²γ` dão

\[
R_{tt}=-3a''/a,\qquad
R_{ab}=(aa''+2a'^2+2)\gamma_{ab},
\]

\[
G_{tt}=\frac{3(a'^2+1)}{a^2},\qquad
G_{ab}=-(2aa''+a'^2+1)\gamma_{ab}.
\]

Aqui `a'=−sin(t/2)` e `a''=−a/4`; portanto

\[
G_{tt}=\frac6{a^2}-\frac34,
\quad G_{ab}=\left(\frac34a^2-2\right)\gamma_{ab},
\quad T_{tt}=\frac{3C}{2a^2},\quad T_{ab}=-\frac C2\gamma_{ab}.
\]

O resíduo temporal da equação de Einstein é

\[
\boxed{(G+\Lambda g-\kappa T)_{tt}
=\frac{6-3\kappa C/2}{a^2}+\Lambda-\frac34.}
\]

Com `Λ=0`, `C=1`, essa expressão não se anula identicamente em nenhum intervalo aberto para qualquer `κ` constante: `a²=4cos²(t/2)` não é constante, e o termo constante `−3/4` permanece. Em particular, o perfil satisfaz `E_P=0`, `E_φ=0` e `E_λ=0`, mas não satisfaz a equação métrica independente em um aberto.

Geometricamente, o Gram da seção 3 é zero neste exemplo: as segundas derivadas de `z` pertencem a `L`, enquanto o normal relevante é `L⊥`. As variações em `P` testam difeomorfismos da métrica e direções sem resposta métrica de primeira ordem; por isso a equação métrica inteira não é recuperada.

### 5.6 Ajuste em que o mesmo perfil está on-shell

Não há conflito com o habitante ajustado já encontrado na outra tarefa. Se **`Λ=3/4` e `κC=4`**, os resíduos temporal e espacial acima se anulam exatamente. O perfil passa então a satisfazer também a equação gravitacional. O contraexemplo utiliza expressamente `Λ=0`; ele mostra que a estacionariedade da ação composta em `P` não força o ajuste gravitacional correto.

A equação de Einstein não satisfeita no controle implica que o matching de área dependente dela também não está demonstrado nesse controle, conforme esperado. Nenhum veredito de natureza ou de uma teoria completa é extraído desse cálculo.

## 6. Consequência operacional

Há três afirmações distintas: existência cinemática de `P` representando `g`; liberdade de variação métrica de `Dg`; liberdade conjunta de `D(g,φ,λ)`. O argumento por Nash paga a primeira. Um certificado de segunda forma normal com Gram positivo pode pagar a segunda dentro de seu escopo e com uma estimativa explícita. A parametrização atual de todos os `φ_j` pelas probabilidades impede tratar essas três afirmações como equivalentes.

O contraexemplo prova que a passagem geral `E_P=0⇒E_g=E_φ=E_λ=0` é falsa para a ação e classe admissível aqui explicitadas, inclusive em alfabetos com mais de cinco probabilidades. Para excluir esse mecanismo seriam necessárias restrições adicionais verificáveis no mapa ou equações independentes adequadas, cuja suficiência teria de ser demonstrada. Esta nota não acrescenta uma hipótese que simplesmente repita a conclusão desejada.

Não foram executados `um.py`, Lean, integradores ou scripts canônicos. Nenhum arquivo existente foi alterado para produzir esta nota.
