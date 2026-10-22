[DERIVED / INPUT / OPEN] Curvatura e conservação geométrica — derivação antes do código, continuação espontânea após 008, 05/09/2026.

## Estado inicial e alvo

A entrega 008 teve sua custódia novamente conferida: a implicação tensorial está provada, mas G ainda era um campo arbitrário conservado. Não há nova ordem no túnel no início desta continuação. O passo alinhado ao objetivo amplo é construir a curvatura geral da conexão de Levi-Civita em uma carta e provar as identidades geométricas que permitem substituir esse G pelo tensor de Einstein. A origem física da identidade nula e os dados de horizonte continuam obrigações distintas.

## Convenção que fixa os sinais

Escrever Γᵢ como a matriz cujo elemento (a,b) é Γᵃᵢᵦ. A curvatura é

    Fᵢⱼ = ∂ᵢΓⱼ − ∂ⱼΓᵢ + ΓᵢΓⱼ − ΓⱼΓᵢ,
    Rᵃᵦᵢⱼ = (Fᵢⱼ)ᵃᵦ,
    Rₐᵦᵢⱼ = gₐc Rᶜᵦᵢⱼ,
    Ricᵦⱼ = Σₐ Rᵃᵦₐⱼ,
    R = Σᵦⱼ gᵦⱼ⁻¹ Ricᵦⱼ,
    G = Ric − ½ Rg.

As derivadas são as derivadas de Fréchet da entrega 008 aplicadas às direções coordenadas. Não se definirá uma suposta curvatura com simetrias ou conservação já colocadas como campos de uma estrutura.

## Cadeia a demonstrar

1. Cálculo de matrizes: derivada de produto, transposta e soma; comutação de duas derivadas coordenadas a partir da simetria da segunda derivada real. Regularidade suave em aberto é uma hipótese explícita dos campos; não resulta de uma matriz de jatos.

2. Curvatura para uma conexão geral: Fᵢⱼ=−Fⱼᵢ e a identidade diferencial

    ∂ᵢFⱼₖ+[Γᵢ,Fⱼₖ] + ∂ⱼFₖᵢ+[Γⱼ,Fₖᵢ] + ∂ₖFᵢⱼ+[Γₖ,Fᵢⱼ] = 0.

O cancelamento usa a comutação das segundas derivadas de Γ, a regra do produto e a identidade de Jacobi matricial. Não usa equações de movimento.

3. Para Γ livre de torção e compatível com g, produzir a primeira Bianchi, a antissimetria nos dois índices abaixados e a troca de pares. Ao escrever derivadas covariantes com todos os índices de R, as correções dos índices de direção cancelam na soma cíclica por torção zero. Isso liga a identidade matricial à segunda Bianchi tensorial.

4. Contrair usando ∇g=0 para obter div Ric=½dR e, portanto, div G=0. Provar a simetria de Ric e G. Instanciar Γ com a conexão de Levi-Civita da entrega 008, sob regularidade suficiente, e aplicar a reconstrução já provada. Se uma etapa ficar incompleta, enunciar exatamente quais são os objetos produzidos e qual ligação falta: um resultado algébrico de jatos não será reclassificado como conservação geométrica geral.

## Limites mantidos

A métrica lorentziana suave e a carta são entradas. Mesmo depois de Bianchi, conservação de matéria e a anulação nula da diferença geométrica não surgem por definição. A ponte para a dinâmica modular, H3, quatro canais, assinatura derivada e globalização não são pagas pela identidade diferencial. O objetivo da gravitação quântica permanece inteiro e aberto.

Escritas somente na bancada Chatgpt. Originais, entregas já publicadas, kernel canônico, um.py, Atlas e memórias não serão modificados.
