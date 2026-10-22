[DERIVED / INPUT / OPEN] Continuação espontânea 010 — focalização por Ricci e balanço local, derivação anterior ao código, 05/09/2026.

A continuação 009 foi entregue e verificada. O túnel ainda termina na ordem 007. A árvore canônica nomeia H3 como entrada física. O último turno teve progresso: curvatura, Bianchi e G geométrico passaram no Lean, com manifesto e entrega próprios. O objetivo amplo continua ativo.

## Escolha do próximo elo

O próximo trabalho é derivar a identidade diferencial de Raychaudhuri na carta da bancada e demonstrar como um balanço local de calor e entropia força a contração de Ricci que a entrega 009 ainda recebe como hipótese. Não se afirmará que a primeira lei modular, isoladamente, fornece área, calor ou horizontes.

Nos fontes consultados:
- TriadMaster.lean define HorizonEquilibriumData com area_entropy e clausius como campos.
- ModularFirstLaw.lean prova HasDerivAt para entropia diagonal com perturbação de traço zero.
- TheImportedEquilibrium.lean fornece uma EquilibriumInput algébrica; a implicação física adicional continua parâmetro em the_trio_is_a_pair.
Esses tipos não serão confundidos entre si. Nenhum será editado.

## Derivação geométrica

Para campo V suave e conexão suave Γ, definir Bᵃᵢ=∂ᵢVᵃ+Γᵃᵢb Vᵇ, θ=tr B, a=BV e D_V f=Σᵢ Vⁱ∂ᵢf. As derivadas são as de Fréchet existentes, não novos jatos independentes.

1. Provar regras de derivação de vetores e produtos matriz-vetor.
2. Provar [∇ᵢ,∇ⱼ]V=FᵢⱼV a partir da curvatura já construída.
3. A derivada covariante mista de B é Cᵢ=∂ᵢB+ΓᵢB−BΓᵢ. Sob torção nula, Cᵢᵃⱼ−Cⱼᵃᵢ=(FᵢⱼV)ᵃ.
4. Produto e traço fornecem div a=tr(B²)+Σₐᵢ(Cₐ)ᵃᵢ Vⁱ. O traço de Cᵢ é ∂ᵢθ.
5. Contrair a identidade anterior: D_V θ=div a−tr(B²)−Ric(V,V).
6. Para a=0 em vizinhança e B=0 no ponto, segue D_V θ=−Ric(V,V) no ponto.

B=0 é uma hipótese de equilíbrio mais forte do que expansão e cisalhamento de tela nulos. Seu uso ficará expresso; existência de congruências nulas adequadas e identificação da expansão com área de tela não serão proclamadas por nomeação de funções escalares. A identidade completa do item 5 é independente dessa especialização.

## Elo analítico e físico

Para uma curva γ com γ'=V∘γ, transportar a derivada de θ por regra da cadeia. Para densidade A>0 obedecendo A'=θA, o equilíbrio implica A''(0)=−A(0)Ric(V,V). Uma condição local de calor tem sinal compatível com o ramo passado: Q'(λ)=−κ λ T(V,V)(γλ) A(λ). Comparar o termo quadrático da diferença de área orientada com Q, ou equivalentemente as derivadas de seus fluxos no ponto, sob balanço de Clausius. O cálculo deve incluir erros de ordem superior quando tipáveis, sem tornar uma aproximação igualdade exata.

Com temperatura κ/(2π), densidade de entropia η constante e não nula, κ≠0 e A(0)≠0, o alvo é Ric(V,V)=(2π/η)T(V,V). Em unidades ħ=1 e η=1/(4G), isso é 8πG. Não se buscará derivar o valor de κ. O balanço em todos os vetores nulos alimentará o teorema geométrico da entrega 009.

## Critérios e limites

A prova deverá distinguir claramente: identidade diferencial construída; condições de congruência; identificação de A com área de horizonte; identificação do fluxo com calor; lei de área e Clausius; passagem para todos os vetores nulos; conservação de T. Só obrigações efetivamente demonstradas serão marcadas pagas. Uma simples estrutura que assuma Ric(V,V)=κT(V,V) não satisfaz o alvo.

[KNOWN] Referência primária consultada: Ted Jacobson, Thermodynamics of Spacetime: The Einstein Equation of State, https://arxiv.org/html/gr-qc/9504004 . O artigo assume entropia proporcional à área, temperatura de Unruh e Clausius para horizontes locais; a identidade geométrica é usada para deduzir a equação de campo. Não fornece uma derivação de H3 a partir da identidade normalizada de um estado abstrato.

[OPEN] Origem quântica da geometria e da lei de área, H3 dinâmico, quatro dimensões, assinatura derivada, estrutura global e solução do objetivo amplo. Esta rodada não altera esse objetivo.

Escritas somente em Chatgpt. Originais, um.py, kernel canônico, Atlas, memórias e entregas seladas ficam intactos. Nenhum dado observacional. Tentativas falhas e backups de bytes serão preservados. A gerência fará a auditoria independente.

## Adendo prévio ao controle de não-vacuidade

Antes de acrescentar o habitante ao código: no caso plano g=η, Γ=0 e T=0, tomar V(y)=v constante e nulo, γ(t)=tv, A(t)=1, Q(t)=0, taxa=1. Então B=0 e a=0 identicamente, θ=0, as duas leis de derivação de área e calor têm lado direito zero e o resíduo integrado é zero. Isso fornece um habitante completo do novo contrato para qualquer densidade η e qualquer v nulo; escolher v=(1,1,0,0) garante um controle não nulo. Esse controle paga consistência do contrato, sem fornecer existência em geometria curva genérica. O controle negativo curvo reutiliza g=exp(2x⁰)η, Ric=diag(0,2,2,2) documentados antes do código na continuação 009.
