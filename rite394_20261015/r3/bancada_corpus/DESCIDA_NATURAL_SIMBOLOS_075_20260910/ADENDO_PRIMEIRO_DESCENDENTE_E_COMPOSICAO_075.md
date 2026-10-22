# Composição: primeiro descendente e descida natural completa

10/09/2026, arco075. [DERIVED — composição escrita]. Adendo novo à [prova por operadores](<C:/IALD/Central de Patentes/Chatgpt/DESCIDA_NATURAL_SIMBOLOS_075_20260910/DESCIDA_NATURAL_POR_OPERADORES.md>), sem editar seu texto ou manifesto. A lacuna sobre o primeiro descendente, ali separada nas seções7/9/10, recebe aqui uma solução com antecedente explícito: a relação inicial de consistência já precisa valer ordinariamente e off-shell.

## 1. Entrada independente lida

A [auditoria075, seções6–7](<C:/IALD/Central de Patentes/Chatgpt/AUDITORIA_DESCIDA_NATURAL_075_20260910/SIMBOLOS_GRASSMANN_E_PRIMEIRO_DESCENDENTE.md>) constrói a primitiva natural de uma top-forma F de ghost positivo que já é uma divergência ordinária. Conferimos sua composição com a prova q<4. As hipóteses são as mesmas: jatos livres dos geradores Z de ghost não zero, coeficientes sem ghost positivo central oculto, conexões naturais independentes de Z e identidade universal off-shell.

Se F=d_Hβ ordinariamente, então todos os seus operadores de Euler em Z se anulam. Decomponha F em grau Euler_Z homogêneo N>0. Por graus, cada F_N continua com operadores de Euler nulos. A linearização par em variações livres v satisfaz a fórmula de primeira variação por integração por partes covariante,

\[
\ell^Z_{F_N}(v)=\sum_A v^A\mathcal E_A(F_N)
                       +d_H\Theta_{F_N}[v]
                    =d_H\Theta_{F_N}[v].
\tag{1}
\]

Cada integração por partes retira uma derivada de v e a transfere ao coeficiente; após um número finito de passos, todas foram transferidas. A corrente Θ é natural, local em jatos e linear em v. Derivadas de coeficientes e conexões não são omitidas; os sinais são os da variação par com ordem dos fatores fixada. Não há uma integral não local de β nem a necessidade de tornar β natural por escolha.

A avaliação v=Z comuta com d_H e dá Euler. Logo

\[
\boxed{F_N=d_H\eta_N,\qquad
\eta_N=\Theta_{F_N}[Z]/N.}
\tag{2}
\]

Isso não declara toda top-forma fechada exata. O antecedente F=d_Hβ é o que zera o termo de Euler; não se pode retirá-lo. Tampouco se aplica (2) ao setor N=0, que contém, por exemplo, densidades características do fundo.

## 2. A descida completa agora pode ser escolhida natural

Suponha que a₄¹ seja natural, s seja natural com s²=0 e {s,d_H}=0, e a consistência ordinária satisfaça

\[
s a_4^1+d_H\beta_3^2=0
\tag{3}
\]

como identidade na álgebra off-shell declarada. F=s a₄¹ tem ghost2, é natural e é uma divergência ordinária por (3). Aplicando (2), escreva F=d_Hη₃² e escolha a₃²=−η₃². Assim o primeiro descendente é natural.

Aplicar s dá d_H(s a₃²)=0. A prova por símbolos da nota principal, agora em grau3<4 e ghost positivo, fornece a₂³ natural com s a₃²+d_Ha₂³=0. Repita em graus2 e1. Em grau0, d_H(s a₀⁵)=0 e o caso zero da mesma prova força s a₀⁵=0. Obtém-se

\[
\Omega=a_4^1+a_3^2+a_2^3+a_1^4+a_0^5,
\qquad (s+d_H)\Omega=0,
\tag{4}
\]

inteiramente no subcomplexo natural escolhido.

Portanto, a necessidade de naturalizar separadamente o primeiro descendente mencionada na nota principal fica paga por (1)–(3) QUANDO o antecedente de consistência ordinária off-shell é fornecido. Não se presume que toda quebra renormalizada já satisfaça esse antecedente na álgebra universal requerida: isso permanece uma verificação de aplicação.

## 3. Contagem perturbativa e limites

Na apresentação por fibrados normalizados de B0 da [nota Rees074](<C:/IALD/Central de Patentes/Chatgpt/COMPLETACAO_REES_BRST_074_20260910/COMPLETACAO_POR_LACOS_E_VALENCIA.md>), as conexões da integração por partes têm grau zero em flutuações. A linearização reduz uma perna Z no coeficiente e introduz uma v; transferir derivadas não muda a quantidade de pernas, e v=Z recompõe o mesmo grau. Dividir por N não altera nenhuma graduação. Assim o primeiro descendente construído por (2), tal como os descendentes q<4, conserva E,N e o peso t^(E+2L−2) de cada componente.

A corrente de cada componente tem ordem de jatos finita. Sua saída no grau E depende apenas da entrada nesse E; a composição é contínua coeficiente a coeficiente na classe Rees especificada. Se s também conserva essa classe, como no controle algébrico074, a cadeia (4) permanece nela. Fontes ou pesos não abrangidos por essa classe exigem sua contagem própria.

Regularidade, naturalidade e peso de engenharia seguem das operações covariantes finitas, nas condições da nota principal. A presença de g0 para escrever a top-forma como densidade e fazer integração por partes é uma escolha natural de fundo já admitida; não é uma métrica positiva auxiliar ou uma mudança do fundo físico.

[DERIVED] Fica construída a DESCIDA NATURAL de uma anomalia natural com consistência ordinária universal, no setor livre de ghost positivo e nas classes de coeficientes e conexões explicitadas.

[OPEN] Não foi construída uma primitiva de Ω para s+d_H. Fazer uma descida inteira natural não demonstra que a classe total ou H¹,⁴(s|d_H) seja nula. Admissibilidade da remoção da anomalia na hierarquia causal, QME e independência quântica de fundo continuam distintas.

Quatro fontes medidas antes/depois da escrita. Zero CAS/Lean novos; nenhum original ou fonte congelada alterado; nenhum um.py executado/importado.
