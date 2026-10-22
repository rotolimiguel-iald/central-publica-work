# Aciclicidade do CE linear de Weyl em todos os graus

10/09/2026. Investigação087 nova, separada da entrega086. Autor: selected_geometry_design. [DERIVED — demonstração escrita, aguardando revisão independente específica]. [KNOWN — importação finito-dimensional de Chevalley–Eilenberg indicada no §3]. Zero execução matemática, CAS ou Lean; nenhum um.py executado ou importado. Os registros de integridade são documentais.

No contrato fixado das investigações082–086, ponha N₁=Rher⊗ℝMcal. Então

\[
\boxed{(N_1\otimes\Lambda^p V_0^*)^{\mathfrak h}=0
\quad (0\leq p\leq4),\qquad
H^q\!\left(C^\bullet(\mathfrak g,N_1)^{\mathfrak h},d_{\rm CE}\right)=0
\quad\text{para todo inteiro }q.}                         \tag{1}
\]

O segundo resultado exige uma prova além da contagem de tipos horizontais: o complexo CE contém ghosts de isotropia e o termo de curvatura. A prova abaixo conserva ambos e termina em no máximo cinco eliminações horizontais. Sua consequência para o primeiro diferencial BRST é explicitada no §6. Não se calcula aqui o coeficiente quadrático N₂, os diferenciais superiores ou a cohomologia BRST total.

## 1. Categoria e entradas efetivamente utilizadas

A referência é uma espaço-forma Lorentziana orientada de dimensão quatro. K>0 e κ≠0 são números reais já fixados. O setor sigma foi projetado em φ₀ constante. Rher é o mesmo fator escalar real, unital, não nulo e inerte da085: a ação de g e o diferencial são triviais nele. Não se introduzem novos ghosts no anel, coeficientes tensoriais externos ou dependência espacial arbitrária. Elementos usam finitíssimos jatos; todos os produtos tensoriais desta nota são algébricos.

Use h=so(1,3), g=h⊕V₀, dim h=6 e dim V₀=4, com o par simétrico e a ação efetiva da [identificação082](<C:/IALD/Central de Patentes/Chatgpt/COMPLEXO_CE_QUADRATICO_082_20260910/IDENTIFICACAO_D1_CE_KILLING_E_JATOS_WEYL.md>), §§2–5. Mcal é o módulo LINEAR de classes gauge-fechadas de jatos métricos modulo todas as relações Einstein/Bianchi e prolongamentos. Ele não é presumido livre.

A entrada decisiva é a [prova de estriteza086](<C:/IALD/Central de Patentes/Chatgpt/SIMBOLO_DIVERGENCIA_TODAS_ORDENS_086_20260910/ESTRITEZA_E_DETECTOR_PRINCIPAL_DE_DIVERGENCIA.md>), §§2–3. A filtração F_jMcal é induzida do quociente dos jatos de h de ordem ≤j pelas EOM. Suas peças são h-finitas e ela é exaustiva e limitada inferiormente. A estriteza da imagem das EOM, demonstrada naquela fonte, fornece uma injeção h-equivariante

\[
\operatorname{gr}_{r+2}\mathcal M_{\mathbb C}
\ \hookrightarrow\ (r+4,r)\oplus(r,r+4),\qquad r\geq0,
\quad \operatorname{gr}_j\mathcal M=0\ (j<2).              \tag{2}
\]

Os pares são PESOS INTEIROS 2j de sl₂⊕sl₂; em particular V₀,ℂ=(1,1). O grau r+2 conta derivadas de h. K tem grau zero nessa filtração. O lado direito de(2) é o módulo plano maior; não se troca a injeção por uma igualdade nem se supõe que qualquer jato plano se levante a uma solução curva. A compatibilidade com a derivada foi provada086; aqui só a injeção de representações e a preservação finita da ação serão necessárias.

O resultado086 foi submetido a [revisão independente integral](<C:/IALD/Central de Patentes/Chatgpt/REVISAO_SIMBOLO_DIVERGENCIA_086_20260910_064135_2856684/PARECER_ESTRITEZA_E_DIVERGENCIA_086.md>). A presente aplicação linear ainda requer sua própria revisão. A [redução084](<C:/IALD/Central de Patentes/Chatgpt/REDUCAO_ISOTROPIA_CE_084_20260910/REDUCAO_FINITA_GHOSTS_E_CANAL_EULER.md>), §§1–2, fornece a decomposição vertical/horizontal no mesmo contrato; a [generalização085](<C:/IALD/Central de Patentes/Chatgpt/PRIMEIRA_PAGINA_TODOS_GRAUS_085_20260910/COHOMOLOGIA_S0_GERAL_E_INVARIANTES_POSITIVOS.md>), §§2–3, identifica o primeiro diferencial para qualquer grau polinomial m, incluindo m=1.

## 2. Ausência de formas horizontais lineares em todos os graus

Em dimensão quatro orientada, a decomposição complexa das formas é

| p | ΛᵖV₀,ℂ* |
|---|---|
| 0 | (0,0) |
| 1 | (1,1) |
| 2 | (2,0) ⊕ (0,2) |
| 3 | (1,1) |
| 4 | (0,0) |

A métrica e o volume dão as identificações duais da tabela. As representações finitas (a,b) são autoduais. Consequentemente, um tensor invariante em E⊗ΛᵖV₀* só aparece se E contiver um dos tipos da respectiva linha. Nenhum tipo (r+4,r) ou (r,r+4), r≥0, coincide com eles: a diferença entre os dois pesos tem módulo quatro, enquanto na tabela ela tem módulo zero ou dois. Logo

\[
\bigl(((r+4,r)\oplus(r,r+4))\otimes\Lambda^pV_{0,\mathbb C}^*\bigr)^{\mathfrak h_{\mathbb C}}=0.   \tag{3}
\]

Essa afirmação passa do graduado para o módulo CURVO sem hipótese de liberdade. De fato, suponha X∈(Mcal⊗ΛᵖV₀*)^h não nulo. Por finitude de X e exaustividade da filtração, existe um menor j com X∈F_j e X∉F_{j−1}. Seu símbolo é não nulo e h-invariante. Tensorizar(2) pelo espaço exterior finito injeta esse símbolo no espaço de(3), que não possui invariantes. Contradição. Para j<2 a peça graduada já é zero. A complexificação é fiel, portanto a conclusão retorna aos reais:

\[
B^p_{\mathbb R}:=(\mathcal M\otimes\Lambda^pV_0^*)^{\mathfrak h}=0
\qquad(0\leq p\leq4).                                    \tag{4}
\]

Isso inclui escalares, vetores e duas-formas lineares naturais no módulo efetivo. Não elimina curvaturas com quatro índices livres, observáveis com tensores externos ou a própria Mcal. Tampouco afirma que as COCADEIAS completas de CE sejam zero: os fatores Λʳh* podem fornecer os tipos adicionais. Por exemplo, a contração W_abcd pᵃpᵇθᶜᵈ e sua dual pertencem ao setor (p,r)=(2,1) tratado em [080](<C:/IALD/Central de Patentes/Chatgpt/GERACAO_WEYL_H3_E4_080_20260910/GERACAO_NATURAL_H3_E4_E_LIMITE_DOS_COEFICIENTES.md>). Seus candidatos não nulos são compatíveis com(4); a aciclicidade demonstrada abaixo diz algo sobre ciclos e fronteiras, não sobre inexistência de cocadeias.

## 3. Cada coluna vertical é acíclica, com primitivas h-invariantes finitas

Fixe p. E_p=Mcal⊗ΛᵖV₀* é localmente finito sob h. Uma quantidade finita de seus elementos está contida em um módulo h finito-dimensional, por exemplo a imagem de F_jMcal⊗ΛᵖV₀*. Por(4), esse módulo não tem componente trivial.

[KNOWN — contrato exato da importação] [Chevalley–Eilenberg1948, §23 e Teorema24.1, pp.115–119](https://www.sas.rochester.edu/mth/sites/doug-ravenel/otherpapers/chev-eilen.pdf) definem os coeficientes finito-dimensionais e provam nulidade em todos os graus para uma representação irredutível não trivial de uma álgebra semissimples em característica zero. Aplicamos isso SOMENTE à álgebra h e aos somandos finitos de E_p. A completa redutibilidade finita e a decomposição do complexo em somandos dão Hʳ(h,E)=0 para cada corte E sem invariantes. Em grau zero isso também segue diretamente de E^h=0.

É preciso preservar naturalidade. O diferencial vertical é h-equivariante e os espaços de cocadeias de um corte são finito-dimensionais. Se um ciclo h-invariante z admite uma primitiva a no corte, a aplicação sobrejetiva d₀:C^{r−1}(h,E)→im d₀ admite uma cisão h-equivariante por completa redutibilidade. Aplicar a cisão a z fornece uma primitiva h-invariante no MESMO corte. Não se faz média no grupo Lorentz não compacto, nem se exige uma primitiva sob a álgebra g inteira.

Como Λʳh é finito-dimensional, qualquer cocadeia com coeficientes em E_p tem todos os seus coeficientes em um desses cortes. Assim a união filtrante conserva a aciclicidade e as primitivas finitas. Com a convenção de shuffle da084,

\[
C^{p,r}_{\mathbb R}=(\mathcal M\otimes\Lambda^pV_0^*\otimes\Lambda^r\mathfrak h^*)^{\mathfrak h},
\qquad H^r(C^{p,\bullet}_{\mathbb R},d_0)=0
\quad\text{para todos }p,r.                              \tag{5}
\]

Não se invocou Whitehead ou completa redutibilidade para o módulo sob g: as transvecções podem elevar a ordem dos jatos e não preservar os cortes. Também não se apagou H³(h,ℝ): suas duas classes de Cartan e a classe de grau seis continuam existindo para coeficientes triviais. A fórmula084 é Bᵖ⊗Hʳ(h,ℝ), e aqui o fator Bᵖ é que se anula.

## 4. Eliminação finita com o termo de curvatura conservado

Use a decomposição da084

\[
d=d_0+d_{\rm hor}+d_{\rm curv},\qquad
\deg d_0=(0,1),\quad\deg d_{\rm hor}=(1,0),\quad
\deg d_{\rm curv}=(2,-1).                                \tag{6}
\]

O ghost horizontal é p e o ghost de isotropia θ é Mghost da082, com θ_ab=−m_ab. O último termo contém d_curv θ=Kpp♭. Os sinais e shuffles são herdados do MESMO dCE; em particular d²=0. Não se usa d_hor²=0 no espaço de cocadeias inteiro.

Seja Q um ciclo de grau total q≥0. Decomponha Q=ΣₚQ_{p,q−p}, com 0≤p≤4 e 0≤q−p≤6. Escolha o menor p com componente não nula. Todas as componentes de menor p são zero. A equação de grau (p,q−p+1) de dQ=0 reduz então a

\[
d_0Q_{p,q-p}=0.                                          \tag{7}
\]

Se r=q−p>0, (5) fornece R_{p,r−1}, finito e h-invariante, tal que d₀R=Q_{p,r}. Substitua Q por Q−dR usando o diferencial COMPLETO. Isso remove a componente de grau horizontal p; as parcelas adicionais têm graus horizontais p+1 ou p+2. Nenhuma componente inferior reaparece. O novo elemento continua ciclo por d²=0.

Se r=0, a mesma equação diz que Q_{p,0} é um elemento de H⁰ da coluna, sem fronteiras de grau negativo. Por(5), Q_{p,0}=0. Assim não existe um obstáculo residual horizontal nem a necessidade de uma primitiva com grau vertical −1.

Repita para os graus horizontais seguintes. Há somente cinco valores possíveis de p, de modo que o procedimento termina, deixando zero. A soma FINITA das primitivas escolhidas satisfaz

\[
Q=d\!\left(\sum R_{p,r-1}\right).                        \tag{8}
\]

Cada primitiva vertical está num corte h-finito; cada aplicação de d_hor aumenta a ordem no máximo finitamente, e d_curv é algébrico nos ghosts. Um número finito de passos mantém a ordem finita. Não é necessária uma cota uniforme de ordem para todos os Q. O grau q=0 foi incluído: a única condição é um ciclo de grau zero, necessariamente zero. Para q<0 ou q>dim g=10 o complexo é zero.

Isso demonstra a segunda igualdade de(1) sobre ℝ. Equivalentemente, a filtração horizontal de comprimento cinco tem E₁^{p,r}=0 em todas as posições; por ser uma filtração FINITA do complexo, ela não envolve lim¹ ou uma hipótese Mittag–Leffler. A prova direta(7–8) dispensa qualquer ambiguidade de convergência. Os canais de curvatura foram conservados em cada subtração; não se postula que toda classe de Cartan seja permanente.

## 5. Coeficientes herdados, inclusive nilpotentes

O operador e sua referência são fixados antes da extensão escalar. Rher pode ser uma álgebra real com divisores de zero ou nilpotentes. Nenhum desses elementos precisa ser separado por avaliação numérica.

Para justificar as passagens, todo elemento de Rher⊗E usa finitíssimos coeficientes aᵢ. Escolha uma base REAL do subespaço real por eles gerado e escreva o elemento nessa base. Como a ação de h e d não alteram os aᵢ, invariância, fechamento e a identidade da primitiva são verificadas coeficiente a coeficiente. Cada coeficiente admite as primitivas reais finitas anteriores. A sua soma tensorizada dá uma primitiva sobre Rher. De modo equivalente, os mapas reais exatos permanecem exatos ao tensorizar por um espaço vetorial sobre ℝ.

Isso prova tanto (N₁⊗ΛᵖV₀*)^h=Rher⊗Bᵖ_ℝ=0 quanto a aciclicidade CE em(1). Não se afirma exatidão de produtos completados em jatos, preservação automática de uma filtragem causal de contratermos ou validade em um anel que mantenha K variável. Uma subclasse adicional de pesos/analiticidade deve ser confrontada com as primitivas nela, em vez de ser herdada pelo nome Rher.

## 6. Consequência precisa para a primeira página BRST

A [generalização085](<C:/IALD/Central de Patentes/Chatgpt/PRIMEIRA_PAGINA_TODOS_GRAUS_085_20260910/COHOMOLOGIA_S0_GERAL_E_INVARIANTES_POSITIVOS.md>), equação(1) e §3, identifica

\[
D^q:=H^q(s_0)\big|_{E=q+1}
\ \simeq\ R_{\rm her}\otimes[\mathcal M\otimes\Lambda^qG]^{\mathfrak h},
\qquad (D^\bullet,d_1)\simeq C^\bullet(\mathfrak g,N_1)^{\mathfrak h}.   \tag{9}
\]

Aqui d₁ é o diferencial induzido por s₁ na cohomologia de s₀, não apenas o termo d_hor de(6). Ele aumenta E e q de um, preservando m=E−q=1. A identificação dos dez ghosts G com o lado CE e todos os sinais são os fixados082/085; não se cria um ghost Lorentz independente.

Portanto, para cada q,

\[
\ker\!\left(d_1:H^q(s_0)|_{E=q+1}\to H^{q+1}(s_0)|_{E=q+2}\right)
=\operatorname{im}\!\left(d_1:H^{q-1}(s_0)|_{E=q}\to H^q(s_0)|_{E=q+1}\right).    \tag{10}
\]

O termo de origem em q=0 é zero. A igualdade vale nos espaços naturais de jatos finitos, com primitivas finitas na cohomologia identificada; escolher representantes e correções s₀-exatas usa precisamente a comparação085 já estabelecida. Não são descartados termos s₂ em uma tentativa de levantamento na álgebra inteira.

(10) elimina TODO o setor linear m=1 da cohomologia do primeiro diferencial, em todos os números de ghost. Não afirma que cada Dᵠ seja zero. Não elimina o setor constante m=0, com suas classes de Cartan, nem o setor quadrático m=2. Também não identifica uma página intermediária com H(s₀+s₁+s₂+⋯), não estabelece limite inverso dos truncamentos, e não paga admissibilidade Q2, QME ou anomalia física.

## 7. Entrega e limites

[DERIVED] As novidades desta nota são a eliminação dos tipos horizontais lineares por(2–4), a aplicação vertical finita(5) e a aciclicidade total(7–10). A importação primária é estritamente finito-dimensional e foi conferida no texto original; a ação de g no módulo de jatos é consumida das fontes locais pinadas.

[OPEN — fora desta nota] O complexo com N₂ e graus polinomiais superiores; outros fundos sigma; jatos de ordem infinita por elemento; espectadores tensoriais; K como parâmetro variável ainda pertencente ao operador; admissibilidade causal das primitivas; diferenciais superiores, QME e UV. O resultado não é uma falsificação ou confirmação da TGL e não altera o seletor, o programa canônico ou seus gates.

[REAL — documental] O manifesto registra os arquivos efetivamente relidos e medidos antes/depois da emissão, os links locais e a primária consultada. A emissão usa somente leitura de bytes e escrita atômica de arquivos novos dentro de Chatgpt. Nenhum original, Atlas, memória canônica, fonte congelada, CAS ou Lean foi executado ou modificado. Os pareceres antecedentes citados não são apresentados como aprovação antecipada desta demonstração087.
