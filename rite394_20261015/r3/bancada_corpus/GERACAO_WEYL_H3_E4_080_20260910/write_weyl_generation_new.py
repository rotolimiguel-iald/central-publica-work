from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import re

ROOT = Path('C:/IALD/Central de Patentes/Chatgpt').resolve()
OUT = ROOT / 'GERACAO_WEYL_H3_E4_080_20260910'
SOURCES = [
    ROOT / 'PRIMEIROS_TRUNCAMENTOS_BRST_077_20260910_030228_0972771/S0_KILLING_E_PRIMEIRA_TRANSICAO.md',
    ROOT / 'PRIMEIROS_TRUNCAMENTOS_BRST_077_20260910_030228_0972771/ADENDO_SINAL_KOSZUL_TATE_077.md',
    ROOT / 'LIBERDADE_DE_LEVANTAMENTO_079_20260910/CORRECOES_E4_E5_PROJECAO_SIGMA_E_SISTEMA_LOCAL.md',
    ROOT / 'LIBERDADE_DE_LEVANTAMENTO_079_20260910/ADENDO_IDEAL_FECHADO_E_COEFICIENTES_HERDADOS_079.md',
    ROOT / 'CANDIDATOS_WEYL_E_OBSTRUCAO_079_20260910_041607_7604358/WEYL_CC_M_E_FALHA_DO_COMPLETAMENTO.md',
    ROOT / 'RESIDUO_PONTRYAGIN_S0_078_20260910/CERTIFICADO_NAO_EXATIDAO_A6_E_LIMITE_DO_RAMO.md',
    ROOT / 'COMPLETACAO_REES_BRST_074_20260910/COMPLETACAO_POR_LACOS_E_VALENCIA.md',
]
NOTE = r'''# Geração de H³(s0) na valência quatro: Weyl, Calabi e coeficientes escalares

10/09/2026. Investigação080 NOVA, excluída da entrega079. [DERIVED — demonstração escrita com importação Calabi identificada; aguardando revisão independente]. Zero CAS, Lean ou execução/importação de um.py. Somente arquivos novos na pasta Chatgpt.

**Resultado delimitado.** Fixe uma referência Lorentziana espaço-forma g0, K=Λ/3>0, φ0 constante, e a ação Einstein herdada com κ não nulo. No complexo métrico mínimo, de zeroformas naturais orientadas, polinomiais de valência E=4 e ordem de jatos finita por elemento, com coeficientes herdados que sejam ESCALARES inertes da referência fixada, vale

\[
\boxed{H^3(s_0)_{E=4,\mathrm{grav,nat}}
=R_{\rm her}[P]\oplus R_{\rm her}[P^\star],\qquad
P=W[1]_{abcd}C^aC^b m^{cd},\quad
P^\star=W[1]^\star_{abcd}C^aC^b m^{cd}.}
\tag{1}
\]

m_ab=∇bar_[a C_b] contém o fator 1/2. A estrela atua na segunda dupla de Weyl, na orientação e assinatura (+---) das notas078–079. O termo “referência fixada” e o anel R_her são essenciais e estão especificados no §1.

O cálculo não se limita a decompor representações: §§2–5 justificam a passagem do complexo de jatos à torre de Weyl, incluindo fronteiras com antifields. A prova usa somente um limite superior pela torre; não pressupõe liberdade de todos os seus jatos em todas as ordens. Os dois certificados079 fornecem a independência restante.

Pelo resultado079, o primeiro diferencial induzido d1=[s1] é injetivo nesse módulo de posto dois. Assim uma correção E4 que admita completamento E5 é s0-exata e pode ser retirada por uma fronteira do BRST truncado. Isso NÃO resolve as correções que começam em E5, nem decide −[A6]∈δ(K).

## 1. Categoria efetivamente calculada e preservação do anel

A fonte077 já faz sua contagem de isotropia com Λ, φ0 e a referência fixados: [§4 de077](<C:/IALD/Central de Patentes/Chatgpt/PRIMEIROS_TRUNCAMENTOS_BRST_077_20260910_030228_0972771/S0_KILLING_E_PRIMEIRA_TRANSICAO.md>). Seguimos exatamente esse teste de espaço-forma; não substituímos o fundo físico φ=id por uma matéria constante.

Os únicos geradores dinâmicos são h, C, h*, C*, com ghosts 0,1,−1,−2. As paridades são os ghosts módulo dois. Todos os seus jatos são livres ANTES do diferencial. Não há gauge fixing, antighosts não mínimos, fontes centrais, um frame escolhido, vetores de referência extras ou coeficientes tensoriais não construídos de g0 e da orientação. g0, sua curvatura constante e os escalares herdados são inertes sob s0 e s1.

R_her designa a álgebra real dos parâmetros escalares permitidos que restam nesse teste, incluindo c ou dados do ponto φ0 quando a classe de origem os admite. Eles não são apagados. Os números K e a normalização não nula κ da equação linear são aqui valores FIXADOS, como na fonte077. Outros escalares formais inertes podem permanecer em R_her. Nesse caso o complexo é a extensão escalar

\[
\mathcal A_{R_{\rm her}}=R_{\rm her}\otimes_{\mathbb R}\mathcal A_{\mathbb R},
\qquad s_0=1\otimes s_{0,\mathbb R}.
\tag{2}
\]

Toda álgebra real é plana como módulo sobre o CORPO R. Por isso essa extensão conserva a cohomologia, sem exigir que R_her seja um domínio ou que todos os seus elementos sejam invertíveis. A prova não substitui R_her por um anel menor. Ela fornece fronteiras R_her-lineares a partir de fronteiras reais.

Limites precisos:

- Se K/κ são variáveis de um anel universal restrito, não se pode usar (2) fingindo que o diferencial deixou de depender delas. A prova abaixo vale em cada fibra fixada; não afirma, sem outro argumento, uma base global polinomial sobre esse anel.
- Se o espectador inclui jatos de escalares NÃO constantes que produzem covetores de fundo, ou outros tensores externos, o módulo de coeficientes da isotropia muda. Eles não são “escalares triviais” para a contagem. Nesse caso (1) não foi demonstrado.
- A classificação é de zeroformas, com igualdade pontual em jatos e fronteiras de s0. Não se trabalha módulo d_H, não se toma cohomologia de seções globais e não se usa a cohomologia do grupo difeomórfico inteiro como se fosse a da isotropia.

Essas precisões preservam o [adendo079 sobre o anel herdado](<C:/IALD/Central de Patentes/Chatgpt/LIBERDADE_DE_LEVANTAMENTO_079_20260910/ADENDO_IDEAL_FECHADO_E_COEFICIENTES_HERDADOS_079.md>).

## 2. O complexo LINEAR basta nesse bidegrau, sem uma importação KT excessiva

Use o [sinal KT corrigido](<C:/IALD/Central de Patentes/Chatgpt/PRIMEIROS_TRUNCAMENTOS_BRST_077_20260910_030228_0972771/ADENDO_SINAL_KOSZUL_TATE_077.md>):

\[
s_0h=R_0C=2\bar\nabla_{(a}C_{b)},\quad s_0C=0,\quad
s_0h^*=+H_0h,\quad s_0C^*=R_0^\dagger h^*.
\tag{3}
\]

H0 é a Hessiana Einstein sem gauge fixing. H0R0=0 e R0†H0=0 dão s0²=0, com prolongamento covariante e referência inerte. Seja L o espaço graduado de combinações LINEARES finitas dos jatos desses geradores. O complexo polinomial é a álgebra simétrica GRADUADA S(L); E conta o número de fatores.

Há uma exaustão de L por subcomplexos finitos. Para um jato simetrizado de ordem |I|, use os pesos auxiliares

\[
w(C_I)=|I|,\quad w(h_I)=|I|+1,\quad
w(h_I^*)=|I|+3,\quad w(C_I^*)=|I|+4.
\tag{4}
\]

R0 tem ordem um, H0 ordem dois, R0† ordem um. A conexão de g0 comuta com s0; comutadores de derivadas apenas introduzem K e ordens menores. Portanto s0 preserva w≤N. Os pesos (4) são cortes técnicos de prova, NÃO um limite de jatos imposto ao modelo. Sua união contém todo elemento local finito.

Sobre R, um complexo linear cinde em representantes de H(L) e pares a_i,b_i=s0a_i. Ao estender ρ=Σa_i∂/∂b_i com os sinais graduados, temos {s0,ρ}=N_pares. Dividir por N_pares>0 contrai todos os monômios que usam um par. Em cada monômio há somente um número finito de fatores. Isso prova

\[
H(S^E(L),s_0)\simeq S^E(H(L)).
\tag{5}
\]

Alternativamente, faz-se a mesma construção nos subcomplexos finitos de (4) e passa-se ao limite DIRETO; limites diretos de espaços vetoriais são exatos. Não é um limite inverso de cohomologias. A contração conserva E.

Cada classe LINEAR tem ghost≤1. Com quatro fatores, obter ghost3 exige precisamente os graus (1,1,1,0); qualquer fator de ghost−1 ou −2 tornaria a soma no máximo dois. Logo

\[
\boxed{H^3(S^4L,s_0)\simeq H^0(L)\otimes\Lambda^3H^1(L).}
\tag{6}
\]

Este argumento não afirma a nulidade de H^−1(L) ou H^−2(L). Ela simplesmente não é necessária para (6). Os antifields NÃO foram descartados: H⁰(L) ainda é quocientado pela imagem s0h*=+H0h, e as fronteiras polinomiais de ghost2/E4 incluem h* C³, além de h²C². Isso é exatamente a liberdade de EOM que a equação079 exige preservar.

A técnica dos pares contráteis é apresentada em [Barnich–Brandt–Henneaux, apêndice2.B](https://arxiv.org/pdf/hep-th/0002245); (4) e a contagem específica que leva a (6) são a aplicação explícita aqui, sem importar o resultado da teoria de Yang–Mills como um teorema sobre Einstein.

## 3. H¹(L): somente valores e primeiras rotações de Killing

Pela definição de (3),

\[
H^1(L)=\{\text{jatos lineares de }C\}/
\langle\bar\nabla_I(R_0C)\rangle.
\tag{7}
\]

As relações anulam a parte simétrica de ∇barC. A integrabilidade de Killing expressa ∇bar∇barC por Rbar·C; seus prolongamentos expressam todos os demais jatos por C e m. Em curvatura constante, ∇barRbar=0. Existem Killing locais para quaisquer dados (C(p),m(p)), pela realização por quádrica de077, ou pela conexão de transporte de Killing plana. Assim não há relação adicional:

\[
G:=H^1(L)\simeq V\oplus\Lambda^2V,\qquad \dim_{\mathbb R}G=10.
\tag{8}
\]

É o dual do espaço de dados de Killing; g0 permite a identificação com a representação escrita. Aqui s0 induz diferencial ZERO sobre G. O diferencial CE da álgebra de isometrias aparece em s1, não em (8).

O transporte de Killing e a completude Calabi usados a seguir estão em [Khavkine, arXiv1805.03751v2, §3 e §3.1, equações22–25 e32](https://arxiv.org/pdf/1805.03751). Seu operador seguinte é completo no sentido de fatorização por operadores diferenciais finitos. Não usamos somente a inclusão “curvatura é invariante”.

## 4. H⁰(L): Calabi, traço e quociente pelas EOM

H⁰(L) consiste em observáveis LINEARES gauge-invariantes de h, modulo combinações lineares de todos os jatos de H0h. Para explicitar qual curvatura entra, defina

\[
\mathcal R_1[h]_{abcd}=
\left.\frac d{dt}\right|_0
\bigl(R_{abcd}(g_0+th)
-K[(g_0+th)_{ac}(g_0+th)_{bd}
 -(g_0+th)_{ad}(g_0+th)_{bc}]\bigr).
\tag{9}
\]

O tensor entre parênteses se anula em g0. Sua variação gauge é zero. Com a normalização correspondente, (9) é o primeiro operador de compatibilidade Calabi, proporcional ao C1 da convenção de Khavkine.

**Importação delimitada [KNOWN].** A completude desse operador em espaço-forma afirma: se um operador linear finito O satisfaz O R0=0, existe um operador diferencial finito Q tal que O=Q R1. A formulação e a validade pseudo-Riemanniana são as da fonte citada. A discussão mais detalhada está em [Khavkine, The Calabi complex and Killing sheaf cohomology](https://arxiv.org/pdf/1409.7212). Não se importa daí uma conclusão sobre o BRST não linear.

Portanto os jatos de R1 geram o espaço linear de invariantes. A imagem dos antifields elimina seus traços. De fato, com

\[
E_{bd}=\delta\operatorname{Ric}_{bd}-3Kh_{bd},
\]

uma contração direta em (9) dá

\[
g_0^{ac}\mathcal R_{1\,abcd}=E_{bd}.
\tag{10}
\]

Para conferir: a contração da variação de R covariante é δRic+K[(trh)g0−h], enquanto a da variação do termo Kgg é K[(trh)g0+2h]. Sua diferença é (10).

A equação Einstein linearizada é E−(trE)g0/2=0. O traço reverso é invertível em quatro dimensões; H0 difere dela apenas por um isomorfismo algébrico densitizado e a normalização não nula da ação. Logo o espaço de jatos de E coincide com a imagem s0h*, incluindo a normalização da fonte KT. Modulo essa imagem, R1 é W[1].

\[
\boxed{\text{Os jatos covariantes de }W[1]\text{ geram }H^0(L).}
\tag{11}
\]

Não se precisa supor que esses jatos sejam livres. Suas Bianchi e equações de traço induzem relações; desprezá-las só daria um limite superior demasiadamente grande.

**Por que a fatorização pode ser usada naturalmente.** Em ordem finita, os espaços de jatos simetrizados, os mapas de Calabi e suas relações são módulos tensoriais da isotropia SO⁺(1,3). Uma fatorização finita inicialmente coordenada pode ser avaliada em p. Tome o espaço finito de tensores que contém seus coeficientes, complexifique e projete o mapa sobre os intertwiners pela forma compacta SU(2)×SU(2). Como o mapa original que se quer fatorar e o operador Calabi são equivariantes, a projeção preserva a igualdade de fatorização. Tomar a parte real devolve um intertwiner real. Isso não é média sobre o grupo Lorentz não compacto.

Um intertwiner entre esses fibrados tensoriais define uma expressão natural com ∇bar, g0, sua inversa e, no setor orientado, ε0; seu valor não depende do frame usado na conta. A homogeneidade do espaço-forma transporta a identidade pontual por toda a carta. Esse passo fornece naturalidade na FIBRA FIXADA do §1, com ordem de jatos ainda finita; não demonstra uma escolha global polinomial em um K variável.

## 5. Torre de Weyl: redução triangular suficiente, sem afirmar liberdade indevida

Complexifique apenas para decompor os módulos tensoriais. Localmente V_C=S⊗S', com dois espaços de spinor de dimensão dois. Essa linguagem não exige acrescentar um spinor físico ou uma estrutura spin global ao modelo; no fim usamos apenas intertwiners tensoriais da isotropia.

O Weyl se decompõe em Ψ_ABCD simétrico e seu conjugado. Em um fundo Einstein conformemente plano, a Bianchi linearizada e (10) fornecem, modulo TODOS os jatos de E,

\[
\bar\nabla^{AA'}\Psi_{ABCD}=0,\qquad
\bar\nabla^{AA'}\bar\Psi_{A'B'C'D'}=0.
\tag{12}
\]

Aqui Ψ significa a variação de Weyl, portanto o termo de variação da conexão multiplicando W(g0) é zero. Não se aplica (12) ao Weyl off-shell sem o quociente que foi justificado em (10–11).

O controle da ordem das derivadas é o seguinte.

1. Reordene uma cadeia de r derivadas usando comutadores. Cada comutador é Rbar atuando em um spinor, portanto K vezes um jato com r−2 derivadas. Não surge termo com mais derivadas.
2. Uma contração entre um índice não pontuado de derivada e um dos quatro de Ψ é um prolongamento de (12), depois de reordenar; os termos de reordenação têm ordem menor.
3. Contrações entre índices de derivadas são reduzidas pela mesma divergência diferenciada e pelo comutador de duas derivadas. No símbolo, a identidade p_AA' p_B{}^{A'}=(ε_AB/2)p² e (12) anulam essas contrações. Fora do símbolo, o defeito é K vezes ordem r−2, mais jatos de E.
4. Depois dessas reduções, todos os r+4 índices não pontuados podem ser simetrizados. A simetria dos pares de derivadas força a simetria dos r índices pontuados. Os restos antissimétricos em um espaço de spinor de dimensão dois são precisamente contrações por ε já tratadas.

Em r=0 resta Ψ_(ABCD); em r=1, a decomposição
(1/2,1/2)⊗(2,0)=(5/2,1/2)⊕(3/2,1/2)
tem o segundo termo removido por (12). Repetir os quatro passos dá uma redução FINITA de qualquer jato à parte totalmente simétrica e ordens menores. A única divisão nessa redução simbólica é por constantes não nulas dos projetores de simetrização/traço, nunca por um componente dinâmico de Weyl.

Assim o graduado associado pela ordem de derivada em (11) é um QUOCIENTE de somas dos tipos

\[
\mathcal W_r=
(2+r/2,r/2)\oplus(r/2,2+r/2),\qquad r=0,1,2,\ldots.
\tag{13}
\]

Para o argumento seguinte basta “quociente”. Não foi necessário importar uma parametrização livre de todos os jatos ou provar realizabilidade simultânea de dados arbitrários em toda a torre.

As equações87–91 de [Vasiliev, hep-th/9611024v2, §9](https://arxiv.org/pdf/hep-th/9611024) dão um controle primário dessa organização: na parte linear, a derivada do spinor com (r+4,r) índices envolve a próxima parte simétrica e um termo de curvatura com dois índices a menos; os termos quadráticos em Weyl são de valência superior. Aqui não se importa o sinal convencional de λ² da fonte para K: a redução acima usa o comutador da própria referência, e apenas o seu grau inferior importa. A parametrização Ricci-flat de [Torre, equação8](https://arxiv.org/pdf/gr-qc/9508005) é consistente com o símbolo, mas não é usada sozinha para afirmar o resultado com Λ não nulo.

## 6. Naturalidade passa pela filtração; a decomposição isolada não era suficiente

Seja V_r a imagem em H⁰(L) dos invariantes gerados por até r derivadas de Weyl. São módulos finitos da isotropia e V_r/V_(r−1) é quociente de W_r pelo §5. Para uma representação finita da álgebra semissimples so(1,3), o functor de invariantes é exato: uma cisão equivarante existe após complexificar e tomar a forma compacta, e depois se toma a parte real. Portanto

\[
\bigl((V_r/V_{r-1})\otimes\Lambda^3G\bigr)^{SO^+(1,3)}
\]

é quociente dos invariantes em W_r⊗Λ³G. A curvatura pode misturar um representante com ordens menores, mas não cria um tipo de representação novo no quociente. Se esse espaço de invariantes é zero, então toda classe natural da ordem r já vem de ordem menor. A indução pára porque o elemento tinha ordem finita.

A mesma exatidão dos invariantes permite aplicar (6) ao SUBCOMPLEXO natural: se uma expressão natural é fronteira coordenada de s0, uma primitiva finita pode ser projetada equivariantemente sem perder a identidade. Uma potência formal infinita de jatos não é introduzida. Assim

\[
H^3(\mathcal A_{\rm nat},s_0)_{E=4}
\simeq\bigl(H^0(L)\otimes\Lambda^3G\bigr)^{SO^+(1,3)}.
\tag{14}
\]

No §4 a média naturaliza um operador de fatorização; aqui ela naturaliza uma cisão/fronteira. São usos de semissimplicidade em espaços FINITOS, não uma afirmação de que toda primitiva da teoria não linear ou do complexo relativo seja natural.

## 7. Decomposição explícita e exclusão de todas as derivadas superiores

Ponha V=(1/2,1/2), A=(1,0), B=(0,1), de modo que G=V⊕A⊕B. Expandimos

\[
\Lambda^3G=\Lambda^3V\oplus
[\Lambda^2V\otimes(A\oplus B)]\oplus
[V\otimes\Lambda^2(A\oplus B)]\oplus
\Lambda^3(A\oplus B).
\]

Usando Λ²V=A⊕B, Λ³V=V, Λ²A=A, Λ²B=B e Λ³A=Λ³B=1, obtemos

\[
\begin{aligned}
\Lambda^3G={}&4(0,0)\oplus(1,0)\oplus(0,1)
\oplus(2,0)\oplus(0,2)\oplus4(1,1)\\
&\oplus4(1/2,1/2)
\oplus2(3/2,1/2)\oplus2(1/2,3/2)
\oplus(3/2,3/2).
\end{aligned}
\tag{15}
\]

Controle dimensional ESCRITO: 4+6+10+36+16+32+16=120=10·9·8/6. Nenhum CAS foi executado.

Os únicos tipos de (13) que ocorrem em (15) são (2,0) e (0,2), cada um com multiplicidade um, em r=0. Para r≥1, um dos spins de (13) é pelo menos 5/2, enquanto nenhum spin em (15) excede dois. Todos esses módulos são autoduais como representações complexas das duas sl2, de modo que a mesma verificação controla a ocorrência de um escalar no produto.

Pelo argumento FILTRADO do §6, segue

\[
\dim_{\mathbb R}H^3(\mathcal A_{\rm nat},s_0)_{E=4}\le2.
\tag{16}
\]

Não se trocou aqui o grupo difeomórfico pela isotropia: naturalidade já colocou os coeficientes em fibrados tensoriais de g0; SO⁺(1,3) é o estabilizador usado para contrair seus índices no ponto. O BRST linear e suas fronteiras foram tratados antes da contagem.

Na forma real Lorentziana, as duas contrações podem ser tomadas como P e P*. A estrela tem quadrado−1 nas duas-formas, e não exige escolher somente um setor autodual. Sem orientação espaço-temporal, o setor par sob O(1,3) contém somente a combinação correspondente sem ε. Esta última é uma restrição diferente, não aplicada em (1).

## 8. Independência e primeiro diferencial: o certificado079 paga a outra desigualdade

Ambos P e P* são s0-fechados porque s0W[1]=0 e s0C=s0m=0. A [nota079 dos candidatos Weyl](<C:/IALD/Central de Patentes/Chatgpt/CANDIDATOS_WEYL_E_OBSTRUCAO_079_20260910_041607_7604358/WEYL_CC_M_E_FALHA_DO_COMPLETAMENTO.md>) demonstra, com a solução Einstein linearizada078 e Killing genuínos, as avaliações

\[
\operatorname{ev}_{p,k}(s_1P)=-2z_0^{-1}\theta^{0123},
\qquad
\operatorname{ev}_{p,k}(s_1P^\star)=2k\theta^{0123}.
\tag{17}
\]

Essa avaliação anula s0 de QUALQUER expressão finita, inclusive com antifields e todos os seus jatos. Os dados satisfazem as equações em uma vizinhança, não apenas no ponto.

Se λ[P]+μ[P*]=0, então s1(λP+μP*) é s0-exato, pois s0s1+s1s0=0 e s1λ=s1μ=0. A avaliação teria de ser zero para k e −k no MESMO fundo e ponto. Somar e subtrair as duas equações em (17) dá λ=μ=0. O mesmo argumento prova que d1 não tem núcleo nesse módulo.

Sobre R_her o teste pode ser tensorizado com a álgebra real de coeficientes; não é preciso presumir que avaliações numéricas separem nilpotentes. O resultado é a identidade algébrica −λ/z0+μk=0 em R_her para k e −k. Como z0 e k são números reais não nulos, são unidades em qualquer álgebra real unital. Logo λ=μ=0 nesse próprio anel.

Isso prova a desigualdade oposta à de (16), e assim (1). Não reexecutamos078 nem o cálculo079; seu certificado escrito, com o sinal KT corrigido, é a entrada identificada.

## 9. Consequência operacional para correções E4/E5

O [sistema079](<C:/IALD/Central de Patentes/Chatgpt/LIBERDADE_DE_LEVANTAMENTO_079_20260910/CORRECOES_E4_E5_PROJECAO_SIGMA_E_SISTEMA_LOCAL.md>) exige

\[
s_0b_4=0,\qquad s_0b_5+s_1b_4=0.
\tag{18}
\]

A segunda equação implica d1[b4]=0. Pela injetividade acabada de provar, b4=s0v4 para uma zeroforma natural v4 de ghost2/E4 e ordem finita. Subtraia s(v4) no complexo truncado C5. O termo E4 desaparece e o novo termo E5 é

\[
b'_5=b_5-s_1v_4,\qquad s_0b'_5=0.
\tag{19}
\]

O sinal segue de s0s1=−s1s0. Assim, nessa categoria, qualquer elemento do núcleo da passagem C5→C3 pode ser representado sem termo E4 após remover seu líder exato em C3 da maneira já usada079.

O que resta em E5 inclui h²C³ e h*C⁴. A classificação de H³(s0) nessa valência, a ação de s1 nesse novo módulo e o efeito de termos de ordem superior NÃO foram calculados aqui. Consequentemente (19) não prova δ(K)=0, não prova que −[A6] esteja fora de δ(K) e não encerra todas as escolhas com o mesmo líder CE.

## 10. Filtração Rees e limites de admissibilidade

As operações lineares em geradores, as contrações de pares, os projetores tensoriais e os quocientes pelas EOM conservam a valência E. Em E4, permanece o fator t^(4+2Lloop−2) da [classe Rees074](<C:/IALD/Central de Patentes/Chatgpt/COMPLETACAO_REES_BRST_074_20260910/COMPLETACAO_POR_LACOS_E_VALENCIA.md>). Cada elemento e cada primitiva construídos usam ordem finita de jatos. As reduções por curvatura terminam pela ordem de derivada.

Não há série infinita de jatos dentro de um coeficiente, nem avaliação numérica de t, nem troca de limite inverso com cohomologia. A comparação linear nessa valência não paga a cohomologia de toda a completação ou o levantamento a valências arbitrárias. Também não foi imposta nem verificada uma cota adicional de scaling degree que pudesse restringir as primitivas: se uma classe causal específica exigir tal cota, sua preservação é uma obrigação separada. T9/T11, contatos, QME, split Ward e UV não são conclusões desta nota.

[DERIVED — escopo fixado] Geração por P,P*, injetividade do primeiro diferencial e redução de qualquer correção completável a início E5.

[OPEN] O problema de cancelamento completo −[A6]∈δ(K); a classificação das correções E5; extensão para coeficientes tensoriais de referência, um anel universal restrito em K variável ou φ0 não constante; a comparação com o fundo físico φ=id.

[REAL — documental] O manifesto mede sete fontes antes/depois e os arquivos novos. Nenhum arquivo079,078, original ou memória canônica foi alterado; nenhuma fonte antiga é apresentada como aprovação independente desta nova prova080.
'''


def pin(path):
    data = path.read_bytes()
    return {'path': path.as_posix(), 'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}


def emit(path, data):
    if path.exists():
        raise FileExistsError(path)
    temp = path.with_name(path.name + '.tmp_new')
    with temp.open('xb') as handle:
        handle.write(data)
        handle.flush()
        os.fsync(handle.fileno())
    if temp.read_bytes() != data:
        raise RuntimeError('TEMP_BYTE_MISMATCH')
    if path.exists():
        raise FileExistsError(path)
    temp.rename(path)
    if path.read_bytes() != data:
        raise RuntimeError('FINAL_BYTE_MISMATCH')


before = [pin(path) for path in SOURCES]
links = re.findall(r'\]\(<(C:/[^>]+)>\)', NOTE)
if not all(Path(path).is_file() for path in links):
    raise RuntimeError('MISSING_LOCAL_LINK')
OUT.mkdir(exist_ok=True)
note_path = OUT / 'GERACAO_NATURAL_H3_E4_E_LIMITE_DOS_COEFICIENTES.md'
emit(note_path, NOTE.encode('utf-8'))
after = [pin(path) for path in SOURCES]
if before != after:
    raise RuntimeError('SOURCE_CHANGED')
manifest = {
    'created_utc': datetime.now(timezone.utc).isoformat(),
    'author': '/root/prepare_integration_83',
    'kind': 'fixed_spaceform_linear_BRST_valence_four_generation',
    'status': 'DERIVED_WRITTEN_WITH_CALABI_INPUT_AWAITING_INDEPENDENT_REVIEW',
    'source_pins_before': before,
    'source_pins_after': after,
    'sources_unchanged': True,
    'note': pin(note_path),
    'creator': pin(Path(__file__).resolve()),
    'local_links': [{'path': path, 'exists': True} for path in links],
    'primary_sources_consulted': [
        {'url': 'https://arxiv.org/pdf/1805.03751', 'version_read': 'v2', 'scope': 'section 3.1; Calabi complete compatibility and Killing transport'},
        {'url': 'https://arxiv.org/pdf/1409.7212', 'scope': 'Calabi complex and formal homotopy distinctions'},
        {'url': 'https://arxiv.org/pdf/hep-th/0002245', 'version_read': 'v3', 'scope': 'appendix 2.B contractible pairs; no Yang-Mills theorem silently transferred'},
        {'url': 'https://arxiv.org/pdf/hep-th/9611024', 'version_read': 'v2', 'scope': 'equations 87-91; linear Weyl spinor derivative tower; no sign of cosmological constant imported'},
        {'url': 'https://arxiv.org/pdf/gr-qc/9508005', 'version_read': 'v1', 'scope': 'equation 8; Ricci-flat comparison only'},
    ],
    'results': [
        'H3 of fourth graded symmetric power uses only linear H0 and H1',
        'stable finite jet weights C:h:h*:C* = 0:1:3:4 plus derivative order',
        'Calabi and linear Einstein trace quotient give Weyl-jet generation',
        'triangular spinor-symbol reduction and finite invariant exactness give upper bound two',
        '079 evaluations give two independent classes and injective d1',
        'completable E4 corrections can be removed, leaving an E5 representative',
    ],
    'coefficient_scope': 'fixed spaceform and fixed nonzero linear-action normalizations; arbitrary inherited inert real scalar algebra by explicit flat extension',
    'not_claimed': [
        'uniform polynomial module over variable curvature parameter without further proof',
        'classification with external positive-rank spectator tensors',
        'full E5 or delta(K) classification',
        'QME or all-orders lift',
        'replacement of physical phi=id by constant matter',
        'independent approval already received',
    ],
    'executions': {'CAS': 0, 'Lean': 0, 'um_py_execution_or_import': 0},
}
manifest_path = OUT / 'MANIFESTO_GERACAO_WEYL_080.json'
emit(manifest_path, (json.dumps(manifest, ensure_ascii=False, indent=2) + '\n').encode('utf-8'))
print(json.dumps({'note': pin(note_path), 'manifest': pin(manifest_path),
                  'source_count': len(before), 'sources_unchanged': True,
                  'local_links_existing': len(links)}, ensure_ascii=False))
