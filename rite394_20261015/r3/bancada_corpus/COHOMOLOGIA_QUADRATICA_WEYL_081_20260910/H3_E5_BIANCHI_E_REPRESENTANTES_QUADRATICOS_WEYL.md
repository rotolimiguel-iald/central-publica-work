# E5: anulação do módulo linear de ghost −1 e redução a Weyl quadrático

10/09/2026. Investigação081 NOVA, excluída da entrega080. [DERIVED — demonstração escrita, aguardando revisão independente]. Nenhum original, fonte congelada, Atlas ou um.py modificado/executado/importado. Zero CAS e Lean.

**Resultado.** Na mesma referência espaço-forma FIXADA e na mesma álgebra de escalares herdados da nota080, a fatoração diferencial de Bianchi079 implica

\[
\boxed{H^{-1}(L,s_0)=0.}
\tag{1}
\]

Aqui L é o complexo LINEAR dos jatos dos geradores métricos mínimos, antes de formar os polinômios. Como consequência,

\[
\boxed{
H^3(\mathcal A_{\rm nat},s_0)_{E=5}
\simeq R_{\rm her}\otimes_{\mathbb R}
\bigl[\operatorname{Sym}^2M\otimes\Lambda^3G\bigr]^{SO^+(1,3)},
\quad
M=H^0(L,s_0),\quad G=H^1(L,s_0).
}
\tag{2}
\]

G é o módulo de dez dados de Killing, V⊕Λ²V. M é o módulo REAL de observáveis lineares de curvatura modulo todas as equações Einstein linearizadas; os jatos de Weyl geram M, como demonstrado080. M não é declarado livre em todos esses geradores.

Toda classe de (2) admite um representante natural Q, quadrático em jatos lineares de Weyl e cúbico nos representantes C,m dos ghosts restantes. O representante Q é s0-fechado OFF-SHELL, embora as relações entre suas classes usem as EOM e fronteiras com antifields. Isso remove a necessidade de antifields no REPRESENTANTE de cada classe E5; não remove antifields do complexo nem das primitivas.

Não se afirma que o módulo quadrático seja finito, não se apresenta uma base completa e não se calcula a imagem de s1 nele. A decisão de −[A6]∈δ(K) continua aberta.

## 1. Categoria e fatos080 efetivamente usados

Fixe g0 Lorentziana espaço-forma em dimensão quatro, K=Λ/3>0, φ0 constante e κ não nulo. A categoria é a métrica mínima pura obtida pela projeção sigma, com todos os coeficientes escalares herdados CONSERVADOS. O fundo físico φ=id não foi substituído por esse teste.

Seguimos o [contrato080 e sua prova](<C:/IALD/Central de Patentes/Chatgpt/GERACAO_WEYL_H3_E4_080_20260910/GERACAO_NATURAL_H3_E4_E_LIMITE_DOS_COEFICIENTES.md>), já objeto de [revisão independente delimitada](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_GERACAO_WEYL_080_20260910_044142_861011/PARECER_GERACAO_NATURAL_WEYL_E4_080.md>). A aprovação080 não é uma aprovação desta nota081.

Cada cochain é uma zeroforma natural orientada, polinomial homogênea em campos, ghosts e antifields normalizados, com uma ordem FINITA de jatos por elemento. Os argumentos dinâmicos são livres antes do diferencial. Não se trabalha módulo d_H ou sobre a cohomologia de soluções globais. Não há fontes externas de ghost positivo, frame extra ou tensores espectadores adicionais.

Após fixar K e as normalizações não nulas do operador linear, R_her é uma álgebra real de escalares inertes e o diferencial é 1⊗s0,R. A extensão escalar é plana por estar sobre o corpo real. Isso não apaga c, φ0 ou parâmetros escalares que a origem permita. Mantemos o [adendo079 do anel herdado](<C:/IALD/Central de Patentes/Chatgpt/LIBERDADE_DE_LEVANTAMENTO_079_20260910/ADENDO_IDEAL_FECHADO_E_COEFICIENTES_HERDADOS_079.md>). Um anel global restrito com K variável, ou coeficientes tensoriais não triviais da referência, não é substituído automaticamente por esse caso.

Os geradores lineares h,C,h*,C* têm ghosts 0,1,−1,−2. Com o [sinal KT corrigido](<C:/IALD/Central de Patentes/Chatgpt/PRIMEIROS_TRUNCAMENTOS_BRST_077_20260910_030228_0972771/ADENDO_SINAL_KOSZUL_TATE_077.md>),

\[
s_0h=R_0C,\quad s_0C=0,\quad
s_0h^*=+H_0h,\quad s_0C^*=R_0^\dagger h^*.
\tag{3}
\]

080 provou, para L e sua álgebra simétrica GRADUADA:

- os cortes de jatos por w(C_I)=|I|, w(h_I)=|I|+1, w(h*_I)=|I|+3, w(C*_I)=|I|+4 são finitos e estáveis;
- H(S^E L,s0)=S^E H(L,s0), por cisão linear e contração dos pares;
- a passagem aos invariantes naturais é exata em cada módulo tensorial finito;
- G=V⊕Λ²V; Calabi e a imagem dos antifields geram M por jatos de Weyl modulo EOM.

A novidade necessária em E5 é calcular H^−1(L), que não podia contribuir em E4.

## 2. Normalização que identifica a imagem linear de C*

A [fatoração079](<C:/IALD/Central de Patentes/Chatgpt/SUBSETOR_ANTIFIELD_PURO_079_20260910_041018_659161/ANTIFIELD_PURO_FATORACAO_BIANCHI_E_DELTA.md>) introduziu as mudanças invertíveis naturais

\[
p_{ab}=v_0^{-1}g_{0,ac}g_{0,bd}h^{*cd},\qquad
q_b=-\frac{C_b^*}{2v_0},\qquad v_0=\sqrt{|\det g_0|}.
\tag{4}
\]

p é ímpar de ghost−1 e q é par de ghost−2. Os fatores de referência são paralelos e s-inertes. Nessa apresentação,

\[
s_0p=Hh,\qquad s_0q=\mathcal Dp,\qquad
(\mathcal Dp)_b=\bar\nabla^a p_{ab},\qquad
\mathcal D H=0.
\tag{5}
\]

H é a identificação não degenerada do mesmo Hessiano canônico. Seu símbolo é um múltiplo não nulo do símbolo de Einstein. A identidade DH=0 é a Bianchi linearizada no fundo Einstein: os termos de variação da conexão multiplicam a equação de fundo nula. Não é uma hipótese de inversibilidade de H.

Um elemento linear de ghost−1 é uma combinação finita de jatos de p:

\[
z=P[p]=\sum_{|I|\le r} A^{I,ab}\bar\nabla_{(I)}p_{ab}.
\tag{6}
\]

Neste cálculo os coeficientes A têm ghost ZERO e não contêm nenhum gerador dinâmico. Eles podem carregar os índices de um módulo tensorial, pois precisamos do módulo linear inteiro, e não apenas de sua parte escalar natural. O caso escalar é obtido por contrações no fim.

O fechamento em (3) equivale a PH=0 como identidade sobre jatos livres de h. Uma fronteira linear é B[D p]=s0(B[q]). Portanto a obrigação exata é:

\[
PH=0\quad\Longrightarrow\quad P=B\mathcal D
\quad\text{com }B\text{ finito.}
\tag{7}
\]

079 construiu essa fatoração com coeficientes quárticos em ghosts. O algoritmo era linear nos coeficientes e não usava esse grau para fatorar: aplica-se igualmente ao grau zero de (6). Abaixo explicitamos também a aplicação pontual aos jatos.

## 3. Símbolo de Einstein e uma fatoração polinomial sem dividir por p²

Denote a covariável do símbolo por k_a, para distingui-la do antifield p_ab. Para um tensor simétrico A_ab(k), o núcleo do símbolo Einstein satisfaz, a menos de um fator global não nulo,

\[
2\mathsf E_k(A)_{ab}
=k_av_b+k_bv_a-k^2 A_{ab}-k_ak_b a
-g_{0,ab}(k^cv_c-k^2a)=0,
\tag{8}
\]

onde v_b=k^aA_ab e a=tr A. O traço de (8), em dimensão n≥3, implica k·v=k²a. No aberto k²≠0,

\[
A_{ab}
=k_a\frac{v_b-k_ba/2}{k^2}
+k_b\frac{v_a-k_aa/2}{k^2}.
\tag{9}
\]

Esta fração só permite inferir que a dupla curl polinomial

\[
\mathscr C_{abcd}
=k_ak_cA_{bd}-k_bk_cA_{ad}
-k_ak_dA_{bc}+k_bk_dA_{ac}
\tag{10}
\]

é zero no aberto denso k²≠0. Logo C é o polinômio zero. NÃO usamos (9) como uma primitiva racional.

Se A tem grau homogêneo r, ponha N=n+r,
D_b=∂A_ab/∂k_a e S=∂²A_ab/(∂k_a∂k_b). Diferenciar (10) duas vezes e usar homogeneidade dá

\[
0=N(N-1)A_{bd}-(N-1)(k_bD_d+k_dD_b)+k_bk_dS.
\tag{11}
\]

Assim

\[
\boxed{
B_b(k)=\frac1N\left(D_b-\frac{k_bS}{2(N-1)}\right),\qquad
A_{ab}=k_aB_b+k_bB_a.
}
\tag{12}
\]

Os denominadores são inteiros positivos. Em r=0, D=S=0 e A=0. Em r≥1, B é polinomial de grau r−1. A construção é tensorial e linear em A, preservando coeficientes reais herdados e sua extensão escalar.

O símbolo de H é autoadjunto na identificação (4). Portanto σ_r(P)σ_2(H)=0 pode ser identificado com o núcleo de (8). Ao voltar ao operador divergência, o símbolo do fator é 2B: a contração de k_aB_b+k_bB_a com um argumento simétrico vale duas vezes B^b k^a p_ab.

## 4. A indução de símbolos também resolve um ciclo que só foi dado no ponto

Primeiro considere uma identidade de operadores PH=0 em uma carta. Quantize 2B substituindo k por derivadas covariantes simetrizadas, com todos os coeficientes À ESQUERDA. Chame o resultado B_(r−1). Então

\[
P'=P-B_{(r-1)}\mathcal D
\tag{13}
\]

tem ordem no máximo r−1 e P'H=0, pois DH=0. Os termos de conexão e curvatura da composição não são apagados: entram nos coeficientes inferiores do próximo P'. A repetição termina no resto de ordem zero, que é zero pelo lema. Somar os fatores produz (7).

O mesmo procedimento vale para o complexo linear de coordenadas de jatos em um ponto x:

- z(x)=P_x[p] é um ciclo precisamente quando (P_xH)[h](x)=0 para TODO jato livre de h.
- Isso implica a mesma identidade polinomial no símbolo superior, avaliada em x.
- A composição (B_x D)H é zero em x porque DH é uma identidade diferencial em toda a referência.
- Consequentemente subtrair B_xD preserva o fechamento P_x'H=0 em x e reduz a ordem no argumento.

Não se precisa inferir que os coeficientes iniciais A_x já definam uma identidade global. Cada estágio usa apenas os seus valores e os jatos finitos dos operadores H,D em x. Os coeficientes ficam à esquerda, e derivadas da composição agem sobre D e o argumento; não se escolhe arbitrariamente uma extensão cujas derivadas seriam depois usadas como se fossem dados.

Ao fim,

\[
P_x[p]=B_x[\mathcal Dp]=s_0(B_x[q]).
\tag{14}
\]

Se P foi natural como expressão em uma carta, o algoritmo inteiro também é natural: usa (12), a conexão de g0, contrações e os termos inferiores preservados em (13). Para um coeficiente tensorial arbitrário no ponto, a construção é equivarante. Isso paga a nulidade do módulo linear inteiro, antes de tomar invariantes:

\[
\boxed{H^{-1}(L,s_0)=0.}
\tag{15}
\]

A ordem de B no argumento q é no máximo r−1; se r=0, o ciclo era zero. O peso auxiliar dos jatos se conserva: p com r derivadas tem peso r+3, enquanto q com r−1 derivadas tem peso r−1+4=r+3. Os termos inferiores não exigem uma cadeia infinita de operadores.

Essa conclusão é sobre IDENTIDADES DIFERENCIAIS LOCAIS. A existência de soluções Killing não a contradiz: uma seção k com R0k=0 não é um operador que produza soluções R0(fk)=0 para argumentos arbitrários f. Também não se passou para o quociente por divergências, no qual podem aparecer classes de correntes/cargas de outro tipo.

O [parecer da raiz sobre079](<C:/IALD/Central de Patentes/Chatgpt/REVISOES_RAIZ_079_20260910/PARECER_SUBSETOR_ANTIFIELD_079.md>) conferiu o símbolo e a indução originais. (6–15) explicitam a nova aplicação ao grau zero dos coeficientes e ao módulo pontual; não atribuímos a esse parecer antigo a aprovação dessa aplicação081.

## 5. Contagem de graus em Sym⁵: onde o módulo negativo poderia entrar

Como demonstrado080, a cohomologia da álgebra simétrica graduada é a álgebra simétrica graduada da cohomologia linear. Cada gerador de H(L) tem ghost≤1. Para cinco fatores, a soma de ghosts três admite exatamente:

\[
(1,1,1,0,0),\qquad (1,1,1,1,-1).
\tag{16}
\]

Um fator de ghost−2 já daria soma no máximo dois. Assim, ANTES de usar (15),

\[
H^3(S^5L,s_0)
\simeq
[\operatorname{Sym}^2M\otimes\Lambda^3G]
\oplus[H^{-1}(L,s_0)\otimes\Lambda^4G].
\tag{17}
\]

M é par, G é ímpar. Os dois fatores de M dão uma potência simétrica ordinária; os ghosts dão potências exteriores. Não há um terceiro termo esquecido com C*, pois seu grau linear é −2.

Substituir (15) elimina o segundo somando. Sobre R_her, a extensão escalar explícita do §1 conserva esse resultado. Para os cochains naturais, tome invariantes da isotropia em cada espaço finito de jatos e passe à união. A exatidão dos invariantes de módulos tensoriais finitos, justificada080 pela forma compacta da complexificação, permite comutar esse passo com a cohomologia. O resultado é (2).

Nenhuma afirmação de H^−2(L)=0 foi necessária. Não se importou uma resolução KT inteira por nome; o único módulo negativo capaz de contribuir foi eliminado pela fatoração explícita.

## 6. O representante quadrático pode ser fechado off-shell

Por080, M é gerado pelas classes dos tensores lineares ∇bar_I W[1][h], com suas relações de Bianchi e de EOM. Cada tensor escolhido é s0-fechado como expressão OFF-SHELL: W(g0)=0 implica W[1][R0C]=0 para todo ghost C livre; a conexão de fundo é inerte e comuta com s0.

G pode ser representado por C e m=∇bar_[aC_b]. Esses representantes também são s0-fechados antes de impor quaisquer equações ao ghost. Reduzir jatos superiores de C a G significa tomar seu quociente por fronteiras; não significa impor à configuração ghost a condição física de ser um Killing.

Escolha elementos reais z_i, de ordem finita, que representem as classes lineares necessárias de M. Cada classe em Sym²M⊗Λ³G é uma combinação finita de

\[
z_i z_j\,\vartheta_\alpha\vartheta_\beta\vartheta_\gamma,
\qquad
\vartheta_\alpha\in\{C^a,m_{ab}\},
\tag{18}
\]

com os índices contraídos naturalmente. Os z_i podem ser tomados como combinações lineares finitas dos jatos de Weyl, modulo as fronteiras já identificadas. Projetar o produto sobre os invariantes em um espaço tensorial finito dá um representante Q natural e s0-fechado.

Portanto, para TODO ciclo b5 de ghost3/E5, existe uma primitiva χ5 natural, ghost2/E5 e finita, tal que

\[
\boxed{b_5=Q(W[1],\bar\nabla W[1],\ldots;C,m)+s_0\chi_5,
\qquad s_0Q=0.}
\tag{19}
\]

Q é quadrático nos jatos de h através dos dois fatores de Weyl e cúbico nos ghosts. As relações na sua CLASSE usam as EOM; isso não enfraquece o fechamento exato s0Q=0 do representante.

Não se trocou M por uma álgebra livre em todos os jatos de Weyl. Precisamente, se J_W é o espaço linear de símbolos de jatos de Weyl e N_W o núcleo do mapa para M, então

\[
\operatorname{Sym}^2M
=\operatorname{Sym}^2(J_W/N_W)
\simeq
\operatorname{Sym}^2J_W/
\operatorname{span}\{n\odot z:n\in N_W,\ z\in J_W\}.
\tag{20}
\]

Uma eventual parametrização por uma torre totalmente livre requer uma prova adicional. (19) usa somente geração e o quociente real, que bastam.

## 7. Antifields mistos permanecem nas fronteiras: o avanço além do caso puro079

Os ciclos gerais de E5 podem misturar h²C³ e h*C⁴. A fonte079 só eliminava um h*C⁴ que fosse fechado SEPARADAMENTE. Aqui não se exige isso: a contração da álgebra simétrica do complexo linear, combinada com (15), trata o ciclo total.

As espécies possíveis para χ5, em ghost2/E5, são

\[
h^3C^2,\qquad h^*hC^3,\qquad C^*C^4,
\tag{21}
\]

com jatos e contrações permitidos. Os fatores são contados pela valência, não por ordem de derivada. Em particular, uma primitiva h*hC³ produz tanto termos quadráticos de EOM em h quanto termos de antifield multiplicando R0C. Esses são justamente os termos que não podem ser ignorados ao desfazer uma combinação mista.

Assim (19) não afirma que o pedaço h*C⁴ do b5 original fosse, sozinho, uma identidade de Noether. A prova de (15) é usada no nível LINEAR; a álgebra de pares contráteis gera as fronteiras mistas necessárias em (21).

Também não é legítimo proibir χ5 com antifields depois de obter (19). O resultado representa classes do complexo BV completo mínimo, não de um subcomplexo artificial que retire suas fronteiras antifield.

## 8. O que a redução permite perguntar sobre o próximo diferencial

080 mostrou que, na mesma categoria, um elemento de K=ker[H³(C5)→H³(C3)] pode ser representado sem termo E4. Escolha esse representante b5, com s0b5=0. Subtrair sχ5 em C5, usando (19), deixa Q como representante.

O defeito na próxima valência é representado por s1Q. Uma mudança Q→Q+s0χ5 altera s1Q por −s0s1χ5 e, portanto, não muda sua classe no grupo receptor de E6. Isso torna a seguinte tarefa concreta e bem tipada:

\[
\text{examinar }[s_1Q]\in H^4(s_0)_{E=6}
\quad\text{para as classes naturais de }
[\operatorname{Sym}^2M\otimes\Lambda^3G]^{SO^+(1,3)}.
\tag{22}
\]

Nenhum valor de (22) foi calculado nesta nota. Tampouco se afirmou que todos os Q tenham a mesma imagem, imagem zero ou uma combinação capaz de cancelar A6. A equação −[A6]∈δ(K) permanece sem decisão.

## 9. Finitude correta, completação e limites

A construção (12–14) termina em no máximo r etapas para um operador de ordem r. As cisões usadas na álgebra simétrica envolvem um corte finito que contém o elemento e os coeficientes necessários; sua união cobre todas as ordens finitas. Isso garante FINITUDE ELEMENTO A ELEMENTO.

O espaço M envolve jatos de Weyl de ordens sem limite uniforme. O produto Sym²M também. O fato de G ter dimensão dez não torna automaticamente finito o espaço de invariantes quadráticos: produtos de representações de ordens altas podem conter tipos pequenos. A exclusão de r≥1 que resolveu o problema LINEAR em E4 não pode ser reutilizada sem um novo cálculo nos produtos de duas torres. Não fornecemos aqui dimensão, base finita, independência de uma família infinita ou limite universal de derivadas.

Cada operação conserva valência e o fator t^(5+2Lloop−2) da [classe Rees074](<C:/IALD/Central de Patentes/Chatgpt/COMPLETACAO_REES_BRST_074_20260910/COMPLETACAO_POR_LACOS_E_VALENCIA.md>). Não se forma uma série infinita em jatos dentro de um único coeficiente. O limite técnico em ordem de jatos é direto; nenhum lim¹ ou permutação com um limite inverso de cohomologias é usado.

Se a classe de renormalização quântica impuser restrições adicionais de scaling degree, contatos ou inserções, sua preservação deve ser verificada separadamente. As notas080/081 não identificam automaticamente todos esses cochains com normalizações Q2 admissíveis.

[DERIVED — no domínio fixado] H^−1(L)=0; fórmula(2); representação(19) por quadráticos de Weyl, com as fronteiras antifield preservadas.

[OPEN] A estrutura completa do módulo quadrático, seus geradores/relações explícitos, o primeiro diferencial sobre ele, a decisão de −[A6]∈δ(K), um anel universal restrito em K variável, espectadores tensoriais e o fundo físico φ=id. Nenhuma conclusão QME, UV ou fechamento geral da prova é feita.

[REAL — documental] O manifesto mede oito fontes antes/depois e os novos arquivos. Nenhum arquivo079/080, original ou memória canônica foi alterado. As revisões anteriores foram lidas como antecedentes de alcance delimitado, sem lhes atribuir aprovação desta nova dedução081.
