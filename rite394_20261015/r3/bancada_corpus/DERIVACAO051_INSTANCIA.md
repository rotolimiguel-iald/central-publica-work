# Continuação051 — instância óptica da identidade finita

[DERIVED — derivação prévia à fonte OpticalFiniteBalance.lean; nenhuma prova051 compilada nesta emissão]

A fonte geral OpticalVolterraBalance será instanciada nas funções já existentes: q_a=jacobiLogDerivative a, q_c=jacobiLogDerivative c, A=geometricJacobiArea a c e Q=opticalHeat a c rate mass. Exigimos a,c≥0 e um intervalo aberto convexo I contendo0, no qual ambos os osciladores são não nulos. Nenhum relógio ou contratermo é escolhido para anular o defeito.

Definições independentes do calor:
θ=q_a+q_c; F=q_a²+q_c²;
E(t)=∫₀ᵗ A(s)(∫₀ˢF(u)du)ds.

A área já é |f_a f_c|. Fora dos zeros, A>0 e A'=Aθ, mesmo sem antecipar o sinal do produto: prova-se a derivada nos dois casos do valor absoluto. Riccati043 dá θ'=−(a+c)−F e θ(0)=0. A derivada real do calor041 é Q'=−rate*mass*t*A e Q(0)=0.

Tomando K=(rate/(2π))*eta e r=a+c, o matching explícito eta*r=2π*mass transforma Q' em −K*r*t*A. O teorema integral genérico fornece
Q(t)−K(A(t)−1)=K E(t).
A relação de Ricci–matéria permanece hipótese; não é apresentada como consequência do estado. A parte de curvatura variável da lei geral não é eliminada fora desta instância de r constante.

F≥0 e A≥0 dão E≥0 para ambos os sinais de t, usando a orientação das integrais. A identidade física para o sentido passado→origem é ΔS=eta*(1−A(t)), Q_segmento=−Q(t). Não nomeamos E produção física de entropia sem uma ponte adicional.

O germe perto de0 vem de continuidade e f_a(0)=f_c(0)=1. A identificação com opticalScreenHeat/constructedHeat043 usa exclusivamente optical_screen_heat_germ, de filtro 𝓝[<]0. Nenhuma igualdade global para a extensão de calor043 será presumida.

Para recuperar o limite quártico de E sem novo axioma de expansão, especializamos a identidade em rate=2π, eta=1, mass=(a+c)/(2π): o fator K é1. Então E coincide localmente com opticalClausiusDefect desses parâmetros. O limite041 dá E(t)/t⁴→(a²+c²)/12. Essa transferência segue a identidade exata já demonstrada; E não foi definido a partir do defeito.

Escrita somente dos dois novos arquivos051 atribuídos, em Chatgpt; fontes≤050, canônico, Atlas, memórias e selos somente leitura. Derivação anterior ao código, backup de bytes antes de revisão, temporário verificado, todas as declarações impressas e compilação apenas quando o runner for liberado. Origem quântica, H3 e reconstrução geral permanecem OPEN.
