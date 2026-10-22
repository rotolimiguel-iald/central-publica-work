# Representação probabilística livre em toda a esfera S³ e no intervalo (0,π)

[DERIVED — demonstração escrita; não compilada em Lean] O habitante Einstein–sigma da entrega 067 admite uma representação por **1.289 probabilidades estritamente positivas**, definida em todo `M=(0,π)×S³`, que preserva os sinais de `φ=id`, reproduz a mesma métrica e tem um inverso global da primeira variação conjunta de métrica e sigma. A contagem é suficiente, não mínima. A realização residual utiliza apenas o teorema de Nash para uma métrica na esfera **compacta tridimensional**, junto com fórmulas explícitas para a direção temporal.

[INPUT/POSTULATE] A partição em pares assinados, o relógio escolhido, a parametrização ampliada e a ação Einstein–sigma são dados do modelo. [KNOWN] O mergulho isométrico compacto de Nash é importado e indicado no passo exato em que entra. O resultado não afirma uma representação para todo relógio previamente selecionado ou para toda topologia. A carta positiva de quatro amplitudes da entrega anterior não foi estendida por decreto: é substituída por uma codificação global diferente, reversível e explicitada abaixo.

## 1. O mesmo campo sigma global em oito pesos coletivos positivos

Seja `φ=(φ₁,…,φ₄):M→S³⊂ℝ⁴`, com seus sinais usuais. Para `0<ε<1`, defina oito pesos

\[
B_{a,+}=\frac{1+\varepsilon\phi_a}{8},\qquad
B_{a,-}=\frac{1-\varepsilon\phi_a}{8},\qquad a=1,\ldots,4.
\]

Eles satisfazem globalmente

\[
B_{a,\pm}\ge\frac{1-\varepsilon}{8}>0,\quad
B_{a,+}+B_{a,-}=\frac14,\quad\sum_{a,\pm}B_{a,\pm}=1,
\quad\boxed{\phi_a=\frac4\varepsilon(B_{a,+}-B_{a,-}).}
\]

Os rótulos `+` e `−` fazem parte do registro; nenhum sinal da componente física é omitido. A imagem é a subvariedade dos pesos positivos que satisfaz as quatro relações de pares e

\[
\sum_a\left[\frac4\varepsilon(B_{a,+}-B_{a,-})\right]^2=1.
\]

Essas relações são vínculos explícitos da parametrização, não equações adicionais da dinâmica. A construção é uma codificação suave global da esfera como subvariedade do simplex; não pretende fornecer uma única carta euclidiana de S³.

A contribuição de cada par ao tensor de Fisher dá exatamente

\[
\boxed{F_B=\sum_a\frac{\varepsilon^2}{4(1-\varepsilon^2\phi_a^2)}
\,d\phi_a\otimes d\phi_a.}
\]

Escolheremos `ε=1/2`. Para `φ=id` na esfera unitária, `Σ_a dφ_a²=γ`, e

\[
\frac1{16}\gamma\le F_B\le\frac1{12}\gamma,
\qquad B_{a,\pm}\ge\frac1{16}.
\]

A fórmula é regular inclusive nos pontos em que uma ou várias componentes de φ se anulam.

## 2. Dados finos e identidade exata de Fisher

Enumere os oito rótulos coletivos por `b`. Para condicionais positivas normalizadas `Q_{b\ell}`, escreva

\[
P_0=q,\qquad P_{b\ell}=(1-q)B_bQ_{b\ell},\qquad
\sum_\ell Q_{b\ell}=1.
\]

Todos os dados finos são recuperados de P:

\[
s=1-q,\quad B_b=\frac{\sum_\ell P_{b\ell}}s,
\quad Q_{b\ell}=\frac{P_{b\ell}}{sB_b},
\quad\phi_a=\frac4\varepsilon(B_{a,+}-B_{a,-}).
\]

Portanto o registro guarda relógio, componentes físicas assinadas e todas as condicionais. As normalizações cancelam os termos cruzados e fornecem

\[
\boxed{F[P]=\frac{dq^2}{q(1-q)}+(1-q)F_B
+(1-q)\sum_b B_bF[Q_b].}
\]

O representante construído terá o mesmo Q em todos os oito grupos. Nesse fundo,

\[
F[P]=dq^2/[q(1-q)]+(1-q)(F_B+F[Q]).
\]

Permitir condicionais distintas durante uma variação não perde o registro; para provar a liberdade conjunta já bastará variar simultaneamente o mesmo bloco interno nos oito grupos.

## 3. Um relógio global que paga a positividade residual

Preserve o fundo físico da entrega 067:

\[
g=dr^2-a(r)^2\gamma,\quad a(r)=2\cos(r/2),\quad
\phi(r,z)=z,\quad r\in(0,\pi),\ z\in S^3.
\]

A ação física tem `c>0`, `κc=4` e `Λ=3/4`. Os extremos r=0 e r=π continuam fora do espaço-tempo adotado.

Para uma constante `0<ρ<1/4`, escolha

\[
s=\rho a^2,\qquad q=1-\rho a^2,
\qquad q'=2\rho\sin r>0.
\]

Logo `0<q<1` em todo M e `dq` é temporal, nunca zero no intervalo aberto. Para a métrica g prescrita,

\[
b_g=g^{-1}(dq,dq)=q'^2,\qquad
F_{target}=2dq^2/b_g-g=dr^2+a^2\gamma.
\]

O custo de Fisher do relógio e seu complemento são

\[
\frac{q'^2}{q(1-q)}=\frac{4\rho\sin^2(r/2)}q,
\qquad 1-\frac{q'^2}{q(1-q)}=\frac{1-4\rho}q>0.
\]

O tensor que deve ser realizado pelas condicionais é, portanto,

\[
\boxed{\mathcal R
=\frac{F_{target}-dq^2/[q(1-q)]-sF_B}s
=\frac{1-4\rho}{\rho q a^2}dr^2+\frac1\rho\gamma-F_B.}
\]

Fixe agora `ρ=1/8` e `ε=1/2`. Temos

\[
q=1-a^2/8\in(1/2,1),\qquad
\mathcal R=A(r)dr^2+8\gamma-F_B,
\quad A(r)=\frac4{q a^2}\ge1.
\]

Na métrica auxiliar global `k=dr²+γ`,

\[
\boxed{\mathcal R\ge dr^2+\frac{95}{12}\gamma\ge k.}
\]

Essa cota inferior é uniforme em `(0,π)×S³`. A componente radial cresce quando r se aproxima de π; uma cota inferior uniforme não é uma cota superior, nem uma extensão regular através desse extremo.

## 4. Bloco livre global com 21 probabilidades

Use a inclusão usual da esfera em ℝ⁴ e defina, globalmente,

\[
e=1/100,\quad t=r-\pi/2,\quad X=e(t,z)\in\mathbb R^5,
\quad D=1+|X|^2/2.
\]

Em `Sym₅`, tome uma base ortonormal de Frobenius `E_α`, `α=1,…,15`. Ponha

\[
V(X)=\left(1,X,\big(\tfrac12X^TE_\alpha X\big)_\alpha\right)\in\mathbb R^{21},
\qquad Z(X)=2V(X)/D.
\]

As identidades quadráticas dão `|V|²=D²`, `|Z|²=4`. Escolha uma transformação ortogonal constante O que leve o primeiro vetor da base à direção `(1,…,1)/√21`; uma reflexão de Householder fornece uma escolha explícita. Defina

\[
\widehat Z=OZ,\qquad Q^{free}_\ell=\widehat Z_\ell^2/4.
\]

Como `|t|<π/2<2`, temos

\[
|X|^2<1/2000<1/84,\qquad D<4001/4000,
\qquad |Z-2e_0|^2=4|X|^2/D.
\]

A distância ao centro positivo implica `\widehat Z_ℓ≥1/√21` e, consequentemente,

\[
\boxed{Q^{free}_\ell\ge1/84,\qquad\sum_{\ell=1}^{21}Q^{free}_\ell=1}
\]

em toda a esfera e em todo o intervalo. A transformação O é a mesma em todos os pontos; não há colagem de cartas nem pesos de partição variáveis.

### Métrica do bloco livre

Para a aplicação ambiente em ℝ⁵,

\[
F_{free}(v,v)=4|dX(v)|^2/D-2\langle X,dX(v)\rangle^2/D^2.
\]

No cilindro, `z·dz=0`, portanto

\[
\boxed{F_{free}=f_r(r)dr^2+f_s(r)\gamma,}
\]

\[
f_s=4e^2/D,\qquad f_r=4e^2(1+e^2/2)/D^2,
\qquad 0<f_r,f_s\le4e^2=1/2500.
\]

Essa separação temporal/espacial será utilizada para realizar o residual sem um teorema de Nash não compacto.

## 5. Inverso normal global explícito

Para `C∈Sym₅`, usando suas quinze coordenadas de Frobenius, defina

\[
N_X(C)=\left(\tfrac12X^TCX,-CX,C\right)\in\mathbb R^{21}.
\]

O cálculo algébrico fornece

\[
\langle N,V\rangle=0,\qquad \langle N,\partial_{X_i}V\rangle=0,
\quad \langle N,\partial_{X_i}\partial_{X_j}Z\rangle=2C_{ij}/D.
\]

Ao restringir ao cilindro, surgem segundas derivadas de X, mas sua contribuição é pareada com `dZ` e desaparece pela segunda identidade. Se `W=ON_X(C)`, a variação normal produz

\[
\boxed{\delta F_{free}(v,w)=-\frac4D C(dX(v),dX(w)).}
\]

Para inverter essa operação sem escolher um referencial global de `TS³`, use o projetor suave

\[
\Pi_z=I_4-zz^T,\qquad
L_z:\mathbb R\oplus\mathbb R^4\longrightarrow T_{(r,z)}M,
\quad L_z(u_0,u')=(u_0,\Pi_z u').
\]

Esse mapa é uma coisometria para `k` e a métrica euclidiana, e `L_z dX=e Id`. Para qualquer tensor simétrico global K, escolha

\[
C_K(u,v)=-\frac D{4e^2}K(L_z u,L_z v),\qquad
\boxed{W_K=O N_X(C_K).}
\]

Resulta `δF_free=K` ponto a ponto, globalmente. As derivadas de K na variação da métrica cancelam pela normalidade. A construção preserva suporte e é suave em toda a esfera, inclusive onde qualquer coordenada z_a se anula.

O controle de norma é

\[
|N_X(C)|^2=|C|_F^2+|CX|^2+\tfrac14(X^TCX)^2\le D^2|C|_F^2,
\qquad
\boxed{|W_K|\le\frac{D^2}{4e^2}|K|_k.}
\]

Equivalente a esse controle, o Gram das dez componentes da segunda forma normal da imersão quadridimensional satisfaz

\[
\boxed{M_{normal}\ge\frac{4e^4}{D^4}I_{10}
\ge4e^4(4000/4001)^4I_{10}.}
\]

A expressão é intrínseca à norma de Frobenius induzida por k; as dez componentes podem ser escritas em qualquer referencial ortonormal local. Não se exige um referencial global escolhido para provar a cota, pois o inverso foi construído pelo projetor global.

Para K de suporte compacto, a curva exata

\[
\widehat Z_u=2\frac{\widehat Z+uW_K}{|\widehat Z+uW_K|},\qquad
Q^{free}_\ell(u)=\widehat Z_{u,\ell}^2/4
\]

realiza a variação e preserva positividade e normalização para `|u|` suficientemente pequeno. Não se declara um único tamanho de u válido para toda família não limitada de perturbações em direção aos extremos temporais.

## 6. Realização residual global usando Nash apenas em S³

Fixe a mistura constante `η=1/2` e procure uma condicional residual de Fisher

\[
F_{rest}=2\mathcal R-F_{free}
=(2A-f_r)dr^2+(16-f_s)\gamma-2F_B.
\]

Defina a métrica na esfera compacta e a função temporal

\[
G=15\gamma-2F_B\ge\frac{89}{6}\gamma>0,
\qquad U(r)=1-f_s(r)\ge2499/2500>1/2.
\]

Então

\[
F_{rest}=(2A-f_r)dr^2+G+U\gamma.
\]

[KNOWN — único passo de existência isométrica importado] Pelo teorema de Nash para variedades compactas suaves, a esfera riemanniana `(S³,G)` possui um mergulho isométrico `y₀:S³→ℝ³⁰`, pois `n(3n+11)/2=30` quando `n=3`. O teorema inclui regularidade C∞. Fonte primária: [John Nash, *The Imbedding Problem for Riemannian Manifolds*, Teorema 2, p. 59, Annals of Mathematics 63 (1956), 20–63](https://sites.math.rutgers.edu/~feehan/teaching/math866/nash.pdf). A apresentação do resultado compacto também consta na p. 21 do artigo.

A parte temporal é construída por fórmula. Temos

\[
U'=4e^4t/D^2,\qquad |U'|<8e^4<1.
\]

Em particular,

\[
J(r):=2A-f_r-\frac{U'^2}{4U}
>2-1/2500-1/2>1.
\]

Defina

\[
T(r)=\int_{\pi/2}^{r}\sqrt{J(v)}\,dv,
\qquad
\boxed{Y(r,z)=(T(r),\sqrt{U(r)}z,y_0(z))\in\mathbb R^{35}.}
\]

A função T é suave em `(0,π)`; a integral é finita entre quaisquer dois pontos interiores. Não se precisa que T permaneça limitada ao aproximar r=π. Como `z·dz=0`,

\[
|d(\sqrt U\,z)|^2=U\gamma+\frac{U'^2}{4U}dr^2,
\]

logo

\[
\boxed{Y^*\delta_{\mathbb R^{35}}=Jdr^2+U\gamma+
\frac{U'^2}{4U}dr^2+G=F_{rest}.}
\]

Isso demonstra uma realização euclidiana suave **global** do residual no cilindro aberto usando apenas Nash compacto em dimensão três. Não foi necessário aplicar um resultado de existência isométrica a uma variedade não compacta, nem construir uma partição de unidade com termos de Fisher adicionais.

## 7. De qualquer coordenada euclidiana a amplitudes positivas globais

Uma rotação de pares seno/cosseno só garantiria positividade numa imagem pequena. Para evitar essa limitação, cada coordenada `Y_j`, `j=1,…,N`, é convertida em quatro amplitudes deslocadas. Escolha `d_j>0` com `18Σ_j d_j²=4` e ponha

\[
\vartheta_j=Y_j/(\sqrt2\,d_j),
\]

\[
Z_{j,1}=2d_j+d_j\cos\vartheta_j,\quad
Z_{j,2}=2d_j-d_j\cos\vartheta_j,\quad
Z_{j,3}=2d_j+d_j\sin\vartheta_j,\quad
Z_{j,4}=2d_j-d_j\sin\vartheta_j.
\]

Cada amplitude é pelo menos d_j, independentemente do número de voltas da fase. As identidades são

\[
\sum_{\ell=1}^4Z_{j,\ell}^2=18d_j^2,
\qquad\sum_{\ell=1}^4dZ_{j,\ell}^2=dY_j^2.
\]

Defina `Q^{rest}_{j,ℓ}=Z_{j,ℓ}²/4`. Temos então, globalmente,

\[
\sum_{j,\ell}Q^{rest}_{j,\ell}=1,\quad Q^{rest}_{j,\ell}>0,
\quad\boxed{F[Q^{rest}]=\sum_jdY_j^2=F_{rest}.}
\]

Para `N=35`, a escolha uniforme `d_j²=2/(9N)` produz 140 condicionais com

\[
\boxed{Q^{rest}_{j,\ell}\ge1/(18N)=1/630.}
\]

Os deslocamentos não introduzem um termo de Fisher esquecido: o raio total é exatamente constante e a soma dos quadrados das derivadas foi calculada. A periodicidade pode perder a coordenada Y isolada, mas não perde o ponto do espaço-tempo nem o campo físico na representação completa, como será demonstrado abaixo. O papel de Y aqui é realizar a métrica residual; não é declarado um dado independente que o registro teria de decodificar.

## 8. Representante completo: 1.289 probabilidades

Tome ramos internos disjuntos e a mistura **constante**

\[
Q=(\tfrac12Q^{free},\tfrac12Q^{rest}).
\]

Ela possui `21+140=161` componentes e

\[
F[Q]=\tfrac12F_{free}+\tfrac12F_{rest}=\mathcal R,
\qquad Q_\ell\ge1/1260.
\]

Use esse Q em cada um dos oito grupos coletivos e acrescente o relógio. O total é

\[
\boxed{1+8\cdot161=1289.}
\]

As probabilidades finas obedecem, em todo M,

\[
P_0=q>1/2,\qquad
P_{b\ell}=sB_bQ_\ell\ge\frac{a^2}{161280}>0,
\qquad\sum_iP_i=1.
\]

A identidade de Fisher dá exatamente `F[P]=dr²+a²γ=F_target`. Refletir esse tensor com o relógio `dq` devolve

\[
\boxed{g[P]=dr^2-a^2\gamma=g,\qquad\phi[P]=\phi=id_{S^3}.}
\]

A configuração física foi preservada em toda a esfera. Além disso, o mapa `(r,z)↦P(r,z)` é injetivo e tem inversa suave sobre sua imagem: `q` determina r, pois é estritamente crescente,

\[
r=2\arccos\sqrt{2(1-q)},
\]

e as diferenças dos pares determinam `z_a=φ_a`. Assim a periodicidade auxiliar do bloco residual não introduz uma identificação dos pontos físicos. Essa afirmação sobre a imagem concreta não é uma prova de estabilidade de toda decodificação abstrata por um único caráter real.

## 9. Liberdade conjunta global de g e φ

Considere agora variações arbitrárias suaves de suporte compacto em M, `h=δg` e `ψ=δφ`, com `φ·ψ=0`. Use o mesmo relógio, `δq=0`. A variação dos pesos coletivos é

\[
\delta B_{a,\pm}=\pm\varepsilon\psi_a/8.
\]

Para `c_a(φ_a)=ε²/[4(1−ε²φ_a²)]`,

\[
\delta F_B[\psi]=\sum_a\left[
\frac{\varepsilon^4\phi_a\psi_a}{2(1-\varepsilon^2\phi_a^2)^2}d\phi_a^2
+c_a\,d\phi_a\odot d\psi_a\right].
\]

Como as condicionais dos oito grupos coincidem no fundo, `Σ_bδB_b F[Q_b]=0`. Ao variar simultaneamente o mesmo bloco livre em todos os grupos, a resposta total é

\[
\delta F[P]=s\,\delta F_B[\psi]+s\eta\,\delta F_{free},\qquad\eta=1/2.
\]

Com `w=F^{-1}dq`, `b=dq(w)`, a derivada da reflexão a relógio fixo é a involução

\[
L_F(H)=-H+2H(w,w)dq^2/b^2,\qquad L_F^2=Id.
\]

Escolha o tensor global

\[
\boxed{K_{h,\psi}=\frac{L_F(h)-s\,\delta F_B[\psi]}{s\eta}.}
\]

A seção normal `W_{K_{h,ψ}}` da seção 5 realiza `δF_free=K_{h,ψ}`. Portanto a variação fina reconstruída satisfaz

\[
\boxed{D\Phi\,R(h,\psi)=(h,\psi)}
\]

**globalmente em `(0,π)×S³`**. `R` é diferencial de ordem no máximo um e preserva suporte. Não possui uma singularidade nas faces `φ_a=0`; essas faces deixaram de ser fronteiras da parametrização. Os fatores `1/s` podem crescer quando r→π, mas são suaves no domínio aberto e limitados em qualquer faixa temporal compacta interior.

As curvas `φ_u=(φ+uψ)/|φ+uψ|`, junto com as curvas esféricas internas, realizam as variações exatamente e preservam todos os vínculos de pares e da esfera para parâmetro suficientemente pequeno no suporte compacto. O certificado de Gram estritamente positivo garante também liberdade em vizinhanças C² do bloco em compactos, sem assumir a equação de Einstein para obter essa liberdade.

## 10. Consequências variacionais, lineares e de transporte do estado

Adote a mesma ação física da quantização,

\[
S_{phys}=-\frac1{2\kappa}\int\mu_g(R-2\Lambda)
+\frac c2\int\mu_g\sum_a g^{-1}(d\phi_a,d\phi_a),
\qquad |\phi|^2=1.
\]

A ação composta é **`S_{P,phys}=S_phys∘Φ`**. O sinal é o da [convenção explícita da entrega 067](<C:/IALD/Central de Patentes/Chatgpt/CONVENCAO_ACAO_ESTADO_LOCAL_20260909_214710_215498/CONVENCAO_SINAL_E_TRANSPORTE.md>); não se identifica uma forma simplética com a sua negativa.

Na classe de dados com o certificado livre global, testar estacionariedade contra `R(h,ψ)` recupera as equações métricas e sigma restritas no interior de todo M. O multiplicador geométrico é reconstruído por `λ_geom=−Σ_a g^{-1}(dφ_a,dφ_a)`; se o termo da ação for `λ_phys(|φ|²−1)/2`, então `λ_phys=cλ_geom`. A ação e a representação continuam entradas explícitas. O habitante com `κc=4`, `Λ=3/4` é um representante concreto on-shell dessa classe.

No fundo construído, `A=DΦ` e R são operadores globais suaves, `AR=Id`. O argumento do [adendo linearizado](<C:/IALD/Central de Patentes/Chatgpt/ADENDO_LINEARIZADO_COARSE_LIVRE_20260909_214421_410751/ADENDO_LINEARIZADO_E_SIMPLÉTICO.md>) passa a valer no cilindro inteiro: `R^*A^*=Id` sobre distribuições, `B=A^*HA` para a Hessiana restrita, `Bp=0⇔HAp=0`, e os quocientes por `ker A` e difeomorfismos admissíveis correspondem.

A corrente composta contém o termo de integração por partes `J^μ=E_α b^{αμ}_i p^i`, com `A=a+b∂`. No fundo, sua diferença em relação ao pullback da corrente ambiente é `(HAp₁)_αb^{αμ}_ip₂^i−(HAp₂)_αb^{αμ}_ip₁^i`, que se anula nas soluções linearizadas. Logo as formas coincidem nas seções de Cauchy `r=const`, agora **S³ inteiras e sem fronteira espacial**. Em faixas temporais interiores, Stokes e as equações lineares dão conservação; os extremos excluídos não são usados como superfícies de integração.

Consequentemente, se usamos o espaço de soluções e o grupo de gauge da [construção física de Hadamard da entrega 067](<C:/IALD/Central de Patentes/Chatgpt/HADAMARD_ACOPLADO_AUDITORIA_20260909_213919_496912/ESTADO_FISICO_HADAMARD_E_CONTRATOS.md>), a obstrução anterior de ausência de uma representação probabilística global em S³ foi removida **para este fundo e esta extensão**. O isomorfismo simplético global permite transportar o estado da álgebra física reduzida ao quociente da representação fina. Essa composição utiliza a construção de estado anterior; os controles CAS desta nota não provam novamente a completude SVT ou sua análise microlocal.

O resultado é sobre o quociente das perturbações. Ainda não define probabilidades como operadores positivos para toda amplitude gaussiana, uma seleção física única de estado, um problema não linear quântico, ou uma parametrização global para todo fundo gravitacional. A possibilidade de representar o fundo e todas as suas direções lineares não assegura que toda solução linearizada integre uma família exata global de soluções; as condições não lineares de segunda ordem em Cauchy compacta continuam distintas.

## 11. Evidência e limites desta entrega

[REAL — execução de controles exatos] O script novo `verify_global_s3.py` foi executado com Python e SymPy 1.14.0. O recibo `VERIFICACAO_GLOBAL_S3.json` contém **47/47 controles aprovados**, cada qual com residual simbólico zero. Foram conferidas as identidades quadráticas em ℝ⁵, normais e Hessianas, os pares assinados, as quatro amplitudes positivas, o relógio, a separação radial/espacial e as contagens. A execução foi restrita ao script novo e gravou apenas o recibo novo nesta pasta.

[DERIVED/KNOWN] As cotas, o uso de Nash compacto, as conclusões de suavidade global e as equivalências variacionais/lineares possuem demonstrações escritas acima. Não são convertidas em teoremas Lean pela contagem de controles. Não foi importado nem executado `um.py`, e não houve integração ou compilação Lean.

[OPEN/INPUT] Permanecem: o vínculo físico com dados selecionados, a adoção da ação e dos agrupamentos, a generalização a outros fundos/topologias/relógios fixados, a extensão através dos extremos singulares quando reivindicada, a integrabilidade não linear e a quantização interagente. A margem positiva dos pesos finos não é uniforme até r=π, onde `s→0`; o enunciado é global no **intervalo aberto**, não no seu fecho. Em qualquer faixa `[r_-,r_+]×S³` estritamente interior há margens uniformes e todos os controles são regulares.

Nenhuma fonte ou nota congelada foi alterada. Este arquivo e seu manifesto são aditivos e permanecem em Chatgpt.
