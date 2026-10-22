[REAL / INPUT / KNOWN / OPEN] Reconstrução tensorial condicional em domínio coordenado — continuação espontânea após a ordem 007, 05/09/2026.

## Resultado e enunciado exato

Foi construída uma cadeia de provas para tensores simétricos com componentes diferenciáveis em um domínio aberto preconexo U de ℝ⁴. O domínio pode ser vazio, caso trivial admitido pela biblioteca; para um domínio físico não vazio, a hipótese é a conexão usual. O referencial E(x) e sua inversa D(x) têm componentes diferenciáveis em U e satisfazem E D = D E = I. Definem-se efetivamente

    g(x) = E(x)ᵀ η E(x),       g⁻¹(x) = D(x) η D(x)ᵀ,
    η = diag(1,−1,−1,−1).

O teorema `conserved_null_tensor_is_constant_metric_multiple` prova:

    Aᵀ=A,
    g(v,v)=0 ⇒ A(v,v)=0 para todo v, em cada x∈U,
    div_g A=0, com a conexão de Levi-Civita construída de g
    ─────────────────────────────────────────────────────
    existe uma constante real c tal que A=cg em todo U.

Não há restrição diagonal para E, g ou A. O coeficiente c não é inserido como dado: primeiro constrói-se a função f(x)=(Dᵀ A D)₀₀, prova-se A=fg e sua diferenciabilidade, e então prova-se sua constância. Não se pede ao chamador uma testemunha diferenciável escondida na conclusão.

O corolário `conserved_null_balance_has_constant_term` aplica o resultado a A=G−κT. Assume G e T simétricos, componentes diferenciáveis, a anulação nula dessa diferença e a conservação separada de G e de T. A linearidade da divergência é demonstrada a partir das derivadas. Conclui

    existe Λ∈ℝ, constante em U, tal que G+Λg=κT.

Aqui G e T são os campos tensoriais do enunciado. O símbolo G NÃO foi definido nesta entrega como Ric−½Rg. A identificação de G com o tensor de Einstein da curvatura ainda precisa de construção e prova. A igualdade final tem a forma da equação gravitacional, mas sua interpretação depende dessa dívida e da origem da hipótese nula.

## Como a prova chega ao resultado

`TensorNullCone.lean` transporta a rigidez já existente de `GeneralNullCone.lean` para matrizes e congruências. A prova anterior dos dez coeficientes em referencial de Minkowski é reutilizada, não contada como uma novidade. Polarização identifica matrizes simétricas a partir de suas formas quadráticas. Para g=EᵀηE, a transformação DᵀAD reduz o problema ao cone de η e o transporte inverso devolve A=cg. O teorema matricial também aceita diretamente o contrato canônico `TGLExt.LorentzByCongruence`.

`MetricCompatibleJet.lean` constrói os símbolos

    Γˡᵢⱼ = ½ Σₖ g^{lk}(∂ᵢgₖⱼ+∂ⱼgᵢₖ−∂ₖgᵢⱼ)

como uma expressão algébrica em g⁻¹ e no primeiro jato. Demonstra torção zero, compatibilidade e a contração div(fg)=df. O módulo declara explicitamente que seus argumentos são jatos, sem fingir que uma lista de números já é a derivada de um campo.

`CovariantScalarConservation.lean` fornece essa ligação: cada ∂ᵢAⱼₖ é `fderiv ℝ (fun x => A x j k) x` aplicado ao vetor coordenado. A regra do produto usa diferenciabilidade. A igualdade local em U passa para as derivadas porque U é aberto. Se as quatro derivadas coordenadas de f se anulam, a derivada de Fréchet inteira se anula; a constância em U usa o teorema do valor médio da mathlib em domínio preconexo.

`MetricFieldConnection.lean` aplica os jatos às derivadas reais de g e produz a conexão. A simetria de g⁻¹ segue da simetria de g e das identidades de inversão. Torção zero e compatibilidade são conclusões, não campos de uma estrutura presumida. As identidades formais de `fderiv` podem ser enunciadas mesmo fora do conjunto de diferenciabilidade; os teoremas finais carregam explicitamente a diferenciabilidade necessária para lê-las como derivadas.

`LorentzMetricField.lean` constrói g, g⁻¹ e f=(DᵀAD)₀₀ e prova as identidades de inversão e a diferenciabilidade das componentes. `TensorFieldLinearity.lean` demonstra linearidade da divergência por subtração e multiplicação por escalar constante. `GeneralTensorReconstruction.lean` compõe os resultados.

As hipóteses são de diferenciabilidade das componentes, sem exigir continuidade de todas as primeiras derivadas. Portanto a formulação não deve ser descrita como se a biblioteca tivesse provado regularidade C¹ ou superior para os dados de entrada.

## Controle de uma hipótese indispensável

`TensorReconstructionControls.lean` usa A(x)=x⁰η. Sua forma quadrática anula todos os vetores nulos de η, mas nenhum escalar constante representa A em todo ℝ⁴. Sua divergência na métrica constante η e conexão zero é exatamente d(x⁰): a componente temporal vale 1. Isso mostra concretamente por que a informação sobre o cone nulo, sozinha, determina uma função multiplicadora e não uma constante cosmológica.

## O que permanece como entrada ou dívida

| Item | Estatuto nesta continuação |
|---|---|
| η e existência do referencial real invertível | [INPUT]. A assinatura lorentziana entra explicitamente; não foi extraída de positividade completa ou de um boost. |
| Referencial e inversa diferenciáveis em uma carta | [INPUT]. A origem desse referencial na dinâmica modular não foi construída. |
| Anulação de A sobre todos os vetores nulos | [INPUT]. Não foi deduzida de Clausius, Raychaudhuri ou da normalização do estado. |
| Conservação de A; no corolário, de G e T | [INPUT]. As consequências são provadas; Bianchi contraída e conservação física não foram presumidas como se fossem conclusões. |
| Curvatura Riemann, Ricci, escalar e G=Ric−½Rg | [OPEN] para a cadeia geral desta entrega. Não foram construídos aqui. |
| Transformação entre cartas e colagem global | [OPEN] nesta formalização. O resultado é em um domínio coordenado, com coeficiente constante em cada componente conexa pertinente. |
| H3 produzido pela dinâmica, quatro canais, assinatura derivada | [OPEN]. Os obstáculos da ordem 007 continuam válidos. |
| Gravitação quântica demonstrada em sentido amplo | [OPEN]. Nenhuma contagem de teoremas ou implicação condicional foi promovida a essa conclusão. |

[KNOWN] A rota termodinâmica clássica de Jacobson exige relações para todos os horizontes locais e condições termodinâmicas específicas. Referência primária consultada: [Thermodynamics of Spacetime: The Einstein Equation of State](https://arxiv.org/abs/gr-qc/9504004). Esses pressupostos não são fornecidos pela mera normalização de um estado. Nenhum resultado dessa fonte foi acrescentado como axioma Lean.

## Integração e custódia

Não havia ordem 008 no início desta continuação. A entrega é espontânea, conforme o protocolo do túnel, e não uma ordem atribuída à sessão irmã. Os módulos usam o namespace `ChatgptAudit`; transposição ao kernel, auditoria independente, incorporação em `um.py`, selos e atualização das memórias continuam com a gerência.

Somente a bancada Chatgpt recebeu escritas. As entregas 006 e 007 foram novamente verificadas por seus auditores de bytes, sem alteração de seus artefatos. O Atlas foi apenas consultado. Nenhum `um.py` foi executado, importado ou alterado, e não se fez pesquisa de dados observacionais.

Os logs finais, suas saídas axiomáticas, os hashes efetivos e as falhas preservadas serão inventariados pelo auditor desta continuação. A aprovação independente da gerência permanece pendente; a construção não aprova a si mesma nem altera o gate.
