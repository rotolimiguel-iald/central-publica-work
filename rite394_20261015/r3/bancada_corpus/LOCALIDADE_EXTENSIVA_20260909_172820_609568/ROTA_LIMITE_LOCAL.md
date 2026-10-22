# Rota concreta de interação extensiva

[DERIVED — dedução e plano de formalização; o próximo limite dinâmico não está concluído]

## O que precisa mudar no tipo

O contrato anterior LocalInteractionData pede Σ_j ‖V_j‖ < ∞ e apenas V_j no andar j+1. A somabilidade constrói um operador V global limitado; o andar j+1 contém todos os sítios até j+1 e, sozinho, não expressa alcance espacial finito.

O novo [BondInteractionData](<C:/IALD/Central de Patentes/Chatgpt/LOCALIDADE_EXTENSIVA_20260909_172820_609568/BondLocalityEstimates.lean:12>) exige V_j auto-adjunto, suportado na álgebra canônica da região {j,j+1}, e ‖V_j‖≤J com J≥0. Não há somabilidade global, comutação entre termos ou pertença ao centralizador. A realização atual usa a cadeia canônica de sítios de dois níveis e seu mesmo TowerHilbert P. Não substitui o codomínio por uma álgebra abstrata de mesmo nome.

O objetivo extensivo é a evolução de observáveis locais e sua extensão ao fecho em norma da união das álgebras locais. Um limite de Hamiltonianos ou cociclos implementadores em norma global não é exigido. Automorfismo do fecho quase local não equivale, por si, a automorfismo normal da álgebra de von Neumann inteira na representação escolhida.

## Primeiro bloco que foi implementado

- [operator_bracket_norm](<C:/IALD/Central de Patentes/Chatgpt/LOCALIDADE_EXTENSIVA_20260909_172820_609568/BondLocalityEstimates.lean:23>) dá ‖[A,B]‖≤2‖A‖‖B‖. [operator_bracket_mem_union](<C:/IALD/Central de Patentes/Chatgpt/LOCALIDADE_EXTENSIVA_20260909_172820_609568/BondLocalityEstimates.lean:31>) e [operator_bracket_eq_zero_of_disjoint](<C:/IALD/Central de Patentes/Chatgpt/LOCALIDADE_EXTENSIVA_20260909_172820_609568/BondLocalityEstimates.lean:43>) usam a localidade efetiva do kernel.
- [cutoffHamiltonian](<C:/IALD/Central de Patentes/Chatgpt/LOCALIDADE_EXTENSIVA_20260909_172820_609568/BondLocalityEstimates.lean:85>) define H_N=Σ_{j<N}V_j; [cutoff_hamiltonian_selfadjoint](<C:/IALD/Central de Patentes/Chatgpt/LOCALIDADE_EXTENSIVA_20260909_172820_609568/BondLocalityEstimates.lean:89>) e [cutoff_hamiltonian_mem_prefix](<C:/IALD/Central de Patentes/Chatgpt/LOCALIDADE_EXTENSIVA_20260909_172820_609568/BondLocalityEstimates.lean:95>) certificam esse operador finito. [cutoff_hamiltonian_bracket](<C:/IALD/Central de Patentes/Chatgpt/LOCALIDADE_EXTENSIVA_20260909_172820_609568/BondLocalityEstimates.lean:105>) identifica seu comutador real com a soma de comutadores usada na estimativa.
- Se A está no prefixo 0,…,R, [cutoff_bracket_stabilizes](<C:/IALD/Central de Patentes/Chatgpt/LOCALIDADE_EXTENSIVA_20260909_172820_609568/BondLocalityEstimates.lean:118>) mostra [H_N,A]=[H_{R+1},A] para N≥R+1.
- [iterated_bracket_mem_prefix](<C:/IALD/Central de Patentes/Chatgpt/LOCALIDADE_EXTENSIVA_20260909_172820_609568/BondLocalityEstimates.lean:167>) põe ad(H_N)^k(A) no prefixo R+k. [iterated_bracket_cutoff_independent](<C:/IALD/Central de Patentes/Chatgpt/LOCALIDADE_EXTENSIVA_20260909_172820_609568/BondLocalityEstimates.lean:177>) mostra igualdade dos iterados para N,M≥R+k.
- [iterated_bracket_uniform_bound](<C:/IALD/Central de Patentes/Chatgpt/LOCALIDADE_EXTENSIVA_20260909_172820_609568/BondLocalityEstimates.lean:205>) fornece, para TODOS os cortes N,
  ‖ad(H_N)^k(A)‖ ≤ (2J)^k · Π_{r<k}(R+r+1) · ‖A‖.
  A função [commutatorGrowth](<C:/IALD/Central de Patentes/Chatgpt/LOCALIDADE_EXTENSIVA_20260909_172820_609568/BondLocalityEstimates.lean:192>) guarda esse majorante explicitamente; sua recorrência também é provada.

As hipóteses de auto-adjunção são usadas no Hamiltoniano finito. As estimativas puramente algébricas não precisam de comutação entre diferentes bonds.

## Caminho mais curto até existência local

1. [OPEN — próximo lema implementável] Identificar a série com a evolução finita real:
   tau_N(t)(A)=exp(i t H_N) A exp(-i t H_N)
   =Σ_{k≥0}(i t)^k/k! · ad(H_N)^k(A).
   O lado esquerdo deve usar evolution de UnitaryDuhamel e H_N acima. A identidade pode vir de séries de exponenciais em álgebra de Banach ou da unicidade da ODE para o operador linear ad(H_N). Não basta definir o lado direito e chamá-lo tau.

2. [DERIVED] Para |t|≤T e q=2JT<1, dividir a estimativa já implementada por k! produz
   q^k · binomial(R+k,k) · ‖A‖.
   A soma escalar converge e vale ‖A‖/(1-q)^(R+1). O caso J=0 é tratado separadamente (todos os termos são zero). A identidade factorial, a somabilidade e a cauda ainda precisam de prova Lean; não são hipóteses de um novo contrato.

3. [DERIVED] Se N,M≥R+K, os primeiros K+1 coeficientes coincidem. A diferença entre tau_N e tau_M fica limitada por duas caudas do majorante, uniformemente em |t|≤T. Isso dá Cauchy e existência por completude para cada A local, sem supor um limite. O raio temporal 1/(2J) independe de R e do volume; a constante da cauda depende do suporte de A.

4. [OPEN] Construir o fecho em norma da união local e estender o limite de tempo pequeno por densidade e isometria. As evoluções finitas são unitárias, multiplicativas e preservam a adjunção; as leis passam ao limite. É necessário provar que suas imagens continuam no mesmo fecho.

5. [DERIVED] Para t arbitrário, escolher m com |t/m| no intervalo de tempo pequeno e usar tau_N(t)=tau_N(t/m)^m. A isometria permite passar ao limite com argumentos variáveis; isso produz a evolução global como limite dos próprios cortes. Grupo, inversa e independência da partição vêm desse limite, não de escolha arbitrária. A uniformidade em compactos para argumentos em órbitas compactas exige o lema usual de equicontinuidade mais cobertura finita, ou construção equivalente.

Essa rota constrói primeiro a dinâmica da interação pura. Não entrega uma estimativa espacial exponencial de Lieb–Robinson. A cota grosseira do comutador iterado é suficiente para tempo pequeno, mas não deve ser somada diretamente em todo tempo sem o passo de extensão.

## Fundo modular canônico

[REAL — fontes lidas] SiteModularInvariance.lean:37, chain_flow_into, preserva cada região pela ação alpha_t canônica. SummableInteractionModularOrbit.lean:43 prova isometria; :57 prova continuidade em norma em suporte finito. Assim V_j(t)=alpha_t(V_j) conserva o suporte e o bound J.

[OPEN] Se os geradores modulares locais log(P.w_j) não tiverem controle uniforme, não se pode absorvê-los silenciosamente em J. A rota adequada é uma expansão de Dyson para a interação temporal V_j(t), com simplices temporais, suporte por iteração e normas uniformes. A estrutura temporal correspondente e a identificação com os cortes H0_N+H_N ainda precisam de construção. A folha atual não identifica a dinâmica pura com a dinâmica modular perturbada anterior.

## Alternativa por Lieb–Robinson

[KNOWN] Nachtergaele–Ogata–Sims demonstram uma desigualdade integral de comutadores, sua iteração por caminhos e uma estimativa independente do volume; o teorema seguinte obtém a dinâmica por Cauchy de observáveis locais. Referência primária: [Propagation of Correlations in Quantum Lattice Systems, teoremas 2.1 e 2.2](https://arxiv.org/abs/math-ph/0603064).

[KNOWN] Para termos locais de fundo sem bound uniforme, Nachtergaele–Sims usam a representação de interação e provam estimativas e limite termodinâmico sob controle adequado da interação. Referência primária: [On the dynamics of lattice systems with unbounded on-site terms in the Hamiltonian, teoremas 3.1 e 4.1](https://arxiv.org/abs/1410.8174).

No caso de bonds vizinhos, cada bond só intersecta seu antecessor, ele mesmo e seu sucessor. Essa contagem de caminhos pode substituir a infraestrutura métrica geral na primeira prova de Lieb–Robinson, mas é mais longa que o limite local por séries acima. Nenhum desses resultados da literatura foi inserido como axioma Lean.

## Limites desta entrega

Não foi provada ainda existência de dinâmica extensiva, estimativa Lieb–Robinson, limite relativista/UV, invariância normal do fator inteiro, estado KMS ou ponte gravitacional adicional. O primeiro ganho concreto é uma família de estimativas do gerador local que não usa somabilidade global. O recibo de compilação separado determina o estatuto REAL do bloco Lean. Os originais permanecem intocados; nenhum um.py foi executado ou importado.
