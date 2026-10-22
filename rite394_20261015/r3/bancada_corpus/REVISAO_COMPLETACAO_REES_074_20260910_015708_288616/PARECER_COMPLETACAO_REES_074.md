# Parecer independente — completação por laços e valência074

10/09/2026. [DERIVED — revisão matemática escrita e delimitada]. [REAL — medições documentais por bytes]. Não identifiquei erro material no teorema condicionado da nota examinada. Este parecer não constitui uma nova demonstração Lean, teste CAS ou validação independente da construção geométrica do operador b_N.

## 1. Fonte, leitura e conclusão

Fonte integralmente lida: [Completação por laços e valência](<C:/IALD/Central de Patentes/Chatgpt/COMPLETACAO_REES_BRST_074_20260910/COMPLETACAO_POR_LACOS_E_VALENCIA.md>), 11945 bytes, SHA-256 68855257cf07817eb12e0262ae0f9e0a560d2ff669c8ff95107fad22be75f3da. Também li integralmente Q2_069 e o Contrato de admissibilidade Q2_072, nos caminhos pinados no recibo. O manifesto foi lido para verificar suas entradas. Os outros dois documentos históricos listados pelo manifesto foram medidos para custódia; esta revisão não reabre seus teoremas.

**Parecer favorável no alcance declarado:** a translação b=t⁻¹B preserva a completação R_L, tem exponencial finita e inversível, e não produz expoentes negativos de t para L≥1. A derivada horizontal preserva a mesma organização. O antibracket canônico normalizado soma os rótulos de laço. O controle de peso depende da homogeneidade dos coeficientes do operador, como a fonte explicita.

A conclusão é condicional à pertença da entrada a R_L e às propriedades de B. Não se afirma que toda série Laurent da teoria estendida tenha essa forma, nem que toda liberdade de renormalização já esteja contemplada por ela.

## 2. Verificações algébricas

Para o grafo conectado, Σ_v n_v=E+2I e l=I−V+1 dão
\[
 \sum_v(n_v+2L_v-2)=E+2\left(l+\sum_vL_v\right)-2.
\]
Anticampos entram como pernas externas mesmo sem propagador. Vértices de contratermo são abrangidos quando já respeitam o mesmo rótulo. Esta igualdade não é cálculo de um coeficiente de diagrama.

Como B retira exatamente um fator ghost normalizado e insere uma 1-forma de fundo, B:P_E^q→P_{E−1}^{q+1}; coeficientes, formas e demais geradores não criam pernas. Logo b baixa também a potência de t em uma unidade e conserva E+2L−2 em sua relação com o novo grau E−1.

Em dimensão quatro b⁵=0. Para o grau de saída E e forma q:
\[
 (e^{\pm b}F)_E^q
 =\sum_{j=0}^{q}\frac{(\pm1)^j}{j!}B^j F_{E+j}^{q-j}.
\]
São no máximo cinco entradas. Cada uma tem um número finito de monômios e jatos; a ação local de B em cada jato conserva essa finitude. Não se exige um limite uniforme na ordem dos jatos para todos os E. Trata-se de continuidade formal por coeficientes, sem convergência analítica da série de campos.

As exponenciais são inversas porque são polinômios no mesmo operador nilpotente e e^b e^−b=Id. O número de laços L não muda. Para L≥1, o menor expoente possível na saída é 2L−2≥0. O exemplo t⁰C fora de R_1 e tC dentro de R_1 distingue corretamente o teorema de uma afirmação sobre todas as séries positivas.

No antibracket canônico, cada derivada funcional retira uma perna. Derivadas totais dos operadores de Euler preservam o grau nos jatos de flutuação. Para saída E, somente E_1+E_2=E+2 com E_1,E_2≥1 contribuem: são E+1 pares, todos finitos. O expoente é E+2(L+M)−2. Termos de grau zero têm antibracket nulo. Portanto (R_L,R_M)⊂R_{L+M} no domínio em que o antibracket variacional está definido; a ação S_t∈R_0 gera um diferencial preservando R_L. A nilpotência ainda consome a CME, não decorre da graduação.

## 3. Precisão aditiva: escala simplética e sigma

As convenções da seção2 são suficientes; registro a identidade explícita para evitar um fator t duplicado. Seja f_t(X) a mudança dos campos completos e
\[
 A_t=t^{-1}D_X f_t.
\]
No sigma, f_t(ξ)=Exp_{B_0}(tξ), com A_0=Id. O lift reescalado dos anticampos é p=t A_t^{-T}X^*, com B0 fixo. Então a forma de Liouville satisfaz
\[
 \Psi_t^*(p\,d f_t)=t^2X^*dX,\qquad
 \Psi_t^*\omega_{\rm BV}=t^2\omega_{\rm can}.
\]
O d desta fórmula é o diferencial no espaço dos campos/anticampos, com referência fixa; não é a derivada horizontal d_H. Para variáveis ímpares, usa-se o lift cotangente graduado com as mesmas convenções de antibracket. A identidade tensorial permanece.

Consequentemente,
\[
 (F\circ\Psi_t,G\circ\Psi_t)_{\rm can}
 =t^2(F,G)_{\rm BV}\circ\Psi_t.
\]
Assim S_t=t^−2 S∘Ψ_t gera o diferencial transportado sem outro fator t^−2 no antibracket canônico normalizado. Colocar esse fator adicional duplicaria a escala. O lift do sigma requer o inverso transposto do Jacobiano normalizado; não é a mera multiplicação de suas componentes de anticampo por t.

Estas identidades podem ser verificadas no espaço formal com t invertido; a afirmação principal da nota mostra depois a preservação dos setores R_L≥1 sem expoentes negativos. Não é necessária uma avaliação t≠0 ou uma inversão numérica. Na vizinhança formal da seção zero, A_t=Id+O(t) tem inversa formal cujos coeficientes são finitos em cada ordem.

## 4. Precisões aditivas: álgebra e truncagem

Os “automorfismos” da seção4 são isomorfismos lineares inversos do espaço total de formas e valências, preservando L e o grau total ghost+forma. Não se deve entendê-los como a afirmação de que cada R_L seja uma álgebra sob produto ordinário. Na graduação ambiente:
\[
 R_L R_M\subset R_{L+M-1}.
\]
Se os índices admitidos forem somente L≥0, esse produto pode inclusive sair da soma desses setores quando L=M=0. Isso não interfere na conjugação linear de complexos ou no fechamento do antibracket indicado. A operação exponencial é uma automorfia da álgebra ambiente quando esta é escolhida fechada para o produto; essa escolha adicional não é necessária ao teorema.

A perda t-ádica máxima é quatro. Para calcular a saída até t^N, basta conhecer a entrada até t^{N+4}; uma contribuição inicialmente em N+4 pode chegar a N. Portanto truncar antecipadamente em N não é uma operação que, em geral, comute com e^b. A fórmula componente a componente dá uma margem menor quando graus de forma ou de ghost excluem alguns j. A fonte já anuncia a perda limitada; esta é sua regra operacional explícita.

## 5. Peso, regularidade e limites de consumo

Com t adimensional, [c]=−1, [dx]=−1 e [∇]=1, um jato ∇^r c tem peso r−1. Sob a hipótese da seção6, sua imagem é dx multiplicado por um coeficiente de fundo de peso r, portanto tem o mesmo peso. Se B comuta com o operador de escala e seus coeficientes são homogêneos, também preserva cadeias finitas de quase homogeneidade/logaritmos. Suavidade ou analiticidade são conservadas apenas na classe efetivamente preservada pelos coeficientes e operações de B.

Esse argumento é próprio do operador e da graduação declarados. Ele não verifica aqui, pelo nome b_N, a naturalidade de todos os jatos normais ou as identidades de seus comutadores. Tampouco transforma a conjugação numa homotopia contrátil.

Ficam expressamente fora da conclusão: aciclicidade natural; construção da primitiva da anomalia; preservação de R_L pelos demais homotópicos; limites de escala de cada aridade; independência funcional, inserções, contatos e T9/T11 da aplicação multilinear inteira; compatibilidade de fontes de outros pesos; remoção da anomalia, P2, QME e fechamento UV. A existência de P0_073 não foi reexaminada.

## 6. Custódia e estatuto da revisão

O recibo mede fonte, manifesto e seus quatro antecedentes por leitura de bytes e verifica que permaneceram idênticos durante esta revisão. Nenhum desses arquivos foi editado. Só este parecer e seu recibo foram criados em pasta nova. Não se executaram um.py, CAS, Lean, finalizadores ou programas dos documentos examinados.

Os checks automáticos do recibo são documentais. O parecer algébrico é a análise escrita desta revisão, não uma prova automatizada nem uma aprovação atribuída a terceiro. O estatuto inicial INDEPENDENT_REVIEW_PENDING do manifesto de origem é histórico; a presente revisão está registrada separadamente e não o altera.
