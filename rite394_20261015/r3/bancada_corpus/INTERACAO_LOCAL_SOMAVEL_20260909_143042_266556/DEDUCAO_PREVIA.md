# Dedução prévia — interação local somável na torre
[DERIVED — alvo de formalização; ainda sem recibo Lean] 09/09/2026.

O próximo objeto é efetivo: no Hilbert canônico H=TowerHilbert P e no fator M=theFactorObject P, seja B_j=X_j X_(j+1). Os operadores Pauli pertencem a M, são auto-adjuntos, têm quadrado I e comutam em sítios distintos. Logo B_j é auto-adjunto, B_j²=I e sua norma é no máximo 1, independentemente de j e do número de sítios.

Para coeficientes reais c_j absolutamente somáveis, definir V_N=Σ_(j<N)c_j B_j e V=Σ_j c_j B_j. Provar a partir dessas definições: auto-adjunticidade, pertinência ao fator, convergência em norma, norma de V limitada por Σ|c_j| e cauda ‖V−V_N‖≤Σ_(j≥N)|c_j|. A somabilidade é hipótese explícita; a conclusão de existência do limite não será campo de uma estrutura assumida.

O acoplamento de dois sítios deve ser atestado algebricamente. Para B=X_0X_1 e A=Y_0X_1, BA=iZ_0 e AB=−iZ_0. Assim ω(BA)−ω(AB)=2i(2P.w0−1), não nulo se P.w0≠1/2. B está no fator mas fora do centralizador nessas condições. No perfil tracial não se afirma essa exclusão. Além disso, o duplo comutador [[B,Z_0],Z_1]=−4Y_0Y_1 é não nulo: a ação gerada não preserva a álgebra de um sítio. Esta será a testemunha explícita de interação.

[OPEN — etapa seguinte] Construir o cociclo perturbativo não comutante na dinâmica modular α: u'_N(t)=i u_N(t)α_t(V_N), u_N(0)=I, e provar sua unitariedade, lei torcida e a estimativa ‖u_N(t)−u_M(t)‖≤|t|Σ_tail|c_j|. O ponto de partida finito é exp(it(H+V))exp(−itH), com H e V hermitianos. A estimativa uniforme no fundo H é o elo importante para remover o corte; não basta declarar um QuantumCompletion.

[INPUT/OPEN — interpretação física] O perfil P, os sítios, os coeficientes/couplings e sua somabilidade são dados. A realização de um cociclo não o identifica automaticamente com o fluxo modular de um novo estado físico; essa identificação necessita construção do estado e prova/hipótese correspondente. A atribuição a regiões físicas e a ligação do gerador ao tensor gravitacional não decorrem do nome. O limite ℓ¹ é controle em norma desta classe de interação limitada, não controle UV relativista, renormalização ou ausência de anomalias.

Originais e módulos congelados intocados. Só fontes novas e builds isolados nesta pasta. Nenhum um.py executado/importado.
