# Revisão da raiz — certificado A6 e alcance da obstrução078

10/09/2026. [DERIVED — revisão matemática escrita] [REAL — controles simbólicos com recibos separados].

Li integralmente o certificado de Singer e o parecer independente de Turing. Conferi a avaliação de cadeia, a solução linearizada, a contração de Weyl, a classe do resíduo truncado e a conclusão sobre o mapa entre cortes. Parecer favorável no alcance abaixo.

A referência usa coordenadas (τ,x,y,z), η=diag(+---), z espacial positivo e g0=(ℓ/z)²η. Com a convenção de Riemann declarada, Ric(g0)=+3g0/ℓ². Não se pode transportar para esse cálculo uma fórmula com z temporal ou convenção oposta de Riemann. A sugestão inicial de troca de sinal feita durante a revisão foi retirada pelo revisor: derivava de ler z como índice temporal. O certificado conserva a convenção correta. A conferência direta dos símbolos Γ e de suas variações confirma esse sinal.

O tensor h=(ℓ/z)²γ, com γ11=f cos(kτ), γ22=−γ11, γ12=f sin(kτ), satisfaz a equação de Einstein linearizada se f''−2f'/z+k²f=0. As duas soluções elementares da nota têm Wronskiano k³z²; os dados f(z0)=0 e f'(z0)=1 são admissíveis para k≠0, z0>0. O fundo sigma constante e ξ=0 anulam a equação sigma linearizada e a mistura linear. Não se está afirmando que g0+t h seja solução não linear exata.

A avaliação toma todos os jatos de uma solução linearizada e de quatro campos de Killing reais, com os antifields zerados. Isso anula s0 de todos os geradores e de seus jatos. É um mapa de complexos para uma álgebra exterior com diferencial zero; não é um mapa para o diferencial BRST completo. A existência de uma primitiva formal implicaria uma primitiva de valência seis, finita em jatos, à qual essa avaliação se aplica sem somar uma série infinita.

O cálculo de Weyl no ponto dá tr(W1∧W1)=−4k/z0 dτ∧dx∧dy∧dz. Os quatro Killings ∂τ, ∂x, ∂y e D/z0, com D a dilatação, têm valores formando a base coordenada no ponto. Logo ev(A6)=−4k/z0 θ0θ1θ2θ3≠0. A não exatidão inclui primitivas regulares com antifields: s0 dos antifields é anulado pela solução linearizada, não simplesmente descartado.

O resíduo r6 da série truncada obedece r6=A6−s0α6. Portanto [r6]=[A6]≠0. Acrescentar somente um termo de valência seis não corrige T≤5. Se uma classe em H³(C6) restringisse à mesma classe [T≤5] em H³(C5), levantar sua fronteira de diferença e subtrair s dessa cochain produziria a mesma correção impossível. Assim o impedimento vale para a classe em C5, não só para um representante escolhido.

Isso não determina a imagem de TODAS as outras classes de C5 com o mesmo líder em C3. Modificações anteriores podem alterar a classe do resíduo. Não há conclusão de anomalia física inevitável, falha da QME, falha de toda a teoria ou obstrução UV. A valência seis com ghost4 e forma zero não é uma anomalia quântica de ghost1 e forma quatro.

A validação simbólica direta da raiz tem 105 asserções; o controle pontual de Weyl tem 17. Turing fez revisão estática independente de ambos, sem nova execução CAS. Os totais não são contagem de teoremas sobre o objetivo completo. Zero nova compilação Lean, zero execução/importação de um.py.

Fontes e recibos estão pinados em REGISTRO_RAIZ_078.json. O estatuto da fonte autoral anterior à revisão permanece histórico; esta revisão e a revisão independente são registros posteriores, não alterações daquela fonte.
