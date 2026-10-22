# Regularidade dos jatos de Einstein–sigma e certificado polinomial de igualdade fraca

09/09/2026, arco 069. [DERIVED — demonstração escrita, não Lean]. Esta nota é nova; não altera a nota C0 do arco 068 nem qualquer fonte congelada.

**Resultado central.** Para a ação de Einstein com constante cosmológica e sigma minimamente acoplado, em uma carta suave regular do alvo, a anulação de uma forma natural polinomial na superfície estacionária **formal** equivale a pertencer ao ideal diferencial das equações, com coeficientes naturais da mesma classe. A prova abaixo constrói o split por ordem de jato e uma homotopia polinomial. Não usa uma divisão por uma componente da métrica, por gradientes da matéria ou por invariantes de curvatura.

Com a demonstração Euler/Pontryagin do arco 068, esse resultado paga o passo residual de igualdade fraca para a condição característica C0/(7.33), na classe explicitada. Isso não calcula toda a cohomologia BRST do sigma, não constrói uma teoria global do alvo nem prova convergência de séries perturbativas.

## 1. Ação, classe e significado de igualdade fraca

[INPUT] Considere, em dimensão quatro e assinatura (+---),

\[
 S[g,y]=-\frac1{2\kappa}\int(R-2\Lambda)\,d\mathrm{vol}_g
       +\frac c2\int g^{ab}h_{AB}(y)u_a^Au_b^B\,d\mathrm{vol}_g,
 \qquad u_a^A=\partial_a y^A,
\tag{1}
\]

com κ,c não nulos, Λ constante e h suave não degenerada numa carta U do alvo. Para o modelo já construído, c=k/(π cosh²k)>0, κc=4 e Λ=3/4; a prova de regularidade não precisa desses valores, nem do sinal de Λ. A aplicação topológica C0 precisa Λ>0. O alvo S³ tem, na carta y∈B³,

\[
 h_{AB}=\delta_{AB}+\frac{y_Ay_B}{1-|y|^2},\qquad
 h^{AB}=\delta^{AB}-y^Ay^B.
\]

Esses coeficientes são suaves em toda a carta; a fronteira |y|=1 não é incluída. Não há potencial, gauge interno ou gauge de Weyl. A isometria do alvo é uma simetria rígida, não uma identidade de Noether com parâmetro local arbitrário.

Ponhamos

\[
 W_{ab}=h_{AB}u_a^Au_b^B,\quad Q=g^{ab}W_{ab},\quad
 T_{ab}=c(W_{ab}-\tfrac12g_{ab}Q),
\]
\[
 E_{ab}=G_{ab}+\Lambda g_{ab}-\kappa T_{ab},\qquad
 \tau^A=g^{ab}(\partial_a\partial_b y^A-\Gamma^d_{ab}u_d^A
                  +\Gamma^A_{BC}(h)u_a^Bu_b^C).
\tag{2}
\]

As equações densitizadas de Euler são múltiplos invertíveis de E e τ. Em particular, variar g covariante dá δS/δg_ab=√|g| E^{ab}/(2κ), e variar y dá −c√|g|h_AB τ^B. O ideal não muda com esses fatores.

**Classe A_nat.** Formas tensorialmente naturais, de ordem de jato finita, polinomiais nos jatos diferenciados, com coeficientes suaves nos valores y∈U. A dependência na métrica é por g, g⁻¹, volume orientado e contrações naturais; na apresentação por vielbein são permitidos apenas denominadores det(e)^m. Constantes não nulas podem ser invertidas. Os coeficientes e suas derivadas no alvo permanecem suaves em U. Não se admitem funções suaves arbitrárias dos jatos diferenciados, denominadores em g^{00}, dy ou curvatura, referencial externo ou primitivas não tensoriais de Chern–Simons.

**Superfície estacionária formal.** E_∞ é o limite projetivo dos jatos finitos que anulam E, τ e todos os seus prolongamentos disponíveis. F≈0 significa que F se anula em todos esses jatos formais admissíveis. Não significa somente anulação num fundo escolhido, numa família de soluções, ou em dados observacionais. A realização de cada jato formal por uma solução convergente é uma questão analítica distinta e não é usada.

## 2. O que as fontes afirmam e o que se demonstra aqui

[KNOWN] [BBH 2000, §5.1.3, Lema 5.1 e Teorema 5.1](https://arxiv.org/pdf/hep-th/0002245v3) condicionam a resolução KT a um split regular de equações e identidades de Noether. O lema de igualdade fraca declara preservação polinomial; sua prova usa coordenadas independentes de EOM e uma homotopia. A definição de normalidade em §6.4.3 é adicional, ligada ao complexo linearizado e à filtragem por derivadas, não sinônimo de existência de um propagador.

[KNOWN] [BBH 1995, §2 (2.11), §3 e apêndices C–E](https://arxiv.org/pdf/hep-th/9505173v2) tratam Einstein–matéria usual como exemplo normal, usam uma álgebra polinomial nos tensores covariantes e separam a dependência no vielbein. A extensão para coeficientes suaves no alvo não deve ser presumida só pelo nome do modelo. A construção abaixo mantém essa dependência como anel de coeficientes e demonstra diretamente o certificado requerido.

[KNOWN] O [teorema de isomorfismo de jatos de Jentsch, v2, §1 e Teorema 3](https://arxiv.org/pdf/1509.08269v2) fornece a conversão universal polinomial entre jatos métricos normais e jatos de curvatura. O artigo inclui métricas pseudo-riemannianas explicitamente no primeiro parágrafo, apesar do título abreviado. [Anderson–Torre, §2C, Teoremas 2.7–2.8](https://arxiv.org/pdf/gr-qc/9404030v1), dão coordenadas e prolongações sobrejetivas para jatos Ricci-flat. O argumento próprio a seguir trata a constante cosmológica e a fonte sigma; não atribui essa extensão ao enunciado Ricci-flat.

## 3. Lema algébrico: Einstein linearizado sobre polinômios homogêneos

Fixe η=diag(1,−1,−1,−1) e escreva P_m para polinômios homogêneos de grau m em x=(t,x¹,x²,x³), com P_m=0 para m<0. Para N≥2, considere

\[
 \mathsf G_N:P_N\otimes\operatorname{Sym}^2V^*\longrightarrow
 P_{N-2}\otimes\operatorname{Sym}^2V^*,\qquad h\mapsto G^{(1)}_\eta(h),
\]
\[
 \mathsf D_N E=\partial^a E_{ab},\qquad
 \mathcal K_N=\ker\mathsf D_N.
\tag{3}
\]

**[DERIVED] Lema 1.** Im G_N=K_N. Para N≥3, D_N é sobrejetiva em P_{N−3}⊗V*. Os mapas admitem inversos à direita nos respectivos alvos com coeficientes numéricos racionais. Também □:P_N→P_{N−2} é sobrejetiva.

**Prova da afirmação Einstein, com sinais verificáveis.** Bianchi linearizado dá Im G_N⊂K_N. Tome E∈K_N, ponha m=N−2 e use a inversão de traço \bar h_ab=h_ab−η_ab tr(h)/2. Será suficiente construir

\[
 \Box\bar h_{ab}=-2E_{ab},\qquad v_b:=\partial^a\bar h_{ab}=0,
\tag{4}
\]

pois em gauge de Donder G^{(1)}(h)=−□\bar h/2.

Existe um inverso polinomial da Laplaciana espacial Δ₃ em cada grau. Para f homogêneo de grau d em três variáveis, com ρ²=Σ_i(x^i)², um inverso é

\[
 R_\Delta f=\sum_{j=0}^{\lfloor d/2\rfloor}a_j\rho^{2j+2}\Delta_3^j f,
 \quad a_0=\frac1{2(2d+3)},\quad
 a_j=-\frac{a_{j-1}}{2(j+1)(2d-2j+3)}.
\tag{5}
\]

A identidade Δ₃(ρ^{2j+2}Δ₃^j f)=2(j+1)(2d−2j+3)ρ^{2j}Δ₃^j f+ρ^{2j+2}Δ₃^{j+1}f prova Δ₃R_Δf=f por cancelamento telescópico. Todos os denominadores são inteiros positivos.

Escolha em t=0 os dados A_ab=\bar h_ab|₀ e B_ab=∂_t\bar h_ab|₀:

\[
 A_{00}=2R_\Delta(E_{00}|_0),\quad A_{0i}=A_{ij}=0,
 \quad B_{00}=B_{0i}=0.
\tag{6}
\]

Para B_ij, tome V_i=R_Δ(−2E_{0i}|₀) e

\[
 B_{ij}=\partial_iV_j+\partial_jV_i-\delta_{ij}\partial_kV_k,
 \qquad \partial_jB_{ji}=-2E_{0i}|_0.
\tag{7}
\]

A tem grau N e B grau N−1. Resolva (4) por Taylor em t: se \bar h=Σ_{j=0}^N t^j H_j e E=Σ t^j E_j, então H₀=A, H₁=B e

\[
 H_{j+2}=\frac{\Delta_3H_j-2E_j}{(j+2)(j+1)}.
\tag{8}
\]

A recorrência termina porque os graus espaciais diminuem; produz um polinômio homogêneo total de grau N. Como ∂^aE_ab=0, □v_b=0. Os dados acima dão

\[
 v_b|_0=0,\quad
 \partial_tv_0|_0=\Delta_3 A_{00}-2E_{00}|_0-\partial_iB_{i0}=0,
\]
\[
 \partial_tv_i|_0=\Delta_3 A_{0i}-2E_{0i}|_0-\partial_jB_{ji}=0.
\tag{9}
\]

Unicidade da mesma recorrência homogênea implica v=0. Inverta o traço novamente para obter h. Isso prova sobrejetividade, por um mapa linear racional.

A sobrejetividade de □ sem condição tensorial segue da recorrência (8) com dados iniciais zero e fonte qualquer. Para D_N, dado f_b∈P_{N−3}⊗V*, escolha □V_b=f_b e defina E_ab=∂_aV_b+∂_bV_a−η_ab∂^cV_c. Então ∂^aE_ab=f_b. □

**O tempo usado nessa prova é auxiliar.** Trata-se de uma prova de sobrejetividade de mapas entre espaços de dimensão finita, não de um operador inverso físico ou não local de EOM. Nenhum campo ou componente da métrica foi invertido.

## 4. Jatos normais e inversos covariantes sem denominadores novos

Denote por N_N o subespaço dos h∈P_N⊗Sym²V* tais que h_ab(x)x^b=0. É o espaço dos coeficientes métricos homogêneos em coordenadas normais.

**[DERIVED] Lema 2.** A restrição G_N:N_N→K_N continua sobrejetiva. Para N≥2, um h arbitrário pode ser posto nessa forma por uma transformação puramente gauge com coeficientes racionais:

\[
 f_a=h_{ab}x^b,\quad F=h_{ab}x^ax^b,\quad
 \xi_a=\frac1N\left(f_a-\frac{\partial_aF}{2(N+1)}\right),
 \qquad h^{\rm nor}_{ab}=h_{ab}-\partial_a\xi_b-\partial_b\xi_a.
\tag{10}
\]

Com ξ homogêneo de grau N+1, ξ_ax^a=F/[2(N+1)] e (∂_aξ_b+∂_bξ_a)x^b=∂_a(ξ·x)+Nξ_a=f_a. Portanto h^nor x=0. Einstein linearizado anula esse termo gauge, provando o lema.

Os espaços N_N, K_N, Im D_N e os espaços escalares são representações tensorais finitas do grupo de Lorentz, e os mapas G_N,D_N,□ são equivariantes. A completa redutibilidade permite escolher complementos e inversos à direita **equivariantes**. Eis a justificativa algébrica usada, para não disfarçar uma média inexistente sobre grupo não compacto:

1. Complexifique. A álgebra so(1,3)_C≅sl₂(C)⊕sl₂(C) é semissimples. Suas representações finitas são completamente redutíveis, de modo que toda sequência exata desses módulos se cinde.
2. A condição de ser uma cisão e comutar com os geradores de Lorentz é um sistema linear finito com coeficientes racionais, pois η, derivação, simetrias e contrações têm tais coeficientes. Uma solução complexa implica consistência desse sistema racional; eliminação de Gauss produz uma solução racional real.
3. Se desejadas as componentes desconexas do grupo ortogonal, faça a média finita das cisões conjugadas por representantes. Não se faz média integral sobre Lorentz. Para formas orientadas basta a versão orientada.

Logo os inversos e projetores necessários são construídos com constantes numéricas e operações tensorais. Esta prova de existência de cisões não lista suas matrizes para cada N; não precisa de limites ou inversões dependentes do campo. Em outro referencial, a mesma cisão transforma tensorialmente. A identificação por jatos normais/curvatura converte o resultado em operações naturais, com apenas os inversos de g permitidos. Não permanece o eixo temporal escolhido nas equações (6)–(9).

## 5. Triangularidade da ação completa e a identidade de Noether

Fixe y e g num ponto, escolha um referencial ortonormal orientado e coordenadas normais. Os coeficientes métricos H_N∈N_N, N≥2, são independentes; a condição de normalidade é linear em cada grau. Os jatos simetrizados covariantes do mapa, Y_N∈Sym^N V*⊗T_yU, também são independentes: sua diferença dos jatos parciais de ordem N envolve apenas jatos de ordem inferior e coeficientes suaves de h. Para N=1 temos u livre. A dependência de Y_N nos jatos métricos vai no máximo até ordem N−1, de modo que essa mudança de coordenadas permanece triangular.

Escreva E_N para o polinômio homogêneo de grau N−2 que representa ∇_{(I)}E, |I|=N−2, com a normalização Taylor usual. De modo análogo escreva τ_N para D_{(I)}τ. Nos coeficientes de ordem N,

\[
 E_N=\mathsf G_NH_N+F_N(\text{jatos}<N),\qquad
 \tau_N=\Box Y_N+J_N(\text{jatos}<N).
\tag{11}
\]

Os termos F_N,J_N são polinomiais em jatos diferenciados, com coeficientes suaves em y. A fonte E_N envolve derivadas do mapa no máximo de ordem N−1, pois T é quadrático em dy. A equação τ_N envolve jatos métricos no máximo de ordem N−1, pois a conexão métrica tem uma derivada. Λg e a curvatura do alvo não alteram os dois blocos principais de (11).

**Noether off-shell, incluindo a matéria:**

\[
 \nabla^aE_{ab}+\kappa c\,h_{AB}\tau^A u_b^B=0.
\tag{12}
\]

Deriva-se tanto da variação difeomórfica de (1) quanto de ∇^aT_ab=c h(τ,u_b). Em ordem N≥3, (12) e seus prolongamentos exprimem D_NE_N em termos polinomiais de E e τ de ordem de jato **menor que N**. Comutar e simetrizar derivadas acrescenta curvatura multiplicando prolongamentos inferiores de E; não acrescenta uma condição independente. Em particular, num jato estacionário de ordem N−1, D_NE_N=0.

Escolha uma cisão equivarante S_N de D_N e ponha Π_N=I−S_ND_N, projetor sobre K_N. Para N=2, D_N=0 e Π_N=I. Defina como novas equações independentes

\[
 z_N=\Pi_NE_N\in\mathcal K_N,\qquad \zeta_N=\tau_N.
\tag{13}
\]

Pelo Lema 2, z_N é coordenada afim em um complemento de ker G_N no espaço H_N; ζ_N é coordenada afim em um complemento de ker □ no espaço Y_N. Se R_N e R_N^y são as cisões, as inversões explícitas têm a forma

\[
 H_N=U_N+R_N[z_N-\Pi_NF_N],\qquad
 Y_N=V_N+R_N^y[\zeta_N-J_N],
\tag{14}
\]

com U_N∈ker G_N e V_N∈ker □ livres. A inversão usa somente jatos inferiores já invertidos. Por indução em N, é uma mudança triangular polinomial, com inversa da mesma classe, para toda ordem finita.

**Não se ignoraram as constraints.** Elas são as componentes (I−Π_N)E_N=S_ND_NE_N. A identidade (12) as põe no ideal gerado pelas equações dos níveis inferiores. Em particular,

\[
 \langle E,\nabla E,\ldots,\tau,D\tau,\ldots\rangle_{\le r}
   =\langle z_2,\zeta_2,\ldots,z_r,\zeta_r\rangle
\tag{15}
\]

no anel dos jatos de ordem r. Todos os coeficientes em (15) são da classe admitida. A indução começa em N=2, quando não há identidade diferencial de ordem inferior e todas as dez componentes de Einstein e os componentes de τ são independentes.

O mesmo argumento mostra que a projeção E_r→E_{r−1} é sobrejetiva: escolha U_r,V_r arbitrários e ponha z_r=ζ_r=0. Um jato estacionário finito estende-se indutivamente a um jato estacionário formal, sem restrições extras nas coordenadas livres.

## 6. Certificado na mesma classe: o passo que faltava a C0

**[DERIVED] Teorema.** Seja F∈A_nat, de ordem de jato r, com F≈0 no sentido formal da seção 1. Então existem coeficientes naturais U_I,V_J, polinomiais nos jatos diferenciados e suaves em y, tais que

\[
 F=\sum_{|I|\le r-2}\langle U_I,\nabla_{(I)}E\rangle
   +\sum_{|J|\le r-2}\langle V_J,D_{(J)}\tau\rangle.
\tag{16}
\]

As contrações incorporam o grau de forma de F. Os coeficientes podem usar jatos até r, mas não denominadores novos. Se r<2, a conclusão é simplesmente F=0.

**Prova.** Use as coordenadas (q,z), nas quais q reúne y,u,U_N,V_N e z reúne todos os z_N,ζ_N até r. Pelo prolongamento sobrejetivo, F≈0 implica F(q,0)=0 para todos os q. Portanto

\[
 F(q,z)=\sum_\alpha z_\alpha
   \int_0^1(\partial_{z_\alpha}F)(q,tz)\,dt.
\tag{17}
\]

Aqui a integral é uma operação **finita sobre um polinômio**: cada monômio t^m é substituído por 1/(m+1). Ela não produz uma função suave arbitrária de z. Como y não é escalado, os coeficientes suaves no alvo permanecem na mesma classe. Como (14) e sua inversa são polinomiais em jatos, reescrever (17) nas coordenadas originais mantém a classe. Substitua z_N=Π_NE_N e ζ_N=τ_N para obter (16).

As cisões e as escalas de (17) são equivariantes; logo, se F é um tensor ou uma forma natural, os coeficientes da identidade total transformam nos módulos duais apropriados. Jatos normais e a conversão universal em curvatura produzem uma identidade natural que glua. Em vielbein só aparecem potências de det(e) nos denominadores, provenientes dos inversos métricos; não há divisão por g^{00} nem pelo gradiente do mapa. □

**Controle explícito no nível 2.** Ricci e Weyl são as componentes independentes da curvatura algébrica. A inversão de traço transforma E=0 em Ric_ab=Λg_ab+κcW_ab; τ é o traço do Hessiano covariante do mapa. A mudança do par (Ric,Hessiano) para (E,τ,Weyl,Hessiano sem traço) é afim e invertível, com constantes 1/2 e 1/4. A homotopia (17) já fornece nesse nível o certificado. As seções 3–5 são o pagamento efetivo da extensão a ordens arbitrárias.

## 7. Identidades independentes, KT e comparação métrica/vielbein

A sobrejetividade de D_N identifica o número exato de equações dependentes em cada ordem: para N≥3, há dim(V*⊗P_{N−3}) componentes, correspondentes aos prolongamentos simetrizados da identidade (12). Não há uma relação linear principal extra entre elas. A substituição de equações dependentes pela identidade (12) é triangular, com bloco diagonal invertível constante. Depois de (14), as únicas relações entre as coordenadas independentes z são as relações de Koszul de uma sequência de variáveis; essas relações são trivialidades algébricas, não novos parâmetros gauge.

Em uma normalização conveniente de antifields covariantes, tome

\[
 \delta p_{ab}=E_{ab},\qquad \delta r_A=h_{AB}\tau^B,
 \qquad \delta C_b^*=\nabla^a p_{ab}+\kappa c\,r_Au_b^A,
\tag{18}
\]

e prolongue por derivação. δ anula os campos; por (12), δ²C*=0. Rescalas e inversões de índices convertem (18) na normalização densitizada canônica. A mesma mudança triangular de equações redefine os antifields em pares

\[
 (p_\alpha,z_\alpha),\qquad (C_\Delta^*,\widetilde p_\Delta),
 \quad \delta p_\alpha=z_\alpha,\quad
 \delta C_\Delta^*=\widetilde p_\Delta,\quad
 \delta\widetilde p_\Delta=0.
\tag{19}
\]

Os polinômios nesses pares têm a contração de Koszul pelo operador de contagem dos pares, com inversão apenas de inteiros positivos. Todo elemento contém finitos jatos, portanto o argumento permanece finito. Isso explicita a resolução KT local correspondente: H₀ é o quociente estacionário e os graus de antifield positivos são acíclicos, mantendo o mesmo anel de coeficientes. Ghosts, sobre os quais δ não atua, podem ser incluídos como coeficientes. Essa conclusão é sobre δ, não sobre δ modulo d ou sobre s modulo d.

**Comparação suficiente para H₀.** Para g_μν=η_ab e^a_μ e^b_ν, a regra da cadeia dá

\[
 \mathcal E^{\mu}_{e,a}=2\mathcal E_g^{\mu\nu}e_{\nu a},\qquad
 \mathcal E_g^{\mu\nu}=\tfrac12\mathcal E^{\mu}_{e,a}e^{a\nu}.
\tag{20}
\]

O segundo membro é simétrico porque a identidade Lorentz anula a parte antissimétrica; a inversa usa apenas e⁻¹. Prolongar (20) preserva o ideal na classe racional. Assim o certificado métrico levanta ao vielbein e, sendo Lorentz básico, desce sem escolher uma seção global do fibrado de referenciais. Não se requer uma raiz quadrada global da métrica, uma estrutura spin ou um coframe global. Uma equivalência global de **toda** a cohomologia BRST, incluindo possíveis classes topológicas de vielbein, não decorre só dessa igualdade de ideais.

## 8. Normalidade: o que está efetivamente coberto

[DERIVED] A propriedade de regularidade necessária ao certificado H₀/KT foi demonstrada diretamente, para a equação não linear exata, em toda ordem finita. Não foi deduzida da hiperbolicidade de um único fundo. O bloco homogêneo de maior ordem é Einstein linearizado mais campos escalares de onda; as mesmas cisões provam sua aciclicidade KT e ausência de identidades locais adicionais.

Há, entretanto, uma precisão de linguagem ao importar a **normalidade** de BBH. A definição de sua filtragem de grau em campos parte de uma expansão com termo inicial quadrático. Com Λ>0, uma expansão ingênua em torno da métrica plana e mapa constante tem um termo linear cosmológico e não é essa expansão on-shell. Pode-se usar um fundo Einstein com mapa constante, ou uma filtragem formal que conte Λ como parâmetro de deformação, mas essa escolha deve ser explicitada antes de importar teoremas de δ|d que usam tal filtragem. Esta nota não troca esse contrato de localização/filtragem pelo resultado H₀ aqui provado.

Além disso, h_AB(y) suave não é, em geral, uma série analítica convergente em y. O argumento de jatos não a expande: preserva C∞(U) exatamente. Uma classificação que exija polinômios nos **campos não derivados** ou uma conclusão em uma álgebra formal diferente precisa de comparação adicional. Para o sigma S³ da carta acima, h é analítica na carta, mas avaliar uma série perturbativa no acoplamento em 1 continua sendo outra questão.

## 9. Consequência para C0 e fronteira precisa

Considere a nota anterior [Euler/Pontryagin on-shell](../CLASSES_CARACTERISTICAS_C0_20260909_221649/EULER_PONTRYAGIN_ON_SHELL_E_LIMITE_C0.md), preservada integralmente. Ela exclui, na classe natural algébrica e para Λ>0, uma identidade

\[
 A\,\mathrm{Euler}_4+B\,\mathrm{Pontryagin}_4=d\beta+\mathcal I_{\rm EOM}
\]

salvo A=B=0. Se agora se assume somente A Euler₄+B Pontryagin₄≈dβ na superfície estacionária **formal** do sigma, aplique (16) a F=A Euler₄+B Pontryagin₄−dβ. Obtém-se precisamente o certificado excluído. Logo A=B=0. A presença de dβ só aumenta a ordem finita r; não altera o argumento.

**[DERIVED] O resíduo C0/KT, referente à identificação de igualdade fraca com o ideal na classe indicada, está pago por esta demonstração escrita.** A continuação de assinatura e o teste global S⁴/CP² continuam sendo os da nota anterior. A regularidade em um mapa constante admissível permanece essencial para esse teste; uma álgebra que invertesse dy ou fosse definida apenas no setor de mapas de posto três não satisfaria o contrato.

Continuam separados:

- [OPEN/contrato específico] Transporte integral da classificação de s|d para o sigma suave e para a filtragem efetivamente adotada, além do componente característica/KT agora tratado.
- [OPEN] Classes dependentes da topologia global do alvo, large diffeomorphisms, condições de contorno e eventuais anomalias globais.
- [OPEN] QME interagente renormalizada e seus demais contratos analíticos, independência entre fundos, convergência ou completude UV.
- [ESCOPO] A equivalência “≈” provada usa jatos estacionários formais. Não usa só o conjunto de soluções de um ansatz nem pressupõe convergência de todo jato formal.

## 10. Custódia e uso

[DERIVED] Lemas 1–2, split triangular, certificado e consequência C0 são argumentos escritos de autoria desta análise. [KNOWN] Os ingredientes de isomorfismo de jatos e o enquadramento BBH estão identificados por fontes primárias e versões. [REAL] O manifesto ao lado registra os bytes e hashes efetivamente lidos dos documentos de entrada e desta nota. Nenhuma compilação Lean, execução de um.py ou ensaio físico foi realizado aqui; não se atribui aprovação a outro agente ou ao operador.

Uma implementação futura útil e limitada seria certificar as matrizes G_N,D_N e as identidades (10)–(12) para os primeiros graus, mantendo a demonstração geral acima como especificação. Isso é uma recomendação, não uma alegação de formalização já existente.
