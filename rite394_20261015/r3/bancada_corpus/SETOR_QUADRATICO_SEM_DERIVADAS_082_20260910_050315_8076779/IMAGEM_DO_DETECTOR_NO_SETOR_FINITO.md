# Setor quadrático sem derivadas082: imagem unidimensional do detector

10/09/2026, investigação082, separada de080/081. [DERIVED — prova escrita própria]. [REAL — 18 controles algébricos exatos e um controle documental de preservação de fontes]. Somente novos arquivos em Chatgpt; nenhum original, um.py, Lean ou fonte anterior executado/importado ou alterado.

**Resultado delimitado.** No setor das dez contrações invariantes com DOIS Weyl linearizados sem derivadas e três ghosts residuais, nenhuma combinação com coeficientes escalares herdados, independentes de k, satisfaz

\[
L_k(s_1z_5)=+4k/z_0\quad\text{para todo }k.
\tag{1}
\]

A imagem desse setor pelo detector é gerada por um único perfil,

\[
\boxed{R(k)=24k^3/z_0-96k/z_0^3.}
\tag{2}
\]

As duas cúbicas pseudoescalares de ghosts não permitem cancelar o termo k³ conservando o termo linear: suas respostas são proporcionais. Os dois candidatos quadráticos de tipo Weyl também não ajudam, pois sua resposta é zero por uma identidade algébrica de Bianchi.

Em particular, **k=2/z0 anula todo esse setor**, enquanto o lado direito de (1) vale +8/z0². O resultado também vale se forem acrescentadas contribuições diretas de antifields da espécie h*C⁴, porque o detector079 as anula. Não é uma exclusão das classes E5 que usam DERIVADAS de Weyl ou outras estruturas fora do setor especificado.

## 1. Domínio, orientação e o que são as dez contrações

Mantenha o fundo fixado g0=(ℓ/z)²diag(+---), φ0 constante, K=1/ℓ²>0 e o acoplamento κ não nulo. A orientação é dτ∧dx∧dy∧dz. Fixe z0=ℓ, p0=(0,0,0,z0), e mantenha os mesmos quatro Killing do [detector079](<C:/IALD/Central de Patentes/Chatgpt/FUNCIONAL_IMPAR_TT_079_20260910/FUNCIONAL_IMPAR_E_ELIMINACAO_DA_CONTRIBUICAO_ANTIFIELD.md>): três translações ∂τ,∂x,∂y e D/z0, com D=τ∂τ+x∂x+y∂y+z∂z. Apenas a perturbação TT h_k muda quando k varia.

O anel Rher é a extensão por escalares inertes dessa referência fixada. K, κ, z0 e os dados de referência são os mesmos para todos os k. Não se introduzem funções do k dinâmico como coeficientes das cocadeias. A conclusão é algébrica sobre essa extensão escalar; não supõe que avaliações numéricas separem elementos nilpotentes de Rher.

W=W[1][h] é o Weyl linearizado. Os quatro tipos de ghosts escalares são construídos de C e m_ab=∇bar_[a C_b], com o fator 1/2 nos colchetes. No módulo residual G=V⊕Λ²V de077/080, a [contagem081](<C:/IALD/Central de Patentes/Chatgpt/DETECTOR_IMPAR_WEYL_QUADRATICO_081_20260910_044754_4983199/CONTRAEXEMPLO_FECHADO_A_ANULACAO_DO_DETECTOR.md>) dá

\[
\operatorname{Sym}^2\mathcal W
=(8,0)\oplus(0,8)\oplus(4,0)\oplus(0,4)
\oplus2(0,0)\oplus(4,4),
\]

\[
\dim\bigl(\operatorname{Sym}^2\mathcal W\otimes\Lambda^3G\bigr)^{\mathfrak{sl}_2\oplus\mathfrak{sl}_2}=10,
\qquad\mathcal W=(4,0)\oplus(0,4).
\tag{3}
\]

Os pesos são inteiros 2j. A [decomposição080 de Λ³G](<C:/IALD/Central de Patentes/Chatgpt/CARACTERES_LORENTZ_EXATOS_080_20260910_043034_5085368/CARACTER_EXATO_LAMBDA3_WG_080.json>) contém quatro escalares e uma cópia de cada tipo (4,0),(0,4). Assim os dez emparelhamentos se separam em oito produtos escalar×cúbica e dois produtos de tipo Weyl quadrático×C²m. Não há sobreposição com (8,0),(0,8),(4,4).

Esta é uma classificação do espaço de contrações desse SETOR REPRESENTACIONAL. Não é tomada como classificação de H³(s0)E5 inteiro. A prova abaixo age sobre representantes explícitos das dez contrações; relações cohomológicas adicionais só podem reduzir esse setor.

## 2. Base real das cúbicas e convenção da estrela

Defina M^a_b=g0^{ac}m_cb, a matriz obtida do m covariante. Em Killing, M=−A para A^a_b=∇bar_bC^a. Ponha

\[
\begin{array}{ll}
\beta_e=m_{ab}C^aC^b,&
\beta_o=\frac12\varepsilon_{abcd}C^aC^b m^{cd},\\
\gamma_e=\operatorname{tr}(M^3),&
\gamma_o=\operatorname{tr}((*M)M^2).
\end{array}
\tag{4}
\]

Aqui *M significa dualizar o tensor covariante m na dupla de índices e levantar novamente o primeiro índice. Na assinatura (+---), *²M=−M. Todos os fatores M são ímpares; os traços usam ciclicidade graduada.

βe,βo ocupam as duas contrações escalares de Λ²V⊗Λ²V; γe,γo ocupam as duas cúbicas de Λ²V. São os quatro escalares de Λ³G. A estrela torna explícito qual das cúbicas Lorentz é utilizada; não se troca M por ∇C sem o sinal M=−A.

Defina os invariantes escalares quadráticos de Weyl

\[
I=W_{abcd}W^{abcd},\qquad
\operatorname{tr}(W\wedge W)=J\,\operatorname{vol}_{g_0}.
\tag{5}
\]

I é escalar e J pseudoscalar. Os oito produtos são Iβe,Iβo,Iγe,Iγo e os quatro análogos com J. Se for exigido peso de engenharia zero, multiplicam-se os produtos com β por κ e os produtos com γ por κ²: [I]=[J]=4, [β]=−2, [γ]=0 e [κ]=−2. Esses são fatores herdados, sem inversos novos.

## 3. Avaliações exatas das quatro cúbicas

Na avaliação do detector, C=ΣθA vA e C(p0)=θ. A [conta081](<C:/IALD/Central de Patentes/Chatgpt/DETECTOR_IMPAR_WEYL_QUADRATICO_081_20260910_044754_4983199/CONTRAEXEMPLO_FECHADO_A_ANULACAO_DO_DETECTOR.md>) dá

\[
m^{i3}(p_0)=-\theta^i/z_0,\quad
m^{3i}(p_0)=+\theta^i/z_0\quad(i=0,1,2),
\tag{6}
\]

demais componentes independentes zero. Portanto m é, nesse ponto, o bivector (n∧C)/z0 com n=e3. O vetor n é um dado da AVALIAÇÃO, não um coeficiente acrescentado à definição dos candidatos.

O cálculo matricial/exterior separado produz:

| Cúbica | Avaliação em p0 | Avaliação de s1 |
|---|---|---|
| βe | 0 | 0 |
| βo | −6 θ012/z0 | −18 θ0123/z0² |
| γe | 0 | 0 |
| γo | +6 θ012/z0³ | +18 θ0123/z0⁴ |

Para conferir o sinal da última linha, use as matrizes Jab de077, com Jab[a,b]=ηaa e Jab[b,a]=−ηbb. Temos

\[
A=z_0^{-1}(-\theta^0J_{03}+\theta^1J_{13}+\theta^2J_{23}),\quad M=-A,
\]

\[
*J_{03}=-J_{12},\qquad *J_{13}=-J_{02},\qquad *J_{23}=J_{01}.
\tag{7}
\]

Os três produtos não nulos em tr((*A)A²) dão −2θ012/z0³ cada um. Como M=−A, tr((*M)M²)=+6θ012/z0³, conforme a tabela. O traço par tr(M³) é zero nessa avaliação; não é uma identidade para um ghost Lorentz arbitrário.

As derivadas na terceira coluna também são controladas diretamente pela subálgebra dos quatro Killing:

\[
d_\theta\theta^i=\theta^i\theta^3/z_0\ (i=0,1,2),\qquad d_\theta\theta^3=0.
\tag{8}
\]

Assim dθ(θ012)=3θ0123/z0. Os coeficientes de fundo permanecem inertes. Em particular,

\[
\operatorname{ev}\gamma_o=-K\operatorname{ev}\beta_o,
\quad
\operatorname{ev}(s_1\gamma_o)=-K\operatorname{ev}(s_1\beta_o),
\qquad K=z_0^{-2}.
\tag{9}
\]

Isso é uma proporcionalidade nesta avaliação. Não identifica γo e −Kβo como cocadeias universais.

## 4. Os oito produtos escalares: uma só direção visível

Para os invariantes naturais I e J, a expansão completa na métrica ativa dá, por exemplo, s1J+s0J3=C·∂J. Avaliar em Killing anula s0J3. O mesmo argumento vale para I. Não se presume s1J=C·∂J como identidade off-shell antes de retirar esse termo.

Se T é uma cúbica da tabela com ev(T)=bT θ012, então (8) e a regra de Leibniz dão

\[
\operatorname{ev}(s_1(XT))
=b_T\left(\frac{3X}{z_0}-\partial_zX\right)\theta^{0123},
\qquad X=I\text{ ou }J.
\tag{10}
\]

O sinal do termo de transporte vem de θ3θ012=−θ0123. Os outros componentes Cμ∂μX se anulam por repetição de gerador quando multiplicados por θ012.

Ao longo da solução TT, na linha τ=x=y=0, escreva

\[
E=\tfrac12(k^2f-f'/z),\qquad B=\tfrac12kf'.
\]

As contrações de (5) são

\[
I=16(z/\ell)^4(E^2-B^2),\qquad
J=16(z/\ell)^4EB.
\tag{11}
\]

Como f−k=fk, I e ∂zI são pares em k. Todos os quatro produtos com I têm detector ímpar zero. βe e γe também dão zero para X=J pela tabela.

Os valores de J necessários já foram calculados081:

\[
J(z_0)=-4k/z_0,\qquad
\partial_zJ(z_0)=4k^3-28k/z_0^2,
\tag{12}
\]

obtidos diferenciando em z a ℓ fixo ANTES de impor z0=ℓ e os dados de f. Substituindo em (10),

\[
\boxed{L_k(s_1(J\beta_o))=R(k),\qquad
L_k(s_1(J\gamma_o))=-K R(k).}
\tag{13}
\]

Com peso de engenharia zero, as duas respostas são κR(k) e −κ²KR(k). Portanto qualquer combinação dos oito produtos tem resposta A R(k), com A um escalar herdado independente de k. Nenhuma escolha entre essas duas cúbicas muda a razão entre os termos k³ e k.

## 5. Os dois tipos Weyl quadráticos são invisíveis por Bianchi

Os dois emparelhamentos restantes de (3) podem ser representados por

\[
Q_S=S_{abcd}[W,W]C^aC^b m^{cd},
\qquad Q_{S^\star}=S^\star_{abcd}[W,W]C^aC^b m^{cd},
\tag{14}
\]

onde S é a projeção quadrática de tipo Weyl de W⊗W, e S* seu dual. São tensores algébricos de Weyl para QUALQUER h, sem usar EOM. A projeção existe como intertwiner tensorial: Sym²W contém cada tipo (4,0),(0,4) uma vez. Pode-se obtê-la projetando a composição do operador de Weyl sobre a parte Weyl de curvatura; remover a parte de quatro-forma e os traços é uma operação algébrica com coeficientes numéricos. Ela é não nula, por exemplo, ao quadrar um Weyl elétrico diagonal de entradas (1,−1,0): sua parte quadrática sem traço tem entradas proporcionais a (1,1,−2). O dual distingue as duas combinações reais.

A normalização de S não importa para a anulação seguinte. Para QUALQUER tensor algébrico de Weyl T, a relação (6) fornece

\[
T_{abcd}C^aC^b m^{cd}
=-\frac2{z_0}T_{abcd}C^aC^bC^c n^d
=0,
\tag{15}
\]

porque o produto dos três C seleciona T_[abc]d=0. O mesmo vale para T*. O controle exato verifica (15) em uma base real de dez Weyl, construída de matrizes elétricas e magnéticas simétricas sem traço, conferindo também seus traços e Bianchi.

Ainda é preciso verificar a variação, não apenas o valor. A identidade (15) vale para TODOS os jatos de h antes das EOM: S[h] e sua variação em qualquer direção continuam no espaço algébrico de Weyl. Logo a parte em que s1 age em h também se anula. A parte em que s1 age nos ghosts é dθ aplicado à identidade avaliada, pois os quatro Killing fecham a subálgebra (8). Ela também é zero.

Formalmente, a substituição C=ΣθA vA é compatível com a transformação s1C=dθC; a derivada em h é tomada na direção s1h=Lie_Ch. Aplicar essas duas derivações a uma identidade polinomial que é zero para todo h e θ conserva zero. Não foi presumido que a avaliação fosse mapa de complexos para s1 com diferencial ZERO.

Portanto

\[
\boxed{\operatorname{ev}_{\pm k}(s_1Q_S)
=\operatorname{ev}_{\pm k}(s_1Q_{S^\star})=0,}
\tag{16}
\]

e seus detectores são zero. Este é um caso em que o fechamento da subálgebra dos Killing importa. Não contradiz o detector079 usado para excluir P=W[1]CCm: aquele certificado empregava OUTROS quatro Killing, com valores e primeiros jatos independentes, para os quais a relação m=(n∧C)/z0 não valia.

## 6. Impossibilidade no setor inteiro de dez contrações

As oito respostas de (13) e as duas nulidades de (16) esgotam o setor definido em (3). Consequentemente

\[
\boxed{L_k(s_1z_5)=A\left(24k^3/z_0-96k/z_0^3\right)}
\tag{17}
\]

para qualquer combinação desse setor, com A∈Rher independente de k, absorvendo os fatores κ pertinentes. Essa é uma igualdade de perfis para todos os k admissíveis, não uma interpolação em alguns valores.

Se (1) valesse para todos os k, o coeficiente k³ em (17) daria A=0, pois 24/z0 é uma unidade real. Então o coeficiente linear do lado esquerdo seria zero, contradizendo 4/z0. A mesma conclusão usa um único teste fixado:

\[
k=2/z_0:\qquad L_k(s_1z_5)=0,\qquad +4k/z_0=+8/z_0^2\ne0.
\tag{18}
\]

A prova permanece válida sobre a extensão por escalares inertes, inclusive com nilpotentes: os números reais não nulos são unidades. Não usa um inverso de um elemento variável de Rher e não elimina seus parâmetros herdados.

Por079, acrescentar qualquer termo B_R da espécie h*C⁴, incluindo jatos, tem Lk(s1B_R)=0. Logo ele não muda (18), mesmo se necessário para pagar alguma outra identidade de fechamento. Somar uma fronteira s0V ao representante E5 também não muda o detector de s1, pois s1s0V=−s0s1V e Lk anula s0. Não foram descartados antifields por conveniência: a anulação de sua contribuição DIRETA é uma entrada provada separadamente pelo detector079.

## 8. Extensão que NÃO foi demonstrada

O resultado não diz que δ(𝒦)=0. Pelo contrário, o candidato081 continua tendo imagem não nula, com o perfil R(k). Aqui se mostra que esse setor não contém a direção exigida pelo resíduo sob o mesmo detector.

Não foi classificado o setor com ∇W, ∇²W ou jatos superiores. Dois jatos de mesma ordem podem produzir tipos escalares por contração, mesmo quando cada torre linear individual não se sobrepõe a Λ³G. A exclusão linear E4 de080, baseada em um maior spin crescente, não elimina automaticamente esses produtos quadráticos E5.

A identidade (15) vale para qualquer tensor de tipo Weyl colocado naquela contração, mas isso não prova que todos os candidatos com derivadas tenham essa forma. Podem aparecer invariantes escalares ou outros tipos com perfis diferentes, assim como relações cohomológicas que exigem análise própria. Nenhuma cota de ordem de derivadas foi introduzida para fingir uma exaustão geral.

[OPEN] Se −[A6] pertence a δ(𝒦) na classe completa; se candidatos com derivados e compensações satisfazem todo o sistema universal; transporte para outros fundos, coeficientes tensoriais ou anel universal variável. Também não se conclui QME, anomalia efetiva, estabilização, lim¹, carga ou UV.

## 9. Custódia do cálculo

O [recibo082](<C:/IALD/Central de Patentes/Chatgpt/SETOR_QUADRATICO_SEM_DERIVADAS_082_20260910_050315_8076779/CONTROLES_SETOR_SEM_DERIVADAS_082.json>) tem 19 itens: 18 algébricos, um documental de fontes inalteradas. Houve uma execução do script novo, somente biblioteca padrão Python e aritmética racional/Laurent/exterior. A interpretação de todos os h e a completude do setor tensorial são provas escritas acima; não são atribuídas a uma amostra numérica.

As funções aritméticas puras foram extraídas por AST de uma fonte081 SOMENTE LIDA e copiadas para um script novo082, com novo corpo de cálculo. A [proveniência da cópia](<C:/IALD/Central de Patentes/Chatgpt/SETOR_QUADRATICO_SEM_DERIVADAS_082_20260910_050315_8076779/PROVENIENCIA_COPIA_ARITMETICA_082.json>) mede origem antes/depois, funções copiadas e destino. Não se importou nem executou o script081. Todos os pins do manifesto final se referem a arquivos presentes; temporários usados para escrita não são cadastrados como fontes finais.
