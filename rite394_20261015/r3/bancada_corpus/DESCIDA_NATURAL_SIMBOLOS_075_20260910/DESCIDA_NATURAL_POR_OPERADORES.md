# Descida natural por operadores diferenciais e símbolos

10/09/2026, arco075. [DERIVED — prova escrita]. Arquivos novos; fontes congeladas preservadas; zero CAS/Lean; nenhum um.py executado ou importado. Este resultado trata a derivada horizontal d_H, sem pressupor a exatidão de H(s).

## 1. Teorema e categoria

Seja M de dimensão n, em particular n=4. Divida os geradores em Y, de ghost zero, e Z, de ghost não zero. Z e todos os seus jatos são geradores LIVRES de fibrados vetoriais graduados. Permita coeficientes naturais suaves nos valores de Y e do fundo B0, com dependência finita/polinomial nos jatos diferenciados e em Z. As mudanças admitidas nos fibrados de Z são lineares, com coeficientes de ghost zero. Os geradores e seus jatos obedecem à supercomutatividade usual, mas a nenhuma equação diferencial imposta.

Escolha conexões naturais nos fibrados de Z e em TM, com coeficientes independentes de Z. No setor métrico Einstein–sigma, a conexão Levi-Civita de g0 serve para os tensores de espaço-tempo e suas densidades. Para os antifields sigma, usa-se a conexão alvo pullback apropriada. O campo que define esse pullback tem ghost zero. Na apresentação perturbativa Q2, todos esses fibrados podem ser apresentados sobre B0, e as conexões podem ser escolhidas independentes das flutuações; esta precisão será usada na seção8.

Não se usa o ghost Lorentz convencional com transformação afim sem especificar seu fibrado. A [precisão de frames074](<C:/IALD/Central de Patentes/Chatgpt/HOMOTOPIA_NORMAL_COVARIANTE_074_20260910/PRECISAO_FRAME_LOCAL_074.md>) permanece válida. Aqui basta a apresentação MÉTRICA efetiva de Q2.

**Teorema.** Seja ω uma q-forma horizontal natural, de grau Euler N>0 em Z e seus jatos. Se

\[
d_H\omega=0
\quad\text{como identidade universal off-shell},\qquad 0<q<n,
\]

existe uma (q−1)-forma natural η, de ordem finita, do mesmo grau N e mesmo ghost, tal que

\[
\boxed{\omega=d_H\eta.}
\tag{1}
\]

Ela é construída por operações diferenciais finitas e divisores inteiros positivos. Para q=0, a mesma hipótese e N>0 implicam ω=0; não se introduz uma forma de grau −1. Toda forma de ghost positivo tem somente componentes N>0, portanto o resultado vale somando suas componentes homogêneas finitas ou formalmente admissíveis.

O enunciado é sobre o núcleo de d_H. Não é uma afirmação de aciclicidade de s, não resolve H¹,⁴(s|d_H), e não diz que uma top-forma arbitrária seja divergência.

## 2. Linearização com sinais controlados

Introduza variações v de mesma paridade, ghost e tipo fibrado que Z, mas como NOVOS geradores independentes, incluindo todos os seus jatos. Com parâmetro ε par de ghost zero, defina

\[
P[v]=\ell^Z_\omega(v)
 :=\left.\frac{d}{d\varepsilon}\right|_{0}
        \omega(Y,Z+\varepsilon v).
\tag{2}
\]

A variação é par. Seu prolongamento comuta com as derivadas totais, pois manda cada jato Z_I em v_I. Portanto

\[
d_HP[v]=\ell^Z_{d_H\omega}(v)=0.
\tag{3}
\]

P é um operador diferencial linear finito em v, com coeficientes que podem depender dos jatos de Y,B0 e Z. Essa dependência não é congelada ao aplicar d_H: todas as derivadas dos coeficientes serão conservadas.

Os jatos de v são livres e independentes dos de Z. Assim, igualdade de operadores significa igualdade de cada coeficiente em cada jato de v, também quando v é ímpar. Não se substitui v=Z antes de extrair os símbolos; isso impediria conclusões falsas obtidas por anulações de Grassmann.

Fixamos dx à esquerda nas formas. Contragredientes, contrações e derivadas em variáveis ímpares são prolongados de forma graduada. A variação par (2) evita um sinal adicional na identidade de Euler que será usada ao final.

## 3. Contração canônica do símbolo

Considere P de ordem r em v. Seu símbolo principal σ_r(P) é uma q-forma com coeficientes polinomiais homogêneos de grau r numa variável cotangente par p. A parte de ordem r+1 de d_HP é

\[
\delta\sigma_r(P),\qquad
\delta=p_i\,dx^i\wedge.
\tag{4}
\]

Derivar os coeficientes de P não aumenta a ordem em v; por isso esses termos não participam da ordem r+1. A liberdade dos jatos de v e (3) implicam δσ_r(P)=0.

Defina

\[
h=\sum_i\frac{\partial}{\partial p_i}\iota_i,
\qquad \iota_i=\iota_{\partial/\partial x^i}.
\]

Este é um operador canônico: a transformação de ∂/∂p compensa a transformação de ι. Portanto h é GL-equivariante e não usa produto interno, volume, frame ortonormal ou origem de coordenadas. Ele reduz em um o grau em p e o grau de forma.

Usando \(\iota_i(dx^j\wedge\alpha)=\delta_i^j\alpha-dx^j\wedge\iota_i\alpha\), obtemos, em grau (r,q),

\[
\boxed{\delta h+h\delta=(r+n-q)\,\mathrm{Id}.}
\tag{5}
\]

Prova explícita: ao derivar p_j em hδ, aparece Σ_iι_i dx^i∧=n−q; ao derivar o polinômio restante, aparece o operador Euler p_i∂/∂p_i=r. Os termos cruzados se cancelam com δh. A mesma identidade vale com coeficientes Grassmann: dx à esquerda e o prolongamento graduado já incluem os sinais de travessia desses coeficientes.

Como q<n, r+n−q é estritamente positivo. Logo, para σ_r δ-fechado,

\[
\sigma_r=\delta\tau_{r-1},\qquad
\tau_{r-1}=\frac{h\sigma_r}{r+n-q}.
\tag{6}
\]

O polinômio τ tem grau r−1 e é uma (q−1)-forma. A identidade (5) é demonstrada aqui na convenção cohomológica necessária. Como referência primária de contexto, [Arnold, seção3.2, teorema3.1 e corolário3.2](https://www-users.cse.umn.edu/~arnold/papers/fe-families.pdf) apresenta a contração dos complexos polinomiais de de Rham/Koszul. Não se troca sua convenção de graus pela nossa sem o cálculo (5).

## 4. Quantização covariante e indução finita

Quantize τ_{r−1} usando as conexões já escolhidas e derivadas covariantes SIMETRIZADAS de v. Denote o operador resultante por Q_{r−1}. Com a normalização usual do símbolo, isto significa substituir p_{i1}…p_{ik} por \(\nabla_{(i1}\cdots\nabla_{ik)}\), mantendo os coeficientes à esquerda. Seu símbolo principal é exatamente τ_{r−1}.

Essa receita é natural: os símbolos são tensores, as conexões são naturais nos dados transportados, e a simetrização é canônica. As conexões dos índices tensoriais e das densidades estão incluídas. Se o fibrado alvo é não trivial, a conexão pullback fornece a mesma operação nas sobreposições; não se precisa de uma carta global de S³.

O símbolo principal de d_HQ_{r−1} é δτ_{r−1}=σ_r(P). Logo

\[
P^{(r-1)}:=P-d_HQ_{r-1}
\quad\text{tem ordem no máximo }r-1.
\tag{7}
\]

Também d_HP^{(r−1)}=0, pois d_H²=0. Todos os termos de derivada dos coeficientes e todos os comutadores de derivadas covariantes ficam no resíduo. Curvatura não foi zerada: ela altera as ordens inferiores, que o algoritmo processa nos passos seguintes.

Repita (6)–(7) em ordens r−1,r−2,… . Após um número finito de passos, resta um operador de ordem zero P^(0). Seu símbolo satisfaz δσ_0=0. Mas hσ_0=0 e (5) dá

\[
(n-q)\sigma_0=0.
\tag{8}
\]

Para q<n isso implica P^(0)=0. Somando as primitivas parciais, resulta

\[
\boxed{P=d_HQ,\qquad \operatorname{ord}_v Q\le r-1.}
\tag{9}
\]

Se r=0 desde o início, P=0. Se q=0, hσ_r=0 em TODAS as ordens, e (5) força cada símbolo a zero: P=0 sem uma primitiva de grau negativo. Se q=n e r=0, o denominador de (8) é zero; esse é precisamente o caso em que o método não elimina o termo de Euler de uma densidade arbitrária.

A construção pode ser feita com um limite superior fixado R para a ordem, inserindo símbolos zero nas ordens ausentes. Cada passo é linear em P; aumentar R só acrescenta passos zero. Assim Q é uma escolha linear natural no espaço dos operadores fechados de ordem finita. Não afirmamos aqui a identidade de homotopia dH+Hd=Id sobre TODAS as formas; construímos a escolha de primitiva sobre o núcleo de d.

## 5. Volta à forma por Euler e finitude

Como ω é homogênea de grau N em Z, (2) tem grau N−1 em seus coeficientes Z e é linear em v. Conexões independentes de Z, derivadas totais, símbolos, h, quantização e subtração em (7) conservam esse grau. Portanto Q tem a mesma graduação.

A avaliação ev(v_I)=Z_I comuta com as derivadas totais. Em covariantes, v e Z usam a MESMA conexão, logo a afirmação permanece verdadeira. Euler para a variação par dá

\[
P[Z]=N\omega,\qquad
P[Z]=d_H(Q[Z]).
\]

Assim podemos escolher

\[
\boxed{\eta=\frac1NQ[Z].}
\tag{10}
\]

A primitiva tem o mesmo ghost e grau N de ω. Para q=0, P=0 implica Nω=0 e portanto ω=0. Para uma soma finita de componentes N>0, aplique (10) a cada uma. d_H conserva N, então cada componente de uma forma fechada é fechada separadamente.

Cada símbolo, divisão e contração é finito. Há no máximo r passos que introduzem Q, e cada passo aplica apenas operações diferenciais finitas aos coeficientes já presentes. A ordem dos jatos dos coeficientes pode crescer; não a confundimos com a ordem em v, que decresce estritamente. Isso prova finitude por entrada. Não prova uma cota universal de ordem para todas as valências ou todas as formas.

Não se contrai g0 a zero, não se integra sobre uma família de fundos, não se escolhe uma partição da unidade e não se impõe trivialidade topológica do alvo. Toda possível classe independente de Z pertence ao grau Euler zero e foi excluída pela hipótese. É por isso que a topologia não produz uma classe adicional nesta parte positiva do complexo.

## 6. Naturalidade, regularidade e escala

O procedimento depende somente da escolha declarada de conexões naturais e da forma ω. Ele é natural conjuntamente sob transformações dos campos e fundos. Para a apresentação métrica de Q2, as conexões induzidas por g0 e pelo alvo são globais nos fibrados relevantes. Portanto, se ω é global nessa categoria, as primitivas produzidas nas cartas coincidem por naturalidade da receita; não há colagem por primitivas escolhidas separadamente.

A construção é local em jatos. Ela continua diferenciando B0 e Y dentro dos coeficientes; sB0=0 não é usado para eliminar d_HB0. Também não é exigido sω=0 para aplicar o teorema: apenas d_Hω=0 entra.

Coeficientes suaves permanecem suaves. Quando a entrada e as conexões pertencem à classe analítica de famílias permitida, derivação, contração, simetrização e divisões pelos inteiros N e r+n−q conservam a analiticidade. Não se obtém analiticidade a partir de uma entrada meramente C∞. Na apresentação formal sigma via Exp do alvo S³, cada coeficiente é tratado na classe real disponível, sem avaliar a série em uma flutuação finita.

Para o controle de engenharia, dê a ∂ e p peso +1, a dx peso −1 e a cada v seu peso físico declarado. h remove simultaneamente um p e um dx e tem peso total zero; δ=p·dx também tem peso zero. A quantização troca p por uma derivada do mesmo peso. Derivar coeficientes no resíduo é acompanhado pelo dx da derivada horizontal. Assim a primitiva conserva o peso TOTAL da forma, se as conexões usadas são homogêneas com essas atribuições. Em componentes, a passagem de q a q−1 reduz em um a dimensão exigida do coeficiente, como deve ocorrer para uma primitiva.

Os divisores numéricos não introduzem escala, e o algoritmo finito não cria integrações que possam aumentar por si a ordem de logaritmos de escala. Essa afirmação é sobre a operação na classe homogênea ou quase homogênea especificada. Ela não substitui os limites de escala de cada mapa multilinear renormalizado.

[OPEN] Este resultado não constrói a hierarquia completa de contatos, T9/T11, a independência funcional dos campos dos mapas de renormalização ou uma normalização simultânea de todos os produtos temporais. Tais propriedades envolvem a família causal inteira, enquanto (10) atua numa forma local fechada dada. O [contrato072](<C:/IALD/Central de Patentes/Chatgpt/COMPARACAO_CAUSAL_FUNDOS_072_20260910/CONTRATO_ADMISSIBILIDADE_Q2.md>) continua distinguindo essas obrigações.

## 7. Limites: identidade off-shell, fontes centrais e top-formas

A livre escolha de v e dos seus jatos é a hipótese decisiva. Se d_Hω=0 vale apenas após impor equações aos ghosts ou antifields, a linearização pode valer somente para v que resolve as equações linearizadas. Então δσ(P)=0 como identidade no símbolo livre não segue. Não aplicamos o lema a esse quociente on-shell por analogia.

Uma fonte CENTRAL de ghost positivo não pertence automaticamente a Z. Por exemplo, se uma variável ímpar constante ζ satisfaz d_Hζ=0 por definição e tem ghost1, ela já produz uma classe não nula em forma0. Colocá-la formalmente em Z, mas negar-lhe jatos livres, violaria a hipótese. Assim, ghost positivo garante N>0 somente quando não há coeficientes externos de ghost positivo fora do conjunto de geradores livres contado por N.

O teorema vale com campos Y/B0 arbitrários, inclusive especializações de seus valores, desde que a identidade que se quer usar conserve a liberdade diferencial de Z e sua linearização. Ele não converte uma igualdade numérica num fundo em identidade universal de todos os jatos.

Em q=n uma densidade arbitrária pode ter operador de Euler não nulo e não ser divergência. Por isso (1) não pode começar diretamente em uma anomalia aⁱ₄ arbitrária. Para iniciar uma descida BRST, é necessária a relação de consistência s aⁱ₄+d_H a²₃=0 com primeiro descendente natural, ou um argumento adicional que naturalize esse primeiro descendente a partir da nulidade dos operadores de Euler do termo s aⁱ₄. A próxima seção formula separadamente a parte que o teorema efetivamente paga.

## 8. Completação perturbativa: controle que esta homotopia paga

Use a [classe Rees074](<C:/IALD/Central de Patentes/Chatgpt/COMPLETACAO_REES_BRST_074_20260910/COMPLETACAO_POR_LACOS_E_VALENCIA.md>) motivada pela [construção Q2_069](<C:/IALD/Central de Patentes/Chatgpt/CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/PRODUTOS_TEMPORAIS_E_ANOMALIA_LOCAL.md>). Denote por X TODOS os campos normalizados, inclusive Y de ghost zero, ghosts e antifields. E conta cada campo e cada jato como uma perna, enquanto B0 tem grau zero. Seja

\[
\mathcal R_L^q=\prod_{E\ge0}t^{E+2L-2}\mathcal P_E^q.
\tag{11}
\]

Escolha as conexões nos fibrados perturbativos fixados por B0: h é tensor de espaço-tempo, ξ é seção de φ0*TS³, os antifields pertencem aos duais densitizados correspondentes, e os ghosts são seções dos demais fibrados naturais fixos. A transformação cotangente da expansão sigma é a da nota Rees074. Nesta apresentação, as conexões têm coeficientes de B0 e NÃO acrescentam pernas.

Considere uma componente ω_E, de grau total E, e decomponha-a pelo grau N>0 em Z. Linearizar em Z retira uma perna Z e introduz uma variação v, contada como uma perna do mesmo tipo. Os coeficientes do operador têm grau E−1 em X. As derivadas totais conservam esse grau: derivam coeficientes de B0 ou trocam um jato de X por outro. Extração de símbolos, h e quantização com conexão B0 conservam o grau. Avaliar v=Z devolve uma perna. Logo a escolha de primitiva satisfaz

\[
H_q:\ker d_H\cap\mathcal P_E^{q,N}
\longrightarrow\mathcal P_E^{q-1,N},
\qquad d_HH_q\omega_E=\omega_E.
\tag{12}
\]

Não há fator t⁻¹ nessa operação: diferentemente da translação b_N, a retirada de Z na linearização é compensada por sua reposição na avaliação. Portanto

\[
H_q\bigl(t^{E+2L-2}\omega_E\bigr)
 =t^{E+2L-2}H_q\omega_E,
\tag{13}
\]

e H_q conserva R_L, L, E, N e o expoente de t. Cada coeficiente de saída depende apenas do MESMO coeficiente E de entrada, que tem ordem de jatos finita; por isso a operação é contínua na topologia de produto por valência. Para L≥1, não surgem potências negativas de t. Uma ordem de jatos crescente com E é permitida em (11) e não exige somar infinitas derivadas num coeficiente fixo.

Essa conclusão usa a apresentação perturbativa e a conexão de B0 explicitadas. Na prova em campos completos, uma conexão pullback pelo φ completo continua independente de Z e preserva N, mas sua reexpansão pode misturar graus de flutuação. Não se identifica automaticamente essa versão com (12)–(13). Para pagar o controle perturbativo, aplique a construção diretamente nos fibrados normalizados de B0 que definem (11).

Graus adicionais de fontes externas são conservados se as conexões e as operações não os alteram e se essas fontes não fornecem ghost positivo central fora de Z. A fórmula não reclassifica os tadpoles Laurent da Ward072 como elementos de (11) sem suas contagens próprias. Também não demonstra continuidade de uma futura homotopia de s: só da escolha H_q de (12).

## 9. Descida natural que segue, sem resolver H(s)

Suponha já estabelecida uma relação natural

\[
s a_4^1+d_H a_3^2=0.
\tag{14}
\]

Como s²=0 e {s,d_H}=0, d_H(s a_3²)=0. Seu grau de forma é3<4 e seu ghost é3>0. Aplicando o teorema, escolhemos a_2³=−H₃(s a_3²), obtendo s a_3²+d_H a_2³=0. Repetindo em graus2 e1, obtemos

\[
s a_q^{5-q}+d_H a_{q-1}^{6-q}=0\quad(q=3,2,1).
\tag{15}
\]

No final, d_H(s a_0⁵)=0 e s a_0⁵ tem ghost6; o caso q=0 do teorema dá s a_0⁵=0. Assim a soma dos descendentes é um cociclo NATURAL do diferencial total s+d_H. Quando a entrada e s preservam (11), a escolha horizontal descrita conserva essa mesma completação a cada passo.

O resultado paga a passagem horizontal da descida, antes de qualquer tentativa de resolver a cohomologia do cociclo total. Para obter um contratermo que remova a anomalia, ainda seria necessário demonstrar a exatidão apropriada para s+d_H ou H¹,⁴(s|d_H) na classe causal admissível. A construção de descendentes não é essa demonstração.

[KNOWN — comparação delimitada] O lema algébrico de Poincaré e seu papel nas descidas aparecem em [BBH2000, teorema4.2 e seção9](https://arxiv.org/pdf/hep-th/0002245v3). Aqui não se importa automaticamente a naturalidade de uma primitiva coordenada: (4)–(10) a constroem por símbolos e conexões, conservando a categoria positiva em Z.

## 10. Resultado desta contribuição

[DERIVED] Formas naturais universalmente d_H-fechadas de grau 0<q<4, com grau Euler positivo nos ghosts/antifields livres, possuem primitivas naturais finitas. O caso q=0 é nulo. A prova conserva Grassmann, jatos dos coeficientes, curvatura nas ordens inferiores e naturalidade dos fibrados declarados.

[DERIVED] Na apresentação perturbativa com conexões fixadas por B0, a escolha de primitiva conserva E,N,L e o peso t^(E+2L−2), com continuidade coeficiente a coeficiente. Regularidade e peso de engenharia são conservados nas subclasses e convenções explicitadas.

[OPEN] O passo inicial de top-forma requer (14) ou sua naturalização separada. A cohomologia BRST natural, a primitiva da anomalia e sua implementação na hierarquia causal não foram deduzidas apenas deste lema. Não se alegam QME, independência quântica de fundo ou fechamento UV.

As duas revisões independentes recebidas nesta tarefa conferiram o símbolo, os sinais, a redução por ordem e os casos q=0/r=0, com as hipóteses de liberdade dos jatos visíveis. O manifesto mede cinco fontes locais antes/depois; essas revisões não são um certificado Lean nem aprovação de QME.
