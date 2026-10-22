# Revisão independente da covariantização suave e colagem em S³

10/09/2026, arco 071. [DERIVED — revisão matemática escrita de autoria própria] [REAL — leitura e pins medidos]. Fonte examinada: `COVARIANTIZACAO_SUAVE_071_20260910_001058_826723/COVARIANTIZACAO_E_H2_GLOBAL.md`. Nenhuma fonte congelada foi alterada; nenhum CAS, Lean ou um.py foi executado.

**Resultado:** não identifiquei erro material nem circularidade nos passos examinados, considerando L0–L2 na classe indicada. A passagem coordenada→covariante é explicitada e não consiste em avaliar uma série de Taylor da matéria. A precisão de notação da seção 3 abaixo deve acompanhar o limite de antifields: usa-se o grau da própria primitiva. O resultado continua sendo H² característico covariante da ação ambiente, com as restrições declaradas, não a QME ou a aplicação automática a todo espaço de contratermos renormalizados.

## 1. Fontes e dependências efetivamente confrontadas

Li a nota integral e confrontei seus passos com [BBH1995, §3, Teorema 6.1 e Apêndice E](https://arxiv.org/pdf/hep-th/9505173v2), incluindo os geradores (3.6)–(3.7) e (E.11)–(E.16). A comparação formal em antifields e sua limitação de ordem foram conferidas em [BBH2000, Teorema 7.1 e §7.3](https://arxiv.org/pdf/hep-th/0002245v3). Esses locadores sustentam os mecanismos citados; não são apresentados como um teorema pronto sobre o alvo suave desta tarefa.

L0 é a resolução KT ordinária anterior; L1 é o resultado horizontal ordinário suave da nota M₂071 e seus adendos; L2 é a transformação triangular de jatos. A nota usa esses resultados como entradas. Em particular, não extrai L1 da exatidão covariante que pretende provar.

## 2. Comparação da descida com s e dependência explícita em x

Para k=2,3,4, a comparação KT/horizontal usa respectivamente H², H¹ e H⁰/R; para k>4 termina na KT positiva. Assim L0/L1 fornecem a nulidade relativa necessária. A passagem ao BRST pode inicialmente produzir uma série por número de antifields, mantendo cada coeficiente suave nos valores e finito nos derivados. Esse uso está de acordo com a distinção entre o Teorema 7.1 e a advertência de §7.3 da fonte.

O operador b=dx^μ∂/∂ξ^μ integra a descida sobre coeficientes sem x explícito. A fonte examinada não aplica [b,s]=d_H a uma função externa arbitrária f(x): ela conserva primeiro a derivada dω dos coeficientes externos, retira os coeficientes positivos fechados pela homotopia local em x e chega à identidade de zeroformas α=sβ. Só nessa última identidade avalia x=x₀, pois s não deriva as coordenadas explícitas.

Essa ordem é suficiente para evitar o salto de classe mais imediato. Avaliar x numa igualdade anterior que contivesse d_H seria inválido, mas essa operação não é usada. O enunciado (3.3) é para os elementos covariantes considerados, sem formas externas arbitrárias de espaço-tempo. Não significa que f(x) deixe de ser um cociclo de s na álgebra coordenada irrestrita.

## 3. Avaliação dos pares e finitude

Em geradores (U,V;ξ̂,Ĉ,T,T*), sU=V e sV=0; o diferencial dos geradores covariantes não depende de U,V. Portanto a avaliação U₀=e₀ invertível, U_positivo=0,V=0 é um mapa de complexos de zeroformas. O ideal da avaliação é estável por s. A escolha e₀ pertence à carta de suavidade: não há avaliação singular em e=0.

A mudança de geradores é finita por ordem de jato. Nos antifields, BBH (3.6) normaliza por e e e⁻¹; a combinação ξ̂*_a envolve ξ*_μ−A_μ^I C*_I. Os dois termos possuem antigh dois. Os antifields de campos e suas derivadas covariantes mantêm seus graus. Essa mudança preserva a filtração utilizada na contagem.

Depois da avaliação restam dez geradores positivos anticomutantes: quatro ξ̂ e seis Ĉ. Para um termo homogêneo de grau total r,

\[
\operatorname{antigh}=\operatorname{puregh}-r\le10-r.
\]

Logo uma série formal em antigh conserva somente um número finito de coeficientes após a projeção. Cada coeficiente era local finito; o máximo das ordens sobreviventes é finito. O diferencial comuta com a projeção, inclusive nos componentes que desaparecem, de modo que uma contribuição da cauda não reaparece após aplicar s.

**Precisão do símbolo q em (4.3):** o limite deve sempre usar o grau do próprio elemento. Se α tem ghost q e α=sβ, então gh(β)=q−1 e

\[
\operatorname{antigh}(\beta)\le10-\operatorname{gh}(\beta)=11-q.
\]

No caso central gh(α)=2, o teto seguro para β é 9. A fórmula (4.3) está correta quando q nomeia o grau do termo nela considerado; não se deve cortar a primitiva no teto 8 usando o grau de α. Essa precisão não altera o argumento de finitude.

A dependência suave arbitrária nos valores métricos torna-se numérica em e₀. Os coeficientes C∞(y) continuam funções suaves genuínas. A projeção sobre tipos de Lorentz é realizada numa soma finita de módulos tensorais e deixa esses coeficientes intactos. Como s é equivariante, pode-se projetar uma primitiva sem mudar o cociclo invariante. Não é necessária uma média sobre o grupo de Lorentz não compacto. A conversão de volta aos índices coordenados usa os tensores invariantes permitidos, sem manter e₀ como um campo externo.

## 4. Colagem: os termos sρ estão presentes

O feixe de expressões polinomiais covariantes com coeficientes suaves é estável sob multiplicação por partições de unidade no alvo. Isso o torna adequado à contração de Čech, embora s não seja linear sobre essas funções: sρ=ξ̂^a u_a^A∂_Aρ.

Para o cociclo global de grau dois, a sequência de diferenças das primitivas locais tem graus 1,0,−1,−2. O único obstáculo constante surge no grau zero, como cociclo de Čech de grau dois. H²(S³;R)=0 remove-o. Nos graus negativos, a exatidão local fornece os passos restantes. Uma cobertura boa de multiplicidade quatro termina a cocadeia em grau de Čech três.

Ao eliminar a maior componente de Čech pela contração h, subtrai-se o diferencial total de hB. A parte de s dessa operação diferencia também os coeficientes da partição; produz justamente os termos sρ. Em seguida essa correção está na componente de Čech inferior que será eliminada. Portanto a colagem não é a soma ingênua Σρ_iβ_i. Ela termina depois de um número finito de eliminações e preserva ordem finita e suavidade.

Os argumentos de grau zero e negativo não enfrentam outro obstáculo constante positivo: constantes locais não nulas não são s-exatas, e o alvo conectado identifica uma única constante. A construção não elimina a classe de volume em H³(S³), nem aborda torsão ou fases globais discretas.

## 5. Identidade básica com F e sinais

Escreva D=δ+s₁ para a parte em C=0. Da invariância Lorentz de β e {s,∂_I}=L_I resulta s(∂_Iβ)=0. Como gh(∂_Iβ)=0, a possível parcela constante d_I pertence ao coadjunto. A semissimplicidade elimina esse covetor invariante, portanto ∂_Iβ=sβ_I. Os β_I podem ser escolhidos no tipo tensorial correspondente.

A anticomutação das derivadas em C e a transformação coadjunta dão s(∂_(Iβ_J))=0. O grau é −2, de modo que a exatidão negativa fornece ∂_(Iβ_J)=sβ_IJ, com β_IJ simétrica.

A componente C=0 de α=sβ é

\[
\alpha=D\beta_0+F^I(\partial_I\beta)_0.
\]

Usando as duas relações anteriores e DF=0 nas contrações invariantes,

\[
\alpha=D\bigl[\beta_0+F^I(\beta_I)_0
                  +F^IF^J(\beta_{IJ})_0\bigr]+
 F^IF^JF^K(\partial_K\beta_{IJ})_0.
\]

O último termo é zero em dimensão quatro, pois contém seis ξ̂. Os sinais são positivos: F é par. Não falta fator 1/2, porque F^IF^J já seleciona a parte simétrica de ∂_Iβ_J, com a mesma convenção de parênteses empregada na equação definidora de β_IJ. A expressão entre colchetes é Lorentz-invariante e independente de C, de modo que seu s é seu D. A fórmula (6.4) é consistente.

## 6. Retorno característico e alcance

A elevação de ρ₂(ξ̂) por antifields até os níveis de ξ̂ três e quatro usa KT covariante positiva e termina por ξ̂⁵=0. Depois de obter a primitiva básica, sua componente de antifield zero recupera ρ₂≈d_Hβ₁. Isso não confunde a cohomologia horizontal coordenada com a básica: a avaliação, a projeção tensorial, a colagem e a identidade com F são precisamente os passos adicionais.

O resultado retirado é o contrato H²_char,cov para a ação ambiente Einstein–sigma e a álgebra natural finita descrita. A prova não fornece automaticamente um limite uniforme de ordem de derivadas exigido por um esquema de renormalização específico. A transferência para os contratermos admissíveis, a identificação da anomalia efetivamente produzida e a construção da QME continuam separadas, como a própria fonte ressalva.

Não há nesta revisão uma afirmação de ausência de todas as anomalias globais, inclusão de gauge de Weyl ou torsão, equivalência com a ação composta em P, nem completude UV. A precisão de graduação registrada acima basta para a ambiguidade de notação encontrada; não identifiquei necessidade de corrigir o argumento matemático por cima da fonte congelada.
