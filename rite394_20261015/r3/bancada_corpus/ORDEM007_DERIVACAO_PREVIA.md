[DERIVED / KNOWN / OPEN] Ordem 007 — derivação anterior aos novos módulos, 05/09/2026.

## A — média periódica

A continuidade forte do fluxo em todo H já existe em `modularFlow_strongly_continuous`; foi relida nesta rodada. Não é uma dívida nova. A continuidade conjunta (t,v)↦U_t v decorre dela e da isometria uniforme: separar U_t(v−v₀) de (U_t−U_t₀)v₀. Logo t↦U_t x U_−t ξ é contínua para x limitado.

Para perfil constante p, os log-pesos de quaisquer dois índices no mesmo andar diferem por kℓ, k inteiro, ℓ=log(p/(1−p)). Prova por indução tensorial: as diferenças dos sítios são 0,ℓ,−ℓ; ao acrescentar um sítio as diferenças se somam. O argumento generaliza se cada log-razão de sítio pertence a ℤλ. Em T=2π/|λ|, as fases são 1; igualdade nos locais densos estende-se ao unitário. O perfil ½ tem período arbitrário positivo.

Definir A_T(x)ξ=T⁻¹∫₀ᵀU_t x U_−t ξ dt, por integral vetorial. Continuidade dá integrabilidade; linearidade da integral e ‖U_t x U_−t ξ‖≤‖x‖‖ξ‖ dão um operador limitado de norma ≤‖x‖. A construção não requer continuidade em norma de operadores. Para x∈M e y∈M′, y pode atravessar a integral contínua vetorial e comuta com cada integrando: A_T(x)∈M″=M.

Para passar ao andar basta avaliar sobre Ω e usar a projeção ortogonal limitada `levelProject N`, que atravessa a integral em H. U_tΩ=Ω e `project_flow_commutes` reduzem essa projeção à média do fluxo local. Integrar fase a fase dá `specExpect` quando há período e a frequência é não nula, ou identidade quando é zero. A igualdade de operadores segue de separância depois de identificar os vetores em Ω. Isso evita pedir uma continuidade de E_N em norma de B(H) que a prova não usa.

Com essa ponte, os campos do contrato seguem da ordem 006: `into` por `centralizer_from_expectations`; `fixes` por aproximação E_NxΩ→xΩ e separância; `ortho` por produtos internos das aproximações e ortogonalidade finita. Não inserir a existência da média como hipótese do habitante final. Obrigações intermediárias condicionais deverão ser marcadas como tais se a formalização não completar.

## B — cauda e translações

Para x∈T₁, o bicomutante da cauda faz x comutar com todo o primeiro andar. `expectation_central_scalar` dá E₀(x)=cI; preservação de ω fixa c=ω(x). Bimodularidade fornece ω(ex)=pω(x). Assim v=(e−pI)Ω é ortogonal a T₁Ω, e ‖v‖²=p(1−p)>0. Esta rota usa a cauda já fechada e dispensa uma nova passagem WOT por aproximação da cauda.

Consequência abstrata: dado E:M→N com E(x)∈N e ortogonalidade de (x−E(x))Ω a NΩ, se NΩ é denso então xΩ=E(x)Ω; separância implica x=E(x), logo M=N. A esperança é hipótese explícita neste teorema, não a construção pendente do alvo A. Invariância e normalidade são suficientes para obter a esperança na literatura, mas não necessárias no enunciado depois que seus campos são dados.

Possível obstrução adicional [DERIVED, a formalizar]: se o fluxo modular tem período T>0 e um grupo de translação fortemente contínuo satisfaz a relação de Borchers, então U(a)=U(exp(−2πT)a). Iterar a contração e passar a a=0 força U(a)=I. A relação de Borchers deve ser hipótese explícita na versão elementar; deduzi-la de energia positiva, compressão e vetor padrão usa o teorema de Borchers [KNOWN]. Não chamar essa derivação de prova Lean da hipótese espectral. Para perfis aperiódicos o argumento do período não se aplica; invariância de sítios sozinha não exclui translações de outra origem.

## C — a hipótese de identificação precisa ser testada, não presumida

Um boost real B(s) preserva η e, para s≠0, não preserva a métrica euclidiana. Isso pode ser demonstrado em blocos 2×2 e transportado a 4×4. Porém NÃO demonstra que Δ^{it} é esse boost: para Δ positiva numa representação finita de Hilbert, Δ^{it} é unitário. Nenhum subespaço finito invariante com métrica positiva pode carregar um boost hiperbólico não trivial por entrelaçamento invertível; um autovetor de boost teria norma multiplicada por exp(s)≠1. O próprio `ConcreteFourFrame` tem E=I por teorema, o que torna explícita essa obstrução se a ação for a mesma em ℂ⁴.

Além disso, escolher previamente B(s) não seleciona sozinho (1,3): ele preserva uma forma indefinida no plano do boost, mas as duas direções transversais admitem formas de sinais diversos. Preservação de η e não preservação de I não equivalem a unicidade da assinatura. Para a representação completa de Lorentz, outra hipótese e outro teorema seriam necessários.

A continuação a tempo imaginário e a condição KMS não constituem congruência REAL invertível transformando uma forma positiva em lorentziana: a inércia é preservada por tal congruência. Uma interpretação geométrica pode usar um espaço de representação diferente do Hilbert positivo e uma ponte construída entre os dois; essa ponte não existe por simples renomeação da exponencial. A entrega deverá levar o enunciado exato, incluindo a obstrução se confirmada pelo kernel, sem afirmar que a assinatura foi derivada quando se escolheu η como entrada.

## Adendo anterior ao módulo adicional de Borchers

Após provar o caso periódico, uma obstrução mais forte apareceu: todo perfil produto da torre tem família TOTAL de autovetores modulares (`localEigenvectors_total`), mesmo sem período comum. Para um autovetor ξ, as fases cancelam no funcional diagonal ⟨ξ,σ_t(V(a))ξ⟩. A relação de Borchers torna esse funcional invariante sob a↦exp(−2π)a. Continuidade em zero implica ⟨ξ,V(a)ξ⟩=‖ξ‖². Se V(a) é isometria, a identidade de ‖V(a)ξ−ξ‖² força V(a)ξ=ξ. Densidade do span dos autovetores dá V(a)=I. Portanto o resultado pode valer para TODOS os perfis produto sob a relação de Borchers, não apenas para os periódicos. A relação continua hipótese nomeada; sua derivação a partir de energia positiva/compressão é o teorema externo de Borchers, não um novo axioma Lean.
