# Potência, ordem de derivadas e Mittag–Leffler no complexo causal/Rees

10/09/2026, etapa078, fora das entregas076/077. [DERIVED — demonstrações escritas] [KNOWN — referências primárias delimitadas] [REAL — medição documental]. Somente arquivos novos em Chatgpt; nenhum um.py, Lean ou CAS executado. Não se usa a revisão ainda em curso de077 como aprovação de seus resultados.

**Resultado.** A contagem de potência permite demonstrar uma cota de derivadas para o setor de contratermos gerado recursivamente pela ação inicial de duas derivadas, quando a normalização conserva essa cota. Ela não torna automaticamente finitos os grupos H²(C_N), H³(C_N) do complexo natural/Rees de076. Há cocadeias admissíveis nesse complexo com L, E e peso de engenharia fixos, mas ordem de jatos arbitrariamente alta. Mesmo uma redução a módulos finitos sobre coeficientes de fundo não bastaria para Mittag–Leffler: construímos uma torre explícita que refuta essa inferência. Nenhuma dessas observações prova que o sistema Einstein–sigma tenha lim¹ não nulo.

## 1. Três classes que as fontes efetivamente distinguem

As referências locais são:

1. [Q2_069, §§2–5](<C:/IALD/Central de Patentes/Chatgpt/CONSTRUCAO_INTERAGENTE_CAUSAL_069_20260909/PRODUTOS_TEMPORAIS_E_ANOMALIA_LOCAL.md>): produtos de todas as inserções locais permitidas, ação inicial de duas derivadas e contagem dos grafos.
2. [Admissibilidade072, §§3–5](<C:/IALD/Central de Patentes/Chatgpt/COMPARACAO_CAUSAL_FUNDOS_072_20260910/CONTRATO_ADMISSIBILIDADE_Q2.md>): cota da aplicação multilinear inteira, coeficientes de fundo, regularidade e acoplamentos dimensionais.
3. [Ward072, §§7–9](<C:/IALD/Central de Patentes/Chatgpt/COMPARACAO_CAUSAL_FUNDOS_072_20260910/TRANSPORTE_E_WARD_REFERENCIA.md>): grau externo de θ,ω, tadpoles e partes Laurent.
4. [Rees074, §§2–6](<C:/IALD/Central de Patentes/Chatgpt/COMPLETACAO_REES_BRST_074_20260910/COMPLETACAO_POR_LACOS_E_VALENCIA.md>): R_L=∏_E t^(E+2L−2)P_E, com jatos finitos em cada coeficiente, sem limite uniforme de ordem; peso de engenharia opcional quando preservado pelos operadores.
5. [Comparação076, §6](<C:/IALD/Central de Patentes/Chatgpt/MUDANCA_BASE_BRST_076_20260910_024632_6031800/MUDANCA_BASE_E_COMPLETACAO_H3_H4.md>): C_N=A_nat/F^(N+1), com corte de valência e todas as ordens finitas de jatos.
6. [Truncamentos077, §§1–2](<C:/IALD/Central de Patentes/Chatgpt/PRIMEIROS_TRUNCAMENTOS_BRST_077_20260910_030228_0972771/S0_KILLING_E_PRIMEIRA_TRANSICAO.md>), consumidos com o [adendo de sinal](<C:/IALD/Central de Patentes/Chatgpt/PRIMEIROS_TRUNCAMENTOS_BRST_077_20260910_030228_0972771/ADENDO_SINAL_KOSZUL_TATE_077.md>): os fantasmas têm jatos livres antes de dividir pelas fronteiras; o diferencial linear contém R₀ e H₀.

A primeira distinção é entre **inserção local admissível** e **contratermo admissível para entradas multilineares já fixadas**. Q2 contém operadores locais compostos de ordens diferenciais diferentes; cada conjunto de entradas tem sua própria cota. Não se pode acrescentar um operador de derivadas arbitrárias ao contratermo de uma aridade/entrada de baixa ordem só porque ele é uma inserção local válida em outro ponto da hierarquia.

A segunda é entre essa hierarquia causal e o complexo C_N efetivamente definido em076. C_N não fixa aridade, lista de inserções, grau dos acoplamentos nem uma cota uniforme de derivadas. A comparação de limite foi demonstrada para esse complexo, não para um subcomplexo finito ainda por construir. A identidade s a+d b=0 pode ser estudada nele, mas uma primitiva nele ainda precisa do contrato multilinear para corrigir Q2.

## 2. Cota real para os grafos gerados pela ação inicial

Conte por d_v o número total de derivadas de um vértice, incluindo derivadas distribuídas no fundo; curvatura conta como duas. Acoplamentos de peso positivo, como Λ, podem reduzir o número de derivadas necessário, mas não aumentam a cota seguinte. Para um grafo conectado com l laços topológicos e vértices já renormalizados de ordens de laço L_v, a fonte069 fornece

\[
 D_{\rm loc}\le 2+2l+\sum_v(d_v-2),\qquad
 L=l+\sum_v L_v.                                      \tag{1}
\]

Suponha que os vértices iniciais tenham d_v≤2 e que, em cada ordem já construída, a normalização escolhida conserve d_v≤2+2L_v. Substituir essas desigualdades em (1) dá

\[
 \boxed{D_{\rm loc}\le2+2L.}                           \tag{2}
\]

Isso é uma indução efetiva: a propriedade dos contratermos anteriores fornece a propriedade dos novos. A valência pode ser arbitrária, pois os vértices de g⁻¹, volume e Exp têm graus arbitrários nos campos, mas suas derivadas originais continuam de ordem dois. Inserções de potencial têm d_v=0 e apenas melhoram (1). A distribuição da ordem entre campos, coeficientes e derivadas da delta deve obedecer à mesma contagem; integrar por partes não apaga essa ordem.

Uma inserção marcada adicional de ordem d>2 acrescenta o excesso d−2 à contagem. Vários operadores EFT iniciais ou inserções arbitrárias exigem seus excessos na soma. Portanto (2) é uma cota para o setor gerado com as entradas especificadas e a normalização declarada. Não é a consequência isolada dos rótulos L,E para toda inserção da álgebra Q2.

[KNOWN] A liberdade de renormalização é uma hierarquia D_n sujeita às inserções, independência funcional, escala e ação por partes; é esse o alcance do Teorema2 e das equações256–259 de [Hollands, 0705.3340v4](https://arxiv.org/pdf/0705.3340v4). A fonte não identifica uma componente de peso de engenharia de todo o complexo BRST com o conjunto dos contratermos de entradas fixadas.

## 3. Engenharia e Rees não fornecem uma cota de jatos em C_N

Use a apresentação geométrica das fontes: [g]=[φ]=[h]=[ξ]=0, [∇]=1, [C]=−1, [κ]=−2, [Λ]=[c_sigma]=2 e [t]=0. A referência B0 é inerte. A contração das fibras abaixo é feita com g0 e com a métrica redonda do alvo; todas as expressões são naturais, sem um frame adicional.

### 3.1 Controle explícito em ghost dois e três

Defina o endomorfismo ímpar

\[
 M^\mu{}_\nu=g_0^{\mu\alpha}\bar\nabla_{[\alpha}C_{\nu]},
 \qquad \bar\Box=g_0^{\rho\sigma}\bar\nabla_\rho\bar\nabla_\sigma.
\]

A conexão em M é a induzida por g0. M tem uma perna e peso zero. Para m≥1, considere as zeroformas

\[
 b_m=\kappa^m\operatorname{tr}(M\bar\Box^m M),\qquad
 a_m=\kappa^m\operatorname{tr}((\bar\Box^m M)M^2).       \tag{3}
\]

b_m tem ghost2/E2; a_m tem ghost3/E3. Ambos têm peso de engenharia zero: as 2m derivadas extras são compensadas por κ^m. A maior ordem de jato de C é 2m+1. Para qualquer L≥1, t^(2+2L−2)b_m e t^(3+2L−2)a_m pertencem respectivamente às componentes E2 e E3 de R_L. O rótulo L não muda com m.

Essas expressões não são identicamente nulas por paridade. Para b_m, tome um gerador T de so(1,3) com tr(T²)≠0; jatos inferiores e superiores independentes dão ηζ tr(T²). Para a_m, use três geradores do subgrupo de rotações so(3) para os quais tr(T₁[T₂,T₃])≠0 e três coeficientes ímpares independentes. O produto M² contém o comutador dos dois geradores inferiores. O símbolo principal de □^m pode ser isolado numa direção não nula; seus jatos são independentes dos jatos de ordem inferior. Isso também prova independência linear das expressões com valores distintos de m como **cocadeias**, pelo maior jato presente em uma combinação finita.

Na truncagem mínima C₂, b_m é fechado; na C₃, a_m é fechado: sC=t C·∂C aumenta a valência e sB0=0. Isso NÃO prova que suas classes sejam independentes, nem que sejam não nulas em cohomologia. Fronteiras provenientes de h, ξ e seus jatos podem eliminá-las. Precisamente esse quociente precisa ser calculado; uma cota de cocadeias não o substitui.

A família (3) já refuta uma função universal r=r(L,E,peso) que limite a ordem de jatos em P_E/C_N tal como esses espaços foram definidos. São polinômios finitos nos jatos, regulares em todos os fundos admitidos e independentes do alvo, portanto também compatíveis com a naturalidade O(4). Não se usa inverso de dφ0, 1/Λ ou 1/κ. Cada membro individual é até polinomial em κ. Exigir analiticidade em κ=0 não elimina os membros; um limite no **grau** em κ é outra condição.

Não se afirma que (3) seja a anomalia real de Q2, nem que cada membro possa aparecer como contratermo de uma mesma aridade de baixa ordem. O contraexemplo tem o alcance exato dos alvos C_N utilizados na comparação076.

### 3.2 Inserções da própria hierarquia causal

Há um controle semelhante em ghost zero, que evita restringir artificialmente quais observáveis Q2 admite. Para m≥2, ponha

\[
 O_m=\kappa^{m-2}\,
 \gamma_{ab}(\phi_0)
 (\bar D_{(\mu_1}\cdots\bar D_{\mu_m)}\xi)^a
 (\bar D^{(\mu_1}\cdots\bar D^{\mu_m)}\xi)^b.            \tag{4}
\]

O_m é real, natural, quadrático nas flutuações e tem peso quatro. Com volume tem peso total zero. O operador usa apenas o fibrado pullback da referência e a conexão redonda, globalmente definidos. Cada m dá um operador composto local de ordem finita, admitido como inserção pelo contrato Q2; seu produto de Wick e produtos temporais usam a cota correspondente a essa inserção. O maior jato cresce com m mesmo com valência e peso fixos. Uma potência formal de ħ/t pode apenas registrar em qual componente se está discutindo a inserção; isso não afirma que ela tenha sido gerada pela ação inicial naquele laço.

Um rótulo de inserção que inclua m permite uma cota. Os três números L,E,peso isolados não o recuperam, porque a potência dimensional de κ foi descartada desses rótulos. Esta é a diferença concreta entre finitude a uma ordem **e truncagem de operadores especificadas** e finitude da união de todas as inserções.

### 3.3 Coeficientes espectadores

O mesmo fenômeno já aparece nos coeficientes permitidos de B0: se Q0=g0^μνγ_ab(φ0)∂μφ0^a∂νφ0^b, então x=κQ0 é um escalar natural inerte de peso zero. x^m tem E0 e peso zero para todo m. Não requer derivadas de ordem maior que um, mas seu número total de fatores derivados cresce sem limite. Assim um limite na maior ordem de jato, sozinho, tampouco limita a dimensão do espaço de polinômios de fundo.

Quando a classe admite dependência C∞ nesses invariantes, a situação é de um módulo sobre um anel de coeficientes, não automaticamente de um espaço vetorial real finito. Mesmo sob uma exigência analítica, os polinômios x^m continuam existindo. A cota multilinear pode excluir muitos desses coeficientes para entradas específicas; essa exclusão não foi imposta na definição de todo C_N.

[KNOWN] A prova do Teorema6.2 de [Khavkine–Melati–Moretti, 1710.01937](https://arxiv.org/pdf/1710.01937), em sua equação de pesos e passo4, obtém ordem global finita usando a admissibilidade s_j+l_j≥0 e os pesos positivos crescentes dos jatos. Coeficientes marginais conservam dependência suave. Uma coleção ampliada com κ escalar de peso negativo não satisfaz automaticamente essa hipótese. O teorema trata potências de Wick; não é importado aqui como classificação de toda a hierarquia BV do multiplet.

## 4. Quais cortes os diferenciais preservam

**Laços no BRST clássico.** A fonte074 demonstra (R_L,R_M)⊂R_(L+M). Como S_cl∈R₀, s_cl=(S_cl,·) preserva cada L. A translação b=t⁻¹B também preserva L, pois retira simultaneamente uma perna e uma potência de t. A conjugação e^b conserva essa graduação. Logo seria incorreto atribuir uma falha do corte em L a esses operadores clássicos.

**Potência isolada de t.** b pode diminuir essa potência; o controle é Rees, não truncagem ingênua apenas em t. A fórmula coeficiente a coeficiente de074 requer no máximo quatro graus adicionais de valência. Ela não cria uma cota de derivadas que não existia.

**Derivadas brutas.** O espaço de polinômios com no máximo D derivadas não é em geral um subcomplexo. Já s₀h=2∇̄_(μC_ν) aumenta o número de derivadas; em ∂^D h produz jatos de ordem D+1. A parte KT corrigida s₀u*=+H₀u contém duas derivadas físicas. Preservação do peso total é possível porque os geradores têm pesos diferentes. Projetar fora as derivadas que ultrapassam D sem provar um ideal/subcomplexo estável não define o mesmo H(s).

**Normalizações quânticas.** Se S_eff=Σ_{r≥0}ħ^r S_r, o antibracket com S_r envia a ordem L à ordem L+r. Uma normalização finita quântica ou uma transformação canônica com gerador de laço positivo pode misturar as componentes individuais. Quando há apenas potências não negativas, o quociente módulo ħ^(K+1) é estável; o subespaço de polinômios de grau≤K, sem projeção, não precisa ser estável. No cálculo da primeira quebra usa-se o diferencial clássico, para o qual a preservação de L acima permanece válida. Não se identifica normalização quântica arbitrária com a conjugação clássica e^b.

**Fontes θ,ω.** d_θ troca θ por ω e conserva o grau externo total, com prolongamentos. Na Ward072, fixar esse grau k limita os vértices de tadpole e de variação quadrática; as partes negativas em t são finitas nessa graduação. Um corte apenas em L, deixando k e todas as inserções livres, não fornece a finitude combinatória demonstrada na fonte. Derivadas das fontes entram por Leibniz e não são constantes descartáveis. Retrações que substituem fontes por campos/fantasmas exigem seu transporte de multigrau; o argumento mínimo sem fontes não as recategoriza. Nenhuma falha nova de uma identidade já demonstrada em072 é afirmada aqui.

## 5. O que bastaria para finitude, e o que ainda precisaria ser provado

Há um critério elementar de dimensão finita: a E≤N, limitar os geradores de jatos disponíveis e seus graus, e restringir os coeficientes a um espaço vetorial real finito, produz espaços finitos de cocadeias. Se esses espaços forem complexos estáveis e formarem a mesma torre em discussão, cada H^g é finito. Para um N fixo, as imagens

\[
 \operatorname{im}(H^g(C_{N+k})\to H^g(C_N))
\]

formam uma cadeia decrescente de subespaços de um espaço finito e estabilizam. Isso é a condição Mittag–Leffler. Não exige que todas as transições sejam sobrejetivas desde o começo.

Uma contagem útil mostra quais dados faltam. Na apresentação mínima, [u*]=4 e [C*]=5. Para um monômio de peso w, suponha potência de κ limitada superiormente por P, potências não negativas de Λ e c_sigma e nenhuma outra fonte de peso negativo não controlada. Denotando por D o número total de derivadas, a equação de pesos dá

\[
 D+2n_\Lambda+2n_\sigma+4n_{u^*}+5n_{C^*}
       -n_C-2p_\kappa=w,
 \qquad D\le w+N+2P.                                 \tag{5}
\]

Com número finito de espécies e E≤N, (5) limita os jatos diferenciados. Mas ainda é preciso controlar os coeficientes de peso zero, regularidade/globalidade, logaritmos de escala, possíveis acoplamentos adicionais e estabilidade dos operadores nessa mesma restrição. Um limite de P não foi deduzido de L para todas as cocadeias, como (3) demonstra. Normalização canônica dos campos pode reorganizar potências de κ; não basta mudar sua dimensão nominal.

Fixar numericamente todos os jatos de B0 pode converter certos coeficientes em números. Isso é uma análise de fibra. Ela não demonstra uma primitiva natural regular em todos os fundos, nem comuta automaticamente com tomar cohomologia. A seção seguinte mostra que até uma torre de módulos livres de posto um, com todas as fibras finitas, pode falhar em Mittag–Leffler sobre o anel dos coeficientes.

## 6. Contraexemplo calculado: finito sobre coeficientes não implica ML

Esta é uma torre algébrica auxiliar, não o diferencial Einstein–sigma. Ela testa precisamente a inferência que se pretendia usar. Seja A=ℝ[x] ou o anel de germes C∞ em x=0; o diferencial não atua em x. Para N≥0, tome o complexo concentrado nos graus dois e três

\[
 D_N^2=A^{N+1},\quad D_N^3=A^N,\quad
 (d_Na)_i=a_i-xa_{i+1},\quad 0\le i<N.                \tag{6}
\]

Os mapas D_(N+1)→D_N retiram o último componente em ambos os graus. São sobrejetivos nas cocadeias e comutam com d, pois as primeiras N equações permanecem as mesmas. Todos os operadores são de ordem zero e todos os módulos de cocadeias são finitos livres.

d_N é sobrejetivo: ponha a_N=0 e resolva a_i=b_i+xa_(i+1) de trás para frente. Seu núcleo é

\[
 a=(x^N r,x^{N-1}r,\ldots,xr,r),\quad r\in A.
\]

Logo H²(D_N)≃A e H³(D_N)=0. Sob essa identificação pelo último componente, a transição H²(D_(N+1))→H²(D_N) é multiplicação por x. As imagens no alvo fixado são

\[
 A\supset xA\supset x^2A\supset\cdots,                \tag{7}
\]

e são estritamente decrescentes. Em ℝ[x] isso segue pelo grau/ordem de anulação. Para germes suaves, x^m=x^(m+1)f exigiria f=1/x fora de zero, impossível para f suave em zero. A torre, portanto, não é ML, apesar da finitude de posto e da sobrejetividade de cocadeias. Em cada fibra numérica x=a, a transição é um isomorfismo se a≠0 e é zero se a=0; em ambos os casos a torre de fibras é ML.

O controle ainda permite calcular um lim¹ não trivial no caso **polinomial**. Para a torre ℝ[x] --x← ℝ[x] --x←⋯, considere

\[
 (y_N)\longmapsto\sum_{N\ge0}x^Ny_N
       \pmod{\mathbb R[x]}.                                  \tag{8}
\]

A série é bem definida formalmente. Em uma sequência y_N=a_N−xa_(N+1), a soma telescopa para a₀, portanto (8) anula a imagem de Δ. É sobrejetiva, escolhendo y_N como os coeficientes constantes de uma série arbitrária. Se a soma de (8) é um polinômio P, a fórmula

\[
 a_N=x^{-N}\left(P-\sum_{j<N}x^j y_j\right)
\]

define um polinômio: o numerador é divisível por x^N pela igualdade das séries. Isso mostra que o núcleo de (8) é exatamente imΔ. Consequentemente,

\[
 \operatorname{lim}^{1}H^2(D_N)
       \simeq \mathbb R[[x]]/\mathbb R[x]\ne0.                        \tag{9}
\]

Na fórmula (9), o anel de coeficientes é A=ℝ[x]. Não se transporta (9) sem prova ao anel suave: a não estabilização de (7) continua, mas lim¹ pode mudar ao ampliar coeficientes. Também não se transporta (9) ao BRST real.

O papel físico de x aqui é apenas ilustrar um coeficiente espectador regular e inerte, como um escalar adimensional de B0. A álgebra do exemplo é polinomial e de ordem zero, portanto não depende de coeficientes patológicos ou inversos singulares. Não é necessário identificar sua matriz bidiagonal com a Hessiana gravitacional para refutar a inferência geral “posto finito sobre coeficientes ⇒ ML”.

## 7. Consequência delimitada para078

[DERIVED] A cota (2) paga uma parte concreta da finitude diagramática na normalização recursiva indicada. As famílias (3) mostram que engenharia, laços e valência não limitam os jatos de todo C_N; (4) mostra por que a união das inserções Q2 também não possui essa cota sem o rótulo da inserção. O exemplo (6)–(9) mostra que substituir dimensão real finita por geração finita sobre espectadores não paga ML, nem mesmo com transições sobrejetivas de cocadeias e fibras finitas.

[OPEN] Para concluir ML no modelo ainda é necessário calcular/controlar as imagens cohomológicas da torre efetiva, ou construir uma substituição por complexos realmente finitos com comparação demonstrada, regular em B0 e compatível com a hierarquia Q2. Um setor diagramático com d≤2+2L pode ser parte desse trabalho, mas sua estabilidade BRST, suas primitivas e sua comparação com C_N não vieram da contagem de grafos. Esta nota não prova que H²(C_N) ou H³(C_N) sejam infinitos, que ML falhe no Einstein–sigma ou que exista anomalia irremovível.

Nenhuma conclusão nova sobre QME, carga, positividade interagente, reconstrução geral ou UV é tomada. A entrega077 e os originais permanecem intactos; o manifesto registra os pins documentais da presente etapa078.
