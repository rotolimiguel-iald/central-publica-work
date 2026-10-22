# Revisão independente085: invariantes de Killing no módulo quadrático

10/09/2026. Autor desta revisão: selected_geometry_design. [DERIVED — revisão matemática escrita]. [KNOWN — importação primária delimitada abaixo]. [REAL — custódia no recibo]. Esta revisão pertence exclusivamente à investigação085 e não integra a entrega084. Nenhum um.py, CAS ou Lean executado/importado.

**Conclusão.** Li integralmente a [nota085](<C:/IALD/Central de Patentes/Chatgpt/INVARIANTES_QUADRATICOS_KILLING_085_20260910_060005_9363957/N_INVARIANTES_KILLING_ZERO_POR_KT_LINEAR.md>) e seu manifesto. Conferi a aplicação dos resultados primários de BBH, a nova aciclicidade KT linear completa, o retorno ao quociente pontual e a extensão inerte por Rher. Não identifiquei erro material na conclusão

(Rher⊗Sym²Mcal)^g=0,

para a referência espaço-forma fixada, setor métrico mínimo, elementos finitos em jatos e extensão escalar trivial declarados. O resultado elimina os coeficientes quadráticos invariantes dos canais de Cartan na forma normal084; não decide se J_W é divergência de uma corrente natural.

As provas079 de fatoração e084 de redução por isotropia são antecedentes de minha autoria, já submetidos a revisões próprias. Aqui examino a NOVA aplicação de Turing; não atribuo a mim aprovação independente retroativa desses antecedentes nem tomo meus pareceres anteriores como validação automática de085.

## 1. Os quocientes e a injeção estão corretamente tipados

Em cada ponto, U consiste nas combinações lineares finitas de jatos métricos, E é a imagem dos jatos de Hh e γ é o mapa linear para os jatos de ghost gerado por h↦R0C. A identidade HR0=0 dá E⊂ker γ. Portanto o mapa

Mcal=ker γ/E → U/E

é injetivo por definição, antes de qualquer escolha de geradores Weyl. A potência simétrica preserva essa inclusão sobre o corpo real: basta cindir os espaços vetoriais. Para cada expressão, uma cisão de um espaço finito que contenha seus fatores é suficiente.

Como E é um subespaço LINEAR, o ideal polinomial que ele gera satisfaz Sym(U)/(E)=Sym(U/E). Logo Sym²Mcal injeta no grau dois desse quociente. A afirmação não seria automática para relações não lineares arbitrárias, mas estas não são usadas aqui. Também não requer que os jatos de Weyl sejam livres.

A distinção entre o módulo gauge-invariante, o quociente pelas EOM e H_char de grau zero é mantida. Em particular, a inclusão não é uma identificação de Mcal com todos os jatos on-shell.

## 2. Exatidão linear KT: completude e extremo de antifield dois

Os [sinais corrigidos077](<C:/IALD/Central de Patentes/Chatgpt/PRIMEIROS_TRUNCAMENTOS_BRST_077_20260910_030228_0972771/ADENDO_SINAL_KOSZUL_TATE_077.md>) e a [normalização081](<C:/IALD/Central de Patentes/Chatgpt/COHOMOLOGIA_QUADRATICA_WEYL_081_20260910/H3_E5_BIANCHI_E_REPRESENTANTES_QUADRATICOS_WEYL.md>) dão δp=Hh e δq=Dp, com DH=0. As mudanças de densidade e fibra são invertíveis e dependem apenas do fundo. É possível regressar às variáveis variacionais originais para aplicar os argumentos de Euler–Lagrange; não se presume que o Hessiano normalizado tenha a mesma matriz do Hessiano densitizado.

O grau positivo um usa a fatoração PH=B D, incluindo sua versão pontual. Conferi novamente os passos pertinentes de079/081: o núcleo polinomial do símbolo Einstein é uma imagem de gradiente simetrizado; a fatoração por divergência tem o fator dois correto; subtrair B D conserva PH porque DH=0 e reduz a ordem estritamente. A saída B tem ordem no máximo r−1 quando P tem ordem r.

O uso de coeficientes C∞(x) é legítimo nesse algoritmo. Os coeficientes do operador ficam à esquerda; a composição diferencia D e seu argumento, não uma extensão arbitrária dos valores dos coeficientes de B. Em cada passo os novos coeficientes dependem suavemente dos dados iniciais e dos jatos do fundo.

O novo extremo de085 também confere. Se ZD=0 sobre p simétrico arbitrário, seu símbolo z(ζ) satisfaz ζ_a z_b+ζ_b z_a=0, depois das identificações de fibra. Para ζ≠0, uma componente não nula ζ_j permite concluir primeiro z_j=0 pela diagonal jj, depois todos os z_b=0 pela componente jb. Isso prova a nulidade do polinômio, inclusive no cone nulo, sem construir inversos de ζ². A indução na ordem dá Z=0.

Essa é ausência de IDENTIDADES DIFERENCIAIS entre as identidades. Não é ausência de seções Killing. Uma solução R0v=0 não fornece um operador R0Z[f]=0 para parâmetros livres. A nota não descarta os grupos relativos em outros graus que podem detectar essas soluções.

## 3. Cortes, regularidade local e aciclicidade polinomial

Os pesos h_I:|I|+1, p_I:|I|+3 e q_I:|I|+4 dão cortes finitos estáveis: H tem ordem dois e D ordem um. A primitiva de um ciclo p com r derivadas usa q com no máximo r−1, portanto permanece no corte r+3. A nulidade no extremo q vale também em cada corte.

Na referência espaço-forma, as matrizes de jatos covariantes simetrizados, em um frame ortonormal local, são tensoriais com parâmetros K fixados. Comutadores inserem curvatura constante e graus inferiores; os postos são constantes na carta. Cisões reais dessas matrizes produzem cisões suaves locais. Não se introduz uma integração sobre o grupo Lorentz não compacto.

A cisão em pares u_i,v_i=δu_i fornece a homotopia ímpar ρ=Σu_i∂/∂v_i, com anticomutador δρ+ρδ igual ao número de fatores de pares. O denominador é um inteiro positivo. As duas paridades dos pares — h/p e p/q — são tratadas na álgebra simétrica GRADUADA, não como uma álgebra puramente comutativa.

Cada polinômio e os seus diferenciais vivem em algum corte finito; assim H_{k>0}(δ)=0 e H_0(δ)=Sym(U)/(E) na união. A contração conserva o grau polinomial total. Não é necessário escolher cisões compatíveis para uma completação inversa, pois a categoria usa elementos finitos e a passagem é por união.

Uma precisão útil para interpretar os cortes: mesmo se uma combinação P H de ordem alta resultar num jato de ordem inferior, pode-se subtrair o fator do símbolo B D enquanto o símbolo superior de P H cancela. DH=0 conserva a saída e reduz a ordem de P. Isso impede que relações ocultas de ordem arbitrariamente alta obriguem a tratar o quociente de baixa ordem como uma torre livre. A prova principal necessita apenas da exatidão positiva e do ideal completo na união, já fornecidos.

## 4. Importação primária: caso linear, não apenas linearizável

Li diretamente [BBH2000](https://arxiv.org/pdf/hep-th/0002245v3), Teorema6.2/equação(6.17), Teorema6.5(i) e apêndice6.B/equações(6.44–6.49), páginas39–40,43–44,53–55. O primeiro identifica H⁰₀(d|δ)/R com H⁴₄(δ|d). O segundo anula Hⁿ_k(δ|d) para k≥3 no caso irreducível linear. A prova separa esse caso do apenas linearizável: os restos em(6.49) desaparecem quando a ação é quadrática e os geradores são independentes dos campos. A homotopia de escala então termina; a etapa formal iterativa é outra situação.

Na aplicação085, a ação é exatamente o quadrático Einstein sobre um fundo on-shell, e R0 depende de g0, não de h. O §2 da nota fornece a resolução exigida. Dependência suave explícita em x permanece permitida; a derivada total e δ conservam o grau nos geradores. Em grau positivo fixado, a integração da homotopia é divisão pelo grau. Logo a aplicação conserva polinomialidade e ordem finita.

A conclusão utilizada é somente H_char⁰=R na carta auxiliar. Não se importam Whitehead, ausência de Killing ou nulidade da cohomologia natural inteira.

## 5. Invariância e passagem a uma função horizontalmente constante

Um elemento n∈(Sym²Mcal)^g é, em particular, h-invariante. Ele usa um corte finito da isotropia. Nesse corte, os módulos tensoriais reais da álgebra semissimples h são completamente redutíveis; portanto um representante quadrático pode ser escolhido h-invariante. A geração por jatos Weyl e suas relações é a de080/081, não uma nova liberdade de dados.

Transportar as contrações invariantes por g0 e ε0 dá um escalar natural local F(h). Os coeficientes dependem dos parâmetros fixados e são paralelos. Pela [identificação082](<C:/IALD/Central de Patentes/Chatgpt/COMPLEXO_CE_QUADRATICO_082_20260910/IDENTIFICACAO_D1_CE_KILLING_E_JATOS_WEYL.md>), incluindo os índices de derivadas, a ação de uma transvecção no ponto é a classe de ∇bar_aF. A invariância de n zera essas quatro classes.

A homogeneidade local da espaço-forma e a equivariância dos operadores e relações transportam a igualdade do ponto base a uma carta. Essa passagem não vale por simples escolha de coordenadas em um fundo arbitrário; aqui é justificada pela hipótese específica de espaço-forma e pela natureza do representante. Como F é escalar orientado, obtemos d_HF=0 no quociente polinomial on-shell.

Não se usam dados TT, convergência de uma solução com jatos Weyl arbitrários ou separação de classes por testes.

## 6. Por que C∞(x) auxiliar não invalida o retorno

O resultado horizontal dá F−c∈(E), para c real, dentro da álgebra local auxiliar. Trata-se de uma igualdade algébrica: pode-se escrever F−c=δB com B finito de antifield number um, ou uma soma finita de coeficientes polinomiais vezes jatos das EOM.

Ao especializar em x0, esses coeficientes suaves tornam-se números. O diferencial δ não age em x nem nos dados de fundo. A igualdade especializada pertence, portanto, ao MESMO ideal das EOM lineares no ponto. A constante-posto local e as cisões dos cortes garantem que a fibra é o quociente usado em(2–4), e não um quociente diferente criado por germes escolhidos.

Como o ideal é homogêneo e F tem grau dois, a avaliação no jato h=0 implica c=0. A classe de F é então zero em Sym²(U/E). A injeção de Sym²Mcal força n=0.

Esse retorno não exige uma primitiva natural: só a igualdade zero e a inclusão. Tampouco radicaliza o ideal por anulação numérica. Assim, a ampliação coordenada temporária é legítima para esta conclusão de NULIDADE, embora não pagasse automaticamente a naturalidade de uma primitiva não nula exigida em outro problema.

## 7. Escalares herdados e consequência delimitada

Após fixar K e as normalizações, a ação é trivial no fator Rher. Para uma base real X_A da álgebra de Killing, Φ(v)=(ρ_{X_A}v)_A é injetiva por V^g=0, V=Sym²Mcal. Tensorizar essa injeção por Rher preserva a exatidão, pois a base é o corpo real. O espaço de chegada tem dez cópias; seu núcleo é precisamente a invariância na extensão escalar.

A prova é válida com nilpotentes ou divisores de zero em Rher. Não usa homomorfismos de avaliação Rher→R. Exige, porém, o produto tensorial algébrico e uma ação realmente inerte; não inclui produtos completados, espectadores tensoriais ou um operador ainda dependente de K variável.

No [critério084](<C:/IALD/Central de Patentes/Chatgpt/REDUCAO_ISOTROPIA_CE_084_20260910/REDUCAO_FINITA_GHOSTS_E_CANAL_EULER.md>), f∈N^g é quadrático. Sua nulidade retira o termo K²f e deixa a condição J_W=div V. Retira também o coeficiente quadrático do canal traço na forma normal. A unidade de Rher tem grau zero e não fornece uma exceção nesse setor.

Não se provou a existência ou inexistência de V. Grau horizontal zero e grau horizontal quatro não são a mesma obrigação. Permanecem fora a imagem geral CE, QME, UV, causalidade Q2 integral, o fundo sigma físico não constante, outros anéis e construções globais.

## 8. Custódia e âmbito desta revisão

O recibo mede os doze arquivos antes/depois e confronta os pins da origem e do registro inicial. A fonte085 e seu manifesto foram lidos integralmente; os antecedentes foram relidos nas partes necessárias, aproveitando as revisões anteriores já registradas. O helper085 foi somente pinado, sem execução; não afirmo auditoria integral de seu código. O PDF primário foi consultado pela web, sem hash local inventado.

Uma primeira tentativa de leitura usou um nome de manifesto inexistente; a falha foi visível, seguida de descoberta por rg --files e leitura do nome real MANIFESTO_INVARIANTES_QUADRATICOS_085.json. Nenhuma escrita ocorreu nessa tentativa.

Todas as verificações numéricas do recibo são documentais. As demonstrações acima são análise escrita, não CAS nem Lean. Nenhum original ou arquivo congelado foi alterado. O resultado085 permanece separado da entrega084 encerrada.
