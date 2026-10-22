# Diamante causal, resto modular e supressão no canto

2026-09-16 — análise em elaboração; conferir os recibos de compilação antes da entrega.

A resposta proposta pelo operador é substancialmente correta, com três precisões: uma carga local numa seção não equivale por definição a um fluxo geométrico em todo o diamante; a referência geométrica precisa existir na mesma álgebra; o gerador modular completo não é o Hamiltoniano unilateral. A expressão “teoria verdadeira” não especifica uma álgebra, um vácuo e um tensor de energia suficientes para calcular um operador único.

## O resultado físico conhecido e seu alcance

[KNOWN] No vácuo de uma CFT em Minkowski, a bola de raio R admite a carga modular local

K_B = 2π ∫_B [(R²−r²)/(2R)] T₀₀ d^(d−1)x + C I.

Interações são compatíveis com esse resultado. A passagem da cunha à bola usa uma simetria conforme implementada que preserva o vácuo, não somente uma mudança de coordenadas. A constante normaliza a densidade regularizada. No HTML de Casini–Huerta–Myers consultado a fórmula aparece como equação (22); a numeração citada no texto recebido precisa ser conferida na edição PDF antes de se afirmar “(2.20)”. [Fonte primária](https://arxiv.org/html/1102.0440v2).

[KNOWN] Uma integral local sobre um plano nulo pode produzir uma ação não local fora dele. Isso impede tratar “integral local” e “ação geométrica em todo o espaço-tempo” como sinônimos universais. [Casini–Testé–Torroba, §§1 e 7](https://arxiv.org/html/1703.10656v3).

[KNOWN] Para férmions livres de pequena massa em 1+1 dimensões, o núcleo modular regional tem, na correção de primeira ordem, termos suportados em x+y=0 e termos distribuídos fora da diagonal x=y, além de termos locais. Há contribuições m log m; não é uma série analítica ordinária em m nem solução exata para toda massa. O exemplo demonstra não localidade modular em uma teoria controlada; não é por si uma prova sobre a teoria interagente fundamental pretendida. [Cadamuro–Fröb–Minz, equações 4.15–4.16](https://link.springer.com/article/10.1007/s00023-024-01508-0).

[KNOWN] A versão corrigida de Longo–Morsella retirou as alegações sobre a bola massiva por uma lacuna e trata da teoria sem massa. [Registro dos próprios autores](https://arxiv.org/abs/2012.00565).

[KNOWN] Deformações relevantes de uma CFT podem acrescentar contribuições à variação entrópica de pequenas bolas além do termo de energia. O resultado perturbativo depende da dimensão do operador e da ordem em raio/amplitude. Completude UV não implica conformalidade exata em qualquer escala. [Casini–Galante–Myers, equações 6–7 e discussão](https://arxiv.org/html/1601.00528v2).

## Diagnóstico pela corrente conforme

[DERIVED] Para T simétrico, ∂_μ T^{μν}=0 e um campo conforme de Killing,

∂_μ(T^{μν} ξ_ν) = T^{μν} ∂_(μ ξ_ν)
                 = [(∂·ξ)/d] T^μ_μ.

Para ξ⁰=π(R²−t²−r²)/R e ξⁱ=−2πt xⁱ/R, a divergência é −2πdt/R. Portanto a corrente tem divergência −2πt T^μ_μ/R. A álgebra desta contração e as derivadas dos componentes são alvos explícitos do módulo DiamondConformalCurrent. Uma equação de conservação para distribuições renormalizadas em QFT exige as hipóteses correspondentes; não é construída pelo cálculo de componentes.

Traço operatorial não nulo diagnostica falha da carga conforme conservada, mas não calcula o Hamiltoniano modular inteiro. Em t=0 o coeficiente se anula sem tornar a corrente conservada para todos os tempos. Termos de borda, melhorias do tensor e anomalias precisam ser tratados na teoria escolhida.

## Resto definido exatamente numa regularização fiel

[DERIVED] Escolhido Q=Q†, tome Z=Tr exp(−Q), σ=exp(−Q)/Z e uma densidade fiel normalizada ρ do vácuo regional. Defina

R = log σ − log ρ.

Então −log ρ = Q + log Z I + R. Esta é uma decomposição exata para uma referência especificada, não uma construção do vácuo a partir de Q. Alterar a referência muda R; trocar ρ e σ inverte seu sinal. R=0 equivale a ρ=σ pela injetividade do logaritmo sobre operadores estritamente positivos.

[DERIVED] A identidade escalar para a>0,

log a = ∫₀∞ [(1+u)⁻¹−(a+u)⁻¹] du,

aplicada separadamente às decomposições espectrais de ρ e σ dá

R = ∫₀∞ [(ρ+uI)⁻¹−(σ+uI)⁻¹] du.

Não se diagonalizam ρ e σ simultaneamente. A diferença converge em norma: as inversas são limitadas perto de u=0 pela positividade estrita, e a identidade do resolvente dá decaimento O(u⁻²) no infinito. A representação permite também

δK = −∫₀∞ (ρ₀+uI)⁻¹ δρ (ρ₀+uI)⁻¹ du.

Isso segue da derivada de uma inversa. Uma cota espectral uniforme positiva permite passar a derivada pelo integral. Se δρ não comuta com ρ₀, não se pode substituí-lo por −ρ₀⁻¹δρ. Estas duas fórmulas receberam controle numérico independente; sua formalização integral em Lean ainda não está declarada concluída.

## Cociclo e o que significa invisibilidade

[KNOWN] Para estados normais fiéis na mesma álgebra, o cociclo de Connes relaciona os fluxos por σ^ω_t=Ad(u_t)∘σ^φ_t e u_(t+s)=u_t σ^φ_t(u_s). Há versão para pesos fiéis normais semifinitos. [Lledó, Teorema 5.2](https://arxiv.org/html/0901.1004v1).

O adjetivo geométrico só entra se σ^φ já foi identificado com a ação geométrica pretendida. A existência desse φ não é automática para qualquer diamante. A literatura de produtos cruzados explicita essa hipótese e resultados em cenários particulares. [Ali–Suneeta, introdução e referências a JSS](https://arxiv.org/html/2404.00718v2).

[DERIVED] Na regularização u_t=ρ^(it)σ^(−it). Sua derivada na origem é i(logρ−logσ)=−iR, portanto R=i u′₀. A lei temporal e a unitariedade já existem em TGLExt.Cocycle. O entrelaçamento sem comutatividade é formalizado nesta bancada. No contínuo não se presume uma derivada limitada nem um domínio comum.

Em uma álgebra A, Ad(u)=id em todos os observáveis equivale a u comutar com todos eles. Como o cociclo pertence a A, isso é centralidade em A; num fator, escalaridade. Se estivermos comparando implementadores arbitrários em B(H), a conclusão pode ser pertinência ao comutante A′, não escalaridade: é preciso preservar a tipagem.

O fluxo modular completo usa Δ; a notação K̂=−logΔ é distinta de −logρ_D. Em uma fatorização regulada K̂=K_D−K_complemento. Um escalar regional de normalização e um operador do comutante não são o mesmo objeto.

## Teste por estados e balanço entrópico

[DERIVED] Se todas as expectativas em estados puros normalizados de um operador autoadjunto R são c, a polarização implica R=cI. Um vetor só não basta. A prova admite inclusive espaços de Hilbert gerais para operadores lineares onde a forma quadrática esteja definida; a interpretação por matrizes densidade pertence à regularização finita.

Para densidades fiéis normalizadas, S(ρ||ρ₀)=Tr ρ(logρ−logρ₀) e S(ρ)=−Trρlogρ dão por álgebra

Δ⟨R⟩ = S(ρ||ρ₀)+ΔS−Δ⟨Q⟩.

O termo cI desaparece porque ambas as densidades têm traço um. A identidade não diz R=Srel: um é operador, o outro é número. Na primeira ordem, quando a primeira lei se aplica, δS=δ⟨Q⟩+δ⟨R⟩. Não se elimina o último termo usando apenas normalização.

## O teorema do canto que é necessário

[DERIVED] Fixado p²=p, com α(p)=p e β=Ad(u)∘α, temos

β|_(pAp)=α|_(pAp) ⇔ [u,x]=0 para todo x∈pAp.

Uma condição suficiente é [u,p]=0 e pup=c p; a unitariedade de u fornece o cancelamento da fase. Para uma família, as condições valem para todos os tempos. Não se usa a escalarização automática de um canto de posto um como substituto de invariância.

[DERIVED] O contraexemplo construído usa p=diag(1,0), G=[[0,1],[-1,0]], R=iG. Este R é autoadjunto e pRp=0, mas U(t)=exp(−itR)=Smat(t) e pU(t)p=cos(t)p. Em t=π/2, U p U†=I−p. A exponencial é a mesma já provada no kernel em SMatrix; não foi postulada outra dinâmica para fazer o controle funcionar.

## Relação com o motor de reconhecimento

O motor anterior E(ρ)=Σ C_aρC_a e L=Γ(E−id) é dissipativo. R, como diferença de Hamiltonianos, produz uma correção unitária por comutador. Não são o mesmo tipo de gerador. A correção unitária pode recriar coerências entre os blocos que E apaga. É por isso que conhecer E, ou ter pRp=0, não dispensa o teste de invariância e da ação completa do cociclo.

O critério novo deve ler as provas pertinentes; não criar outro gate, outro Hamiltoniano por definição ou outra camada que declare a geometricidade que deveria demonstrar.

## Sobre “inércia” e zero absoluto

[ONTO] A expressão pode nomear uma resistência relativa entre a ação modular efetiva e a ação geométrica escolhida. Há uma estrutura matemática para essa diferença: R e, de forma mais geral, Ad(u_t).

[OPEN] Isso ainda não identifica R com massa inercial, uma força física ou o operador canônico do zero absoluto. A definição é relativa à referência, não possui sinal universal, e R pode ser nulo em situações com dinâmica física não trivial. O Atlas distingue o zero absoluto sem habitante e operadores negativos específicos, como A_C=−H₃L; nenhum deles pode ser substituído por logσ−logρ somente por receber o mesmo nome.

Uma ligação física requer fixar o operador que recebe o nome “inércia”, seu domínio, suas unidades e sua ação sobre os mesmos observáveis, e então demonstrar a igualdade ou a equivalência operacional. A questão exata é se essa ação residual desaparece no setor físico escolhido. A construção algébrica fornece o critério; os dados da teoria precisam satisfazê-lo.

## Gravidade e escopo

[KNOWN] JLMS relaciona o Hamiltoniano modular da borda a área e Hamiltoniano modular do bulk em um regime semiclassicamente controlado. A área é operatorial e o gerador do bulk não precisa ser uma carga geométrica local. Isso não é uma fórmula universal para o diamante de uma teoria fundamental não especificada. [Jafferis–Lewkowycz–Maldacena–Suh](https://arxiv.org/html/1512.06431v1).

Não há declaração de gravidade quântica confirmada ou de fechamento físico neste documento. Há critérios matemáticos, provas em elaboração e um mapa explícito do dado físico ainda necessário.
