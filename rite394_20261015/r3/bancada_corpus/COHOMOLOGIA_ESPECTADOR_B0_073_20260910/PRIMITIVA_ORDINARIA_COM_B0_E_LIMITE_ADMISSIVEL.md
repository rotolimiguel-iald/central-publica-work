# Primitiva ordinária com B0 inerte e limite de admissibilidade

10/09/2026, arco073. [DERIVED — demonstração escrita com entradas071 delimitadas]. Nenhuma fonte anterior alterada. Zero CAS/Lean e nenhum um.py executado/importado.

## 1. Resultado

Um fundo B0 inerte para BRST não precisa ser inerte para a derivada horizontal. Mantendo d_HB0 e todos os seus jatos, provamos:

**Teorema ordinário.** Na classe coordenada local, suave nos valores e de ordem finita/polinomial nos jatos diferenciados, acrescentar jatos externos livres de uma métrica Lorentziana temporalmente orientada e de um mapa para S³ não cria uma classe de H¹,⁴(s|d_H) para o complexo completo Einstein–sigma de071. Toda quebra que seja um cociclo nessa álgebra ampliada possui uma primitiva ordinária nessa mesma álgebra.

Há uma versão no quociente pelo ideal diferencial completo das equações Einstein–sigma de B0, consumindo os resultados horizontais071 desse segundo sistema. Ela exige uma identidade no espaço estacionário universal, não apenas uma igualdade avaliada no FRW escolhido.

O teorema não fornece automaticamente a primitiva natural, com a condição analítica/escala específica ou contínua numa determinada completação de flutuações exigida por Q2. A seção8 demonstra concretamente por que a homotopia coordenada não pode ser chamada natural. Este é um avanço cohomológico preciso, não a QME.

Entradas:

- [Corolário H5_071](<C:/IALD/Central de Patentes/Chatgpt/COVARIANTIZACAO_SUAVE_071_20260910_001058_826723/COROLARIO_H5_E_ANOMALIA_LOCAL.md>), sobretudo §§1–3: H⁵(s,A_sm)=0 e distinção de classes.
- [Covariantização071](<C:/IALD/Central de Patentes/Chatgpt/COVARIANTIZACAO_SUAVE_071_20260910_001058_826723/COVARIANTIZACAO_E_H2_GLOBAL.md>) e [graus zero/um](<C:/IALD/Central de Patentes/Chatgpt/M2_SUAVE_RELATIVO_071_20260910_000347/COROLARIO_H0_H1_E_FINITUDE.md>): os graus baixos e sua finitude.
- [Retração072](<C:/IALD/Central de Patentes/Chatgpt/RETRACAO_BRST_FUNDOS_072_20260910_003743_284187/RETRACAO_RELATIVA_E_CONTRATO_CAUSAL.md>) e [Ward de referência072](<C:/IALD/Central de Patentes/Chatgpt/COMPARACAO_CAUSAL_FUNDOS_072_20260910/TRANSPORTE_E_WARD_REFERENCIA.md>): delimitam o espectador que sobrou.

As entradas071 são consumidas, não reexecutadas ou promovidas a uma nova auditoria Lean. O manifesto mede os arquivos referidos antes e depois.

## 2. Álgebra, diferenciais e retirada do setor não mínimo

Trabalhe numa carta contrátil U⊂ℝ⁴. Φ denota vielbein, mapa sigma, ghosts difeomórficos/Lorentz e antifields mínimos dos CAMPOS COMPLETOS. A apresentação métrica pode ser comparada à de vielbein no escopo já declarado071. Use coeficientes C∞ conjuntos nos valores de Φ e B0, não apenas somas finitas de produtos separados. Os jatos diferenciados, ghosts e antifields permanecem polinomiais finitos.

B0=(g0,φ0) tem ghost zero, sem antifields próprios e sem ação por s:

\[
s(B_{0,I}^A)=0,\qquad
d_H B_{0,I}^A=dx^\mu B_{0,I\mu}^A.
\tag{1}
\]

Os valores g0 ficam no espaço de métricas Lorentzianas da assinatura adotada, com orientação temporal; φ0 fica em S³. Todos os jatos externos são livres na primeira versão do teorema.

Primeiro desfaça o gauge por sua transformação canônica. Depois contraia os pares não mínimos c̄,b e os pares conjugados, com todos os jatos. Para pares tipados su=v,sv=0, o operador h=Σu_I∂/∂v_I, dividido pelo grau positivo do par, dá sh+hs=N. Seu prolongamento comuta com as derivadas totais, de modo que a contração vale modulo d_H; seus coeficientes podem depender de B0.

Essa ordem é necessária. No dicionário gauge fixado, s c̄=−b não contém a derivada de Lie; portanto a identidade de translação de ghosts usada abaixo não vale diretamente sobre c̄. A contração remove o setor antes de aplicá-la. Após obter uma primitiva mínima, o homotópico relativo e a conjugação de gauge restauram a apresentação completa. [KNOWN] O mecanismo de pares contráteis está em [BBH2000, Apêndice2.B](https://arxiv.org/pdf/hep-th/0002245v3).

## 3. Conjugação que conserva d_HB0

No complexo mínimo, s depende dos campos dinâmicos, não de B0. Separe

\[
d_H=d_{\rm dyn}+d_{\rm ext},\qquad
d_{\rm ext}=dx^\mu\left(\frac{\partial}{\partial x^\mu}
 +\sum_{A,I}B_{0,I\mu}^A\frac{\partial}{\partial B_{0,I}^A}\right).
\tag{2}
\]

d_dyn prolonga apenas jatos dinâmicos. Em (2), esses jatos são variáveis independentes e ficam constantes para d_ext; não são funções avaliadas de x. Ambos os operadores anticomutam com s com a convenção de grau total.

Se c^μ é o ghost difeomórfico em suas coordenadas originais, defina o operador de grau total zero

\[
b=dx^\mu\frac{\partial_L}{\partial c^\mu},
\quad b(\partial_Ic^\mu)=0\quad(|I|>0),
\tag{3}
\]

e b=0 nos demais geradores. A ação mínima de difeomorfismos sobre campos/antifields implica

\[
[b,s]=d_{\rm dyn},\qquad
[b,d_{\rm dyn}]=[b,d_{\rm ext}]=0.
\tag{4}
\]

Pode-se conferir (4) em cada gerador: ao substituir o ghost NÃO derivado por dx no termo c^μ∂_μΦ, sobra d_dynΦ; as partes com derivadas de c dão zero, assim como a parte KT sem ghosts. No ghost, sc^μ=c^ν∂_νc^μ fornece dx^ν∂_νc^μ. Os ghosts Lorentz e os antifields mínimos também contêm a parte de transporte correspondente. Para B0 e x, [b,s] é zero, razão pela qual d_ext não pode ser omitido.

[KNOWN] (3)–(4) sobre os geradores dinâmicos são a identidade de [BBH1995, equações6.7–6.8](https://arxiv.org/pdf/hep-th/9505173v2). A extensão com o termo d_ext é o cálculo desta nota.

Como b eleva o grau de forma, b⁵=0 em quatro dimensões. A série exponencial é finita; os comutadores seguintes de (4) se anulam. Portanto

\[
\boxed{s+d_H=e^b(s+d_{\rm ext})e^{-b}.}
\tag{5}
\]

Em particular, sobre B0 o lado direito vale d_extB0=d_HB0. Esta é a diferença em relação ao argumento incorreto que trataria B0 como uma constante numérica na descida.

## 4. As entradas de cohomologia dinâmica e externa

### Parte dinâmica

Na álgebra A_sm de071, precisam-se somente de

\[
H^1(s,A_{\rm sm})=H^2(s,A_{\rm sm})=H^5(s,A_{\rm sm})=0.
\tag{6}
\]

O último é o corolário H5. Os graus1/2 seguem da mesma decomposição: GL⁺₄ tem cohomologia real somente nos graus0,3,6; no fator covariante os graus1/2 foram eliminados pelo cálculo horizontal baixo e KT de071. Não há classe GL de grau1/2 que acrescente um termo. A ausência de graus negativos após a redução e as homotopias finitas são as entradas das notas referidas.

O uso com parâmetros C∞ conjuntos em B0 requer uma precisão. As contrações KT, dos pares, de de Rham/Hodge no valor do vielbein e a colagem no alvo usadas071 atuam nas variáveis dinâmicas. Os parâmetros externos podem ficar fixos durante essas operações. Elas preservam suavidade paramétrica; polinômios finitos nos jatos externos continuam finitos. Não se substitui C∞ conjunto por um produto tensorial algébrico inadequado. Não é afirmada uma cota universal de ordem para todas as primitivas.

### Parte externa livre

O complexo d_ext é exatamente o horizontal do fibrado de B0, com os demais símbolos como parâmetros. Para q<4, sua cohomologia ordinária é a de de Rham do espaço de valores/base. [KNOWN] Usamos [Giachetta–Mangiarotti–Sardanashvily, Proposições13–14 e Teorema18](https://arxiv.org/pdf/math/0006074): a comparação vale com ordem finita de jatos. O caráter polinomial nos jatos diferenciados é preservado pelas homotopias locais, e colagens suaves nos valores não acrescentam uma série de derivados.

Sobre U contrátil, os valores externos são Y0≃L⁺×S³. O espaço L⁺ das métricas Lorentzianas com orientação temporal tem o tipo de homotopia de S³. Uma descrição concreta escolhe uma métrica euclidiana auxiliar: a linha própria positiva, com sinal futuro, fornece v∈S³; seu autovalor positivo e a forma negativa no complemento são fibras contráteis. Deformar esses fatores a1 e −Id preserva a assinatura. A escolha euclidiana serve à prova ordinária; não foi declarada natural. Se se usa vielbein de fundo, GL⁺₄ substitui L⁺ e também não tem H¹/H² reais.

Assim, com coeficientes reais ou complexos,

\[
H^1_{\rm dR}(Y0)=H^2_{\rm dR}(Y0)=0,\qquad
\boxed{H^1(d_{\rm ext})=H^2(d_{\rm ext})=0.}
\tag{7}
\]

Não se exige H³(d_ext)=0: as classes de S³ são conservadas.

Controle de finitude local: em uma carta convexa de valores externos, contraia diferenças z=B0−B* para um valor B* admissível, nunca uma métrica nula. O homotópico horizontal polinomial de BBH2000 §4.5 usa operadores D⁺ que reduzem a contagem de derivados e uma soma

\[
\eta_{q-1}=
\sum_{m=0}^{\bar m}
\frac{(-1)^m\rho P_m\widetilde\omega_q}
     {(4-q)(5-q)\cdots(4-q+m)}
\quad(d_{\rm ext}\widetilde\omega_q=0),
\tag{8}
\]

onde P_m contém m operadores D⁺ e m derivadas totais e ρ=D⁺ν∂/∂dx^ν. A contagem finita de derivados do polinômio dá P_{\bar m+1}=0; para q=1,2 os denominadores não se anulam. O resíduo sem campos externos é tratado pela homotopia ordinária em x. [Fonte primária para essa fórmula e a finitude, BBH2000, Teorema4.2/equações4.12–4.16](https://arxiv.org/pdf/hep-th/0002245v3).

As integrações são em parâmetros de contração dos valores/jatos, não na configuração B0 avaliada em outros pontos do espaço-tempo. Os resultados globais em valores de (7) seguem pela comparação de de Rham e a exatidão finita citada; os operadores/colagens podem ser escolhidos independentemente dos parâmetros dinâmicos, preservando a dependência suave conjunta. Suavidade e finitude não implicam, aqui, naturalidade ou a cota de escala particular de Q2.

## 5. Eliminação dos cinco canais

Pela (5), calcule o grau total cinco de s+d_ext. Filtre pelo grau de forma q, de0 a4. A primeira página toma H(s), e o próximo diferencial é induzido por d_ext nos coeficientes externos. Não é necessário declarar colapso completo da sequência.

| Ghost dinâmico p | Forma externa q | Canal de grau total5 | Razão da eliminação |
|---|---:|---|---|
| 5 | 0 | H⁵(s) | (6) |
| 4 | 1 | H¹(d_ext;H⁴(s)) | (7), com parâmetros |
| 3 | 2 | H²(d_ext;H³(s)) | (7), com parâmetros |
| 2 | 3 | H²(s) | (6), mesmo que H³ externo não seja zero |
| 1 | 4 | H¹(s) | (6), sem precisar calcular Lagrangianas externas de grau4 |

Todos os termos dessa diagonal são zero, no máximo na segunda página. Páginas posteriores são subquocientes e não recriam esses termos. A filtração tem cinco graus de forma, logo a convergência na diagonal é finita, inclusive quando a álgebra contém antifields. Segue

\[
\boxed{H^5(s+d_H)=H^5(s+d_{\rm ext})=0.}
\tag{9}
\]

Isto também fornece um algoritmo para uma primitiva de uma forma total Ω de grau5. Depois de conjugar por e⁻ᵇ:

1. Remova q=0 com uma primitiva s de ghost5.
2. Em q=1, use (7) no H⁴(s) para retirar sua classe por um termo d_ext de q=0; retire o restante s-exato.
3. Em q=2, faça o mesmo no H³(s), usando o segundo grupo de (7).
4. Remova q=3 e q=4 por H²(s)=0 e H¹(s)=0.
5. Conjugue de volta por eᵇ.

Em cada remoção os termos novos têm grau de forma maior; não se reinicia indefinidamente a etapa anterior. Há apenas esses cinco estágios e um número finito de levantamentos. As primitivas utilizadas têm ordem finita elemento a elemento, pelas entradas e (8). Não é uma afirmação sobre um inverso diferencial não local no espaço-tempo.

## 6. Retorno à anomalia a¹₄

Se sa¹₄+d_Ha²₃=0, complete a descida nas formas de grau3,2,1,0. O lema horizontal abaixo do grau máximo não tem classes de ghost positivo: as possíveis classes topológicas dos valores dos campos/B0 têm ghost zero, enquanto ghosts/antifields são fibras contráteis para essa comparação horizontal. Isso fornece uma forma total Ω₅ fechada por s+d_H cuja componente superior é a¹₄.

Pela (9), Ω₅=(s+d_H)Θ₄. Extraindo a componente de ghost1/forma4,

\[
\boxed{a^1_4=s\,b^0_4+d_Hb^1_3.}
\tag{10}
\]

As primitivas pertencem à álgebra coordenada ampliada com jatos de B0. A dependência global nos valores S³ de ambos os mapas é mantida. O enunciado é local no espaço-tempo; não se afirma uma cohomologia global em M arbitrário. Após restaurar os doublets não mínimos e o gauge, a exatidão ordinária permanece.

Não aplicamos diretamente a isomorfia6.15 de BBH1995 com B0 tacitamente constante. Em seu lugar, (5)–(9) calculam os termos externos adicionais que essa tentativa teria omitido.

## 7. Três sentidos de “B0 on-shell”

### A. Identidade com jatos externos livres

É o teorema acima. Se a_ref possui um levantamento que seja cociclo nessa álgebra, (10) se aplica. Uma avaliação posterior em qualquer B0 suave, on-shell ou não, é um mapa que comuta com s e d_H e preserva a identidade. A escolha de uma solução depois da prova não a invalida.

### B. Identidade no espaço estacionário UNIVERSAL de B0

Pode-se, em vez disso, trabalhar no quociente pelo ideal diferencial completo Einstein–sigma de B0, sem misturá-lo às equações dos campos dinâmicos. Como sB0=0, o ideal é s-estável; por ser diferencial, é d_ext-estável. A conjugação (5) desce a esse quociente.

Nesse caso (7) precisa ser substituído por H¹_char(B0)=H²_char(B0)=0. As entradas M2/H0H1 de071 fornecem justamente a exatidão coordenada nesses graus em cartas de valores, com finitude. Sua globalização ordinária nos valores usados aqui pode ser vista pelas mesmas etapas: os levantamentos de contato enviam as formas horizontais de graus1/2 a formas totais fechadas; os splits triangulares KT dão fibras estacionárias afins/contráteis por ordem; H¹/H² dos valores L⁺×S³ são zero. A contração de fibras e a primitiva de de Rham removem essas formas, conservando ordem finita por coeficiente. Não se impõe posto máximo de dφ0 nem um ansatz cosmológico.

Assim o mesmo argumento de cinco canais vale para um cociclo definido UNIVERSALMENTE nesse quociente. Ele pode ser avaliado na solução física. A palavra “fraco” aqui significa todos os jatos estacionários formais completos, como nas entradas071; não significa “a expressão zerou nesta solução”.

### C. Igualdade apenas numa referência FRW fixa

A consistência da Ward072 foi construída numa álgebra de referência particular. Para consumir A ou B como uma primitiva universal em jatos, é preciso mostrar que seu coeficiente local e a identidade de consistência constituem um cociclo na respectiva álgebra. A mera existência de uma fórmula com símbolos de curvatura não prova essa universalidade.

Se B0 é tratado somente como uma função fixa de x, a descida coordenada usual ainda pode fornecer uma primitiva como função de x. Ela pode, entretanto, depender de integrais dos valores da referência e não ser uma função de um número finito de jatos de B0. Esse procedimento não fornece a família local natural de contratermos Q2.

**Controle de que a distinção é real.** Considere um espectador z sujeito apenas a ∂₂z=∂₃z=∂₄z=0, com seus jatos em x¹ livres. A forma β=f(z)dx¹, f não constante, é horizontalmente fechada nesse quociente. Não existe F(x,z,z′,…,z^(N)) universal de ordem finita com d_HF=β. Na equação D₁F=f(z), o coeficiente do jato livre z^(N+1) força F_{z^(N)}=0; repetindo, F independe de todos os jatos e de z. Então D₁F não pode depender de z. Mesmo permitindo x explícito a contradição permanece.

Para uma única função z(x¹) escolhida, ∫f(z(u))du é uma primitiva ordinária; ela não é o F local universal inexistente. O exemplo não é Einstein–sigma nem uma anomalia gravitacional: demonstra por que uma família especial de referências pode mudar a cohomologia externa e por que avaliar antes não substitui o teorema de jatos. No caso B, a entrada M2 elimina precisamente os grupos relevantes para o sistema completo, e não para restrições arbitrárias.

## 8. A homotopia construída não é automaticamente natural

Há um teste concreto no próprio b da equação(3). Sob x′=f(x), escreva J^μ_σ=∂x′μ/∂xσ e K=J⁻¹. Os ghosts transformam por c′μ=J^μ_σcσ. Portanto

\[
\partial'_\nu c'^\mu
=K_\nu^\rho[(\partial_\rho J^\mu_\sigma)c^\sigma
             +J^\mu_\sigma\partial_\rho c^\sigma].
\tag{11}
\]

Aplicar b definido nas coordenadas antigas ao direito de (11) produz

\[
K_\nu^\rho(\partial_\rho J^\mu_\sigma)\,dx^\sigma,
\tag{12}
\]

em geral não zero. Mas definir novamente (3) em coordenadas primadas daria b′(∂′c′)=0. Logo essa receita não entrelaça automaticamente mudanças não lineares de coordenadas. A primitiva que ela entrega é coordenada; chamar b de operador natural seria incorreto.

Isso é uma obstrução à identificação de UMA homotopia com a homotopia admissível, não uma prova de que nenhuma primitiva natural exista. A covariantização073 ou outro argumento deve corrigir essa escolha e controlar sua classe. Também a métrica euclidiana auxiliar, os pontos de contração e eventuais partições suaves usadas na prova ordinária não são dados físicos que possam ficar silenciosamente em Q2.

A invariância O(4) diagonal de071 não basta: transporta φ e φ0 conjuntamente, deixando possíveis invariantes relativos. A média compacta pode projetar uma primitiva que JÁ seja global/admissível na família correta; não cria as propriedades que faltem.

## 9. Analiticidade, escala, suporte e completação

As primitivas de (10) são suaves e finitas em jatos. O método não prova que sejam racionais no vielbein; logaritmos suaves podem aparecer, como já explica o corolárioH5. Tampouco uma colagem C∞ preserva automaticamente a condição analítica forte que se escolha para Q2.

A equação(8) controla finitude, não o limite específico de escala de uma aplicação multilinear de renormalização. Homogeneidade em pesos, grau de fontes, número de pernas e as relações entre aridades/contatos precisam ser preservados por uma eventual construção admissível. Substituir jatos por funções suaves continua local no sentido de avaliação em um ponto; não basta para provar a hierarquia inteira dos mapas de normalização.

Para uma densidade testada por f, (10) gera também termos df. Estes permanecem e só desaparecem na região de cutoff constante. Não se inferiu suporte compacto de uma primitiva de de Rham global apenas porque a densidade original foi testada.

A nota prova o enunciado na álgebra local completa especificada. Aplicá-lo à série formal de flutuações de Q2 requer que o cociclo e a homotopia pertençam à mesma completação/filtração e que a operação seja contínua coeficiente a coeficiente. A exatidão de funções C∞ do campo completo não autoriza, sozinha, recentrar ou somar uma série formal em valores finitos. A organização Laurent com tadpoles da Ward072 continua válida; não foi substituída por uma convergência analítica.

## 10. Efeito sobre a pendência072

[DERIVED] O simples acréscimo dos jatos inertes de B0 não gera uma obstrução cohomológica ordinária nos graus necessários, desde que se trabalhe na álgebra livre universal ou no espaço estacionário completo da seção7B. A prova conserva d_HB0, fornece cinco estágios de remoção e mantém finitude. Portanto essa parte do problema deixou de ser apenas a observação “há um espectador”.

[OPEN] Para a anomalia de referência efetivamente construída072, ainda é preciso verificar seu enquadramento universal/completado e produzir a primitiva natural admissível com regularidade, escala e contatos de Q2. A translação de ghosts fornece um diagnóstico explícito do passo de covariância que não foi pago. Acordo perturbativo entre fundos, QME causal e setor físico interagente continuam resultados separados.

Nenhuma possibilidade de anomalia foi declarada não nula por este argumento; nenhuma ausência de teste foi convertida em confirmação. Os pins, as importações e os limites estão no manifesto desta pasta.
