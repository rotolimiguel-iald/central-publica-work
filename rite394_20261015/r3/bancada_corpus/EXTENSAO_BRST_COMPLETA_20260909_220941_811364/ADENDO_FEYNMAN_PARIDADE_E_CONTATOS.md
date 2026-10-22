# Adendo: propagador de Feynman BRST, paridade e convenção fixa

09/09/2026. **[DERIVED + KNOWN — prova escrita; não Lean.]**
Este adendo complementa [a extensão BRST](./EXTENSAO_BRST_E_CORRECOES_SUAVES.md).
Nenhum arquivo anterior é alterado. A ação, o fundo e os domínios são os mesmos.

## 1. Fixar ε sem uma escolha silenciosa de sinal

Use \(E=G^{\mathrm{ret}}-G^{\mathrm{adv}}\).
A Hessiana de um modo físico canônico da ação 067 é
\[
P_u=-(\partial_\eta^2+\omega(\eta)^2).
\]
No caso constante,
\[
E_u(\eta,\eta')=-\frac{\sin\omega(\eta-\eta')}{\omega}.
\]
Com a ordem de campos determinada pelos modos 067,
\[
W_u^+(\eta,\eta')=
\frac{\hbar e^{-i\omega(\eta-\eta')}}{2\omega},\qquad
W_u^-=\overline{W_u^+},
\]
temos
\[
W_u^+-W_u^-=-i\hbar\frac{\sin\omega(\eta-\eta')}{\omega}
=i\hbar E_u.
\]
A identidade de Wronskiano transporta exatamente essa normalização ao caso
dependente do tempo e à reconstrução simplética 067. Portanto a escolha
deste adendo é
\[
\boxed{\epsilon=i\hbar,\qquad W^+-W^-=i\hbar E.}
\tag{1.1}
\]
Ela vale para D e Q na extensão BRST, com a mesma convenção causal.

As referências que escrevem \(i^{-1}E\), com ℏ=1, usam a convenção oposta
para a etiqueta da covariância/ordem dos campos ou para E. Ao usar seus
projetores iniciais, as etiquetas são convertidas para (1.1). Não se
troca a orientação microlocal apenas por conservar o nome “+”:
aqui W⁺ acompanha \(e^{-ip\eta}\), como em 067.

## 2. A matriz de paridade nos blocos permitidos

Na ordem \((u,b,c,\bar c)\), defina
\[
Z=\mathrm{diag}(1_V,1_W,-1_W,-1_W).
\]
As covariâncias da nota principal só ligam graus opostos. Por isso Z,
agindo na esquerda, implementa nessas entradas a paridade
\((-1)^{\mathrm{gh}_i\mathrm{gh}_j}\) da CCR/CAR graduada. Em particular,
Z troca o sinal dos dois blocos ghost e deixa os bosônicos fixos.
A relação completa é
\[
\boxed{\Lambda_L^+-Z\Lambda_L^-=i\hbar E_L.}
\tag{2.1}
\]
Não se trata de uma diferença bosônica comum no setor ghost.

Como o próprio L preserva a separação de paridade,
\(LZ=ZL\). Assim \(Z\Lambda_L^-\) é também uma bisolução de L.
Além disso \(\gamma Z=-Z\gamma\) nos blocos relevantes. A identidade
do setor menos, \(\gamma\Lambda_L^-=-\Lambda_L^-\gamma^*\), implica
\[
\gamma(Z\Lambda_L^-)=(Z\Lambda_L^-)\gamma^*.
\tag{2.2}
\]
O sinal menos em (2.2) antes da multiplicação por Z é exatamente o que
decorre das matrizes (7.1) da nota principal.

## 3. Definição e inversão exata

Ponha
\[
\boxed{
G_L^F=G_L^{\mathrm{ret}}-\frac{i}{\hbar}Z\Lambda_L^-
     =G_L^{\mathrm{adv}}-\frac{i}{\hbar}\Lambda_L^+ .
}
\tag{3.1}
\]
A igualdade entre as expressões é (2.1). Como a parcela de covariância
é bisolução,
\[
LG_L^F=G_L^FL=1
\tag{3.2}
\]
sobre testes suaves compactos. Esses sinais não são deduzidos de analogia
com um propagador escalar de outra assinatura: (1.1) e a Hessiana física
fixam a normalização.

Para explicitar todos os blocos, defina
\[
G_D^F=G_D^{\mathrm{ret}}-\frac{i}{\hbar}W_D^-,
\qquad
G_Q^F=G_Q^{\mathrm{ret}}-\frac{i}{\hbar}W_Q^- .
\]
Então
\[
\boxed{
G_L^F=
\begin{pmatrix}
G_D^F&KG_Q^F&0&0\\
G_Q^FK^*&0&0&0\\
0&0&0&G_Q^F\\
0&0&G_Q^F&0
\end{pmatrix}.}
\tag{3.3}
\]
Os blocos ghost têm esse sinal porque as entradas ghost de
\(\Lambda_L^-\) já são \(-W_Q^-\), e Z as troca de volta.
Ignorar uma dessas duas trocas daria o propagador errado.

As Ward completas, incluindo seus termos de contato, são
\[
\ell CG_D^F=G_Q^FK^*,\qquad
\ell G_D^FC^*=KG_Q^F,\qquad QG_Q^F=G_Q^FQ=1,
\]
\[
\mathcal HG_D^F=1-C^*G_Q^FK^* .
\tag{3.4}
\]
Por multiplicação de blocos, elas reproduzem (3.2).
Também
\[
\gamma G_L^F=G_L^F\gamma^* .
\tag{3.5}
\]
A identidade segue de (2.2) e da identidade correspondente aos Green,
ou diretamente de (3.3). Não foi afirmada uma Ward interagente renormalizada.

## 4. Relação com ordenação temporal e frente de onda

Em regiões de tempos estritamente ordenados, o kernel graduado ordenado
no tempo é
\[
\mathcal T_L(X,Y)=
\Theta(\eta_X-\eta_Y)\Lambda_L^+(X,Y)
+\Theta(\eta_Y-\eta_X)(Z\Lambda_L^-)(X,Y).
\tag{4.1}
\]
A paridade Z é a troca de sinal ao inverter dois campos ghost.
De \(E_L=G_L^{\mathrm{ret}}-G_L^{\mathrm{adv}}\),
\(\Theta(\eta_X-\eta_Y)E_L=G_L^{\mathrm{ret}}\) na interpretação
distribucional com os Green já fixados, e (2.1), resulta
\[
\boxed{\mathcal T_L=i\hbar G_L^F.}
\tag{4.2}
\]
A definição global segura é (3.1); ela fixa também o contato na diagonal,
em vez de escolher separadamente um valor de Θ(0). As entradas mistas
envolvem derivadas K; seus contatos são os de (3.3)–(3.4).

Com a convenção de fase de 067, fora da diagonal a frente de onda de
\(G_L^F\) acompanha a relação nula com covariável temporal negativa na
primeira entrada quando \(\eta_X>\eta_Y\), e positiva quando
\(\eta_X<\eta_Y\). Na diagonal inclui-se a relação conormal exigida
por \(LG_L^F=1\). Mais precisamente, em notação de frente primada:
\[
\mathrm{WF}'(G_L^F)\subset
\Delta^*\ \cup\
\{(X,k;Y,k'):(X,k)\sim(Y,k'),\
 [\eta_X>\eta_Y,\ k_\eta<0]\ \text{ou}\
 [\eta_X<\eta_Y,\ k_\eta>0]\}.
\tag{4.3}
\]
Isso é a condição Feynman na orientação aqui fixada. Derivadas por K/K*
e a paridade não criam relações canônicas adicionais.
A inclusão e a inversão exata fazem de \(G_L^F\) um inverso Feynman,
não apenas de uma bisolução física um propagador por mudança de nome.

A separação entre função de duas pontas Hadamard e inverso Feynman é
compatível com a construção por dados de Cauchy usada em
[Gérard–Murro–Wrochna, §5.2](https://link.springer.com/article/10.1007/s00023-025-01539-1);
as fórmulas de paridade seguem das convenções matriciais
[Wrochna–Zahn, (3.23) e §3.2](https://arxiv.org/html/1407.8079v2).
As identidades (1.1)–(4.3) foram deduzidas aqui para os operadores concretos.

## 5. O requisito pago e o que não se segue

**[DERIVED + KNOWN]** Está fornecido o propagador livre de gauge, auxiliar
e ghost, com inversão completa, normalização e Ward lineares compatíveis.
Esse é o dado de contração/ordenação temporal quadrática para a construção
perturbativa.

**[OPEN]** Esta nota não constrói produtos ordenados no tempo de ordens
superiores nas diagonais, não escolhe contra-termos e não prova a identidade
mestra quântica da interação. Ter um inverso Feynman não elimina essas
obrigações. Também não acrescenta um teorema de convergência da série
perturbativa, estabilidade não linear, UV ou seleção observacional do estado.

Não houve execução/importação de um.py, alteração das fontes anteriores
ou nova prova Lean neste adendo.
