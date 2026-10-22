# Módulos H³/H⁴ e setor explicitamente calculado de Ē_N

10/09/2026. [DERIVED — investigação escrita delimitada, subsequente à descida075]. Arquivos novos; fontes congeladas preservadas; zero CAS/Lean e nenhum um.py executado/importado.

## 1. Resultados concretos

Esta nota não identifica sem prova os módulos suaves071 com os módulos naturais formais de Q2. Ela entrega três controles:

1. No setor de escalares naturais construídos de tensores ativos, antifields mínimos e ghosts difeomórficos NÃO derivados, sem fundo explícito, E_N se anula exatamente. Isso inclui ciclos explícitos A_L de ghost4 associados a densidades naturais ativas. A ação sobre coeficientes de fundo é calculada na seção5.
2. O ciclo de ghost3 construído com o volume do alvo S³ possui uma primitiva BRST natural explícita na vizinhança formal φ=Exp_(φ0)(tξ). A prova vale quando φ0 é não constante. Esse candidato topológico não pode ser importado como gerador não trivial do H³ do esquema formal.
3. As duas classes CE³ de so(1,3), os dois geradores de H³_dR(GL⁺₄) e o ciclo de volume do alvo são objetos diferentes. Os canais de grau das fontes071 são identificados abaixo, sem atribuir a eles uma sobrevivência automática nos grupos finais.

Os grupos visados pelo [critério074, seção6](<C:/IALD/Central de Patentes/Chatgpt/NATURALIDADE_E_CURVATURA_B0_074_20260910/NORMALIZACAO_S_E_OBSTRUCAO_EULER.md>) são

\[
H^1(\bar E_N;H^4(s)),\qquad H^2(\bar E_N;H^3(s)).
\tag{1}
\]

Eles continuam exigindo a identificação dos módulos NA MESMA classe natural formal. Um cálculo de E_N num conjunto de ciclos, embora útil, não prova que esse conjunto gere todos esses módulos ou que não tenha novas relações com coeficientes de fundo.

## 2. O que071 realmente identifica em graus três e quatro

O [corolário H5_071](<C:/IALD/Central de Patentes/Chatgpt/COVARIANTIZACAO_SUAVE_071_20260910_001058_826723/COROLARIO_H5_E_ANOMALIA_LOCAL.md>) usa duas álgebras diferentes. B contém tensores covariantes, antifields covariantes, quatro ghosts de translação ξ̂ e seis ghosts Lorentz Ĉ. A_sm acrescenta o fator suave de valores de vielbein e∈GL⁺₄ e seus pares de jatos. O alvo é globalmente S³, com coeficientes C∞; não há espectador B0 nessa A_sm.

Na filtração de B por grau em ξ̂, a primeira redução usa KT e CE de so(1,3). Os graus CE possíveis são0,3,6. Antes de resolver os diferenciais restantes, os canais relevantes são:

| Ghost total | Grau ξ̂ | Grau CE | Conteúdo inicial que precisa ser completado |
|---|---:|---:|---|
| 3 | 0 | 3 | Dois polinômios primitivos θ³_α(Ĉ); ainda sujeitos à curvatura |
| 3 | 3 | 0 | Correntes características de grau3, com levantamentos KT; candidatos globais do alvo |
| 4 | 1 | 3 | Formas características de grau1 vezes θ³_α; o grau baixo é eliminado na classe071 |
| 4 | 4 | 0 | Densidades invariantes, com relações por divergências, EOM e possíveis transgressões |

Essa é uma tabela de canais, não uma declaração de uma base final de H³/H⁴. A [covariantização071](<C:/IALD/Central de Patentes/Chatgpt/COVARIANTIZACAO_SUAVE_071_20260910_001058_826723/COVARIANTIZACAO_E_H2_GLOBAL.md>) fornece os graus baixos empregados ali, mas não classifica todas as correntes do Einstein–sigma nem uma base de densidades EFT de todas as ordens.

Há uma razão concreta para não identificar θ³ com H³(s). Na decomposição de071,

\[
s\theta_\alpha^{(3)}
 =s_2\theta_\alpha^{(3)}
 =\widehat F^I\frac{\partial\theta_\alpha^{(3)}}{\partial\widehat C^I}.
\tag{2}
\]

O lado direito tem grau ξ̂2, CE2 e ghost total4, e não é identicamente zero em curvatura genérica. A conclusão “CE tem dois geradores de grau3, logo H³(s) tem dois geradores Lorentz” omite esse diferencial.

[KNOWN — alcance delimitado] Em [BBH1995, equações7.2–7.3 e teorema7.2](https://arxiv.org/pdf/hep-th/9505173v2), a conclusão completa distingue ciclos de densidades, levantamentos de correntes e polinômios de Chern–Simons/curvatura. O teorema exige a condição7.33 e a classe de coeficientes declarada. A identidade s q_P=f_P para os polinômios de transgressão mostra por que completar θ³ ainda deixa um teste de curvatura em ghost4. Não importamos a classificação inteira para o sigma suave/formal com espectadores.

No fator suave de vielbeins, o próprio argumento de decomposição071 dá, usando seus graus baixos,

\[
H^3(s,A_{\rm sm})\cong H^3(s,B)
 \oplus H^3_{\rm dR}(GL^+_4)\otimes H^0(s,B),
\]
\[
H^4(s,A_{\rm sm})\cong H^4(s,B)
 \oplus H^3_{\rm dR}(GL^+_4)\otimes H^1(s,B)
 \cong H^4(s,B).
\tag{3}
\]

O segundo termo de H³ é o par de classes de de Rham de GL⁺₄, com H⁰(s,B)=R; não é uma segunda cópia das classes CE de so(1,3). A coincidência numérica “dois graus3” vem de complexos distintos. (3) continua sendo uma identificação na A_sm global de071; não é uma identificação do H³/H⁴ natural formal de Q2.

## 3. Um setor no qual E_N pode ser calculado exatamente

Use a apresentação MÉTRICA mínima da [translação normal074](<C:/IALD/Central de Patentes/Chatgpt/HOMOTOPIA_NORMAL_COVARIANTE_074_20260910/TRANSLACAO_NORMAL_E_CURVATURA_BRST.md>), com a [precisão de frames](<C:/IALD/Central de Patentes/Chatgpt/HOMOTOPIA_NORMAL_COVARIANTE_074_20260910/PRECISAO_FRAME_LOCAL_074.md>) preservada. Temos D_N=[b_N,s], E_N=d_H−D_N, C_N=[d_H,b_N].

Defina o setor K como os escalares naturais de forma0 construídos de:

- c não derivado;
- tensores, densidades e seus derivados covariantes construídos APENAS de g,φ e dos antifields mínimos ativos;
- contrações naturais, sem B0 explícito e sem derivadas de ghosts na expressão final.

Precisamos da propriedade BRST dos coeficientes tensoriais T:

\[
sT=\mathcal L_cT+\delta T,
\qquad b_N(\delta T)=0.
\tag{4}
\]

Para g,φ e suas expressões naturais sem antifields, δT=0. Nos antifields mínimos do Einstein–sigma métrico, a parte KT e seus prolongamentos não contêm c; b_N a aniquila. A hipótese (4) é o alcance exato do argumento: ela não se estende por nome a um ghost Lorentz covariantizado ou a uma expressão que contenha derivadas de c.

Como b_Nc=dx e b_N(∂_μc^ν)=−Γ̄^ν_μσdx^σ, aplicar b_N à derivada de Lie de um tensor dá sua derivada exterior covariante para Γ̄:

\[
D_NT=b_N(sT)=\bar D T.
\tag{5}
\]

No ghost não derivado, a regra sc^ν=c^μ∂_μc^ν dá

\[
D_Nc^\nu=dx^\mu(\partial_\mu c^\nu
                         +\bar\Gamma^\nu_{\mu\rho}c^\rho)
            =\bar D c^\nu.
\tag{6}
\]

O sinal positivo da conexão vem de mover o dx da segunda inserção através do primeiro c, ambos ímpares. D_N e \bar D são derivações de grau total1. Em uma contração escalar natural completa, os termos de conexão de todos os fatores se cancelam. Assim

\[
\boxed{E_N\alpha=0,\qquad C_N\alpha=0
       \quad(\alpha\in K).}
\tag{7}
\]

C_N anula c não derivado e todos os fatores sem ghosts, inclusive os antifields em que não insere; por isso a segunda igualdade é imediata. A primeira igualdade vale nesse setor mesmo antes de impor sα=0. Para um ciclo sα=0, resulta \bar E_N[α]=0. Isso não contradiz C_N(∇̄c)=−R̄ da nota074: ∇̄c não pertence a K.

## 4. Ciclos explícitos de ghost4 e candidatos de ghost3

### 4.1 Densidades ativas

Seja L₄=ρ_L d⁴x uma densidade natural orientada de g,φ e seus jatos, sem antifields e sem B0. Defina o escalar natural

\[
A_L=\rho_L\,c^0c^1c^2c^3,
\qquad \mathrm{gh}(A_L)=4.
\tag{8}
\]

A expressão é o emparelhamento da densidade covariante de grau4 com quatro ghosts vetoriais; a escrita em coordenadas não adiciona um frame físico. Se η_c=c⁰c¹c²c³, então

\[
s\rho_L=c^\mu\partial_\mu\rho_L
              +(\partial_\mu c^\mu)\rho_L,
\qquad s\eta_c=-\eta_c\partial_\mu c^\mu.
\]

O termo c^μ∂_μρ_L η_c tem cinco ghosts não derivados em quatro dimensões e vale zero. Os termos de divergência se cancelam. Portanto

\[
\boxed{sA_L=0,\quad E_NA_L=0,\quad C_NA_L=0.}
\tag{9}
\]

Esta é uma família explícita de ciclos, válida off-shell, incluindo densidades de volume, curvatura e matéria de qualquer ordem finita permitida. Não se afirma que cada A_L represente uma classe não nula nem que densidades diferentes gerem classes independentes: relações por EOM, divergências, transformações de campos ou transgressões continuam a ser divididas no H⁴ apropriado.

### 4.2 Correntes sigma

Na apresentação de S³ como Y^A Y_A=1 em R⁴, os seis campos de Killing de rotações fornecem as correntes

\[
j_{AB}^{\mu}=c_\sigma
 (Y_A\nabla^\mu Y_B-Y_B\nabla^\mu Y_A),\qquad A<B.
\tag{10}
\]

Sua divergência é c_σ(Y_A□Y_B−Y_B□Y_A); ela é zero sob a equação sigma □Y_A=λY_A. Aqui c_σ é o coeficiente da ação sigma, distinto do ghost c. A 3-forma correspondente é J_AB=ι_(j_AB)dV_g.

O canal de ghost3 associado a uma corrente desse tipo tem termo sem antifields J_AB(c,c,c) e um termo KT de grau4 nos ghosts e antifield1, portanto também ghost3. A identidade de Noether é a entrada para completar esse representante. Quando tal levantamento é escrito com tensores ativos e c não derivado, pertence a K e (7) calcula E_N=0 sobre ele.

Não contamos “seis” como dimensão provada de H³. A lista exibe seis correntes de simetria; provar a independência modulo melhorias, a ausência de outras correntes generalizadas e a sobrevivência na completação com B0 é outra tarefa. O volume do alvo, estudado na seção6, é ainda um candidato de natureza diferente: é identicamente fechado e não uma das seis correntes de Killing.

## 5. Ação sobre coeficientes de fundo: mapa de módulos efetivo

Se β(B0) é uma forma natural de fundo, então sβ=0, D_Nβ=C_Nβ=0 e E_Nβ=d_Hβ. Para α∈K, (7) dá

\[
\boxed{E_N(\beta\alpha)=(d_H\beta)\alpha.}
\tag{11}
\]

Os sinais de Leibniz são os de grau total; o termo com E_Nα é zero. Para sα=0, esta igualdade induz a ação de \bar E_N na classe [βα]. Mais geralmente, para qualquer ciclo sα=0, a definição de D_N dá

\[
E_N\alpha=d_H\alpha+s(b_N\alpha),
\qquad [E_N\alpha]_s=[d_H\alpha]_s.
\tag{12}
\]

A fórmula (12) é uma identidade entre classes de s; não permite substituir d_H por uma derivada de fundo ingênua sobre qualquer representante.

Denote por M_g^K o espaço de classes representadas por ciclos de ghost g no setor K, e por C_nat(B0) o complexo das formas naturais somente de B0. Há um mapa de complexos no setor explicitado,

\[
\mu:C_{\rm nat}(B0)\otimes M_g^K
 \longrightarrow H^g(s,A_{\rm nat}),
\qquad \mu(\beta\otimes[\alpha])=[\beta\alpha],
\quad\bar E_N\mu=\mu d_H.
\tag{13}
\]

(13) expressa o cálculo obtido. Não foi provado que μ seja sobrejetivo ou injetivo, que M_g^K seja um módulo livre com base constante, nem que toda relação entre seus geradores continue a mesma após acrescentar os jatos de B0 e completar por valência. Sem essas propriedades ou uma resolução adequada, não se pode substituir os dois grupos (1) por H¹/H² de de Rham do fundo com coeficientes constantes.

## 6. Primitiva explícita do ciclo de volume do alvo na classe formal

Seja Ω a 3-forma volume orientada de S³. Defina, em qualquer carta alvo e de forma intrínseca,

\[
\tau_3=\frac1{3!}\Omega_{ABC}(\phi)
                 (s\phi^A)(s\phi^B)(s\phi^C).
\tag{14}
\]

É o pullback de Ω pelo diferencial s. Como s²φ=0 e d_targetΩ=0, sτ₃=0. Além disso, sφ=c^μ∂_μφ, então τ₃ pertence a K e E_Nτ₃=C_Nτ₃=0. Não usamos as equações Einstein ou sigma para essas identidades.

Agora use EXATAMENTE o domínio formal de Q2: φ=Exp_(φ0)(tξ), com sφ0=0. Para u∈[0,1], ponha

\[
F_u=\operatorname{Exp}_{\phi_0}(u t\xi),
\qquad V_u=sF_u,\qquad W_u=\partial_uF_u.
\]

A conexão/métrica alvo é a redonda; ξ pertence a φ0*TS³. A família é global sobre esse fibrado formal, mesmo quando φ0 percorre todo S³. Não exige uma carta alvo única, uma imagem constante de φ0 ou uma continuação da série a t numérico.

Defina a zeroforma de ghost2

\[
\boxed{K_2=\int_0^1\frac12\Omega_{ABC}(F_u)
                          W_u^A V_u^B V_u^C\,du.}
\tag{15}
\]

Cartan com os dois diferenciais s e ∂_u, que comutam, fornece

\[
\partial_u\left(\frac1{3!}\Omega_{ABC}(F_u)V_u^AV_u^BV_u^C\right)
 =s\left(\frac12\Omega_{ABC}(F_u)W_u^AV_u^BV_u^C\right).
\tag{16}
\]

Pode-se verificar (16) por Leibniz: o termo com sW_u=∂_uV_u dá as três variações de V; a identidade dΩ=0 combina as derivadas dos coeficientes Ω. Não há termo sV_u porque s²F_u=0.

Em u=1 aparece τ₃. Em u=0, F₀=φ0 e V₀=sφ0=0. Integrar (16) dá

\[
\boxed{\tau_3=sK_2.}
\tag{17}
\]

Essa primitiva é natural conjuntamente no alvo e em B0. Se a orientação alvo é invertida, τ₃ e K₂ transformam com o mesmo sinal; não declaramos τ₃ um escalar O(4)-invariante independente dessa paridade. O resultado de exatidão respeita qualquer setor de representação em que ambos sejam admitidos.

### Controle no fundo não constante

Não se pode confundir sφ0=0 com sφ avaliado em φ=φ0. O primeiro é a inércia do espectador; o segundo, no campo ativo, é c^μ∂_μφ0 e pode ser não nulo. Isso NÃO invalida (17). A primitiva K₂ pode valer zero em ξ=0 e ter variação BRST não nula nesse ponto.

Com c=tC e s=s_t nas variáveis normalizadas, a expansão inicial é

\[
K_2=\frac{t^3}{6}\Omega_{ABC}(\phi_0)
                 \xi^A(s_t\xi^B)(s_t\xi^C)+O(t^4),
\tag{18}
\]

e s_tξ em ξ=0 contém C^μ∂_μφ0. Portanto s_tK₂ produz o termo t³Ω(C·∂φ0)³/6, justamente o valor de τ₃ no fundo. Avaliar antes de aplicar s apagaria esse termo e seria incorreto.

### Finitude e Rees

Cada coeficiente de F_u, V_u e W_u tem um número finito de termos em u e em jatos; a integral de u em (15) é feita coeficiente a coeficiente. Ela divide por inteiros positivos e não resolve uma equação diferencial no espaço-tempo. Para S³, a exponencial tem coeficientes analíticos na seção zero. Não estamos especializando em1 uma série formal no parâmetro de curvatura do alvo.

A escala F_u=Exp_(φ0)(utξ), junto de c=tC e do BRST normalizado, mantém para cada termo o peso t^E correspondente ao número E de campos normalizados. W acrescenta uma ξ enquanto as duas V substituem dois fatores sφ: (15) mantém esse peso total. Multiplicar por um prefator t^(2L−2) coloca ambos os lados na organização R_L da [nota Rees074](<C:/IALD/Central de Patentes/Chatgpt/COMPLETACAO_REES_BRST_074_20260910/COMPLETACAO_POR_LACOS_E_VALENCIA.md>). Isso é uma contagem formal; não atribui a τ₃ uma amplitude física de um laço.

## 7. Qual identificação mudou

A conclusão071 sobre a topologia de valores do alvo considerava φ global em S³, sem um φ0 inerte e sem restringir (φ0,φ) a uma vizinhança formal da diagonal. A primitiva (15) usa precisamente φ0 e o Log/Exp relativo dessa vizinhança. Não existe uma escolha global única desse caminho para todos os pares de pontos de S³; não há aqui uma primitiva global do volume de S³ em sua álgebra de de Rham ordinária.

Por isso (17) não contradiz o cálculo suave global anterior, e o candidato τ₃ não pode ser transportado como um gerador não trivial para a completação Q2 apenas porque o alvo continua sendo S³. Seu s-classe nessa vizinhança formal é explicitamente zero.

Há uma mudança análoga no fator de valores de vielbein U de071. O complexo de formas SU,V=sU, FORMAL em U−U0 ao redor de um U0 invertível, tem contração radial coeficiente a coeficiente: os graus positivos de de Rham formais são exatos. As duas classes globais de H³_dR(GL⁺₄) presentes em (3) não se transportam como classes não nulas a esse fator formal. Isso é uma afirmação sobre esse fator (U,V), não sobre o complexo natural inteiro nem uma identificação do ghost Lorentz com um ghost difeomórfico. A apresentação métrica e a redução de pares Lorentz já devem ser tratadas com seu próprio alcance formal.

O [lema de normalização074](<C:/IALD/Central de Patentes/Chatgpt/NATURALIDADE_E_CURVATURA_B0_074_20260910/NORMALIZACAO_S_E_OBSTRUCAO_EULER.md>) transporta uma primitiva ordinária de s que JÁ pertença à completação escolhida para uma primitiva natural. Ele não fornece, por si, uma base de H³/H⁴ dessa completação nem um teorema de mudança de base para todos os coeficientes de B0.

## 8. Resultado utilizável e resíduo específico

[DERIVED] E_N foi calculado exatamente em K e sobre seus produtos com formas de fundo, equações(7)–(13). A_L é uma família explícita de ciclos de ghost4. O candidato de ghost3 do volume alvo é explicitamente s-exato na classe formal de Q2, inclusive sobre φ0 não constante.

[DERIVED] Os canais CE de Lorentz e o fator global GL⁺₄ foram separados. A identificação suave071 não fornece diretamente os dois módulos do critério074; uma parte topológica possível é anulada pela primitiva(15), e a parte GL global muda sob a completação de valores.

[OPEN — problema agora identificado] Para concluir os dois grupos(1), falta demonstrar que os ciclos restantes de H³/H⁴ na mesma classe natural/Rees são gerados pelo setor calculado ou por uma lista adicional explícita, e determinar suas relações com coeficientes de fundo. Em H³ isso inclui a classificação efetiva dos levantamentos de correntes; em H⁴ inclui o quociente das densidades pelas relações permitidas e os efeitos de transgressão. O cálculo de μ em(13) não permite assumir injetividade, sobrejetividade ou coeficientes constantes.

[OPEN] Nenhum resultado desta nota demonstra H¹,⁴(s|d_H)=0 na classe causal completa, uma primitiva admissível da anomalia, QME ou independência quântica de fundo. Não houve nova comparação do canônico um.py.

O manifesto mede as sete fontes locais antes e depois da escrita. Os novos cálculos de módulos aqui expostos ainda exigem revisão independente; as revisões anteriores da descida075 não são reaproveitadas como aprovação desses cálculos.
