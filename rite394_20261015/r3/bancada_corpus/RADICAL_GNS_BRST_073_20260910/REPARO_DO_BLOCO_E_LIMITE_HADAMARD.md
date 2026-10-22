# Reparo do bloco auxiliar e limite da conclusão Hadamard

10/09/2026, frente 073. [DERIVED — prova algébrica escrita]. Adendo novo à nota `RADICAL_DA_PSEUDOCOVARIANCIA_E_P0.md`; não modifica essa nota ou qualquer fonte anterior.

## 1. Reparo efetivo do contraexemplo finito

Conserve exatamente o plano F, a matriz G⁺, o fator ℓ, os mapas k,c,r e a forma simplética da seção 5 da nota principal. Substitua apenas

\[
B_t^+=\begin{pmatrix}0&\ell G^+\\\ell G^+&-tI\end{pmatrix}
\quad\hbox{por}\quad
B_0^+=\begin{pmatrix}0&\ell G^+\\\ell G^+&0\end{pmatrix}.
\tag{1.1}
\]

A alteração é h(u,u′)=t⟨cu,cu′⟩, uma forma real simétrica no plano real. Acrescentá-la igualmente aos sinais + e − conserva suas diferenças CCR. Como ck=0, conserva a Ward. Como c=0 no espaço físico fechado clássico, não modifica a covariância física. Se esse plano é realizado por dados suaves no sistema 068, h tem posto finito e kernel suave; sua evolução é uma bisolução suave. Nesse caso, Hadamard também é conservado.

Agora

\[
N_E=kN_G\oplus rN_G,
\qquad cN_E=N_G.
\tag{1.2}
\]

De fato, as duas equações para um radical (x,z) são Gz=0 e Gx=0. O vetor ry que antes fornecia a classe negativa tornou-se um vetor radical e desaparece da representação cíclica. A cohomologia do bloco auxiliar é zero. Se acrescentamos ortogonalmente o bloco físico A, então

\[
N_E=N_A\oplus kN_G\oplus rN_G,
\tag{1.3}
\]

e as duas saturações S1/S2 são satisfeitas. A cohomologia é precisamente H/N_A, com sua forma positiva anterior. Portanto o contraexemplo não constitui uma obstrução à existência de uma escolha adequada: o reparo do próprio bloco está explícito.

## 2. Critério algébrico que uma construção global pode realizar

Em qualquer decomposição simplética E=H⊕kF⊕rF que satisfaça as identidades de 068, a forma

\[
B_{\mathrm{can}}^+(u,u')
=A(pu,pu')+\ell G(qu,cu')+\ell G(cu,qu')
\tag{2.1}
\]

tem a matriz de (1.3), com C=0 e D_c=0. Aqui q é o extrator de gauge da decomposição; não é a carga BRST. O termo A pode ser escrito mediante a identificação simplética s:H→dados físicos de 067 como A₀₆₇(spu,spu′).

Se A e G realizam as CCR de suas parcelas, (2.1) realiza as CCR da soma simplética: o par kF,rF tem os únicos blocos ℓΩ_Q e H é ortogonal a ele. A Ward segue de qk=1 e ck=pk=0. Os radicais são exatamente (1.3), mesmo sem positividade de G no setor auxiliar. Logo a nota principal, seção 7, fornece P₀ na Fock algébrica desse W, com a mesma cohomologia física positiva.

Este cálculo não exige tornar a forma ghost estritamente positiva ou injetiva. Permite um radical ghost desde que sua imagem pelo levantamento r esteja também no radical bosônico. Isso paga diretamente S1, e C=0 paga S2.

**Contrato analítico indispensável:** a expressão (2.1) é Hadamard se a diferença para um par Hadamard de referência for suave, ou se for demonstrada diretamente sua orientação microlocal. A seção 3 da fonte 068 declara explicitamente que seu extrator inicial não é presumido preservador de frequência positiva; a seção 6 explica por que um projetor arbitrário de Cauchy não basta. Portanto não se promove (2.1), usando aquele extrator arbitrário, a uma construção Hadamard já demonstrada. Uma escolha de extratores compatíveis com os projetores de frequência módulo operadores suavizantes é uma rota concreta para pagar esse contrato adicional. A verificação dessa rota é independente deste adendo.

## 3. O que a alteração de D_c pode e não pode fazer

Na matriz geral da nota principal, S2 é

\[
\forall v\in N_A\quad C^*v\in\operatorname{Ran}G.
\tag{3.1}
\]

Ela não contém D_c. Assim nenhuma alteração apenas de D_c pode reparar uma falha de S2. O reparo finito da seção 1 funciona porque seu C já é zero. Se G for escolhido sem radical, S1 é automática, mas (3.1) continua necessária.

Uma mistura ghost com ocupações suavizantes pode tornar G injetivo e manter Hadamard. Isso, por si, não prova (3.1) em dados suaves: a inversa de ocupações que tendem rapidamente a zero pode amplificar sequências para fora de C∞. É preciso construir uma solução x na classe declarada ou modificar o bloco C de forma admissível. Não se troca essa obrigação por uma inversa formal.

O resultado aqui registrado é, portanto, construtivo e limitado: reparo completo do bloco finito; critério explícito para o bloco global; e identificação do requisito microlocal que separa os dois. Nenhuma mudança foi feita nos kernels, arquivos ou entregas anteriores.
