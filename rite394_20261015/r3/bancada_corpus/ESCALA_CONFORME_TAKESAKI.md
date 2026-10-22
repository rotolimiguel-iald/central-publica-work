# Cones, rede modular e escala do traço

[DERIVED] Os dados pedidos não determinam uma métrica a menos de isometria sem uma ponte adicional entre traço e medida geométrica. [OPEN] A torre ainda não fornece uma rede CGMA fiel de regiões gerais. Resposta ao alvo B da ordem 001, 05/09/2026.

## 1. Qual rede existe, e qual rede seria necessária

[REAL — leitura de fontes] A torre dá a cadeia M_N⊂M_(N+1)⊂M. Estes índices são andares de um produto de matrizes; não são pontos, cunhas ou coordenadas. Cada Ω é separante para M_N mas não cíclico em H inteiro: sua órbita é H_N, finito dimensional. Portanto os pares (M_N,Ω) não são automaticamente os pares standard de cunhas exigidos para ação modular geométrica em H.

[REAL — leitura de `WedgeNet.lean`] Existe uma rede construída sobre regiões de R⁴: atribui M quando a região contém alguma cunha direita transladada; M′ quando contém alguma esquerda; o bicomutante da união quando contém ambas; o centralizador de todos os operadores quando não contém nenhuma. Translações têm U(a)=1. Assim cunhas direitas com posições distintas têm a mesma álgebra. Regiões limitadas não contêm essas cunhas e recebem apenas escalares. Essa rede satisfaz o contrato fraco do arquivo, mas não fornece a correspondência fiel entre posição e álgebra necessária para reconstruir deslocamentos. Não a renomeamos como rede CGMA completa.

A especificação da rota pretendida, ainda [INPUT], é:

1. Uma variedade X conexa, dimensão d≥3, causalidade e conjunto de cunhas W. Sem X prévio, fornecer um poset abstrato de regiões com axiomas de representação geométrica; a cadeia N sozinha não tem esses dados.
2. W↦A(W)⊂B(H), isotônica, com discriminação de regiões suficiente para reconstrução, Ω cíclico e separante em cada cunha e dualidade A(W′)=A(W)′.
3. Para regiões menores O, A(O)=∩_{W⊃O}A(W), com interseções não triviais e propriedades de standardness requeridas pela reconstrução escolhida.
4. Conjugação modular geométrica J_W A(V) J_W=A(j_W V), junto às condições de ordem e continuidade da versão de CGMA aplicada. Para identificar fluxos, também Δ_W^{it}A(V)Δ_W^{-it}=A(λ_W(t)V); esta condição é adicional à mera definição da cadeia.
5. Relações entre cunhas distintas e inclusões modulares meio-laterais que produzam translações não triviais; escolha demonstrada do espaço-tempo e da classe de simetrias. Um único grupo Δ^{it} não entrega essa família.

[KNOWN] A rota e suas hipóteses devem ser confrontadas com [Buchholz–Dreyer–Florig–Summers, Geometric Modular Action and Spacetime Symmetry Groups](https://arxiv.org/abs/math-ph/9805026). A lista acima especifica obrigações de construção para a torre, não afirma que toda lista informal de axiomas equivale ao teorema daquele artigo.

## 2. O que a escala de Takesaki realmente informa

[INPUT] Um core, seu traço semifinito τ e a ação dual θ satisfazem τ(θ_s a)=e^(−s)τ(a). θ_s é ação DUAL no core, enquanto σ_t é o fluxo modular em M. Não são identificados pelo nome do parâmetro.

[REAL — leitura] Em `BisognanoWichmann.lean`, o fator e^(−s) aparece na contração de um raio nulo pelo boost. O próprio comentário distingue coincidência da forma exponencial de identificação física. O molde `DualScalingData` está em `GlobalLiftLadder.lean`: contém τ, θ e a lei como campo; não contém métrica, medida de volume, localização nem conversão dimensional.

[DERIVED] A lei é homogênea: τ′=cτ, c>0, também a satisfaz. Mesmo se τ inteiro for fornecido com normalização fixa, falta um mapa que associe regiões geométricas a objetos do core e seus traços a volumes/áreas. Conhecer a lei de transformação de τ não fornece esse mapa.

## 3. Refutação da determinação métrica sem essa ponte

[INPUT] Suponha obtida uma rede geometricamente modular para uma métrica g. Preserve a rede, Ω, J_W, Δ_W, o core, τ e θ, e substitua g por g′=c²g, com c>0 constante.

[DERIVED] Os cones são idênticos. As mesmas transformações que são isometrias de g são isometrias de g′, porque F*(c²g)=c²F*g. O mesmo vale para ações conformes. Regiões causalmente definidas e todas as relações de inclusão/interseção continuam iguais. Parâmetros de boosts são adimensionais e não mudam. A ação modular da rede e a lei do traço permanecem literalmente as mesmas. Nenhum dos dados listados compara uma unidade de comprimento com τ.

Para que isto refute igualdade **a menos de isometria**, não basta citar Minkowski com fator constante: nesse caso uma dilatação global fornece isometria. Use uma métrica de curvatura escalar constante não nula. Exemplo em X={(t,x,y,z):t>0}:

    g = t^(-2) diag(-1,1,1,1),     g′ = 4g.

Com a convenção de Riemann R^a_bcd = ∂c Γ^a_db − ∂d Γ^a_cb + …, R(g)=12 e R(g′)=3. Nenhuma isometria, mesmo local, troca constantes escalares diferentes. Esse cálculo será reproduzido em script exato. A geometria de de Sitter admite também a formulação global: raios diferentes têm a mesma ação de grupo em coordenadas adimensionais e curvaturas escalares diferentes.

O argumento é uma **obstrução à inferência a partir dos dados indicados**: qualquer realização de uma rede compatível com ambas mantém todos esses dados. Não afirma construir aqui uma rede CGMA de de Sitter a partir da torre. Mesmo conceder a rede pretendida não introduz a calibração ausente. Se condições adicionais da rede já contiverem massa, relógio ou comprimento fixado, elas são precisamente dados extras e devem aparecer no enunciado.

## 4. Dado suficiente e custo exato

[INPUT] Uma densidade de volume positiva μ, geometricamente localizada e calibrada, fixa o representante de uma classe conforme lorentziana. Se g₀ representa a classe e g=e^(2f)g₀ em dimensão d, então

    dvol_g = e^(df) dvol_g₀,
    f = (1/d) log(dμ/dvol_g₀).

[DERIVED] Dois representantes da mesma classe que realizem a mesma densidade μ coincidem ponto a ponto. Se os dados forem apresentados abstratamente, a reconstrução fica a menos dos difeomorfismos que preservam esses dados.

Para usar τ, é preciso construir um mapa O↦q_O (ou um POVM/densidade apropriada no core), provar aditividade e compatibilidade com localização, e demonstrar τ(q_O)=C·Vol_g(O), com C finito positivo **calibrado**, onde a fórmula faz sentido. Projeções finitas de um core não são automaticamente volumes de regiões; isso é a ponte a construir. A lei dual, se interpretada como lei de volume, só daria um expoente de dilatação depois dessa identificação. Não fixa sozinha a normalização nem a função conforme espacial.

Se a ação geométrica já for provadamente isométrica e transitiva, uma função conforme invariante é constante; ainda falta uma calibração global. Sem transitividade/isometria demonstradas, pode faltar uma função inteira. Escala de área/entropia, constante G e identificação de tempo próprio continuam dados separados até haver teoremas que os liguem.
