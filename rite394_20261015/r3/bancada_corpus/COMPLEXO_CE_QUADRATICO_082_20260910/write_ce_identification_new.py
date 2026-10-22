from pathlib import Path
import hashlib
import json
import os
import re
from datetime import datetime, timezone

ROOT = Path(r"C:/IALD/Central de Patentes/Chatgpt")
OUT = ROOT / "COMPLEXO_CE_QUADRATICO_082_20260910"
NOTE_NAME = "IDENTIFICACAO_D1_CE_KILLING_E_JATOS_WEYL.md"
SOURCES = [
    ROOT / "TRANSGRESSAO_BRST_CARACTERISTICA_076_20260910/TRANSGRESSAO_TOTAL_E_PRIMITIVA_GHOST4.md",
    ROOT / "REVISAO_TRANSGRESSAO_BRST_076_20260910/PARECER_TRANSGRESSAO_TOTAL_E_GHOST4.md",
    ROOT / "SOBREVIVENTE_PONTRYAGIN_077_20260910/DICIONARIO_CARTAN_DO_RECIBO_077.md",
    ROOT / "PRIMEIROS_TRUNCAMENTOS_BRST_077_20260910_030228_0972771/ADENDO_SINAL_KOSZUL_TATE_077.md",
    ROOT / "GERACAO_WEYL_H3_E4_080_20260910/GERACAO_NATURAL_H3_E4_E_LIMITE_DOS_COEFICIENTES.md",
    ROOT / "COHOMOLOGIA_QUADRATICA_WEYL_081_20260910/H3_E5_BIANCHI_E_REPRESENTANTES_QUADRATICOS_WEYL.md",
    ROOT / "REVISAO_REDUCAO_QUADRATICA_081_20260910_050052_914909/PARECER_H3_E5_E_REPRESENTANTES_QUADRATICOS_081.md",
    ROOT / "LIBERDADE_DE_LEVANTAMENTO_079_20260910/ADENDO_IDEAL_FECHADO_E_COEFICIENTES_HERDADOS_079.md",
    ROOT / "COMPLETACAO_REES_BRST_074_20260910/COMPLETACAO_POR_LACOS_E_VALENCIA.md",
]
NOTE = r"""# O diferencial d1 como CE da álgebra de Killing no módulo quadrático de jatos

10/09/2026. Investigação082 NOVA, fora da entrega081. [DERIVED — demonstração escrita, aguardando revisão independente específica]. Zero CAS, Lean ou execução/importação de um.py. Todas as fontes anteriores permanecem intactas.

**Resultado.** Na categoria métrica, espaço-forma fixada, de080/081, o primeiro diferencial no setor de duas pernas métricas é o diferencial de Chevalley–Eilenberg da álgebra de Killing, atuando sobre o módulo quadrático dos jatos lineares de Weyl modulo EOM. A naturalidade seleciona o subcomplexo invariante pela isotropia. A identificação inclui as translações e toda ordem FINITA de jatos, com os termos de curvatura e as fronteiras s0 explícitos.

Não se calcula aqui a cohomologia desse CE, não se demonstra local finitude sob a álgebra de Killing inteira e não se decide se −[A6] pertence à imagem do canal livre δ(K).

## 1. Categoria, notação e diagonal cohomológica

Conservamos exatamente o domínio da [redução081](<C:/IALD/Central de Patentes/Chatgpt/COHOMOLOGIA_QUADRATICA_WEYL_081_20260910/H3_E5_BIANCHI_E_REPRESENTANTES_QUADRATICOS_WEYL.md>): referência g0 Lorentziana orientada, espaço-forma em quatro dimensões, K=Λ/3>0 fixado, κ não nulo fixado, φ0 constante, complexo métrico mínimo puro projetado. O anel real R_her de escalares herdados é conservado e tem ação trivial das isometrias. Nenhum tensor espectador adicional, fonte externa de ghost positivo ou frame físico extra entra.

O [adendo079](<C:/IALD/Central de Patentes/Chatgpt/LIBERDADE_DE_LEVANTAMENTO_079_20260910/ADENDO_IDEAL_FECHADO_E_COEFICIENTES_HERDADOS_079.md>) continua valendo: não substituímos o anel herdado por um anel menor. Aqui ele já foi separado como extensão escalar após fixar os parâmetros do operador de referência. Não concluímos um teorema uniforme num anel restrito em K variável.

Denote por \(\mathcal M=H^0(L,s_0)\) o módulo real de observáveis lineares de curvatura modulo todas as EOM lineares, e por \(G=H^1(L,s_0)\) o espaço dos dez geradores de ghost. A letra M SEM caligrafia, usada abaixo, será uma matriz de ghost antissimétrica, não o módulo \(\mathcal M\). Ponha
\[
N=\operatorname{Sym}^2\mathcal M,\qquad
\mathfrak h=\mathfrak{so}(1,3).
\tag{1}
\]

080/081 provaram a geração de \(\mathcal M\) por jatos de Weyl e \(H^{-1}(L,s_0)=0\). O [parecer independente081](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_REDUCAO_QUADRATICA_081_20260910_050052_914909/PARECER_H3_E5_E_REPRESENTANTES_QUADRATICOS_081.md>) foi lido como aprovação da aplicação081, não desta nova identificação082.

A mesma contagem estende-se a toda a diagonal E=q+2: como os graus dos geradores lineares não excedem1, o déficit
\[
E-\mathrm{gh}=\sum_i(1-\mathrm{gh}_i)=2
\]
só admite dois fatores de ghost0, ou um de ghost−1. O segundo caso desaparece por081. Portanto, para q≥0,
\[
\boxed{
H^q(\mathcal A_{\rm nat},s_0)_{E=q+2}
\simeq R_{\rm her}\otimes_{\mathbb R}
   [N\otimes\Lambda^qG]^{\mathfrak h}.
}
\tag{2}
\]
É uma afirmação sobre zeroformas de jatos pontuais, antes de qualquer quociente por d_H. Como em081, invariantes são tomados em cortes tensoriais finitos e depois na união. Não se usa exatidão de invariantes para um módulo arbitrário da álgebra de Killing completa.

Escrevemos \(s_t=s_0+t s_1+\cdots\), \(g=g_0+t h\), \(c=tC\). O diferencial induzido por s1 aumenta ghost e valência em uma unidade. Assim (2) é a diagonal correta tanto para o domínio q=3/E5 quanto para o alvo q=4/E6.

## 2. Os ghosts corretos vêm do mesmo transporte métrico076

Use as convenções \(sg=\mathcal L_cg\), \(sc^\mu=c^\rho\partial_\rho c^\mu\) e o [sinal KT corrigido077](<C:/IALD/Central de Patentes/Chatgpt/PRIMEIROS_TRUNCAMENTOS_BRST_077_20260910_030228_0972771/ADENDO_SINAL_KOSZUL_TATE_077.md>). Defina
\[
H=g_0^{-1}h,\qquad
B^a{}_b=\bar\nabla_bC^a,\qquad
M=\tfrac12(B-g_0^{-1}B^Tg_0),\qquad p^a=C^a.
\tag{3}
\]
Temos
\[
B-M=s_0(H/2).
\tag{4}
\]
Com \(m_{ab}=\bar\nabla_{[a}C_{b]}\), a matriz de(3) satisfaz \(M_{ab}=-m_{ab}\). Esse sinal não será alterado por conveniência.

Na [transgressão076](<C:/IALD/Central de Patentes/Chatgpt/TRANSGRESSAO_BRST_CARACTERISTICA_076_20260910/TRANSGRESSAO_TOTAL_E_PRIMITIVA_GHOST4.md>), a MESMA raiz formal e o MESMO ghost transportado são
\[
S=(g_0^{-1}g)^{1/2},\qquad v=\nabla^gc,\qquad
k=SvS^{-1}-(sS)S^{-1}.
\tag{5}
\]
k é antissimétrico para g0 e não é um ghost Lorentz independente. Não se toma uma conexão homônima como se fosse(5). As identidades exatas076 são
\[
sk+k^2=\Omega,\qquad
\Omega=S\bigl(\tfrac12R(g)^a{}_{bcd}c^cc^d\bigr)S^{-1}.
\tag{6}
\]

Há também um vetor de ghost transportado \(\widetilde p=Sc\). Pela torsão zero e pela paridade ímpar de c,
\[
sc=-vc.
\]
Logo
\[
s\widetilde p=(sS)c-Svc=-k\widetilde p.
\tag{7}
\]
Aqui S é par; o sinal em \(sc=-vc\) vem de trocar os dois fatores ímpares \(\nabla c\) e c.

Expandindo
\[
\widetilde p=t p+t^2p_2+\cdots,\quad p_2=\tfrac12Hp,\qquad
k=tM+t^2k_2+\cdots,
\]
e usando a curvatura constante, o coeficiente de t² em(6–7) fornece
\[
s_1p+s_0p_2=-Mp,
\qquad
s_1M+s_0k_2=-M^2+Kpp^\flat.
\tag{8}
\]
Portanto, em \(H(s_0)\),
\[
\boxed{d_1p=-Mp,\qquad d_1M=-M^2+Kpp^\flat.}
\tag{9}
\]
Não se impôs Killing ao ghost livre para obter essas igualdades. Os termos s0 exibidos são o que permite passar dos seus jatos livres aos representantes de cohomologia.

O [dicionário matricial077](<C:/IALD/Central de Patentes/Chatgpt/SOBREVIVENTE_PONTRYAGIN_077_20260910/DICIONARIO_CARTAN_DO_RECIBO_077.md>) já comparava(9) com o CE de constantes. Agora precisamos também da ação nos coeficientes N; isso não estava pago apenas pela matriz dos ghosts.

## 3. Completar naturalmente cada jato de Weyl paga os termos s0

Fixe o tipo tensorial \((1,3+r)\) e considere, com todos os índices de derivadas mantidos,
\[
T_r(g)=(\nabla^g)^r W(g),\qquad r\ge0.
\tag{10}
\]
Como \(W(g_0)=0\) e todas as suas derivadas são zero,
\[
T_r(g_0+t h)=t W_r+t^2T_{r,2}+\cdots,\qquad
W_r=\bar\nabla^rW_{[1]}[h].
\tag{11}
\]
Para r fixo, esses coeficientes têm ordem finita de jatos, no máximo r+2 nas derivadas de h. Não se usa uma série infinita em jatos num único coeficiente.

T_r é um tensor natural do campo completo. Assim
\[
sT_r(g)=\mathcal L_cT_r(g),
\]
e o coeficiente de t² é a identidade OFF-SHELL
\[
\boxed{s_1W_r+s_0T_{r,2}=\mathcal L_CW_r.}
\tag{12}
\]
A fórmula vale para TODO r, não apenas para r=0 ou numa avaliação de Killing.

Para um endomorfismo A, denote por \(\mathfrak r(A)\) a operação de índices da derivada de Lie: −A em cada índice alto e +A em cada índice baixo. Portanto
\[
\mathcal L_CW_r=p^a\bar\nabla_aW_r+\mathfrak r(B)W_r.
\tag{13}
\]
Os r índices de derivadas são índices baixos adicionais e entram na segunda parcela. Omiti-los daria uma ação incorreta nos jatos superiores.

Pelas identidades \(s_0W_r=0\) e(4),
\[
s_0\bigl(\mathfrak r(H/2)W_r\bigr)
=\mathfrak r(B-M)W_r.
\]
Consequentemente
\[
\boxed{
s_1W_r=p^a\bar\nabla_aW_r+\mathfrak r(M)W_r
-s_0\bigl(T_{r,2}-\mathfrak r(H/2)W_r\bigr).
}
\tag{14}
\]
Isso calcula o termo que seria indevidamente perdido ao escrever apenas “s1W é Lie”.

Existe uma interpretação direta do parêntese. Transporte cada índice alto de T_r por S e cada índice baixo por S⁻¹. O tensor resultante \(\widetilde T_r\) tem segundo coeficiente
\[
\widetilde T_{r,2}=T_{r,2}-\mathfrak r(H/2)W_r.
\tag{15}
\]
O sinal pode ser conferido no tensor covariante g: o transporte \(S^{-T}gS^{-1}=g_0\) tem variação oposta à ação de índices \(\mathfrak r(H/2)\).

Logo o primeiro diferencial nas classes dos jatos é
\[
\boxed{d_1[W_r]=p^a[\bar\nabla_aW_r]+\mathfrak r(M)[W_r].}
\tag{16}
\]
O resultado respeita produtos: os W_r são pares e fechados por s0, então multiplicar o termo s0 de(14) por outro W_l continua dando uma fronteira. As correções de(8) e(14), inseridas por Leibniz, dão uma correção finita também para qualquer Q quadrático de081.

As relações de EOM não foram apagadas. A seguir verificamos que a ação de(16) desce ao quociente \(\mathcal M\); isso é diferente de declarar a torre de W livre.

## 4. Qual álgebra de Killing e qual sinal de representação?

É preciso separar três objetos: campos vetoriais Killing com o colchete usual, matrizes infinitesimais de isometria, e derivações evolutivas sobre coordenadas de jatos.

Uma realização local da espaço-forma usa a quádrica no espaço com forma bilinear
\[
\widehat g=\operatorname{diag}(g_0,1/K).
\]
Na origem da carta normal escolhida sobre a quádrica, o ponto base é \((0,1)\), com tangente identificado a V. A álgebra matricial \(\mathfrak g\) consiste em
\[
X(A,a)=
\begin{pmatrix}A&a\\-K a^\flat&0\end{pmatrix},
\qquad A\in\mathfrak h,\ a\in V.
\tag{17}
\]
Aqui g0 na matriz denota sua forma bilinear no ponto. O artifício da quádrica fixa o dicionário de sinais; os resultados(8–16) são tensoriais e não exigem um embedding escolhido como dado físico.

O campo infinitesimal correspondente é \(v_X(q)=Xq\). Com o colchete usual de campos vetoriais,
\[
[v_X,v_Y]=-v_{[X,Y]}.
\tag{18}
\]
De fato, \(v_X\cdot\partial v_Y=YXq\). A atribuição matriz→campo fundamental é um anti-homomorfismo nesta convenção.

Agora defina a derivação EVOLUTIVA \(\delta_v\) sobre jatos de h por
\[
\delta_vh=\mathcal L_vh,\qquad
\delta_vg_0=0,
\]
prolongando às derivadas e deixando fixos os coeficientes de v e da referência. Em particular, ela não é o operador que transporta simultaneamente esses coeficientes como campos ativos. Duas dessas derivações obedecem
\[
[\delta_v,\delta_w]h
=\mathcal L_w\mathcal L_vh-\mathcal L_v\mathcal L_wh
=-\mathcal L_{[v,w]}h.
\tag{19}
\]
Os dois sinais se cancelam. Portanto
\[
\boxed{\rho_X:=\delta_{v_X},\qquad
[\rho_X,\rho_Y]=\rho_{[X,Y]}}
\tag{20}
\]
é uma representação da álgebra MATRICIAL \(\mathfrak g\) nas coordenadas de jatos.

Para os ghosts, escreva \(c=\theta^A v_{e_A}\), numa base matricial fixa. De \(sc=c\partial c\) e(18) resulta
\[
d\theta^A=-\tfrac12f^A{}_{BC}\theta^B\theta^C.
\tag{21}
\]
São precisamente a convenção CE e os sinais de(9). Se se preferir a álgebra de campos Killing com o colchete usual, deve-se trocar simultaneamente a identificação de ghosts e a ação para a representação \(-\delta_v\). Não misturamos as duas convenções.

Na notação matricial de(17), o ghost total é
\[
\Theta=
\begin{pmatrix}M&p\\-Kp^\flat&0\end{pmatrix}.
\]
A equação \(d\Theta=-\Theta^2\) reproduz(9). Nenhuma divisão por K aparece nessa equação. O uso de \(1/K\) em \(\widehat g\) apenas realiza geometricamente a álgebra para o K fixo não nulo do contrato; não amplia a classe natural a coeficientes singulares em K.

## 5. A ação desce ao módulo de Weyl on-shell e inclui todas as translações

Cada v_X é Killing da referência. Sua ação preserva o operador de gauge linear, o Hessiano Einstein de fundo e os mapas adjuntos nas densidades. Isso segue da naturalidade dos operadores e de \(\mathcal L_{v_X}g_0=0\): conjugá-los por uma isometria não os altera, e diferenciar essa identidade dá a comutação.

Prolongando também a ação natural a ghosts e antifields, \([\rho_X,s_0]=0\) no complexo linear. Logo ciclos e fronteiras lineares são preservados. A ação induzida em
\[
\mathcal M=H^0(L,s_0)
\]
é bem definida; estende-se por Leibniz a \(N=\operatorname{Sym}^2\mathcal M\). Uma relação entre jatos de Weyl proveniente de EOM, Bianchi ou fronteira permanece uma relação após a ação. Não se introduz um módulo livre diferente do quociente081.

A identificação de todos os jatos de Killing com \((v(x),\bar\nabla v(x))\) pode ser vista pela conexão de transporte de Killing, que é plana na espaço-forma. [Khavkine, arXiv:1805.03751v2, §3, equações(22–25)](https://arxiv.org/pdf/1805.03751) fornece essa conexão e o critério de planura. Usamos apenas essa afirmação local; a fonte não é invocada como um cálculo de CE com os coeficientes quadráticos desta nota.

Seja \(P_a=X(0,e_a)\) uma transvecção. No ponto base,
\[
v_{P_a}=e_a,\qquad \bar\nabla v_{P_a}=0.
\]
Se \(X_A=X(A,0)\) pertence à isotropia, no mesmo ponto \(v_{X_A}=0\) e \(\bar\nabla v_{X_A}=A\). Aplicando a derivada de Lie ao tensor completo W_r,
\[
\rho_{P_a}[W_r]=[\bar\nabla_aW_r],
\qquad
\rho_{X_A}[W_r]=\mathfrak r(A)[W_r].
\tag{22}
\]
A notação \(\bar\nabla_aW_r\) inclui o jato seguinte na ordem indicada. Não se afirma que um corte de ordem r fique estável sob transvecções.

Os colchetes matriciais são
\[
[X_A,P_a]=P_{Ae_a},\qquad
[P_a,P_b]=-KX_{J_{ab}},\qquad
J_{ab}=e_a e_b^\flat-e_b e_a^\flat.
\tag{23}
\]
A curvatura reproduz o segundo colchete em TODOS os jatos:
\[
\begin{aligned}
[\rho_{P_a},\rho_{P_b}][W_r]
&=[(\bar\nabla_a\bar\nabla_b-\bar\nabla_b\bar\nabla_a)W_r]\\
&=-\mathfrak r(\bar R_{ab})[W_r]
=-K\mathfrak r(J_{ab})[W_r].
\end{aligned}
\tag{24}
\]
Nossa \(\mathfrak r\) é a operação de índices da derivada de Lie: a ação de curvatura tem o sinal oposto, +R nos índices altos e −R nos baixos. Essa é a razão do sinal em(24).

O comutador age também nos r índices covariantes que registram as derivadas. Por exemplo, no jato \(\bar\nabla_eW\), a curvatura tem a parcela \(-\bar R^f{}_{eab}\bar\nabla_fW\), além das quatro parcelas dos índices de W. Esse termo não pode ser omitido nem tratado como uma derivada plana.

Também não se pode obter(24) congelando a primeira ordem de um Killing e esquecendo o resto de seus jatos. As derivações de(20) são prolongadas: ao atuar outra vez, derivam os coeficientes do primeiro campo quando estes aparecem dentro da expressão diferenciada no argumento. A identidade \(\mathcal L_v\bar\nabla T=\bar\nabla\mathcal L_vT\), válida para uma isometria da conexão, fornece exatamente esses termos. Equivalentemente, as coordenadas de jatos tratam todos os índices de \(\bar\nabla^rW\) como índices tensoriais em(22).

Se os jatos forem reduzidos a derivadas simetrizadas e aos tipos irredutíveis080, os comutadores de derivadas geram os termos inferiores proporcionais a K. A ação no graduado superior não deve ser confundida com a ação inteira. O teorema presente usa o módulo real de jatos com essas relações e termos inferiores, e não apenas seus símbolos.

## 6. Identificação do diferencial no complexo de cochains

Defina o CE com coeficientes N pela derivação
\[
d_{\rm CE}
=\theta^A\rho_{e_A}
-\tfrac12 f^A{}_{BC}\theta^B\theta^C
 \frac{\partial^L}{\partial\theta^A}
\quad\text{em }N\otimes\Lambda^\bullet\mathfrak g^*.
\tag{25}
\]
A derivada exterior nos ghosts é à esquerda. N é par; os sinais nos produtos vêm dos ghosts. As equações(20–21) garantem \(d_{\rm CE}^2=0\).

A identificação \(G\simeq\mathfrak g^*\) é feita pelos dez dados de(3), com a convenção(17–21). Em geradores de cohomologia, (8) e(14) calculam precisamente as duas partes de(25). Por Leibniz, isso vale em todos os produtos finitos. Logo
\[
\boxed{
\left(
\bigoplus_{q\ge0}H^q(\mathcal A_{\rm nat},s_0)_{E=q+2},
\,d_1
\right)
\simeq
R_{\rm her}\otimes_{\mathbb R}
\left(C^\bullet(\mathfrak g,N)^{\mathfrak h},\,d_{\rm CE}\right).
}
\tag{26}
\]
Aqui a soma em q é finita nos ghosts restantes porque \(\dim\mathfrak g=10\); a ordem dos jatos nos coeficientes N continua sem limite uniforme.

Em particular,
\[
\boxed{
[s_1Q]\ \longleftrightarrow\ d_{\rm CE}[Q],
\quad
Q\in[N\otimes\Lambda^3\mathfrak g^*]^{\mathfrak h}.
}
\tag{27}
\]
Uma diferença \(Q\mapsto Q+s_0\chi\) altera o representante de s1Q por \(-s_0s_1\chi\), como já tipado081. Não são retiradas as fronteiras antifield do alvo.

Uma maneira concreta de ler(27) é substituir em Q:
\[
d_1p=-Mp,\quad
d_1M=-M^2+Kpp^\flat,\quad
d_1W_r=p^a\bar\nabla_aW_r+\mathfrak r(M)W_r,
\tag{28}
\]
usar Leibniz graduado e depois passar às relações lineares de Weyl/EOM em cada um dos dois fatores. As fórmulas(8),(14) asseguram que esse procedimento computa a CLASSE do s1 original; não só uma avaliação especial de seus ghosts.

A isotropia atua diagonalmente nos coeficientes e nos ghosts. O diferencial(25) é equivarante, portanto preserva essa parte invariante. As contrações naturais no ponto e seu transporte por isometrias locais são justamente a naturalização fixada080. Nenhuma média sobre o grupo Lorentz não compacto é introduzida aqui.

## 7. Invariante pela isotropia não significa CE relativo

O lado direito de(26) é \(C^\bullet(\mathfrak g,N)^{\mathfrak h}\). Não o identificamos com o complexo RELATIVO \(C^\bullet(\mathfrak g,\mathfrak h;N)\).

O complexo relativo exige, além da invariância, horizontalidade: inserir um elemento da isotropia deve anular o cochain. Os representantes081 podem conter M, isto é, ghosts da própria isotropia. Eles não são horizontais por definição. Retirá-los mudaria o problema e eliminaria, por exemplo, as espécies CCm examinadas079/081.

Também não comutamos automaticamente a cohomologia do CE inteiro com os invariantes para substituí-lo por outro grupo. O que foi provado é o isomorfismo de complexos(26) com o subcomplexo indicado. Qualquer simplificação cohomológica posterior requer uma demonstração própria no módulo N pertinente.

## 8. Finitude, filtração e o que não se pode concluir por Whitehead

Cada elemento de \(\mathcal M\) é representado por uma combinação FINITA de jatos de Weyl; cada elemento de N é uma combinação finita de produtos de dois deles. A ação de uma transvecção aumenta a ordem em no máximo uma unidade antes de reduzir as relações, enquanto a isotropia preserva a ordem.

Isso define um módulo algébrico da álgebra de Killing: uma ação infinitesimal sobre cada elemento termina em outro elemento finito. Não exige integrar a ação de transvecções para mover o ponto por uma série de Taylor convergente, nem autoriza fazê-lo sobre jatos apenas formais.

Os cortes finitos são localmente finitos sob a ISOTROPIA. Eles não foram provados estáveis sob \(\mathfrak g\). Aplicar repetidamente translações pode exigir ordens cada vez maiores. Logo não se usa o lema de Whitehead nem a cohomologia de um módulo finito apenas porque G tem dimensão dez ou \(\mathfrak h\) é redutiva. A dimensão da álgebra não é a dimensão do módulo de coeficientes.

As correções p2,k2,\(\widetilde T_{r,2}\) conservam o déficit de pernas apropriado: cada uma acrescenta uma perna h ao representante linear; s0 troca uma perna h por C. O termo \(t s_1\), atuando em \(t^{E+2L_{\rm loop}-2}Q_E\), dá o peso \(t^{E+1+2L_{\rm loop}-2}\), como exige a [completação Rees074](<C:/IALD/Central de Patentes/Chatgpt/COMPLETACAO_REES_BRST_074_20260910/COMPLETACAO_POR_LACOS_E_VALENCIA.md>).

Para cada aridade, as fórmulas de(8),(14) envolvem um número finito de produtos e derivadas. Assim a identificação de d1 é válida coeficiente a coeficiente nessa completação. Não se permuta cohomologia com um limite inverso; não se introduz uma soma infinita de jatos no mesmo coeficiente; não se decide um possível termo lim¹ da cohomologia completa.

Naturalidade e esse controle de valência tampouco demonstram todas as restrições Q2 de scaling degree, contatos, inserções ou normalização causal. Uma solução de(27) num módulo maior ainda teria de pertencer à classe admissível exigida. O presente cálculo não usa uma especialização numérica do parâmetro formal t.

## 9. Avanço e obrigação remanescente

[DERIVED — no domínio fixado] O próximo diferencial da redução081 foi identificado, com sinais, ação nos coeficientes e termos s0: é(25–28). Ação de transvecções, curvatura K e índices de todos os jatos estão contabilizados. A referência é inerte, mas suas conexões e curvaturas não são congeladas dentro das derivadas.

[OPEN] Calcular a imagem do operador
\[
d_{\rm CE}:
[N\otimes\Lambda^3\mathfrak g^*]^{\mathfrak h}
\longrightarrow
[N\otimes\Lambda^4\mathfrak g^*]^{\mathfrak h}
\]
no módulo quadrático real com suas relações e, especificamente, testar a classe −[A6]. O cálculo finito de uma família de Q pode restringir essa imagem, mas não substitui a determinação do módulo inteiro.

Permanecem fora do alcance: fundo físico φ=id, espectadores tensoriais ou não constantes, mudança de anel uniforme em K variável, classificação da anomalia geral, transporte de esquemas causais, QME, UV e suficiência geral da gravidade quântica.

[REAL — documental] O manifesto mede as fontes listadas antes/depois e os novos artefatos. As revisões anteriores são antecedentes de alcance próprio. Esta nova identificação não recebe aprovação externa por herança. Nenhum arquivo existente ou fonte congelada foi modificado.
"""

def pin(path):
    data = path.read_bytes()
    return {"path": str(path), "bytes": len(data), "sha256": hashlib.sha256(data).hexdigest()}

def emit_exclusive(path, data):
    if path.exists():
        raise FileExistsError(path)
    temp = path.with_name(path.name + ".new_pending")
    with temp.open("xb") as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    if temp.read_bytes() != data:
        raise RuntimeError("Temporary bytes differ")
    if path.exists():
        raise FileExistsError(path)
    temp.rename(path)
    if path.read_bytes() != data:
        raise RuntimeError("Final bytes differ")
    return pin(path)

OUT.mkdir(parents=True, exist_ok=True)
self_path = Path(__file__).resolve()
before = [pin(path) for path in SOURCES]
self_before = pin(self_path)
data = NOTE.encode("utf-8")
if not data or b"\x00" in data:
    raise RuntimeError("Empty or NUL-bearing note")
links = re.findall(r"\]\(<(C:/[^>]+)>\)", NOTE)
link_checks = [{"path": link, "exists": Path(link).is_file()} for link in links]
if not all(item["exists"] for item in link_checks):
    raise RuntimeError("Missing local link")
note_pin = emit_exclusive(OUT / NOTE_NAME, data)
after = [pin(path) for path in SOURCES]
self_after = pin(self_path)
if before != after or self_before != self_after:
    raise RuntimeError("Source or writer changed; preserve output as diagnostic")
manifest = {
    "scope": "DERIVED_WRITTEN_082_AWAITING_SPECIFIC_INDEPENDENT_REVIEW",
    "created_utc": datetime.now(timezone.utc).isoformat(),
    "sources_before": before, "sources_after": after,
    "all_sources_unchanged": before == after,
    "script_before": self_before, "script_after": self_after,
    "script_unchanged": self_before == self_after,
    "artifacts": [note_pin],
    "local_link_checks": link_checks,
    "all_local_links_exist": all(item["exists"] for item in link_checks),
    "primary_source_read": {
        "url": "https://arxiv.org/pdf/1805.03751",
        "version_read": "v2",
        "scope": "Section 3 equations22-25: Killing transport, flat at constant curvature; not CE coefficient cohomology"
    },
    "mathematical_status": "Written derivation; no automated mathematical proof claimed",
    "new_cas_controls": 0, "new_lean_controls": 0,
    "um_py_executed_or_imported": False,
    "existing_files_modified": False,
    "external_approval_attributed": False
}
manifest_pin = emit_exclusive(OUT / "MANIFESTO_IDENTIFICACAO_CE_082.json", (json.dumps(manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))
print(json.dumps({
    "note": note_pin, "manifest": manifest_pin,
    "sources_unchanged": len(before),
    "local_links_verified": len(link_checks),
    "new_cas_controls": 0, "new_lean_controls": 0
}, ensure_ascii=False, indent=2))

