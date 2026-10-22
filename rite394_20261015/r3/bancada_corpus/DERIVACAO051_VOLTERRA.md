# Derivação051 — lei integral de Volterra para o balanço óptico

[DERIVED — escrito antes do fonte; sem compilação051 nesta emissão]

Trabalhamos num conjunto I⊆ℝ aberto, convexo e contendo0. Os dados reais A, θ, R, F, M, Q satisfazem, em I,
A′=Aθ, θ′=−R−F, θ(0)=0, Q′=−K t M(t) A(t), Q(0)=0.
R, F e M são contínuos em I. A continuidade de A e θ é consequência das derivadas assumidas. Não se assume uma conclusão de Clausius nem se define um contratermo pela diferença alvo.

Definem-se primeiro Z_f(t)=∫₀ᵗ f(s)ds e E_F(t)=∫₀ᵗ A(s)Z_F(s)ds. A convexidade mantém cada intervalo não orientado [0,t] dentro de I; a abertura permite usar o FTC para a derivada de Z_f em cada ponto.

O FTC aplicado a θ fornece θ(t)=−Z_R(t)−Z_F(t). Para D(t)=Q(t)−K(A(t)−A(0)), as derivadas já dadas fornecem
D′(s)=−K s M(s)A(s)−K A(s)θ(s)
      =K A(s)[Z_F(s)+Z_R(s)−sM(s)].
Como D(0)=0, outro FTC prova a identidade finita exata
Q(t)−K(A(t)−A(0))=K∫₀ᵗ A(s)[Z_F(s)+Z_R(s)−sM(s)]ds.
Todos os termos são intervalarmente integráveis pela continuidade no intervalo compacto; a prova deve incluir essa obrigação.

Se M=R, permanece o termo Z_R(s)−sR(s). Ele só se cancela automaticamente quando R é constante. Para R=M=r constante, o balanço reduz a K E_F(t). Nenhuma igualdade geral de curvatura variável será substituída por esse caso especial.

Se A≥0 e F≥0 em I, E_F(t)≥0 para todo t∈I:
- t≥0: Z_F(s)≥0 para 0≤s≤t e ambas as integrais têm orientação positiva;
- t≤0: Z_F(s)=−∫ₛ⁰F≤0 para t≤s≤0, então A(s)Z_F(s)≤0 e a orientação exterior 0→t troca o sinal.
A não negatividade de K E_F exige ainda K≥0; não se presume isso na identidade.

[INPUT] As equações ópticas, a lei de Q e qualquer casamento R=M são hipóteses explícitas deste resultado abstrato. A instância geométrica construída é responsabilidade de outro módulo. [OPEN] A identificação do termo com produção física de entropia, H3 geral e reconstrução gravitacional não decorrem somente desta lei.

Custódia: somente os novos DERIVACAO051_VOLTERRA.md e OpticalVolterraBalance.lean podem ser escritos por esta tarefa. Toda revisão preserva backup dos bytes imediatamente anteriores, usa temporário exclusivo verificado e substituição. Originais, memórias e etapas≤050 permanecem somente leitura.
