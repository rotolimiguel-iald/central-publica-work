# Dados por grupos, bloco interno livre e equivalência variacional local

[DERIVED — demonstração escrita, sem compilação Lean] Uma organização das probabilidades por grupos, preservando também as probabilidades condicionais internas, remove a obstrução anterior à liberdade conjunta de métrica e sigma. O mecanismo é um bloco interno com certificado explícito de segunda forma normal, construído abaixo sem pressupor que um mergulho de Nash seja livre.

[INPUT] A partição dos ramos e a escolha dos campos sigma coletivos são dados adicionais da extensão. [POSTULATE] A ação utilizada é Einstein–Hilbert mais sigma normalizada, com seus acoplamentos. [KNOWN] Nash é usado somente para realizar um tensor residual riemanniano; o certificado livre é fornecido por uma fórmula independente e explícita. Não se atribui este resultado à versão canônica atual do programa.

## 1. Organização reversível dos dados e identidade de Fisher

Seja `A` um conjunto finito de grupos. Em uma carta de dimensão quatro, escreva

\[
P_0=q,\qquad P_{a\ell}=(1-q)\phi_a^2Q_{a\ell},\qquad
0<q<1,\quad\phi_a>0,\quad\sum_a\phi_a^2=1,
\quad Q_{a\ell}>0,\quad\sum_\ell Q_{a\ell}=1.
\]

Toda a informação fina é preservada se o registro guarda as condicionais internas. Com `S_a=Σ_ℓP_{aℓ}`, a inversa é

\[
q=P_0,\qquad \phi_a=\sqrt{S_a/(1-q)},\qquad Q_{a\ell}=P_{a\ell}/S_a.
\]

Assim `P↔(q,φ,Q)` é uma mudança invertível de variáveis no domínio positivo. As somas por grupo, isoladamente, não constituiriam o registro completo exigido aqui.

Para `F[Q]=Σ_ℓdQ_ℓ⊗dQ_ℓ/Q_ℓ`, a normalização das condicionais cancela os termos cruzados internos. Depois, `Σ_aφ_a dφ_a=0` cancela os termos cruzados entre `q` e `φ`. Resulta exatamente

\[
\boxed{F[P]=\frac{dq\otimes dq}{q(1-q)}
+4(1-q)\sum_a d\phi_a\otimes d\phi_a
+(1-q)\sum_a\phi_a^2F[Q_a].}
\]

Essa identidade também pode ser obtida primeiro para os pesos de grupo `w_a=(1−q)φ_a²`: `F[P]=dq²/q+Σ_a(dw_a²/w_a+w_aF[Q_a])`.

## 2. Uma família livre explícita com quinze probabilidades

Use em `Sym₄` o produto interno de Frobenius e uma base ortonormal `E₁,…,E₁₀`: os quatro elementos diagonais e os seis elementos simétricos fora da diagonal, estes divididos por `√2`. Para `x∈ℝ⁴`, defina em `ℝ¹⁵`

\[
V(x)=\left(1,x,\left(\tfrac12x^TE_\alpha x\right)_{\alpha=1}^{10}\right),
\qquad D(x)=1+\tfrac12|x|^2,\qquad z(x)=\frac{2V(x)}{D(x)}.
\]

Pela identidade `Σ_α(xᵀE_αx)²=|x|⁴`, temos

\[
|V|^2=1+|x|^2+\tfrac14|x|^4=D^2,\qquad |z|^2=4.
\]

### Positividade das coordenadas

Escolha uma transformação ortogonal **constante** `O` que leve `e₀` a `u=(1,…,1)/√15`. Por exemplo, a reflexão de Householder associada a `e₀−u` tem essa propriedade. Ponha `\widehat z=Oz` e `Q^{free}_ℓ=\widehat z_ℓ²/4`.

Como

\[
|z(x)-2e_0|^2=\frac{4|x|^2}{D(x)},
\]

na bola `|x|≤1/(2√15)` cada coordenada de `\widehat z` é pelo menos `1/√15`. Portanto

\[
Q^{free}_\ell\ge\frac1{60},\qquad\sum_{\ell=1}^{15}Q^{free}_\ell=1.
\]

O tensor de Fisher é o tensor induzido pela imersão esférica. Para um vetor `v`, um cálculo direto dá

\[
F_{free}(v,v)=\frac4D|v|^2-\frac2{D^2}(x\cdot v)^2,
\qquad \frac4{D^2}I\le F_{free}\le\frac4D I.
\]

Em particular, é positivo definido.

### Normal explícita e resposta a qualquer tensor simétrico

Para uma matriz simétrica `C`, denote suas coordenadas na base `E_α` também por `C`, e forme

\[
N_x(C)=\left(\tfrac12x^TCx,-Cx,C\right)\in\mathbb R^{15}.
\]

Verifica-se diretamente

\[
\langle N_x(C),V\rangle=0,\qquad
\langle N_x(C),\partial_iV\rangle=0,
\]

e, portanto, `N_x(C)` é normal a `z` e a todos os `∂_iz`. Os termos de derivada da normalização desaparecem nessa contração, deixando

\[
\boxed{\langle N_x(C),\partial_i\partial_jz\rangle=\frac2D C_{ij}.}
\]

Se `W=O N_x(C)` e `δ\widehat z=W`, a identidade `⟨W,∂_i\widehat z⟩=0`, diferenciada em `x`, implica

\[
\delta F_{free,ij}=-2\langle W,\partial_i\partial_j\widehat z\rangle
=-\frac4D C_{ij}.
\]

Logo, para **qualquer campo tensorial simétrico** `K(x)`, a escolha

\[
\boxed{W_K(x)=O N_x\left(-\frac{D(x)}4K(x)\right)}
\]

realiza exatamente `δF_free=K`. Não aparecem derivadas de `K` no resultado, embora a variação seja um campo: elas cancelam pela normalidade. Se `K` é suave e tem suporte compacto, `W_K` também tem.

O controle quantitativo é

\[
|N_x(C)|^2=|C|_F^2+|Cx|^2+\tfrac14(x^TCx)^2
\le D^2|C|_F^2,
\qquad\boxed{|W_K|\le\frac{D^2}{4}|K|_F.}
\]

### Certificado de Gram positivo

O espaço normal a `z,dz` tem dimensão dez e é parametrizado por `C↦N_x(C)`. O operador de segunda forma `W↦⟨W,∂²z⟩` envia `N_x(C)` a `2C/D`. Assim o Gram das dez segundas derivadas projetadas no normal satisfaz

\[
\boxed{M(x)\ge\frac4{D(x)^4}I_{10}.}
\]

Na bola positiva acima, `D≤121/120`, logo `M≥4(120/121)^4 I`. Em `x=0`, o Gram é exatamente `4I₁₀`. Esse certificado é explícito; sua positividade não é uma hipótese que repete a sobrejetividade pretendida.

### Curvas admissíveis exatas

Toda variação normal considerada é realizada pela curva

\[
\widehat z_t=2\frac{\widehat z+tW_K}{|\widehat z+tW_K|},
\qquad Q^{free}_\ell(t)=\widehat z_{t,\ell}^2/4.
\]

Como `⟨\widehat z,W_K⟩=0`, sua derivada em zero é `W_K`. A soma das probabilidades é exatamente um. Em suportes compactos e para parâmetro suficientemente pequeno, a positividade estrita persiste.

## 3. Mistura com um residual: isometria e liberdade simultaneamente

Seja `𝓡>0` um tensor riemanniano suave prescrito em uma vizinhança. Após restringir a um compacto interior, existem `μ,L>0` com `𝓡≥μI` e `F_free≤LI`. Escolha uma constante

\[
0<\eta<\min\{1/2,\mu/(2L)\},\qquad
F_{rest}=\frac{\mathcal R-\eta F_{free}}{1-\eta}>0.
\]

O tensor `F_rest` pode ser realizado localmente por probabilidades positivas `Q_rest`: um mergulho isométrico suave de Nash seguido da construção em pares seno/cosseno na esfera de raio dois fornece essa realização. O passo usa o Teorema 2 de Nash para uma extensão compacta da métrica e foi detalhado na nota anterior. [Nash, *The Imbedding Problem for Riemannian Manifolds*, Teorema 2, p. 59](https://mccuan.math.gatech.edu/courses/6455/nash55.pdf); [demonstração local anterior](<C:/IALD/Central de Patentes/Chatgpt/REPRESENTACAO_FISHER_LORENTZ_LOCAL_20260909_202637_1088578/NOTA_REPRESENTACAO_LOCAL.md>).

Use ramos disjuntos para definir a mistura de peso **constante**

\[
Q=(\eta Q_{free},(1-\eta)Q_{rest}).
\]

Então `F[Q]=ηF_free+(1−η)F_rest=𝓡`. Variações somente no bloco livre, congelando o restante e `η`, dão `δF[Q]=ηK`, com a fórmula explícita da seção 2. Dessa forma, a mesma realização possui isometria exata e liberdade de variação. Não foi necessário supor liberdade do mapa fornecido por Nash, nem um inverso suave da escolha de Nash em função da métrica.

Uma contagem suficiente, sem otimização, usa quinze probabilidades no bloco livre e 92 no bloco de Nash em dimensão quatro: 107 condicionais por grupo. Essa é uma escolha finita de construção, não uma afirmação de minimalidade.

## 4. Liberdade conjunta de métrica e campos sigma coletivos

Suponha que cada `Q_a` seja construído como acima; basta, de fato, que um grupo `a*` contenha um bloco livre de peso constante `η>0`. Ponha `s=1−q`. Mantenha `q` fixo. A variação de `F[P]` devida a uma variação coletiva `δφ=ψ`, com `Σ_aφ_aψ_a=0`, é

\[
D_\phi F[\psi]=4s\sum_a d\phi_a\odot d\psi_a
+2s\sum_a\phi_a\psi_aF[Q_a],
\]

onde `α⊙β=α⊗β+β⊗α`.

Para a métrica refletida, escreva `c=dq`, `w=F⁻¹c`, `b=c(w)>0` e

\[
g=2c\otimes c/b-F,\qquad
L_F(h)=-h+2h(w,w)c\otimes c/b^2.
\]

Como `q` está fixo, `δg=L_F(δF)` e `L_F²=Id`. Dado qualquer par de variações suaves compactamente suportadas `(h,ψ)`, com `h` simétrica e `ψ` tangente à esfera sigma, escolha no bloco livre do grupo `a*`

\[
\boxed{K=\frac{L_F(h)-D_\phi F[\psi]}{s\phi_{a*}^2\eta}.}
\]

A variação interna da seção 2 realiza esse `K`. Consequentemente, a variação total satisfaz **`δg=h` e `δφ=ψ`**, mantendo o relógio fixo. Não há cancelamento presumido: o termo métrico produzido por `ψ` é explicitamente compensado pelas condicionais internas.

As curvas coletivas podem ser escolhidas como `φ(t)=(φ+tψ)/|φ+tψ|`, e as condicionais pela curva esférica da seção 2. As probabilidades finas são então reconstruídas exatamente por `P_{aℓ}(t)=sφ_a(t)²Q_{aℓ}(t)`. Isso realiza as variações, com normalização e positividade preservadas, dentro da classe de dados adotada.

Para a componente interna da variação fina, a norma de Fisher no espaço de probabilidades obedece

\[
\|\delta P_{internal}\|_{I_P}
\le\frac{D^2}{4\sqrt{s\phi_{a*}^2\eta}}
\left|L_F(h)-D_\phi F[\psi]\right|_F.
\]

Aqui a norma tensorial do lado direito é a norma de Frobenius na carta usada para o bloco explícito; o subíndice indica Frobenius, não o tensor de Fisher do espaço-tempo. A parte coletiva tem norma `2√s|ψ|` e é ortogonal à parte interna nessa norma de probabilidades. Portanto há também um controle explícito da variação completa. Em compactos com `s`, `φ_{a*}` e `η` afastados de zero, os denominadores são uniformemente controlados. Esse controle diferencial não é uma afirmação de estabilidade global da decodificação por um único caráter real.

## 5. O recíproco variacional que de fato é obtido

Considere a ação adotada

\[
S[g,\phi,\lambda]=\int\sqrt{|g|}\left[
\frac{R-2\Lambda}{2\kappa}
-\frac C2\left(\sum_a g^{-1}(d\phi_a,d\phi_a)
+\lambda(\sum_a\phi_a^2-1)\right)\right],
\quad C>0,\quad\kappa\ne0.
\]

Na parametrização normalizada o termo de multiplicador desaparece identicamente da ação composta. A estacionariedade em todos os dados finos `P`, na classe com o certificado livre, permite os testes da seção 4:

1. Escolher `ψ=0` e todo `h` fornece a equação métrica completa `G+Λg=κT` pelo lema fundamental das variações.
2. Escolher `h=0` e todo `ψ` tangente à esfera fornece a equação sigma tangencial `Π_{φ⊥}Box_gφ=0`.
3. Como `Σφ²=1`, existe um único multiplicador que completa a equação sigma:

\[
\boxed{\lambda_{rec}=\sum_a\phi_a\Box_g\phi_a
=-\sum_a g^{-1}(d\phi_a,d\phi_a).}
\]

A segunda igualdade vem de aplicar `Box_g` à identidade `Σφ²=1`. Com esse multiplicador, `Box_gφ_a=λ_rec φ_a` e a equação de normalização também é satisfeita.

Reciprocamente, uma solução dessas equações clássicas, representada pelos dados com bloco livre, é estacionária em `P` pela regra da cadeia da primeira variação. Obtém-se assim equivalência variacional **com a equação sigma restrita à esfera e o multiplicador reconstruído**. Não se afirma que a estacionariedade em `P` determine um multiplicador arbitrário adicionado como variável redundante; ela é independente desse valor antes da reconstrução.

O certificado de liberdade é derivado de um mapa explícito e de uma mistura controlada. A equivalência não assume como hipótese que a equação de Einstein já valha, nem uma hipótese que simplesmente repita o recíproco pretendido.

## 6. Métrica e sigma prescritos: condição residual e seus limites

Para uma métrica lorentziana prescrita `g`, campos `φ` prescritos e um relógio `q` cujo diferencial seja temporal para `g`, ponha

\[
b_g=g^{-1}(dq,dq)>0,\qquad
F_{target}=2dq\otimes dq/b_g-g.
\]

A condição adicional para a construção acima é

\[
\boxed{\mathcal R=
\frac{F_{target}-dq\otimes dq/[q(1-q)]-4(1-q)\sum_a d\phi_a\otimes d\phi_a}{1-q}>0.}
\]

Ela não é automática para dados e relógio fixados. Se for satisfeita, realize `𝓡` pelo `Q` misto da seção 3 e use o mesmo `Q` como valor de fundo de todos os grupos. Como `Σφ²=1`, `Σφ_a²F[Q_a]=𝓡`, e a identidade da seção 1 fornece exatamente `F[P]=F_target`, portanto `g[P]=g` e os campos coletivos reconstruídos são exatamente os `φ` prescritos. As condicionais dos grupos continuam disponíveis para variações independentes.

Se o relógio for uma escolha livre de construção, existe ainda uma forma quantitativa de obter a positividade local. Escolha uma coordenada temporal `τ`, com `F₀=2dτ²/g⁻¹(dτ,dτ)−g>0`, e em um compacto escreva

\[
\sum_a d\phi_a^2\le MF_0,\qquad
g^{-1}(d\tau,d\tau)\le A,\qquad |\tau|\le T.
\]

Escolha `δ>0` com `δ≤1/4` e `6δM≤1/4`; tome `q=1−δ+ετ`, com `ε>0` satisfazendo `εT≤δ/2` e `ε²A≤δ/16`. Então `1−q∈[δ/2,3δ/2]`, `q≥1/2`,

\[
4(1-q)\sum_a d\phi_a^2\le\tfrac14F_0,
\qquad\frac{dq^2}{q(1-q)}\le\tfrac14F_0.
\]

Como `F_target=F₀`, o numerador residual é pelo menos `F₀/2`. Isso demonstra positividade local para essa escolha de relógio. Tal liberdade de escolher `q` é [INPUT] de representação; não autoriza alterar um relógio já determinado por dados físicos.

## 7. Representante livre do mesmo habitante Einstein–sigma ajustado

Considere a solução local anteriormente verificada, numa carta positiva da esfera unitária `S³`,

\[
g=dr^2-a(r)^2\gamma,\quad a(r)=2\cos(r/2),\quad
\phi=(\phi_1,\ldots,\phi_4)\in S^3_+,
\quad\sum_a d\phi_a^2=\gamma,
\quad\lambda=3/a^2.
\]

Os ajustes são `Λ=3/4` e `κC=4`. O representante antigo com `q_bg=sin²(r/2)` tinha residual zero e não possuía o certificado livre. Preserve **a mesma métrica e os mesmos campos sigma**, escolhendo agora, somente para a representação estendida, um relógio local `q(r)` que satisfaça

\[
q(r_0)>\sin^2(r_0/2),\qquad q'(r)\ne0,\qquad
q'(r)^2<q(r)(1-q(r)).
\]

Isso é possível com `q(r)=q₀+ε(r−r₀)`, `q₀∈(sin²(r₀/2),1)`, `ε≠0` pequeno e uma restrição da vizinhança. A desigualdade estrita `q>sin²(r/2)` persiste localmente por continuidade.

Para esse novo relógio, `F_target=dr²+a²γ`, e

\[
\boxed{\mathcal R=
\frac{\left(1-\frac{q'^2}{q(1-q)}\right)dr^2
+\left(a^2-4(1-q)\right)\gamma}{1-q}>0.}
\]

Os dois coeficientes são estritamente positivos pelas escolhas acima. A mistura da seção 3 fornece então condicionais `Q` que realizam o residual e contêm o bloco livre explícito. Usando essas condicionais nos quatro grupos, obtemos probabilidades estendidas positivas que representam **exatamente o mesmo** `g,φ,λ` ajustado, agora com liberdade conjunta de variação. Uma escolha suficiente tem 429 probabilidades finas: um relógio e quatro grupos de 107 condicionais.

O on-shell desse habitante não é presumido a partir de `P`: ele é a solução Einstein–sigma previamente calculada e é preservado pela identidade dos campos reconstruídos. No novo representante, o recíproco da seção 5 também vale, graças ao bloco livre. O antigo contraexemplo de estacionariedade com `Λ=0` permanece válido para a classe anterior sem certificado e não é apagado por esta extensão.

## 8. Estatuto do avanço

[DERIVED] Foram dados: uma identidade exata de Fisher para grupos; uma família de quinze probabilidades com Gram explicitamente positivo; uma mistura que combina realização isométrica e liberdade; um inverso explícito da primeira variação conjunta; e um representante livre do mesmo habitante ajustado, mantendo todos os dados internos no registro.

[INPUT/POSTULATE] A partição, o novo relógio quando escolhido, a parametrização ampliada e a ação Einstein–sigma são parte do modelo adotado. [KNOWN] A existência da realização riemanniana residual usa Nash. [OPEN] Esta prova não seleciona esses dados na natureza, não elimina as redundâncias restantes da parametrização, não fornece por si um estado quântico físico nem resolve anomalias ou a construção quântica interagente. Também não transporta para o canônico uma formalização Lean que ainda não foi realizada.

Nenhum `um.py`, integrador ou compilador Lean foi executado nesta construção escrita. As fontes e notas anteriores permanecem preservadas.
