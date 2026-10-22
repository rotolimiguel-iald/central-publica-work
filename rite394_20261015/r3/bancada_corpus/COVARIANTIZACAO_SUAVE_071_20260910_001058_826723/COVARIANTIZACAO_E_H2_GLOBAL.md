# Covariantização finita e colagem suave do grau característico dois

10/09/2026, arco 071. [DERIVED — demonstração escrita]. Esta nota prova um teorema de transporte: a exatidão horizontal ordinária suave nos graus 0, 1 e 2, junto da resolução KT na mesma classe, implica a exatidão covariante em grau 2 para o Einstein–sigma com alvo S³. A entrada ordinária é identificada, não escondida como parte da conclusão. Não houve Lean, CAS ou execução de um.py.

A novidade em relação ao arco 070 é evitar a avaliação de séries formais nos valores de φ. Primeiro se constroem primitivas suaves em cartas; depois se eliminam variáveis de escolha de referencial, se colam os dados no alvo e se retiram os ghosts de Lorentz por uma identidade finita. A hipótese de normalidade formal não é usada como substituto desse transporte.

## 1. Enunciado e entradas exatas

[INPUT — modelo] Dimensão 4, métrica Lorentziana não degenerada, conexão de Levi-Civita, alvo (S³,h) redondo, κc≠0 e Λ constante. A ação ambiente contém g e φ independentes:

\[
S=-{1\over2\kappa}\int(R-2\Lambda)dV_g+
 {c\over2}\int g^{ab}h_{AB}(\phi)\partial_a\phi^A\partial_b\phi^B\,dV_g.
\]

Há difeomorfismos e, na apresentação por vielbein, redundância local de Lorentz. Não há gauge interno no alvo, conexão independente com torção, potencial sigma ou gauge de Weyl.

A álgebra natural contém expressões de ordem finita, polinomiais nos jatos diferenciados e antifields, com coeficientes C∞ globais no alvo. Métrica, inversa e volume entram tensorialmente; em vielbein, os denominadores permitidos são potências de det(e). Não se invertem dy, curvaturas ou componentes como g⁰⁰. Igualdade fraca significa igualdade em todos os jatos estacionários formais, inclusive os degenerados em dy.

São entradas matemáticas, demonstradas nas notas anteriores:

- **L0:** resolução KT ordinária com homotopias finitas na classe coordenada C∞(x,g,y)[jatos diferenciados, antifields], sem completar y.
- **L1:** numa carta contrátil dos valores, H⁰ horizontal estacionário é R e H¹=H²=0, com primitivas na mesma classe coordenada.
- **L2:** as mudanças entre jatos parciais e covariantes são triangulares, polinomiais nos derivados, suaves nos valores; as equações/gauge são naturais.

L0 e L2 estão em [certificado KT069](../REGULARIDADE_KT_JATOS_20260909_224852/CERTIFICADO_POLINOMIAL_EINSTEIN_SIGMA.md), especialmente §§4–7. L1 em grau 2 foi construído em [M2 suave071](../M2_SUAVE_RELATIVO_071_20260910_000347/M2_SUAVE_POR_COMPATIBILIDADE_E_SPENCER.md), §§3–8. Os graus 0 e 1 seguem dos mesmos grupos de contato: E₁^{1,1}=E₁^{2,0}=E₁^{1,0}=0. Para ρ₁ fechado, levanta-se ρ₁+α₁₀ a uma forma total fechada; para f horizontalmente fechado, d_Vf=0. A contração finita de fibras e de valores dá respectivamente uma primitiva e uma constante.

**Teorema de transporte.** Sob L0–L2,

\[
\boxed{H_{\mathrm{char,cov}}^2(E_\infty;\mathcal A_{\mathrm{nat}})=0.}
\tag{1.1}
\]

Mais explicitamente, se ρ₂ é natural, suave global no alvo e d_Hρ₂≈0, existe uma 1-forma β₁ da mesma classe com ρ₂≈d_Hβ₁. A prova não introduz um novo limite analítico, uma série nos valores do alvo ou uma localização no posto de dφ.

A conclusão vale para a ação ambiente indicada. Não calcula por si a cohomologia de uma ação reduzida pela substituição simultânea g=g[P],φ=φ[P], nem transforma (1.1) em QME renormalizada.

## 2. Fontes primárias e ponto em que são adaptadas

[KNOWN] [BBH1995, §3, §6 e apêndices C–E](https://arxiv.org/pdf/hep-th/9505173v2) fornecem a separação de jatos covariantes/pares de gauge, a comparação das descidas e a obstrução de Chern–Weil à primitiva básica. Sua álgebra material é polinomial; por isso a extensão C∞ no alvo é demonstrada abaixo.

[KNOWN] [BBH2000, Teoremas 6.2 e 7.1 e §7.3](https://arxiv.org/pdf/hep-th/0002245v3) distinguem a comparação relativa da hipótese de número limitado de antifields. Usaremos primeiro a comparação formal em antifields e depois um truncamento efetivo, sem completar os valores materiais.

[KNOWN] [Verbovetsky, §3.1](https://arxiv.org/pdf/math/9803115v1) é a fonte do cálculo de contato usado na entrada L1. Esta nota não refaz esse cálculo e não o apresenta como teorema covariante.

As seções seguintes verificam a mudança de classe: suavidade, dependência explícita em x, denominadores métricos, finitude e colagem global.

## 3. O passo coordenado até uma primitiva BRST

Considere inicialmente uma carta contrátil no alvo e nos valores métricos. De L0 e do lema de Poincaré horizontal off-shell, a descida/subida KT identifica H⁴_k(δ|d_H), k=2,3,4, aos grupos horizontais estacionários de graus 2,1,0, com as constantes removidas no último. Para k>4 chega-se a um grupo KT positivo de forma zero. L1 e L0 dão, portanto,

\[
H_k^4(\delta\mid d_H)=0\quad(k\ge2).
\tag{3.1}
\]

Essa comparação é finita em grau de forma; em cada etapa a primitiva KT e a primitiva horizontal permanecem suaves nos valores e polinomiais nos derivados.

No complexo BRST completo, a comparação em ghost negativo transforma (3.1) na ausência de classes de forma máxima e ghost ≤−2. Se necessário, ela é efetuada primeiro como uma expansão por **número de antifields**: cada coeficiente é uma expressão local finita e C∞ nos valores. Isso é distinto da expansão de y em série de Taylor.

Para uma zeroforma BRST de ghost q≤2 nas variáveis covariantes, a descida gravitacional liga uma classe não constante a uma classe de forma máxima de ghost q−4. A integração da descida é gerada, sobre coeficientes sem x explícito, por

\[
b=dx^\mu{\partial\over\partial\xi^\mu},\qquad [b,s]=d_H,\qquad
a^{q-p,p}={b^p\alpha\over p!}.
\tag{3.2}
\]

**Precisão sobre x.** A identidade (3.2) não vale sobre um coeficiente arbitrário f(x), pois s(x)=0. Mantêm-se primeiro os coeficientes externos ω(x,dx): sua contribuição adicional é dω. Na descida não trivial esses coeficientes devem ser fechados; numa carta do espaço-tempo, a homotopia ordinária em x remove as formas positivas e o coeficiente da zeroforma final é constante. Só depois de obter uma identidade de zeroformas α=sβ é permitido avaliar um x explícito restante em x₀. Nessa identidade s comuta com tal avaliação. Não se avalia x numa igualdade que ainda contém d_H.

Assim, localmente nos valores, a comparação dá

\[
H^q(s)=0\ (q<0,\ q=1,2),\qquad H^0(s)=\mathbb R,
\tag{3.3}
\]

para os elementos covariantes considerados, com uma primitiva inicialmente coordenada e eventualmente formal em número de antifields. O próximo passo torna a primitiva estritamente local.

Uma apresentação métrica pode ser levantada localmente a vielbein sem acrescentar equações físicas. Numa seção suave local do fibrado de referenciais, a coordenada Lorentz de e e sua variação BRST formam pares (l,sl), inclusive os derivados; a redundância Lorentz é livre nessa fibra. Eliminar esses pares compara os complexos locais. Essa operação pode gerar dependência suave não racional em g apenas nessa etapa intermediária. Não requer uma seção de vielbein global, e não identifica as cohomologias topológicas globais de métricas e de referenciais.

## 4. Projeção concreta para os tensores covariantes

Use os geradores independentes

\[
(U,V;\ \widehat\xi^a,\widehat C^I,T,T^*),\qquad
sU=V,\quad sV=0.
\tag{4.1}
\]

U reúne o vielbein e jatos simetrizados de escolha de coordenadas; V são suas variações BRST. T,T* são os tensores covariantes e antifields covariantes, inclusive os valores y. O diferencial dos últimos geradores não depende de U,V.

Escolha para o valor do vielbein uma matriz invertível fixa e para os U de derivada positiva os valores zero. Ponha V=0. A avaliação

\[
\pi_0:\quad U_0=e_0,\ U_{>0}=0,\ V=0
\]

é um mapa de complexos de zeroformas: π₀s=sπ₀. Em particular, se α não depende de U,V e α=sβ, então

\[
\alpha=s(\pi_0\beta).
\tag{4.2}
\]

Não se põe e=0. O ponto e₀ está dentro da carta em que β é suave. A mudança de geradores usa somente operações finitas em cada ordem e e⁻¹; é polinomial nos jatos derivados e suave em y. Portanto π₀β tem coeficientes C∞(y) e dependência polinomial nos tensores diferenciados. A dependência suave arbitrária em valores métricos foi avaliada em e₀ e tornou-se numérica.

**Finitude em antifields.** Depois de π₀ restam somente quatro ghosts anticomutantes \(\widehat\xi^a\) e seis \(\widehat C^I\). Se um termo tem ghost total q, seu número de antifields é

\[
\mathrm{antigh}=\mathrm{puregh}-q\le10-q.
\tag{4.3}
\]

A mudança (4.1) preserva antigh. Logo toda a cauda de uma primitiva formal de antigh>10−q é anulada por π₀. Apenas um número finito de coeficientes locais da construção da seção 3 sobrevive; a ordem máxima de seus jatos é finita. Este é um truncamento algébrico em variáveis de ghost, não uma avaliação de série infinita nos campos.

Denote por \(\mathcal B\) a álgebra obtida de T,T*,ξ,C. Em cada carta do alvo ela satisfaz exatamente (3.3), agora com primitivas **finitas**, C∞(y) e polinomiais nos jatos covariantes.

**Representações de Lorentz.** Um polinômio finito nesses tensores pertence a uma soma finita de tipos tensorais de Lorentz; C∞(y) é um anel de coeficientes escalares para esse grupo. A completa redutibilidade de so(1,3) permite projetar no tipo trivial. Como s comuta com Lorentz, uma primitiva de um elemento invariante pode ser escolhida invariante. A operação é linear nos índices de Lorentz e não expande nem integra y. Não se faz média integral sobre o grupo não compacto. Quando esse polinômio invariante é reescrito em coordenadas, as contrações usam g,g⁻¹ e volume; a matriz auxiliar e₀ não permanece como um campo externo.

## 5. Colagem global no S³, com as derivadas das partições incluídas

A álgebra \(\mathcal B\) define um feixe no alvo: as transições entre cartas são as transformações tensoriais dos jatos covariantes. Seus elementos têm coeficientes suaves no alvo e grau/ordem finitos em cada carta. A multiplicação por uma partição de unidade ρ(y) preserva a classe.

Isso **não** significa que sρ=0. De fato,

\[
s\rho=\widehat\xi^a u_a^A\partial_A\rho.
\tag{5.1}
\]

Por isso a soma ingênua de primitivas locais ponderadas não é a prova de colagem.

Eis o argumento finito. Escolha uma boa cobertura finita de S³, subordinada a uma triangulação, de multiplicidade no máximo quatro. Para α global s-fechada de ghost 2, (3.3) fornece primitivas β_i de ghost 1. Nos encontros,

\[
\beta_j-\beta_i=s b_{ij},\qquad \mathrm{gh}(b_{ij})=0,
\]

porque H¹ local é zero. Em encontros triplos,

\[
b_{ij}+b_{jk}+b_{ki}=c_{ijk}+s c'_{ijk},
\tag{5.2}
\]

onde c_ijk é constante e gh(c')=−1, pois H⁰ local é R. As constantes constituem um cociclo de Čech: uma constante não nula não é s-exata, e aplicar a diferença de Čech a (5.2) dá δČech c=0.

Como H²(S³;R)=0, pode-se subtrair uma cocadeia constante de b_ij e eliminar c_ijk. Em encontros quádruplos, a diferença de c' tem ghost −1, é s-fechada e, por H⁻¹ local=0, é s-exata. Não há um próximo encontro de multiplicidade cinco. Obtém-se assim uma cocadeia total finita B de grau 1 com

\[
(\delta_{\check C}+(-1)^{\mathrm{deg}_{\check C}}s)B=\alpha.
\tag{5.3}
\]

Para convertê-la numa seção global, use a contração de Čech determinada pela partição de unidade. Comece pelo maior grau de Čech e subtraia o diferencial total de sua contração; repita para os graus 2 e 1. A parcela produzida por s inclui **exatamente** (5.1). Após essas três eliminações sobra uma seção global β com sβ=α. Todas as somas, derivadas e integrações de coeficientes suaves anteriores são finitas. A cobertura finita dá um máximo finito das ordens/pesos das expressões utilizadas.

O mesmo argumento prova globalmente H^q(\(\mathcal B\),s)=0 para q<0. Em grau 0, constantes locais se identificam nos encontros e dão uma única constante, pois S³ é conexo; os restos negativos colam pelo mesmo procedimento. Logo,

\[
H^2(\mathcal B,s)=0,\qquad H^0(\mathcal B,s)=\mathbb R,\qquad
H^{q<0}(\mathcal B,s)=0
\tag{5.4}
\]

globalmente no alvo.

Esse passo não elimina H³(S³): o volume do alvo continua uma possível classe de grau total 3. O que foi utilizado foi somente a ausência da obstrução de grau 2. Tampouco se está calculando a cohomologia de de Rham do espaço-tempo físico: trata-se de operadores locais naturais sem formas externas de espaço-tempo.

## 6. Retirada explícita dos ghosts de Lorentz em grau dois

Seja \(\mathcal B_{\rm bas}\) o subcomplexo Lorentz-invariante e independente de \(\widehat C\). Escreva

\[
s=\delta+s_1+\gamma_L+s_2,\quad
s_1=\widehat\xi^aD_a,\quad
s_2=\widehat F^I\partial_I,\quad
\widehat F^I={1\over2}\widehat\xi^a\widehat\xi^bR_{ab}{}^I,
\quad\partial_I={\partial\over\partial\widehat C^I}.
\]

As identidades de Cartan são

\[
\{s,\partial_I\}=L_I,\qquad [L_I,s]=0.
\tag{6.1}
\]

Considere α∈\(\mathcal B_{\rm bas}\), gh(α)=2, sα=0. Por (5.4), α=sβ. Projete β no tipo Lorentz trivial, como na seção 4. De (6.1), s(∂_Iβ)=0. O grau é zero. Portanto

\[
\partial_I\beta=d_I+s\beta_I.
\tag{6.2}
\]

O possível d_I é constante e transforma no coadjunto. Como so(1,3) é semissimples, um covetor invariante do adjunto é zero: d_I[X,Y]=0 e [\(\mathfrak g,\mathfrak g\)]=\(\mathfrak g\). Assim d_I=0. As primitivas β_I podem ser escolhidas com transformação coadjunta por projeção tensorial finita.

Diferencie (6.2) e simetrize I,J. A anticomutação das ∂_I e a transformação coadjunta implicam

\[
s\bigl(\partial_{(I}\beta_{J)}\bigr)=0,\qquad
\mathrm{gh}\bigl(\partial_{(I}\beta_{J)}\bigr)=-2.
\]

Por (5.4), existe β_IJ simétrica, no tipo tensorial correspondente, com

\[
\partial_{(I}\beta_{J)}=s\beta_{IJ}.
\tag{6.3}
\]

Não há constante nesse grau negativo. Ponha X₀=X|_{\widehat C=0} e defina a expressão finita

\[
\boxed{\widehat\beta=\beta_0+
 \widehat F^I(\beta_I)_0+
 \widehat F^I\widehat F^J(\beta_{IJ})_0.}
\tag{6.4}
\]

Então α=sβ̂. Para conferir: a componente sem C de α=sβ é
α=sβ₀+F^I(∂_Iβ)₀. Substituir (6.2) retira o segundo termo por s[F^I(β_I)₀], deixando F^IF^J(∂_(Iβ_J))₀. Substituir (6.3) produz o último termo de (6.4). O resto contém F³, que é zero pois possui seis ξ anticomutantes em dimensão quatro. A identidade (δ+s₁)F=0 e as contrações invariantes justificam cada passagem do s através dos F.

β̂ é global no alvo, Lorentz-invariante, sem C, finita e da classe de coeficientes desejada. Isso prova que a inclusão do complexo básico no completo é injetiva em grau 2 neste modelo. A inexistência de tr R é consequência do cálculo (6.2), não foi usada como slogan para saltar a prova de existência da primitiva básica.

## 7. Retorno à forma característica e simetria do alvo

Dada ρ₂ natural com d_Hρ₂≈0, substitua dx por ξ em seus índices de forma. A igualdade fraca tem um certificado KT covariante de L0/L2. Levante sucessivamente o representante por termos de ξ-graus 3 e 4, de antifield 1 e 2. A aciclicidade KT elimina cada obstrução; ξ⁵=0 termina a construção. Obtemos α∈\(\mathcal B_{\rm bas}\), gh2, sα=0, com parte sem antifields igual a ρ₂(ξ).

A seção 6 dá α=sβ̂. A parte sem antifields e de ξ-grau 2 dessa igualdade é

\[
\rho_2(\xi)=s_1\widehat\beta_{[0,1]}+
 \delta\widehat\beta_{[1,2]}.
\]

Na superfície estacionária, a última parcela some. Repondo dx no lugar de ξ resulta ρ₂≈d_Hβ₁, provando (1.1).

Se o problema impõe invariância sob SO(4) ou O(4) no alvo, pode-se agora fazer a média compacta da **primitiva global suave já construída**, juntamente com seu certificado KT. O grupo age naturalmente nos jatos e comuta com s,d_H e as equações. A média preserva grau polinomial e ordem finita; uma cobertura compacta controla as derivadas dos coeficientes. Isso entrega uma primitiva com a simetria requerida. Não se faz média de germes formais, não se translada uma série de y₀ para outro ponto e não se confunde invariância rígida O(4) com gauge local no alvo.

## 8. Aplicação, controles e fronteira

[DERIVED — composição das demonstrações escritas] L0/L2 são precisamente o resultado KT069; L1 é o resultado ordinário071. Portanto o transporte acima retira o resíduo **H²_char,cov suave global no alvo S³**, na classe natural explicitada. Não depende de uma escolha de solução com simetrias, da parametrização FLRW nem de uma região de posto máximo de dφ.

Controles que delimitam o teorema:

- Num alvo com H² não nulo, o passo (5.2) pode falhar; uma forma alvo global fechada pode fornecer a obstrução. A prova usa S³ concretamente.
- Com gauge abeliano, d_I em (6.2) pode sobreviver e produzir um representante de Chern–Weil de grau 2; a primitiva completa não teria necessariamente uma primitiva básica.
- Uma prova que use somente normalidade formal e depois avalie y não verifica L1. Nossa projeção (4.3) trunca antifields por contagem de ghosts; não trunca uma série de valores materiais.
- Uma álgebra que só exista em dy de posto máximo é diferente da utilizada. Não autorizaria a prova universal de reducibilidade nem os controles em mapas constantes.
- O setor é Einstein–sigma ambiente com Levi-Civita. Não inclui torção/espinores, gauge adicional, bordos, classes globais discretas ou mudança do espaço de contratermos.

A redução de anomalias do arco 070 pode consumir (1.1) dentro do complexo exato que foi definido. A transferência ao espaço admissível de contratermos da renormalização e a QME interagente continuam sendo enunciados distintos. Nenhuma conclusão experimental ou de completude UV decorre desta nota.

A rota alternativa por filtragem do número de jatos positivos não foi necessária: congelar y nesse argumento deixaria classes de 1-formas e 2-formas materiais, cujo diferencial seguinte seria de Rham do alvo. Não se declara uma classificação do complexo covariante livre que não foi demonstrada. A presente rota utiliza a exatidão ordinária efetiva e paga separadamente a covariantização e a colagem.
