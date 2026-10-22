# Ação BV em dimensão continuada e rota perturbativa de renormalização

10/09/2026. [DERIVED — aplicação escrita ao modelo] [KNOWN — resultado de renormalização identificado]. Esta nota cria uma rota adicional para a anomalia efetivamente produzida. A classificação suave covariante de todas as classes possíveis permanece um problema próprio.

## 1. Objeto e domínio

Mantemos a ação ambiente Einstein–sigma das entregas 067–070, com alvo S³ redondo, três coordenadas materiais locais y, métrica lorentziana e apenas difeomorfismos como gauge. Não acrescentamos fermions quirais, gauge de Weyl ou campos de formas superiores. A ação de quatro dimensões é

\[
 S[g,y]=\int dV_g\left[-\frac{R-2\Lambda}{2\kappa}
       +\frac c2 g^{\mu\nu}h_{AB}(y)\partial_\mu y^A\partial_\nu y^B\right].
\tag{1}
\]

A relação κc=4 pertence ao modelo considerado. Ela não é necessária à identidade BV desta nota. A origem da ação e sua correspondência física com os dados selecionados conservam os estatutos das entregas anteriores.

Usamos D=4−ε como parâmetro da álgebra tensorial de regularização dimensional. Isso não descreve uma variedade física com número fracionário de coordenadas. Índices de espaço-tempo, contrações métricas e integrais de momentos são continuados pelo esquema; os índices internos A,B do alvo continuam tendo dimensão três. A construção é local e perturbativa. Não afirma uma rotação global de Wick do habitante I×S³.

## 2. Extensão explícita e identidade clássica exata

[DERIVED] Defina

\[
 S_D=\int d^Dx\sqrt{|g|}\left[-\frac{R-2\Lambda_D}{2\kappa_D}
       +\frac{c_D}{2}g^{\mu\nu}h_{AB}(y)\partial_\mu y^A\partial_\nu y^B\right].
\tag{2}
\]

Os parâmetros bare são tomados como independentes nesta identidade. Se y é adimensional, [κ_D]=2−D, [c_D]=D−2 e [Λ_D]=2 em unidades de massa. Assim κ_D c_D é adimensional e pode valer quatro também na extensão. Os fatores de escala usados para definir parâmetros renormalizados são tratados depois; não se introduz um termo finito proporcional a ε para corrigir uma identidade que já é exata.

Seja s uma derivação ímpar à esquerda, com

\[
\begin{aligned}
 s g_{\mu\nu}&=C^\rho\partial_\rho g_{\mu\nu}
       +(\partial_\mu C^\rho)g_{\rho\nu}
       +(\partial_\nu C^\rho)g_{\mu\rho},\\
 s y^A&=C^\rho\partial_\rho y^A,\qquad
 s C^\mu=C^\rho\partial_\rho C^\mu,\\
 s\bar C_\mu&=-b_\mu,\qquad s b_\mu=0.
\end{aligned}
\tag{3}
\]

O último par mantém a convenção não minimal da entrega 069. Os coeficientes h_AB(y) transformam pela regra da cadeia; h é um tensor fixo do alvo, não um novo campo de gauge.

**Nilpotência.** Em y, os dois termos com (∂C)C se cancelam e o termo C^ρ C^σ ∂_ρ∂_σ y é zero por antissimetria. O mesmo cálculo no vetor C deixa apenas termos cancelados por renomeação de índices e antissimetria. Para g, a representação tensorial da derivada de Lie dá a mesma identidade de álgebra de difeomorfismos. Nenhum passo conta quatro índices, usa dualidade de Hodge específica de quatro dimensões ou uma matriz de quiralidade. O par não minimal é evidentemente nilpotente.

**Invariância da ação.** A transformação do determinante fornece

\[
 s\sqrt{|g|}=\partial_\rho(C^\rho\sqrt{|g|}).
\]

R e Q=g^{μν}h_AB(y)∂_μy^A∂_νy^B são escalares de espaço-tempo. Em Q, as derivadas do ghost provenientes de g inversa e dos dois diferenciais do mapa cancelam; os termos de h são C^ρ∂_ρh. Logo sQ=C^ρ∂_ρQ, e vale a identidade análoga para R. Portanto s da densidade de (2) é sua divergência de Lie. A integral desaparece módulo divergências, ou com suporte compacto nas variações. Esse argumento vale para qualquer dimensão inteira permitida e é uma identidade tensorial na continuação D.

Introduza antifields para Φ=(g,y,C,bar C,b) e a ação mínima estendida

\[
 \Sigma_D=S_D+\langle\Phi^*,s\Phi\rangle.
\tag{4}
\]

O pareamento graduado é escolhido com a convenção canônica sΦ=(Φ,Σ_D); a posição das fontes ímpares segue essa convenção. Separar o anticolchete por grau de antifield mostra que (Σ_D,Σ_D) tem coeficiente de grau zero igual a 2sS_D e coeficientes lineares proporcionais a s²Φ. Pelas identidades anteriores,

\[
 (\Sigma_D,\Sigma_D)=0
\tag{5}
\]

**exatamente na álgebra regularizada**, e não somente até O(ε). A igualdade vale módulo divergências com a mesma convenção de funcionais locais.

## 3. Gauge, coordenadas do alvo e o fundo

Uma escolha de gauge de Donder usa a métrica de fundo gbar, q=g−gbar e

\[
 F_\mu=\bar\nabla^\nu q_{\mu\nu}
          -\tfrac12\bar\nabla_\mu(\bar g^{\rho\sigma}q_{\rho\sigma}),
\quad
 \Psi_D=-\int dV_{\bar g}\,\bar C^\mu
       \left(F_\mu-\frac{b_\mu}{2\ell_D}\right),
\quad \ell_D=\frac1{2\kappa_D}.
\tag{6}
\]

O fator 1/2 em F é a escolha de gauge e faz sentido em qualquer D; não é uma projeção que deva ter traço zero. A transformação canônica de fontes gerada por Ψ_D preserva (5). Assim o gauge não produz um defeito evanescente na equação clássica. Os dados de fundo são fixos sob s e transformam conjuntamente sob mudanças externas de coordenadas; isso não prova independência de fundo.

Uma mudança suave invertível de coordenadas do alvo, com o correspondente levantamento cotangente, também preserva (5). Na expansão em torno de ybar, a coordenada geodésica y=Exp_ybar ξ é usada apenas como série formal invertível em ξ. Isso fornece a mesma descrição perturbativa do sigma empregada na bancada. Não se integra sobre uma única carta para representar silenciosamente todos os mapas globais.

No entorno de um mapa constante, κc=4 permite escrever y=Exp_y0(√κ ξ/2) e g=η+√κ q. O termo cinético sigma quadrático é então (1/2)h_y0(∂ξ,∂ξ). A escala de interação da matéria é √κ/2, e a gravitacional é √κ. Essa parametrização deixa explícita a expansão EFT; uma truncatura precisa controlar também a ordem em campos externos e nos acoplamentos, além das derivadas. A constante cosmológica é conservada como parâmetro. Expandir em um fundo que não a satisfaz mantém os termos lineares; esta nota não os descarta.

## 4. O resultado importado e a aplicação delimitada

[KNOWN] Anselmi constrói renormalização e extensão de parâmetros para uma ação que satisfaz a identidade BV exatamente no regulador dimensional. O algoritmo não exige previamente a classificação cohomológica dos contratermos. A subtração local mantém a identidade ordem a ordem; completar os parâmetros permite organizar os termos gerados e sua dependência de escala. Em teorias sem renormalizabilidade por contagem de potências, usam-se truncaturas compatíveis. [Anselmi, 1301.7577v2, identidade (1.6), §3 e §4](https://arxiv.org/pdf/1301.7577v2).

[DERIVED — aplicação] As equações (2)–(6) fornecem a hipótese algébrica do regulador para o Einstein–sigma bosônico. No esquema perturbativo dimensional da fonte, incluindo localidade das subtrações e o tratamento infravermelho requerido, a aplicação dá uma rota de renormalização com identidade BV para este modelo e sua extensão EFT. Não é necessário, nessa rota, que todo candidato formal de anomalia seja trivial: a ação regularizada controla a quebra que os próprios diagramas produzem.

A conclusão importada pertence ao esquema declarado. Não identificamos o funcional 1PI Γ renormalizado dessa construção com a álgebra causal curva Q2 sem um mapa de comparação. Tampouco identificamos a equação (Γ,Γ)=0 com a existência de um estado físico positivo ou de uma medida funcional convergente. A relação com a equação mestra quântica de Q2 exige o mesmo dicionário de fontes, produtos renormalizados e contatos.

O uso da fonte não fixa um número finito de parâmetros do modelo completo. Sua extensão pode modificar o setor de fontes e os representantes do gauge. A equivalência do gauge renormalizado com a apresentação geométrica original requer controle próprio; a nota não o declara automaticamente. Os coeficientes finitos continuam sendo dados de renormalização.

Não invocamos aqui o teorema Adler–Bardeen de 1501.07014 como um atalho incondicional: seu enunciado tem hipóteses cohomológicas e de truncatura próprias. A aplicação acima usa a identidade exata de (5) e o esquema de 1301.7577, nos limites descritos.

## 5. A diferença entre uma identidade exata e um erro pequeno em ε

[DERIVED] A precisão de (5) é material. Uma quebra εB pode produzir um termo finito se um polo 1/ε a multiplica. Portanto uma verificação somente em D=4 não forneceria a hipótese necessária. Aqui a invariância segue de identidades de difeomorfismos sem uma operação dependente de D=4. Não há γ5, projetor quiral ou tensor epsilon de espaço-tempo na ação ou no gauge escolhidos.

Já a redução de contratermos da entrega 070 **usa quatro dimensões**, equações de movimento e integrações por partes. Ela não deve ser aplicada a um integrando regularizado antes de extrair os polos. Em particular, o termo de Euler é topológico em quatro dimensões; sua extensão como combinação de contrações de curvatura em D não pode ser simplesmente retirada por esse motivo. Produtos entre termos evanescentes e polos podem afetar subtrações posteriores. Isso não muda os coeficientes de 070 em seu alcance, mas determina como a sessão que codifica deve tipar um futuro regulador.

O valor de C4 de ghost zero também não é, por definição, a anomalia BV de ghost um. A prova dimensional e o cálculo do calor são objetos distintos, com funções distintas na construção.

## 6. Contrato concreto para transportar a rota à Q2

[DERIVED — lema condicional de transporte] Suponha que uma construção T_DR tenha sido realizada para os mesmos campos, fontes e fundos da Q2 e satisfaça seus axiomas de localidade, suporte, causalidade, realidade graduada e dependência suave/covariante. Suponha ainda uma equivalência de renormalização local admissível Z entre T_DR e os produtos de Q2, incluindo as inserções BV e os termos de contato. Se T_DR satisfaz a identidade quântica pertinente, transportar a ação, as inserções e a operação BV pela mesma equivalência fornece essa identidade na apresentação de Q2. A conclusão segue conjugando a identidade pelo isomorfismo; transportar somente a ação, deixando as inserções inalteradas, não é a hipótese do lema.

O lema especifica o elo seguinte, mas não constrói T_DR em espaço-tempo curvo nem Z. Em ordem n, quando as ordens inferiores já estão casadas, a diferença admissível é local; o respectivo contratermo é a informação que permite comparar as quebras naquela ordem. Essa diferença precisa ser calculada ou produzida por um teorema de comparação com hipóteses verificadas.

[OPEN] Nesta entrega permanecem: realização do esquema dimensional com os axiomas da família causal curva; identificação das inserções e contatos; transporte das normalizações; globalização no alvo e comparação entre fundos. A ação regularizada explícita paga a entrada algébrica dessa rota. Ela não é anunciada como QME interagente já satisfeita na Q2 da bancada.

## 7. Especificação para integração futura

Uma implementação deve distinguir pelo menos estes objetos:

- `dimensional_classical_bv_identity`: a identidade escrita (5), com D simbólico e sem redução de quatro dimensões;
- `dimensional_renormalization_scheme`: o resultado importado e suas hipóteses analíticas/perturbativas;
- `causal_scheme_comparison`: o mapa de produtos, fontes e contatos, ainda por construir;
- `causal_quantum_master_identity`: a identidade na Q2, que depende da comparação ou de outra prova direta;
- `finite_coupling_conditions` e `uv_completion`: obrigações próprias, que a renormalização EFT não substitui.

O registro deve conservar o fato de que a discussão é perturbativa e permite novos parâmetros. Nenhum gate canônico é movido por esta nota. Nenhum programa um.py foi executado ou importado. Não há compilação Lean, cálculo novo de diagramas ou controle simbólico executado nesta construção escrita.
