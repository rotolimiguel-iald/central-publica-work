# Parecer independente: identificação de d1 com CE no setor quadrático082

10/09/2026. Autoria desta revisão: agente finish_gibbs_realization. [DERIVED — revisão matemática escrita independente]. [REAL — custódia documental no recibo ao lado]. Nenhum cálculo matemático automatizado, CAS, Lean ou execução/importação de um.py nesta revisão.

**Conclusão delimitada.** Li integralmente a [nota CE082](<C:/IALD/Central de Patentes/Chatgpt/COMPLEXO_CE_QUADRATICO_082_20260910/IDENTIFICACAO_D1_CE_KILLING_E_JATOS_WEYL.md>) e seu manifesto. Não identifiquei erro matemático material nas identidades nem no isomorfismo de complexos declarado, dentro da referência espaço-forma fixada, setor métrico mínimo puro, escalares herdados inertes e jatos de ordem finita por elemento. A identificação inclui a ação sobre os coeficientes de Weyl, suas relações on-shell e os índices de derivadas. Não é um cálculo da cohomologia CE nem uma demonstração de cancelamento de A6.

Este parecer registra minhas verificações abaixo. Os resultados de redução080/081 são entradas delimitadas; não reexecutei nem reconstruí integralmente suas demonstrações de Calabi, fatoração de Bianchi ou eliminação de antifields. Não atribuo minha conclusão a aprovação do operador ou de outro agente.

## 1. A diagonal e o papel do quociente linear

Na notação da fonte, chamo \(\mathcal M=H^0(L,s_0)\) ao módulo de classes lineares e \(M_{\rm gh}\) à matriz antissimétrica de ghost. Isso evita trocar ambos com a matriz de sinal oposto utilizada na nota finita082. O complexo linear mínimo tem graus \(1,0,-1,-2\). Como cada fator tem valência um, o déficit de um monômio é
\[
E-\mathrm{gh}=\sum_i(1-\mathrm{gh}_i).
\]
Déficit dois admite exatamente dois fatores de grau zero ou um de grau menos um, acompanhados pelos fatores de grau um necessários. Um fator de grau menos dois já tem déficit três e não cabe.

Consumindo \(H^{-1}(L,s_0)=0\) e a comparação entre a álgebra simétrica graduada e a cohomologia linear estabelecidas em081, resulta
\[
H^q(s_0)_{E=q+2}
=R_{\rm her}\otimes
[\operatorname{Sym}^2\mathcal M\otimes\Lambda^qG]^{\mathfrak h}.
\]
Essa contagem vale também em q=0; para q maior que dez o lado reduzido é zero. Não remove fronteiras antifield do alvo por decreto: o próprio quociente \(\mathcal M\) e a comparação081 já as incorporam.

A tomada de invariantes usada aqui é a da isotropia em cada espaço tensorial finito e depois na união. Não foi aplicada a um módulo arbitrário de todas as isometrias. Tampouco se concluiu que uma cohomologia relativa horizontal ou uma completação inversa tenha essa mesma descrição.

## 2. Ghost transportado: sinais e fronteiras s0

Refiz as igualdades dos §§2–3 da fonte com as convenções explicitadas:
\[
B^a{}_b=\bar\nabla_bC^a,\qquad
M_{\rm gh}=\tfrac12(B-g_0^{-1}B^Tg_0),\qquad
H=g_0^{-1}h.
\]
Como \(s_0h=\mathcal L_Cg_0\), a parte simétrica é \(B-M_{\rm gh}=s_0(H/2)\). Com \(m_{ab}=\bar\nabla_{[a}C_{b]}\), baixar o primeiro índice dá \((M_{\rm gh})_{ab}=-m_{ab}\). Trocar esse sinal sem trocar o restante do dicionário alteraria o cálculo.

O transporte usa o mesmo \(S=(g_0^{-1}g)^{1/2}\) e \(k=SvS^{-1}-(sS)S^{-1}\) da fonte076. Torsão zero e paridade dão \(sc=-vc\): de fato \(v^\mu{}_\nu c^\nu=(\nabla_\nu c^\mu)c^\nu=-c^\nu\nabla_\nu c^\mu\). Portanto
\[
s(Sc)=-kSc.
\]
Expandi essa identidade e \(sk+k^2=\Omega\) até a ordem quadrática. Com \(p_2=Hp/2\) e o coeficiente \(k_2\) do mesmo transporte, obtive exatamente
\[
s_1p+s_0p_2=-M_{\rm gh}p,\qquad
s_1M_{\rm gh}+s_0k_2=-M_{\rm gh}^2+Kpp^\flat.
\]
As igualdades são entre jatos livres antes de impor Killing. As fronteiras explícitas justificam a passagem a \(H(s_0)\); a mera substituição dos ghosts por Killing não bastaria para essa afirmação.

## 3. As duas antirrepresentações e o sinal CE

Para \(X(A,a)=\left(\begin{smallmatrix}A&a\\-Ka^\flat&0\end{smallmatrix}\right)\), o campo fundamental \(v_X(q)=Xq\) satisfaz
\[
[v_X,v_Y]=(YX-XY)q=-v_{[X,Y]}.
\]
Aqui se usa o colchete usual dos campos e o comutador usual das matrizes. O primeiro sinal é, assim, direto.

O segundo sinal provém da ação evolutiva sobre as coordenadas dos campos, mantendo os coeficientes dos vetores e da referência inertes. Se \(\delta_vh=\mathcal L_vh\), então
\[
\delta_v(\delta_wh)=\mathcal L_w(\mathcal L_vh),\qquad
[\delta_v,\delta_w]=-\delta_{[v,w]}.
\]
É a ordem inversa da composição dos operadores lineares no argumento h. Logo \(\rho_X=\delta_{v_X}\) satisfaz \([\rho_X,\rho_Y]=\rho_{[X,Y]}\).

Para \(c=\theta^A v_{e_A}\), antissimetrizar os dois ghosts em \(sc=c\partial c\) e usar o primeiro sinal dá
\[
d\theta^A=-\tfrac12 f^A{}_{BC}\theta^B\theta^C.
\]
Portanto o diferencial escrito na fonte, com derivada esquerda nos ghosts, é o CE para essa representação:
\[
d_{\rm CE}=\theta^A\rho_{e_A}
-\tfrac12f^A{}_{BC}\theta^B\theta^C\partial^L_{\theta^A}.
\]
Os dois sinais não devem ser absorvidos separadamente numa troca informal \(C\mapsto-C\).

Precisão de leitura que evita uma falsa contradição: \(\rho\) atua no espaço linear de **coordenadas de jatos**, prolongado à álgebra de polinômios. A operação de índices \(\mathfrak r(A)\), quando representada por uma matriz agindo numa coluna de valores tensoriais, tem a ordem de composição correspondente a essa convenção dual. Não se pode substituir a composição das derivações na álgebra pela multiplicação dessas matrizes na mesma ordem. Por exemplo, para geradores covariantes \(w_i\), \(\rho_Aw_i=A^j{}_iw_j\) dá
\[
[\rho_A,\rho_B]w_i=[A,B]^j{}_iw_j
\]
ao aplicar as derivações aos geradores e deixar os coeficientes fixos. Isso confirma a convenção da fonte, não exige corrigi-la.

## 4. Todos os jatos: o termo omitido por uma identificação apenas formal com Lie

Para \(T_r(g)=(\nabla^g)^rW(g)\), \(W(g_0)=0\) implica
\[
T_r(g_0+th)=tW_r+t^2T_{r,2}+\cdots.
\]
A identidade natural \(sT_r=\mathcal L_cT_r\) produz, coeficiente a coeficiente,
\[
s_1W_r+s_0T_{r,2}=\mathcal L_CW_r.
\]
Decompondo a derivada de Lie em transporte e índices,
\[
\mathcal L_CW_r=p^a\bar\nabla_aW_r+\mathfrak r(B)W_r,
\]
e substituindo \(B-M_{\rm gh}=s_0(H/2)\), obtém-se
\[
s_1W_r=p^a\bar\nabla_aW_r+\mathfrak r(M_{\rm gh})W_r
-s_0\!\left(T_{r,2}-\mathfrak r(H/2)W_r\right).
\]
Conferi o sinal do parêntese: transportar os índices altos por S acrescenta \(+H/2\); transportar os baixos por \(S^{-1}\) acrescenta \(-H/2\). Isso é precisamente \(-\mathfrak r(H/2)\), pois \(\mathfrak r\) foi definida pela derivada de Lie.

O tensor \(W_r\) tem r índices covariantes adicionais, além dos quatro índices de Weyl. Todos entram em \(\mathfrak r\). O argumento é válido para cada r finito, com ordem máxima r+2 em h; não depende da TT utilizada pelos detectores079/081. Multiplicar essas fronteiras por outro jato de Weyl fechado por s0, e aplicar Leibniz aos ghosts, constrói uma fronteira finita para qualquer representante quadrático de ordem finita.

Assim a passagem de s1 a CE foi demonstrada em geradores do módulo efetivo, incluindo seus termos s0; não foi inferida somente de uma avaliação especial.

## 5. Transvecções, curvatura e relações do módulo

No ponto base, \(P_a=X(0,e_a)\) tem valor \(e_a\) e derivada covariante nula; \(X_A=X(A,0)\) tem valor zero e derivada A. Logo
\[
\rho_{P_a}W_r=\bar\nabla_aW_r,\qquad
\rho_{X_A}W_r=\mathfrak r(A)W_r.
\]
O comutador matricial é
\[
[P_a,P_b]=-KX_{J_{ab}},\qquad
J_{ab}=e_ae_b^\flat-e_be_a^\flat.
\]
Com essa definição explícita de \(J_{ab}\), a curvatura da referência é \(\bar R_{ab}=KJ_{ab}\). A ação de curvatura é oposta à operação de índices da derivada de Lie: +R nos índices altos e −R nos baixos. Portanto
\[
[\rho_{P_a},\rho_{P_b}]W_r
=[\bar\nabla_a,\bar\nabla_b]W_r
=-K\mathfrak r(J_{ab})W_r.
\]
Em particular, para o jato \(\bar\nabla_eW\), há o termo \(-\bar R^f{}_{eab}\bar\nabla_fW\). Ele é necessário e está presente na fonte.

As fórmulas no ponto não autorizam truncar o Killing ao seu primeiro jato antes de prolongar. A igualdade \(\mathcal L_v\bar\nabla T=\bar\nabla\mathcal L_vT\) para isometrias da conexão inclui as derivadas dos coeficientes de v produzidas pelas derivadas totais. Dizer que esses coeficientes são inertes para \(\delta_v\) não significa que sejam constantes nas derivadas espaciais. É essa distinção que torna compatíveis (19), (22) e (24) da fonte.

Finalmente, isometrias da referência preservam R0, o Hessiano e os mapas adjuntos com suas densidades. Diferenciar essa equivariância dá \([\rho_X,s_0]=0\) no complexo linear completo. Assim \(\rho\) preserva ciclos e fronteiras; Bianchi, EOM e todas as relações lineares usadas em \(\mathcal M\) permanecem relações. Não se trocou \(\mathcal M\) por uma torre livre de símbolos. As derivadas simetrizadas apenas reorganizam a torre; seus comutadores produzem os termos inferiores em K.

## 6. Isotrópico invariante, relativo e módulo infinito

A identificação dos §§2–5 leva ao complexo
\[
\left(C^\bullet(\mathfrak g,\operatorname{Sym}^2\mathcal M)^{\mathfrak h},
d_{\rm CE}\right)
\]
com extensão escalar inerte por \(R_{\rm her}\). O diferencial é equivariante pela isotropia e preserva esse subcomplexo.

O complexo CE relativo exige adicionalmente anulação de todas as inserções de elementos de \(\mathfrak h\). Os cochains presentes contêm \(M_{\rm gh}\); eles podem ser invariantes e não horizontais. Portanto remover esses ghosts ou substituir o subcomplexo invariante pelo relativo mudaria o problema. A fonte evita expressamente essa substituição.

Também é correto não aplicar Whitehead: G tem dimensão dez, mas os coeficientes \(\operatorname{Sym}^2\mathcal M\) contêm jatos de ordem arbitrariamente alta. Um corte de ordem finita é preservado pela isotropia; uma transvecção pode elevar essa ordem. A prova define uma ação infinitesimal no módulo algébrico de elementos finitos, sem demonstrar local finitude sob toda \(\mathfrak g\), integração por Taylor ou simplificação da cohomologia.

## 7. Fonte primária, parâmetros e estatuto

[KNOWN — fonte primária conferida] Li [Khavkine, arXiv:1805.03751v2](https://arxiv.org/pdf/1805.03751v2), §3, equações (22–25), e o parágrafo imediatamente seguinte. A conexão de transporte de Killing ali escrita relaciona o vetor e sua derivada antissimétrica; sua planura na curvatura constante sustenta o uso local dos dez dados. A citação da nota é adequada a esse alcance. Ela não fornece o cálculo CE com o módulo quadrático específico, e não a utilizei como se fornecesse.

K e κ são reais fixados no domínio revisado; \(R_{\rm her}\) permanece extensão escalar inerte. O embedding auxiliar com \(1/K\) não institui uma categoria uniforme em K variável. As fórmulas cohomológicas não eliminam essa restrição.

Os coeficientes da raiz formal e dos completamentos naturais são finitos em cada aridade. O fator \(t s_1\) aumenta a valência em uma unidade e é compatível com o expoente Rees explicitado. Isso não comuta cohomologia com limite inverso, não prova Mittag–Leffler e não paga automaticamente as condições causais Q2 de escala, inserções ou contatos. Nenhuma restrição de peso suplementar foi silenciosamente imposta para obter um espaço finito.

[OPEN] Continua necessário calcular a imagem efetiva de \(d_{\rm CE}\) entre os graus três e quatro, com todas as relações do módulo e a admissibilidade requerida, para decidir o problema de −[A6]. O teste de dez contrações sem derivadas e a presente identificação do diferencial são resultados distintos. Não incorporo resultados083.

## 8. Custódia desta revisão

[REAL] O helper novo desta pasta apenas lê bytes, mede SHA-256, compara os pins do manifesto, verifica destinos de links e publica este parecer e seu recibo por arquivo temporário seguido de renomeação. Não executa o writer da fonte nem qualquer código matemático antecedente. Os pins do recibo nomeiam arquivos finais existentes; nenhum caminho temporário renomeado permanece como pin.

O recibo discrimina controles documentais de demonstrações escritas. A contagem documental não constitui prova Lean ou validação CAS. As fontes congeladas permanecem intactas. A conclusão é de minha análise no domínio acima; não constitui mudança de gate, confirmação física, QME ou resolução da gravidade quântica.
