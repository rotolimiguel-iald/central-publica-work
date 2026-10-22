# Envelope completo de correlações com diagonais fixas — R1

Estatuto: [DERIVED], prova analítica; controles racionais sintéticos são verificações de exemplos, não prova Lean. Reaproveitamento: c1, AUDITORIA_F3_1_F3_2_C1_20261007.md:99–105,185 já estabelece sigma_GLS <= min sigma_i e condiciona a combinação GLS; aa2908da:23–30 já registra a cota nominal5.269. Fontes e linhas em SOURCE_PINS_R1.json. Não se repete a busca aleatória de200.000 matrizes nem o composto.

## 1. Objeto e hipóteses, antes do cálculo

Seja X vetor real de estimadores do MESMO parâmetro theta, E[X_i]=theta, com variâncias TOTAIS corretas sigma_i²>0, na mesma unidade. Considere E_sigma={C=Cᵀ>=0:diag(C)=sigma²}. As distribuições só precisam de segundos momentos para a álgebra de variância. A fonte/mapeamento e a hipótese de erro de média zero não são certificados por esta definição. O envelope contém todos os sinais de correlação; não é a caixa N/T anterior nem um limite inferido favorável para cada componente. Os termos já incorporados nas diagonais não são somados novamente.

## 2. Contraste fixo: máximo exato

Para qualquer vetor real w fixado sem os centros, |C_ij|<=sigma_i sigma_j pela positividade dos menores2x2. Logo

    wᵀCw <= sum_ij |w_i| |w_j| sigma_i sigma_j = (sum_i |w_i|sigma_i)².

A igualdade é atingida por C_w=v vᵀ, v_i=sign(w_i)sigma_i (sign(0)=1). Portanto é o máximo EXATO no envelope PSD. Se apenas PD for permitida, C_epsilon=(1-epsilon)C_w+epsilon diag(sigma²), 0<epsilon<1, tem a mesma diagonal e aproxima a igualdade: o mesmo número é o supremo. Nenhum zero cruzado é pressuposto. Pesos negativos entram em módulo; não são proibidos, mas podem ampliar o pior caso.

## 3. Desenho minimax, seleção só por erros

Sob sum_i w_i=1,

    sum_i |w_i|sigma_i >= sigma_min sum_i |w_i| >= sigma_min.

O peso e_k no menor sigma (desempate pelo índice pré-fixado) atinge sigma_min². Assim

    min_{1ᵀw=1} max_{C in E_sigma} wᵀCw = sigma_min².

Este é um resultado sobre o desenho sem informação de correlação: o robusto minimax pode descartar o ganho nominal de combinar leitores. Não é uma ordem para mudar a família primária; mudar a função de teste exigiria uma versão nova antes do composto. Se for exigido peso estritamente positivo de todos, o ótimo único e_k deixa de ser admissível quando o mínimo é único; pode restar só um ínfimo. Não esconder essa escolha.

## 4. Relação precisa com a cota GLS existente

Para cada C PD CONHECIDA e usada no cálculo, var_BLUE(C)=min_{1ᵀw=1}wᵀCw=1/(1ᵀC^-1 1)<=sigma_min² porque e_k é candidato. Isso não permite aplicar a cota aos pesos calculados com OUTRA C0 e usados na verdadeira C desconhecida.

A cota é afiada também quando se escolhe C primeiro. Ponha m=sigma_min² e C*=m11ᵀ+diag(sigma_i²-m). É PSD, preserva a diagonal, e para todo w de soma1,

    wᵀC*w=m+sum_i (sigma_i²-m)w_i²>=m.

Logo max_C min_w wᵀCw=m. C* é PD se o mínimo for único; se houver empates, o argumento continua variacional em PSD, sem usar uma fórmula de inversa/pseudoinversa indevida. A construção C* é distinta da matriz rank1 que maximiza um w arbitrário. O resultado não exige gaussianidade; a tradução em significância de cauda exige modelo/calibração adicional.

## 5. Fundo: coeficientes diferentes para os dois contrastes

Escreva D_f=wᵀX-f B, sum w=1, com B estimador do fundo. Para compatibilidade TGL, f=K; para rejeição LCDM, f=1. Não transferir o denominador de um contraste para o outro.

Se toda correlação entre locais e B também for desconhecida, aplicando a seção2 ao vetor de coeficientes (w,-f):

    sup Var(D_f)=(sum_i |w_i|sigma_i + |f|sigma_B)².

O minimax entre pesos locais é (sigma_min+|f|sigma_B)². Se, e somente se, se impuser a hipótese nomeada Cov(X_i,B)=0, o envelope local dá Var(D_f)<=sigma_min²+f²sigma_B². A cota nominal5.269 do acervo usa essa segunda forma com f=K. Este adendo não achou uma prova nova de independência local–BG.

O planejamento autorizado usa somente a mesma BG1 e os sigmas do precision_budget_r1.py: Delta=(K-1)H_BG e Delta/SE. beta=ALPHA_FINE_CODATA_2018*sqrt(e) em runtime; K é recalculado e comparado ao pin. Serão apresentados ambos f, primário e sem cefeidas. Delta/SE é separação nominal sob hipóteses, não sigma observado, probabilidade de detecção ou decisão de confirmação. Incerteza cosmológica de K é mantida fixa nesta conta e pertence a R3.

## 6. O que este envelope resolve e o que não resolve

[DERIVED] Resolve o pior caso de VARIÂNCIA de qualquer contraste linear pré-fixado no envelope de diagonais corretas; não precisa recuperar individualmente cada correlação residual para essa cota. O preço é conservadorismo e possível seleção de um único leitor.

[OPEN] Não torna corretas as diagonais, nem elimina um viés comum: X_i=theta+b+epsilon_i tem a mesma C para qualquer b e desloca a média. Não corrige mapas físicos errados, dependência das compressões, seleção de fontes ou escala/unidade equivocada. Não resolve covariâncias que mudem quando a receita da compressão mudar. Se vieses forem limitados por b_i, outro contrato pode adicionar |bias|<=sum|w_i|b_i; sem limite não há garantia uniforme de teste.

[OPEN] Não fornece distribuição de cauda. Por exemplo, erro sintético de média0 com P(+5)=P(-5)=1/50 e P(0)=24/25 tem variância1 e probabilidade bilateral4% em5 unidades de desvio padrão. Mesma variância não significa cauda gaussiana. R4 qualifica a significância.

## 7. Falsificadores e uso permitido

A1: com C PSD, diagonal declarada correta e pesos fixos, encontrar wᵀCw maior que a cota falsifica o teorema/implementação. A2: encontrar desenho de soma1 cujo pior caso seja menor que sigma_min² contradiz a construção C*. A3: rank1 C_w não atingir a cota ou C* não preservar a diagonal é falha algébrica. A4: aceitar como garantia física erro de média não controlado, mapa OPEN, viés não limitado, ou tratar Delta/SE como cauda é falha de escopo.

Os controles são exatos/racionais e pré-fixados, sem centros observados. O catálogo R1 anterior permanece OPEN; este envelope é uma alternativa analítica aditiva de desenho, não substituição automática da matriz N/T ou autorização de abertura. Não produz alvo pós-ajustado pelo z.
