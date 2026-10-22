# Detector ímpar081: uma classe quadrática fechada com imagem não nula

10/09/2026, investigação081. [DERIVED — prova escrita própria]. [REAL — 14 controles racionais/exteriores e de caracteres executados em Python puro]. Somente arquivos novos em Chatgpt; nenhum original, fonte079/080, Lean ou um.py alterado/executado/importado.

**Resultado.** Na categoria mínima natural do fundo espaço-forma fixado, com φ0 constante e escalares herdados, existe uma expressão de valência cinco, sem antifields e sem derivadas do Weyl linearizado, tal que

\[
\boxed{s_0 b_5=0,\qquad
L_k(s_1b_5)=\kappa\left(\frac{24k^3}{z_0}-\frac{96k}{z_0^3}\right).}
\tag{1}
\]

Escolhendo z0=ℓ e k=1/z0, o valor é −72κ/z0⁴, não nulo para o acoplamento κ não nulo do modelo. Portanto o detector não anula todas as classes quadráticas fechadas. Mais precisamente, este b5 define uma classe em 𝒦=ker[H³(C5)→H³(C3)] cuja imagem δ[b5] é não nula. Assim **δ(𝒦)≠0** nessa categoria fixada.

Isso não demonstra que −[A6] pertença a δ(𝒦). Um funcional detecta uma componente e não decide igualdade de classes. A nota constrói um contraexemplo à anulação universal proposta; não resolve o sistema completo de cancelamento.

## 1. Categoria e o candidato explícito

Mantenha o [sistema079](<C:/IALD/Central de Patentes/Chatgpt/LIBERDADE_DE_LEVANTAMENTO_079_20260910/CORRECOES_E4_E5_PROJECAO_SIGMA_E_SISTEMA_LOCAL.md>) e o [detector ímpar079](<C:/IALD/Central de Patentes/Chatgpt/FUNCIONAL_IMPAR_TT_079_20260910/FUNCIONAL_IMPAR_E_ELIMINACAO_DA_CONTRIBUICAO_ANTIFIELD.md>): apresentação métrica mínima, B0=(g0,φ0) inerte, Ric(g0)=3K g0, K=1/ℓ²>0 fixado, φ0 constante, orientação e assinatura (+---). O acoplamento gravitacional κ é real não nulo e herdado. Não se introduz coeficiente dependente do parâmetro k usado na solução de teste.

Os campos ativos permanecem off-shell na álgebra. Todos os jatos admitidos são finitos em cada expressão. O diferencial linear é

\[
s_0h=R_0C,\quad s_0C=0,\quad
s_0h^*=+H_0h,\quad s_0C^*=R_0^\dagger h^*.
\tag{2}
\]

W=W[1][h] denota a curvatura de Weyl linearizada como duas-forma com valores em End(TM), com seus índices internos levantados pelo fundo. Defina o pseudoscalar real J por

\[
\operatorname{tr}(W\wedge W)=J\,\operatorname{vol}_{g_0},
\tag{3}
\]

onde vol_g0 é a forma volume da orientação fixada. J é quadrático em h e usa nenhuma derivada de W além das já presentes em W[1]. Ponha

\[
m_{ab}=\bar\nabla_{[a}C_{b]},\qquad
\beta=\frac12\varepsilon_{abcd}C^aC^b m^{cd},
\qquad
\boxed{b_5=\kappa J\beta.}
\tag{4}
\]

Os colchetes incluem 1/2. O epsilon é o tensor volume de g0, e todos os índices de m são levantados com g0. J e β usam a mesma orientação. Nenhum vetor normal escolhido entra na definição (4); tal vetor aparecerá somente ao avaliar os Killing concretos.

Há dois fatores h e três ghosts, de modo que b5 tem valência5, ghost3 e paridade ímpar. Com [C]=−1, [∇]=1, [h]=0 e [κ]=−2, temos [J]=4, [β]=−2 e [b5]=0. Portanto o fator κ preserva o peso de engenharia zero sem introduzir inverso de K, de gradiente ou de campo. A candidata é polinomial nos jatos e nesse acoplamento. Isso não acrescenta uma verificação de eventuais restrições causais adicionais de um problema de renormalização particular.

Como W(g0)=0, a naturalidade dá W[1][Lie_Cg0]=Lie_CW(g0)=0 para C arbitrário. Assim s0W=0, enquanto s0C=s0m=0 e s0g0=s0κ=0. Segue a identidade UNIVERSAL de jatos

\[
\boxed{s_0b_5=0.}
\tag{5}
\]

Nenhuma equação de Einstein ou condição de Killing foi imposta para obter (5). O candidato já é fechado sem compensação por antifields. No sistema079 pode-se tomar b4=0 e a espécie R=0 para as duas condições de fechamento até C5. Se o termo métrico for escrito como Q[h,h;C³]/2, então Q/2=b5; nesta nota b5 é a expressão inteira, evitando uma ambiguidade de fator dois.

## 2. Contagem exata do setor sem derivadas

Esta contagem delimita a família finita examinada, sem a promover a uma classificação dos jatos. Use os pesos inteiros 2j da álgebra Lorentz complexificada sl2×sl2. O Weyl tem tipo

\[
\mathcal W=(4,0)\oplus(0,4).
\]

Como os fatores W são pares, as expressões quadráticas sem derivadas pertencem a Sym²W. A enumeração dos pesos em pares de índices com repetição, seguida da decomposição por maiores pesos, produz

\[
\boxed{\operatorname{Sym}^2\mathcal W
=(8,0)\oplus(0,8)\oplus(4,0)\oplus(0,4)
\oplus2(0,0)\oplus(4,4).}
\tag{6}
\]

A dimensão é 9+9+5+5+2+25=55=10·11/2. A [decomposição exata080 de Λ³G](<C:/IALD/Central de Patentes/Chatgpt/CARACTERES_LORENTZ_EXATOS_080_20260910_043034_5085368/CARACTER_EXATO_LAMBDA3_WG_080.json>), com G=V⊕Λ²V, contém quatro escalares e uma cópia de cada (4,0),(0,4). Portanto

\[
\dim\bigl(\operatorname{Sym}^2\mathcal W\otimes\Lambda^3G\bigr)^{\mathfrak{sl}_2\oplus\mathfrak{sl}_2}
=2\cdot4+1+1=10.
\tag{7}
\]

Os oito primeiros emparelhamentos vêm dos dois invariantes escalares quadráticos de Weyl multiplicados pelos quatro tipos escalares cúbicos de ghosts. Os outros dois vêm das projeções quadráticas de tipo Weyl emparelhadas com C²m. O candidato (4) pertence ao primeiro bloco: J é o pseudoscalar quadrático e β uma das contrações epsilon de C²m.

G aqui é o espaço dos valores e primeiras rotações do ghost após as relações lineares de Killing. A identidade (7) é uma contagem de emparelhamentos tensoriais nesse módulo finito. Não afirma que o espaço cohomológico completo E5 tenha dimensão dez; nele entram todos os jatos de Weyl, relações, outras espécies e antifields. A passagem080 para E4 não é automaticamente uma passagem para E5.

## 3. Os quatro Killing do detector e o valor de β

Use exatamente os quatro Killing e a carta do certificado078:

\[
g_0=(\ell/z)^2\eta,\quad
\eta=\operatorname{diag}(1,-1,-1,-1),\quad
p_0=(0,0,0,z_0),
\]

\[
v_0=\partial_\tau,\quad v_1=\partial_x,\quad v_2=\partial_y,
\quad v_3=D/z_0,
\quad D=\tau\partial_\tau+x\partial_x+y\partial_y+z\partial_z.
\tag{8}
\]

Tome C=ΣθA vA, com θ0,…,θ3 geradores ímpares independentes. Fixe z0=ℓ; então g0(p0)=η e C^a(p0)=θa. A coordenada z é ESPACIAL. Não se troca a convenção de curvatura usada para Ric(g0)=+3g0/ℓ².

Com w=ln(ℓ/z), a conexão conforme é

\[
\bar\Gamma^a{}_{b\mu}
=\delta^a_b w_\mu+\delta^a_\mu w_b-\eta_{b\mu}w^a.
\]

A derivada ordinária de C inclui θ3δa_b/z0. No ponto, esse termo cancela a primeira parcela da conexão contraída com C, deixando

\[
A^a{}_b:=\bar\nabla_bC^a
=-\frac{\delta_{b3}\theta^a+\delta^a_3\theta_b}{z_0}.
\tag{9}
\]

A é antissimétrica para η, como deve ser para um Killing. Como A_ab=−m_ab, segue para i=0,1,2

\[
m^{i3}(p_0)=-\theta^i/z_0,\qquad
m^{3i}(p_0)=+\theta^i/z_0,
\]

com as outras componentes independentes zero. Inserindo em (4), as seis permutações de 0,1,2 fornecem

\[
\boxed{\operatorname{ev}(\beta)
=-\frac6{z_0}\theta^0\theta^1\theta^2.}
\tag{10}
\]

O fator 1/2 de β cancela a duplicação das duplas i3/3i; não cancela as seis permutações dos três índices restantes. O controle exterior no recibo calcula essa soma diretamente pelas 24 permutações de epsilon.

## 4. A variação de β: o termo CE não é zero

Os Killing de (8) fecham a subálgebra de translações e dilatação. Como s1C=C·∂C, a sua avaliação é reproduzida pelo diferencial nos geradores constantes

\[
d_\theta\theta^i=\theta^i\theta^3/z_0\quad(i=0,1,2),
\qquad d_\theta\theta^3=0.
\tag{11}
\]

Isso segue também diretamente de ∂bC^a=θ3δa_b/z0. A regra vale para todos os jatos da mesma combinação de Killing; não é uma tentativa de definir s1 em qualquer avaliação arbitrária.

Por Leibniz graduado,

\[
d_\theta(\theta^0\theta^1\theta^2)
=\frac3{z_0}\theta^0\theta^1\theta^2\theta^3.
\]

O coeficiente −6/z0 de (10) é de fundo e permanece inerte sob s1. Portanto

\[
\boxed{\operatorname{ev}(s_1\beta)
=-\frac{18}{z_0^2}\theta^{0123}.}
\tag{12}
\]

Não se exige dCEβ=0 para que b5 seja ciclo de C5: a variação s1b5 tem valência seis, justamente a obstrução investigada. Exigir que β fosse previamente um cociclo CE eliminaria candidatos admitidos pelo sistema.

## 5. Pseudoscalar J ao longo da solução TT

O [certificado078](<C:/IALD/Central de Patentes/Chatgpt/RESIDUO_PONTRYAGIN_S0_078_20260910/CERTIFICADO_NAO_EXATIDAO_A6_E_LIMITE_DO_RAMO.md>) usa h=(ℓ/z)²γ e ξ=0, com

\[
\gamma_{11}=f(z)\cos(k\tau),\quad
\gamma_{22}=-\gamma_{11},\quad
\gamma_{12}=f(z)\sin(k\tau),
\]

\[
f''-2f'/z+k^2f=0,\qquad f(z_0)=0,\quad f'(z_0)=1.
\tag{13}
\]

Esse h satisfaz H0h=0 em toda uma vizinhança, incluindo todos os prolongamentos. f−k=fk por unicidade, e k→−k conserva o fundo, a orientação e os ghosts do detector.

É necessário conhecer J(z) antes de substituir os dados em z0, pois s1J contém uma derivada. Na linha τ=x=y=0, ponha

\[
E(z)=\tfrac12(k^2f-f'/z),\qquad B(z)=\tfrac12 kf'.
\tag{14}
\]

Para conferir a origem dessas funções: em η+tγ, R[1]0i0j=k²fQij/2 e R[1]3i3j=−f''Qij/2, enquanto Ric[1]ij=f'Qij/z pela EDO. O Schouten linearizado é f'Qij/(2z), e sua subtração dá W0i0j=W3i3j=E Qij. As componentes mistas são −kf' vezes o tensor transversal fora da diagonal, dividido por dois. Essas são as mesmas convenções do certificado, agora antes de impor f(z0)=0.

Assim, com índices internos abaixo e formas coordenadas eab=dx^a∧dx^b,

\[
\begin{aligned}
W_{01}&=E e^{01}+B e^{23},&
W_{02}&=-E e^{02}+B e^{13},\\
W_{13}&=B e^{02}+E e^{13},&
W_{23}&=B e^{01}-E e^{23}.
\end{aligned}
\tag{15}
\]

O Weyl matricial de tipo (1,3) é conformemente invariante. A contração do traço usa

\[
\operatorname{tr}(W\wedge W)
=-2\sum_{a<b}\eta_{aa}\eta_{bb}W_{ab}\wedge W_{ab}
=16EB\,d\tau\,dx\,dy\,dz.
\]

Como vol_g0=(ℓ/z)^4 dτ dx dy dz, segue a identidade ao longo dessa linha

\[
\boxed{J(z)=4k\left(\frac z\ell\right)^4
f'(z)\left(k^2f(z)-\frac{f'(z)}z\right).}
\tag{16}
\]

Seu valor no ponto coincide com o certificado: J(z0)=−4k/z0 quando z0=ℓ. O fator conforme é indispensável para a derivada de J, embora valha um no ponto.

Diferencie (16) mantendo ℓ e k fixos, e SÓ DEPOIS imponha f=0, f'=1, f''=2/z0, ℓ=z0. Obtém-se

\[
\boxed{J(z_0)=-4k/z_0,\qquad
\partial_zJ(z_0)=4k^3-28k/z_0^2.}
\tag{17}
\]

Derivar apenas o valor pontual −4k/z0 como se fosse a função J(z) seria incorreto: os dados de f são fixados em z0 e não se reafixam ao mover z. O recibo implementa a derivada total em z com f'=p, p'=q antes de aplicar os dados, evitando esse erro.

## 6. Variação do candidato e antissimetrização

A passagem para a derivada de Lie pode ser conferida na série completa, antes de avaliar. Defina o pseudoscalar natural da métrica ativa por

\[
\mathcal J(g)=\frac{\operatorname{tr}(W(g)\wedge W(g))}{\operatorname{vol}_g},
\qquad
\mathcal J(g_0+t h)=t^2J+t^3J_3+O(t^4).
\]

Não há termos anteriores porque W(g0)=0; o coeficiente quadrático é exatamente (3), já que a primeira variação do volume multiplicaria W0. A covariância do pseudoscalar sob difeomorfismos locais que preservam orientação dá s𝒥=t C·∂𝒥. Comparar o coeficiente de t³, com s=s0+t s1 nos campos, produz a identidade OFF-SHELL

\[
\boxed{s_1J+s_0J_3=C^\mu\partial_\mu J.}
\tag{18a}
\]

J3 é um coeficiente natural finito em jatos da série junto ao fundo não degenerado. Na avaliação por Killing, s0J3 contém R0C e seus prolongamentos e é zero. Portanto ev(s1J)=ev(C·∂J). A igualdade sem o termo s0J3 não foi afirmada universalmente antes da avaliação. Isso coincide com o argumento de equivariância de W[1] pelas isometrias de g0. J é par. Logo

\[
\operatorname{ev}(s_1b_5)
=\kappa\bigl[(C^\mu\partial_\mu J)\,\operatorname{ev}\beta
+J\,\operatorname{ev}(s_1\beta)\bigr].
\tag{18}
\]

Em p0, β só contém θ012. As parcelas μ=0,1,2 do primeiro termo têm um gerador repetido e se anulam; somente θ3∂zJ contribui. Ao colocar θ3 à direita de θ012 atravessam-se três fatores ímpares. Assim (10), (12) e (17) dão

\[
\begin{aligned}
\operatorname{ev}(s_1b_5)
&=\kappa\left[\frac6{z_0}\partial_zJ
-\frac{18}{z_0^2}J\right]_{z=z_0}\theta^{0123}\\
&=\kappa\left(\frac{24k^3}{z_0}-\frac{96k}{z_0^3}\right)\theta^{0123}.
\end{aligned}
\tag{19}
\]

Os termos são ímpares em k. O funcional079 é a metade da diferença entre as avaliações k e −k, na MESMA orientação e com os mesmos ghosts. Portanto conserva exatamente o coeficiente de (19), produzindo (1). Não há fator dois adicional no detector.

Em k=1/z0, que é permitido pela EDO e é não nulo, o resultado é −72κ/z0⁴. O candidato não é reescolhido em função de k: a expressão natural (4) é fixada antes da família de avaliação. A escolha desse valor de k serve somente para exibir uma avaliação não nula.

## 7. Consequência cohomológica e papel dos antifields

Cada avaliação do detector anula s0 de toda expressão finita, incluindo antifields, pois h satisfaz H0h=0, os ghosts são Killing e os antifields foram postos em zero depois da aplicação do diferencial. Logo Lk(s0F)=0.

Como s0b5=0, s0s1+s1s0=0 implica que s1b5 é s0-fechado. A avaliação não nula prova

\[
\boxed{[s_1b_5]\ne0\quad\text{em }H^4(s_0)_{E=6}.}
\tag{20}
\]

b5 é um ciclo do BRST truncado em C5, porque sua variação seguinte começa em E6. Sua restrição a C3 é zero, logo [b5] pertence a 𝒦. O homomorfismo de conexão C6→C5 envia essa classe precisamente a [s1b5]. Portanto

\[
\boxed{\delta(\mathcal K)\ne0.}
\tag{21}
\]

O argumento não depende de classificar todos os representantes com antifields. Se b5 ou sua imagem fossem fronteiras no sentido que as tornasse nulas nesses grupos, (20) contraditaria a avaliação. Adicionar uma fronteira s0 à expressão E5 muda s1b5 por uma fronteira s0 e não altera o detector. A contribuição direta s1(h*R) continua anulada pelo detector079, mas o presente candidato não precisa dela para ser s0-fechado.

Não se conclui que b5 compense A6. A resposta (19) contém um termo k³, enquanto Lk(A6)=−4k/z0. Um único múltiplo escalar herdado deste candidato não reproduz a resposta requerida para TODOS os k: comparar o coeficiente de k³ o obrigaria a ser zero. Tampouco a coincidência de valores para algum k isolado demonstraria igualdade de classes. Outros candidatos, seus jatos e compensações podem produzir respostas diferentes e ainda precisam ser examinados.

## 8. O que ficou pago e o que permanece aberto

[DERIVED] Foi construído um candidato natural explícito, universalmente s0-fechado no fundo conformemente plano fixado, de engenharia zero com o κ herdado. Sua imagem no detector ímpar é não nula. Assim é falsa a hipótese de que Lk anule d1 de TODAS as classes admissíveis E5 dessa categoria. O contraexemplo já ocorre no setor sem derivadas de Weyl; não depende de uma extrapolação para jatos infinitos.

[REAL] O [recibo081](<C:/IALD/Central de Patentes/Chatgpt/DETECTOR_IMPAR_WEYL_QUADRATICO_081_20260910_044754_4983199/CONTROLES_DETECTOR_WEYL_QUADRATICO_081.json>) registra 14 controles em uma execução do script Python puro: contração epsilon de β, diferencial dos ghosts, contração de Weyl, derivada total, resposta ímpar, avaliação não nula e contagem de caracteres. As cinco fontes foram medidas antes/depois e permaneceram inalteradas. Os controles não repetem toda a prova Einstein078 ou a geração080, nem importam scripts anteriores.

[OPEN] Continua sem decisão se −[A6] pertence a δ(𝒦), se uma combinação mais ampla satisfaz o sistema universal em jatos e as condições com antifields, e como o resultado se transporta para outros fundos, anéis universais variáveis ou a categoria causal completa. Não se determina H³(s0)E5 inteiro. Não há conclusão sobre lim¹, estabilização, anomalia efetiva, QME, carga interagente ou UV; nenhum gate é alterado.
