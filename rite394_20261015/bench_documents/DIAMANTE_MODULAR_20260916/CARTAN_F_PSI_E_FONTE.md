# Campo de sustentação e conexão: consequência condicional do termo F(ψ)R

17/09/2026. [DERIVED — demonstração analítica condicional; ainda sem revisão independente; não Lean]. Não altera um.py ou gate. Continuação de CONTORCAO_FONTE_E_CARGA_REGIONAL.md.

## Fonte e hipótese que não se pode ocultar

Leitura direta de tgl_paper_unified.py, linhas 10121–10190, identifica Lgrav = F R, F = 1/(2κ_artigo²) + ξ|Ψ|², ξ=1/6, κ_artigo²=8πG/c⁴. O trecho não determina se R usa uma conexão independente. Apresenta também uma cinética de uma forma Ψ_μ e chama Ψ de escalar: a tipagem precisa ser resolvida no consumidor físico; não corrigimos a fonte por interpretação.

A derivação abaixo vale para um setor em quatro dimensões, coframe invertível, F positivo e suave, conexão de Lorentz independente e compatível com a métrica, ação ∫√|g| F R(Γ), sem outros termos dependentes da conexão. Correntes de spin, termos de Holst e termos adicionais de torsão alteram a equação. Não foi demonstrado que todos os termos da ação completa satisfazem esta restrição. Em particular, a presença de férmions não autoriza descartá-los da variação da conexão.

## Equação e solução

A variação da conexão, com variações de suporte interior ou condições de bordo apropriadas, dá Dω(F eᵃ∧eᵇ)=0 após inverter o dual interno. Ponha ẽᵃ=√F eᵃ. A equação é Dω(ẽᵃ∧ẽᵇ)=0, a equação de Cartan sem fonte de spin para um coframe invertível. Logo sua conexão de Lorentz é a conexão sem torsão de ẽ. Em termos do coframe original,

0=Dω(√F eᵃ)=√F[Tᵃ+(1/2)d ln F∧eᵃ],

portanto Tᵃ=(1/2)eᵃ∧d ln F.

Com a convenção ∇μVρ=∂μVρ+Γρ_{μσ}Vσ e Γ=LC(g)+C, a solução é

vμ=(1/2)∂μ ln F,
Cρ_{μσ}=δρμ vσ−gμσ vρ,
Tρ_{μν}=δρμ vν−δρν vμ.

A substituição direta dá Dω(F eᵃ∧eᵇ)=(dF−2Fv)∧eᵃ∧eᵇ=0. A compatibilidade métrica segue de Cρμσ+Cσμρ=0 após baixar o primeiro índice. A conclusão sobre unicidade usa a equação de Cartan para coframe invertível, não apenas a verificação do ansatz vetorial.

Se F for constante neste setor sem spin, a torsão é zero. Se R for definido como R(g) desde o começo, não existe esta variação independente: C=0 é parte da definição da formulação métrica. Não são escolhas intercambiáveis apenas porque a ação foi escrita como FR.

## Critério para uma torsão de traço prescrita

Defina Vμ=Tρ_{ρμ}=3vμ. Uma prescrição Tρ_{μν}=(δρμ Vν−δρν Vμ)/3 resolve a equação anterior precisamente quando V=(3/2)d ln F. Assim dV=0 é necessário; localmente também permite reconstruir F até uma constante positiva. Globalmente é necessária exatidão, não apenas fechamento: períodos não nulos impedem um F positivo global dessa forma.

Se V=q n, exige-se d(q n)=0 e d ln F=(2/3)q n. Uma identidade algébrica de Bianchi satisfeita por V arbitrário não substitui esta equação dinâmica. q deve carregar a unidade necessária para V ser uma conexão; um ângulo adimensional sozinho não estabelece essa escala.

## A contribuição que chega à ação efetiva e ao bordo

Na convenção de curvatura da nota anterior,
R(Γ)=R(g)−6∇μvμ−6vμvμ
=R(g)−3□ln F−(3/2)(∂ln F)².

Consequentemente, como identidade de densidades,
F R(Γ)=F R(g)+(3/(2F))(∂F)²−3□F.

A última parcela é uma divergência. Num diamante finito, não pode ser apagada antes de fixar ação de bordo, cantos e condições de variação. A integral de uma divergência usa o elemento orientado adequado, inclusive em faces nulas; não se presume normal unitária numa face nula.

O termo cinético efetivo adicional e a parcela de bordo afetam a construção do tensor de energia/carga. Não basta inserir C na antiga carga mantendo silenciosamente os mesmos termos de bordo. A solução da conexão não demonstra positividade física, propagação de gráviton ou completude UV.

## Consequência para a questão modular

Este resultado fornece C em função de F(Ψ), em vez de um C arbitrário, sob as hipóteses acima. Não fornece o estado interagente ω nem sua resposta. Em família Fε=F0+εf+O(ε²), com métrica fixa, v1=(1/2)d(f/F0); para F0 constante, C1 é determinado por esse gradiente. Isso pode alimentar a fórmula de fonte da nota anterior, depois de incluir a variação correta da ação e do bordo.

Ainda não se segue [Kω−Kξ,A]=0 no centralizador, nem um coeficiente modular universal. Uma contribuição geométrica clássica multiplicada por I continua central e não demonstra um operador não central. O fator 1/2 desta equação de Cartan não é o coeficiente R1 do problema modular, nem uma demonstração independente da Meia-Nat.

## Conferência externa de convenções

Inagaki–Taniguchi, https://arxiv.org/pdf/2204.01255, equações 2.4–2.7, explicitam a hipótese de matéria independente da conexão e a estrutura R=RE−3□ln F′−(3/2)(∂ln F′)². Ali F′ é derivada de uma função de R; aqui F é coeficiente dependente de Ψ. Usamos a fonte somente para conferir a estrutura, não para identificar as duas teorias. A ordem dos índices inferiores da conexão na fonte difere da convenção acima.
