# Parecer independente — potência, jatos e Mittag–Leffler078

[DERIVED — revisão matemática escrita] Li integralmente a versão final da nota e seu manifesto. Conferi a álgebra da torre, as famílias de cocadeias e os pesos, bem como as definições de Q2/Rees/C_N nas fontes locais pertinentes. Consultei os pontos primários de Hollands e de Khavkine–Melati–Moretti citados abaixo.

**Parecer favorável ao núcleo matemático, com uma precisão pontual obrigatória de domínio na frase sobre fibras do §6.** Não identifiquei erro na cota condicional de derivadas, no contraexemplo à cota universal de jatos, na não-ML da torre auxiliar ou na fórmula de lim¹ sobre ℝ[x]. A frase “cada fibra numérica x=a” aplica-se ao anel polinomial; para germes suaves em zero, só a avaliação em zero é canônica. A precisão não muda os resultados centrais.

## 1. Indução da cota de derivadas

A identidade de grafos conectados é 4l−2I+Σd_v=2+2l+Σ(d_v−2), usando l=I−V+1. Para vértices já construídos que obedecem d_v≤2+2L_v, sua substituição dá imediatamente D_loc≤2+2l+2ΣL_v=2+2L. Não falta contribuição do número de vértices.

A leitura indutiva requer os vértices de ordens anteriores e a hipótese explícita de que as normalizações finitas conservam a cota. O grafo degenerado constituído apenas de um contratermo de ordem L, sem linha interna, não demonstra a cota desse próprio contratermo: repete a hipótese sobre ele. Isso é evitado pela expressão “vértices já renormalizados” da nota. O novo contratermo é limitado pela divergência dos grafos das ordens já disponíveis e pela normalização admitida. Não se infere esse limite de uma liberdade finita arbitrária.

É correta a distinção entre o setor gerado por vértices iniciais de até duas derivadas e uma inserção marcada de ordem d>2: esta acrescenta d−2 à soma. Derivadas nos fundos e nas deltas contam; integração por partes apenas as redistribui. Valência arbitrária da expansão de g⁻¹/Exp não aumenta o número de derivadas originais.

A cota é diagramática e condicional à normalização, não uma prova de estabilidade BRST do espaço de polinômios com corte bruto de derivadas. Tampouco prova admissibilidade simultânea de todos os contatos da hierarquia.

## 2. Famílias b_m e a_m

Em (3), M tem um ghost, uma perna e peso zero. □̄^m acrescenta 2m derivadas e κ^m peso −2m. Logo:

- b_m=κ^m tr(M□̄^mM) tem ghost2, E2 e peso zero;
- a_m=κ^m tr((□̄^mM)M²) tem ghost3, E3 e peso zero;
- o maior jato de C tem ordem 2m+1, enquanto L pode permanecer fixo na classe Rees indicada.

A não nulidade foi conferida sem cálculo computacional. Para b_m, os jatos de primeira ordem podem dar ηT e os de ordem 2m+1 podem dar ζT, com η,ζ ímpares independentes e tr(T²)≠0. O termo ηζ não é o quadrado de uma mesma geradora ímpar. Para a_m, escolha M=ηT1+θT2 nos jatos baixos e □̄^mM=ζT3 nos altos; o coeficiente é ζηθ tr(T3[T1,T2]), que é não nulo para três rotações adequadas. A anticomutação produz o bracket, não o anula.

O símbolo (g0^{μν}k_μk_ν)^m pode ser isolado em uma direção não nula. A simetria dos jatos ordinários de C permite escolher os jatos superiores pertinentes independentemente dos inferiores; os termos de curvatura são de ordem menor. Numa combinação finita com m máximo, o maior jato não pode ser cancelado pelos outros membros. Isso prova independência de cocadeias, no espaço de coeficientes e acoplamento κ não nulo do modelo.

Como B0 é inerte e sC é quadrático, as expressões só de ghost aumentam sua valência sob s. Assim b_m é ciclo em C2 e a_m em C3. Isso não demonstra sua independência ou não nulidade em H(s): as fronteiras vindas dos campos e antifields continuam presentes. Também não se toma esta independência pontual de zeroformas como independência de funcionais integrados módulo divergências. Esse limite é essencial e a nota o preserva.

As famílias são naturais no fundo métrico e independentes de coordenadas do alvo. O rótulo L em sua inserção numa componente R_L é organização algébrica; não prova que todos esses termos sejam gerados no mesmo laço pelos vértices iniciais.

## 3. Inserções, acoplamentos e finitude

O_m em (4) é quadrático, real, natural e possui peso 2m−2(m−2)=4. A forma volume fornece peso −4. A conexão no pullback de φ0 torna a expressão uma inserção global do fibrado de flutuações, sem exigir uma carta única de S³. Cada m tem ordem finita; a união dos rótulos não tem cota uniforme. A afirmação de que são inserções possíveis não autoriza incorporá-las como contratermos de uma mesma lista de entradas de baixa ordem.

Para a equação (5), isolar D e usar n_C≤N, p_κ≤P e não negatividade das demais contribuições dá D≤w+N+2P. A hipótese sobre todos os pesos negativos é necessária. Ela não foi deduzida de L. Coeficientes de peso zero e funções de invariantes de B0 ainda podem formar um espaço vetorial real infinito, mesmo após limitar a ordem máxima dos jatos.

A nota distingue corretamente:
a) ordem máxima de um jato;
b) número total de derivadas/fatores derivados num monômio;
c) grau dos acoplamentos;
d) dimensão do espaço de coeficientes.
Fixar alguns desses dados não fixa automaticamente os outros.

[KNOWN — importação delimitada] Hollands, Th2 e eqs.256–259, descreve uma hierarquia D_n com independência funcional, escala, realidade e ação por partes, dependente das entradas. Isso sustenta a separação entre inserção e contratermo de aridade/entradas fixadas; não fornece uma cota para todo C_N. [Fonte primária](https://arxiv.org/pdf/0705.3340v4), pp.65–67 do PDF.

[KNOWN — hipótese efetivamente verificada] KMM, Def6.1, exige s_j+l_j≥0. No Th6.2, passo4, os coeficientes dos graus crescem com a ordem dos jatos, fornecendo a cota global. Um escalar de peso −2 como κ não satisfaz essa admissibilidade. O resultado trata a classificação de renormalizações de potências de Wick; não classifica todo o complexo BV. [Fonte primária](https://arxiv.org/pdf/1710.01937), pp.24,27 e32–33 do PDF.

Essas referências foram consultadas nesses pontos, não como importação de ausência de anomalias do Einstein–sigma.

## 4. L e filtrações

A aplicação clássica s=(S_cl,·), com S_cl∈R0 e bracket R_L×R_M→R_(L+M), preserva L. O mesmo vale para a translação b=t⁻¹B e sua exponencial finita em grau de forma. Não há uma falha do grau de laço clássico produzida pelo mero uso de b.

Um corte em derivadas brutas não é, por esse nome, estável: s0h já introduz uma derivada de C e H0 contém duas derivadas físicas. A conservação da engenharia usa os diferentes pesos dos geradores; não corrige por si um corte bruto inválido.

A distinção entre ordem clássica e correções quânticas também está correta. Um gerador de ordem positiva em ħ mistura componentes individuais para ordens superiores, mas respeita o quociente formal módulo ħ^(K+1) quando não há potências negativas. Fontes θ/ω exigem o multigrau próprio e a parte Laurent finita indicada na Ward072. O argumento mínimo não contém essa extensão por convenção.

## 5. Torre auxiliar: prova conferida

Para d_N:A^(N+1)→A^N, (d_Na)_i=a_i−xa_(i+1), escolher a_N=0 e resolver retroativamente prova sobrejetividade. Sem grau1, H²(D_N)=ker d_N. A parametrização
r ↦ (x^Nr,x^(N−1)r,…,r)
é um isomorfismo A→ker d_N, e H³(D_N)=0.

A projeção que retira a última componente leva esse vetor, no nível N+1, àquele do nível N com parâmetro xr. Logo os mapas em H² são multiplicação por x, embora os mapas nas cocadeias sejam sobrejetivos. Suas imagens x^kA são estritamente decrescentes em ℝ[x] e no anel de germes C∞ em zero. Neste último, a divisibilidade x^m=x^(m+1)f contradiz a continuidade de f na origem. Isso demonstra a falha de ML para essa torre auxiliar.

**Precisão de domínio em [linha153](<C:/IALD/Central de Patentes/Chatgpt/FINITUDE_POTENCIA_E_ML_078_20260910_032141_4248196/POTENCIA_DERIVADAS_E_MITTAG_LEFFLER.md:153>):** a expressão “em cada fibra numérica x=a” é válida para A=ℝ[x], ou para funções suaves numa vizinhança fixa que contenha a. Para o anel de germes em zero, não existe avaliação canônica em um a≠0: dois representantes do mesmo germe podem diferir nesse ponto. Sua fibra numérica canônica é a origem e nela o mapa é zero, portanto ML. A demonstração “posto finito e fibras finitas não implicam ML” já fica inteiramente paga pelo exemplo polinomial, com todas as suas fibras. A não-ML no anel de germes é válida separadamente, sem recorrer a avaliações não definidas.

Não se identifica a matriz bidiagonal com R0, H0 ou outro mapa do Einstein–sigma. A fonte a apresenta como contraexemplo a uma inferência algébrica geral, e esse é seu alcance.

## 6. Cálculo de lim¹ e mudança do anel

Para A=ℝ[x], a soma F(y)=Σ_N x^N y_N é bem definida em ℝ[[x]]: cada coeficiente recebe apenas finitíssimos termos. Se y_N=a_N−xa_(N+1), a telescopagem formal dá F(y)=a0. Assim a aplicação a ℝ[[x]]/ℝ[x] anula im Δ.

Toda série é obtida tomando y_N seus coeficientes constantes. Se F(y)=P é polinomial, a_N=(P−Σ_(j<N)x^j y_j)/x^N é polinomial por divisibilidade exata. Substituir mostra a_N−xa_(N+1)=y_N. Isso prova tanto o núcleo quanto a sobrejetividade e, portanto, lim¹≅ℝ[[x]]/ℝ[x] para a torre polinomial.

O símbolo x⁻N na construção da preimagem não amplia o anel: representa divisão exata de um polinômio divisível por x^N. Não foi introduzido um coeficiente singular.

Um controle do limite de escopo: y_N=1 representa 1/(1−x), não polinomial, logo uma classe não nula nessa versão. No anel de germes suaves, a mesma sequência já é Δa com a_N=1/(1−x), suave perto de zero. Isso demonstra concretamente por que essa fórmula não pode ser transferida sem prova ao anel suave. Não decide todo o lim¹ suave.

A falha de ML da torre não é uma afirmação sobre o lim¹ gravitacional. Tampouco a infinitude das cocadeias demonstra infinitude dos grupos H²(C_N),H³(C_N). As primitivas ou uma comparação efetiva com complexos finitos ainda precisariam ser construídas.

## 7. Custódia e conclusão

[REAL — documental] O pin da nota final e os sete pins de dependências foram relidos e confrontados com o manifesto. Os links locais existem; os arquivos lidos permaneceram idênticos. O rascunho .pending não foi usado como versão final. Não se executaram seu finalizador, CAS, Lean ou um.py; não se recapturaram originais.

**PASS_WITH_DOMAIN_PRECISION:** o núcleo da nota está correto no alcance delimitado, consumido com a precisão do §5 deste parecer sobre as fibras do anel de germes. Permanecem abertas a condição ML da torre efetiva Einstein–sigma, a classificação cohomológica completa, a admissibilidade causal e QME. Não há conclusão adicional de reconstrução geral ou UV.

## Pins medidos dos alvos principais

- [POTENCIA_DERIVADAS_E_MITTAG_LEFFLER.md](<C:/IALD/Central de Patentes/Chatgpt/FINITUDE_POTENCIA_E_ML_078_20260910_032141_4248196/POTENCIA_DERIVADAS_E_MITTAG_LEFFLER.md>) — 20123 bytes; SHA-256 bfcc6789adc973620c6d9f45addf865ad905e9c19caf45574b1a3b921fb7c5f5.
- [MANIFESTO_FINITUDE_ML_078.json](<C:/IALD/Central de Patentes/Chatgpt/FINITUDE_POTENCIA_E_ML_078_20260910_032141_4248196/MANIFESTO_FINITUDE_ML_078.json>) — 5422 bytes; SHA-256 07e9b6c90d790799855ddaadd4479ee2cafc550bd925d2ee07faf21e18c594bd.
